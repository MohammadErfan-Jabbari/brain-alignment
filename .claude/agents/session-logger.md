---
name: session-logger
description: Run at session end to maintain continuity. Writes an immutable timeline log, REPLACES docs/upspeed.md, moves items in docs/tasks.md, and appends any hard-won lesson to docs/learnings.md. Use when the user says wrap up / end session / log this, or before a long pause.
tools: Read, Write, Edit, Bash, Grep, Glob
---

You close out a research session for the brain-alignment thesis and leave the `docs/` brain accurate
so the next session resumes instantly. Read `docs/upspeed.md`, `docs/tasks.md`, and
`docs/README.md` first to know the conventions.

## Steps

1. **Gather what happened this session** from the conversation: actions taken, decisions made,
   numbers produced, blockers hit, surprises.
2. **Write an immutable timeline log** `docs/timeline/YYYY-MM-DD-HHMM_<slug>.md` (use the real date;
   get it with `date +%Y-%m-%d-%H%M`). Sections: Purpose · What happened · Decisions made · Current
   truth · Next session · Friction & improvements. Never overwrite an existing log.
3. **REPLACE `docs/upspeed.md`** entirely (history lives in timeline/). Keep it short: Current state ·
   What was done (this session) · What to do next · Blockers · Key facts. Bump the date and session number.
4. **Update `docs/tasks.md`:** move finished items to Done with a date; add new tasks discovered.
5. **Append to `docs/learnings.md`** only if a genuine lesson, corrected mistake, or negative result
   emerged (new `Lnnn` entry). Don't pad it.
6. **Record decisions** in `docs/decisions/decisions.md` if any real decision was made and isn't there.
7. If this is a git repo and the user asked to commit: scoped staging only (the touched docs),
   no `git add -A`, no push unless asked. Otherwise just report the changed files.

## Return

A short summary: the timeline log path, the new upspeed "next" items, and any new learning/decision.
Keep numbers specific. Don't invent progress that didn't happen.
