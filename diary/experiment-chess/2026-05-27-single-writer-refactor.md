---
type: diary
touched_work: [experiment-chess]
touched_concepts: [tools-component, agent-infrastructure-vs-capability]
status: open
---

# 2026-05-27 — Single-writer refactor: agent-commit replaces agent-move

Long session today. Started with the args-contract migration ([[2026-05-27-run-script-args-list]]) and ended with a structural refactor of the agent's move-commit path. The structural fix is in [[2026-05-27-single-writer-move-contract]] — this diary entry is the narrative.

## How we got here

Today's debugging chased a sequence of related bugs across the agent's move-commit path. Each fix was layer-local and looked correct in isolation, but kept exposing a deeper structural issue.

The sequence (compressed):

1. **AgentPanel.tsx crashed** on `scriptArgs.match is not a function` after the `args: list[str]` migration. Frontend assumed `args` was a string. One-line fix in `extractMove()`/`argsDisplay()`. ✓
2. **Maia stopped responding after the agent's first move.** Game `2adaecb9...` shows `move_count=1` with no lc0 process. CSV shows `aborted_reason: "expected uci string to be of length 4 or 5: 'e4'"`. Root cause: `AgentPlayer.get_move`'s return path called `chess.Move.from_uci(committed_uci)` directly on the script's `move` field — which after the args-contract change was now SAN (`"e4"`) instead of UCI (`"e2e4"`). Fix: try UCI then SAN against the pre-move board snapshot, mirroring `_push_uci_move`. ✓ (commit 4e492e0)
3. **First move fails before that** — the API schema layer rejected SAN strings entirely with "string_too_short". `MoveRequest`'s `min_length=4, pattern=^[a-h][1-8][a-h][1-8][qrbn]?$` was strict UCI. Fix: split into `MoveRequest` (strict, for human moves) and `AgentMoveRequest` (looser, for agent submissions where `_push_uci_move` handles UCI-or-SAN). ✓ (commit fa368de)
4. **The hard one — phantom `exd5` on the host board.** Game `4632ac7a...` turn 4: agent's prompt FEN was correct (4 plies, white to move). Agent imagined `exd5`, imagined `Nf3`, decided `Nf3`, POSTed `make_move(Nf3)`. Server returned `"It is not the agent's turn"` with black's legal moves. Host board had 5 plies — `e4d5` somehow added between T4 prompt construction and event 9. **No code path I could find pushed `exd5`.** The agent log had no `make_move(exd5)` call. The imagine_move.py script does only GET requests. `_push_uci_move` was only called from `submit_agent_move`. Two writers (bot loop + `/agent-move`) made the system unauditable.

That fourth bug is what triggered the step-back.

## The step-back

The user pushed me to stop debugging in the small and reason about the contract:

> "It should be a back and forth right, agent submits move → sends to ai → ai commits move → sends to agent as a prompt. Think about what should be handled universally as the game, and what should be up to the different kinds of players and how they submit and receive moves."

That framing reorganises the whole problem. The bot loop should be the single mutator. Each player is a black box from `(board, last_move_san) → chess.Move`. The fact that *one* player (AgentPlayer) used a side-channel HTTP endpoint to push the move directly to the board — bypassing `get_move`'s return path — was the entire root cause of the cluster.

Maia, ChessCom, Human: all follow "player returns move, loop pushes."
AgentPlayer: pushed via `/agent-move`, then returned a move that the loop detected as "already applied" and skipped. Two paths to mutation; the bot loop tried to coordinate them with `already_applied`.

## The refactor

Documented fully in [[2026-05-27-single-writer-move-contract]]. The shape:

