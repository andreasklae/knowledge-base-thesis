---
type: diary
touched_work: [experiment-chess]
touched_concepts: [skills-component, tools-component]
status: open
---

# 2026-05-26 — Stabilization pass on perception-tool configuration

Second change on the `visualization-and-context-management` branch.
The first change ([[2026-05-25-perception-tools-and-skill-rewrite]])
introduced three perception scripts and confirmed qualitatively that
the agent plays much better with them. This change cleans up the
failure modes that prevented games from completing.

ADR: [[2026-05-26-stabilization]].

## What surfaced in testing

User ran several games on the new configuration. Wins were
qualitatively impressive — the agent "dominated" chess.com 700 — but
no full game completed. Three layered problems:

1. **Massive looping.** One observed turn made 169 tool calls before
   hitting `max_turns` and aborting. Inspecting the trace: roughly
   half were `manage_todos` (a SDK-bundled native tool the model
   used to re-set and re-set the same 4-item plan across fresh-context
   retries), and ~10 were `use_skill` reloads. The model would burn
   through the budget without committing a move, fall into 9–10
   fresh-context retries with the same pattern, and finally resign
   on a winning position.

2. **A 400 BadRequest** from vLLM mid-stream (`Expecting ','
   delimiter: line 1 column 115 (char 114)`). Diagnosis: Gemma 4
   sometimes emits a tool-call whose JSON arguments are malformed.
   vLLM rejects the model's own output at parse time. There's no
   clean fix in our code or in skillful-agent — it's a model
   output-quality issue.

3. **Reasoning shown as garbage.** The recorded `*_agent.json` files
   had `thinking` events containing literal `<|channel>thought
   <channel|>` framing markers from Gemma's chain-of-thought
   channel, never the prose between them. Root cause: the markers
   arrive as separate streaming tokens (`<|channel>`, `thought`,
   `\n`, `<channel|>`), so the frontend's per-token regex stripper
   never matched a complete marker. The frontend also had no
   handler for the consolidated `thinking` event.

Plus four lower-priority things the user wanted addressed:

- `evaluate_position.py` as a separate agent-callable tool was
  decision overhead for what was effectively one number; the verdict
  bands ("winning") were misleading for a tactically-blind eval.
- `list_legal_moves` returned bare UCI with no SAN, no description,
  no check/mate flags.
- Per-game JSON had `white.elo: null` even when the agent's ELO was
  known. No per-move evaluation logging.
- Tool results rendered in `<pre>` with no markdown, no line
  wrapping; long lines overflowed horizontally.

## What we changed

Full per-section breakdown is in the ADR; the headlines:

- **Tighter tool surface.** Added `disabled_tools` and
  `disable_native_skills` to `AgentConfig` (in skillful-agent). The
  chess agent disables 13 native tools and all native skills. The
  observation "169 tool calls in one turn" is now mechanically
  impossible — `manage_todos` doesn't exist for this agent.
- **Per-turn budget warning + dropped `_MAX_ATTEMPTS` 30 → 10.**
  Counts tool calls inside each attempt; at 70% of `max_turns`,
  emits a UI event and flags the *next* retry to be prompted with
  an explicit "commit now" reminder. Mid-stream injection into a
  live pydantic-ai run isn't straightforward, so the model-side
  effect lands between attempts rather than mid-attempt.
- **Static eval folded into show/imagine.** `evaluate_position.py`
  removed. Both `show_position` and `imagine_move` now show a
  `Material balance:` line with the new material-focused verdict
  ("slight material lead for white", not "white winning") and a
  one-line warning that the eval is tactically blind.
- **Annotated `list_legal_moves` + full opponent moves in
  `imagine_move`.** Both now return markdown tables with UCI, SAN,
  short description, and a tactical flag (check/checkmate/stalemate).
  Opponent-replies section in `imagine_move` no longer truncates to
  the first 12 — the agent needs the full set to spot killer
  replies.
- **Markdown rendering frontend-wide.** Scripts produce markdown;
  the frontend renders it via ReactMarkdown. Long lines wrap.
  ASCII board sits in a fenced code block so monospace alignment
  is preserved.
- **Backend strips Gemma channel markers** before emitting the
  `thinking` event. Recorded JSONs now have clean prose.
- **Per-move Stockfish + static eval logged** under
  `turns[].evals` in `*_agent.json`. 200ms Stockfish probe so
  added wall-clock latency stays modest.
- **`agent_elo: {before, after}`** in the per-game JSON, separate
  from the PlayerConfig (which schema-rejects an `elo` field on
  agents by design).
- **400 BadRequest recovered** in the attempt loop instead of
  killing the game.

