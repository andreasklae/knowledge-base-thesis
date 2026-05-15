---
type: literature
citekey: zhang2025
title: Equipping agents for the real world with Agent Skills
authors: [Zhang, Mahesh, and Anthropic Applied AI team]
year: 2025
venue: Anthropic Engineering Blog
raw_path: raw/literature/Zhang_et_al(2025).pdf
related_concepts: [skills-component, framework-four-components, mcp-vs-skills, tools-component, context-engineering]
related_work: []
status: summarized
ingested: 2026-05-15
updated: 2026-05-15
---

# Zhang et al. (2025) — Equipping agents for the real world with Agent Skills

## Summary

An Anthropic Applied-AI engineering post introducing **Agent Skills**: a packaging convention for *folders of instructions, scripts, and resources* that Claude can discover and load on demand. A Skill is, at its simplest, a directory containing a `SKILL.md` file with YAML frontmatter (a name and a description); Claude reads only the frontmatter at startup, and loads the rest only when the description matches the current task. The post frames Skills as the answer to a specific gap left by MCP: MCP standardises how agents connect to *external systems*, but most operational knowledge a frontier agent needs is procedural and contextual — *how* to fill in a particular client's PDF form, *how* to format a brand-styled deck, *what* internal naming convention applies — and that knowledge is not naturally expressed as a tool call. Skills are *progressive disclosure of procedural context*: cheap to enumerate, loaded only when relevant, composable, and portable across Claude.ai, Claude Code, and the API. For the thesis, this is the canonical reference for the **skills component** of the four-component framework.

## Main claims

### 1. The problem Skills solve

Pre-Skills, the operational pattern was: stuff every relevant instruction into the system prompt, or wire a long chain of tools and hope the model invokes them correctly. Both fail at scale:
- **System-prompt bloat.** Every "for this client, use template X; for that client, use template Y" consumes context permanently.
- **Tool sprawl.** Bare tool calls don't carry the rich procedural context ("when generating a quarterly report, first pull the closed-deals view, then…") that defines real workflows.
- **Discoverability.** A user can't easily tell Claude what it doesn't know it doesn't know.

Skills are designed to address all three: load on demand, carry procedural context, and be discoverable via descriptions.

### 2. What a Skill is, mechanically

- A **directory** with a `SKILL.md` at the root and arbitrary supporting files (scripts, reference docs, templates).
- The `SKILL.md` has YAML frontmatter with at minimum:
  - `name` — short identifier.
  - `description` — what the skill does and when to use it. **This is the only field Claude reads at startup.** It must be specific enough that Claude can decide whether to load the skill.
- The body of `SKILL.md` is the procedural instruction Claude reads *after* deciding to load the skill.
- Supporting files (e.g. `scripts/`, `references/`) are accessible from inside the skill's execution context.

### 3. Progressive disclosure as the central design principle

The post returns repeatedly to **progressive disclosure**: the architecture should expose *just enough information to decide* before paying the cost of loading the full content. Three nested layers:
1. **Skill listing layer.** Claude sees `name` + `description` only. Cheap; many skills can be enumerated.
2. **Skill body layer.** When a skill matches the task, Claude loads `SKILL.md`.
3. **Resource layer.** When the skill body references a script or reference, *that* is loaded.

The lesson: **context engineering is a layered access problem, not a packing problem.** The wrong default is "load everything that might be relevant"; the right default is "expose handles, load on demand."

### 4. Skills compose with tools and with each other

