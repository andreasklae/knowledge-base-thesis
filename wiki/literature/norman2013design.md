---
type: literature
citekey: norman2013design
title: The Design of Everyday Things (Revised and Expanded Edition)
authors: [Norman, Donald A.]
year: 2013
venue: Basic Books, New York
raw_path: raw/literature/Norman(2013).pdf
related_concepts: [framework-four-components, workspace-component, tools-component, calibration-thread, deterministic-tools-hypothesis, context-engineering]
related_work: [experiment-incubation, experiment-calibration]
status: summarized
ingested: 2026-05-14
updated: 2026-05-14
---

# Norman (2013) — The Design of Everyday Things (Revised and Expanded Edition)

## Summary

The foundational text of human-centred design, originally published 1988 as *The Psychology of Everyday Things*, comprehensively revised in 2013. Norman argues that **most "human error" is bad design**: when a coffee pot scalds the user, a door cannot be opened without a sign, or a refrigerator's temperature cannot be set despite years of trying, the fault lies not in the user but in a designer who failed to expose the right affordances, signifiers, mappings, constraints, and feedback. The book systematises the cognitive psychology of action (the seven-stage action cycle), error (slips vs. mistakes, the Swiss cheese model), and the design response (the six principles plus conceptual models). The 2013 edition adds substantial material on activity-centred design, the realities of business constraints (featuritis, design within schedule/budget), and a final chapter on design's moral obligations and the role of small empowered creators. The book is the canonical statement that **the locus of usability is the relationship between system image and the user's mental model** — not user training, not user intelligence, not user discipline.

## Main claims

### The fundamental principles (Chapter 1, codified in Chapter 2)

Seven fundamental principles of design, derived from the seven-stage action cycle:

