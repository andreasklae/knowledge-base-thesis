---
type: decision
status: accepted
---

# 2026-05-25 — Agent resigns when it cannot commit a move; context overflow and environmental errors still abort

## Context

Three failure modes can prevent `AgentPlayer.get_move()` from returning a legal move:

1. **Agent capability failure.** After `_MAX_ATTEMPTS = 3` fresh-context runs, the model has not called `make_move.py` successfully. Examples: the model exhausted `max_turns=10` reasoning without acting; the run_stream finished cleanly without ever invoking the tool; the model repeatedly proposed the same illegal move (the failure mode that motivated the make_move.py-commits-on-call redesign earlier today).
2. **Infrastructure limit.** The model's input context overflowed (`AgentContextOverflowError`).
3. **Environmental error.** The browser crashed, the network failed, the inference server died.

Until now all three were treated identically: `PlayerError` raised → `game.aborted_reason` set → game recorded with `result=""` → `BatchRunner` skips ELO update. This conflates a chess-equivalent failure (the agent could not produce a move at all) with infrastructure failures that are not the agent's fault.

The conflation has two methodological consequences:

- It flatters the agent's ELO. A configuration that consistently fails to dispatch tools correctly looks the same on the rating curve as a configuration that hit a one-off network hiccup.
- It creates a perverse incentive: a buggy future configuration could "improve" its ELO by hanging on losing positions.

## Decision

### 1. Agent capability failure → resignation (loss)

When `AgentPlayer.get_move()` exhausts `_MAX_ATTEMPTS` without a committed move, it raises a new `AgentResignedError` (subclass of `PlayerError`). The game service treats this as resignation: the game ends with `result = "0-1"` (black wins) and `aborted_reason = "agent_resigned_no_move"`.

`BatchRunner._handle_game_finished` sees a normal `0-1` result and updates ELO accordingly (loss against the matched opponent). No special path in the batch runner is required — the rating system sees a clean chess loss.

The `aborted_reason` column on the CSV row preserves the forensic detail that this was a resignation by capability failure, not a chessboard checkmate. Downstream analysis can filter on it.

**Rationale:**

- **A human player who cannot move loses on time.** Resignation is the chess-correct analogue. If the agent has been given the position, the legal moves, three fresh-context attempts and capped output tokens, and still cannot produce a legal move, it has functionally lost the game.
- **The ELO trajectory now reflects total agent capability** — chess reasoning *and* tool-dispatch reliability. For a thesis on agent infrastructure, this is the right thing to measure. A model that reasons well but can't translate reasoning into action is a weaker agent, full stop.
- **It closes the perverse-incentive loophole.** No matter what goes wrong inside the agent's run, it cannot escape the rating consequence of "can't make a move."

### 2. Infrastructure limits → abort (no ELO change)

`AgentContextOverflowError` continues to raise `PlayerError("context_overflow: ...")` and produces an aborted game with `result=""`. ELO is unchanged.

**Rationale:** context overflow is a property of the model serving infrastructure, not of the agent's chess play. A 65k-token window that the prompt exceeds is the same kind of problem as a network drop — outside the agent's domain. Charging it against the rating would conflate methodology layers.

### 3. Environmental errors → abort (no ELO change)

Other player exceptions (browser crash, lc0 process death, HTTP failures from chess.com) continue to raise `PlayerError` and produce an aborted game with `result=""`. ELO is unchanged.

**Rationale:** same as §2. The agent did not cause these and could not have prevented them.

### 4. System prompt change: explicit short-reasoning instruction

The system prompt in `agent_player.py:_build_agent` is tightened to make the reasoning budget explicit:

> "Keep reasoning short — 2–4 sentences max. If you find yourself reasoning longer than that, stop and call make_move.py with your best candidate."

This is a soft constraint (the model may ignore it) but it complements the hard `max_tokens=1024` cap. Together they make runaway reasoning the worst case rather than the common case.

### 5. Implementation: `Game.result_override`

The mechanism is a single new field on `Game`:

```python
result_override: str | None = None  # If set, replaces board.result() in is_over() / result()
```

`is_over()` returns `True` when `result_override is not None`. `result()` returns `result_override` when set, otherwise the existing logic. This keeps the resignation path going through the same `_record_game_end` → `_on_game_finished` → `BatchRunner` flow as any other game ending — no parallel code paths.

In the bot loop's exception handler, `AgentResignedError` sets:

```python
game.result_override = "0-1"
game.aborted_reason = "agent_resigned_no_move"
```

before calling `_record_game_end` and `_on_game_finished`. All other `PlayerError` subclasses keep the existing behaviour: `result_override` stays `None`, `aborted_reason` is set, `result()` returns `None`, ELO is unchanged.

## Consequences

- The CSV gains a new value in the `aborted_reason` column: `agent_resigned_no_move`. Rows with this value will also have a `0-1` result (loss). Downstream analysis distinguishing "real losses" from "resignations" can filter on the column.
- The agent's ranked ELO trajectory is now more pessimistic than before: failures that previously left ELO unchanged now drop it. This is the intended methodological change.
- For an agent whose true ELO is below the pool floor (post-[[2026-05-25-chesscom-pool-floor]], floor 700), repeated resignations would walk ELO downward indefinitely. This is correct behaviour — the rating accurately reflects that the agent is not competitive at any rated level. It is also a useful experimental signal: a steady stream of resignations against pool-floor opponents indicates a configuration that needs intervention, not a calibration drift.
- The thesis writeup needs one sentence explaining what `aborted_reason=agent_resigned_no_move` means and why it's counted as a loss while other `aborted_reason` values are not. The ADR provides the source.

## Open items

- After the next batch, audit the proportion of `agent_resigned_no_move` vs. real-result losses. If resignations dominate, that signals tool-dispatch is the bottleneck rather than chess reasoning — informative either way.
