---
type: concept
sources: []
related_concepts: [deterministic-tools-hypothesis, skills-component, data-component, calibration-thread]
related_work: [experiment-chess]
related_decisions: [2026-06-02-tool-fairness-rulebook, 2026-06-02-chess-agent-wiki-architecture]
status: stable
updated: 2026-06-02
---

# Tool Fairness

The **tool-fairness rulebook** for [[experiment-chess]] defines which tools the agent may use during play without compromising the experimental comparison. The core question: which tool uses constitute the agent exercising its own accumulated intelligence, and which constitute importing an external oracle that bypasses the learning loop?

## The settled rule

> **Mechanics tools are always permitted. Retrieval tools are permitted if and only if the corpus they retrieve over was built through the learning loop.**

### Mechanics tools (always permitted)

Tools that read the board without chess understanding embedded in them:

- `legal_moves()` — enumerate all legal moves from the current position
- `what_if(move) → board_after` — compute the resulting board state
- `is_attacked(square)` — geometric check
- `list_pieces_attacking(square)` — board geometry
- Pattern detection that is purely geometric (e.g., back-rank mate pattern check) — these use spatial structure only, not encyclopedic chess knowledge

These are analogous to tools that give a human player a clearer view of the board — they provide no chess strategy.

### Retrieval tools: permitted iff corpus is agent-curated

Smart retrieval over an *agent-built* corpus is permitted — the question is what the retrieval runs over, not how sophisticated the algorithm is. A human GM with an organised notebook doesn't scan every page sequentially; they use indexing. The agent may do the same, over its own accumulated chess wiki (see the parallel LLM-wiki in [[data-component]]).

- `search_my_notes(position)` — semantic search over the agent's own game-analyses, pattern pages, and opening notes
- `retrieve_opening_theory(moves)` — vector or keyword lookup over the agent's own `openings/` wiki
- Tactical pattern matching over the agent's own `patterns/` pages

### Retrieval tools: not permitted (contamination)

- Pre-loaded vector DBs of "every position from these 10 books" — externally built, not processed through the loop
- Pre-curated Stockfish evaluation databases
- `recognize_opening()` backed by an externally built encyclopedia — even if the retrieval algorithm is trivial, the corpus is contamination

The key criterion: *the act of reading-and-noting is part of the loop*. An agent that reads a chess book during Phase 1 and writes its own synthesis into its wiki may later retrieve from those notes. Dumping raw book content into a vector DB the agent never processed is not permitted.

### Calculation tools

The agent may use `what_if_i_play(move) → board_after` and manually recurse over candidate lines. A tool that returns "the best 3-move sequence from here" is a chess engine with its interface filed off — not permitted.

## Stockfish: post-game only

Stockfish and Lichess analysis are permitted for *post-game reflection* — synthesising what went wrong, building skills and notes from game analysis. Calling Stockfish *during* a game is not permitted: it would contaminate the Phase 2 Config 3 comparison (full-engine-as-tool as the deterministic upper bound).

## Why this rule matters for the experiment

The rule operationalises the [[deterministic-tools-hypothesis]] test cleanly. Phase 2 compares:
- Config 1: inference alone
- Config 2: inference + agent-curated skill library and tools
- Config 3: inference + a deterministic chess engine API

If tool use during play were unconstrained in Configs 1 and 2, the gap between configurations would not isolate the variable. The fairness rule ensures Config 2's advantage over Config 1 comes from *accumulated intelligence in the skill library*, not from incidental engine assistance. Config 3's advantage over Config 2 then measures the ceiling contribution of a fully deterministic tool.

An additional reproducibility consequence: chess tools that live inside the skill's `scripts/` directory are captured by `skill_repo_sha` in the logging CSV. Tools injected outside the skill are not. Routing everything through the skill preserves the SHA's meaning as a complete snapshot of the agent's configuration at game time.

## Status

Settled in the [[diary/experiment-chess/2026-05-16]] design session and now formally recorded as [[2026-06-02-tool-fairness-rulebook]] — the citable ADR for the thesis methods chapter. This page is the synthesis-layer statement; the ADR is the durable record. The pre-seeded, agent-curated wiki of [[2026-06-02-chess-agent-wiki-architecture]] is fair under the reading-and-noting clause.
