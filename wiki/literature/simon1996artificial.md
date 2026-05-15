---
type: literature
citekey: simon1996artificial
title: The Sciences of the Artificial (3rd edition)
authors: [Simon, Herbert A.]
year: 1996
venue: MIT Press (book; based on Compton lectures 1968 + Gaither lectures 1980, with 1996 additions)
raw_path: raw/literature/Simon(1996).pdf
related_concepts: [framework-four-components, agent-infrastructure-vs-capability, distributed-cognition, deterministic-tools-hypothesis, context-engineering]
related_work: []
status: summarized
ingested: 2026-05-14
updated: 2026-05-14
---

# Simon (1996) — The Sciences of the Artificial (3rd edition)

## Summary

Simon's *The Sciences of the Artificial* is the foundational text for what is meant by "designed systems" and "sciences of design" as objects of study distinct from natural science. Its central thesis: **certain phenomena are "artificial" in a specific sense — they are as they are only because a system has been moulded, by goals and purpose, to an environment.** Natural phenomena have an air of necessity; artificial phenomena have an air of contingency. An artifact is best understood as an **interface** between an "inner environment" (the artifact's substance and organisation) and an "outer environment" (the surroundings in which it operates). If the inner is appropriate to the outer, the artifact serves its purpose. The book then applies this frame to economics (bounded rationality, organisations vs markets), cognitive psychology (the human as a symbol-processing system), design as a science (the curriculum for engineering, the role of representation), social planning, and complexity (the "Architecture of Complexity" essay establishing **hierarchic, near-decomposable systems** as the dominant form of complex systems). Together with [[hutchins1995wild]] and [[norman2013design]], Simon is the third leg of the cognitive-science framing the thesis inherits — and arguably the most thesis-relevant of the three because the *infrastructure-as-bottleneck* argument is essentially a sciences-of-the-artificial argument.

## Main claims

### 1. The four indicia of the artificial (Ch. 1, p. 5)

Simon defines artificial systems by four criteria:
1. **Synthesised by humans** (though not always with full forethought).
2. **May imitate natural appearances** while lacking, in one or many respects, the reality of the natural.
3. **Characterised in terms of functions, goals, adaptation.**
4. **Often discussed in imperatives as well as descriptives** ("how it ought to be" alongside "how it is").

This frame is the conceptual ground for the thesis's whole approach. The "agent productivity infrastructure" the thesis studies *is* an artificial system by all four criteria: it is human-synthesised, it imitates natural cognitive scaffolding, it is characterised by function (what the agent should accomplish), and it is discussed normatively (how the infrastructure *should* support the agent).

### 2. The artifact as interface (Ch. 1, pp. 6-9)

The single most-cited Simon idea outside the book is this: **"An artifact can be thought of as a meeting point — an 'interface' in today's terms — between an 'inner' environment, the substance and organization of the artifact itself, and an 'outer' environment, the surroundings in which it operates."**

The corollary is methodologically load-bearing: **"we can often predict behavior from knowledge of the system's goals and its outer environment, with only minimal assumptions about the inner environment."** This is the licence for studying agent productivity *as a function of infrastructure (outer)* without committing to specific claims about model internals (inner). The thesis can cite this directly when it argues that infrastructure choices dominate model-internals choices for productivity outcomes.

### 3. Bounded rationality and procedural rationality (Ch. 2)

Simon's most-cited contribution. Real decision-makers (human, organisational, or artificial) have **limited rationality** — limited information, limited computation, limited attention. They satisfice rather than optimise. **Procedural rationality** (rationality of the *process* of deciding under bounded resources) replaces substantive rationality (rationality of the *outcome* given full information) as the operational concept.

For the thesis: the agent's "rationality" is bounded by context window, by token budget, by tool availability, by latency. Infrastructure design *is* the design of the bounds on the agent's procedural rationality. Cite Simon (Ch. 2) as the canonical reference.

### 4. Symbol systems and the human as physical-symbol system (Ch. 3-4)

Simon and Newell's claim: **a physical symbol system has the necessary and sufficient means for general intelligent action** (the Physical Symbol System Hypothesis). Humans and computers are both instances; the form of intelligence does not depend on the substrate.

