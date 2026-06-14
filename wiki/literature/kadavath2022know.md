---
type: literature
citekey: kadavath2022know
title: Language Models (Mostly) Know What They Know
authors: [Kadavath, Saurav, Conerly, Tom, Askell, Amanda, Henighan, Tom, Drain, Dawn, Perez, Ethan, Schiefer, Nicholas, Hatfield-Dodds, Zac, DasSarma, Nova, Tran-Johnson, Eli, Johnston, Scott, El-Showk, Sheer, Jones, Andy, Elhage, Nelson, Hume, Tristan, Chen, Anna, Bai, Yuntao, Bowman, Sam, Fort, Stanislav, Ganguli, Deep, Hernandez, Danny, Jacobson, Josh, Kernion, Jackson, Kravec, Shauna, Lovitt, Liane, Ndousse, Kamal, Olsson, Catherine, Ringer, Sam, Amodei, Dario, Brown, Tom, Clark, Jack, Joseph, Nicholas, Mann, Ben, McCandlish, Sam, Olah, Chris, Kaplan, Jared]
year: 2022
venue: arXiv:2207.05221
raw_path: raw/literature/Kadavath(2022).pdf
related_concepts: [calibration-thread, agent-infrastructure-vs-capability, deterministic-tools-hypothesis, prototypicality-bias]
related_work: []
status: summarized
ingested: 2026-05-14
updated: 2026-05-16
---

# Kadavath et al. (2022) — Language Models (Mostly) Know What They Know

## Summary

Anthropic's foundational study of whether large language models can evaluate their own knowledge. The paper makes three connected claims: (1) **large LMs are well-calibrated** on diverse multiple choice questions when formatted appropriately (e.g., MMLU, BIG Bench, TruthfulQA, QuALITY, LogiQA), with calibration improving with model size and few-shot prompting; (2) **LMs can self-evaluate** their own free-form generations by producing P(True) — the probability that a sample is correct — with reasonable calibration when few-shot prompted, and this self-evaluation improves further when the model sees multiple T=1 samples for the same question before judging one (analogous to self-consistency); (3) LMs can be **finetuned to predict P(IK)** — the probability that *they* will answer a question correctly — which generalises partially across tasks and *increases appropriately* when relevant source materials or hints are added to context. The work is the empirical underpinning for Anthropic's "honesty" research agenda (truthfulness + calibration + self-knowledge + explainability + non-deceptiveness) and the implicit theoretical complement to [[kalai2024hallucinate]].

## Main claims

### Calibration on multiple choice (Sections 2-3)

- **Format matters.** With visible lettered choices (A/B/C) and answer identified only by label, the 52B model produces **ECE ≈ 0.01–0.05** on BIG Bench, MMLU, TruthfulQA, QuALITY, LogiQA. Switching to BIG Bench's default format (where the model must write the full answer) breaks calibration substantially (ECE ~0.10+).
- **Calibration improves with model size and few-shot prompting.** Going from 800M → 52B parameters and from 0-shot → 5-shot both reduce ECE.
- **"None of the above" breaks things.** Replacing option (D) with "none of the above" significantly *degrades* both accuracy and calibration on MMLU. The model is biased *against* using this option. This breaks even 20-shot.
- **True/False format is well-calibrated.** When questions are reformulated as "Is this answer True or False?", the 52B model is very well-calibrated (Figure 8). This is the bridge to self-evaluation.

### RLHF policy miscalibration is fixed by temperature scaling (Section 3.3)

RLHF-trained policies appear *very* miscalibrated naively — RL training collapses the output distribution toward high-reward behaviours. But a single temperature adjustment (T = 2.5, the *same* value for all three evaluations they tried: MMLU, MMLU True/False, TruthfulQA) largely restores calibration. This is conceptually identical to [[guo2017calibration]]'s post-hoc temperature scaling fix, applied to RL-finetuned LMs instead of supervised classifiers.

### P(True) self-evaluation (Section 4)

The procedure:
1. Sample an answer from the model.
2. Re-prompt the model with "Question / Proposed Answer / Is the proposed answer (A) True (B) False" and read off P(True) as the probability of the (A) token.

Findings:
- **Self-evaluation works, but worse than third-party evaluation.** Models find their own samples more plausible than third-party-written ones, so P(True) sits closer to 50% than it would for human-written candidates.
- **Zero-shot P(True) is poorly calibrated**; few-shot fixes calibration without much improving discrimination. The AUROC for separating correct vs. incorrect samples is similar 0-shot and few-shot; what 20-shot mainly does is *calibrate* the probability.
- **Showing the model 5 other T=1 samples improves self-evaluation.** "Brainstorming" gives the model context for what other plausible answers look like, and helps it judge one specific sample. This is the experimental cousin of self-consistency (Wang et al. 2022 chain-of-thought self-consistency) but operates on T/F judgement rather than majority voting on final answer.
- **Verification scales faster than generation.** On TriviaQA, Codex HumanEval, GSM8k, Arithmetic, Lambada: the gap between *base accuracy* and *accuracy-conditioned-on-P(True)>0.5* grows with model size. The 52B model is much better than the 800M model at both generating *and* judging, but it improves more at judging. This is the "verification is easier than generation" claim — load-bearing for the bootstrapping-honesty programme.

