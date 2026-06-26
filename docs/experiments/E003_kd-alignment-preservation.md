---
title: "Experiment — E003: does perplexity-only knowledge distillation preserve or destroy brain alignment?…"
tags: [experiment]
aliases: [E003]
---

# Experiment — E003: does perplexity-only knowledge distillation preserve or destroy brain alignment? (R04 Q1 kill-test)

**Created:** 2026-06-10 · **Status:** COMPLETE (ran 2026-06-10) — Q1 PARTIAL: monotone alignment gradient (not preserve-for-free), but alignment co-varies with perplexity (ρ=−0.88), KD-specific shedding only p≈0.1 (L011) · **Mode:** working
**Direction:** `../reports/R04_gap-analysis.md` §6(a) / §8 (Q1) · `../reports/R03_brain-as-training-signal.md` (ladder)
**Theory:** `../06-theory-grounding.md` §2 (data-processing inequality) + §4 (rate–distortion = the F1 trade-off curve)
**Predecessor:** [`E002_tuckute-encoding-feasibility.md`](E002_tuckute-encoding-feasibility.md) (A2 PASS — the encoding signal is real on Tuckute)
**Code:** `scripts/run_kd_alignment.py` (E003 runner), reuses `scripts/distill.py`, `scripts/pilot_lib.py`, `scripts/data_adapters.py:load_tuckute`
**Output:** `outputs/E003_cold.json` + `outputs/E003_warm.json` (+ `.log` each). Provenance sidecars (recomputed 2026-06-17): `outputs/E003_perplexity.json` (reference-arm held-out ppls), `outputs/E003_dissociation.json` (the log-ppl fit + dissociation stats). See "Provenance repair" at the end.

---

## Objective — the single sharpest cheap question on the R04 ladder

R04's structural map (§1) places the thesis (F1) in the empty *shrink × optimize* cell, and §6 factors the sharpest question into a cheap decisive half and a thesis half:

> **6(a) — cheap, decisive, nobody has run it:** Does standard perplexity/logit-only knowledge distillation into a smaller student **preserve** or **destroy** the teacher's brain alignment? [`oota-2026`](../literature/canonical/oota-2026_brain-encoding-scale-compression.md) answered this for quantization and pruning; it is *unmeasured for KD* — a far more destructive transform (KD re-fits a smaller function from scratch, rather than perturbing a fixed function).

This experiment is 6(a). It builds **no** `L_brain` and runs **no** alignment-guided KD — that is 6(b)/E004, and only happens if E003 shows headroom. E003 is pure measurement plus cheap perplexity-only KD runs.

## What E003 actually measures (reframed after adversarial review — see "Review" below)

Two Opus reviews (oracle-reviewer + an independent counter-argument) flagged that a naive "preserve vs destroy" binary **contradicts R04 §4 itself** (compete on the rate–distortion *curve*, not the binary) and that the data-processing inequality (`06` §2) makes "a compressed student loses *some* alignment" near-certain *in the limit* — so the scientific content is **how much**, not **whether**. E003 is therefore framed as a **gap / headroom measurement**:

- The teacher sits at an alignment level $A_T$ (the DPI ceiling a compressed student can inherit).
- Perplexity-only KD lands the student at $A_S \le A_T$.
- The **gap $\Delta = A_T - A_S$ is the headroom** an alignment-guided objective ($\lambda_{\text{brain}}>0$, E004) could recover. It is the vertical distance on the rate–distortion curve (`06` §4) between perplexity-only KD and the loss-free point at the same rate.
- **Large gap** ⇒ KD sheds alignment ⇒ F1 has a confirmed job. **~Zero gap** ⇒ perplexity-only KD is already near the DPI-tight bound ⇒ F1's win would be marginal (it survives only as a trade-off-curve / measurement-rigor note, the way [`oota-2026`](../literature/canonical/oota-2026_brain-encoding-scale-compression.md) complicates the quantization story — *not* a headline).

E003 does **not** by itself kill or confirm F1 (that needs the two-curve comparison in E004). It **sizes the headroom** and answers 6(a).

## The initialization trap (the flaw the review caught — and the fix)

