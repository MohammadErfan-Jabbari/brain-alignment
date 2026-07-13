---
description: Enter the write stance and draft settled evidence directly into the extended manuscript.
argument-hint: <claim or manuscript section>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, Skill
---

Enter `/write` on: $ARGUMENTS

1. Read the owning E records and current manuscript section.
2. State the intended claim, scope, caveats, and evidence before editing.
3. Draft directly into `docs/manuscript/extended/`; do not create an intermediate report or lattice.
4. Preserve `\evd{Ennn}` provenance and `numbers.tex`; use `\gap{...}` for genuinely missing evidence.
5. Run `uv run python .claude/scripts/manuscript_check.py docs/manuscript/extended`.
6. Run one fresh independent prose and scientific-scope review, revise, and obtain Erfan’s approval for load-bearing framing.

If prose reveals a scientific contradiction, stop the prose correction, set `manuscript-sync-pending`, and route the issue to `/interpret`.
