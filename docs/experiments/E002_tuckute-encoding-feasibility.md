# Experiment — E002 real-data encoding feasibility on Tuckute 2024 (the A2 question)

**Created:** 2026-06-10 · **Status:** done — A2 PASS across 3 models (gpt2, gpt2-medium, Qwen2.5-0.5B)
**Direction:** `../reports/R03_brain-as-training-signal.md` (Layer 0 of the ladder) · **Mode:** working
**Code:** `scripts/run_encoding_feasibility.py`, `scripts/data_adapters.py:load_tuckute`, `scripts/pilot_lib.py`
**Output:** `outputs/E002_tuckute_feasibility.json`
**New to the vocabulary?** Voxel/ROI, encoding model, unique R², noise ceiling, "% of ceiling", what Tuckute is → `../07-concepts-primer.md`.

---

## Objective

Answer the charter's gating question on **real neural data** for the first time (E001 used synthetic fMRI and *could not* answer it by construction — L004):

> Does an LM's contextual middle-layer representation predict human language-network BOLD **beyond nuisance** (length, position, static embeddings), under the contiguous-split anti-confound protocol — and how large is that *unique* signal relative to an untrained-network control and the noise ceiling?

This is **A2** (measured alignment is not primarily nuisance). If it fails, the thesis premise fails and we reframe to measurement rigor (charter kill condition).

## Claim tuple

- **Metric:** unique encoding R² = R²([length, position, PCA(static), PCA(context)]) − R²([length, position, PCA(static)]), contiguous 5-fold CV, capacity-fair PCA (rank 50).
- **Pass:** trained-model unique R² is positive AND materially exceeds the untrained-network control (random init, same architecture, ≥3 seeds). Reported NC-normalised against LangNetw nc ≈ 0.353.
- **Kill:** trained unique R² ≈ 0, or ≈ untrained control → A2 fails.

## Design (locked before running)

- **Data:** Tuckute 2024 (`data/tuckute2024/`), 1000 isolated baseline sentences × 5 LH language ROIs (`lang_LH_{AntTemp,IFG,IFGorb,MFG,PostTemp}`), averaged over the 5 train participants (UIDs 848/853/865/875/876, matching the paper's encoding fit). Rows ordered by `item_id` (deterministic, contiguous-split friendly).
- **Models:** `gpt2` (12L), `gpt2-medium` (24L), `Qwen/Qwen2.5-0.5B` (24L). Layers probed: a spread around the middle (the brain-alignment sweet spot, Oota 2023).
- **Nuisance:** length + position (raw 2-D) and the mean **input-embedding** per sentence (static, non-contextual). Static and contextual blocks PCA-reduced to equal rank (50) per fold → capacity-fair partition (the L004 fix).
- **Control:** randomly-initialised model of the same architecture (Feghhi 2024 untrained-network control), ≥3 seeds, to show the signal is about *trained* language processing, not architecture + nuisance.
- **Anti-confound:** contiguous-block CV only (no shuffling); unique variance after nuisance subtraction is the only number claimed (L003).
- **Stop rule:** fixed model/layer grid; no training, no tuning. Pure measurement.

## How to run

```bash
cd /home/centcom/data/brain-alignment
export HF_HOME=/home/centcom/data/hf-cache CUDA_VISIBLE_DEVICES=0 HF_HUB_OFFLINE=1
uv run python scripts/run_encoding_feasibility.py \
  --models gpt2 gpt2-medium Qwen/Qwen2.5-0.5B --untrained-seeds 0 1 2
```

## Results — GPT-2 (final, n=5 contiguous folds; untrained over 3 seeds)

| Model · layer | raw R² | nuisance R² | full R² | **unique R²** |
|---|---|---|---|---|
| gpt2 trained · L3 | +0.0158 | +0.0203 | +0.0299 | +0.0095 ± 0.0055 |
| gpt2 trained · L6 | +0.0252 | +0.0198 | +0.0372 | +0.0174 ± 0.0067 |
| **gpt2 trained · L7** | +0.0263 | +0.0199 | +0.0398 | **+0.0200 ± 0.0084** |
| gpt2 trained · L9 | +0.0229 | +0.0203 | +0.0389 | +0.0186 ± 0.0068 |
| gpt2 **untrained** · L7 (3 seeds) | ≈ −0.04 | ≈ −0.004 | ≈ −0.01 | **−0.010 (range −0.005…−0.014)** |

**GPT-2 verdict:** trained unique R² peaks at **+0.020 ± 0.008** (layer 7, mid-network); the untrained control is **negative at every layer and every seed**. Trained − untrained ≈ **+0.030**. NC-normalised: +0.020 / 0.353 ≈ **0.057** of the noise ceiling. The signal is real, mid-layer-peaked, and absent in random features — a clean **A2 pass for GPT-2 on real neural data**.

## Results — cross-model summary (best mid-layer; trained n=5 folds, untrained n=3 seeds)

| Model (layers) | best layer | trained unique R² | untrained unique R² | **trained − untrained** | NC-normalised |
|---|---|---|---|---|---|
| gpt2 (12L) | L7 | +0.0200 ± 0.0084 | −0.0105 | **+0.0304** | 0.056 |
| gpt2-medium (24L) | L14 | +0.0187 ± 0.0050 | −0.0143 | **+0.0330** | 0.053 |
| Qwen2.5-0.5B (24L) | L12 | **+0.0362 ± 0.0102** | −0.0136 | **+0.0498** | **0.102** |

All three: trained unique R² **positive and mid-layer-peaked**; untrained controls **negative at every layer and seed**. Qwen2.5-0.5B (the most capable, most recent model) shows the strongest alignment — ~10% of the LangNetw noise ceiling — a sensible model-quality ordering. Full per-layer numbers in `outputs/E002_tuckute_feasibility.json`.

## Interpretation

The headline E001 could never produce: on **real** language-network BOLD, a trained LM's mid-layer representation carries **positive unique contextual variance** that survives length/position/static-embedding subtraction under contiguous splits, while a same-architecture **untrained** network carries **none** (negative across 3 seeds, all models). This is exactly the Feghhi-style discrimination the protocol was built for, and it lands on the right side for every model. The effect is modest in absolute R² (a few percent) but that is the expected scale at ROI level against a 0.35 noise ceiling — the honest denominator is the NC-normalised number (5–10%), not raw R². The trained−untrained gap (+0.030 to +0.050) is the clean signal: it isolates what *language training* adds over architecture + nuisance.

**A2 verdict: PASS on Tuckute.** The alignment signal is real, not nuisance, on real neural data. The charter's gating kill condition is **not** triggered.

**What this licenses:** climbing to **Layer 1** of the R03 ladder (is the signal a *lever* we can move by training — i.e. can we brain-tune a small model and watch unique R² rise?). **What it does NOT license:** any A3 / distillation claim — that preserving the signal *buys* something practical is still untested. **Caveats:** (1) Tuckute is ROI-level (5 dims, coarse); the powered *voxelwise* verdict belongs to LeBel UTS03 (Layer 3, data now staged, adapter pending). (2) Isolated sentences make this a *lower-bound-friendly* test (no temporal-autocorrelation inflation) — a genuine plus for trusting the positive result.
