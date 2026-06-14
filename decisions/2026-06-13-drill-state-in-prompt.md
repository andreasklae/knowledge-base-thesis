---
type: decision
status: accepted
---

# 2026-06-13 — Drill state in every turn prompt; claimable-draw semantics

Follow-up to [[2026-06-12-blunder-gate-and-memory-channels]], from the same
validation campaign (puzzle games `3a787edc`, `9d2e1e58`, `185afd0b`,
`acfb27a4`).

## Context

After the blunder gate, no exercise was lost by giving away material — but
ladder, K+R, K+Q, and K+P all still drew. The transcripts show a delivery
problem, not a knowledge problem: the drill-state advisor (the
geometry-matched "which rule applies now" line in `_radar.py`) only reached
the model inside `chess__show_position` output, and the model skipped that
call on roughly half its turns (8 of 15 in ladder game `3a787edc`),
freestyling checks instead. Separately, draw detection used
`is_repetition(3)`/`is_fifty_moves()` while the backend ends non-chesscom
games on `claim_draw=True` — strictly weaker, so the gate let through a
move that instantly drew game `185afd0b`.

## Decision

1. **The turn prompt carries the drill-state line.** `AgentPlayer.get_move`
   imports the skill's `_radar.py` and appends `_drill_state_lines` to the
   prompt, beside the FEN and legal-move list. *Fairness:* the prompt
   already delivers mechanical board facts (FEN, legal moves); the drill
   state is the same class — geometry matched against the agent's own wiki
   recipes — and identical in content to what `show_position` embeds. The
   change is delivery (cannot be skipped), not capability.
2. **All draw detection uses claimable-draw semantics**
   (`can_claim_threefold_repetition` / `can_claim_fifty_moves`) in the
   gate, `draw_flag`, and `imagine_move` warnings, matching how the
   backend actually ends games.
3. **Drill coverage extended** where the validation games failed: K+P
   single-pawn escort (king-in-front / opposition / never-7th-with-check),
   ladder anti-patterns (king touching a rook paralyses it even defended;
   rooks stacked on one file must split wings), slide-away rules name the
   exact line and far-side square, opposition checks name the exact
   rank/file. The free-capture gate nets the move's own capture (trades
   pass) and always trips when the loss leaves insufficient material to
   win (the last-pawn case).

## Consequences

- The agent sees the applicable drill rule every turn whether or not it
  runs perception tools; transcripts can now distinguish "didn't know the
  rule" from "saw the rule and deviated" — the latter is the remaining
  failure mode to measure.
- Backend restarts are required for `agent_player.py` changes; skill
  scripts stay hot-reloaded (fresh subprocess per call).
- Harness fixes from the same campaign, recorded in git only (not
  methodology): cap-ended games no longer report active forever
  (`MOVE_CAP` termination), and creating/loading a game cancels the prior
  bot loop before building the new agent (process-global `CHESS_GAME_ID`
  cross-commit race).
