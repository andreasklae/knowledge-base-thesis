---
type: literature
citekey: weber2024taxonomy
title: Large Language Models as Software Components — A Taxonomy for LLM-Integrated Applications
authors: [Weber, Irene]
year: 2024
venue: arXiv:2406.10300 (cs.SE, June 2024)
raw_path: raw/literature/Weber(2024).pdf
related_concepts: [framework-four-components, tools-component, agent-infrastructure-vs-capability, deterministic-tools-hypothesis]
related_work: []
status: summarized
ingested: 2026-05-15
updated: 2026-05-15
---

# Weber (2024) — Large Language Models as Software Components: A Taxonomy for LLM-Integrated Applications

## Summary

Weber proposes a **taxonomy for LLM-integrated applications** by treating each LLM invocation as a discrete software component — an "**LLM component**" — and characterising it along 13 dimensions grouped into five metadimensions: **Invocation, Function, Prompt, Skills, Output**. A complete application is described as a *combination of LLM components*. The taxonomy is constructed using Nickerson's iterative empirical-to-conceptual method on a sample of 11 LLM-integrated applications (Honeycomb, LowCode, MyCrunchGpt, MatrixProduction, WorkplaceRobot, AutoDroid, ProgPrompt, FactoryAssistants, SgpTod, TruckPlatoon, ExcelCopilot). A visualisation using compact one-letter feature vectors per LLM component allows applications to be displayed as tabular feature matrices. The taxonomy explicitly distinguishes the *LLM-as-software-component* perspective from two existing perspectives in the literature: *LLM-as-tool-for-development* (e.g. Copilot for coders) and *LLM-as-autonomous-agent* (multi-agent systems). For the thesis, this is the canonical academic-software-engineering taxonomy for describing how LLMs are integrated into applications, and it is a useful comparison point for the thesis's own four-component framework.

## Main claims

### 1. The "LLM-as-software-component" framing

Weber explicitly stakes out a third position between two existing literatures:
- **LLM-as-tool** (software engineering literature) — LLMs as a developer's aid (e.g. Copilot).
- **LLM-as-agent** (multi-agent systems literature) — LLMs as autonomous reasoners with goals.
- **LLM-as-software-component** (Weber) — LLM invocations embedded inside conventional software applications, performing specific tasks within a larger architecture.

This third framing is the thesis's frame too: agent infrastructure as software systems around an LLM.

### 2. The LLM component as unit of analysis

