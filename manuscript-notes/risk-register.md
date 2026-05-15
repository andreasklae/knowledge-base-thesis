# Risk Register

Four risks identified at the extended-description stage. Each has a mitigation committed to.

| Risk | Description | Mitigation |
|---|---|---|
| **API and dataset stability** | Riksantikvaren or other source APIs may change mid-thesis, invalidating earlier experimental runs. | Snapshot data early. Document any post-snapshot changes as methodological notes. Applies to [experiment-riksantikvaren](../work/experiment-riksantikvaren.md) and to any dataset-dependent experiment. |
| **Model release effects** | A frontier release in late 2026 or early 2027 may shift empirical baselines, making comparisons across the thesis non-uniform. | Record model versions used in each experiment. Treat the framework as model-agnostic. Discuss the issue explicitly in the conclusion. |
| **Experiment scope creep** | [experiment-chess](../work/experiment-chess.md) is the largest single piece of work and most likely to expand. | Define the plateau criterion for phase 1 *before starting*. Resist extending phase 2 beyond Elo measurement. |
| **Day-job integration** | Full-time employment on related problems provides additional case material with employer permission, but introduces delivery risk. | Phased timeline with regular supervisor check-ins. Treat employer-domain material as bonus, not baseline. |

## Notes

The model-release risk is real and recurring; this thesis's response is to keep the framework substance independent of any specific model and to record versions experiment by experiment. The framework should remain useful as a vocabulary even if every measurement on it shifts.

The scope-creep risk on chess is acute because phase 1 has no natural stop unless one is imposed. The plateau criterion is the stop.

## Source

`../Essay/essay.tex` §4.4.
