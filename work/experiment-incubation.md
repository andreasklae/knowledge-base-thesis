---
type: experiment
status: planning
related_concepts: [incubation-as-infrastructure, workspace-component, context-engineering, calibration-thread]
related_work: [interview-erfan-analysis]
sources: [wallas1926art, sio2009incubation]
updated: 2026-05-13
---

# Experiment: Incubation Intervention

Exercises the **Sleep** chapter. Estimated effort: ~2 weeks. The most speculative experiment in the thesis and the one with the highest potential novelty — no published work yet measures incubation as agent infrastructure.

## Hypothesis

Coding agents run on bug-fix or implementation tasks accumulate fixation: long debugging trajectories where user and model jointly stabilise the wrong problem formulation (see [[incubation-as-infrastructure]]). An intervention that strips working context back to goal-plus-summary and prompts for meta-level review should measurably improve task success when applied at the point of fixation — beyond what context cleanup alone provides.

## Task source

Bug-fix or implementation tasks drawn from existing failure trajectories on a SWE-bench-style benchmark, where the baseline-no-intervention condition is known to fail or stall. Using *known-failing* trajectories sharpens the test: success in the intervention condition is unambiguous evidence that something other than the model's first-pass behaviour produced the rescue.

## Three conditions

At a fixed turn count corresponding to the empirical fixation point:

1. **No intervention.** Full original context continued unchanged.
2. **Context cleanup only.** Context stripped to goal-plus-summary, normal continuation prompt.
3. **Cleanup + meta-review prompt.** Context stripped to goal-plus-summary, with an explicit meta-review prompt asking whether the problem is being framed correctly.

Condition 2 is the critical control. Without it, any positive result for condition 3 would be attributable to context length alone rather than to incubation. With condition 2 in place, the difference between 2 and 3 isolates the meta-review effect.

## Measures

- **Rescue rate.** Of known-failing trajectories, what fraction does each condition rescue?
- **Turns-to-solution after intervention.** Conditional on rescue, how fast?
- **Qualitative coding.** Does the post-intervention response identify a meta-issue the pre-intervention conversation missed? This is the directional test of [[incubation-as-infrastructure]]'s mechanism claim.

## Why this is a workspace-component experiment

The intervention is a manipulation of session state — a [[workspace-component]] move. The agent has no biological need for sleep, but removal from active context is a workspace operation, and it can be triggered, parallelised, and repeated in ways biology does not permit. The intervention is also a [[context-engineering]] move: re-curating what enters the finite attention budget at the moment fixation has degraded the budget's value.

## Calibration role

A fixated agent reports high confidence on the wrong framing. The intervention is a calibration intervention as much as a correctness one — see [[calibration-thread]].

## Open design questions

- The fixation-point definition. Possibilities: fixed turn count, fixed token count, declining proposal novelty, repeated tool calls, token-level repetition. Empirical pilot work needed before locking this in.
- Summary generation. Who or what produces the goal-plus-summary that condition 2 and 3 start from? If the same model that fixated, there is a confound. If a separate model, the experiment is partly testing model-to-model context handoff.
- Meta-review prompt phrasing. Specific wording matters; pilot work to settle.

## Substrate-independent extensions (out of scope for this experiment)

Parallel side-process exploration of adjacent framings; fixation-triggered (vs. scheduled) intervention; returning with multiple reframings and picking. These are flagged in [[incubation-as-infrastructure]] and reserved for follow-up work.

## Connection to practitioner observation

Erfan Nariman's account (see [[interview-erfan-analysis]]) of the XY problem in AI-assisted programming motivates the intervention design and is treated as inspirational, not evidential. See [[../decisions/2026-05-13-methodology-design-science.md]].

---
*Lifted from `../manuscript-notes/essay-pointer.md` (Essay/essay.tex §3.6, §4.2-Experiment 6).*
