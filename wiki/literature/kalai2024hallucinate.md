---
type: literature
citekey: kalai2024hallucinate
title: Calibrated Language Models Must Hallucinate
authors: [Kalai, Adam Tauman, Vempala, Santosh S.]
year: 2024
venue: arXiv:2311.14648 (v3, March 2024)
raw_path: raw/literature/Kalai(2024).pdf
related_concepts: [calibration-thread, deterministic-tools-hypothesis, data-component, prototypicality-bias]
related_work: []
status: summarized
ingested: 2026-05-14
updated: 2026-05-14
---

# Kalai & Vempala (2024) — Calibrated Language Models Must Hallucinate

## Summary

Kalai and Vempala prove a **statistical lower bound** on the rate at which pretrained, calibrated language models must hallucinate on "arbitrary" facts (facts whose veracity cannot be determined systematically from training data). The bound has nothing to do with transformer architecture, training data quality, or model size — it is a property of the calibration objective itself. The headline result: the probability of generating a hallucination is at least the **monofact rate** (Good-Turing estimate: the fraction of facts that appear exactly once in training) minus a miscalibration term and small additive terms. The paper reframes hallucination from "model bug" to "predictable statistical consequence of training pretrained models to be good predictors." The corollary is that **post-training (RLHF, etc.) reduces hallucination at the cost of reducing calibration** — confirmed by the GPT-4 calibration curves they reproduce (ECE rises from 0.007 to 0.074 after PPO).

## Main claims

### The lower bound (Corollary 1)

For an s-sparse regular world distribution, with probability ≥ 1 − δ over training:

$$g(H) \geq \widehat{MF} - \text{Mis}_b(g, p) - \frac{3e^{-s}}{\delta} - \sqrt{\frac{6\ln(6/\delta)}{n}}$$

where g(H) is the hallucination rate, $\widehat{MF}$ is the monofact estimator (fraction of facts appearing exactly once in training), and Mis is miscalibration. For large training sets and exponentially sparse facts (many more plausible falsehoods than facts), the bound is essentially: **hallucination rate ≥ monofact rate − miscalibration.**

### Why this matters

- The bound applies in an **idealized setting**: perfect training data (no falsehoods), one fact per document, i.i.d. sampling, no prompts, static world. Real-world conditions only make hallucination worse. The lower bound is therefore robust.
- The bound depends only on a **statistical** property of the fact distribution (the monofact rate) and a calibration property of the model. It does *not* depend on architecture, parameter count, or training algorithm. The authors are explicit (p. 1, abstract): "having nothing to do with the transformer LM architecture or data quality."
- Equivalence with trigram models is illuminating: trigram models are calibrated at the token level but generate gibberish; they don't hallucinate because their outputs aren't plausible. Modern LMs hallucinate *because they are good predictors* — they produce plausible-sounding output and calibration forces them to spread probability mass across plausible alternatives in proportion to how often each appears in training.

### Type-of-fact taxonomy

The paper sharply distinguishes:
- **Arbitrary facts** (5W = Who-Ate-What-When-Where-Why; specific citation titles): cannot be inferred from rules; only memorisable from training. The lower bound applies in full force.
- **Systematic facts** (arithmetic: 572 < 120523; deducible facts): in principle determinable by rules. The lower bound does *not* require these to be hallucinated. The authors suggest different architectures and learning algorithms may mitigate systematic-fact hallucination.
- **Citation/reference hallucinations** are interesting boundary case: each reference is published once but its title and authors appear in many places (CVs, indexes, cross-posts), so monofact rate for references is low. The paper *predicts that citation hallucinations are not statistically necessary* — they arise from capacity limits, not calibration constraints. **This is a load-bearing prediction for the thesis: it implies citation hallucinations should be fixable with retrieval (RAG) or larger models, while 5W hallucinations should not.**

### Open- vs closed-domain hallucinations

- **Open-domain**: free generation, no source document. The paper's bounds apply here.
- **Closed-domain**: hallucinations that contradict a provided source (e.g., in summarisation, translation). No statistical argument forces these. They can in principle be filtered out by verifying against the source. The authors note OpenAI 2023 found greater reduction in closed-domain hallucinations than open-domain — consistent with the theory.

### Pretraining vs post-training

