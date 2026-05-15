# Thesis Chapter Outline

The thesis is structured around the four-component framework. The Framework chapter establishes the vocabulary; five chapters then exercise it.

| Chapter | What it does | Component(s) exercised | Experiments |
|---|---|---|---|
| **Framework** | Establishes the four-part decomposition (workspace / tools / skills / data) as a working vocabulary another researcher can use to describe a new agent system. Introduces the two cross-cutting threads: calibration as a systems property, and the deterministic-tools hypothesis. | — | — |
| **Tools** | Tests the deterministic-tools hypothesis on domains with verifiable answers. Engages the MCP-vs-skills integration-spectrum question. | Tools | [experiment-riksantikvaren](../work/experiment-riksantikvaren.md), [experiment-math](../work/experiment-math.md) |
| **Skills** | Tests skills as a separable contribution to productivity. Both the static "loaded checklist" case (WCAG) and the dynamic "trial-and-error accumulation" case (chess phase 1). | Skills (+ Knowledge via the library) | [experiment-wcag-skill](../work/experiment-wcag-skill.md), [experiment-chess](../work/experiment-chess.md) |
| **Eyes** | Probes the tools component under perception. Prototypicality bias makes the failure mode of inference sharply visible. | Tools | [experiment-vision-landmarks](../work/experiment-vision-landmarks.md) |
| **Knowledge** | Compares retrieval architectures for a fixed corpus. Then tests skill acquisition that writes to the storage layer. | Data (+ Skills via acquisition) | [experiment-riksantikvaren](../work/experiment-riksantikvaren.md) (shared), [experiment-chess](../work/experiment-chess.md) (phase 1) |
| **Sleep** | Probes the workspace component through session-state manipulation. Tests incubation as agent infrastructure. The most exploratory chapter; potentially the most publishable. | Workspace | [experiment-incubation](../work/experiment-incubation.md) |

## Notes on chapter ordering

Eyes and Sleep are not separate components — they are applications of the framework where the corresponding failure mode is sharp enough to make the prediction testable. They earn their own chapters by the clarity of their probe, not by introducing new components.

Knowledge and Tools share the Riksantikvaren experiment; the same data supports both chapters from different angles. The same applies to Skills and Knowledge sharing the chess experiment.

## Cross-cutting threads

- **Calibration thread.** Runs through every chapter where a configuration externalises verification. See [../wiki/concepts/calibration-thread.md](../wiki/concepts/calibration-thread.md).
- **Deterministic-tools hypothesis.** Testable at three points: Riksantikvaren, math, and the chess-engine condition of chess phase 2. See [../wiki/concepts/deterministic-tools-hypothesis.md](../wiki/concepts/deterministic-tools-hypothesis.md).

## Source

`../Essay/essay.tex` §3.
