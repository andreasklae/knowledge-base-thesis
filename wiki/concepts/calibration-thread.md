---
type: concept
sources: [kalai2024hallucinate, guo2017calibration, kadavath2022know, sofroniew2026emotions, lin2022truthfulqa, aizawa2025tools]
related_concepts: [deterministic-tools-hypothesis, framework-four-components, workspace-component, tools-component, skills-component, data-component]
related_work: [experiment-riksantikvaren, experiment-math, experiment-vision-landmarks, experiment-chess, experiment-incubation]
status: draft
updated: 2026-05-13
---

# Calibration as a Systems Property

**Claim.** The gap between what a model claims to know and what it actually knows is partly a systems property, not a model property. Infrastructure can close gaps the model cannot close on its own.

## The mechanism

External verification of internal belief. Infrastructure improves calibration in proportion to how cleanly it externalises verification.

- **Tools** verify by execution.
- **Skills** verify by encoding procedures whose preconditions are checkable.
- **Workspaces** verify by letting actions have observable consequences.
- **Data** verify by grounding claims against external state.

Any infrastructure that does not externalise verification cleanly should not improve calibration, even if it improves accuracy. This turns the calibration thread into a per-experiment prediction rather than a recurring motif.

## The supporting literature

- [[kalai2024hallucinate]] prove that any pretrained language model satisfying a natural calibration condition must hallucinate arbitrary facts at a rate close to the fraction of facts that appear exactly once in the training data, regardless of architecture or data quality. Hallucination is a structural consequence of the training objective.
- [[guo2017calibration]] show modern neural networks are systematically miscalibrated, and that miscalibration can worsen even as classification error improves.
- [[kadavath2022know]] find that language models often have introspective access to their own reliability that they fail to surface in standard outputs.
- [[sofroniew2026emotions]] provide a mechanistic counterpart: emotion-concept representations inside Claude Sonnet 4.5 causally influence sycophantic and reward-hacking behaviour, and post-training shifts these representations in ways more visible in activation space than in output text. Miscalibration is partly a property of internal representation, not only of training data.
- [[lin2022truthfulqa]] is the canonical empirical pair to [[kalai2024hallucinate]]: TruthfulQA exhibits **inverse scaling** on imitative falsehoods — larger models are *less* truthful when distributional likelihood and factual truth diverge. The 21% → 58% lift from a "helpful" prompt on GPT-3-175B is a clean single-intervention demonstration that calibration is infrastructure-shaped, not capability-shaped.
- [[aizawa2025tools]] reports an unexpected calibration intervention at the tool layer: resolving alphanumeric UUIDs to semantically meaningful identifiers reduces Claude's retrieval hallucinations. Calibration is operating on the surface form of identifiers — tool design can route around the calibration problem by making identifiers themselves more interpretable.

## Limit case

The limit case of the mechanism is [[deterministic-tools-hypothesis]]: where verification is itself the answer rather than a check on it. The thread predicts an ordering across experiment configurations — calibration should improve monotonically with how cleanly the configuration externalises verification.

## Where it is tested

- [[experiment-riksantikvaren]] — calibration across four retrieval architectures on heritage questions.
- [[experiment-math]] — calibration shift when reasoning is replaced by execution.
- [[experiment-vision-landmarks]] — per-image calibration on a benchmark explicitly annotated for it, with confident "cannot determine" as a target answer.
- [[experiment-chess]] — calibration of move evaluation against an external strong-play oracle.
- [[experiment-incubation]] — a fixated agent reports high confidence on the wrong framing; the intervention is a calibration intervention as much as a correctness intervention.

---
*Framing drawn from `../../manuscript-notes/essay-pointer.md` (Essay/essay.tex §1, §2.3, §3.1).*
