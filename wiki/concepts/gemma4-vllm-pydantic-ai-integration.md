---
type: concept
sources: []
related_concepts: [capability-delivery-dimensions, mcp-vs-skills, ex3]
related_work: [module-llm-server, experiment-chess]
status: stable
updated: 2026-06-10
---

# Gemma 4 + vLLM + pydantic-ai: Tool-Call Integration

How the three layers fit together when the chess experiment (and any other skillful-agent consumer) runs tool-calling against Gemma 4 31B-it on eX3.

---

## The three-layer stack

```
pydantic-ai (skillful-agent SDK)
    ↓  OpenAI Chat Completions API request  (JSON, with tools[])
vLLM  (OpenAI-compatible HTTP server)
    ↓  chat template renders request → token ids
Gemma 4 31B-it  (model weights)
    ↑  generates tokens
vLLM  (parses Gemma's output → OpenAI-format response JSON)
    ↑  OpenAI Chat Completions API response
pydantic-ai
```

pydantic-ai never speaks to Gemma directly. It speaks OpenAI-format JSON to vLLM's compatibility layer. vLLM translates that into Gemma's native token format using a Jinja2 chat template baked into the model repository, and translates Gemma's output back to OpenAI format before returning the response.

---

## Gemma 4's native tool format

Gemma 4 was trained on a custom structured format, **not JSON**. The chat template renders tool definitions inside `<|tool>...<tool|>` delimiters using a brace-key syntax:

```
<|tool>declaration:run_script{
  description:"Run a Python script bundled with a skill.",
  parameters:{
    properties:{
      skill_name:{description:"...",type:"STRING"},
      filename:{description:"...",type:"STRING"},
      args:{items:{type:"STRING"},type:"ARRAY"}
    },
    required:["skill_name","filename","args"],
    type:"OBJECT"
  }
}<tool|>
```

Key differences from OpenAI JSON:
- Types are **uppercase** (`STRING`, `ARRAY`, `OBJECT`) not lowercase
- No JSON quotation marks on keys — bare key names with `:` separator
- String values use `<|"|>...<|"|>` quoting tokens, not double quotes
- Tool definitions are wrapped in `<|tool>...<tool|>` not a `tools` JSON array

Tool calls from the model come back in a matching format:
```
<|tool_call>call:run_script{skill_name:"chess",filename:"make_move.py",args:["e2e4","Pushed pawn"]}<tool_call|>
```

Tool results are injected as:
```
<|tool_response>response:run_script{value:"..."}<tool_response|>
```

**vLLM handles all of this translation transparently** — pydantic-ai sends standard OpenAI format in both directions and never sees the native tokens.

---

## vLLM tool-call parser: must use `gemma4`

vLLM must be started with both:
```bash
--enable-auto-tool-choice --tool-call-parser gemma4
```

Without `--enable-auto-tool-choice`: vLLM returns HTTP 400 for any request with `tool_choice: auto`.

Without `--tool-call-parser gemma4` (e.g. using `pythonic` instead): Gemma's tool-call tokens leak into the `content` field of the response as raw text rather than being parsed into `tool_calls`. This was vLLM issue #39043. The `gemma4` parser knows how to split `<|tool_call>...<tool_call|>` out of the content stream.

See [[module-llm-server]] for the full verified launch flags.

---

## Thinking / chain-of-thought channel

Gemma 4 wraps its chain-of-thought in:
```
<|channel>thought
[reasoning text]
<channel|>
```

**Template-level stripping:** The vLLM chat template includes a `strip_thinking` macro that removes this channel block from any assistant message `content` field before re-injecting it into conversation history. This means thinking content does **not** accumulate in subsequent turns — the template strips it automatically when building the next request.

**Disabled thinking still emits an empty channel block.** When `enable_thinking=False` (the default when `<|think|>` is absent from the system prompt), the template pre-emits:
```
<|turn>model
<|channel>thought
<channel|>
```
before generation. The model still produces the channel framing with an empty thought body. This is by design, not a bug.

**pydantic-ai side:** With `openai_chat_thinking_field=None` (the default for `OpenAIProvider`), pydantic-ai treats thinking tokens as plain text content. The tokens arrive as `TextDeltaEvent` chunks in the stream. The chess experiment accumulates them in `thinking_buf` and strips `<|channel>thought` / `<channel|>` markers with a regex before emitting a `thinking` event. vLLM's template separately strips thinking from history, so the two stripping operations don't interfere.

---

