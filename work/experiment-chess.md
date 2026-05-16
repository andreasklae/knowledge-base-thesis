---
type: experiment
status: planning
related_concepts: [skills-component, data-component, deterministic-tools-hypothesis, learning-as-temporal-dimension, calibration-thread]
related_work: [experiment-math, experiment-riksantikvaren]
sources: [ericsson1993deliberate, sequoia2026karpathy, karpathy2025wiki]
updated: 2026-05-16
---

# Experiment: Skill-Acquisition Trajectory and Chess Tournament

Exercises the **Skills** and **Knowledge** chapters. Estimated effort: ~4–5 weeks combined. The largest single piece of experimental work in the thesis and the one most likely to expand — see [[../manuscript-notes/risk-register.md]].

## Two phases

The experiment tests two claims jointly:

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

Flagged as future work in [[../manuscript-notes/open-questions-future-work.md]]; explicitly out of scope here. The chess experiment tests within-domain accumulation; whether the same loop produces transferable structure is a separate question.

## Risk

The largest scope-creep risk in the thesis. Mitigations are in [[../manuscript-notes/risk-register.md]]: plateau criterion defined up front, phase 2 not extended beyond Elo measurement.

## Methodology: white-only across both phases

The agent learns to play *white only*. Phase 1 trains white-only; Phase 2 evaluates all three configurations playing white against a shared pool of black-playing opponents. The white-advantage cancels across configurations because they all get it equally; what is preserved is the relative ranking via shared-opponent Elo. What is given up is direct head-to-head Config-vs-Config matches.

Implication: the matchmaking pool used in Phase 1 and the tournament pool in Phase 2 can be the *same* pool. Phase 1 builds the library against pool X; Phase 2 freezes the library and measures all three configs against pool X.

Caveat to disclose in write-up: white-only Elo against a fixed bot pool is *internal* Elo and is not directly comparable to FIDE or Lichess Elo. The thesis claim depends on relative comparison across configurations, which is preserved.

Time controls are excluded. The agent's move latency is dominated by API and network, not by chess-skill time management; including time would add complexity without measuring what the experiment is about.

## Implementation architecture

Settled 2026-05-16; full reasoning in [[../diary/2026-05-16.md]].

### Stack

| Layer | Choice |
|---|---|
| Rules engine | python-chess |
| Backend | FastAPI |
| Frontend board | chessground (the widget Lichess uses; headless on rules) |
| Frontend ↔ Backend | SSE for state, POST for human moves |
| Agent ↔ Backend | Direct API (the agent is just another `Player`) |
| Agent reasoning UI | Separate SSE side-channel from the agent harness |
| Engines | Stockfish (Phase 2 Config 3, plus post-game analysis); Maia Chess (opponent pool for human-like calibrated Elo bands) |
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

### Logging schema

Files-in-git rather than a database, because the data is part of the thesis artefact and should be git-diffable.

- `games/games.csv` — one row per game. Columns: `game_id`, `batch_id`, `datetime`, `opponent`, `result`, `elo_before`, `elo_after`, `skill_repo_sha`, `model`, `temperature`.
- `games/<game_id>.pgn` — full PGN.
- `games/<game_id>.json` — agent reasoning trace (tool calls, skills loaded, decisions).
- `diary/<batch_id>.json` — structured batch diary (lessons learned, actions taken, hypotheses tested).

