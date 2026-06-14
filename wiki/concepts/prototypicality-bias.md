---
type: concept
sources: [lin2022truthfulqa, kalai2024hallucinate, sofroniew2026emotions]
related_concepts: [tools-component, calibration-thread, framework-four-components, data-component]
related_work: [experiment-vision-landmarks]
status: draft
updated: 2026-05-15
---

# Prototypicality Bias in Vision-Language Models

**Claim (preliminary, from pilot work).** Vision-language models exhibit a recurring failure mode on long-tailed domains: when a photograph matches a familiar architectural or visual style, the model defaults to the most famous instance of that style rather than to the correct, less-famous target.

A Gothic cathedral in Tallinn gets identified as Notre-Dame. A modernist concert hall in Reykjavik gets identified as a more famous building in the same style. The model has a strong prior over the *style* and a weak prior over the *long tail* of instances.

## Why this matters for the framework

The failure is the kind that infrastructure rather than retraining can fix. If a tool constrains the candidate set — e.g. GPS reverse-geocoding to a geographic region, plus a landmark-lookup database — the prototypicality default no longer has free rein. See [[tools-component]].

This is the calibration thread under perception. The model reports high confidence on the prototype answer; the correct calibrated response is often "this is a Gothic cathedral, but I can't identify which specific one from this angle." Tool-constrained candidate sets convert that into a checkable claim. See [[calibration-thread]].

## Bench design

[[experiment-vision-landmarks]] is annotated for both accuracy and calibration. Each image is tagged with the realistic difficulty of identification, including cases where the correct answer is a confident "cannot determine." By construction this makes the benchmark implicitly a *calibration* benchmark, not just an accuracy benchmark — a property few public landmark datasets have.

## Status

The bias claim is from pilot observation, not from a published paper. No specific citation in the essay; the structural conjecture is original to the thesis. Once the experiment runs and the failure mode is characterised quantitatively, this page can advance from `status: draft` toward `stable`.

## Related published findings

- [[lin2022truthfulqa]]'s **imitative falsehoods** are the same phenomenon in a different modality: the model defaults to the high-prior answer (a popular misconception, a famous instance) when that answer has higher likelihood on the training distribution than the correct one. TruthfulQA's *inverse scaling* finding — larger models are *more* likely to produce imitative falsehoods — predicts the same shape for vision: larger VLMs may be *more*, not less, susceptible to prototypicality bias on long-tail buildings.
- [[kalai2024hallucinate]] gives the theoretical lower bound: at the rate of singleton training facts, calibrated models *must* default to high-prior alternatives. Prototypicality bias in vision is the visual instantiation.
- [[sofroniew2026emotions]] shows that some output biases have *readable internal signatures* (e.g. sycophancy correlates with positive-valence vector activation). Whether prototypicality bias has a similar internal signature in vision-language models is an open question worth raising — if so, the intervention surface widens beyond candidate-set constraints.

---
*Framing drawn from `../../manuscript-notes/essay-pointer.md` (Essay/essay.tex §3.4).*
