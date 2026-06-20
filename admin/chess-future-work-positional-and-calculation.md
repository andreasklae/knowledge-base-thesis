# Chess agent — future-work backlog: positional knowledge, calculation, and recipes (2026-06-15)

Captured from the user's observations after the first PR2 ranked smoke
batch. **Nothing here has been implemented** — this is the design backlog
for the *next* improvement cycle. Do NOT touch the chess wiki or anything
affecting agent capabilities until this is scheduled work; this document
and the KB are the only things to edit now. Companion to the ADR
[[2026-06-15-config2-calibration-and-next-steps]], which holds the
already-recorded items (trade SEE, forks, opponent-plan, quiet-move
checklist). This doc goes deeper and adds the new themes.

> **Caveat on grounding:** the user asked for a deep analysis of "game 4 of
> the batch" (vs a 700, an easy win thrown away with blundered pieces and a
> pawn promoted into immediate capture). That batch was reverted at the
> user's request and the per-game JSON logs were deleted, so the move-level
> detail no longer exists. The *pattern* is recorded below from the user's
> description and the ranked.csv summary (PR2 games 063–068: a 1-0, two
> draws, and three losses incl. vs 700 and 850). Re-analysis requires
> re-running and KEEPING such a game before the next cycle.

---

## A. Principles / playing rules (wiki: `principles/`, `strategic-thinking/`)

A library of heuristics the agent should follow "unless there is a good
reason not to." Surfaced as quiet-move guidance and as wiki theory. The
deep-dive task: **research what is canonically considered good vs bad play**
(opening principles, middlegame strategy, endgame technique) and turn each
into a short, machine-checkable wiki page + a one-line radar trigger.

Opening / general conduct:
- Don't move the queen out early.
- Don't move the king before castling; castle early.
- Develop minor pieces before major pieces; don't move the same piece twice
  in the opening without reason.
- Don't double your own pawns without compensation; keep pawns connected
  ("pawns should go together").
- Control the centre.

