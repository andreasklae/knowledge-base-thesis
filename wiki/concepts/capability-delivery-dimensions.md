---
type: concept
sources: [anthropic2024mcp, zhang2025, fielding2000, aizawa2025tools]
related_concepts: [mcp-vs-skills, tools-component, skills-component, framework-four-components, context-engineering, deterministic-tools-hypothesis, agent-infrastructure-vs-capability]
related_work: [experiment-chess, experiment-wcag-skill, experiment-riksantikvaren]
status: draft
updated: 2026-06-01
---

# Capability Delivery Dimensions

The choice between native tools, MCP, and skills is not a single-axis spectrum — it is a position in a roughly six-dimensional space. The existing "presets" (native, MCP, skills) are historical bundles, not a taxonomy. Understanding the dimensions lets you evaluate any new packaging proposal and recognise which trade-offs you are actually making.

## The six axes

1. **Invocation format** — typed JSON-Schema call vs. loose script command vs. free text. The model is fine-tuned for the first: structured arguments, per-field descriptions, constrained output. A `run_script(name, args)` dispatcher demotes this to a stringly-typed `name` and an untyped `args` array whose meaning lives in prose — taking the part the model is best at and pushing it out of the schema.

2. **Locality / transport** — in-process function, cross-process JSON-RPC, or filesystem + subprocess. Determines latency, language constraints, and what kind of infrastructure the capability requires.

3. **State ownership** — stateless pure function vs. stateful authoritative service. Stateless tools can be cold-started per call; stateful services (a browser session, a DB connection, a live game board) must persist across calls. This axis is orthogonal to everything else; confusing it with the invocation-format axis is the single most common design error.

4. **Context economics** — eager disclosure (all schemas always resident in context) vs. progressive disclosure (name first, detail on demand). MCP and native tools are eager; skills are progressive. For a large capability surface, this difference is significant. The harness-that-wraps-scripts idea ([[mcp-vs-skills]]) is an attempt to get progressive disclosure *and* typed schemas, resolving the tension.

5. **Packaging / ownership** — baked into the agent vs. standalone reusable service vs. bundled-with-knowledge. Determines portability, coupling, and who can consume it.

6. **Determinism** — deterministic code vs. model judgment. Orthogonal to all five axes above. A deterministic function can ship any of these ways. Detection, lookup, and search tasks should be deterministic; fuzzy reasoning tasks should be model-judgment. Conflating the two — letting the model "identify" an opening by having read about it rather than by running a book lookup — is a failure to apply the deterministic-tools principle ([[deterministic-tools-hypothesis]]).

The standard presets bundle these axes:

| | Invocation | Transport | State | Context | Ownership |
|---|---|---|---|---|---|
| Native tools | typed schema | in-process | stateless (typically) | eager | baked into agent |
| MCP | typed schema | cross-process / HTTP | stateful or stateless | eager | standalone reusable |
| Skills | loose script/prose | subprocess | stateless (typically) | progressive | bundled with knowledge |

Nothing forces these groupings. The chess experiment reasoning identified a coherent coordinate — **progressive disclosure *and* typed schema *and* bundled-with-knowledge** — that has no clean off-the-shelf name and is only partially buildable today.

## The field is pre-paradigmatic

MCP is ~2024, skills ~2025. The *transport/protocol* axis is consolidating (MCP looks like the LSP-for-tools winner), but the *packaging and disclosure* axes are still unsettled. Products bundle the six dimensions in incompatible ways. This is roughly where web APIs were in the SOAP/REST years: enough working examples to see the shape, no agreed vocabulary.

Open questions:

- **Versioning/coupling.** When the app's tools change, how does a bundled skill that references them stay in sync? Nobody has semver-for-tool-surfaces yet.
- **Validation layering.** Where should schema validation live — model, harness, or authoritative service? The answer is probably defense-in-depth, but the layering isn't agreed.
- **Who owns the disclosure decision.** The tool provider knows the capability; the harness owns the context budget. These interests diverge.
- **Runtime discovery vs. curated static toolsets.** Whether a large dynamic tool list actually helps the model or bloats context is largely untested empirically.

## HCI and systems analogues

Three prior frameworks map almost too cleanly:

**Norman's "knowledge in the head vs. knowledge in the world."** The context window is knowledge in the head — bounded, expensive, fast. Files/resources are knowledge in the world — cheap, large, retrieved on demand. Progressive disclosure *is* the retrieval discipline between them. Norman's **gulfs of execution and evaluation** map directly: a good tool description narrows the gulf of execution (the model knows it *can* do the thing and how); a clean `tool_result` narrows the gulf of evaluation (did it work, what's the state now). Tool surfaces are affordances for a bounded-rationality agent — exactly what HCI has studied for forty years.

**HATEOAS / hypermedia from REST.** The idea that a response carries the available next actions — so the client discovers capability from state rather than hardcoding it — is state-driven progressive tool disclosure. REST mostly abandoned HATEOAS because human-coded clients couldn't exploit runtime affordances. Whether the LLM is the first client that *can* (because it reads descriptions at runtime) is a thesis-grade open question: a 20-year-dead idea may become live precisely because the consumer changed.

**OS kernel/userland and capability-based security.** An authoritative board server is a kernel: narrow validated syscall ABI (the typed tools), no caller allowed to corrupt state. The skill is a userland program composing syscalls. A bash tool is handing out a shell. The "narrow keyhole vs. broad surface" trust axis is capability-based security, rediscovered.

**LSP as the direct precedent.** MCP is consciously LSP-for-tools. LSP solved "every editor reimplementing every language's analysis" by standardising the editor↔backend protocol. Its consolidation history is the single most transferable case study — not analogy, but the same architectural move one domain earlier.

## Three-party structure and interface C

Agent systems have a three-party structure: user ↔ AI (natural language + structured elicitation), AI ↔ app (typed tool calls), and user ↔ app (consent and authority). The third interface, user ↔ app, **must be a direct trusted channel, not relayed through the AI.** The model is the untrusted party in the middle; a permission system that routes consent through the AI is the vulnerability, not the feature. The OAuth consent screen rendering directly to the user (bypassing the agent) is the correct instantiation of this principle. MCP added URL-mode elicitation for exactly this reason.

This three-interface decomposition, with the trust asymmetry on interface C, is a concrete articulation of the infrastructure-not-capability claim: the productivity-determining decisions live at the *boundaries between the three parties*, not inside the model.

---
*Derived from `../../raw/discussions/Claude Conversation on tools, mcp and skills.md` (2026-06-01).*
