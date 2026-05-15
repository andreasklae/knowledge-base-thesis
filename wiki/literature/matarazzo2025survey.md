---
type: literature
citekey: matarazzo2025survey
title: A Survey on Large Language Models with some Insights on their Capabilities and Limitations
authors: [Matarazzo, Andrea, Torlone, Riccardo]
year: 2025
venue: arXiv preprint (Expedia Group / Roma Tre University)
raw_path: raw/literature/Matarazzo(2025).pdf
related_concepts: [calibration-thread, framework-four-components, agent-infrastructure-vs-capability, deterministic-tools-hypothesis, data-component]
related_work: []
status: summarized
ingested: 2026-05-15
updated: 2026-05-15
---

# Matarazzo & Torlone (2025) — A Survey on Large Language Models with some Insights on their Capabilities and Limitations

## Summary

A comprehensive ~150-page survey by Andrea Matarazzo (Expedia Group) and Riccardo Torlone (Roma Tre) covering the **foundations, scaling laws, architectures, applications, and limitations of Large Language Models** as of mid-2025. The survey is structured in six sections: (1) introduction; (2) LLM definitions, scaling laws, prominent families (BERT, T5, GPT, LLaMA, Gemma, Claude), and specialised domain LLMs (healthcare, finance, education, law, science); (3) foundations — pre-training, data sources/preprocessing, instruction/alignment tuning, transformer architecture, PEFT; (4) utilisation strategies — in-context learning, chain-of-thought, program-of-thoughts, planning, LLM-modulo frameworks, RAG; (5) original empirical contribution — *testing CoT capabilities on Llama-family models on GSM8k/gsm-hard*, with the central finding that **CoT capability is driven by code-in-pre-training-data, not by model size**; (6) conclusions emphasising hallucination, planning weakness, and the need for hybrid systems (LLM + verifiers + retrieval). For the thesis, this is the **comprehensive technical reference** for the LLM substrate beneath the agent infrastructure layer — useful primarily as a citation surface for technical claims rather than as a source of novel arguments.

## Main claims

### 1. Scaling laws and their limits

- **KM scaling law (Kaplan et al. 2020):** model performance L scales as power laws of model size N, dataset size D, and compute C.
- **Chinchilla scaling law (Hoffmann et al. 2022):** different exponents; *compute-optimal training* requires balancing N and D — many earlier models were under-trained for their size.
- Scaling laws explain why bigger-with-more-data works, but **don't address sustainability**: computational and environmental costs become prohibitive; future work must elicit emergent abilities without excessive compute.

### 2. Emergent abilities — three canonical examples

Wei et al.'s definition: *"Emergence is when quantitative changes in a system result in qualitative changes in behaviour."*
1. **In-context learning** (ICL) — model learns from examples in the prompt with no gradient updates. *"Seemingly a mismatch between pretraining (next-token prediction) and in-context learning."* Dai et al. argue ICL implicitly performs meta-optimisation via attention.
2. **Instruction following** — appears at ~62B+ parameters (LaMDA-PT, PaLM). Smaller models don't generalise from instruction tuning.
3. **Step-by-step reasoning (CoT)** — CoT prompting gains appear with >60B parameters for some tasks; the survey's own experiments (§5) show that *size is not deciding — pre-training data is*.

### 3. The four-stage history of language models

Matarazzo structures the field into four eras:
1. **Statistical LMs** (n-gram, Markov assumption).
2. **Neural LMs** (RNN, LSTM, word2vec).
3. **Pre-trained LMs** (ELMo, BERT, GPT-2, T5). *"Pre-train and fine-tune"* paradigm.
4. **Large LMs** (transformer-based, billions to trillions of parameters; emergent abilities).
- (Plus a fifth, *Small Language Models* — pruning, quantization, knowledge distillation for edge deployment.)

### 4. Section 5 — empirical CoT investigation (the original contribution)

The survey's most distinctive contribution. The authors run experiments on Llama-family models with LMStudio on HuggingFace, testing GSM8k and gsm-hard with CoT and Program-of-Thought (PoT) prompts. The conclusion:
- **CoT capability is correlated with code in the pre-training data mix, not with model size.**
- Small Llama models trained on code mixes can produce CoT-style reasoning; large models without strong code mixes underperform on CoT.
- This challenges the *naive scaling story* — emergent abilities have *substantive* prerequisites (data composition), not just *capacity* prerequisites.

### 5. LLM-modulo framework — the planning-with-external-verifier pattern

Section 4.4.5, drawing on Kambhampati et al.: **LLMs are not effective planners or self-verifiers in isolation**. The LLM-modulo framework integrates:
- **LLM as idea generator** (System 1, fast/intuitive).
- **External critics** (hard constraints: VAL, unit tests; soft constraints: style, preferences).
- **Reformulator** (LLM converts plans into formats critics can evaluate).
- **Meta (Backprompt) Controller** coordinating LLM + critics.

