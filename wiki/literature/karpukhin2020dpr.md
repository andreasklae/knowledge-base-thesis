---
type: literature
citekey: karpukhin2020dpr
title: Dense Passage Retrieval for Open-Domain Question Answering
authors: [Karpukhin, Vladimir, Oguz, Barlas, Min, Sewon, Lewis, Patrick, Wu, Ledell, Edunov, Sergey, Chen, Danqi, Yih, Wen-tau]
year: 2020
venue: EMNLP 2020 (arXiv:2004.04906)
raw_path: raw/literature/Karpukhin(2020).pdf
related_concepts: [data-component, tools-component, deterministic-tools-hypothesis, context-engineering]
related_work: []
status: summarized
ingested: 2026-05-14
updated: 2026-05-15
---

# Karpukhin et al. (2020) — Dense Passage Retrieval for Open-Domain Question Answering

## Summary

Karpukhin and colleagues introduce **Dense Passage Retrieval (DPR)**: a dual-encoder retrieval system that learns a dense embedding for both questions and Wikipedia passages, and retrieves the top-k closest passages by inner-product (MIPS via FAISS). The headline contribution: with the **right training scheme** (in-batch negatives + one BM25 hard negative), simply fine-tuning two BERT encoders on existing question-passage pairs **outperforms BM25 by 9-19 absolute percentage points on top-20 retrieval accuracy**, and **does not require expensive specialised pretraining** (which ORQA had previously needed). DPR is the retrieval foundation that [[lewis2020rag]] builds RAG on, and is the canonical reference for *dense* retrieval in modern LLM stacks. Released 2020; widely deployed in industry.

## Main claims

### Architectural simplicity wins

