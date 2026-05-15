---
type: literature
citekey: hutchins1995wild
title: Cognition in the Wild
authors: [Hutchins, Edwin]
year: 1995
venue: MIT Press, Cambridge MA
raw_path: raw/literature/Hutchins(1995).pdf
related_concepts: [distributed-cognition, framework-four-components, workspace-component, tools-component, context-engineering]
related_work: [experiment-incubation, experiment-calibration]
status: summarized
ingested: 2026-05-14
updated: 2026-05-14
---

# Hutchins (1995) — Cognition in the Wild

## Summary

A 400-page ethnography of how a US Navy ship's navigation team computes its position, used as a vehicle for the most rigorous theoretical statement available of **distributed cognition**: the claim that cognitive systems are properly bounded not by the skin of an individual but by the functional unit of people, tools, representations, and social organisation that together propagate representational state to a useful end. The book's central technical move is to treat David Marr's three levels of analysis (computational, representational/algorithmic, implementational) as applying not to a brain but to a *sociotechnical system* — a navigation bridge with quartermasters, charts, pelorus instruments, a fathometer, a bearing log, and an organisational hierarchy. The book's central polemical move is to argue that **mainstream cognitive science systematically mistook the properties of socio-cultural systems for the properties of individual minds**, because Turing modelled a person interacting with material symbols on paper, then later research forgot the paper and the person and put the symbols inside the head. Hutchins's claim is that this was a deep error, that "the computer was made in the image of the *sociocultural system*, and the human was remade in the image of the computer," and that recovering an honest account of human cognition requires putting cognition back into the world.

For this thesis the book is foundational: it is the cleanest available argument that the unit of analysis for cognitive work should be the agent-plus-environment, not the agent alone. This is the conceptual move the thesis makes for LLM agents.

## Main claims

### Cognition is a property of systems larger than the individual

The book's central claim, repeated and demonstrated chapter by chapter. The navigation bridge of the USS *Palau* (pseudonym) performs computations no individual aboard could perform alone. Fixing the ship's position requires:

- A pelorus operator on each wing taking visual bearings on landmarks
- A bearing-taker recording those bearings in a log book
- A plotter transferring the bearings to a chart and intersecting them
- A fathometer operator continuously calling out depth
- A quartermaster of the watch supervising and maintaining the log
- A navigator overseeing all of this
- The chart itself, which is not a passive surface but an active representational medium that pre-computes the geometry of bearing-intersection
- The compass rose, the parallel rulers, the dividers, the gyrocompass repeater
- The shared lexicon ("LOP," "fix cycle," "true bearing")
- The standing watch organisation that makes all this scheduled, redundant, and survivable across watch changes

None of these elements alone has the cognitive property "knows where the ship is." The property emerges from the coordinated propagation of representational state across them. **Cognitive properties of the system are not predictable from the cognitive properties of its individual members** (p. 175ff).

### Computation as propagation of representational state across media

Hutchins's technical re-framing. Instead of "computation as symbol manipulation inside a head," he proposes "computation as the propagation of representational state across a structured set of representational media." A bearing taken on the wing becomes a number called out, which becomes an entry in a log, which becomes a line drawn on the chart, which becomes an intersection that becomes the ship's position. Each transformation is a computational step, and most of them happen *outside* any individual's head. The framing dissolves the inside/outside boundary as the primary unit of cognitive analysis. Inside-the-head processes are one kind of representational medium among several, distinguished by being biological and partly private, but not by being the *locus* of cognition.

### The three Marr levels apply to the system, not the individual

A core methodological argument (Chapter 2). The computational-level description of ship navigation — what gets computed, why, and what constraints the computation must satisfy — applies identically to modern Western pilotage, to traditional Micronesian wayfinding, and to medieval European dead-reckoning. The systems differ at the *representational/algorithmic* level (Western navigators encode the world in geographic-coordinate charts; Micronesians encode it in star paths and reference islands) and at the *implementational* level (which media carry which representations: paper, memory, body posture, song). The substantive variation across human cultures is at the lower two levels; the computational problem of "where am I, where am I going, what do I need to do to get there" is universal.

### The artefactual environment is itself cognitive infrastructure

Chapter 3 demonstrates in detail that navigation tools are not memory aids; they are *cognitive infrastructure that does part of the computation*. The chart pre-computes the geometry of bearing-intersection. The Mercator projection pre-computes the relationship between heading and ground track. The compass rose pre-computes the addition of variation and deviation. The pelorus pre-computes the alignment of a sight line with a reference axis. Generations of accumulated structure in the tools encode partial solutions to recurring problems, so that when a quartermaster takes a bearing they do not have to re-derive the geometry from first principles. Hutchins states: **"Humans create their cognitive powers by creating the environments in which they exercise those powers"** (p. 169).

