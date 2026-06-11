# Experiment — E008: in-domain F1 solidification — is the brain-specific gain real ACROSS individual participants?

**Created:** 2026-06-11 · **Status:** DESIGN (pre-lock; oracle review pending) · **Mode:** working
**Direction:** L3/F1 (the in-domain headline). Closes the n=1 pseudo-replication hole the S8 panel found in E005 (L015) **before** any transfer/curve work.
**Predecessors:** `E005` (in-domain F1, but "CI excludes 0" was a 15-cell bootstrap over ONE subject-average — L015 honest re-analysis: fold-level t-CI includes 0, median +0.0034, one outlier fold carries 52%) · `E004` (lever, fragile)
**Theory:** `../06-theory-grounding.md` §3 (conditional-MI = unique R²)
**Code:** extends `scripts/run_brain_lever.py` (add `--uids` per-subject loop + n_perm null + across-subject inference)
**Output:** `outputs/E008_per_participant_Qwen.json`

---

## The question

> Does the brain-specific, perplexity-independent alignment gain from alignment-guided KD
> (paired `kd_brain − kd_brain_permuted` at matched perplexity) hold **across individual
> participants**, treating each participant as an independent replication unit — rather than only
> in the 5-UID *average* on which E005 was run?

**Why this, why now (lowest-layer-first).** The S8 panel (counter-argument) showed E005's headline rests
on pseudo-replication: 15 cells = 3 seeds × 5 folds, all from **one** 5-UID-averaged target on the same
1000 sentences. The legitimate independent replication unit is the **participant**, and Tuckute ships
**10 participants** (UIDs 797, 837, 841, 848, 853, 856, 865, 875, 876, 880), each with all 1000 sentences
× the 5 LH-language sub-ROIs. Running per-participant converts "n=1, pseudo-replicated 15×" into "n=10
independent brains" — a genuine power gain *and* a stronger claim (generalization across people, the
thing a reviewer actually cares about), in-domain and cheap. It must hold here before transfer/curve work
is worth any compute.

## Arms (per participant)

| Arm | Objective | Brain target |
|---|---|---|
| **kd_brain** (`mse`) | `λ_kd·KL(student‖teacher) + λ_brain·MSE(W·hₛ, fMRI)` | that participant's real BOLD (5 ROIs) |
| **kd_brain_permuted** (`mse_perm`) | same objective, block-permuted BOLD | matched-ppl null; **n_perm ≥ 3** draws per (fold,seed) to de-noise the null (fixes E005's `n_perm=1`, L015) |
| **kd_ppl** (`lm_only`) | `λ_kd·KL` only | none (secondary "beyond-KD" reference; ppl-unmatched) |

Teacher Qwen2.5-1.5B → student Qwen2.5-0.5B (LoRA, KD-KL retention) — the E005 lineage. λ_brain=10, KD corpus + ppl-heldout as E005. Verdict layer L12.

## The inference design (the load-bearing change — L015)

- **Per participant** u: run 5 rotating contiguous folds × 2 seeds; within each (fold,seed) form the paired
  contrast `Δ_brain − mean_over_perm(Δ_brain_permuted)` (base cancels; matched ppl by construction since the
  twin shares the KD+MSE objective). Average over folds×seeds → **one effect estimate per participant** `e_u`.
- **Across participants (the honest unit, n=10):** report `mean(e_u)` with a **t-CI95 (df=9)**, a **sign test**
  (binomial on #{e_u>0}), and a **Wilcoxon signed-rank**. Also **leave-one-participant-out** and the
  **median** (the f4-outlier lesson: never let one unit carry the verdict).

## Claim tuple / decision rule (PREDECLARED, before running)

- **Metric:** across-participant mean of the per-participant paired effect `e_u = mean_{fold,seed}(Δ_mse − Δ_mse_perm)`, unique-R² units; n=10 participants the inference unit.
- **F1 in-domain CONFIRMED (cross-subject):** `mean(e_u) > 0` with **t-CI95 (df=9) excluding 0**, AND **≥ 8/10 participants positive** (sign test one-sided p ≈ 0.055), AND the verdict survives leave-one-participant-out (no single subject flips it). → in-domain F1 generalizes across individuals; *then* transfer/curve work is licensed.
- **F1 in-domain WEAK/AVERAGE-ONLY (the L015-honest null):** t-CI includes 0 OR < 7/10 positive OR one subject carries it. → the effect is an average-only/borderline trend, not a cross-subject result; do **not** claim in-domain generalization; pivot effort to A3 (does any of this buy something practical) and report this honestly (Fork-B-consistent).
- **Anti-confound (mandatory, unchanged from E002/E004):** rotating contiguous folds (no tune↔eval leakage), input embeddings frozen (LoRA), static nuisance S + scalar nuisance Z from the UNTUNED base byte-identical across arms, the permuted twin as the matched-ppl brain-specificity null. Report per-arm perplexity (the matched axis) and the A/B imageability/surprisal balance per fold.
- **Power note (required before lock):** with n=10 and E005's per-fold sd ≈ 0.009, the across-participant SE depends on between-subject variance (unknown until run). Predeclare: if the observed between-subject sd inflates the MDE above the effect, report the result as power-limited rather than over-reading a null. (The MDE will be computed from the run's own between-subject variance and reported, à la E006.)

## Open design questions (resolve at oracle review)

- **2 seeds vs 3:** with participants as the new replication axis, 2 seeds × 5 folds = 10 within-subject samples/condition is likely adequate; oracle to confirm vs the compute cost.
- **n_perm:** 3 (compute) vs 5 (cleaner null). Default 3; bump if the null is still noisy.
- **All 10 vs 5-train-UIDs first:** stage? Run all 10 in one job (GPUs free) is cleaner for the n=10 claim; a 5-train-UID first pass is the cheaper smoke. Lean: smoke on 2 UIDs, then all 10.
- **Per-subject NC normalization:** the NC file has per-UID ceilings; verdict is on raw Δ (NC for display only), so use the matched-NC mean as in E005 unless oracle wants per-subject.

## Compute

10 participants × 5 folds × 2 seeds × (mse 1 + mse_perm 3 + lm_only 1 = 5 conditions) ≈ 500 LoRA tunes of a 0.5B student (~30–50 s each incl. teacher KD forward + scoring). ~1.5 h split across the 4 L40S by participant. Pure in-domain; no new data.

## How to run (after oracle PASS + harness extension)

```bash
export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1
CUDA_VISIBLE_DEVICES=0 uv run python scripts/run_brain_lever.py \
  --model Qwen/Qwen2.5-0.5B --kd-teacher Qwen/Qwen2.5-1.5B \
  --arms mse lm_only --permute-kinds mse --uids 797 837 841 848 853 856 865 875 876 880 \
  --seeds 0 1 --folds 5 --lambda-grid 10 --n-perm 3 --out outputs/E008_per_participant_Qwen.json
```

## Status

DESIGN — pending oracle-reviewer PASS, then the `--uids` harness extension, then run, then the S8 thinking panel on the result. Predeclared kill/confirm rule above is the lock.
