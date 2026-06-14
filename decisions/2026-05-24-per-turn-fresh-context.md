---
type: decision
status: accepted
supersedes: null
---

# Per-turn fresh context for the chess agent (baseline calibration)

## Context

Phase 1 calibration measures **the bare Gemma 4 31B-it model's chess strength** — no skills, no planning, no memory beyond the current turn. That measurement is the floor against which every future improvement (skill library, planning, retrieval, etc.) is compared.

The skillful-agent SDK accumulates conversation state in `Agent._conversation_messages` across calls to `run_stream()` on the same `Agent` instance. The chess backend creates one `AgentPlayer` per game ([[work/experiment-chess]] enforces fresh `Agent` between games), but within a single game every move's prompt, reasoning, tool calls, and tool results accumulate. A long game's per-move prompt grew to >61k tokens, hitting Gemma's 65k context window and 400'ing the request mid-game.

The 65k window is a deliberate vLLM cap (`software/ex3/serve.py` `--max-model-len 65536`); Gemma 4 31B supports 256K natively but raising the cap on the GH200 risks OOM. Even at 256K, unbounded growth would just delay the failure.

Three context strategies were considered:

| | Pros | Cons |
|---|---|---|
| Per-turn fresh (no cross-turn memory) | Bounded prompt size; deterministic; clean baseline | Loses cross-turn reasoning |
| Auto-compaction (skillful-agent's existing) | Already implemented | Non-deterministic; injects compression noise into baseline |
| Sliding window (last N moves) | Some continuity | Arbitrary N; unprincipled |

## Decision

**Run baseline calibration with per-turn fresh context.** Implementation: `AgentPlayer.get_move()` calls `self._agent.clear_conversation()` at the start of every turn. The agent enters each turn seeing exactly: system prompt + skill list + one user message (opponent's last move + FEN).

Rationale: the FEN encodes complete game state. Move selection at the model level requires no historical context to be correct. Cross-turn memory is a separate experimental variable that future configurations will introduce and measure as an ELO delta against this baseline. Bundling it into the baseline would conflate "model strength" with "model's ability to use its own conversation history."

This decision applies to the **baseline configuration only**. Configurations testing memory, planning, or retrieval skills will deliberately violate this and the methods chapter will record the deviation explicitly.

## Aborted-game handling (related)

When a player exception fires mid-game (context overflow, illegal move, browser crash), `GameService` now:

1. Stamps `game.aborted_reason` with the error message.
2. Records the game to `games.csv` with `result=""` and the reason in a new `aborted_reason` column.
3. Fires `_on_game_finished` so `BatchRunner` advances to the next game.
4. Tears down player resources cleanly.

`BatchRunner` skips the ELO update for aborted games (`parse_game_result` returns `None` for unfinished games, which already short-circuits `apply_result`). This is the **no-ELO-change** policy: aborted games are observed and logged, but do not count for or against the agent's measured strength. Justification: the model did not technically play out the position; punishing or rewarding it would distort the rating.

## Skillful-agent: typed overflow exception (related)

The SDK now raises `AgentContextOverflowError` (in `skill_agent/exceptions.py`) when a model rejects a request for exceeding context length. Callers can catch this without parsing provider-specific error strings. The chess backend catches it in `AgentPlayer.get_move()` and re-raises as `PlayerError("context_overflow: …")`, which the bot loop turns into the aborted-game path above.

The SDK's existing auto-compression fires *after* a successful run; it cannot prevent a pre-flight overflow. A TODO comment in `Agent._event_stream` marks pre-flight compaction with retry as the natural next-level fix, deferred to avoid changing framework behaviour during baseline calibration.

## Consequences

- **Baseline ELO is now a clean measurement of bare model strength.** Combined with [[2026-05-24-initial-elo-600]] (informed prior) and [[2026-05-24-reason-before-move]] (reasoning order), 2026-05-24 batches onward are the first methodologically-clean Phase 1 floor.
- **Games can no longer die silently.** Overflow → typed exception → recorded abort → batch advances. Operators see `aborted_reason` in the CSV.
- **`games.csv` schema gains an `aborted_reason` column.** Existing analysis tools that select columns by name continue to work; tools that read by position need an update.
- **Future improvement axes are well-isolated:**
  - baseline → +memory (e.g. sliding window, auto-compaction)
  - baseline → +skills (the actual thesis claim)
  - baseline → +planning (managed context)
  Each contribution becomes an ELO delta against this baseline.
- **The methods chapter must state explicitly** that "the agent's prompt at turn N is a function of turn N only — system prompt + FEN + opponent's last move." Anyone reproducing the baseline must call `clear_conversation()` per turn or the numbers will not match.

## Open follow-ups

- Pre-flight compaction with retry inside `Agent._event_stream` — TODO comment left in code; revisit once baseline is captured.
- Decide if/when the experiment graduates to a memory-bearing configuration. Likely after the skill-library experiment establishes the basic learning loop works.

## Related decisions
- [[2026-05-20-elo-and-batch-runner]] — ELO formula, batch runner, opponent stepping
- [[2026-05-24-initial-elo-600]] — informed starting prior
- [[2026-05-24-reason-before-move]] — reasoning must precede the move
- [[work/experiment-chess]] — main experiment design page
