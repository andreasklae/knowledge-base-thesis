---
type: concept
sources: [martin2026managed, simon1996artificial, hutchins1995wild, rajasekaran2025, karpathy2025wiki]
related_concepts: [framework-four-components, distributed-cognition, calibration-thread, incubation-as-infrastructure, data-component, context-engineering]
related_work: [experiment-incubation, experiment-chess]
status: draft
updated: 2026-05-13
---

# Workspace Component

The workspace is the environment in which the agent acts. Three properties matter.

- **Bounded consequences.** Actions are reversible or contained; mistakes do not propagate to the world outside the workspace until explicitly promoted.
- **Observable state.** The agent can see what its actions have done. State is externalised, not held only in working memory.
- **Persistent history.** Prior actions remain referenceable; the workspace records what was done so future actions (in this session or a later one) can build on or revise it.

## Relation to Martin et al.

[[martin2026managed]] split managed agents into harness, session, and sandbox. This thesis's workspace component is closest to their sandbox; their session — the append-only log of what happened — is the workspace's persistent-history property as an artefact. The harness sits outside the framework: it is the orchestration infrastructure inside which these affordances are exposed to the model.

## Relation to distributed cognition

[[simon1996artificial]]'s ant on the beach is the foundational version of the point. The complexity of the ant's path reflects the structure of the beach, not internal complexity of the ant. The same principle applies to agents: a great deal of what looks like inner cognitive sophistication is the structure of the environment doing the work. Productivity is a property of the agent-environment pair, and improving the structure of the environment is often a more tractable lever than improving the cognitive system acting within it. See [[distributed-cognition]] for the fuller Simon/Hutchins/Norman synthesis.

## Calibration role

Workspaces verify by letting actions have observable consequences. A claim made and then refuted by the workspace's response is a calibration signal the model could not generate on its own. See [[calibration-thread]].

## Filesystem as routing infrastructure

[[rajasekaran2025]] makes the operational point explicit: in a workspace, *metadata is routing*. Folder hierarchies, naming conventions, timestamps — `test_utils.py` in `tests/` means something different from `test_utils.py` in `src/core_logic/` — all function as discovery signals that the agent reads progressively rather than as a flat preloaded payload. This is *just-in-time retrieval* at the workspace layer: hold lightweight identifiers, load on demand via `glob`/`grep`/`head`/`tail`. The line *"mirrors human cognition: we use external organization and indexing systems"* makes the [[distributed-cognition]] connection explicit.

## The LLM Wiki as a workspace architecture

[[karpathy2025wiki]] proposes a concrete workspace architecture for knowledge work: raw sources (immutable, human-curated), wiki (LLM-owned markdown, cross-referenced, schema-governed), schema file (CLAUDE.md / AGENTS.md, co-evolved by human + agent). The three-layer split — *raw / wiki / schema* — instantiates the workspace's bounded-consequences, observable-state, persistent-history properties for a knowledge-base task. The thesis's own knowledge base is an instance, which makes it operational evidence for this concept page.

## Where workspace is probed

- [[experiment-incubation]] — manipulating session state at the fixation point is a workspace-component intervention. The agent has no biological need for sleep, but removal from active context, parallelisation, and explicit re-framing are workspace moves; see [[incubation-as-infrastructure]].
- [[experiment-chess]] phase 1 — the skill library plus the trial-and-error loop is a workspace that accumulates across games; the agent learns by writing to its workspace, not by retraining.

---
*Framing drawn from `../../manuscript-notes/essay-pointer.md` (Essay/essay.tex §2.5, §3.1, §3.6).*