Empirical: on PlanBench, vanilla LLMs solve ~28-59% on Blocksworld (best Claude-3-Opus zero-shot at 59.3%) and only ~0-2.5% on Mystery BW (obfuscated). With LLM-modulo back-prompting from VAL, Blocks World hits 82% in 15 iterations; Logistics 70%. Travel-planning improves from 0.7% baseline to ~4.2% (6×). The paper makes Kambhampati's *"LLMs are System 1, not System 2"* argument explicit.

### 6. RAG — three paradigms

Section 4.5 surveys RAG evolution:
- **Naïve RAG** — index → retrieve → read. Effective but suffers from retrieval precision and generation accuracy issues.
- **Advanced RAG** — pre-retrieval (query rewriting, expansion) + post-retrieval (re-ranking, compression) optimisations.
- **Modular RAG** — orchestrates Search / RAGFusion / Memory / Routing / Predict / Task Adapter modules. Supports flexible interaction patterns (Rewrite-Retrieve-Read, Generate-Read, etc.).

### 7. Limitations and future work

The conclusion section frames LLMs as having:
- **Hallucination** — plausible-but-wrong outputs, especially risky in medicine/law.
- **Reasoning/planning gaps** — repetitive token generation under standard sampling; cannot independently verify their own solutions.
- **Ethical concerns** — bias, environmental cost, misuse potential.

Recommended directions:
- Parameter-efficient fine-tuning, specialised domain adaptation.
- Integration of external knowledge sources and tools (essentially the agent-infrastructure thesis).
- Interdisciplinary work with cognitive science and linguistics.

### 8. Specialised LLMs by domain (Section 2.4)

Survey-style coverage of:
- **Healthcare**: Med-PaLM, ClinicalBERT, BioMedLM — clinical decision support, diagnostics.
- **Finance**: FinGPT, BloombergGPT — sentiment, market prediction, risk.
- **Education**: tutoring, content generation.
- **Law**: contract analysis, case summarisation.
- **Scientific research**: literature review assistance, code generation.

These are useful as citation sources for thesis claims about LLM applicability but largely descriptive.

## Method / evidence

- **Survey style** — heavy on synthesis of prior literature, light on novel claims except for §5 (CoT experiments).
- **Original empirical work** (§5) is genuine but limited to Llama-family models on GSM8k/gsm-hard. Specific numbers and configurations are reported but the experiments are not adversarial-design controlled.
- Authority rests on comprehensive citation breadth (~400 references) and clear hierarchical structure rather than on novel results.
- The §5 experiment is the most distinctive contribution; the rest is a textbook-style synthesis.

## Relevance to this thesis

### 1. Citation surface for LLM substrate claims

The thesis sits *on top* of the LLM substrate. Matarazzo provides the *technical reference* the thesis can cite for substrate-level claims:
- Scaling law citations (Kaplan, Chinchilla).
- Transformer architecture details.
- Pre-training/fine-tuning/RLHF taxonomy.
- Emergent ability literature (Wei et al.).

The thesis doesn't need to re-derive these; Matarazzo is the convenient one-stop reference.

### 2. CoT-driven-by-code finding supports the data-component argument

The survey's §5 finding — *CoT capability is determined by pre-training data composition, not by model size* — is direct support for the thesis's [[data-component]] argument writ large. **Even at the substrate (training-data) level, data determines capability.** Pair with [[lin2022truthfulqa]] (imitative falsehoods are data-determined) and [[lewis2020rag]] (retrieval lifts factuality).

### 3. LLM-modulo framework is the deterministic-tools hypothesis in plan-form

Section 4.4.5 is essentially **a planning-domain instantiation of the thesis's [[deterministic-tools-hypothesis]]**: the LLM generates candidate solutions (non-deterministic, intuitive); external verifiers (deterministic, formal) accept or reject. The 0.7% → 4.2% travel-planning improvement is a concrete operational metric. Cite as direct evidence: *"hybrid systems with formal verifiers outperform LLM-alone."*

### 4. The Kahneman System 1 / System 2 framing is operationally useful

Matarazzo (via Kambhampati): *"LLMs are akin to Kahneman's 'System 1' — fast, intuitive, and associative, but not capable of the deliberate, logical thinking attributed to 'System 2'."*

This is a useful framing for the thesis: **agent infrastructure provides System 2 — deterministic verifiers, structured workspace, persistent memory, retrieval — bolted onto System 1 LLMs.** Pair with [[wallas1926art]]'s stages of thought (preparation/incubation/illumination/verification) — the LLM is fast pattern completion; the infrastructure is the deliberation surrounding it.

### 5. Hallucination + planning gaps + System 1/System 2 = the thesis problem statement

The survey's conclusion section essentially *states the thesis problem*:
- Hallucination is real and unsolved by scaling.
- Reasoning/planning is weak in pure LLMs.
- External knowledge sources and tools are needed.

Matarazzo's recommended directions explicitly endorse the infrastructure-around-the-model approach. The thesis can cite this as **industry/academic consensus that the agent-infrastructure approach is the right direction**, not a niche position.

### 6. Modular RAG vocabulary aligns with the four-component framework

Modular RAG's modules (Search, Memory, Routing, Predict, Task Adapter) overlap substantially with the thesis's framework components. Pairing both is useful:
- Search Module + Memory ↔ [[data-component]].
- Routing + Task Adapter ↔ [[skills-component]] + [[tools-component]].
- The orchestration pattern itself ↔ [[workspace-component]].

