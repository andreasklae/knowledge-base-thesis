---
source_type: web-article
author: Matthew Mayo (KDnuggets / Machine Learning Mastery)
title: Gemma 4 tool calling with sandboxed filesystem and restricted Python interpreter
url_note: User-pasted; KDnuggets/Machine Learning Mastery article. Companion code repo: github.com/mmmayo13/gemma_4_tool_calling
captured: 2026-05-27
captured_via: pasted into /kb session by user
---

# Gemma 4 + filesystem + python interpreter (Mayo, KDnuggets)

User-pasted tutorial. The model is `gemma4:e2b` via Ollama. The pattern:

## Orchestration loop (two-pass synthesis)

1. Query Ollama with user prompt + tool registry (JSON schema array).
2. If response has `tool_calls`, dispatch each via `TOOL_FUNCTIONS` dict, append result as `role: tool` message.
3. Re-query Ollama with enriched history. Model produces grounded final answer.

Same pattern as a previous tutorial (weather/news APIs). The architectural point: the loop generalizes — what changes is the tools and their blast radius.

## Tool 1: `list_directory_contents`

Confined to a `SAFE_BASE_DIR` (set to `os.getcwd()` at script start). Path-traversal guard:

```python
requested = os.path.abspath(os.path.join(SAFE_BASE_DIR, path))
if not (requested == SAFE_BASE_DIR or requested.startswith(SAFE_BASE_DIR + os.sep)):
    return f"Error: Access denied. The path '{path}' resolves outside the permitted workspace..."
```

Returns plain-English structured listing with `[DIR]` / `[FILE]` markers and byte sizes. Schema description does light prompt engineering: *"Use this to inspect the environment before answering questions about local files."*

## Tool 2: `execute_python_code`

`exec()` with stripped builtins. Whitelist of ~30 safe builtins (no `open`, `eval`, `exec`, `__import__`). Pre-imports `math`, `statistics` into restricted globals so the model doesn't fight `__import__`. Stdout captured via `contextlib.redirect_stdout`.

**Empty-output branch matters:** if buffer is empty, returns `"Code executed successfully but produced no output. Use print() to return a value."` Small models routinely write `x = sum(...)` and forget `print(x)`; this gives the loop a chance to retry instead of synthesizing on an empty string.

Explicitly a learning sandbox, not hardened — author notes `().__class__.__mro__` introspection breakouts.

## CLI formatting note

Tool args are flattened/truncated for display (newlines → `\n`, 60-char cap); full string still passed to the function.

## Worked examples

- "What scripts are in my folder and which processes CSVs?" → 1 tool call, grounded inference on filenames.
- "Std dev of [12,18,...] to 4 dp?" → model writes `statistics.stdev(...)`, prints, reports.
- "Total size in KB of files here?" → uses **both tools in sequence**: list_directory → execute_python_code with the byte sizes from the listing.

Safety check: asking for `/etc` produces denial; `open('/etc/passwd')` produces `NameError`. Failures degrade to useful error strings.

## Bonus: Google's official Gemma 4 tool-calling notebook

The user's paste also includes the Google ai.google.dev notebook for Gemma 4 tool calling with the `transformers` library (not Ollama). Key bits:

- Tools passed via `processor.apply_chat_template(message, tools=[...])`. Tools can be JSON schemas or raw Python functions (auto-schema via `transformers.utils.get_json_schema`).
- Gemma 4 tool-call syntax in the chat template:
  ```
  <|tool_call>call:get_current_weather{location:<|"|>Tokyo, JP<|"|>}<tool_call|>
  ```
- Tool response is appended to history with `role: assistant`, fields `tool_calls` and `tool_responses` (note: not the OpenAI `role: tool` convention — Gemma's chat template expects them attached to the assistant turn).
- `enable_thinking=True` enables a chain-of-thought channel before the tool call. Parsed with `processor.parse_response(output)` into `role`/`thinking`/`content`/`tool_calls`.
- Caveat: auto-schema for parameters typed as custom classes returns `"type": "object"` with no inner properties. For nested objects, write the JSON schema by hand.

---

## Why this is in raw/other/

Same context as [[2026-05-mirko-gemma-ollama-pydantic-recipe]]: user is questioning whether skillful-agent is the right harness for Gemma 4 in [[experiment-chess]]. This article and the Google notebook together sketch what a from-scratch Gemma 4 tool-calling loop looks like — minimal, two-pass, JSON-schema tools, with the option of `NativeOutput`-style constrained decoding for argument reliability.
