# knowledge-base-thesis

Personal knowledge base for a master's thesis on AI agent productivity as an infrastructure problem.

It tracks literature, experiments, decisions, daily reflections, and evolving synthesis. The thesis manuscript and experiment source code live in separate repositories.

## Structure

| Path | Owner | Contents |
|---|---|---|
| `raw/literature/` | external | PDFs of papers, `references.bib` |
| `raw/interviews/` | external | finalized interview transcripts |
| `raw/datasets/` | external | external data files |
| `wiki/literature/` | LLM | one summary page per source in `raw/literature/` |
| `wiki/concepts/` | LLM | cross-cutting synthesis pages |
| `work/` | user | experiments, modules, external repos |
| `diary/` | user | `YYYY-MM-DD.md`, one file per working day |
| `admin/` | user | deadlines, supervisor notes, ideas, todos |
| `decisions/` | user | ADR-style records |
| `archive/` | user | abandoned experiments, scrapped drafts |
| `manuscript-notes/` | user | thesis-writing context |
| `inbox/` | user | capture surface for thoughts awaiting processing |
| `index.md` | LLM | catalog of the wiki |
| `log.md` | LLM | append-only chronological record of operations |

`CLAUDE.md` (symlinked as `AGENTS.md`) is the schema and workflow specification for any LLM agent operating on the knowledge base. Read it before working with the repo through an agent.

## Daily workflow

### Capturing into `inbox/`

`inbox/` is a flat folder for anything you want to write down without deciding where it belongs yet. Drop in `.md`, `.txt`, no-extension, whatever's at hand — no naming convention, no frontmatter, no structure required. Half-thoughts, screenshots' OCR, pasted Slack snippets, a single sentence in a file: all fine.

When you want it processed, ask the agent to "process the inbox" (or anything equivalent). It will:

1. Read each file and decide where it belongs (idea → `admin/ideas.md`; substantial concept → new `wiki/concepts/` draft; decision → `decisions/` after confirming with you; reflection → `diary/YYYY-MM-DD.md`).
2. Ask you if a destination is ambiguous, leaving the file in `inbox/` until you clarify.
3. Delete the source file once the destination writes succeed, and append a single entry to `log.md` per file.

Use the inbox aggressively. It exists to absorb friction at the moment of capture — sorting is the agent's job, not yours.

### Adding sources to `raw/`

`raw/` holds external sources of truth: PDFs of papers, interview transcripts, datasets. The agent reads them but never rewrites them (typo fixes and version replacements only).

- **Literature.** Drop a PDF into `raw/literature/` using the citekey-style name already established there (e.g. `Kalai(2024).pdf`). Then ask the agent to ingest it. The agent will run docling to convert the PDF, add a BibTeX entry to `raw/literature/references.bib` (asking you to confirm if it had to generate one), create the wiki summary page, update any concept pages the paper touches, and log the ingest. Ingest one paper at a time — the conversation about key takeaways matters as much as the resulting wiki page.
- **Interviews.** Place finalized transcripts in `raw/interviews/`. Drafts and analysis live in `work/` instead.
- **Datasets.** Put external data files in `raw/datasets/` with a short README alongside them describing source and date.

The agent edits `wiki/` confidently in response to anything in `raw/`. You own `raw/`; you read `wiki/`.

## PDF extraction with docling

PDFs in `raw/literature/` are converted to Markdown using [docling](https://github.com/DS4SD/docling) before being summarized into `wiki/literature/`. The conversion script is at [raw/literature/pdf_to_md.py](raw/literature/pdf_to_md.py).

### One-time setup

Docling pulls in `torch`, `transformers`, and other heavy dependencies that conflict with system Python installs (e.g. Anaconda), so it lives in its own virtualenv. The venv is gitignored — every clone needs to recreate it locally.

```bash
cd raw/literature
python3 -m venv .docling-venv
.docling-venv/bin/pip install --upgrade pip
.docling-venv/bin/pip install docling
```

Requires Python 3.10+ (this repo was set up with 3.12). The install is ~2 GB on disk and the first conversion downloads another ~500 MB of model weights into `~/.cache/docling`. Subsequent runs reuse the cache and are fast.

### Converting a PDF

```bash
cd raw/literature
.docling-venv/bin/python pdf_to_md.py Kalai\(2024\).pdf Kalai\(2024\).md
```

The script takes two positional arguments — input PDF and output Markdown path — and writes the converted text plus a `Wrote <path> (N chars)` confirmation line. It does no OCR by default; scanned PDFs without an embedded text layer will produce empty or garbled output. For those, enable OCR via docling's `DocumentConverter` options (see [docling docs](https://ds4sd.github.io/docling/)).

### Why not commit the venv?

The venv weighs ~1.2 GB and contains platform-specific binaries (`libtorch_cpu.dylib` alone is 237 MB). Committing it would exceed GitHub's per-file size limit, require Git LFS, and break on any machine with a different OS or Python version. The `requirements` are pinned implicitly by `pdf_to_md.py`'s single import (`docling`) — anyone can reproduce the environment with the setup steps above.

If pinning becomes important, run `.docling-venv/bin/pip freeze > raw/literature/requirements.txt` and install from that file instead.
