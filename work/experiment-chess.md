---
type: experiment
status: in-progress
related_concepts: [skills-component, data-component, deterministic-tools-hypothesis, learning-as-temporal-dimension, calibration-thread]
related_work: [experiment-math, experiment-riksantikvaren, module-skillful-agent, module-llm-server]
sources: [ericsson1993deliberate, sequoia2026karpathy, karpathy2025wiki]
related_decisions: [2026-05-20-elo-and-batch-runner, 2026-05-26-single-step-matchmaking, 2026-05-25-baseline-calibration-complete, 2026-05-25-initial-elo-1200, 2026-06-02-chess-agent-wiki-architecture, 2026-06-02-tool-fairness-rulebook, 2026-06-20-defer-minor-piece-mates]
updated: 2026-06-20
---

# Experiment: Skill-Acquisition Trajectory and Chess Tournament

Exercises the **Skills** and **Knowledge** chapters. Estimated effort: ~4–5 weeks combined. The largest single piece of experimental work in the thesis and the one most likely to expand — see [[risk-register]].

## The hypothesis in one sentence

**We hold the model fixed and improve everything around it.** The claim
under test is that the same things that make *humans* better at a task —
accumulated skills, better tools, written-down procedural knowledge,
deliberate practice against feedback — can be applied to an AI agent to
make it measurably better at that task *without changing the model's
weights*. This is the thesis's central claim ([[agent-infrastructure-vs-capability]])
brought down to a single concrete, externally-scored task: chess.

The model never gets smarter. The *infrastructure* around it — in this
experiment, the chess skill (its SKILL.md plus the perception/analysis
scripts bundled with it) and the harness that runs it — is what
improves. Elo is the external critic that says whether the improvement
was real. This is the agent analogue of deliberate practice
([[ericsson1993deliberate]]) and of the scientific method as productivity
infrastructure: a self-correcting loop where game outcomes play the role
peer review and replication play for human researchers. See the essay
§3.7 and Experiment 5 (`../../Essay/essay.tex`) for the canonical
statement.

## What "baseline" means here

The **baseline** is the bare model given *only the two tools required to
play legally at all*: `list_legal_moves` (read the legal moves) and
`make_move` (commit one of them). Nothing else — no perception scripts,
no analysis, no notes, no engine.

This is the irreducible minimum, and it is deliberately the analogue of
**a human who has been told the rules of chess and the legal moves in
front of them, and nothing more**. A true zero-tool baseline is
impossible (the agent would produce illegal moves and break the laws of
the game), so "model + the two legality tools" *is* the floor. Everything
the experiment measures is the contribution of infrastructure *added on
top of this floor*.

The bare-model baseline was calibrated at **≤ 700** (recorded 684.2,
bounded by the chess.com pool floor). See
[[2026-05-25-baseline-calibration-complete]]. All subsequent
configurations continue from that number — the trajectory upward *is*
the result the experiment is measuring; there is no reset.

## The experimental cycle: PR = configuration, ranked batch = calibration

*This cycle is specific to the chess experiment.* It may be adopted for
other experiments later, but as of now it is not a project-wide
methodology — it is how Phase 1 of *this* experiment advances.

Phase 1 advances in discrete, version-controlled increments:

1. **A PR is one increment of infrastructure improvement.** Work on a
   branch — add a perception script, sharpen the SKILL.md workflow,
   add a new analysis tool. Sanity-check with experimental games (Elo
   frozen) on the branch.
2. **Merging to `main` means "this works, adopt it."** The PR becomes
   the new current configuration of the agent.
3. **A ranked batch on clean `main` formalizes the improvement** by
   re-calibrating Elo. The batch's games update `agent_elo.json`; the
   move from the previous configuration's Elo to this one is the
   measured contribution of that PR's infrastructure work.

The **PR is the unit of "agent configuration version,"** not the commit.
`git revert` on a PR reverses both the code and the calibration rows it
produced together. See [[2026-05-24-ranked-vs-experimental]].

**Bug-fixes are not configuration changes.** A change that only stops
games from *breaking* — fixing a parser that rejected well-formed tool
calls, repairing a crashed browser session — does not add capability or
chess knowledge, so it is not a new "configuration" even when it runs on
a ranked batch. It restores the configuration to measuring what it was
always supposed to measure. A configuration change is one that gives the
agent a *new or better way to play*; a bug-fix removes an obstacle to the
agent playing at all. Only the former is a datapoint on the
skill-acquisition trajectory.

