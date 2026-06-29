---
title: "S45 — /work Q4 E024: gaze-as-privileged-information → NEGATIVE (gate-blocked)"
tags: [timeline, work]
aliases: [S45, 2026-06-29-work-E024]
---

# S45 (2026-06-29) — /work: E024 gaze-PI sample-efficiency → recorded NEGATIVE

**Stance:** `/work` (explicit, Erfan). **Isolation:** git worktree `worktree-E024-sample-efficiency` (8 commits, merged to main at close). **Rung change:** none — Q4/A3 stays ❌; the privileged-information/sample-efficiency axis is added to the robust null.

## What ran
A full `/work` climb on Q4's reopened privileged-information line (E024), driven to a recorded verdict through the binding positive-control gate. Continuous opus review at every chunk (Erfan's mandate).

1. **Substrate decision (converged, dual-opus-reviewed).** `dataset-scout` mapped the gaze-corpus landscape; decision stress-tested by `oracle-reviewer` (DESIGN: HOLD→PASS) + `first-principles-grounder` (GROUNDED). Chose **ZuCo-1.0 NR relation-detection, gaze-first** over OneStop: under the held-out-test-sentence estimand, OneStop's reliable-but-label-correlated gaze is a *transferability trap* (gaze→label channel severed at test); ZuCo's clean low-leak label constrains the real text→label space. Lopez-Paz 2016 digested → confirms the LUPI precondition is target-tied capacity/approximation, **not** teacher reliability (hardens the choice).
2. **Loader + reliability.** Built the ZuCo-NR per-word gaze loader (MATLAB v5/scipy, not h5py; 300 sentences, 12 subjects, 300/300 labels joined via alnum-exact+fuzzy). **Codex second-impl review caught a reliability-deflation bug** (no-word-data sentences → fake all-zero words for ZJS/ZPH) — true gaze split-half reliability **0.71**, not the buggy 0.51. Embeddings: Qwen2.5-0.5B layer-12, 896-d.
3. **Binding positive-control gate → FAIL.** Built the LUPI learning-curve harness (paragraph-disjoint splits, capacity-fair PCA, matched linear student, distillation + feature-aug mechanisms) and the MDE gate. Building it reproduced the **DPI/severed-channel point empirically**: train-only PI can't transfer info text can't represent. The gate's first MDE was spurious (one-sided deterministic boost → zero-width CI); fixed to a **test-item bootstrap** → empirical low-n MDE 8pp (and fragile — see below).
4. **The decisive finding.** a_real (gaze→relation-label CV acc) = 0.543 ≈ chance 0.547. A richness probe (rich 35-d, RandomForest, multiclass) confirmed **gaze ⊥ relation-label is airtight**: binary AUC 0.508 (perm p=0.45), multiclass balanced-acc 0.202 (chance 0.20, p=0.35). The *reliable* gaze features are a sentence-length confound (r≈0 to label).
5. **Post-result panel.** `counter-argument` SURVIVES-IF-NARROWED (the binary-collapse objection refuted by the multiclass+rich probe); `stat-aggregation-auditor` VERDICT-SAFE (gaze-null solid; the 8pp MDE is fragile because **ZuCo-NR has only 7 paragraphs** → no stable paragraph-disjoint split exists).
6. **Leak sharpening (Erfan-chosen).** Ran the same probe on TSR (task-directed reading): gaze→relation-type balanced-acc **0.295, perm p=0.003** vs NR's chance. → gaze carries the relation **only when the reader hunts it** (a task-direction leak), not in natural reading. A LUPI "gain" from such gaze would be the leak, not transferable cognition.

## Verdict
**E024 = recorded NEGATIVE.** Gaze cannot serve as transferable privileged information for relation detection on ZuCo (gaze⊥label in natural reading; leaks only under task-direction; substrate can't form a stable split). The binding gate worked exactly as designed — it blocked a multi-day 5-arm build on a dead substrate. The contribution is the **control battery + DPI bound that caught it** (matches §8's "methodology/negative most likely"). Path (Erfan): stop the ZuCo gaze-relation line, consolidate the negative; OneStop not pursued (transferability trap).

## Artifacts
- Code: `scripts/e024/{zuco_nr_loader,embed,lupi_harness,probe_gaze_richness}.py` (all selftested).
- Numbers: `outputs/e024/{zuco_nr_reliability,positive_control,gaze_richness_probe_NR,gaze_richness_probe_TSR}.json` (gitignored).
- Record: `docs/experiments/E024_*.md` (substrate decision + RESULT S45 + Findings 1–3 + panel verdicts).
- Canonical note: `docs/literature/canonical/lopez-paz-2016_unifying-distillation-privileged-information.md`.
- Brain: `projects/brain-alignment-e024-gaze-lupi-negative`.

## Learnings
- **L069** — for a held-out-text estimand, train-only PI helps only to the extent its signal is text-recoverable; the reliable-but-leaked trap.
- **L070** — gaze corpora have few unique paragraphs → paragraph-disjoint splits are unstable; run the informativeness (PI→label) probe + the positive-control gate BEFORE any build.

## Process notes
- 8 atomic commits in the worktree, merged to main at close (not pushed).
- One self-correction: edits initially went to the main checkout by absolute path (relocated to the worktree); thereafter all edits targeted the worktree path.
