# Open Questions and Future Work

Questions flagged in the extended description as outside thesis scope but worth pursuing. Recording them now helps Phase-1 scope decisions stay disciplined.

## Framework-level

- **Cross-timescale validity.** Does the productivity-infrastructure framework hold across the session-to-session and long-term timescales? The thesis tests within-session and across-session-via-skill-library; multi-month and multi-year timescales (where the artefacts themselves evolve, the model swaps under the framework, etc.) are not covered.

## Skills and learning

- **Production deployment of the skill-acquisition mechanism.** Does the trial-and-error skill-acquisition loop tested in [experiment-chess](../work/experiment-chess.md) phase 1 generalise from research-style tasks to production deployments where the environment is open-ended, the failure cost is real, and the feedback signal is noisier?
- **Cross-domain transfer.** Whether skills accumulated in one domain (chess) produce transferable structure usable in another (an unrelated game, or non-game tasks).
- **Junior-agent apprenticeship.** What does an apprenticeship structure for a less-capable agent look like, and can a senior–junior pairing accelerate skill acquisition in measurable ways?

## Multi-agent and organisational

- **Organisational-pathology taxonomy.** Does a taxonomy of organisational pathologies (information siloing, deference cascades, coordination tax) predict multi-agent failure modes? Would importing the corresponding mitigations from organisational design produce measurable improvements? This is the multi-agent extension of the human-productivity analogy that drives the thesis.

## Benchmarks

- **The landmark benchmark as a calibration benchmark.** The 211-image landmark benchmark used in [experiment-vision-landmarks](../work/experiment-vision-landmarks.md) is implicitly a calibration benchmark by virtue of its per-image difficulty and confidence annotations. Few public landmark datasets are designed this way. The benchmark itself, properly written up, is a potential standalone contribution.

## Source

`../Essay/essay.tex` §6.
