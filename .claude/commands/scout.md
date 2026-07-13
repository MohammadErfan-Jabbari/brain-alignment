---
description: Enter the scout stance — bring external papers and datasets into the brain (the Map phase of the pipeline).
argument-hint: <topic or dataset, e.g. "privileged-information distillation" or "ZuCo">
allowed-tools: Read, Write, Glob, Grep, Bash, Task, WebSearch, WebFetch, Skill
---

Enter the **scout** stance. Load the `stances` skill and follow `.claude/skills/stances/modes/scout.md`
on: $ARGUMENTS

- Papers: `lit-scout` → `paper-digest`; the `firecrawl-research-index` skill is
  the second retrieval lane.
- Data: `dataset-scout` → `dataset-verifier`.
- A paper's claim is not our number: cite it, flag a `\gap`, never vibe-cite or fill from memory.
