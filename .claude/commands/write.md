---
description: Enter the write stance — turn a settled finding into report or manuscript prose via the scientific-writing skill.
argument-hint: <what to write, e.g. "the R08 report" or "tighten the intro">
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Skill
---

Enter the **write** stance. Load the `stances` skill, follow `.claude/skills/stances/modes/write.md`,
and load the `scientific-writing` skill as the engine, on: $ARGUMENTS

- Pick the path (fast edit vs full loop) *with* the user; draft from evidence with `\evd`/`\gap`; run
  `run_checks.py`; run the non-skippable review pass for anything supervisor-facing.
- Reports are verdict-first with a plain-language lead. Never invent a number; a missing one is a `\gap`.
