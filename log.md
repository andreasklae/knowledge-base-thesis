# Log

## [2026-05-13] init | knowledge-base | Initial scaffolding created

## [2026-05-13] import | existing-materials | Copied prior thesis materials into raw/, work/, manuscript-notes/
- Copied 21 PDFs and 4 markdown sources from `Essay/sources/` → `raw/literature/`
- Replaced empty `raw/literature/references.bib` with `Essay/references.bib`
- Copied `Erfan-interview/transcription.md` → `raw/interviews/erfan-transcription.md`
- Copied `Erfan-interview/Rotterdam Centraal.m4a` → `raw/interviews/erfan-rotterdam-centraal.m4a` (audio source)
- Copied `karpathy-interview/transcript.md` → `raw/interviews/karpathy-transcript.md`
- Copied `Erfan-interview/analysis.md` → `work/interview-erfan-analysis.md` (user-authored analysis)
- Copied `karpathy-interview/analysis1.md` and `analysis2.md` → `work/interview-karpathy-analysis-1.md`, `work/interview-karpathy-analysis-2.md`
- Copied `Essay/resources/extended-project-description.md` → `manuscript-notes/`
- Created `manuscript-notes/essay-pointer.md` pointing at the extended project description (not duplicated here)
- Skipped: `Essay/sources/index.md` (URL list — superseded by `raw/literature/references.bib` and the future wiki index); `Essay/` build artifacts and `essay.tex`/`essay.pdf` (manuscript, stays in place); the deleted `Anthropic-on-managed-agents.md`
- No wiki synthesis written; PDFs to be read one-by-one in a later session

## [2026-05-13] ingest | essay | Extracted Essay/essay.tex into concepts, work, manuscript-notes, decisions
Synthesised from `../Essay/essay.tex` (the extended project description). PDFs in `raw/literature/` were not read — citekeys cited from the essay's references, not from the source PDFs.

Concept pages created in `wiki/concepts/` (14):
- `framework-four-components.md` — the workspace/tools/skills/data decomposition
- `workspace-component.md`, `tools-component.md`, `skills-component.md`, `data-component.md` — one per affordance
- `calibration-thread.md` — calibration as a systems property, verification mechanism
- `deterministic-tools-hypothesis.md` — limit case of the calibration mechanism
- `mcp-vs-skills.md` — integration spectrum
- `context-engineering.md` — finite attention budget, just-in-time retrieval
- `incubation-as-infrastructure.md` — fixation, XY problem, substrate-independent re-implementation
- `prototypicality-bias.md` — vision LM failure mode under long-tailed domains
- `distributed-cognition.md` — Simon / Hutchins / Norman lineage
- `learning-as-temporal-dimension.md` — learning is how the four components grow
- `agent-infrastructure-vs-capability.md` — the "wrong question" umbrella claim

All 14 are `status: draft` pending one-by-one PDF passes. Each cites its sources by citekey and ends with a footnote attributing framing to `manuscript-notes/essay-pointer.md`.

Experiment pages created in `work/` (6, all `status: planning`):
- `experiment-riksantikvaren.md` — four-configuration Askeladden study (Tools + Knowledge)
- `experiment-wcag-skill.md` — WCAG audit no-skill vs. skill
- `experiment-math.md` — math three-configuration (Tools)
- `experiment-vision-landmarks.md` — 211-image landmark threefold (Eyes)
- `experiment-chess.md` — skill-acquisition trajectory + frozen-library tournament
- `experiment-incubation.md` — fixation-point three-condition intervention (Sleep)

Manuscript-notes pages created in `manuscript-notes/` (5):
- `thesis-chapter-outline.md`, `thesis-timeline.md`, `risk-register.md`, `scope-and-limitations.md`, `open-questions-future-work.md`

Decision records created in `decisions/` (3, all `status: accepted`):
- `2026-05-13-methodology-design-science.md`
- `2026-05-13-framework-committed-in-extended-description.md`
- `2026-05-13-vendor-choice-anthropic.md`

Updated `index.md` with all new pages under Concepts / Work / Decisions / Manuscript-notes headings.

