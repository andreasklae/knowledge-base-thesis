---
type: decision
status: accepted
---

# 2026-05-26 — Stabilization pass on the perception-tool configuration

Follow-up to [[2026-05-25-perception-tools-and-skill-rewrite]].

## Context

Initial testing of the perception-tool configuration on the
`visualization-and-context-management` branch confirmed the original
hypothesis qualitatively — the agent plays meaningfully better against
chess.com 700 with `show_position` and `imagine_move` available, the
user described it as "dominating". However, no full game completed
because of layered stability problems:

- One observed turn made **169 tool calls** before the runner hit
  `max_turns` and aborted the run. Roughly half were `manage_todos`
  calls (the SDK-bundled todo tool, used by the model to re-set and
  re-set the same 4-item plan across fresh-context retries), and
  another ~10 were `use_skill` reloads. The model would burn through
  the budget without committing a move, fall into
  `_MAX_ATTEMPTS=10` retries (which had been bumped to 30 during
  manual testing), and finally resign on what was — by chess content
  — a winning game.
- A `BadRequestError: Expecting ',' delimiter: line 1 column N` was
  returned by vLLM partway through some turns, killing the whole
  game and forcing manual resume. This is Gemma 4 producing a
  tool-call whose JSON arguments are malformed; vLLM's parser
  rejects the model's own output mid-stream. There is no clean fix
  inside our codebase or inside skillful-agent — it is an
  upstream model-output-quality issue.
- The recorded `thinking` events in `*_agent.json` contained literal
  `<|channel>thought<|channel>` framing tokens from Gemma's
  chain-of-thought channel rather than the prose between them. The
  frontend's per-token regex stripper never matched because the
  markers arrive split across multiple tokens. The frontend also had
  no handler for the consolidated `thinking` event at all.
- The `evaluate_position.py` script encouraged the model to make a
  separate tool call for what was effectively one number. Output
  rendered as bare text in `<pre>` blocks without wrapping; long
  lines forced horizontal scroll the user couldn't see by default.
  `list_legal_moves.py` returned a bare UCI array with no SAN, no
  description, no tactical flags.
- The per-game JSON's `white.elo` was always null even though the
  agent's ELO was known (it lives separately in `agent_elo.json` and
  in the CSV's `elo_before`/`elo_after` columns). No per-move
  evaluation telemetry was recorded.

The intended outcome of this stabilization pass: games run to
completion reliably; the model's tool surface is tight enough that
runaway loops are mechanically prevented; the UI shows what's
actually happening; per-move evaluation is logged so the thesis can
analyse where in the game the model is strong.

## Decision

### 1. Suppress noise tools at AgentConfig level

`AgentConfig` (in skillful-agent) gained two fields:

- `disabled_tools: list[str]` — names of built-in tools to skip
  registering with the pydantic-ai runner. Matched tools never
  appear in the model's callable surface.
- `disable_native_skills: bool` — when True, skip loading
  SDK-bundled skills under `native-skills/`. The chess agent has no
  reason to invoke `web-search-free`.

The chess agent disables: `manage_todos`, `register_skill`,
`scaffold_skill`, `write_skill_file`, `read_reference`,
`call_client_function`, `compress_message`, `retrieve_message`,
`compress_all`, `read_thread`, `reply_to_thread`, `archive_thread`,
`spawn_agent`. Only `use_skill` and `run_script` remain.

The implementation lives in skillful-agent itself — patches there
will be pushed to the SDK's main once the chess experiment confirms
the change is stable. This is a generally-useful capability for
domain-specific agents.

### 2. SKILL.md owns commit guidance, not "more tools"

The SKILL.md was rewritten with three structural changes:

- A new **"When to stop investigating and commit"** subsection above
  the turn workflow. Concrete trigger conditions: "if you find an
  obviously good move (free capture, forced mate, winning sequence
  with no real downside) commit it without further verification";
  "after imagining 2–3 serious candidates, pick the best and
  commit"; "if you find yourself calling the same tool on the same
  arguments twice in a row, or imagining the same candidate twice,
  you are looping — commit now".
- A note that the harness will warn the model when it is more than
  70% of the way through the per-attempt tool budget without
  committing (see §3 below); seeing that warning means commit now.
- All references to `evaluate_position.py` removed; the material+PST
  eval is now folded into `show_position` and `imagine_move`
  output, with new material-focused verdict phrasing (see §4).

