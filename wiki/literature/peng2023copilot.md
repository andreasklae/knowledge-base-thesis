---
type: literature
citekey: peng2023copilot
title: The Impact of AI on Developer Productivity — Evidence from GitHub Copilot
authors: [Peng, Sida, Kalliamvakou, Eirini, Cihon, Peter, Demirer, Mert]
year: 2023
venue: arXiv:2302.06590
raw_path: raw/literature/Peng(2023).pdf
related_concepts: [agent-infrastructure-vs-capability, framework-four-components, tools-component]
related_work: []
status: summarized
ingested: 2026-05-14
updated: 2026-05-15
---

# Peng et al. (2023) — The Impact of AI on Developer Productivity: Evidence from GitHub Copilot

## Summary

Peng, Kalliamvakou, Cihon, and Demirer report on the **first published controlled experiment measuring the productivity effect of an AI coding assistant** in professional software development. 95 freelancer developers recruited via Upwork were randomly assigned to use GitHub Copilot (treated, n=45) or not (control, n=50), and tasked with implementing an HTTP server in JavaScript as quickly as possible. **The treated group completed the task 55.8% faster on average (95% CI: 21–89%, p=0.0017).** Heterogeneity analysis shows the benefit is *larger* for less-experienced developers, older developers (25–44 band), and those with heavy daily programming load. The paper is the canonical empirical citation for "AI tools meaningfully accelerate software development tasks." Limitations: a single standardised task, JavaScript only, no code-quality measurement, freelancers (not enterprise developers).

## Main claims

- **55.8% faster task completion** in the treated group (mean 71.2 min) vs control (mean 160.9 min). Statistically significant (p=0.0017). All four >300-minute outliers are in the control group; result is robust to dropping them.
- **Success rate** of Copilot users was 7 percentage points higher than the control group, but the difference was *not* statistically significant (95% CI: [-0.11, 0.25]). The intervention sped people up; it did not (in this sample) reliably increase completion rates.
- **Heterogeneous treatment effects (Table 1):**
  - **Less programming experience → more benefit** (coefficient: -8.23 min reduction per year of experience for the control; positive coefficient in treatment effects regression indicates benefit decreases with experience). Less-experienced developers gain the most.
  - **More daily coding hours → more benefit** (-11.70, p=0.0168).
  - **Age 25–44 → more benefit** than 18–24 (-74.55, p=0.0303).
  - Employment status, income, education, and language preference: no statistically significant heterogeneity.
- **Self-reported productivity gain estimate: 35%** (both groups, post-tutorial). Underestimates the *measured* 55.8% gain. Developers underestimate the speedup they actually get from the tool.
- **Willingness-to-pay (WTP):** treated group's "irrelevant price" (highest price at which they'd still want notification of release) was $27.25/month; control group $16.91/month. Difference statistically significant. **Hands-on experience increases WTP.**

## Method / evidence

- **Experimental design:** controlled randomised trial. Pre-registered with Microsoft Research ethics board.
- **Recruitment:** Upwork freelancer job posting (May 15 – June 20, 2022). 166 offers sent → 95 accepted → 70 completed task & survey (35 each).
- **Task:** Implement an HTTP server in JavaScript. Skeleton repo provided via GitHub Classroom; 12 test cases for success. Compensation $20–$160 based on completion time (incentive to be fast).
- **Treatment:** access to GitHub Copilot + 1-minute tutorial video.
- **Control:** no Copilot; otherwise unrestricted (could use Stack Overflow, search, etc.).
- **Metrics:** task success (binary), task completion time (timestamp diff: repo creation → first commit passing all 12 tests).
- **Sample bias notes:** participants mostly from India/Pakistan, age 25–34, median income $10k–$19k/year, 6 years average coding experience, ~9 hours/day coding. Not a representative sample of US/EU enterprise developers.

## Relevance to this thesis

### 1. Empirical anchor for "AI tools improve developer productivity"

The thesis's headline claim — that agent productivity is a real, measurable phenomenon worth studying — needs an empirical anchor. **Peng 2023 is the canonical such citation.** Pre-2023 work on AI coding productivity was mostly perception-based (surveys, qualitative); Peng is the first RCT with measured task completion time. The 55.8% effect size is large enough that it survives serious caveats.

### 2. Less-experienced developers benefit most

This is the most thesis-relevant heterogeneity. **Infrastructure (here, an AI coding tool) provides differentially larger gains to people who lack the human capital that would otherwise substitute.** This is the [[agent-infrastructure-vs-capability]] argument applied to *human* developers being augmented: infrastructure improvements compress the productivity distribution. If true for human developers, an analogous claim for AI agents — that good infrastructure compresses the gap between weaker and stronger models — becomes plausible.

