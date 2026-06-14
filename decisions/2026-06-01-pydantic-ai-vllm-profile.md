---
type: decision
status: accepted
---

# 2026-06-01 — pydantic-ai OpenAIModelProfile for vLLM/Gemma 4

## Context

The chess experiment and skillful-agent server both use pydantic-ai's
`OpenAIProvider` to talk to vLLM, which serves Gemma 4 31B-it behind an
OpenAI-compatible HTTP interface. pydantic-ai's `OpenAIProvider` uses an
`OpenAIModelProfile` that defaults to OpenAI-API semantics. Two defaults
do not apply to vLLM/Gemma and cause intermittent failures.

**`openai_supports_strict_tool_definition=True` (default)**

With this flag set, pydantic-ai adds `"strict": true` inside every tool's
`function` object in the JSON request body:

```json
{"type": "function", "function": {"name": "run_script", "strict": true, ...}}
```

Gemma 4's vLLM chat template renders tool definitions in an entirely
different format — brace-key syntax, uppercase types (`STRING`, `ARRAY`),
`<|tool>declaration:name{...}<tool|>` delimiters, not JSON. The template
ignores the `strict` field during rendering. However, vLLM itself may
reject or mishandle the field depending on version. This was the most
likely cause of intermittent HTTP 400 responses with "malformed JSON"
messages that appeared in the chess experiment's agent logs.

**`openai_supports_tool_choice_required=True` (default)**

When pydantic-ai's `allow_text_output=False`, this flag causes it to send
`tool_choice: "required"`. vLLM's behaviour for `tool_choice: "required"`
with Gemma is undefined. vLLM is started with `--enable-auto-tool-choice`,
which is designed to handle `tool_choice: "auto"` — not `"required"`.

## Decision

On the `use_ex3` code path (and only on that path), construct the model
with an explicit profile that disables both flags:

```python
profile = OpenAIModelProfile(
    openai_supports_strict_tool_definition=False,
    openai_supports_tool_choice_required=False,
)
model = OpenAIChatModel(model_name, provider=provider, profile=profile)
```

Azure and OpenAI public API code paths pass `profile=None`, preserving
pydantic-ai's defaults for those providers (which do support `strict` and
`tool_choice: "required"`).

Applied in:
- `software/skillful-agent/server/app.py:_build_agent`
- `experiments/chess/backend/app/agent_player.py:_build_agent`

## Out of scope

**`openai_chat_thinking_field`**: Must be left as `None` (the default).
If set, pydantic-ai routes thinking tokens through a separate JSON field;
vLLM's template would re-inject them as a `<|channel>thought...<channel|>`
block in subsequent turns — violating Gemma 4's multi-turn rule that prior
turn thoughts must not appear in history. The template's `strip_thinking`
macro handles stripping automatically as long as thinking arrives as plain
`content`, which it does when this field is `None`. See
[[gemma4-vllm-pydantic-ai-integration]] §Multi-turn conversation and
thinking history.

**Sampling parameters**: Gemma 4's model card recommends `temperature: 1.0,
top_p: 0.95, top_k: 64`. The chess experiment currently uses pydantic-ai
defaults. Aligning with these values is deferred; it's not a
correctness issue, just a tuning question.

## Consequences

### Positive

- Eliminates the `"strict": true` source of intermittent HTTP 400 errors
  in vLLM/Gemma tool-call requests.
- `tool_choice: "auto"` aligns with how vLLM is configured
  (`--enable-auto-tool-choice`).
- Safe, non-breaking change: Azure and OpenAI paths are untouched.

### Negative

- If pydantic-ai adds support for strict tool definitions to `OpenAIProvider`
  in a way vLLM eventually honours, we'll need to revisit. Not a real concern
  for the current thesis timeline.

## References

- [[gemma4-vllm-pydantic-ai-integration]] — full write-up of the three-layer
  stack and all known integration issues.
- [[module-llm-server]] — vLLM launch flags; `--enable-auto-tool-choice` and
  `--tool-call-parser gemma4` are required.
- [[2026-05-26-stabilization]] — prior layer of the same root cause (stringly-
  typed args reaching Gemma; schema-layer contract tightening as the fix pattern).
- [[2026-05-27-run-script-args-list]] — same root cause in yet another layer
  (shell-string args fallback).
