# Experiment — E004: is `$\mathcal{L}_{\text{brain}}$` a usable *lever*? (R03 Layer 1) + the D010 loss-form resolution

**Created:** 2026-06-10 · **Re-locked:** 2026-06-11 (after oracle-reviewer HOLD → design reshaped) · **Status:** DESIGN LOCKED (pre-run) · **Mode:** working
**Direction:** `../reports/R03_brain-as-training-signal.md` §5 (Layer 1 of the ladder) · `../ladder.md` (L1 rung)
**Theory:** `../06-theory-grounding.md` §1 (MI gen-bound), §2 (DPI ceiling), §3 (conditional MI = unique R²)
**Predecessors:** `E002` (A2 PASS — encoding signal is real on Tuckute) · `E003` (Layer-2a PARTIAL — KD lands below teacher, alignment co-varies with ppl, L011)
**Resolves:** decision **D010** (the form of `$\mathcal{L}_{\text{brain}}$`) — empirically, on real neural data.
**Code:** `scripts/run_brain_lever.py` (runner), `scripts/brain_loss.py` (loss family), `scripts/pilot_lib.py`, `scripts/data_adapters.py:load_tuckute`
**Output:** `outputs/E004_brain_lever.json`

---

## Objective — the kill-gate for the whole thesis below it

The ladder's Layer 1: **is the brain-alignment signal a *lever* we can move by optimizing it, or only a property we can *measure*?**

> When we fine-tune a small LM with a differentiable brain-alignment loss `$\mathcal{L}_{\text{brain}}$` on held-in stimuli, does its **held-out** unique encoding R² (on stimuli it was never tuned on) *rise* above the untuned model — under the E002 anti-confound protocol — and does that rise survive the controls that separate "the brain objective worked" from "any fine-tune / domain-adaptation would have done it"?