### P(IK) — training models to predict "I know"

Procedure: add a value head, train (mostly on TriviaQA) to predict P(IK) = fraction of T=1 samples that are correct.

Findings:
- **In-distribution: very well calibrated** on TriviaQA (Figure 13 left).
- **OOD AUROC improves with model size**: trained on TriviaQA only, the 52B P(IK) head still discriminates correct vs. incorrect questions on Lambada, Arithmetic, Python Function Synthesis, GSM8k — with AUROC of ~0.85–0.93.
- **OOD calibration is poor.** Trained on TriviaQA only, P(IK) is systematically underconfident on other tasks. Training on all four tasks (TriviaQA + Lambada + Arithmetic + Python Function Synthesis) substantially fixes this for the four trained tasks, but generalisation to *novel* tasks (GSM8k) still degrades calibration.
- **P(IK) responds appropriately to context.** When given a Wikipedia article relevant to a question, P(IK) on that question *increases*. When given a partial hint to a GSM8k problem, P(IK) increases proportionally to the amount of hint shown. **Bad hints (chain-of-thought that leads to wrong answers) also raise P(IK)** but less than good hints. **Distracting hints (from another question) lower P(IK)**. This is non-trivial generalisation: the model was only trained on bare questions, but its P(IK) head is now functioning as a *retrieval-aware* confidence signal.
- **Cross-model experiments (Section 5.5)** with two 12B models trained on different pretraining mixes: each model assigns higher P(IK) to questions *it* (not the other model) can answer. The signal is small (~6%) but real. This is evidence that P(IK) is partly a self-knowledge signal, not just a difficulty signal.

## Method / evidence

- **Models.** 800M, 3B, 12B, 52B parameter language models trained for 850B tokens. Architecture matches Bai et al. 2022. Also a brief look at HH-RLHF policies.
- **Tasks.** All BIG Bench multiple-choice, MMLU, TruthfulQA, QuALITY, LogiQA (multiple choice); TriviaQA, Lambada, Codex HumanEval, GSM8k, custom Arithmetic, custom Python Function Synthesis (free-form generation).
- **Metrics.** ECE (10 bins, equal mass), RMS calibration error, Brier score, AUROC.
- **P(IK) training.** Value head; for each question generate 30 T=1 samples, label each as IK or IDK based on correctness, train with cross-entropy. Batch size 7680, learning rate 1/3 of pretraining. Note: this is *finetuning the whole model along with the value head*, not just a probe.
- **Negative result on "natural language" P(IK).** Tried having the model output P(IK) as text ("0%, 10%, 20%, ..., 100%"). Did not see major gains, defaulted to value head. Mentioned as worth revisiting.

## Relevance to this thesis

### 1. Empirical complement to [[kalai2024hallucinate]]

Kalai proves that calibrated LMs *must* hallucinate at a rate ≥ monofact rate. Kadavath shows that LMs *can detect when they have hallucinated*, after the fact, via P(True) self-evaluation. These are perfectly consistent: the lower bound says hallucinations occur with some frequency; Kadavath says the model has access to its own confidence signal. The combination opens a thesis-level design space: **infrastructure that surfaces the model's own P(True) or P(IK) signal can do useful filtering even though the model itself cannot avoid hallucinating.**

This is *exactly* the kind of agent-infrastructure intervention the thesis argues for. [[agent-infrastructure-vs-capability]] concept page should cite Kadavath as the empirical foundation for "the capability is already there; what's missing is infrastructure that uses it."

### 2. Verification > generation as a design principle

The finding that self-evaluation accuracy scales faster than generation accuracy is one of the most thesis-relevant claims in the paper. It justifies a class of agent designs: **let the model generate, then let the model judge.** This is the architectural pattern behind self-consistency (Wang 2022), best-of-N sampling with a verifier, and the more general "agent generates → tool verifies" pattern.

The thesis can use Kadavath as the empirical anchor for this claim and Kalai as the theoretical anchor for *why* verification is needed (the generator cannot avoid hallucinating).

### 3. P(IK) generalises to source materials

The finding that **P(IK) increases when relevant Wikipedia is in context, even though the head was never trained to do this**, is a startling generalisation result. It suggests that the model's internal "do I know this?" representation is *already* contextually sensitive — adding sources makes the model "know more" in a way the P(IK) head picks up. For the thesis's [[data-component]] argument, this is direct evidence that **putting the right data in context** doesn't just change the answer; it changes the model's confidence signal in a way you can read off externally.

### 4. RLHF temperature fix as a deployment pattern

The single-temperature fix for RLHF miscalibration is concretely useful for the thesis: any post-training step that improves an agent's behaviour likely degrades calibration; a one-parameter temperature scan on a small validation set fixes it. This should go on [[calibration-thread]] as a deployment hygiene note.

### 5. Distinguishing self-knowledge from difficulty