### The Palau breakdown: a worked example of distributed cognition under stress

Chapter 1 opens with a vivid 25-minute incident: the *Palau*'s steam plant fails as the ship enters San Diego harbor at 10 knots. The ship loses propulsion, electrical power, rudder control, communications, and its steam horn. The navigation team, augmented by the captain and the bridge officers, brings the ship safely to anchor through a sequence of distributed adaptations: manual rudder control from after-steering, hand-cranked foghorn from the flight deck, captain's voice over the flight-deck PA to warn a sailboat. No individual could have managed this; the team adapts as a system, including a re-division of cognitive labour around the modular arithmetic of the bearing computation that none of the individuals fully represents. The chapter is the book's existence proof that *system-level adaptation can occur without any individual having a system-level model of what is being adapted*.

### Learning as the propagation of organisation through an adaptive system (Chapters 6–8)

Hutchins's account of how novice quartermasters become expert is anti-individualistic. The "context of learning" is not a curriculum; it is the structured task environment in which the novice progressively takes on more and more of the propagation work as their internal organisation comes into coordination with the external structure they are interacting with. Learning is the gradual internalisation of patterns that were already in the world. This dovetails with the broader claim that **symbols are in the world first, and only later in the head** (p. 370). The novice does not first internalise symbols and then learn to use the chart; they first learn to use the chart, and the internal symbolic structure emerges as a residue of that interaction.

Chapter 8 extends this to *organisational* learning: the *Palau*'s navigation team, faced with a change in the deviation table mid-passage, reorganises its division of labour in a way that no single member designed. Some members propose local fixes ("Here, you add these"); the global reorganisation emerges from the local interactions. **The solution is discovered by the organisation before it is discovered by any of the participants** (p. 364). The cost of this evolutionary mode is that the solution is not always saved — when the watch crew rotates off the ship, the discovered routine may not be preserved.

### The polemical history of cognitive science (Chapter 9)

The book's most ambitious move. Hutchins offers a counter-history of cognitive science. The standard story is: cognitive science discovered that the mind is a symbol-processing computer, took the digital computer as its model, and made progress. Hutchins's counter-story: Turing's original insight came from observing **himself** doing mathematics — manipulating physical symbols on paper with his eyes and hands. Turing then *abstracted away* the person and the paper to isolate "the essence of the manipulation of symbols." This was a description of the *socio-cultural system* of a mathematician-plus-paper, not of an individual mind. When cognitive science later took this abstracted symbol-manipulation as the model *of* mind, it imported the architecture of an external socio-cultural system into the head, lost the eyes, hands, paper, and emotions in the process, and then spent forty years trying to explain how an isolated head could do what a person-plus-environment had originally been doing.

This is, in Hutchins's framing, why cognitive science has had such trouble integrating perception, motor action, emotion, culture, and context: these were precisely what was discarded when the system-level abstraction was imported as a description of the individual. Searle's Chinese Room thought experiment, Hutchins argues, is correctly read not as a refutation of strong AI but as an unwitting demonstration that the cognitive properties of the room (which speaks Chinese) are not the cognitive properties of the person in the room (who does not).

## Method / evidence

Cognitive ethnography. Hutchins spent extended periods aboard US Navy ships as a civilian researcher at the Navy Personnel Research and Development Center, observing navigation teams, recording interactions on audio tape, and transcribing them. The book is built around extensive transcripts of bridge dialogue, photographs of chart-table work, and detailed analyses of specific bearing-fix cycles. The Micronesian comparison material comes from Thomas Gladwin's *East Is a Big Bird* (1970) and Hutchins's own work in the Caroline Islands.

The methodological novelty is not the ethnographic method itself but the choice to study cognition through an ethnographic lens at all. Hutchins is explicit (Chapter 9) that "the laboratory studies cognition in captivity, and the everyday world studies cognition in its natural habitat" — a deliberate biological-ecological framing. He treats the navigation team as the natural unit of cognitive analysis, in the same way an ecologist would treat a coral reef rather than a single polyp.

The evidence base is one ship, one navigation team, one extended period of observation, plus secondary literature on other navigation traditions. This is N=1 ethnography. The book's reliance is on *depth and theoretical articulation* rather than statistical generalisation. The argument's force comes from how well the framework reorganises one's understanding of a domain where the cognitive work is unambiguously real (the ship really does need to know where it is, and people really do work out where it is together), not from large samples.

## Relevance to this thesis

