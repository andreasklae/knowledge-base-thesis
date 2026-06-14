---
type: literature
citekey: mayo2026gemma4tools
title: Gemma 4 tool calling with sandboxed filesystem and restricted Python interpreter
authors: [Mayo, Matthew]
year: 2026
venue: KDnuggets / Machine Learning Mastery
raw_path: raw/other/2026-05-mayo-gemma4-tool-calling-fs-python.md
related_concepts: [tools-component, deterministic-tools-hypothesis, framework-four-components, mcp-vs-skills]
related_work: [experiment-chess]
status: summarized
ingested: 2026-05-27
updated: 2026-05-27
---

# Mayo (2026) — Gemma 4 tool calling: filesystem + Python interpreter

## Summary

A KDnuggets tutorial that builds a from-scratch tool-calling loop with `gemma4:e2b` via Ollama, exposing two tools to the model: a sandboxed filesystem-listing function and a restricted Python interpreter. The companion repo is `mmmayo13/gemma_4_tool_calling`. The post is paired in the captured pack with Google's official `ai.google.dev` Gemma 4 tool-calling notebook, which uses Hugging Face `transformers` instead of Ollama; the two together specify Gemma 4's *actual* tool-call protocol (chat-template tokens, role conventions, thinking channel).

## Main claims

### 1. The orchestration loop is minimal

Two-pass synthesis: (a) query Ollama with the user prompt + tool registry as a JSON-schema array; (b) if the response carries a `tool_calls` block, dispatch each via a `TOOL_FUNCTIONS` dict, append the result back into the message history as `role: tool`, and re-query. The author explicitly notes that the loop is unchanged from the previous (web-API-only) tutorial — what changes is the tools and their blast radius. There is no framework here: it is the Ollama client, a dict, and a regex.

### 2. Tool-description prompt engineering matters

The filesystem tool's schema description ends with: *"Use this to inspect the environment before answering questions about local files."* This sentence pushes Gemma to call the tool on vague questions about "my files" instead of guessing. Tool design is part description, part operation ([[aizawa2025tools]]'s contract framing).

### 3. The empty-output branch in the interpreter matters more than it looks

`execute_python_code` captures stdout via `contextlib.redirect_stdout`. If the buffer is empty after `exec`, the function returns a *specific* error: `"Code executed successfully but produced no output. Use print() to return a value."` The author flags this as crucial: small models routinely write `x = sum(...)` and forget `print(x)`. Without the explicit retry-hint, the orchestration loop synthesises a final answer on an empty string and confidently invents a value.

### 4. Safety guards as part of the contract

`list_directory_contents` pins a `SAFE_BASE_DIR` and rejects any resolved path outside it. `execute_python_code` replaces `__builtins__` with a 30-entry whitelist so `open`, `eval`, `__import__` are not in scope; pre-imports `math` and `statistics` so the model doesn't fight import restrictions. Failures degrade to *useful* error strings (`"Access denied. The path '/etc' resolves outside..."`, `NameError: open`) — the model can read them and pivot.

### 5. Google's official notebook documents the chat-template surface

The paired Google notebook (`ai.google.dev/gemma/docs/capabilities/text/function-calling-gemma4`) shows Gemma 4's actual tool-call tokens:

```
<|tool_call>call:get_current_weather{location:<|"|>Tokyo, JP<|"|>}<tool_call|>
```

Tool responses are appended to history with `role: assistant`, attached as `tool_calls` and `tool_responses` fields *on the assistant turn itself* — **not** as a separate `role: tool` message (the OpenAI convention). Pydantic AI / OpenAI-compatible servers like vLLM that surface a `role: tool` message are bridging this gap; whether the bridge introduces errors is an open question. The `enable_thinking=True` mode emits a CoT channel before the tool call, parsed via `processor.parse_response(...)` into `role`/`thinking`/`content`/`tool_calls`.

The notebook also flags a sharp caveat: `transformers.utils.get_json_schema` auto-converts Python type hints to JSON schema, but for parameters typed as custom classes it returns `{"type": "object"}` with no inner properties. **Hand-written JSON schemas are required for nested objects.** This corresponds directly to a chess-experiment design choice — the four tool scripts are CLI-style with flat `--uci` / `--reasoning` flags, so auto-schema gives the right thing.

## Relevance to this thesis

Two channels of relevance to [[experiment-chess]]:

1. **The chess agent's `imagine_move` empty-args loop has the same shape as Mayo's empty-output-branch problem.** In Mayo's case, the model writes Python that produces no output, the tool returns a specific retry-hint, and the next attempt succeeds. In the chess case, the model calls `imagine_move` without `--uci`, the script returns a specific retry-hint (`"Missing --uci. Example: ..."`), but the next attempt sometimes *repeats the empty call*. The hint exists; what differs is whether the model can act on it. The Mayo pattern says the error-string approach is sound; the chess failure suggests something else is interfering — fresh-context per turn discarding the just-seen hint, or constrained decoding that would mechanically prevent the malformed call in the first place.

2. **The two-pass loop is far simpler than skillful-agent's per-turn fresh-context model.** This is not an argument that simpler is better — skillful-agent does load-bearing work (skill registry, disabled tools, context summary, SSE replay) that the Mayo loop doesn't. But it is a useful reference for what a Gemma-native harness *could* look like if rebuilt around constrained decoding and the model's actual chat template, rather than the pydantic-ai / OpenAI-compatible bridge.

## What this is NOT

A tutorial blog, not a paper. The author is explicit that the Python sandbox is a *learning* sandbox, not hardened — `().__class__.__mro__` introspection breaks out. The tools are toys, not production capabilities. The value is in the pattern, not the artefact.

## See also

- [[mirko2026gemma]] — paired in the same ingest session; the constrained-decoding (`NativeOutput`) finding complements Mayo's regex-parsing approach.
- [[aizawa2025tools]] — Anthropic's account of tool design as a contract; Mayo's empty-output-branch is a concrete instance.
- [[diary/experiment-chess/2026-05-27]] — the diary entry that triggered this ingest.
