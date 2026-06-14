---
type: concept
sources: [zhang2025, rajasekaran2025, ericsson1993deliberate, weber2024taxonomy, aizawa2025tools]
related_concepts: [framework-four-components, tools-component, mcp-vs-skills, context-engineering, learning-as-temporal-dimension, calibration-thread, deterministic-tools-hypothesis, tool-fairness, skill-acquisition-loop]
related_work: [experiment-wcag-skill, experiment-chess, interview-erfan-analysis]
status: draft
updated: 2026-06-01
---

# Skills Component

Skills are compiled, reusable, progressively-disclosed procedural knowledge an agent can deploy without rebuilding from scratch. They are the senior practitioner's checklist made loadable.

## The format

[[zhang2025]] formalise Agent Skills: filesystem-based directories containing a `SKILL.md` file plus optional scripts and resources, loaded on demand through progressive disclosure. Only metadata is loaded until a skill is needed, then the full body, then bundled resources only when the body refers to them. This is just-in-time loading at the skill granularity, conceptually close to [[context-engineering]]'s approach to retrieval.

## Terminological disambiguation — two distinct concepts

There are *two* established meanings of "skill" in the agent literature, and the thesis uses Zhang's:

- **Skill as packaging mechanism** (Zhang 2025; this thesis): a folder of instructions, scripts, and resources progressively disclosed to the model.
- **Skill as output-property dimension** (Weber 2024 taxonomy): one of six output capabilities — reWrite / Create / conVerse / Inform / Reason / Plan — that an LLM invocation can exercise.

[[weber2024taxonomy]]'s *Skills* dimension classifies *what an invocation does*; Zhang's *Skills* package *how the agent knows what to do*. The two are orthogonal and should not be conflated. The thesis vocabulary uses the Zhang sense throughout.

## Authoring discipline

The eval-driven loop Anthropic describes for tools ([[aizawa2025tools]] — prototype, evaluate, iterate with Claude Code) applies equally to skills. The authoring guidance translates: descriptions are *routing signals* (Claude reads `name` + `description` to decide whether to load the body); bodies are *imperative instructions to an agent*, not documentation for humans; reference deterministic scripts for anything that does not need LLM judgement.

## Why skills are separable from model capability

A skill encodes patterns that a reviewer would otherwise have to flag manually. The model does not get smarter; the agent gets the senior engineer's checklist.

The Erfan/Zypp example illustrates this directly (see [[interview-erfan-analysis]]). Lightly-supervised AI-assisted frontend work at Zypp reliably produced React code with predictable anti-patterns: misused `useEffect` dependencies, unnecessary re-renders from poorly chosen component coupling — the kind of mistakes a senior reviewer catches on every pull request and a junior reproduces every time. The fix that worked was a React skill loaded whenever the agent touches React code, encoding the patterns a reviewer would otherwise have to flag. Tools extend reach; skills extend competence; both are separable contributions to productivity.

## Skills as compressed expertise

Skills accumulate. Phase 1 of [[experiment-chess]] tests whether skills acquired by trial-and-error in a self-correcting loop compound into a deployable artefact — the agent analogue of deliberate practice in the sense of [[ericsson1993deliberate]]: focused exposure to tasks at the edge of current capability, with feedback-driven retention of what works. See [[learning-as-temporal-dimension]] for the broader claim that learning is how the four framework components grow.

## Calibration role

Skills verify by encoding procedures whose preconditions are checkable. A skill that says "before publishing, run the test suite" is calibration infrastructure: it externalises a step that the model would otherwise skip and over-report success on. See [[calibration-thread]].

## Where skills are probed

- [[experiment-wcag-skill]] — WCAG audits with and without a dedicated skill, compared against human-conducted Tilsynet audits.
- [[experiment-chess]] — both phases: phase 1 builds a skill library by trial and error; phase 2 freezes and evaluates it.

## Typed-tool contract: progressive disclosure + native schemas

The canonical skill interaction uses `run_script(skill, filename, args: list[str])` — the model assembles an untyped argument list and calls a generic dispatcher. A stronger contract exposes each non-private script as its own named tool with a JSON Schema extracted from the script's argument declarations (argparse, typed entrypoint, or graceful fallback to generic `args[]`). This is the *typed-tool contract* described in [[2026-06-01-typed-tool-harness-spec]].

The two properties that seem to be in tension — progressive disclosure (tools enter the model's context only when the skill loads) and typed schemas (all tool definitions must be known to the runner at build time) — are resolved by pydantic-ai's `prepare` hook. All script-tools are registered at build time, but each has a `prepare` closure that returns `None` (hiding the tool) unless the skill is in `activated_skills`. Per-request, pydantic-ai calls `prepare_tool_def` per step; the tool appears only when the skill is active. No runner rebuild.

The `activated_skills` lifecycle must match: the list persists across `run()` calls (so skills loaded in turn N are visible in turn N+1) and resets only on `clear_conversation()`. This is a behavioural change from the current implementation, where `activated_skills` clears between every `run()`.

Concrete benefits over the generic dispatcher: the model uses native tool-calling format (what it is fine-tuned for), and malformed arguments are rejected before subprocess spawn via `args_validator` — not discovered as a Python traceback inside the subprocess.

## The skill-corpus boundary as a methodological line

[[experiment-chess]]'s tool-fairness rulebook (see the experiment page) sharpens an otherwise-implicit distinction: a *tool* encodes mechanics (board geometry, legal-move generation); a *skill* encodes knowledge the agent has learned. The methodological line is that any chess knowledge the agent uses must enter the system through the learning loop — through skills written into the agent's library — and not be hardcoded into a tool by the experimenter. A retrieval tool with smart algorithms is fine; what makes it fair or unfair is whether the *corpus* it retrieves over was built by the agent's own skill-writing activity.

This generalises beyond chess: the experimental cleanliness of any skill-acquisition study depends on the corpus boundary holding. Pre-loaded knowledge dressed up as a retrieval tool is the failure mode. See [[deterministic-tools-hypothesis]] for the related question of what counts as the deterministic side of the boundary.

---
*Framing drawn from `../../manuscript-notes/essay-pointer.md` (Essay/essay.tex §2.6, §3.3, §3.5).*
