---
type: concept
sources: [aizawa2025tools, anthropic2024mcp, martin2026managed, fielding2000, weber2024taxonomy, rajasekaran2025, mirko2026gemma, mayo2026gemma4tools]
related_concepts: [framework-four-components, deterministic-tools-hypothesis, calibration-thread, mcp-vs-skills, skills-component, context-engineering]
related_work: [experiment-riksantikvaren, experiment-math, experiment-vision-landmarks]
status: draft
updated: 2026-05-27
---

# Tools Component

Tools are the agent's reach into external systems. A tool is a deterministic operation the agent calls but does not perform itself: an API request, a database query, a shell command, a calculator.

## What a tool actually is

Two artefacts: the operation (what the tool does when invoked) and the description (what the agent reads to decide whether to call it and how). Both are part of the tool. [[aizawa2025tools]] report that small refinements to tool descriptions produced state-of-the-art performance on SWE-bench Verified, and propose a prototype-evaluate-collaborate loop in which agents help refine the tools they use. The description is engineering material, not packaging.

Aizawa's central framing — *"tools are a new kind of software which reflects a contract between deterministic systems and non-deterministic agents"* — names what distinguishes tool design from API design: the caller is fallible and probabilistic, so design has to absorb that. The empirical anchor: Anthropic's internal Slack tools moved from 67.4% → 80.1% accuracy on held-out evals and Asana from 79.6% → 85.7% under Claude-assisted tool optimisation. Same model, same protocol — only the tools changed.

## Protocol heritage

[[fielding2000]] derives REST as a set of architectural constraints (client-server, stateless, cache, uniform interface, layered system, code-on-demand) and shows each constraint induces a property and accepts a trade-off. [[anthropic2024mcp]] is the explicit re-application of those constraints to agent-tool integration 24 years later: client-server architecture, stateless JSON-RPC requests, a uniform interface (prompts/resources/tools/roots/sampling), and layered proxyability. Reading MCP as REST-for-agents makes Fielding's interface constraints — *identification of resources, manipulation through representations, self-descriptive messages, hypermedia as the engine of application state* — directly applicable as a design checklist for tool surfaces.

## Distinction from skills

Tools reach into external systems; [[skills-component]] is procedural knowledge for using them. A tool description rich enough to teach use is approaching a skill; a skill that calls a deterministic script is also a tool with documentation. The framework expects overlap. The integration-spectrum question — when to expose capability as a vendor-published interface (MCP) versus a lightweight developer-owned module (a skill) — is taken up in [[mcp-vs-skills]].

## Calibration role

Tools verify by execution. The output of a tool call is external state the agent's belief can be checked against, or in the limit case (see [[deterministic-tools-hypothesis]]) replaced by. This is the cleanest case of the verification mechanism in [[calibration-thread]].

## Where tools are probed

- [[experiment-riksantikvaren]] — the Askeladden API as a tool for grounding heritage answers.
- [[experiment-math]] — a coding sandbox as a tool for turning reasoning into executable verification.
- [[experiment-vision-landmarks]] — GPS reverse-geocoding and landmark-lookup tools to constrain the candidate set against prototypicality bias; see [[prototypicality-bias]].
- [[experiment-chess]] — four perception/action scripts (`show_position`, `list_legal_moves`, `imagine_move`, `make_move`) called via `run_script` with a typed `args: list[str]` contract. Surfaces two distinct contract-design patterns:

  - **Contract-at-the-transport-layer** ([[2026-05-27-run-script-args-list]]): the harness's original `shlex.split(args_string)` mangled free-text reasoning containing apostrophes; the typed `list[str]` schema eliminates the shell-parse step entirely. Pydantic-ai's schema becomes the contract — calls that don't match the shape are rejected before any code runs.
  - **Contract-at-the-mutation-boundary** ([[2026-05-27-single-writer-move-contract]]): when `make_move` *also pushed* to the live board via its HTTP side-channel, there were two writers to `game.board` (the bot loop and the agent endpoint). Race surfaces, double-push bugs, and "phantom move on the board" symptoms followed. The fix: the endpoint becomes a pure validator; only the bot loop pushes. The tool returns a result; the *caller* of `get_move()` decides what to do with it. Players are uniform — they emit moves, the loop owns the board.

  Both patterns generalise: as the contract between agent and tool gets tighter (schema, single writer, no side-channels) the class of failures available to the system collapses.

## Constrained decoding as a contract-tightening mechanism

A repeating pattern in small-model tool calling: the model emits argument JSON that almost matches the schema, but small errors (missing required fields, malformed quoting) break the parse. Two independent grey-lit sources document the same fix: switch from free-form tool-call generation to schema-constrained decoding. [[mirko2026gemma]] reports that Pydantic AI's default `ToolOutput` is unreliable with Gemma 4 via Ollama; `NativeOutput` (which maps to Ollama's `format=` with a JSON schema, engaging server-side constrained decoding) plus temperature 0.2 makes it reliable. vLLM's analogue is `guided_json`. [[mayo2026gemma4tools]] confirms via a from-scratch loop that small Gemma variants need *specific* retry-hint error strings to recover from malformed output; constrained decoding eliminates the need to recover. The corresponding chess-experiment observation — vLLM 400 BadRequest on malformed Gemma tool-call JSON — is the same failure mode in a different stack.

---
*Framing drawn from `../../manuscript-notes/essay-pointer.md` (Essay/essay.tex §2.6, §3.2).*
