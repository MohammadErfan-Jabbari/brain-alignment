---
description: Enter the teach stance — a guided-learning walkthrough of a finding-report (or concept), anchored to recorded numbers, that transfers understanding into your head.
argument-hint: <report or topic, e.g. R07 or "knowledge distillation"> [guided|walkthrough|feynman|drill]
allowed-tools: Read, Write, Edit, Glob, Grep, Skill
---

Enter the **teach** stance. Load the `stances` skill and follow `.claude/skills/stances/modes/teach.md`
as your operating instructions for this session, on: $ARGUMENTS

- Default sub-mode is **guided** unless the user named one (walkthrough / feynman / drill).
- First, read the learning ledger (`docs/learning/`) for the report in play: skip mastered findings,
  start at the first finding with no passing record, or where the user asks.
- Teach only numbers the report records. If a lesson needs a number the report does not carry, say so
  and call it a `\gap`; never invent one.
- One concept, one question, then stop and wait. Hints, not answers.
- Write a learning record only on demonstrated mastery (the per-mode bar), never on coverage.