1. **Discoverability** — it is possible to determine what actions are possible and what the current system state is
2. **Feedback** — full, continuous, and intelligible information about results of actions
3. **Conceptual model** — a coherent story about how the system works, projected by the design
4. **Affordances** — the relationship between the agent's capabilities and the object's properties that determines what actions are possible
5. **Signifiers** — perceivable signals that communicate what actions are possible and where (Norman's most important conceptual addition in the revised edition)
6. **Mappings** — the correspondence between controls and the things they control; ideally natural (spatial)
7. **Constraints** — physical, cultural, semantic, and logical limits on action that guide behaviour and reduce error

The critical clarification: **affordances are about possibility; signifiers are about communication of that possibility**. The cabinet door that springs open when pushed has an affordance (push) but no signifier; users pull it. The flat plate on a push-door is a signifier; the door's hinge structure provides the affordance.

### The seven stages of action (Chapter 2)

Goals lead to action through three execution stages (plan → specify → perform), and outcomes are evaluated through three evaluation stages (perceive → interpret → compare). Two gulfs separate the user from the system:

- **Gulf of Execution** — the gap between user intention and the means the system provides to act. Bridged by signifiers, constraints, mappings, and conceptual model (collectively: feedforward).
- **Gulf of Evaluation** — the gap between system state and the user's understanding of that state. Bridged by feedback and conceptual model.

### Three levels of processing (Chapter 2)

Borrowed from Norman's *Emotional Design*: every interaction triggers responses at three levels of brain processing, each tied to different stages of the action cycle:

- **Visceral** — automatic, biological, sub-conscious; immediate aesthetic and threat response. Tied to the perform/perceive stages.
- **Behavioural** — learned, skilled, sub-conscious; the locus of expectations and the satisfaction or frustration when expectations are confirmed or violated. Tied to specify/interpret.
- **Reflective** — slow, conscious, deliberative; the home of goal-setting, planning, and post-hoc judgment. Tied to plan/compare/goal. Reflective memory of an experience is more important than the experience itself, which is why a frustrating product with a great ending is remembered fondly.

### Knowledge in the head vs. in the world (Chapter 3)

Precise behaviour can emerge from imprecise knowledge by **distributing knowledge between the head and the world**. People do not remember the design of a penny, yet they use coins correctly, because the constraints of the environment (which coins exist, their physical differences) supply most of the discrimination work. Designers can deliberately shift the burden:

- Knowledge in the world: easy first encounter, requires no training, but visually demanding and inelegant.
- Knowledge in the head: efficient once learned, allows cleaner designs, but requires learning and is forgotten between uses.

The tradeoff governs the design of every interface. The hidden gesture menu is knowledge-in-the-head; the visible button is knowledge-in-the-world. Norman generally favours world-side, but acknowledges that experts prefer head-side once mastery is achieved.

### Constraints as design tools (Chapter 4)

Four kinds of constraints reduce the space of possible actions:

- **Physical** — the plug only fits one way (when designed properly)
- **Cultural** — red means stop, the senior person enters first
- **Semantic** — the rider faces forward on the motorcycle because that's what "riding" means
- **Logical** — if all other pieces are placed, the last piece has only one place to go

**Forcing functions** are constraints that prevent the next step until the current step is complete: interlocks (microwave door cuts power), lock-ins (save-before-quit dialog), lockouts (basement gate in stairwell prevents fire-fleeing residents from going past ground floor).

### Human error is design error (Chapter 5)

The book's most thesis-shaping chapter. Norman, drawing on James Reason and Jens Rasmussen, distinguishes:

- **Slips** — wrong action despite correct intention. Subdivided into:
  - **Action-based slips** (e.g., pouring coffee into the sugar bowl) — capture errors, description-similarity errors, mode errors
  - **Memory-lapse slips** — forgetting a step (leaving the original in the photocopier)
- **Mistakes** — wrong intention. Subdivided into:
  - **Rule-based** — invoking the wrong rule (the rule applies, but to a different situation)
  - **Knowledge-based** — incomplete or wrong knowledge of the domain
  - **Memory-lapse mistakes** — forgetting the goal or plan itself

Most accidents are not single events but **chains of latent failures aligning** ("Swiss cheese model" — each defence has holes; accidents happen when holes line up). Therefore: **the answer to error is never to blame the operator and re-train**. The answer is to redesign the system so the alignment cannot happen, or so that when one defence fails, others catch it.

Critical design implications:
- Eliminate the term *human error*; replace with *system error* or *communication failure*
- Provide undo wherever possible
- Confirm destructive actions, but make the *object* of the action (not the action itself) prominent in the dialog
- Use sensibility checks ("are you sure you want to administer 1000× the normal dose?")
- Apply forcing functions only at well-chosen points (nuisance kills compliance)
- Make modes visible; minimise modes where possible

### The four stages of human-centred design (Chapter 6)

Iterate through:

1. **Observation** (ethnographic field research with target users)
2. **Idea generation** (diverge widely; quantity over quality at this stage)
3. **Prototyping** (rapid, throwaway; "Wizard of Oz" methods are valid)
4. **Testing** (Nielsen's "five users" rule — five users in one round is more useful than fifty in one round, because iteration matters more than sample size)

The "double-diamond" model (British Design Council, popularised by Norman in this edition): first diverge to find the right problem (problem-finding), then converge on the problem definition; then diverge to find solutions (solution-finding), then converge on the chosen solution. Designers' instinct is **never to solve the problem as stated** — always question the framing first.

The chapter introduces *activity-centred design* as a corrective to over-individualised user-centred design: design for the activity (commuting, cooking) and the system will fit a wide range of individuals, rather than designing for "Persona Janet, 34, marketing executive" and producing something that only fits Janet.

### Design in business (Chapter 7)

The 2013 addition that gives the book its current relevance. Key themes:

- **Featuritis** (creeping featurism) — the disease whereby successful products accumulate features over each release cycle because the previous version was successful, the competition added features, and adding features is easier to justify than removing them. Result: products become unusable through bloat.
- **Norman's Law of Product Development** — "the day the product team is announced, it is behind schedule and over budget." HCD methods must accommodate brutal scheduling reality, not pretend it away.
- **Two innovation modes**:
  - Incremental — most successful innovation; hill-climbing within an existing paradigm
  - Radical — rare, slow, usually fails on first introduction; succeeds only when timing, technology, and market converge. Norman uses the videophone (conceived 1879, broadly adopted ~2010 via Skype/FaceTime) as the canonical example of how slow radical innovation actually is.
- **Standardisation** as the design principle of desperation — when no good design exists, standardise on a workable one (QWERTY, clock direction) and accept the loss of optimality for the gain of universal learnability.
- **Stigma in inclusive design** — designs marked as "for the disabled" or "for the elderly" are rejected by their target users. OXO's success: design tools that arthritis sufferers can use, but market them as better for everyone. Universal design wins by not being labelled universal design.

## Method / evidence

The book is a synthesis text, not a primary empirical study. Evidence comes from:

- Norman's own observation of design failures (the "Norman doors," the unsetable refrigerator, the Italian washer-dryer, the inscrutable digital watch) — the book is in large part a 25-year collection of detailed case observations
- Reference to the experimental cognitive psychology literature on memory, action, error (Nickerson & Adams on penny recognition; Reason on slip taxonomy; Rasmussen on skill/rule/knowledge-based behaviour)
- Reference to industrial accident investigations (Three Mile Island, KLM Tenerife crash, Air Florida bridge crash, F-22 oxygen incidents, Royal Majesty grounding)
- Reference to industrial practice (Toyota Production System's Jidoka, poka-yoke; NASA's Aviation Safety Reporting System; the Toyota "Five Whys")
- Norman's experience as VP of Advanced Technology at Apple, in particular advocating against the Sculley-era and post-Sculley product strategy

The method is **abstraction from observation, anchored in cognitive psychology, validated by industrial accident analysis**. The book does not present new experiments; it presents a vocabulary and a framework with which a designer can analyse any everyday object and identify what makes it good or bad.

## Relevance to this thesis

This book sits at the foundation of the thesis's design vocabulary. Specific connections:

- **[[framework-four-components]]**: Norman's seven design principles are about *how* to expose a workspace to a user. The framework's emphasis on the workspace as the primary site of intervention is consistent with Norman's emphasis on the system image as the locus of usability. Where Norman is about a human user interacting with a designed artifact, the thesis extends the same logic to an LLM agent interacting with a designed workspace. The translation is: signifiers in Norman → affordance metadata in tool descriptions; conceptual model → the documentation and context the agent receives; mappings → the relationship between agent actions and observable state.
- **[[workspace-component]]**: Norman's argument that "the difficulties reside in the design, not in the user" maps directly to the thesis's argument that agent productivity is bottlenecked by workspace design, not by model capability. When an agent fails to find a file, edits the wrong line, or runs the wrong command, the thesis's claim is that this is workspace error, not model error — the same move Norman makes for the door, the stove, and the photocopier.
- **[[tools-component]]** and the **[[deterministic-tools-hypothesis]]**: Norman's principle of *constraints* — physical, cultural, semantic, logical — is the conceptual ancestor of the deterministic tools hypothesis. A well-designed tool, in Norman's vocabulary, makes the wrong action physically or semantically impossible. The deterministic tools claim is the same idea applied to LLM agents: a tool with strong constraints (deterministic outputs, narrow input space, clear error states) makes agent error harder, much as Norman's well-designed lock makes user error harder.
- **[[calibration-thread]]**: The Gulf of Evaluation is the human-design analogue of LLM miscalibration. The agent (like the user) is uncertain about whether its action achieved the goal because the feedback is poor, delayed, or ambiguous. Norman's prescription — make feedback fast, salient, and intelligible — is one of the calibration thread's design moves at the workspace level. Where Norman talks about a user being unable to tell if the room temperature is being controlled by them, the thesis talks about an agent being unable to tell whether its edit succeeded.
- **[[context-engineering]]**: Norman's distinction between knowledge in the head and knowledge in the world is a precise framing of the context engineering problem. The agent's "head" is its context window plus its weights; the "world" is the file system, the tool outputs, the visible state. Designing for an agent is a question of how much knowledge to put in each, with the same tradeoffs Norman identifies (head-side is efficient once mastered but invisible and forgettable; world-side is robust but cluttered).
- **The Swiss cheese model** is directly relevant to the [[experiment-incubation]] design's failure analysis and to the broader thesis stance on error attribution. When an agent fails, Norman's framework says: do not blame the agent; find the chain of design defences that all failed, and add or thicken one of them. This is the disposition the thesis takes toward agent failure throughout.

The book is **the** source for the framing "blaming the user (here: the agent) is a category error; design the system to absorb the error." This framing structures most of the thesis's normative claims.

## Notable concepts introduced (for future routing)

- **Affordance / signifier distinction** (Norman, building on Gibson 1979) — affordance is the relationship; signifier is the communicated cue. The thesis should use *signifier* whenever it means "the part of the system that tells the agent what's possible," and reserve *affordance* for the underlying capability.
- **The seven-stage action cycle** — plan, specify, perform, perceive, interpret, compare, goal. Maps cleanly onto agent action loops and is useful as a checklist for "where can this fail?"
- **Gulfs of Execution and Evaluation** — the two gaps that good design closes. Directly applicable to agent-workspace interaction.
- **The three levels of processing** (visceral, behavioural, reflective) — less directly applicable to agents (which lack the visceral level), but the behavioural/reflective distinction maps onto the agent's fast pattern-matching vs. slow deliberation, and to the cost differential between cached/skill-based action and explicit reasoning.
- **Slips vs. mistakes** — slip is right intention, wrong action; mistake is wrong intention. For agents: slip is a tool call that does the wrong thing despite a correct plan; mistake is a wrong plan executed correctly. The thesis's analysis of agent failures should make this distinction.
- **Mode errors** — when an action means different things depending on hidden state. Highly relevant to agent design: modes are everywhere in modern agent harnesses (tool-mode vs. text-mode, planning vs. executing, dry-run vs. live), and they cause exactly the same class of error that Norman documents for human users.
- **The Swiss cheese model of accidents** — accidents are alignments of latent failures, not single causes. Should structure how the thesis discusses agent failures.
- **Forcing functions, lock-ins, interlocks, lockouts** — categories of constraints that prevent specific error classes. The thesis's discussion of safety-critical agent actions (file deletion, git push, financial transactions) should explicitly invoke these.
- **The double-diamond design process** — diverge-converge-diverge-converge. Useful for structuring the thesis's own design proposals.
- **Featuritis and the temptation to add** — directly relevant to LLM agent harness design, where the temptation is to add tools, modes, and capabilities rather than to design coherent restricted ones.
- **Norman's Law of Product Development** — "the day the product team is announced, it is behind schedule." Useful as a realism check whenever the thesis proposes a methodology that would slow down a real agent development team.
- **The stigma problem in inclusive design** — relevant if the thesis ever discusses making "easier" agent interfaces that might mark the user as less technically sophisticated.
- **Activity-centred design** as a corrective to over-personalised user-centred design — relevant to the question of whether agent design should target individual developers or the activity of software engineering writ large. Probably the latter.

## Tensions and qualifications

- **Norman writes for humans, not agents.** The translation from human user to LLM agent is mostly clean but not exact. Agents do not have a visceral level; agents do not get fatigued in the same way; agents do not have the same kind of long-term memory; agents do not feel the emotional weight of a failed expectation in the same way a frustrated user does. The thesis should be careful not to over-apply the human-cognitive framework to entities whose cognitive architecture is very different. In particular, Norman's emphasis on aesthetic design (visceral level) and emotional response is almost entirely irrelevant to agent productivity; the thesis should not import this without explicit justification.
- **Norman's "designer" is a single intelligent author.** In the thesis context, the designer of an agent's workspace is rarely a single person; it is the accreted result of many developers, framework authors, and the agent itself making changes during execution. Norman's design principles are still useful, but the agency-of-design question is more diffuse for agent workspaces than for, say, a coffee pot.
- **Norman is sceptical of users learning their way out of bad design.** The thesis position is more mixed: agents *can* learn from documentation and prior experience in ways that humans, at scale, often cannot. The thesis should not import Norman's full pessimism about learning; the question of what an agent can be taught vs. what must be designed in is a real one, and Norman's framework, taken whole, biases too hard toward "design it in."
- **Norman's case studies are nearly all about single-user, single-device interaction.** The thesis's setting (an agent in a workspace, interacting with code, tools, documentation, and possibly other agents over hours-to-days) is more like Norman's brief discussion of "distributed cognition" (citing Hutchins) than like his canonical Stove Control example. The thesis may need to lean more on the distributed cognition tradition (which Norman gestures at but does not develop) than on Norman himself for the multi-agent, multi-tool case.
- **Norman's chapter on business (Chapter 7) is mostly orthogonal to thesis concerns.** The thesis is not about products in markets; it is about an open research question. The business material is useful background but should not drive thesis structure.
- **The 2013 edition's optimism about "the rise of the small"** (the closing section) reads as dated in 2026. The actual trajectory has been the opposite: concentration of AI/agent capability in a small number of large labs, with individual creators tooling on top rather than building from scratch. The thesis should note this gap when citing Norman's predictions.
- **Norman's signifier vs. affordance distinction has not been universally adopted** in the design community. Many writers still use "affordance" to mean what Norman now calls "signifier." The thesis should pick one usage and stick to it; recommending Norman's 2013 vocabulary for clarity.

## Concept-page reconciliation

**[[framework-four-components]]** does not currently cite Norman explicitly, though the framework is clearly built on his vocabulary. The concept page should be updated to acknowledge that *workspace*, *tools*, *skills*, and *data* are most cleanly understood through Norman's signifier/affordance/conceptual-model frame, with each component being a different surface through which the agent encounters the world.

**Proposed concept-page edits (not applied):**

1. In `wiki/concepts/framework-four-components.md`, under "Theoretical grounding," add:

   > The four-component framework can be read as a Norman-style design taxonomy applied to LLM agents. Where Norman analyses how a human user encounters a designed artifact through signifiers, mappings, and feedback, the four components specify the corresponding surfaces for an agent: the workspace provides the signifiers and the state visibility (Norman's "system image"); tools provide the affordances; skills are the agent's learned mappings between intentions and tool sequences (Norman's "behavioural-level skill"); data are the world-side knowledge the agent does not need to keep in context. The thesis's claim that infrastructure is the productivity bottleneck is, in Norman's terms, the claim that signifier and feedback quality dominate agent capability — exactly the move Norman makes for human users.

2. In `wiki/concepts/workspace-component.md`, under "Why the workspace matters," add:

   > Norman (2013) argues that the design of the system image — the totality of what the user can perceive about the system's state and possibilities — is where usability lives, not in user training. The thesis's emphasis on workspace design over agent training is the same argument, extended to a non-human user. When an agent fails, the workspace's signifiers, feedback, and conceptual model are the first place to look, not the agent's prompt or weights.

3. In `wiki/concepts/calibration-thread.md`, under "Mechanisms for improving calibration," add:

   > Norman (2013) frames poor calibration as a Gulf of Evaluation problem: the user (or agent) cannot tell whether the action produced the intended outcome because feedback is missing, delayed, or ambiguous. Closing this gulf — through fast, salient, intelligible feedback at every action step — is one of the workspace-level interventions the calibration thread proposes. The Norman framing makes clear that calibration is not primarily a property of the agent; it is a property of the agent's environment.

## Connections

- [[simon1996artificial]] — the deeper theoretical foundation Norman builds on (the science of design, the externalisation of cognition). Norman is the popular, practitioner-facing distillation; Simon is the philosophical underpinning.
- [[hutchins1995wild]] — distributed cognition, which Norman explicitly cites but does not develop. Hutchins is the more rigorous source for the multi-agent, multi-tool case that the thesis actually inhabits.
- [[ericsson1993deliberate]] — Norman's overlearning/automaticity discussion (Chapter 2) is the cognitive-psychology side of the same phenomenon Ericsson studies as deliberate practice. Both agree that skill, once automated, is fast and subconscious; both agree that learning it requires sustained, effortful attention.
- [[wallas1926art]] and [[sio2009incubation]] — less direct, but Norman's discussion of the reflective level of processing (Chapter 2) and the value of stepping back from a problem connects loosely to the incubation literature.
- [[framework-four-components]] — the thesis's central organising structure, which inherits Norman's design vocabulary throughout.
- [[experiment-incubation]] — the Swiss cheese model in Chapter 5 is the appropriate analytical frame when interpreting why an agent fixates: it is rarely one cause, it is the alignment of several.
- [[aizawa2025tools]] — Norman's *signifiers* and *affordances* are the cognitive-design vocabulary behind Aizawa's tool-description and namespacing principles. Tool names, parameter names, and response shapes are signifiers that route agent action; bad tool design is a gulf-of-execution problem.
- [[zhang2025]] — Agent Skills' *progressive disclosure* is Norman-shaped: the description field is a *signifier* of when to load the body. Norman's design principles translate cleanly to agent-facing infrastructure.
- [[fielding2000]] — Fielding's *uniform interface* + *self-descriptive messages* constraints are Norman's *visibility of state* and *feedback* principles applied to network protocols. REST is design-of-everyday-things for distributed systems.
- [[rajasekaran2025]] — Norman's *minimise gulf of execution* principle is the cognitive-science antecedent of just-in-time retrieval: don't make the agent traverse stale indexes; expose the discovery primitives (glob, grep, ls) directly.

---
*Ingested 2026-05-14. Full book read end-to-end including all seven chapters, the preface to the revised edition, and the closing acknowledgements and notes.*
