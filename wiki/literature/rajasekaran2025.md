---
type: literature
citekey: rajasekaran2025
title: Effective context engineering for AI agents
authors: [Rajasekaran, Prithvi, Dixon, Ethan, Ryan, Carly, Hadfield, Jeremy]
year: 2025
venue: Anthropic Engineering Blog (Sep 29, 2025)
raw_path: raw/literature/Rajasekaran_et_al(2025).pdf
related_concepts: [context-engineering, framework-four-components, tools-component, skills-component, data-component, workspace-component, agent-infrastructure-vs-capability]
related_work: []
status: summarized
ingested: 2026-05-15
updated: 2026-05-15
---

# Rajasekaran et al. (2025) — Effective context engineering for AI agents

## Summary

An Anthropic Applied-AI engineering post (Sep 29, 2025) that names and frames **context engineering** as "the natural progression of prompt engineering" — the discipline of curating the optimal set of tokens (system prompt, tools, examples, message history, retrieved data, memory) during inference, against the inherent constraint that LLM attention is a finite resource. The post advances three load-bearing claims: (1) **context rot** — as token counts rise, recall and reasoning degrade for architectural reasons (n² pairwise relationships, training-distribution skew toward shorter sequences); (2) good context is the *smallest possible set of high-signal tokens* — system prompts at the "right altitude," tools that are minimal and unambiguous, examples that are canonical not exhaustive; (3) **just-in-time retrieval beats pre-inference retrieval** when the agent has good tools and metadata — file paths, glob/grep, on-demand reads — because the agent can navigate the information landscape progressively, mirroring how humans use file systems and bookmarks instead of memorising corpora. For long-horizon tasks the post offers three techniques: **compaction**, **structured note-taking**, and **sub-agent architectures**. For the thesis, this is the canonical Anthropic statement of context engineering as a discipline; it operationalises [[anthropic2024mcp]] and [[zhang2025]] into a unified design vocabulary.

## Main claims

### 1. Context engineering ≠ prompt engineering — a shift in unit of work

- **Prompt engineering** is about writing the perfect system prompt for a one-shot task.
- **Context engineering** is about curating the *entire* token-state of an agent operating in a loop — system prompt, tools, MCP servers, external data, memory, message history — and doing so *iteratively, each turn*.
- The post explicitly positions the diagram from page 3 (prompt-engineering vs context-engineering) as the conceptual centre: prompt engineering has a static input; context engineering has a *curation phase* that happens "each time we decide what to pass to the model."

### 2. Context rot — the architectural argument for treating context as finite

- **Empirical:** needle-in-a-haystack benchmarks show recall degrades as token count grows. Universal across models, more gentle in some than others.
- **Architectural reasons:**
  - Transformer attention is **n² pairwise** — every token attends to every other token. More tokens = thinner attention budget per pair.
  - **Training distributions skew short.** Models have fewer specialised parameters for long-range dependencies.
  - **Position encoding interpolation** (the trick that extends context windows past training length) introduces precision loss in token-position understanding.
- **Performance gradient, not cliff.** Models remain capable at long context; they're just *less precise* for retrieval and long-range reasoning. The conclusion: context is finite even when the *window* is large.

### 3. The anatomy of effective context (system prompts, tools, examples)

**System prompts at the right altitude.** The post's most memorable visual: a spectrum from "too specific" (brittle if-else hardcoded) → "just right" (the customer-support bakery example) → "too vague" (assumes shared context). Guidance:
- Use distinct sections — `<background_information>`, `<instructions>`, `## Tool guidance`, `## Output description` — via XML or Markdown.
- Strive for the *minimal set of information that fully outlines expected behaviour*. Minimal ≠ short.
- Start with a minimal prompt on the strongest model; iterate based on observed failure modes.

**Tools that promote efficiency.**
- Self-contained, robust to error, clear in intended use.
- Input parameters: descriptive, unambiguous, play to model strengths.
- **The bloat failure mode:** "If a human engineer can't definitively say which tool should be used in a given situation, an AI agent can't be expected to do better." Tool sprawl creates ambiguous decision points the model resolves poorly. (Pairs directly with [[aizawa2025tools]].)

