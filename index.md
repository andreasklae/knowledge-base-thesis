# Index

## Literature

Per-source synthesis pages. Each links back to `raw/literature/` and to the concept pages that cite it.

**Foundational classics (cognitive science, design, methodology)**
- [simon1996artificial](wiki/literature/simon1996artificial.md) — Sciences of the Artificial; inner/outer environment, bounded rationality, attention as scarce resource
- [hutchins1995wild](wiki/literature/hutchins1995wild.md) — Cognition in the Wild; distributed cognition across human + artefact + environment
- [norman2013design](wiki/literature/norman2013design.md) — Design of Everyday Things; affordances, signifiers, gulfs of execution/evaluation
- [wallas1926art](wiki/literature/wallas1926art.md) — The Art of Thought; preparation/incubation/illumination/verification
- [ericsson1993deliberate](wiki/literature/ericsson1993deliberate.md) — deliberate practice; expertise as accumulated structured training
- [sio2009incubation](wiki/literature/sio2009incubation.md) — incubation meta-analysis; effect size and moderators
- [yin2018case](wiki/literature/yin2018case.md) — Case Study Research (6th ed.); analytic generalisation, replication logic, plausible rival explanations

**Calibration / hallucination / model-internal state**
- [kalai2024hallucinate](wiki/literature/kalai2024hallucinate.md) — calibrated LMs *must* hallucinate at the monofact rate
- [guo2017calibration](wiki/literature/guo2017calibration.md) — ECE, temperature scaling, modern-NN miscalibration
- [kadavath2022know](wiki/literature/kadavath2022know.md) — P(IK), P(True), self-evaluation
- [lin2022truthfulqa](wiki/literature/lin2022truthfulqa.md) — TruthfulQA; imitative falsehoods, inverse scaling
- [sofroniew2026emotions](wiki/literature/sofroniew2026emotions.md) — emotion vectors as readable internal signal of model state

**Retrieval / data infrastructure**
- [karpukhin2020dpr](wiki/literature/karpukhin2020dpr.md) — Dense Passage Retrieval; dual-encoder, in-batch negatives, FAISS
- [lewis2020rag](wiki/literature/lewis2020rag.md) — RAG; index hot-swap demonstration

**Architecture / protocol heritage**
- [fielding2000](wiki/literature/fielding2000.md) — REST dissertation; constraints-induce-properties methodology; protocol-design ancestor of MCP

**Substrate survey**
- [matarazzo2025survey](wiki/literature/matarazzo2025survey.md) — LLM survey; scaling laws, emergent abilities, LLM-modulo, RAG paradigms

**Agent engineering (industry / Anthropic)**
- [anthropic2024mcp](wiki/literature/anthropic2024mcp.md) — Model Context Protocol; primitives (prompts/resources/tools/roots/sampling)
- [martin2026managed](wiki/literature/martin2026managed.md) — managed agents; brain/hands/session decomposition, harness/sandbox
- [krishnan2025multiagent](wiki/literature/krishnan2025multiagent.md) — multi-agent on MCP; reference 6-layer architecture
- [zhang2025](wiki/literature/zhang2025.md) — Agent Skills; progressive disclosure for procedural context
- [rajasekaran2025](wiki/literature/rajasekaran2025.md) — context engineering; just-in-time retrieval, compaction, sub-agents
- [aizawa2025tools](wiki/literature/aizawa2025tools.md) — writing effective tools; eval-driven design, namespacing, response format
- [weber2024taxonomy](wiki/literature/weber2024taxonomy.md) — LLM-component taxonomy; 13 dimensions, feature-vector visualisation

**Productivity / vision**
- [peng2023copilot](wiki/literature/peng2023copilot.md) — Copilot RCT; 55.8% faster task completion
- [karpathy2025wiki](wiki/literature/karpathy2025wiki.md) — LLM Wiki gist; raw/wiki/schema pattern, Memex with maintenance solved
- [sequoia2026karpathy](wiki/literature/sequoia2026karpathy.md) — Software 3.0, vibe coding vs agentic engineering, jagged intelligence

## Concepts

- [agent-infrastructure-vs-capability](wiki/concepts/agent-infrastructure-vs-capability.md) — the "wrong question": infrastructure dominates capability for production behaviour
- [framework-four-components](wiki/concepts/framework-four-components.md) — workspace / tools / skills / data as affordances
  - [workspace-component](wiki/concepts/workspace-component.md)
  - [tools-component](wiki/concepts/tools-component.md)
  - [skills-component](wiki/concepts/skills-component.md)
  - [data-component](wiki/concepts/data-component.md)
- [calibration-thread](wiki/concepts/calibration-thread.md) — calibration as a systems property; verification mechanism
- [deterministic-tools-hypothesis](wiki/concepts/deterministic-tools-hypothesis.md) — the limit case of the calibration mechanism
- [mcp-vs-skills](wiki/concepts/mcp-vs-skills.md) — integration spectrum: vendor-published interface vs. local module
- [context-engineering](wiki/concepts/context-engineering.md) — curating the finite attention budget
- [incubation-as-infrastructure](wiki/concepts/incubation-as-infrastructure.md) — cognitive function during pauses, re-implemented for agents
- [prototypicality-bias](wiki/concepts/prototypicality-bias.md) — vision-language models defaulting to the famous instance of a style
- [distributed-cognition](wiki/concepts/distributed-cognition.md) — Simon / Hutchins / Norman intellectual lineage
- [learning-as-temporal-dimension](wiki/concepts/learning-as-temporal-dimension.md) — learning is how the four components grow over time

## Work

### Experiments

- [experiment-riksantikvaren](work/experiment-riksantikvaren.md) — four-configuration Askeladden study (Tools + Knowledge)
- [experiment-wcag-skill](work/experiment-wcag-skill.md) — WCAG audit no-skill vs. skill (Skills)
- [experiment-math](work/experiment-math.md) — math three-configuration (Tools)
- [experiment-vision-landmarks](work/experiment-vision-landmarks.md) — 211-image landmark threefold (Eyes)
- [experiment-chess](work/experiment-chess.md) — skill-acquisition trajectory + frozen-library tournament (Skills + Knowledge)
- [experiment-incubation](work/experiment-incubation.md) — fixation-point three-condition intervention (Sleep)

### Interviews (analysis)

- [interview-erfan-analysis](work/interview-erfan-analysis.md)
- [interview-karpathy-analysis-1](work/interview-karpathy-analysis-1.md)
- [interview-karpathy-analysis-2](work/interview-karpathy-analysis-2.md)

## Decisions

- [2026-05-13 methodology: design science](decisions/2026-05-13-methodology-design-science.md)
- [2026-05-13 framework committed at extended-description stage](decisions/2026-05-13-framework-committed-in-extended-description.md)
- [2026-05-13 vendor choice: Anthropic; exclude state-constrained models](decisions/2026-05-13-vendor-choice-anthropic.md)

## Manuscript notes

- [thesis-chapter-outline](manuscript-notes/thesis-chapter-outline.md)
- [thesis-timeline](manuscript-notes/thesis-timeline.md)
- [risk-register](manuscript-notes/risk-register.md)
- [scope-and-limitations](manuscript-notes/scope-and-limitations.md)
- [open-questions-future-work](manuscript-notes/open-questions-future-work.md)
- [extended-project-description](manuscript-notes/extended-project-description.md) — UiO's template for the extended description
- [essay-pointer](manuscript-notes/essay-pointer.md) — pointer to the extended project description (`../Essay/essay.tex`)
