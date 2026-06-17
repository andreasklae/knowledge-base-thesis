---
type: decision
status: accepted
---

# 2026-06-17 — Chess wiki: split basic technical mates from named attacking mates

Amends §1 (folder structure) of
[[2026-06-02-chess-agent-wiki-architecture]], which fixed the original
`patterns/ endgames/ strategic-thinking/ …` layout and required that any
later structural change carry its own record. This is that record.

## Context

Live puzzle sessions on 2026-06-17 (games `49389f2b`, `5028bc89`,
`3567fffe`, all K+2R-vs-K conversions) exposed three navigation faults in
the wiki that cost the agent moves and tool calls:

1. **Duplicate two-rook mate.** A new `endgames/two-rook-mate.md`
   (herding/support framing) was written the same day the radar and
   SKILL.md triggers already pointed at
   `patterns/mating-patterns/ladder-mate.md` (fence/check framing). Two
   pages, two names, two techniques, **one endgame** (K+2R vs lone king).
   The radar and the explicit read-triggers disagreed about which page to
   open.
2. **Basic mates split across two folders.** "Mate with K+R" lived in
   `patterns/mating-patterns/` while "mate with K+2R" (the new page) lived
   in `endgames/`. The two index pages cross-referenced each other to
   paper over the split ("also see endgames/", "also see
   mating-patterns/"). A reader asking "how do I finish this won
   endgame?" had to know which of two folders held the technique for its
   exact material.
3. **An orphan and two empty folders.** `patterns/deflection.md` was the
   only content page directly under `patterns/` (every other page is one
   level deeper); it exists solely to resolve a dead `[[wikilink]]` from
   back-rank-mate. `openings/` and `strategic-thinking/pawn-structures/`
   have index pages but zero content, yet the top index routes into them
   as if populated.

The underlying conceptual error: **a basic technical mate (your material +
the enemy's lone king, a forced drill you either know or don't) is a
different kind of knowledge from a named attacking mate (a motif that
appears mid-game when the enemy king is exposed but still has its army).**
The original layout filed K+Q/K+R under `mating-patterns` next to
back-rank and smothered, conflating the two.

## Decision

### 1. New home for basic technical mates: `endgames/basic-mates/`

Basic mates — your king + material vs a **lone** enemy king, a forced
drill — move under `endgames/`, where the rest of "few pieces left,
technique you either know or don't" already lives:

```
endgames/
├── index.md
├── basic-mates/
│   ├── index.md
│   ├── king-queen-mate.md          (moved from patterns/mating-patterns/)
│   ├── king-rook-mate.md           (moved from patterns/mating-patterns/)
│   └── two-rook-ladder-mate.md     (consolidated; see §2)
└── king-pawn-endings.md
```

`patterns/mating-patterns/` keeps **only the named attacking motifs** that
fire mid-game against a king that still has defenders: back-rank,
smothered, anastasia, arabian, hook, greco, opera, queen-contact,
blind-swine.

The dividing test, stated in both index pages: *is the enemy down to a
bare king (+ pawns)?* Yes → `endgames/basic-mates/`. No (king still has
pieces, you spotted a mating motif) → `patterns/mating-patterns/`.

### 2. Consolidate the two-rook duplication into one page

`endgames/two-rook-mate.md` and the two-rook content of
`patterns/mating-patterns/ladder-mate.md` merge into a single
**`endgames/basic-mates/two-rook-ladder-mate.md`**. The name keeps
"ladder" (the technique is the rank-fence/alternate-check ladder) and
scopes it to "two-rook" because:

- The **Q+R ladder** and the **Q+Q ladder** are genuinely different (a
  queen can deliver the cut-off and the check from one piece, the
  king-adjacency traps differ, stalemate risk is higher). They get their
  **own pages** when seeded — `queen-rook-ladder-mate.md`,
  `two-queen-ladder-mate.md` — rather than being crammed into the
  two-rook page.

The merged page keeps ladder-mate's thorough trap coverage (fence-next-to-
king, checking-rook-adjacent waiting move, own-king-blocks-the-check) and
folds in the herding-vs-fence framing as one "the idea" section, not a
rival technique.

### 3. Fix the orphan and flag the stubs

- `patterns/deflection.md` → `patterns/tactics/deflection.md` (a
  `tactics/` subfolder mirrors `mating-patterns/`; deflection is a tactic,
  not a mate). The dead-link-resolution purpose is unchanged; the
  placement stops it looking like the only thing in `patterns/`.
- `openings/` and `strategic-thinking/pawn-structures/` index pages get an
  explicit **"(stub — no pages yet)"** marker, and the **top index stops
  routing into them** until they hold content. The folders stay (the ADR's
  seeding plan still expects them); they just no longer advertise empty
  shelves to a token-bounded reader.

### 4. Update every pointer

All `read_reference` paths that move are repointed in: the radar
(`scripts/_radar.py` `_PAGE_*` constants and `_drill_excerpt` calls),
SKILL.md's explicit read-triggers and material-change table, the system
prompt's K+2R/K+R wiki paths, every affected folder `index.md`, and every
`related_pages` / `[[wikilink]]` that referenced a moved page. `log.md`
records each move/merge/retire op.

## Consequences

- One page per technique; the radar and the triggers agree. The
  bare-king test gives the agent (and the radar) a single rule for which
  folder to open.
- `git mv` preserves history on the moved pages; the `log.md` entries plus
  the diff remain faithful Phase-1 data (wiki growth is a measured
  output — [[2026-06-02-chess-agent-wiki-architecture]] §"Consequences").
- Ladder variants (Q+R, Q+Q) are now *named gaps* with reserved filenames,
  not silently-missing pages — clearer for the next seeding pass.
- Invariant unchanged: maintenance is done here by the tutor at the batch
  boundary, never by the agent mid-game.
- A future change that re-merges basic mates back into `mating-patterns`,
  or that removes the bare-king dividing test, needs its own record.
