---
type: decision
status: accepted
supersedes: null
---

# Reasoning must precede the move, not follow it

## Context

After switching the chess agent from GPT-4o to Gemma 4 31B-it via eX3 vLLM, observation of the live agent feed showed Gemma's default behaviour is **tool-first**: on a chess-move prompt, it calls `make_move.py` immediately and then produces reasoning text afterwards. The text rendered in the UI as "reasoning" was in fact post-move analysis of the move just played — it had no causal influence on the move that was already committed.

This was confirmed by isolating the model with two test prompts directly against vLLM:

1. **Plain user query, no instruction to reason** ("What's the weather in Tokyo?" with a `get_weather` tool available): Gemma emitted zero `delta.content` tokens and went straight to the tool call. ~1 second total.
2. **Explicit "reason step by step before calling any tool" system prompt** on a math problem: Gemma streamed ~35 seconds of reasoning text and had not yet called the tool when the stream was cut off.

Conclusion: Gemma 4 **can** reason before acting, but only does so when the prompt explicitly demands it. The original chess system prompt ("Think out loud before every move") was not strong enough to override Gemma's default tool-first behaviour.

This matters for the experiment: if the move is decided before any reasoning is produced, the reasoning text is decorative and the agent is effectively playing blind. The thesis's claim about agent behaviour rests on reasoning *informing* the move, not the other way around.

## Decision

1. **Strengthen the chess agent's system prompt** to require an explicit, numbered sequence: load skill → list legal moves → **write 2-4 sentences of reasoning comparing candidate moves** → call `make_move.py` → end the turn. The reasoning step is enforced verbally; the prompt also explicitly says any text after `make_move.py` is treated as post-hoc and discarded for analysis.

2. **Label pre-move and post-move text differently in the UI.** The frontend tracks whether `make_move.py` has been called in the current turn. Text deltas before the call are rendered as `reasoning` (the move-influencing artefact). Text deltas after the call are rendered as `post-move` in a visually muted style, clearly marked as not informing the move.

3. **Do not yet hide post-move text.** It remains visible in the UI because it is potentially useful for later analysis (e.g. consistency checks: does the agent's post-hoc justification align with its pre-move reasoning?). It is just labelled honestly.

## Consequences

- The methods chapter must document that the "reasoning" recorded per move is the text emitted between `list_legal_moves` and `make_move` within a single turn. Post-move text exists in the agent JSON logs but should not be cited as the move's justification.
- For batches run **before this decision**, the recorded reasoning is post-hoc rather than ante-hoc. Those batches are not invalidated, but the framing in the analysis must reflect that distinction.
- Calibration runs starting from 2026-05-24 onward use the strengthened prompt. Combined with the [[2026-05-24-initial-elo-600]] starting ELO, this is the first methodologically-clean Phase 1 baseline.
- A future tool for analysis: compare pre-move vs post-move text per turn. Disagreement between them is a signal of either model inconsistency or a flawed move that the model post-rationalises.
- Open question, not closed by this decision: whether to use `manage_todos` as a structural scaffold for reasoning ("plan, then act"). Deferred — could become a tool for *improving* the model rather than just observing it. See [[work/experiment-chess]] open items.

## Related decisions
- [[2026-05-20-elo-and-batch-runner]] — ELO formula, batch runner, opponent stepping
- [[2026-05-24-initial-elo-600]] — informed starting prior
- [[2026-05-24-per-turn-fresh-context]] — per-turn fresh context (baseline calibration)
- [[work/experiment-chess]] — main experiment design page
