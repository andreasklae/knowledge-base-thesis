---
type: concept
sources: [simon1996artificial, hutchins1995wild, norman2013design, martin2026managed, krishnan2025multiagent, fielding2000, weber2024taxonomy, zhang2025, rajasekaran2025, aizawa2025tools]
related_concepts: [workspace-component, tools-component, skills-component, data-component, calibration-thread, deterministic-tools-hypothesis, distributed-cognition, learning-as-temporal-dimension, agent-infrastructure-vs-capability]
related_work: [experiment-riksantikvaren, experiment-wcag-skill, experiment-math, experiment-vision-landmarks, experiment-chess, experiment-incubation]
status: draft
updated: 2026-05-15
---

# The Four-Component Framework

The thesis's central decomposition: what an agent needs to be productive resolves into four affordances.

1. **Workspace** — an environment where actions have bounded consequences, where state is observable, and where prior actions can be referred to. The agent acts in the workspace; the workspace persists what was done.
2. **Tools** — the agent's reach into external systems. A tool is a deterministic operation the agent calls but does not perform itself.
3. **Skills** — compiled, reusable, progressively-disclosed procedural knowledge. A skill is what a senior practitioner has internalised that a junior has not yet.
4. **Data** — live access to information beyond what fits in context or what was memorised at training time.

## Affordances, not a partition

The four are affordances, not a strict partition. A skill that calls a deterministic script is also a tool with documentation; a workspace that records prior actions is also a data source for later sessions; a tool description rich enough to teach use is approaching a skill. Overlap is expected. The framework's value is in naming what to look for, not in placing every artefact in exactly one bucket. Experiments test each affordance individually rather than claim mutual exclusivity.

## The human analogies

Three analogies motivate the decomposition and are referenced repeatedly across the thesis.

- **The civil engineer.** A modern civil engineer is not measurably more intelligent than a Roman aqueduct builder but produces work the Roman could not — two thousand years of materials science, codes, finite-element analysis, and post-mortems sit between them. Productivity is a property of the inheritable stock of compressed solutions the worker can draw on, not primarily of the brain doing the work.
- **The musician.** Training on a large corpus is like a musician listening to thousands of hours of music: deep intuition, recognition of almost anything heard, but no piano-playing. To play a song one needs theory, sheet music, an instrument, and procedural skill. Some knowledge is irrelevant (the wavelength of each note, the history of music).
- **The driver.** A car makes its driver enormously more productive without the driver knowing how the engine works. Bounded knowledge with stable interfaces between specialists — F1 driver, engine mechanic — is what makes the system work.

## Relation to Martin et al.'s decomposition

[[martin2026managed]] uses three abstractions: harness, session, sandbox. This thesis's framework translates them:

- Their **sandbox** is closest to this thesis's **workspace**.
- Their **session** (the append-only log of what happened) becomes part of the broader problem of persistence and context management, taken up in the Sleep and Knowledge chapters.
- Their **harness** (the loop calling the model and routing tool calls) is the orchestration infrastructure these four affordances sit inside; the framework describes what the harness has to offer the model rather than how the harness itself is built.

[[krishnan2025multiagent]] extends the analysis to multi-agent systems on MCP, with coordination patterns intended to scale across agents.

[[weber2024taxonomy]] provides an orthogonal decomposition: 13 invocation-property dimensions (Invocation / Function / Prompt / Skills / Output) for a single LLM call. The four-component framework decomposes by *infrastructure substrate*; Weber decomposes by *invocation property*. The two are complementary axes of analysis. (Note: Weber's *Skills* dimension is an output-property — reWrite/Create/conVerse/Inform/Reason/Plan — which is not the same concept as [[zhang2025]]'s *Skills* packaging mechanism. The thesis vocabulary uses Zhang-Skills.)

## Constraint-derivation methodology

[[fielding2000]] derives REST by adding architectural constraints one at a time, naming the property each induces and the trade-off it accepts (null → client-server → stateless → cache → uniform interface → layered system → code-on-demand). The four-component framework can be presented the same way: starting from a bare LLM, each component is a *named, coordinated set of constraints* whose properties can be enumerated. This is more rigorous than "here are four nice components"; it forces the framework to declare what each constraint costs and what it buys.

## Progressive disclosure as a cross-component design principle

[[zhang2025]] frames skills around *progressive disclosure*: expose a description, load the body on demand, load resources only when needed. [[rajasekaran2025]] generalises the same principle to data via *just-in-time retrieval*: hold lightweight identifiers (file paths, queries), load content on demand. The principle is not skills-specific or data-specific — it is a **cross-component design principle** that applies to workspace (file tree → glob → read), tools (tool list → schema → result), skills (description → body → resources), and data (index → result → document). Token efficiency is a workspace and infrastructure problem, not just a context-engineering trick — see [[aizawa2025tools]] for the tool-layer instantiation (DETAILED vs CONCISE response formats).

## What the framework is for

The framework is a working vocabulary. Another researcher should be able to use it to describe and reason about a new agent system. Each experiment exercises one or more components: workspace through rescue rate and turns-to-solution after intervention; tools through accuracy and calibration; skills through performance gains and reuse; data through answer accuracy, calibration, and efficiency across retrieval architectures.

## What learning is not

Learning is not a fifth component. It is the temporal dimension of the existing four — see [[learning-as-temporal-dimension]].

## Cross-cutting threads

Two claims run through every component:

- [[calibration-thread]] — calibration improves in proportion to how cleanly the component externalises verification.
- [[deterministic-tools-hypothesis]] — the limit case of the calibration mechanism: where the externalised step is itself the answer.

---
*Framing drawn from `../../manuscript-notes/essay-pointer.md` (Essay/essay.tex §1, §3.1).*
