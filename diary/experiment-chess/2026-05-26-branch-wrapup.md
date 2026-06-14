---
type: diary
touched_work: [experiment-chess]
touched_concepts: [skill-acquisition-loop, deterministic-tools-hypothesis]
status: open
---

# 2026-05-26 — Wrapping up the `visualization-and-context-management` branch

## What this branch did

The branch started as "give the agent better eyes" and ended up touching
perception, prompting, retry handling, turn memory, and the logging
layout. The work splits naturally into themes, and each one has its own
diary entry from when it landed:

- **Perception tools** — `show_position`, `imagine_move`, `list_legal_moves`,
  all with material balance, attack/defense maps, and enemy king mobility.
  See [[2026-05-25-visualization-tools]].
- **Stabilization** — tightened the agent's tool surface (disabled the
  built-in todo/thread/spawn tools the chess agent doesn't need), reworked
  retry handling, fixed Gemma's split chain-of-thought markers, switched
  the agent UI to use SSE event-by-event rendering. See
  [[2026-05-26-stabilization]] and [[decisions/2026-05-26-stabilization]].
- **Endgame fixes** — `imagine_move` now flags newly hanging own pieces,
  and the skill prompt actively asks the agent to look for mates,
  especially when the enemy king has few escape squares. See
  [[2026-05-26-endgame-fixes]].
- **Context management** — per-turn fresh context via a `HistoryProcessor`
  that injects the previous turn's reasoning as the only carry-forward.
  See [[2026-05-26-context-management]] and
  [[decisions/2026-05-26-agent-turn-memory]].
- **Agent-authored turn memory** — `make_move.py` now requires a
  `--reasoning` argument that the agent writes itself at commit time. The
  text becomes the first message of the next turn. Replaced a throwaway
  LLM summariser that was hallucinating move intent from the bare UCI
  string.
- **SDK fix** — `run_script` tool description in the upstream
  `skillful-agent` repo used to say "JSON-encoded args"; this caused
  Gemma to either skip args entirely or attempt to pass JSON when scripts
  expect shell tokens. Fixed in upstream `main` and the chess venv was
  reinstalled.
- **SAN/UCI dual support** — `make_move.py` and `imagine_move.py` now
  accept either `--uci e2e4` or `--uci Nf3`. The model defaulted to SAN
  on first attempts (familiar notation from training) and only corrected
  to UCI on retry, which wasted half a turn each time. Now both notations
  work.
- **Logging reorganization** — per-PR subfolders under `backend/games/`,
  sequential `NNN_` filename prefixes inside non-baseline folders, and a
  new `pr_number` column on both CSVs. Detected automatically via
  `gh pr view` at game-record time, with fallback to the live branch name
  when `gh` is missing or there's no PR yet. Existing pre-PR ranked games
  moved into `games/baseline/` keeping their bare UUIDs.

## What got better

Perception tools were the most decisive change. Before the branch the
agent had to parse FEN strings by hand and was constantly miscounting
attackers, missing pins, and overlooking defended pieces. The `attack/
defense` lines in `show_position` and the `newly hanging` warnings in
`imagine_move` map directly onto the kinds of mistakes the agent was
making, and the win-rate at the lower elos jumped noticeably as soon as
they landed.

The biggest behavioural unlock was the **mate-seeking prompt**: telling
the agent to look at enemy king mobility in `list_legal_moves` and in
the `imagine_move` reports, and to actively chase king-cornering
sequences when material ahead. Before this, the agent would happily
maintain a 10-point material lead for 60 moves without trying for mate.
Game `ed2bfd9d` was the first decisive checkmate against a 700-elo
chess.com bot (Rd5#, move 34, with a bishop sacrifice setup at move 14).

Context management improved efficiency more than strength. The agent
spends less time re-analysing the position now because the previous
turn's reasoning is in front of it; turn budgets stay under 16 tool
calls more often. The harder-to-measure benefit is that the
infrastructure is now in place for long-term planning experiments later
in the project, where carrying multi-turn state across moves will
matter much more than it does for one-shot tactics.

## What still struggles

- **King + rook mates**. The agent rarely finds the technique even when
  winning by 10+ points of material. In practice it wins by pushing a
  pawn to promotion and mating with Q+K instead, which is inefficient
  but works. Complex multi-step mating patterns (smothered, back-rank,
  Anastasia, etc.) are not in its repertoire.
- **Occasional piece blunders**. The `newly hanging` warning fires, the
  agent reads it, and sometimes commits the move anyway. The warning
  caught the common case (moving a defender away) but doesn't override
  intuition when the agent has already convinced itself the move is
  right.
- **First-attempt move format**. Even with the SDK description fixed and
  SAN now accepted, the model occasionally still writes `imagine_move()`
  with no `--uci` argument at all. That now errors cleanly instead of
  looping silently, but it's still a wasted tool call.

## Logging migration

Reorganised `backend/games/` from a flat layout (~80 files of mixed game
JSONs and agent logs) into:

```
backend/games/
├── baseline/                                  # 26 pre-PR ranked games, bare UUIDs
├── visualization-and-context-management/      # this branch's games, NNN_ prefixed
├── ranked.csv                                 # + pr_number column
├── experimental.csv                           # + pr_number column
└── agent_elo.json
```

Four orphan game JSONs from this branch (committed on `b807601` and
later) that never made it into the CSVs were swept into the branch
folder without renumbering — they have no CSV row to update, so their
bare UUID stays the stable identifier.

The migration is in `scripts/reorganize_games.py`. It's idempotent;
re-running it after the move is a no-op. Future games land in the right
folder automatically via the new `app/folder_resolver.py` module, which
caches the result of `gh pr view` for 60 seconds.

## What's next (not part of this branch)

Merge to main, then run a fresh ELO calibration batch on the new agent
version. The baseline (which lives in `games/baseline/` and updated
ELO from 600 → some value) is the comparison point; the new batch will
write into `games/main-<next-pr-slug>/` and produce the post-merge
ranking.
