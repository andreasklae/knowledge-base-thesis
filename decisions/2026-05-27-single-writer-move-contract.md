---
type: decision
status: accepted
---

# 2026-05-27 — Single-writer move contract: agent-commit endpoint replaces agent-move

## Context

The chess experiment used to have **two writers** to `game.board`:

1. The bot loop's `_push_move(game, move)` for every player's returned move.
2. `submit_agent_move` on the `POST /api/games/{id}/agent-move` endpoint,
   which `_push_uci_move`'d the move directly when `make_move.py` POSTed it.

The bot loop tried to coordinate the two via an `already_applied` branch:
after `agent.get_move()` returned, the loop checked `len(game.uci_moves) >= move_number` to decide whether to push or skip. This pattern was a documented seam at the time it was introduced ([[2026-05-25]]), but it carried hidden costs that surfaced as a cluster of bugs over the next two days:

- An asymmetry in the player contract: Maia, ChessCom, Human players returned a `chess.Move` and the bot loop pushed it; AgentPlayer pushed via a side channel and the bot loop detected-and-skipped.
- A chain of fragile string round-trips for the agent's move: SAN→UCI parse in `_push_uci_move`, then a second UCI→Move parse in `AgentPlayer.get_move` to recover a `chess.Move` for the bot loop's expected return type, then a check against a stale board snapshot.
- A class of bugs that look impossible from disk evidence: a move appearing on the board that no visible code path pushed. On 2026-05-27 the agent committed `Nf3` and got "It is not the agent's turn" because the host board already had `exd5` applied; the agent log showed no `make_move(exd5)` call. With two writers we couldn't rule out a leaked task, a chesscom-driver mis-attribution, or a stale callback as the second writer. The system was unauditable.

The schema-vs-stack mismatches caused by these layers also produced the rapid-fire failure modes we just chased: the API validator rejecting SAN strings ([[2026-05-27-batch-analysis]]), then `AgentPlayer.get_move` calling `chess.Move.from_uci` on SAN strings, then the bot loop seeing a stale board snapshot, and so on. Each fix was a layer-specific patch over the same structural problem.

## Decision

**The bot loop is the single writer to `game.board`.** Every player —
agent, chesscom, maia, human — returns a `chess.Move` from `get_move()`; the bot loop pushes it under `game.lock`.

The agent-specific side-channel changes from "push the move" to **"validate the move"**:

