---
type: diary
touched_work: [experiment-chess]
touched_concepts: [skill-acquisition-loop, deterministic-tools-hypothesis]
status: open
---

# 2026-05-26 — Endgame fixes: hanging-rook warning + checkmate-seeking

## What we observed

Game on 2026-05-26 reached this position after white played Rxe7+ (e1e7):

```
FEN: 4k3/4R1p1/r2p4/8/5P2/8/PPPB2PP/7K b - - 0 25  (black to move)

8  . . . . k . . .
7  . . . . R . p .
6  r . . p . . . .
5  . . . . . . . .
4  . . . . . P . .
3  . . . . . . . .
2  P P P B . . P P
1  . . . . . . . K
   a b c d e f g h
```

The `imagine_move` output showed the rook on e7 was "attacked by: king on e8" and "defended by: (none)" — the classic hanging-piece situation — but the hanging warning was **not emitted**. This is why the model hung the rook without warning.

Two separate issues were identified:

## Bug 1: Hanging-piece warning suppressed on checking moves

### Root cause

`_moved_piece_hanging_warning` in `imagine_move.py` had an early-return when `board_after.is_check()` was True. The rationale was that the opponent must address the check first and may not be able to capture. This is correct for many positions (e.g. a discovered check where the checking piece is far from the king and no legal reply reaches it), but was too broad. In this case, Kxe7 is a legal reply — the king itself takes the checking rook — making the piece genuinely hanging.

### Fix

Instead of suppressing the warning whenever `is_check()`, the function now checks whether any legal reply actually captures the moved piece (`m.to_square == move.to_square`). If at least one legal reply captures it, the piece is hanging and the warning fires. If none can (e.g. the king is checked from a distance by a queen and has to run), the warning is suppressed as before.

This is strictly correct: the warning fires iff the opponent can actually take the piece on their next move.

### Verification

Tested with the exact FEN from the game. Output after fix:

```
⚠ rook on e7 is hanging — attacked by king on e8; defended by nothing. The opponent can capture it immediately.
```

And the opponent legal replies include `e8e7 | Kxe7 | king takes rook on e7`.

## Bug 2: Agent plays passive endgame moves, doesn't seek checkmate

### Observation

The agent plays better than the bare model but fails to convert won endgame positions. It maintains material advantage but doesn't look for checkmates and plays passive moves when it should be closing out.

### Root cause

SKILL.md had no instruction to look for checkmates. The turn workflow started with `show_position` and then candidate selection — no step told the agent to prioritize mating moves. The `list_legal_moves` table already flags moves with a `checkmate` tag in the Flag column, so the information is available, but the agent wasn't prompted to scan for it.

### Fix (minimal, prompt-only)

Two targeted additions to SKILL.md:

1. Added **step 0** to the turn workflow: "Always check for checkmate first." Instructs the agent to run `list_legal_moves` in endgame positions and scan the Flag column for `checkmate` — and to commit immediately if found. Also adds: "Do not skip this step in any position where you have a material advantage — the goal is to win, not just to maintain an edge."

2. Extended the "obviously good move" paragraph to mention that a `checkmate` flag is the ultimate obviously good move — commit immediately.

3. Updated the candidate-selection step (step 2) to explicitly mention checking/cornering moves as priority candidates.

### Rationale for minimal approach

The thesis question is about whether the skill changes behavior. A checkmate-dedicated branch is planned for later. For now, the minimal prompt change is appropriate: we're not teaching the agent new chess knowledge, we're fixing a workflow gap where it never checked whether a winning move was already on the table. The `list_legal_moves` infrastructure was already correct (checkmate flag was already computed and displayed); we just needed to tell the agent to look for it.

## Files changed (session 1)

- `backend/skills/chess-player/scripts/imagine_move.py` — `_moved_piece_hanging_warning`: replaced blanket `is_check()` skip with targeted check for whether any legal reply captures on the same square.
- `backend/skills/chess-player/SKILL.md` — added step 0 (checkmate scan), extended "obviously good move" bullet, added aggressive-candidate guidance to step 2.

---

## Session 2: King mobility feature (2026-05-26, later)

### Motivation

Even with checkmate scanning, the agent needs a way to see at a glance which moves corner the opponent king. The existing tools report whether a move gives check, but give no signal about how much a move restricts the king's escape routes. A move that cuts the king from 5 squares to 1 is far more forcing than one that gives check but leaves 4 escape squares.

### What was built

**`_eval.py` — `enemy_king_mobility(board)` helper**

Counts how many squares the enemy king can legally move to from a given board position. Implementation: flip the board's turn to the enemy's colour on a copy, then count their legal king moves. Uses `flipped.legal_moves` so pins, check, and blocked squares are all respected by python-chess's move generator.

**`_eval.py` — `annotate_move` extended**

Now returns two additional keys: `king_before` (enemy king legal squares before the move) and `king_after` (enemy king legal squares after). `king_after` is computed directly from `work.legal_moves` after pushing the move, since it's then the enemy's turn.

