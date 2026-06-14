---
type: concept
sources: [anthropic2024mcp, zhang2025, fielding2000, aizawa2025tools, weber2024taxonomy]
related_concepts: [tools-component, skills-component, data-component, framework-four-components, capability-delivery-dimensions, context-engineering]
related_work: [experiment-riksantikvaren, experiment-wcag-skill, experiment-chess]
status: draft
updated: 2026-06-01
---

# MCP vs. Skills: The Integration Spectrum

The same agent capability can be exposed as a vendor-published interface (Model Context Protocol [[anthropic2024mcp]]) or as a lightweight developer-owned module (a skill file [[zhang2025]]). The choice is structural, not technical. For a fuller decomposition of the axes involved, see [[capability-delivery-dimensions]].

## What each one is

**MCP** is a transport protocol. Its core loop: the host calls `tools/list` at runtime, receives JSON-Schema tool definitions, injects them into the model API call, intercepts the model's `tool_use` block, translates it into a `tools/call` JSON-RPC request to the server, and feeds the result back as a `tool_result`. The model layer is *identical* to native tool calling — the model sees schemas and emits structured calls; it is never in "MCP mode." MCP is a layer between the *client and the tool provider*, not between the model and the client.

**Native tools** (Pydantic AI style) are the in-process version: same schema format, same model mechanics, but tool execution is a direct function call in the same address space, no process boundary, no serialization.

**Skills** are not a calling protocol at all — they are a *folder*: a `SKILL.md` (instructions + context) plus optional bundled `scripts/`. There is no `skills/list`, no `skills/call`. The model interacts with a skill using an ordinary tool it already has — usually bash. Discovery is progressive: only the skill's name + description sit in context initially (cheap); the model reads `SKILL.md` when it decides to use the skill, and only then does heavier content enter the context.

The three mechanisms at a glance:

| | Discovery | Execution | Boundary | Context cost |
|---|---|---|---|---|
| Native tools | dev-time, from code | direct function call | none (in-process) | eager: all schemas always resident |
| MCP | runtime `tools/list` | JSON-RPC `tools/call` | process / network | eager: all schemas always resident |
| Skills | name+desc in context, then read `SKILL.md` | runs via an existing tool (bash) | filesystem + subprocess | progressive: detail enters only on use |

**The token-economics difference is often the real deciding factor.** MCP front-loads all tool definitions into the model's context; a skill front-loads almost nothing and pulls in detail on demand. For a large capability surface, that gap is significant.

## The two ends of the spectrum

- **MCP (the API model).** A vendor publishes a stable interface; multiple consumers connect to a single source of truth; updates propagate uniformly. Paid for in server infrastructure, versioning discipline, and slower iteration.
- **Skills (the local module model).** A markdown file plus scripts dropped into a folder. Trivial to author and modify. Paid for in absent shared truth and the corresponding risk of drift across deployments.

## When skills win on simplicity — and when they don't

Skills shine in a trusted coding/agentic setup with a sandbox: write the bash harness once, extend forever by dropping in folders, no per-capability boilerplate. That is a genuine architectural win.

But skills-via-bash quietly assume three things:

1. **You are handing the model a shell.** A bash tool is arbitrary code execution — the model can do *anything* on that machine. A native/MCP tool is a keyhole: the model can call `get_weather`, it cannot `rm -rf`. In anything multi-tenant or user-facing, deliberately *not* granting a shell is the point.
2. **An execution environment exists.** A consumer app or website backend often cannot run subprocesses. An MCP server can run somewhere else and expose a thin HTTP surface.
3. **Stateless is acceptable.** A script is a cold start every call. MCP servers can persist: hold a DB connection, an auth session, a live browser across ten steps.

Rough rule: **trusted sandbox + procedural logic → skills win on simplicity. Untrusted surface, no execution env, or stateful connections → MCP. Tight parameter reasoning the model should chain → native tool.**

## The "ship with the skill" insight

A skill is `SKILL.md` *plus* a `scripts/` folder, and the scripts are first-class members of the package. "Ship the tool with the skill" is not a workaround — it is the skill model working as designed. This resolves the coupling problem: if `SKILL.md` says "call `visualize_threats()`" and that function lives on a board server, you've welded your playing-knowledge package to a specific engine's API. Bundle the helper into the skill and the package is self-contained and portable.