The obvious cheap design — fine-tune a **pretrained** `gpt2` student toward `gpt2-medium` with KD — is a **trap**. E002 already measured pretrained gpt2 at unique R² ≈ +0.020: such a student *starts at full teacher-grade alignment*, so a high retention just means "a few KD epochs didn't erase the alignment it was born with from pretraining." That is fine-tuning drift, not distillation, and it would yield a false "preserve" with ~80% probability. The DPI argument is about a *function fit from scratch* against teacher outputs; warm-start never instantiates that function.

**Fix (locked):** the verdict-bearing arm is a **cold-init (randomly-initialised) gpt2 student trained only via logit-KD** — the only arm where any alignment the student ends with was *transmitted through the KD channel*, not inherited from pretraining. Warm-init KD is kept as a labelled *fine-tuning-drift control*, and a *fine-tune-only (no-teacher)* arm separates corpus-drift from the KD objective.

## Models scored (all on Tuckute, full anti-confound, NC-normalised unique R²)

The **primary verdict comparison is entirely within 12-layer gpt2-architecture models at a fixed layer (L7, E002's gpt2 peak)** — so there is *no* cross-architecture layer confound and *no* winner's-curse layer selection for the comparison that decides the verdict.

| Tag | Model | Role | Init | Layer for verdict |
|---|---|---|---|---|
| **teacher** | gpt2-medium (24L, 355M) | DPI ceiling $A_T$ | pretrained | L14 (matched frac. depth ≈0.58; E002 peak) |
| **gpt2** | gpt2 (12L, 124M) | conventional same-arch reference | pretrained | L7 |
| **kd_cold** | gpt2 ← KD(gpt2-medium) | **THE 6(a) arm** | **random** | L7 |
| **kd_warm** | gpt2 ← KD(gpt2-medium) | fine-tuning-drift control | pretrained | L7 |
| **lmft_warm** | gpt2 ← plain-LM finetune | corpus-drift control (no teacher) | pretrained | L7 |
| **untrained** | gpt2 (random) | floor $A_0$ (≥3 seeds) | random | L7 |
| **distilgpt2** | distilgpt2 (6L, 82M) | FREE real-distillation *context* | distilled-from-gpt2 | L3 (frac. depth ≈0.5) |

Trained arms (`kd_cold`, `kd_warm`, `lmft_warm`) are run over **≥3 seeds** at **matched budget** (same corpus, same optimizer-step count) — single-run would leave a real 50% drop at p≈0.10 (review Objection 3). `distilgpt2` is scored against **gpt2** (its real teacher), never gpt2-medium (lineage-meaningless ratio); it is **context, not the verdict** — it carries a capacity confound (82M/6L vs 124M/12L) and its training included a hidden-state cosine term, so it is *not* perplexity-only and is upper-bound-friendly for retention.

## Claim tuple (predeclared, locked before running)

- **Metric:** NC-normalised unique encoding R² = [R²([len, pos, PCA(static), PCA(context)]) − R²([len, pos, PCA(static)])] / NC, contiguous 5-fold CV, capacity-fair PCA. Identical protocol to E002 (L003 anti-confound). NC(LangNetw) ≈ 0.353.
- **Floor-anchored retention** (the well-conditioned statistic — review Objection 4): $\rho' = \dfrac{A_S - A_0}{A_T - A_0}$, where $A_0$ = untrained floor, $A_T$ = gpt2-medium teacher. Denominator $A_T-A_0 \approx 0.029$ (vs the raw teacher ≈0.019), so it is far better conditioned than the naive ratio, and $\rho'=0$ correctly means "fell back to the floor" = destroyed. Bootstrap the CI over folds×seeds; **decide on $\rho'$ with its CI and on $\Delta=A_T-A_S$ with a paired CI + p — never on a raw point ratio.**
- **Convergence guard:** report each student's **held-out perplexity**. A cold student that never converged (perplexity ≫ teacher's) makes its alignment number *preliminary* (under-training confound, review Objection 5), not a clean verdict.
- **Robustness:** report unique R² at **n_pca ∈ {25, 50, 100}**; the verdict must be stable across PCA rank (else it is a representational-geometry artifact, not brain structure). Report the **full layer sweep**, not only the peak.

### Decision rule (headroom, conditioned on convergence)

Primary read on **`kd_cold`** (the only arm that answers 6(a)); corroborated by `distilgpt2` and interpreted via `kd_warm`/`lmft_warm`.

