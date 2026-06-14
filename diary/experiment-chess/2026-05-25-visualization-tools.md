---
type: diary
touched_work: [experiment-chess]
touched_concepts: [skills-component, tools-component, deterministic-tools-hypothesis, learning-as-temporal-dimension]
status: open
---

# 2026-05-25 — Perception tools and skill rewrite (visualization-and-context-management branch)

Started the first post-baseline improvement on a new branch,
`visualization-and-context-management`. The branch will land two
related changes: this one (perception tools) and a context-management
change to follow. ADR for the first change:
[[2026-05-25-perception-tools-and-skill-rewrite]].

## What we built

Three new scripts in `backend/skills/chess-player/scripts/`:

- **`show_position.py`** — labelled ASCII board + FEN + phase
  annotation + attack/defense map with x-ray batteries and `(pinned)`
  annotations. Effectively a "look at the position properly" tool.
- **`imagine_move.py --uci <move>`** — one-ply look-ahead. Shows the
  resulting board, what the move captures, whether it gives check or
  mate, what the moved piece now attacks and defends, what it stopped
  attacking and defending, any pieces of ours that became newly
  hanging as a side-effect, any discovered attacks our other pieces
  gain, en-passant offered to the opponent, and the opponent's legal
  replies. Designed to be called on candidate moves before commit.
- **`evaluate_position.py [--moves uci1,uci2,...]`** — static eval:
  material plus Michniewski's Simplified Evaluation Function PSTs,
  with per-side king-table selection. Verdict bands (`equal`,
  `slightly better`, `clearly better`, `winning`). With `--moves`,
  plays a candidate line and evaluates the endpoint, prepending the
  SAN line for legibility.

All three are env-var driven (no FEN argument needed) and run on a
copy of the live board — only `make_move.py` commits to the real
game. Comprehensive tests: 95 total across the three scripts (27
show_position, 44 evaluate_position, 24 imagine_move), all passing.

Frontend updated so each script's output renders cleanly in the agent
feed — multi-line text in a scrollable `<pre>` block rather than the
old 80-char-truncated single-line summary. Stderr is surfaced when a
script exits nonzero.

## Why we built it

Baseline calibration ([[2026-05-25-baseline-calibration-complete]])
established that the bare-model Gemma 4 31B-it agent plays at or
below ELO 700. Watching the games, almost all the losses were
*perceptual*, not strategic: misread attackers, missed pins, hung
pieces from moving defenders away, captures that lost material to a
recapture the agent failed to count. The agent often reasoned
correctly in text and then played a different (wrong) move — see
the toolcall investigation in this folder's other 2026-05-25 entry.

These are precisely the failures that cheap deterministic tools
fix. The tool-fairness rulebook in [[experiment-chess]] already
permits "mechanics tools" of exactly this shape: `legal_moves()`,
`what_if(move) -> board_after`, `is_attacked(square)`,
`list_pieces_attacking(square)`. The bare-model baseline ran
without them deliberately so we had a clean reading on raw model
competence. With the baseline locked in, this configuration adds
the tools the rulebook already allows.

The hypothesis we're testing with this batch — informally, before
the real measurement runs — is that *most of the baseline loss was
perception, not chess knowledge*. If that's right, the perception
tools alone should close a meaningful share of the gap to the
chess.com pool's middle (the pool runs 700 → 3200 in 25 discrete
steps, so the bare model is at the floor; "middle" here means the
agent starts winning enough games to drift upward off the floor).

If the tools *don't* help much, we learn something more interesting:
the model's chess weakness is in the next layer up — pattern
recognition, planning, evaluation — and perception was not the
binding constraint. That's a useful negative result for the thesis's
broader claim that procedural-knowledge scaffolding can recover
substantial capability around a fixed model.

## What we hope to achieve

Three nested goals:

1. **Concrete:** A measurable upward delta in agent ELO vs the
   684.2 baseline ceiling, on a ranked batch under the new
   configuration. The number we'd take as "meaningful" hasn't been
   set yet — see the deferred success criterion in the baseline ADR.
2. **Thesis-level:** Evidence for or against the
   [[deterministic-tools-hypothesis]] within Phase 1, before the
   full skill-library work begins. The hypothesis says that
   deterministic tools meaningfully outperform raw inference and
   meaningfully underperform a chess-engine-as-tool. This batch
   gives us the lower bound (raw inference) vs (raw inference +
   perception tools) gap, which is the first data point on that
   curve.
3. **Methodological:** Validate that the new system-prompt/SKILL.md
   structure works — system prompt limited to context and rules,
   SKILL.md owning strategy. If the model successfully uses the
   tools without the system prompt prescribing a tool sequence,
   that pattern generalises to the full skill-library work in
   Phase 1 (many skills, no system prompt that knows about any of
   them).

## Skill and system-prompt rewrite

This came up partway through the tool work, separate from the
scripts themselves: the previous system prompt embedded a hardcoded
four-step turn sequence (`use_skill` → `list_legal_moves` →
"write 2–4 sentences" → `make_move`) and a length cap on reasoning.
That worked when there were two scripts. With five, the prompt
either bloats with new prescribed steps or stops describing the
actual workflow.

The rewrite splits responsibility:

