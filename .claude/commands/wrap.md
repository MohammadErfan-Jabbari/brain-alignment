---
description: Session close — run the session-logger ritual, update the ladder (with Erfan's confirmation), then a continuity audit (friction, broken tooling, doc consistency, new-artifact check). The mirror of /orient.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, mcp__gbrain__query, mcp__gbrain__get_page, mcp__gbrain__put_page
---

Close out this `brain-alignment` session so the next one resumes instantly from the docs alone. This is the canonical close; it runs the `session-logger` ritual **plus** a continuity audit, and it **scales to the session**: a trivial session is closed inline (you have the full context), a heavy one fans out an independent audit swarm over the exact changeset before you write. Two hard rules throughout: **never invent progress that didn't happen**, and **confirm every verdict / ladder flip with Erfan before it lands** — the ladder is the source of truth and must stay honest.

## Part 0 — Session changeset & tier (do this first)

1. **Get the changeset.** Read `.claude/state/wrap/start.json` (written by the SessionStart hook): it holds `start_sha` and the authoritative `transcript_path`. Compute what this session changed: `git diff --stat <start_sha>..HEAD` plus `git status --short` (committed + uncommitted). If `start.json` is missing (a session that predates the hook, or the hook didn't fire), fall back to identifying the session's first commit from `git log` and diffing from its parent — and say in the close summary that you used the fallback.
2. **Pick the tier and state it in one line:**
   - **Trivial** (a couple of files, no science/manuscript/skill doc touched): close **inline** — Part A then Part B yourself. Skip the swarm.
   - **Heavy** (multiple docs changed, or any of `ladder.md`, `docs/experiments/`, `docs/reports/`, `docs/manuscript/`, `.claude/skills/`, `decisions/`, `learnings.md` touched): run the **audit swarm** (Part C) in place of doing Part B alone.

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

## Part C — the audit swarm (heavy sessions only)

An independent parallel audit of the changeset that **replaces doing Part B alone**. The pattern is **fan out read, then single-write** — auditors are read-only and the orchestrator (you) is the only writer.

1. **Extract a transcript slice** (the intent a git diff does not carry). From the `transcript_path` in `start.json`, `jq` out this session's user messages and your stated decisions — distill it, never load the raw multi-MB `.jsonl` into an agent. Roughly: `jq -r 'select(.type=="user") | .message.content | if type=="string" then . else (.[]?|select(.type=="text").text) end' <transcript_path>` then drop tool-result/command-wrapper lines and cap the length.
2. **Spawn the auditors in parallel** — one `wrap-auditor` per scope, in a single message so they run concurrently. Each gets its `SCOPE`, the `git diff <start_sha>..HEAD` + `git status`, and (for `records-completeness` and the friction note) the transcript slice. Model routing: **`ladder-integrity` on opus**, the other four on sonnet. The five scopes (`ladder-integrity`, `number-provenance`, `continuity-docs`, `records-completeness`, `git-and-artifacts`) together cover Part B's checks.
3. **Reconcile — verify before you trust.** Collect the findings. Confirm each against the evidence yourself; an auditor can be wrong, so never apply a fix you cannot see in the diff or the doc. Drop the unfounded ones and say so.
4. **Apply as the single writer.** Do Part A (the ritual writes) and apply the confirmed fixes. **Never parallel-write shared docs.** Commit **atomically per scope/concern** with conventional messages (D007), scoped staging only — not one mega-commit.
5. **Flips and the brain mirror stay with you.** Any `REQUIRES-ERFAN` proposal is surfaced to Erfan and lands only on his confirmation (D015). The gbrain mirror (Part B.6) is yours — it is a write and needs MCP, not an auditor's job.

The swarm finds and proposes; you confirm, write, and commit. The invariants are unchanged: never invent progress, never flip a rung without Erfan, never `git add -A`.

## Return

A short close summary: the **session mode**; the **tier** chosen (and the fallback note if `start.json` was missing); on a heavy session, the **swarm findings** (applied vs dropped-as-unfounded); the timeline log path; the **proposed ladder change** (and confirm it with Erfan if a rung flips); the new `upspeed.md` "next" step; any new learning/decision; and the **continuity-audit findings** — friction + proposed fixes, tooling issues, doc inconsistencies fixed/flagged, any new-artifact proposal, and git status. Keep numbers specific. End by stating clearly what (if anything) needs Erfan's confirmation before it's final.
