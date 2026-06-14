---
type: decision
status: accepted
partially_superseded_by: 2026-05-26-single-step-matchmaking
---

# 2026-05-20 — ELO tracking, batch runner, and game-level provenance for [[experiment-chess]]

> **Partial supersession.** §3 (opponent-selection algorithm) — both the original single-step and the same-day doubling revision recorded below — was reverted to plain single-step by [[decisions/2026-05-26-single-step-matchmaking]]. The Elo formula, adaptive-K rule, batch runner, and provenance fields in this record still stand.

## Context

[[experiment-chess]] needs a measurable agent skill level that updates after every game, an opponent-selection algorithm that picks an appropriately matched bot for each next game, and a way to run many such games unattended so the agent's skill curve can be charted across commits to the skill library. Today we settled the methodology for all three, plus the provenance fields recorded against every agent game.

## Decisions

### 1. ELO update formula — classical Elo, adaptive K

We use the classical Elo update:

```
expected   = 1 / (1 + 10^((opponent - own) / 400))
new_own    = own + K * (result - expected)
```

where `result` is 1.0 for a win, 0.5 for a draw, 0.0 for a loss, all from the agent's perspective.

**K-factor: adaptive.** K = 40 for the first 15 games (the *provisional* phase), then K = 20 for the rest of the agent's lifetime.

Rationale:

- The provisional/stable split mirrors FIDE's rule for unrated players: K is high until enough games have been played to constrain the rating, then drops to a stable value. FIDE itself uses K = 40 for the first 30 games for new players, K = 20 for established players (and K = 10 for masters); we shorten the provisional window because our agent plays much faster than a human and we only need ~15 games to bracket its skill given streak-based matchmaking (see §3).
- Chess.com uses K = 20 for casual rapid play and a higher K (≈ 40) during the initial 10-game calibration window — the same shape we adopt.
- K = 32 (which was the value before 2026-05-20) was rejected because it gives mediocre calibration speed (≈ 30 games to converge from 1200 to a true 300 ELO) when combined with single-step opponent selection. K = 40 alone helps the *rating* move faster but the bottleneck was the opponent step size, fixed in §3.
- The K value used for each game is recorded implicitly via `games_played` in `agent_elo.json`; the CSV's `elo_before` / `elo_after` columns let analysis reconstruct it without re-running the experiment.

### 2. Initial agent ELO — 1200

Chosen as the "casual amateur novice" anchor. Rationale:

- **Industry conventions for new/unrated players cluster around 1200 in the scholastic/amateur band.** USCF (United States Chess Federation) has historically used 1200 as the unrated player's tournament-entry estimate, particularly for scholastic events. Many chess sites use 1200 as the default for new accounts before calibration kicks in, on the reasoning that it sits at the "casual player who knows the rules but has no formal training" level.
- **Lichess uses 1500 as the global mean** but accompanies it with a high rating deviation (RD), so a new player's effective bracket is wide. We don't have RD/Glicko, so anchoring at the lower end of "uncalibrated amateur" (1200 rather than 1500) gives the agent a starting point that doesn't *overstate* expected skill — important because our agent's true skill at gpt-4o-mini is below most playable opponents in either pool.
- **It sits at a useful coverage point**: 1200 is exactly mid-grid on the Maia pool (which runs 1100–1900) and is a real chess.com Engine rating (slider position 8 of 25). The first game of a fresh batch can therefore be played at *exactly* the agent's nominal rating with no rounding artefacts.

**Note for the thesis:** 1200 is conventional, not canonical — there is no universal "starting ELO" in chess. The choice is documented and justified rather than discovered. Re-running the experiment from a different starting ELO (e.g., 600 for sub-1100 calibration or 1500 for the Lichess convention) would produce the same true skill estimate after enough games — the starting point only affects how many games the calibration takes.

If we want a different starting point (e.g. 600 for sub-1100 calibration), `POST /api/agent-elo/reset` clears the state file but does not yet accept a custom value. Adding a `?elo=600` parameter would be a small change if needed.

### 3. Opponent-selection algorithm — streak-based exponential stepping

After each batch game, the next opponent is chosen by *anchoring* to the agent's current ELO on the pool's discrete grid, then *stepping* a number of grid notches in the direction of the running win/loss streak. The step size doubles with consecutive same-direction results.

**Algorithm:**

```
anchor_idx = index of the pool rating closest to agent_elo
            (ties round to the lower rating)
step       = sign(streak) * min(2^(|streak| - 1), MAX_STEP)
opponent   = pool_ratings[clamp(anchor_idx + step, 0, len(pool) - 1)]
```

with `MAX_STEP = 4` to cap how far one transition can move.

