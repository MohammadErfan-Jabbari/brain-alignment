# Experiment — E006: LeBel UTS03 voxelwise A2-feasibility (powered substrate validation)

**Created:** 2026-06-11 · **Status:** DESIGN — LOCKED pending oracle review (do not run until PASS) · **Mode:** working
**Direction:** R03 Layer 0/A2 at *powered* (voxelwise) resolution — the prerequisite substrate for the LeBel lever re-test (E007) that confirms E004's fragile PARTIAL.
**Predecessors:** `E002` (A2 PASS on Tuckute, 5 ROIs) · `E004` (Tuckute lever = PARTIAL/fragile — routes here per its predeclared, power-limited rule)
**Code:** `scripts/lebel_adapter.py` (built, CPU+GPU-validated), `scripts/run_lebel_encoding.py` (TBD after oracle PASS), reuses `data/paper-repos/deep-fMRI-dataset/encoding/ridge_utils`
**Output:** `outputs/E006_lebel_feasibility.json`

---

## Why this exists (and why A2-only, not the lever)

E004 found a *fragile* brain-specific lever on Tuckute (Qwen co-trained-MSE − its permuted twin = +0.0032 [CI +0.0006,+0.0058], but fold 4 carries ~half; the absolute lever-vs-base CI includes 0). The 5-ROI screen (MDE≈+0.006) is underpowered for a +0.003 effect. Its predeclared rule routes to LeBel UTS03 voxelwise (~95k voxels, within-subject deep-sampling) for the powered confirmation.

**But a powered lever re-test is only meaningful if the substrate carries the signal at all.** E006 establishes that — the E002/A2 question at voxel scale: does a *trained* LM's middle-layer representation predict UTS03 BOLD *beyond nuisance*, under contiguous **story-level** splits, materially above an *untrained* control? This is pure measurement (no brain-tuning), cheaper, and a clean kill-gate: if it fails, LeBel is a dead substrate for our pipeline and E004's routing is moot (reframe per charter). If it passes, **E007** (the lever re-test: brain-tune Qwen co-trained-MSE at TR level, held-out-story unique R² vs its permuted twin) becomes worth the heavier TR-level training loop.

## Claim tuple (predeclared)

- **Metric:** voxelwise encoding R² (ridge, story-grouped CV), then **unique R²** = R²([nuisance, LM-features]) − R²([nuisance]), averaged over voxels and over the NC-reliable voxel subset; trained−untrained gap is the honest signal (L007). CC_norm-normalised where repeats permit.
- **Anti-confound (L003, naturalistic variant):** contiguous **story-level** held-out CV (whole stories out — no within-story TR leakage; the time-series analogue of contiguous blocks, and the fix for bilgin-2026's TR-shuffle inflation). FIR delays 1–4 TRs (hemodynamics). Nuisance = **word-rate** (words/TR) + **static/non-contextual embedding** (mean input-embedding per word → downsampled), FIR-delayed identically. **Surprisal stays OUT** (LM-derived → over-subtracts the construct, E004/L012). Static nuisance from the *untuned* model, byte-identical across the trained/untrained contrast.
- **Pass:** trained-LM unique R² > 0 AND materially exceeds the untrained-same-architecture control (≥3 seeds), on the NC-reliable voxels.
- **Kill:** trained ≈ untrained or ≈ 0 after nuisance → LeBel does not carry the signal for our pipeline at voxel scale.

## Design (LOCKED pending oracle review)

- **Subject/data:** UTS03, 84 stories on disk (`preprocessed_data/UTS03/*.hf5`, (TRs, 95556 voxels)); 84 TextGrids staged; `english1000sm.hf5` + `respdict.json` staged. Adapter validated: `ridge_utils` reuse for TextGrid→wordseq→Lanczos(window=3)→trim(feat[10:-5])→FIR(make_delayed 1..4); BOLD as-is (verified alignment, e.g. adollshouse 256→241=BOLD 241). LM word-features GPU-validated (697 words→768d, 0.2s, non-degenerate).
- **Stories used:** a fixed set of **~20 stories** (the LeBel "train" pool minus a held-out test set), leave-**N-stories**-out CV (e.g. 5 folds of 4 held-out stories) — keeps compute tractable while powered (each story ~150–300 TRs → thousands of TRs total, ≫ Tuckute's 1000 items × 5 ROIs). Story list pinned for reproducibility.
- **Models:** gpt2 (L7) + Qwen2.5-0.5B (L12), matching E002/E004; untrained same-arch control (≥3 seeds, the Feghhi control).
- **Encoding:** ridge per voxel (RidgeCV with a fixed alpha grid at first pass; banded/bootstrap-alpha is a refinement). Voxel chunks to bound memory over 95k voxels. Report mean-voxel R², **top-NC-voxel** R² (CC_norm>0.05, à la merlin-2026), and unique-over-nuisance.
- **NC / CC_norm:** LeBel ships repeated stories → split-half CC_norm per voxel where available; else report raw R² + the trained−untrained gap (the gap is the verdict regardless of normaliser, L007).
- **Compute:** LM feature extraction over ~20 stories × {gpt2,Qwen} × {trained, 3×untrained} (~minutes/config, GPU); ridge over 95k voxels × CV (the heavy part, chunked). Est. ~1–2 h. GPUs 0/3 free.
- **Stop rule:** fixed story set, fixed layers (E002 peaks), fixed CV, fixed nuisance, fixed seed count. Pure measurement — no training, no tuning toward the outcome.

## Decision rule (predeclared)

- **PASS (powered A2 holds).** Trained unique R² > 0 with CI excluding 0 AND trained−untrained gap > 0 (CI excludes 0), on NC-reliable voxels. → LeBel carries the signal; **proceed to E007** (the lever re-test: brain-tune Qwen co-trained-MSE, the E004 front-runner, at TR level with story-held-out unique R² vs **its block-permuted twin as the PRIMARY predeclared specificity test** — fixing E004's mis-specified unpaired permuted test — plus a perplexity-matched/gentler regime since E004's LoRA finetune degraded ppl ~2×).
- **KILL (substrate dead).** Trained ≈ untrained or ≈ 0 after nuisance. → LeBel cannot resolve our question; E004's PARTIAL cannot be confirmed there. Reframe (charter): the alignment signal is real (E002) but neither cleanly optimizable (E004) nor voxelwise-separable here.

## How to run

```bash
cd /home/centcom/data/brain-alignment
export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1
CUDA_VISIBLE_DEVICES=0 uv run python scripts/run_lebel_encoding.py --model gpt2 --untrained-seeds 0 1 2
CUDA_VISIBLE_DEVICES=3 uv run python scripts/run_lebel_encoding.py --model Qwen/Qwen2.5-0.5B --untrained-seeds 0 1 2
```

## Status

`lebel_adapter.py` built + validated (non-LM path CPU; LM-feature path GPU). `run_lebel_encoding.py` + the oracle review are the remaining work before a run. Scope deliberately A2-only (kill-gate); the lever re-test is E007, gated on this passing. The E004→E006 routing and the corrected paired-primary predeclaration are the load-bearing carry-forwards.

## Iteration log

| Date | Run / seed | Command / config | Result | Observation | Next |
|---|---|---|---|---|---|
| 2026-06-11 | design | — | adapter validated; design locked pending oracle | scoped A2-only (lever→E007) | oracle review → build runner → run |
