---
type: diary
touched_work: [experiment-chess]
touched_concepts: [tools-component, deterministic-tools-hypothesis, context-engineering]
status: open
---

# 2026-05-27 — Batch trace analysis: what the logs actually show

Follow-up to [[2026-05-27]]. Ran a structured scan over the 12 most
recent agent JSON files
(`backend/games/visualization-and-context-management/02[0-9]_*_agent.json`
and `030_*`, `031_*`) — that's the post-merge ranked calibration batch
plus the trailing experimental runs. Three of the five diary
observations are now grounded in counts; one is partially explained;
one needs to be rephrased.

ELO over this batch: **712.7 → 783.6** (+71 across 10 ranked games),
won 7 of 10 against chesscom-700/850 (one connection error, two
losses). Significant improvement on top of the just-merged baseline.

## Batch shape

| Game | Turns | run_script calls | use_skill | imagine errors | make_move errors |
|------|------:|-----------------:|----------:|---------------:|-----------------:|
| 020  | 36    | 109              | 19        | 18             | (in 18)          |
| 021  | 57    | 139              | 29        | 10             |                  |
| 022  | 63    | 196              | 33        | 29             |                  |
| 023  | 76    | 215              | 38        | 16             |                  |
| 024  | 76    | 247              | 39        | 42             |                  |
| 025  | 61    | 150              | 31        | 19             |                  |
| 026  | 91    | 260              | 47        | 21             |                  |
| 027  | 123   | 401              | 65        | 67             |                  |
| 028  | 129   | 398              | 66        | 31             |                  |
| 029  | 41    | 107              | 22        | 24             |                  |
| 030  | 105   | 317              | 55        | 53             |                  |
| 031  | 79    | 253              | 42        | 46             |                  |

Across all 12 games: **1424 imagine_move calls, 375 failed (26.3%)**.
**592 make_move calls, 118 failed (19.9%)**. `show_position` and
`list_legal_moves` (the two no-required-args scripts) **never failed**.
This is not a model-reasoning problem. The failures are concentrated
on the two scripts that require flags.

## Finding 1 — `make_move` "missing --uci" is a harness bug, not a model bug

Of the 118 failed `make_move` calls, **116 had the `--uci` flag
present in the args string**. argparse rejected them anyway with
`error: the following arguments are required: --uci`. The mechanism:

`skill_agent/skill_tools.py:459-463`:

```python
if args:
    try:
        cmd.extend(shlex.split(args))
    except ValueError:
        cmd.append(args)   # <-- falls back to passing the whole
                           #     string as a single positional arg
```

When the model emits

    --uci c1e3 --reasoning Developed bishop to e3 ... pressure from Black's g7 bishop ...

`shlex.split` parses left-to-right, hits the apostrophe in `Black's`,
treats it as an opening quote, scans for a closing apostrophe, doesn't
find one, and raises `ValueError("No closing quotation")`. The
fallback then passes the *entire* `--uci c1e3 --reasoning ...` string
as a single positional. argparse sees no `--uci` flag (it is inside the
positional) and dies. The error message naming `--uci` as missing is
misleading — `--uci` *was* in the args; it was eaten by a
failed shell-split.

This is a textbook case of [[aizawa2025tools]]'s "contract failure":
the tool's *operation* is correct, the model's *call* is correctly
formed, but the *contract* leaks at an intermediate parser. The
SKILL.md text "no quoting needed. Write it as plain text after
`--reasoning`" promises a contract the harness doesn't honour.

Three possible fixes, in order of cost:

1. **Cheapest:** in `run_script`, do not call `shlex.split` on a
   string that contains `--reasoning` (or treat the post-`--reasoning`
   tail as opaque text). Or use `shlex.split(args, posix=False)` which
   doesn't try to honour unmatched quotes — but that has its own edge
   cases.