This is the most directly load-bearing single source for the thesis's overall framing. The thesis claim is that LLM agent productivity is bottlenecked by infrastructure rather than by the agent itself; Hutchins's claim is that human cognitive performance is *constituted* by infrastructure, not just supported by it. The conceptual translation is almost mechanical.

Specific connections:

- **[[framework-four-components]]**: The four components (workspace, tools, skills, data) are most cleanly read as *the elements of a distributed cognitive system around an LLM agent*, in Hutchins's sense. The workspace is the medium across which representational state propagates; the tools are the structured artefactual environment that pre-computes parts of the task; the skills are the agent's internalised coordination with that environment; the data are the historical residua of past propagations available for re-coordination. The framework, viewed through Hutchins, is not "what an agent needs to do work" but "what *system* does work, of which the agent is one component." This reframing should be made explicit on the concept page.
- **[[workspace-component]]**: Hutchins's Chapter 3 is the strongest available source for the thesis claim that the workspace is *itself doing cognitive work*. The chart is not where the navigator stores information; the chart is computing geometry on behalf of the navigator. By analogy, the agent's workspace is not where the agent stores context; it is computing structure on the agent's behalf, through directory hierarchies, tool descriptions, error messages, type signatures, version-control state, test results, etc. The thesis's claim that workspace design is the locus of intervention is essentially Hutchins's claim about charts, applied to file systems and tool harnesses.
- **[[distributed-cognition]]**: This concept page, if it does not already exist, should be created with Hutchins as the canonical source. The concept is the intellectual ancestor of essentially every claim in the thesis about why agent capability is the wrong unit of analysis.
- **[[tools-component]]**: Hutchins on the navigation tools (compass rose, parallel rulers, pelorus, chart) is the strongest available philosophical foundation for the thesis's claim that tools are not just affordances but *carriers of accumulated cognitive structure*. The deterministic tools hypothesis is in part the claim that LLM tools should carry as much accumulated structure as possible (in their type signatures, error messages, idempotence guarantees), because then the agent has to do less internal computation. This is exactly Hutchins's "humans create their cognitive powers by creating the environments in which they exercise those powers."
- **[[context-engineering]]**: Hutchins's claim that "symbols are in the world first, and only later in the head" is directly relevant. Context engineering, in his framing, is the management of which representational structures live in the world (in files, in tool outputs, in the screen) versus in the head (in the context window, in the agent's working state). The dual-coding tradeoff the thesis discusses is a special case of Hutchins's general analysis of how distributed cognitive systems allocate work across media.
- **[[calibration-thread]]**: Less directly, but Hutchins's Chapter 5 on communication and Chapter 6 on learning offer mechanisms by which feedback in a distributed system can keep the individual elements calibrated to the system's state. The "publishing" of intermediate computations between bearing-taker and plotter (described in Chapter 8) is a feedback mechanism in exactly the sense the calibration thread cares about: each member's representation of the joint state is kept honest by the structure of inter-member communication.
- **[[experiment-incubation]]**: Hutchins's account of how a navigation team reorganises its division of labour under stress (Chapter 8) is suggestive for the thesis. The team's solution to a novel sub-problem (modular addition of bearing corrections) emerges not from any individual's deliberation but from a sequence of local accommodations. If the thesis incubation experiment is partly about an agent stepping back to let structure re-emerge, Hutchins offers a model where the structure is *in the environment*, not in the head, and "stepping back" is really "letting the environmental structure reorganise itself through local interaction." This is a different mechanism than Sio & Ormerod's selective forgetting, and may suggest a different experimental design.

The book is **the** source for the framing claim that the agent is not the right unit of analysis. The thesis should cite it whenever it makes this move, not just because it is influential but because Hutchins makes the argument far more rigorously than anyone else.

## Notable concepts introduced (for future routing)

