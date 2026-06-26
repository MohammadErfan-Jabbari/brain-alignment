---
title: "Upspeed — last-session state (read first)"
tags: [reference]
aliases: [upspeed]
---

# Upspeed — read first, write last

**Last updated:** 2026-06-26 (S43 — **/meta: D048 `/write` cutover EXECUTED; `sci-write-v2` is now the default
`/write` engine.** Took the redesigned pipeline through its final phase: P3-0 a committed 12-scenario dress
rehearsal (opus-audited for fixture fairness), P3-1 the full **94-RUB acceptance suite graded in 7 batches →
PASS, Erfan-signed** (suite `e49865ea3939f212`), P3-2 the cutover (routing repointed, old skill tombstoned,
hook layer cut over). 14 commits. **NO experiment, NO science number, NO rung change — Q0–Q5 stand.** Prior:
S42 — /meta built the G1 RUB-grading harness + cleared the pre-P3 checklist.)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md)** (Q0–Q5 unchanged). The `/write` rebuild (D048)
> is **DONE** — `sci-write-v2` is the default engine; the old `scientific-writing` skill is tombstoned (delete
> on/after 2026-07-03). With no task, run `/orient`.

## What this session did (/meta — execute the P3 cutover)
- **P3-0 dress rehearsal** — 12 scenarios across all 4 grading mechanisms + both anchors, real grader spawns
  with `--raw` provenance. An opus oracle audited fixture fairness → caught 4 unfair fixtures (1 self-graded,
  3 answer-leaking); all rebuilt cue-free and re-run clean. (`state/p3-0/fixtures.md`)
- **P3-1 full suite** — 7 grader batches, each committed; **94/94 RUB PASS + 13 DET green → `score: PASS`**,
  signed by Erfan. Two scenarios Erfan adjudicated (SC-VIO-2511-1 → noflag idiom; SC-EX-2510-4 → flag
  overclaim); SC-ARG-5 rewritten to genuinely test the unmapped-objection path.
- **P3-2 cutover** — routing scientific-writing → sci-write-v2 (live surface, incl. 4 sites a wrap-auditor
  caught); old skill tombstoned (read-only ~1 week); hooks cut over (retired `stop_register_gate`,
  `prose_writecheck` → v2 `ai_tell_lint`); D048 amended COMPLETE.

## What's next (resume here)
- **The `/write` rebuild is closed.** Next `/write` session runs on `sci-write-v2` (gated-loop spine: F16
  AskUserQuestion gate before prose, parallel stage-5 readers, `stop_sw_converge` convergence, D050 handoff).
- **Live science thread (UNCHANGED since S25):** the science lane is where the next real work is —
  **`/work` Q4 sample-efficiency E024** (re-substrate to a higher-N gaze corpus → synthetic-PI MDE positive-
  control → re-gate → build), OR **`/write` R08 (Q2)** as the next finding-report (now on sci-write-v2), OR
  **`/interpret`** the parked E006 voxelwise-CI item. Erfan's call which.
- **Dated chore (on/after 2026-07-03):** delete the tombstoned `scientific-writing/` + dead
  `stop_register_gate.py` + old register-verdict scripts (see `tasks.md`).

## Blockers / open loops
- **50 commits unpushed on main** (push only when asked).
- **Pre-existing D011 gap:** `docs/manuscript/README.md:34` bare `+0.06` (no cite) + em-dashes — predates this
  session; a navigational README, fix on a `/write` touch, not chased here.
- **Two untracked strays** left untouched: `.obsidian/` (editor config) and
  `docs/learning/lessons/2026-06-24-boruta-feature-selector.md` (foreign to repo conventions, per Erfan).

## Key facts for next session
- **`sci-write-v2` is the `/write` engine.** Sanity (one shot): `cd .claude/skills/sci-write-v2/scripts && uv run
  python {run_checks,verdicts,rub_harness}.py --selftest` — all PASS. The acceptance suite: `rub_harness.py score`
  → PASS; `sign-off --status` → SIGNED (suite `e49865ea3939f212`).
- **The suite is the regression guard.** A scenario or judge change re-stales the sign-off (hash-bound); re-sign
  after. Run protocol: `references/rub-harness-protocol.md`.
- **Hook layer now:** Stop = `stop_sw_converge` only (register gate retired); PostToolUse on docs/{reports,
  manuscript} = `honesty_writecheck` (D011) + `prose_writecheck` (→ v2 `ai_tell_lint`). Both fail SOFT.
- **Run code:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache`; 4× L40S. Git: `main`, push only when asked.
- **Wrap mechanics gotcha:** on a *resumed* session `start.json` holds a mid-session SHA — use the
  first-commit-parent fallback for the true changeset.
