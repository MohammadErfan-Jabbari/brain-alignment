---
description: Orient from the single operational status, Git, and only the evidence/manuscript links needed for the first action.
allowed-tools: Read, Bash(git status:*), Bash(git log:*), Glob
---

Read `docs/status.md`, then run `git status --short`. Follow only the E-record or extended-manuscript links needed to understand the first listed next action.

Return a compact briefing:

- manuscript state and whether `manuscript-sync-pending` is set;
- current active work and blockers;
- the first recommended action and its stance;
- dirty-worktree or unpushed-commit warning, if any.

Do not reconstruct state from timelines or historical documents. Do not edit or start work inside `/orient`; wait for Erfan’s direction.