- **Distributed cognition** as a theoretical position. Cognition is not located inside individual heads but is a property of functional systems that include people, tools, and representations.
- **Propagation of representational state** as the unit of cognitive analysis. Replaces "symbol manipulation" as the basic move; symbol manipulation is one special case.
- **Computation across media** with media including: human memory, written records, spoken utterances, drawings on charts, instrument readings, body postures, social structures of authority and turn-taking. All are representational media.
- **The cognitive ecology** — the structured environment of representations that supports thinking. Internal cognition adapts to fit this ecology; the ecology accumulates structure across generations.
- **Cognitive ethnography** as a research method: detailed observation of how cognitive work actually gets done in real settings, as a corrective to laboratory studies that treat cognition as an individual mental act.
- **The Marr-levels-applied-to-systems move**: computational, representational/algorithmic, and implementational levels apply to a navigation bridge as a whole, not to any single brain in the bridge.
- **The Chinese Room as a distributed system**: Searle's thought experiment is correctly read as evidence that the system "Searle plus rulebook plus baskets of characters" speaks Chinese even though no element of it does. Hutchins inverts Searle's intended conclusion.
- **Symbols are in the world first** — ontogenetic claim. The infant learns to use external symbol structures (numerals on a page, words spoken aloud) before internalising them; "internal symbol manipulation" is the late accomplishment, not the prior architecture.
- **The cost of misidentifying system boundaries**: when cognitive science put symbols inside the head and bounded the cognitive system at the skin, it inevitably had to invent internal apparatus to do the work that was previously done by the environment. This produced overattribution of internal structure and the persistent failure to integrate perception, action, and emotion.
- **Learning as adaptation in a dynamic system**: the novice does not acquire symbolic knowledge and then learn to use it; the novice progressively internalises coordinations with the external environment that they have been doing all along.
- **Organisational learning without representation**: the team can collectively discover a better division of labour without any team member having a representation of the new division. This challenges classical organisational theory (Cyert, March, Chandler) which assumes change is driven by representational design.
- **Cultural evolution as accumulated cognitive structure in artefacts**: charts, compasses, log books, etc., are the precipitate of generations of distributed cognitive work, and their structure is therefore part of what enables present cognitive performance.
- **The "physical symbol system hypothesis" as a description of socio-cultural systems**: Newell and Simon's central hypothesis is not wrong, Hutchins argues, but it is a description of the wrong thing — it describes a person-plus-paper, not a brain.

## Tensions and qualifications

- **Hutchins's argument is theoretical, not predictive.** The book does not claim that taking the distributed-cognition stance lets you predict any specific outcome that the standard cognitive-science stance cannot. It claims that the distributed stance correctly describes a phenomenon (collective cognition on the bridge) that the standard stance gets wrong. The thesis should not over-claim what distributed cognition *does for you* in the agent setting; what it does is correctly bound the problem.
- **N = 1.** The book is built on one ship, one team, and adjacent literature on other navigation cultures. Hutchins is candid about this; he calls Chapter 1 "an existence proof." The thesis should not cite Hutchins as providing statistical evidence for any claim; he provides conceptual evidence and a worked-out vocabulary.
- **The book's polemic against mainstream cognitive science is dated in places.** The hostile reading of symbol-processing AI was directed at 1980s and early 1990s GOFAI. Modern LLMs are not symbol-processing systems in the sense Hutchins criticises; they are sub-symbolic statistical learners with emergent capacities. The historical argument about how symbols got inside the head still stands, but the modern AI landscape Hutchins's framing maps onto is the *combination* of an LLM (a non-symbolic core) with a symbolic infrastructure (file system, tools, scripts) — which is, satisfyingly, exactly the Hutchins-style hybrid he would have predicted is necessary.
- **The book underweights the speed at which cognitive ecologies can change.** Hutchins's examples are slow: chart conventions accumulated over centuries, watch-team practices over decades. The thesis is concerned with cognitive ecologies (agent + workspace) that change month to month or week to week. This is a real difference in time-scale, and the thesis should be careful when importing Hutchins's account of cultural-evolutionary slowness — agent workspaces evolve far faster than human navigation practice ever did.
- **The book does not address artefactual cognition where the artefact is itself learning.** All of Hutchins's representational media are passive: the chart does not learn, the pelorus does not learn, the log book does not learn. The agent setting introduces a new case where the central element of the system *is* learning, possibly within a single task. Hutchins's framework does not break under this, but it does not pre-anticipate it either, and the thesis should be explicit about what changes when a representational medium has its own internal model.
- **Distributed cognition has a soft research programme.** Twenty-five years after publication, the field that Hutchins inaugurated has produced some good ethnographies (Goodwin, Latour, Star) and a vocabulary that has spread widely, but it has not produced robust design heuristics. The thesis should be honest that adopting Hutchins's framing is conceptually clarifying but does not, by itself, tell you what to build.
- **The Norman parallels.** [[norman2013design]] and Hutchins worked together at UCSD; Hutchins's distributed cognition and Norman's user-centred design are sibling research programmes. The thesis will get the most mileage by using them together: Norman for the *design principles* operating on the agent-workspace interface, Hutchins for the *unit-of-analysis claim* that the interface is where the cognitive work actually lives.

## Concept-page reconciliation

The existing concept layer was written without direct engagement with Hutchins, but [[framework-four-components]] and [[workspace-component]] in particular are quietly Hutchinsian in their assumptions. Making this explicit would strengthen the conceptual foundations.

