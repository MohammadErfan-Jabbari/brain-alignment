---
title: "Learning Agent Guidance"
tags: [learning, reference]
aliases: [learning-agents]
---

# Learning Agent Guidance

This directory is the memory and working surface of the `/teach` stance. Keep raw teaching process separate from curated mastery.

## Layout

| Path | Use |
|---|---|
| `lessons/` | Rendered teaching artifacts, one Markdown file per teaching session. These are the whiteboard: explanation, math, diagrams, questions, and mistakes. |
| `records/` | Curated mastery ledger. Each file is one durable mastery event, written only on demonstrated mastery or a corrected misconception. |

## Rules

- Do not create a `README.md` here. Folder guidance belongs in `AGENTS.md`.
- Lessons are raw process and must not leak into reports as evidence.
- Records are the resume authority for `/teach` once any exist. The ledger is still empty while `lessons/` keeps growing, so resume reads `lessons/` today; the moment the first record lands it takes precedence. Do not treat the empty ledger as evidence that nothing was learned, and do not read the gap between the two directories as a backlog to fill: a record is written only on demonstrated mastery, so most lessons correctly never produce one.
- Supersede records when needed; do not delete them.
- Render lesson Markdown to HTML for math/diagrams with:

```bash
uv run .claude/skills/teach/scripts/render_lesson.py <file>
```

- Lesson format: `.claude/skills/teach/formats/lesson-format.md`.
- Learning-record format and write gate: `.claude/skills/teach/formats/learning-record.md`.

## Related

- [Teach skill](../../.claude/skills/teach/SKILL.md)
- [Operational status](../status.md)
