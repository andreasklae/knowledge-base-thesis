---
type: literature
citekey: karpathy2025wiki
title: LLM Wiki — A pattern for building personal knowledge bases using LLMs
authors: [Karpathy, Andrej]
year: 2025
venue: GitHub Gist (idea file)
raw_path: raw/literature/Karpathy(2025).md
related_concepts: [data-component, workspace-component, agent-infrastructure-vs-capability, framework-four-components, context-engineering]
related_work: []
status: summarized
ingested: 2026-05-15
updated: 2026-05-15
---

# Karpathy (2025) — LLM Wiki: A pattern for building personal knowledge bases using LLMs

## Summary

A short, deliberately abstract gist by Andrej Karpathy proposing a design pattern: **LLM-maintained, persistent, interlinked wiki on top of curated raw sources**, mediated by a schema file (e.g. CLAUDE.md / AGENTS.md). The pattern is positioned explicitly *against* default RAG-style document upload: where RAG re-derives knowledge from scratch on every query, the **LLM Wiki accumulates synthesis** in a structured, editable artefact that *gets richer with every source*. The architecture is three-layered: raw sources (immutable, human-curated), wiki (LLM-owned markdown files with cross-references), schema (human + LLM co-evolved configuration for how the wiki is structured and maintained). Four canonical operations: **Ingest, Query, Lint, plus an Indexing/Logging discipline**. Tools mentioned: Obsidian as the IDE, qmd or similar for search at scale, Marp for slide generation, Dataview for frontmatter queries. The closing line names the precedent: **Vannevar Bush's Memex (1945)** — the part Bush couldn't solve was who does the maintenance; LLMs do it. For the thesis, this is the canonical *vision document* for the workspace-and-data infrastructure pattern the thesis is studying; it is also directly load-bearing because **the thesis's own knowledge base is an implementation of this pattern**.

## Main claims

### 1. RAG re-derives; the Wiki accumulates

The post's central distinction:
- **RAG default:** upload documents → retrieve at query time → answer. Each query starts from raw chunks. *Nothing builds up.*
- **LLM Wiki:** ingest document → LLM reads, extracts, integrates into existing wiki → updates entity pages, revises summaries, flags contradictions. Each ingest is a *compounding edit*.

The key sentence: *"The wiki is a persistent, compounding artifact. The cross-references are already there. The contradictions have already been flagged. The synthesis already reflects everything you've read."*

This is a direct architectural critique of standard RAG: not "RAG is wrong" but "RAG doesn't accumulate, and accumulation is the bottleneck on long-horizon knowledge work."

### 2. Three-layer architecture

- **Raw sources** — immutable, human-curated. The LLM reads but never modifies. *Source of truth.*
- **Wiki** — LLM-owned markdown directory. Summaries, entity pages, concept pages, comparisons, index, log. *The LLM writes; the human reads.*
- **Schema** (CLAUDE.md / AGENTS.md) — the *configuration file* that defines wiki structure, conventions, and operation workflows. *Co-evolved by human and LLM over time.*

This is exactly the architecture the thesis's knowledge base uses. The post is operationally load-bearing for the thesis's workflow.

### 3. Four operations

- **Ingest** — drop source in raw/, LLM reads, discusses, writes summary, updates index, propagates across 10-15 pages, appends to log. Karpathy's stated preference: one source at a time with human in the loop.
- **Query** — ask question; LLM searches index, reads pages, synthesizes answer. **Crucial point:** *"good answers can be filed back into the wiki as new pages"* — explorations should compound, not vanish into chat history.
- **Lint** — periodic health check. Contradictions, stale claims, orphan pages, missing concepts, missing cross-references, data gaps. Result: questions to investigate, sources to find.
- **(Implicit) Capture** — observations, decisions, diary entries, ideas. Not named here but a natural fourth operation; the thesis's own CLAUDE.md adds it explicitly.

### 4. Indexing and logging as load-bearing files

- **index.md** is content-oriented, organised by category, updated on every ingest. At ~100 sources / hundreds of pages, **the index file is sufficient — no embedding-based retrieval needed.** This is a strong, contrarian operational claim: *for personal-scale wikis, BM25 + index lookup beats vector search.*
- **log.md** is chronological, append-only. Consistent prefix per entry (e.g. `## [2026-04-02] ingest | Article Title`) makes it grep-parseable. **Unix-style log discipline.**

### 5. CLI tools optional

