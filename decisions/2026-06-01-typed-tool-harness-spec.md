---
type: decision
status: accepted
---

# Typed-Tool Harness: Skill Scripts as Native Tools

## Context

The current harness exposes skill scripts through a single generic dispatcher: `run_script(skill_name, filename, args: list[str])`. This requires the model to manually assemble an argument list from an untyped string array, bypasses the model's native tool-calling format (which it is fine-tuned for), and provides no pre-invocation argument validation.

The alternative: expose each non-private script as its own first-class tool with a JSON Schema derived from the script's argument declarations, advertise only the tools for currently-loaded skills, and keep the existing subprocess executor unchanged.

Constraint: no edits to any `SKILL.md` or script. Schemas are extracted statically; existing skills work unchanged or degrade gracefully to the generic `args[]` form.

## Decision

**Adopt the typed-tool contract.** Each skill's non-`_` scripts become individually named tools (`{skill}__{script_stem}`) with typed JSON Schemas extracted via static AST analysis. The progressive-disclosure invariant is preserved via pydantic-ai's `prepare` hook: all script-tools are registered at build time but hidden from the model until their skill is loaded.

### Architecture

**1. Static schema extraction (parse time)**

Extend `registry.py:_parse_skill` with a `ToolSpec` extraction pass over each non-`_` script. Tiered strategy, first match wins:

1. Typed `run(...)` / `main(...)` entrypoint with annotations → schema from signature + docstring.
2. argparse (primary): AST-walk for `ArgumentParser()` + `.add_argument(...)` calls. Covers the canonical format.
3. click / typer: optional later extractors, same output shape.
4. No extractable metadata (raw `sys.argv` indexing): emit `{ "args": { "type": "array", "items": { "type": "string" } } }` — namespaced generic tool, same behaviour as `run_script` today. Universality preserved.

Partial argparse parses (loops, non-literal kwargs) fall back to tier 4 and are flagged in logs. Never fail closed.

Each `ToolSpec` stores both the JSON Schema (for advertising) and an `argv_map` (for reconstruction): per argument, whether it is a flag (option string) or positional (index), plus `store_true` and `nargs` semantics.

argparse → JSON Schema mapping:

| argparse | JSON Schema |
|---|---|
| `"--move"` (option) | property `move`; marshalled as `["--move", value]` |
| positional `"path"` | property `path`; marshalled positionally by index |
| `type=str/int/float` | `"string"/"integer"/"number"` |
| `action="store_true"` | `"boolean"` (emit flag if true, omit if false) |
| `choices=[...]` | `"enum": [...]` |
| `nargs="+"`/`"*"`/N | `"type": "array"` |
| `required=True` | added to `required` |
| `default=...` | recorded in `argv_map`; property optional |
| `help="..."` | property `description` |

**2. Tool registration (build time)**

At `_build_agent`, register all script-tools upfront using `Tool.from_schema(...)` (available in pydantic-ai ≥ 1.73.0). Each tool gets a `prepare` closure:

```python
def prepare(ctx, tool_def):
    return tool_def if skill_name in ctx.deps.activated_skills else None
```

`prepare_tool_def` calls this per request step. Returning `None` omits the tool from that step's tool list — no runner rebuild, no routing shim.

**3. `activated_skills` lifecycle change**

Move `activated_skills` out of `_reset_run_state()`. It must persist across `run()` calls and reset only on `clear_conversation()`. This is the only structural change needed for the `prepare` gating to work across a multi-turn conversation.

Current behaviour: `_deps.activated_skills.clear()` in `_reset_run_state()` (`agent.py:422`) — clears between every `run()` call. Proposed: list persists until `clear_conversation()`.

**4. Invocation**

Per-tool dispatch calls the existing subprocess executor. Marshalling: named args → argv via `ToolSpec.argv_map`. Pre-invocation validation via `args_validator` (available in pydantic-ai ≥ 1.73.0) rejects malformed arguments before subprocess spawn — the concrete payoff of the typed schema. Tier-4 (generic `args[]`) tools cannot be validated this way; they behave exactly as `run_script` does now.

**5. Import-context fix**

The current `run_script` uses `cwd=None` (`skill_tools.py:474`) — a confirmed bug that breaks sibling imports (e.g. `import _eval` from within a script). Fix: run with `cwd=skill_root` and `PYTHONPATH` including both the skill root and `scripts/`. Prefer `-m scripts.<name>` when the skill implies package style (`scripts/__init__.py` exists or SKILL.md invocations use `-m`); otherwise direct path. Make this a per-skill executor option detected at parse time.

**6. `list_skill_files` tool (new)**

Add a standalone `list_skill_files(skill_name)` tool that returns the directory listing of `references/` (and `assets/` if useful). Enables progressive discovery of references without loading `use_skill` again.

Path safety requirement for `list_skill_files` and for any `read_reference` update: resolve the requested path and assert the real path is inside `<skill_dir>/references/` before reading. The current `read_reference` (`skill_tools.py:391`) prevents traversal via whitelist (filename must appear in the pre-enumerated `skill.references` list, which `_list_files` builds from real filesystem entries). This is adequate for current use but does not call `.resolve()` + assert containment — a stronger check required by the spec. Close the gap when implementing `list_skill_files`.

## Consequences

**Positive**
- Model uses native tool-calling format (fine-tuned for this) instead of assembling `args[]` strings.
- Pre-invocation validation: malformed calls fail before subprocess spawn, not inside it.
- Sibling import bug (`cwd=None`) fixed as a side effect of the import-context fix.
- No skill or script changes required. Tier-4 degradation preserves universality.

**Negative / risks**
- `activated_skills` lifecycle change is a behavioural break: skills loaded in turn N are now visible in turn N+1 (previously they were not). Downstream callers relying on per-run skill isolation must be audited.

**eX3 / vLLM operational note**

Activating a skill via `use_skill` changes the tool set sent to the model. On the eX3 path (vLLM `--tool-call-parser gemma4`, KV prefix cache enabled):

- Tool definitions are part of the prompt prefix vLLM caches. Adding a skill's tools on `use_skill` **busts the prefix cache from that point** — one-time latency hit per skill activation, not per turn. Acceptable cost; `use_skill` is already designed as a deliberate, infrequent act.
- **The Gemma tool-call parser needs explicit validation** for tolerance of a tool set that grows mid-conversation. Open-weight parsers are less robust to this than frontier models. Test before relying on it in [[experiment-chess]].

See [[gemma4-vllm-pydantic-ai-integration]] for the current tool-call stack and known parser issues.

## Related

- [[skills-component]] — progressive disclosure and typed-tool contract
- [[mcp-vs-skills]] — where this fits the integration spectrum
- [[gemma4-vllm-pydantic-ai-integration]] — eX3 parser consequences
- [[experiment-chess]] — first consumer of the typed-tool contract
