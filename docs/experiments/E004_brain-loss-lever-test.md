---
title: "Experiment — E004: is `$\mathcal{L}_{\text{brain}}$` a usable *lever*? (R03 Q2) + the D010…"
tags: [experiment]
aliases: [E004]
---

# Experiment — E004: is `$\mathcal{L}_{\text{brain}}$` a usable *lever*? (R03 Q2) + the D010 loss-form resolution

**Created:** 2026-06-10 · **Re-locked:** 2026-06-11 (after oracle-reviewer HOLD → design reshaped) · **Status:** COMPLETE (ran 2026-06-11) — Q2 verdict **REVISED S25 (2026-06-19, Erfan-confirmed): NO DEMONSTRATED LEVER** (was "🟡 PARTIAL — fragile lever"). The headline +0.0032 [+0.0006,+0.0058] ("excludes 0") was a **15-cell pseudo-replicated bootstrap** (3 seeds × 5 folds as 15 independent — the L015 error the project fixed for E005 but never applied here); at the honest n=5-fold unit t-CI = **[−0.0023,+0.0086] includes 0**, fold-4 carries **64%** (LOFO-f4 → +0.0014), `beats_permuted_null=False`. → no valid-unit evidence the loss moves held-out alignment. **Caveat: n=5 underpowered to exclude a small (~+0.003) lever → "undemonstrated," NOT "proven zero."** Still perplexity-entangled (L011/L012). See the S25 recompute note at the bottom. · **Mode:** working
**Direction:** Q2 lever test; current interpretation is in the [extended manuscript](../manuscript/extended/main-extended.tex) and [`status.md`](../status.md).
**Theory:** [`../06-theory-grounding.md`](../06-theory-grounding.md) §1 (MI gen-bound), §2 (DPI ceiling), §3 (conditional MI = unique R²)
**Predecessors:** [`E002`](E002_tuckute-encoding-feasibility.md) (A2 PASS — encoding signal is real on Tuckute) · [`E003`](E003_kd-alignment-preservation.md) (Q1 PARTIAL — KD lands below teacher, alignment co-varies with ppl, L011)
**Resolves:** decision **D010** (the form of `$\mathcal{L}_{\text{brain}}$`) — empirically, on real neural data.
**Code:** `scripts/run_brain_lever.py` (runner), `scripts/brain_loss.py` (loss family), `scripts/pilot_lib.py`, `scripts/data_adapters.py:load_tuckute`
**Output:** `outputs/E004_brain_lever.json`

---

## Objective — the kill-gate for the whole thesis below it

The ladder's Q2: **is the brain-alignment signal a *lever* we can move by optimizing it, or only a property we can *measure*?**

> When we fine-tune a small LM with a differentiable brain-alignment loss `$\mathcal{L}_{\text{brain}}$` on held-in stimuli, does its **held-out** unique encoding R² (on stimuli it was never tuned on) *rise* above the untuned model — under the E002 anti-confound protocol — and does that rise survive the controls that separate "the brain objective worked" from "any fine-tune / domain-adaptation would have done it"?

If yes → Q2 PASS, and we have the loss form for E005 (the headline alignment-guided-KD experiment). If a confident no on the powered benchmark → the signal is measurement-only and F1 dies (reframe to measurement rigor, charter). This experiment also **resolves D010**: D010's three candidate forms are run head-to-head on real Tuckute data; the lever effect + the controls pick the winner.

## Grounding (what the literature + theory dictate)

