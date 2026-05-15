---
type: decision
status: accepted
---

# Primary AI Vendor: Anthropic; Exclude State-Constrained Models

## Context

The choice of AI vendor is not neutral. Vendors differ on autonomous weapons, mass surveillance, military contracts, alignment-research investment, and on whether their model outputs are shaped by state-mandated content controls. For a thesis on AI infrastructure whose threads include calibration, grounding, and honest treatment of evidence, the vendor choice has methodological consequences, not just commercial ones. Every payment to a vendor also signals validation of their practices.

## Decision

**Primary vendor: Anthropic.** Models from Anthropic (Claude family) are the default for all experimental work.

**Excluded: Chinese frontier models under state-mandated content controls.** This includes DeepSeek, Qwen, GLM, and any other model whose provider is bound by China's Interim Measures for the Management of Generative Artificial Intelligence Services (in force 15 August 2023), which require providers to ensure outputs uphold "Core Socialist Values." The exclusion is structural, not geopolitical: a thesis grounded in honest treatment of evidence cannot rely on a tool whose evidence selection is mandated by parties external to the research. The principle generalises to any jurisdiction that imposes ideological constraints on model outputs.

## Rationale

Two strands.

**Ethical posture.** Anthropic publicly maintains acceptable-use restrictions prohibiting use of its models for fully autonomous lethal weapons and mass domestic surveillance. After the US Department of War designated the company a supply-chain risk on those grounds, another major vendor reportedly filled the gap with fewer reservations (Rooprai, Reuters, 2026). Anthropic also invests in alignment research, including interpretability work that makes safety-relevant model internals empirically tractable — for instance the emotion-concept causal study (Sofroniew et al., 2026) used as a load-bearing reference in the calibration-thread argument. This treats AI safety as a research problem rather than a marketing position.

**Methodological soundness.** Journalists have documented systematic refusal on topics such as Tiananmen Square, Taiwan, and criticism of senior CCP leadership in Chinese frontier models, and statements contrary to fact where outright refusal would be conspicuous — e.g. DeepSeek's assertion that Taiwan has "always been an inalienable part of China's territory since ancient times" (Lu, *The Guardian*, January 2025). A model that deliberately lies is unacceptable for academic work and counterproductive for a thesis investigating factual retrieval, grounding, and calibration.

The objection is **not** about capability or openness — Chinese frontier models are highly capable and often open-weight, and they have meaningfully broadened access. The objection is about a specific structural property: outputs shaped by parties external to the research.

## Consequences

- All experiments report the specific Anthropic model version used. Cross-vendor comparisons are out of scope.
- Model-release effects are tracked as a risk (see [`../manuscript-notes/risk-register.md`](../manuscript-notes/risk-register.md)).
- If future work needs to compare across vendors for a specific research question, the constraint above applies to that comparison: state-constrained models are excluded.
- The thesis discusses this decision openly in the Ethical Reflections section.

## References

- Rooprai (2026), Reuters: Anthropic–Pentagon dispute over AI safeguards. `references.bib`: `rooprai2026pentagon`.
- Lu (2025), *The Guardian*: DeepSeek refusal patterns. `references.bib`: `lu2025deepseek`.
- Cyberspace Administration of China (2023): Interim Measures for the Management of Generative AI Services. `references.bib`: `cac2023interim`.
- Sofroniew et al. (2026): emotion concepts and their function in a large language model. `references.bib`: `sofroniew2026emotions`.

## Source

`../Essay/essay.tex` §5 (Ethical Reflections).