**Examples (few-shot) that are canonical, not exhaustive.**
- Diverse, canonical examples that portray expected behaviour.
- Don't stuff edge cases. "For an LLM, examples are the 'pictures' worth a thousand words."

### 4. Just-in-time context retrieval — the central operational shift

The most thesis-relevant section. The post distinguishes:
- **Pre-inference retrieval** (classic RAG, [[lewis2020rag]]): embed and retrieve relevant data *before* generation. Surface everything that might be relevant.
- **Just-in-time retrieval:** agent holds *lightweight identifiers* (file paths, stored queries, URLs); pulls data into context *only when needed*, via tools.

**The Claude Code example** is the recurring illustration:
- Claude Code does NOT pre-index the codebase.
- It uses `glob`, `grep`, `head`, `tail`, and on-demand file reads.
- It uses *file system metadata* (file names, folder hierarchies, timestamps) as routing signals — `test_utils.py` in `tests/` means something different than `test_utils.py` in `src/core_logic/`.

**Why this matters: progressive disclosure.** Agents "incrementally discover relevant context through exploration." File sizes hint at complexity; names hint at purpose; timestamps proxy for relevance. The agent's understanding is *assembled layer by layer*, not delivered as a frontloaded payload. This is **the same progressive disclosure principle [[zhang2025]] articulates for skills — generalised to data.**

**Trade-off explicitly named:** runtime exploration is slower than pre-computed retrieval, and requires opinionated tool design to avoid dead-ends. The hybrid model (some data pre-loaded — e.g., CLAUDE.md — plus just-in-time navigation primitives) is what Claude Code actually does.

**Where the boundary will move:** "As model capabilities improve, agentic design will trend towards letting intelligent models act intelligently, with progressively less human curation." This is a prediction the thesis can engage with.

### 5. Context engineering for long-horizon tasks

Three techniques, each suited to different task profiles:

**Compaction.**
- Summarise the conversation when approaching the context window limit; reinitialise with summary + N most-recent files.
- Preserve architectural decisions, unresolved bugs, implementation details; discard redundant tool outputs.
- **Tuning advice:** maximise recall first (capture everything that *might* matter), then iterate to improve precision.
- **Tool result clearing** is the safest, lightest-touch compaction — feature now on Claude Developer Platform.

**Structured note-taking / agentic memory.**
- Agent maintains an external notes file (NOTES.md, TODO list, memory tool) outside the context window.
- Pulled back in selectively when needed.
- **Claude playing Pokémon** is the post's striking example: thousands of steps, precise tallies ("for the last 1,234 steps I've been training my Pokémon in Route 1, Pikachu has gained 8 levels toward the target of 10"), maps of explored regions, achievement tracking, combat strategy notes — *all in external notes, not context*.
- The Sonnet 4.5 **memory tool** (public beta) gives this a first-class file-based primitive.

**Sub-agent architectures.**
- Specialised sub-agents handle focused tasks with clean context windows.
- Each sub-agent uses tens of thousands of tokens; returns a 1,000-2,000 token distilled summary.
- Lead agent stays focused on synthesis; detailed search context stays isolated.
- "Substantial improvement over single-agent systems on complex research tasks" (per the multi-agent research system post — [[martin2026managed]] is the architectural companion).

**Selection guidance:**
- Compaction → conversational back-and-forth tasks.
- Note-taking → iterative development with milestones.
- Multi-agent → complex research/analysis with parallel exploration.

### 6. The guiding principle

Three times, the post returns to one sentence: **"find the smallest possible set of high-signal tokens that maximize the likelihood of your desired outcome."** That is, treated literally, the thesis-relevant slogan of the entire post.

## Method / evidence

- **Engineering blog post**, not a paper. No formal evaluation, no quantitative benchmarks reported beyond hand-waves at internal results.
- Authority rests on Anthropic's product role and the authors' visible work on Claude Code, Sonnet 4.5 memory tool, and the multi-agent research system.
- Examples are concrete (Claude Code's glob/grep, Pokémon agent's note-taking, customer-support bakery prompt spectrum) but presented illustratively, not measured.
- The post is descriptive of *current Anthropic practice*, not prescriptive in a normative-without-evidence way; it is the team that runs this in production speaking.