### 3. Per-turn budget warning + restore `_MAX_ATTEMPTS = 10`

`agent_player.py` now counts tool calls inside each attempt. When
the count crosses 70% of the runner's `max_turns` (currently 16),
the harness:

- Emits a UI-visible `budget_warning` event.
- Sets a flag so the *next* retry, if one fires, is prompted with
  an explicit "you ran more than N tools last time without
  committing — pick a move and play it" reminder.

Mid-stream injection into a live pydantic-ai run is not
straightforward, so the model-side effect of the warning lands
between attempts rather than mid-attempt. In practice this is fine:
the warning is a safety net for the case where the model failed to
self-regulate within the SKILL.md guidance, and a retry with
explicit framing is a reasonable place to land that signal.

`_MAX_ATTEMPTS` is restored to **10** (it had been bumped to 30 in
manual testing). With manage_todos disabled and the budget warning
in place, retries should be rare; 10 leaves comfortable margin.

### 4. Static eval folded into show/imagine; `evaluate_position.py` removed

The static eval (material + Michniewski piece-square tables, per-side
king-table selection) was small and cheap; making it a separate
agent-callable tool introduced decision overhead with no real
benefit. It now appears as a single line:

- In `show_position` output: `Material balance: +0.30 (slight
  material lead for white)`.
- In `imagine_move` output: `Material balance: +0.30 → +0.20
  (Δ -0.10, slight material lead for white)`.

Both lines are followed by a one-line warning that the eval is
material+PST only and tactically blind. **Verdict band phrasing was
rewritten** away from "winning" / "losing" (which a tactically
blind eval cannot honestly claim) to "material balanced",
"roughly balanced", "slight material lead for {side}", "clear
material lead for {side}", "decisive material lead for {side}".

Helpers extracted to `backend/skills/chess-player/scripts/_eval.py`
(underscore-prefixed; the SDK's registry skips underscore-prefixed
files when listing a skill's scripts, so the agent cannot call it
as a tool). The `evaluate_position.py` script is deleted; its tests
moved to `test_eval_helpers.py`.

### 5. Annotated `list_legal_moves` + full opponent moves in `imagine_move`

`list_legal_moves` now returns a markdown table with columns UCI,
SAN, short description ("bishop takes knight on c4", "kingside
castle"), and a tactical flag (`check` / `checkmate` / `stalemate`
/ blank). The UCI column is still the exact string the agent
passes to `make_move --uci`.

`imagine_move`'s opponent-replies section was previously truncated
to the first 12 UCI strings. It now shows the full annotated table
— the agent needs to see *every* reply to spot the killer move.

The annotation helpers (`annotate_move`, `render_moves_table`) live
in `_eval.py` so both scripts share them.

### 6. Markdown output everywhere; frontend renders it

`show_position`, `imagine_move`, and `list_legal_moves` now produce
markdown output: section headings (`## Move`, `## Opponent legal
replies`), inline bold for key facts (`**FEN:** ...`), fenced code
blocks for the ASCII board, tables for the legal-move lists.

The frontend's `AgentPanel.tsx` renders these via `ReactMarkdown`
with `remark-gfm`, so headings, tables, and code blocks display
properly. The CSS for `agent-result-pre` was changed from
`white-space: pre` to `pre-wrap` with `overflow-wrap: anywhere` so
long lines wrap rather than scroll horizontally. The ASCII board
keeps `white-space: pre` inside its own fenced block so columns stay
aligned.

A new `budget_warning` event is rendered as a small amber-tinted
row in the agent feed when the per-attempt budget threshold is
crossed.

### 7. Backend strips Gemma channel markers before logging the thinking event

Gemma 4 wraps its chain-of-thought in `<|channel>thought ...
<channel|>` framing tokens. These arrive as separate streaming
deltas (e.g. `<|channel>`, `thought`, `\n`, `<channel|>`) so a
per-token regex never matches. The harness now accumulates text
deltas into a buffer and strips on the accumulated string at
flush time, before emitting the `thinking` event. The frontend
keeps its own stripper as a defensive belt on the live `text_delta`
stream, and now applies it on the accumulated reasoning content
at render time rather than per-delta.

The recorded `*_agent.json` now contains clean reasoning prose
instead of channel-marker garbage — relevant for post-hoc analysis
and for the thesis chapter that will quote model reasoning.

### 8. Per-move evaluation telemetry

