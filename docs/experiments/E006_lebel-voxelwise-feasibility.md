# Experiment — E006: LeBel UTS03 voxelwise encoding feasibility (powered substrate validation)

**Created:** 2026-06-11 · **Status:** DRAFT design (oracle review + lock pending; do not run until locked) · **Mode:** working
**Direction:** R03 Layer 0/A2 at *powered* resolution; the substrate for re-running L1 (E004) and L3/F1 (E005) at voxel scale.
**Predecessors:** `E002` (A2 PASS on Tuckute, 5 ROIs) · `E004` (Tuckute lever screen — if null/underpowered, routes here per its predeclared rule)
**Code:** `scripts/lebel_adapter.py` (built + CPU-validated), `scripts/run_lebel_encoding.py` (TBD), reuses `data/paper-repos/deep-fMRI-dataset/encoding/ridge_utils`
**Output:** `outputs/E006_lebel_feasibility.json`

---

## Why this exists

E004 tests the lever on Tuckute (5 ROIs, NC≈0.49) where MDE(80%)≈+0.006–0.010 — adequate only for a moderate-to-large effect. Its predeclared rule routes a null (or a small unconfirmed effect) to **LeBel UTS03 voxelwise** (~95k voxels, within-subject deep-sampling), the powered benchmark. But a powered re-test is only meaningful if the substrate itself carries the signal. **E006 establishes that**: does a trained LM's middle-layer representation predict UTS03 BOLD *beyond nuisance*, under contiguous **story-level** splits, materially above an untrained control — the E002/A2 question at voxel resolution.

If E006 fails (trained ≈ untrained, or ≈ 0 after nuisance), LeBel is a dead substrate for our question and the routing from E004 is moot — we'd reframe (charter). If it passes, LeBel becomes the powered home for the lever (E004') and the headline (E005).

## Claim tuple (predeclared)

- **Metric:** voxelwise encoding R² (or CC), then **unique** R² after nuisance subtraction, averaged over voxels (and NC/CC_norm-normalised). Anti-confound = the time-series analogue of L003: **story-level held-out** (whole stories out — no within-story TR leakage), FIR delays (1–4 TRs) for hemodynamics, nuisance = word-rate + per-word low-level features (length, log-frequency) downsampled identically; static/non-contextual embedding control.
- **Pass:** trained-LM unique R² > 0 and materially exceeds the untrained-same-architecture control (≥3 seeds), NC/CC_norm-normalised.
- **Kill:** trained ≈ untrained or ≈ 0 → LeBel doesn't carry the signal at voxel scale for our pipeline.

## Design (DRAFT — to lock + oracle-review before running)

- **Subject/data:** UTS03, 84 stories on disk (`data/lebel_ds003020/preprocessed_data/UTS03/*.hf5`, (TRs, ~95k voxels)); 84 TextGrids staged. Adapter `lebel_adapter.py` reuses the official LeBel pipeline (Lanczos window=3 downsample, feat[10:-5]+zscore, BOLD[5:-5]+zscore, FIR make_delayed(1..4), TR=2.0045) — CPU-validated end-to-end (the non-LM path).
- **Models:** gpt2 (L7) + Qwen2.5-0.5B (L12), matching E002/E004; untrained same-arch control (≥3 seeds).
- **Features:** per-word contextual hidden state at the verdict layer (chunked extraction, `lm_word_features`) → Lanczos→TR → FIR. **GPU-validate `lm_word_features` first** (it is the one custom piece; the CPU smoke covers everything else).
- **Splits:** story-level held-out CV (e.g. leave-N-stories-out, contiguous within story). NO TR shuffling (the Feghhi/Oota leakage; cf. bilgin-2026's TR-shuffle weakness, L003).
- **Encoding:** ridge per voxel (banded/bootstrap-alpha per the LeBel pipeline, or RidgeCV at first pass); report mean voxel R², top-k-voxel R², and unique-over-nuisance.
- **NC:** LeBel uses CC_norm (split-half); compute per-voxel CC_norm from repeats if available, else report raw + trained−untrained gap.
- **Compute:** LM features over 84 stories × ~1.5k words is the GPU cost (~chunked); ridge over 95k voxels is memory-managed (voxel chunks). Run after E004 frees the GPUs.

## Open design questions (resolve at lock)

- Exact nuisance set for naturalistic data (word-rate, low-level acoustic? — we have text only; use word-rate + length + log-freq + static embedding). Surprisal stays OUT of nuisance (LM-derived, over-subtracts — E004 lesson).
- Leave-N-out story CV vs the LeBel canonical train/test split (their sess→story mapping). Prefer a few contiguous story-holdout folds.
- Voxel selection: all 95k vs NC-thresholded (e.g. CC_norm>0.05, as merlin-2026) to focus power on reliable voxels.

## Status

`lebel_adapter.py` built + CPU-validated (wordseq→downsample→trim→FIR→BOLD align). `run_lebel_encoding.py` + the locked design + oracle review are the remaining work before a run. Sequenced after the E004 verdict (which determines whether the first LeBel run is A2-feasibility-only or folds in the lever re-test).
