---
type: decision
status: accepted
---

# 2026-05-25 — Perception tools (`show_position`, `imagine_move`, `evaluate_position`) and skill/system-prompt rewrite

## Context

Baseline calibration is complete ([[2026-05-25-baseline-calibration-complete]]):
the bare-model Gemma 4 31B-it agent plays at or below the chess.com pool
floor of 700, with a recorded trajectory of ELO 1200 → 684.2 over 26
ranked games. The agent had only two skill scripts available
(`list_legal_moves.py` and `make_move.py`) and a system-prompt-enforced
four-step turn sequence.

The agent's failure modes in those baseline games were almost entirely
*perceptual* rather than strategic:

- It misread which pieces were attacking or defending a square.
- It missed pins. It treated pinned pieces as available defenders or
  active attackers.
- It hung pieces by moving defenders away without noticing.
- It walked into one-ply tactics — captures that lost material to a
  recapture sequence it had failed to count.
- It made illegal-move attempts on positions it had geometrically
  misread (see [[diary/experiment-chess/2026-05-25]] for the Gemma
  toolcall failure, where the model reasoned correctly in text about
  falling back to a legal move but called the original illegal move
  twice anyway).

These are *the kinds of mistakes that deterministic tools fix
cheaply*. The tool-fairness rulebook in [[experiment-chess]] explicitly
permits mechanics tools that "read the board without encoding chess
knowledge" — `legal_moves()`, `what_if(move) -> board_after`,
`is_attacked(square)`, pattern detection. The bare-model baseline
deliberately ran without any such tools so we had a clean reading on
the raw model's chess competence. With baseline established, the next
configuration to measure adds the perception tools the rulebook
already permits.

## Decision

### 1. Three new scripts added to the `chess-player` skill

All three are pure-Python utilities built on `python-chess`. They read
the live game state from the backend (via `CHESS_API_BASE` and
`CHESS_GAME_ID` env vars, same pattern as `list_legal_moves.py`) and
return plain text intended for the model to read. None of them mutate
the live board; only `make_move.py` commits.

**`show_position.py`** — Returns:

- A phase annotation (early/late opening / middlegame / endgame) using
  a weighted non-pawn material count (queen 4, rook 2, minor 1; max 24)
  with move-number and queens-on-board tiebreakers.
- A labelled ASCII board (uppercase white, lowercase black, files a–h,
  ranks 8–1, white at the bottom).
- The FEN and side to move.
- "Your pieces under attack" — for each of your pieces with at least
  one opponent attacker, who attacks and who defends. Attacker and
  defender chains expand x-ray batteries (a slider behind an immediate
  attacker on the same line is listed as `(then ... via x-ray)`).
  Pinned pieces are annotated `(pinned)`.
- "Opponent pieces you are attacking" — same, from the other side.

The script does not score exchanges. It surfaces geometry; the agent
counts material itself.

**`imagine_move.py --uci <move>`** — One-ply look-ahead. Plays the
move on a copy of the board and reports the resulting position plus a
tactical report: `Move:` line (with capture/castle/en-passant/promotion
detail and centipawn delta for captures), `Check:` status (none / check
/ checkmate / stalemate), `Discovered attacks:` (own pieces that gain
new attacks because the moved piece cleared a line), `Moved piece
status` (attacker/defender chains for the new square plus what it
now attacks/defends), `No longer attacking / defending` (deltas from
the old square — this is where "you moved a defender away" surfaces),
`Newly hanging own pieces` (pieces that became unsafe as a side-effect
of this move), `En passant available:` (when the move grants the
opponent an en-passant), and `Opponent legal moves:` (count + first 12).

Illegal `--uci` exits nonzero with a categorised error.

**`evaluate_position.py [--moves uci1,uci2,...]`** — Static position
score in centipawns from white's perspective. Uses Tomasz Michniewski's
Simplified Evaluation Function: piece values (P=100, N=320, B=330,
R=500, Q=900; king material excluded from totals) plus piece-square
tables, with per-side king-table selection by Michniewski's canonical
rule (endgame table iff that side has no queen, or has only queen +
king). Material + PST only — no mobility, pawn-structure, or
king-safety terms. Output includes verdict bands (`equal`,
`roughly equal`, `slightly better`, `clearly better`, `winning`).

With `--moves` the script plays the comma-separated UCI list on a copy
of the board and evaluates the resulting position, prepending `Line:`
(SAN) and `After:` (UCI) headers. Illegal moves in the line abort with
a categorised error naming which move index failed and why.

### 2. SKILL.md rewritten

Two structural changes:

- **Leads with the turn workflow**, not per-script contracts. The
  model's first need on a turn is "what do I do?", not "what's the
  FEN field in show_position's output?". The workflow now sits at
  the top with five numbered steps (see → candidates → imagine →
  optional eval → commit) and an explicit framing of when to skip
  steps versus when to be thorough.
- **Explicit "Trust your tools over your intuition" section.** The
  model's chess intuition is unreliable; the deterministic tools are
  not. When they disagree, the tool wins on facts. Intuition still
  has a role — proposing candidates, weighing strategic ideas the
  tools cannot evaluate — but the division of labour is **intuition
  proposes, tools verify**. This framing was added at the user's
  request and is, in retrospect, the single most important paragraph
  on the page for an LLM with weak procedural chess knowledge.

Per-script contracts moved below the workflow as a reference section,
one subsection per script.

### 3. System prompt trimmed

