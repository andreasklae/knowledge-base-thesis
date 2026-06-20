# wtharvey.com — mate-in-N puzzle collections (from real games)

**Source:** https://wtharvey.com/ — a long-running free collection of
checkmate puzzles drawn from real games, grouped by mate length and motif.
Each puzzle is given as a **FEN plus the full solution move sequence**, which
is exactly what the chess experiment's puzzle harness needs (a verified
starting position and a known forced line — we replay the line in
python-chess to confirm it, rather than trusting a solver).

## Useful index pages

- Mate in 2 (White or Black to move): `https://wtharvey.com/m8n2.txt`
- Mate in 3: `https://wtharvey.com/m8n3.txt`
- Mate in 4: `https://wtharvey.com/m8n4.txt`
- Back-rank mates (Lichess-rated): `https://wtharvey.com/brm.html`
- Format: each line is `FEN | 1. Move reply 2. Move reply ... #`

## Why this matters (tool-fairness + methodology)

These are **sourced** puzzles, not invented by us — the user asked
specifically to avoid hand-made mate positions and use real puzzle FENs.
They are White-to-move forced mates, so the agent's success is a genuine
test of finding the mate, not of the opponent blundering (we also run them
against the strongest Maia-1900 to remove that confound).

## Verified puzzles wired into the experiment (scripts/run_puzzles.py)

All replayed and confirmed forced mate in python-chess on 2026-06-16:

- `brm-d-file` — `4kb1r/p2n1ppp/4q3/4p1B1/4P3/1Q6/PPP2PPP/2KR4 w k - 1 0`
  → 1.Qb8+ Nxb8 2.Rd8# (deflect the knight, mate on the open d-file).
- `brm-e-file` — `r1b2k1r/ppp1bppp/8/1B1Q4/5q2/2P5/PPP2PPP/R3R1K1 w - - 1 0`
  → 1.Qd8+ Bxd8 2.Re8# (deflect the bishop, mate on the open e-file).
- `brm-rxf8` — `5rk1/1p1q2bp/p2pN1p1/2pP2Bn/2P3P1/1P6/P4QKP/5R2 w - - 1 0`
  → 1.Qxf8+ Bxf8 2.Rxf8# (remove the back-rank defender, rook mates).

The longer Lichess back-rank deflection #JxR8M (mate in 3) is also wired in
as `backrank-deflection`.
