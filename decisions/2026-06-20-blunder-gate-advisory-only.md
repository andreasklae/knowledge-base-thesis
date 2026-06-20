---
type: decision
status: accepted
supersedes: 2026-06-12-blunder-gate-and-memory-channels
---

# 2026-06-20 — The blunder gate is advisory-only (no non-overridable "hard" class)

Amends the blunder-gate design of [[2026-06-12-blunder-gate-and-memory-channels]]
(and the "hard / unconfirmable" class added 2026-06-14): the commit-time safety
gate may **no longer refuse a legal move**. Every warning is overridable with
`confirm=true`.

## Context

The `_blunder_gate` (`backend/skills/chess/scripts/make_move.py`) checks a
candidate move one ply deep and warns when it hangs a piece, stalemates, draws
while ahead, or — for the most catastrophic cases — drops to insufficient
material / repeats against a bare king. Those catastrophic cases were marked
**hard**: `confirm=true` could *not* override them; the commit was refused
outright.

Two problems:

1. **It is unfair and contaminates the measurement.** A gate that *refuses* a
   legal move is the tool making the move decision, not the agent. The
   experiment measures the agent's own strength around a fixed model
   ([[agent-infrastructure-vs-capability]]); silently forbidding its worst moves
   inflates measured skill and muddies the capability-vs-infrastructure reading.
   Under [[tool-fairness]] a mechanics tool gives a clearer *view*, not a
   decision — "intuition proposes, tools verify," but the agent commits. The
   agent must be free to blunder; the tool's job is to advise, strongly.
2. **It can deadlock.** When the agent is in check and *every* legal move trips
   a hard rule, the gate refuses them all and the agent can never commit —
   it loops to exhaustion. Observed live in an agent-vs-chesscom-850 game
   (2026-06-20): Ke5 in check from Rg5 with Rb5 hanging, all five king moves
   dropping the rook into K+B-vs-K (a dead draw); every move was hard-refused,
   so the agent could not move at all. The true result there is a *draw*, not a
   forfeit — the gate turned a drawn position into a no-move.

## Decision

**The gate is advisory-only.** It still fires on the same mechanical conditions
(hang, stalemate, draw-while-ahead, drop-to-insufficient-material,
repeat-vs-bare-king), and the wording for the catastrophic cases stays **very
strong** ("this almost certainly loses/draws the game — only override if you are
certain"). But all warnings are now **soft**: the agent commits the move by
re-calling with `confirm=true`. No legal move is ever refused.

The severity distinction is kept only as *wording* (catastrophic vs ordinary),
not as a block.

## Consequences

- **No commit deadlock.** Any legal move is always committable, so an in-check
  position where every move is bad reaches its true result (draw / loss) instead
  of hanging the agent.
- **Fairer measurement.** Blunders the agent insists on (after the strong
  warning + an explicit `confirm`) are part of its measured strength. The gate
  prevents *accidental* one-ply throwaways via the warning, without overriding a
  deliberate choice.
- **Risk accepted.** The agent can now confirm its way into a lost/drawn
  position the hard gate used to prevent (e.g. the reflexive `confirm=true`
  Rb6+?? Kxb6 from game ab02f31d that motivated the hard class). This is the
  intended trade: agency over a guard-rail. The strong wording is the
  mitigation; the agent's propensity to override it is itself a result.
- **SKILL.md** updated to describe a single, overridable SAFETY CHECK (no
  "cannot override" class).
- Connects to [[deterministic-tools-hypothesis]]: the gate is a mechanics tool
  that *informs*; it must not become a decision-maker, or it leaks tool strength
  into the agent's measured score.
