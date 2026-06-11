# Log

## [2026-06-02] capture + lint | module-skillful-agent work page + KB lint pass | Added the harness as a tracked module; full link-integrity / orphan / index pass
- Created `work/module-skillful-agent.md` — the agent harness as a first-class module (was referenced in diary frontmatter but had no page): what it is, why it's in the thesis, architecture essentials (progressive disclosure, scripts-as-typed-tools, path-based read_reference, configurable tool surface), how experiments consume it, evolution log, files/paths.
- Wired backlinks: added `module-skillful-agent` to `related_work` of `work/experiment-chess.md` and `work/module-llm-server.md`; added it to `index.md` (Modules) and `OVERVIEW.md` (supporting infrastructure).
- Lint pass: 0 genuine dead wikilinks (62 raw hits were all syntax examples in CLAUDE/AGENTS/ADRs, append-only log history, or valid bare-stem diary links); 0 unresolved frontmatter `related_*`/`sources`; 0 orphan concept/work pages; index.md catalogs every page; AGENTS.md→CLAUDE.md symlink intact.
- Fixed one schema/data mismatch surfaced by the lint: `wiki/concepts/tools-component.md` lists grey-lit citekeys (`mirko2026gemma`, `mayo2026gemma4tools`) in `sources:` that have wiki pages but no bib entry — clarified in `CLAUDE.md` that grey-lit citekeys are valid `sources` without a references.bib entry.

## [2026-06-02] capture | SDK system-prompt slim + contradiction sweep | Slimmed the harness system prompt, tidied rule-stripping, purged stale run_script/doubling references
- skillful-agent: slimmed `system_prompt.md` to harness essentials and removed the stale `run_script` tool description; documented that skill scripts appear as typed tools `<skill>__<script>` after `use_skill` (`188c841`).
- Made the disabled-tool prompt stripper renumber surviving rules 1..N and collapse blank lines; added `tests/test_system_prompt.py` (`556af8e`). SDK now at 151 tests.
- Contradiction sweep for abandoned decisions: fixed lingering `run_script` references in SDK `CLAUDE.md`, `README.md`, and both bundled native skills (`web-search`, `learner` SKILL.md + script docstrings) to the typed-tool syntax; corrected the stale SDK test count (109→151). Found and fixed a real in-code contradiction in the chess experiment: `app/elo.py`'s module docstring described the superseded **doubling** matchmaking rule that `step_from_streak` (same file) says it replaced with single-step ([[2026-05-26-single-step-matchmaking]]); fixed it and a matching pointer in `app/batch_service.py`.
- Appended the day's wiki-scaffolding strand to `diary/experiment-chess/2026-06-02.md` (the open harness entry) and broadened its title; added `data-component`, `skill-acquisition-loop`, `tool-fairness` to its touched_concepts.

## [2026-06-02] capture | chess wiki scaffold + read_reference SDK change | Built the wiki skeleton in the chess skill; reworked read_reference to be path-based
- skillful-agent: reworked `read_reference` to take a `path` (subfolders, path-jailed) instead of a flat-allowlisted filename; committed + pushed (`435fa8d`), added `tests/test_read_reference.py`. Updated SDK CLAUDE.md row.
- Resynced the chess experiment's `skill-agent` git pin (`aba275f`→`435fa8d`), picking up both the path-based `read_reference` and the earlier `run_script`→typed-tools (`chess__<name>`) change.
- Built the wiki skeleton at `experiments/chess/backend/skills/chess/references/`: top `index.md` (routing decision-tree), `log.md`, six folder indexes (openings, principles, strategic-thinking{,/pawn-structures}, patterns{,/mating-patterns}, endgames, game-analyses), each with a "Read with" column showing the `read_reference` call. One verified seed page (`patterns/mating-patterns/back-rank-mate.md`, FEN checked as mate in python-chess) to validate the page contract.
- Added `scripts/search_wiki.py` (→ `chess__search_wiki`): keyword search returning path + frontmatter + the exact `read_reference` call, never bodies. Dropped the transient `read_wiki.py` (read_reference is the page reader).
- Rewrote chess `SKILL.md` from `run_script(...)` to typed-tool syntax (`chess__make_move(move=, reasoning=)` etc.); fixed runtime error strings + docstrings in `make_move.py`/`imagine_move.py`; fixed backend move-detection (`_committed_move_from_result` keys on `chess__make_move`, not a `run_script`+filename check); updated `_DISABLED_TOOLS` (re-enabled `read_reference`, disabled `list_skill_files`) and the system prompt.
- Updated chess `CLAUDE.md`: rewrote tool list + added the wiki-maintenance section (tutor-as-maintainer: ingest/post-game/lint ops, page contract, verify-every-claim rule).
- Updated `decisions/2026-06-02-chess-agent-wiki-architecture.md` §2 with the corrected retrieval mechanism (path-based read_reference + search_wiki) and the SDK-change implementation note.
- Next: ingest content into `strategic-thinking/` and `patterns/mating-patterns/`.

## [2026-06-02] capture | chess agent wiki architecture + tool-fairness ADR | Fixed wiki architecture, search contract, and promoted tool-fairness rulebook to an ADR
- Created `decisions/2026-06-02-chess-agent-wiki-architecture.md` — references/-as-wiki, index-as-decision-tree retrieval, search_wiki.py returns path+frontmatter only (never bodies), required one-line `description:` field, ~400-word page cap, draft→tested status, read-only-during-play, hand-seeding strategy, fairness reframing (tutored deliberate practice)
- Created `decisions/2026-06-02-tool-fairness-rulebook.md` — promoted the rulebook from work-page/concept-page to a citable ADR (mechanics always; retrieval iff agent-curated; calculation agent-driven; engines/Lichess post-game only); licenses the pre-seeded wiki via the reading-and-noting clause
- Updated `wiki/concepts/tool-fairness.md` — Status now points to the ADR; added related_decisions; updated date
- Updated `work/experiment-chess.md` — rewrote §"Knowledge structure"; added §"Future work / ideas" (in-game note() tool → raw/; Lichess post-game analysis pass); closed both wiki-architecture and tool-fairness open items; updated frontmatter
- Updated `index.md` — added both decision records under experiment-chess methodology
- No wiki pages built yet — next step is hand-seeding the chess skill's references/ (indexes + first strategic-thinking/ and mating-patterns/ pages)

## [2026-06-01] query | skillful-agent + chess + eX3 contract | Read source to trace skill loading, script execution, and system contract end-to-end
- Read skill_agent/registry.py, agent.py, skill_tools.py, server/app.py, server/config.py
- Read experiments/chess/backend/app/agent_player.py
- Synthesis delivered in conversation; no new KB pages created (no new synthesis beyond existing concept pages)

## [2026-06-01] capture | pydantic-ai vLLM profile fix | Documented and applied two-profile-flag fix for Gemma 4 / vLLM
- Created `wiki/concepts/gemma4-vllm-pydantic-ai-integration.md` — three-layer stack, native tool format, vLLM flags, profile mismatches, thinking channel mechanics
- Updated `wiki/work/module-llm-server.md` — added profile configuration section
- Applied fix in `software/skillful-agent/server/app.py:_build_agent` and `experiments/chess/backend/app/agent_player.py:_build_agent`
- Created `decisions/2026-06-01-pydantic-ai-vllm-profile.md`
- Created `diary/experiment-chess/2026-06-01.md`
- Updated `index.md` — added concept page entry and decision record

## [2026-06-01] capture | discussions schema | Added raw/discussions/ folder type to KB; processed first discussion file
- Updated `CLAUDE.md` — added `raw/discussions/` row to directory table and capture-routing rule
- Updated `index.md` — added Discussions section
- Updated `wiki/concepts/mcp-vs-skills.md` — rewrote with MCP transport mechanics, state/knowledge split, "ship with the skill", lazy-typed-tools synthesis, analogues
- Created `wiki/concepts/capability-delivery-dimensions.md` — six axes, pre-paradigmatic assessment, HCI analogues, three-party interface model
- Appended to `admin/ideas.md` — harness auto-wrapping bundled scripts as lazy-revealed typed tools

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

## [2026-05-14] capture | diary/2026-05-14 | KB design session — three-zone ownership model, inbox-with-deletion, no wiki/work asymmetry

Diary entry processed (backdated; entry written on the day it describes, processed 2026-05-16). The entry is the design rationale for this knowledge base itself, tagged `meta-observation`. Created the diary file and propagated the load-bearing design points to three concept pages.

### Diary
- Created `diary/2026-05-14.md` — full record of the design discussion: PDFs-stay-as-PDFs, central BibTeX, per-working-day diary cadence, retention of `raw/` for the immutability invariant, three-roles model (external / user-authored / LLM-compiled) as the refinement of Karpathy's two-zone framing, mutability rules per zone, the coverage-check destination map, the `wiki/literature/`-but-no-`wiki/work/` asymmetry, the four-then-five operations (added Process Inbox with on-success deletion), the meta-observation framing of the KB as case material for the thesis's Knowledge component. `touched_concepts: [data-component, workspace-component, agent-infrastructure-vs-capability, framework-four-components]`. `tags: [meta-observation]`.

### Concepts (additions, not rewrites)
- `wiki/concepts/data-component.md` — added "The thesis's own knowledge base as a working instance" section: positions the thesis KB as the *primary* working instance of the compiled-summary pattern (with the chess wiki as the second), and records the three-zone refinement of Karpathy's two-zone model along with the architectural reason for `wiki/literature/` existing while `wiki/work/` does not.
- `wiki/concepts/workspace-component.md` — added "Ownership zones structure the workspace" section: formalises the three ownership zones as a workspace-design pattern, with the rationale "top-level folder structure encodes ownership, not content type." Frames the property at stake as *whose voice the page represents* — a workspace property for research records, not just retrieval substrates.
- `wiki/concepts/agent-infrastructure-vs-capability.md` — added "The thesis's own workflow as latent case material" section: ties the `meta-observation` tag to the framework's claim, noting that the maintaining agent's operations (ingest, capture, propagate, lint, process inbox) instantiate the data and skills components the framework attributes infrastructure dominance to.

### Decisions
Not promoted yet. The diary contains several decision-record-quality moves that the user may want as formal ADRs under `decisions/`: the three-ownership-zone ownership model, the inbox-with-deletion / no-processed-folder design, the `wiki/literature/` vs `wiki/work/` asymmetry, the per-working-day diary cadence. Decision records are durable; awaiting user confirmation before creating any.

### Index
- Not updated. Index does not catalog diary entries (user-authored content); only literature, concepts, work, decisions, and manuscript-notes appear there.

### Lint
- All new `[[wikilinks]]` resolve: `karpathy2025wiki`, `experiment-math`, `diary/2026-05-14`, `experiment-chess`, `skills-component`.
- No new orphan pages introduced.
- `updated:` dates on touched concept pages set to `2026-05-14` (matching the date of the source diary entry, per user instruction that propagation dates reflect when the source content was authored).
- Status of all touched concept pages remains `status: draft` per convention.

## [2026-05-16] schema | CLAUDE.md | Added raw/other/ to the directory reference and revised the Ingest workflow

User created `raw/other/` for non-academic external sources (gists, blog posts, web articles, slide decks, talks). Updated the schema accordingly.

### Schema
- `CLAUDE.md` Directory Reference — added `raw/other/` row.
- `CLAUDE.md` Ingest workflow — rewritten in eight steps. Notable changes:
  - Added a duplicate-check as step 1 (search `wiki/literature/` for existing citekey; search `raw/` for the same content under another filename or folder). Motivated by today's near-miss: a copy of the Karpathy gist appeared in `raw/other/` even though `raw/literature/Karpathy(2025).md` was already ingested as `karpathy2025wiki`.
  - Added a clause for `raw/other/` sources: no BibTeX entry; wiki page still lives under `wiki/literature/<citekey>.md` (one folder for all summary pages keeps the index structure); `venue:` frontmatter records the actual venue (e.g. `GitHub Gist (idea file)`, `Personal blog`, `YouTube`).
  - Fixed a stale citekey in the example log entry (`kalai2024calibration` → `kalai2024hallucinate`) and the corresponding concept page (`calibration.md` → `calibration-thread.md`).