The paper's reading of the GPT-4 calibration curves (Figure 1, reproduced from OpenAI 2023 Fig. 8):
- After pretraining: ECE = 0.007 (well-calibrated)
- After PPO/RLHF: ECE = 0.074 (significantly miscalibrated)

Interpretation: **post-training trades calibration for reduced hallucination.** This is consistent with the lower bound — to reduce hallucination below the monofact rate, you have to *increase* the miscalibration term. There is no way around this from inside the statistical framework.

## Method / evidence

- **Mathematical theorem.** The core result is a probability lower bound proven from first principles (Theorem 1 + corollaries). The proof uses Markov's inequality, Good-Turing missing-mass concentration (from McAllester and Ortiz 2003, Berend and Kontorovich 2013), and a "coarsening" lemma about how calibration partitions induce TV distance.
- **No experiments.** This is a theory paper. The GPT-4 calibration data is reproduced from OpenAI's GPT-4 Technical Report, not generated here.
- **Two relaxations of regularity** (r-regular-facts, r-regular-probabilities) allow the bound to extend beyond uniform distributions to power-law and 5W-with-negative-correlations cases. The 5W example is worked out in detail.
- **Matching upper bound** (Section 7): the authors give a (computationally inefficient) algorithm that is calibrated and hallucinates at exactly the monofact rate, showing the lower bound is tight.

## Relevance to this thesis

Kalai & Vempala is one of the **most load-bearing single sources** for this thesis. It provides the formal underpinning for:

### 1. The deterministic-tools hypothesis

The thesis argues that delegating tasks to deterministic tools rather than to the language model itself reduces error rates. Kalai's framework gives the rigorous version: **for arbitrary facts, no amount of LM training can avoid hallucination if calibration is preserved.** The escape route is therefore *not* a better LM — it is moving the task outside the LM. Retrieval-augmented generation (cited explicitly in the paper, Borgeaud 2022) does this for citation-style facts. Tool use, more broadly, does this for systematic facts (arithmetic via a calculator, code via execution, lookups via a database).

This must go on [[deterministic-tools-hypothesis]] explicitly as the *formal* underpinning. The current concept page does not cite Kalai.

### 2. The pretraining/post-training tension

The thesis describes a tension between pretrained models (calibrated, hallucinate-prone) and post-trained models (less hallucination, less calibrated). Kalai gives this a precise form: you cannot have both. The GPT-4 ECE numbers (0.007 → 0.074) are concrete data the thesis can cite.

### 3. Monofact rate as a design lever

The paper's monofact-rate analysis suggests a concrete intervention: **reduce the monofact rate in training by deduplication and repeated exposure for facts you want the model to retain.** The paper notes that LM corpora already deduplicate (Shen et al. 2023 SlimPajama). This is directly relevant to data-curation arguments the thesis can make on [[data-component]].

### 4. Why "agents know when they're hallucinating" is consistent

Kalai cites [[kadavath2022know]] approvingly: it is consistent with the theory that LMs can detect their own hallucinations. The theory says hallucinations *occur* at a certain rate; it does not say the model cannot *recognise* them in retrospect. This opens a thesis-level design space: an agent infrastructure that surfaces the model's own calibration as a signal (which is what self-consistency, SelfCheckGPT, and Kadavath-style probes already do).

## Notable concepts introduced

- **Monofact / MonoFacts estimator** — fraction of facts in training data that appear exactly once. Good-Turing missing-mass estimator. Directly determines minimum hallucination rate.
- **Generative calibration** — calibration of the model at the *semantic* level (over facts) rather than token level. Token-level calibration was the previous standard; the paper argues it's not the right notion for hallucination analysis (because trigram models are token-calibrated but mostly produce gibberish).
- **Arbitrary vs. systematic facts** — fundamental taxonomic distinction. Arbitrary facts require memorisation; systematic facts admit rule-based generation. The lower bound only applies to arbitrary.
- **Sparsity (s-sparse)** — there are exponentially more plausible falsehoods than facts. Captured as $|F| \leq e^{-s}|H|$.
- **r-regularity** — relaxed condition allowing for anti-correlations between facts (e.g., a person eats one lunch per day, ruling out alternatives for that meal-slot).
- **Closed-domain vs open-domain hallucinations** — useful taxonomy for the thesis when distinguishing summarisation/translation experiments from open generation experiments.

## Concept-page reconciliation

The current concept layer should be checked against Kalai. Specifically:

1. **`wiki/concepts/calibration-thread.md`** should cite Kalai as the *formal* source for the calibration-hallucination tradeoff, not just as supporting evidence. The lower bound is the precise version of what calibration-thread.md likely argues qualitatively. Proposed edit: add a section "The Kalai-Vempala lower bound" with the formula and the monofact interpretation.

2. **`wiki/concepts/deterministic-tools-hypothesis.md`** should add Kalai as the formal justification for *why* deterministic tools help: for arbitrary facts, the LM cannot avoid hallucination at the calibration boundary, so moving the task to a deterministic tool is the only escape. Proposed edit: add a paragraph "Why this works formally: Kalai & Vempala (2024) prove the LM cannot do better than the monofact rate. Deterministic tools take the fact out of the LM's distribution entirely."

3. **`wiki/concepts/data-component.md`** should note that **monofact rate is a property of the training data** and is therefore a data-curation lever, not a model-training lever. The thesis can use this to argue for deduplication and curated exposure to facts the model should retain.

4. **`wiki/concepts/prototypicality-bias.md`** intersects with Kalai in an interesting way. Kalai's regularity assumptions break down when facts are *predictable* (e.g., people who eat the same lunch every day; the paper notes "LMs might hallucinate less if there are predictable eaters"). Prototypicality biases toward the most-frequent option, which corresponds to facts whose probability is far from uniform. Worth flagging the connection.

These edits are *proposed*, not applied. The user owns concept pages.

## Tensions and qualifications

- **Idealised setting.** The paper proves a lower bound under unrealistically clean conditions. Real-world hallucination has many other causes the paper does not address (training data errors, OOD prompts, snowballing in long generations per Zhang et al. 2023b, multi-step reasoning errors). The bound is therefore *necessary* but very far from *sufficient*.
- **Semantic calibration is hard to measure.** The notion of calibration the paper uses (over facts) is more meaningful than token-level calibration but is computationally intractable to evaluate for real models. The paper notes this as a limitation (Section 9). The GPT-4 ECE numbers reproduced from OpenAI use *multiple-choice* calibration, which is a proxy.
- **Systematic facts.** The paper explicitly says systematic facts (arithmetic) need not be hallucinated. But modern LMs *do* hallucinate on arithmetic. The paper acknowledges this and pushes the explanation onto "limited model capacity" and architectural limitations. This is unsatisfying — the lower bound is silent here, and the practical phenomenon remains.
- **No prescription.** The paper is diagnostic, not prescriptive. It says calibrated models *must* hallucinate; it does not say what to do about it. The implicit recommendation is post-training (which the GPT-4 data shows reduces hallucination but breaks calibration) or retrieval-augmented generation (which moves the fact outside the LM's distribution). The thesis can be the prescriptive complement to this diagnostic.

## Connections

- [[guo2017calibration]] — the modern calibration baseline for neural networks; Kalai builds on this lineage.
- [[kadavath2022know]] — LMs know when they're hallucinating; consistent with Kalai's framework and complementary (Kalai says they *will* hallucinate; Kadavath says they can detect when they have).
- [[lewis2020rag]], [[karpukhin2020dpr]] — retrieval-augmented generation is the escape route from Kalai's bound for arbitrary facts whose verification has a non-parametric source.
- [[sofroniew2026emotions]] — separately argues for treating model internal state as observable; complements Kalai's external-statistical view with an internal-mechanistic view.
- [[lin2022truthfulqa]] — the canonical *empirical* benchmark of imitative falsehoods (the kind Kalai's bound predicts). Lin's inverse-scaling finding is the empirical signature of Kalai's lower bound: when distributional likelihood and factual truth diverge, larger models track likelihood more reliably and become *less* factual. Pair as theory + empirics.
- [[aizawa2025tools]] — Aizawa's UUIDs → semantic-identifiers result is a behavioural intervention against Kalai-style hallucination at the tool-design layer; calibrated bound is unchanged, but the surface form of the *task* is reshaped so the bound bites less.
- [[matarazzo2025survey]] — surveys hallucination as a recurring LLM limitation across the substrate; pairs as the field-overview companion to Kalai's targeted theoretical result.
- Thesis experiments: any experiment whose error mode is "model fabricates plausible-sounding wrong information" should cite this as the *floor* it cannot go below without sacrificing calibration.

---
*Ingested 2026-05-14. Read in full (28 pages including appendices).*