2. **Medium:** change the contract: have `run_script` accept `args`
   as a **list of strings** instead of a single shell-format string.
   Then the model emits `["--uci", "c1e3", "--reasoning", "..."]`.
   No shell parsing, no apostrophe failure. Requires SKILL.md updates
   and pydantic-ai schema changes; affects every skill that uses
   `run_script`.
3. **Most ambitious:** Pydantic-AI-side schema. Each script declares
   typed parameters; the agent calls a typed function; `run_script`
   becomes an implementation detail. This is closer to MCP semantics
   ([[mcp-vs-skills]]).

## Finding 2 — `imagine_move` empty-args loop is real but partially self-correcting

**337 imagine_move calls (of 1424) had `args=""`.** Of those, most
self-correct on the next call: the script returns
`{"ok": false, "error": "Missing --uci. ... Example: ..."}` and the
model immediately retries with `--uci xxxx`.

But **44 turns across the batch had 3+ consecutive identical
empty-args imagine_move calls**, including one turn (game 020 turn 13)
with **14 identical failed calls in a row** before the budget warning
triggered a fresh-context retry. The retry then succeeded on the first
attempt.

The error-string contains the exact retry-hint
([[mayo2026gemma4tools]] pattern: be specific about how to fix it).
Sometimes the model uses it; sometimes it loops. The pattern of "loops
within a turn, succeeds on fresh-context retry" suggests context
contamination: once the model has committed `args=""` early in the
turn, it's reading its own prior empty call as authoritative and
re-emitting it. The fresh-context boundary at the start of the next
attempt breaks the spell.

Why `imagine_move` and not `show_position` or `list_legal_moves`? The
latter two take **no required args**. The model has formed the
heuristic *"the `args` field is optional/empty"* from those two and
fails to override it for `imagine_move`. The asymmetry the diary
flagged is real, but it is not a SKILL.md issue — SKILL.md correctly
shows `--uci e2e4`. It is a **tool-surface asymmetry** between
no-arg scripts and required-arg scripts, exacerbated by the fact that
`run_script` takes `args` as one stringy field.