Middlegame / strategic:
- Put rooks on open and half-open files; double rooks on a file.
- Put pressure on pinned pieces (they can't move — pile attackers on them).
- Knights want outposts; bishops want open diagonals; trade your bad piece.
- Create and exploit weaknesses in the opponent's structure.

Simplification / converting an advantage:
- **When up material, trade pieces (not pawns)** to simplify toward a won
  endgame.
- Prefer promoting a pawn over hunting a fancy mate; prefer an easy/simple
  mate over the fastest mate.
- Know when NOT to push for mate — when to take a draw or force stalemate-
  free simplification.

"My piece is attacked — the four responses" (a decision recipe):
1. defend it, 2. move it, 3. counter-check, 4. create a bigger threat.
Plus: **don't bother threatening a piece that can just step away without
cost** — only threats that actually win something or force a concession
count.

## B. Per-move pros/cons on `imagine_move`

Augment `imagine_move` so each candidate gets a short, structured
**pros / cons** read, in addition to the existing geometry. Example the
user gave:
> Pros: doubling the rooks, weakens the opponent's king.
> Cons: rook no longer defends the knight, blocks the dark-squared bishop.

Each pro/con must be a mechanical fact (a file opened, a defender dropped, a
diagonal blocked, a square weakened, a piece's mobility changed) — not an
engine verdict. This is the move-level mirror of the positional checklist.

## C. Strengths & weaknesses lists (both sides)

`show_position` / radar should list, for BOTH colours:
- **Weaknesses:** doubled/isolated/backward pawns, open king, loose pieces,
  fork squares (e.g. "K and Q/R can be forked by a knight landing on c2,
  which is unprotected"), bad pieces, holes.
- **Strengths:** passed pawns, centre control, material lead, rook on an
  open file, bishop pair, space, outposts.

Then — the harder part the user emphasised — **instruct/suggest how to ACT
on each**: a weakness in the opponent's camp is a target (attack the
backward pawn, occupy the hole); a strength of yours is something to press
(push the passed pawn, open a second front with the bishop pair). The wiki
pages carry the "how to use this feature" method; the radar names the
feature and points to the page.

## D. Calculation, look-ahead, and predicting opponent moves

The big capability gap. Needs:
- **Exchange calculation** beyond the single-square SEE already added —
  multi-square / multi-exchange sequences.
- **Visualising future positions** generally: a way to *scope* candidate
  continuations a few plies deep without exploding context.
- **A good way to predict the opponent's reply** so look-ahead is realistic
  (not just assuming the opponent cooperates). Today the only primitive is
  `imagine_move(move="pass")`.
- Open design question: how to give bounded, useful multi-ply look-ahead
  while staying inside the tool-fairness rulebook (mechanics/agent-driven
  calculation, NOT an engine search). This is the riskiest item for
  fairness — flag for explicit user ruling before building.

## E. New tool: list legal moves for a specific piece

Concrete, low-risk, high-value. When `show_position` says "your queen is in
danger," the agent should be able to call something like
`list_legal_moves(piece="queen")` or `list_legal_moves(square="d1")` to see
just that piece's escape/relocation options, instead of scanning the whole
legal-move table. Pure mechanics (legal-move enumeration filtered by piece).

**DONE (2026-06-16, partial): safe-squares-for-a-hanging-piece, folded into
`show_position`.** When a piece is attacked and losing material (SEE < 0), the
radar now lists that piece's *safe* legal destination squares (squares that
are not attacked by the enemy, or are defended) so the agent can relocate it
without re-hanging it. Motivated live: in a K+R drill the agent slid an
attacked rook H5→A5 (fine for a rank-fence, but it had no list of which
squares kept it safe). Pure mechanics; tool-fair.

**Still future work (the harder cases the safe-squares list does NOT yet
handle):**
- **Discovered attacks:** moving the hanging piece may open a line, so a
  "safe" destination can lose *other* material (or, conversely, a move may be
  good because it discovers an attack). The square-by-square safe list is
  blind to what moving the piece *uncovers*. Need to evaluate the resulting
  position's hanging-piece set, not just the moved piece's landing square.
- **Several pieces under attack at once:** when two or more of our pieces are
  attacked, a single piece's safe-square list is insufficient — we need to
  rank moves by *how much total material they save* (e.g. a move that defends
  or removes the attacker on the more valuable piece, or a fork-escape that
  saves both). This is a small search/priority problem: for each candidate,
  sum the material still hanging after it and minimise. Keep it
  agent-decides (report the saved/lost totals; do not pick the move).

## F. Mate knowledge in the MIDDLEGAME, not just endgames

The mate radar / triggers currently seem to fire mainly in thinned-out
endgame positions. The agent needs to recognise **mating threats with full
boards** — both delivering them and (critically) **defending against the
opponent's**. The user saw it blunder **mate-in-2 against it** at least
twice (one in a lost position, one not). Defensive mate-threat detection is
as important as offensive. The named-mate pages exist; the gap is the
*trigger* surfacing them mid-game and a "are I/they threatening mate next
move?" check.

## G. More recipes for specific scenarios

Beyond the basic mates, the user wants recipes for recurring concrete
situations, e.g.:
- **Pawn-promotion strategies** — the user saw the agent fail to walk two
  connected pawns up with the king escorting; it lost one pawn (then
  promoted the other faster, so not fatal, but it should know the
  technique). K+2P, K+P vs K (already have one), outside passed pawn, etc.
- Other endgame/middlegame "how to do X" recipes as they surface.

The architectural requirement the user stressed: **a RICH wiki but a SCOPED
context.** The agent needs good tools + instructions to NAVIGATE the wiki —
read the few critical pages, skip the irrelevant ones — so the corpus can
grow large without blowing the context budget or causing the agent to miss
the one page that matters. This is a retrieval/navigation problem on top of
the content problem.

## H. Tactical motifs to add

- **Pins** — how to pin a piece and then pile up to win it.
- **Skewers** — the reverse pin.
- **Forks** — already in the ADR; reiterate as part of a unified
  tactical-motif set.

## I. Narrate the opponent's last move ("what changed")

When the opponent moves, tell the agent **what that move did**, in
mechanical terms, e.g.:
> "Opponent played Bc2 — now attacking your queen and no longer defending
> its rook on a4."
> "You were in check; the check is now blocked by the knight on e5."

Then instruct the agent to **reflect on how this changes the position and
its plan**. Crucial framing the user insists on: the agent is bad at
visualising, so it must **reason over the information the tools give it,
not over what it imagines it 'sees'** on the board. The whole design
philosophy is: tools convert the board into explicit facts; the agent
reasons over the facts.

## J. The unsolved one: it still blunders despite warnings + the gate

The user flagged this with no clear fix: the agent **still sometimes
blunders pieces even though `imagine_move` warned and the commit gate is
on.** The gate catches free hangs (and now minor-for-pawn into undefended
squares) and refuses hard losses, but soft cases get `confirm`'d or the
move differs from what was imagined. Connects to
[[chess-perception-action-gap]] and [[chess-gemma-toolcall-behaviour]]. The
specific recurring sub-pattern the user named:
> It gains a lot of material points and **doesn't realise those points will
> be lost immediately** — e.g. promoting a pawn that is captured next move
> (the promotion shows +800 material, the recapture isn't weighed).

Candidate angle: the material-delta line and SEE should net the *opponent's
immediate forced recapture* into the number the model sees, so a promotion-
into-capture reads as ~0, not +800. But the deeper issue may be that the
model anchors on the headline gain and doesn't process the follow-up — a
capability limit, not purely a tooling one. Needs investigation, and is the
most important behavioural failure to crack.

**UPDATE 2026-06-15 — largely RESOLVED this session.** The commit gate was
extended to refuse ALL single-square losing trades via static-exchange
evaluation (SEE): defended-but-losing trades (the Ne5/Nxd6/Nxe5 class),
promotion-into-capture, side-effect hangs the move causes, and a soft
warning when committing with a rescuable already-hanging piece. Hard
(unconfirmable) for self-losing cases. Validated live (game d9a0fba2,
Gemma vs Maia-1100): the agent held material at -1 with ZERO piece blunders
through 24+ of its own moves (vs move-~16 losses in every prior game); the
gate fired 15x on real losing-trade attempts. So the blunder class is
eliminated within the fairness rules. What remains under J is only the
RESIDUAL capability question — whether the model would still find a way to
shed material the single-ply SEE can't see (multi-ply tactics) — which
folds into item D (calculation / look-ahead).

## K. Opening theory — the new bottleneck once blunders are gone

With blunders gated out (item J), the agent's losses shifted to a different
cause: it walks into a **pawn-down book line in the opening** and then loses
the long endgame on technique. Game d9a0fba2: a Ruy Lopez where
7.O-O Nxe4 8.d3 left it a clean pawn down to known theory — not a blunder
the gate can catch (no single-ply hanging piece), just bad opening play.
Root cause confirmed: **the `openings/` wiki folder is EMPTY** (only the
index, "none yet — the tutor seeds these by ingestion"). The agent has no
opening guidance at all, so it drifts into inferior/pawn-losing lines.

Next-cycle work: seed `openings/` with a small, high-value set of opening
pages (a sound repertoire for White as the agent plays White — e.g. handle
the Ruy Lopez/Italian/Scotch lines it actually reaches, with the key "don't
drop this pawn / recapture here" notes), following the page contract and
machine-verified lines. This is the most direct lever toward
1100-competitiveness now that the early-middlegame piece-hangs are fixed.
Pairs with the radar surfacing "you are still in the opening, develop /
castle / don't grab that pawn" (the development items under C). Tutor-side
ingestion task (the user supplies/points at opening sources); do NOT
auto-generate opening theory from the model's own memory — that violates
the learning-loop fairness contract.

---

## Cross-cutting research task

The user explicitly asked for a **deep dive into chess principles and
patterns** — what is canonically good vs bad — before building. Sources to
mine: the Capablanca book already in the corpus (`raw/`, "Chess
Fundamentals" — look for MORE material there beyond the basic mates already
extracted), plus standard strategy references. Output: the principle/recipe
wiki pages (A, G, H) with machine-verified examples, and the radar triggers
that point to them (B, C, F, I).

## What the 2026-06-15 session actually established (read this before re-prioritising)

Three empirical results from this session reshape the priorities above. They
are findings, not plans — but they change what the next cycle should attack
first.

### L. The blunder failure mode is MODEL-INVARIANT at this Elo (cross-model probe)

We ran the same "play Maia-1100" task across a wide capability range:
- **Haiku, no skill** (bare API, own knowledge): coherent opening, then
  middlegame collapse, mated ~move 19.
- **Haiku, with the full skill** (tools + wiki via standalone scripts):
  SAME — mated ~move 19, 2x the tokens, and it reported *never reading the
  wiki*.
- **Sonnet, with the skill**: SAME class — 6.Nxe5?? netted a piece for
  pawns in a Ruy Lopez, lost.
- **Gemma-31B + full scaffolding**: the original Ne5/Nxd6/Nd2 blunders.

**Implication for the model-upgrade question** (the user was weighing
Gemini 3.x Flash / Grok / a stronger model): a model upgrade will NOT fix
the piece-blundering — Sonnet does it too. The dominant loss mode at 1100
is the perception-to-action gap ([[chess-perception-action-gap]]), not raw
capability. This is a genuinely useful thesis result: it argues that the
*infrastructure* (a mechanical gate) is the lever, not the model — which is
exactly the framework's claim. It also means: if a model tier is added, add
it as a SECOND BASELINE (replication axis), not as a fix, and keep each tier
internally fixed across its PR ladder (the chess experiment's whole point is
gains from the *user* side around a fixed model).

### M. The SEE gate works and reframes "the gate" as a real contribution

The commit-time gate, extended to refuse all single-ply losing trades via
static-exchange evaluation (defended-but-losing trades, promotion-into-
capture, side-effect hangs; soft-overridable vs hard-unconfirmable), was
**validated live**: across two agent-vs-Maia-1100 games the agent held
material even / -1 for 12-24 of its own moves with ZERO piece blunders,
versus move-~16 piece-hang losses in every prior game. The gate fired ~15x
per game on real losing-trade attempts and the agent rerouted each time.
Because even Sonnet needs it (finding L), the gate is not a crutch for a
weak model — it is a **model-independent productivity layer**, which is the
cleanest possible instance of the framework's "infrastructure over
capability" claim. Worth writing up as such. (Fairness: pure single-ply
rules arithmetic, agent still chooses, settled by the user across three
passes — see [[chess-perception-action-gap]].)

### N. The residual losses are now MEASURED, not guessed — re-prioritise to these

With single-ply blunders gone, both validation games still lost, but to two
specific, higher-up-the-ladder causes:
1. **Opening pawn-drops in book lines** (game d9a0fba2: Ruy Lopez, dropped
   the e4 pawn to known theory). Root cause: the `openings/` wiki is EMPTY
   (item K). This is the single most direct lever toward 1100 now.
2. **Multi-ply tactics — specifically FORKS / capture-with-tempo** (game
   bf4e1dd7: ...Nd4 then Nxc2 winning a pawn AND hitting the a1 rook ->
   Nxa1, losing the exchange). The single-ply gate cannot see this by
   design; it is items D (calculation/look-ahead) and H (fork detection).
   A FORK/THREAT DETECTOR in the radar (defensive: "the enemy knight can
   land on c2 winning a pawn and attacking your rook") is the highest-value
   tactical add — pure geometry, perception-level, same fairness class as
   the SEE gate and the defensive back-rank warning. It is a real feature
   (false-positive tuning needed), prototyped but not built this session.

## Suggested sequencing (REVISED 2026-06-15 with the above evidence)

1. **Fork / capture-with-tempo threat detector** in the radar (defensive +
   offensive) — finding N.2 shows this is now the top tactical loss cause;
   same fair class as the shipped SEE gate. Tune for low noise.
2. **Seed `openings/` with a minimal White repertoire** (item K / finding
   N.1) — stops the opening pawn-drops; tutor-side ingestion, needs source
   material.
3. Low-risk isolated wins: **list-legal-moves-for-a-piece** (E),
   **opponent-move narration** (I), **per-move pros/cons** (B).
4. Content: **principles/strategy/recipe wiki** (A, G, H) + **strengths/
   weaknesses radar** (C, F) with scoped-context navigation tooling (G) —
   and crucially, address WHY the agent does not read the wiki even when it
   has it (finding L: Haiku ignored the wiki entirely). The retrieval-
   behaviour problem may matter more than adding more pages.
5. Hardest / needs fairness ruling: **multi-ply calculation & opponent
   prediction** (D). Note J (blunders-despite-gate) is now largely resolved
   by the SEE gate; what remains there folds into D.

**Meta-finding worth its own line in the thesis:** the agent under-uses the
wiki it is given (Haiku reported never reading it; Gemma read it rarely).
So "build a richer wiki" is necessary but NOT sufficient — the binding
constraint is getting the model to *retrieve and act on* the right page at
the right time (the scoped-navigation problem in G, and the act-on-tool-
output problem in [[chess-perception-action-gap]]). Inline radar text (which
the model always sees) outperformed read_reference (which it must choose to
call) — a concrete data point for the Knowledge chapter's retrieval-vs-
preload question.
