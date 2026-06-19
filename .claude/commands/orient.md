---
description: Session-start orientation — read the docs, report where we are and the single next step plus the stance it calls for, then wait for go-ahead.
allowed-tools: Read, Bash(git log:*), Bash(git status:*), Glob, mcp__gbrain__query
---

You are starting a session in the `brain-alignment` thesis repo with **no specific task given**. Your job is to orient from the docs (the source of truth) and tell Erfan exactly where we are and what to do next. **Do not start any experiment, write any code, or edit any file in this command** — orientation only, then stop for his go-ahead.

Do this:

1. **Read, in order:** `docs/ladder.md` (the canonical status board — current position, rung table, "Next session" block), then `docs/upspeed.md` (last-session prose), then the most recent file in `docs/timeline/` (what literally just happened). Skim `docs/tasks.md` for the backlog. If anything in ladder.md is ambiguous, the rung's linked experiment doc in `docs/experiments/` is the tiebreaker.
2. **Optionally** `mcp__gbrain__query` the brain for `brain-alignment` latest, only if the docs look stale or contradictory.
3. **Determine and report**, in a short briefing (no preamble):
   - **Where we are:** the last rung climbed and its verdict (one line), and the current position from ladder.md.
   - **The next step:** the single recommended next action from ladder.md's "Next session" block, and the **stance** it calls for (`/work`, `/interpret`, `/teach`, …), and why.
   - **Any blockers or dependencies** (e.g. "E004 depends on building `$\mathcal{L}_{\text{brain}}$` first").
   - **One alternative**, if the docs support a reasonable different next step, so Erfan can choose.
   - **Working-tree + wrap check:** run `git status --porcelain` — flag any uncommitted tracked work or work-like untracked file before starting; and if `git log` shows commits dated after the latest `docs/timeline/` entry, warn that the previous session may not have `/wrap`ped (S16/S17 each cost a reconciliation session).
4. **Confirm the stance with Erfan and wait.** End by asking him to confirm the recommended step/stance or redirect. Only after he responds do you begin work (and at that point, enter the stance per the `stances` skill, `CLAUDE.md`).

Keep it tight: a few lines, decision-useful, no restating the whole ladder. If the docs are internally inconsistent or out of date, say so plainly and propose the fix before anything else — a stale source of truth is the one thing that breaks this whole process.
