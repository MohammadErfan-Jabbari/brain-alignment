# Upspeed — read first, write last

**Last updated:** 2026-06-12 (Session 9 — ANALYSIS: teaching-walk Layer 0→1, concepts primer + R05 living narrative, panel-hardened)

> **Canonical state lives in [`ladder.md`](ladder.md)** (the rung board + next step, D015). This file is
> the last-session prose; if it disagrees with the ladder, the ladder wins. With no task, run `/orient`.

## Current state

Phase = **Argue/Compound (write-up + understanding)**. The science is unchanged from S8: experimental program **complete, Fork B** (a measurement-validity result + well-powered nulls), manuscript v0.9 artifact-complete. **No rung moved this session — it was analysis only.** What changed is the *communication layer*: Erfan is being walked through the thesis from first principles, and that walk is being captured as durable docs.

- **L0/A2 — alignment real & powered — ✅ PASS.** Unchanged (E006: +0.0207/+0.0277 gap, 95–99% voxels+).
- **L3/F1 — ❌ NULL per-subject, robust.** Unchanged. **L2b/A3 — ❌ bounded NULL.** Unchanged.
- The honest figure for E002's NC-fraction is **~7%** (functional ceiling 0.491/0.559), not the ~10% that the anatomical-mask 0.353 gave — L012; now corrected in R05.

## What was understood / written this session (analysis)

1. **Taught Layer 0 + Layer 1** (the frame & bet → measurement → the lever → the E007 reroute). Erfan can now reconstruct: MI-lens vs encoding-R²-measured; why linear; A2 gates A1/A3; real ≠ movable ≠ useful; statistical power & MDE (the bathroom-scale framing); why E006's MDE killed E007 and rerouted to E005.
2. **`docs/07-concepts-primer.md`** — NEW. Plain-language home for the reusable primitives (voxel/ROI, encoding model, unique R², noise ceiling & "% of ceiling", trained−untrained gap, permuted twin, **perplexity**, the datasets, E/R/L/D-number naming). E002/R03/README point at it.
3. **`docs/reports/R05_thesis-narrative-from-first-principles.md`** — NEW, **LIVING**. The pedagogical, course-grounded narrative of the whole arc, role-distinct from the terse manuscript. Covers Layer 0 → Layer 1 / E007 reroute; §9+ (E005 collapse → robustness → Fork B) are structured placeholders for the next sessions. **Panel-reviewed and revised** (see below).
4. **`docs/learning/thesis-arc-checklist.md`** — the teaching tracker (Layer 0 ✅, Layer 1 content delivered).

## What to do next (Erfan's call)

**Mode = ANALYSIS.** Resume the walk at **Layer 3 = E005** (the apparent +0.0081 headline and how the panel + E008 collapsed it to a per-individual null). Teaching it and writing **R05 §9** are the same motion. Then §10 (E008/the powered null), §11 (Fork-B reframe), §12 (robustness E011/E013b/E013/E014), §13 (E009 + E015), §14 (where we stand). After R05 reaches the end: figures check + manuscript read-through (the original analysis backlog).

## Blockers / open loops

- **No running jobs; working tree clean** (~9 atomic commits this session, all docs).
- **Doc-audit follow-ups filed in `tasks.md`** (real, low-severity, write-up phase): ~8 experiment docs have stale "pre-run/pending" Status lines despite recorded results; **E005's body still leads with the retracted "F1 CONFIRMED"** (addendum should be the lead); R03/R01 carry pre-R04-correction literature phrasings without inline notes.
- **Pending Erfan (process, carried from S8):** the Stop-hook re-fire operating rule (L031).

## Key facts

- **Run Python:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1`. GPUs 4× L40S free.
- **Teaching:** native `socratic-tutor` skill is the tool for the walk (did NOT install the external mattpocock `teach` skill — redundant). Quiz style: **vary the correct-answer position; prefer open-ended "explain it" or genuinely hard MCQs** (Erfan feedback, saved to memory + gbrain).
- **R05 vs manuscript:** R05 = teach-it-from-scratch narrative (math explained at length); manuscript = terse submission artifact. Keep them role-distinct; do not let R05 become a second paper.
- **Corrected number to carry:** Tuckute functional NC ceiling = 0.491 (mean) / 0.559 (network); 0.353 was the anatomical-mask mislabel (L012). E002's "~10%" → honest ~7%.
- **Tooling gotcha (carried):** offline `load_dataset("wikitext",...)` FAILS — use `"Salesforce/wikitext"`. `outputs/` is gitignored.
- **Git:** `main`, push only when asked.
