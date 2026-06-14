---
type: concept
sources: [simon1996artificial, hutchins1995wild, norman2013design, karpathy2025wiki, rajasekaran2025]
related_concepts: [framework-four-components, workspace-component, agent-infrastructure-vs-capability, data-component]
related_work: []
status: draft
updated: 2026-05-15
---

# Distributed Cognition

The intellectual lineage the thesis draws on for the claim that productivity is a property of the agent-environment pair, not of the agent alone.

## Simon: the ant on the beach

[[simon1996artificial]] makes the foundational version. An ant traverses a beach. Its path is irregular and complex: it angles around pebbles, climbs dunes obliquely, detours around obstacles, and only loosely aims toward home. Sketched on paper, the path looks like the trace of a sophisticated problem-solver. Simon's point: the complexity of the path is not evidence of complexity in the ant. The ant is a relatively simple system following a few local rules; the apparent sophistication is a reflection of the *complexity of the beach*.

The same principle extends to human cognition. A great deal of what looks like inner cognitive sophistication is in fact the structure of the environment doing the work, with the cognitive system navigating that structure rather than reproducing it internally. Productivity is a property of the agent-environment pair. Improving the structure of the environment is often a more tractable lever than improving the cognitive system acting within it.

This is the foundational warrant for [[agent-infrastructure-vs-capability]] and for the framework in [[framework-four-components]].

## Hutchins: cognition in the wild

[[hutchins1995wild]] develops the empirical and systems-level version. In his study of naval navigation, he describes a distributed cognitive system in which trained practitioners, charts, instruments, procedures, and representational transformations jointly carry the work. Cognitive performance is helped by distributing cognitive labour across skilled humans, specialised tools, and external representations that preserve and transform state. The structure accumulated in the tools of the trade is part of the explanation. A person using a tool can become a local functional system with capabilities neither has alone.

For agents, this maps directly onto [[workspace-component]] (the workspace as the carrier of distributed state) and onto the framework's general claim that productivity decomposes into the affordances the surrounding system provides.

## Norman: affordances and cognitive artifacts

[[norman2013design]] provides the bridge from cognitive science to interface and tool design. Cognitive artifacts, affordances, and mental models explain how humans routinely accomplish tasks by leaning on environmental structure rather than by fully understanding the underlying mechanism. This is the human analogue of the infrastructure argument: productivity improves when the environment exposes the right actions clearly, stores state externally, and reduces what must be held in working memory.

Norman is therefore directly relevant not only to tools in the narrow sense, but also to workspace design and to the broader ergonomics of agent harnesses.

## Why this reference set

These are not the conventional references for a thesis on AI systems, which is part of the point. If the productivity metaphor is correct, the next decade of AI engineering is likely to draw at least as much on cognitive science, human factors, and organisational design as on machine learning.

## Contemporary instantiations

Two recent industry sources name the same idea in agent-specific terms:

- [[rajasekaran2025]] explicitly invokes the lineage: *"mirrors human cognition: we generally don't memorize entire corpuses of information, but rather introduce external organization and indexing systems like file systems, inboxes, and bookmarks to retrieve relevant information on demand."* Just-in-time retrieval — `glob`/`grep`/file metadata as routing signals — is Hutchins' distributed cognition operationalised for agents.
- [[karpathy2025wiki]] closes its argument with the historical precedent: Vannevar Bush's Memex (1945) was a Hutchins-style distributed cognitive system *whose binding constraint was maintenance*. Agents lift that constraint; the human-plus-LLM-plus-files system the LLM Wiki proposes is a working distributed-cognitive architecture for knowledge work.

---
*Framing drawn from `../../manuscript-notes/essay-pointer.md` (Essay/essay.tex §2.4).*
