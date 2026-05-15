---
type: experiment
status: planning
related_concepts: [skills-component, data-component, deterministic-tools-hypothesis, learning-as-temporal-dimension, calibration-thread]
related_work: [experiment-math, experiment-riksantikvaren]
sources: [ericsson1993deliberate, sequoia2026karpathy]
updated: 2026-05-13
---

# Experiment: Skill-Acquisition Trajectory and Chess Tournament

Exercises the **Skills** and **Knowledge** chapters. Estimated effort: ~4–5 weeks combined. The largest single piece of experimental work in the thesis and the one most likely to expand — see [[../manuscript-notes/risk-register.md]].

## Two phases

The experiment tests two claims jointly:

1. A self-correcting learning loop produces measurably better agents over time.
2. The resulting skills and tools meaningfully outperform raw inference — and meaningfully *under*perform a deterministic strong-play tool (the chess engine), in line with [[deterministic-tools-hypothesis]].

### Phase 1: Skill-acquisition trajectory

A human-supervised agent plays games against bots in an Elo-matchmaking pool, identifying its weaknesses after each batch of games using a game-analysis API, and writing skills, documentation, and helper tools into a persistent library.

Runs until Elo plateaus. The plateau criterion is defined *before starting*; resisting extension is part of the risk mitigation.

**Measures, phase 1:**

- Elo over time.
- Size and structure of the library (number of skills, dependencies, naming patterns).
- Which skills are retrieved most frequently — and which are written but never used.

This is the agent analogue of deliberate practice [[ericsson1993deliberate]] and the productivity-as-infrastructure claim playing out at the skill-acquisition layer. See [[learning-as-temporal-dimension]] and [[skills-component]].

### Phase 2: Chess tournament

The library is *frozen* as a fixed artefact. Three configurations compete in a tournament alongside calibrated bots at varying Elos to give a meaningful Elo computation.

**Configurations:**

1. **Inference alone.** Fixed model, no library, no engine.
2. **Inference with the artefact.** Fixed model with the frozen skill library and helper tools from phase 1.
3. **Inference with a chess-engine API.** Fixed model with a chess engine as a deterministic strong-play tool. Upper bound and the [[deterministic-tools-hypothesis]] limit case.

**Measures, phase 2:**

- Computed Elo per configuration.
- The gap between configurations 1 and 2 (the skill-library contribution).
- The gap between configurations 2 and 3 (the deterministic-tool contribution beyond procedural knowledge).
- Calibration of move-evaluation against the engine where applicable.

## The deeper thesis claim under test

Karpathy's [[sequoia2026karpathy]] observation that the chess-capability jump between GPT-3.5 and GPT-4 was largely a lab data-curation decision is the lab-side version of this experiment's user-side claim: that the same kind of gain can be reached *around* a fixed model by skill accumulation rather than by retraining.

This is also the framework's claim that the data and skills components can be filled in automatically rather than requiring manual curation. See [[data-component]] and [[learning-as-temporal-dimension]].

## Cross-domain transfer

Flagged as future work in [[../manuscript-notes/open-questions-future-work.md]]; explicitly out of scope here. The chess experiment tests within-domain accumulation; whether the same loop produces transferable structure is a separate question.

## Risk

The largest scope-creep risk in the thesis. Mitigations are in [[../manuscript-notes/risk-register.md]]: plateau criterion defined up front, phase 2 not extended beyond Elo measurement.

---
*Lifted from `../manuscript-notes/essay-pointer.md` (Essay/essay.tex §3.3, §3.5, §4.2-Experiment 5).*