### 3. Self-estimates underestimate measured productivity gains

Developers underestimate Copilot's impact by ~21 percentage points (35% estimated vs 55.8% measured). For the thesis: **self-reported productivity is an unreliable measurement**. The thesis's own experimental design should privilege measured outcomes over surveys whenever possible.

### 4. Single-task limitation echoes thesis experimental design considerations

Peng explicitly notes (Discussion): "this study examines a standardized programming task ... [productivity benefits] may vary across specific tasks and programming languages." This is the same limitation the thesis's own task-bounded experiments face. The community is aware of the issue; the thesis can position its own experiments as expanding the task-coverage of the Peng-style evidence base.

### 5. Code quality unmeasured

Peng explicitly does not measure code quality. The thesis can engage with the open question: does AI-assisted code generation trade speed for quality? Subsequent work (e.g., Sandoval 2022 on security, Mozannar 2022 on user behaviour) starts to address this, but the question remains live.

## Notable concepts introduced

- **AI pair programmer** — framing GitHub Copilot in this way. Influential terminology.
- **Self-reported vs. measured productivity gap** — developers underestimate measured speedups by ~20 pp.
- **Heterogeneous treatment effects via Horvitz-Thompson** — methodological pattern for productivity experiments.
- **Willingness-to-pay (WTP) as a productivity proxy** — used here as an indirect measure.

## Concept-page reconciliation

1. **`wiki/concepts/agent-infrastructure-vs-capability.md`** — Peng's heterogeneity finding (less-experienced developers benefit more) is direct empirical support for the thesis's claim that infrastructure can compress capability differences. Worth surfacing as a concrete data point.
2. **`wiki/concepts/tools-component.md`** — Copilot is a *tool* in the four-component framework. Peng provides the empirical productivity payoff for that component class.
3. **`wiki/concepts/framework-four-components.md`** — Peng measures one specific instantiation (a code-completion tool). The thesis's larger framework predicts similar gains from the other three components (workspace, skills, data) but Peng-style RCTs for those are rarer.

## Tensions and qualifications

- **Single task, single language.** HTTP server in JavaScript. Generalisability to other tasks (refactoring, debugging, design) and languages is open.
- **Single tool.** Copilot circa May 2022 (powered by Codex). Modern Copilot (GPT-4-class models, agent mode) is qualitatively different.
- **No code quality measure.** Speed gains might mask quality losses. The thesis should note this explicitly when citing Peng.
- **Upwork freelancer sample.** Not representative of enterprise developers or open-source maintainers. Replications in other populations are needed.
- **N=70 (completed).** Modest sample. Confidence intervals on heterogeneity effects are wide.
- **Selection into Upwork freelancing.** Self-selection bias is real; freelancers may be unusually motivated by hourly-rate incentives.
- **Five treated participants started without Copilot due to incomplete signup.** Counted in treated group (intent-to-treat); reduces measured effect.
- **Compensation scale rewards speed.** The 55.8% gain may overestimate speedup in settings where speed is not directly rewarded — though it may also *underestimate* gain since slower control participants had a sunk-cost-style incentive to finish.

## Connections

- Productivity claims downstream: any thesis argument about "AI tools accelerate work" should cite Peng as the empirical anchor.
- [[karpathy2025wiki]] — Karpathy's LLM-Wiki idea is a knowledge-base instantiation of the productivity-gain hypothesis Peng demonstrates for code; the mechanism is similar (model does mechanical work, human does direction).
- [[anthropic2024mcp]] — MCP makes more tools available to coding agents; predicts further productivity gains beyond Copilot circa 2022.
- [[zhang2025]], [[rajasekaran2025]], [[aizawa2025tools]] — Anthropic's engineering practice posts assume Peng-style productivity payoffs; they're about *how* to make them happen at scale.
- [[sequoia2026karpathy]] — Karpathy's claim that *agentic-engineering peaks much higher than 10×* is the qualitative ceiling Peng's 55.8% measured floor is bounded below by. Pair as 2022 RCT + 2026 expert observation.
- [[martin2026managed]] — managed-agent harness reports 60–90% time-to-first-token reductions. Peng's 55.8% is on the *task-completion* axis; Martin's numbers are on the *latency* axis. Both are infrastructure-layer productivity gains without model change.
- [[yin2018case]] — methodological contrast: Peng is the RCT pole; Yin is the case-study pole. The thesis cites Peng for the canonical productivity anchor and Yin for the methodological scaffold of its own case-shaped experiments.
- Concept pages: [[agent-infrastructure-vs-capability]], [[tools-component]], [[framework-four-components]].

---
*Ingested 2026-05-14. Read in full (19 pages).*