- **LARGE HEADROOM — KD sheds alignment, F1 has a confirmed job.** `kd_cold` unique-R² CI includes 0 / sits at the floor ($\rho' \le 0.33$) **and** $\Delta=A_T-A_S$ is significant (>2σ). An alignment-guided objective has clear room to recover.
- **SMALL HEADROOM — KD preserves alignment, F1 motivation is weak.** `kd_cold` CI overlaps the teacher ($\rho' \ge 0.80$), $\Delta$ not significant. Perplexity-only KD is already near the DPI-tight bound; F1 survives only as a trade-off-curve / rigor note, not a headline (the [`oota-2026`](../literature/canonical/oota-2026_brain-encoding-scale-compression.md)-complicates-quantization outcome).
- **MODERATE HEADROOM (PARTIAL):** $0.33 < \rho' < 0.80$, $\Delta$ real but modest ⇒ headroom exists but is partial; **triggers confirmation on LeBel UTS03 voxelwise** (Q3, the powered benchmark — Tuckute is ROI-coarse, 5 dims, NC≈0.35, adequate only for a cheap screen).

Negative results count (D007 / charter). A SMALL-HEADROOM verdict is a real, publishable finding that re-weights the thesis, and it ends F1 *as a headline* cheaply — exactly what a kill-test is for.

## Design (locked)

- **Data (alignment):** Tuckute 2024 (`data/tuckute2024/`), 1000 isolated baseline sentences × 5 LH language ROIs, averaged over the 5 train UIDs (848/853/865/875/876). Rows ordered by `item_id` (contiguous-split friendly). Identical to E002.
- **KD corpus:** wikitext-103-raw-v1, split into sentences, **disjoint from Tuckute's sentences** (no train/eval leakage of the stimulus distribution; broad English to minimise domain shift). A held-out slice is reserved for perplexity. Capped to a fixed sentence budget shared by all trained arms.
- **KD objective:** `distill.py` with `lambda_kd=1.0`, `lambda_brain=0`, `lambda_hidden=0` — temperature-scaled (T=2) KL on next-token logits over the shared GPT-2 BPE vocab (token-aligned, no remapping). This is the *purest* perplexity-only KD — purer than distilgpt2 (which adds a hidden-state cosine term that would protect mid-layer structure). `lmft_warm` uses plain causal-LM loss (no teacher).
- **Matched budget:** batch size, max_length, lr, and corpus matched across all trained arms. Compression ratio gpt2-medium→gpt2 ≈ **2.9×**. **Provenance correction (2026-06-17):** the optimizer-step count was *not* identical as-run — `kd_cold` ran 2 epochs (~12k steps), the warm arms (`kd_warm`, `lmft_warm`) 1 epoch (~6k steps) (`config.epochs` in the JSONs). So "matched budget" holds for corpus/batch/lr/architecture but not step count; the cold arm got ~2× the steps. This *strengthens* the under-training caveat — the cold arm reached only ppl 477 *despite* the larger budget — and does not move any alignment number. (R07 still phrases the screen as "matched budget"; that is an analysis-lane wording flagged for Erfan, not edited here.)
- **Anti-confound (mandatory, L003):** contiguous-block CV only; unique variance after length+position+static-embedding subtraction is the only number claimed; untrained same-architecture control over ≥3 seeds; static-nuisance from the frozen reference so it is byte-identical across arms.
- **Stop rule:** fixed model set, fixed layer for the verdict (L7 for all 12L gpt2-arch models), fixed seed count (≥3), fixed step budget. No tuning toward a desired outcome.

## How to run

```bash
cd /home/centcom/data/brain-alignment
export HF_HOME=/home/centcom/data/hf-cache
# one-time corpus fetch (network on; models stay cached/offline):
uv run python scripts/run_kd_alignment.py --prepare-corpus
# the experiment (GPU 0; teacher+student fit easily in 46 GB):
CUDA_VISIBLE_DEVICES=0 uv run python scripts/run_kd_alignment.py --seeds 0 1 2
```

## Results

Ran 2026-06-10 on 4× L40S (cold arm on GPU 0, warm controls on GPU 3, parallel; ~58 min wall). KD corpus = 96k wikitext-103 sentences (2k held out for perplexity), deduped against Tuckute. Trained arms over 3 seeds; references deterministic. The two parallel runs scored the same references on different GPUs and **reproduced them to ~0.0003** — the measurement is stable. Positive controls behave: off-the-shelf gpt2 ≈ teacher (ρ′≈1.0), untrained gpt2 at the floor.

**Headline table** — unique R² at the fixed verdict layer (L7 for 12L gpt2-arch, L14 teacher, L3 distilgpt2), NC-normalised (NC=0.353), floor-anchored retention ρ′=(A−A₀)/(A_T−A₀) with bootstrap 95% CI, Δ=A_T−A_s, p(no-drop)=bootstrap P(no drop from teacher), held-out perplexity.

| Arm | init / objective | unique R² | NC-norm | ρ′ [95% CI] | Δ vs teacher | p(no-drop) | ppl |
|---|---|---|---|---|---|---|---|
| **teacher** gpt2-medium | pretrained | +0.0188 | 0.053 | — | — | — | 74 |
| **gpt2** | pretrained (conventional) | +0.0195 | 0.055 | 1.02 [0.77, 1.27] | ≈0 | 0.57 | 105 |
| **lmft_warm** | warm + plain LM finetune | +0.0174 | 0.049 | 0.95 [0.81, 1.13] | +0.0016 | 0.265 | 44 |
| **kd_warm** | warm + pure logit KD | +0.0144 | 0.041 | 0.84 [0.67, 1.04] | +0.0046 | 0.061 | 95 |
| **distilgpt2** | real distillation (6L/82M, +hidden-cosine) | +0.0076 | 0.021 | 0.60 [0.42, 0.84] | +0.0119 | 0.001 | 169 |
| **kd_cold** | **random + pure logit KD** | +0.0005 | 0.002 | 0.37 [0.14, 0.58] | +0.0181 | 0.000 | 477 |
| **untrained** | random (floor) | −0.0102 | −0.029 | 0 | — | — | ~6×10⁴ † |

(distilgpt2 ρ′ is anchored to its own teacher gpt2, not gpt2-medium.) Raw output: `outputs/E003_cold.json`, `outputs/E003_warm.json`. The four **reference-arm** perplexities (teacher 74, gpt2 105, distilgpt2 169, untrained) were not stored in the original run (`record()` passed `ppl=None` for references); they are recomputed on the original cached held-out slice with the run's own estimator and archived in `outputs/E003_perplexity.json` (teacher 74.0, gpt2 104.9, distilgpt2 169.0 — all match the table within rounding). † untrained ppl is order-of-magnitude only: a random-init net's held-out ppl is large and seed-variable (measured 56k–60k, near the BPE vocab scale |V|=50257), not a stable converged-LM measurement. Trained-arm ppls (477/95/44) were measured in the run.

**The robust finding — a monotone alignment gradient.** Ordered by how much the representation was rebuilt through the KD channel rather than inherited from conventional pretraining: conventional gpt2 (ρ′≈1.0) > warm-KD (0.84) > full distillation distilgpt2 (0.60) > from-scratch cold-KD (0.37) > floor (0). The **rank order is robust to PCA rank** (holds at n_pca ∈ {25,50,100}) even though the absolute magnitudes are not (see below). From-scratch logit KD lands far below the teacher (Δ=+0.018, p<0.001) despite learning language (ppl 50000→477); a real published distillation retains only ~60% of its teacher's alignment above floor (Δ=+0.012, p=0.001). **So the kill-test did *not* return "perplexity-only KD preserves alignment by default"** — the `oota-2026`-style preserve-for-free outcome that would have complicated F1 the way it complicates quantization.

**The over-reach the post-run adversarial review caught — alignment co-varies with perplexity.** The tempting next claim — "KD sheds alignment *beyond* the perplexity it costs" — is **not supported at this benchmark.** Across the five trained/distilled points, alignment is tightly predicted by log-perplexity (Pearson r=−0.88); fitting align = 0.050 − 0.0079·ln(ppl) puts kd_warm **exactly on the line** (residual +0.0001) and leaves off-the-shelf gpt2 as the lone outlier *above* it (+0.006). The two dissociations that would separate "KD-specific shedding" from "alignment tracks LM quality" are both **marginal, not significant**: kd_warm has lower alignment than gpt2 despite better ppl, but bootstrap P(gpt2≤kd_warm)=0.092; and at matched budget lmft_warm beats kd_warm on both ppl and alignment, but P(lmft≤kd_warm)=0.085. Both lean on a single unreplicated gpt2 and (under a paired-fold test) on one fold carrying ~44% of the signal. The cold-arm result is further confounded with **under-training** (ppl 477 ≈ 6.4× the teacher's, ≈4.5× the gpt2 student's) — its near-floor alignment partly just reflects "a worse LM," exactly the convergence-guard caveat the design predeclared. *(These statistics are now archived in `outputs/E003_dissociation.json` (re-derived 2026-06-17): the fit r=−0.88 / slope −0.0079 / intercept 0.050 / residuals and the 44%-fold reproduce; the two P-values reproduce to 0.091/0.083 under a fold×seed bootstrap and are construction-sensitive — a fold-only bootstrap gives ~0.00 — which is itself why this benchmark cannot attribute the gradient to the objective. The within-family r is a **hedge against** the strong claim, not a standalone result: its bootstrap CI is [−1.0, +0.31] and **E015 retired the within-family alignment∝−ppl correlation as layer-unstable noise**, claiming only the cross-family law.)*

**PCA-rank sensitivity (a real caveat on magnitudes).** The absolute unique-R² at the verdict layer declines with PCA rank for every model, and the two confounded arms **flip sign**: kd_cold = +0.009 / −0.004 / −0.010 and distilgpt2 = +0.017 / +0.008 / −0.004 at n_pca = 25 / 50 / 100. The gradient's *ordering* is preserved at every rank, but the quoted shed fractions (16–63%) should be read as rank-dependent, not exact.

## Interpretation

**Verdict (predeclared decision rule): MODERATE / PARTIAL HEADROOM — route to confirmation, do not over-claim.** By the locked rule, kd_cold at ρ′=0.37 (CI [0.14, 0.58]) is in the PARTIAL band (0.33 < ρ′ < 0.80), bordering LARGE; the drop from teacher is highly significant. So the kill-test cleanly rules out the *preserve-for-free* outcome — there is genuine alignment headroom that perplexity-only KD does not recover, growing with compression aggressiveness — **but it does not license "F1 has a confirmed job" as a settled causal claim**, because the headroom co-varies with perplexity and the KD-specific dissociation is only p≈0.1 at this ROI-coarse (5-dim, NC≈0.35) benchmark.

**What this means for F1, stated honestly.** F1 is neither killed nor confirmed by E003. It is *not* in the `oota-2026` trap (alignment is plainly lost under real/aggressive distillation, not preserved by default), so the thesis cell stays open and motivated. But the load-bearing question — *is there alignment recoverable beyond what the perplexity objective already implies?* — is unresolved here. That is the right question for the next experiment, and E003's deflation sharpens its design precisely: **E004 must compare alignment-guided KD (λ_brain>0) against perplexity-only KD at *matched perplexity*, not just matched budget.** If the brain term buys alignment at matched ppl, that is exactly the dissociation E003 could not establish — and it is the only evidence that would convert "headroom" into "confirmed job." Per R04 §4 / `06` §4, F1 still lives on the rate–distortion trade-off curve; E003 shows the perplexity-only curve sits well below the teacher's alignment ceiling under aggressive compression, but cannot yet attribute that gap to the compression *objective* rather than to LM quality.

**What licenses the next steps (two confirmations the design predeclared for a PARTIAL outcome):**
1. **A converged cold arm** — re-run from-scratch logit KD to *matched perplexity* (not just matched step budget), to de-confound under-training from alignment shedding. Cheap follow-up; needs more KD compute or a smaller perplexity target.
2. **LeBel UTS03 voxelwise** — the powered benchmark (thousands of voxels vs 5 ROIs) where a real ~0.005 gap is detectable; Tuckute is adequate only as a screen. Adapter is the pending Layer-3 work.
3. **E004 itself** (alignment-guided KD vs perplexity-only KD at matched perplexity) is the experiment that actually tests F1.

**Caveats carried forward:** ROI-coarse benchmark (screen, not powered); cold arm under-trained (ppl ≈6.4× teacher) and run at ~2× the warm arms' step budget (still only reached ppl 477); distilgpt2 carries capacity + hidden-cosine confounds (so its retention is upper-bound-friendly); absolute magnitudes are PCA-rank-sensitive (ordering is not). Negative/qualified results count (charter, D007) — the kill-test did its job: it eliminated both the naive "F1 confirmed" over-read and the "F1 dead (preserve-by-default)" outcome, leaving one precise, well-scoped next experiment.

## Post-run review (adversarial, integrated above)

An Opus skeptic was tasked to *refute* the preliminary "F1 confirmed" read and succeeded on the causal claim: verified P(gpt2≤kd_warm)=0.092 (not significant), the r=−0.88 log-ppl fit with kd_warm on the line and gpt2 the outlier, the kd_cold/distilgpt2 PCA sign-flips, and that dropping the two confounded arms leaves no significant shed. Its verdict — "NEEDS-SOFTENING: the data support 'perplexity-only KD from scratch lands below teacher alignment, and alignment tracks LM quality,' but not 'KD sheds alignment beyond ppl'" — is adopted as the verdict above. What survives its attack: the from-scratch sub-teacher result (Δ=0.018, p<0.001, though under-training-confounded), the PCA-robust gradient *ordering*, the floor-anchored fixed-layer design, and cross-GPU reproducibility (~0.0003).

## Review (adversarial, pre-run — integrated into the locked design above)

Two Opus reviews stress-tested the draft before compute. Both independently identified the **initialization trap** as near-fatal (warm-init can only show drift, not distillation) → fixed by the **cold-init arm**. Both flagged the **binary-vs-curve** framing as contradicting R04 §4 → fixed by reframing E003 as **headroom/gap measurement**, with the F1 verdict deferred to the E004 two-curve comparison. Both quantified **underpower** (a 50% drop at p≈0.10 single-run) → fixed by **≥3 seeds** on verdict arms. Both showed the **raw ratio ρ is ill-conditioned** near the cutoffs → fixed by the **floor-anchored ρ′ with bootstrap CI**, deciding on Δ. Additional fixes: distilgpt2 scored vs gpt2 (correct lineage) and demoted to context; perplexity reported (convergence guard); fixed-layer verdict (no winner's curse) + PCA-rank robustness. Verdict after fixes: the design can give a trustworthy *gap* read for a clean preserve or a clean destroy; a PARTIAL outcome is the expected hard case and routes to LeBel voxelwise.

## Provenance repair (2026-06-17) — no science changed

A provenance audit (R07 review panel, then a counter-argument / premortem / first-principles / socratic panel) found four record gaps and one undocumented design fact. All were repaired **provenance-only**: every unique-R²/ρ′/Δ/CI/p value and the PARTIAL verdict are byte-identical before and after.

1. **Reference-arm ppls were unsourced** (`perplexity: null` in both run JSONs). Recomputed on the original cached held-out slice (`data/kd_corpus/wikitext103_sentences_heldout.txt`) with the run's own estimator (`scripts/recompute_e003_reference_ppl.py` → `outputs/E003_perplexity.json`): teacher 74.0, gpt2 104.9, distilgpt2 169.0 — all match the table within rounding, confirming they *were* on-slice measurements just never written to the JSON. untrained relabelled order-of-magnitude (~6×10⁴, seed-variable).
2. **Dissociation stats were prose-only.** Re-derived and archived (`scripts/reanalyze_e003_dissociation.py` → `outputs/E003_dissociation.json`): the r=−0.88 fit, slope, intercept, residuals and 44%-fold reproduce; the P-values reproduce (0.091/0.083) under a fold×seed bootstrap and are flagged construction-sensitive. The within-family r is archived as a hedge with its wide CI and an E015 forward-pointer, not promoted to a result.
3. **Dead `Output:` pointer** fixed to the real files (top of doc).
4. **"4.5× the teacher" mislabel** corrected to "≈6.4× the teacher (≈4.5× the gpt2 student)" here and in L011.
5. **Step-budget asymmetry** (cold 2 epochs vs warm 1) recorded in the Design "Matched budget" bullet; R07's "matched budget" wording flagged for an analysis-lane review (not edited).

The estimator note for both sidecars: single-window, `max_length=64`, no sliding-window stride — matched to the trained arms, so cross-arm ratios and the log-ppl fit are coherent.


## Related
- [`ladder.md`](../ladder.md) — the canonical status board
- [`map.md`](../map.md) — code system (Q/E/A/D/L) & journey map
