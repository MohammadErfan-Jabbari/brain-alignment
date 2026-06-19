---
description: Enter the interpret stance — turn a recorded result into a panel-survived, manifest-scored verdict (proposes a verdict; never flips a rung).
argument-hint: <result or question, e.g. E021 or "is the lever real">
allowed-tools: Read, Glob, Grep, Bash, Task, Skill
---

Enter the **interpret** stance. Load the `stances` skill and follow
`.claude/skills/stances/modes/interpret.md` as your operating instructions for this session, on:
$ARGUMENTS

- Write the Claim-Intent-Manifest first (claim · evidence pointer · what-would-overturn-it), before
  adjudicating.
- If the verdict rests on an aggregated statistic, run `stat-aggregation-auditor` to re-compute it.
- Run the thinking panel + `oracle-reviewer` (RESULT mode); reconcile every `PANEL-VERDICT` to
  `PANEL-CLEAN:YES` before the verdict lands.
- State only numbers a working session recorded; a missing number is a `\gap`, never invented.
- Propose the verdict; a rung flips only on the user's confirmation. Hand the clean finding to `/write`.
