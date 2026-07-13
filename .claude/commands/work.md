---
description: Enter the work stance — produce evidence (lock design, run, judge, record) at high autonomy. Explicit-only; never auto-fires.
argument-hint: <experiment or goal, e.g. E023 or "run the LUPI pilot">
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, Skill
---

Enter the **work** stance. Load the `stances` skill and follow `.claude/skills/stances/modes/work.md`
on: $ARGUMENTS

- Gate first with `/precheck` to `READY-TO-RUN`; then run the clearly stated completion condition. No compute before PASS.
- Kill criteria predeclared, design locked, contiguous splits, the anti-confound battery, ≥3 seeds,
  every number with its uncertainty and named test.
- Keep raw evidence in `experiments/` separate from interpretation; record the *why* of each non-obvious
  design choice at choice-time.
- Hand the result to `/interpret` for adjudication; do not declare the verdict here.
