---
type: literature
citekey: anthropic2024mcp
title: Introducing the Model Context Protocol
authors: [Anthropic]
year: 2024
venue: Anthropic engineering blog
raw_path: raw/literature/Antropic(2024).md
related_concepts: [tools-component, mcp-vs-skills, framework-four-components, context-engineering]
related_work: []
status: summarized
ingested: 2026-05-14
updated: 2026-05-15
---

# Anthropic (2024) — Introducing the Model Context Protocol

## Summary

Anthropic's launch announcement for the **Model Context Protocol (MCP)** — an open standard for connecting LLM-based AI assistants to external data sources and tools via a uniform two-way protocol. The post is short (a launch blog rather than a technical specification), but it is the canonical primary source for *the existence and motivation* of MCP. The argument: model capability has been advancing rapidly, but models remain "trapped behind information silos," and every new data source has required a custom integration. MCP replaces N×M custom integrations with N+M (one protocol on each side). The launch shipped: the specification and SDKs, local MCP server support in Claude Desktop, pre-built servers for Google Drive, Slack, GitHub, Git, Postgres, and Puppeteer, and a public open-source repository. Early adopters named: Block, Apollo, Zed, Replit, Codeium, Sourcegraph.

## Main claims

- **Capability advancement has outpaced data integration.** "Even the most sophisticated models are constrained by their isolation from data." Model quality has improved dramatically; the bottleneck has moved.
- **The fragmentation problem.** "Every new data source requires its own custom implementation, making truly connected systems difficult to scale." This is the classic N×M integration problem.
- **MCP is a uniform protocol.** Developers expose data through **MCP servers**; AI applications consume data via **MCP clients**. Two-way connections, single standard.
- **Three launch artefacts:**
  - The MCP specification and SDKs on GitHub (`github.com/modelcontextprotocol`)
  - Local MCP server support in Claude Desktop apps
  - An open-source repository of MCP servers
- **Pre-built servers** at launch: Google Drive, Slack, GitHub, Git, Postgres, Puppeteer — covering enterprise documents, chat, code repos, version control, structured data, and browser automation. This pre-built coverage is what made MCP immediately useful.
- **Authored by David Soria Parra and Justin Spahr-Summers** at Anthropic.
- **Sonnet 3.5 is good at writing MCP servers.** This is significant: a small but real claim that the protocol is *bootstrappable* by an LLM, lowering the cost of building new connectors. (Caveat: this is a marketing claim in a launch post.)

## Method / evidence

This is a launch announcement, not an empirical paper. There are no benchmarks, no evaluations, no comparative studies. The evidence is:
- Existence proof: the spec and SDKs are public.
- Adoption signal: named early adopters.
- A capability claim about Sonnet 3.5 building MCP servers (uncited).

Treat the post as a primary source for *what MCP is and why it was built*, not as evidence that MCP solves the problems it claims to solve. For empirical evidence about MCP in practice, the thesis should look to [[krishnan2025multiagent]] (architecture and applications), [[martin2026managed]] (managed agents), and downstream practitioner reports.

## Relevance to this thesis

### 1. The canonical primary source for [[tools-component]] and [[mcp-vs-skills]]

The thesis's four-component framework ([[framework-four-components]]) treats *tools* as one of the four infrastructure dimensions for agent productivity. MCP is the *industry-standard* answer to "how do agents access tools and data uniformly." Any thesis-level discussion of how agents acquire tools should cite this post as the launch-point and then cite later technical work for substance.

### 2. The fragmentation/standardisation argument is direct support for the infrastructure thesis

The post's framing — "model capability has advanced, but integration has not, and the integration is what's holding the system back" — *is* the thesis's framing applied to one specific component (tools). This is direct support for [[agent-infrastructure-vs-capability]]. The thesis can quote the launch post: "Even the most sophisticated models are constrained by their isolation from data."

### 3. The protocol/standard pattern is reusable

MCP's success (whatever final form that takes) is a concrete case study for *standardisation as the unlock*. The thesis can use MCP as the lead example when arguing that other parts of the four-component framework (workspace, skills, data) are similarly under-standardised and could benefit from analogous protocols. See [[mcp-vs-skills]].

### 4. Timing matters

MCP was launched November 2024. The thesis's framing of "agent infrastructure as the bottleneck" is *contemporary* with MCP's emergence. The thesis can use the rapid adoption of MCP across IDEs (Zed, Replit, Codeium, Sourcegraph) as evidence that the field is independently converging on the infrastructure-first reading.

## Notable concepts introduced

- **MCP server / MCP client** — the protocol's two roles. Servers expose data/tools; clients (AI applications) consume them. Two-way.
- **Standardisation as the unlock** — the implicit framing that capability advancement has been faster than integration standardisation.
- **Bootstrapping connectors via LLMs** — the claim that LLMs can write their own MCP servers, lowering the cost of long-tail integrations.

## Concept-page reconciliation

1. **`wiki/concepts/tools-component.md`** — should cite Anthropic 2024 as the launch event for the dominant industry-standard protocol. Currently the concept page likely treats tools more abstractly; MCP is the concrete instantiation.
2. **`wiki/concepts/mcp-vs-skills.md`** — this concept page exists precisely to distinguish MCP from Anthropic's Agent Skills approach ([[zhang2025]]). The two are complementary rather than competing. Anthropic 2024 is one of the two anchor sources.
3. **`wiki/concepts/framework-four-components.md`** — MCP is the tools-component standard; should be referenced as the canonical example.
4. **`wiki/concepts/agent-infrastructure-vs-capability.md`** — the post's framing is direct support; should be quoted.

## Tensions and qualifications

- **Marketing source, not research.** All claims should be cross-referenced with empirical work (Krishnan 2025, Martin 2026, etc.) before being load-bearing in the thesis.
- **MCP's eventual adoption shape is unsettled** as of the launch. The thesis should be careful about treating MCP as the *final* answer; it may be displaced by competing standards or refined substantially.
- **Security/auth model is not addressed in the launch post.** MCP's security implications (tool access permissions, authentication, sandboxing) are entirely outside the announcement's scope; substantive treatment is in [[martin2026managed]] and elsewhere.
- **What MCP does *not* cover.** The post is about exposing data and tools to models. It does not address how models *learn* to use new tools, how skills are composed, or how the agent's workspace is maintained. Those are separate components of the thesis's framework.

## Connections

- [[krishnan2025multiagent]] — multi-agent systems on MCP; architecture and applications. Empirical follow-up.
- [[martin2026managed]] — managed agents; covers harness, session, sandbox concerns adjacent to MCP.
- [[zhang2025]] — Agent Skills; complementary mechanism. The [[mcp-vs-skills]] concept page is the synthesis.
- [[rajasekaran2025]] — context engineering; MCP is one mechanism for getting context into the model.
- [[aizawa2025tools]] — writing effective tools for agents; the practitioner companion to MCP.
- [[fielding2000]] — the *protocol-design ancestor*. MCP imports REST's architectural constraints — client-server, stateless, uniform interface, layered system — into agent-tool integration. Reading MCP as REST-for-agents makes Fielding's four interface constraints (identification of resources / manipulation through representations / self-descriptive messages / HATEOAS) directly applicable as a design checklist.
- [[matarazzo2025survey]] — surveys the LLM substrate beneath MCP-style agent integration; situates MCP among RAG and LLM-modulo frameworks for grounding LLMs.
- Concept pages: [[tools-component]], [[mcp-vs-skills]], [[framework-four-components]], [[agent-infrastructure-vs-capability]].

---
*Ingested 2026-05-14. Read in full (short blog post).*