Issues flagged (not silently fixed):
- The essay cites Fielding 2000 (REST dissertation) in §2.7. The PDF is in `raw/literature/Fielding(2000).pdf` but there is no `fielding2000` entry in `references.bib`. Concept page `mcp-vs-skills.md` references the missing entry in its body so the gap is visible; adding the bib entry is a small follow-up task.
- Interview-analysis files in `work/` still lack YAML frontmatter (they were copied from the originals which had none). Per CLAUDE.md they should have frontmatter; not added in this pass because they are user-authored and the user should review before frontmatter is fixed to them.

## [2026-05-13] patch | knowledge-base | Added inbox/ capture surface and process-inbox operation
- Created empty `inbox/` directory.
- Updated `CLAUDE.md` (4 edits): added `inbox/` to the user-authored list in the Three Roles section; added `inbox/` row to the Directory Reference table; added a `### Process Inbox` operation immediately before `### Lint`; revised the `### Capture` opening to note that captures can arrive either in-conversation or via `inbox/`.
- `AGENTS.md` is a symlink to `CLAUDE.md`, so it picks up all four edits automatically.
- `index.md` unchanged — `inbox/` is a workflow surface, not a catalog target.

## [2026-05-13] revise | manuscript-notes/essay-pointer.md | Reframed as extended project description, not "prior course essay"
- The earlier version of `essay-pointer.md` mislabelled `../Essay/` as a "Prior Essay (Course Essay)" that preceded the thesis. Per user clarification: `../Essay/` is the **extended project description** — the UiO-required pass/fail document that lays out the plan the thesis is written *against*. The thesis manuscript does not yet exist.
- Rewrote `manuscript-notes/essay-pointer.md` to state this clearly, explain how the knowledge base relates to the extended description (citations, experiments, decisions, manuscript-notes all derive from it), and note that the "Essay" folder name is a legacy holdover.
- Updated the corresponding line in this log (the original ingest entry, line ~14) and the `index.md` entry for `essay-pointer` to use "extended project description."
- All 20 wiki/concept and work footnotes pointing to `essay-pointer.md` are unchanged in form; they now resolve to the corrected document.

## [2026-05-14] ingest | literature corpus pass 1/2 | Group A foundational classics + Group B calibration
- Created `wiki/literature/` pages for Group A (foundational classics): `simon1996artificial`, `hutchins1995wild`, `norman2013design`, `wallas1926art`, `ericsson1993deliberate`, `sio2009incubation`.
- Created Group B (calibration / hallucination / internal state): `kalai2024hallucinate`, `guo2017calibration`, `kadavath2022know`, `sofroniew2026emotions`.
- Created Group C (retrieval): `karpukhin2020dpr`, `lewis2020rag`.
- Workflow per CLAUDE.md and user instruction: read each source in full (PDFs directly; books in chapter-by-chapter passes; Simon and Sofroniew via docling → md → synthesis → delete md; docling converter script kept at `raw/literature/pdf_to_md.py`).
- Each page follows the schema: 2-4 sentence summary, main claims, method/evidence, relevance to thesis (opinionated), notable concepts, concept-page reconciliation (flag tensions; do not silently rewrite concept pages), tensions/qualifications, connections.

## [2026-05-15] ingest | literature corpus pass 2/2 | Group D agent engineering + Group E productivity/methodology + Yin/Lin
Continued the literature ingest. Added:
- Group D (Anthropic-line agent engineering): `anthropic2024mcp`, `martin2026managed`, `krishnan2025multiagent`, `zhang2025`, `rajasekaran2025`, `aizawa2025tools`, `weber2024taxonomy`.
- Group E (productivity + vision): `peng2023copilot`, `karpathy2025wiki`, `sequoia2026karpathy`.
- Methodology: `yin2018case` (via docling → md → synthesis → delete md).
- Newly discovered: `lin2022truthfulqa` — PDF in `raw/literature/Lin(2022).pdf` but missing from `references.bib` until this pass. Page written; bib entry needs to be added.
- Pending: `fielding2000` and `matarazzo2025` (docling conversions running in background at time of writing).
- Updated `index.md` with a fully reorganised Literature section grouping pages by theme (foundational classics; calibration; retrieval; agent engineering; productivity).