**Streak rules** (in `app.elo.update_streak`):
- Win after wins: `streak += 1`
- Loss after losses: `streak -= 1`
- Win after losses (direction flip): `streak = +1`
- Loss after wins (direction flip): `streak = -1`
- Draw: `streak //= 2` (decays toward zero — a single draw in the middle of a streak doesn't fully reset the search)

**Step examples for a |streak| of 1, 2, 3, 4+: step = 1, 2, 4, 4 (capped)** — doubling until the cap.

**Rationale:**

- The prior algorithm — closest rating *strictly above* on a win, *strictly below* on a loss/draw — took linear time to bracket the agent's true skill. An agent starting at 1200 with true skill 300 needed 5+ pure-loss games to walk down to the bottom of the chess.com pool. Empirically the "elo calibration" batch the user ran showed exactly this: every game was a slow downward walk through opponents the agent had no business playing.
- The new algorithm gives logarithmic calibration: a 4-loss streak jumps 1 + 2 + 4 + 4 = 11 grid notches in 4 games. From chess.com's idx-8 (rating 1200), 11 notches down is below idx 0 → clamped to idx 0 (rating 250). That's the right neighbourhood after 4 games, not 11.
- Doubling-with-cap is the exponential-search shape used in similar discrete-grid calibration problems (network congestion control's slow start, TCP RTO backoff, online rating-ladder calibration tournaments). It's the cheap-and-defensible version of binary search when bounds are unknown.
- TrueSkill (Halo / Xbox) would be the rigorous choice but requires switching from a point estimate (Elo) to a Bayesian distribution (μ, σ). That's a bigger methodological change than this experiment justifies — we'd lose the comparability to FIDE/USCF/chess.com Elo numbers.
- The Elo update formula is unchanged. Only opponent *selection* is affected. Methodologically the rating system is still classical Elo; the matchmaking heuristic is the only added moving part.

**Trade-off:** a single noisy game (lucky win or blunder loss) can fling the agent further than under the previous algorithm. `MAX_STEP = 4` caps the worst case; in the Maia pool that's 4 × 100 = 400 ELO, and in the chess.com pool it's a span varying from 600 to 800 ELO depending on the part of the grid. For thesis interpretation, the agent's *running average* ELO over its last ~20 games is the meaningful number, not the instantaneous value.

**Note:** because step size depends on the *current* streak rather than the most recent game alone, a sequence of mixed results converges to single-step behaviour (which is the calm, equilibrium-state matchmaking). Streak-based doubling only kicks in during the initial calibration or during a true skill gap.

### 4. Pool selection per batch

Each batch is bound to one pool — Maia or chess.com — chosen by the user at batch-creation time in the UI. Rationale:

- **Maia** is preferable inside its range (1100–1900): fast, deterministic, no browser dependency, plays human-like chess.
- **chess.com** is the only option for sub-1100 (where Maia doesn't reach) and 1900+ (where Maia stops). It's also the right choice for "the agent against a real chess.com bot" scenarios that simulate the production target.

Mixing pools inside a single batch was rejected because the methodological story is cleaner when each batch describes one opponent population. Mixed pools can be reconstructed in analysis by concatenating batch CSVs.

### 5. Temperature — 1.0 (Azure OpenAI default)

The `skillful-agent` SDK does not currently set a temperature on the pydantic-ai `ModelSettings`. Azure OpenAI's chat-completions endpoint defaults to **1.0** when temperature is not specified. We record `"1.0"` in every agent game's CSV row as the *effective* sampling temperature.

The decision *not* to override this is deliberate: the experiment tests the agent as the SDK ships, and we don't want a future SDK change that introduces an explicit temperature default to silently invalidate prior batches. If we later want lower temperature (typical for deterministic move selection), it will be a recorded change to the experiment's `pyproject.toml` skillful-agent pin, and `skill_repo_sha` will reflect it.

### 6. Skill repo SHA — git HEAD of the chess experiment repo

The chess experiment repo (`experiments/chess/`) was initialised today. Every change to the agent's skills (`backend/skills/chess-player/`), system prompt, model config, or driver code is committed there. `skill_repo_sha` in `games.csv` is the HEAD SHA at game-record time — `git -C experiments/chess rev-parse HEAD`. Cached for the process lifetime; restart the backend after a commit to pick up a new SHA.

Rationale: any of those four surfaces (skill content, prompt, model, driver) can change agent behaviour, and they all live in the same repo. One SHA captures all of them. The alternative — a separate skill-library repo — was rejected as premature: skills are still being co-developed with the agent infrastructure, and pulling them into a separate repo would create a synchronisation burden.

### 7. games.csv schema (final, as of 2026-05-20)

| Column | Source | Purpose |
|---|---|---|
| `game_id` | uuid4 hex | Primary key |
| `batch_id` | `Batch.batch_id` (uuid4 hex), or "" for ad-hoc | Groups games into runs |
| `batch_name` | user-supplied free-text label | Human-readable batch identifier ("elo calibration", "post-fix retest", etc.) |
| `datetime` | `datetime.now(UTC).isoformat()` | When the row was written |
| `white_type` / `black_type` | `PlayerConfig.type` | One of human/maia/agent/chesscom |
| `opponent` | derived | `maia-1500`, `chesscom-850`, `human`, etc. |
| `opponent_elo` | `PlayerConfig.elo` | Numeric opponent rating (for engine opponents) |
| `result` | python-chess `Board.result()` | `1-0`, `0-1`, `1/2-1/2`, or "" if aborted |
| `elo_before` | `AgentEloState.elo` snapshot at game start | Agent's rating going into the game |
| `elo_after` | `AgentEloState.elo` after Elo update | Agent's rating coming out of the game |
| `skill_repo_sha` | `git rev-parse HEAD` of `experiments/chess/` | Configuration provenance |
| `model` | `SKILL_AGENT_OPENAI_MODEL` env var | The model that played |
| `temperature` | `"1.0"` (constant, see above) | Sampling temperature |
| `agent_log_path` | `<game_id>_agent.json` or "" | Relative path to the reasoning trace JSON |

Only **agent games** are logged. Human-vs-Maia, human-vs-chesscom, and other non-agent matchups skip the CSV write entirely. This preserves the CSV as a pure agent skill log.

### 8. Batch persistence

Each batch is one JSON file at `<backend>/batches/<batch_id>.json`:

```json
{
  "batch_id": "...",
  "label": "elo calibration",
  "pool": "maia",
  "total_games": 30,
  "status": "running|paused|completed|stopped|failed|pending",
  "created_at": "2026-05-20T14:00:00Z",
  "games": [
    {"game_id": "...", "opponent_elo": 1200, "result": "win",
     "agent_elo_before": 1200.0, "agent_elo_after": 1216.0},
    ...
  ],
  "current_game_id": "<live game in progress, or null>",
  "last_error": ""
}
```

`AgentEloState` lives separately at `<backend>/games/agent_elo.json`:

```json
{"elo": 1216.0, "games_played": 1, "last_result": "win"}
```

Both are derivable from `games.csv` but the materialised files are cheaper to read and let the backend resume a paused batch across restarts.

### 9. Sequential execution, pause between turns

The batch runner plays games one at a time. The same `_game` slot in `GameService` is reused — when a game ends, `BatchRunner._handle_game_finished` triggers Elo update and creates the next game.

**Pause semantics**: pausing an agent game (either standalone or batch-driven) is honoured *between turns*, not mid-inference. A pause request flips `Game.paused=True`; the bot loop completes any in-flight `player.get_move()` then returns at the top of its next iteration. Resuming re-schedules the bot loop. Mid-inference pause was rejected as too invasive — we'd have to cancel the asyncio task and roll back or discard a partial OpenAI completion.

For batch pause: setting `Batch.status = "paused"` is observed by the runner's outer loop on its next iteration; the in-flight game continues to completion, then the runner stops creating new games until the user clicks Resume.

### 10. Agent isolation between games

Each game in a batch instantiates a fresh `AgentPlayer`, which builds a fresh `skill_agent.Agent`. No conversation state, skill cache, or message history carries between games. The agent's view of game N is identical whether N is the first game of a batch or the hundredth.

This is enforced by `PlayerFactory.create()`: agent players are constructed per-game, not pooled.

### 11. Stockfish evaluation needle

A live position eval is computed via Stockfish (`/opt/homebrew/bin/stockfish`) after every move and published on the existing board SSE channel as `eval_cp` and `eval_mate` fields on `GameState`. Centipawns are from White's perspective; mate-in-N is a positive integer for White, negative for Black.

Eval depth defaults to 15 (controlled by `CHESS_STOCKFISH_EVAL_DEPTH`). Each eval takes ~100–300 ms; runs in the background so it doesn't block the bot loop. If Stockfish is unavailable the needle is silently disabled.

Methodologically this is independent of the agent — it's a UX feature for monitoring games, not a signal the agent has access to.

## Consequences

- Reproducibility: any CSV row + `skill_repo_sha` + `model` + `temperature` is enough to reconstitute the exact agent configuration that played the game (modulo Azure model drift, which is outside our control).
- Resumability: paused or in-flight batches survive backend restarts as long as the games on disk match the batch's recorded `games[]`.
- Single-game-at-a-time: by construction we cannot run two batches concurrently. This was a deliberate choice — `GameService._game` is a single slot, and Maia/chesscom share local resources (Lc0 process, single Chrome). Parallelism would require multiple GameService instances and is rejected as scope creep.
- The batch runner is currently the only writer to `AgentEloState`. Ad-hoc games (human vs agent, lobby flow) **do not** update the agent ELO. This is deliberate: ad-hoc games are testing scaffolding, not experiment data.

## Open items

- Define the matchmaking-pool weighting for the trajectory experiment — how many sub-1100 (chesscom-only), how many mid-range (Maia), how many 1900+ (chesscom-only) games per batch. Currently the user picks one pool per batch; that may need to become a stratified sample.

## Revision history

- **2026-05-20** (initial): classical Elo with K = 32, single-step opponent selection (closest above on win, closest below on loss/draw), initial ELO 1200.
- **2026-05-20** (revision, same day): switched to adaptive K (40 for the first 15 games, then 20) and streak-based doubling opponent selection capped at 4 grid notches. Motivated by observing slow calibration on the first real batch — a true ~300 ELO agent was taking 11+ losses to reach the bottom of the chess.com pool. The Elo update formula is unchanged.
