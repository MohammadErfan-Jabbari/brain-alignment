---
title: "Upspeed — last-session state (read first)"
tags: [reference]
aliases: [upspeed]
---

# Upspeed — read first, write last

**Last updated:** 2026-06-29 (S45 — **/work Q4 E024: gaze-as-privileged-information → recorded NEGATIVE,
gate-blocked.** Ran the full LUPI sample-efficiency climb on ZuCo-NR through the binding positive-control
gate (continuous opus review). Verdict: **gaze ⊥ relation-label** (airtight null, every readout) → the
5-arm build was correctly NOT triggered. Q4/A3 stays ❌; the privileged-information axis is added to the
robust null. 8 commits in worktree `worktree-E024-sample-efficiency`, merged to main. Prior: S44 — /meta
Obsidian vault overhaul.)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md)** (Q0–Q5 unchanged since S25; Q4 now also
> null on the gaze-PI/sample-efficiency axis). With no task, run `/orient`.

## What this session did (/work — E024, the privileged-information line)
- **Substrate converged + dual-opus-reviewed:** ZuCo-1.0 NR relation-detection, gaze-first (over OneStop —
  OneStop's reliable-but-label-correlated gaze is a transferability trap). Lopez-Paz 2016 digested.
- **Built + Codex-reviewed the per-word gaze loader** (MATLAB v5/scipy; 300 sentences, 12 subjects; Codex
  caught a reliability-deflation bug → true gaze split-half reliability **0.71**).
- **Binding positive-control gate → FAIL → recorded NEGATIVE.** Two findings: (1) **gaze ⊥ relation-label**,
  airtight (binary AUC 0.51 p=0.45; multiclass balanced-acc 0.20 p=0.35; rich-35d + RandomForest;
  within-subject) — the reliable gaze features are a length confound; (2) **structural disqualifier** —
  ZuCo-NR has only 7 paragraphs → no stable paragraph-disjoint split (MDE fragile, ≥~10pp).
- **Leak sharpening (Finding 3):** TSR (task-directed reading) gaze predicts relation-type at balanced-acc
  0.295 (perm **p=0.003**) vs NR's chance → gaze carries the relation ONLY when actively hunted (a
  task-direction leak), not in natural reading.
- Panel converged (counter-argument SURVIVES-IF-NARROWED, stat-aggregation-auditor VERDICT-SAFE, Codex clean).

## What's next (resume here)
- **E024 ZuCo gaze-relation line is STOPPED (Erfan, S45).** The negative + the DPI bound + the control
  battery that caught it is the methodology contribution — to be **consolidated** (an analysis/`/write` task,
  not `/work`): fold into the broader negative-results spine. OneStop NOT pursued (transferability trap).
- **Live science thread otherwise unchanged since S25:** `/write` R07/R08 finding-reports (the deferred
  sci-write-v2 evaluation), OR `/interpret` the parked E006 voxelwise-CI item. Erfan's call.

## Blockers / open loops
- None new. The E024 work is self-contained (`scripts/e024/`, `outputs/e024/` gitignored, the E024 doc).
- The full E024 record (substrate decision + RESULT S45 + Findings 1–3 + panel verdicts) is in
  [`experiments/E024_zuco-lupi-sample-efficiency.md`](experiments/E024_zuco-lupi-sample-efficiency.md).

## Key facts for next session
- **Brain:** the result is mirrored at `projects/brain-alignment-e024-gaze-lupi-negative`.
- **The LUPI design rule (L069):** train-only PI helps a held-out-text task only to the extent its
  label-relevant part is text-recoverable; reliable-but-leaked PI is a trap. **The substrate rule (L070):**
  check the paragraph/grouping count (not just N) and run the PI→label probe + positive-control gate before
  any build.
- **Run code:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache`; 4× L40S. ZuCo `.mat` are MATLAB v5
  (scipy, not h5py). Git: `main` (the worktree was merged + removed at close).
- **Pushing (if asked):** `gh auth setup-git` once, then `git push origin main`.
