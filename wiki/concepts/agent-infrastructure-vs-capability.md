---
type: concept
sources: [simon1996artificial, sequoia2026karpathy, sofroniew2026emotions, peng2023copilot, weber2024taxonomy, aizawa2025tools, karpathy2025wiki, martin2026managed, fielding2000, lin2022truthfulqa]
related_concepts: [framework-four-components, distributed-cognition, deterministic-tools-hypothesis, calibration-thread, learning-as-temporal-dimension]
related_work: []
status: draft
updated: 2026-05-13
---

# Agent Infrastructure vs. Capability

**The wrong question.** The dominant question driving AI research is how to make models more intelligent. This thesis asks a different question: what infrastructure makes already-capable models productive on real-world tasks?

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

---
*Framing drawn from `../../manuscript-notes/essay-pointer.md` (Essay/essay.tex §1, §2.8, abstract).*
