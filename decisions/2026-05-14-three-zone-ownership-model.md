---
type: decision
status: accepted
---

# 2026-05-14 — Three-zone ownership model for the knowledge base

## Context

The knowledge base is built on [[karpathy2025wiki]]'s LLM-Wiki pattern, which proposes a two-layer architecture: **raw** (immutable, human-curated sources) and **wiki** (LLM-owned synthesis), with a schema file (`CLAUDE.md` / `AGENTS.md`) governing the operations.

For an academic project, this two-layer split is insufficient. A thesis generates substantial *user-authored* content — diary entries, decision records, experiment notes, scope choices, supervisor admin, manuscript drafts. None of this is external evidence (so it does not belong in `raw/`), and none of it should be LLM-owned and freely rewritable (so it does not belong in `wiki/`). Treating diary entries as raw evidence corrupts their character (they are not external to the project); treating them as wiki synthesis erodes their evidentiary value (the LLM rewriting yesterday's thinking destroys what makes the diary useful as a record).

The session of 2026-05-14 (see [[diary/meta/2026-05-14]]) worked through this and settled on a refinement.

## Decision

The knowledge base runs **three ownership zones**, not two. Top-level folder structure encodes ownership, not content type.

1. **External, immutable** — `raw/`
   - Contents: papers (`raw/literature/`), finalized interview transcripts (`raw/interviews/`), datasets (`raw/datasets/`), non-academic external sources (`raw/other/`).
   - LLM permission: read only. Typo fixes and version replacements are allowed; rewriting to change what a source says is not. Note any edit in `log.md`.

2. **User-authored** — `diary/`, `work/`, `decisions/`, `admin/`, `archive/`, `manuscript-notes/`, `inbox/`
   - Contents: the user's authored material in all its forms (reflections, experiment notes, ADRs, admin, drafts, capture).
   - LLM permission: read freely; propose edits; make edits only when the user asks. Preserve the user's voice. Never restructure without confirmation.

3. **LLM-compiled synthesis** — `wiki/`
   - Contents: per-source summary pages (`wiki/literature/`), cross-cutting concept pages (`wiki/concepts/`).
   - LLM permission: own. Create, rewrite, restructure, propagate. The user reads.

The schema (`CLAUDE.md`) sits at the root and is *co-evolved*: either party can propose edits, the user owns final say.

## Consequences

**Positive**

- The property at stake — *whose voice the page represents* — is encoded in the directory structure. A reader (human or agent) sees ownership by path.
- The LLM has a bright line for what it may rewrite, which prevents drift between user authoring and LLM synthesis.
- Diary entries retain their evidentiary character: tagging some `meta-observation` (see [[diary/meta/2026-05-14]]) gives the thesis usable case material on its own Knowledge component.
- The pattern admits an asymmetry that turns out to be correct: `wiki/literature/` exists (external sources need an LLM summary tailored to the project), but there is no `wiki/work/` (the user's experiment notes are already project-tailored authoring; an LLM "synthesis of an experiment" would just be a rewrite of in-flight user thinking, and a risky one). Cross-cutting synthesis happens in `wiki/concepts/` instead.

**Negative / risks**

- Operationally heavier than Karpathy's two-zone model: three categories of file with different mutability rules to keep straight. Mitigated by the schema documenting each zone explicitly.
- The boundary between "the LLM proposes edits to user-authored files" and "the LLM rewrites them" depends on convention, not enforcement. Mitigated by the workflow norm in `CLAUDE.md` ("ask before substantial rewrites").
- Diverges from the canonical Karpathy pattern, which means the thesis cannot claim its KB is a *pure* implementation. This is honest — the divergence is part of the contribution.

**Connections**

- Refines [[karpathy2025wiki]]'s two-layer architecture.
- Instantiates [[workspace-component]] (ownership-zone structure for a knowledge workspace).
- Provides the *primary* working instance of the LLM-Wiki pattern that [[data-component]] tracks; the chess wiki in [[experiment-chess]] is the second instance.
- Tagged `meta-observation` because the KB is case material for the [[agent-infrastructure-vs-capability]] thesis.