Same Finding 1 fix (`args` as a list, or a typed pydantic-ai tool
shape) would eliminate this too: the schema would mark `--uci` as
required and constrained decoding (or pydantic-ai's own validation)
would refuse to emit a call without it.

## Finding 3 — `use_skill` reload pattern is NOT every-turn

The diary said "it loads the skill every turn." The data:

- **460 turns with exactly 1 use_skill call** (≈49%).
- **464 turns with 0 use_skill calls** (≈49.5%).
- **13 turns with 2+ use_skill calls** (≈1.4%).
- **473 of 937 turns** open with `use_skill` as the first tool call.

So roughly half the turns reload the skill, not every turn. The
pattern correlates with fresh-context boundaries (a retry inside a
turn re-issues `use_skill` because the per-turn context is wiped per
[[2026-05-24-per-turn-fresh-context]]). Net cost is still real — for
game 027 alone that's 65 `use_skill` calls = ~65 round-trips × SKILL.md
in the response — but the priority of this fix should drop.

The two correct framings:
- **"Skill reloads on every fresh context"** — yes; this is by design
  per the per-turn fresh-context model.
- **"Skill reloads on every turn"** — no; the model successfully
  caches the skill across the first-attempt context within a turn.

## Finding 4 — Hanging-piece warnings: 0 fires in 1424 imagine_move calls

This was a surprise. The diary noted false positives on the
hanging-piece warning. The data shows **zero `⚠ hanging` warnings and
zero "Newly hanging own pieces" non-(none) entries across the entire
batch.** The warning code paths exist in `imagine_move.py:206-240` and
`:157-190` but never fired during these 12 games.

Two readings:

- **The heuristic is too conservative.** The count-attackers /
  count-defenders gate is the right *shape* but with thresholds that
  rarely trip. The [[2026-05-26-branch-wrapup]] session-3 note
  already flagged this for the `count(attackers) == count(defenders)`
  case (bishop defended by queen vs pawn attacker — silent because the
  count math is balanced even though the value math is −230cp).
- **The agent is not imagining moves that would trigger it.** Selection
  bias: the imagine_move calls in this batch are dominated by
  reasonable candidate moves, not "I will give up my queen" moves.

The diary's "false positive on a protected piece" observation cannot
be checked from this batch — no warnings fired at all. Need to
either (a) reproduce a specific position the user remembers, or
(b) lower the heuristic threshold until the rate is non-zero and then
review the resulting fires. **Without a concrete instance the false-
positive claim cannot be acted on.**

## Finding 5 — Mate-in-1-hanging blunders: this batch's losses look different

Spot-checked game 023 (a 0-1 loss). Final position before mate: agent
was **+14.00 material** but in a forced sequence where the only legal
move (`d7d1`, blocking check) walked into `Rxd1#` (queen on g6 didn't
defend d1, king on g1 had no back-rank escape).

The agent skipped `imagine_move` because the move was forced. There is
nothing the perception layer can do here — the loss was already
sealed several moves earlier. The deeper failure was not seeing that
two moves back, allowing the opponent rook onto c1 was inviting a
back-rank mating net. That is a **planning depth** problem, not a
perception problem. Adding mate-in-1-after-opponent-reply to
`imagine_move` would help in *some* positions but doesn't help the
endgame mating-net failure.

Recommend: the diary's framing of "hanging mate in one" should be
narrowed. Pull 2–3 specific positions where the agent committed a
*choice* move (not a forced one) that allowed mate-in-1, and study
those. Mate-in-1 detection on opponent reply is still a sensible
addition, but the calibration-batch losses are mostly mating-net
strategic failures, not single-move tactical blindspots.

## What changes in the priority order from [[2026-05-27]]

Revised:

1. **Fix `args`-as-shell-string contract.** This single fix
   eliminates Finding 1 (118 make_move failures, ~20% rate) and
   plausibly most of Finding 2 (44 multi-call loops within a turn).
   Cheapest version is the `posix=False` shlex tweak or a
   reasoning-tail extraction; medium version is `args: list[str]`.
2. **Fork detection.** Still genuinely missing, still concept-shaped.
3. **Mate-in-1-after-opponent-reply in imagine_move.** Useful even if
   not the dominant failure in this batch.
4. **Hanging-piece SEE-lite** (value-aware exchange evaluation).
   [[2026-05-26-branch-wrapup]] session-3 follow-up.
5. **Pre-inject SKILL.md, disable use_skill for this agent** — drop
   in priority; the cost is half what the diary assumed.
6. **"Near-mate hint" surfacing** — still concept-shaped, still
   carefully sized.

The hanging-piece false-positive claim is unverifiable from this batch.
Park it until a specific instance is recorded.

## On the harness question

The trace strongly increases my prior that the chess agent is being
held back by harness-level decisions, not model capability:

- `make_move` succeeds on 80% of calls (474/592) — the model is
  forming legal, well-reasoned chess moves. It fails on 20% to a
  *parser* bug, not a chess bug.
- `imagine_move` succeeds on 74% — and most failures are recoverable
  on the next call. The 26% failure rate is mostly the same harness-
  level shell-string contract problem.
- The two scripts that don't take args have **0% failure rate** in
  1500+ calls. The model can drive the tools when the contract is
  tight.

This is the [[deterministic-tools-hypothesis]] showing up from an
unexpected angle: the *tool* is deterministic, but the *contract*
between non-deterministic agent and deterministic tool is
non-deterministic too, and that's where errors concentrate. See
[[mirko2026gemma]] and [[mayo2026gemma4tools]] for two grey-lit
treatments of how to tighten that contract (constrained decoding,
specific retry-hints).

This does not by itself justify replacing skillful-agent. It does
justify a focused ADR on the `args` contract — and depending on what
shape it takes, opens the door to either a small surgical fix
(option 1) or a deeper schema-driven rework that pulls in pydantic-ai
typed tools and possibly `guided_json` for argument constraint
(options 2–3). Worth thinking carefully about scope before committing.
