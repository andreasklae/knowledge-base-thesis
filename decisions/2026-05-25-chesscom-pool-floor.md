---
type: decision
status: accepted
supersedes:
---

# 2026-05-25 — Raise the chess.com opponent-pool floor to 700; archive prior ranked games

## Context

The first four ranked games under the 1200-initial-ELO + Gemma 4 31B-it configuration produced three losses (vs chess.com 1200, 1100, 1000) and one aborted game (vs chess.com 550, separately fixed in `2026-05-25` make_move.py commit-on-call work). Streak-based stepping moved the matchmaker rapidly toward the bottom of the chess.com pool. The aborted game and informal observation surfaced a property of the pool itself: chess.com Engine bots at the lowest slider positions (250, 400, 550) play moves so erratic that neither side reliably converts the game to a result within the 150-half-move cap. Games at that level converge on time-cap draws regardless of the agent's true skill.

This is a property of the **opponent pool**, not of the rating system. The Elo update formula, K-factor adaptation, streak-based opponent stepping, and initial ELO are unchanged. The pool is curated.

## Decision

### 1. Raise the chess.com pool floor from 250 to 700

`CHESSCOM_ELOS` in `experiments/chess/backend/app/schemas.py` and `experiments/chess/backend/app/elo.py` is trimmed:

- **Before:** 25 ratings, 250–3200, slider positions 1–25.
- **After:** 22 ratings, 700–3200, slider positions 4–25. The three lowest bots (250, 400, 550) are removed from the experiment's pool.

The `chesscom_driver` package's `mapping.py` is **unchanged** — it describes the chess.com slider as it physically exists, not which positions our experiment uses. Removing slider positions 1–3 from `CHESSCOM_ELOS` makes them unselectable through the lobby UI (the dropdown reads `allowed_elos` from `GET /api/player-types`) and through batch creation, while leaving the driver capable of driving them if some future experiment configuration wants them back.

### 2. Initial ELO unchanged at 1200

The supporting evidence (3 losses) is not yet strong enough to revise the initial ELO. The lowest opponent the agent has played under the new configuration that we have any meaningful data on is chess.com 1000, where the agent lost. We do not yet have a single ranked game at the new pool floor (700) or even at 850 — the previous batch never reached either because the matchmaker jumped past them to 550. Initial ELO 1200 remains as in [[2026-05-25-initial-elo-1200]].

If subsequent batches show another rapid downward walk that stalls inside the new floor (700–1000), a follow-up ADR can revisit the initial ELO with that evidence in hand. Today's evidence is about the pool, not the prior.

### 3. Full reset of ranked-state files

`games/ranked.csv` and `games/agent_elo.json` are reset to their initial state:

- The four pre-revision rows from `ranked.csv` are appended to `games/experimental.csv` with their original content intact. They remain auditable as research record — they are the data that motivated this revision — but they no longer participate in the ranked ELO trajectory.
- `ranked.csv` is truncated to its header line.
- `agent_elo.json` is deleted (next batch starts with the default `AgentEloState`: ELO 1200, games_played 0, streak 0).
- Per-game JSON artefacts (`<game_id>.json`, `<game_id>_agent.json`) and the prior `batches/<batch_id>.json` are kept on disk and tracked in git. They are referenced by the experimental rows; deleting them would orphan those rows.

### 4. No methodology change to the rating system

Unchanged: classical Elo update, adaptive K (40 provisional / 20 stable, switch at 15 games), streak-based exponential opponent stepping capped at 4 grid notches, anchor-then-step opponent selection, pool-per-batch, sampling temperature, per-turn fresh context. All ADRs from 2026-05-20 through 2026-05-25 prior to this one stand.

## Consequences

- The matchmaker now cannot select chess.com 250, 400, or 550 as an opponent. The lowest reachable rating in a chess.com batch is 700. From the agent's current state (post-reset: ELO 1200, streak 0), a 4-loss streak would walk anchor 1200 (idx 8 in the new pool) → 1100 (idx 7) → 850 (idx 5, since 1100 - step 2 = idx 5) → … in practice converging into the 700–1100 band rather than the unplayable 250–550 band. Calibration of an agent whose true ELO is in the 400–700 range will compress against the new floor and show as a streak that doesn't recover — exactly the signal we want, in contrast to the silent draw-cap stalls under the old pool.
- The four archived rows in `experimental.csv` remain queryable. They carry their original `phase=ranked` value as a forensic marker; if downstream analysis assumes `phase=ranked` rows live only in `ranked.csv`, that assumption is broken for these four rows. Documented here rather than rewritten.
- The reset means we lose the three legitimate ranked losses against chess.com 1200/1100/1000. This is a real cost. The rationale for taking it: mixing pre- and post-revision games produces a kinked ELO trajectory that's harder to defend in the thesis than a clean restart. The three losses are preserved as `experimental.csv` rows, so they remain research record.
- No source of truth shifts. `app/elo.py:CHESSCOM_ELOS` and `app/schemas.py:CHESSCOM_ELOS` are duplicated by design (the schema module avoids importing from `elo.py`); both are updated together.

## Open items

- A follow-up review after the next chess.com batch completes — if the agent's ELO again stalls at the new floor with continuing losses, the supporting evidence will support an initial-ELO revision and we revisit §2 then.