The decisive insight: **detection and tactics are deterministic, not model-judgment.** Opening identification is an ECO-book lookup. Fork/pin detection is a position scan. Mate-in-N is search. Letting the LLM "recognize the Najdorf from having read about it" is strictly worse than `identify_opening(fen)` hitting a deterministic book — slower, probabilistic, and wrong under pressure. The skill container is the right place for these helper scripts precisely because it bundles deterministic tools *and* strategic prose (for the genuinely fuzzy judgment calls) in one package.

The invariant that makes this hold: **skill scripts must be pure functions of a position.** They take authoritative state from the server, compute over it, return analysis, and hold no game state of their own. The instant a skill script starts tracking its own state you have two sources of truth. Server = mutable authority; skill scripts = stateless read-only analysis over that authority.

## The "both" case: typed tools for state + skill for knowledge

The mature architecture is not a pick between MCP and skills — it's a split along the state/knowledge line:

- **Typed tools (native or MCP) for anything that touches authoritative mutable state.** Legality, current position, move application — validated, stateful, no model hallucination risk on the rules.
- **Skill for theory, playbooks, and deterministic analysis helpers.** Opening ID, tactical-motif detection, threat visualization — bundled scripts + strategic prose.

The typed-tool concern is strongest for the move/state layer and weakest for the analysis layer. Draw the boundary there.

## Typed-tool synthesis: lazy-revealed schemas from a bundled skill

This idea has been formalised into a full decision record: [[2026-06-01-typed-tool-harness-spec]].

The core synthesis: a harness that auto-wraps each bundled script as a first-class tool — JSON Schema extracted via static AST analysis of argparse declarations — with those tools hidden from the model until the skill is loaded. This resolves the progressive-disclosure vs. typed-schema tension without a runner rebuild: all tools are registered at build time with a `prepare` hook that gates on whether the skill is in `activated_skills`. The tool list visible to the model expands when the skill activates, contracts when the conversation resets.

This is the framework-native path in pydantic-ai (confirmed in ≥ 1.73.0 via `Tool.from_schema` + `prepare`). Runtime tool-set growth is a supported move — pydantic-ai's `prepare_tool_def` is called per step. On the vLLM / Gemma 4 path, growing the tool set busts the KV prefix cache once per `use_skill` activation; see [[2026-06-01-typed-tool-harness-spec]] §Consequences for the eX3 operational note.

## Historical analogues

The same tension played out with SOAP/WS-* vs. REST (heavyweight protocol vs. lighter deployment-context winner), and again with LSP (Language Server Protocol), which MCP is consciously modelled on. LSP solved "every editor reimplementing every language's analysis" by standardising the editor↔backend conversation. Its history — what consolidated, what got over-engineered, how capabilities are negotiated — is the single most transferable case study, and it's not analogy: it's the same architectural move one domain earlier.

[[fielding2000]] is the canonical REST reference. REST constraints (client-server, stateless, cache, uniform interface, layered system, code-on-demand) map near-directly onto MCP primitives. The MCP-skills choice is the agent-era replay of REST-vs-RPC, with skills playing the lighter-weight role.

## Where it surfaces in experiments

- [[experiment-riksantikvaren]] — the Askeladden integration is closer to MCP (single authoritative source, broadly useful) but the prompts and retrieval glue around it are skill-shaped (one team, local control).
- [[experiment-wcag-skill]] — a WCAG audit skill is the canonical skill-shaped case: a small team, a specific task, drift acceptable because the team controls the deployments.
- [[experiment-chess]] — the chess app design reasoning worked out the state/knowledge split concretely: typed tools for the rules engine, skill for theory + deterministic analysis helpers.

## Authoring discipline cuts across both ends

The integration choice is one axis; tool/skill *quality* is orthogonal. [[aizawa2025tools]]'s prototype-evaluate-iterate loop and authoring principles (namespacing, response-format enums, prompt-engineered errors, semantic identifiers) apply on both ends of the spectrum. [[weber2024taxonomy]]'s LLM-component taxonomy provides a 13-dimension classification that applies whether the underlying capability is exposed as MCP, as a skill, or as inline tooling.

---
*Framing drawn from `../../manuscript-notes/essay-pointer.md` (Essay/essay.tex §2.7) and `../../raw/discussions/Claude Conversation on tools, mcp and skills.md`.*
