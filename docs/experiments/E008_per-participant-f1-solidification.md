---
title: "Experiment — E008: in-domain F1 solidification — is the brain-specific gain real ACROSS individual…"
tags: [experiment]
aliases: [E008]
---

# Experiment — E008: in-domain F1 solidification — is the brain-specific gain real ACROSS individual participants?

**Created:** 2026-06-11 · **Status:** COMPLETE (ran 2026-06-11) — per-individual F1 NULL, well-powered (n=9, mean +0.00010, t-CI [−0.0004,+0.0006], power 1.0 at δ=+0.003); E005's +0.0081 = group-averaged-target artifact (L016) · **Mode:** working
**Direction:** Q3/F1 (the in-domain headline). Closes the n=1 pseudo-replication hole the S8 panel found in E005 (L015) **before** any transfer/curve work.
**Predecessors:** [`E005`](E005_alignment-guided-kd-tradeoff.md) (in-domain F1, but "CI excludes 0" was a 15-cell bootstrap over ONE subject-average — L015 honest re-analysis: fold-level t-CI includes 0, median +0.0034, one outlier fold carries 52%) · [`E004`](E004_brain-loss-lever-test.md) (lever, fragile)
**Theory:** [`../06-theory-grounding.md`](../06-theory-grounding.md) §3 (conditional-MI = unique R²)
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

## Results (ran 2026-06-11; 9 UIDs × 5 folds × 3 seeds × 7 conditions = 945 runs; uid 853 excluded)

| Axis | statistic | verdict |
|---|---|---|
| **Subject (n=9)** | mean e_u = **+0.00010**, t-CI95 **[−0.00037, +0.00058]** | **INCLUDES 0**; sign **5/9** (p=0.50) |
| **Fold-clustered (n=5, conservative)** | mean +0.00026, t-CI95 [−0.0004, +0.0009]; bootstrap p(≤0)=0.111 | **INCLUDES 0**; **LOO-fold fails on every drop** |
| Train-4 (848,865,875,876) | mean **−0.00010** (2/4 +) | the subjects E005 averaged → individually null/negative |
| Held-out-5 (797,837,841,856,880) | mean +0.00026 (3/5 +) | INCLUDES 0 |
| SNR control | Spearman(e_u, baseline uR²)=+0.28; drop top-2 SNR → mean +0.00001 | consistent with noise, not signal |
| Null stability | per-cell perm SE 0.00144 ≫ effect 0.00010 | — |

## Verdict: **WEAK / NULL — the in-domain F1 effect does NOT generalize across individual participants** (L016)

The brain-specific gain collapses from E005's averaged **+0.0081** to a per-subject **+0.00010** (~80× smaller, centered at zero). Every predeclared CONFIRM condition fails. The thinking panel (counter-argument + first-principles-grounder, fable) adjudicated the one real interpretive fork and converged:

- **It is a WELL-POWERED null, not a noise-floor null.** Subject-axis MDE(80%) ≈ **+0.0006–0.0013** — 6–12× below E005's +0.0081. A real per-subject effect of that size would have shown as ~9/9 strongly positive (t≈19); instead 5/9, centered at 0, max subject +0.002.
- **E005's +0.0081 was a measurement against the group-AVERAGED target** = the *shared stimulus-evoked response*, inflated ~1.7× by averaging (NC≈0.49 → noise-ceiling math) and ~2.4× by one outlier fold (fold4/seed0 = 52% of E005's signal; L015). The estimand "effect on averaged target" ≠ "mean per-subject effect" (unique-R² doesn't commute with averaging) — both panelists confirmed, and the averaging-SNR steelman (Fork B) was *tested and rejected* by E008's power.
- The 4 subjects E005 literally averaged show **−0.00010** individually — the effect is a property of the average, not those brains.
- Even the averaged-target "brain-specific" is only specific relative to an **incomplete nuisance set** (surprisal/imageability unsubtracted — L011/L012).

**Defensible claim after E008:** *"Alignment-guided KD shows no detectable per-individual brain-specific alignment gain beyond perplexity (n=9, mean +0.0001, 95% CI [−0.0004,+0.0006], well-powered, MDE≈+0.0006); the positive in-domain signal appears only against a multi-subject-averaged target as a higher-SNR measurement of the shared stimulus-evoked response, not per-person brain alignment."* This is a clean, literature-consistent (Hadidi/Feghhi ≤10%) **Fork-B** result.

**Implication:** the thesis's in-domain F1 "headline" (Q3) does not hold at the individual level. The honest contribution becomes (1) A2 (alignment is real & measurable, powered — E006), (2) this **well-powered per-subject null** + the rigorous anti-confound characterization, and (3) **A3** (does any of this buy something practical — E009), now the central open question. The only grounded path to a per-individual positive is higher per-subject SNR (within-subject repeats) or conditioning surprisal/imageability into the nuisance — not more averaging.

## Status

VERDICT RECORDED (NULL, well-powered, panel-adjudicated). **Ladder Q3/F1 flip pending Erfan's confirmation (D015)** — the in-domain F1 downgrades from 🟡 PARTIAL-PASS to a per-subject NULL / averaged-target-only trend. Next: A3 (E009) as the central contribution, gated on Erfan's confirmation of the reframe.


## Related
- [`status.md`](../status.md) — the canonical status board