**Key insight (Weber's own framing):** "rather than analyzing an LLM-integrated application in whole, analysis should start with the identification and description of its distinct LLM components." An application like ExcelCopilot turns out to comprise four distinct LLM components (ActionExecutor, Advisor, IntentDetector, Explainer); MyCrunchGpt has three (DesignAssistant, SettingsEditor, DomainExpert); MatrixProduction has two (Manager, Operator). The unit of analysis is the *invocation pattern*, not the *product*.

### 3. The 13 dimensions, 5 metadimensions

**Invocation** (how the LLM is called):
- **Interaction**: App (programmatic, no user dialogue) / Command (single user command) / Dialog (multi-turn).
- **Frequency**: Single / Iterative.

**Function** (which application layer the LLM contributes to, using classical three-tier architecture):
- **Logic**: cAlculate (output processed as data) / Control (output drives control flow).
- **UI**: none / Input / Output / Both (does the LLM replace UI elements?).
- **Data**: none / Read / Write / Both (does the LLM read/write persistent storage?).

**Prompt** (where each part comes from):
- **Instruction** (static part defining the task) — always Program in practice.
- **State** (situation-dependent context) — none / User / LLM / Program.
- **Task** (specific task in this invocation) — none / User / LLM / Program.
- **Check** (mechanism to control/modify prompt before invocation) — none / User / LLM / Program.

**Skills** (capabilities leveraged — non-exclusive):
- **reWrite** (transform existing text/data), **Create** (generate novel content), **conVerse** (purposeful dialogue), **Inform** (use training knowledge), **Reason** (logical inference), **Plan** (multi-step planning).

**Output**:
- **Format**: FreeText / Item (single class label) / Code / Structure (custom formats).
- **Revision**: none / User / LLM / Program.
- **Consumer**: User / LLM / Program / Engine.

### 4. The feature-vector visualisation

The 13 dimensions per LLM component are rendered as a single row of single-letter codes (e.g. ExcelCopilot ActionExecutor: `A S A · · P P L · · · · · · P F C · · E`). Multiple LLM components from the same application are stacked vertically. This compactness is the taxonomy's distinctive contribution — it can put a complete LLM-integrated application on a single screen.

### 5. Sample observations (Figure 2)

Aggregating across 21 LLM components in the sample:
- **Frequency**: 16 Single, 9 Iterative.
- **Logic**: 13 cAlculate, 8 Control.
- **UI**: most have no UI replacement role; some Input, some Output.
- **Data**: only 2 Read, 0 Write — most LLM components don't touch persistent storage directly.
- **State**: dominated by Program-generated (17). User-generated State is rare.
- **Task**: User (11) and Program (7) dominate.
- **Check**: mostly none. Only 2 instances of Program-checking; none of User or LLM checking.
- **Skills**: Plan (8), Inform (7), Reason (4), Create (4), conVerse (3), reWrite (1).
- **Format**: FreeText (10), Code (6), Structure (8), Item (4).
- **Revision**: mostly none. Only 1 Program revision.
- **Consumer**: Engine (10), Program (3), User (3), LLM (5).

The bias toward "no Check, no Revision" is itself a finding: real-world LLM-integrated applications are *not* defensively wrapping LLM outputs as much as the safety literature might suggest they should.

### 6. Overloaded LLM components

Some LLM components serve multiple purposes — SgpTod's PolicyPrompter outputs both a class label *and* a chatbot response in a single invocation. Weber calls these **"overloaded LLM components"** and adopts the simplification rule of categorising by predominant purpose. The analogy is "function overloading" in classical programming.

### 7. Open practical challenges

Section 7 (Conclusion) names a set of open problems Weber observes from the sample:
- **No automated testing** — LLM invocation costs prohibit the test-driven-development practice that's standard elsewhere.
- **Prompt management as software asset** — currently ad-hoc, needs proper SE practice.
- **LMaaS reliability/availability** — provider model changes can break applications.
- **Latency** as a hard constraint — Honeycomb explicitly rejects GPT-4 as "far too slow" (Table 4).
- **Format adherence** — outputs need to parse reliably; current models don't guarantee this.

## Method / evidence

- **Design Science Research** methodology with Nickerson et al.'s (2013) iterative taxonomy-development method.
- **Empirical-to-conceptual + conceptual-to-empirical** iteration cycles. 5 major refinement passes.
- **Sample of 11 applications** (6 for development, 5 for evaluation), spanning industrial production, robotics, mobile automation, observability, TOD systems, expert systems.
- **Quality evaluation** against established taxonomy criteria (Nickerson, Unterkalmsteiner): comprehensiveness, robustness, conciseness, mutual exclusiveness, explanatory power, extensibility.
- **Single-researcher evaluation** (Weber alone), consistent with related work but a limitation acknowledged.

## Relevance to this thesis

### 1. A counterpoint and benchmark for the four-component framework

The thesis's [[framework-four-components]] proposes *workspace, tools, skills, data* as the primary infrastructure dimensions. **Weber's 13 dimensions are a different — and more granular — decomposition.** The thesis can position its framework explicitly against Weber's:
- Weber decomposes by *invocation properties* (interaction, frequency, function, prompt parts, output).
- The thesis decomposes by *infrastructure components* the LLM has access to.

These are *orthogonal* axes of analysis. Weber's taxonomy describes the *interface* of an LLM invocation; the thesis's framework describes the *substrate*. The thesis should cite Weber as a complementary academic framing.

### 2. Empirical evidence that LLM-integrated applications are componentised

Weber's most useful single finding for the thesis: **real-world LLM applications are composed of multiple, specialised LLM invocations**, not single monolithic prompts. ExcelCopilot has 4, MyCrunchGpt has 3, MatrixProduction has 2, AutoDroid has 3 (one TaskExecutor, two MemoryGenerators). This is direct evidence that **agent design at the production level is already de facto compositional**, supporting the thesis's argument that infrastructure design is a multi-component design problem.

### 3. The Prompt dimensions formalise context engineering

The Instruction / State / Task / Check decomposition is a useful formalisation of what [[rajasekaran2025]] calls context engineering. Weber gives it more structure: each prompt part has a provenance (User / LLM / Program / none). This vocabulary is worth borrowing.

### 4. Skills as a dimension precedes [[zhang2025]]

Weber's *Skills* dimension (reWrite/Create/conVerse/Inform/Reason/Plan) is an *output-property* taxonomy of what an LLM does in an invocation. Zhang 2025's *Agent Skills* is a *packaging-mechanism* concept. Both share the name; they are different things. The thesis should clarify this in [[skills-component]] to avoid conflation.

### 5. The "Function" dimension is the strongest match to the thesis's productivity argument

Weber's Function dimension breaks LLM contribution into UI / Logic / Data. The thesis's argument is that *infrastructure* determines what role the LLM plays. Weber's empirical observation that most LLM components have *no Data role* (only 2 Read, 0 Write across 21 components) is interesting: **the data component is currently underdeveloped relative to its potential.** Pair with [[lewis2020rag]] / [[rajasekaran2025]] just-in-time retrieval as the future direction.

### 6. The "no Check, no Revision" finding is a productivity-risk gap

Across 21 components, almost none implement Check (prompt review) or Revision (output review) beyond ad-hoc parsing. This is *infrastructure missing in practice*. The thesis can cite this as evidence that current LLM-integrated applications operate without the defensive infrastructure that production systems typically have — a known gap, not a solved one.

### 7. Taxonomy as descriptive vocabulary

For thesis chapters that compare or describe specific agent systems, Weber's vocabulary (LLM component, Instruction/State/Task, Single/Iterative, etc.) is *the academic vocabulary*. Use it where appropriate to give the thesis SE-discipline anchoring.

## Notable concepts introduced

- **LLM component** — discrete software component realised by an LLM invocation. Unit of analysis.
- **LLM-integrated application** — software system that invokes an LLM and processes its output; composed of LLM components.
- **13-dimension taxonomy** — Invocation, Function, Prompt, Skills, Output.
- **Prompt parts: Instruction / State / Task / Check** — standardised vocabulary for the parts of a prompt.
- **Overloaded LLM component** — single invocation serving multiple distinct purposes.
- **Feature-vector visualisation** — single-row compact rendering of a categorised LLM component.

## Concept-page reconciliation

1. **`wiki/concepts/framework-four-components.md`** — Weber is the closest academic taxonomy and the natural comparison point. Add a section: "Compared to Weber 2024's 13-dimension taxonomy, our four-component framework decomposes by *infrastructure substrate* rather than *invocation property*. The two are complementary."
2. **`wiki/concepts/tools-component.md`** — Weber's "Output Consumer = Engine" is the tools-component empirical signature: 10 of 21 components emit code/structure intended for an engine. Tools usage is *common* in the sample.
3. **`wiki/concepts/data-component.md`** — Weber's "Data: 2 Read, 0 Write" finding is empirical evidence the data component is *underdeveloped* in current production systems. Flag this.
4. **`wiki/concepts/skills-component.md`** — disambiguate *Weber-Skills* (output-property dimension) vs *Zhang-Skills* (packaging mechanism). Both exist; don't conflate.
5. **`wiki/concepts/agent-infrastructure-vs-capability.md`** — Weber's "no Check, no Revision" finding supports the thesis: infrastructure-around-the-LLM is currently thin in production. Plenty of headroom.
6. **`wiki/concepts/deterministic-tools-hypothesis.md`** — Weber's empirical observation that "Output Consumer = Engine" is common is the empirical form of the deterministic-tools hypothesis. Pair.
7. **`wiki/concepts/context-engineering.md`** — Weber's Instruction/State/Task formalisation precedes [[rajasekaran2025]]; the thesis can cite both as complementary vocabulary layers.

## Tensions and qualifications

- **Small sample.** 11 applications, mostly research papers (with the exception of Honeycomb, ExcelCopilot). Industrial production deployments are likely far more complex than this sample suggests.
- **2024 vintage.** Predates MCP, agent skills, claude code, and most of the maturity in the agent-infrastructure stack. The taxonomy doesn't accommodate concepts that appeared after publication.
- **No multi-LLM-call patterns formalised.** Weber represents *chaining* via "Prompt State = LLM," but more elaborate multi-agent orchestration patterns aren't first-class.
- **No tool-use / function-call dimension explicitly.** Tool use is mostly captured indirectly through Output Consumer = Engine, but this loses fidelity — modern agents call tools mid-generation in ways Weber's taxonomy can't cleanly represent.
- **No agent-state or memory dimension.** Stateful conversation history is buried in "Prompt State." Long-term memory (NOTES.md, file system, vector DBs) doesn't have a clean home.
- **No model dimension.** Weber notes which LLMs each application uses (Table 4) but no taxonomy dimension addresses model size/family/version. Updated taxonomies will need this.
- **Single-researcher evaluation.** Acknowledged limitation. Independent application of the taxonomy by others is needed.
- **Feature-vector compactness vs interpretability trade-off.** The visualisation requires constant reference to a legend. Not great for casual readers; effective for systematic comparison.
- **Excluded interview/qualitative data.** Weber relies on published descriptions; in practice many details (the prompt examples, the failure modes) are not in the cited papers.

## Connections

- [[anthropic2024mcp]] — MCP postdates Weber; the taxonomy doesn't model protocol-mediated tool access cleanly.
- [[aizawa2025tools]] — Aizawa's design-quality view of tools complements Weber's structural view.
- [[zhang2025]] — Zhang's "Skills" packaging differs from Weber's "Skills" capability dimension. Disambiguate.
- [[rajasekaran2025]] — context engineering as a discipline; Weber's Prompt dimensions are an earlier formalisation of the same concern.
- [[martin2026managed]] — managed-agent harness/session/sandbox; Weber's taxonomy doesn't address harness-level concerns.
- [[krishnan2025multiagent]] — Krishnan operates at a higher architectural altitude (6-layer reference); Weber operates at the per-invocation altitude.
- [[peng2023copilot]] — Peng's empirical productivity result is on a specific LLM component (a code-completion ActionExecutor in Weber's vocabulary).
- [[simon1996artificial]] — Simon's near-decomposability view supports Weber's decision to analyse by per-component invocation.
- [[fielding2000]] — orthogonal decomposition methodology. Fielding derives by *adding architectural constraints*; Weber decomposes by *invocation properties*. Pair the two as complementary axes of analysis (substrate vs. invocation).
- [[matarazzo2025survey]] — Matarazzo's substrate survey provides the foundation that Weber's 11 sampled applications run on top of; useful as the LLM-substrate companion when Weber's per-invocation taxonomy needs grounding in model capability.
- Concept pages: [[framework-four-components]], [[tools-component]], [[data-component]], [[skills-component]], [[agent-infrastructure-vs-capability]], [[deterministic-tools-hypothesis]], [[context-engineering]].

---
*Ingested 2026-05-15. Read in full (26 pages including references).*