- **Metric = conditional MI.** `06` §3: unique R² beyond nuisance *is* $I(\text{LM};B\mid\text{nuisance})$. The lever must move *that* (nuisance-subtracted, contiguous-split), not raw R².
- **MSE/ridge encoding loss is theory-preferred.** `06` §3 + Prob-ML block: under a Gaussian-linear model, maximizing $I(\text{LM};B\mid\text{nuisance})$ *is* minimizing the squared error of a linear LM→B map after partialling nuisance — the differentiable twin of the eval metric ("optimize what you measure"). → **`mse` is the predeclared primary confirmatory loss form.**
- **Text-LM brain-tuning precedents:** bilgin-2026 (cosine + CE, co-trained ridge readout, LoRA on late layers, adaptive weight) and merlin-2026 (negative-squared-Pearson + CE). Speech (moussa-2025/b) uses **L2/MSE** and ablates L2 vs correlation vs cosine — **L2 best at scale, correlation best at small data**. Tuckute's tune block is *small*, so cos/pearson are live contenders → run as exploratory.
- **Nobody freezes the readout; nobody uses CKA to brain-tune a text LM.** So `frozen` and `cka` are genuine design probes, flagged as deviations. CKA is rotation/scale-invariant (a model can satisfy it by rotating) and pirlot-2022's shuffled-label control nearly matched real data for a geometric loss → **`cka` is treated as a negative-control-ish probe: a `cka` "pass" LOWERS, not raises, confidence that the lever reads brain-specific structure.**
- **DPI ceiling** (`06` §2): achievable alignment is bounded by training-data+architecture; we report the strongest reference for context but measure the lever against the *same-model untuned* base.

## Candidate loss family (the D010 contenders) — `scripts/brain_loss.py`

`h` = masked-mean pool of the model's verdict-layer hidden state; `W` = linear readout to the 5 ROIs; `B` = Tuckute BOLD. Every brain arm also carries an LM-retention CE term on the same block-A text.

| Arm | `$\mathcal{L}_{\text{brain}}$` | Readout | Lineage | Role |
|---|---|---|---|---|
| **`mse`** | $\lVert W h - B\rVert^2$ | co-trained | moussa L2 / theory-preferred | **PRIMARY confirmatory — decides the verdict alone** |
| `cos` | $1-\cos(Wh,B)$ | co-trained | bilgin-2026 | exploratory (small-data contender) |
| `pearson` | $-\,\overline{r(Wh,B)^2}$ | co-trained | merlin-2026 / moussa small-data winner | exploratory |
| `frozen` | $\lVert W_0 h - B\rVert^2$, $W_0$=ridge on untuned features, frozen | frozen | D010 option (b); no precedent | exploratory (deviation probe) |
| `cka` | $1-\text{linearCKA}(h,B)$ | none | D010 option (c) | exploratory **negative-control-ish** |

