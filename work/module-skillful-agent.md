---
type: module
status: in-progress
related_concepts: [skills-component, capability-delivery-dimensions, mcp-vs-skills, context-engineering, gemma4-vllm-pydantic-ai-integration]
related_work: [experiment-chess, module-llm-server]
sources: [zhang2025, rajasekaran2025, anthropic2024mcp, karpathy2025wiki]
updated: 2026-06-02
---

# module-skillful-agent

The **agent harness** the thesis's experiments run on: a pydantic-ai-based SDK
for building agents with **progressive skill disclosure**. The agent discovers
skills from a directory, loads a skill's full instructions on demand
(`use_skill`), and uses the skill's bundled resources — scripts (exposed as
typed tools) and reference docs. It is the concrete instantiation of the
framework's [[skills-component]]: skills as packaged, lazily-revealed
procedural context ([[zhang2025]], [[rajasekaran2025]]).

Lives outside this knowledge base at `software/skillful-agent/` (its own git
repo, `github.com/andreasklae/skillful-agent`). Experiments depend on it as a
git-pinned package (`skill-agent`). The repo's own operating manual is
`software/skillful-agent/CLAUDE.md` — read that before editing the SDK; this
page is the thesis-side record of what it is and why it matters.

## Why it exists in the thesis

The thesis argues productivity is an infrastructure problem
([[agent-infrastructure-vs-capability]]). This SDK is the infrastructure under
test: it holds the model fixed and varies the *workspace, tools, skills, and
data* around it ([[framework-four-components]]). Every experiment that needs an
agent (not just raw inference) runs on this harness, so its design choices —
what the tool surface is, how skills are disclosed, how context is managed —
are part of the experimental apparatus, not incidental plumbing.

It also sits at a specific point on the [[capability-delivery-dimensions]]
axes: skills are local modules (not a vendor-published interface like MCP —
see [[mcp-vs-skills]]), disclosed just-in-time, with scripts as the
deterministic tool layer.

## Architecture (essentials)

Full detail is in `software/skillful-agent/CLAUDE.md`; the load-bearing facts
for the thesis:

- **Progressive disclosure.** The system prompt lists only skill *names +
  descriptions*. A skill's full `SKILL.md` body is loaded only when the agent
  calls `use_skill`. This is the context-economics core of the
  [[skills-component]] and [[context-engineering]].
- **Skill scripts as typed tools.** There is **no generic `run_script` tool**
  (removed 2026-06). Each `scripts/*.py` in a skill is registered as a typed
  pydantic-ai tool named `<skill>__<script>`, with a JSON schema extracted
  statically from the script (typed `main`/`run` → argparse → generic
  `args: list[str]` fallback). A `prepare` gate hides each script tool until
  its owning skill is active, so `use_skill` reveals the skill's tools without
  a runner rebuild. This puts the model in native tool-calling format — the
  format it is fine-tuned for — rather than an untyped dispatcher.
- **`read_reference`** reads a skill's `references/` docs **by path**
  (subfolders supported, jailed to `references/`). This is what makes a
  bundled knowledge wiki navigable — see the chess agent's wiki in
  [[2026-06-02-chess-agent-wiki-architecture]].
- **Configurable tool surface.** `AgentConfig.disabled_tools` and
  `disable_native_skills` let a consumer narrow the surface; the chess agent
  uses this heavily (see [[2026-05-26-stabilization]]).
- **Context management.** Auto-compression and explicit
  compress/retrieve tools; a typed `AgentContextOverflowError`. The chess
  baseline deliberately runs **per-turn fresh context** instead
  ([[2026-05-24-per-turn-fresh-context]]).
- **Threads + subagents.** Named-thread message channels and `spawn_agent`
  for inter-agent communication (unused by chess; relevant to multi-agent
  framings, [[krishnan2025multiagent]]).
- **Server.** A FastAPI app (`server/`) exposes the agent over HTTP/SSE.

## How experiments consume it

Two integration shapes, both documented in [[module-llm-server]] §"Downstream
integration":

1. **Via the HTTP server** (`software/skillful-agent/server/`) — configured by
   `.env`, backend-selection priority `SKILL_AGENT_EX3_BASE_URL` → Azure →
   OpenAI.
2. **As a library** — the chess experiment imports `skill-agent` as a git
   dependency but **builds its own `Agent`** in
   `experiments/chess/backend/app/agent_player.py:_build_agent`, replicating
   the backend-selection logic locally. The git pin in the experiment's
   `pyproject.toml`/`uv.lock` is the exact SDK version a batch ran against —
   part of experimental provenance alongside `skill_repo_sha`.

The harness runs Gemma 4 31B-it on eX3 via vLLM through pydantic-ai's
OpenAI-compatible bridge; the three-layer tool-call stack and its known issues
are in [[gemma4-vllm-pydantic-ai-integration]].

## Status / evolution

In active development; the chess experiment is its primary driver and most of
the recent changes were made to support it. Notable changes (newest first):

- **2026-06**: `run_script` removed in favour of per-script typed tools
  (prepare-gated); `read_reference` reworked to be path-based; system prompt
  slimmed. See [[diary/experiment-chess/2026-06-02]] and
  [[2026-06-02-chess-agent-wiki-architecture]].
- **2026-05**: `disabled_tools` / `disable_native_skills` added
  ([[2026-05-26-stabilization]]); `run_script` args switched to `list[str]`
  ([[2026-05-27-run-script-args-list]]); typed `AgentContextOverflowError`
  ([[2026-05-24-per-turn-fresh-context]]); pydantic-ai vLLM/Gemma profile
  fix applied in the server ([[2026-06-01-pydantic-ai-vllm-profile]]).

Because the SDK is shared apparatus, **any change is a methodology event for
every experiment that runs on it** — record it, and note the new git pin in
the consuming experiment when resyncing.

## Files and paths

- **SDK repo**: `software/skillful-agent/` (`github.com/andreasklae/skillful-agent`)
- **Operating manual**: `software/skillful-agent/CLAUDE.md`
- **Core**: `skill_agent/agent.py`, `skill_tools.py`, `registry.py`,
  `_schema_extractor.py`, `context_tools.py`, `thread_tools.py`,
  `system_prompt.md`
- **Server**: `software/skillful-agent/server/`
- **Bundled native skills**: `software/skillful-agent/native-skills/`
  (`web-search`, `learner`)
