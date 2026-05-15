---
type: concept
sources: [anthropic2024mcp, zhang2025, fielding2000, aizawa2025tools, weber2024taxonomy]
related_concepts: [tools-component, skills-component, data-component, framework-four-components]
related_work: [experiment-riksantikvaren, experiment-wcag-skill]
status: draft
updated: 2026-05-13
---

# MCP vs. Skills: The Integration Spectrum

The same agent capability can be exposed as a vendor-published interface (Model Context Protocol [[anthropic2024mcp]]) or as a lightweight developer-owned module (a skill file [[zhang2025]]). The choice is structural, not technical.

## The two ends of the spectrum

- **MCP (the API model).** A vendor publishes a stable interface; multiple consumers connect to a single source of truth; updates propagate uniformly. Paid for in server infrastructure, versioning discipline, and slower iteration.
- **Skills (the local module model).** A markdown file plus scripts dropped into a folder. Trivial to author and modify. Paid for in absent shared truth and the corresponding risk of drift across deployments.

## Historical analogue

The same tension played out in the early 2000s between heavyweight protocol-based web services and lighter resource-based ones — the choice the web-services world eventually settled by deployment context rather than by which technology was more capable.

[[fielding2000]] is the canonical reference. REST is a *named, coordinated set of constraints* (client-server, stateless, cache, uniform interface, layered system, code-on-demand) that induces *evolvability, scalability, intermediary support*; MCP imports those constraints into agent-tool integration with near-direct correspondences (JSON-RPC for stateless requests; prompts/resources/tools/roots/sampling for the uniform interface). The MCP-skills choice is the agent-era replay of REST-vs-RPC, with skills playing the lighter-weight role.

## The decision rule

- Publish an MCP server when the interface is stable, the consumer set is broad, and the cost of inconsistency exceeds the cost of maintenance.
- Write a skill when the task is specific, the consumer set is one team, and the cost of drift is acceptable because the same team controls the deployments.

## The prediction

Skills are likely to dominate inside organisations; MCP is likely to dominate across them. The choice is driven by *who owns the interface contract* rather than by which technology is more capable.

## Where it surfaces in experiments

- [[experiment-riksantikvaren]] — the Askeladden integration is closer to MCP (single authoritative source, broadly useful) but the prompts and retrieval glue around it are skill-shaped (one team, local control).
- [[experiment-wcag-skill]] — a WCAG audit skill is the canonical skill-shaped case: a small team, a specific task, drift acceptable because the team controls the deployments.

## Authoring discipline cuts across both ends

The integration choice is one axis; tool/skill *quality* is orthogonal. [[aizawa2025tools]]'s prototype-evaluate-iterate loop and authoring principles (namespacing, response-format enums, prompt-engineered errors, semantic identifiers) apply on both ends of the spectrum. An MCP server can be poorly designed; a skill can be excellent. The protocol layer does not determine the authoring discipline.

[[weber2024taxonomy]]'s LLM-component taxonomy is a useful cross-cutting reference: the same 13-dimension classification (Invocation / Function / Prompt / Skills / Output) applies whether the underlying capability is exposed as MCP, as a skill, or as inline tooling.

---
*Framing drawn from `../../manuscript-notes/essay-pointer.md` (Essay/essay.tex §2.7).*