**Proposed concept-page edits (not applied):**

1. Create a new concept page `wiki/concepts/distributed-cognition.md` with Hutchins as the primary source and Norman as a secondary one. The page should articulate the central claim that the unit of analysis for cognitive work is the agent-plus-environment system, and should link to all four components of the framework as instances of the distributed-cognition view.

2. In `wiki/concepts/framework-four-components.md`, under "Why these four," add:

   > The four components reflect a distributed-cognition view of agent work (Hutchins 1995). The agent is not the bounded cognitive system; the system includes the workspace through which representational state propagates, the tools that pre-compute parts of the task, the skills that are the agent's learned coordination with that environment, and the data that are the historical residua of past propagations. The framework's claim that infrastructure is the bottleneck is the claim that the non-agent elements of the distributed system carry most of the cognitive load, and that their design therefore dominates outcomes.

3. In `wiki/concepts/workspace-component.md`, under "What the workspace is doing," add:

   > Hutchins (1995, Chapter 3) argues that the artefactual environment of a cognitive task — the chart, the log book, the instruments — is not a passive support for cognition but an active participant: it pre-computes geometry, accumulates state across time, and enforces coordination across human team members. The agent's workspace plays the same role. File hierarchies pre-compute relevance; tool descriptions pre-compute affordances; type signatures pre-compute constraints. The workspace is doing cognitive work; the agent's job is to coordinate with the workspace's structure, not to derive that structure from scratch each turn.

4. In `wiki/concepts/tools-component.md`, under "Tools as accumulated structure," add:

   > Hutchins's analysis of navigation tools shows that each generation of practitioners adds structure to the tool that captures partial solutions to recurring problems. The compass rose, the chart projection, and the pelorus are not memory aids; they are externalised cognition. The thesis's claim that good tools for agents should carry as much accumulated structure as possible is a direct application: tools that bake in idempotence, return informative errors, validate inputs at the boundary, and expose narrow interfaces are tools that have *taken on cognitive work* that the agent would otherwise have to do.

## Connections

- [[norman2013design]] — Norman and Hutchins were colleagues at UCSD; the books are sibling treatments of the same underlying view from different sides (design principles vs. unit-of-analysis claim). Cite together.
- [[simon1996artificial]] — Simon's *Sciences of the Artificial* is the deeper philosophical source for the claim that human cognitive performance is the result of an externalised, designed environment. Hutchins criticises Simon's "physical symbol system" formulation but inherits much of his framework. Read in sequence: Simon for the meta-claim about artefacts, Hutchins for the ethnographic substantiation.
- [[wallas1926art]] — distantly related; Wallas's stages are about an individual mind, but the social-context turn in his later work (about deliberate use of preparation, incubation, illumination across a *career*) is sympathetic to Hutchins's longer time-scales of cultural learning.
- [[ericsson1993deliberate]] — Ericsson is about how individual skill emerges from sustained practice; Hutchins is about how individual skill is constituted by participation in a structured environment. The two views are complementary; the thesis should use them together for the question of how an agent develops skill.
- [[distributed-cognition]] — proposed new concept page, with this source as primary.
- [[framework-four-components]] — should be re-grounded explicitly in Hutchins's view.
- [[workspace-component]] — should cite Hutchins on artefactual cognition.
- [[tools-component]] — should cite Hutchins on accumulated structure in tools.
- [[experiment-incubation]] — Hutchins's account of organisational adaptation suggests an additional mechanism the experiment could examine: the team-level rather than individual-level reorganisation.
- [[karpathy2025wiki]] — the LLM Wiki is a worked instance of a distributed-cognitive system: raw sources, LLM-maintained synthesis, and a co-evolved schema together carry knowledge work neither human nor LLM could carry alone. The thesis's own knowledge base implements the pattern.
- [[rajasekaran2025]] — Rajasekaran's just-in-time retrieval is Hutchins-shaped: agents read folder hierarchies, file names, and timestamps the way navigators read charts and instruments. The line *"mirrors human cognition: we generally don't memorize entire corpuses of information, but rather introduce external organization and indexing systems"* makes the inheritance explicit.
- [[martin2026managed]] — Martin's harness/session/sandbox decomposition makes distributed cognition explicit at the agent-architecture layer: the session is the externalised state record; the sandbox is the structured environment; the harness is the coordination layer.

---
*Ingested 2026-05-14. Full book read end-to-end via docling conversion to markdown; key chapters (1, 2, 3, 6, 7, 8, 9) read in detail; chapters 4 and 5 sampled.*
