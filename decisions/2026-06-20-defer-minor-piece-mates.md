---
type: decision
status: accepted
---

# 2026-06-20 — Defer the K+2B and K+B+N basic mates as out of scope for the current model

## Context

The chess Phase-1 basic-mate curriculum ([[experiment-chess]]) was extended on
2026-06-20 to cover *every* forced-mate material configuration against a lone
king. Each combination was tested by dropping the agent (Gemma 4 31B-it,
internal Elo ~700–800) into tablebase-verified positions against Maia-1100 and
checking whether it converts to mate. See [[diary/experiment-chess/2026-06-20]]
for the full run.

Results split cleanly by material:

- **Converts** (a fair deterministic geometric potential carries the weak
  model): K+Q, K+R, K+2R, every combination containing a queen or rook, and the
  *over-material* minor combinations K+2B+2N (35 plies) and K+B+2N (65 plies).
- **Does not convert**: the two *minimal* minor-piece mates **K+2B** (drew at
  the move cap — the agent spammed aimless bishop checks and never built the
  two-bishop barrier) and **K+B+N** (the hardest basic mate; Delétang's
  triangles / the W-manoeuvre, ~33 moves with perfect play).

Two facts make this a boundary rather than a fixable gap:

1. **No simple fair tool solves them.** The K+R/K+Q advisor works because the
   confinement *box* is a true potential function — every good move strictly
   reduces it and reducing it leads to mate. For K+2B and K+B+N no analogous
   simple potential exists: region-size-, corner-distance-, and
   king-march-dominant weightings were all tested with depth-4 alpha-beta
   search against optimal defense and **none mate** — they shrink the king's
   space but cannot find the precise cornering coordination.
2. **A full solver would break tool-fairness.** A tool that computed the exact
   Delétang/W-manoeuvre move is "a chess engine with the interface filed off,"
   forbidden during play by [[2026-06-02-tool-fairness-rulebook]]. The fair
   ceiling is a sub-goal advisor that reports facts (region size, target
   corner) and a visualization the agent reads — which is in place and was not
   enough.

These mates are also **unrealistic for the rating under test**: K+2B and K+B+N
almost never arise in real games and are hard even for ~1800-rated humans;
forcing the bare 31B to execute them measures something the experiment does not
care about.

## Decision

**Stop investing in making the agent convert K+2B and K+B+N.** Keep the two
principle pages (`mates/king-two-bishops-mate.md`,
`mates/king-bishop-knight-mate.md`), the net/region visualization in
`show_position`, the region-based advisor, and the `chess__imagine_line` tool —
they are correct, fair curriculum and help the over-material cases — but treat
the non-conversion of the two minimal minor mates as a **result**, not a defect
to engineer away. The basic-mate curriculum is considered **complete**.

## Consequences

- **The curriculum boundary is now defined**: all major-piece mates and all
  over-material minor combinations (≥3 minors, or any with a major) convert via
  fair infrastructure; the two minimal minor mates are the documented edge.
- **Sharper deterministic-tools picture** ([[deterministic-tools-hypothesis]]):
  a fair *mechanics* tool (a geometric potential) substitutes for model skill
  up to a complexity threshold; past it — exactly the two minimal minor mates —
  only a full engine (Config 3) or genuine model capability suffices. K+B+N is
  the cleanest single example of where "infrastructure around a fixed model"
  stops being able to stand in for capability.
- **Tooling kept** is reusable for the realistic-conversion work that follows
  (`king_free_region`, `imagine_line`, the fair ply-cap, the repetition-aware
  advisor gate).
- **Next**: realistic late-middlegame / early-endgame conversion testing —
  positions where white leads on material and must convert against Maia-1100 —
  began 2026-06-20. That is the rating-appropriate version of "can it finish a
  won game."

Revisit only if the model under test changes materially (a stronger base model
might warrant re-testing K+2B), at which point this decision is superseded
rather than amended.
