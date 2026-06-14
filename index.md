# Index

**Orientation:** [OVERVIEW.md](OVERVIEW.md) — what the thesis argues, the four-component framework, the six experiments, and a cold-start reading order. Read it first if you're new to the project.

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

**Grey literature (blog / tutorial)**
- [mirko2026gemma](wiki/literature/mirko2026gemma.md) — Gemma 4 + Pydantic AI structured output; `NativeOutput` + constrained decoding as the fix for unreliable Gemma tool calls
- [mayo2026gemma4tools](wiki/literature/mayo2026gemma4tools.md) — from-scratch Gemma 4 tool-calling loop (filesystem + Python sandbox); paired with Google's official chat-template notebook

## Concepts

- [agent-infrastructure-vs-capability](wiki/concepts/agent-infrastructure-vs-capability.md) — the "wrong question": infrastructure dominates capability for production behaviour
- [framework-four-components](wiki/concepts/framework-four-components.md) — workspace / tools / skills / data as affordances
  - [workspace-component](wiki/concepts/workspace-component.md)
  - [tools-component](wiki/concepts/tools-component.md)
  - [skills-component](wiki/concepts/skills-component.md)
  - [data-component](wiki/concepts/data-component.md)
- [calibration-thread](wiki/concepts/calibration-thread.md) — calibration as a systems property; verification mechanism
- [deterministic-tools-hypothesis](wiki/concepts/deterministic-tools-hypothesis.md) — the limit case of the calibration mechanism
- [mcp-vs-skills](wiki/concepts/mcp-vs-skills.md) — integration spectrum: vendor-published interface vs. local module; state/knowledge split; "ship with the skill" pattern
- [capability-delivery-dimensions](wiki/concepts/capability-delivery-dimensions.md) — six independent axes (invocation format, transport, state ownership, context economics, packaging, determinism); HCI analogues; three-party interface structure
- [context-engineering](wiki/concepts/context-engineering.md) — curating the finite attention budget
- [incubation-as-infrastructure](wiki/concepts/incubation-as-infrastructure.md) — cognitive function during pauses, re-implemented for agents
- [prototypicality-bias](wiki/concepts/prototypicality-bias.md) — vision-language models defaulting to the famous instance of a style
- [distributed-cognition](wiki/concepts/distributed-cognition.md) — Simon / Hutchins / Norman intellectual lineage
- [learning-as-temporal-dimension](wiki/concepts/learning-as-temporal-dimension.md) — learning is how the four components grow over time
  - [skill-acquisition-loop](wiki/concepts/skill-acquisition-loop.md) — the self-correcting loop in experiment-chess: play → analyse → synthesise → batch
  - [tool-fairness](wiki/concepts/tool-fairness.md) — which tools the agent may use during chess play without contaminating the experimental comparison

**Infrastructure**
- [ex3](wiki/concepts/ex3.md) — eX3 HPC cluster at Simula; GPU partitions, Slurm workflow, storage layout, known gotchas for LLM workloads
- [gemma4-vllm-pydantic-ai-integration](wiki/concepts/gemma4-vllm-pydantic-ai-integration.md) — three-layer tool-call stack; Gemma's native format vs OpenAI wire format; vLLM chat template mechanics; pydantic-ai profile mismatches; thinking channel handling; known issues and fixes

## Work

### Experiments

- [experiment-riksantikvaren](work/experiment-riksantikvaren.md) — four-configuration Askeladden study (Tools + Knowledge)
- [experiment-wcag-skill](work/experiment-wcag-skill.md) — WCAG audit no-skill vs. skill (Skills)
- [experiment-math](work/experiment-math.md) — math three-configuration (Tools)
- [experiment-vision-landmarks](work/experiment-vision-landmarks.md) — 211-image landmark threefold (Eyes)
- [experiment-chess](work/experiment-chess.md) — skill-acquisition trajectory + frozen-library tournament (Skills + Knowledge)
- [experiment-incubation](work/experiment-incubation.md) — fixation-point three-condition intervention (Sleep)

### Modules

- [module-skillful-agent](work/module-skillful-agent.md) — the agent harness (pydantic-ai SDK with progressive skill disclosure); skills-as-typed-tools, the shared apparatus all agent experiments run on
- [module-llm-server](work/module-llm-server.md) — self-hosted vLLM inference on eX3; working Gemma 4 31B-it config, SSH tunnel procedure, capacity notes

### Interviews (analysis)

- [interview-erfan-analysis](work/interview-erfan-analysis.md)
- [interview-karpathy-analysis-1](work/interview-karpathy-analysis-1.md)
- [interview-karpathy-analysis-2](work/interview-karpathy-analysis-2.md)

## Decisions

