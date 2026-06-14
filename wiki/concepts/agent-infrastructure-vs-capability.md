---
type: concept
sources: [simon1996artificial, sequoia2026karpathy, sofroniew2026emotions, peng2023copilot, weber2024taxonomy, aizawa2025tools, karpathy2025wiki, martin2026managed, fielding2000, lin2022truthfulqa]
related_concepts: [framework-four-components, distributed-cognition, deterministic-tools-hypothesis, calibration-thread, learning-as-temporal-dimension]
related_work: [experiment-chess, experiment-riksantikvaren, experiment-math, experiment-wcag-skill, experiment-vision-landmarks, experiment-incubation]
status: draft
updated: 2026-05-28
---

# Agent Infrastructure vs. Capability

**The wrong question.** The dominant question driving AI research is how to make models more intelligent. This thesis asks a different question: what infrastructure makes already-capable models productive on real-world tasks?

**The primary research question** (essay §1, `../../manuscript-notes/essay-pointer.md`): *how can principles of human productivity be operationalised as design patterns for AI agent systems?* The motivating intuition is that productivity is not primarily a property of the brain doing the work but of the inheritable stock of compressed solutions the worker can draw on. A modern civil engineer is not smarter than a Roman aqueduct builder but produces work the Roman could not, because two thousand years of materials science, codes, and post-mortems sit between them. A musician with thousands of hours of listening still needs sheet music, an instrument, and procedural skill to play a piece. A driver is made productive by the car without understanding the engine. The thesis asks whether the same structural pattern — bounded knowledge behind stable interfaces, plus an accumulated stock of skills and tools — is what makes a *language-model agent* productive, and whether that stock can be grown around a **fixed** model rather than baked into a new one.

The experiments are the test of that claim. Each holds a model fixed and varies the infrastructure around it: [[experiment-chess]] (skill accumulation around a fixed model, measured by Elo trajectory), [[experiment-riksantikvaren]] (four knowledge-access configurations on one corpus), [[experiment-math]] (inference vs. skills vs. coding sandbox), [[experiment-wcag-skill]] (skill vs. no skill), [[experiment-vision-landmarks]] (tools to constrain a biased candidate set), and [[experiment-incubation]] (workspace/session-state manipulation for fixated agents).

## The diagnosis

AI productivity is shifting from a machine-learning problem toward something closer to cognitive ergonomics for non-human cognition. The next decade of useful AI engineering will be a design discipline, and it is currently being built without a vocabulary. Engineers at frontier labs and agent-tooling startups are converging on the same primitives (skills, sessions, sandboxes, tools, retrieval) without a shared way of talking about what those primitives are for or how they relate.

## Why infrastructure dominates for production behaviour

Three reasons, each operationalised somewhere in the framework:

1. **The structural limits of inference.** Hallucination is bounded below by training-data structure (see [[calibration-thread]]). You cannot get past these limits with model scale alone — but you can get around them by externalising verification ([[deterministic-tools-hypothesis]]).
2. **Substrate is not the dominant variable.** [[simon1996artificial]]'s ant: the complexity of behaviour reflects the structure of the environment, not the complexity of the agent. Better environments produce better outputs from the same agent. See [[distributed-cognition]].
3. **Capability gains are often infrastructure gains in disguise.** Karpathy's [[sequoia2026karpathy]] observation that the chess-capability jump between GPT-3.5 and GPT-4 was largely a lab data-curation decision is the lab-side version of the same point: improving the *information environment* around the model improves outputs more reliably than improving the model.

## The role of training is not nil

The framework's claim is not that training is irrelevant. It is that for production behaviour, infrastructure approaches dominate, with fine-tuning and activation-level steering [[sofroniew2026emotions]] reserved for cases where prompting and skills cannot reliably reach the target behaviour.

## Existing work on AI-assisted development

Empirical work on AI-assisted development has focused predominantly on code-completion tools, reporting significant productivity gains for routine tasks: [[peng2023copilot]] found that developers given GitHub Copilot completed a standardised HTTP-server task 55.8% faster than a control group, with the largest gains among less experienced programmers. This thesis addresses a different setting — full-system scaffolding, where the agent generates entire components and the developer's primary role becomes integration and validation. [[weber2024taxonomy]] provides a useful taxonomy of LLM-integrated applications that situates this setting.

## Direct empirical anchors

Three recent industry findings give the infrastructure-dominates claim quantitative support without invoking new model capability:

- **[[aizawa2025tools]]** report that Claude-assisted optimisation of internal MCP tool sets moved Slack tool accuracy from **67.4% → 80.1%** and Asana from **79.6% → 85.7%** on held-out evals. Same model, same protocol — only the tools changed. Tool-design quality is itself a productivity lever, distinct from the model.
- **[[lin2022truthfulqa]]** show that prompt infrastructure alone (a "helpful" prompt) moves GPT-3-175B from 21% to 58% truthful — a 37 pp gain without any model change. Scale, by contrast, *hurts* on the same benchmark (inverse scaling).
- **[[martin2026managed]]** reports that managed-agent harnesses reduce time-to-first-token by 60–90% across deployments. Harness-level infrastructure changes the realised performance of the underlying model substantially.

## Agent-native infrastructure as the ecosystem-scale gap

Karpathy's "pet peeve" in [[sequoia2026karpathy]] — *"every time I'm told 'go to this URL' or something like that, it's just like 'ah'. What is the thing I should copy-paste to my agent?"* — is the same argument applied to the *broader software ecosystem*: most current infrastructure (docs, settings GUIs, signup flows) is human-first, not agent-native. The bottleneck on agent productivity is not just inside the agent harness; it is the entire surrounding world that has not yet been re-shaped for non-human cognition. [[karpathy2025wiki]]'s closing line names the historical precedent: Vannevar Bush's Memex (1945) vision was constrained by *who maintains the structure*; agents lift that constraint.

## Properties induced by infrastructure, not by components

[[fielding2000]] derives REST by adding architectural constraints and naming the properties each induces. The framework's deepest theoretical support: **system-level properties (scalability, evolvability, calibration, factuality) are induced by *infrastructure constraints*, not by component implementation**. This is the architectural-style version of the thesis's main claim. Tools as MCP-mediated REST primitives are simply the agent-era instantiation of Fielding's protocol-design discipline.

## Why a framework before rubrics

The field needs the vocabulary before it needs the rubrics. The contribution of this thesis is the vocabulary plus six test cases exercising it. See [[framework-four-components]].

## Failures are semantic, not syntactic

A specific framing from [[sequoia2026karpathy]] (developed further in [[interview-karpathy-analysis-2]]) sharpens the infrastructure claim. Agent failures in production are typically *not* syntax errors — those are caught by compilers, type checkers, and unit tests. The failures that matter are semantic: mistaken assumptions about identity, ownership, persistence, security, or real-world use. Karpathy's canonical example is the MenuGen billing bug, where the agent matched Stripe email addresses against Google email addresses to associate credit purchases with users — locally plausible, conceptually wrong, because a user may transact under different emails on each service.

Two consequences for the framework:

1. The model can produce code that runs, passes tests, and is wrong. The agent has no concept of *why* a persistent user ID matters, only of how to write code that compiles and looks plausible.
2. The compensating infrastructure has to operate at the *specification* layer, not just the verification layer. Tests can verify that the wrong specification is correctly implemented; only better specs, adversarial cases, integration tests with realistic identity models, or human review can catch the bug.

This is the [[calibration-thread]] applied to specification rather than to factual claims. The model is miscalibrated about what its code *means* in the real world, not just about whether its facts are true. Tools and skills can carry domain invariants (identity, ownership, atomicity, transactional boundaries) into the agent's context as enforceable preconditions; this is one of the strongest infrastructure-side levers because the model cannot generate the invariants on its own.

## The thesis's own workflow as latent case material

The knowledge base supporting this thesis is itself an instance of the infrastructure pattern under study (see [[diary/meta/2026-05-14]]). It implements [[karpathy2025wiki]]'s LLM-Wiki architecture with a three-ownership-zone refinement (raw / user-authored / LLM-compiled), governed by a CLAUDE.md schema that is co-evolved by the user and the agent. The maintaining agent reads sources, writes synthesis, propagates updates across pages, lints for link integrity and contradictions, and processes captured thoughts into structured destinations — all functions the thesis attributes to the data and skills components of the framework. Diary entries from the design and operation of this KB are tagged `meta-observation` so the evidence is preserved even though writeup is not yet committed to. If the KB's compounding synthesis succeeds (or fails) in interesting ways, the trace is on disk.

---
*Framing drawn from `../../manuscript-notes/essay-pointer.md` (Essay/essay.tex §1, §2.8, abstract).*
