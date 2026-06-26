---
description: Enter the write stance — turn a settled finding into report or manuscript prose via the sci-write-v2 pipeline.
argument-hint: <what to write, e.g. "the R08 report" or "tighten the intro">
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Skill
---

Enter the **write** stance. Load the `stances` skill, follow `.claude/skills/stances/modes/write.md`,
and load the `sci-write-v2` skill as the engine, on: $ARGUMENTS

- Follow the gated-loop spine: build the claim-lattice + skeleton, gate the whole package as one (F16,
  via `AskUserQuestion`) *before* any prose, then draft, audit ×N, and revise to convergence.
- Draft from evidence with `\evd`/`\gap`; run `scripts/run_checks.py` after each stage write; the
  `stop_sw_converge` Stop-hook holds the turn until every reader is `ready_to_ship`.
- Reports are verdict-first with a plain-language lead. Never invent a number; a missing one is a `\gap`;
  a defect the prose can't fix routes upstream via the cross-stance handoff (D050), never papered over.
