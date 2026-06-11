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
| **kd_brain_permuted** (`mse_perm`) | same objective, block-permuted BOLD | matched-ppl null; **n_perm = 5** draws per (fold,seed); verdict subtracts the per-cell perm **mean** (fixes E005's `n_perm=1`, L015; oracle #4) |
| **kd_ppl** (`lm_only`) | `λ_kd·KL` only | none (secondary "beyond-KD" reference; ppl-unmatched) |

Teacher Qwen2.5-1.5B → student Qwen2.5-0.5B (LoRA, KD-KL retention) — the E005 lineage. λ_brain=10, KD corpus + ppl-heldout as E005. Verdict layer L12.

## The inference design (the load-bearing change — L015, hardened by oracle HOLD)

**The oracle's correct objection:** per-participant alone does NOT remove pseudo-replication — all 10
participants see the **same 1000 sentences** on the **same 5-fold partition**, so the per-subject effects
are positively correlated (shared stimuli), not independent. A fold-4-type spike (E005 proved the
real−permuted pairing does *not* fully cancel it: fold4/seed0 real=0.073, perm=0.010) would appear
**correlated across many "independent" brains** → a naive n=10 t-CI is anti-conservative and would read
"robust 9/10" for what is one lucky stimulus fold replicated 10×. So the inference is **crossed** over
two axes (subjects AND stimulus-folds), and the verdict must survive BOTH.

- **Per cell** (subject u, fold k, seed s): paired diff `d[u,k,s] = uR²_mse − mean_{p=1..5}(uR²_mse_perm)`
  (base cancels; matched ppl by construction; per-cell perm **mean** subtracted — de-noised).
- **Per participant:** `e_u = median_{k,s} d[u,k,s]` (robust within-subject aggregate — the f4-outlier
  lesson; report the mean too). 3 seeds × 5 folds = 15 cells per subject.
- **Subject-axis inference (n=10):** `mean(e_u)` with t-CI95 (df=9), sign test (binomial on #{e_u>0}),
  Wilcoxon. **Leave-one-participant-out:** require the sign of `mean(e_u)` stays positive for all 10 drops.
- **Fold-axis inference (n=5, the CONSERVATIVE headline — oracle #1,#2):** per-fold-across-subjects value
  `f_k = mean_{u,s} d[u,k,s]` → 5 fold values → t-CI95 (df=4) + cluster-bootstrap over folds.
  **Leave-one-fold-out:** drop each fold, recompute `mean(e_u)`; require the fold-clustered CI still
  excludes 0. This is the gate that catches a shared-stimulus spike (LOO-subject cannot).
- **Report the MORE CONSERVATIVE of the subject-CI and fold-CI as the headline** (never the df=9 t-CI alone).
- **Train vs held-out split (oracle #3):** report `mean(e_u)` separately for the **train-5** UIDs
  (848,853,865,875,876 — the subjects E005 averaged, i.e. data reuse) and the **held-out-5** UIDs
  (797,837,841,856,880 — genuine out-of-sample brains). Generalization requires the held-out-5 to show it too.
- **SNR control (oracle #5):** Spearman `e_u` vs per-subject baseline uR² (signal proxy). If positively
  rank-correlated and `mean(e_u)` collapses when the top-SNR subjects are dropped → SNR artifact, not
  brain-specificity.
- **Null-stability check:** report the per-cell perm SE; if not ≪ the effect, treat the verdict as
  null-noise-limited (don't over-read).

## Claim tuple / decision rule (PREDECLARED, before running)

- **Metric:** across-participant mean of the per-participant paired effect `e_u = mean_{fold,seed}(Δ_mse − Δ_mse_perm)`, unique-R² units; n=10 participants the inference unit.
- **F1 in-domain CONFIRMED (cross-subject):** the **conservative (fold-clustered) CI excludes 0** AND it **survives leave-one-fold-out** (no single shared stimulus fold carries it) AND **≥ 8/10 participants positive** (sign test one-sided p≈0.055) survives leave-one-participant-out AND the **held-out-5 UIDs also show mean(e_u)>0** AND it is not an SNR artifact. → in-domain F1 generalizes across individuals and stimulus folds; *then* transfer/curve work is licensed.
- **F1 in-domain WEAK/AVERAGE-ONLY (the L015-honest null):** the fold-clustered CI includes 0, OR LOO-fold flips it, OR **≤ 7/10** positive, OR held-out-5 null while train-5 positive (data reuse), OR e_u tracks SNR. → an average-only/fold-limited trend, not a cross-subject result; do **not** claim in-domain generalization; report honestly (Fork-B-consistent) and pivot effort to **A3** (does any of this buy something practical — the escape from the stimulus-fold power ceiling).
- **KILL the in-domain F1 line** if ≥2 of: LOO-fold collapses the conservative CI to include 0 (one shared fold carries it, like E005); held-out-5 null while train-5 positive; e_u rank-correlates with SNR and collapses when top-SNR subjects removed.
- **Anti-confound (mandatory, unchanged from E002/E004):** rotating contiguous folds (no tune↔eval leakage), input embeddings frozen (LoRA), static nuisance S + scalar nuisance Z from the UNTUNED base byte-identical across arms, the permuted twin as the matched-ppl brain-specificity null. Report per-arm perplexity (the matched axis) and the A/B imageability/surprisal balance per fold.
- **Power note (required before lock):** with n=10 and E005's per-fold sd ≈ 0.009, the across-participant SE depends on between-subject variance (unknown until run). Predeclare: if the observed between-subject sd inflates the MDE above the effect, report the result as power-limited rather than over-reading a null. (The MDE will be computed from the run's own between-subject variance and reported, à la E006.)

## Resolved at oracle review (HOLD → addressed)

- **Seeds = 3** (not 2): per-subject targets are noisier than the 5-UID average → keep the within-subject sample count up + use the robust median e_u (oracle #2/#4).
- **n_perm = 5**, subtract per-cell perm mean, report null SE (oracle #4).
- **Inference is crossed** (subject AND fold); the fold-clustered CI + LOO-fold is the conservative headline (oracle #1/#2). The df=9 subject t-CI is never reported alone.
- **Train-5 vs held-out-5 reported separately** (oracle #3). NC normalization: raw Δ (NC display only) + the SNR rank-correlation control replaces per-subject NC-norm, which is blocked (the NC file covers only the 5 train UIDs; no within-subject repeats).
- **Stage:** 2-UID smoke first (sanity + timing), then all 10 in one job (GPUs free).

## Compute

10 participants × 5 folds × 3 seeds × (mse 1 + mse_perm 5 + lm_only 1 = 7 conditions) ≈ 1050 LoRA tunes of a 0.5B student (~30–50 s each incl. teacher KD forward + scoring). ~2.5–3 h split across the 4 L40S by participant. Pure in-domain; no new data.

## How to run (oracle HOLD addressed; harness extension `--uids` + crossed inference)

```bash
export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1
# smoke (2 UIDs, fast):
CUDA_VISIBLE_DEVICES=0 uv run python scripts/run_brain_lever.py \
  --model Qwen/Qwen2.5-0.5B --kd-teacher Qwen/Qwen2.5-1.5B \
  --arms mse lm_only --permute-kinds mse --uids 848 797 \
  --seeds 0 1 2 --folds 5 --lambda-grid 10 --n-perm 5 --out outputs/E008_smoke.json
# full (all 10 UIDs; split across GPUs by UID subset if desired):
CUDA_VISIBLE_DEVICES=0 uv run python scripts/run_brain_lever.py \
  --model Qwen/Qwen2.5-0.5B --kd-teacher Qwen/Qwen2.5-1.5B \
  --arms mse lm_only --permute-kinds mse --uids 797 837 841 848 853 856 865 875 876 880 \
  --seeds 0 1 2 --folds 5 --lambda-grid 10 --n-perm 5 --out outputs/E008_per_participant_Qwen.json
```

## Iteration log

| Date | Step | Result | Next |
|---|---|---|---|
| 2026-06-11 | design v1 | per-participant, n=10, t-CI(df=9) | oracle review |
| 2026-06-11 | **oracle HOLD** | shared-stimulus pseudo-replication NOT fixed by per-subject alone; need LOO-fold + fold-clustered CI + train/held-out split + 3 seeds + n_perm≥5 + SNR control | addressed above → harness extension → run |
| 2026-06-11 | data note | **uid 853 EXCLUDED** — 60 NaNs (incomplete 5-ROI coverage); the other 9 UIDs are complete. **n=9** (train-4: 848,865,875,876; held-out-5: 797,837,841,856,880). | run on 9 UIDs, 4-GPU split |
| 2026-06-11 | smoke PASS | 2-UID plumbing (limit-tune=64): per-UID loop + analyzer end-to-end OK (`outputs/E008_plumbing_smoke.json`) | full run launched (4 GPUs) |

## Status

RUNNING (2026-06-11, 4-GPU split over 9 UIDs; uid 853 excluded). Shards: `outputs/E008_g{0,1,2,3}.json`
(g0=797,837,841 · g1=848,856 · g2=865,875 · g3=876,880). Harness extension + smoke + analyzer all PASS.

**To finish (merge → verdict → panel):**
```bash
uv run python scripts/analyze_e008.py outputs/E008_g0.json outputs/E008_g1.json outputs/E008_g2.json outputs/E008_g3.json
```
Then run the thinking panel (counter-argument + premortem) on the printed verdict, address holes, record
the verdict here + in gbrain, and bring it (with the E005 L3/F1 downgrade) to Erfan for the ladder flip (D015).
**Predeclared rule (the lock):** CONFIRMED iff the conservative fold-clustered CI excludes 0 AND survives
LOO-fold AND ≥8/9 sign AND held-out-5 mean>0 AND not an SNR artifact; else WEAK/average-only (Fork-B-honest).