**Project-wide**
- [2026-05-13 methodology: design science](decisions/2026-05-13-methodology-design-science.md)
- [2026-05-13 framework committed at extended-description stage](decisions/2026-05-13-framework-committed-in-extended-description.md)
- [2026-05-13 vendor choice: Anthropic; exclude state-constrained models](decisions/2026-05-13-vendor-choice-anthropic.md)
- [2026-05-14 three-zone ownership model for the knowledge base](decisions/2026-05-14-three-zone-ownership-model.md)

**Infrastructure**
- [2026-05-23 eX3 LLM inference server: architecture and access pattern](decisions/2026-05-23-ex3-llm-inference-server-architecture.md)
- [2026-06-01 pydantic-ai OpenAIModelProfile for vLLM/Gemma 4](decisions/2026-06-01-pydantic-ai-vllm-profile.md)
- [2026-06-01 typed-tool harness: skill scripts as native tools](decisions/2026-06-01-typed-tool-harness-spec.md)

**experiment-chess — methodology**
- [2026-05-20 ELO tracking, batch runner, and game provenance](decisions/2026-05-20-elo-and-batch-runner.md)
- [2026-05-24 reasoning must precede the move, not follow it](decisions/2026-05-24-reason-before-move.md)
- [2026-05-24 per-turn fresh context for the chess agent](decisions/2026-05-24-per-turn-fresh-context.md)
- [2026-05-24 ranked vs experimental games (PR-as-version logging)](decisions/2026-05-24-ranked-vs-experimental.md)
- [2026-05-25 initial agent ELO 1200](decisions/2026-05-25-initial-elo-1200.md) — supersedes [2026-05-24 initial ELO 600](decisions/2026-05-24-initial-elo-600.md)
- [2026-05-25 move cap 150 half-moves + consecutive-draw batch halt](decisions/2026-05-25-move-cap-and-draw-halt.md)
- [2026-05-25 raise chess.com pool floor to 700; archive prior ranked games](decisions/2026-05-25-chesscom-pool-floor.md)
- [2026-05-25 agent resigns when it cannot commit a move; infra errors still abort](decisions/2026-05-25-agent-resigns-when-stuck.md)
- [2026-05-26 agent-authored turn memory (`--reasoning` carry-forward)](decisions/2026-05-26-agent-turn-memory.md)
- [2026-05-26 single-step opponent selection (supersedes the 05-20 doubling rule)](decisions/2026-05-26-single-step-matchmaking.md)
- [2026-05-27 `run_script` args as `list[str]` (supersedes the shell-string contract)](decisions/2026-05-27-run-script-args-list.md)
- [2026-05-27 single-writer move-commit contract (`/agent-commit` validates, bot loop pushes)](decisions/2026-05-27-single-writer-move-contract.md)
- [2026-06-02 tool-fairness rulebook (mechanics always; retrieval iff agent-curated; engines post-game only)](decisions/2026-06-02-tool-fairness-rulebook.md)
- [2026-06-02 chess agent's knowledge wiki: architecture and seeding strategy](decisions/2026-06-02-chess-agent-wiki-architecture.md)

**experiment-chess — milestones**
- [2026-05-25 bare-model baseline calibration complete (ELO ≤ 700, recorded 684.2)](decisions/2026-05-25-baseline-calibration-complete.md)
- [2026-05-25 perception tools + skill/system-prompt rewrite (first post-baseline configuration)](decisions/2026-05-25-perception-tools-and-skill-rewrite.md)
- [2026-05-26 stabilization pass on the perception-tool configuration](decisions/2026-05-26-stabilization.md)

## Discussions

Extended dialogues and reflections dropped by the user into `raw/discussions/`. These are working material, not citable sources. Each entry notes what it fed into the concept layer.

- [Claude Conversation on tools, mcp and skills](raw/discussions/Claude%20Conversation%20on%20tools,%20mcp%20and%20skills.md) — MCP transport model, tool-calling mechanics, skill architecture, six-axis decomposition of capability delivery, chess-app design reasoning, the "missing synthesis layer" observation. Produced: updated [[mcp-vs-skills]], new [[capability-delivery-dimensions]], new idea in `admin/ideas.md`.

## Manuscript notes

- [thesis-chapter-outline](manuscript-notes/thesis-chapter-outline.md)
- [thesis-timeline](manuscript-notes/thesis-timeline.md)
- [risk-register](manuscript-notes/risk-register.md)
- [scope-and-limitations](manuscript-notes/scope-and-limitations.md)
- [open-questions-future-work](manuscript-notes/open-questions-future-work.md)
- [extended-project-description](manuscript-notes/extended-project-description.md) — UiO's template for the extended description
- [essay-pointer](manuscript-notes/essay-pointer.md) — pointer to the extended project description (`../Essay/essay.tex`)
