---
type: concept
sources: [sequoia2026karpathy, kalai2024hallucinate, aizawa2025tools, matarazzo2025survey, lin2022truthfulqa]
related_concepts: [calibration-thread, tools-component, framework-four-components, agent-infrastructure-vs-capability, skills-component]
related_work: [experiment-math, experiment-riksantikvaren, experiment-chess]
status: draft
updated: 2026-06-20
---

# Deterministic-Tools Hypothesis

**Hypothesis.** For any sub-task with a verifiable correct answer, deterministic tools outperform inference, and the productive role of inference is choosing which deterministic tool to apply rather than performing the operation itself.

## The cases

- A calculator beats mental arithmetic.
- A spell-checker beats proofreading from memory.
- A test runner beats reasoning about whether a test would pass.
- A chess engine beats inferring a move from positional intuition alone.
- An authoritative-source API beats recalling a historical fact.

## Relation to Karpathy's verifiable-boundary framing

Karpathy [[sequoia2026karpathy]] frames traditional computers as automating what can be *specified*, and language models as automating what can be *verified*. This hypothesis pushes past that: within the verifiable boundary, deterministic tools still beat inference. The verifiable region is where inference is most usefully replaced, not where inference is most usefully deployed.

## Why this is structural to the framework, not incidental

A deterministic tool does not just verify the model's belief against external state; it *replaces* the belief with computation against external state. Other infrastructure (skills, workspaces, retrieval) narrows the gap between belief and verification. Deterministic tools collapse it. The hypothesis is therefore what [[calibration-thread]] predicts at the limit, where the externalised step is the answer rather than a check on it.

This connects directly to [[kalai2024hallucinate]]: if a calibrated model is structurally bound to hallucinate at the rate of singleton facts, then for any sub-task answerable by external computation, the productive design move is to externalise the computation rather than improve the model.

## Empirical anchors

- **The LLM-modulo framework** ([[matarazzo2025survey]] §4.4.5, drawing on Kambhampati et al.): vanilla LLMs solve only 28–59% of Blocksworld planning problems; under back-prompting from VAL (a deterministic plan validator) Blocksworld reaches **82% in 15 iterations**, Logistics 70%, and travel planning improves 6× over baseline. The pattern: *LLM as System 1 idea generator + deterministic verifier as System 2*. This is the deterministic-tools hypothesis operationalised in the planning domain.
- **TruthfulQA's WebGPT result** ([[lin2022truthfulqa]] Appendix B.3): retrieval-augmented browsing pushes truthfulness from ~21% (GPT-3 default) to ~75%, a larger lift than any scaling intervention on the same benchmark. The browser is functioning as a partially-deterministic verifier (the page either says what the agent claims or it doesn't).
- **Anthropic's tool-evaluation loop** ([[aizawa2025tools]]): the central design framing is *"tools are a new kind of software which reflects a contract between deterministic systems and non-deterministic agents."* The hypothesis is operationalised in production agent design.
- **The chess basic-mate boundary** ([[experiment-chess]], 2026-06-20; see [[decisions/2026-06-20-defer-minor-piece-mates]]): a refinement observed at the *skill* layer rather than the engine-during-play layer. A fair *mechanics* tool — a deterministic geometric potential ("shrink this confinement box / region") that states facts without naming the move — lets even the weak base model (internal Elo ~700–800) convert K+R, K+Q, K+2R and all over-material mates. But it provably **cannot** be built for the two minimal minor-piece mates (K+2B, K+B+N): region-, corner-, and king-march-dominant potentials all fail to mate under depth-4 search against optimal defense, and a tool computing the exact Delétang/W-manoeuvre move would be a banned engine. So K+B+N marks the threshold where a fair tool stops substituting for capability and only a full engine (Config 3) or genuine model skill suffices — the hypothesis's boundary made concrete at the sub-task level.

## Design implication

If the hypothesis holds, orchestration capacity should be reserved for inference, and any sub-task reducible to a deterministic operation should be reduced. The boundary becomes the question worth getting right: which sub-tasks have verifiable answers, and which do not?

## Where it is tested

The hypothesis is testable at three points across the experiments:

- [[experiment-riksantikvaren]] — inference vs. deterministic Askeladden API on factual heritage questions.
- [[experiment-math]] — inference vs. coding sandbox on math problems with externally checkable answers.
- [[experiment-chess]] — inference and learned skills vs. chess-engine API as an upper-bound deterministic strong-play tool.

If the hypothesis holds, the gap between inference and the deterministic configuration should be the largest one observed in each experiment, and calibration should improve monotonically with how cleanly the configuration externalises verification. If it fails in any of the three, the failure mode tells the thesis where the verifiable boundary itself is fuzzier than the hypothesis assumes — that is itself a contribution to the framework.

## Keeping the engine-during-play boundary clean

In [[experiment-chess]] the three configurations are designed so that the engine is *only* present in Config 3, and only at play time. Stockfish is still allowed as a *post-game* analysis tool for Configs 1 and 2 — feeding the agent's learning loop, contributing to the skill library — but not invocable during a move. This separation matters: if the engine were available during play in Configs 1 or 2 (even indirectly, e.g. a cached evaluation table), the deterministic-tool contribution would leak into the skill-library contribution, and the gap between Configs 2 and 3 (the hypothesis's most direct test) would collapse. The tool-fairness rulebook in [[experiment-chess]] formalises this constraint. See also [[skills-component]] for the related question of corpus boundaries on retrieval tools.

## Comparison via shared opponents, not head-to-head

The Phase 2 tournament structure in [[experiment-chess]] does not run Config-vs-Config matches; it runs each configuration as a gauntlet against a shared pool of calibrated opponents, computes an internal Elo per configuration against the shared pool, and ranks them. This preserves the gap measurements (1→2 and 2→3) that the hypothesis predicts, under matched conditions, and is methodologically necessary given the white-only training constraint. The cost is that direct head-to-head wins between configurations are not measured; the gain is that the comparison is controlled.

---
*Framing drawn from `../../manuscript-notes/essay-pointer.md` (Essay/essay.tex §1, §3.2, §3.7, §6).*
