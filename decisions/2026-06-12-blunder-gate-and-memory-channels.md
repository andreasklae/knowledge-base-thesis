---
type: decision
status: accepted
---

# 2026-06-12 — Commit-time blunder gate; goal channel; reference dismissal

Three changes motivated by the 2026-06-12 mating-puzzle sessions, where the
agent lost won basic-mate positions in identical ways. Amends the memory
model of [[2026-06-10-structured-turn-memory]] (and the blocklist follow-up
committed as `43c777e`) and extends the mechanics-tool surface under the
[[2026-06-02-tool-fairness-rulebook]].

## Context

Session evidence (games in `backend/games/mating-patterns-and-strategy/`):

- **Every lost exercise ended in a free capture by the bare king.** K+R
  game `62427a9b`: 54 plies of drill, then 27.Kd6?? abandoning the rook to
  Kxb7. K+Q game `ba6cd737`: 3.Qd4+?? Kxd4. Ladder games `00db2be3` /
  `531c1ff6`: rooks left adjacent to the king and taken. In each case the
  agent committed the losing move *without imagining it first* —
  `chess__imagine_move` reports exactly this geometry, but verification was
  skippable and got skipped.
- **A legal winning move bounced for verbosity.** Game `bf129584`: the
  `/agent-commit` schema caps `reasoning` at 4000 chars and rejected a
  commit, costing the turn.
- **A dead game burned the whole retry budget.** Game `291e7938`: after the
  backend closed the game, all chess tools returned 404/"Game not found"
  for ten consecutive harness attempts before `agent_resigned_no_move`.
- **Tunnel failures cascaded.** Games 037–039 each recorded a bogus 0-1
  within 30 seconds of the eX3 tunnel dropping mid-game 036, because
  `run_puzzles.py` marched on.

## Decision

1. **Commit-time mechanical safety gate** (`make_move.py::_blunder_gate`).
   Before POSTing, the script replays the move on the live board and
   refuses to commit — once, with an explanatory error — when the move:
   (a) allows an opponent reply capturing a piece of minor value or better
   with **zero** defenders of the target square (a free capture); (b)
   delivers stalemate; or (c) instantly draws by threefold repetition or
   the 50-move rule while the mover leads on raw material count. The agent
   overrides with `confirm=true` (a genuine sacrifice costs one extra
   call). *Fairness argument:* the gate computes legal replies, defender
   counts, and the draw rules — the same one-ply geometry
   `chess__imagine_move` already reports, moved to the boundary where it
   cannot be skipped. It evaluates nothing strategic and never chooses a
   move; agency stays with the agent via the override. This is the
   mechanics-tool clause of the rulebook, not engine assistance.
2. **Short-term `goal` channel.** `make_move` gains optional `goal`
   alongside `plan`: the plan is the long-term intention ("trade down,
   then drill-mate"), the goal is what the next 1–3 moves must achieve
   ("drive the king from e6 to the 8th rank"). Same persistence and
   clearing rules as `plan`; both render in every turn prompt. Rationale:
   anti-shuffling — a concrete, checkable objective each turn gives the
   model something to advance instead of re-deriving intent.
3. **Reference dismissal.** `make_move` gains optional
   `dismiss_references="<path>[,…]"|"all"`. Wiki pages stay in context
   indefinitely by default (they are the agent's theory), but when the
   strategy changes the agent can drop pages read for the old strategy;
   the pruning processor collapses their `read_reference` results from the
   next model request on. Pages remain re-readable.
4. **Hardening.** `make_move.py` truncates `reasoning` at 3900 chars
   instead of letting the endpoint reject the commit. `AgentPlayer` aborts
   the turn with `PlayerError("game_vanished…")` on any chess-tool 404
   instead of retrying. `run_puzzles.py` stops the suite on
   infrastructure-shaped aborts (it already ran puzzles strictly one at a
   time — each game blocks until finished).
5. **Thinking retention raised.** The pruning processor keeps the head of
   old thinking text to 600 chars (was 400) — the conclusion usually lives
   in the head; perception dumps stay fully pruned.

## Consequences

- The free-capture blunder class that decided every lost exercise now
  requires an explicit, logged override to play.
- `confirm=true` appearing in a transcript is a signal: either a real
  sacrifice or the model fighting the gate — both worth reading.
- The gate adds one state-fetch per commit and is best-effort: if the
  fetch or parse fails it falls through to the endpoint, which remains the
  authoritative validator.
- Phase-1 baseline note: these are Config-2 infrastructure changes on a
  branch; ranked ELO is unaffected until merged per
  [[2026-05-24-ranked-vs-experimental]].
