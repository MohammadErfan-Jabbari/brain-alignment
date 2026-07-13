---
title: "Experiment — E001 toy brain-alignment distillation pilot (GPT-2 medium → small)"
tags: [experiment]
aliases: [E001]
---

# Experiment — E001 toy brain-alignment distillation pilot (GPT-2 medium → small)

**Created:** 2026-06-09 · **Status:** done (scaffold + synthetic smoke; real-data run pending)
**Hypothesis:** [`../hypotheses/H001_alignment-guided-distillation.md`](../hypotheses/H001_alignment-guided-distillation.md) · **Mode:** exploratory
**Code:** `scripts/{pilot_lib,distill,data_adapters,run_toy_pilot}.py`, `configs/toy_pilot.json`,
`scripts/AGENTS.md`

---

## Objective

Decide whether the **pipeline** for the make-or-break feasibility test is sound, and whether adding a
brain-alignment loss to GPT-2-medium → GPT-2 distillation changes the student's encoding-model fit to
fMRI under the anti-confound protocol. Tonight: build the harness and validate it; the real scientific
verdict waits on neural data.

## Claim tuple (from H001)

- **Metric:** unique encoding R² (contextual variance after nuisance subtraction).
- **Threshold:** brain arm beats matched-budget perplexity-only KD by ≥ +0.05 (thesis-level win).
- **Baseline:** identical distillation with `lambda_brain = 0` (brain-blind KD).
- **Condition:** matched data, epochs, lr, KD weight; contiguous splits; ≥ 3 seeds.

## What was actually run vs scaffolded

- **Scaffolded + validated:** the full pipeline — distillation (logit-KD + brain-head loss), hidden-state
  extraction, ridge encoding, scalar + static nuisance baselines, capacity-fair variance partition,
  contiguous block CV, ≥3-seed paired reporting. Smoke test + full 3-seed run both pass on GPU.
- **Real data path:** **NOT run on real fMRI.** The chosen plumbing benchmark (Pereira, OSF crwz7)
  ships only stimulus sentences, not neural responses (see [`../04-data-benchmarks.md`](../04-data-benchmarks.md)). So the run used
  the **hybrid path: real Pereira sentences + synthetic fMRI** (a known-structure stand-in built from
  teacher features + length/position confound + noise). **A synthetic result tests plumbing, not science.**

## Design (locked before running)

- **Models / data:** teacher `gpt2-medium`, student `gpt2` (both HF-cached). Stimuli: 384 real Pereira
  Exp-2 sentences (`data/pereira/Pereira_Materials/stimuli_384sentences.txt`, CC-BY, downloaded from
  OSF crwz7, no login). fMRI: synthetic (200 voxels; signal 1.0 / nuisance 0.7 / noise 1.0).
- **Baselines:** brain-blind KD (`lambda_brain=0`) vs brain KD (`lambda_brain>0`); identical data,
  3 epochs, lr 5e-5, KD weight 1.0, temperature 2.0 — matched budget, only the brain term differs.
- **Metrics:** raw encoding R² and **unique R²** = R²([length,position,PCA(static),PCA(context)]) −
  R²([length,position,PCA(static)]); reported as paired Δ across seeds.
- **Seeds:** 0, 1, 2 (canonical); λ-sweep at seed 0.
- **Confound controls:** contiguous train/eval split (last 30% held out from the brain loss entirely);
  contiguous 5-fold CV within the eval block; nuisance = length + position + static (non-contextual)
  embeddings; static + contextual PCA-reduced to equal rank (50) for a capacity-fair partition.
- **Stop rule / budget:** toy scale, < ~10 min total on one L40S. No long training, no large downloads.
- **Promotable vs exploratory:** exploratory only. No claim about the thesis can rest on synthetic fMRI.

## How to run

```bash
cd /home/centcom/data/brain-alignment
export HF_HOME=/home/centcom/data/hf-cache
uv run python scripts/run_toy_pilot.py --config configs/toy_pilot.json            # 3-seed hybrid
uv run python scripts/run_toy_pilot.py --config configs/toy_pilot.json --smoke    # fast pipeline check
uv run python scripts/run_toy_pilot.py --config configs/toy_pilot.json --backend pereira \
    --data-dir data/pereira/<neural>                                              # real data (tomorrow)
```

## Iteration log

| Date | Run / seed | Config | Result (unique R²) | Observation | Next |
|---|---|---|---|---|---|
| 2026-06-09 | smoke, seed 0 | 64 sents, 40 vox | runs; numbers noisy (eval=19) | pipeline OK end-to-end | scale up |
| 2026-06-09 | full, seeds 0-2 | 240 sents (dup-key bug) | base 0.0169 / brain 0.0112 | found JSON dup `n_items` | fix config |
| 2026-06-09 | **canonical, seeds 0-2** | **384 sents, λ=1.0** | **base 0.0265±0.0007 / brain 0.0254±0.0010** | clean; teacher 0.0424 > students | sweep λ |
| 2026-06-09 | sweep, seed 0 | λ ∈ {0.1, 0.5, 5.0} | Δ = −0.0004 / −0.0010 / −0.0069 | monotonic degradation in λ | real data |

## Results (canonical, synthetic fMRI — PLUMBING ONLY)

| Arm | unique R² (mean ± sd, n=3) |
|---|---|
| teacher (gpt2-medium, reference) | 0.0424 |
| untrained student (gpt2) | 0.0270 |
| **baseline KD** (`λ_brain=0`) | **0.0265 ± 0.0007** |
| **brain KD** (`λ_brain=1`) | **0.0254 ± 0.0010** |
| **Δ (brain − baseline), paired** | **−0.0011 ± 0.0007** |

λ-sweep (seed 0): Δ(unique R²) = −0.0004 (0.1), −0.0010 (0.5), −0.0069 (5.0). Monotonic.
Nuisance-alone R² ≈ 0.006 (the partition is clean: nuisance explains little of this synthetic signal).
Raw vs unique behave sanely; teacher > student ordering holds.

## Interpretation

**What this licenses.** The harness is real and trustworthy: it runs GPT-2-medium → GPT-2 distillation
with both arms at matched budget, extracts hidden states, fits encoding models with the full Feghhi/L003
anti-confound protocol (contiguous CV, nuisance baselines, capacity-fair variance partition), reports
≥3-seed paired deltas, and is one config swap from real neural responses. It produces sensible,
reproducible, low-variance numbers and the expected teacher > student ordering.

**What it does NOT license.** Nothing about the thesis. On synthetic fMRI the "brain signal" is by
construction a linear function of the *teacher's* features, so plain KD (which pulls the student toward
the teacher) is already near-optimal for preserving it, and a separate student→fMRI head can only
distract — hence the small, monotonic-in-λ *negative* Δ. This is the mechanistically expected outcome
and is **not evidence against H001**; it is evidence the plumbing and the anti-confound machinery work
and do not rubber-stamp the brain loss. The real test needs neural data whose brain-predictive structure
is *not* trivially a function of teacher features (LeBel `ds003020`).

**Design lessons for the real run.** (1) The static-embedding nuisance must be PCA-matched to the
contextual block or it unfairly absorbs the signal — fixed here. (2) On real data, consider a frozen
teacher-encoding-map loss or a CKA proxy rather than a trainable head, since the head overfits the train
block (this was the then-open `L_brain` design decision, later resolved by the subsequent E records). (3) Keep λ modest; large λ degrades.

Hypothesis status: **H001 remains untested** (synthetic cannot test it). Learning recorded as L004.


## Related
- [`status.md`](../status.md) — the canonical status board