### Concept-page contradictions surfaced (not auto-fixed; flagged inside each literature page)
- `weber2024taxonomy.md` — Weber's *Skills* dimension (output-property: reWrite/Create/conVerse/Inform/Reason/Plan) is *not* the same concept as Zhang's *Skills* (packaging mechanism). `wiki/concepts/skills-component.md` should disambiguate before being promoted from draft.
- `lin2022truthfulqa.md` — direct empirical pair to `kalai2024hallucinate`. `wiki/concepts/calibration-thread.md` should cite both; theoretical lower bound + empirical demonstration.
- `karpathy2025wiki.md` — the thesis's own knowledge-base architecture *is* the LLM Wiki pattern. Operational rather than contestable, but worth surfacing in `data-component` and `workspace-component`.
- `aizawa2025tools.md` — Slack tools 67.4% → 80.1% and Asana 79.6% → 85.7% under Claude-assisted tool optimisation. Direct empirical anchor for `agent-infrastructure-vs-capability` (cite Slack/Asana numbers).
- `rajasekaran2025.md` — *progressive disclosure for data* (just-in-time retrieval) unifies with Zhang's *progressive disclosure for skills* into a cross-component design principle for `framework-four-components`.
- `martin2026managed.md` — naming convention "brain / hands / session" is a clean alternative to Krishnan's 6-layer architecture; both worth comparing in `framework-four-components`.

### Bibliography gaps surfaced
- `Lin(2022).pdf` (TruthfulQA) — present in `raw/literature/` but no entry in `references.bib`. Needs `lin2022truthfulqa` entry.
- `Fielding(2000).pdf` — present, no entry in `references.bib`. Needs `fielding2000` entry (issue carried over from earlier log entry).
- `Matarazzo(2025).pdf` — present, no entry in `references.bib`. Identification of the paper is itself pending the docling conversion.
- Orphan citekeys (in bib, no PDF): `cac2023interim`, `rooprai2026pentagon`, `lu2025deepseek` — no synthesis page possible without source.

## [2026-05-15] ingest | literature corpus pass 2/2 close-out | Fielding + Matarazzo
After the docling conversions completed in background, wrote the final two literature pages:
- `wiki/literature/fielding2000.md` — REST dissertation; reframed for agent-infrastructure context. The *constraints-induce-properties* methodology and the four interface constraints (identification / representations / self-descriptive / HATEOAS) are presented as the methodological ancestor of MCP and of the thesis's four-component framework.
- `wiki/literature/matarazzo2025survey.md` — comprehensive 2025 LLM survey by Matarazzo (Expedia) & Torlone (Roma Tre). Used primarily as a substrate citation surface; the original §5 empirical contribution (CoT capability driven by code in pre-training data, not by model size) is highlighted as data-component support; §4.4.5 LLM-modulo framework is highlighted as deterministic-tools-hypothesis support.

Added bib entries: `fielding2000` (@phdthesis), `matarazzo2025survey` (@article). Both md conversions deleted after synthesis per workflow.

Updated `index.md` Literature section with two new themed sub-headings ("Architecture / protocol heritage" for Fielding; "Substrate survey" for Matarazzo).

### Final state — literature ingest complete
- **26 literature pages** in `wiki/literature/` (all sources from `raw/literature/` with citekeys identifiable).
- All pages follow the schema (frontmatter + summary + main claims + method/evidence + relevance to thesis + notable concepts + concept-page reconciliation + tensions + connections).
- `references.bib` updated for all three previously missing entries (`lin2022truthfulqa`, `fielding2000`, `matarazzo2025survey`).
- Orphan bib entries (no PDF): `cac2023interim`, `rooprai2026pentagon`, `lu2025deepseek` — flagged; no synthesis page possible.
- `pdf_to_md.py` and `.docling-venv/` retained for future use.

