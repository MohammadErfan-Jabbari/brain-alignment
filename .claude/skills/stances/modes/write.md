# Write mode

Turn settled findings into report or manuscript prose. The engine is the `scientific-writing` skill;
this stance loads it and works inside it.

Load `scientific-writing` and follow it: pick the path (fast edit vs full loop) *with* the user, draft
from evidence with `\evd`/`\gap` tags, sweep the style, run
`scripts/run_checks.py --layer <report|extended|public>`, and for anything supervisor-facing run the
non-skippable Devil's-Advocate review pass. Reports are stored verdict-first with a plain-language lead;
the simple-first walk is `/teach`'s job, not a second shape of the file. Knowledge flows down only:
evidence into a report, report into the extended manuscript, extended into a public cut, and the
manuscripts are rebuilt only at a checkpoint Erfan calls.

## The ship gate (D046)

A manuscript build or revision is its own logged `/write` session, never an add-on at the tail of a
`/meta` or analysis session — that bypass is exactly how v0.1 storytelling prose reached a supervisor
un-reviewed (L054). No prose in `docs/manuscript/` reaches a human until the full loop has run on it, the
non-skippable review pass (which spawns `prose-register-auditor`) included. The `prose_writecheck.py` hook
is the always-on per-edit tripwire; a clean deterministic run is not a clearance, because the linter cannot
catch the register class.

**Convergence is enforced (D047).** A `Stop` hook will not let you end the turn while an edited
`docs/manuscript/` or `docs/reports/` deliverable lacks a clean register verdict keyed to its current
bytes. "Done" = a fresh quorum (≥2 new `prose-register-auditor` spawns, no writing context) returns **zero**
findings on the final draft, recorded via `scripts/record_register_verdict.py`. Stopping at
`REGISTER-CLEAN: NO`, or self-reviewing your own edits, is the v0.2 failure (L055) — the gate now refuses it.
This lives in the write pipeline, not `/wrap`.

## Boundary

Writes, checks, and routes prose that already traces to recorded evidence. It never invents a result,
adjudicates a hypothesis, or flips a rung. A needed-but-missing number is a `\gap`, never a guess.
