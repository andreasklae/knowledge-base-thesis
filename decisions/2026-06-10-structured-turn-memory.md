---
type: decision
status: accepted
supersedes: 2026-05-26-agent-turn-memory
---

# 2026-06-10 — Structured turn memory: a standing plan that survives turns

Amends [[2026-05-26-agent-turn-memory]] (agent-authored reasoning note as
the sole cross-turn context) by splitting the memory into two channels with
different lifetimes, and fixes a latent system-prompt bug in the injection
mechanism. Part of the `mating-patterns-and-strategy` branch.

## Context

Under the single-note memory, every turn's note overwrote the previous one.
A multi-move intention (mate a cornered king, escort a passer to promotion —
5–15 moves of coordinated play) only survived if the agent happened to
restate it in every note. The batch data shows the cost: three of the five
games before this branch were 150-ply draws in trivially won positions
(Q+pawns v Q, R+2B v bare king, Q+P v R) — the agent re-derived a plan each
turn, drifted, and shuffled checks until the cap.

Separately, while reworking the injection, a probe against pydantic-ai 1.99
(FunctionModel capture) showed the existing HistoryProcessor **dropped the
system prompt from every turn after the first**: pydantic-ai attaches the
system prompt only to the first request of an empty history, and the
processor rebuilt history without a `SystemPromptPart`. Since 2026-05-26 the
model has played turns 2+ with no skill list and no harness instructions.

## Decision

1. **Two memory channels on `make_move`.** `reasoning` (required) remains
   the note about *this* move, shown back once and then replaced. New
   optional `plan` is the standing plan (goal + method, 1–2 sentences): it
   persists until the agent passes a new one (`plan="none"` clears), and is
   re-rendered every turn with its age ("set on move 12", plus a check-it-
   still-fits warning at ≥10 moves old).
2. **Retention policy (aggressive forgetting).** Kept across turns: standing
   plan, last note, previous turn's prompt. Forgotten: older notes, tool
   transcripts, failed attempts. Rationale: the FEN is the complete game
   state; a weak model handed a transcript hallucinates more, not less; the
   `show_position` radar covers repetition/draw history mechanically.
3. **Injection contract.** A history processor replaces the incoming
   history once per *attempt* (armed by `get_move` before each
   `run_stream`) with: `ModelRequest(system prompt + previous prompt)` →
   `ModelResponse(rendered note + plan)` → current request; within-attempt
   requests pass through so the live tool conversation survives. Replacing
   per attempt also makes retry attempts genuinely fresh — previously a
   turn's failed attempts accumulated in context.
4. **System prompt re-injected explicitly** in the synthetic request,
   fixing the bug above. Regression-tested with a FunctionModel probe
   (`test_turn_memory.py::TestSystemPromptRegression`).

## Consequences

- The plan is the one artefact only the agent can carry forward, and the
  skill now says so (SKILL.md "Your memory between turns", workflow step
  0b); `strategic-thinking/make-a-plan.md` teaches when to write/replace it.
- Games after this change run with a system prompt on every turn — a
  confound to remember when comparing ELO across the boundary: part of any
  improvement may come from the bug fix rather than the memory/wiki work.
  (Both land in the same PR, so the per-PR calibration unit is unaffected.)
- `context_summary` events now carry the standing plan alongside the note;
  game JSONs record it.
- The baseline "per-turn fresh context" invariant
  ([[2026-05-24-per-turn-fresh-context]]) is already superseded in practice
  by [[2026-05-26-agent-turn-memory]]; this record keeps its spirit — no
  unbounded accumulation — while making the *useful* part of the context
  durable.

## Alternatives considered

- **Rolling window of N notes.** Rejected for now: notes describe move-level
  intent that goes stale in two plies; the plan channel carries the durable
  part explicitly. Can revisit if games show the agent forgetting tactical
  context it wrote two turns ago.
- **Harness-side plan synthesis (LLM summariser).** Rejected for the same
  reasons as in [[2026-05-26-agent-turn-memory]] — extra call, indirect,
  summarises the wrong thing when attempts are rushed.
- **Putting memory in the user prompt instead of a synthetic exchange.**
  Functionally similar; the synthetic assistant message keeps the memory in
  the agent's own voice and leaves the user prompt identical to what the
  backend logs as the turn prompt.
