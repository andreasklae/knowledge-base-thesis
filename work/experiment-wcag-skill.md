---
type: experiment
status: planning
related_concepts: [skills-component, framework-four-components, mcp-vs-skills]
related_work: [interview-erfan-analysis]
sources: [zhang2025]
updated: 2026-05-13
---

# Experiment: WCAG No-Skill vs. Skill

Exercises the **Skills** chapter. Estimated effort: ~1 week.

## Hypothesis

An agent equipped with a WCAG-specific skill produces accessibility audits whose issue-overlap with human-conducted audits is materially higher than the same agent with only generic web-fetch tools, without a corresponding rise in false positives. The skill encodes the kind of structured procedural knowledge a senior accessibility auditor would otherwise have to flag manually — see [[skills-component]] and the Erfan/React parallel in [[interview-erfan-analysis]].

## Configurations

1. **No-skill baseline.** Agent with generic web-fetch and HTML-inspection tools only.
2. **With WCAG skill.** Same agent equipped with a WCAG skill file in the format of [[zhang2025]], including bundled accessibility-tool scripts (axe-core or equivalent, colour-contrast checker, alt-text inspection, etc.).

## Sample

A sample of Norwegian public-sector websites for which human-conducted WCAG audits have already been published by Tilsynet for universell utforming av ikt. Number to be determined at experiment start.

## Measures

- **Issue-overlap rate.** Of issues found by human auditors, what fraction does each agent configuration recover?
- **False-positive rate.** Of issues flagged by each agent configuration, what fraction the human auditors did not include (verified manually).
- **Net-new findings.** Issues identified by the agent that human auditors missed, verified by a second human pass. Genuinely interesting if any are valid.

## Open design questions

- Skill design: how much guidance the SKILL.md contains, which helper scripts are bundled, what progressive-disclosure layers exist.
- Whether the agent is allowed iterative passes or runs one-shot.
- Audit scope per site (homepage vs. full crawl).

## Why this experiment

WCAG is a domain where:

- "Correct" is well-defined (the WCAG criteria), so calibration and false positives are checkable.
- A senior auditor's checklist is concrete and structured, making it a natural skill candidate.
- Public-sector audits are already published, removing the need for a separate ground-truth labelling pass.

This sits at the skill-shaped end of [[mcp-vs-skills]]: a specific task, a small team, drift acceptable.

---
*Lifted from `../manuscript-notes/essay-pointer.md` (Essay/essay.tex §3.3, §4.2-Experiment 2).*