### Decisions
- Created `decisions/2026-05-14-three-zone-ownership-model.md`. Promotes the foundational architectural choice from [[diary/2026-05-14]] to a formal ADR. Context, decision, consequences. Linked from [[data-component]], [[workspace-component]], and [[karpathy2025wiki]] via wikilinks in the body. Status: `accepted`. The other diary candidates (inbox-with-deletion, no `wiki/work/` asymmetry, per-working-day diary cadence) are operational rather than architectural; they live in the schema and do not need separate ADRs.

### Index
- `index.md` Decisions section — added the new ADR.

### Lint pass 1 (after schema + decision edits)
- **Fixed** two non-canonical wikilinks: `[[calibration-thread.md]]` in `wiki/literature/guo2017calibration.md` and `wiki/literature/kadavath2022know.md` normalised to `[[calibration-thread]]`. These are LLM-owned literature pages; safe to edit.
- **Flagged, not fixed**: six path-style wikilinks of the form `[[../path/file.md]]` in `work/experiment-incubation.md`, `work/experiment-riksantikvaren.md`, `work/experiment-chess.md`, and `work/experiment-vision-landmarks.md`. They all resolve to real targets but violate the bare-slug convention specified in the schema. Held off on fixing because these are user-authored files; awaiting user permission to normalise.
- **Flagged, not fixed**: three interview-analysis pages (`work/interview-erfan-analysis.md`, `work/interview-karpathy-analysis-1.md`, `work/interview-karpathy-analysis-2.md`) lack YAML frontmatter entirely. They predate the schema. Adding frontmatter is structural rather than substantive, but the body preservation norm is strong. Awaiting user permission before touching them.
- **Inbox**: `inbox/Untitled.md` exists but is empty (Obsidian artefact). Nothing to file; left in place.
- **Orphans**: zero.
- **Frontmatter completeness**: all 14 concept pages and all 26 literature pages have `type`, `status`, `updated`.

### Exploratory pass — strengthening synthesis

Read `manuscript-notes/` (6 files), `admin/ideas.md` (empty), and the two unread `work/interview-karpathy-analysis-*` files. The Karpathy analyses contain framings that the [[sequoia2026karpathy]] wiki page captures only thinly. Two targeted additions:

- `wiki/concepts/agent-infrastructure-vs-capability.md` — added "Failures are semantic, not syntactic" section. The Stripe-vs-Google email-matching bug from MenuGen is a sharp single-example articulation of where the infrastructure-dominates claim meets the specification boundary: agent failures in production are typically not syntax errors but mistaken assumptions about identity, ownership, persistence, and security. Tools and skills can carry domain invariants into the agent's context as enforceable preconditions — one of the strongest infrastructure levers because the model cannot generate the invariants on its own.
- `wiki/concepts/data-component.md` — added "The dual audience: compiled summaries serve the human, not only the agent" section. Generalises the data component's role: a wiki page is read by the agent on the next ingest, and by the user months later when revisiting a topic. *"Information making it into my brain"* (Karpathy) is the bottleneck on human direction of agent work; the compiled-summary architecture targets the human's context budget as well as the agent's. Names the *"you can outsource thinking but you can't outsource understanding"* maxim as the human-residual property the infrastructure preserves.

Both additions cite [[sequoia2026karpathy]] and [[interview-karpathy-analysis-2]] (and the latter case [[interview-karpathy-analysis-1]] also).

