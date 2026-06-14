---
type: decision
status: accepted
---

# 2026-06-02 — Chess agent's knowledge wiki: architecture and seeding strategy

Concretises the "agent's own LLM wiki" sketched in
[[experiment-chess]] §"Knowledge structure" and
[[skill-acquisition-loop]] §"The parallel chess wiki". Until now those
were a plan (`openings/ patterns/ endgames/ game-analyses/ raw/`); this
record fixes the actual structure, the retrieval mechanism, the page
contract, and who writes the pages when. It is a methodology-affecting
choice: the wiki *is* the agent-curated corpus that the
[[tool-fairness]] rulebook turns on, and its growth across batches is a
first-class Phase 1 result.

## Context

The chess agent ([[experiment-chess]]) accumulates procedural chess
knowledge as a parallel LLM wiki, the same [[karpathy2025wiki]]
compiled-synthesis pattern as the thesis knowledge base itself, but with
a chess-specific schema and a much dumber reader. Two facts about the
reader drive the whole design:

1. **The agent runs per-turn with fresh context**
   ([[2026-05-24-per-turn-fresh-context]]). It cannot hold the wiki in
   memory across turns; every turn it must *navigate to* the relevant
   page from scratch. Progressive disclosure is therefore not a nicety —
   it is the only thing that keeps the wiki usable inside a turn's token
   budget.
2. **The agent cannot run maintenance during play.** The thesis KB's
   four operations (ingest/capture/query/lint) are run by Claude Code,
   the meta-agent. The chess agent during a game can only *read*. Any
   maintenance — splitting an oversized page, deduping, promoting a
   draft, fixing a dead link — happens at the **batch boundary /
   post-game analysis** step, not mid-game.

### The fairness question, resolved

Pre-seeding the wiki with synthesised chess theory is **fair** under the
[[tool-fairness]] rulebook. The rulebook's "cheating" case is dumping
book content into a vector DB the agent never processed; the "fair" case
is the agent (or its tutor) reading material and writing its own notes.
Synthesising theory into wiki pages is the latter — it is reading a
chess book the way a human student does. The experiment is not "an
infinite self-play loop that bootstraps from zero"; it is **deliberate
practice under a tutor** ([[ericsson1993deliberate]]): the user points
the agent in the right direction, supplies tools, says what to read, and
the agent accumulates a compounding artefact over time. The wiki is that
artefact. This reframes Phase 1 away from pure self-improvement toward
tutored knowledge acquisition — the more honest description of what the
experiment actually tests.

## Decision

### 1. Structure — the wiki lives under the skill's `references/`

The wiki is the chess skill's `references/` directory. This is exactly
what `references/` is for in skillful-agent: files the agent reads for
knowledge via `read_reference`. No new harness mechanism is needed.

```
chess/
├── SKILL.md
├── scripts/                     # perception scripts + search_wiki.py
└── references/
    ├── index.md                 # top-level catalog + navigation decision-tree
    ├── log.md                   # append-only: one entry per page created/updated
    ├── openings/index.md
    ├── principles/index.md          # short heuristics ("don't hang pieces")
    ├── strategic-thinking/
    │   ├── index.md                 # long-term planning, mental models
    │   └── pawn-structures/index.md # isolated/passed/doubled pawns, chains
    ├── patterns/
    │   ├── index.md                 # tactical patterns (forks, pins, skewers, discoveries)
    │   └── mating-patterns/index.md
    ├── endgames/index.md
    └── game-analyses/index.md       # per-game post-mortems
```

Category split rationale:

- **principles/** — bite-sized rules of thumb the agent checks the
  position *against* ("when under attack: defend, move, or pose a bigger
  threat"; "look for passed pawns when down material").
- **strategic-thinking/** — long-term planning and the mental models for
  forming a plan from a position. Different retrieval moment from
  principles: invoked when *building a plan*, not when *checking a move*.
- **pawn-structures/** lives under strategic-thinking because pawn
  structure is long-term positional planning that crosses
  opening/middlegame/endgame.
- **patterns/** — concrete, calculable tactical sequences.
  **mating-patterns/** is a subfolder because it is dense enough to
  warrant one.
- No `tools/` folder. Tool usage is procedural, not declarative: pages
  point to the relevant `scripts/` (e.g. "verify this exchange with
  `imagine_move.py`"); SEE and evaluation heuristics are described where
  they are used, not catalogued separately.

### 2. Retrieval — SKILL.md points to one index; indexes are decision-trees

- **SKILL.md** gives the turn workflow and *one* pointer:
  `references/index.md`. It also gives general when-to-look-up guidance —
  after `show_position`, if the position enters a new phase, matches a
  known structure, or the plan is unclear, read the top index and
  navigate from there. SKILL.md does **not** enumerate pages.
- **Indexes are navigation decision-trees, not tables of contents.** The
  top `index.md` routes by board condition ("opening unclear →
  `openings/`; down material → `principles/` + `strategic-thinking/`;
  few pieces → `endgames/`; exposed enemy king →
  `patterns/mating-patterns/`"). Each subfolder `index.md` routes one
  level deeper. This is the KB's actual practice — its `index.md` is
  organised for navigation, and at moderate scale a good index beats
  embedding search ([[karpathy2025wiki]] §4).
- **Two access tools: `read_reference` (read a page) and
  `search_wiki.py` (find a page).** `read_reference` takes a **path**
  relative to the skill's `references/` directory and returns that page's
  body; it supports subfolders and is jailed to `references/`.
  `search_wiki.py` (a skill script, exposed as the typed tool
  `chess__search_wiki`) scans `references/` by keyword and returns each
  matching page's **path + frontmatter only** (never the body), including
  the exact `read_reference` call to open it. The agent navigates by
  reading `index.md`, following its routing to a folder index, then a
  page — or, when it knows a concept but not its location, searching first
  and reading the hit. SKILL.md points at `index.md` and does **not**
  enumerate pages; the index pages (and the search tool) are the
  navigation layer.

  *Implementation note (amends an earlier assumption):* this required a
  change to skillful-agent. The harness's original `read_reference` took a
  bare top-level *filename*, gated on a flat allowlist
  (`_list_files(references/)`, non-recursive) and ignored the SKILL.md
  `references:` frontmatter entirely — so a nested wiki was unreachable
  through it, and the planned "declare index files in frontmatter" scheme
  did nothing. `read_reference` was reworked to take a path with subfolder
  support and a path-jail instead of an allowlist
  (skillful-agent commit `435fa8d`). Separately, a prior harness change
  had already removed the generic `run_script` tool in favour of exposing
  each `scripts/<name>.py` as a typed tool `chess__<name>` revealed by
  `use_skill`; the chess SKILL.md and the backend's move-detection were
  updated to match (`chess__make_move` instead of a `run_script` +
  `filename` check). The chess experiment's `skill-agent` git pin was
  resynced to pick both up.

### 3. Page contract — borrowed from the KB, adapted for a dumb reader

Every content page has frontmatter and a fixed body shape, and is
**capped at ~400 words / ~60 lines** (the KB's own pages mostly land at
40–90 lines, which validates the cap). Progressive disclosure is the
whole point; a page that grows past the cap defeats it.

Frontmatter:

```yaml
---
category: strategic-thinking          # which folder
description: Playing with and against the isolated queen pawn.  # one line, human-readable
triggers: [isolated queen pawn, IQP]  # board conditions that make this page relevant
related_pages: [patterns/minority-attack, endgames/iqp-endgames]
tags: [pawn-structure, middlegame]
status: draft                         # draft → tested
updated: 2026-06-02
---
```

The `description:` line is required and kept to one sentence: it is what
`search_wiki.py` shows the agent to let it decide whether a page is worth
loading (see §6).

Body sections: **When to use** (board conditions) · **The idea**
(concept) · **What to do** (actionable steps) · **Watch out for**
(pitfalls) · **Examples** (FEN/PGN, optional).

Adopted from the KB, with reasons:

- **`triggers:` + `tags:` + `related_pages:`** — the retrieval glue
  `search_wiki.py` indexes over, and the inline `[[wikilink]]` chain that
  lets one page point to the next relevant page (the KB's
  `related_concepts` convention). This is how progressive disclosure
  *chains*: a pawn-structure page links `[[patterns/minority-attack]]`,
  the agent follows it.
- **`status: draft → tested`** — a page is `draft` when first written and
  promoted to `tested` once a game in which it was applied confirms it
  helped. This is itself a thesis result: it shows the wiki
  self-correcting ([[skill-acquisition-loop]]).
- **`log.md`** — append-only, `## [date] op | page | description`. The
  wiki's *growth* is half the Phase 1 data: `git diff` between batch SHAs
  plus the log shows exactly what the agent learned and when.

### 4. Maintenance happens at the batch boundary, not during play

During play the agent only reads. The maintenance operations — split an
oversized page into Part 1/Part 2, dedupe, promote `draft → tested`, fix
dead `[[wikilinks]]`, write `game-analyses/` entries — run during
post-game analysis / batch reflection. This mirrors the KB's "user reads
/ LLM maintains" split but relocates maintenance to a dedicated loop
step, because the per-turn reader cannot do it.

### 6. `search_wiki.py` returns frontmatter, never bodies

`search_wiki.py` is a discovery tool, not a content-delivery tool. Given a
keyword query it scans `references/` and returns, for each matching page,
**only its path and its YAML frontmatter** — `description`, `triggers`,
`tags`, `status`, `related_pages`. It never returns page bodies.

The agent reads the frontmatter, decides which one page (or few) is worth
the token cost, and then loads that page deliberately — either by
following the index (`read_reference` on the relevant `index.md`) or, once
content pages are reachable, by a targeted body read. The two-step
"search returns frontmatter → load returns body" keeps every search cheap
and makes each body load a conscious choice, which is the point of
progressive disclosure under a fresh-context, token-bounded reader.

This is why `description:` is a required, one-sentence frontmatter field
(§3): it is the human-readable summary the agent sees in search results.

### 5. Seeding — you and me, by hand, now

The initial pages (a handful of `strategic-thinking/` and
`patterns/mating-patterns/` pages plus all index scaffolding) are
written by the user and Claude Code by hand, to establish and validate
the page format before any automation. Later, page authorship extends to
the agent (post-game analyses, promoting discovered patterns) and
possibly a dedicated ingestion pass over chess books in `raw/`. See
[[experiment-chess]] §"Future work" for the `note()` tool and Lichess
post-game-analysis ideas that build on this.

## Consequences

- The chess skill gains a `references/` wiki and a `search_wiki.py`
  script. SKILL.md grows a "How to use the wiki" section and a
  `references:` frontmatter list of index files only.
- Phase 1's measurable output now explicitly includes wiki growth (page
  count, draft→tested promotions, `log.md`, inter-batch `git diff`)
  alongside Elo — consistent with [[experiment-chess]] Phase 1 measures.
- The fairness reframing (tutored deliberate practice, not zero-start
  self-play) should be reflected in the [[experiment-chess]] hypothesis
  framing and eventually in the thesis chapter. The [[tool-fairness]]
  rulebook already permits this; this record makes the permission
  explicit for the pre-seeded-theory case.
- Page-length cap and the read-only-during-play rule are invariants: a
  future change that lets the agent write to the wiki mid-game, or
  removes the cap, needs its own decision record.

## Open items

- ~~Promote the tool-fairness rulebook to its own ADR.~~ Done:
  [[2026-06-02-tool-fairness-rulebook]]. This record cites it for the
  fairness of a pre-seeded, agent-curated wiki.
- ~~Decide `search_wiki.py`'s output contract.~~ Settled in §6: returns
  path + YAML frontmatter only (never bodies). First implementation is a
  keyword scan over `references/` frontmatter; the agent loads a body
  deliberately as a second step.
- Remaining for implementation: `search_wiki.py`'s match ranking and the
  cap on number of pages returned per query (the per-page cost is already
  bounded — frontmatter is small). Settle when the script is written.
