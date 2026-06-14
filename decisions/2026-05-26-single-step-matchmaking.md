---
type: decision
status: accepted
supersedes: 2026-05-20-elo-and-batch-runner
---

# Single-step opponent selection (replacing doubling)

## Context

The original matchmaking policy (defined in
[[decisions/2026-05-20-elo-and-batch-runner]] §3) used streak-based
doubling: `|streak|=1 → step 1, 2 → 2, 3 → 4, 4+ → 4 (capped)`. The
rationale at the time was logarithmic calibration — getting an agent
that started at 1200 down to its true ~300 ELO in a handful of games
instead of an 11-game walk.

That worked for the initial descent. But once the agent reached its
neighbourhood it kept producing jumps that were too aggressive for
steady-state calibration.

Observed on the post-merge batch on 2026-05-26 (agent at ELO ~684 on
chesscom pool):

| Game | Opponent | Result | Agent ELO after |
|------|----------|--------|-----------------|
| 1    | 700      | win    | 694.7           |
| 2    | 850      | win    | 708.9           |
| 3    | 1000     | loss   | 705.7           |

Two wins from an ELO-700 agent triggered a 300-point opponent jump
(700 → 850 → 1000), against a player whose own rating was barely 700.
The next loss against 1000 produced a small ELO downward correction
because the model "expected to lose," but the game itself was
uninformative.

The chess.com pool spacing is the root cause: notches are 150 ELO apart
at the low end (700 / 850 / 1000) so doubling magnifies fast. A
doubling policy would be reasonable on a 50-ELO grid; on a 150-ELO
grid, the very first multiplication of the step already overshoots.

## Decision

Replace doubling with always-single-step:

```python
def step_from_streak(streak: int) -> int:
    if streak == 0:
        return 0
    return 1 if streak > 0 else -1
```

`MAX_STEP` constant removed (no longer needed).

Streak rules unchanged — they still drive draw decay, direction flips,
and the per-batch streak counter. Only the step magnitude is affected.

## Consequences

**For calibration around the agent's true ELO** (the post-baseline
regime we're now in):
- Each game moves at most one notch in either direction.
- A 4-game flip-flop (win/loss/win/loss) stays at the same opponent
  ±1.
- Convergence speed is bounded by the size of one grid step, which is
  the appropriate granularity given Stockfish-style noise in single-game
  outcomes.

**For first-time calibration of a new model** (the case the original
doubling was built for):
- An 800-ELO gap would take ~6 games to traverse instead of ~4. Worth
  it given that the agent's first calibration is a one-time cost and
  the steady-state batches are repeated.

**For draws**:
- Existing behaviour preserved. A draw halves the streak toward zero;
  a draw at streak 0 stays at 0 (re-plays the same opponent next time,
  which is the right behaviour for "haven't conclusively beaten or lost
  this rating yet").

## Alternatives considered

- **Gentle additive (1, 1, 2, 2, 3, capped)**: less radical but still
  has the same issue at the low end of chess.com where notches are 150
  apart.
- **Lower MAX_STEP from 4 to 2**: would have produced a step sequence
  of 1, 2, 2, ... — better than the original but still allows a 2-notch
  jump after a single subsequent win.
- **Direction-asymmetric stepping** (faster down than up): could match
  the user's intuition that losses should explore faster than wins
  (because the floor is more interesting than the ceiling for a weak
  model) but adds methodological complexity that's hard to justify in
  the thesis.

Single-step is the simplest robust choice and matches what the user
actually wanted to see.
