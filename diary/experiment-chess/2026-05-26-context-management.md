# 2026-05-26 — Context management and agent-authored turn memory

## What was confirmed

Ran a full game (84 turns, agent vs 700-rated bot) with the HistoryProcessor-based context injection active. Inspected the `_agent.json` log to verify the mechanism works end-to-end.

**Context injection confirmed working.** From turn 3 onward, the `context_summary` event appears in the log immediately after each committed move. The HistoryProcessor fires before every `run_stream_events` call, replacing prior history with the `(original_prompt, summary)` two-message exchange. Retries within a turn correctly see the full turn context rather than a premature compressed version.

## What was broken: throwaway LLM summaries

The summaries were bad. The throwaway agent received only the UCI string and rejected candidates — no board context, no position, no analysis. It hallucinated move intent: `e1e7` became "promoting the pawn to a queen" (it was a rook capture); `d5d7` became "creating a passed pawn" (it was the queen moving). The `Watch` field was generic noise ("opponent's central counterplay") repeated verbatim across 30 turns. `Rejected` was empty almost every turn because the agent rarely called `imagine_move` on attempt 1, and never on the rushed retry.

The summaries were also often of *different* moves than the ones the agent intended — the agent described one move in text on attempt 1, then committed a different move under the retry prompt on attempt 2 (having lost its analysis context). The throwaway summariser then faithfully summarised the wrong move.

## The no-move loop and queen blunder

Every turn followed the same pattern:
1. Agent reads skill, writes detailed analysis prose, never calls `make_move.py`
2. Retry with bare FEN, no prior analysis context
3. Agent picks a different move (sometimes worse) and commits it under pressure

Turn 51 was the critical failure: the agent played `Rd6` (a hanging rook) on the rushed retry because it had no memory of the analysis it did on attempt 1. Black captured with `Qxd6` and the game was lost from there despite white having a large material advantage.

## Fix 1: retry prompt carries prior analysis

When a turn attempt ends without `make_move.py` being called, the next retry prompt now includes the agent's thinking text from the previous attempt: "Your reasoning from the previous attempt: ...". The agent can immediately call `make_move.py` on the candidate it already identified rather than re-deriving the position.

## Fix 2: agent-authored turn memory via --reasoning

Removed the throwaway LLM summariser entirely. `make_move.py` now requires a `--reasoning` argument. The agent writes its own note at commit time — when it has the full position, analysis, and intent in front of it. The text is free-form; no server-side format enforcement. It is stored verbatim and injected as the first message on the next turn.

This solves the hallucination problem (the agent knows what it played and why), closes the wrong-move/wrong-summary loop (you can't have a reasoning without committing a move), and eliminates the async throwaway agent call.

The `--reasoning` requirement also acts as a second forcing function: the move does not commit without it. The error message shows the expected format, so a model that forgets can self-correct.

## Fix 3: SKILL.md framing

Rewrote the opening to make the player role unambiguous: "You are the white player. Your only job is to call `make_move.py`." Added a dedicated "mandatory closing action" section at the top with a code block showing the full `--uci ... --reasoning ...` syntax. Added a "turn memory" explanation framing `--reasoning` as writing a note to your future self.

Also fixed: the skill name is `chess-player`, not `chess` or `chess_engine`. Added that explicitly to prevent the model reverting to training-data variants on retry.

## Game result

Agent lost in an endgame (84 turns). The loss was caused by the move-quality problem described above — the agent played well when it committed on first attempt, but committed bad moves on retries. The context management infrastructure itself worked correctly.