**`_eval.py` — `render_moves_table` extended**

Added a fifth column **King mvt** showing `before→after (±delta)`. E.g. `6→3 (−3)`. A negative delta means the move restricts the king; `0` after means check or stalemate. The column sorts alongside the existing UCI/SAN/Description/Flag columns, so the agent can scan it to find forcing and king-cornering moves.

Example output:
```
| UCI    | SAN    | Description                       | Flag     | King mvt   |
|--------|--------|-----------------------------------|----------|------------|
| a1a7   | Ra7    | rook to a7                        |          | 6→3 (−3)   |
| a1a8   | Ra8    | rook to a8                        | check    | 6→0 (−6)   |
| e5e6   | e6     | pawn to e6                        |          | 6→6 (0)    |
```

**`imagine_move.py` — "Enemy king mobility" line in main report**

After the Check line, a new line shows: `**Enemy king mobility:** 6 → 3 (−3 squares)`. This appears at the top of the report where the agent reads it immediately alongside the check status. A delta of −N means the move tightens the net; 0 after means the king has no legal moves (check or checkmate).

**SKILL.md — documentation updates**

- Step 2 (candidate selection): Explains the King mvt column in `list_legal_moves` and the Enemy king mobility line in `imagine_move`. Instructs the agent to hunt for forcing sequences by looking for progressively smaller mobility numbers.
- `imagine_move` script docs: Added bullet for enemy king mobility to the "what it reports" list.
- `list_legal_moves` script docs: Added bullet for the King mvt column.

### Verification

- `uv run pytest tests/ -q` → 120 passed, 2 pre-existing failures unchanged.
- The `test_annotate_move_quiet` test was updated to check for the new `king_before`/`king_after` keys rather than exact dict equality (the old assertion was a strict dict comparison that would fail when new keys are added).

### Suggested extensions (deferred)

The user asked for suggestions beyond the implemented features. Candidates for future sessions:

1. **King confinement indicator in `show_position`**: Show the enemy king's current mobility at the start of each turn report, so the agent builds an ongoing sense of how cornered the king is without needing to call `imagine_move` first.
2. **"Forcing reply" summary in `imagine_move`**: After showing opponent legal replies, flag whether the opponent has any check, capture of your highest-value piece, or king escape — summarised in one line. Tells the agent at a glance whether the position after the move is forcing or gives the opponent counterplay.
3. **Dedicated checkmate-seeking branch**: A separate SKILL.md configuration that instructs the agent to run `list_legal_moves`, filter by Flag=checkmate/check, and imagine all checking moves before committing. Useful as a standalone "closing" configuration. Not yet built — the step 0 prompt addition is the minimal intervention; a dedicated branch is a future experiment configuration.

## Files changed (session 2)

- `backend/skills/chess-player/scripts/_eval.py` — `enemy_king_mobility()` helper; `annotate_move` gains `king_before`/`king_after`; `render_moves_table` gains King mvt column.
- `backend/skills/chess-player/scripts/imagine_move.py` — imports `enemy_king_mobility`; `render_imagine` computes and renders enemy king mobility line.
- `backend/skills/chess-player/SKILL.md` — step 2 and script docs updated for king mobility info.
- `backend/tests/test_eval_helpers.py` — `test_annotate_move_quiet` updated to check new keys rather than exact dict equality.

---

## Session 3: First win — agent delivered checkmate in a dominating game

**This is a single-game observation, not a conclusion.** N=1; no claims about effect size, generalisation, or which intervention mattered most. Recording it because it's the first checkmate the agent has produced under this configuration, and the qualitative shape of the game is worth capturing while it's fresh.

### What happened

The agent played a dominating game and finished it with checkmate. The mating attack was actually carried through to mate rather than meandering into a draw or losing the won position — which is exactly the failure mode the morning's endgame work targeted.

### Tentative observations (single game)

- The step-0 checkmate-scanning instruction in SKILL.md plausibly carried the closing sequence. Before today the agent had a habit of playing passive king-safety moves in won endgames; this game it converted. Whether that's because of the new instruction or because of the king-mobility column drawing its attention to forcing moves — or both, or coincidence — is unknown from one game.
- The king-mobility information and the perception tools more broadly likely contributed earlier in the game (piece coordination, not hanging things). Again, not separable from a single game.
- The compound configuration (perception tools + step-0 mate scan + king mobility) is doing *something*. Whether each individual piece pulls weight is what future batches will need to show.

No conclusions yet. The right next step is a batch run to see whether this generalises, and ideally an ablation comparing with/without step-0 and with/without king-mobility — though ablations cost time and the experimental-vs-ranked distinction means we have to think about which configuration becomes the next "main".

### Bug observed: bishop sacrifice not flagged as hanging

In the early-to-middlegame the agent sacrificed a bishop (user thinks dark-squared, not certain) and `imagine_move` did not emit the hanging-piece warning. The game went on to be won anyway — possibly the sac was sound, possibly not — but the warning gap is a regression we need to characterise.