The previous system prompt embedded the turn flow as a four-step
prescribed sequence ("1. use_skill, 2. list_legal_moves, 3. write
2–4 sentences of reasoning, 4. call make_move") and a hard cap on
reasoning length. Both moved out of the system prompt entirely.

The new system prompt contains only:

- Role (white in a live game).
- A pointer to call `use_skill` at the start of each turn to load
  the skill.
- `make_move.py` commit semantics and retry-on-illegal.
- An anti-loop instruction: "Take the time you need to think, but
  avoid loops. If you find yourself calling the same tool repeatedly
  on the same position, or oscillating between candidates without
  converging, commit the move you currently believe is best rather
  than continuing to deliberate." Lenient phrasing — encourages care
  but explicitly forbids infinite deliberation.
- Resignation-on-no-move rule.

This separation lets the SKILL.md evolve without touching the
system-level prompt, which the model treats as more authoritative.
The skill is the strategy layer; the system prompt is the rules
layer.

### 4. Per-turn limits adjusted

`max_tokens=1024` per response is **unchanged**. Each individual
response is reasoning text + at most one tool call; 1024 is plenty
for the model to react to one tool's output before calling the next.
The 1024 cap is also part of the original reason-before-move ADR's
intent ([[2026-05-24-reason-before-move]]) — bounding any single
response prevents the model from producing a monolithic analysis
block that mixes pre- and post-move reasoning.

`max_turns=10` raised to **`max_turns=16`** per run. The old budget
fit 3–4 tool calls per turn; the new flow fits 4–9 (use_skill +
show_position + 1–3 imagine_move calls + optional evaluate_position
+ make_move, with reasoning text between). 16 is comfortably above
a thorough turn, still bounds runaway loops, and leaves headroom
for one or two illegal-move retries inside a single run before the
harness-level retry kicks in.

## Consequences

- The agent now has perception tools that fix exactly the failure
  modes baseline calibration surfaced: misread attackers, missed
  pins, hung pieces, miscalculated one-ply tactics. Every one of
  those should now be detectable by `show_position` + `imagine_move`
  before commit.
- The chess-player skill grew from two scripts to five. The SKILL.md
  page grew from ~110 lines to ~210, still well under the
  skill-creator's 500-line guidance.
- The thesis's claim — that procedural skill accumulation around a
  fixed model produces measurable gains — gets its first real test
  with the next ranked batch. The ELO delta vs the 684.2 baseline
  is the headline measurement.
- The deterministic-tools hypothesis ([[deterministic-tools-hypothesis]])
  gets a within-Phase-1 reading: if these tools alone close most of
  the gap to the pool's midpoint, that is evidence that perception,
  not chess knowledge, was the dominant baseline limit.
- Methodology change: future batches use the new SKILL.md and the
  trimmed system prompt. The CSV's `branch` and `commit_sha` columns
  preserve forensic precision; the PR that merges this work is the
  conceptual unit of "configuration change" per
  [[2026-05-24-ranked-vs-experimental]].

## Tool-fairness audit

The rulebook in [[experiment-chess]] permits "mechanics tools" that
"read the board without encoding chess knowledge". Each new script
was checked against it:

- **`show_position`** — Renders geometry: legal attackers, defenders,
  x-rays, pins. No move recommendations. No exchange scoring. The
  rulebook explicitly lists `is_attacked(square)` and
  `list_pieces_attacking(square)` as fair; this is the same shape.
  **Fair.**
- **`imagine_move`** — `what_if(move) -> board_after` is the canonical
  example given in the rulebook as the fair form of calculation. The
  script extends that with derivations *from* the after-board (check
  status, discovered attacks, newly hanging pieces, opponent legal
  replies), all of which are geometric facts the agent could compute
  itself with repeated `what_if` calls. Pre-bundling those derivations
  is a UX improvement, not a knowledge addition. **Fair.**
- **`evaluate_position`** — This is the closest to the line. Material
  values are common knowledge (any chess source lists them); PSTs
  encode positional heuristics (knights belong in the centre, kings
  belong on the back rank in middlegame and centralised in endgame).
  Those are *chess knowledge*, not pure mechanics.
  
  Two reasons to permit it nonetheless:
  
  1. Michniewski's PSTs are a published, well-known set — the kind
     of common-knowledge baseline a beginner reads in their first
     week of study. The rulebook's "fair" examples include `piece_values`
     which is the same kind of common-knowledge tabulated constant;
     PSTs sit on the same footing.
  2. The script is bundled with the agent from the start of the
     experiment, before the learning loop has produced anything. It
     is not a retrieval over an agent-curated corpus — it is a
     baseline tool. The library work (Phase 1 proper) is what tests
     the agent-curated-corpus claim.
  
  **Fair, with the caveat documented here.** If a reader of the
  thesis pushes back on PSTs as "encoded chess knowledge", the
  honest answer is that they are — at the level of a beginner's
  primer. The eval is intentionally weak (no tactics, no mobility,
  no king safety) so it does not encode strong-play knowledge.

The broader fairness principle: these tools fix *perceptual* failure,
not *evaluative* failure. The agent still has to decide which moves
to consider, what they mean strategically, when to attack and when
to defend. The tools help it count what is actually on the board.
That division is consistent with what `experiment-chess.md` calls the
"mechanics tools" tier.

## Open items

- Run an experimental batch on the `visualization-and-context-management`
  branch to sanity-check the new flow before merging. Verify the
  model actually uses `show_position` and `imagine_move`, doesn't
  loop, and commits within `max_turns=16`.
- After merge, run the official ranked calibration batch on `main`
  to measure the ELO delta vs the 684.2 baseline.
- Context management is the planned next change on this branch
  (see [[diary/experiment-chess/2026-05-25-visualization-tools]]).
  Once that work lands it should get its own ADR rather than being
  bundled with this one — the measurements should be separable.