## Two phases

Within that frame, the experiment tests two claims jointly:

1. A self-correcting learning loop produces measurably better agents over time.
2. The resulting skills and tools meaningfully outperform raw inference — and meaningfully *under*perform a deterministic strong-play tool (the chess engine), in line with [[deterministic-tools-hypothesis]].

### Phase 1: Skill-acquisition trajectory

A human-supervised agent plays games against bots in an Elo-matchmaking pool, identifying its weaknesses after each batch of games using a game-analysis API, and writing skills, documentation, and helper tools into a persistent library.

Runs until Elo plateaus. The plateau criterion is defined *before starting*; resisting extension is part of the risk mitigation.

**Measures, phase 1:**

- Elo over time.
- Size and structure of the library (number of skills, dependencies, naming patterns).
- Which skills are retrieved most frequently — and which are written but never used.

This is the agent analogue of deliberate practice [[ericsson1993deliberate]] and the productivity-as-infrastructure claim playing out at the skill-acquisition layer. See [[learning-as-temporal-dimension]] and [[skills-component]].

### Phase 2: Chess tournament

The library is *frozen* as a fixed artefact. Three configurations compete in a tournament alongside calibrated bots at varying Elos to give a meaningful Elo computation.

**Configurations:**

1. **Inference alone.** Fixed model, no library, no engine.
2. **Inference with the artefact.** Fixed model with the frozen skill library and helper tools from phase 1.
3. **Inference with a chess-engine API.** Fixed model with a chess engine as a deterministic strong-play tool. Upper bound and the [[deterministic-tools-hypothesis]] limit case.

**Measures, phase 2:**

- Computed Elo per configuration.
- The gap between configurations 1 and 2 (the skill-library contribution).
- The gap between configurations 2 and 3 (the deterministic-tool contribution beyond procedural knowledge).
- Calibration of move-evaluation against the engine where applicable.

## The deeper thesis claim under test

Karpathy's [[sequoia2026karpathy]] observation that the chess-capability jump between GPT-3.5 and GPT-4 was largely a lab data-curation decision is the lab-side version of this experiment's user-side claim: that the same kind of gain can be reached *around* a fixed model by skill accumulation rather than by retraining.

This is also the framework's claim that the data and skills components can be filled in automatically rather than requiring manual curation. See [[data-component]] and [[learning-as-temporal-dimension]].

## Cross-domain transfer

Flagged as future work in [[open-questions-future-work]]; explicitly out of scope here. The chess experiment tests within-domain accumulation; whether the same loop produces transferable structure is a separate question.

## Risk

The largest scope-creep risk in the thesis. Mitigations are in [[risk-register]]: plateau criterion defined up front, phase 2 not extended beyond Elo measurement.

## Methodology: white-only across both phases

The agent learns to play *white only*. Phase 1 trains white-only; Phase 2 evaluates all three configurations playing white against a shared pool of black-playing opponents. The white-advantage cancels across configurations because they all get it equally; what is preserved is the relative ranking via shared-opponent Elo. What is given up is direct head-to-head Config-vs-Config matches.

Implication: the matchmaking pool used in Phase 1 and the tournament pool in Phase 2 can be the *same* pool. Phase 1 builds the library against pool X; Phase 2 freezes the library and measures all three configs against pool X.

Caveat to disclose in write-up: white-only Elo against a fixed bot pool is *internal* Elo and is not directly comparable to FIDE or Lichess Elo. The thesis claim depends on relative comparison across configurations, which is preserved.

Time controls are excluded. The agent's move latency is dominated by API and network, not by chess-skill time management; including time would add complexity without measuring what the experiment is about.

## Implementation architecture

Settled 2026-05-16; full reasoning in [[diary/experiment-chess/2026-05-16]].

Initial Phase 1 scaffold built 2026-05-18; see [[diary/experiment-chess/2026-05-18]]. The experiment source lives outside the knowledge base at `experiments/chess/`.

### Stack

