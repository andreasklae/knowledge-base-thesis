---
type: concept
sources: [rajasekaran2025, zhang2025, martin2026managed, sequoia2026karpathy, aizawa2025tools]
related_concepts: [data-component, skills-component, framework-four-components, incubation-as-infrastructure, workspace-component, tools-component]
related_work: [experiment-incubation, experiment-riksantikvaren]
status: draft
updated: 2026-05-13
---

# Context Engineering

**Definition.** The discipline of curating what enters a model's finite attention budget.

[[rajasekaran2025]] frame this as a structural constraint: as token count grows, the model's effective attention degrades (context rot). Productive use of a model is partly a matter of deciding what *not* to put in the window.

## Strategies

- **Just-in-time retrieval.** Keep lightweight identifiers (file paths, citekeys, summaries) in context; fetch full content only when needed. The skills format [[zhang2025]] is the same pattern at the skill level: only metadata is loaded until a skill is needed, then the body, then bundled resources.
- **Pre-loading.** Put the small, dense, certain-to-be-needed material in the window up front.
- **Hybrid.** Combine pre-loading of the spine with just-in-time retrieval for branches.

The right mix depends on the task. The unifying principle is that context is a budget; spending it well is the design problem.

## Relation to the framework

Context engineering is not a fifth component — it is the discipline by which the four affordances in [[framework-four-components]] are *exposed* to the model at any given moment. The data component is what *exists* to be retrieved; context engineering is how a slice of it gets surfaced now.

## Software 3.0 — programming via context

[[sequoia2026karpathy]] gives the deepest single-sentence framing of context engineering in industry voice: *"your programming now turns to prompting and what's in the context window is your lever over the interpreter that is the LLM."* The context window is the program; the LLM is the interpreter. Context engineering is the discipline of programming in this paradigm.

## Long-horizon techniques

[[rajasekaran2025]] catalogues three techniques for tasks that exceed the context window:

- **Compaction.** Summarise the conversation, reinitialise with summary + N most-recent files. Preserve architectural decisions; discard redundant tool outputs.
- **Structured note-taking / agentic memory.** External notes file the agent maintains and pulls back in selectively. Sonnet 4.5's memory tool is the first-class primitive.
- **Sub-agent architectures.** Specialised sub-agents handle focused tasks with clean context windows and return distilled 1–2k-token summaries.

These map onto different task profiles: compaction for conversational flow; note-taking for iterative development; sub-agents for parallel exploration. [[martin2026managed]] is the harness-level counterpart — sessions, sandboxes, and the broader managed-agent architecture in which compaction, notes, and sub-agents live.

## Token efficiency at the tool layer

Context engineering is not only an inference-time concern. [[aizawa2025tools]] shows the same discipline applied to tool design: Claude Code caps tool responses at 25,000 tokens by default; a `DETAILED` vs `CONCISE` response-format enum lets the agent tune verbosity per call; helpful truncation and prompt-engineered errors steer the agent toward token-efficient strategies. The cleanest framing: *tool responses participate in the agent's context budget; tools that respect it are infrastructure-aligned*.

## Fixation as a context-engineering failure

When a long debugging trajectory accumulates partial solutions and wrong turns, the working context drifts away from the goal and toward the local hypotheses. The intervention [[experiment-incubation]] tests — strip working context back to goal-plus-summary, then prompt for meta-review — is a context-engineering move at the point of fixation. See [[incubation-as-infrastructure]].

---
*Framing drawn from `../../manuscript-notes/essay-pointer.md` (Essay/essay.tex §2.6).*
