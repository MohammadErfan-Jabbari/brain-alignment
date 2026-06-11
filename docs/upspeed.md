# Upspeed — read first, write last

**Last updated:** 2026-06-11 (Session 7 — working — E004 lever + E006 powered A2 + E005 F1-confirmed)

> **Canonical state lives in [`ladder.md`](ladder.md)** (the rung board + next step, D015). This file is
> the last-session prose; if it disagrees with the ladder, the ladder wins. With no task, run `/orient`.

## Current state

Phase = **Run → Judge**, three rungs climbed this session. The keystone `$\mathcal{L}_{\text{brain}}$` is **built** and the thesis now has its **positive headline result**:

- **L0/A2 — alignment is real — ✅ PASS, now POWERED.** E002 (Tuckute 5-ROI) + **E006** (LeBel UTS03 voxelwise): trained−untrained gap **+0.021 (gpt2) / +0.028 (Qwen)** on 11.4k NC-reliable voxels, 95–99% positive, after the full phone-tier+eng1000 anti-confound. Clears the Hadidi/Feghhi 2026 bar.
- **L1 — is it an optimizable lever — 🟡 PARTIAL.** E004: brain loss built (D010 → co-trained MSE); a brain-SPECIFIC lever exists (+0.0032 vs permuted twin) but small/fragile, sub-threshold on 5 ROIs.
- **L3/F1 — the headline — 🟡 PARTIAL-PASS (in-domain).** **E005**: alignment-guided KD beats perplexity-only KD **at matched perplexity**, brain-specifically — paired (kd_brain − kd_brain_permuted) = **+0.0081 [+0.0023, +0.0171]**, CI excludes 0, 4/5 folds + (robust to fold-4), gain holds despite slightly-worse ppl. **The dissociation E003/E004 couldn't establish.** Small (~1.6% NC) → an **A+B synthesis**: F1 confirmed + the honest rate–distortion characterization.

## What was done (Session 7 — working, autonomous)

Three full Design→Run→Judge cycles, each oracle-gated before compute (one HOLD caught a fatal confound each time):
1. **E004** (lever): built `brain_loss.py` (loss family) + `run_brain_lever.py` (LoRA, rotating folds, per-kind permuted twins). 2 reviews caught the covariate-shift confound (→ rotating folds), full-FT ppl-collapse (→ LoRA), readout absorption (→ permuted twins). Verdict PARTIAL.
2. **E006** (powered A2): built `lebel_adapter.py` + `run_lebel_encoding.py` (reuse official LeBel pipeline; staged TextGrids+eng1000; CC_norm voxel selection from `wheretheressmoke` repeats; phone-tier+eng1000 nuisance). Verdict STRONG PASS; lever statistic underpowered (don't build E007).
3. **E005** (F1 headline): extended the harness with a KD-teacher term (permuted twin = matched-ppl control by construction); reordered to Tuckute-in-domain (powered MDE +0.0035). Verdict F1 CONFIRMED in-domain.
4. Literature: paper-digested **Hadidi/Feghhi 2026** (residual ≤10% — the anti-confound bar, matches our finding). lit-scout sweep.

## What to do next (ordered — what's next to *run*)

1. **LeBel voxelwise TRANSFER test** — does E005's in-domain F1 gain (+0.0081) generalize cross-dataset/granularity? **Needs a powered statistic** (per-voxel paired / LH-region-restricted; the mean-over-voxels MDE +0.013 ≫ the effect) — **design + oracle-gate FIRST**, then measure each E005 KD student on the E006 LeBel protocol. Positive = strong generalization; powered null after in-domain positive = "real but doesn't transfer."
2. **λ-sweep / multi-rate trade-off curve** — trace kd_brain & kd_ppl (ppl, alignment) frontiers (λ_brain grid, ≥2 compression rates) for the rate–distortion / "how small" characterization. In-domain Tuckute (powered) first, then LeBel.
3. **Doc-consistency (carry-over):** dedup `feghhi-2024`/`hadidi-2024` (same paper, arXiv-vs-NatComms first author); sweep R03/R04 for stale "E004 = headline" (now E005, E004 = lever).

## Blockers

- **None rate-limiting.** Data staged, harness + powered LeBel substrate built, GPUs free.
- **Watch:** the transfer/curve statistics must be powered (the LeBel mean-over-voxels is not — use per-voxel-paired/region-restricted; the in-domain paired contrast IS powered, MDE +0.0035). Keep the permuted-twin-at-matched-ppl as the confound-clean primary (L014). Effect is small — frame as A+B, never overclaim (Hadidi/Feghhi ≤10%).

## Key facts

- **Run Python:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1`. GPUs: 4× L40S (0,3 free; 1,2 had other jobs). Background jobs: standalone `nohup ... >| log &` (zsh noclobber needs `>|`; don't chain `& ; grep`), or `run_in_background` waiter loops (nohup jobs aren't harness-tracked).
- **E005 rerun:** `CUDA_VISIBLE_DEVICES=0 uv run python scripts/run_brain_lever.py --model Qwen/Qwen2.5-0.5B --kd-teacher Qwen/Qwen2.5-1.5B --arms mse lm_only --permute-kinds mse --seeds 0 1 2 --folds 5 --lambda-grid 10`. Primary stat = paired mse − mse_perm.
- **E006 rerun:** `... run_lebel_encoding.py --model Qwen/Qwen2.5-0.5B --n-stories 20 --n-folds 5 --reliability-thresh 0.5`. Verdict = trained−untrained gap on NC voxels.
- **Outputs** (gitignored): `outputs/E00{4,5,6}_*.json`, `E004_premises.json`. **Models cached:** gpt2 family, Qwen2.5 0.5/1.5/3/7B. **Data:** Tuckute `data/tuckute2024/`; LeBel UTS03 responses + TextGrids + eng1000 `data/lebel_ds003020/`.
- **Git:** `main`. Commit continuously/atomically (D007); push only when asked. **Deps added:** peft, accelerate, wordfreq, tables.