For the thesis, this matters in two ways:
- It is the philosophical ground for treating LLMs as cognitive systems comparable in *function* (if not substrate) to humans. The thesis's frequent appeals to human cognitive science (Wallas, Hutchins, Ericsson, Norman) presuppose roughly this functionalist stance.
- The PSS hypothesis is contested. The thesis can stand on it without committing to its strong form — it suffices that *functional* analogies between human and LLM workflows are productive for design.

Chapters 3-4 also cover memory ("memory as environment for thought"), which connects to the thesis's [[context-engineering]] / [[workspace-component]] arguments — the agent's available context *is* its working memory environment.

### 5. The science of design (Ch. 5)

Simon's argument: design is a science, not an art, and it has a curriculum. The science of design covers:
- **Representation of the design problem** — choice of representation often dominates choice of solution.
- **Generation and search of alternatives** — design as search through a problem space.
- **Evaluation against goals** — including under uncertainty.
- **Hierarchical structure of design** — decomposing into nearly-independent subproblems.

The thesis's whole project is in this tradition. Phrases like "infrastructure as a designed system" and "the agent as the designer of its workspace" inherit Simon's framing. The thesis can use Ch. 5 explicitly as the methodological model: this is **engineering as a science** applied to a new artifact (the productive AI agent and its infrastructure).

### 6. Social planning and "designing without forecasts" (Ch. 6)

Two thesis-relevant ideas:

- **Attention is the scarce resource, not information.** Pages 143-145: "A design representation suitable to a world in which the scarce factor is information may be exactly the wrong one for a world in which the scarce factor is attention." Simon writes this in 1996 about management information systems; it transfers verbatim to LLM context windows. **"The real design problem is not to provide more information to people but to allocate the time they have available for receiving information."** The design of agent infrastructure is, in Simon's frame, the design of intelligent information-filtering for an attention-bounded processor.

- **Design via feedback, homeostasis, and bounded prediction.** Simon argues (pp. 147-150) that good adaptive systems do not depend on accurate long-range prediction. They use feedback, homeostatic insulation from short-term variation, and only as much prediction as is needed to inform current commitments. For the thesis: agent infrastructure that depends on accurate long-range forecasts is brittle; infrastructure that uses feedback (verifier loops, tool outputs, self-evaluation) is robust. This directly supports the verification-by-tool / verification-by-self arguments from [[kalai2024hallucinate]] and [[kadavath2022know]].

### 7. Hierarchy and near-decomposability (Ch. 8, originally 1962)

The "Architecture of Complexity" — Simon's most cited paper. Claim: **complex systems that survive evolution tend to be hierarchic and nearly decomposable.** A complex system organised into subsystems, where interactions within a subsystem are stronger and faster than interactions across subsystems, is more robust, more evolvable, and more analytically tractable than a flat or strongly-coupled system.

The example: assembling a complex watch made of 1000 parts. If assembled flat (any disruption sends you back to zero), it is essentially infeasible. If assembled hierarchically (1000 parts → 100 modules of 10 → 10 super-modules of 10 modules → 1 watch), disruption costs only the current sub-assembly. The math favours hierarchy by orders of magnitude.

For the thesis: **agent infrastructure should be organised in nearly-decomposable layers** (workspace ↔ tools ↔ skills ↔ data, in [[framework-four-components]]). Each layer can be developed, debugged, and replaced semi-independently of the others. This is Simon's argument applied to agent infrastructure.

### 8. Functional explanation and substrate independence (Ch. 1)

Simon's example: white Arctic animals. The colour is explained by reference to the *function* (camouflage) and the *outer environment* (snow). Once you know the outer environment and the goal (survival via predator avoidance), you can predict the colour without knowing biological details.

The thesis-relevant generalisation: **for systems shaped by adaptation, knowing the outer environment + goal often suffices to predict behaviour.** The agent's "outer environment" is its task domain and its infrastructure. Goal: be productive. Prediction: the agent's observable behaviour will be shaped strongly by the infrastructure (outer) and weakly by model internals (inner). This is the thesis's central claim, restated in Simon's vocabulary.

## Method / evidence