- **Dual-encoder, BERT-base, [CLS] vector, dot product.** Two independent BERT-base networks (uncased), 768-d output, inner-product similarity. No cross-attention (which would prevent pre-computing the passage index).
- **Inference via FAISS.** Pre-compute all 21M passage embeddings, store in FAISS HNSW index, retrieve top-k in sublinear time. **~995 questions/second** on a single Intel Xeon CPU + memory machine — comparable to BM25 (23.7/sec/thread) in real-world settings but with much better accuracy.
- **No specialised pretraining needed** (unlike ORQA's Inverse Cloze Task). The headline result: with the right training, vanilla BERT is enough.

### The right training is the contribution

The paper's real contribution is the training scheme:

1. **In-batch negatives.** With batch size B, each question's positive passage doubles as a negative for the other B-1 questions in the batch. This gives B² training pairs per batch essentially for free. Top-20 accuracy: ~73% with 7 gold negatives (no in-batch) → 83% with 127 in-batch negatives.
2. **One hard BM25 negative per question** (passage that scores high on BM25 but does not contain the answer) — adds 5+ percentage points on top of in-batch negatives. The single BM25 hard negative is enough; adding a second hurts.
3. **Loss:** negative log-likelihood of the positive passage among in-batch alternatives (cross-entropy over similarity scores).

### Empirical results

- **Retrieval (Top-20 accuracy):**
  - Natural Questions: BM25 59.1% → DPR 78.4%
  - TriviaQA: 66.9% → 79.4%
  - WebQuestions: 55.0% → 73.2%
  - TREC: 70.9% → 79.8%
  - **SQuAD: 68.8% → 63.2** (DPR loses — see Tensions)
- **End-to-end QA (Exact Match):** new SOTA on multiple benchmarks (NQ 41.5, TriviaQA 56.8, WQ 42.4, TREC 49.4 in Multi-dataset setting).
- **Sample efficiency:** with only **1,000 training examples** DPR already outperforms BM25 on NQ. The pretrained BERT base does most of the work.

### When BM25 still wins

SQuAD: DPR loses to BM25 (63.2 vs 68.8 top-20). Two reasons (paper, p. 5):
1. **High lexical overlap** between SQuAD questions and source paragraphs — annotators wrote questions after reading the passage.
2. **500+ Wikipedia articles only** — biased training distribution.

Qualitatively (Appendix C, Table 7): DPR is better when the answer requires *semantic matching* ("bad guy" → "villain"), BM25 is better when the answer hinges on a *rare salient phrase* ("Thoros of Myr") that has no semantic neighbours. **Combining them (BM25 + DPR linear combination) is often the best move.**

### Cross-dataset generalisation

DPR trained on NQ generalises to WQ and TREC with only 3-5 point drop, still beating BM25 by 15+ points. This suggests DPR captures *general* query-passage semantic matching, not just NQ-specific patterns.

## Method / evidence

- **Datasets:** Natural Questions, TriviaQA, WebQuestions, CuratedTREC, SQuAD v1.1.
- **Corpus:** English Wikipedia Dec 2018 dump, split into 100-word non-overlapping passages → 21M passages.
- **Encoders:** BERT-base uncased, two independent copies (one for questions, one for passages).
- **Training:** batch size 128, learning rate 1e-5, Adam, linear schedule with warmup, dropout 0.1, 40 epochs (large datasets) or 100 (small datasets).
- **Reader (for end-to-end QA):** separate BERT-base extractive reader with cross-attention; selects passage and extracts span.

## Relevance to this thesis

### 1. Empirical foundation for retrieval as an infrastructure component

The thesis's [[data-component]] / [[tools-component]] argument is that the model should not memorise everything — retrieval moves facts out of parameters and into a queryable index. DPR is the canonical empirical demonstration that this works at scale. The thesis can cite Karpukhin et al. as the *implementation foundation* for this design.

### 2. The escape hatch from Kalai's lower bound

[[kalai2024hallucinate]] proves that calibrated LMs must hallucinate at the monofact rate for arbitrary facts. The paper explicitly identifies retrieval (RAG, citing Borgeaud 2022) as the way out: move the fact outside the LM's parametric distribution. **DPR is the retrieval implementation that makes this escape route real.** The thesis can present Kalai → Lewis/Karpukhin as the theoretical motivation and concrete implementation respectively.

### 3. Hybrid sparse + dense is the right default

The BM25 + DPR linear combination is often the best in the paper's experiments. This is a thesis-relevant design principle: **deterministic tools (sparse retrieval, exact match) and learned tools (dense retrieval, semantic matching) are complementary, not competing.** See [[deterministic-tools-hypothesis]] for the broader pattern.

### 4. The 1000-example sample efficiency claim

The finding that 1k training pairs suffices is operationally important. For domain-specific applications (where the thesis's experiments often live), this means you don't need massive QA datasets to train a useful retriever. Domain-specific DPR is feasible with realistic annotation budgets.

### 5. Pre-computability via decomposable similarity

The paper's design constraint — "the similarity function needs to be decomposable so that the representations of the collection of passages can be pre-computed" — is the architectural reason DPR uses dot product over cross-attention. This is a general infrastructure principle: **pre-computation is what makes retrieval at 21M-passage scale feasible.** The thesis can use this as a concrete instance of how infrastructure constraints shape model architecture.

## Notable concepts introduced

- **In-batch negatives** — reuse other questions' positives as negatives. Memory-efficient way to increase effective batch size to B².
- **Hard negatives** — BM25-scored, answer-free passages. One per batch is enough.
- **Decomposable similarity** — required for offline indexing; trades expressivity for precomputability.
- **The DPR architecture** — dual BERT-base, [CLS] vectors, inner product, FAISS HNSW. Now the de facto baseline.
- **Sample efficiency of dense retrieval** — 1k examples enough.

## Concept-page reconciliation

1. **`wiki/concepts/data-component.md`** should cite Karpukhin et al. as the canonical implementation of retrieval-as-data-component. Currently the page is likely abstract; this is the concrete instantiation.
2. **`wiki/concepts/tools-component.md`** — retrieval is a tool the agent invokes. DPR is the canonical retrieval tool.
3. **`wiki/concepts/deterministic-tools-hypothesis.md`** — Karpukhin's BM25 + DPR combination is direct evidence that deterministic (BM25) and learned (DPR) retrieval are complementary. The deterministic-tools page should note this hybrid finding.
4. **`wiki/concepts/context-engineering.md`** — what to put in context is partly a retrieval question; DPR is one mechanism.

## Tensions and qualifications

- **No multi-hop reasoning.** DPR retrieves passages for *one* question. Multi-hop questions (where the answer requires combining passages) are not its strength. Subsequent work (e.g., MDR, ColBERT, ANCE) extends this.
- **Wikipedia is the corpus assumption.** DPR is trained on Wikipedia-style text. Out-of-domain retrieval (code, scientific papers, conversational logs) may require domain-specific training.
- **Top-k accuracy != end-to-end accuracy.** The thesis should be careful: high retrieval accuracy is necessary but not sufficient. The reader/generator still has to use the retrieved passages well.
- **FAISS HNSW is approximate.** The retrieval is exact only at the embedding level; the index is approximate-nearest-neighbour. Trade-off between recall and latency.
- **The lexical-vs-semantic dichotomy is brittle.** The paper notes DPR fails on rare salient phrases ("Thoros of Myr"). This suggests dense retrieval is not strictly better than sparse — they have different failure modes.

## Connections

- [[lewis2020rag]] — the paper that uses DPR as the retrieval module in retrieval-augmented generation. The pair is canonical.
- [[kalai2024hallucinate]] — DPR is the empirical retrieval implementation that the thesis can cite as the escape route from Kalai's lower bound.
- [[kadavath2022know]] — Kadavath finds that P(IK) rises when relevant Wikipedia is in context. DPR is one way to *get* the relevant Wikipedia in context.
- [[anthropic2024mcp]] — MCP is the modern protocol for connecting tools to LLMs; retrieval over a custom corpus is a natural MCP server. DPR-style retrievers are the underlying mechanism.
- [[rajasekaran2025]] — DPR is the canonical *pre-inference* retrieval mechanism; Rajasekaran's just-in-time retrieval is its operational contrast. Pair as the two ends of the retrieval-target spectrum (pre-indexed semantic vectors vs. on-demand exploration via tools).
- [[lin2022truthfulqa]] — DPR underlies the retrieval component of WebGPT, which is the strongest single-system data point in Lin's benchmark (~75% truthfulness, vs ~21% for vanilla GPT-3-175B). Retrieval quality is part of the truthfulness lift.
- [[matarazzo2025survey]] — Matarazzo §4.5 surveys how DPR fits into the broader RAG evolution (Naïve → Advanced → Modular); useful for situating DPR historically.
- Concept pages: [[data-component]], [[tools-component]], [[deterministic-tools-hypothesis]], [[context-engineering]].

---
*Ingested 2026-05-14. Read in full (13 pages including appendices).*