- The `POST /api/games/{id}/agent-move` endpoint is replaced by **`POST /api/games/{id}/agent-commit`**.
- The new endpoint is a pure validator. It checks turn (must be the agent's), legality against `game.board.legal_moves`, and move-string shape (UCI-or-SAN, trailing `+`/`#` stripped). On success it returns the canonical UCI; on failure it raises HTTP 400 with detail.
- It **does not push to the board**.
- `make_move.py` POSTs to `/agent-commit`, receives the canonical UCI, prints the same success-result JSON as before (`{ok, move, reasoning, message}`).
- `AgentPlayer.get_move`'s tool-result handler still parses that JSON, returns the parsed `chess.Move`. **The bot loop pushes it on the next lock acquisition.**

The `already_applied` branch is removed. The bot loop always pushes the move that the player returned.

### Contract symmetry

The "player only returns moves; bot loop pushes them" contract now applies uniformly. A player has no concept of who the opponent is or how the opponent submits — it sees `(board, last_move_san)` and returns a `chess.Move`. Maia runs an engine; ChessCom mirrors to a browser and waits for chess.com's reply; AgentPlayer runs the LLM. Each player's internals are its own concern. The bot loop owns turn sequencing, lock acquisition, and the only mutation to `game.board`.

ChessCom remains the *odd one out* in a minor sense: it still has a side-channel (the browser), but the browser is an external system, and ChessComPlayer's `get_move` ensures host-and-browser sync internally. The host's push surface is untouched by chesscom — only by the bot loop's `_push_move`.

### Make-move failure semantics

Two distinct failure modes inside one chess turn:

- **Failed `make_move` call within a stream (illegal move).** The endpoint returns HTTP 400; the script prints `{ok: false, error, legal_moves: [...]}`; the model sees the error inline and retries within the same stream, in the same `agent.get_move()` attempt. No turn-level retry needed.
- **Stream ends without any successful `make_move`.** AgentPlayer's outer loop opens a new attempt with `_NO_MOVE_REMINDER_TEMPLATE` prefixed onto the same `base_prompt` (the turn's position hasn't changed). Up to `_MAX_ATTEMPTS=10` total. Beyond that → `AgentResignedError` → game ends 0-1.

Compaction (the `_pending_summary` slot consumed by `_make_turn_memory_processor`) fires only on a *successful* `make_move`. Failed attempts don't compact; the model's prior-turn memory is whatever the last successful commit produced.

### Make-move is always the last action

A successful `make_move` ends the agent's turn. The `ToolResultEvent` handler in `AgentPlayer.get_move` returns immediately on success, breaking out of the streaming loop. The model is instructed (in SKILL.md) to stop calling tools after a successful `make_move`. The bot loop then pushes the move, and the next iteration of `_run_until_human_or_finished` handles the opponent's turn.

## Consequences

### Positive

- **Single writer ⇒ provable consistency.** Every mutation to `game.board` is traceable to one site (`_push_move` called from the bot loop). Bugs of the form "where did this move come from" cannot happen.
- **Removes `already_applied` and the second push path.** The class of races and double-pushes the previous design enabled is gone by construction.
- **Removes the `chess.Move.from_uci` reparse fragility.** The endpoint returns the canonical UCI; `from_uci` on that always succeeds because the endpoint validated it against the live board.
- **Removes `_push_uci_move` from the agent code path.** It still exists for `_submit_human_move` (where chessground emits canonical UCI), but the agent path no longer uses it.
- **Consistent player contract.** No special-case handling for AgentPlayer anywhere in the bot loop.

### Negative

- **HTTP round-trip is still required** for the validation, so wall-clock latency per agent commit is unchanged. The endpoint's work is lighter (no push, no eval task, no publish), but the network hop dominates.
- **Reasoning text travels through the script's stdout JSON rather than being persisted in a server-side slot.** Acceptable: it's already in the script's success-result, which is what `_committed_move_from_result` parses, and it's what feeds `_pending_summary`. No new round-trip needed.

### What stays

- `_push_uci_move` (used by `_submit_human_move`).
- `MoveRequest` schema (strict UCI for human moves from chessground).
- Compaction logic, HistoryProcessor, prior-turn memory injection.
- `imagine_move.py`, `show_position.py`, `list_legal_moves.py` — pure GETs, unchanged.
- ChessCom driver, Maia runner, all other player types.

## Verification

- Backend tests: 120 pass (2 pre-existing failures in `test_backend.py` unrelated).
- Live vLLM test: Gemma 4 31B emits `args=["Nxf6+", "<reasoning with apostrophes>"]`; the endpoint accepts the SAN+check form, strips `+`, returns canonical UCI `f3f6` (or whatever).
- End-to-end: a single game agent-vs-Maia or agent-vs-chesscom should complete without any "It is not the agent's turn" mismatches, without any phantom board states, and without the `_committed_move_from_result` reparse path being exercised.

## References

- [[2026-05-25-perception-tools-and-skill-rewrite]] — where the original `/agent-move` push design was introduced
- [[2026-05-26-stabilization]] — earlier stabilisation pass over the same code area
- [[2026-05-27-run-script-args-list]] — the args-contract change that exposed how fragile the SAN/UCI string handling was
- [[2026-05-27-batch-analysis]] — the trace evidence that surfaced the SAN-at-API and reparse bugs
- [[diary/experiment-chess/2026-05-27-single-writer-refactor]] — implementation diary
