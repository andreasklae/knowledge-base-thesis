# Ideas

## Harness that auto-wraps bundled skill scripts as lazy-revealed typed tools (2026-06-01)

Design proposal: a harness that takes a skill in the standard format (SKILL.md + scripts/) but, on skill-load, introspects each script's Pydantic-typed entrypoint and registers it as a first-class tool — with a full JSON Schema, per-field descriptions from the docstring, and runtime validation. Tools from unloaded skills are not listed in the model's context; loading the skill triggers a `list_changed` notification and the tool schemas appear. 

This resolves the progressive-disclosure vs. typed-schema tension: the model gets lazy loading (context economics of skills) and the structured invocation format it is fine-tuned for. Schema contract lives in the script's Pydantic signature — single source of truth for both model-facing schema and runtime validation.

Works cleanly for stateless analysis tools (take a position, return analysis); requires process-lifecycle management for stateful tools (persistent servers, not subprocesses). The endpoint: "MCP host whose packaging format is a skill." See [[capability-delivery-dimensions]] and [[mcp-vs-skills]] for context.

Security note: auto-publishing executable tools on skill-load is a trust event. Treat like a plugin install: signed source, sandboxed execution at the process level.

## Chess agent: positional knowledge, calculation, and recipes backlog (2026-06-15)

Deep future-work backlog for the chess agent's next improvement cycle —
playing principles, per-move pros/cons, strengths/weaknesses lists for both
sides, calculation/look-ahead and opponent prediction, a list-legal-moves-
for-a-piece tool, middlegame mate awareness (offensive AND defensive),
scenario recipes (pawn promotion etc.) in a rich-but-scoped wiki, tactical
motifs (pins/skewers/forks), opponent-move narration, and the unsolved
"blunders despite warnings + gate" problem (promotes into immediate
capture, anchors on headline material gain). Full doc:
[chess-future-work-positional-and-calculation](chess-future-work-positional-and-calculation.md).
Captured from user notes after the PR2 smoke batch. NOT yet implemented; no
chess-wiki/agent changes until scheduled.
