---
type: concept
sources: [lewis2020rag, karpukhin2020dpr, anthropic2024mcp, karpathy2025wiki, rajasekaran2025, lin2022truthfulqa, matarazzo2025survey]
related_concepts: [framework-four-components, mcp-vs-skills, context-engineering, calibration-thread, learning-as-temporal-dimension, workspace-component]
related_work: [experiment-riksantikvaren, experiment-chess]
status: draft
updated: 2026-05-19
---

# Data Component

The data component answers: how does an agent reach information beyond what fits in context or what was memorised at training time?

## Four retrieval architectures

- **Inference alone.** Rely on parametric knowledge. Broad but frozen at training time, with structural hallucination at the rate of singleton facts in training data (see [[calibration-thread]]).
- **Direct tool / API.** Query the source at runtime. Always current. Pays in per-query latency and integration cost. The pattern formalised in Anthropic's Model Context Protocol [[anthropic2024mcp]] and used in [[experiment-riksantikvaren]]'s Askeladden API condition.
- **Retrieval-augmented generation.** Pre-index documents into a vector store, retrieve relevant passages at query time, feed them to the model [[lewis2020rag]], typically with dense passage retrieval [[karpukhin2020dpr]]. Re-derives knowledge on every query against a static index.
- **Compiled summary / LLM wiki.** Persistent compiled synthesis maintained across sessions [[karpathy2025wiki]]. Promising for bounded corpora; does not obviously generalise to continuously changing or very large sources.
- **Just-in-time retrieval.** Hold lightweight identifiers (file paths, queries, URLs); pull content on demand via tools, using metadata (folder hierarchy, naming convention, timestamps) as routing signals. Trades pre-computation for runtime exploration cost. [[rajasekaran2025]] is the canonical reference; Claude Code is the canonical implementation (`glob`, `grep`, `head`, `tail`, on-demand reads).

Each has a distinct cost and coverage profile. The architectures differ in *how* knowledge reaches the model; the corpus is the same. This is precisely the comparison [[experiment-riksantikvaren]] runs.

The four points form a *retrieval-target spectrum*: raw chunks (RAG) → curated synthesis (LLM Wiki) → on-demand exploration (just-in-time) → live API (direct tool). The infrastructure question is which point on the spectrum a given corpus and task profile call for, not which one is universally best.

## Storage vs. compression

This thesis takes the position that persistence across sessions is fundamentally a storage-and-retrieval problem rather than a compression problem: storage is cheap, but retrieval at the right granularity is hard. The question is how to surface the right slice of accumulated knowledge at the right moment — closely related to [[context-engineering]].

## Calibration role

Data sources verify by grounding claims against external state. RAG and direct-tool retrieval give the model an explicit, checkable reference. A compiled summary verifies less directly: the model trusts the synthesis, which trusts the underlying retrieval pass. See [[calibration-thread]].

[[lin2022truthfulqa]] gives the operational empirical evidence: WebGPT — GPT-3 plus browser access — achieves ~75% on TruthfulQA versus ~58% for the best non-retrieval prompt and ~21% for default GPT-3-175B. **Retrieval lifts truthfulness more than scale does**, on the imitative-falsehood benchmark that scale makes worse.

## Data composition determines capability — even at substrate

[[matarazzo2025survey]] §5 reports a particularly thesis-relevant finding from CoT experiments on Llama-family models: **chain-of-thought capability is correlated with the presence of code in the pre-training data mix, not with model size**. Small models with code-heavy mixes produce CoT-style reasoning; larger models without strong code mixes underperform. Data is determinative *at the substrate*, not only at runtime retrieval. Pair with [[lin2022truthfulqa]] (data-determined imitative falsehoods) and [[lewis2020rag]] (runtime retrieval). The pattern is consistent across substrate, runtime, and post-hoc retrieval: data infrastructure is load-bearing at every layer.

## Integration spectrum

The choice between MCP (vendor-published, stable, broad consumer base) and skills (lightweight, developer-owned, one team) is taken up in [[mcp-vs-skills]]. The data component is where the choice has the most concrete consequences: a stable corpus across many consumers tends toward MCP; an evolving local index tends toward skills + scripts.

## Skill acquisition writes to data

The data component is also where learned procedures land. Phase 1 of [[experiment-chess]] is a direct test of whether the data and skills components can be filled in automatically rather than requiring manual curation. See [[learning-as-temporal-dimension]].

## The dual audience: compiled summaries serve the human, not only the agent

A point developed in [[sequoia2026karpathy]] and articulated more fully in [[interview-karpathy-analysis-2]]: compiled-summary infrastructure is not only context for the agent — it is also a *projection* of the underlying corpus that helps the human maintain enough understanding to direct the work. Karpathy's framing in the interview: *"information making it into my brain"* is the bottleneck, not the agent's output rate. A wiki re-organises raw sources into a structure that supports human comprehension while simultaneously providing the agent with persistent context across sessions. The same artefact serves both audiences.

This generalises the data component's role. RAG and direct-tool retrieval target the model's context; the compiled-summary architecture additionally targets the *human's* context. A literature page in `wiki/literature/` is read by the agent on the next ingest; it is also read by the user when revisiting a topic months later. The compiled synthesis is what survives the user's own forgetting curve. Where the agent compounds across sessions by accumulating wiki content, the user compounds across sessions by reading what the agent wrote — and asking the next question from a stronger position than they would otherwise have. *"You can outsource your thinking but you can't outsource your understanding"* names what this infrastructure preserves: the human stays load-bearing as director, and the wiki is what keeps that role tractable.

## The thesis's own knowledge base as a working instance

The knowledge base that hosts this concept page is itself an instance of the compiled-summary architecture (see [[diary/meta/2026-05-14]] for the design discussion). It departs from [[karpathy2025wiki]] on one structural point: where Karpathy collapses everything to *raw* vs *wiki*, an academic project also has substantial *user-authored* content (diary, decisions, experiment notes, scope choices) that is neither external evidence nor LLM-owned synthesis. The thesis KB therefore runs three ownership zones — `raw/` (external, immutable), user-authored folders (`diary/`, `work/`, `decisions/`, `admin/`, `archive/`, `manuscript-notes/`, `inbox/`), and `wiki/` (LLM-owned). Top-level folder structure encodes *ownership*, not content type. The wiki is one zone of three, not a container for everything.

A practical consequence visible in the directory structure: `wiki/literature/` exists (external sources need an LLM summary tailored to the project) but there is no `wiki/work/` (the user's experiment notes are already project-tailored authoring; an LLM "synthesis page" of those would just be a rewrite). Synthesis across experiments happens here in `wiki/concepts/` instead.

This is the *primary* working instance of the wiki pattern. The chess wiki below is a *second, narrower* instance with an agent rather than a human as maintainer.

## A second LLM-wiki instance in a different domain

[[experiment-chess]] structures the agent's accumulated chess knowledge as a parallel LLM wiki — openings, patterns, endgames, game-analyses — applying the [[karpathy2025wiki]] compiled-summary pattern in a second, narrower domain with the agent itself as maintainer. This is methodologically useful in two ways. First, it gives the thesis a second empirical data point for the wiki architecture: does the pattern transfer to a non-research domain when the maintainer is an agent rather than a human? Second, the wiki *is* the agent-curated corpus referenced by the chess experiment's tool-fairness rulebook (see [[skills-component]]) — retrieval over the wiki is permitted; retrieval over externally-built encyclopedias is not. The architecture choice and the methodological constraint are aligned.

---
*Framing drawn from `../../manuscript-notes/essay-pointer.md` (Essay/essay.tex §2.2, §3.5).*