Each agent turn now records (in the per-game `*_agent.json` under
`turns[].evals`):

- `stockfish_cp_before` / `stockfish_cp_after` — Stockfish eval at
  depth-capped 200ms time limit (separate from the UX-facing
  advantage-needle call, which still runs at the configured depth).
  White-positive centipawns. `None` if Stockfish is unavailable.
- `static_cp_before` / `static_cp_after` — the chess-player skill's
  material+PST eval, computed via `_eval.evaluate`. White-positive
  centipawns.
- `move_time_ms` — wall-clock time the agent spent producing the move.

These let the thesis analyse where in a game the model loses
material (Stockfish delta from before to after), where the model's
own static eval disagrees with Stockfish (potential
misunderstanding), and how much wall-clock time individual moves
cost.

### 9. agent_elo in per-game JSON

PlayerConfig schema deliberately rejects an `elo` field on
agent players (the agent's ELO is set by the experimental harness,
not the request that creates the game). The per-game JSON now
carries a separate top-level `agent_elo: {before, after}` block
when the values are known, and omits it when they aren't. The
batch runner re-persists the game JSON after the game finishes so
both `before` and `after` are captured.

### 10. SSE event replay on subscriber connect

The agent-events SSE endpoint was originally live-only: new subscribers
only received events broadcast *after* they connected. Anyone who
opened the board page mid-game saw an empty reasoning panel for every
prior turn because those `text_delta` events had already been consumed
by the live queue and discarded. Hard to notice in batch runs; obvious
the moment a human spectator joins a long game.

The fix: `LoggingService.get_past_agent_events` returns all events
from completed turns plus any events already emitted in the current
in-progress turn. The SSE endpoint subscribes first (so no live
events are dropped during the read), then yields all past events,
then enters the live-queue loop. The frontend resets its entry list
on `gameId` change so the replay populates a clean feed.

Side note: the in-progress turn is included on purpose. Anyone who
opens the board mid-turn sees the partial reasoning so far, then
picks up live deltas at the seam — much better UX than a blank panel
followed by a tool-call action.

### 11. 400 BadRequest recovered, not fatal

Gemma 4 sometimes emits a tool-call whose JSON arguments are
malformed (missing comma, unescaped quote). vLLM rejects the
streaming response with a 400 `Expecting ',' delimiter` error.
The harness now catches this specific provider error in the
attempt loop, emits a `provider_error_recovered` event, and
retries with cleared conversation rather than crashing the game.

This is a model-output-quality issue, not something we can fix
in our code — but we can fail gracefully instead of forcing the
user to manually resume the game.

## Consequences

- The model's tool surface is mechanically narrower. The
  observation that one turn used 169 tool calls is no longer
  possible: with manage_todos and friends disabled and the
  budget warning between attempts, a turn that doesn't commit
  inside `max_turns=16` triggers a retry with a strong reminder,
  and the resignation kicks in cleanly after 10 attempts
  rather than after an order-of-magnitude longer.
- Every game's per-game JSON now carries `agent_elo` (when
  applicable) and a `turns[].evals` block with both Stockfish
  and static evals. The thesis chapter can analyse move quality
  over the course of a game from this alone, without needing to
  re-run Stockfish post-hoc.
- The frontend reasoning panel shows actual model reasoning
  prose rather than channel-marker garbage, and tool results
  render as proper markdown with wrapped long lines.
- This is the second methodology-affecting change on the
  `visualization-and-context-management` branch. Per
  [[2026-05-24-ranked-vs-experimental]], no ranked games are
  logged from this branch. Merging to `main` and re-running the
  ranked calibration batch will measure the ELO delta vs the
  684.2 baseline once the user is satisfied with stability.
- The `disabled_tools` and `disable_native_skills` mechanisms
  added to skillful-agent are generally useful — any
  domain-specific agent benefits from the ability to narrow its
  tool surface. These should ship to skillful-agent's `main`
  branch as a separate PR.

## Open items

- After this branch merges, run an experimental batch (3–5 games)
  to verify stability, then run a ranked calibration batch on
  `main`.
- Context management is still the planned next change on this
  branch (see [[diary/experiment-chess/2026-05-25-visualization-tools]]).
- If the 400 BadRequest fires often enough to harm pacing,
  consider enabling vLLM's `guided_json` schema-constrained
  decoding for tool calls. Out of scope for this pass.
