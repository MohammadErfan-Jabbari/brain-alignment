---
title: "The learning workspace"
tags: [learning]
---

# The learning workspace

This directory is the memory and working surface of the `/teach` stance, in two layers:

- **`lessons/`** — the rendered learning artifacts (the "whiteboard"). One markdown file per teaching
  session, `YYYY-MM-DD-<subject>.md`, carrying the explanation, math, diagrams, the questions, and the
  mistakes. This is the raw learning *process*, kept here so it never leaks into a report. Render to HTML
  for math/diagrams with `uv run .claude/skills/stances/scripts/render_lesson.py <file>`. Format and the
  non-canonical banner: `.claude/skills/stances/formats/lesson-format.md`.
- **`records/`** — the curated mastery ledger. Each `NNNN-<slug>.md` is one durable mastery event,
  anchored to the subject and the recorded number/claim it concerns. This is the **single source of
  resume truth**: on resuming, `/teach` re-reads the records to know what is mastered and what to teach
  next. Written only on demonstrated mastery (or a corrected misconception), never on coverage.
  Supersede, never delete. Format and the when-to-write gate:
  `.claude/skills/stances/formats/learning-record.md`.

Raw process (`lessons/`) stays separate from curated mastery (`records/`) — the repo's raw-vs-interpreted
discipline. `thesis-arc-checklist.md` is the prior whole-thesis comprehension tracker, kept for history.
This README is not a record.


## Related
- [`ladder.md`](../ladder.md) — the canonical status board
- [`map.md`](../map.md) — code system (Q/E/A/D/L) & journey map