## pydantic-ai profile mismatches (known issues)

When using `OpenAIProvider(base_url=..., api_key="dummy")` without a custom profile, pydantic-ai applies its default OpenAI profile. Two fields cause problems with vLLM/Gemma:

### `openai_supports_strict_tool_definition: True` (default)
pydantic-ai sends `"strict": true` inside every tool's `function` definition:
```json
{"type": "function", "function": {"name": "...", "strict": true, ...}}
```
Gemma's chat template does not know about `strict` — it's ignored during rendering. But **vLLM itself may reject or mishandle** the field depending on version. This is a likely contributor to intermittent HTTP 400 responses with malformed JSON error messages.

**Fix:** Set `openai_supports_strict_tool_definition=False` in the profile.

### `openai_supports_tool_choice_required: True` (default)
When `allow_text_output=False`, pydantic-ai sends `tool_choice: "required"`. vLLM may not honour this for Gemma — behavior depends on vLLM version. Setting it to `False` makes pydantic-ai send `tool_choice: "auto"` instead, which is what `--enable-auto-tool-choice` is designed to handle.

**Fix:** Set `openai_supports_tool_choice_required=False` in the profile.

### Applying the fixes — in `agent_player.py:_build_agent`

```python
from pydantic_ai.models.openai import OpenAIChatModel, OpenAIModelProfile

profile = OpenAIModelProfile(
    openai_supports_strict_tool_definition=False,
    openai_supports_tool_choice_required=False,
)
model = OpenAIChatModel(model_name, provider=provider, profile=profile)
```

This is a safe, non-breaking change. It does not affect Azure or OpenAI public API paths (those use a different provider/model construction).

**Status as of 2026-06-01:** Applied in both `experiments/chess/backend/app/agent_player.py:_build_agent` and `software/skillful-agent/server/app.py:_build_agent`. The profile is only set on the `ex3_base_url` branch; Azure and OpenAI paths use `profile=None` (default).

---

## Multi-turn conversation and thinking history

From the Gemma 4 model card (best practices, section 3):

> In multi-turn conversations, the historical model output should only include the final response. Thoughts from previous model turns must **not** be added before the next user turn begins.

vLLM's chat template enforces this via the `strip_thinking` macro applied to all `role: model` messages in history. As long as pydantic-ai sends thinking as part of `content` (not in a separate `reasoning` field), the template strips it correctly.

If `openai_chat_thinking_field` were set in the profile (e.g. to `"reasoning"`), pydantic-ai would send thinking back as a separate field and the template would re-inject it as a channel block — violating the multi-turn rule. **Do not set `openai_chat_thinking_field`** for Gemma 4 on vLLM.

---

## Recommended sampling parameters (from model card)

```
temperature: 1.0
top_p: 0.95
top_k: 64
```

The chess experiment currently uses pydantic-ai's defaults (temperature not explicitly set). If Gemma's outputs feel overconfident or repetitive, aligning with these values is the first thing to try.

---

## Summary: what works, what doesn't, what's pending

| | Status | Notes |
|---|---|---|
| Tool calling via vLLM OpenAI-compat | ✅ Works | Requires `--tool-call-parser gemma4` |
| Thinking channel stripping in history | ✅ Works | Template handles it; harness has belt-and-suspenders regex |
| `strict: true` in tool defs | ✅ Fixed | `openai_supports_strict_tool_definition=False` applied in both `_build_agent` functions |
| `tool_choice: required` | ✅ Fixed | `openai_supports_tool_choice_required=False` applied in both `_build_agent` functions |
| `openai_chat_thinking_field` | ✅ Leave as None | Setting it breaks multi-turn thinking-stripping |
| Sampling params | ⚠️ Not aligned | Model card recommends temp=1.0, top_p=0.95, top_k=64 |

---

## Pitfall: history processors silently drop the system prompt (fixed 2026-06-10)

pydantic-ai attaches the static system prompt only to the first request of
an **empty** history; when `message_history` is non-empty it assumes the
history already carries it. A history processor that rebuilds the message
list from scratch must therefore re-inject a `SystemPromptPart` itself —
otherwise every turn after the first reaches the model with **no system
prompt at all** (no skill list, no harness rules). The chess experiment's
turn-memory injection had exactly this bug from 2026-05-26 to 2026-06-10;
it was found with a FunctionModel probe and is regression-tested in the
chess backend (`test_turn_memory.py::TestSystemPromptRegression`). See
[[2026-06-10-structured-turn-memory]].
