---
description: Session close — run the session-logger ritual, update the ladder (with Erfan's confirmation), then a continuity audit (friction, broken tooling, doc consistency, new-artifact check). The mirror of /orient.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, mcp__gbrain__query, mcp__gbrain__get_page, mcp__gbrain__put_page
---

Close out this `brain-alignment` session so the next one resumes instantly from the docs alone. You have the full session context, so do this inline (don't spawn a fresh agent that would have to reconstruct what happened). This is the canonical close; it runs the `session-logger` ritual **plus** a continuity audit. Two hard rules throughout: **never invent progress that didn't happen**, and **confirm every verdict / ladder flip with Erfan before it lands** — the ladder is the source of truth and must stay honest.

## Part A — the session-logger ritual (the mechanical record)

Follow `.claude/agents/session-logger.md` steps 1–8, in order:

1. **Declare the session mode** — working (evidence produced) or analysis (evidence consumed/communicated). State it; it frames everything.
2. **Gather what happened** — actions, decisions, numbers-with-uncertainty, blockers, surprises.
3. **Write the immutable timeline log** `docs/timeline/YYYY-MM-DD-HHMM_<slug>.md` (real date via `date +%Y-%m-%d-%H%M`; never overwrite).
4. **REPLACE `docs/upspeed.md`** — short, framed by mode (working: what ran / next to run; analysis: what's understood / written / figured).
5. **Update `docs/tasks.md`** — move finished to Done with a date; add new tasks.
6. **`docs/ladder.md`** — flip changed rungs, record verdicts (specific numbers + named test; ✅ only on an `experiments/`-recorded result, partials stay 🟡 with the caveat), update supporting tracks, **rewrite the "Next session" block** (mode + the single concrete next step). **Get Erfan's confirmation before flipping any rung.**
7. **Append to `docs/learnings.md`** only if a genuine lesson/corrected mistake/negative result emerged (new `Lnnn`). Don't pad.
8. **Record decisions** in `docs/decisions/decisions.md` if a real decision was made and isn't already there.

## Part B — the continuity audit (the reflection that stops repeat pain)

Run each check. For most, the output is either "nothing" or a concrete fix or a new task — keep it honest and unpadded, the way `learnings.md` is kept.

1. **Friction worth fixing.** What slowed us or went wrong that will happen *again*? For each recurring friction, name the durable fix and where it goes: a `docs/` line, a new/edited agent, a command, a hook, or a `CLAUDE.md` rule. Adaptive semistructure (`03-methodology.md`): a workflow reconstructed twice earns a structure — propose it, and with Erfan's OK do it now or file it in `tasks.md`.
2. **Tooling that misbehaved.** Any tool, script, agent, command, MCP call, or background mechanism that failed or surprised us (e.g. the bare-`nohup` run that died silently). Record the symptom + the workaround in `upspeed.md` Key facts or in `learnings.md`, so the next session doesn't rediscover it.
3. **Doc consistency / source-of-truth audit.** Do `ladder.md`, `upspeed.md`, `tasks.md`, and the relevant report (R03/R04/…) agree? Any number stated in a doc that is *not* backed by an `experiments/` entry (the D011 cite-or-flag rule)? Any claim this session contradicted that is now stale? Fix it, or flag it loudly in the timeline if the fix needs Erfan.
4. **New-artifact check.** Did a need recur enough to warrant a new doc / agent / command / experiment template? Propose it; do **not** create preemptively. Equally, did anything become dead weight worth deleting?
5. **Ladder integrity.** Every rung status matches an `experiments/` record; partials carry their caveat; the "Next session" block is concrete and mode-tagged; kill criteria still predeclared for open rungs. (This is the one file the whole continuity process trusts.)
6. **Brain mirror.** Was any durable decision / finding / idea mirrored to gbrain (per the global brain-first protocol)? If a `put_page` is warranted and not done, do it (provenance `author: agent`; never secrets), or say why it's pure ephemeral plumbing.
7. **Git hygiene.** Is every meaningful step committed atomically with a conventional message (D007), scoped staging only (never `git add -A`/`.`)? Is the working tree clean, with nothing important left uncommitted? Run `git status --short` and report. Push only if Erfan asked.
8. **Open loops.** Any background job still running, half-finished edit, or unverified result? Surface it explicitly in `upspeed.md` Blockers/Next so it isn't silently lost.

## Return

A short close summary: the **session mode**; the timeline log path; the **proposed ladder change** (and confirm it with Erfan if a rung flips); the new `upspeed.md` "next" step; any new learning/decision; and the **continuity-audit findings** — friction + proposed fixes, tooling issues, doc inconsistencies fixed/flagged, any new-artifact proposal, and git status. Keep numbers specific. End by stating clearly what (if anything) needs Erfan's confirmation before it's final.
