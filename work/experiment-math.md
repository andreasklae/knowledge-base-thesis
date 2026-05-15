---
type: experiment
status: planning
related_concepts: [deterministic-tools-hypothesis, tools-component, skills-component, calibration-thread]
related_work: [experiment-riksantikvaren, experiment-chess]
sources: [sequoia2026karpathy]
updated: 2026-05-13
---

# Experiment: Math Three-Configuration

Exercises the **Tools** chapter. Estimated effort: ~1 week.

## Hypothesis

[[deterministic-tools-hypothesis]] on a domain where calibration is canonical: replacing inference with executable computation should produce the largest accuracy and calibration gain. Specifically, the gap between inference-only and coding-sandbox conditions should be large and monotonic, with the skills-and-tools condition sitting in between (procedural knowledge that helps but does not replace the operation).

## Configurations

1. **Inference-only.** Model reasons through math problems in natural language.
2. **Inference with skills and tools.** Model has access to skills providing relevant procedural knowledge (factoring patterns, identity tables, solver heuristics) plus tools for symbolic manipulation but no general-purpose code execution.
3. **Coding sandbox.** Model can write and execute Python with `sympy`, `numpy`, etc. — verifiable computation against external state.

Configuration 3 is the deterministic-tools limit case (see [[deterministic-tools-hypothesis]]): the externalised step is itself the answer rather than a check on it. Configuration 2 separates the contribution of procedural knowledge ([[skills-component]]) from the contribution of execution ([[tools-component]]).

## Benchmark

An existing math benchmark selected at experiment start. Selection criteria: problems with externally checkable answers, range of difficulty, public availability for reproducibility. Candidates include MATH, GSM8K, MATH-500, and similar.

## Measures

- **Accuracy** across configurations and difficulty bins.
- **Calibration.** Reported confidence vs. realised accuracy.
- **Difficulty-gap relationship.** The inference-vs-tools gap as a function of problem difficulty. The structural prediction is that the gap widens with difficulty: easy problems are answerable by inference; hard problems require execution. Where the gap saturates or inverts is the location of the verifiable-boundary edge.

## Why math specifically

Math is the canonical case for the deterministic-tools argument: every step has a verifiable correct answer, calibration is well-defined, and execution is cheap and reliable. If the hypothesis fails here, it is unlikely to hold anywhere.

Karpathy's framing in [[sequoia2026karpathy]] — traditional computers automate what can be specified, language models automate what can be verified — is operationalised directly: math has both, so the experiment is partly about which axis dominates within the verifiable region.

## Open design questions

- Whether to enforce a chain-of-thought structure in conditions 1 and 2 for comparability.
- For condition 3: whether the sandbox is invoked freely or only after the model commits to a problem decomposition.
- How to score partial credit (or whether to).

---
*Lifted from `../manuscript-notes/essay-pointer.md` (Essay/essay.tex §3.2, §4.2-Experiment 3).*