- Skills can invoke tools (via MCP or built-in code execution).
- A skill can reference scripts that the agent executes deterministically (Anthropic's "use code, not prose" recommendation).
- Skills can chain: one skill's output can be the input to another.
- Multiple skills active in a session don't need to "know about" each other — Claude orchestrates them.

This composition pattern is the operational realisation of the [[deterministic-tools-hypothesis]]: skills package *procedures*, which contain calls to *deterministic scripts* where appropriate, mediated by the LLM as orchestrator.

### 5. Authoring guidance (the most practically useful section)

- **Names are routing.** A skill called "pdf-form-fill" with a vague description won't get loaded; the description must say *what counts as a PDF form to be filled* and *what the skill returns*.
- **Descriptions are decision aids for Claude.** Write them in the second person, naming the trigger conditions explicitly. Examples in the post: "Use this skill when the user uploads a PDF that contains form fields, or asks to fill out a form…"
- **Bodies are instructions to the agent.** Not documentation for humans. Use imperative voice; assume Claude has access to the tools listed.
- **Reference deterministic scripts** for anything that doesn't need LLM judgement — date parsing, CSV manipulation, image cropping. Keeps the LLM out of the verification loop.
- **Test the skill in isolation** before deploying it; the post recommends a workflow of (a) write the skill, (b) start a fresh session, (c) describe the task in user-language, (d) verify Claude invokes the skill and produces the right output.

### 6. Distribution and reuse

- Skills are folders, so they can be checked into git, shared via PRs, distributed as packages.
- Anthropic ships skills inside Claude.ai (e.g., document creation skills).
- Customers can develop their own and load them via Claude Code's skills folder or via the API's skills parameter.
- Cross-surface portability: the same skill folder works in Claude.ai, Claude Code, and via the API.

## Method / evidence

- This is an **engineering blog post**, not a paper. No formal evaluation, no quantitative comparisons.
- The post references *internal use cases* (Anthropic Applied-AI team using skills with customers) without naming specific customers or reporting numbers.
- Authority rests on Anthropic's own product role: this is the team that built the feature describing how it works and how to use it well.

## Relevance to this thesis

### 1. The canonical reference for the skills component

The thesis's [[framework-four-components]] argues for *workspace, tools, skills, data* as the four primary infrastructure components. The **skills** component is the youngest of the four; until Zhang 2025, "skills" as a distinct architectural category didn't have a clean industry referent. This post is that referent. The thesis must cite it as the canonical source.

### 2. Progressive disclosure as a thesis-load-bearing concept

Progressive disclosure is the right framing for *all four components*, not just skills:
- **Workspace:** disclose files on demand (file tree → glob → read).
- **Tools:** disclose tool list → tool schema → tool result.
- **Skills:** disclose name/description → body → resources.
- **Data:** disclose index summary → retrieval results → full document.

The thesis can use Zhang's "progressive disclosure" language across the framework, not just for skills. This unifies the four components under a shared principle.

### 3. Skills ≠ tools — the contrast point

Zhang stays mostly in the skills frame. [[anthropic2024mcp]] stays in the tools frame. The thesis's [[mcp-vs-skills]] page is exactly about the contrast:
- **Tools** are atomic actions: one call, one return value, well-typed schema.
- **Skills** are procedures: multi-step recipes, prose instructions, internal logic, possibly internal tool calls.

A tool answers *what action can I take?* A skill answers *how do I do this task?* Both are infrastructure; they sit at different levels of abstraction.

### 4. Operational realisation of deterministic-tools

Zhang's authoring guidance — "reference deterministic scripts for anything that doesn't need LLM judgement" — is the operational form of the thesis's [[deterministic-tools-hypothesis]]. Skills are the *packaging mechanism* by which deterministic scripts are paired with the LLM-side context that tells the model when and how to use them.

### 5. Discoverability as a productivity constraint

A recurring thesis theme is that *capabilities the agent doesn't know it has are equivalent to capabilities it doesn't have*. Zhang's emphasis on description-quality-as-routing is direct support: a skill that exists but isn't surfaced is a skill that doesn't exist. **Discoverability is a first-class component of productivity infrastructure.**

### 6. The thesis's own knowledge-base concept page reconciliation

The thesis is currently in `wiki/concepts/skills-component.md` — that page should cite Zhang 2025 as its primary external reference and adopt the progressive-disclosure framing. Worth promoting from `draft` to `summarized` after this ingest.

## Notable concepts introduced

- **Agent Skill** — folder with `SKILL.md` + frontmatter (`name`, `description`) + body + optional resources.
- **Progressive disclosure** — three-layer load model (listing → body → resources).
- **Description as routing signal** — `description` field is the primary cost-effective discovery mechanism.
- **Cross-surface portability** — same skill folder works in Claude.ai, Claude Code, and API.
- **Skills compose** — skills can invoke tools, scripts, and each other.

## Concept-page reconciliation

1. **`wiki/concepts/skills-component.md`** — Zhang 2025 *is* the canonical reference. The concept page should cite it as primary, adopt the progressive-disclosure framing, and lift the authoring guidance verbatim where it serves. Promote `status: draft → summarized`.
2. **`wiki/concepts/mcp-vs-skills.md`** — Zhang stays in the skills frame; [[anthropic2024mcp]] stays in the tools frame. The concept page should pair them and articulate the contrast (atomic actions vs procedures; tools-as-capability vs skills-as-recipe).
3. **`wiki/concepts/framework-four-components.md`** — Zhang's progressive-disclosure principle can be lifted from the skills section and presented as a *cross-component* design principle, applied to workspace, tools, and data as well.
4. **`wiki/concepts/context-engineering.md`** — progressive disclosure is the most operationally useful context-engineering pattern in the post. Cite Zhang as the practical instantiation; pair with [[rajasekaran2025]] for the more general framing.
5. **`wiki/concepts/deterministic-tools-hypothesis.md`** — Zhang's authoring guidance ("reference deterministic scripts for anything that doesn't need LLM judgement") is direct industry support for the thesis's hypothesis. Worth a short citation.

## Tensions and qualifications

- **No empirical evaluation.** The post is normative ("here's how to author skills well") and lacks comparison data ("skills outperform X by Y%").
- **Anthropic-specific.** The skill format is an Anthropic convention. Whether it generalises (OpenAI's GPTs, Google's Gems are analogous-but-different) is open.
- **Description quality is human-authored.** The whole progressive-disclosure architecture relies on humans writing good descriptions. Mediocre descriptions silently degrade skill use.
- **Skill orchestration is implicit.** The post doesn't deeply address what happens when two skills overlap, conflict, or could both apply. The model arbitrates; the rules of arbitration aren't formalised.
- **Scaling to hundreds of skills.** The "listing layer is cheap" claim is true for tens of skills; at hundreds, even just enumerating names/descriptions starts to compete for context. The post doesn't address this.
- **Security/permissions.** Skills can invoke tools and scripts; the post doesn't address sandboxing or permission boundaries in detail. [[martin2026managed]] is the better reference for that.

## Connections

- [[anthropic2024mcp]] — the tools side of the agent-infrastructure stack; skills are the complementary side.
- [[martin2026managed]] — covers harness/session/sandbox; skills run inside that harness.
- [[rajasekaran2025]] — context engineering more broadly; progressive disclosure is one instance.
- [[aizawa2025tools]] — writing effective tools; mirrors Zhang's authoring guidance for the tools layer.
- [[krishnan2025multiagent]] — Krishnan stays entirely in MCP frame; doesn't address skills. The contrast is what makes [[mcp-vs-skills]] valuable.
- [[weber2024taxonomy]] — terminological disambiguation: Weber's *Skills* dimension (output-property: reWrite/Create/conVerse/Inform/Reason/Plan) is a different concept from Zhang's *Skills* (packaging mechanism). The two share the name but classify different things; the thesis should clarify on every joint citation.
- [[fielding2000]] — Zhang-skills are Fielding-style architectural conventions on top of the file system: a coordinated set of constraints (`SKILL.md` schema, name+description frontmatter, progressive load order) that induce discoverability and composability. The pattern is REST-shaped — uniform interface plus self-descriptive metadata.
- [[karpathy2025wiki]] — the LLM Wiki's schema file (CLAUDE.md / AGENTS.md) is the same packaging idea applied to knowledge bases: a procedural conventions document the agent reads alongside the workspace. Skills are to tools what schemas are to wikis.
- Concept pages: [[skills-component]], [[framework-four-components]], [[mcp-vs-skills]], [[tools-component]], [[context-engineering]], [[deterministic-tools-hypothesis]].

---
*Ingested 2026-05-15. Read in full (engineering blog post, ~20 pages PDF export).*