## Relevance to this thesis

### 1. The canonical reference for context engineering as a discipline

The thesis already uses "context engineering" as a concept page label. **Rajasekaran 2025 is the canonical naming/framing source for that term in the Anthropic engineering canon.** Every concept-page invocation of "context engineering" should cite this post.

### 2. Operational rendering of "infrastructure-as-bottleneck"

The thesis's [[agent-infrastructure-vs-capability]] argues that the binding constraint on agent productivity is infrastructure quality, not raw model capability. Rajasekaran gives this argument a concrete operational form: *the same model performs very differently depending on how its context is curated.* The post implicitly assumes the conclusion the thesis argues for — making it strong external support.

### 3. Progressive disclosure unifies the four components

The post says progressive disclosure for data (just-in-time retrieval via file paths and globs). [[zhang2025]] says progressive disclosure for skills (description → body → resources). Together they generalise: **progressive disclosure is the design principle that ties workspace, tools, skills, and data into a single framework.** The thesis's [[framework-four-components]] page can lift this synthesis.

### 4. Context rot as the architectural argument for the entire thesis

The thesis's framing — that bigger models alone won't solve agent productivity — is supported by Rajasekaran's mechanistic argument: **transformer attention is n²; training-distribution skew is permanent; even infinite context windows still suffer context rot.** This is the most concise published statement of *why* the thesis's infrastructure focus is permanent, not transitional. Use it.

### 5. Just-in-time retrieval as the [[data-component]] modern instantiation

[[lewis2020rag]] is the canonical pre-inference retrieval reference. Rajasekaran is the canonical *just-in-time* retrieval reference. The thesis's [[data-component]] page should pair them: classic RAG and agentic-search-with-glob-grep are two design points on the same axis, with different trade-offs.

### 6. The compaction/notes/sub-agent triad as long-horizon infrastructure

The thesis's experimental work runs into context-window limits whenever tasks are long-horizon. Rajasekaran names three industry-standard responses. **The thesis's discussion of long-horizon agent infrastructure should adopt this taxonomy.**

### 7. Bloated-tool-set failure mode is a measurable productivity tax

"If a human engineer can't definitively say which tool should be used, an AI agent can't be expected to do better." This is a *testable* productivity claim: tool-set ambiguity correlates with agent errors. The thesis could design an experiment around exactly this — comparing performance on a fixed task across tool-sets of increasing ambiguity.

## Notable concepts introduced

- **Context engineering** — the post's namesake discipline.
- **Context rot** — performance degradation as context grows.
- **Attention budget** — finite resource framing for inference-time attention.
- **Right altitude** for system prompts — Goldilocks zone between brittle hardcoded logic and vague high-level guidance.
- **Just-in-time retrieval** — agent navigates with lightweight identifiers, loads on demand.
- **Progressive disclosure (for data)** — agents discover context incrementally via exploration.
- **Compaction** — summarise + reinitialise with summary.
- **Tool result clearing** — lightest-touch compaction variant.
- **Structured note-taking / agentic memory** — external notes outside context.
- **Sub-agent architectures with distillation** — sub-agents return 1-2K token summaries.

## Concept-page reconciliation

1. **`wiki/concepts/context-engineering.md`** — Rajasekaran is *the* canonical source. The page should cite it as primary, lift the context-rot mechanism, the right-altitude framing, and the three long-horizon techniques. Promote `status: draft → summarized`.
2. **`wiki/concepts/framework-four-components.md`** — combine Rajasekaran's just-in-time data retrieval with Zhang's skills progressive disclosure to argue progressive disclosure is a *cross-component design principle*.
3. **`wiki/concepts/data-component.md`** — Rajasekaran's just-in-time retrieval is the modern operational form of the data component. Pair with [[lewis2020rag]] as the pre-inference counterpart.
4. **`wiki/concepts/tools-component.md`** — bloated-tool-set warning, ambiguity-as-failure-mode, "self-contained, robust to error, clear in intended use." Pair with [[aizawa2025tools]] which is the deep version.
5. **`wiki/concepts/workspace-component.md`** — file-system-as-context-engineering (folder hierarchies, naming, timestamps as routing signals) belongs here. Rajasekaran gives the most operational statement.
6. **`wiki/concepts/agent-infrastructure-vs-capability.md`** — context-rot mechanism is the architectural justification for the thesis's main claim; cite explicitly.
7. **`wiki/concepts/skills-component.md`** — Rajasekaran name-checks skills as part of the context-state; combine with [[zhang2025]] for the full picture.