### Aggregated concept-page edit recommendations (surfaced; not auto-applied)
- `wiki/concepts/skills-component.md` — disambiguate Weber-Skills (output dimension) vs Zhang-Skills (packaging) before promoting from draft.
- `wiki/concepts/calibration-thread.md` — cite `kalai2024hallucinate` (theoretical) + `lin2022truthfulqa` (empirical) as the primary pair.
- `wiki/concepts/framework-four-components.md` — restructure using Fielding's constraint-derivation methodology (null state → add constraint → induced property → trade-off); add cross-component progressive-disclosure synthesis from Zhang + Rajasekaran.
- `wiki/concepts/tools-component.md` — cite `aizawa2025tools` Slack/Asana numbers as empirical anchor; pair with `fielding2000` for REST-inheritance argument.
- `wiki/concepts/deterministic-tools-hypothesis.md` — add `matarazzo2025survey` §4.4.5 LLM-modulo framework as planning-domain operational form (Blocksworld 28% → 82%; travel-planning 0.7% → 4.2%).
- `wiki/concepts/data-component.md` — three-point retrieval-target spectrum: raw chunks ([[lewis2020rag]]) → curated synthesis ([[karpathy2025wiki]]) → on-demand exploration ([[rajasekaran2025]]); also Matarazzo §5 CoT-by-code.
- `wiki/concepts/agent-infrastructure-vs-capability.md` — cite Aizawa empirical numbers; cite Karpathy ecosystem-level *agent-native infrastructure* argument; cite Fielding's *properties induced by infrastructure constraints* methodology.
- `wiki/concepts/workspace-component.md` — `rajasekaran2025` glob/grep/timestamps as routing signals; `karpathy2025wiki` Obsidian-as-IDE pattern.

## [2026-05-15] lint + strengthen | wiki | Comprehensive cross-reference pass after corpus ingest
Goal: now that all 26 literature pages exist, ensure the concept and literature layers actually use the new material rather than treating it as appendix.

