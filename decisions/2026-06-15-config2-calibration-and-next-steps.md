---
type: decision
status: accepted
---

# 2026-06-15 — Close the Config-2 mate/blunder cycle; calibrate; next steps

Records the decision to conclude the current improvement cycle on the
`mating-patterns-and-strategy` branch, merge it to `main` as the Config-2
unit, run the official ranked calibration, and defer the next class of
improvement (middlegame trade evaluation and opponent-plan reading) to a
following cycle. Builds on [[2026-06-12-blunder-gate-and-memory-channels]]
and [[2026-06-13-drill-state-in-prompt]]; the fairness boundary throughout
is [[2026-06-02-tool-fairness-rulebook]].

## Context

This branch's work targeted the agent's self-inflicted failures and basic
mate technique. By 2026-06-15 the evidence (puzzle suite + chesscom/Maia
smoke games) shows that layer is substantially fixed:

- **Eliminated failure classes:** illegal-move retry loops; free-piece
  hangs (commit-time blunder gate, with a hard/unconfirmable tier);
  dead-game 404 cascades; cap-ended "immortal ghost" games; the cross-game
  `CHESS_GAME_ID` race; and the ritual per-turn `use_skill` call.
- **Mate technique is no longer the weak link.** The agent wins and mates
  an 850 chess.com bot with a clean pattern; back-rank mate-in-1 is solved
  instantly. The ladder still does not reliably *convert* (it executes the
  method partway then mis-finishes), but that is a model-composition limit,
  not a tooling gap — and basic mating is no longer what loses games.
- **Perception tools were hardened to report VALUE, not just count.** Both
  1000-rated losses were decided by a "defended-square bad trade" — a piece
  moved to a square defended by count but losing material by value
  (16.Ne5?? fxe5 dxe5; 9.Nd2?? bxc3 bxc3). `imagine_move` now runs a
  single-square static-exchange evaluation and warns ("⚠ Losing exchange on
  <sq>"; "lose ~N pawns" in Newly-hanging). This stays on the fair side of
  the rulebook — it is perception reporting, the same category as the
  material-balance line; the gate was deliberately NOT given SEE veto power.

## Decision

1. **Conclude this cycle and calibrate.** Merge
   `mating-patterns-and-strategy` to `main` as the Config-2 configuration
   unit, then run the official ranked batch (clean `main` → `ranked.csv`,
   ELO updates) to measure Config-2 strength against the Config-1 baseline
   (~794 ELO over 53 ranked games). This comparison is the cycle's headline
   result.
2. **Do not chase the next weakness before measuring.** The remaining
   failures are a different class and would make calibration a moving
   target.

## Next steps (next improvement cycle — explicitly deferred)

The agent's weak link is now **middlegame judgment**, not blunders or mate
technique:

- **Trade evaluation.** The new SEE warning catches single-square losing
  exchanges, but the model must still *act* on it (it has historically
  ignored count-based warnings — see [[chess-perception-action-gap]]).
  Open question for the next cycle: does surfacing exchange *value* change
  behaviour, or is value-weighted trade decision a model-capability ceiling?
- **Tactical awareness — forks (both directions).** The agent misses
  forks: it walked into an opponent fork, and separately failed to play a
  knight fork that would have won the enemy queen with check. The current
  perception tools report attacker/defender geometry on individual squares
  but never flag a *single piece attacking two valuable targets at once*.
  Candidate fair improvement (perception-level, per the rulebook): a
  fork/double-attack detector in `imagine_move` / the radar — "this knight
  on e6 would attack both the king and the queen" — for the agent's own
  candidate moves and as a threat-scan of the opponent's replies. Geometry
  only; the agent still chooses.
- **Reading the opponent's plan.** The agent does not anticipate the
  opponent's threats/plans well — e.g. allowing a passed pawn to promote
  (smoke game 1b3e94c0: g3-g2-g1=Q conceded a queen). Candidate fair
  improvements: a "what does the opponent threaten" prompt discipline using
  the existing `imagine_move(move="pass")` primitive; radar emphasis on
  enemy passed pawns and immediate threats. All must stay perception-level
  per the rulebook.

- **Quiet-move / positional guidance (when nothing is forcing).** This is
  the agent's biggest behavioural gap and the largest single next-cycle
  item. When there is no capture, check, or immediate threat, the agent has
  no sense of *what to improve*, so it drifts and shuffles (this is also
  what kills the basic-mate conversions and the long middlegames). A human
  consults a standing checklist of positional considerations. We want the
  radar (mechanical, geometry-only, fair) to surface these **only when the
  position is quiet** — i.e. suppressed whenever a tactic/threat is live, so
  it is signal not noise — AND the same content must exist in the wiki as
  general theory the agent can read (`strategic-thinking/`, `principles/`),
  so the tool is a pointer into the agent's own corpus, not an oracle.

  Candidate checklist items (each is pure board geometry / counting):
  - **Development:** undeveloped minor pieces still on the back rank;
    "you have not castled and the king is still in the centre"; rooks not
    connected / not on open or half-open files.
  - **King safety:** open files or diagonals pointing at your king; missing
    pawn shield; no luft (already have the defensive back-rank check —
    generalise it).
  - **Pawn-structure weaknesses:** doubled pawns, isolated ("lone") pawns,
    backward pawns, pawn islands, holes/outposts (squares no pawn can ever
    defend) for both sides.
  - **Loose pieces and latent tactics:** undefended ("loose") pieces of
    either side (the "loose pieces drop off" heuristic); a square from which
    a knight would fork two valuable pieces — e.g. "a black knight reaching
    c2 forks your king and rook, and c2 is not covered" (ties into the fork
    detector above, applied as a *standing* warning, not just on a candidate
    move).
  - **Piece activity:** a piece with very low mobility ("bad bishop" blocked
    by its own pawns, a knight on the rim), or an enemy piece dominating an
    outpost in your camp.
  - **Space and files:** who controls the open file; space-count by half.

  Design constraints: gate hard on "position is quiet" so these never fire
  over a real tactic; keep each line short and prioritised (a wall of
  positional text every quiet turn would drown the agent); and pair every
  radar line with the wiki page that teaches the concept, since the corpus
  *is* the Config-2 contribution. Each wiki page follows the existing page
  contract (When to use / The idea / What to do / Watch out for) and every
  concrete claim stays machine-verified by the wiki validator.

## Consequences

- Merging locks this configuration as a measured Config-2 version; future
  changes are a new cycle / new PR.
- The SEE exchange warning ships unvalidated in a *finished* game (only
  unit-tested + spot-checked on the two blunder positions). Acceptable: it
  is additive perception with tests, and the calibration itself is its
  field test.
- ELO baseline semantics unchanged ([[2026-05-25-initial-elo-1200]]).
