---
title: "Upspeed — last-session state (read first)"
tags: [reference]
aliases: [upspeed]
---

# Upspeed — read first, write last

**Last updated:** 2026-06-29 (S45 — /write + /meta. **/write:** rebuilt R07 from scratch through the
`sci-write-v2` pipeline as a skill-eval (full gated loop, F16 gate, converged after 4 revise rounds /
~40 opus reader-passes) → [`reports/R07_sci-write-v2-rebuild.md`](reports/R07_sci-write-v2-rebuild.md),
a comparison artifact, NOT a canonical finding-report and NOT in the reports ordering. **/meta:**
restored the audience-by-layer "two modes" rule the D048 cutover dropped — `meta.layer` now drives the
reader-model code/gloss policy (D053). **NO experiment, NO science number, NO rung change — Q0–Q5 stand.**)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md)** (Q0–Q5 unchanged since S25). With no task,
> run `/orient`. **Next: Erfan validates D053 by re-running the R07 rebuild in `report` mode.**

## What this session did
- **Worktree.** Ran in an isolated git worktree (`worktree-r07-write`) so a parallel Q4 `/work` session
  could use the main checkout without contention. Committed + merged to `main` at close.
- **/write — R07 rebuild (skill-eval).** Re-derived R07 (Q1) from the frozen evidence (E003) through the
  whole `sci-write-v2` loop — lattice → F16 gate (Erfan-approved) → draft → audit. An opus
  `oracle-reviewer` ran at every stage on top of the pipeline's intrinsic judges. The stage-5 panel
  caught the draft's headline over-claiming "the objective sheds alignment" and pulled it back to E003's
  recorded PARTIAL verdict, within recorded evidence (no handoff). Converged (draft `aed2b50a`).
- **Comparison.** Two blind opus analyses (ours + Erfan's external, top-venue rubric) agreed: the rebuild
  is *external/manuscript* register (standalone, codes stripped); the baseline is *internal-report*
  register (project-embedded). Both bound claims correctly.
- **/meta — D053.** The external register traced to the reader-model audience being set externally,
  because the D048 cutover dropped the archived "codes descend by layer" rule. Restored via `meta.layer`
  (report|extended|public), 3 files, zero script-logic change, all selftests pass. D053; L069.

## What's next (resume here)
- **Validate the two-mode fix (Erfan, new session):** re-run the R07 rebuild with `meta.layer: report` —
  expect report-register prose (Q1/R06/E003 used in prose, closer to the baseline). The end-to-end test
  that D053 works.
- **Live science thread (UNCHANGED since S25):** `/work` Q4 sample-efficiency E024, OR `/write` R08 (Q2),
  OR `/interpret` the parked E006 voxelwise-CI item. Erfan's call.
- **Deferred /meta follow-up:** per-layer F17 register exemplars (an internal-report exemplar set) — not
  built (D053 honest-limit).

## Blockers / open loops
- The R07 rebuild is a comparison artifact in *external* register; to become canonical it must be
  re-derived in `report` mode (the validation above).
- `docs/manuscript/README.md:34` bare `+0.06` (no cite) — pre-existing, fix on a `/write` touch.

## Key facts for next session
- **Two modes are now live in `sci-write-v2`:** set `meta.layer` at Stage 1 (report = internal/codes-OK;
  extended = parenthetical; public = zero codes, all named in prose). See D053 + the SKILL Stage 1.
- **Run code:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache`; 4× L40S. Git: `main`.
- **Worktrees:** this session used `git worktree` under `.claude/worktrees/` (`EnterWorktree`/`ExitWorktree`),
  merged to main at close — the clean way to run two sessions without status-doc collisions.