### 7. Small Language Models section is thesis-adjacent

SLMs (pruning, quantization, distillation) are relevant for *deployment* arguments but tangential to the thesis's main framework. Worth a brief acknowledgement — *infrastructure matters for SLMs too, perhaps more so given their reduced capacity*.

## Notable concepts introduced (or canonically articulated)

- **Scaling laws** (KM and Chinchilla variants) — formal expressions for performance vs N, D, C.
- **Emergent abilities** triad — ICL, instruction following, step-by-step reasoning.
- **CoT-by-code hypothesis** — pre-training data mix drives CoT, not size.
- **LLM-modulo framework** — LLM + critics + reformulator + meta-controller.
- **System 1 vs System 2 framing** for LLM limits.
- **Three RAG paradigms** — Naïve, Advanced, Modular.
- **Pre-train + fine-tune + align** as the canonical lifecycle.

## Concept-page reconciliation

1. **`wiki/concepts/data-component.md`** — Matarazzo's §5 CoT-driven-by-code result is direct support for *data composition determines capability* even at substrate level. Cite alongside [[lin2022truthfulqa]] and [[lewis2020rag]].
2. **`wiki/concepts/deterministic-tools-hypothesis.md`** — LLM-modulo framework is the planning-domain operational form of this hypothesis. Add citation with Blocksworld 28% → 82% numbers.
3. **`wiki/concepts/agent-infrastructure-vs-capability.md`** — Matarazzo's conclusion explicitly endorses external-knowledge / hybrid-system direction. Useful as "field consensus" citation.
4. **`wiki/concepts/calibration-thread.md`** — Matarazzo's hallucination discussion (§6) is consistent with [[kalai2024hallucinate]] and [[lin2022truthfulqa]] but not novel. Worth citing for completeness.
5. **`wiki/concepts/framework-four-components.md`** — Modular RAG's module taxonomy is a near-parallel to the four-component framework. Useful comparative reference; **disclose** that some thesis readers may want to compare.

## Tensions and qualifications

- **Survey-style.** Most content is recapitulation of prior work; novel claims are limited to §5.
- **§5 experiment is preliminary.** Llama-family only; GSM8k/gsm-hard only; not a controlled adversarial design like [[lin2022truthfulqa]]. The "CoT driven by code" finding is suggestive, not definitive.
- **No agent / MCP coverage.** Matarazzo treats LLMs largely as monolithic models with peripheral tools (RAG, LLM-modulo). Agent harnesses, MCP, multi-turn workspaces aren't deeply addressed. The thesis fills this gap.
- **Heavy reliance on Kambhampati's planning critique.** §4.4.5 leans on Kambhampati et al. for the System 1/System 2 framing; that line of argument is contested (Wei et al.'s emergent-abilities literature treats CoT as genuine reasoning).
- **Author affiliations.** Industry (Expedia) and academic (Roma Tre) co-authorship gives the survey a balanced but not deeply researched character. Not peer-reviewed in a journal venue.
- **Some redundancy with earlier surveys.** Zhao et al. 2023 ("A Survey of Large Language Models") covers much of the same ground; Matarazzo updates and slightly extends but doesn't fundamentally re-frame.
- **English-only focus.** Multilingual aspects barely addressed.
- **Limited coverage of post-2024 frontier developments.** Tool use, agents, multi-agent systems, reasoning-as-RL (o1/o3-style) get cursory treatment compared to the foundational chapters.

## Connections

- [[lin2022truthfulqa]] — Matarazzo's hallucination discussion is consistent; Lin provides the canonical benchmark.
- [[kalai2024hallucinate]] — theoretical lower bound on hallucination; complements Matarazzo's empirical observations.
- [[lewis2020rag]] — RAG canonical reference; Matarazzo §4.5 surveys evolutions.
- [[rajasekaran2025]] — context engineering for agents; Matarazzo's "external knowledge integration" recommendation maps directly.
- [[anthropic2024mcp]] — MCP is the protocol layer Matarazzo glosses; tools-and-verifiers Matarazzo describes are MCP-shaped in practice.
- [[krishnan2025multiagent]] — multi-agent on MCP; Matarazzo doesn't deeply engage with multi-agent but sets the substrate.
- [[wallas1926art]] — stages of thought; pairs with System 1/System 2 framing.
- [[karpukhin2020dpr]] — DPR underlies RAG retrieval components Matarazzo describes.
- [[guo2017calibration]] — calibration substrate; Matarazzo discusses hallucination but not calibration directly.
- Concept pages: [[data-component]], [[deterministic-tools-hypothesis]], [[agent-infrastructure-vs-capability]], [[calibration-thread]], [[framework-four-components]].

---
*Ingested 2026-05-15. Converted via docling, read selectively (Introduction, Section 2.1-2.2 overview, Section 4.4.5 LLM-modulo, Section 4.5 RAG, Section 6 Conclusions). Full 4032-line markdown conversion read in samples; deleted after synthesis per workflow.*
