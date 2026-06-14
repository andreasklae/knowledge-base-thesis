---
type: experiment
status: planning
related_concepts: [tools-component, data-component, deterministic-tools-hypothesis, calibration-thread, framework-four-components]
related_work: [experiment-math, experiment-chess]
sources: [anthropic2024mcp, lewis2020rag, karpukhin2020dpr, karpathy2025wiki, kalai2024hallucinate]
updated: 2026-05-16
---

# Experiment: Riksantikvaren Four-Configuration Study

Exercises the **Tools** and **Knowledge** chapters. Estimated effort: 3–4 weeks. Pilot work has already produced the heritage-agent prototype this experiment builds on (engineering on it as a polished product ends after May 2026).

## Hypotheses

Two, jointly.

1. **Deterministic tools.** On factual heritage questions, the configuration with the Askeladden API as a deterministic tool produces the largest accuracy and calibration gain over inference-only. See [[deterministic-tools-hypothesis]].
2. **Calibration improves with externalised verification.** Calibration improves monotonically across the four configurations in the order: inference-only → LLM-wiki summary → RAG → direct API. See [[calibration-thread]].

## Corpus

The Askeladden register (Riksantikvaren's Norwegian heritage register). Convenient because it is:

- structured enough for direct query (API);
- document-rich enough for retrieval-augmented generation;
- small enough to be summarised into an LLM-wiki style compilation.

The shared corpus makes the comparisons clean: configurations differ only in how knowledge reaches the model.

## Configurations

1. **Inference-only.** Model answers from parametric knowledge alone.
2. **API tool.** Model has access to the Askeladden API as a tool. Maps to [[tools-component]] and is the direct test of [[deterministic-tools-hypothesis]].
3. **RAG.** Retrieval-augmented generation over the document set with vector embeddings ([[lewis2020rag]], [[karpukhin2020dpr]]).
4. **LLM-wiki summary.** A persistent compiled summary in the style of [[karpathy2025wiki]].

See [[data-component]] for the broader architecture comparison.

## Question set

A single fixed set of factual questions about Norwegian heritage sites. The same set is run against all four configurations.

## Measures

- **Answer accuracy.** Compared against authoritative answers derived from the register.
- **Calibration.** Reported confidence vs. realised accuracy across the question set.
- **Confident-hallucination rate.** Specifically tracked in the inference-only condition — the test case for [[kalai2024hallucinate]]'s structural prediction.
- **Efficiency frontier.** Setup cost, per-query token use, per-query latency.

## Open design questions

- Question-set construction: difficulty stratification; how to avoid questions trivially answerable from the model's training data; whether to include questions whose answer is "this is not in the register."
- For RAG: chunk size, embedding model, top-k, reranking.
- For the LLM-wiki summary: how the summary is generated and maintained (one-shot? incremental?). This is itself a design decision worth recording when made.

## Dependencies

- Pilot work on the heritage-agent prototype (already done).
- Frozen Askeladden snapshot to guard against post-snapshot API changes (see [[risk-register]]).

## Cross-references

- Also serves the [[data-component]] retrieval-architecture comparison; shared work with the Knowledge chapter.
- Companion test of [[deterministic-tools-hypothesis]]: [[experiment-math]] and [[experiment-chess]].

---
*Lifted from `../manuscript-notes/essay-pointer.md` (Essay/essay.tex §3.2, §3.5, §4.2-Experiment 1).*
