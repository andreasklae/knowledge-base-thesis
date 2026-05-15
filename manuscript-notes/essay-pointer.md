# Extended Project Description

The thesis is preceded by an **extended project description** — a UiO-required document submitted at the start of the thesis work, assessed pass/fail by the supervisor, that lays out the research question, background literature, planned experiments, methodology, and timeline. It is the canonical plan the thesis is written *against*: where the framework is committed, where the experiments are specified, where the scope is fixed, and where the methodological and ethical posture is recorded.

The thesis itself does not yet exist as a manuscript. When it does, it will live outside this knowledge base. The extended project description lives outside this knowledge base too — its files are in `../Essay/`.

## Where it is

- LaTeX source: `../Essay/essay.tex`
- Compiled PDF: `../Essay/essay.pdf`
- Bibliography: `../Essay/references.bib` (copied into `raw/literature/references.bib`)

The "Essay" folder name is a holdover from how the file was originally set up; the document is the extended project description, not a course essay.

## How this knowledge base uses it

- Concept pages in `wiki/concepts/` cite citekeys from `references.bib` in their frontmatter and footnote the extended description as the framing source.
- Experiment pages in `work/` lift their hypothesis, configurations, and measures from the extended description and will evolve as the work proceeds.
- Decision records in `decisions/` codify positions explicitly committed in the extended description (methodology, framework commitment, vendor choice).
- Manuscript-notes pages (`thesis-chapter-outline.md`, `thesis-timeline.md`, `risk-register.md`, `scope-and-limitations.md`, `open-questions-future-work.md`) restate sections of the extended description in scannable form for ongoing reference.

The source PDFs and markdown originals that the extended description cites have been copied into `raw/literature/`. The extended description itself is not duplicated into the knowledge base — read it from `../Essay/essay.pdf` (or `essay.tex`) when you need the canonical statement of the plan.

## When this pointer changes

If the extended description is revised before final submission, the changes flow inward to the knowledge base, not the other way around: a revision means re-checking the experiment pages, concept pages, decision records, and manuscript-notes pages against the new text. If revisions happen, log them in `log.md` as a `revise` operation against this pointer.