Investigation pending. Hypotheses to check:
1. The bishop had at least one defender (so `len(defenders) >= len(attackers)` short-circuit), but the defender was lower-value or pinned and the exchange was actually losing — current logic only counts pieces, not values.
2. The bishop's attackers chain involved x-rays and the immediate-attackers count was zero or matched defenders.
3. The bishop was the moved piece *and* the position after the move involved the opponent's king already being checked in some way that suppressed the warning.
4. The bishop wasn't the moved piece — it was a *side-effect* hanging, and `_newly_hanging_own_pieces` uses the same "count attackers vs defenders" heuristic which is value-blind.

The current `_moved_piece_hanging_warning` and `_newly_hanging_own_pieces` both compare attacker *count* to defender *count*. A bishop defended only by a queen against an attack by a pawn satisfies `defenders >= attackers` (both = 1) but the exchange loses material. Same for a rook defended only by a king when attacked by a knight backed by another piece via x-ray — counting alone misses the SEE-style evaluation.

To investigate: identify the game in `backend/games/`, find the turn where the bishop hung, read the agent JSON trace and the `imagine_move` output, and reproduce the position to confirm which hypothesis fires.

### Investigation findings

Game `ed2bfd9d43824d919feaf917fb37bebb` (1-0, mate in 34 by Rd5#). The bishop sacrifice was move 14: **Bxf6** (dark-squared bishop g5 takes knight f6, recaptured by gxf6).

Reproducing the position before move 14 (`r1b1kb1r/6pp/p2ppn2/5PB1/3Q4/2N5/PPP2PPP/R4RK1 w - - 1 14`) and running `imagine_move --uci g5f6` shows:

```
## Moved piece status (f6, bishop)
- attacked by: pawn on g7
- defended by: queen on d4
- now attacks: pawn on g7
- now defends: queen on d4
```

**No hanging warning fires.** Why: the bishop on f6 is "defended" by the queen on d4 (the queen sits on the b8–h2 diagonal — actually d4-f6 is a clear diagonal). So:

- `attackers = [g7 pawn]` → length 1
- `defenders = [d4 queen]` → length 1
- `len(defenders) >= len(attackers)` → suppressed

But the exchange is materially losing: if gxf6, white loses a bishop (330) and gains a knight (320, already counted in the +320cp move summary) — so the *net* of "knight captured then bishop lost" is `+320 − 330 = −10 cp`. Essentially an even trade. So the warning suppression is *almost* correct here: this wasn't a blunder, it was an equal trade that opened the black king. The agent's reasoning likely valued the king-attack continuation more than the 10 cp.

So **this particular bishop sac was not a hanging blunder** — the warning correctly didn't fire because it wasn't materially hanging. The user's intuition that "the bishop hung" was probably the visual of "white gave up a bishop voluntarily on g7's diagonal" without registering that black had to recapture with a pawn (low-value attacker) and that the queen was defending.

### But the underlying gap is real

The current hanging logic counts pieces, not values. There IS a class of position where this fails:

- **Bishop (330) defended by queen (900), attacked by pawn (100)** → `1 vs 1`, no warning, but the exchange loses 230 cp (we lose the bishop, recapture with the queen, opponent can't recapture cheaper but we've still net-lost queen-vs-pawn if there's a follow-up). Actually in pure 1-vs-1 with no further recapture, we lose bishop and recapture the pawn, ending material `-330+100 = -230`.
- **Knight (320) defended by queen (900), attacked by knight (320)** → `1 vs 1`, no warning. We get knight-for-knight (`-320+320 = 0`) but only if we choose to recapture; if we don't, we lose the knight. The warning would help highlight this as needing thought.

For move 14 (Bxf6 in this game), the bishop *captures* a knight first, so the math is `+320 (capture) -330 (loss) +100 (recapture pawn) = +90` if the recapture happens — actually advantageous! The simple count was right by accident.

A SEE (Static Exchange Evaluation) would handle this properly: walk the attacker/defender chains cheapest-first and tally signed material. python-chess doesn't have SEE built in, but it's implementable from the chains we already compute in `compute_attack_chain`.

### Recommendation (not implemented yet)

Add a SEE-lite to the hanging detection:
- Use the existing `attacker_chain` and `defender_chain` ordering (cheapest-first).
- Walk the exchange: opponent captures with cheapest attacker, we recapture with cheapest defender, alternate until one side has no more pieces in the chain.
- If the final net material is negative for the mover (worse than not allowing the capture at all), emit the warning.
- This subsumes the current count-based heuristic and correctly handles the bishop-defended-by-queen-attacked-by-pawn case.

This is a meaningful change to the tactical reporting layer and should be its own task. I won't implement it in this session — flagging for follow-up.

### Conclusion for this session

The move 14 bishop sacrifice was NOT a missed warning; it was an even-or-slightly-positive trade that the current logic correctly didn't flag. But the user's question surfaced a real latent gap in the hanging detection: it's value-blind for the count match case. That gap should be closed with SEE-lite before the next ranked configuration change.
