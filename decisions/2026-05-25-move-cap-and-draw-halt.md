---
type: decision
status: accepted
---

# Move cap (150 half-moves) and consecutive-draw batch halt (3 draws)

## Context

First calibration batch revealed two failure modes:

1. **Infinite endgames.** The agent repeatedly reached queen + king vs
   lone king positions but could not deliver checkmate. python-chess's
   75-move rule (mandatory termination at 150 half-moves for chesscom
   games, which disable 3-fold/50-move claim draws) is the only existing
   safeguard. One game ran 274 half-moves before aborting on a chess.com
   browser sync error rather than a natural termination.

2. **Draw cascades.** Repeated move-cap draws at the same rating level
   indicate the agent is stuck — it wins materially but cannot convert.
   Continuing the batch wastes games and distorts the streak-based
   opponent-selection logic (draws halve the streak, so the agent stays
   at the same rating indefinitely).

## Decision

**Move cap:** `Game.max_half_moves = 150`. When `len(uci_moves) >= 150`
and the position is not already over by chess rules, `Game.is_over()`
returns `True` and `Game.result()` returns `"1/2-1/2"`. This is recorded
as a draw for ELO purposes. 150 half-moves (75 full moves) is generous
enough to cover any normal decisive game and tight enough to cut off
conversion failures quickly.

**Consecutive-draw halt:** `MAX_CONSECUTIVE_DRAWS = 3` in
`batch_runner.py`. After 3 consecutive drawn games the batch transitions
to `status="stopped"` with an explanatory `last_error` message. The user
must inspect and decide whether to adjust the rating floor, the move cap,
or the agent's conversion strategy before restarting.

## Consequences

- Move-cap draws count as draws for ELO (score 0.5 for both sides), which
  is correct: the agent failed to convert a won position, so a draw is a
  fair outcome.
- The draw halt surfaces conversion failures early instead of letting a
  batch silently produce a run of misleading draws.
- Both thresholds (150 half-moves, 3 draws) are configurable constants
  (`Game.max_half_moves`, `MAX_CONSECUTIVE_DRAWS`) and can be changed
  without a new ADR as long as the rationale here is updated.
