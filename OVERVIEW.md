# Project Overview — start here

This is the orientation map for the knowledge base. If you are an LLM
agent (or a human) landing here cold, read this page first, then follow
the reading order at the bottom. For *how to operate on* the KB (schema,
workflows, ownership rules), read [CLAUDE.md](CLAUDE.md) — this page is
about *what the project is*.

## What the thesis argues

A master's thesis on **AI agent productivity as an infrastructure
problem** (University of Oslo, due June 2027). The canonical statement is
the extended project description at `../Essay/essay.tex` ("The Wrong
Question"); everything in this KB is written *against* that document.

**The wrong question** (the one the field mostly asks): how do we make
models more *intelligent*?

**The thesis's question** instead: *how can principles of human
productivity be operationalised as design patterns for AI agent
systems?* — i.e. what **infrastructure** makes an already-capable, fixed
model productive on real tasks?

The motivating intuition: productivity is not mainly a property of the
brain doing the work, but of the accumulated stock of compressed
solutions the worker can draw on. A civil engineer is not smarter than a
Roman aqueduct builder but builds things the Roman could not, because
two millennia of materials science, codes, and post-mortems sit between
them. The thesis asks whether the same pattern — skills, tools, and
written-down knowledge behind stable interfaces — is what makes a
*language-model agent* productive, and whether that stock can be grown
**around a fixed model** rather than baked into a new one. See
[[agent-infrastructure-vs-capability]].

## The framework (the primary contribution)

A four-part decomposition of what an agent needs to be productive —
affordances, not a strict partition:

| Component | One-line | Page |
|---|---|---|
| **Workspace** | where actions have bounded consequences | [[workspace-component]] |
| **Tools** | reach external systems / deterministic operations | [[tools-component]] |
| **Skills** | compiled, reusable procedural knowledge, progressively disclosed | [[skills-component]] |
| **Data** | live knowledge access when memory is insufficient | [[data-component]] |

See [[framework-four-components]]. **Learning** is not a fifth component
but the *temporal dimension* of the four — how the affordances grow over
time ([[learning-as-temporal-dimension]]).

Two cross-cutting claims run through nearly every chapter:

- **Calibration thread** — miscalibration is partly a *systems* property,
  not only a model property; infrastructure that externalises
  verification improves it. [[calibration-thread]]
- **Deterministic-tools hypothesis** — for any sub-task with a verifiable
  answer, deterministic tools beat inference; inference's job is to
  *choose* the tool, not perform the operation. The limit case of the
  calibration mechanism. [[deterministic-tools-hypothesis]]

## The experiments (the evidence)

Six experiments, each holding a model fixed and varying the
infrastructure around it. This is the claim↔evidence link: the framework
above is *tested* here.

| Experiment | Chapter(s) | Tests | Status |
|---|---|---|---|
| [[experiment-chess]] | Skills + Knowledge | skill accumulation around a fixed model lifts Elo over time (deliberate-practice / scientific-method loop) | in-progress |
| [[experiment-riksantikvaren]] | Tools + Knowledge | 4 knowledge-access configs on one heritage corpus (inference / API / RAG / compiled wiki) | planning |
| [[experiment-math]] | Tools | inference vs. skills vs. coding sandbox on verifiable problems | planning |
| [[experiment-wcag-skill]] | Skills | WCAG-audit skill vs. no skill, against human audits | planning |
| [[experiment-vision-landmarks]] | Eyes | tools that constrain a biased candidate set (GPS + lookups) fix prototypicality bias | planning |
| [[experiment-incubation]] | Sleep | workspace/session-state manipulation rescues fixated agents | planning |

Supporting infrastructure: [[module-skillful-agent]] (the agent harness all
agent experiments run on — the four-components framework made concrete) and
[[module-llm-server]] (self-hosted Gemma 4 on eX3). Practitioner interviews
([[interview-erfan-analysis]],
[[interview-karpathy-analysis-1]], [[interview-karpathy-analysis-2]])
are directional/inspirational, not statistical evidence.

## What "baseline" means project-wide

Every experiment defines a **baseline** as the fixed model given only the
*irreducible-minimum* scaffolding needed to make the task possible at
all — then measures the contribution of infrastructure added on top.
(Chess: model + `list_legal_moves` + `make_move`, the analogue of a human
told only the rules and the legal moves. Other experiments have their own
minimum.) The result that matters is always the *delta* above baseline.

## Reading order for a cold start

1. **This page** — what the project is.
2. `../Essay/essay.tex` (or `essay.pdf`) — the canonical plan. Abstract +
   §1 + §3 give you the whole argument.
3. [[agent-infrastructure-vs-capability]] and [[framework-four-components]]
   — the central claim and its vocabulary.
4. The work page for whatever experiment you're touching (table above),
   then its recent `diary/<experiment>/` entries and its `decisions/`.
5. [CLAUDE.md](CLAUDE.md) before you *edit* anything — ownership roles,
   frontmatter, the log convention.

[index.md](index.md) is the full wiki catalog; [log.md](log.md) is the
chronological record of operations.