If yes → L1 PASS, and we have the loss form for E005 (the headline alignment-guided-KD experiment). If a confident no on the powered benchmark → the signal is measurement-only and F1 dies (reframe to measurement rigor, charter). This experiment also **resolves D010**: D010's three candidate forms are run head-to-head on real Tuckute data; the lever effect + the controls pick the winner.

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
- **Why the metric nuisance stays standard (a deliberate deviation from the reviewer's #1b).** The reviewer proposed adding imageability+surprisal to the metric's nuisance. **gpt2-xl surprisal is itself LM-derived** — subtracting it over-subtracts the very next-word-prediction structure LMs and brains share (the construct), and empirically it inflates the partition variance (gpt2 std 0.008→0.021). So the **primary metric keeps the ladder-standard nuisance [length, position, static-S]** (comparable to E002/E003, matches the Feghhi/Oota low-level confound set), and the covariate-shift threat is handled by rotation + the `lm_only`/`permuted` controls (which share any residual shift, so it cancels in the paired contrasts). An **imageability-subtracted unique R² is reported as a labeled robustness sensitivity** for the winning arm (surprisal-subtraction reported only as a sensitivity, never the primary — over-subtraction noted). The expanded-nuisance finding itself is recorded (`outputs/E004_premises.json`, reproducible via `scripts/verify_e004_premises.py`): adding imageability+surprisal retains **~66% (gpt2) / ~34% (Qwen)** of the unique signal — part of E002's "unique R²" co-varied with imageability/surprisal (→ `learnings.md`).
- **Nuisance held fixed across arms (L004/E003 discipline):** scalar `Z`=length+position; static `S`=mean input-embedding per item from the **untuned base**, byte-identical across all arms.
- **Frozen input embeddings during tuning (review #5):** `wte`/`embed_tokens` are frozen (`requires_grad=False`) so a "lever" cannot come from relabeling lexical vectors — the test asks whether the *contextual computation* moves. Robustness for the winner: re-score unique R² with `S` recomputed from that arm's own embeddings.
- **Metric:** held-out **unique R²** = $R^2([\text{len,pos,PCA}(S),\text{PCA}(h)]) - R^2([\text{len,pos,PCA}(S)])$, contiguous 5-fold internal CV, capacity-fair PCA. **NC-normalised by the mean of the 5 functional target sub-ROI NCs = 0.491** (`lang_LH_{AntTemp,IFG,IFGorb,MFG,PostTemp}` NCs = 0.458/0.452/0.452/0.515/0.579; the network-level `lang_LH_netw` = 0.559 is the alternative). This is the ceiling matched to the actual functional targets — *not* the anatomical-Glasser `anatglasser_LHRH_LangNetw` = 0.353 that `load_tuckute`/E002/E003 mislabeled with (verified against `NC-allroi-data.csv`, 2026-06-11; the verdict is on raw Δ either way; E002/E003 understated their NC-fraction — flagged for the wrap). An oracle re-review claimed 0.559 was unsupported; the file refutes that (row `lang_LH_netw`).
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

**MDE (80% power):** gpt2 ≈ +0.010, Qwen ≈ +0.006. The design detects a moderate-to-large lever but would miss a small one (Δ≈+0.003). **Consequence for the verdict (locked):** a positive result at adequate effect size confirms L1; **a Tuckute null does NOT license a KILL** (underpowered for small effects) — it routes to the LeBel UTS03 voxelwise benchmark (thousands of voxels → far higher power), exactly the E003-PARTIAL routing.

## Oracle re-review refinements (PASS verdict — accepted, baked in)

The second oracle pass returned PASS (HOLD resolved; rotating-fold + shared-control defense judged sufficient; the rejection of #1b judged sound). Three refinements adopted:
- **Imageability-sensitivity gets teeth (predeclared):** if the winning arm's imageability-subtracted Δ drops *below the permuted-null 95th percentile*, the verdict downgrades to PARTIAL (not a clean PASS). The sensitivity is not a number to wave away post hoc.
- **A/B balance table is reported *before* unblinding Δ** — a pathological fold can't be explained after the fact.
- **`cka` + frozen embeddings:** freezing `wte` fixes part of `h`'s variance to input-embedding content, biasing linear-CKA toward the input geometry and *toward null*. Since `cka` is already negative-control-ish, this is harmless to the verdict — but a `cka` null must not be read as "geometry can't move."

## Decision rule (predeclared kill criteria)

Verdict on the **`mse` arm on Qwen** (primary substrate, primary confirmatory loss); gpt2 + exploratory arms corroborate.

- **LEVER CONFIRMED (L1 PASS).** `mse` Δ_lever > 0 with 95% CI excluding 0, **AND** beats `lm_only` (paired CI excludes 0), **AND** exceeds the 95th-pct permuted-null, **AND** held-out perplexity not significantly worse than `lm_only`. → The signal is optimizable; **`mse` is the locked D010 form** for E005. An exploratory arm only displaces `mse` if it beats `mse` reproducibly across folds *and* substrates (guards winner's-curse, review #2). Climb L1 ✅.
- **LEVER KILLED (L1 FAIL → F1 dead as a training story).** On **Qwen at adequate power** (MDE shown ≤ base +0.036), `mse` Δ_lever CI includes 0 **and** does not exceed the permuted-null. → Optimizing the loss does not move held-out alignment where the signal is largest and confounds are controlled. F1/E005 does not run; reframe per charter. (Negative result counts — D007.) *A null on gpt2 alone, or any null at inadequate power, is NOT a KILL — it routes to LeBel.*
- **AMBIGUOUS / NOT-BRAIN-SPECIFIC (PARTIAL).** `mse` raises held-out alignment but does **not** beat `lm_only` and/or the permuted-null → generic fine-tuning / domain adaptation, not brain-specific. Route to LeBel voxelwise before confirming or killing; do not carry an unconfirmed form into E005.

Degenerate arms (perplexity significantly worse than `lm_only`) are reported but disqualified from "winner" — a lever that breaks the LM is not the lever F1 needs. **A `cka` pass with `mse`/`pearson` null lowers confidence** (geometric stats, not brain correspondence).

## The L1 → F1 inferential gap (review #6 — stated up front)

A PASS here resolves **L1** (the signal is optimizable) and **selects the loss form**. It does **NOT** establish A3/F1. E005 (the headline) must still: (a) test the brain term inside **KD** (teacher→student, where it competes with KL, not just CE); (b) compare alignment-guided vs perplexity-only KD **at matched perplexity** (L011 — the only design that converts "headroom" to "confirmed job"); (c) confirm on **LeBel voxelwise**, not ROI-coarse Tuckute. E005 is designed against these from the start.

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

## Results

_TBD — populated after the run._

## Interpretation

_TBD — populated after the run; updates `../ladder.md` (L1), `../learnings.md`, and D010 status._
