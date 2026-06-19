---
description: Enter the review stance — stress-test a result, claim, or design with the thinking panel + Codex on demand.
argument-hint: <the target, e.g. "the Q2 verdict" or "this analysis script">
allowed-tools: Read, Glob, Grep, Bash, Task, Skill
---

Enter the **review** stance. Load the `stances` skill and follow `.claude/skills/stances/modes/review.md`
on: $ARGUMENTS

- Spawn the panel (`counter-argument`, `socratic-thinker`, `premortem-analyst`,
  `first-principles-grounder`) + `oracle-reviewer`; add the Codex code-critic when a script is in question.
- Reconcile every `PANEL-VERDICT` to `PANEL-CLEAN:YES`. Review produces no number and flips no rung.
