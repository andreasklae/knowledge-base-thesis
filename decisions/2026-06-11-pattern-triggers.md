---
type: decision
status: accepted
---

# 2026-06-11 — Wiki-driven pattern triggers: geometry-present, page-traced

Settles how mating-pattern *recognition hints* may be surfaced to the chess
agent without crossing the [[2026-06-02-tool-fairness-rulebook]]. Outcome
of a design discussion (Andreas + Claude sparring session, 2026-06-10/11).

## Context

A human player glances at a board and thinks "rook + knight, cornered king
— Arabian mate territory". That is memory and pattern recognition, not
calculation, and the experiment's premise is that such recognition can be
infrastructure. The rulebook already permits geometric pattern detection
(its own example: back-rank vulnerability). The open question was hints for
*multi-move* patterns, where detection and verification come apart.

## Decision

1. **Hints fire on geometry-present, never on mate-verified.** Operational
   test: a hint must still fire on a position where the pattern is
   refuted. A tool that goes quiet on refuted positions has run the search
   — that is the engine with its interface filed off, and it would
   contaminate the Config-2 vs Config-3 contrast.
2. **Every hint traces to a wiki page.** Pattern knowledge lives as
   machine-readable `template_*` frontmatter on the agent's own pages
   (piece inventory, king zone, own-blockers, king mobility, open file
   near king, rook-on-seventh — a fixed vocabulary of knowledge-free
   geometric predicates). One generic matcher (`_patterns.py`) consumes
   them; a pattern with no page produces no hint; a new pattern is a new
   page, never new code. The hint *is* the learning loop firing — the
   agent's notebook recognising its own pattern — and the corpus stays
   under `skill_repo_sha`.
3. **Spam control is part of the contract:** hints are capped (3,
   most-specific first) and gated so a quiet middlegame and the opening
   produce none — retrieval pollution biases a fresh-context reader.

Same session, same fairness reasoning: `imagine_move` gained `fen=` and
`move="pass"` (null move). Threat detection is therefore agent-composed
(imagine candidate → pass → read own follow-ups) rather than a
`threatens_mate()` oracle; `show_position` gained `fen=` for hypothetical
boards. A tutor-side validator (`test_wiki_examples.py`) machine-checks
every FEN and mate line in the corpus, guarding against seeding wrong
theory.

## Consequences

- Recognition is now infrastructure; verification and execution remain
  the measured agent behaviour. Future patterns scale through page
  authorship alone.
- A future hint type that requires search to decide whether to fire needs
  a superseding record — it changes what Config 2 measures.