Simon's method is **multi-disciplinary essay**, not empirical study or formal proof. The book draws on:
- Decades of work on administrative behaviour, economics, and management science (Simon's Nobel was for bounded rationality).
- Cognitive psychology research, much of it Simon's own (with Newell): GPS, EPAM, protocol analysis.
- Engineering examples (the motor controller patent in Ch. 1; the Marshall Plan / ECA case in Ch. 6).
- Computer science (computational complexity, simulation).
- Cross-disciplinary synthesis.

The third edition adds Ch. 7 on alternative views of complexity (chaos, adaptive systems, genetic algorithms), placing Simon's hierarchy/near-decomposability view in dialogue with later complexity-science traditions.

## Relevance to this thesis

### 1. The philosophical ground

Simon is the canonical reference for *why* one would study "agent productivity as an infrastructure problem" at all. The whole sciences-of-the-artificial framing — that designed systems can be studied scientifically, that their behaviour is largely a function of the outer environment, that "ought" can sit alongside "is" — is what authorises the thesis project methodologically. **The thesis's most natural single citation for its methodological framing is Simon 1996 Ch. 1 and Ch. 5.**

### 2. Attention as the scarce resource (Ch. 6) maps directly onto context window economics

Simon's 1996 line about "the task is not to design information-distributing systems but intelligent information-filtering systems" is *exactly* the modern context-engineering argument ([[rajasekaran2025]], [[karpathy2025wiki]]). The thesis can use Simon as the deep historical anchor for an argument that looks contemporary. See [[context-engineering]].

### 3. Hierarchy and near-decomposability justify [[framework-four-components]]

The four-component framework (workspace / tools / skills / data) is a near-decomposable architecture. Simon's argument is *why* this is the right shape: nearly-decomposable systems are more evolvable, more debuggable, more analytically tractable than flat or strongly-coupled ones. The thesis can cite Ch. 8 directly when defending the four-component split.

### 4. Bounded rationality is the operating constraint

The agent is a bounded-rational decision maker. Context window is a memory bound; tool latency is a time bound; reasoning steps are a computation bound. Procedural rationality (Ch. 2) — making good decisions *given* these bounds — is what the thesis is trying to design for. This is not just a metaphor; it is the same conceptual move Simon applied to administrative decision-making, applied now to AI agents.

### 5. Inner/outer environment dichotomy is the licence to study infrastructure

The thesis can study agent infrastructure (outer) without committing to specific claims about model internals (inner). Simon (Ch. 1) explicitly authorises this methodological move: "we can often predict behavior from knowledge of the system's goals and its outer environment, with only minimal assumptions about the inner environment." This is a direct refutation of "you can't study agent productivity until you understand the model." You can.

### 6. Design as search through alternatives (Ch. 5) frames the experimental method

The thesis's experiments are, in Simon's frame, design experiments: try alternative infrastructures, evaluate them against goals, iterate. This is **engineering as a science** in Simon's exact sense. The experimental method needs no further methodological justification beyond Simon 1996.

## Notable concepts introduced

- **Inner / outer environment / interface.** The artifact as the interface between them.
- **Sciences of the artificial.** A category of science distinct from natural science.
- **Bounded rationality.** Decisions made under limited information, computation, attention.
- **Procedural rationality.** Rationality of the process given the bounds.
- **Satisficing.** Choosing an acceptable rather than optimal alternative.
- **Physical Symbol System Hypothesis.** Symbol systems are necessary and sufficient for general intelligence (with Newell).
- **Attention as the scarce resource.** The design problem in information-rich environments.
- **Hierarchy and near-decomposability.** Complex systems organise this way; this is *why* design is feasible.
- **Functional explanation.** Behaviour can often be explained by goal + outer environment, without inner detail.
- **Design as search.** Generation and evaluation of alternatives in a problem space.
- **Discounting the future for bounded rationality.** Our limited foresight is not adaptive but symptomatic of our limits.

## Concept-page reconciliation

1. **`wiki/concepts/framework-four-components.md`** — should explicitly invoke Simon's near-decomposability as the architectural justification. The four components are nearly-decomposable layers; this is *why* the framework is the right granularity. Proposed addition: a paragraph "Why four components? Simon (1996, Ch. 8) argues complex systems that survive are organised into nearly-decomposable hierarchies. The four-component split is the agent-infrastructure analogue."

2. **`wiki/concepts/agent-infrastructure-vs-capability.md`** — Simon's inner/outer environment dichotomy is the deep theoretical ground for separating infrastructure (outer) from model capability (inner). Should cite Simon Ch. 1 directly.

3. **`wiki/concepts/context-engineering.md`** — Simon (1996, Ch. 6, pp. 143-145) is the deep historical anchor for the attention-as-scarce-resource argument. Should be cited.

4. **`wiki/concepts/distributed-cognition.md`** (if it exists; created in the [[hutchins1995wild]] page) — Simon's view of human cognition as embedded in a symbol environment is the older, individualist counterpart to Hutchins's distributed view. The contrast is worth noting: Simon locates cognition in the symbol-processing system; Hutchins locates it across people + artifacts + environment. The thesis can use both.

5. **`wiki/concepts/deterministic-tools-hypothesis.md`** — Simon's feedback-and-homeostasis discussion (Ch. 6) is direct support: well-designed adaptive systems do not depend on accurate prediction; they use feedback. Tools providing deterministic feedback are exactly this pattern.

## Tensions and qualifications

- **Substrate independence is contested.** The PSS hypothesis is foundational but not universally accepted. The thesis can stand on it without committing to its strong form.
- **Hierarchy is a *tendency*, not a law.** Simon argues complex systems *tend to be* hierarchic because hierarchic ones survive; this is not a universal claim. Some complex systems (e.g., highly coupled physical systems) are not nearly decomposable. The thesis should not claim the four-component split is forced by Simon's argument; it should claim it is *consistent with* and *motivated by* it.
- **"Outer environment" can be over-emphasised.** The strong reading — "we can predict behaviour from outer environment alone" — risks ignoring real model-internals effects (capability ceiling, in-context learning quirks, prompt sensitivity). The thesis should adopt a *softened* version: outer-environment factors dominate productivity differences within a given model class.
- **Simon's economics is dated in places.** Some of the rational-expectations and management-information-systems references (Ch. 2, Ch. 6) reflect 1990s debates. The core concepts (bounded rationality, attention scarcity) are not dated.
- **The 1962 hierarchy paper is the most enduring contribution.** If the thesis cites only one Simon chapter, it should be Ch. 8 ("The Architecture of Complexity"). Ch. 1 and Ch. 5 are the next most useful.

## Connections

- [[hutchins1995wild]] — distributed cognition; Simon is the symbol-processing predecessor that Hutchins both inherits from and reacts against.
- [[norman2013design]] — design of everyday things; Norman is to Simon as design practice is to design science.
- [[ericsson1993deliberate]] — Simon and Ericsson collaborated on protocol analysis; the deliberate practice work descends from Simon's symbol-processing model of expertise.
- [[wallas1926art]] — the four-stage model of creativity is a pre-Simon proto-cognitive-architecture; Simon's bounded rationality + procedural rationality is what makes it implementable.
- [[kadavath2022know]] — Kadavath's self-evaluation findings are Simon's feedback-over-prediction principle applied to LLMs.
- [[kalai2024hallucinate]] — Kalai's lower bound is a constraint on the inner environment; the thesis's response (move things outside the LM via tools and retrieval) is a sciences-of-the-artificial design move.
- [[fielding2000]] — Fielding's *architectural style as named, coordinated constraints* is Simon's *artifact design under bounded rationality* applied to network-based software. REST is a sciences-of-the-artificial worked example.
- [[martin2026managed]] — Martin's brain/hands/session decomposition is Simon's near-decomposability applied to managed agents. The OS metaphor in the post is explicitly Simon-shaped.
- [[rajasekaran2025]] — Rajasekaran's *attention budget* framing is Simon's *attention as scarce resource* in agent-era language.
- [[karpathy2025wiki]] — the LLM Wiki pattern is Memex with the maintenance constraint lifted; Memex is one of Simon's 1990s-era references and a sciences-of-the-artificial archetype.
- Concept pages: [[framework-four-components]], [[agent-infrastructure-vs-capability]], [[context-engineering]], [[deterministic-tools-hypothesis]], [[distributed-cognition]].

---
*Ingested 2026-05-14. Read in full via docling conversion (chapters 1, 2, 5, 6, 8 in depth; chapters 3, 4, 7 skimmed). The full markdown conversion was deleted after synthesis per workflow.*