| Layer | Choice |
|---|---|
| Rules engine | python-chess |
| Backend | FastAPI |
| Frontend board | chessground (the widget Lichess uses; headless on rules) |
| Frontend ↔ Backend | SSE for state, POST for human moves |
| Agent ↔ Backend | Direct API (the agent is just another `Player`) |
| Agent reasoning UI | Separate SSE side-channel from the agent harness |
| Engines | Stockfish (Phase 2 Config 3, plus post-game analysis); Maia Chess (opponent pool for 1100-1900 ELO); chess.com Engine bots via Playwright (opponent pool for 700-3200 ELO since [[2026-05-25-chesscom-pool-floor]] — driver still supports the full 250-3200 slider, but the bottom three positions are excluded from the experiment's pool because games converge on time-cap draws) |
| Logging | CSV + per-game PGN/JSON files in git |
| Query | pandas |
| Skill library | Separate git repo; SHA logged per game |
| Agent's chess knowledge | Parallel LLM wiki (openings / patterns / endgames / game-analyses) |

### Player abstraction

The backend orchestrates. Each side of the board is configured to a `Player` implementation:

```
class Player:
    async def get_move(self, board: chess.Board) -> chess.Move: ...

HumanPlayer  -> blocks on a queue filled by frontend POST
EnginePlayer -> wraps a UCI engine via python-chess.engine
AgentPlayer  -> hits the agent's API
```

Game creation is config: `POST /games { white: "agent", black: "maia-1500" }`. Switching between configurations is per-side, no orchestration code changes.

Critical design choice: **the backend orchestrates, not the frontend.** Phase 1 is fundamentally headless — a matchmaking pool of hundreds or thousands of games cannot depend on a running browser tab. The frontend is one optional adapter; the same backend runs Phase 1 training with no frontend at all.

### Phase 1 scaffold status: 2026-05-18

The first implementation is a testing scaffold, not yet the agent-learning loop:

- `experiments/chess/backend/` — FastAPI + python-chess service with `HumanPlayer`, `MaiaPlayer`, one backend-owned current game, singleton endpoints (`GET /api/game`, `POST /api/game/moves`, `GET /api/game/events`), and compatibility ID routes.
- `experiments/chess/frontend/` — React + Vite + chessground UI with white/black player selectors, Maia Elo selector, board interaction, current-game reload on refresh, status panel, FEN, and SAN move list.
- `experiments/chess/diary/` — local experiment diary for implementation notes before these are summarized into the main knowledge base.

The backend intentionally owns exactly one in-memory current game during this stage. Creating a new game replaces it. Refreshing the frontend reloads the current game from the backend; restarting the backend clears it. This matches the current manual-testing workflow and avoids making the browser the source of truth.

Lc0 was installed locally and the Maia-1 weights for Elo 1100-1900 were downloaded into the experiment folder. Backend tests cover player validation, legal/illegal moves, singleton current-game behavior, game replacement, finished-game rejection, mocked Maia creation, and SSE initial state. Frontend production build passes.

### Opponent pool: Maia + chess.com Engine bots

Maia covers 1100-1900 ELO with the lc0-based weights already installed. For the sub-1100 range (the agent at gpt-4o-mini plays around 300 raw) and for the 1900+ range used in tournament evaluation, the experiment uses chess.com's Engine bots via the `chesscom-driver` package built 2026-05-19 (see [[diary/experiment-chess/2026-05-19]]). Engine bots cover 250-3200 ELO in 25 discrete steps with no time control, accessed by driving real Chrome with Playwright. The package is a sibling of `backend/` and `frontend/` at `experiments/chess/chesscom-driver/`; the backend integrates via a `"chesscom"` `PlayerConfig.type` and a `ChessComPlayer` adapter in `app/players.py`. The package import is guarded so the backend works without it installed.

End-to-end working as of 2026-05-20 (see [[diary/experiment-chess/2026-05-20]]). The lifecycle is: lobby restricts chess.com to black-only and agents to white-only; ELO is a dropdown of the 25 actual slider ratings; `create_game` eagerly launches a fresh Chrome (ephemeral `tempfile.mkdtemp()` per game, not the persistent `chesscom-profile/` of the original design) so the frontend either gets a working game or a clean 502 error; game-over awaits `Game.close_players()` which quits Chrome and wipes the temp dir; new games close the prior game's players before launching. Active chess.com games are not resumable across backend restarts (the browser session is gone) — `load_game()` refuses with a 400; the BoardPage works around this by trying `GET /api/games/{id}` first, falling back to `POST /load` only if the game isn't already in memory. The driver itself was updated for chess.com's current DOM: dismiss the intro modal, hide the OneTrust cookie banner via JS, scroll the Engine group into view at the bottom of the bot-group list, expand, drive the slider, click Play. The first agent-vs-chess.com game ran to completion (chess.com won by checkmate at ELO 850).

Lichess bots were considered for the low-ELO range but rejected: every Lichess game requires a time control, and time controls are excluded from this experiment (agent move latency is dominated by API/network, not by chess-skill time management, so timing the agent measures the wrong variable).

### Logging schema

Files-in-git rather than a database, because the data is part of the thesis artefact and should be git-diffable. See [[decisions/2026-05-20-elo-and-batch-runner]] for the original schema and [[decisions/2026-05-24-ranked-vs-experimental]] for the two-CSV split.

**Two CSVs, one schema.** Agent games are written to one of two files based on the live git state at record time:

- `games/ranked.csv` — game played while the repo is on `main` with a clean working tree. **Updates `agent_elo.json`.** This is the official thesis record.
- `games/experimental.csv` — every other game: lobby agent games, batches run from a feature branch, batches with uncommitted changes. **Does not update `agent_elo.json`.** Preserves iterative work behind a PR plus everything tried during exploration.

Columns (both CSVs): `game_id`, `batch_id`, `batch_name`, `datetime`, `phase` (`ranked`/`experimental`), `branch`, `commit_sha`, `white_type`, `black_type`, `opponent`, `opponent_elo`, `result`, `aborted_reason`, `elo_before`, `elo_after`, `model`, `temperature`, `agent_log_path`, `analysis_path`. Aborted games (player exception mid-play) have `result=""` and a non-empty `aborted_reason`. The `analysis_path` column is empty by default; it's populated when a game is sent to lichess / chess.com / another tool for external analysis. Non-agent games (e.g. human-vs-Maia tests) are NOT logged.

Other artefacts (also tracked in git):

- `games/<game_id>.json` — persisted board state for resumability and replay.
- `games/<game_id>_agent.json` — agent reasoning trace (prompt, streaming events, tool calls, move chosen) per turn. Evidence per move for thesis analysis.
- `games/agent_elo.json` — materialised view of `ranked.csv`'s ELO trajectory. Could be rebuilt from `ranked.csv` alone; cached here for cheap reads.
- `batches/<batch_id>.json` — per-batch state. Also tracked.

A **batch** is a sequence of agent games sharing a pool (Maia or chess.com) and a user-supplied label. In `ranked` mode the ELO updates after each game and the next opponent is chosen by [[decisions/2026-05-20-elo-and-batch-runner]]'s win-up / loss-down / draw-down rule. In `experimental` mode the ELO is frozen — opponent selection still uses the live ELO state but doesn't write back.

**PR-as-version.** The intended workflow is: branch off main → iterate (experimental games for sanity-checking) → merge to main → run the official calibration batch on main (ranked games) → commit. Reverting a PR with `git revert` reverses both the code change and its calibration CSV rows together. PRs (not individual commits) are the conceptual unit of "agent configuration version"; closed-without-merge PRs leave their experimental rows as a research record of what was tried and rejected. See [[decisions/2026-05-24-ranked-vs-experimental]].

### ELO methodology (2026-05-20)

See [[decisions/2026-05-20-elo-and-batch-runner]] for the full record. In brief:

- Classical Elo update; **adaptive K** (40 for the first 15 games, 20 after — mirrors FIDE's provisional-player rule).
- **Initial ELO 1200** — "casual amateur novice" anchor, conventional in scholastic/amateur chess. Documented as a convention, not a canonical value. See [[decisions/2026-05-25-initial-elo-1200]] (current); [[decisions/2026-05-24-initial-elo-600]] is the superseded earlier choice.
- **Opponent selection: single-step stepping (current).** Anchor to the nearest pool rating, then move one grid notch up on a win, one down on a loss/draw. This is the current rule per [[decisions/2026-05-26-single-step-matchmaking]], which reverted the streak-based *doubling* (`2^(|streak|-1)`, capped at 4) introduced on 2026-05-20 ([[decisions/2026-05-20-elo-and-batch-runner]] §3): on the compressed 700/850/1000 low end the doubling over-stepped and oscillated rather than converging.
- Sampling temperature: 1.0 (vLLM/Azure OpenAI default — `skillful-agent` does not configure one).
- **Inference backend (as of 2026-05-24): self-hosted Gemma 4 31B-it on eX3** via [[module-llm-server]] (`http://localhost:11500/v1`); the switch from Azure is recorded in [[diary/experiment-chess/2026-05-24]]. `agent_player._build_agent` branches on `SKILL_AGENT_EX3_BASE_URL` → `SKILL_AGENT_AZURE_ENDPOINT` → OpenAI. Backend swap is one `.env` toggle. The model used for each game is recorded in the `model` CSV column; the per-game `branch` and `commit_sha` columns capture the repo state at that moment.
- One pool per batch (Maia or chess.com), chosen at batch-creation time in the UI.
- **chess.com pool floor: 700** ([[decisions/2026-05-25-chesscom-pool-floor]]) — slider positions 1–3 (250/400/550) excluded because games at those ratings converge on time-cap draws.
- Stockfish provides a live advantage needle for any active game (`eval_cp` / `eval_mate` on `GameState`); independent of the agent's view.
- **Reasoning must precede the move** — system prompt enforces an explicit ordered sequence; text after `make_move.py` is labelled "post-move" in the UI and treated as post-hoc, not move-influencing. See [[decisions/2026-05-24-reason-before-move]].
- **Per-turn fresh context** — `AgentPlayer.get_move()` calls `clear_conversation()` at the start of every turn. The agent enters each turn seeing only the system prompt, skill list, and one user message (opponent's last move + FEN). The FEN encodes complete game state; cross-turn memory is a separate variable for future experimental configurations. See [[decisions/2026-05-24-per-turn-fresh-context]].
- **`make_move.py` validates the move via POST /api/games/{id}/agent-commit; the bot loop pushes it.** The endpoint is a pure validator — never mutates `game.board`. On `ok=true` the agent's turn is over; the bot loop reads the canonical UCI from the script's stdout and pushes the move under its own lock, the same way it pushes moves returned by every other player (Maia, chesscom, human). This keeps one writer and removes the side-channel mutation that produced two race-prone code paths under the previous `/agent-move` design. Up to `_MAX_ATTEMPTS=10` fresh-context attempts per chess turn; per-response `max_tokens=1024`, per-run `max_turns=16`. A per-attempt budget warning fires at 70% of `max_turns` and prepends a "commit now" reminder to the next retry — see [[decisions/2026-05-26-stabilization]]. See `diary/experiment-chess/2026-05-25` for the original redesign trace and `diary/experiment-chess/2026-05-27-single-writer-refactor` for the validator-only rewrite.
- **Agent resigns when it cannot commit a move.** After exhausting `_MAX_ATTEMPTS` retries, the game ends `0-1` (agent loses, ELO drops); `aborted_reason="agent_resigned_no_move"` preserves the forensic detail. Context-overflow and environmental errors still abort without ELO change. See [[decisions/2026-05-25-agent-resigns-when-stuck]].
- **Aborted games are recorded but not counted toward ELO.** Player exceptions other than `AgentResignedError` produce `result=""` with a non-empty `aborted_reason`; ELO unchanged; the batch advances.
- **Ranked vs experimental gating.** A game updates `agent_elo.json` and writes to `ranked.csv` only if the repo is on `main` with a clean working tree; otherwise it goes to `experimental.csv` with ELO frozen. PRs are the unit of "agent configuration version". See [[decisions/2026-05-24-ranked-vs-experimental]].

### Bare-model baseline (calibration complete, 2026-05-25)

The bare-model agent (Gemma 4 31B-it, no skill library, no helper tools) was calibrated over 26 ranked games against the chess.com pool. Result: ELO 1200 → **684.2** (22 losses, 4 draws, 0 wins). After game 4 the matchmaker reached the chess.com pool floor (700) and every subsequent game was played there; the streak counter continued downward but was clamped by the floor.

**Methodologically: the bare-model agent's true ELO is ≤ 700. The recorded 684.2 is a ceiling, not a point estimate** — the pool floor bounds the measurement. The four draws observed at chess.com-700 corroborate the pool-floor rationale that games at this level converge on time-cap draws regardless of agent skill.

Subsequent batches (skill-library configurations) continue from `agent_elo.json` as-is — no reset. The visible upward (or downward) drift from 684.2 is the trajectory the experiment is measuring. See [[decisions/2026-05-25-baseline-calibration-complete]].

## Tool-fairness rulebook

The experiment turns on a methodological commitment about which tools the agent is allowed to use. The rule:

> **Mechanics tools are always fair. Retrieval tools are fair if-and-only-if the corpus they retrieve over was built through the learning loop.**

**Mechanics tools (always allowed).** `legal_moves()`, `what_if(move) -> board_after`, `is_attacked(square)`, `piece_values`, `list_pieces_attacking(square)`, geometric pattern detection (back-rank vulnerabilities, pin detection, etc.). These read the board without encoding chess knowledge.

**Retrieval tools (allowed if corpus is agent-curated).** `search_my_notes(position)`, `retrieve_opening_theory(moves_so_far)`. The retrieval algorithm can be arbitrarily smart (vector search, indexing, semantic similarity) — the question is *what* it retrieves over. A GM with an organised notebook does not sequentially scan every page; they use an index. The deterministic-tool equivalent is fine for the same reason.

**Retrieval tools (cheating).** Pre-loaded vector databases of "all positions from these books" without the agent having processed them through the loop. Pre-curated Stockfish evaluation tables. `recognize_opening()` backed by an externally-built encyclopedia. The retrieval algorithm being trivial does not redeem a contaminated corpus.

**Subtle case.** The agent reads a chess book during Phase 1 and writes its own notes about positions into its wiki. Those notes become agent-curated corpus even though the source material was external. The act of reading-and-noting is part of the loop. What is *not* allowed is dumping book content into a vector DB the agent has never processed.

**Calculation.** Allowed, but the agent must drive the search. `what_if_i_play(move) -> board_after` is fine — the agent decides whether to recurse manually. A tool that returns "the best 3-move sequence from here" is a chess engine with the interface filed off and is not allowed.

**Stockfish and Lichess.** Allowed for post-game analysis only — synthesising what went wrong, building skills/notes from the analysis. **Not allowed during play** in Configs 1 or 2, because Config 3 is the engine-during-play condition and the deterministic-tools-hypothesis test depends on that contrast being clean.

This rulebook is now the settled ADR [[decisions/2026-06-02-tool-fairness-rulebook]]; see also the [[tool-fairness]] concept page.

## Knowledge structure: the agent's own LLM wiki

The agent's accumulated chess knowledge is structured as a parallel LLM
wiki, the same [[karpathy2025wiki]] compiled-synthesis pattern as this
thesis knowledge base, with a chess-specific schema and a per-turn
fresh-context reader. Architecture, retrieval mechanism, page contract,
and seeding strategy are fixed in
[[decisions/2026-06-02-chess-agent-wiki-architecture]]. In brief:

- The wiki **is the chess skill's `references/` directory** — exactly
  what `references/` is for in skillful-agent (files read for knowledge).
  No new harness mechanism needed.
- Folders: `openings/`, `principles/` (short heuristics), `strategic-thinking/`
  (long-term planning, with `pawn-structures/` beneath it), `patterns/`
  (tactical, with `mating-patterns/` beneath it), `endgames/`,
  `game-analyses/`. Each folder has an `index.md`.
- **Retrieval is progressive.** SKILL.md points to one top-level
  `index.md`; indexes are navigation decision-trees (route by board
  condition), not tables of contents. `read_reference` loads index files
  (the only ones declared in SKILL.md frontmatter); a `search_wiki.py`
  script reaches content pages by keyword so frontmatter stays stable as
  the wiki grows.
- **Pages are capped (~400 words / ~60 lines)** with a fixed body shape
  (When to use · The idea · What to do · Watch out for · Examples) and
  frontmatter (`triggers`, `tags`, `related_pages`, `status: draft →
  tested`). `log.md` records every page write — the wiki's growth is half
  the Phase 1 data.
- **Read-only during play; maintenance at the batch boundary.** The
  per-turn agent only reads the wiki mid-game; splitting oversized pages,
  promoting `draft → tested`, writing `game-analyses/`, and fixing links
  happen during post-game analysis.

The wiki is the agent-curated corpus referenced in the tool-fairness
rule above. Pre-seeding it with synthesised theory is **fair**: it is the
agent (or its tutor) reading material and noting it, not dumping an
unprocessed corpus — the experiment is *tutored deliberate practice*
([[ericsson1993deliberate]]), not zero-start self-play. The user points
the agent in the right direction, supplies tools, and says what to read;
the agent accumulates a compounding artefact.

This gives the thesis a bonus result: a second-domain test of the LLM
Wiki pattern alongside the thesis knowledge base itself. See
[[data-component]] for the architectural framing of compiled-summary
retrieval.

## Open items before Phase 1 learning starts

1. ~~Promote the tool-fairness rulebook to a decision record under `decisions/`.~~ Done: [[decisions/2026-06-02-tool-fairness-rulebook]].
2. Confirm Maia opponent setup under experiment load — local Lc0 + Maia-1 weights are installed for testing; latency and throughput still need measurement.
3. Define the Phase 1 plateau criterion concretely (already flagged in [[risk-register]]; needs a number before first game).
4. Defer until Phase 1 runs: whether to use cutechess-cli / fast-chess for Phase 2 tournament management by wrapping the agent as a UCI engine.
5. **Plan the memory/context configuration axis.** Baseline runs with per-turn fresh context (see [[decisions/2026-05-24-per-turn-fresh-context]]). When the skill-library experiment begins, decide what memory configuration the agent gets — likely sliding window or auto-compaction — and measure the ELO delta against this baseline as a first-class result.
6. **Pre-flight compaction in `skill_agent`.** TODO left in `Agent._event_stream`: when `AgentContextOverflowError` fires, run `compress_all_impl` and retry once. Deferred until baseline is captured to avoid changing framework behaviour mid-measurement.
7. **ELO rebuild script.** Write `scripts/rebuild_elo.py` so `git revert` on a calibration PR can be paired with a one-command recomputation of `agent_elo.json` from the post-revert `ranked.csv`. See [[decisions/2026-05-24-ranked-vs-experimental]].

Closed by recent decisions:
- ~~Agent integration path~~ — settled: harness end-to-end via skillful-agent. See [[decisions/2026-05-23-ex3-llm-inference-server-architecture]] and [[decisions/2026-05-24-per-turn-fresh-context]].
- ~~Agent wiki architecture~~ — settled: structure, retrieval, page contract, seeding. See [[decisions/2026-06-02-chess-agent-wiki-architecture]].

## Future work / ideas

Deferred enhancements that build on the agent wiki
([[decisions/2026-06-02-chess-agent-wiki-architecture]]). Not in scope
for the initial hand-seeded wiki; noted so they aren't lost.

1. **In-game `note()` tool.** Give the agent a tool to drop a freeform
   note during a game — e.g. "left my queen hanging because I didn't see
   the bishop on b7." Notes land in the wiki's `raw/` (unprocessed source
   material). The user, as tutor, later decides what to do with each:
   write a new pattern page, add a principle, fix a perception script
   that should have surfaced the threat, etc. This is the agent's own
   error log feeding the deliberate-practice loop. Read-only-during-play
   is preserved — a note is an append to `raw/`, not a wiki edit.
2. **Lichess post-game analysis pass.** After a game finishes, pull the
   Lichess (or Stockfish) analysis of the whole game. Both the agent and
   the user read it; either can write notes and act: the agent may need a
   new pattern/endgame page, a principle revised, or a perception tool
   fixed. This is the concrete post-game maintenance step the wiki
   architecture reserves for the batch boundary — it turns each game into
   structured input for the next batch's wiki edits, and is where
   `draft → tested` promotions and new `game-analyses/` pages are
   produced. May need new tooling (analysis fetch + parse) and may surface
   gaps that call for more theory or a tool fix.

---
*Lifted from `../manuscript-notes/essay-pointer.md` (Essay/essay.tex §3.3, §3.5, §4.2-Experiment 5). Implementation architecture and methodology refined 2026-05-16 — see [[diary/experiment-chess/2026-05-16]].*