SKILL.md was rewritten:
- New "When to stop investigating and commit" section above the
  workflow. Concrete trigger conditions: free capture → just play
  it, forced mate → just play it, after 2–3 candidates imagined
  pick the best, same tool with same args twice → commit, same
  candidate imagined twice → commit, budget warning seen → commit.
- All `evaluate_position` references removed.
- Workflow updated to reference the new markdown output and
  baked-in material balance.

## What I expect from the next test batch

If the loop-prevention work is sufficient:

- Average tool calls per turn drops from observed 169 to single
  digits (≤10 expected; ≤20 acceptable). The dominant factor was
  manage_todos and use_skill reloads, both eliminated.
- Most turns commit on the first attempt; retries should be rare.
- Games run to completion without manual intervention.
- ELO trajectory should be visibly upward from the 684.2 baseline
  in the experimental batch (no ranked CSV write on this branch
  per [[2026-05-24-ranked-vs-experimental]] — actual measurement
  happens after merging to main).

Things to watch in the trace files:

- Is there *any* `manage_todos` call in the agent log? If yes the
  disabled-tools mechanism is misconfigured.
- Does `use_skill` appear more than once per turn? Once per turn
  is expected; multiple suggests the model is forgetting it loaded
  the skill, which is a sign of confusion about workflow.
- Does the model treat the new `Material balance` line as a
  verdict (e.g. "I have a slight material lead, time to attack")
  or as a coarse check (e.g. "the move loses material — bad
  candidate")? The warning phrasing is designed for the latter;
  if it's read as the former we may need stronger framing.
- Does `imagine_move`'s full opponent-reply table change how the
  agent reasons about replies? Specifically, does it spot
  defensive tactics in the opponent's list it would have missed
  before?
- Does the budget warning fire at all in normal play? If yes,
  that's a signal something else is still going wrong with
  in-attempt convergence.

## Reflection on what stayed out of scope

Context management. Still next-up on this branch. The
stabilization work is independent — and arguably had to come
first; you can't measure a context-management change cleanly when
the agent isn't completing games. The diary file
[[diary/experiment-chess/2026-05-25-visualization-tools]]
already has a placeholder section for it with three concrete
options on the table; that gets filled in after the next test
batch shows what the agent's current memory/recall failure modes
look like.

`guided_json` (vLLM's schema-constrained decoding for tool calls)
is also out of scope. The 400 BadRequest is now caught and
recovered, which unblocks games today. If the recovery rate is
high enough to harm wall-clock pacing in a real batch, switching
to `guided_json` becomes the natural next move on stability.

## Late-day update: reasoning panel empty in the UI

After the stabilization work above landed, the user observed that the
reasoning section in the live UI was still empty — the agent was
producing reasoning text (`text_delta` events in the recorded JSON)
but the panel showed only tool calls and results.

Root cause was on the SSE layer, not the agent: the
`/api/games/{id}/agent-events` endpoint was live-only. New subscribers
only got events broadcast after they connected. By the time the user
navigated to the board page, the early turns' `text_delta` events had
already been consumed by the live queue and discarded. The reasoning
*was* arriving over the wire, just not to anyone who hadn't been
listening since game start.

Fix: replay history on connect. `LoggingService.get_past_agent_events`
returns all events from completed turns plus the in-progress turn's
events so far; the SSE endpoint subscribes first (so live events
aren't dropped during the read), yields the past events, then enters
the live-queue loop. `AgentPanel` resets its entry list on `gameId`
change so the replay populates a clean feed.

Also took a code-cleanup pass through the harness and the frontend
panel — extracted `_record_per_move_evals` from the bot loop,
deduplicated the reasoning/post-move renderers in `AgentPanel.tsx`,
dropped a dead `extractStdout` helper and an unused `_color_name`
alias in `_eval.py`. Tests: 105 pass (the one pre-existing
`test_player_types` failure is unrelated to this work).

## Diary notes for follow-up

- Run an experimental batch (3–5 games) and inspect agent-tool-call
  histograms. Mean turn duration. Frequency of `provider_error_recovered`
  events. Pattern of budget warnings.
- Confirm `_eval.py` doesn't show up in the agent's available scripts
  list. (`registry._list_files` now skips underscore-prefixed
  files; this should be belt-and-suspenders fine.)
- Spot-check that the new SKILL.md "when to stop" guidance is being
  followed by reading a couple of complete turns: when the model has
  imagined 3 candidates and one is plainly best, does it commit?
- Once the batch looks clean, consider merging to main and running
  the official ranked calibration batch — the measurement against
  baseline that the user's "dominating" observation suggests should
  produce a visible upward delta.