The cross-model experiments (Section 5.5) try to distinguish "P(IK) captures what I specifically know" from "P(IK) captures how hard the question is." The results are mixed but lean toward genuine self-knowledge. For the thesis, this matters because: **if P(IK) is genuinely self-referential**, then agents can in principle learn calibrated abstention or hedging in ways that *depend on their own training history*. If it's just task-difficulty, the signal is much weaker.

## Notable concepts introduced

- **P(True)** — model's probability that its own sample is correct. Externally accessible via re-prompting; no finetuning needed.
- **P(IK)** — model's probability that it can answer a question correctly. Requires finetuning a value head.
- **"Show many T=1 samples"** — improves self-evaluation by giving the model context for what plausible answers look like. Conceptual relative of self-consistency.
- **Honesty taxonomy** — truthfulness, calibration, self-knowledge, explainability, non-deceptiveness. Useful framing for thesis discussions of trust between agent and user.
- **OOD calibration vs OOD AUROC dissociation** — discriminative power generalises better than calibration. A signal that's useful but uncalibrated may still be useful with thresholding.
- **RLHF temperature fix** — single T parameter remediates most RLHF miscalibration on the evaluations tried.

## Concept-page reconciliation

1. **`wiki/concepts/calibration-thread.md`** should cite Kadavath as the demonstration that *base* LMs (pre-RLHF) are well-calibrated when prompted in the right format, and that calibration improves with scale and few-shot. The RLHF temperature fix is a concrete deployment recommendation.

2. **`wiki/concepts/agent-infrastructure-vs-capability.md`** — Kadavath is direct evidence for the thesis's headline claim. The *capability* to detect hallucinations is already in the model (P(True) AUROC ~ 0.8). The *infrastructure* to surface, threshold, and route on that signal is the missing piece. Proposed addition: a paragraph that says "Kadavath et al. show large LMs can self-evaluate at AUROC ~0.8. The thesis argues this signal goes unused in current agent infrastructure."

3. **`wiki/concepts/deterministic-tools-hypothesis.md`** — relevant indirectly. If the model can self-evaluate, then "verify by tool" can be combined with "verify by self" to get a better composite signal. The deterministic-tools page should note Kadavath as enabling a hybrid verification architecture.

4. **`wiki/concepts/prototypicality-bias.md`** — the multiple-choice format calibration story has an interesting connection. The reason "none of the above" breaks calibration is plausibly that it's *atypical* as an answer position — the model has learned strong priors about A/B/C/D distributions and (D)="none" violates that prior. This is prototypicality bias manifesting in calibration.

5. **`wiki/concepts/context-engineering.md`** — the P(IK)-with-Wikipedia finding is direct evidence that context-engineering changes not just answers but *confidence signals*. Worth surfacing.

## Tensions and qualifications

- **Anthropic models only.** All experiments use Anthropic's 800M–52B series. The results are likely to replicate on other large LMs but no external replication is in the paper.
- **Pure language models, not deployed agents.** Section 6.1 explicitly flags that RLHF-finetuned policies are not as well-calibrated, and that some methods may not transfer. The thesis should be careful when extending these results to agent settings.
- **The honesty/deception distinction is not addressed.** The paper studies whether models *can* report their confidence; it does not study whether models trained against rewards might *strategically* misreport. The thesis's safety-related framings should note this gap.
- **"Knows what" ≠ "Knows that".** P(IK) is trained on whether a sample at T=1 is correct. This is statistical knowledge, not propositional knowledge. The paper is careful here; the thesis should be too.
- **GSM8k OOD performance is much weaker.** Even after training on 4 tasks, GSM8k AUROC is only 0.75. The generalisation story is real but not complete.

## Connections

- [[kalai2024hallucinate]] — Kalai's lower bound + Kadavath's self-evaluation are the canonical theoretical + empirical pair for the thesis's calibration arguments. Kalai cites Kadavath approvingly.
- [[guo2017calibration]] — Kadavath's temperature fix for RLHF is the same idea as Guo's temperature fix for modern CNNs, applied to a different miscalibration source.
- [[lewis2020rag]], [[karpukhin2020dpr]] — RAG and Kadavath's P(IK)-with-Wikipedia finding align: providing source material both changes the answer and the confidence signal. The thesis can connect these as two sides of the same retrieval-augmented infrastructure.
- [[sofroniew2026emotions]] — internal-representation view of model state; complementary to Kadavath's external (P(True)/P(IK)) view.
- [[lin2022truthfulqa]] — TruthfulQA's findings (models confidently produce imitative falsehoods) are seemingly in tension with Kadavath (models know what they don't know). The resolution: Kadavath measures *introspective* signals available to the model; Lin measures the *output* that prompting actually surfaces. Infrastructure (helpful prompts, RLHF, retrieval) is what bridges the gap.
- Concept pages: [[calibration-thread]], [[agent-infrastructure-vs-capability]], [[context-engineering]], [[data-component]].

---
*Ingested 2026-05-14. Read in full (43 pages including all appendices).*
