# Knowledge Base Schema and Workflows

This file tells you (the LLM agent) how this knowledge base is structured and how to operate on it. Read it at the start of every session before making any changes. If anything below is ambiguous in a specific situation, ask the user rather than guessing.

## Purpose

This knowledge base supports a master's thesis on AI agent productivity as an infrastructure problem. It tracks literature, experiments, decisions, reflections, and evolving synthesis. It does not contain the experiments' source code or the thesis manuscript — those live in separate repositories.

## The Three Roles

Every file in this knowledge base plays one of three roles:

1. **External source of truth** (in `raw/`) — papers, interview transcripts, datasets. You read these. You do not edit their content; typo fixes and version replacements are allowed, but never rewrite a source to change what it says.

2. **User-authored content** (in `diary/`, `admin/`, `work/`, `decisions/`, `archive/`, `manuscript-notes/`, and `inbox/`) — owned by the user. You read these as input. You may propose edits, and you may make edits when the user asks, but the user owns them.

3. **LLM-compiled synthesis** (in `wiki/`) — owned by you. You create, update, and maintain these pages. The user reads them.

A wiki page may contain information that has no source in `raw/`. Many concept pages will draw primarily from the user's diary, experiment results, and conversations. This is correct.

## Directory Reference

| Path | Owner | Contents |
|---|---|---|
| `raw/literature/` | external | PDFs of papers, `references.bib` |
| `raw/interviews/` | external | finalized interview transcripts |
| `raw/datasets/` | external | external data files |
| `wiki/literature/` | LLM | one summary page per source in `raw/literature/` |
| `wiki/concepts/` | LLM | cross-cutting synthesis pages |
| `work/` | user | experiments, modules, external repos (flat; `type:` in frontmatter) |
| `diary/` | user | `YYYY-MM-DD.md`, one file per working day |
| `admin/` | user | deadlines, supervisor notes, `ideas.md`, todos |
| `decisions/` | user | ADR-style records: `YYYY-MM-DD-short-slug.md` |
| `archive/` | user | abandoned experiments, scrapped drafts |
| `manuscript-notes/` | user | thesis-writing context |
| `inbox/` | user | flat folder; capture surface for thoughts awaiting processing |
| `index.md` | LLM | catalog of the wiki |
| `log.md` | LLM | append-only chronological record of operations |

## Frontmatter Conventions

Every wiki page and every `work/` file has YAML frontmatter. Frontmatter is required; pages without it are considered drafts.

### Wiki literature pages (`wiki/literature/<citekey>.md`)

```yaml
---
type: literature
citekey: kalai2024calibration
title: Calibrated Language Models Must Hallucinate
authors: [Kalai, Vempala]
year: 2024
venue: arXiv
raw_path: raw/literature/kalai2024.pdf
related_concepts: [calibration, hallucination, deterministic-tools]
related_work: [experiment-math, experiment-riksantikvaren]
status: summarized        # one of: draft, summarized, deeply-read
ingested: 2026-05-13
updated: 2026-05-13
---
```

### Wiki concept pages (`wiki/concepts/<slug>.md`)

```yaml
---
type: concept
sources: [kalai2024calibration, guo2017calibration]    # citekeys from references.bib
related_concepts: [deterministic-tools-hypothesis, framework-four-components]
related_work: [experiment-math, experiment-riksantikvaren]
status: stable             # one of: draft, stable, contested
updated: 2026-05-13
---
```

### Work pages (`work/<slug>.md`)

```yaml
---
type: experiment           # one of: experiment, module, external-repo, interview
status: planning           # for experiments: planning, in-progress, complete, blocked, abandoned
related_concepts: [deterministic-tools-hypothesis]
related_work: [module-eval-harness]
sources: [kalai2024calibration]
updated: 2026-05-13
---
```

### Diary entries (`diary/YYYY-MM-DD.md`)

```yaml
---
type: diary
touched_work: [experiment-math, module-eval-harness]
touched_concepts: [calibration]
status: open               # open while the day might still get edits; closed when finalized
---
```

### Decision records (`decisions/YYYY-MM-DD-slug.md`)

```yaml
---
type: decision
status: accepted           # accepted, superseded, rescinded
supersedes: 2026-04-01-old-decision    # optional
---
```

Decision records use ADR structure: Context, Decision, Consequences. Keep them short.

## Linking

Use wikilink syntax `[[citekey]]` or `[[slug]]` for internal links. Resolve them to filesystem paths during operations. Maintain backlinks implicitly via the `related_*` frontmatter fields; do not write separate backlink sections by hand.

When you create or move a wiki page, search the rest of the knowledge base for references to it and update them. This is the link-integrity workflow described in the Lint section.

## Operations

You perform four kinds of operation: ingest, capture, query, lint. Each has a defined workflow.

### Ingest

The user adds a new source to `raw/` (literature, interview, dataset) and asks you to ingest it.

1. Read the source. For PDFs, read directly; you do not need a markdown equivalent in `raw/`.
2. For a literature source: add the BibTeX entry to `raw/literature/references.bib`. If the user has not supplied it, generate one and ask them to confirm.
3. Create the corresponding wiki page (e.g. `wiki/literature/<citekey>.md`). For literature, the page contains: a 2-4 sentence summary, the source's main claims, its relevance to this thesis, and links to related concepts and work.
4. Update or create relevant concept pages in `wiki/concepts/`. A single source often touches several concept pages. Mark contested claims explicitly.
5. Update `index.md`.
6. Append an entry to `log.md`:
   ```
   ## [2026-05-13] ingest | kalai2024calibration | Calibrated Language Models Must Hallucinate
   - Created wiki/literature/kalai2024calibration.md
   - Updated wiki/concepts/calibration.md (added theoretical lower bound section)
   - Updated wiki/concepts/hallucination.md (created)
   ```