- `POST /api/games/{id}/agent-move` → **`POST /api/games/{id}/agent-commit`**.
- The new endpoint validates legality, turn, and move-shape (UCI-or-SAN, strip `+`/`#`). Returns the canonical UCI on success, HTTP 400 with `detail` on failure. **It does not push.**
- `make_move.py` POSTs to the new endpoint; receives the canonical UCI; prints the same `{ok, move, reasoning, message}` JSON to the model so `_committed_move_from_result` continues to work unchanged.
- `AgentPlayer.get_move` parses that JSON; returns `chess.Move.from_uci(canonical_uci)`. No more SAN reparse — the endpoint guarantees the UCI is valid.
- The bot loop drops the `already_applied` branch. Every player's returned move goes through `_push_move(game, move)`. Same as Maia, same as ChessCom.

### What's gone

- `submit_agent_move()` method on GameService.
- `_push_uci_move` from the agent path (still used by `_submit_human_move`).
- `AgentMoveRequest` schema.
- `already_applied = len(game.uci_moves) >= move_number` detection in `_run_until_human_or_finished`.
- The SAN-fallback `board.parse_san` call in `AgentPlayer.get_move`'s return path.

### What stays

- All other player implementations (Maia, ChessCom, Human, Stockfish).
- All chess-skill scripts other than `make_move.py`.
- The compaction mechanism (`_pending_summary` → HistoryProcessor) — still fires only on successful commit, as before.
- The retry semantics (`_MAX_ATTEMPTS`, `_NO_MOVE_REMINDER_TEMPLATE`, budget warning).
- `imagine_move.py`, `show_position.py`, `list_legal_moves.py` — pure GETs, unchanged.

### Make-move is always the last successful action

The user's framing on this:

> "make a move is always the last thing it does (but remember, only when successful)"

Encoded in the `ToolResultEvent` handler: a successful `make_move` returns immediately from `get_move`. An unsuccessful one (illegal move) keeps the stream alive — the model sees the `legal_moves` list in the result and retries inline. Compaction fires only on success.

## Live verification

Hit vLLM with the new schema (Gemma 4 31B-it). Sent a SAN move with a check annotation and apostrophe-laden reasoning:

```
args = ["Nxf6+", "Captured the knight; ... Black's queen ..."]
```

Both elements survive the JSON envelope. No quoting issues, no string-truncation, no schema-mismatch on the API side (`AgentCommitRequest` accepts move strings 2-12 chars, no regex). Backend tests: 120 pass.

## What I expect from the next batch

The bug I couldn't find this morning — phantom `exd5` — cannot happen under the new contract because there is no second writer. If the host board diverges from expected, the source is one of:
- The bot loop's `_push_move` (visible in INFO logs).
- The human-move path (`_submit_human_move` → `_push_uci_move`) — irrelevant for agent batches.
- Persistence reload from disk (only at game create or load).

No other code path mutates `game.board`. That's the structural guarantee.

Other failure modes from earlier today (apostrophe explosion, 22% `imagine_move` empty-args loops, `make_err` from `--uci` parsing) are all addressed by the args-contract change plus the schema-required `args`. Those fixes are upstream of the structural refactor and still hold.

## Knowledge-base touch list

- New ADR: [[2026-05-27-single-writer-move-contract]]
- Updated: [[work/experiment-chess]] (bullet on `make_move.py` commit semantics)
- Updated: `experiments/chess/scripts/recover_orphan_game.py` docstring (historical note about the old endpoint)
- This diary entry.

The earlier session diary ([[2026-05-27]], [[2026-05-27-batch-analysis]]) still describes the args-contract migration as it was — accurate at the time, superseded today by the structural change.

## Follow-ups

In rough order:

1. Run a single calibration game on the new contract. Expect zero "It is not the agent's turn" errors, zero double-pushes, zero phantom moves.
2. If the single game looks clean, run a 5-game experimental batch to confirm the contract holds under more turns.
3. Watch for `imagine_move` empty-args loops. The schema-required `args` (SDK commit `aba275f`) should prevent the no-args call from being emittable, but verify in trace.
4. Note any new failure modes the refactor reveals. Symmetric players should behave symmetrically; if AgentPlayer still misbehaves uniquely, the issue is now firmly inside AgentPlayer, not in the contract.
