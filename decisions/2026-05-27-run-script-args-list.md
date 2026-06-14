---
type: decision
status: accepted
---

# 2026-05-27 — `run_script` args contract: shell string → list of strings

## Context

The chess experiment ([[experiment-chess]]) calibrates ELO by running
Gemma 4 31B against chess.com bots through skillful-agent (the SDK)
and pydantic-ai (the LLM client) backed by vLLM. Trace analysis of
the 12 most recent ranked-batch games
([[2026-05-27-batch-analysis]]) identified a single harness bug that
accounts for the majority of two of the five user-observed failure
modes ([[2026-05-27]]).

The SDK's `run_script` tool
(`software/skillful-agent/skill_agent/skill_tools.py:431`) takes
`args: str = ""` — a single shell-format string — and parses it
with `shlex.split(args)` before forwarding to `subprocess.run`. When
the model emits a `make_move.py` call with free-text reasoning that
contains an apostrophe (e.g. `--reasoning Black's bishop ...`),
`shlex.split` interprets the apostrophe as an opening quote, scans for
a closing quote that never comes, and raises
`ValueError("No closing quotation")`. The fallback path
(`cmd.append(args)`) passes the *entire* `--uci c1e3 --reasoning ...`
string as a single positional argument. argparse then fails with
`error: the following arguments are required: --uci` — even though
`--uci` was syntactically present in the call.

Counts across 12 ranked-calibration games:

- `make_move.py`: **118 of 592 calls failed (19.9%)**, of which
  **116 had `--uci` in the args** but were rejected by argparse
  due to the shlex-split / fallback path.
- `imagine_move.py`: **375 of 1424 calls failed (26.3%)**, of which
  **337 had empty `args`** and 44 turns showed 3+ consecutive
  identical empty-args calls. The worst case is a single turn with
  14 consecutive empty-args `imagine_move` calls before the budget
  warning fired a fresh-context retry; the retry succeeded
  immediately. Hypothesis: once the model commits to `args=""` early
  in a turn (a heuristic transferred from `show_position.py` and
  `list_legal_moves.py`, which both take no args), it reads its own
  prior empty calls as authoritative and re-emits them; the fresh-
  context boundary at the start of the next attempt breaks the
  spell.
- `show_position.py` and `list_legal_moves.py` (no required args):
  **0% failure rate** across 775 combined calls.

The asymmetry is conclusive: scripts that don't take `args` work
flawlessly; scripts that require `--flag value` args fail at
20–26%. This is a tool-surface contract problem, not a chess- or
model-reasoning problem.

Two independent grey-lit sources surface the same shape of failure
and a tighter-contract fix:

- [[mirko2026gemma]] reports that Pydantic AI's default `ToolOutput`
  pattern is unreliable with Gemma 4 via Ollama; switching to
  `NativeOutput` (which engages Ollama's `format=` JSON-schema
  constrained decoding) plus temperature 0.2 fixes it. The shape of
  the fix is *tightening the contract* between agent and tool.
- [[mayo2026gemma4tools]] documents a from-scratch Gemma 4 tool-
  calling loop where the empty-output case is handled by returning a
  *specific* retry hint. The chess-experiment scripts already do
  this; the hint exists but the model sometimes can't act on it,
  presumably because the malformed call is reaching subprocess via
  the harness's shell-string fallback rather than being rejected at
  the schema layer.

The root cause is shared with [[2026-05-26-stabilization]] problem 2
(vLLM 400 BadRequest on malformed Gemma tool-call JSON), in a
different layer of the same stack: when the agent/tool contract is
expressed as free-form strings, small models malform them. The
correct fix is to remove the free-form string from the contract.

## Decision

Change `run_script`'s `args` parameter from `str` to `list[str]`.
Each element of the list becomes one entry in `sys.argv` of the
spawned script. No shell parsing, no quoting rules, no `shlex.split`,
no fallback path.

The contract is enforced by pydantic-ai's tool-call schema (the
parameter is typed `list[str]`), which means the model must emit a
JSON array of strings or the tool call is rejected at the schema
layer before it reaches our code. This is the constrained-decoding
analogue at the parameter level: not in vLLM's `guided_json`, but in
the pydantic-ai schema itself.

Concrete shape:

```python
# Before
run_script("chess-player", "make_move.py", "--uci e2e4 --reasoning ...")

# After
run_script("chess-player", "make_move.py", ["--uci", "e2e4", "--reasoning", "..."])
```

For scripts that take a JSON payload as `sys.argv[1]` (e.g. the
`learner` native skill's `save_doc.py`), the list contract wraps the
JSON string as a single-element list:

```python
# Before
args='{"skill_path": "...", "source": "..."}'

# After
args=['{"skill_path": "...", "source": "..."}']
```

This is structurally identical — `sys.argv[1]` is still the JSON
string — only the transport changes.

### Scope

**Two repos change:**

1. **skillful-agent (the SDK):** `skill_tools.py` (the
   `run_script` signature and body, plus the tool description that
   the model reads), `system_prompt.md` (the one-line tool list),
   plus the native-skill SKILL.md files (`learner/`, `web-search/`)
   that document `run_script` examples. Native-skill *scripts* do
   not change — they already consume `sys.argv[N]` in ways the new
   contract supports.

2. **experiments/chess (the consumer):** `chess-player/SKILL.md`
   (all `run_script` examples — this is the model-facing contract
   the agent reads each turn), `imagine_move.py` (one error-string
   that documents the call format), and `experiments/chess/CLAUDE.md`
   if it carries examples. The chess harness code (`agent_player.py`)
   does **not** change: it reads `args.get("filename")` from the
   tool-call dict and reads the committed move from
   `result.stdout` JSON, never from the `args` string itself.

### Out of scope

- **vLLM `guided_json` constrained decoding.** Still deferred per
  [[2026-05-27]]. Revisit only if empty-args loops persist after
  this change lands. The pydantic-ai schema layer enforces the
  parameter shape; `guided_json` would enforce the JSON envelope.
  We are tightening from the inside out.
- **The native-skill scripts themselves.** Their argument parsing
  is left as-is. `web-search`'s positional-argv pattern and
  `learner`'s JSON-in-argv pattern both work transparently under
  the new contract.
- **The post-draw batch advancement bug.** Separate issue,
  separate fix, separate commit.

## Consequences

### Positive

- **Eliminates the 20–26% tool-call failure rate on `make_move.py`
  and `imagine_move.py`** — at least the 116-of-118 `make_move`
  failures and the 337 empty-args `imagine_move` calls; the
  remaining few are likely something else.
- **Removes a class of latent shell-injection-like failures** that
  any future skill author would have hit eventually. The current
  `shlex.split` + `ValueError` fallback is a footgun for any tool
  that takes free-text arguments.
- **Schema layer becomes the contract** — pydantic-ai rejects a
  call with `args: "..."` (string) when the schema says `list[str]`,
  before the call reaches our code. This is the right place for
  the contract to live.

### Negative

- **Existing SKILL.md examples across both repos must be updated**
  in lockstep with the SDK change, because the SKILL.md text *is*
  the contract the model reads each turn. A SDK upgrade without a
  SKILL.md update would silently break running games.
- **The user's existing skill libraries (outside this thesis) would
  need their SKILL.md examples updated** the next time they pull
  this SDK. The change is breaking by design.

### Verification

1. Tests pass in both repos.
2. A single experimental game completes cleanly, `*_agent.json`
   shows `args: [...]` lists instead of strings, zero
   "Missing --uci" errors when reasoning text contains apostrophes,
   zero same-turn `imagine_move` loops with empty args.
3. Over a small batch (3–5 games): the script-call failure rates
   drop from 20–26% to near-zero.

## References

- [[2026-05-27-batch-analysis]] — the trace findings supporting
  this decision (counts, mechanism, smoking-gun reproduction with
  `shlex.split` on a `Black's` apostrophe).
- [[mirko2026gemma]] — independent grey-lit confirmation of the
  contract-tightening pattern for Gemma 4 + Ollama.
- [[mayo2026gemma4tools]] — from-scratch Gemma 4 tool-calling loop
  with explicit retry hints; same shape of contract.
- [[2026-05-26-stabilization]] — same root cause in a different
  layer (vLLM 400 BadRequest on malformed tool-call JSON).
- [[tools-component]] §"Constrained decoding as a contract-
  tightening mechanism" — concept-level framing.