7. Report what changed to the user. Highlight any contradictions with existing wiki content.

### Capture

Captures can arrive two ways: the user says something in conversation ("remember this thought," "I had an idea about X," "write a diary entry about what we did"), or the user drops a file into `inbox/` and later asks you to process it. The destination rules below apply identically in both cases. For inbox-originated captures, see the **Process Inbox** operation below for the full workflow including logging and file deletion.

1. Decide where it goes. Use these rules:
   - A half-formed observation or one-liner → append to `admin/ideas.md`.
   - A substantial idea that connects to existing concepts → new or updated page in `wiki/concepts/` with `status: draft`.
   - A scope/architecture decision the user has just made → new file in `decisions/`. Confirm with the user before creating, since decision records are intended to be durable.
   - A reflection on the day's work or a request to log progress → new or appended `diary/YYYY-MM-DD.md`, then propagate to relevant concept and work pages.
2. If unsure, ask. Do not guess silently.
3. Append to `log.md`.

### Query

The user asks a question against the wiki.

1. Read `index.md` first to find relevant pages.
2. Read the pages. If they reference `raw/` sources, read those too if needed for fidelity.
3. Synthesize an answer with citations using wikilink syntax.
4. Offer to file the answer back into the wiki as a new concept page if it represents new synthesis. Do not file silently; ask first.
5. Append to `log.md`.

### Process Inbox

The user asks you to process `inbox/`, or asks something equivalent like "process my notes" or "clear out the inbox."

1. List the files in `inbox/`. If empty, tell the user and stop.
2. For each file, in any order:
   a. Read its contents.
   b. Decide the destination using the Capture rules above (one-liners and half-formed observations → `admin/ideas.md`; substantial ideas → new or updated `wiki/concepts/` page with `status: draft`; scope/architecture decisions → new file in `decisions/` (confirm with user first); reflections on the day's work → new or appended `diary/YYYY-MM-DD.md`).
   c. If the destination is ambiguous, leave the file in `inbox/` and ask the user. Do not guess.
   d. Otherwise, write or update the destination file(s). Propagate to related concept and work pages as for any other capture.
   e. Append a single entry to `log.md` naming the source file and every destination touched:
      ```
      ## [2026-05-15] process | inbox/quick-thought.md | Updated wiki/concepts/calibration.md; appended to admin/ideas.md
      ```
   f. Delete the inbox file once the destination writes succeed. If any destination write fails, leave the inbox file in place and report the failure.
3. After all files are processed (or set aside for clarification), report a summary to the user: how many files were processed, what was created or updated, and which files (if any) are still in `inbox/` awaiting clarification.

Inbox files have no required format or frontmatter — the user drops them in with whatever names and contents feel natural at the moment of capture. Tolerate `.md`, `.txt`, no extension, anything readable as text. Do not enforce structure on the inbox; structure is applied by you during processing.

### Lint

Run periodically, or when the user asks for a health check.

Check for:
- **Link integrity.** Every wikilink resolves to a real file. Every `related_*` frontmatter entry resolves. Report dead links; do not silently delete them.
- **Orphan pages.** Wiki pages with no inbound references from any other page. These may be fine (a new ingest) or may indicate the page didn't get properly integrated.
- **Stale frontmatter.** `updated:` dates that are older than the file's actual last modification.
- **Contradictions.** Claims in one wiki page that conflict with claims in another. Flag these for the user; do not auto-resolve.
- **Missing concept pages.** Concepts mentioned in multiple sources but lacking their own page.
- **Status drift.** Experiments in `work/` with `status: in-progress` that haven't been touched in the diary for weeks.

Report findings; do not auto-fix structural issues without confirmation.

## Workflow Norms

- **Stay involved with the user.** Ingest one source at a time by default. Discuss key takeaways before writing summary pages.
- **Propagate aggressively.** A single user action often touches 10-15 files across the wiki. This is expected. Do not under-update out of caution.
- **Preserve the user's voice in `diary/`, `admin/`, `decisions/`, and `work/`.** When editing these, make minimal changes and ask before substantial rewrites.
- **Own `wiki/` confidently.** Write, rewrite, restructure as needed to keep the synthesis current. The user reads; you maintain.
- **Log everything.** Every ingest, every capture that creates or modifies a wiki page, every lint pass — one entry in `log.md`. Use the format `## [YYYY-MM-DD] <op> | <subject> | <short description>`.
- **Never edit content in `raw/`** except for typo fixes or version replacements. Note such changes in `log.md`.
- **Ask when the destination is ambiguous.** Capture rules above cover most cases, but boundary cases exist. Ask.

## What Does Not Live Here

- The thesis manuscript itself (separate repository).
- Experiment source code (separate repository or repositories).
- Anything the user has not explicitly placed or asked you to create.

If the user references a thesis chapter or experiment code, you may need a path to it. Store paths in `manuscript-notes/` or in the relevant `work/` page's frontmatter; do not copy external content into the knowledge base.

## Initial State

On first run, after the directory structure is created, populate:
- `CLAUDE.md` — this file
- `AGENTS.md` — symlink to `CLAUDE.md`
- `index.md` — empty catalog with section headers (`## Literature`, `## Concepts`, `## Work`, `## Decisions`)
- `log.md` — one entry: `## [<today>] init | knowledge-base | Initial scaffolding created`
- `admin/ideas.md` — empty file with a single `# Ideas` heading
- `raw/literature/references.bib` — empty file

Do not create any other files until the user asks for ingestion or capture.
