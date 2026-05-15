---
type: experiment
status: planning
related_concepts: [prototypicality-bias, tools-component, calibration-thread, framework-four-components]
related_work: []
sources: []
updated: 2026-05-13
---

# Experiment: Vision Landmarks Threefold

Exercises the **Eyes** chapter. Estimated effort: ~2 weeks. Pilot work has already produced the benchmark.

## Hypothesis

Vision-language models default to the most famous instance of a recognised visual or architectural style ([[prototypicality-bias]]). Providing tools that constrain the candidate set — GPS reverse-geocoding plus landmark lookups — should improve identification accuracy on long-tailed sites and, more importantly, improve calibration (more confident "cannot determine" answers where determination is genuinely not possible from the image alone).

## Benchmark

The 211-image global landmark benchmark assembled during pilot work. Covers sites across more than twenty countries. Per-image annotations include:

- the realistic difficulty of identification;
- the correct answer, including cases where the correct answer is a confident "cannot determine";
- the prototypicality trap, where applicable (which famous instance the bias would default to).

By construction the benchmark is implicitly a calibration benchmark rather than just an accuracy benchmark — see [[../wiki/concepts/prototypicality-bias.md]] and [[../wiki/concepts/calibration-thread.md]]. Few public landmark datasets are designed this way; flagged as future-work contribution in [[../manuscript-notes/open-questions-future-work.md]].

## Configurations

1. **Image alone.** Model sees only the photograph in the prompt.
2. **Image + GPS.** Photograph plus GPS coordinates in the prompt.
3. **Image + GPS + tools.** Adds tools for reverse geocoding and landmark lookups within a geographic radius — see [[tools-component]].

## Measures

- **Identification accuracy** across configurations and per-image-difficulty bin.
- **Calibration.** Per-image: did the model express appropriate confidence? Did it surface "cannot determine" where the annotation calls for it?
- **Prototypicality-bias rate.** When the bias is annotated as the obvious trap, how often does each configuration fall into it?
- **Effect size by difficulty.** Easy sites (highly distinctive landmarks) should already be solved by configuration 1; the test is what configurations 2 and 3 do for the long tail.

## Open design questions

- How to handle images whose GPS metadata is genuinely informative for identification (a photograph of a generic-looking building at a known address) vs. images where GPS is uninformative.
- Whether to add an explicit prompt encouraging the model to say "cannot determine" or to let that emerge from the configuration.

## Why this experiment

A sharp probe of [[tools-component]] under a setting where the calibration thread is especially visible: prototypicality bias makes the failure mode of inference — high confidence on the wrong answer — particularly clean to measure.

---
*Lifted from `../manuscript-notes/essay-pointer.md` (Essay/essay.tex §3.4, §4.2-Experiment 4).*
