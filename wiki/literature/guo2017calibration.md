---
type: literature
citekey: guo2017calibration
title: On Calibration of Modern Neural Networks
authors: [Guo, Chuan, Pleiss, Geoff, Sun, Yu, Weinberger, Kilian Q.]
year: 2017
venue: ICML 2017 (PMLR 70)
raw_path: raw/literature/Guo(2017).pdf
related_concepts: [calibration-thread, learning-as-temporal-dimension, prototypicality-bias]
related_work: []
status: summarized
ingested: 2026-05-14
updated: 2026-05-16
---

# Guo et al. (2017) — On Calibration of Modern Neural Networks

## Summary

Guo, Pleiss, Sun, and Weinberger demonstrate empirically that **modern (post-2015) deep neural networks are systematically miscalibrated** — they are overconfident, in contrast to 2005-era networks (Niculescu-Mizil & Caruana) which were well-calibrated. The miscalibration grows with model capacity (depth and width), is exacerbated by Batch Normalization, and is worsened by reduced weight decay. The paper introduces / popularises **Expected Calibration Error (ECE)** as a scalar metric and **temperature scaling** as a one-parameter post-hoc fix that is surprisingly effective. Temperature scaling preserves accuracy (it doesn't change argmax) and on most datasets reduces ECE by an order of magnitude. This is the canonical modern reference on neural network calibration, predating LLM-specific calibration work by several years and providing the conceptual machinery (ECE, reliability diagrams, temperature scaling) that the LLM literature then inherits.

## Main claims

### Modern networks are miscalibrated and the miscalibration has a specific signature

- LeNet (1998, 5 layers, CIFAR-100): average confidence ≈ accuracy. Well-calibrated. ECE small.
- ResNet (2016, 110 layers, CIFAR-100): average confidence substantially > accuracy. Overconfident. ECE = 16.53%.
- This pattern holds across **convolutional networks (with and without skip connections), recurrent networks (TreeLSTMs), and deep averaging networks (DANs)**. Typical ECE ranges 4–10% on miscalibrated models.

### Four architectural/training factors drive miscalibration

1. **Depth.** Deeper ResNets on CIFAR-100 have higher ECE despite lower error. Increasing depth from ~10 to ~110 layers raises ECE from ~0.05 to ~0.20.
2. **Width.** Same pattern: more filters per layer → lower error but higher ECE.
3. **Batch Normalization.** Networks with BatchNorm show *worse* calibration than the same network without it, even when BatchNorm improves accuracy. This finding is robust to learning rate variation.
4. **Reduced weight decay.** Less L2 regularization → better generalisation but worse calibration. The optimum of accuracy is reached *before* the optimum of calibration; if you keep increasing weight decay past the accuracy optimum, calibration continues to improve.

### NLL/0-1 loss disconnect explains miscalibration

The training-curve evidence (Figure 3): after the learning rate drop at epoch 250, test 0/1 error continues to fall (29% → 27%), but test NLL *rises*. The network is **overfitting to NLL without overfitting to 0/1 loss**. Concretely: once the model can correctly classify training samples, additional capacity is used to inflate the *confidence* of the correct prediction, which lowers training NLL but does not change training accuracy. This overfitting shows up at test time as higher confidence on correct *and* incorrect predictions, hence higher ECE. The paper frames this as a re-interpretation of Zhang et al. 2017's "deep networks violate generalisation theory" — they don't, but their overfitting manifests in probabilistic error rather than classification error.

### Temperature scaling is the right post-hoc fix

The paper compares several calibration methods (histogram binning, isotonic regression, BBQ, Platt scaling, vector scaling, matrix scaling, temperature scaling) across 19 dataset/model combinations. **Temperature scaling wins on most vision tasks and ties on NLP.** Temperature scaling:
- Has one parameter (T > 0): replaces softmax(z) with softmax(z/T)
- Preserves the argmax → does *not* change accuracy
- Is optimised on a held-out validation set by minimising NLL
- Has a clean information-theoretic justification (maximum entropy under a balanced-logit constraint — proved in Appendix S2)

The "surprising" finding is that the more expressive variants (vector and matrix scaling) do *worse* than the one-parameter temperature scaling, because they overfit the small validation set. The authors observe that vector scaling tends to learn a vector with nearly constant entries, suggesting **network miscalibration is intrinsically low-dimensional**.

### Concrete numbers worth remembering

- CIFAR-100, ResNet-110: ECE 16.53% → 1.26% with temperature scaling (~13× reduction)
- ImageNet, ResNet-152: ECE 5.48% → 1.86%
- 20 News, DAN-3: ECE 8.02% → 4.11%

Temperature scaling, single line of code, 10 iterations of conjugate gradient, fraction of a second. The paper's pragmatic argument is: this is so cheap and effective that there is no reason not to deploy it.

## Method / evidence

- **Empirical.** 19 dataset/model combinations spanning Caltech-UCSD Birds, Stanford Cars, ImageNet, CIFAR-10/100, SVHN (vision), 20 News, Reuters, SST Binary, SST Fine-Grained (NLP).
- **Architectures.** ResNet (with and without stochastic depth), Wide ResNet, DenseNet, LeNet, TreeLSTM, DAN.
- **Metric.** ECE with M=15 bins (a binned approximation of E[|P(Ŷ=Y | P̂=p) - p|]). Supplementary tables also report MCE (maximum calibration error) and NLL.
- **No claims about LMs.** The 2017 paper predates the LLM hallucination literature. The applicability to generative language models is by extension; Kalai & Vempala 2024 explicitly observes that token-level calibration (which is what Guo et al. would measure on a language model) is *not* the right notion for hallucination analysis, because trigram models are token-calibrated and don't hallucinate (they produce gibberish). This caveat matters for the thesis.

## Relevance to this thesis

### 1. Empirical foundation for [[calibration-thread]]

The thesis claims that calibration is a load-bearing property of model output that interacts with both hallucination (via [[kalai2024hallucinate]]) and with the trust/handoff between agent and user. Guo et al. is the canonical demonstration that **calibration is a property of the training regime, not just the architecture or the data**: large modern networks are reliably overconfident, and the fix (temperature scaling) is post-hoc, cheap, and accuracy-preserving. The thesis can cite Guo as the empirical anchor and Kalai as the theoretical anchor.

### 2. Distinction: token-level vs. semantic calibration

Guo et al. measures token-level (or rather classification-level) calibration. Kalai & Vempala argue this is the wrong notion for LM hallucination because the relationship between tokens and "facts" is many-to-one. For the thesis, this means: **Guo's evidence supports a general claim ("neural networks are miscalibrated when overparameterized and undregularized") but does not directly translate to a claim about LM hallucination.** The thesis should be careful here. The connection runs through Kalai's lower bound: if the model is *generatively* calibrated (Kalai's semantic notion), it must hallucinate; if it's classification-calibrated (Guo's notion), the implication for hallucination is indirect.

### 3. NLL overfitting → confidence inflation is the mechanism

Guo's Figure 3 (NLL overfitting after the accuracy plateau) is conceptually identical to what happens during LLM training: the model continues to push probability mass onto its predictions long after the predictions are correct. The thesis can use Guo's mechanism — "overfitting manifests in probabilistic error rather than classification error" — as the bridge between supervised classification calibration and LLM probability calibration.

### 4. Temperature scaling as a deployment hygiene baseline

For thesis experiments that report model probability outputs (e.g., a self-rated confidence signal from the model, RAG retrieval rerankers, classification heads), **temperature scaling should be the trivial baseline**. If a more elaborate calibration method doesn't beat temperature scaling, it's not contributing.

## Notable concepts introduced

- **Expected Calibration Error (ECE)** — binned approximation of expected difference between confidence and accuracy. Now the standard metric.
- **Maximum Calibration Error (MCE)** — worst-case bin gap; useful for high-stakes settings.
- **Reliability diagrams** — visualisation of accuracy vs. confidence by bin. The paper popularises these.
- **Temperature scaling** — one-parameter post-hoc calibration; softmax(z/T). The "right" method for most modern networks.
- **NLL/0-1 disconnect** — overfitting can show up in probability calibration even when 0/1 loss is still improving.
- **Calibration is low-dimensional** — vector and matrix scaling overfit; one scalar suffices.

## Concept-page reconciliation

1. **`wiki/concepts/calibration-thread.md`** should cite Guo et al. as the empirical foundation for "neural networks are systematically miscalibrated when modern". Proposed addition: a paragraph noting that miscalibration is driven by overparameterization + reduced regularization + BatchNorm, and that it manifests through NLL overfitting after the accuracy plateau.

2. **`wiki/concepts/learning-as-temporal-dimension.md`** (if it exists) — Guo's Figure 3 demonstrates that *time during training matters*: NLL gets worse while accuracy improves. There is no "best epoch" that optimises both. This is a temporal-dimension observation worth incorporating.

3. **`wiki/concepts/prototypicality-bias.md`** — Guo's overconfidence story connects: a network that has overfit NLL on the training distribution will spike probability mass on the most-prototypical option for a given input. This is the *mechanism* behind prototypicality bias.

The token vs. semantic calibration distinction (above) is important to flag in any concept page that treats Guo and Kalai as fully compatible. They measure different things.

## Tensions and qualifications

- **Pre-LLM paper.** All experiments are on supervised classification (vision, document classification). Application to language models is by analogy and requires care.
- **No causal claim about *why* depth/width/BN/weight-decay cause miscalibration.** The paper documents the correlation; the mechanism (NLL overfitting) is partial. Why BatchNorm specifically harms calibration even with controlled hyperparameters is left open.
- **Temperature scaling assumes the validation set is drawn from the same distribution as the test set.** Distribution shift breaks this. The thesis should note this when applying temperature scaling in agent settings where the input distribution at deployment differs from training.
- **Single-parameter fix may not generalise to all settings.** Reuters (DAN-3) and SST Fine-Grained do not benefit much from temperature scaling. Both have unusual properties (Reuters is already well-calibrated; SST Fine-Grained has 5 classes with semantic ordering).

## Connections

- [[kalai2024hallucinate]] — the theoretical complement: calibrated LMs *must* hallucinate. Guo gives the empirical pattern, Kalai gives the lower bound. Together they imply: post-training that reduces hallucination (per Kalai) does so by *deliberately* miscalibrating the model (per Guo's framework).
- [[kadavath2022know]] — LMs know what they know; the internal calibration signal is recoverable even if the output distribution is miscalibrated.
- Concept page [[calibration-thread]] — should treat Guo as the empirical underpinning.
- For thesis experiments: any time a model outputs a probability that downstream code uses (e.g., a retrieval reranker score, a self-assessed confidence), temperature scaling on a small held-out validation set is the trivial baseline to beat.
- [[lin2022truthfulqa]] — Guo studies *output-distribution miscalibration* in classification; Lin studies the same phenomenon for *open-ended generation*. The inverse-scaling result on TruthfulQA is what Guo's pattern looks like when projected onto a generation benchmark that probes imitative falsehoods.
- [[sofroniew2026emotions]] — Sofroniew shows post-training shifts the *internal representation* distribution; Guo shows it shifts the *output* distribution. Two views of the same training intervention from different observational stances.
- [[matarazzo2025survey]] — Matarazzo discusses hallucination as a recurring limitation without going into miscalibration mechanics; Guo is the substrate-level reference for *why* post-training degrades calibration.

---
*Ingested 2026-05-14. Read in full (14 pages including supplementary).*
