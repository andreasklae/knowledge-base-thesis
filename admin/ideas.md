# Ideas

## Harness that auto-wraps bundled skill scripts as lazy-revealed typed tools (2026-06-01)

Design proposal: a harness that takes a skill in the standard format (SKILL.md + scripts/) but, on skill-load, introspects each script's Pydantic-typed entrypoint and registers it as a first-class tool — with a full JSON Schema, per-field descriptions from the docstring, and runtime validation. Tools from unloaded skills are not listed in the model's context; loading the skill triggers a `list_changed` notification and the tool schemas appear. 

This resolves the progressive-disclosure vs. typed-schema tension: the model gets lazy loading (context economics of skills) and the structured invocation format it is fine-tuned for. Schema contract lives in the script's Pydantic signature — single source of truth for both model-facing schema and runtime validation.

Works cleanly for stateless analysis tools (take a position, return analysis); requires process-lifecycle management for stateful tools (persistent servers, not subprocesses). The endpoint: "MCP host whose packaging format is a skill." See [[capability-delivery-dimensions]] and [[mcp-vs-skills]] for context.

Security note: auto-publishing executable tools on skill-load is a trust event. Treat like a plugin install: signed source, sandboxed execution at the process level.