## Tensions and qualifications

- **No empirical benchmarks.** The post asserts context rot, just-in-time superiority, and the three long-horizon techniques without published numbers. Persuasive because Anthropic ships these in production, but not a controlled comparison.
- **"Do the simplest thing that works."** The post explicitly hedges: as models improve, less prescriptive engineering will be needed. The thesis should engage with this prediction rather than assume the current toolset is permanent.
- **Hybrid recommendation is under-specified.** The post says Claude Code uses a hybrid (CLAUDE.md upfront + glob/grep just-in-time), but doesn't give a principled rule for what to pre-load vs leave for retrieval. Open design question.
- **Compaction loss is acknowledged but not measured.** "Overly aggressive compaction can result in the loss of subtle but critical context whose importance only becomes apparent later." How often this matters, and how much, is left open.
- **Multi-agent architectures vs single-agent with compaction** is presented as a task-dependent choice; the actual selection criteria are vague.
- **"Context rot" needle-in-haystack evidence is contested.** Some 2024-2025 work shows specific models maintaining recall at long context; the universal-degradation claim may overstate the case for frontier models.
- **The post is Anthropic-flavoured.** Other labs may converge on different conventions. The thesis should note the framing is most cleanly applicable inside the Claude ecosystem.

## Connections

- [[anthropic2024mcp]] — the protocol layer; Rajasekaran is the *how-to-use-it-well* layer.
- [[zhang2025]] — progressive disclosure for skills; Rajasekaran is progressive disclosure for data. Pair as the operationalisation duo.
- [[aizawa2025tools]] — "Writing tools for AI agents — with AI agents," cited explicitly inside Rajasekaran. Tool-design deep dive that this post summarises.
- [[martin2026managed]] — managed-agent harness/session/sandbox architecture; Rajasekaran's compaction/notes/sub-agents are what runs inside that harness.
- [[lewis2020rag]] — classic pre-inference retrieval; just-in-time retrieval is the contrast.
- [[krishnan2025multiagent]] — Krishnan's MCP-based context management taxonomy overlaps; Rajasekaran is the cleaner, more practical statement.
- [[karpathy2025wiki]] — Karpathy's LLM Wiki proposal is in the same spirit (build infrastructure around the model); Rajasekaran is the operational sibling.
- [[simon1996artificial]] — Simon's finite-attention argument is the cognitive-science antecedent to the "attention budget" framing.
- [[hutchins1995wild]] — distributed cognition; the agent + file system + notes is a distributed-cognitive system, which Rajasekaran implicitly endorses ("mirrors human cognition: we use external organization and indexing systems").
- [[sequoia2026karpathy]] — Software 3.0 ("the context window is the program; the LLM is the interpreter") is the slogan version of what Rajasekaran articulates technically.
- [[lin2022truthfulqa]] — the helpful-prompt 21% → 58% lift is a context-engineering intervention. Rajasekaran's *anatomy of effective context* (system prompts at the right altitude, examples that are canonical not exhaustive) is the design discipline behind interventions like this.
- [[fielding2000]] — Rajasekaran's just-in-time retrieval is REST's *uniform interface* applied to the file system: identifiers are URIs (paths), representations are file contents, metadata (timestamps, names) carries hypermedia-style routing information.
- [[matarazzo2025survey]] — Matarazzo §4.5 surveys the three RAG paradigms; Rajasekaran's just-in-time retrieval sits between Naïve RAG and Modular RAG on Matarazzo's spectrum, with the routing module subsumed into the agent's tool use rather than into a separate orchestrator.
- Concept pages: [[context-engineering]], [[framework-four-components]], [[data-component]], [[tools-component]], [[skills-component]], [[workspace-component]], [[agent-infrastructure-vs-capability]].

---
*Ingested 2026-05-15. Read in full (15-page blog PDF export, content ends at page 11; remainder is site footer).*