Current Elo is computed from `games.csv` (last row's `elo_after`); no separate state.

A **batch** is the set of games played at one `skill_repo_sha`. Between batches is where the self-correction step happens — the agent updates its skill library, the SHA changes, a new batch starts. Batch is therefore the natural unit for analysing the learning loop.

`skill_repo_sha` is the commit hash of the agent's skill library (a separate git repo) at the moment the game was played. This is what makes the experiment reproducible and reversible: `git checkout <sha>` recreates the exact agent that played game N. It also makes "which actions caused the biggest Elo jump" a real question — diff SHAs between consecutive batches, read the batch diary.

## Tool-fairness rulebook

The experiment turns on a methodological commitment about which tools the agent is allowed to use. The rule:

> **Mechanics tools are always fair. Retrieval tools are fair if-and-only-if the corpus they retrieve over was built through the learning loop.**

**Mechanics tools (always allowed).** `legal_moves()`, `what_if(move) -> board_after`, `is_attacked(square)`, `piece_values`, `list_pieces_attacking(square)`, geometric pattern detection (back-rank vulnerabilities, pin detection, etc.). These read the board without encoding chess knowledge.

**Retrieval tools (allowed if corpus is agent-curated).** `search_my_notes(position)`, `retrieve_opening_theory(moves_so_far)`. The retrieval algorithm can be arbitrarily smart (vector search, indexing, semantic similarity) — the question is *what* it retrieves over. A GM with an organised notebook does not sequentially scan every page; they use an index. The deterministic-tool equivalent is fine for the same reason.

**Retrieval tools (cheating).** Pre-loaded vector databases of "all positions from these books" without the agent having processed them through the loop. Pre-curated Stockfish evaluation tables. `recognize_opening()` backed by an externally-built encyclopedia. The retrieval algorithm being trivial does not redeem a contaminated corpus.

**Subtle case.** The agent reads a chess book during Phase 1 and writes its own notes about positions into its wiki. Those notes become agent-curated corpus even though the source material was external. The act of reading-and-noting is part of the loop. What is *not* allowed is dumping book content into a vector DB the agent has never processed.

**Calculation.** Allowed, but the agent must drive the search. `what_if_i_play(move) -> board_after` is fine — the agent decides whether to recurse manually. A tool that returns "the best 3-move sequence from here" is a chess engine with the interface filed off and is not allowed.

**Stockfish and Lichess.** Allowed for post-game analysis only — synthesising what went wrong, building skills/notes from the analysis. **Not allowed during play** in Configs 1 or 2, because Config 3 is the engine-during-play condition and the deterministic-tools-hypothesis test depends on that contrast being clean.

This rulebook should be promoted to a decision record under `decisions/` before Phase 1 begins; flagged as an open item.

## Knowledge structure: the agent's own LLM wiki

The agent's accumulated chess knowledge is structured as a parallel LLM wiki, same architectural pattern as this thesis knowledge base ([[karpathy2025wiki]]), different schema:

- `openings/` — synthesised opening theory pages.
- `patterns/` — tactical and positional patterns.
- `endgames/` — endgame principles.
- `game-analyses/` — per-game post-mortems.
- `raw/` — books, prior games, post-game engine analyses (sources the agent has processed).

Compiled synthesis pages owned by the agent, with backlinks and citations to raw sources. The wiki is the agent-curated corpus referenced in the tool-fairness rule above.

This gives the thesis a bonus result: a second-domain test of the LLM Wiki pattern alongside the thesis knowledge base itself. See [[data-component]] for the architectural framing of compiled-summary retrieval.

## Open items before build starts

1. Promote the tool-fairness rulebook to a decision record under `decisions/`.
2. Confirm Maia opponent setup — local install vs. hosted endpoints; latency budget.
3. Define the Phase 1 plateau criterion concretely (already flagged in [[../manuscript-notes/risk-register.md]]; needs a number before first game).
4. Decide whether the agent uses Anthropic API directly or goes through the existing agent harness end-to-end (probably the latter — SSE + client-side-functions + tool-use plumbing already exist).
5. Defer until Phase 1 runs: whether to use cutechess-cli / fast-chess for Phase 2 tournament management by wrapping the agent as a UCI engine.

---
*Lifted from `../manuscript-notes/essay-pointer.md` (Essay/essay.tex §3.3, §3.5, §4.2-Experiment 5). Implementation architecture and methodology refined 2026-05-16 — see [[../diary/2026-05-16.md]].*
