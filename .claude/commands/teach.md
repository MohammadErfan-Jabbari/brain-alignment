---
description: Enter the teach stance — a guided walkthrough of a concept, file, experiment, manuscript claim, paper, or question grounded in the source.
argument-hint: <subject — e.g. E008, "knowledge distillation", a file path, a paper, or a question> [guided|walkthrough|feynman|drill]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill
---

Enter the **teach** stance. Load the `stances` skill and follow `.claude/skills/stances/modes/teach.md`
as your operating instructions for this session, on: $ARGUMENTS

- Teach **anything**: a concept, a manuscript claim, a code file, an experiment (and why it is designed that
  way), a paper or a topic in it, a course-materials concept, or a free-form question. Ground in the
  source for that subject (the table in `teach.md`) and cite it; never teach from parametric memory.
- Default sub-mode is **guided** unless the user named one (walkthrough / feynman / drill).
- Produce a **lesson** at `docs/learning/lessons/YYYY-MM-DD-<subject>.md` (the rendered whiteboard;
  `formats/lesson-format.md`). Render it with `render_lesson.py` to view math/diagrams in a browser.
  Update it at round boundaries, never mid-question.
- First read the **records** (`docs/learning/records/`) for the subject: skip mastered pieces, start at
  the first un-mastered one, or where the user asks. Records — not lessons — are the resume source of truth.
- Numbers are cited to their source by code and never invented; a missing one is a `\gap`.
- One concept, one question, then stop and wait. Hints, not answers.
- Write a learning **record** only on demonstrated mastery (the per-mode bar), never on coverage.