### Lint pass 2 (after strengthening)
- **Broken wikilinks**: zero new. Remaining non-canonical links (six path-style in `work/`, two schema-placeholder `[[citekey]]` / `[[slug]]` inside `diary/2026-05-14.md`'s verbatim prose) unchanged — preserved deliberately per voice-of-authorship norm.
- **Orphans**: zero.
- **Frontmatter**: complete on all wiki pages; three interview pages still missing (flagged above).
- **Status drift**: not checked deeply — all `work/experiment-*` pages show `status: planning` which matches their being pre-execution. No experiment has reported in-progress status without a recent diary touch.
- All new `[[wikilinks]]` resolve: `sequoia2026karpathy`, `interview-karpathy-analysis-1`, `interview-karpathy-analysis-2`, `calibration-thread`, `diary/2026-05-14`, `data-component`, `workspace-component`, `karpathy2025wiki`, `experiment-chess`, `skills-component`.
- `updated:` dates: data-component bumped to 2026-05-14 (composite — entry from 05-14 plus today's strengthening derived from same Karpathy material); agent-infrastructure-vs-capability bumped to 2026-05-14 likewise.

## [2026-05-16] lint | knowledge-base | Normalised work/ wikilinks and added frontmatter to interview pages

User delegated decision authority on the two flagged items. Did both.

### Wikilink normalisation in work/
Converted six path-style links `[[../path/file.md]]` to canonical bare-slug `[[slug]]` form. Targets unchanged; only syntax. Files touched:
- `work/experiment-incubation.md` — `[[../decisions/2026-05-13-methodology-design-science.md]]` → `[[2026-05-13-methodology-design-science]]`.
- `work/experiment-chess.md` — three distinct targets normalised via replace_all: `[[../manuscript-notes/risk-register.md]]` → `[[risk-register]]`, `[[../manuscript-notes/open-questions-future-work.md]]` → `[[open-questions-future-work]]`, `[[../diary/2026-05-16.md]]` → `[[diary/2026-05-16]]`.
- `work/experiment-riksantikvaren.md` — `[[../manuscript-notes/risk-register.md]]` → `[[risk-register]]`.
- `work/experiment-vision-landmarks.md` — three on one line: `[[../wiki/concepts/prototypicality-bias.md]]` → `[[prototypicality-bias]]`, `[[../wiki/concepts/calibration-thread.md]]` → `[[calibration-thread]]`, `[[../manuscript-notes/open-questions-future-work.md]]` → `[[open-questions-future-work]]`.

Left intact: two `[[citekey]]` / `[[slug]]` placeholders inside `diary/2026-05-14.md` — they are verbatim schema-illustrative prose inside the user's authored diary entry; replacing them would corrupt the entry's meaning.

### Frontmatter added to interview-analysis pages
All three pages predated the schema. Added minimal frontmatter without touching body content:

- `work/interview-erfan-analysis.md` — `type: interview`, `status: complete`, related_concepts spanning skills-component / incubation-as-infrastructure / context-engineering / framework-four-components, related_work to experiment-incubation and experiment-wcag-skill. `updated: 2026-05-13` (the page's apparent vintage).
- `work/interview-karpathy-analysis-1.md` — `type: interview`, `status: complete`, broad related_concepts (the page touches most of the framework), related_work cross-links to analysis-2 and the four experiments whose framing it grounds, sources: [sequoia2026karpathy, karpathy2025wiki]. `updated: 2026-05-15`.
- `work/interview-karpathy-analysis-2.md` — similar; analysis-2 also adds tools-component to related_concepts and experiment-riksantikvaren to related_work given its stronger verifiability emphasis. `updated: 2026-05-15`.

### Lint pass 3 (final, post-normalisation)
- **Broken wikilinks**: zero, excluding the two `[[citekey]]` / `[[slug]]` schema placeholders inside the verbatim diary prose (these are by-design, not navigation links).
- **Orphans**: zero across all 14 concept pages and all 26 literature pages.
- **Frontmatter completeness**: all wiki pages have required fields; all work/ pages now have YAML frontmatter; all decisions have required fields.
- **Status drift**: none flagged; no in-progress experiments without recent diary activity.

KB is in a healthy state heading into the next ingest. Suggested next action when ready: ingest a first literature source end-to-end through the revised 8-step workflow (with duplicate-check) to validate it.

## [2026-05-18] capture | experiment-chess | Phase 1 frontend/backend scaffold implemented

### Experiment docs
- Updated `experiments/chess/README.md` with current run commands, singleton current-game API, frontend refresh semantics, and Maia setup status.
- Updated `experiments/chess/backend/README.md` to document the backend-owned current game (`GET /api/game`, `POST /api/game/moves`, `GET /api/game/events`) and the deferred persistence/progress tracker.
- Updated `experiments/chess/frontend/README.md` to state that the frontend loads the current backend-owned game on refresh.
- Created `experiments/chess/diary/2026-05-18.md` with local implementation notes.

### Knowledge base
- Created `diary/2026-05-18.md` — records the Phase 1 scaffold implementation: FastAPI + python-chess backend, React/Vite/chessground frontend, human/Maia-only testing surface, local Lc0 + Maia-1 weights, chessground `viewOnly` fix, singleton backend state model, validation results, and deferred items.
- Updated `work/experiment-chess.md` — status moved to `in-progress`; added 2026-05-18 scaffold status and path pointer to `experiments/chess/`; updated Maia open item now that local Lc0 + weights are installed for testing.
- Updated `wiki/concepts/workspace-component.md` — added "Source-of-truth boundaries inside an experimental workspace" section using the singleton backend game correction as a workspace/source-of-truth example.

### Validation
- Backend tests: `uv run pytest` — 14 passed.
- Frontend build: `npm run build` — passed.

## [2026-05-18] capture | experiment-chess | Game lobby + JSON persistence added

### Knowledge base
- Updated `diary/2026-05-18.md` — appended second session record covering the lobby/persistence work.

### Experiment changes (summary)

**Backend:**
- Created `app/persistence.py` — JSON file store; one file per game at `games/<game_id>.json`; atomic writes; `games_dir` passed explicitly to all functions (no global state).
- Extended `app/game_service.py` — `Game` gains `created_at`; `_push_move` persists after every move; new methods `load_game`, `list_summaries`, `delete`; startup auto-loads most-recent game.
- Added `GameSummary` schema to `app/schemas.py`.
- Added `games_dir` setting to `app/config.py`.
- Added three endpoints to `app/main.py`: `GET /api/games`, `POST /api/games/{id}/load`, `DELETE /api/games/{id}`.
- Updated `tests/test_backend.py`: all calls pass `tmp_path` as `games_dir` for test isolation; updated one assertion; added three new tests. 17/17 passing.

**Frontend:**
- Added `react-router-dom`; two routes: `/` → `LobbyPage`, `/games/:gameId` → `BoardPage`.
- New `LobbyPage.tsx` — game list with status, move count, last move, date; inline new-game form; Open/Delete per row.
- New `BoardPage.tsx` — board + status panel; calls `loadGame` on mount for URL-navigation correctness; back link to lobby.
- `App.tsx` replaced with router shell.
- Lobby CSS added to `styles.css`.
- `npm run build` — TypeScript clean, production build passed.

## [2026-05-18] capture | experiment-chess | Bug fix + game-over display

### Knowledge base
- Updated `diary/2026-05-18.md` — appended third session record.

### Experiment changes (summary)

**Bug fix — DELETE 204 crash:**
- `frontend/src/api.ts` — `request<T>()` now returns early for HTTP 204 responses instead of calling `.json()` on an empty body. Fix is generic; all future 204 endpoints benefit automatically.

**Feature — game-over banner:**
- `backend/app/schemas.py` — added `termination: str | None` to `GameState`.
- `backend/app/game_service.py` — `Game.state()` now populates `termination` from `board.outcome(claim_draw=True).termination.name` (e.g. `CHECKMATE`, `STALEMATE`, `INSUFFICIENT_MATERIAL`, etc.).
- `frontend/src/types.ts` — `GameState` interface gains `termination: string | null`.
- `frontend/src/BoardPage.tsx` — added `describeOutcome()` mapping `(result, termination)` to headline + detail + kind; renders a full-width `.result-banner` (green for win, cream for draw) between the nav panel and board when `game.status === 'finished'`; status panel Result row also shows termination in parentheses.
- `frontend/src/styles.css` — added `.result-banner`, `.result-banner.win`, `.result-banner.draw`, `.result-headline`, `.result-detail`.

## [2026-05-19] lint | knowledge-base | Diary restructure, link repair, stale-frontmatter bulk fix, two new concept pages

### Diary restructure
- Created `diary/experiment-chess/` and `diary/meta/` subfolders.
- Moved `diary/2026-05-14.md` → `diary/meta/2026-05-14.md` (cross-cutting KB design entry).
- Moved `diary/2026-05-16.md` → `diary/experiment-chess/2026-05-16.md`.
- Moved `diary/2026-05-18.md` → `diary/experiment-chess/2026-05-18.md`.
- Moved `diary/2026-05-19.md` → `diary/experiment-chess/2026-05-19.md`.
- Updated `CLAUDE.md` directory reference and frontmatter section heading to reflect new subfolder convention.

### Link repair
Updated all wikilinks that referenced old flat diary paths:
- `work/experiment-chess.md` — two links updated (`[[diary/2026-05-16]]`, `[[diary/2026-05-18]]`).
- `wiki/concepts/workspace-component.md` — `[[diary/2026-05-14]]` → `[[diary/meta/2026-05-14]]`.
- `wiki/concepts/data-component.md` — same.
- `wiki/concepts/agent-infrastructure-vs-capability.md` — same.
- `decisions/2026-05-14-three-zone-ownership-model.md` — two instances updated.
- `diary/experiment-chess/2026-05-18.md` — internal link to `2026-05-16` updated.
- `log.md` historical entries left intact (they describe creation events, not live links).

### Stale frontmatter fix
- Bulk-updated `updated:` dates on 42 files to match their filesystem mtime (prior-session drift).
- Updated `updated: 2026-05-19` on the four files touched in this session: `agent-infrastructure-vs-capability.md`, `data-component.md`, `workspace-component.md`, `work/experiment-chess.md`.

### New concept pages
- Created `wiki/concepts/tool-fairness.md` — the chess tool-fairness rulebook (mechanics always permitted; retrieval permitted iff corpus is agent-curated; Stockfish post-game only). 11 mentions across the KB had no dedicated page.
- Created `wiki/concepts/skill-acquisition-loop.md` — the self-correcting play/analyse/synthesise/batch loop; batch definition; parallel chess wiki; connection to deliberate practice and the thesis claim; current Phase 1 status.

### Propagation
- `wiki/concepts/learning-as-temporal-dimension.md` — added `skill-acquisition-loop` to `related_concepts`; added pointer to new page in "Batches" section.
- `wiki/concepts/skills-component.md` — added `tool-fairness` and `skill-acquisition-loop` to `related_concepts`.
- `index.md` — added both new concept pages under `learning-as-temporal-dimension`.

### Lint findings resolved
- **Link integrity**: zero broken wikilinks remaining in live files.
- **Orphan pages**: none.
- **Stale frontmatter**: fixed (see above).
- **Missing concept pages**: `tool-fairness` and `skill-acquisition-loop` created.
- **Status drift**: `experiment-chess` is `in-progress`; last diary mention is `diary/experiment-chess/2026-05-19.md` — current, no drift.
- **Contradictions**: none found.

## [2026-05-19] capture | experiment-chess | chesscom-driver package + backend integration

### Context
Lichess rejected on methodology grounds (untimed games impossible). Maia covers 1100-1900 ELO only. Sub-1100 opponents needed for early agent training. chess.com Engine bots span 250-3200 in 25 discrete slider positions, run untimed, and survive Cloudflare via a persistent real-Chrome profile.

### New package
- Built `experiments/chess/chesscom-driver/` as a standalone Python package (Playwright + python-chess).
- Modules: `driver.py` (browser-level `ChessComDriver`), `player.py` (`ChessComPlayer` adapter to the experiment's `Player` ABC), `mapping.py` (hardcoded 25-position ELO table + `closest_position()`), `_js.py` (chess.com DOM/JS snippets), `exceptions.py` (typed errors).
- `pyproject.toml`, `examples/basic_usage.py`, comprehensive instructional `README.md` (TOC, quickstart, integration, internals, ELO table, troubleshooting, maintenance notes for when chess.com changes the DOM).

### Backend integration (additive, guarded)
- `backend/app/schemas.py` — added `"chesscom"` to `PlayerConfig.type` literal; `CHESSCOM_MIN_ELO=250`, `CHESSCOM_MAX_ELO=3200`; validator extension.
- `backend/app/config.py` — `chesscom_user_data_dir`, `chesscom_headless`, `chesscom_chrome_channel` settings.
- `backend/app/players.py` — guarded import of `ChessComPlayer` from `chesscom_driver`; new branch in `PlayerFactory.create` and `validate_config`. Backend still imports cleanly if package is absent.

### KB updates
- `diary/experiment-chess/2026-05-19.md` — appended "Later in the day: the chesscom-driver package" section (discovery, mapping rationale, package architecture, persistent profile, backend wiring, methodological fit, verified-vs-assumed list, why a separate package); updated title and Open items.
- `work/experiment-chess.md` — Engines row in stack table now mentions chess.com Engine bots; added "Opponent pool: Maia + chess.com Engine bots" subsection after Phase 1 scaffold status.

### Verified vs assumed
- Verified manually in earlier exploration: slider control via React-compatible native setter; `board.game` API surface (`fen`, `lastMove`, `historySANs`, `isGameOver`); click-based move submission triggers bot reply (programmatic `board.game.move` does not).
- Assumed and not yet end-to-end tested in the package: persistent Cloudflare bypass over multi-day runs; auto-promote behaviour for promotion moves; recovery from mid-game disconnects. To be exercised in next session.

## [2026-05-20] capture | experiment-chess | Exposed chesscom opponent in the lobby UI for human-vs-bot testing

### Context
The `ChessComPlayer` was fully wired in the backend (`PlayerFactory`, `schemas.py`, `players.py`) but not listed in `GET /api/player-types`, so the frontend lobby never offered it as an option. User wants to play as white (human) against a chess.com Engine bot (black) to test the driver end-to-end.

### Changes
- `experiments/chess/backend/app/main.py` — added `PlayerTypeInfo(type="chesscom", elo_required=True)` to the `player_types()` response list.
- `experiments/chess/frontend/src/types.ts` — added `'chesscom'` to the `PlayerKind` union type.
- `experiments/chess/frontend/src/LobbyPage.tsx` — added `chesscom` branch to `cleanConfig()` (default ELO 800) and `formatPlayer()` (`chess.com <elo>` display string); added number-input ELO control (250–3200) to `PlayerSelector` for the `chesscom` type.

### No backend logic changes needed
All backend plumbing (`PlayerFactory.create`, `ChessComPlayer`, schema validation 250–3200) was already in place from the 2026-05-19 session.

## [2026-05-20] capture | experiment-chess | First end-to-end agent-vs-chess.com game (chess.com won by checkmate); lifecycle overhaul, DOM rediscovery

### Diary
- Created `diary/experiment-chess/2026-05-20.md` — thorough entry covering: lobby UI constraints (chesscom black-only, agent white-only, ELO dropdown of 25 ratings); frontend rendering fixes (`container-type: inline-size` + `100cqw` + `ResizeObserver` redraw); Maia silent-failure root cause (lc0 PATH, narrow exception catch, corrupt weights); browser lifecycle redesign (ephemeral temp profiles, eager launch in `create_game`, awaited cleanup at every transition, no more SingletonLock leaks); chess.com DOM rediscovery (intro modal + OneTrust banner dismissal, Engine group scrolling, scoped slider selector); BoardPage GET-first navigation.

### Work page
- Updated `work/experiment-chess.md` "Opponent pool" section with the end-of-day status: lifecycle (temp profile per game, eager launch, awaited close), restrictions (chesscom = black-only, agent = white-only), active-game GET-first workaround, first agent-vs-chess.com game completion. Removed the misleading ELO range claim ("250-3200" implied free-form; the actual coverage is 25 discrete ratings).

### Code changes (this session)
- `experiments/chess/chesscom-driver/chesscom_driver/driver.py` — `_dismiss_first_run_modal()` (intro Start → JS-hide OneTrust); `_ensure_engine_group_open()` (scroll-into-view + scoped locator + slider-inside-group wait); `_set_slider_position()` scoped to Engine group.
- `experiments/chess/chesscom-driver/chesscom_driver/player.py` — added `async def start(self)` for eager launch.
- `experiments/chess/backend/app/players.py` — `ChessComPlayer` subclass owns ephemeral temp profile and `shutil.rmtree`s it on close; `HumanPlayer`/`MaiaPlayer` signatures fixed to accept `last_san`.
- `experiments/chess/backend/app/game_service.py` — `Game.close_players()` / `Game.start_players()`; awaited cleanup at create/load/delete/game-over/shutdown; `create_game` and `load_game` now async; `_try_load_most_recent()` removed; SSE subscribe calls hoisted out of generators so 404s fire before headers.
- `experiments/chess/backend/app/schemas.py` — `CHESSCOM_ELOS` tuple of 25 ratings; `CreateGameRequest.validate_sides` rejects chesscom-as-white and agent-as-black.
- `experiments/chess/backend/app/main.py` — `chesscom` in `player_types()` with `allowed_elos`; lifespan shutdown hook calls `service.shutdown()`.
- `experiments/chess/backend/.env` — `CHESS_LC0_PATH=/opt/homebrew/bin/lc0`.
- `experiments/chess/frontend/src/styles.css` — `.board-panel { container-type: inline-size }`; `.board-frame { width/height: min(80vh, 100cqw) }`.
- `experiments/chess/frontend/src/ChessBoard.tsx` — `ResizeObserver` calling `redrawAll()`.
- `experiments/chess/frontend/src/LobbyPage.tsx` — per-color type filtering (white excludes chesscom, black excludes agent); chesscom ELO dropdown from `allowed_elos`; "Launching chess.com browser…" message during create; lobby Open just navigates (no preload).
- `experiments/chess/frontend/src/BoardPage.tsx` — GET-first then fall back to POST /load.
- `experiments/chess/frontend/src/api.ts` — added `getGame(gameId)` helper.

## [2026-05-20] decide | experiment-chess | ELO tracking, batch runner methodology, evaluation needle

### Decision record
- Created `decisions/2026-05-20-elo-and-batch-runner.md` — settled ELO formula (K=32 classical Elo), initial ELO (1200), opponent selection (win-up / loss-down / draw-down), pool-per-batch (Maia 1100–1900 OR chess.com 25 ratings), temperature (1.0, Azure default since skillful-agent doesn't set one), `skill_repo_sha` provenance (chess experiment repo HEAD), CSV schema, batch persistence, agent re-init per game, Stockfish eval needle.

### Diary
- Appended afternoon section to `diary/experiment-chess/2026-05-20.md` documenting: edge-case alignment (force-queen on chesscom underpromotion, claim_draw=False for chesscom games), ELO module, EvalService and needle UI, pause/play for agent games, batch runner backend + frontend, CSV schema fixes, agent isolation verification.

### Work page
- Updated `work/experiment-chess.md` "Logging schema" section with the as-of-2026-05-20 CSV columns (added `batch_name`, `opponent_elo`; noted only agent games are logged), batch-runner persistence files (`batches/<id>.json`, `games/agent_elo.json`), and a new "ELO methodology" subsection pointing at the decision record.

### Code (this session)
- `experiments/chess/backend/app/elo.py` — new module with K=32 classical Elo, `pick_opponent_elo` selector, `AgentEloState` persistent dataclass.
- `experiments/chess/backend/app/eval_service.py` — new EvalService wrapping Stockfish UCI via python-chess; one long-lived engine, asyncio-locked.
- `experiments/chess/backend/app/batch_service.py` — Batch model, JSON-per-batch persistence, agent ELO state persistence, `next_create_request` helper.
- `experiments/chess/backend/app/batch_runner.py` — orchestration loop, on-game-finished callback, pause/start/stop lifecycle.
- `experiments/chess/backend/app/repo_state.py` — git HEAD SHA capture, model+temperature provenance.
- `experiments/chess/backend/app/game_service.py` — pause flag, eval triggers, on_game_finished hook before CSV write, per-game `_claim_draw` (chesscom games never claim 3-fold/50-move), underpromotion→queen rewrite for chesscom games.
- `experiments/chess/backend/app/main.py` — wired EvalService + BatchService + BatchRunner via lifespan; added /pause /resume endpoints for individual games and the full /batches endpoint surface.
- `experiments/chess/backend/app/logging_service.py` — added `batch_name`, `opponent_elo` columns.
- `experiments/chess/backend/app/schemas.py` — `GameState.eval_cp`, `eval_mate`, `paused`.
- `experiments/chess/backend/app/config.py` — `stockfish_path`, `stockfish_eval_depth`, `batches_dir`.
- `experiments/chess/backend/.env` — `CHESS_STOCKFISH_PATH=/opt/homebrew/bin/stockfish`, `CHESS_STOCKFISH_EVAL_DEPTH=15`.
- `experiments/chess/frontend/src/EvalBar.tsx` — new vertical advantage needle, sigmoid mapping, mate-aware label.
- `experiments/chess/frontend/src/BatchPage.tsx` — new route `/batch`: agent ELO banner, active batch card with progress + last-10 chips + full table, create form, history list.
- `experiments/chess/frontend/src/BoardPage.tsx` — eval bar next to board, pause/resume button when agent is playing.
- `experiments/chess/frontend/src/App.tsx` — wired `/batch` route.
- `experiments/chess/frontend/src/LobbyPage.tsx` — "Batches →" link in header.
- `experiments/chess/frontend/src/api.ts` + `types.ts` — batch + agent-elo helpers, eval/paused fields on GameState.
- `experiments/chess/frontend/src/styles.css` — eval bar, pause controls, batch page styles.

### Notes
- `games/` cleared at start of session (per user request); ready for first real batch run.
- Stockfish verified locally via python-chess: starting position ≈ +49 cp, white missing rook ≈ −486 cp.
- ELO math verified by hand: K=32, draw at equal ELO is no change, etc.

## [2026-05-20] decide | experiment-chess | Matchmaking made adaptive; uv workspace restructure

### Decision record
- Revised `decisions/2026-05-20-elo-and-batch-runner.md` §1, §2, §3 covering: adaptive K-factor (40 for first 15 games, 20 after); explicit rationale for initial ELO 1200 (USCF amateur-novice convention; clarified as convention not canon); streak-based exponential-doubling opponent selection capped at 4 grid notches. Added "Revision history" section at the end of the record.

### Diary
- Appended "Late afternoon" section to `diary/experiment-chess/2026-05-20.md` covering: uv workspace restructure (`.pth`-based editable install failed silently due to en-dash in path), adaptive K + streak matchmaking implementation, initial ELO rationale, agent baseline capabilities at this commit boundary (gpt-4o-mini, temp 1.0, one skill with two scripts, no other tools), state reset before first calibration batch under the new algorithm.

### Work page
- Updated "ELO methodology" subsection in `work/experiment-chess.md` to reflect new adaptive K + streak-based opponent selection.

### Code (this session)
- `experiments/chess/CLAUDE.md` (new) — project-level operating manual; includes durable rule "never add Claude as commit co-author."
- `experiments/chess/pyproject.toml` (new) — uv workspace root declaring `backend` and `chesscom-driver` members.
- `experiments/chess/backend/pyproject.toml` — `chesscom-driver = { workspace = true }` (was a `path` source).
- `experiments/chess/backend/app/elo.py` — adaptive `k_factor()`, `update_streak()`, `step_from_streak()`, `pick_opponent_elo(agent_elo, streak, pool)` signature change, `AgentEloState.streak` field, `apply_result` now uses adaptive K and updates streak.
- `experiments/chess/backend/app/batch_service.py` — `next_create_request(batch, elo, streak)` signature change.
- `experiments/chess/backend/app/batch_runner.py` — passes `agent_state.streak` to next_create_request; logs include streak.
- `experiments/chess/backend/app/main.py` — `AgentEloResponse.streak` field.
- `experiments/chess/frontend/src/types.ts` — `AgentElo.streak` field.
- `experiments/chess/frontend/src/BatchPage.tsx` — agent-ELO banner shows streak when non-zero.

### Verified
- Unit-style assertions on `k_factor`, `update_streak`, `step_from_streak`, `pick_opponent_elo`, `update_elo`, `AgentEloState.apply_result`.
- Simulated 20-game calibration sequence (true ELO 300 agent vs chess.com pool, true Elo win-probability): bracketed correctly by game 8.
- Backend imports + chesscom-driver imports clean from the new workspace venv.

### State reset
- `games/` cleared (CSV + per-game JSONs + agent_elo.json).
- Next batch run is the first under the post-matchmaking-upgrade SHA.

## [2026-05-23] capture | ex3-inference-architecture | Settled vLLM + on-demand Slurm + SSH tunnel + local CLI
- Created decisions/2026-05-23-ex3-llm-inference-server-architecture.md (status: accepted)
- Created diary/meta/2026-05-23.md
- Rejected: always-on personal API, Ollama, internet-exposed endpoint, login-node controller daemon
- Settled: vLLM on per-session Slurm jobs, SSH tunnel from laptop, local CLI for ssh→sbatch→poll→tunnel→teardown
- Open: email ex3-contact@simula.no to convert verbal approval to written; confirm container runtime (Docker vs Apptainer)
- NOTE: index.md not updated due to filesystem lock during session; needs catalog entry for the new decision file on next pass

## [2026-05-23] capture | ex3-bootstrap-phase-1 | Got vLLM + Qwen2.5-0.5B serving on n014 A100, validated inference end-to-end
- Appended afternoon bootstrap section to diary/meta/2026-05-23.md
- Allocated JOBID 1238143 on n014 (a100q, A100 40GB, 8 CPUs); created venv at /global/D1/homes/$USER/llm-server/venv with vLLM 0.21.0
- Downloaded Qwen2.5-0.5B-Instruct via `git clone` (small files) + `curl -L` (safetensors) into /global/D1/homes/$USER/models/Qwen2.5-0.5B-Instruct
- Launched vLLM on n014:28811 (--max-model-len 4096); cold start ~2.5 min (21 s torch.compile + ~90 s CUDA graph capture)
- Verified /v1/models and /v1/chat/completions both respond correctly with coherent generation
- Discoveries / gotchas:
  - wiki/ex3 says `module load slurm/20.02.7`; actual available is `slurm/21.08.8` — wiki entry is stale
  - `hf` CLI v1.16.1 silently corrupts tokenizer.json on BeeGFS (produces 8.8 MB file vs correct 7 MB, deterministic byte-position corruption at 5 MiB boundary). Not hf_transfer (package not installed). Workaround: use git clone + curl directly
  - git-lfs NOT installed on login node — `git clone` of HF repos returns LFS pointer files for safetensors; must curl them
  - `srun --jobid=X --pty bash` and `srun --jobid=X --overlap --pty bash` both hang. Workaround: `ssh n014` directly from login node when you have an active alloc
  - Local port 11434 is blocked by laptop's Ollama install — use 11500 or other for ssh -L
- Still open: SSH tunnel from laptop showed banner but `curl localhost:11500/v1/models` returned `Connection refused`. Suspect ssh ControlMaster mux reuse stripping the -L flag. Need to diagnose with `lsof` and `ssh -v` next session
- TODO: update wiki/ex3.md to fix the stale slurm version and add the gotchas (hf CLI corruption, git-lfs absence, srun --jobid hang, ssh n014 workaround)
- Clean shutdown: Ctrl+C on vLLM → exit srun → squeue empty → exit all ssh sessions

## [2026-05-23] capture | module-llm-server | Got Gemma 4 31B-it serving on n014 A100×2, validated through SSH tunnel
- Created work/module-llm-server.md documenting full end-to-end setup procedure, working flags, errors-and-fixes, capacity notes
- Created diary/module-llm-server/2026-05-23.md with the day's debugging narrative
- Working config: vLLM 0.21.0, google/gemma-4-31B-it, a100q partition, n014, TP=2, port 28811, tunneled to laptop localhost:11500
- Verified /v1/models and /v1/chat/completions through tunnel; coherent 3-language hello response at ~23:14
- Key learnings:
  - HF_HOME alone is insufficient on eX3; HF_HUB_CACHE and HF_ASSETS_CACHE must be explicitly overridden because the cluster sets HF_HUB_CACHE system-wide
  - Gemma 4 is multimodal (Gemma4ForConditionalGeneration); vLLM force-disables chunked MM input which then requires --max-num-batched-tokens >= 2496 (set to 8192)
  - 31B BF16 on 2× A100 40GB at 8192 context needs --gpu-memory-utilization 0.95 (default 0.9 leaves only 2.71 GiB for KV cache vs 3.44 GiB needed)
  - GH200 nodes (gh200q) are aarch64 — existing x86_64 venv unusable there
  - hgx2q (g002, 8× A100 80GB) currently fully booked by muhammady×5 and uxue×3 with multi-day time limits; falling back to a100q+TP=2 is the practical choice
  - Earlier SSH tunnel "Connection refused" from last session could not be reproduced; treated as transient
- SECURITY: HF token leaked in chat via `env | grep -iE 'hf_'` output. Needs revocation at https://huggingface.co/settings/tokens
- NOTE: index.md not updated this session (filesystem lock made it unreadable); needs catalog entries for module-llm-server and the new diary entry on next pass
- TODO next session: write the local Python wrapper script (sbatch + ssh tunnel automation), the corresponding sbatch script, set up ssh key auth

## [2026-05-24] lint | knowledge-base | Structural audit: moved wiki/ex3.md, updated index, deleted empty inbox file

### Issues found and resolved

**Misplaced wiki page**
- `wiki/ex3.md` was sitting directly in `wiki/` outside any subdirectory (violates schema: wiki pages belong in `wiki/literature/` or `wiki/concepts/`)
- Moved to `wiki/concepts/ex3.md`; wikilinks `[[ex3]]` in decision files and diary are unaffected (slug unchanged)
- Added required YAML frontmatter (was missing entirely; page was a lint violation)
- Fixed stale Slurm module version: `slurm/20.02.7` → `slurm/21.08.8` (noted in 2026-05-23 log as stale)
- Added "Known Quirks / Operational Gotchas" section synthesising discoveries from 2026-05-23 bootstrap sessions (hf CLI BeeGFS corruption, git-lfs absent, srun --jobid hang, HF_HUB_CACHE override, port 11434 conflict)
- Added `[[module-llm-server]]` cross-reference in the LLM serving section and gotchas section

**Index out of date (noted in 2026-05-23 log entries)**
- Added `wiki/concepts/ex3.md` under Concepts → Infrastructure
- Added `### Modules` subsection to Work with `work/module-llm-server.md`
- Added `decisions/2026-05-20-elo-and-batch-runner.md` to Decisions
- Added `decisions/2026-05-23-ex3-llm-inference-server-architecture.md` to Decisions

**Empty inbox file**
- Deleted `inbox/Untitled.md` (1-line empty file, no content to process)

### No-action items

- `work/module-llm-server.md` and `wiki/concepts/ex3.md` have intentional overlap: ex3.md is the general cluster reference; module-llm-server.md is the specific operational procedure for LLM serving. They are correctly distinct; the ex3 page now cross-references module-llm-server rather than duplicating it.
- Decision files `2026-05-20` and `2026-05-23` have minimal frontmatter (type + status only) — valid per schema.
- `inbox/` is now empty — no further processing needed.

## [2026-05-24] capture | experiment-chess | Chess backend wired to eX3 Gemma instead of Azure
- Created diary/experiment-chess/2026-05-24.md
- Updated work/experiment-chess.md — added note that inference backend is now env-controlled, model column captures the backend choice
- Updated work/module-llm-server.md — expanded "Downstream integration" section to document both consumers (skillful-agent server + chess backend) and explain why each needs its own backend-selection logic
- Code changes: experiments/chess/backend/app/agent_player.py:_build_agent now branches on SKILL_AGENT_EX3_BASE_URL → SKILL_AGENT_AZURE_ENDPOINT → OpenAI; experiments/chess/backend/.env switched to eX3 default (Azure commented out)

## [2026-05-24] capture | module-llm-server | Final state: 64k context on gh200q with tool calling and skillful-agent wired up
- Final config: gh200q, --max-model-len 65536, --cpu-offload-gb 120, --tensor-parallel-size 1, tool calling enabled
- Updated software/ex3/README.md — full rewrite reflecting final state: gh200q recommended, 64k context, CPU offload rationale, ARM venv bootstrap instructions, all gotchas documented
- Updated work/module-llm-server.md — 64k context, updated flag explanations, context limit table with all attempts
- Appended diary/module-llm-server/2026-05-24.md — added "Final iteration" section with CPU offload findings (60.25 GiB available with 120 GB offload, 71,760 estimated max tokens), tunnel-detection bugs (substring match bug READY/NOT_READY, ControlMaster tangling), HF token regeneration note
- serve.py: tool-call flags, crash detector, stale-job cleanup, live log status display (replaces dots), curl on eX3 directly for readiness (no tunnel false-positives), tunnel verification with retry, CUDA_HOME fix for gh200q, per-partition venv+tp, ControlMaster=no on tunnel
- skillful-agent wiring: SKILL_AGENT_EX3_BASE_URL env var takes priority over Azure/OpenAI
- Open items: HF token needs to be regenerated at /global/D1/homes/$USER/.hf_token; 128k context would need ~240 GB CPU offload

## [2026-05-24] capture | module-llm-server | serve.py launcher built and verified end-to-end
- Created diary/module-llm-server/2026-05-24.md — full account of serve.py development, bugs hit (module not found, $USER in SBATCH directives, SSH passphrase prompts), and fixes
- Updated work/module-llm-server.md — new "How to start" section pointing to serve.py as canonical entry point; updated files/paths section; marked three todos as done (SSH key auth, wrapper script, HF token revocation); updated frontmatter (related_concepts: [ex3], updated: 2026-05-24)
- Key learnings captured: `bash --login` via stdin for non-interactive SSH; `%u` vs `$USER` in SBATCH directives; ControlMaster + UseKeychain for frictionless repeated SSH calls; HF token stored in ~/.hf_token on eX3 (not laptop)
- Verified: `python3 software/ex3/serve.py` → job 1250530 on n014 → vLLM ready → curl returns coherent chat completion

## [2026-05-24] capture | experiment-chess | Documentation sweep after backend restructure and model switch
- experiments/chess/CLAUDE.md: updated "What this repo is" to reflect chesscom_driver living inside backend/; removed stale workspace-member description; fixed verify-changes command; removed orphaned line about reinstalling workspace members
- experiments/chess/README.md: full rewrite — replaced stale scaffold description and npm/cd instructions with current layout, run instructions (uv, bun, eX3 server), agent/model info, and broken-venv pointer
- experiments/chess/backend/README.md: full rewrite — current run instructions, full API surface (games + batches + ELO endpoints), architecture notes, explanation of why chesscom_driver lives inside backend/
- experiments/chess/chesscom-driver/README.md: removed stale "gpt-4o-mini at this stage / 300 ELO raw" claim

## [2026-05-24] decision | per-turn-fresh-context | Baseline calibration runs with per-turn fresh context; aborted-game handling added; typed AgentContextOverflowError in skillful-agent
- Created decisions/2026-05-24-per-turn-fresh-context.md (full ADR — context, decision, aborted-game policy, skillful-agent typed exception, consequences, follow-ups)
- Updated work/experiment-chess.md: added three new ELO-methodology bullets (initial ELO 600, reason-before-move, per-turn fresh context, aborted games); updated Logging schema for new aborted_reason CSV column; refactored Open items (added memory-axis follow-up, marked agent-integration-path settled)
- Updated index.md: added all three 2026-05-24 ADRs under Decisions
- Code: agent_player.py calls self._agent.clear_conversation() at top of get_move(); catches AgentContextOverflowError → re-raises as PlayerError("context_overflow: …")
- Code: game_service.py — new Game.aborted_reason field; abort path in _run_until_human_or_finished records the game, fires on-game-finished callback, tears down players; _record_game_end passes aborted_reason
- Code: logging_service.py — CSV_COLUMNS gains aborted_reason; record_game accepts and writes it
- Code: batch_runner.py — explicit WARNING log when ELO is skipped because the game aborted; result_label includes the abort reason
- Code: skillful-agent — new skill_agent/exceptions.py with AgentContextOverflowError; agent.py wraps run_stream_events iteration to translate context-overflow provider errors; __init__.py exports the new type; CLAUDE.md gains a "Handle context-overflow gracefully" snippet; TODO left for future pre-flight compaction with retry
- Updated experiments/chess/CLAUDE.md: new "Baseline calibration invariants" section with links to all four chess ADRs and work/experiment-chess.md
- Updated experiments/chess/backend/README.md: new "Context management" section explaining the per-turn clear_conversation() invariant and overflow-handling path

## [2026-05-24] decision | ranked-vs-experimental | Two-CSV logging + PR-as-version + git-tracked game data
- Created decisions/2026-05-24-ranked-vs-experimental.md
- Backend: experiments/chess/backend/app/repo_state.py — added `live_git_state`, `is_ranked_context`, `current_phase`; kept `chess_repo_sha` as deprecated alias
- Backend: experiments/chess/backend/app/logging_service.py — replaced single games.csv with ranked.csv + experimental.csv; new schema (added `phase`, `branch`, `commit_sha`, `analysis_path`; dropped `skill_repo_sha`); routes to correct CSV via `current_phase()`
- Backend: experiments/chess/backend/app/batch_runner.py — `_handle_game_finished` now skips ELO update when `is_ranked_context()` is false, with INFO log explaining why
- Backend: experiments/chess/backend/app/game_service.py — dropped `skill_repo_sha` arg from `record_game` call
- Backend: experiments/chess/backend/app/main.py — new `GET /api/repo-state` endpoint surfacing live phase/branch/sha/dirty for the frontend banner
- Frontend: experiments/chess/frontend/src/RepoStateBanner.tsx (new) — polls /api/repo-state, renders coloured banner
- Frontend: LobbyPage and BatchPage now show the banner; CSS additions for `.repo-banner-*` classes
- Storage: experiments/chess/.gitignore — explicit comment that games/ and batches/ are intentionally tracked
- Cleanup: removed legacy backend/games/games.csv and stray .json artifacts; added .gitkeep to games/ and batches/
- Docs: work/experiment-chess.md updated (Logging schema + ELO methodology bullets + Open items #7 for rebuild_elo.py); experiments/chess/CLAUDE.md updated (conventions, git workflow, open invariants, baseline calibration invariants); experiments/chess/README.md updated (invariants list); experiments/chess/backend/README.md updated (new Ranked vs experimental section + API surface)
- Diary addendum appended to diary/experiment-chess/2026-05-24.md
- Index updated with the new ADR

## [2026-05-24] decision | reason-before-move | Strengthen prompt to force reasoning-before-make_move; label post-move text correctly
- Created decisions/2026-05-24-reason-before-move.md
- Updated experiments/chess/backend/app/agent_player.py: new system_prompt_extra enforcing a numbered sequence (use_skill → list_legal_moves → 2–4 sentences of reasoning → make_move → end turn)
- Updated experiments/chess/frontend/src/AgentPanel.tsx: new `post-move` entry kind; tracks make_move.py calls per turn; pre-move text labelled `reasoning`, post-move text labelled `post-move` in muted styling
- Updated experiments/chess/frontend/src/styles.css: `.agent-post-move` muted/italic styling distinguishing post-hoc commentary from move-influencing reasoning
- Triggered by direct vLLM SSE probes confirming Gemma 4 default behaviour is tool-first; explicit reasoning instruction is required to elicit reason-then-act ordering

## [2026-05-24] decision | initial-elo-600 | Set initial agent ELO to 600 instead of 1200
- Created decisions/2026-05-24-initial-elo-600.md
- Updated backend/app/elo.py: INITIAL_ELO = 600; updated inline docstring
- Rationale: educated guess from observing gameplay during testing; 1200 wastes provisional K-factor games on a long downward drift

## [2026-05-24] capture | experiment-chess | Switched agent backend from GPT-4o (Azure) to Gemma 4 31B-it (eX3 vLLM); cleared all prior game data for fresh calibration
- Deleted all 14 prior game JSON files, agent JSON traces, games.csv, and agent_elo.json from `experiments/chess/backend/games/`
- Deleted 2 prior batch JSON files from `experiments/chess/backend/batches/`
- Updated `backend/app/repo_state.py` docstring: replaced Azure-specific commentary with model-agnostic language reflecting the eX3 vLLM backend; updated `agent_model()` docstring to name Gemma 4 31B-it as the current model
- The `.env` was already configured correctly: `SKILL_AGENT_EX3_BASE_URL=http://localhost:11500/v1` and `SKILL_AGENT_OPENAI_MODEL=google/gemma-4-31B-it`; no code change needed there
- Backend imports verified clean after changes
- Ready to run fresh calibration batch against Maia pool

## [2026-05-25] decision | initial-elo-1200 | Reset initial ELO to 1200; supersedes 2026-05-24-initial-elo-600
- Created decisions/2026-05-25-initial-elo-1200.md
- Updated backend/app/elo.py: INITIAL_ELO = 1200; updated module docstring
- Wiped games/agent_elo.json (no such file — already absent after prior session cleanup)
- Updated index.md: marked old ADR superseded, added new one

## [2026-05-25] decision | move-cap-and-draw-halt | 150 half-move cap + 3-consecutive-draw batch halt
- Created decisions/2026-05-25-move-cap-and-draw-halt.md
- Updated backend/app/game_service.py: Game.max_half_moves=150; is_over() and result() enforce cap
- Updated backend/app/batch_service.py: Batch.consecutive_draws field + from_dict support
- Updated backend/app/batch_runner.py: MAX_CONSECUTIVE_DRAWS=3; halt logic in _handle_game_finished
- Updated index.md

## [2026-05-25] lint | knowledge-base | KB tidy-up after baseline calibration milestone
- `decisions/2026-05-24-initial-elo-600.md`: frontmatter updated — `status: superseded`, `superseded_by: 2026-05-25-initial-elo-1200`. The supersession relationship was previously only visible via the index hover-text; now it's machine-readable from the file itself.
- `index.md` Decisions section regrouped by topic ("Project-wide", "Infrastructure", "experiment-chess — methodology", "experiment-chess — milestones"). The flat date-sorted list had drifted out of chronological order (05-24 entries appeared after 05-25 entries) and the experiment-chess ADRs were difficult to scan. The supersession of 05-24-initial-elo-600 is now expressed inline ("supersedes …") rather than as a *(superseded)* tag at the end.
- No content changes to any ADR body. No code touched. No game data touched.

## [2026-05-25] decision | baseline-calibration-complete | Bare-model baseline calibration declared complete at ELO 684.2 (ceiling, not point estimate)
- Created decisions/2026-05-25-baseline-calibration-complete.md
- 26 ranked games (22 losses, 4 draws, 0 wins) under post-2026-05-25 config (Gemma 4 31B-it, initial ELO 1200, chess.com pool floor 700, per-turn fresh context, resign-on-no-move). Trajectory 1200 → 684.2. After game 4 the matchmaker reached the chess.com pool floor and every subsequent game was played at chess.com-700; the streak counter walked to -5 but was clamped.
- Methodological framing: bare-model agent's true ELO is **≤ 700**. 684.2 is a ceiling bounded by the pool floor, not a point estimate. The four draws at chess.com-700 corroborate the floor rationale (games at this level converge on time-cap draws regardless of agent skill).
- Next batches (skill-library configurations) continue from agent_elo.json as-is — no reset. Visible drift from 684.2 is the trajectory the experiment measures. A success criterion ("library beats baseline by X") will be set in a follow-up ADR when the library work is ready.
- Updated `work/experiment-chess.md`: cleaned up the ELO methodology bullet list (removed the contradictory "Initial ELO 600" bullet that the 05-25 superseding ADR already replaced; added pool-floor and resign-when-stuck bullets; added a new "Bare-model baseline" subsection recording 684.2 and the ceiling framing); bumped frontmatter `updated:`.
- Updated index.md.

## [2026-05-25] cleanup | experiment-chess | Cleanup pass + full game-data reset before next batch
- Behaviour unchanged. Same Elo formula, same pool, same retry count, same resignation semantics, same prompt contract.
- `app/agent_player.py`: `AgentContextOverflowError` import-fallback lifted from `get_move()` (ran every turn) to module scope (runs once at import). System prompt consolidated: removed the redundant "Keep reasoning short" paragraph (workflow step 3 already says it) and collapsed the 3-sentence resignation warning to one sentence.
- `app/game_service.py`: extracted `_finish_game_with_error(game, *, publish_message, aborted_reason, result_override=None)` and routed both the `AgentResignedError` branch and the generic `Exception` branch through it. The two except blocks shrank from ~20 lines each to ~12, with a single definition of "what 'ended badly' means."
- `backend/skills/chess-player/SKILL.md`: trimmed from 66 to 40 lines. Removed the numbered workflow, the "Critical: what make_move.py does" section, and the "Thinking format" subsection — all duplicated by the system prompt, which the model sees every turn (SKILL.md is loaded only on the first `use_skill` call). What remains: skill role, script invocation contract, UCI format.
- Data reset: deleted all per-game JSONs (`backend/games/*.json`, `*_agent.json`), all batch JSONs (`backend/batches/*.json`), `backend/games/agent_elo.json`; truncated `ranked.csv` and `experimental.csv` to header-only. `.gitkeep` files preserved in both directories. The four ranked rows previously archived in `experimental.csv` are sacrificed by the reset — they remain reachable via git history.
- Verified: imports clean, tests show same 2 pre-existing failures (test_player_types and test_sse_subscription_emits_initial_state, both unrelated to today's work). Restart the backend before next batch — `AgentConfig` and the system prompt are loaded at module import.

## [2026-05-25] decision | agent-resigns-when-stuck | Agent resigns when it cannot commit a move; infrastructure errors still abort
- Created decisions/2026-05-25-agent-resigns-when-stuck.md
- Three failure modes now treated differently: (1) agent cannot commit a move after _MAX_ATTEMPTS=3 → resignation (0-1 loss, ELO drops); (2) AgentContextOverflowError → abort, no ELO change; (3) other player exceptions (browser crash, network) → abort, no ELO change. The CSV's `aborted_reason` column distinguishes them: `agent_resigned_no_move` carries a `0-1` result; infra aborts carry `result=""`.
- Rationale: a human who can't move loses on time. Resignation is the chess-correct analogue and forces the ELO trajectory to reflect total agent capability (chess reasoning + tool-dispatch reliability), not just chess. Closes the perverse-incentive loophole where a buggy configuration could "improve" its rating by hanging.
- Code:
  - `app/players.py`: new `AgentResignedError(PlayerError)`
  - `app/agent_player.py`: `_MAX_ATTEMPTS` exhausted now raises `AgentResignedError`; `UsageLimitExceeded` from pydantic-ai's max_turns is caught per-attempt and treated as "no move this attempt" so the outer loop retries (and falls through to resignation if it never succeeds); system prompt tightened with explicit 2–4 sentence reasoning cap and resignation-warning sentence; `max_tokens=1024` per response; `max_turns=10` per run
  - `app/game_service.py`: new `Game.result_override: str | None` field; `is_over()` and `result()` honour it; bot loop's exception handler branches on `AgentResignedError` to set `result_override="0-1"` and `aborted_reason="agent_resigned_no_move"` before flowing through the standard `_record_game_end` → `_on_game_finished` path
- Verified: semantics of result_override (Game.is_over() and Game.result() short-circuit when set); test suite shows same 2 pre-existing failures unchanged
- Updated index.md

## [2026-05-25] decision | chesscom-pool-floor | Raise chess.com pool floor to 700; archive 4 prior ranked rows; full reset of ranked state
- Created decisions/2026-05-25-chesscom-pool-floor.md
- Rationale: first ranked batch produced 3 losses (vs chesscom 1200/1100/1000) and 1 aborted game (vs chesscom 550). The bottom 3 slider positions (250, 400, 550) produce games that converge on time-cap draws regardless of agent skill — a property of the pool, not the rating system.
- Decision: trim `CHESSCOM_ELOS` from 25 ratings (250–3200) to 22 (700–3200). chesscom_driver/mapping.py is intentionally unchanged (still describes the physical slider; only the experiment's selectable pool is curated). Initial ELO stays at 1200 (evidence not yet strong enough for a prior revision). Elo formula, K-factor, streak stepping all unchanged.
- Code: app/schemas.py and app/elo.py CHESSCOM_ELOS tuples updated; comment in each module points at the ADR
- Data migration: 4 ranked rows appended to experimental.csv (rows keep their original `phase=ranked` value as forensic marker — documented in the ADR); ranked.csv truncated to header; agent_elo.json deleted; per-game JSONs and batch JSON kept on disk (referenced by the archived rows)
- Verified: AgentEloState.load() on missing agent_elo.json returns default (elo=1200, games_played=0, streak=0)
- Updated index.md

## [2026-05-25] capture | experiment-chess | make_move.py redesign: tool now commits the move; retry loop added

### Root cause (game bae5639fc5b044dcac842d14c8ae79fd, turn 21)
Gemma 4's internal thought channel (`<|channel>thought<channel|>`) does not reliably propagate into tool dispatch. The model reasoned correctly to a fallback move but dispatched the original illegal move both times. The harness had no retry mechanism.

### Structural fix
- `make_move.py` now POSTs to `POST /api/games/{id}/agent-move` — the move is committed to the board immediately when the tool returns `ok=true`. The tool has real consequences; failure returns the current legal-moves list in the response.
- New `GameService.submit_agent_move()` method handles the POST (no `is_human` check, acquires board lock).
- New `POST /api/games/{id}/agent-move` endpoint in `main.py`.
- `AgentPlayer.get_move()` breaks the stream as soon as `make_move.py` returns `ok=true` (board already moved). Model can call tools freely in any order; harness waits for the real side-effect.
- Retry loop: if `run_stream` ends without a committed move, retry up to `_MAX_MOVE_RETRIES=2` times with `clear_conversation()` + fresh prompt naming legal moves. Mechanical failsafe independent of model architecture.
- Bot loop (`_run_until_human_or_finished`) checks move count before calling `_push_move` to prevent double-apply when the agent script already committed the move.
- `SKILL.md` updated to document the commit-on-call contract and retry behaviour.

### Files changed
- `backend/skills/chess-player/scripts/make_move.py`
- `backend/skills/chess-player/SKILL.md`
- `backend/app/game_service.py`
- `backend/app/main.py`
- `backend/app/agent_player.py`
- Updated `diary/experiment-chess/2026-05-25.md` with full implementation notes

## [2026-05-25] query | experiment-chess | Aborted game investigation: Gemma 4 illegal-move recovery failure
- Read game trace bae5639fc5b044dcac842d14c8ae79fd_agent.json (turn 21, game vs chess.com 550)
- Root cause: three layered issues identified:
  1. Gemma 4 uses a separate `<|channel>thought<channel|>` reasoning stream that does not reliably propagate to the tool call that follows — the model reasons correctly to the fallback move but still calls make_move.py with the original illegal move
  2. max_turns=20 in AgentConfig counts model requests, not chess plies — latent risk for turns with many retries (not the direct cause here; the stream ended normally after exhausting text without a legal move call)
  3. No harness-level retry in AgentPlayer.get_move() — if run_stream ends without a successful make_move.py, the game aborts immediately
- Two fixes proposed: (A) harness-level retry with explicit follow-up prompt in AgentPlayer.get_move(); (B) system-prompt instruction clarifying that ok=false from make_move.py requires an immediate re-call with a different move
- Created diary/experiment-chess/2026-05-25.md with full trace analysis and fix proposals

## [2026-05-25] capture | experiment-chess | Perception tools + skill/system-prompt rewrite (visualization-and-context-management branch)
- Created `decisions/2026-05-25-perception-tools-and-skill-rewrite.md` — ADR for the first post-baseline configuration: three new mechanics tools (`show_position.py`, `imagine_move.py`, `evaluate_position.py`), full SKILL.md rewrite (leads with turn workflow, "trust your tools over intuition" framing), system-prompt trim (drops prescribed step sequence and reasoning length cap; keeps role + commit semantics + anti-loop nudge + resignation rule), max_turns 10 → 16
- Created `diary/experiment-chess/2026-05-25-visualization-tools.md` — implementation diary covering what was built, why, what we hope to achieve, tool-fairness reflection (especially the borderline case of PSTs in evaluate_position), and a placeholder section for the upcoming context-management work
- Updated `index.md` — added the new ADR under experiment-chess milestones
- No changes to existing wiki concept pages yet; will propagate to `tools-component`, `tool-fairness`, `deterministic-tools-hypothesis` after the experimental batch runs and we have data to anchor the claims

## [2026-05-26] capture | experiment-chess | Stabilization pass on perception-tool configuration
- Created `decisions/2026-05-26-stabilization.md` — ADR for ten coupled changes: AgentConfig.disabled_tools + disable_native_skills, SKILL.md commit-nudge rewrite, per-turn budget warning + _MAX_ATTEMPTS 30→10, static eval folded into show_position + imagine_move, evaluate_position.py deleted, annotated list_legal_moves + full opponent-moves table, markdown output everywhere with frontend rendering, backend-side Gemma channel-marker stripping, per-move Stockfish + static eval logging in turns[].evals, agent_elo in per-game JSON, 400 BadRequest recovery
- Created `diary/experiment-chess/2026-05-26-stabilization.md` — implementation diary explaining the failure modes that motivated each change, what's still out of scope (context management, guided_json), and what to watch in the next test batch
- Updated `index.md` — added the new ADR under experiment-chess milestones
- Updated `experiments/chess/CLAUDE.md` — reflects the four-script skill surface (was listing only list_legal_moves + make_move) and the disabled-tools mechanism
- skillful-agent patches (AgentConfig.disabled_tools + disable_native_skills + _list_files underscore-prefix filter) live in `software/skillful-agent/skill_agent/` and a new `software/skillful-agent/skill_agent/_tool_filter.py`. 115 tests pass after the SDK changes; 5 new tests in `tests/test_disabled_tools.py` cover the filter mechanism
- Chess-side tests: 120 of 122 pass; the 2 failures are pre-existing in test_backend.py (unrelated coroutine handling), confirmed by stashing my changes and re-running

## [2026-05-26] capture | experiment-chess | SSE history replay + cleanup pass
- Live-game observation: reasoning panel in the UI was empty because the SSE endpoint was live-only — anyone who subscribed mid-game missed the early turns' `text_delta` events entirely. Fixed by replaying the agent-event history on connect: `LoggingService.get_past_agent_events` returns all events from completed turns plus any from the in-progress turn so far; the SSE endpoint subscribes first to avoid dropping live events during the read, then streams past events, then enters the live-queue loop. `AgentPanel.tsx` resets its entry list on `gameId` change so the replay populates cleanly
- Added §10 to `decisions/2026-05-26-stabilization.md` documenting the SSE replay; added a "late-day update" section to `diary/experiment-chess/2026-05-26-stabilization.md` covering the symptom, the root cause, and the fix
- Updated `experiments/chess/CLAUDE.md` to note the agent-events SSE replay behaviour so the next claude session doesn't re-derive it
- Updated `knowledge-base/work/experiment-chess.md` to reflect current per-turn limits (`_MAX_ATTEMPTS=10`, `max_turns=16`) and the budget warning mechanism; bumped `updated:` to 2026-05-26
- Code cleanup pass: deduplicated reasoning/post-move renderers into a shared `StreamingMarkdown` component in `AgentPanel.tsx`, dropped dead `extractStdout` helper; extracted `_record_per_move_evals` from the bot loop in `game_service.py` to keep `_run_until_human_or_finished` readable; rewrote `agent_player.py` for clarity — dead `AgentContextOverflowError` shim removed, `_committed_move_from_result` now operates directly on the `ToolResultEvent.result` payload instead of scanning `tool_log.output_preview`, helper constants (disabled tool list, system-prompt extra, budget-reminder template) lifted to module scope; dropped unused `_color_name` alias in `_eval.py`; simplified the moved-piece hanging warning in `imagine_move.py` to reuse `describe_piece`
- Tests: 105 chess-backend pass (excluding pre-existing `test_player_types` failure); frontend `tsc --noEmit && vite build` passes

## [2026-05-26] capture | experiment-chess | Endgame fixes: hanging-rook warning bug + checkmate-seeking prompt
- Created `diary/experiment-chess/2026-05-26-endgame-fixes.md`
- **Bug 1 fixed**: `imagine_move.py` `_moved_piece_hanging_warning` was suppressing warnings whenever `board_after.is_check()`, even when a legal reply captures the hanging piece. Fixed: now only suppresses when no legal reply captures on the moved-piece square. Verified with the exact game position (Rxe7+, king can take): warning now fires correctly.
- **Bug 2 (prompt fix)**: SKILL.md had no instruction to seek checkmates. Added step 0 to the turn workflow ("always check for checkmate first — run `list_legal_moves`, scan Flag column, commit immediately if `checkmate` found"). Extended the "obviously good move" bullet to name checkmate flags. Added aggressive-candidate guidance to step 2.
- 120 tests pass (2 pre-existing failures unchanged)

## [2026-05-26] capture | experiment-chess | King mobility feature: enemy king escape squares in all move tables
- Appended session 2 section to `diary/experiment-chess/2026-05-26-endgame-fixes.md`
- **New feature**: `_eval.py` gains `enemy_king_mobility(board)` helper (counts enemy king's legal moves via a turn-flipped copy). `annotate_move` now returns `king_before`/`king_after` keys. `render_moves_table` gains a **King mvt** column: `before→after (±delta)`, e.g. `6→3 (−3)`. Negative delta = move restricts king; 0 after = check/mate.
- **`imagine_move`**: New **Enemy king mobility** line at the top of the report (`before → after (±N squares)`), right after the Check line, so the agent sees restriction impact immediately.
- **SKILL.md**: Step 2 docs updated to explain King mvt column and enemy king mobility line, with explicit instruction to hunt for sequences that progressively reduce king mobility toward zero.
- `test_annotate_move_quiet` updated to check `king_before`/`king_after` keys instead of strict dict equality.
- 120 tests pass (2 pre-existing failures unchanged)

## [2026-05-26] query | experiment-chess | Context read before starting context-management work on visualization-and-context-management branch
- Read CLAUDE.md, index.md, log.md, work/experiment-chess.md, decisions/2026-05-24-per-turn-fresh-context.md, decisions/2026-05-26-stabilization.md, diary/experiment-chess/2026-05-25-visualization-tools.md, diary/experiment-chess/2026-05-26-stabilization.md, diary/experiment-chess/2026-05-26-endgame-fixes.md, wiki/concepts/context-engineering.md, experiments/chess/CLAUDE.md
- Summary handed to user; no writes to wiki or work pages

## [2026-05-26] capture | experiment-chess | First agent checkmate; bishop-sac warning gap investigated
- Appended session 3 section to `diary/experiment-chess/2026-05-26-endgame-fixes.md`
- **First win**: Game `ed2bfd9d43824d919feaf917fb37bebb` — agent vs chess.com 700, 1-0 by Rd5# after 34 moves. First time the agent has converted a winning position into mate under this configuration (perception tools + step-0 mate scan + king mobility). N=1; no claims about which intervention mattered, just an observation worth recording.
- **Bishop-sac investigation**: User flagged that `imagine_move` didn't warn about the move-14 Bxf6 sacrifice. Reproduced the position; found the warning correctly didn't fire because the bishop on f6 was defended by the queen on d4 against the g7 pawn attacker (1 attacker, 1 defender, count-based check passes). For this specific move the math is actually positive (+320 knight capture, −330 bishop lost, +100 pawn recapture if taken = +90 net), so the warning was correct.
- **Latent gap surfaced (not fixed this session)**: The hanging detection is value-blind for the `count(attackers) == count(defenders)` case. Bishop defended by queen against a pawn would lose 230 cp on exchange but currently silent. Recommended follow-up: SEE-lite using existing `compute_attack_chain` output, walking the exchange cheapest-first and tallying signed material. Flagged in diary for a follow-up session — not in scope here.

## [2026-05-26] capture | experiment-chess | Wrap-up diary for visualization-and-context-management branch + ADR update
- Created `diary/experiment-chess/2026-05-26-branch-wrapup.md` consolidating the branch's eight themes (perception tools, stabilization, endgame fixes, context management, agent-authored turn memory, SDK fix, SAN/UCI dual support, logging reorganization) with the user's reflections on what improved (perception + mate-seeking unlocked first 700-elo win) and what still struggles (king-rook mates, occasional blunders, complex mating patterns).
- Updated `decisions/2026-05-24-ranked-vs-experimental.md` to document the new `pr_number` CSV column and the per-PR folder layout under `backend/games/` (`baseline/`, `<pr-slug>/` with `NNN_` prefixed filenames). Resolved by `app/folder_resolver.py` via `gh pr view` with branch-name fallback.

## [2026-05-27] capture | experiment-chess | Diary entry on post-merge calibration batch + Gemma harness references
- Created `diary/experiment-chess/2026-05-27.md` documenting five observed failure modes on the post-merge calibration batch (hanging mate-in-1; `imagine_move` argument-missing loop; missing fork detection; ineffective mate-seeking beyond immediate mate; SKILL.md reloaded every turn) and the structural question of whether skillful-agent is the right harness for Gemma 4
- Captured two external references in `raw/other/` (not full wiki ingest — flagged for user decision):
  - `raw/other/2026-05-mirko-gemma-ollama-pydantic-recipe.md` (Mirko / gammavibe.com blog post on Pydantic AI + Gemma 4 + Ollama; key takeaway: `NativeOutput` + temperature 0.2 + Ollama `format=` for constrained decoding makes Gemma 4 reliable for tool calls)
  - `raw/other/2026-05-mayo-gemma4-tool-calling-fs-python.md` (Mayo / KDnuggets tutorial on from-scratch Gemma 4 tool-calling loop with filesystem + restricted python interpreter; includes Google's official ai.google.dev Gemma 4 tool-calling notebook content)
- No wiki literature pages or concept-page updates yet — held back pending user direction on whether these grey-lit sources warrant full ingest, and whether the harness question becomes an ADR
- Did NOT update `index.md` (no wiki changes); did NOT update `work/experiment-chess.md` (no status / scope change yet — five follow-ups are spec'd in the diary)

## [2026-05-27] ingest+capture | experiment-chess | Grey-lit ingest + batch trace findings
- Promoted both `raw/other/` captures from 2026-05-27 to full wiki literature pages:
  - `wiki/literature/mirko2026gemma.md` (NativeOutput + constrained decoding fix for Gemma 4 + Pydantic AI)
  - `wiki/literature/mayo2026gemma4tools.md` (from-scratch Gemma 4 tool-calling loop + Google's official chat-template notebook)
- Updated `wiki/concepts/tools-component.md`: added experiment-chess to "where tools are probed" with the contract-failure pattern; added a new section "Constrained decoding as a contract-tightening mechanism" citing both grey-lit sources; added both citekeys to frontmatter `sources`; bumped `updated:` to 2026-05-27
- Updated `index.md`: added a new "Grey literature (blog / tutorial)" subsection under Literature with the two new entries
- Created `diary/experiment-chess/2026-05-27-batch-analysis.md` with structured trace findings from the post-merge ranked calibration batch (12 games, `02[0-9]_*_agent.json` + `030`, `031`): ELO 712.7 → 783.6 across 10 ranked; `make_move` 19.9% failure rate driven by `shlex.split(args)` ValueError on apostrophes in `--reasoning` free text (116 of 118 failures); `imagine_move` 26.3% failure rate with 44 turns showing 3+ identical empty-args calls in a row (worst: 14 consecutive); `show_position` and `list_legal_moves` 0% failure rate (no required args); 0 hanging-piece warnings fired in 1424 imagine_move calls (so the false-positive observation cannot be verified from this batch); `use_skill` reload pattern is ≈49% of turns, not "every turn"
- The batch-analysis diary revises the [[2026-05-27]] priority list: `args`-as-shell-string fix is now #1 (a single harness change eliminates Findings 1 and most of 2); pre-injecting SKILL.md drops in priority since the cost is half what was assumed
- No code changes — analysis only, per user instruction

## [2026-05-27] capture | experiment-chess | ADR + dual-repo fix for run_script args contract + chess.com page-load retries
- Created `decisions/2026-05-27-run-script-args-list.md` (status: accepted). ADR documents the trace evidence (116/118 make_move failures, 337 empty-args imagine_move calls), the shlex-split apostrophe smoking gun, and the list[str] migration as the chosen fix. References [[mirko2026gemma]], [[mayo2026gemma4tools]], [[2026-05-27-batch-analysis]], [[tools-component]].
- skillful-agent commit 19fbadb (`run_script: switch args from shell string to list[str]`) pushed to https://github.com/andreasklae/skillful-agent main. Changed: `skill_agent/skill_tools.py` (signature + body + tool description), `skill_agent/system_prompt.md`, `native-skills/web-search/SKILL.md`, `native-skills/learner/SKILL.md`, and the three `learner/scripts/*.py` docstring examples. 118 tests pass.
- chess-experiment commit 5df0120 (`Update run_script call sites to list[str] contract + retry chess.com page load`) pushed to https://github.com/andreasklae/chess-experiment main. Changed: `backend/skills/chess-player/SKILL.md`, `backend/skills/chess-player/scripts/imagine_move.py` (error-string example), `backend/chesscom_driver/driver.py` (goto 60s timeout + 1 retry on transient failure), `backend/app/batch_runner.py` (`_create_next_game` 3-try loop with backoff). Recorded as a follow-up fix to the visualization-and-context-management PR per user request (no new capabilities, only fixes). The recent batch data is checked in alongside the code.
- Investigated the user's "fails to open a new game after a draw" report. Confirmed via `backend/batches/5a03b5ed40b3434c95517d5b9c21b39c.json` that batch failed at 4/10 games after 2 consecutive draws with `last_error: "502: Failed to start player: Page.goto: Timeout 30000ms exceeded."` — chess.com page load timed out on the 5th game start. Root cause is loose (transient chess.com slowness, not a draw-handling logic bug per se) but the retry+timeout-bump in driver.py + batch_runner.py addresses the symptom. Documented in commit message; will validate over the next batch.
- `run_server.py` (skillful-agent) and the chess backend are ready to run. The user can resume calibration.

## [2026-05-27] capture | experiment-chess | Single-writer move-commit refactor (agent-commit replaces agent-move)
- After a day-long debugging chain (SAN at API → SAN reparse in AgentPlayer → phantom exd5 on host board) the user pushed me to step back and reason about the contract. The root cause: two writers to game.board (bot loop's _push_move AND the /agent-move endpoint's _push_uci_move). Player implementations followed different mutation paths; the bot loop tried to reconcile via an `already_applied` detection branch.
- New ADR: `decisions/2026-05-27-single-writer-move-contract.md`. The bot loop is now the only writer. Every player returns a chess.Move; the loop pushes it under game.lock.
- Endpoint change: `POST /api/games/{id}/agent-move` → `POST /api/games/{id}/agent-commit`. The new endpoint validates (legality, turn, move shape — UCI-or-SAN with +/# stripped) and returns the canonical UCI; it never mutates game.board.
- Code changes (chess repo):
  - `backend/app/schemas.py`: replaced `AgentMoveRequest` with `AgentCommitRequest` (adds required `reasoning` field for schema-enforced "you must explain your move")
  - `backend/app/main.py`: route renamed, calls `submit_agent_commit`
  - `backend/app/game_service.py`: `submit_agent_move` → `submit_agent_commit` (validator-only); bot loop's `already_applied` branch removed; `_push_uci_move` retained for `_submit_human_move` only
  - `backend/app/agent_player.py`: tool-result return path drops the SAN-fallback `board.parse_san` — the endpoint guarantees canonical UCI now, `chess.Move.from_uci` always works on it
  - `backend/skills/chess/scripts/make_move.py`: POSTs to `/agent-commit`, sends both move and reasoning in the body, echoes back the canonical UCI from the response
  - `backend/skills/chess/SKILL.md`: updated commit-step description to "your turn is over" rather than "the board has already advanced" (the practical contract for the model is unchanged; the implementation no longer matches the old phrasing)
  - `experiments/chess/scripts/recover_orphan_game.py`: docstring updated with historical note about the old design
- KB updates:
  - New diary entry: `diary/experiment-chess/2026-05-27-single-writer-refactor.md`
  - Updated `work/experiment-chess.md` bullet on `make_move.py` commit semantics
  - Updated `wiki/concepts/tools-component.md` with both contract-design patterns surfaced this week (transport layer + mutation boundary)
- 120 backend tests pass (2 pre-existing failures unrelated). Live vLLM test: Gemma 4 31B-it emits `args=["Nxf6+", "<reasoning with apostrophes>"]` cleanly under the new schema. End-to-end chess validation pending — user will run the next batch after restarting the backend.

## [2026-05-28] capture | experiment-chess | Close PR #1 calibration round + diary entry
- New diary entry: `diary/experiment-chess/2026-05-28.md` — declares PR #1 calibration round complete (converged ~800 ± 15; trajectory 684.2 baseline → 793.6, 14–8–5), records the bug-fix-vs-configuration framing for the args fix, the CSV cleanup, and consolidates standing reflections/limitations for this version.
- Source-data hygiene (in experiment repo, not KB): removed 6 aborted rows from `experiments/chess/backend/games/ranked.csv` and fixed the `eko`→`elo` batch_name typo; Elo chain verified continuous (53 rows, ends 793.6).

## [2026-05-28] revise | knowledge-base | Project-wide orientation + chess framing fix
- Root cause: a cold LLM read of the KB misread the chess experiment's purpose — the "improve infrastructure, not the model" hypothesis and the baseline definition were implicit/scattered, and the central concept page didn't link to the experiments. Fixed after re-grounding against `../Essay/essay.tex`.
- Created `OVERVIEW.md` — top-level "start here" orientation: thesis argument, four-component framework, six-experiment evidence table, baseline definition, cold-start reading order. Linked from `README.md`, `CLAUDE.md`, and `index.md`.
- Rewrote opening of `work/experiment-chess.md`: added "hypothesis in one sentence," crisp baseline definition (model + `list_legal_moves` + `make_move` = the human-told-only-the-rules analogue), the PR-as-configuration / ranked-batch-as-calibration cycle, and the bug-fix-vs-configuration distinction.
- Updated `wiki/concepts/agent-infrastructure-vs-capability.md`: added the primary research question + human-productivity framing up top; populated the previously-empty `related_work` with all six experiments so the central claim links to its evidence.

## [2026-05-28] revise | knowledge-base | Diary authorship model + scope PR-as-configuration to chess
- Corrected a contradiction: CLAUDE.md/README previously labelled `diary/` as "user-authored" and said "preserve the user's voice in diary." Actual model: diary entries are **LLM-written under the user's supervision** — the user decides when an entry is written and its gist; the agent writes it; the agent may *suggest* writing one but must never start one unprompted; the user may also write entries directly. Added a "Diary authorship" section to CLAUDE.md, carved `diary/` into its own ownership role (#4, supervised LLM-authored), updated the directory tables in CLAUDE.md + README, and gated the capture/inbox "reflection → diary" routes on an explicit user request. Also fixed flat-path drift (`diary/YYYY-MM-DD.md` → `diary/<work-slug>/YYYY-MM-DD.md`).
- Scoped the PR-as-configuration / ranked-batch-as-calibration cycle to the chess experiment only: added an explicit "this cycle is specific to the chess experiment" note to `work/experiment-chess.md`. (OVERVIEW.md never claimed it project-wide; the project-wide "baseline = model + irreducible minimum" notion stays general, per user confirmation.)

## [2026-05-28] lint | knowledge-base | Full lint pass: index coverage, link integrity, orphans, contradictions
- **Index coverage:** added 4 missing chess methodology ADRs to `index.md` (`2026-05-26-agent-turn-memory`, `2026-05-26-single-step-matchmaking`, `2026-05-27-run-script-args-list`, `2026-05-27-single-writer-move-contract`). Literature/concepts/work/manuscript-notes were already complete. Index now covers all catalogued files.
- **Dead wikilinks fixed** in `diary/experiment-chess/2026-05-27.md`: `[[2026-05-mirko-gemma-ollama-pydantic-recipe]]` → `[[mirko2026gemma]]`; `[[2026-05-mayo-gemma4-tool-calling-fs-python]]` → `[[mayo2026gemma4tools]]`; `[[productivity-as-infrastructure-stack]]` → `[[agent-infrastructure-vs-capability]]`.
- **Broken frontmatter refs fixed:** dropped non-existent `experiment-calibration` from `related_work` in `hutchins1995wild.md` and `norman2013design.md` (no such experiment — calibration is a cross-cutting *thread*, not an experiment); dropped non-existent concept slugs `methodology`/`case-study-method` from `yin2018case.md` `related_concepts`.
- **Contradiction — matchmaking:** `work/experiment-chess.md` described streak-based *doubling* as the current opponent-selection rule, but [[2026-05-26-single-step-matchmaking]] had reverted it to single-step. Rewrote the bullet to state single-step as current and cite the supersession; added a `partially_superseded_by` banner to [[2026-05-20-elo-and-batch-runner]] (its §3 only — formula/batch-runner/provenance still stand). This also resolved the single-step ADR's orphan status.
- **Contradiction — initial ELO (experiment repo, outside KB):** `experiments/chess/CLAUDE.md` and `experiments/chess/README.md` still stated "Initial agent ELO is 600" citing the superseded ADR, contradicting the live data (1200 → 684.2) and [[2026-05-25-initial-elo-1200]]. Updated both to 1200 with supersession note; refreshed the ADR list in the experiment CLAUDE.md. (Historical diary/ADR/log mentions of 600 left intact — correct as time-stamped records.)
- **Orphans:** down to 1 — today's `diary/experiment-chess/2026-05-28.md`, a newest-leaf entry that links outward to 7 nodes (not a disconnected island). Resolved `2026-05-24.md`'s orphan by linking it from the work page's eX3-backend bullet. Added a `related_decisions` frontmatter field to `work/experiment-chess.md`.
- **Flagged, not changed (raw/ is user-owned):** the literature source file is named `raw/literature/Yin(2028).pdf` (should be `Yin(2018)`); the `raw_path` pointer correctly matches the actual filename, so left as-is — rename the raw file if desired and I'll update the pointer.

## [2026-05-28] revise | yin2018case | Fix Yin source-file year typo (2028 → 2018)
- Renamed `raw/literature/Yin(2028).pdf` → `Yin(2018).pdf` (user-approved) and updated the `raw_path` in `wiki/literature/yin2018case.md` to match. No other references to the old filename existed.

## [2026-06-01] update | module-llm-server + ex3 | hgx2q verified, partition order corrected, broken wikilink fixed
- **`work/module-llm-server.md`** — four corrections + strengthening:
  1. Wrong tool-call-parser flag: `--tool-call-parser pythonic` → `--tool-call-parser gemma4` everywhere (body, critical flags, open todos). `pythonic` is the Llama 3.2/4 parser; using it with Gemma 4 causes tool calls to leak as plain text (vLLM issue #39043).
  2. Partition recommendation inverted: hgx2q (2× A100 80GB, no offload, lower latency) is now recommended; gh200q (1× GH200, CPU offload, higher latency) is fallback. Verified 2026-06-01 with 128k context, TP=2, no offload on g002.
  3. Closed open todo: "Re-attempt hgx2q" marked done (✓ 2026-06-01).
  4. Added `--attach <job_id>` usage note for reconnecting to long reservations; added TP power-of-2 constraint note; added latency column to partition table; added frontmatter `status: in-progress`.
- **`wiki/concepts/ex3.md`** — gh001/gh002 (GH200 96GB HBM3, gh200q) added to hardware table (were missing); "best options" prose updated to reflect hgx2q as current default; `updated` bumped to 2026-06-01.
- **`wiki/literature/mirko2026gemma.md`** — `[[tool.uv.index]]` (TOML syntax accidentally parsed as wikilink) escaped to `[tool.uv.index]` (single brackets). This was the only broken wikilink in the wiki layer.

### Lint pass — 2026-06-01
- **Link integrity:** 62 wikilinks checked; 0 broken (after mirko fix above).
- **Orphans:** none.
- **Status drift:** `experiment-chess` in-progress, last diary 2026-05-28 — current. All other experiments `planning`; no diary expected yet.
- **Concept pages:** all 16 remain `status: draft` — user promotion decision pending.
- **Flagged, not changed:** all 14 non-infra concept pages and the 5 non-chess experiments have not been touched since mid-May. No contradictions found. No missing concept pages identified.

## [2026-06-01] capture | gemma4-vllm-pydantic-ai integration | New concept page + module-llm-server update
- Created `wiki/concepts/gemma4-vllm-pydantic-ai-integration.md`: three-layer stack explanation (pydantic-ai → vLLM → Gemma 4); Gemma's native tool format (brace-key syntax, uppercase types, `<|tool>` delimiters); vLLM tool-call parser requirement (`gemma4` not `pythonic`); thinking channel stripping mechanics; two pydantic-ai profile mismatches (`strict`, `tool_choice_required`) and their fixes; multi-turn thinking history rule; recommended sampling params; summary table of working/broken/pending items.
- Updated `work/module-llm-server.md`: added "pydantic-ai profile configuration" section with the two-field fix and a pointer to the new concept page.
- Updated `index.md`: added `gemma4-vllm-pydantic-ai-integration` to the Infrastructure section.

## [2026-06-01] schema | knowledge-base | Added raw/discussions/ directory type
- Updated `CLAUDE.md`: added `raw/discussions/` to the directory table (user-owned; extended dialogues and reflections); added processing rule to the Ingest section (discussions route to the concept layer as captures, not to wiki/literature/).
- Added **Discussions** section to `index.md` with pointer to the first file and its destinations.

## [2026-06-01] process | raw/discussions/Claude Conversation on tools, mcp and skills.md | Produced 2 wiki updates + 1 idea capture
- Updated `wiki/concepts/mcp-vs-skills.md`: substantially expanded with MCP transport mechanics, the skill-as-package-not-protocol clarification, "ship with the skill" insight, state/knowledge split, the lazy-typed-tool synthesis idea, LSP and HCI analogues (Norman, HATEOAS, capability-based security).
- Created `wiki/concepts/capability-delivery-dimensions.md`: six independent axes (invocation format, transport, state ownership, context economics, packaging/ownership, determinism); pre-paradigmatic field assessment; HCI analogues; three-party interface model with trust asymmetry on interface C.
- Appended idea to `admin/ideas.md`: harness that auto-wraps bundled skill scripts as lazy-revealed typed tools on skill-load (Pydantic entrypoint → JSON Schema; `list_changed` notification; stateless vs. stateful handling).
- Updated `index.md`: added `capability-delivery-dimensions` to the Concepts section.

## [2026-06-01] capture | typed-tool harness spec | Decision record + concept updates from user design spec
- Created `decisions/2026-06-01-typed-tool-harness-spec.md`: typed-tool contract (AST extraction → Tool.from_schema → prepare-gating on persisted activated_skills); import-context fix (cwd=skill_root + dual PYTHONPATH); path-safety gap note for list_skill_files; eX3 prefix-cache and Gemma parser caveat.
- Updated `wiki/concepts/skills-component.md`: added "Typed-tool contract: progressive disclosure + native schemas" section — prepare-gating mechanism, activated_skills lifecycle change, pre-invocation validation benefit.
- Updated `wiki/concepts/mcp-vs-skills.md`: promoted synthesis note to link decision record; replaced vague "idea" framing with the confirmed pydantic-ai 1.73.0 mechanism.
- Updated `index.md`: added decision record under Infrastructure.
- Assumption corrections vs. live code: (1) activated_skills clears per-run in _reset_run_state (agent.py:422), not per HistoryProcessor — "persist across turns" is a proposed change; (2) cwd=None in run_script (skill_tools.py:474) is a confirmed sibling-import bug; (3) read_reference uses whitelist-only path safety, not resolve+assert containment.

## [2026-06-02] diary | experiment-chess + meta | Typed-tool harness verified; chess game end-to-end
- Created `diary/experiment-chess/2026-06-02.md`: harness implementation summary (AST extraction, prepare-gating, activated_skills lifecycle fix, run_script removal); ModelRetry correction (prepare re-runs per step); chess game verification on eX3 (Gemma 4 31B, TP=2).
- Created `diary/meta/2026-06-02.md`: thesis-level reflection — harness is now the standard execution model for all experiments; why it matters beyond chess; two operational caveats (prefix-cache bust per use_skill call; activated_skills persistence across turns).

## [2026-06-10] capture | decisions/2026-06-10-structured-turn-memory.md | Structured turn memory ADR (supersedes 2026-05-26-agent-turn-memory)
- New decision record: make_move gains an optional standing `plan` channel that persists across turns; reasoning note stays per-move; aggressive forgetting otherwise. Documents and fixes the latent bug where the HistoryProcessor injection dropped the system prompt from every turn after the first (verified against pydantic-ai 1.99 with a FunctionModel probe).
- Authored by Claude (Fable 5) during the autonomous mating-patterns-and-strategy work session; see diary/experiment-chess/2026-06-10.md (pending) for the session record.

## [2026-06-10] diary | experiment-chess + meta | Mating-patterns-and-strategy session; Fable 5 delegation reflection
- Created `diary/experiment-chess/2026-06-10.md`: the full branch session — Capablanca ingestion (FEN-verified), nine wiki pages, mate & draw radar, structured turn memory + system-prompt bug fix, puzzle mode, three live test rounds on eX3 with results (mate-in-1 and K+Q conversion now solid; two-rook/K+R technique remains beyond the bare model).
- Created `diary/meta/2026-06-10.md`: Andreas's test of Fable 5 on a large loosely-specified delegation — written by the model itself at his request, with that caveat stated in the entry.
- Updated `wiki/concepts/gemma4-vllm-pydantic-ai-integration.md`: new pitfall section — history processors must re-inject the SystemPromptPart or all turns after the first run with no system prompt (the 2026-05-26→06-10 chess bug).

## [2026-06-11] capture | decisions/2026-06-11-pattern-triggers.md | Pattern-trigger fairness ADR
- Settles wiki-driven mating-pattern hints: fire on geometry-present (must still fire when refuted), every hint traces to a wiki page (template_ frontmatter + one generic matcher), spam-capped. Same record covers the agent-composed threat primitive (imagine fen=/pass) and the tutor-side wiki validator.
