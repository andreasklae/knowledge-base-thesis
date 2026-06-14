---
type: decision
status: accepted
supersedes: null
---

# Ranked vs experimental games: PR-as-version logging

## Context

Until 2026-05-24 the chess experiment recorded every agent game in one CSV (`games.csv`) and stamped each row with the live git HEAD SHA (`skill_repo_sha`). This had three problems for thesis-grade reproducibility:

1. **A SHA is not a unit of "agent configuration"**, but a commit. A single conceptual change (e.g. "switch to Gemma + reason-first prompt + per-turn clear") is three commits, three different SHAs, none of which is a meaningful version marker.
2. **Reverting a buggy change loses code↔ELO coherence.** ELO state in `agent_elo.json` was updated based on games stamped with a now-deleted SHA. The numbers and the code that produced them diverge.
3. **No structural distinction between "playing with the agent" and "measuring the agent."** Lobby games, mid-iteration test batches, and formal calibration batches all wrote to the same CSV and updated the same ELO state. ELO contamination was one accidental click away.

## Decision

Adopt a two-tier logging scheme with hard enforcement at the boundary.

### Two CSV files

| File | When written | Updates `agent_elo.json`? |
|---|---|---|
| `backend/games/ranked.csv` | Game played while the chess repo is on `main` **and** the working tree is clean | yes |
| `backend/games/experimental.csv` | Any other state — lobby games, batches on a feature branch, batches with uncommitted changes | no |

The split is determined per-game at record time by `app.repo_state.is_ranked_context()`, which inspects the live git state. There is no per-game opt-in/out — the decision is mechanical and unambiguous.

### Schema

Both CSVs share one schema (so analysis tooling only learns one shape):

| column | meaning |
|---|---|
| `game_id`, `batch_id`, `batch_name`, `datetime` | identifiers and timing |
| `phase` | `ranked` or `experimental` |
| `branch` | git branch at record time. Per-game commit SHA was previously also recorded but was removed 2026-05-26 in favour of `pr_number` as the agent-version identifier — see [[diary/experiment-chess/2026-05-26-branch-wrapup]] |
| `white_type`, `black_type`, `opponent`, `opponent_elo` | players |
| `result` | `1-0` / `0-1` / `1/2-1/2`, or `""` for aborted |
| `aborted_reason` | non-empty when a player exception aborted mid-play |
| `elo_before`, `elo_after` | meaningful for `phase=ranked`; empty for experimental |
| `model`, `temperature` | model identity, sampling temp |
| `agent_log_path` | relative path to the agent log JSON, under a per-PR subfolder: `<folder>/<NNN_>?<game_id>_agent.json` |
| `analysis_path` | relative path to external analysis (lichess/chess.com); empty by default, populated post-hoc when games are sent out for analysis |
| `pr_number` | GitHub PR number for the agent version that produced the game; empty when no PR resolvable (e.g. branch with no open PR, or pre-PR baseline rows). Added 2026-05-26 — see [[diary/experiment-chess/2026-05-26-branch-wrapup]] |

The previous `skill_repo_sha` column was retired in favour of `branch` + `commit_sha`. As of 2026-05-26, `commit_sha` is also removed — `pr_number` is the durable agent-version identifier, and `branch` is enough live git state for the row.

### Game folder layout

Game JSONs and agent logs live in per-PR subfolders under `backend/games/`:

- `baseline/` — pre-PR ranked games (commit `afe43c0`), bare UUIDs
- `<pr-slug>/` — one folder per PR or branch, with files prefixed by a
  3-digit chronological sequence number (`042_<game_id>_agent.json`)
- The aggregate files (`ranked.csv`, `experimental.csv`, `agent_elo.json`)
  stay at the top level

The destination is resolved per-game by `app/folder_resolver.py`, which
queries `gh pr view` (cached 60s) and falls back to the live branch name
when `gh` is unavailable or no PR exists.

### PR-as-version

The intended workflow is:

1. Branch off `main` for any agent-affecting change.
2. Iterate freely. Run batches on the branch — they write to `experimental.csv`, ELO is frozen. Use the experimental rows for sanity-checking before merging.
3. Merge the PR to `main`.
4. Run the **official calibration batch** on `main` post-merge. These games write to `ranked.csv`. ELO updates.
5. The calibration commit lands on `main` directly (or via a tiny "data only" PR). Reverting the original PR with `git revert` reverses both the code and the CSV rows together.

PRs are the conceptual unit of "agent configuration version." A merged PR boundary in `main`'s history is a calibration boundary. Closed-without-merge PRs leave their experimental rows untouched as a research record of what was tried.

### Enforcement

Three places enforce the policy:

- **`LoggingService.record_game`** routes every row to the correct CSV based on `current_phase()`.
- **`BatchRunner._handle_game_finished`** checks `is_ranked_context()` before applying any result to `agent_elo.json`. On a branch or dirty tree the ELO update is skipped and logged.
- **The frontend `RepoStateBanner`** polls `/api/repo-state` every 5 seconds and shows a coloured banner ("RANKED" green / "EXPERIMENTAL" orange) on the lobby and batch pages, with the current branch, short SHA, and dirty flag. The operator can never be confused about which mode they're in.

### Storage in git

All game data is committed to git, not gitignored:

- `ranked.csv`, `experimental.csv` — the experiment's source of truth.
- `agent_elo.json` — materialised view of `ranked.csv` (could be rebuilt from it; cached for cheap reads).
- `<game_id>.json` (board state) — full replayability.
- `<game_id>_agent.json` (reasoning trace) — evidence per move for thesis analysis.
- `batches/<batch_id>.json` — batch metadata, also part of the record.

This makes the entire experimental history auditable from `git log` alone, and makes `git revert` the recovery primitive for bad calibration runs.

## Consequences

- **Recovery from a bad PR is `git revert`**: code and data come back together.
- **ELO ↔ code coherence is guaranteed** by construction — every row that contributed to `agent_elo.json` came from a commit that is still in `main`'s history. If you `git revert` it, `ranked.csv` no longer has that row, and `agent_elo.json` should be rebuilt to match (todo: a `scripts/rebuild_elo.py`).
- **The methods chapter can describe the experiment as a sequence of merged PRs**, each with starting ELO → ending ELO and the calibration batch's `commit_sha`. The narrative spine is concrete.
- **Lobby games are now part of the experiment record** (as experimental rows). Useful for debugging but worth being aware of: every time you click "agent vs Maia 1500" in the UI, a row appears.
- **Two clean directories shipped empty in git**: `backend/games/.gitkeep` and `backend/batches/.gitkeep`. Both CSVs are created on first backend startup with their header rows.
- **The previous `games.csv` is removed.** Pre-2026-05-24 data lived under the old single-CSV / `skill_repo_sha` schema and is not migrated; the file was empty (header only) at the moment of the change because no calibration batches had been run yet under the Gemma backend.
- **Open follow-up**: write `scripts/rebuild_elo.py` so a `git revert` on a calibration PR can be paired with a one-command ELO rebuild. Tracked in `work/experiment-chess` open items.

## Related decisions

- [[2026-05-20-elo-and-batch-runner]] — ELO formula and matchmaking
- [[2026-05-24-initial-elo-600]] — informed starting prior
- [[2026-05-24-reason-before-move]] — reasoning must precede the move
- [[2026-05-24-per-turn-fresh-context]] — per-turn fresh context (baseline calibration)
- [[work/experiment-chess]] — main experiment design page
