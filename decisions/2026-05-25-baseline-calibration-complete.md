---
type: decision
status: accepted
---

# 2026-05-25 — Bare-model baseline calibration is complete; next batches build on the recorded trajectory

## Context

The first ranked calibration batches under the post-2026-05-25 configuration (Gemma 4 31B-it on eX3, initial ELO 1200, chess.com pool with floor 700, per-turn fresh context, retry-then-resign on missing tool calls) produced 26 games over two batches: 22 losses, 4 draws, 0 wins. The agent's recorded ELO trajectory was 1200 → 684.2.

After game 4 the matchmaker reached the chess.com pool floor at 700, and every subsequent game was played against chess.com-700. The streak-based opponent selector tried repeatedly to step further down (streak reached -5) but was clamped by the floor. Of the 24 games at chess.com-700, 21 were losses and 3 were draws.

This is the signature of an agent whose true ELO is *below* the pool floor: the rating is no longer searching for parity, it is drifting downward against the lowest available opponent at the rate that classical Elo charges for repeated same-rated losses (~10 pts per loss, K=20).

## Decision

### 1. Bare-model baseline calibration is declared complete

We will not run further batches under the bare-model configuration. The recorded number (ELO 684.2 after 26 games) is the calibration result for the bare-model baseline.

**Methodological framing:** the agent's true ELO is **at or below the chess.com pool floor of 700**. We do not have a precise point estimate because the pool ends at 700; what we have is a high-confidence ceiling. This is a property of the experimental setup, not a methodology flaw — the pool floor was set deliberately ([[2026-05-25-chesscom-pool-floor]]) because games against bots rated below 700 converge on time-cap draws regardless of agent skill, producing uninformative results. The four draws at chess.com-700 in the current batch corroborate this empirically: the draw-by-non-conversion pattern is observable at the floor, not only below it.

The number "684.2" should be read as **"≤ 684.2 with measurement bounded by the pool floor"** wherever it appears in the thesis. The methodology chapter should make this bound explicit, not present 684.2 as a point estimate of true skill.

### 2. Subsequent batches continue from the recorded ELO; no reset

When the skill-library work begins, batches will continue from `agent_elo.json` as it stands at the end of this calibration: `elo=684.2, games_played=26, streak=-5`. Two reasons:

- **The trajectory is the experiment.** Phase 1's claim is that the self-correcting learning loop produces measurably better agents over time. Visible improvement means upward drift from a known starting point. Resetting to 1200 would hide that signal under a re-calibration phase.
- **The starting ELO is the bare-model anchor.** Any future configuration's calibrated ELO is interpretable relative to this number ("the library adds N points to the baseline"). Resetting would forfeit that comparability.

Continuing from 684.2 means future configurations inherit the streak counter (-5) and games_played (26). Adaptive K has already moved out of provisional (>15 games), so future games will use K=20. The first few games of the next batch will likely show large opponent-step movements because the streak counter is still loaded — this is expected behaviour and not a calibration artefact; the streak will reset on the first non-loss.

### 3. No success criterion is set today

The threshold for "the skill library beats baseline" is deferred. It depends on what the library configuration looks like at the time, and it can be defined in its own ADR when the library work is ready to start. Setting it now would be premature.

### 4. ranked.csv at this point is the canonical baseline record

The current `experiments/chess/backend/games/ranked.csv` (26 rows ending at `5ae8f02c708a4fdb8e31d3b288c6da8c`) and the corresponding `agent_elo.json` are the durable record of the bare-model baseline. They are tracked in git; the commit they land on is the calibration boundary. Any future analysis comparing library performance against baseline reads from these rows directly.

## Consequences

- The thesis chapter on Phase 1 has a concrete number to anchor on: bare-model Gemma 4 31B-it, no skill library, no helper tools, plays at or below ELO 700 against the chess.com Engine pool.
- The library-development work can start whenever the experiment is ready for it. No further calibration is required first.
- The "≤ pool floor" framing must be carried into the writeup carefully. Naive readers will see 684.2 and assume it is a measurement; the ADR is the authority that says it is a ceiling.
- If a future configuration's ELO rises and then falls back below 700, the same pool-floor caveat applies: we know the configuration is at least as weak as the bare model, but not how much weaker.

## Open items

- When the skill-library configuration is ready, write a follow-up ADR defining the success criterion (specific opponent rating, number of games, win-rate or ELO-delta threshold).
- Consider whether Maia (1100–1900) should be added to the pool for future configurations. The bare-model agent could not reach Maia's lower bound; a library-enhanced configuration might. Decide before the first library batch so the methodology is consistent across the comparison.