- **System prompt** carries context (role: white in a live game),
  rules (`make_move` commits immediately; if illegal, retry; if
  none, that's resignation), an anti-loop nudge ("avoid loops; if
  oscillating between candidates, commit the one you currently
  believe is best"), and a pointer to `use_skill('chess-player')`
  at the start of each turn.
- **SKILL.md** carries the turn workflow (see → candidates →
  imagine → optional eval → commit), per-script contracts, and a
  new "Trust your tools over your intuition" framing at the top.

The "trust your tools" framing is the bit that surprised me how
important it felt to write explicitly. LLMs are trained to be
confident; with weak procedural chess knowledge, that confidence
will sometimes flat-out override correct tool output ("the script
says my bishop is attacked twice but I only see one"). The
paragraph names the failure mode and prescribes the resolution:
intuition proposes, tools verify, tool wins on factual
disagreement. We'll see in the experimental games whether the
model actually internalises this when its intuition is strong.

Per-turn caps: `max_tokens` kept at 1024 (still bounds any single
response), `max_turns` raised 10 → 16 to accommodate the longer
tool flow.

## On fairness

The tool-fairness audit is in the ADR; the short version is that
`show_position` and `imagine_move` are uncontroversial — they're
exactly the "mechanics tools" the rulebook calls out by example.
`evaluate_position` is the one worth a paragraph here because it
sits closer to the line.

The eval encodes *some* chess knowledge: material values (P=100,
N=320, ...) and piece-square tables (knights belong in the centre,
kings belong on the back rank in middlegame and centralised in
endgame). Those are positional heuristics, not pure board geometry.
A purist could argue they shouldn't ship in a "baseline + perception
tools" configuration.

Two reasons I went ahead anyway:

1. Michniewski's PSTs and the standard material values are
   common-knowledge beginner-primer material. They're the kind of
   thing a chess teacher tells a student in the first week. The
   rulebook explicitly permits `piece_values` as a fair mechanics
   tool; PSTs sit on the same footing — a published, well-known
   tabulation rather than synthesised insight.
2. The eval is intentionally weak. No mobility, no pawn structure,
   no king safety beyond the PST's coarse "king belongs here"
   shape, no tactics. It's not strong-play knowledge; it's a
   sanity check on "did this line land me up or down on material
   and rough activity." The README/SKILL.md is explicit that the
   eval is tactically blind and the agent shouldn't trust a small
   positive score after an unverified sequence.

The honest framing for the writeup is: **these tools fix perceptual
failure, not evaluative failure. The agent still has to decide
which moves to consider, what they mean strategically, when to
attack and when to defend.** That division is consistent with what
the thesis already says about mechanics tools.

There's also a deeper point about what "fair" even means in this
experiment. The thesis claim isn't that the agent must operate
without any tools — it's that the *learning loop* produces the
agent-curated corpus and the agent-written skills, which then
outperform raw inference. Tools bundled from day zero (the
perception scripts) are part of the experimental scaffold, not the
learned artefact. The Phase 2 tournament's Config 2 (the frozen
skill library) is what tests the agent-curated claim. Config 1
(inference alone) is the bare-model baseline. The configuration
this batch tests is *between* those — bare model + scaffold tools
— which is a useful intermediate data point but isn't either of
the canonical Phase 2 configurations. That's worth noting in the
thesis chapter; the reader should understand the comparison being
drawn.

## Reflection on what's still missing

The agent now has tools to *see* the board correctly. It doesn't
yet have tools to *remember* what it saw. Every turn currently
starts with a fresh context per
[[2026-05-24-per-turn-fresh-context]], which means the agent
re-derives the position from FEN every turn, with no memory of
previous turns' calculations, no plan, no record of the opponent's
patterns within the game.

That's deliberate for the baseline — the FEN encodes complete game
state, and adding memory was kept as a separate experimental axis
to measure cleanly. Context management is the next change on this
branch and will get its own ADR. The short version of what we'll
probably do: sliding-window memory across turns, or auto-compaction
when context fills, with the same kind of careful pre/post
measurement as this change.

## Context management — to be written after testing

The user will run some experimental games on the new perception-tool
configuration first. Once we have a feel for how the model uses the
new tools and where it still struggles, we'll decide what shape the
context-management change should take. Concrete options on the
table:

- **Sliding-window memory** across turns: keep the last N turns of
  the agent's reasoning and tool outputs in context, drop older.
- **Auto-compaction** when context approaches limit: summarise the
  game so far into a short "current plan + position notes" block,
  carry that forward.
- **Per-game running notes file** that the agent writes to and reads
  from across turns — closer to the eventual Phase 1 skill-library
  pattern, but applied to a single game's state rather than to
  permanent skills.

Decision to be made after seeing the perception-tools batch run.
This section will be filled in then.

## Diary notes for follow-up

- Run a small experimental batch (3–5 games) on the
  `visualization-and-context-management` branch to verify the model
  uses the new tools and doesn't loop. Lands in `experimental.csv`,
  no ELO update.
- Watch the agent traces specifically for: does it call
  `show_position` and `imagine_move` voluntarily, or does it default
  to the old `list_legal_moves` → guess flow? If the latter, the
  SKILL.md workflow framing needs to be more directive.
- Note whether the "trust your tools" paragraph appears to land —
  i.e. whether the model defers to tool output when its reasoning
  disagrees. This may be hard to see from outputs alone; the trace
  has to show the disagreement happening.
- Confirm `max_turns=16` is enough headroom; if many turns hit the
  cap, raise further.

After the experimental batch, decide whether to merge to main and
run the ranked calibration, or iterate on the SKILL.md further first.
