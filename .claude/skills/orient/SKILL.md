---
name: orient
description: >-
  Orient at session start from docs/status.md, Git, and only the evidence or manuscript links
  needed for the first listed next action. Returns a compact briefing and starts no work.
tools: Read, Bash, Glob
---

Read `docs/status.md`, then run `git status --short`. Follow only the E-record or canonical-rewrite-manuscript links needed to understand the first listed next action.

Return a compact briefing:

- manuscript state and whether `manuscript-sync-pending` is set;
- current active work and blockers;
- the first recommended action and its stance;
- dirty-worktree or unpushed-commit warning, if any;
- a warning if any folder `CLAUDE.md` no longer resolves to its sibling `AGENTS.md`, since a broken link silently drops that folder's contract.

Do not reconstruct state from timelines or historical documents. Do not edit or start work inside `/orient`; wait for Erfan’s direction.
