---
type: concept
sources: [ericsson1993deliberate, sequoia2026karpathy, aizawa2025tools, karpathy2025wiki]
related_concepts: [framework-four-components, skills-component, data-component, workspace-component, calibration-thread, skill-acquisition-loop]
related_work: [experiment-chess]
status: draft
updated: 2026-05-16
---

# Learning as the Temporal Dimension of the Framework

**Claim.** Learning is not a fifth component of the framework. It is the temporal dimension of the existing four.

- **Skill acquisition** writes to [[skills-component]].
- **Knowledge updating** writes to [[data-component]].
- **Workspace history** accumulates within and across sessions; see [[workspace-component]].
- **Tool-use experience** refines [[tools-component]] selection.

[[framework-four-components]] describes the affordances an agent needs at the moment of doing work. Learning describes how those affordances grow over time.

## Deliberate practice as the agent analogue

[[ericsson1993deliberate]]: expertise comes from focused exposure to tasks at the edge of current capability, with feedback-driven retention of what works. Phase 1 of [[experiment-chess]] is a direct test of whether this structure transfers to agents — a fixed model in a self-correcting loop, encountering tasks it cannot solve, learning to solve them, and storing the learned procedures as skills that persist across sessions.

The claim under test is that such an agent becomes measurably better at related tasks over time without retraining: improvement comes from the skill store, not from the model.

## The scientific method as productivity infrastructure

The chess setup also instantiates a self-correcting loop whose pattern is the structure of the scientific method — arguably the most consequential productivity infrastructure humans have ever constructed. Science is productive not because individual scientists are correct but because peer review, replication, and accumulated literature surface and rectify error at a rate no individual mind could match. The framework's claim, refracted through this experiment, is that the same logic applies to agents: the productive question is not whether a model can self-correct in isolation but whether the infrastructure around it (a skill store that persists across sessions plus a fixed external critic in the form of game outcomes) can do for an agent what the institutional apparatus of science does for fallible human researchers.

## A relevant Karpathy data point

[[sequoia2026karpathy]] notes that the chess-capability jump between GPT-3.5 and GPT-4 was largely a lab data-curation decision rather than an architectural advance. [[experiment-chess]] tests whether equivalent gains can be reached from the user side, by skill accumulation around a fixed model, rather than from the lab side, by retraining.

## Calibration role

Skill acquisition is only useful if the agent records procedures whose success conditions it can later verify. The temporal dimension of [[calibration-thread]]: the system gets more calibrated as the externalised verification record grows.

## The eval-driven loop as accumulating infrastructure

[[aizawa2025tools]] gives the operational pattern for the tools side: prototype → run evaluation → analyse with agent → refactor tools → repeat, with held-out test sets to guard against overfit. The Slack and Asana cases (67.4% → 80.1%; 79.6% → 85.7%) are *learning over time at the tools layer* — the model is fixed; only the surrounding infrastructure improves. This is direct support for the temporal-dimension claim at a different component layer.

## Wikis as accumulating data infrastructure

[[karpathy2025wiki]] frames the same temporal accumulation at the data layer: *"the wiki is a persistent, compounding artifact"*. Every ingest updates entity pages, revises summaries, flags contradictions; the knowledge base gets richer with every source. The Bush-Memex framing makes the maintenance constraint explicit — what was previously bound by human labour is now bound by agent capability, and the data component grows in proportion to that capability.

## Batches as the operational unit of learning

See [[skill-acquisition-loop]] for the full loop structure and current implementation status. In brief: [[experiment-chess]] operationalises the temporal dimension with a concrete unit: a *batch* is the set of games played at a single commit hash of the agent's skill repo. Between batches is where self-correction happens — the agent inspects what went wrong, writes or revises skills, commits, and starts a new batch. This makes the learning loop both observable and reversible: every game record carries the skill-repo SHA it was played under, so any Elo movement can be attributed to a specific diff in the skill library. `git checkout <sha>` recreates the agent that played a given game.

The methodological pay-off is that "which actions caused the Elo to jump" becomes a query, not a guess: diff consecutive batch SHAs, read the structured batch diary, see what changed. This is the *temporal* claim discharged into experimental method.

## The agent's wiki as a second instance of the pattern

[[experiment-chess]] also runs its own parallel LLM wiki for the agent's chess knowledge — openings, patterns, endgames, game-analyses. This is the [[karpathy2025wiki]] pattern instantiated a second time, in a second domain, with the agent itself as the maintainer rather than the human. If the pattern transfers, that is a second data point for the thesis claim that compiled-synthesis knowledge bases are a viable data-layer architecture. If it doesn't transfer cleanly, the failure mode is itself informative about the pattern's preconditions.

---
*Framing drawn from `../../manuscript-notes/essay-pointer.md` (Essay/essay.tex §3.1, §3.5).*