### Concept pages — all 14 strengthened (still `status: draft` per user instruction)
Every concept-page `sources:` array updated to include all newly-ingested literature it cites. Each concept page received new body sections grounding recent industry literature in the thesis's vocabulary:
- `calibration-thread.md` — added `lin2022truthfulqa` (empirical pair to Kalai) and `aizawa2025tools` (UUIDs→semantic-IDs as a tool-layer calibration intervention).
- `framework-four-components.md` — added Weber-vs-Zhang Skills disambiguation; *constraint-derivation methodology* section grounded in Fielding; *progressive-disclosure as cross-component principle* section combining Zhang and Rajasekaran.
- `tools-component.md` — added Aizawa's Slack/Asana empirical anchor + Aizawa's *contract-across-the-boundary* framing; *protocol heritage* section linking MCP to Fielding's REST constraints.
- `prototypicality-bias.md` — previously had empty sources; added `lin2022truthfulqa`, `kalai2024hallucinate`, `sofroniew2026emotions` with body section connecting vision-prototypicality to imitative-falsehood literature.
- `data-component.md` — extended retrieval architectures to four (added just-in-time retrieval via Rajasekaran); added *retrieval-target spectrum* framing; added Matarazzo §5 (CoT-by-code) and Lin (WebGPT result) to calibration discussion.
- `agent-infrastructure-vs-capability.md` — *direct empirical anchors* section (Aizawa 67.4→80.1, Lin 21→58, Martin TTFT 60-90%); *agent-native infrastructure* section grounded in Karpathy; *properties induced by infrastructure* section grounded in Fielding.
- `workspace-component.md` — *filesystem as routing infrastructure* (Rajasekaran); *LLM Wiki as workspace architecture* (Karpathy).
- `skills-component.md` — *Weber-vs-Zhang disambiguation*; eval-driven authoring discipline (Aizawa).
- `deterministic-tools-hypothesis.md` — three empirical anchors (LLM-modulo Blocksworld 28→82, TruthfulQA WebGPT, Aizawa contract framing).
- `context-engineering.md` — Software 3.0 framing (Karpathy); long-horizon techniques (Rajasekaran compaction/notes/sub-agents); token-efficiency at tool layer (Aizawa).
- `mcp-vs-skills.md` — Fielding as protocol-design ancestor; Weber-Skills disambiguation; authoring-discipline-is-orthogonal section.
- `distributed-cognition.md` — contemporary instantiations section (Rajasekaran's *file system as external organisation*; Karpathy's *Memex with maintenance solved*).
- `incubation-as-infrastructure.md` — adjacent industry framings (Matarazzo System 1/2; Rajasekaran's three long-horizon techniques as partial incubation substrates).
- `learning-as-temporal-dimension.md` — eval-driven loop as accumulating tool-side infrastructure (Aizawa); wikis as accumulating data-side infrastructure (Karpathy).

### Literature pages — strengthened cross-references
Added Fielding and Matarazzo backlinks to 18 of 26 literature pages where the connection is substantive (not mechanical). Also strengthened existing connections lists with the post-ingest set: Lin↔Kalai pair; Karpathy↔Sequoia continuity; Hutchins/Norman/Simon ↔ contemporary instantiations; Aizawa↔Lin (UUID intervention); Kadavath↔Lin (introspective vs surface tension).

### Lint findings
- **Zero broken wikilinks.** All `[[citekey]]` references resolve.
- **Zero orphan files.** Every page receives at least one inbound link.
- The two previously-orphan `interview-karpathy-analysis-{1,2}` pages now linked from `sequoia2026karpathy` (their source transcript) via `related_work` frontmatter + body connection.
- Status of all 14 concept pages remains `status: draft` per user-ownership convention; promotion to `summarized` is a user decision.

## [2026-05-16] capture | experiment-chess | Architecture, methodology, and tool-fairness rulebook settled
Long discussion with Claude on the chess experiment's implementation surface. No code yet; this entry records what was settled and where it lives.

### Diary
- Created `diary/2026-05-16.md` — full record of the discussion: standards survey (FEN/PGN/SAN/UCI), library choice (python-chess), UI choice (chessground), backend architecture (FastAPI orchestrator + Player abstraction with Human/Engine/Agent implementations), logging schema (files-in-git: CSV + per-game PGN/JSON, queried with pandas), tool-fairness rulebook (mechanics tools always allowed; retrieval tools allowed iff corpus is agent-curated), white-only methodology across both phases with gauntlet-vs-shared-pool tournament structure, and the parallel chess LLM-wiki for the agent's knowledge.

### Work
- `work/experiment-chess.md` — substantial extension. Added: Methodology (white-only across both phases, time controls excluded), Implementation architecture (full stack table, Player abstraction, logging schema with rationale for `skill_repo_sha` and batch definition), Tool-fairness rulebook (formalised the mechanics-vs-knowledge distinction; Stockfish/Lichess post-game-only constraint), Knowledge structure section (parallel LLM wiki for chess), and Open items before build starts. Frontmatter `sources` extended with `karpathy2025wiki`; `updated` bumped.

### Concepts (consolidated, not rewritten)
- `wiki/concepts/skills-component.md` — added "The skill-corpus boundary as a methodological line" section grounding the corpus-curation rule developed in the chess experiment as a general principle for any skill-acquisition study. Added `deterministic-tools-hypothesis` to `related_concepts`.
- `wiki/concepts/deterministic-tools-hypothesis.md` — added "Keeping the engine-during-play boundary clean" (why Stockfish must be post-game-only for Configs 1 and 2) and "Comparison via shared opponents, not head-to-head" (the methodological consequence of white-only training for Phase 2 tournament structure). Added `skills-component` to `related_concepts`.
- `wiki/concepts/learning-as-temporal-dimension.md` — added "Batches as the operational unit of learning" (the skill-repo-SHA-per-batch design makes the learning loop observable and reversible) and "The agent's wiki as a second instance of the pattern" (chess wiki as second-domain test of karpathy2025wiki). 
- `wiki/concepts/data-component.md` — added "A second LLM-wiki instance in a different domain" section (the chess wiki is both a second wiki-pattern test *and* the agent-curated corpus that the tool-fairness rulebook relies on; the architecture and the methodological constraint are aligned). Added `experiment-chess` to `related_work`.

### Decisions
Not yet promoted. The diary flags that the tool-fairness rulebook should be promoted to a proper decision record under `decisions/` before Phase 1 begins; user to confirm.

### Lint
- All new `[[wikilinks]]` resolve to existing files: `experiment-chess`, `diary/2026-05-16`, `skills-component`, `deterministic-tools-hypothesis`, `learning-as-temporal-dimension`, `data-component`, `karpathy2025wiki`, `risk-register`, `manuscript-notes/essay-pointer`.
- No new orphan pages introduced.
- Status of all touched concept pages remains `status: draft` per convention.