`$\mathcal{L} = \lambda_{\text{brain}}\,\mathcal{L}_{\text{brain}} + \lambda_{\text{lm}}\,\mathrm{CE}(\text{block-A text})$`, `$\lambda_{\text{lm}}=1$`. **`mse` verdict at `$\lambda_{\text{brain}}=10$` with a reported curve `{2, 10, 40}`** (minor → brain-dominant → over-dominant; the smoke test showed `$\lambda=2$` barely moves the co-trained readout, so the verdict λ is where the brain term is comparable-to-dominant vs CE) so the verdict is not a knife-edge on one weight (review #7); the `permuted` control uses the verdict λ=10; exploratory arms use loss-scale-set λ (blind to unique-R²).

## The two controls that decide *brain-specificity* (predeclared, load-bearing)

Both at identical steps / lr / data / seeds / frozen-embeddings as the brain arms:

1. **`lm_only`** — plain causal-LM fine-tune on the same block-A Tuckute sentences, **no brain target.** Isolates "the model saw in-domain sentences" from "the brain objective shaped features." A real lever must beat `lm_only` (paired bootstrap).
2. **`permuted`** — identical to `mse` but BOLD targets **block-permuted** (`brain_loss.block_permute`: shuffle the stimulus↔response correspondence across contiguous blocks, preserving each ROI's marginal distribution + local autocorrelation). Run with **multiple permutation draws → a null distribution**; a real lever must exceed the **95th percentile of the permuted-null Δ** (a calibrated specificity test, moussa template — the control bilgin omitted). Sanity check (predeclared): `Δ_permuted ≈ Δ_lm_only` (if permuted ≫ lm_only the permutation is leaking structure and is not a clean null).

## Design (LOCKED) — the anti-leakage / anti-confound core

- **Substrate:** **PRIMARY = `Qwen2.5-0.5B`** (verdict layer L12) — E002's strongest aligner and (power analysis below) the better-powered substrate. **SECONDARY = `gpt2`** (L7) for ladder-comparability with E002/E003 and the full loss-family horse-race.
- **Rotating-fold split (fixes the covariate-shift trap, review #1).** A single contiguous 0:700 / 700:1000 split is a **domain-shift split**: across `item_id` 700, imageability shifts A=4.00→B=3.22 (t=+9.8, p=2e-21), both surprisals shift, even network-BOLD mean shifts (p=0.03); and imageability predicts BOLD (r=−0.25, p=1e-15) — a confound *not* in the standard nuisance set (verified in the data, 2026-06-11). **Fix:** K=5 **rotating** contiguous outer folds — tune on 4 folds, evaluate held-out unique R² *only* on the 5th (its own internal 5-fold CV); every item is eval-set exactly once, so the tune↔eval covariate shift averages out across the aggregate Δ, and the eval is always on stimuli the model never optimized against. Report the per-fold A/B balance table as a validity check.
- **Why the metric nuisance stays standard (a deliberate deviation from the reviewer's #1b).** The reviewer proposed adding imageability+surprisal to the metric's nuisance. **gpt2-xl surprisal is itself LM-derived** — subtracting it over-subtracts the very next-word-prediction structure LMs and brains share (the construct), and empirically it inflates the partition variance (gpt2 std 0.008→0.021). So the **primary metric keeps the ladder-standard nuisance [length, position, static-S]** (comparable to E002/E003, matches the Feghhi/Oota low-level confound set), and the covariate-shift threat is handled by rotation + the `lm_only`/`permuted` controls (which share any residual shift, so it cancels in the paired contrasts). An **imageability-subtracted unique R² is reported as a labeled robustness sensitivity** for the winning arm (surprisal-subtraction reported only as a sensitivity, never the primary — over-subtraction noted). The expanded-nuisance finding itself is recorded (`outputs/E004_premises.json`, reproducible via `scripts/verify_e004_premises.py`): adding imageability+surprisal retains **~66% (gpt2) / ~34% (Qwen)** of the unique signal — part of E002's "unique R²" co-varied with imageability/surprisal (→ [`learnings.md`](../learnings.md)).
- **Nuisance held fixed across arms (L004/E003 discipline):** scalar `Z`=length+position; static `S`=mean input-embedding per item from the **untuned base**, byte-identical across all arms.
- **Frozen input embeddings during tuning (review #5):** `wte`/`embed_tokens` are frozen (`requires_grad=False`) so a "lever" cannot come from relabeling lexical vectors — the test asks whether the *contextual computation* moves. Robustness for the winner: re-score unique R² with `S` recomputed from that arm's own embeddings.
- **Metric:** held-out raw **unique R²** = $R^2([\text{len,pos,PCA}(S),\text{PCA}(h)]) - R^2([\text{len,pos,PCA}(S)])$, contiguous 5-fold internal CV, capacity-fair PCA. `NC-allroi-data.csv` gives correlation-scale ceilings (five functional ROI mean $r_{NC}=0.491$); these are reliability context and are not used to normalize the $R^2$ estimand. The verdict is on raw arm differences.
- **Statistic:** $\Delta_{\text{lever}} = A_{\text{tuned}} - A_{\text{base}}$, bootstrap 95% CI over (seed × outer-fold). Specificity: paired bootstrap of (arm − `lm_only`) and the permuted-null exceedance test. Held-out **perplexity** (wikitext-103 slice, `data/kd_corpus/`) per arm.
- **Seeds:** 3 per trained arm (training is stochastic); base is deterministic (scored per fold).
- **`$\lambda_{\text{brain}}$` calibration (review #7):** fixed grid (a 3-point curve), **not** tuned toward unique-R². The grid is set once on a smoke run to bracket "both losses train"; reported as a curve so the verdict isn't a single-λ artifact.
- **Training regime — LoRA (revised at smoke, 2026-06-11):** a full fine-tune at λ=10 **collapsed perplexity** (gpt2 226, Qwen 865) — destroying the LM, which per L011 drags alignment down and confounds the contrast. So the lever uses **LoRA** (rank 16; gpt2 `c_attn/c_proj/c_fc`, Qwen attn+MLP projections; lr 2e-4), the bilgin/merlin/moussa regime: the base LM (incl. embeddings) is frozen by construction, so perplexity stays near base (~125) and any alignment change is attributable to the adapter, not LM damage. Adapters merged before scoring.
- **Per-kind null (revised at smoke):** the smoke showed the **co-trained readout *absorbs* the MSE loss** (`mse ≈ mse_perm` — a free 768→5 map fits real or shuffled BOLD equally, so the gradient to the features is non-brain-specific). This is the pirlot-2022 shuffled-control worry, confirmed. So the lever now tests **both `mse` (co-trained) and `frozen` (fixed readout, forces feature movement) each against its OWN permuted twin** (`mse_perm`, `frozen_perm`); a real brain-specific lever must beat its own null. cos/pearson/cka stay exploratory. This is a principled pre-run refinement, not post-hoc fishing — each candidate is specificity-controlled.
- **Stop rule / budget:** fixed model, fixed verdict layer, fixed K, fixed λ-grid, fixed step budget shared by all trained arms. No tuning toward the alignment outcome.

## Power analysis (review #3 — done before compute, 2026-06-11)

Simulated the locked statistic (Δ CI excludes 0 over 3 seeds × 5 folds) against injected lever sizes, using each substrate's real per-fold noise:

| Substrate | base unique R²/fold | per-fold sd | Δ=+0.003 | Δ=+0.006 | Δ=+0.010 | Δ=+0.015 |
|---|---|---|---|---|---|---|
| gpt2 L7 | +0.013 | 0.013 | 19% | 48% | **86%** | 100% |
| Qwen L12 | +0.009 | 0.009 | 31% | **79%** | 100% | 100% |

**MDE (80% power):** gpt2 ≈ +0.010, Qwen ≈ +0.006. The design detects a moderate-to-large lever but would miss a small one (Δ≈+0.003). **Consequence for the verdict (locked):** a positive result at adequate effect size confirms Q2; **a Tuckute null does NOT license a KILL** (underpowered for small effects) — it routes to the LeBel UTS03 voxelwise benchmark (thousands of voxels → far higher power), exactly the E003-PARTIAL routing.

## Oracle re-review refinements (PASS verdict — accepted, baked in)

The second oracle pass returned PASS (HOLD resolved; rotating-fold + shared-control defense judged sufficient; the rejection of #1b judged sound). Three refinements adopted:
- **Imageability-sensitivity gets teeth (predeclared):** if the winning arm's imageability-subtracted Δ drops *below the permuted-null 95th percentile*, the verdict downgrades to PARTIAL (not a clean PASS). The sensitivity is not a number to wave away post hoc.
- **A/B balance table is reported *before* unblinding Δ** — a pathological fold can't be explained after the fact.
- **`cka` + frozen embeddings:** freezing `wte` fixes part of `h`'s variance to input-embedding content, biasing linear-CKA toward the input geometry and *toward null*. Since `cka` is already negative-control-ish, this is harmless to the verdict — but a `cka` null must not be read as "geometry can't move."

## Decision rule (predeclared kill criteria)

Verdict on the **`mse` arm on Qwen** (primary substrate, primary confirmatory loss); gpt2 + exploratory arms corroborate.

- **LEVER CONFIRMED (Q2 PASS).** `mse` Δ_lever > 0 with 95% CI excluding 0, **AND** beats `lm_only` (paired CI excludes 0), **AND** exceeds the 95th-pct permuted-null, **AND** held-out perplexity not significantly worse than `lm_only`. → The signal is optimizable; **`mse` is the locked D010 form** for E005. An exploratory arm only displaces `mse` if it beats `mse` reproducibly across folds *and* substrates (guards winner's-curse, review #2). Climb Q2 ✅.
- **LEVER KILLED (Q2 FAIL → F1 dead as a training story).** On **Qwen at adequate power** (MDE shown ≤ base +0.036), `mse` Δ_lever CI includes 0 **and** does not exceed the permuted-null. → Optimizing the loss does not move held-out alignment where the signal is largest and confounds are controlled. F1/E005 does not run; reframe per charter. (Negative result counts — D007.) *A null on gpt2 alone, or any null at inadequate power, is NOT a KILL — it routes to LeBel.*
- **AMBIGUOUS / NOT-BRAIN-SPECIFIC (PARTIAL).** `mse` raises held-out alignment but does **not** beat `lm_only` and/or the permuted-null → generic fine-tuning / domain adaptation, not brain-specific. Route to LeBel voxelwise before confirming or killing; do not carry an unconfirmed form into E005.

Degenerate arms (perplexity significantly worse than `lm_only`) are reported but disqualified from "winner" — a lever that breaks the LM is not the lever F1 needs. **A `cka` pass with `mse`/`pearson` null lowers confidence** (geometric stats, not brain correspondence).

## The Q2 → F1 inferential gap (review #6 — stated up front)

A PASS here resolves **Q2** (the signal is optimizable) and **selects the loss form**. It does **NOT** establish A3/F1. E005 (the headline) must still: (a) test the brain term inside **KD** (teacher→student, where it competes with KL, not just CE); (b) compare alignment-guided vs perplexity-only KD **at matched perplexity** (L011 — the only design that converts "headroom" to "confirmed job"); (c) confirm on **LeBel voxelwise**, not ROI-coarse Tuckute. E005 is designed against these from the start.

## How to run

```bash
cd /home/centcom/data/brain-alignment
export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1
# perplexity slice reuses E003's data/kd_corpus/ (already prepared)
CUDA_VISIBLE_DEVICES=0 uv run python scripts/run_brain_lever.py --model gpt2 --seeds 0 1 2          # secondary + horse-race
CUDA_VISIBLE_DEVICES=1 uv run python scripts/run_brain_lever.py --model Qwen/Qwen2.5-0.5B --arms mse lm_only permuted --seeds 0 1 2   # primary verdict
```

## Iteration log

| Date | Run / seed | Command / config | Result (numbers) | Observation / anomaly | Next |
|---|---|---|---|---|---|
| 2026-06-10 | design v1 | — | — | oracle-reviewer HOLD: covariate-shift split (fatal), winner's-curse, no power analysis | reshape |
| 2026-06-11 | design v2 | — | A/B shift + NC mismatch + expanded-nuisance finding verified in data; power sim done | re-locked: rotating folds, mse-primary, permuted-null, frozen-wte, Qwen-primary | re-check → implement → run |
| 2026-06-11 | smoke (full-FT) | gpt2, 250 tune, λ=10 | **perplexity COLLAPSE** (gpt2 226, Qwen 865) | full fine-tune destroys the LM → L011 confound | switch to LoRA |
| 2026-06-11 | smoke (LoRA) | gpt2, 250 tune, λ=10 | ppl preserved (~125); **`mse ≈ mse_perm` and `frozen ≈ frozen_perm`** | co-trained readout *absorbs* the MSE loss (non-brain-specific); frozen forced-movement also ≈ its null at this scale | run full powered verdict |
| 2026-06-11 | FULL run | gpt2 (6 arms+λ-curve) + Qwen (mse/frozen/lm_only), 3 seeds × 5 folds | **Qwen mse − mse_perm = +0.0032 [+0.0006,+0.0058] (brain-specific)**; no arm raises Δ above base; frozen non-specific (regularizer) | PARTIAL → route to LeBel; D010 = mse-leaning (unconfirmed) | lock + oracle E006 |

## Results

Ran 2026-06-11 (LoRA, 3 seeds × 5 rotating folds; gpt2 GPU0 ~27 min, Qwen GPU3 ~28 min). Outputs `outputs/E004_brain_lever_{gpt2,Qwen}.json`; premises `outputs/E004_premises.json`. The matched five-ROI mean correlation ceiling is $r_{NC}=0.491$ and is not used to normalize $R^2$. All Δ = held-out unique R² minus the **untuned base** on the same rotating fold. The original bootstrap over seed×fold cells is superseded by the honest five-fold-unit reanalysis recorded in the status line and addendum.

**Headline (verdict layer; gpt2 base unique R²=+0.0116, Qwen base=+0.0108):**

| Substrate · arm | Δ vs base [95% CI] | **arm − own permuted** [95% CI] (brain-specificity) | arm − lm_only [95% CI] | ppl |
|---|---|---|---|---|
| **Qwen · mse** | +0.0025 [−0.0011, +0.0067] | **+0.0032 [+0.0006, +0.0058] ← excludes 0** | +0.0056 [+0.0031, +0.0089] | 205 |
| Qwen · frozen | −0.0018 [−0.0055, +0.0013] | −0.0009 [−0.0058, +0.0023] | +0.0012 [−0.0005, +0.0028] | 184 |
| Qwen · lm_only | −0.0031 [−0.0063, +0.0005] | — | — | 256 |
| gpt2 · frozen | −0.0009 [−0.0030, +0.0012] | −0.0001 [−0.0018, +0.0014] | +0.0028 [+0.0002, +0.0062] | 177 |
| gpt2 · mse_l2 | −0.0023 [−0.0042, −0.0005] | (mse_perm −0.0022) ≈ 0 | +0.0013 [−0.0007, +0.0034] | 190 |
| gpt2 · mse_l10 / l40 | −0.0029 / −0.0044 | ≈ 0 | +0.0008 / −0.0007 | 199 / 210 |
| gpt2 · lm_only / cos / cka | −0.0037 / −0.0042 / −0.0042 | — | — | 212 / 215 / 228 |

(Base per-fold untuned unique R² ≈ +0.011 both models. Every fine-tuned arm has Δ ≤ 0 vs base — LoRA finetune on 800 Tuckute sentences still mildly degrades held-out alignment and raises ppl ~2× the untuned ~105.)

**What the run shows:**
1. **No arm raises held-out alignment above the untuned base** (every Δ-vs-base CI includes 0 or is negative). Fine-tuning on the 5-ROI screen does not *increase* alignment; the question is whether the brain objective *preserves* it more, and brain-specifically.
2. **A small brain-SPECIFIC effect exists on the strong aligner.** The cleanest test — each arm minus its OWN block-permuted twin, matched on (fold,seed) — is **significant only for Qwen `mse`: +0.0032 [+0.0006, +0.0058]** (real-target tuning beats permuted-target tuning). `frozen` is *not* brain-specific on either model (CI includes 0). The coarse predeclared unpaired `>perm95` test is False for all arms (it is weaker than the paired contrast; the paired vs-control comparison was also predeclared, for `lm_only`).
3. **A regularization (non-specific) effect:** brain objectives degrade alignment *less* than aimless `lm_only` — gpt2 `frozen − lm_only` = +0.0028 (sig), Qwen `mse − lm_only` = +0.0056 (sig) — but for `frozen` this is non-specific (≈ its permuted twin), i.e. just a gentler perturbation.
4. **Loss-form (D010):** the co-trained **MSE** on the strong aligner is the *only* form with a brain-specific paired effect — **reversing the smoke-stage absorption hypothesis** (the short gpt2 smoke had `mse ≈ mse_perm`; at full scale on Qwen the co-trained readout does transmit brain-specific structure that generalizes). `cos`/`cka`/`pearson` are the worst (cka/cos most degrading). `frozen` is a regularizer, not a brain-specific lever.

## Interpretation

**Verdict (predeclared rule): PARTIAL / suggestive — NOT a clean PASS, NOT a KILL. Route to LeBel voxelwise.**

- The **strict predeclared PASS** (Δ-vs-base CI excludes 0 AND beats the unpaired permuted-null AND beats lm_only) is **not met** — the absolute lever does not clear 0 on the 5-ROI screen.
- But the **paired brain-specificity contrast** (the more powerful matched test, consistent with the predeclared paired `lm_only` comparison) is **significant on Qwen `mse` (+0.0032, CI excludes 0)**: optimizing the brain loss produces a held-out alignment gain that is specifically tied to the *real* fMRI targets, not to fine-tuning or domain adaptation. That is a genuine, if small, optimizable brain-specific signal.
- This is exactly the **power-limited PARTIAL** the design anticipated: MDE(80%) on Qwen ≈ +0.006, the effect ≈ +0.003 — below the absolute-test threshold but detectable in the paired contrast. Per the predeclared rule, **a Tuckute null/sub-threshold does not KILL F1; it routes to the powered LeBel UTS03 voxelwise benchmark** (thousands of voxels → far higher power, where a +0.003-scale brain-specific effect should be cleanly resolvable).

**For D010:** the **co-trained MSE encoding loss on the strongest aligner is the most promising form** and the one to carry into the LeBel confirmation and E005 (it is also the theory-preferred, eval-metric-matched form). `frozen` is a non-specific regularizer; geometric (`cka`) and `cos` are the weakest, consistent with the literature caution. D010 is **not yet fully resolved** — the brain-specific effect needs powered confirmation on LeBel before locking the form for the headline.

**Caveats (carried forward):** (1) ROI-coarse 5-dim screen, underpowered for the absolute lever — the verdict rests on the paired specificity contrast, which is the appropriate matched test but should be confirmed at voxel scale. (2) LoRA finetune still degrades ppl ~2× and alignment slightly — a gentler regime (lower lr / fewer steps / a perplexity-matched stop) is worth testing on LeBel. (3) The brain-specific effect is on Qwen-`mse` only; gpt2 shows no specificity — model-dependence to watch. (4) `frozen`'s "beats lm_only" is regularization, not a lever — do not over-read it.

**Historical routing (superseded):** the original read proposed E006 and a voxelwise rerun. The corrected verdict is recorded in this file's final addendum and in the extended manuscript; current operations live in [`status.md`](../status.md).

---

## S25 RECOMPUTE (2026-06-19, Erfan-confirmed): Q2 → NO DEMONSTRATED LEVER

The original Q2 verdict rested on one statistic — the Qwen `mse` − permuted-twin paired contrast,
reported as **+0.0032 [+0.0006, +0.0058]** ("excludes 0"). S25 re-derived this directly from
`outputs/E004_brain_lever_Qwen.json` (the `mse` and `mse_perm` `delta` cells) at two inference units:

| Inference unit | mean | 95% CI | excludes 0? |
|---|---|---|---|
| **Flat 15-cell bootstrap** (3 seeds × 5 folds as 15 independent — the recorded construction) | +0.00316 | [+0.00062, +0.00584] | yes ← the reported number |
| **Honest fold unit (n=5 folds, seeds averaged within fold)** | +0.00316 | **[−0.00227, +0.00858]** | **NO** |

Per-fold paired contrast: `{0: −0.0007, 1: +0.0003, 2: +0.0045, 3: +0.0016, 4: +0.0101}` →
**fold-4 carries 64%** of the summed signal; leave-fold-4-out mean = **+0.0014**. The recorded
`summary.mse.beats_permuted_null = False` (the unpaired exceedance test already failed).

**Why this matters:** the 15-cell flat bootstrap treats non-independent draws (the 5 folds are one
partition of one subject-averaged target; the 3 seeds reuse identical data) as independent, which
under-states the error bars — **the exact pseudo-replication the project diagnosed and corrected for
E005 (L015) but never applied to E004.** At the honest unit the CI includes 0, so there is **no
inference-unit-valid evidence that optimizing the brain loss moves held-out alignment.**

**Verdict (Erfan-confirmed): NO DEMONSTRATED LEVER** — *undemonstrated*, deliberately **NOT** "proven
zero": n=5 folds is underpowered to exclude a small (~+0.003) effect, and a powered voxel-scale test
(the predeclared LeBel re-run) was never run. The honest statement is "no valid-unit evidence of a
lever," and that is consistent with the robust Q3 per-individual null. Ladder Q2 flipped 🟡 → ❌
(with the caveat in-cell). Reproducible: `outputs/E004_brain_lever_Qwen.json` + the L015 fold-level
machinery in `scripts/reanalyze_e005_e006.py`.


## Retained load-bearing artifact

| Artifact | SHA-256 |
|---|---|
| `outputs/E004_brain_lever_Qwen.json` | `5f5582a651ecd86c25691fe24b6827d49a258c33e95127f630c522563d8dc6d4` |

## Related
- [`status.md`](../status.md) — the canonical status board
