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
| `records/` | Curated mastery ledger. Each file is one durable mastery event, written only on demonstrated mastery or a corrected misconception. Currently empty, so `/teach` resumes from `lessons/` until the first record lands. |

## Rules

- Do not create a `README.md` here. Folder guidance belongs in `AGENTS.md`.
- Lessons are raw process and must not leak into reports as evidence.
- Records are the single source of resume truth for `/teach`.
- Supersede records when needed; do not delete them.
- Render lesson Markdown to HTML for math/diagrams with:

```bash
uv run .claude/skills/teach/scripts/render_lesson.py <file>
```

- Lesson format: `.claude/skills/teach/formats/lesson-format.md`.
- Learning-record format and write gate: `.claude/skills/teach/formats/learning-record.md`.

## Related

- `../status.md`
