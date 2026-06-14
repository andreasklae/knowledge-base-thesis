---
type: concept
sources: [ericsson1993deliberate, sequoia2026karpathy]
related_concepts: [learning-as-temporal-dimension, skills-component, data-component, tool-fairness, deterministic-tools-hypothesis]
related_work: [experiment-chess]
status: draft
updated: 2026-05-19
---

# Skill-Acquisition Loop

The **skill-acquisition loop** is the self-correcting learning cycle at the centre of [[experiment-chess]] Phase 1. It is the agent-side analogue of deliberate practice [[ericsson1993deliberate]]: structured, feedback-driven accumulation of procedural knowledge over many iterations, with the key difference that the agent writes its own skill artefacts rather than relying on a human coach.

## The loop structure

1. **Play** — the agent plays a game (white vs a Maia calibrated-Elo opponent).
2. **Analyse** — post-game, the agent uses Stockfish and/or Lichess analysis to identify mistakes (blunders, inaccuracies, missed tactics, positional errors).
3. **Synthesise** — the agent writes or updates pages in its parallel chess wiki: opening theory pages, tactical patterns, endgame principles, game-analyses. The wiki is the agent's accumulated knowledge in persistent compiled-summary form (see [[data-component]]).
4. **Package** — where a pattern is frequent enough or a procedure clear enough, the agent wraps it as a skill in its skill library — a markdown instruction file with associated scripts for board-state queries.
5. **Batch boundary** — after N games at the same `skill_repo_sha`, the agent reflects on the batch, updates the library, and starts a new batch with a new SHA committed.
6. **Plateau detection** — Phase 1 ends when Elo stops improving across successive batches by more than a defined threshold, defined before Phase 1 starts (see [[experiment-chess]] risk section).

## What a batch is

A batch is the set of games played at one `skill_repo_sha`. The SHA is the Git commit hash of the skill library repo at the time of play. This makes the loop reversible and analysable: `git diff <sha_before> <sha_after>` shows exactly what the agent changed between batches; comparing Elo gain to the diff content lets the thesis ask *which skill additions or revisions produced the biggest improvement*.

The batch is the natural unit for the thesis's learning-curve analysis, not just an arbitrary session boundary.

## The parallel chess wiki

The agent's accumulated chess knowledge is structured as a parallel LLM wiki — the same [[karpathy2025wiki]] compiled-summary pattern used by this knowledge base, but domain-specific:

- `openings/` — synthesised opening theory pages the agent built from games
- `patterns/` — tactical and positional patterns with examples
- `endgames/` — endgame principles
- `game-analyses/` — per-game post-mortems

This wiki is the *agent-curated corpus* referenced in the [[tool-fairness]] rulebook: retrieval over this wiki during play is permitted; retrieval over externally-built encyclopedias is not. The architecture choice and the methodological constraint are aligned.

## Connection to the thesis claim

The loop is the direct test of the framework's claim that the data and skills components can be *filled in automatically* through structured iteration, rather than requiring manual curation by the user. Phase 1 answers: does self-directed accumulation of procedural knowledge produce measurable Elo growth? Phase 2 then asks how much of that growth is attributable to the skill library vs to a deterministic chess engine (see [[deterministic-tools-hypothesis]]).

Karpathy's [[sequoia2026karpathy]] observation — that the chess-capability jump between GPT-3.5 and GPT-4 was largely a lab data-curation decision — is the substrate-side version of this claim. The loop tests the user-side version: that the same kind of gain is reachable *around* a fixed model by systematic skill accumulation.

## Current implementation status (2026-05-19)

The Phase 1 scaffold is in place (backend, frontend, game persistence, logging, AgentPlayer with skillful-agent SDK). The agent plays via a `chess-player` skill with `list_legal_moves.py` and `make_move.py` scripts in the skill directory. The first end-to-end game (agent white vs Maia 1500) has not yet been run. See [[diary/experiment-chess/2026-05-19]].

Open items before the loop runs:
- Backend tests for `AgentPlayer` and `LoggingService`
- Wire `skill_repo_sha` to the actual chess experiment git history (currently hardcoded empty string)
- Define the plateau criterion (threshold + minimum batch count)