- **qmd** (Tobi Lütke's local-first markdown search engine, BM25+vector hybrid, MCP server) as one example.
- "You could also build something simpler yourself — the LLM can help you vibe-code a naive search script as the need arises."
- Translation: *tools are emergent infrastructure, not upfront requirements.*

### 6. Memex precedent

Vannevar Bush's 1945 Memex was a personal, curated knowledge store with *associative trails between documents*. The web turned into something else (public, ad-driven). Bush's actual vision matches the LLM Wiki: private, curated, connections as primary content.

**"The part he couldn't solve was who does the maintenance. The LLM handles that."**

This is the post's deepest claim: *maintenance was the binding constraint on the Memex vision, and that constraint is now lifted.*

### 7. Division of labour

*"You're in charge of sourcing, exploration, and asking the right questions. The LLM does all the grunt work — the summarizing, cross-referencing, filing, and bookkeeping."*

Three concrete operational tips:
- **Obsidian Web Clipper** for capturing sources.
- **Local image download** so the LLM can view referenced images directly.
- **Graph view** as the visual surface for the wiki's structure.

## Method / evidence

- **Idea file**, not a research paper. Designed to be "copy-pasted to your own LLM Agent." No empirical evaluation; instead, a normative architectural pattern.
- Authority rests on Karpathy's general influence in AI engineering practice.
- The thesis's own knowledge base is a direct implementation, which is itself a form of validation (existence proof that the pattern is workable).

## Relevance to this thesis

### 1. The thesis's own working environment is an LLM Wiki

The most direct relevance: **this knowledge base is an instance of the LLM Wiki pattern.** The CLAUDE.md, the index.md, the log.md, the wiki/literature/ and wiki/concepts/ split, the four operations (ingest/capture/query/lint) — all derive from this gist. The thesis can cite Karpathy 2025 as the *origin of the pattern*, with the thesis's own knowledge base as a working instance.

### 2. RAG-vs-accumulation as a thesis-relevant contrast

The thesis's [[data-component]] page should articulate the contrast Karpathy draws: *RAG retrieves from raw; wiki retrieves from compiled synthesis.* This maps directly onto:
- [[lewis2020rag]] — classic pre-inference retrieval over raw documents.
- Karpathy 2025 — LLM-maintained intermediate synthesis layer.
- [[rajasekaran2025]] — just-in-time retrieval over a structured workspace.

These are three points on the *retrieval-target spectrum*: raw chunks → curated synthesis → on-demand exploration.

### 3. The maintenance-cost argument for infrastructure-as-bottleneck

Karpathy's deepest claim — *maintenance is the binding constraint, and LLMs lift it* — is a strong statement of the thesis's [[agent-infrastructure-vs-capability]] thesis applied to *the human-LLM symbiosis*. The infrastructure is the wiki; the LLM is the agent; the constraint that capped Bush's vision was a *labor constraint*, and the agent's value is in absorbing it.

### 4. Index-file beats embeddings at moderate scale

A specific operational claim: *at ~100 sources, the index file beats vector retrieval.* This is consistent with [[rajasekaran2025]]'s general anti-pre-indexing position. The thesis should consider this as evidence that **pre-built embeddings infrastructure is often overkill** for the scales most agents operate at.

### 5. Wiki + Obsidian + git = workspace-component instantiation

Karpathy is implicitly arguing for a *specific workspace architecture* — markdown files in git, opened in Obsidian, edited by an LLM via a coding agent. This is a [[workspace-component]] instantiation that the thesis can describe concretely.

### 6. "Good answers can be filed back" = querying as accumulation

A subtle but important point: queries are not consumption-only; they are *generative inputs* to the wiki. The thesis's [[context-engineering]] page can lift this: *the conversation itself is part of the corpus.*

### 7. Schema as co-evolved configuration

CLAUDE.md is not a static config — it's *co-evolved by human and LLM*. This is a meta-level infrastructure pattern: the agent participates in defining how it should work. Worth surfacing as a productivity pattern.

## Notable concepts introduced

- **LLM Wiki** — the pattern itself.
- **Three-layer architecture** — raw sources / wiki / schema.
- **Compounding artifact** — the wiki gets richer with every ingest.
- **Schema file** (CLAUDE.md, AGENTS.md) — co-evolved configuration.
- **Four operations** — ingest, query, lint (+ implicit capture).
- **Index file at moderate scale** — beats embeddings up to ~100 sources.
- **Memex with maintenance solved** — historical framing.
- **"Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."**

## Concept-page reconciliation

1. **`wiki/concepts/data-component.md`** — Karpathy is the canonical informal source for the *accumulated-synthesis-over-raw-retrieval* design point. Cite alongside [[lewis2020rag]] and [[rajasekaran2025]].
2. **`wiki/concepts/workspace-component.md`** — the LLM Wiki is a specific workspace architecture (Obsidian + git + markdown + schema file). Cite as a concrete instantiation.
3. **`wiki/concepts/framework-four-components.md`** — Karpathy's three-layer architecture (raw / wiki / schema) maps roughly onto data / workspace / skills components of the four-component framework. Useful comparison.
4. **`wiki/concepts/agent-infrastructure-vs-capability.md`** — the maintenance-cost argument is the strongest informal articulation of this thesis. Cite the Memex line explicitly.
5. **`wiki/concepts/context-engineering.md`** — "good answers can be filed back" is a context-engineering pattern: the agent's outputs become future context. Worth a section.

## Tensions and qualifications

- **Idea file, not validated implementation.** Karpathy explicitly states this is abstract. Many implementation details (how the LLM decides what to integrate, how it resolves contradictions, how it picks the right cross-references) are left open.
- **Personal scale, not enterprise scale.** Karpathy's "~100 sources / hundreds of pages" is moderate. Patterns that work at this scale may not generalise — coordination, access control, conflict resolution all become harder at team or org scale.
- **Schema co-evolution sounds nice but is fragile.** A human-and-LLM co-edited config file can drift, contradict itself, accumulate dead conventions. The thesis's own CLAUDE.md will need active maintenance.
- **Lint is described but not deeply specified.** "Look for contradictions" is hand-wave; in practice, contradiction detection at the synthesis level is hard.
- **No discussion of cost or latency.** Ingesting one source can touch 10-15 pages, each requiring LLM reads and writes. At scale this is expensive. Karpathy doesn't address it.
- **Heavy reliance on Claude Code / Codex / similar agentic-coding tools.** The pattern presumes the agent has shell, file edit, and read tools. Lower-capability agents (chat-only) cannot implement this.
- **No empirical productivity comparison.** The post asserts the wiki approach beats RAG; no data.
- **The thesis is itself instance evidence — but n=1.** The fact that *this* knowledge base implements the pattern is suggestive but not conclusive.

## Connections

- [[lewis2020rag]] — the architectural foil. RAG retrieves from raw; LLM Wiki maintains synthesis.
- [[rajasekaran2025]] — just-in-time retrieval; same anti-pre-indexing posture.
- [[zhang2025]] — agent skills as procedural-context packaging; LLM Wiki schema is similar (procedural conventions packaged in CLAUDE.md).
- [[anthropic2024mcp]] — MCP-style tools (qmd) are the optional CLI layer Karpathy mentions.
- [[aizawa2025tools]] — Aizawa's "evaluation-driven tool design" complements: the wiki schema *is* a tool design exercise.
- [[simon1996artificial]] — Simon's near-decomposability and Memex-era references precede Karpathy's framing.
- [[hutchins1995wild]] — distributed cognition: the LLM Wiki is a distributed-cognitive system across human + LLM + files.
- [[sequoia2026karpathy]] — Karpathy's later interview elaborates the productivity vision around AI agents; restates and elevates the Wiki framing as *understanding amplifier* ("you can outsource your thinking but you can't outsource your understanding").
- [[fielding2000]] — the LLM Wiki's three-layer architecture (raw / wiki / schema) is a Fielding-style architectural style. Each layer is a coordinated set of constraints (raw is immutable, wiki is LLM-owned and append-evolvable, schema is co-edited and authoritative). Cite as the principled-design ancestor when arguing the pattern is more than a convention.
- [[matarazzo2025survey]] — the wiki sits on top of the LLM substrate Matarazzo surveys; the §4.5 Modular RAG taxonomy has module-level overlaps with the wiki architecture (Search / Memory / Routing / Predict / Task Adapter ↔ retrieval / wiki / schema / lint / ingest).
- Concept pages: [[data-component]], [[workspace-component]], [[framework-four-components]], [[agent-infrastructure-vs-capability]], [[context-engineering]], [[distributed-cognition]].

---
*Ingested 2026-05-15. Read in full (75 lines, single gist).*
