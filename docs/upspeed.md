---
title: "Upspeed — last-session state (read first)"
tags: [reference]
aliases: [upspeed]
---

# Upspeed — read first, write last

**Last updated:** 2026-06-29 (S45 — TWO parallel sessions, both worktree-merged to main. **/work Q4 E024:**
gaze-as-privileged-information → recorded **NEGATIVE**, gate-blocked (gaze ⊥ relation-label on ZuCo-NR; 5-arm
build correctly NOT triggered; Q4/A3 stays ❌; L069/L070). **/write + /meta:** rebuilt R07 through
`sci-write-v2` as a skill-eval (→ comparison artifact) and restored the audience-by-layer "two modes" rule
the D048 cutover dropped (`meta.layer`; D053, L071). **NO experiment-driven rung change — Q0–Q5 stand.**)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md)** (Q0–Q5 unchanged since S25; Q4 also null on the
> gaze-PI/sample-efficiency axis). With no task, run `/orient`.

## What S45 did — two parallel tracks

### /work — E024 (the privileged-information line)
- Ran the LUPI sample-efficiency climb on ZuCo-1.0 NR relation-detection (gaze-first) through the binding
  positive-control gate, continuous opus review + Codex.
- **Recorded NEGATIVE, gate-blocked:** (1) **gaze ⊥ relation-label** — airtight null every readout (binary AUC
  0.51 p=0.45; multiclass balanced-acc 0.20 p=0.35; rich-35d+RF; within-subject), reliable gaze = length
  confound; (2) **structural disqualifier** — ZuCo-NR has only 7 paragraphs → no stable paragraph-disjoint
  split; (3) **leak sharpening** — TSR task-directed gaze predicts relation-type (balanced-acc 0.295, perm-p
  0.003) → gaze carries the relation only when actively hunted. The 5-arm build was correctly NOT triggered.
  **Q4/A3 stays ❌.** Lessons L069 + L070.
- Erfan stopped the ZuCo gaze-relation line; the negative + DPI bound + control battery is the methodology
  contribution to consolidate. Full record:
  [`experiments/E024_zuco-lupi-sample-efficiency.md`](experiments/E024_zuco-lupi-sample-efficiency.md); brain
  `projects/brain-alignment-e024-gaze-lupi-negative`.

### /write + /meta — R07 rebuild + sci-write-v2 two modes
- **/write:** rebuilt R07 (Q1) from frozen E003 through the full `sci-write-v2` loop (lattice → F16 gate,
  Erfan-approved → draft → 4 audit/revise rounds to convergence; an opus oracle-reviewer at every stage). →
  [`reports/R07_sci-write-v2-rebuild.md`](reports/R07_sci-write-v2-rebuild.md), a comparison artifact (NOT
  canonical, NOT in the reports ordering).
- Two blind opus analyses (ours + Erfan's external top-venue rubric) agreed: rebuild = external/manuscript
  register, baseline = internal-report register; both bound claims correctly.
- **/meta — D053:** the external register traced to the reader-model audience being set externally, because the
  D048 cutover dropped the archived "codes descend by layer" rule. Restored via `meta.layer`
  (report|extended|public), 3 files, zero script-logic change, all selftests pass. D053; L071.

## What's next (resume here) — Erfan's call
- **Validate D053:** re-run the R07 rebuild with `meta.layer: report` → expect report-register prose (codes in
  prose, closer to the baseline). The end-to-end test that the two-mode fix works.
- **Consolidate the E024 negative** into the negative-results spine (a `/write`/analysis task).
- **Live science thread (UNCHANGED since S25):** `/write` R08 (Q2), OR `/interpret` the parked E006
  voxelwise-CI item. (The Q4 gaze-PI line is stopped.)

## Blockers / open loops
- R07 rebuild is an external-register comparison artifact; to become canonical, re-derive in `report` mode.
- `docs/manuscript/README.md:34` bare `+0.06` (no cite) — pre-existing, fix on a `/write` touch.

## Key facts for next session
- **Two modes now live in `sci-write-v2`:** set `meta.layer` at Stage 1 (report = internal/codes-OK; extended =
  parenthetical; public = zero codes, all named in prose). D053 + the SKILL Stage 1.
- **The LUPI design rules:** L069 (train-only PI helps only to the extent text-recoverable; reliable-but-leaked
  is a trap), L070 (check the paragraph/grouping count + run the PI→label probe + positive-control gate before
  any build).
- **Run code:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache`; 4× L40S. ZuCo `.mat` are MATLAB v5
  (scipy). Git: `main`.
- **Worktrees:** both S45 sessions used `git worktree` + merged to main — the clean way to run parallel
  sessions; reconcile the four status docs at merge (this wrap did: combined Last-updated/Next-session,
  kept both sessions' learnings L069/L070/L071).
