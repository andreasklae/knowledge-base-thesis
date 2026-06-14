---
type: decision
status: accepted
---

# 2026-06-02 — Tool-fairness rulebook for the chess experiment

Promotes the tool-fairness rulebook from a work-page section and the
[[tool-fairness]] concept page to a durable, citable decision record. The
rule was settled in the [[diary/experiment-chess/2026-05-16]] design
session and flagged there (and repeatedly in [[experiment-chess]]) as an
ADR candidate; this records it formally so dependent decisions — notably
[[2026-06-02-chess-agent-wiki-architecture]] — cite a settled ADR rather
than a work-page section.

## Context

[[experiment-chess]] tests whether infrastructure built *around* a fixed
model improves its measured chess strength ([[agent-infrastructure-vs-capability]]),
and whether a deterministic engine outperforms agent-accumulated
procedural knowledge ([[deterministic-tools-hypothesis]]). Phase 2
compares three configurations:

- **Config 1** — inference alone.
- **Config 2** — inference + the agent-curated skill library and tools.
- **Config 3** — inference + a deterministic chess engine API.

For the Config-1→2 and Config-2→3 gaps to isolate their intended
variables, the set of tools the agent may use *during play* must be
constrained. An unconstrained Config 2 that incidentally called an engine
would contaminate the contrast with Config 3. The question the rulebook
answers: which tool uses are the agent exercising its *own* accumulated
intelligence, and which import an external oracle that bypasses the
learning loop?

## Decision

> **Mechanics tools are always permitted. Retrieval tools are permitted
> if and only if the corpus they retrieve over was built through the
> learning loop. Calculation must be agent-driven. Engines and external
> analysis are post-game only.**

### Mechanics tools — always permitted

Tools that read the board *without chess understanding embedded in them*.
They give the agent a clearer view, not a chess opinion:

- `legal_moves()`, `what_if(move) → board_after`, `is_attacked(square)`,
  `list_pieces_attacking(square)`.
- Purely geometric pattern detection (e.g. back-rank vulnerability, pin
  detection) — spatial structure only, not encyclopedic knowledge.

The experiment's current perception scripts (`show_position`,
`imagine_move`, `list_legal_moves`) are mechanics tools: material + PST
static eval, attack/defense geometry, one-ply look-ahead. They surface
geometry and material; they do not score positions strategically.

### Retrieval tools — permitted iff the corpus is agent-curated

The retrieval *algorithm* may be arbitrarily sophisticated (semantic
search, indexing). What matters is *what it retrieves over*. A GM with an
organised notebook uses an index rather than scanning every page; the
agent may do the same over its **own** accumulated wiki
([[2026-06-02-chess-agent-wiki-architecture]], [[data-component]]):

- `search_my_notes(position)` over the agent's game-analyses / pattern /
  opening pages.
- `retrieve_opening_theory(moves)` over the agent's own `openings/`.
- The wiki's `search_wiki.py` over the agent-built `references/` corpus.

**The criterion is the act of reading-and-noting being part of the loop.**
An agent (or its tutor) that reads a chess book and writes synthesis into
the wiki may later retrieve from those notes — that is permitted, and is
why pre-seeding the wiki with synthesised theory is fair
([[2026-06-02-chess-agent-wiki-architecture]] §"The fairness question").

### Retrieval tools — not permitted (contamination)

- Pre-loaded vector DBs of "every position from these books," never
  processed through the loop.
- Pre-curated Stockfish evaluation tables/databases.
- `recognize_opening()` backed by an externally-built encyclopedia — a
  trivial retrieval algorithm does not redeem a contaminated corpus.

### Calculation — permitted but agent-driven

`what_if_i_play(move) → board_after` with the agent deciding whether to
recurse is fine. A tool that returns "the best 3-move sequence from here"
is a chess engine with its interface filed off — not permitted.

### Stockfish and Lichess — post-game only

Permitted for post-game reflection (diagnosing what went wrong, writing
wiki pages from the analysis — the Lichess post-game pass in
[[experiment-chess]] §"Future work"). **Not permitted during play in
Configs 1 or 2**, because Config 3 is the engine-during-play condition and
the [[deterministic-tools-hypothesis]] test depends on that contrast being
clean.

## Consequences

- The Config-1→2 gap measures accumulated intelligence in the skill
  library; the Config-2→3 gap measures the ceiling contribution of a
  fully deterministic tool. Neither is confounded by incidental engine
  assistance.
- **Everything routes through the skill's `scripts/` and `references/`.**
  Tools and corpus inside the skill directory are captured by
  `skill_repo_sha` (and the per-game `branch` / `commit_sha`); tools
  injected outside the skill are not. Routing everything through the skill
  preserves the SHA as a complete snapshot of the agent's configuration at
  game time — a reproducibility requirement, not just a fairness one.
- The pre-seeded theory wiki is explicitly fair under this rule (the
  reading-and-noting clause), which is what licenses
  [[2026-06-02-chess-agent-wiki-architecture]]'s hand-seeding strategy.
- A future tool that crosses these lines (an engine call during play, a
  pre-built encyclopedia retrieval) requires a new decision record
  superseding the relevant clause — it changes what the experiment
  measures.

## Relationship to existing records

- [[tool-fairness]] (concept page) — the synthesis-layer statement of this
  rule. It now points to this ADR as the settled record; the ADR is the
  citable source for the thesis methods chapter.
- [[2026-06-02-chess-agent-wiki-architecture]] — depends on this ADR for
  the fairness of a pre-seeded, agent-curated wiki.
- [[deterministic-tools-hypothesis]], [[agent-infrastructure-vs-capability]]
  — the claims the rule keeps testable.
