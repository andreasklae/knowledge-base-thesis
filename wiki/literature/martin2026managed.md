---
type: literature
citekey: martin2026managed
title: Scaling Managed Agents — Decoupling the brain from the hands
authors: [Martin, Lance, Cemaj, Gabe, Cohen, Michael]
year: 2026
venue: Anthropic engineering blog (published Apr 08, 2026)
raw_path: raw/literature/Martin(2026).pdf
related_concepts: [framework-four-components, workspace-component, tools-component, agent-infrastructure-vs-capability, context-engineering]
related_work: []
status: summarized
ingested: 2026-05-15
updated: 2026-05-15
---

# Martin, Cemaj, Cohen (2026) — Scaling Managed Agents: Decoupling the brain from the hands

## Summary

Anthropic's engineering post on **Managed Agents**, a hosted service for running long-horizon agent work. The central design move: **decouple the "brain" (Claude + harness) from the "hands" (sandbox + tools) and from the "session" (event log)**. Each becomes an independent interface that can fail or be replaced without disturbing the others. The framing is explicitly modeled on operating-system design — "how to design a system for programs as yet unthought of." Just as the read() syscall stayed stable while disks changed, Managed Agents' interfaces are designed to outlast any particular harness implementation. The post is the cleanest single articulation of **why agent infrastructure is the load-bearing layer**: it explicitly observes that harnesses encode assumptions about model capabilities that go stale (e.g., context-reset code added for Sonnet 4.5's "context anxiety" became dead weight on Opus 4.5). This is the thesis's argument, made in operational terms by the practitioners who run it at scale.

## Main claims

### 1. Harnesses encode model assumptions that go stale

The opening example: Anthropic added context-reset code to the harness because Sonnet 4.5 exhibited "context anxiety" (wrapped tasks up prematurely as context filled). When the same harness ran on Opus 4.5, the behavior was gone and the resets had become **dead weight**. *The harness lagged the model.* This is the thesis's [[agent-infrastructure-vs-capability]] argument restated by practitioners: capability changes faster than infrastructure, and infrastructure designed around one capability profile becomes wrong when the model improves.

### 2. The OS metaphor: virtualize the agent

Operating systems lasted decades by virtualizing hardware into stable abstractions (process, file). Managed Agents virtualizes the agent into:
- **Session**: append-only log of events (Session interface: `getSession`, `getEvents`, `emitEvent`).
- **Harness**: the loop that calls Claude and routes tool calls (Harness interface: `yield Effect<T> → EffectResult<T>`).
- **Sandbox**: execution environment for code and files (Sandbox interface: `provision({resources})`, `execute(name, input) → string`).
- **Orchestration**: scheduler that wakes sessions (`wake(sessionId)`).
- **Resources**: durable stores the sandbox fetches by reference.
- **Tools**: capability descriptions with `{name, description, input_schema}` (satisfied by MCP servers, custom tools).

The interfaces are opinionated about *shape*, not about *implementation*. "We're opinionated about the shape of these interfaces, not about what runs behind them."

### 3. Don't adopt a pet — cattle, not pets

The first attempt put session, harness, and sandbox in **one container**. This "adopted a pet" — if the container failed, the session died. Debugging required nursing the container back to health. Customer VPC requests required either network peering or running the harness in the customer's environment.

**Fix**: decouple the three. The harness leaves the container and calls it as just-another-tool via `execute(name, input) → string`. The container becomes cattle: if it dies, the harness catches a tool-call error, passes it to Claude, and Claude can retry with a fresh container provisioned via `provision({resources})`.

### 4. Harness failure recoverable from session log

Because the session log sits **outside the harness**, the harness itself becomes cattle. When a harness crashes, a new one boots, calls `wake(sessionId)`, fetches the event log via `getSession(id)`, and resumes. The agent loop writes durably via `emitEvent(id, event)`. **The agent's state is the session, not the process.**

### 5. The session is not Claude's context window

The session log is **larger and more durable** than Claude's context window. Standard context-engineering moves (compaction, memory tool, trimming) make irreversible decisions about what to retain. Managed Agents instead:
- Stores everything durably in the session.
- The harness calls `getEvents(session_id)` to selectively slice the event stream — picking up from last stop, rewinding before a moment, rereading before an action.
- The harness can transform fetched events before passing to Claude's context window (prompt-cache optimization, context engineering).
- **Concerns separated**: session = durable storage; harness = arbitrary context management.

### 6. The security boundary: brain and hands must be separated

In the coupled design, Claude's generated code ran in the same container as credentials. A prompt injection could exfiltrate tokens and spawn fresh unrestricted sessions. **Narrow scoping encoded an assumption about what Claude couldn't do, and Claude was getting smarter.** The structural fix: tokens are never reachable from the sandbox where Claude's code runs.

Two patterns:
- **Resource-bundled auth**: For Git, the access token clones the repo during sandbox init and wires the local remote. Push/pull work without the agent handling the token.
- **MCP via proxy + vault**: OAuth tokens stored in a secure vault; Claude calls MCP tools via a proxy that takes a session token, fetches the credential, and makes the external call. **The harness is never made aware of credentials.**

### 7. Many brains, many hands

Decoupling gave:
- **Many brains** via VPC: customers' resources no longer need to be in the harness's container. Network peering no longer required.
- **Performance**: p50 TTFT dropped ~60%; p95 dropped over 90%. Sessions that don't need a sandbox don't pay container provisioning cost up front.
- **Many hands**: each hand is `execute(name, input) → string` — could be a container, a phone, a Pokémon emulator. Brains can pass hands to each other.

### 8. Meta-harness: opinionated about interfaces, not implementations

Managed Agents is a **meta-harness**. Specific harnesses (Claude Code, task-specific narrow harnesses) plug in via the same interfaces. The system makes no assumptions about the number or location of brains or hands. Future harness implementations should slot in.

## Method / evidence

This is an engineering blog post, not a research paper. Evidence:
- A worked design narrative explaining the move from coupled to decoupled architecture.
- Quantitative TTFT numbers (p50 -60%, p95 -90%).
- Code-shaped pseudocode for each interface.
- An origin story (the context-anxiety/context-reset/Opus example) that motivates the design.

No external replication. No benchmarks. The "evidence" is operational experience at Anthropic-scale.

## Relevance to this thesis

### 1. The clearest in-the-wild statement of the thesis's infrastructure-as-load-bearing claim

The opening lines:

> *"Harnesses encode assumptions that go stale as models improve."*

This is the thesis's argument in one sentence, from the people who run it at scale. Anything the thesis writes about infrastructure-as-bottleneck should cite this post as the practitioner-side of the same argument.

### 2. The decoupling of brain / hands / session maps onto the four-component framework

Mapping:
- **Brain** = the model (capability)
- **Hands** = tools + sandbox (the [[tools-component]])
- **Session** = durable state, larger than context window (the [[workspace-component]] / [[data-component]] hybrid)
- **Harness** = the orchestration layer (cross-cuts components)

The thesis's [[framework-four-components]] (workspace / tools / skills / data) and Martin et al.'s brain/hands/session are different decompositions of the same problem space. The mapping is not 1-to-1 (skills aren't in Martin et al.; harness isn't in the four-component framework). Worth surfacing as a discussion point.

### 3. Session ≠ context window — direct vocabulary for the thesis

"The session is not Claude's context window" is a tight, citable phrase. The thesis's [[workspace-component]] page can adopt this distinction explicitly: the workspace is *larger and more persistent* than the context window, and the agent interrogates it via positional slicing.

### 4. "Don't adopt a pet" is a reusable design principle

The cattle-not-pets framing transfers cleanly to the thesis's discussion of agent infrastructure design. Each infrastructure component should be **stateless, replaceable, recoverable**. The agent's state should live in durable interfaces, not in any particular process.

### 5. Security: credentials must never be reachable by model-generated code

The structural-fix-not-narrow-scoping argument is the thesis's [[deterministic-tools-hypothesis]] applied to security: do not rely on the model being unable to do something; rely on the architecture making it impossible. This is the right design move and should be cited when the thesis discusses agent security.

### 6. TTFT as a productivity metric

The 60% / 90% TTFT drop after decoupling is concrete productivity-impact evidence — comparable in spirit to [[peng2023copilot]]'s 55.8% task-completion speedup but at the infrastructure layer. Worth pairing.

## Notable concepts introduced

- **Brain / hands / session decomposition** — the central design move.
- **Meta-harness** — a system unopinionated about the specific harness; opinionated about the interfaces.
- **Context anxiety** — Sonnet 4.5's tendency to wrap up prematurely as context fills. Documented as a model behavior.
- **Dead weight harness code** — harness logic added for one model that becomes a bug-source for the next.
- **Pets vs cattle for agent containers** — applied analogy.
- **Session as context object outside the context window** — sliceable, durable, externally addressable.
- **execute(name, input) → string** — the universal hand interface. Any tool, MCP server, sandbox shape.
- **TTFT (time-to-first-token)** as the user-felt latency metric.
- **Resource-bundled auth and proxy-vault patterns** for credential isolation.

## Concept-page reconciliation

1. **`wiki/concepts/agent-infrastructure-vs-capability.md`** — Martin et al. is the cleanest practitioner statement of the thesis's headline claim. The "harnesses encode assumptions that go stale" line should be quoted directly.

2. **`wiki/concepts/framework-four-components.md`** — Martin et al.'s decomposition is a parallel decomposition of the same problem space. Worth a comparison paragraph: brain/hands/session vs workspace/tools/skills/data. They're not isomorphic but they're addressing the same design problem.

3. **`wiki/concepts/workspace-component.md`** — Martin et al.'s "session is not Claude's context window" directly supports the workspace-as-distinct-from-context-window claim. Add the concrete `getEvents(session_id)` interface as a concrete pattern.

4. **`wiki/concepts/tools-component.md`** — the universal hand interface `execute(name, input) → string` is the operational form of "tools are just things the agent can call."

5. **`wiki/concepts/context-engineering.md`** — Martin et al. explicitly argues against irreversible context decisions (compaction, trimming). Adds nuance to the context-engineering literature (it is *not* always about deciding what to keep; sometimes it's about keeping everything and slicing on demand).

6. **`wiki/concepts/deterministic-tools-hypothesis.md`** — the security pattern (credentials never reachable from sandbox) is a deterministic-architectural fix instead of a model-behavior assumption. Direct support.

## Tensions and qualifications

- **Vendor blog, not research.** Treat as a primary source for *what Anthropic built and why*, not as independent evidence that the design is optimal.
- **No external comparison.** No quantitative comparison against alternative architectures (LangGraph, AutoGen, custom harnesses). Just before-and-after metrics inside Anthropic.
- **The OS metaphor is suggestive, not literal.** Process/file abstractions worked because hardware was bounded and well-understood. Agent capabilities are not bounded the same way; the "interfaces stay stable" claim is aspirational.
- **Cost of generality.** The decoupled architecture adds service boundaries, latency between brain and hands, and operational complexity. The post mentions the pet container's advantages (direct syscalls, no service boundaries) — and chose to give them up. Other teams may make the other tradeoff.
- **The session-log-as-source-of-truth design assumes durable storage is cheap.** For very-long-horizon agents (weeks, months), session log size becomes a real cost.
- **MCP-vault-proxy security pattern is one design.** Other patterns (e.g., zero-trust capability tokens) exist; this one is now the de facto Anthropic pattern but isn't uniquely right.

## Connections

- [[anthropic2024mcp]] — MCP is one of the "many hands" the brain can call. Martin et al. extends MCP into a full multi-component architecture.
- [[krishnan2025multiagent]] — multi-agent on MCP; closely related architecturally.
- [[zhang2025]] — Agent Skills; a complementary mechanism for what the agent knows how to do.
- [[rajasekaran2025]] — context engineering; Martin et al. takes a position on the context-engineering debate (durable session + flexible harness transformation).
- [[aizawa2025tools]] — writing effective tools; the `execute(name, input) → string` interface formalizes what a good tool looks like.
- [[peng2023copilot]] — productivity payoff; Martin et al. shows the infrastructure-layer productivity wins (60% / 90% TTFT).
- [[simon1996artificial]] — the OS metaphor is the same near-decomposability argument Simon made for complex systems generally.
- [[fielding2000]] — the architectural-style methodology that managed-agent harnesses inherit. Martin's brain/hands/session decomposition is a Fielding-style constraint set: each component has a role, an interface, and a property it induces. The MCP-vault-proxy pattern is REST's *layered system* applied to agent-tool security.
- [[matarazzo2025survey]] — Matarazzo's LLM-substrate survey covers the LLMs that Martin's harness wraps; useful as the foundation-layer companion.
- Concept pages: [[agent-infrastructure-vs-capability]], [[framework-four-components]], [[workspace-component]], [[tools-component]], [[context-engineering]], [[deterministic-tools-hypothesis]].

---
*Ingested 2026-05-15. Read in full (12 pages including site chrome).*
