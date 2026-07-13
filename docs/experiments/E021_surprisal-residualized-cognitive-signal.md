---
title: "Experiment E021 — surprisal-residualized cognitive-signal auxiliary training (the keystone, T1.3)"
tags: [experiment]
aliases: [E021]
---

# Experiment E021 — surprisal-residualized cognitive-signal auxiliary training (the keystone, T1.3)

**Created:** 2026-06-17 · **Status:** RESOLVED — **CLEAN NULL on cognition (v5, panel-driven, 2026-06-18).** Surprisal-orthogonality NULL (raw≈residual). The RT edge over learnability-matched controls (the v4 below-trend gap) is REAL but is **signal SHAPE, not cognition**: a phase-randomized twin carrying RT's autocorrelation (lag-1 ~0.62) + heavy-tailed marginal (kurtosis ~13) but ZERO behavioral content TIES the residual (172.1 vs 177.4, +5.3 [−7.9,+18.5]) — a content-free shape twin reproduces the whole advantage. So human reading time carries no cognition-specific trainable structure beyond its statistical shape. Matches H1 + Deng'24 + BabyLM. NO rung flip.**
**Historical program:** Path-B auxiliary-signal test; current state is owned by [`status.md`](../status.md). · **Mode:** promotable

---

## Objective

Decide whether a human cognitive signal (reading-time and/or EEG-N400), **after the component predictable from the language model's own surprisal is regressed out**, provides a cognition-specific training signal that improves a *downstream* metric (sample-efficiency / OOD perplexity) beyond a permuted twin and a matched-budget baseline — or whether, like our fMRI result, it buys nothing because cognitive signals are largely surprisal-redundant.

This is the keystone that unifies the program (§6b): a null generalizes our fMRI negative across **three** modalities (fMRI + behavioral + EEG) under one novel lens (surprisal-residualization) — a general, main-track-shaped negative. A surviving residual arm is the new positive that lifts Path A to main-track. **Both outcomes are publishable**, which is why this is GO despite a weak prior.

## Claim tuple

- **Metric:** downstream Δ (sample-efficiency OR OOD held-out perplexity), arm(iii) − arm(iv) · **Threshold:** CI excludes 0, ≥3 seeds, paired over splits · **Baseline:** permuted-twin (shuffled residualized signal) at matched training budget · **Condition:** auxiliary cognitive-signal objective on a small decoder LM.

## Competing hypotheses (predeclared; no cherished one)

- **H1 — null (high prior).** Residualized-real ≈ permuted ≈ baseline downstream. Cognitive signals are surprisal-redundant; the residual carries no training-useful structure. *Generalizes the fMRI null (E008/E009) across modalities.* Prior support: BabyLM (cognitive aux ≈ randomized-order); the ~0 matched-ppl fulcrum (E009); reading-time/N400 ≈ surprisal (the N400-surprisal literature).
- **H2 — cognition-specific positive (the lottery ticket).** The surprisal-orthogonal residual encodes incremental processing-difficulty structure that, as an auxiliary objective, improves sample-efficiency or OOD beyond permuted. → reopens a real positive; STOP for Erfan before any rung/claim.
- **H3 — non-specific regularization.** A downstream gain appears but the permuted twin matches it (generic aux-objective regularization, cf. the E004 `frozen` arm) → not cognition-specific; folds back into the negative.

## Predeclared kill / decision rule (oracle-revised — triple dissociation)

A cognition-specific positive now requires a **triple dissociation** (oracle §3): residualized-real (iii) > permuted-twin (iv) **AND** (iii) > random-structured (vi). Beating only the permuted twin = generic aux-head regularization (the E004 `frozen` effect, +0.0028, non-specific) — NOT cognition.

- **Positive (H2):** (iii) − (iv) > 0 **and** (iii) − (vi) > 0, both CIs exclude 0, ≥3 seeds, on the *downstream* metric, survives the panel. → escalate to Erfan; flip nothing autonomously (a surviving positive is the Fork-A-equivalent STOP).
- **Non-specific (H3):** (iii) ≈ (vi) (random-structured matches) → generic regularization, folds into the negative.
- **Clean null (H1):** (iii) ≈ (iv) ≈ baseline within the **predeclared MDE**, *and* the gating sequence passed (residual was reliable, downstream contrast was powered). This is the publishable cross-modal negative.
- **Vacuous (not a null):** if the residual fails the reliability floor or the power positive-control fails → "instrument too weak / unpowered on this data," E020-style corroboration at best, NOT a headline. Say so explicitly; do not dress a vacuous result as a clean null.
- The success metric is **downstream**, never "predicts the cognitive signal better" (circular — the whole point). Predeclared reading of the **raw-aux arm (ii):** raw ≈ permuted (because raw is surprisal-redundant); only the *residual* arm can differ — that contrast IS the mechanism check.

## Design (LOCK before running — pending oracle gate)

- **Base LM:** small decoder, our existing family for continuity — **Qwen2.5-0.5B** (primary) and/or **GPT-2** (replication). Reuse `distill.py` / `run_brain_lever.py` scaffolding (co-trained aux head + λ).
- **Cognitive signal + data:** **ZuCo / ZuCo 2.0** (Hollenstein 2018; simultaneous EEG + eye-tracking during natural reading; ~1.1k sentences, word-aligned; public OSF). Behavioral target = total-reading-time / gaze-duration per word; EEG target = N400-window mean amplitude per word. Backstop for behavioral scale: **GECO / Provo / Dundee** (eye-tracking, larger). *Data acquisition is a prerequisite step (not yet on disk).*
- **The residualization (the novelty — operationalized as conditional information / unique R², cf. [`../06-theory-grounding.md`](../06-theory-grounding.md)):** for each arm's *base* LM, extract per-word surprisal; regress the cognitive signal on [surprisal + nuisances: word length, log-frequency, position] via ridge; the **residual** is the training target. This isolates the cognition component the model does *not* already encode. **Leakage control (oracle §2a):** the surprisal→signal ridge is fit on **train folds only** and applied to held-out folds — never fit on eval-fold data.
- **Arms (predeclared, matched budget — 6 arms; oracle §3 added the random-structured arm for the triple dissociation):**
  1. **baseline** — no aux objective, matched steps/tokens/params.
  2. **raw-aux** — predict the raw cognitive signal (the Deng'24 / naive form). Predeclared reading: raw ≈ permuted (surprisal-redundant) ⇒ only the residual can differ.
  3. **residualized-aux** — predict the surprisal-residualized signal. *(the test arm)*
  4. **permuted-twin** — predict the *block-permuted* residualized signal — controls for the residual's marginal distribution.
  5. **random-structured** — predict a *fresh* smooth random regressor matched in scale + autocorrelation to the residual (NOT a permutation of the real signal) — the **E004 `frozen` analog**; controls for "any structured aux head regularizes optimization." Cognition-specificity requires (iii) > (iv) **and** (iii) > (v).
  6. **residualized-EEG-aux** — same as (3) with the N400 residual. **Demoted to a cross-modal STRETCH arm (oracle §3):** single-word N400 at 12 subjects is the noisiest target; the **behavioral (eye-tracking) arm is primary**, EEG runs only if it clears the reliability floor.
- **Auxiliary objective:** a light co-trained head predicting the (residualized) per-word target, added to the LM loss with weight λ (small λ-grid); LoRA or light full-FT; **identical optimizer/steps/data budget across arms** (the matched-budget parity is explicit).
- **Downstream metric — PRIMARY = frozen-representation linear-probe AULC (REVISED S22 after G2 v1 failed).** *Original metric (fine-tune-then-perplexity AULC) is RETIRED:* G2 v1 proved it both unpowered (MDE 9–12 AULC) and **biased** — a scalar aux head perturbs the shared trunk in proportion to its target's learnability, that perturbation degrades next-token quality, and Stage-B fine-tuning *overwrites the installed prior* before measurement, so the metric structurally rewards the least-learnable (noise) target = a built-in false negative (recorded instrument finding; the E009 "prior washed out at measurement" lesson in a new form). **Revised metric:** after Stage-A co-training (LM loss + λ·aux, gradient flows into the trunk — the mechanism), **freeze the trunk** and train only a linear probe / LM-head on held-out-**domain** data across the predeclared caps {100, 300, 1k, 3k}; AULC of held-out-domain probe loss, paired per seed. This measures the representational change the aux objective installed *without* the fine-tune-overwrite or trunk-perturbation confound; the residual arm helping the frozen probe *more than* permuted/random is a fair cognition-specific test. Held-out domain = Wikitext-103 (distinct from Natural Stories narrative). *Never* report signal-prediction as a success.
- **Seeds:** ≥3 (stochastic). Paired contrasts over folds × seeds (the E008 clustering pattern).
- **Confound controls:** contiguous / sentence-block splits (anti-leakage); nuisance baselines already inside the residualization (length, frequency, position); the permuted twin is the specificity control; report arm(iii)−arm(iv) after the residualization. ZuCo is small → **predeclare the MDE and run an E008-style power positive-control**; treat a tight null as informative, not as "underpowered, inconclusive."
- **Stop rule / budget:** small (small LM + small data) — target ≤ a few GPU-hours per arm; ≤4 arms in flight on the 4× L40S. Stop when all arms × ≥3 seeds complete or a predeclared positive triggers the Erfan-escalation.
- **Promotable vs exploratory:** promotable only if the matched-budget parity holds, the power positive-control validates the MDE, and the panel survives. Otherwise exploratory.

## Gating sequence — run BEFORE any science arm (oracle HOLD→PASS path)

These cheap measurements decide whether the full 6-arm × ≥3-seed matrix is worth running at all. Run **in order**; abort at the first failure (each abort is a result, recorded).

- **G0 — residual-existence (cheapest; before touching ZuCo).** On a **clean, large** eye-tracking corpus (GECO / Dundee / Provo — bigger N than ZuCo), compute the **unique R² of the cognitive signal NOT explained by base-LM surprisal + nuisances** (length, log-freq, position), train-fold-fit. *If this residual unique-R² is ≈ 0 on clean behavioral data, the whole keystone is vacuous on behavior → KILL the behavioral instantiation (and EEG is hopeless a fortiori); pivot or stop.* This is the single highest-value check and needs no training — just surprisal + ridge.
- **G1 — residual reliability floor (oracle §2b).** For the chosen corpus, report the residual target's split-half / noise-ceiling-normalized reliability. Predeclare the floor: if the residual's reliable variance is statistically indistinguishable from noise at the available N → the test is **vacuous, not null**. Pass required before training.
- **G2 — power positive-control on the frozen-probe metric (REVISED S22).** Plant a *known representational prior* — co-train Stage-A toward a target that genuinely encodes held-out-domain structure (e.g. a head-start on the held-out domain's own signal) — and confirm the **frozen-probe AULC detects it** (the planted-prior arm beats its control) at the predeclared MDE (computed from the run's own seed variance, L017(3), NOT borrowed). This validates that the frozen-probe metric can see *any* representational prior at all (the fix-2 sanity the v1 metric failed). If it can't → the metric is still dead → do not run the science arms; report bounded/inconclusive (E020-style). *(v1 history: the fine-tune-AULC metric failed this on two target constructions, wrong-sign every seed — `outputs/e021/g2_power_control.json`, `g2v1_*.json`.)*

Only if **G0, G1, G2 all pass** do the 6 science arms run.

## Build dependencies (after the gates pass)
1. **Behavioral corpus acquisition + word-alignment** (GECO/Dundee/Provo for scale → ZuCo for the EEG cross-modal arm). *Not on disk.*
2. **Surprisal-extraction + train-fold residualization script** (per-word surprisal from the base LM; ridge fit train-only).
3. **Aux-training loop** (adapt `distill.py`/`run_brain_lever.py` for the co-trained residual-prediction head, matched budget; the AULC eval harness over the predeclared caps).

**Positioning (done S22):** canonical notes written for **Deng'24** ([`deng-2024_gaze-supervised-finetuning`](../literature/canonical/deng-2024_gaze-supervised-finetuning.md) — raw synthetic-scanpath order, BERT, in-dist GLUE, no residualization; its own shuffle control gives only +0.33pp over shuffled → supports our prior) and **BabyLM** ([`babylm-2025_cognitive-objectives-findings`](../literature/canonical/babylm-2025_cognitive-objectives-findings.md) — cognitive aux ≈ randomized-order null; no submission ever residualized → E021's gap). E021 owns: surprisal-residualization, decoder LM, AULC/sample-efficiency, matched-budget, the random-structured + permuted triple dissociation, the EEG cross-modal arm.

## Iteration log

| Date | Run / seed | Command / config | Result (numbers) | Observation / anomaly | Next |
|---|---|---|---|---|---|
| 2026-06-17 | — | design | — | drafted; oracle HOLD addressed | run gating sequence |
| 2026-06-17 | G0/G1 | `scripts/run_e021_g0g1.py` → `outputs/e021_g0g1/` | residual split-half reliability **0.72** (SB) vs noise ceiling **0.77**; unique-R²(surprisal in RT)=**0.048±0.020**; residual = 77% of RT var | **PASS** — surprisal-orthogonal RT residual is reliable, not noise (Natural Stories, 180 subj, 10k words; GPT-2≈Qwen) | build harness + G2 power control |
| 2026-06-17 | G2 v1 | `scripts/run_e021_arms.py` (fine-tune-AULC) → `outputs/e021/` | planted effect WRONG-SIGN both constructions (+6.3 / +4.8, wrong sign every seed); MDE 9–12 AULC | **FAILED** — metric unpowered + biased: aux head perturbs trunk ∝ learnability, hurts next-token, Stage-B overwrites the prior → rewards least-learnable target (false-negative). Arms NOT run (hard gate held). | revise metric → frozen-probe AULC; re-run G2 |
| 2026-06-17 | G2 v2 | `scripts/run_e021_v2.py` → `g2v2_frozen_probe.json` | planted prior −705.6 AULC [−776,−635], MDE 70.7 | **PASS** — frozen-probe metric detects a representational prior | run 5 arms |
| 2026-06-17 | 5 arms ×3 seeds | `scripts/run_e021_v2.py` → `arms_v2_results.json` | base 742 · raw 221 · resid 228 · perm 266 · rand 249; resid−perm −37.9 [−53,−22], resid−rand −21.2 [−35,−8] | **triple dissociation fired, NOT believed** — raw>residual ⇒ likely GENERIC regularization not cognition; Fork-A STOP | panel + Codex + log-cap robustness → Erfan |
| 2026-06-17 | panels + Codex | counter-argument + first-principles (opus) + Codex review | — | on the BUGGY v2: argued generic-regularization; Codex found a real pad-label bug + control flaws (seed-invariant targets, in-sample residual, non-identical probe init) → v2 numbers untrustworthy | clean rerun + log-freq control |
| 2026-06-17 | clean v3 | `scripts/run_e021_v3.py` → `arms_v3_results.json` (G2v3 PASS, MDE 42.7) | base 628·raw 181·**resid 177**·perm 197·rand 203·logfreq 250; resid−perm −20.0 [−41.6,**+1.6**], resid−rand −26.2 [−52.7,**+0.3**], raw−resid +4.3 [−3.9,+12.6], logfreq WORST | **INCONCLUSIVE (n=3)** — surprisal-orthogonality NULL (raw≈resid); generic regularization dominant; weak non-sig residual hint; logfreq control confounded by learnability. Not clean +/−. | more seeds + learnability-matched control |
| 2026-06-18 | v4 (n=10) | `scripts/run_e021_v3.py --shard` + `analyze_e021_v4_learnability.py` → `arms_v4_results.json`, `v4_within_seed_learnability.json` | resid beats ALL controls (perm −40.8, rand −39.3, other-LM-surp −46.5, wlen −66, logfreq −81; all excl 0); raw−resid +6.1 (≈0); within-seed gap below learnability trend resid −48.3 [−62,−34], all 10 seeds neg | **LIKELY POSITIVE (later superseded)** — human-RT beats every learnability-matched control; surprisal-orthogonality NULL. Auto-"clean null" was wrong (pooled regression); within-seed test showed the gap. | panel → shape-matched control |
| 2026-06-18 | v5 (n=10) | panel (counter-arg + first-principles) → `scripts/run_e021_v5.py` → `arms_v5_results.json` | phase-randomized shape twin (RT autocorr 0.62 + kurtosis 13, zero content) AULC 172.1 TIES residual 177.4 (resid−shape +5.3 [−7.9,+18.5]) | **CLEAN NULL on cognition** — the v4 gap is signal SHAPE not content; a content-free shape twin reproduces the whole RT edge. Surprisal-orthogonality NULL. | record (Erfan); strengthens Path-A negative |

## Results (running)

**G0/G1 (residual existence + reliability) — PASS.** On Natural Stories self-paced RT (180 subjects, 10,256 words; GPT-2-small surprisal, by-item 10-fold CV ridge, 25 subject half-splits SB-corrected):
- unique R² of surprisal (+spillover) in RT = **0.048 ± 0.020** — the LM explains *little* of RT (full model incl. nuisances R²=0.226).
- residual fraction of RT variance = **0.765**.
- **residual split-half reliability = 0.720 (SB)** vs by-word RT noise ceiling **0.767** → the surprisal-orthogonal residual is ~94% as reliable as the raw signal: **reliable structure, not noise.** Qwen2.5-0.5B materially identical (0.722 vs 0.767).
- Cross-checks pass: GPT-2/Qwen surprisal agree r=0.91; surprisal↔RT r=+0.20 (canonical positive effect).

**G2 v1 (fine-tune-then-perplexity AULC metric) — FAILED → metric retired.** The planted-prior positive-control came out **wrong-sign on two independent target constructions** (synthetic−permuted = +6.3 [0.2,12.4] and +4.8 [0.2,9.3], wrong sign every seed), MDE 9–12 AULC. Mechanism (from Stage-A logs): the more-learnable target is fit better yet yields *worse* held-out ppl at every cap, largest at cap-100, shrinking by cap-3000 where Stage-B overwrites Stage-A — a scalar aux head perturbs the shared trunk ∝ target learnability, degrading next-token quality, and the fine-tune overwrites the installed prior before measurement. So the metric structurally rewards the *least*-learnable (noise) target = a built-in false negative. **Recorded instrument finding (→ learnings):** representational-prior experiments cannot be scored by fine-tune-then-perplexity — the prior is washed out at measurement (the E009 lesson, new form); use a frozen-representation probe. Arms NOT run (G2 hard-gate held). Artifacts: `outputs/e021/G2_VERDICT.md`, `g2_power_control.json`, `g2v1_proj-probe_FAILED.json`.

**G2 v2 (frozen-probe metric) — PASSED.** Planted head-start representational prior detected: head-start − control = **−705.6 AULC, CI [−776,−635]**, correct sign every seed, MDE=70.7 (effect ≈10× MDE). The frozen-probe metric can see a representational prior. (`outputs/e021/g2v2_frozen_probe.json`.)

**The 5 arms (frozen-probe AULC, mean over 3 seeds, lower=better) — RUN; NOT BELIEVED (Fork-A STOP, panel + Codex + Erfan pending):**

| arm | mean | seed0/1/2 |
|---|---|---|
| (i) baseline λ=0 | 742.2 | 795/705/726 |
| (ii) raw RT | **220.8** | 252/189/221 |
| (iii) residual | 228.0 | 269/174/241 |
| (iv) permuted | 265.9 | 322/207/268 |
| (v) random-struct | 249.2 | 298/201/248 |

Triple dissociation fired: residual−permuted=−37.9 [−53.3,−22.5] ✓, residual−random=−21.2 [−34.8,−7.6] ✓ (both exclude 0, no seed flip). **BUT the cognition-specific reading is contradicted by the data:** raw (ii, 220.8) is the *best* arm, beating the residual — so the useful ingredient is "real word-aligned signal" broadly (raw carries the most), NOT the surprisal-orthogonal residual the experiment was built to isolate. The dominant effect is the ~500-AULC baseline→any-structured-arm gap = generic aux-regularization of a tiny-corpus fine-tune (the E004 `frozen` effect at scale). **Honest interim read: most likely GENERIC regularization, not cognition-specific.** Caveats: post-lock metric switch (principled, G2-validated); cap-3000 dominates the AULC mean (noisiest term) → log-cap robustness pending. Artifacts: `outputs/e021/{ARMS_VERDICT.md,arms_v2_results.json}`; harness `scripts/run_e021_v2.py`.

**CLEAN v3 (Codex fixes 1–5 + log-freq control arm; the TRUSTWORTHY numbers — supersedes v2).** G2v3 PASS (planted prior −548 AULC [−591,−505], MDE 42.7, ≈13× MDE). 6 arms × 3 seeds, frozen-probe AULC (lower=better):

| arm | mean±sem | | contrast | mean [95% CI] |
|---|---|---|---|---|
| baseline λ=0 | 628.4±22.1 | | residual−permuted | −20.0 [−41.6, **+1.6**] ✗ |
| raw RT | 181.3±16.0 | | residual−random | −26.2 [−52.7, **+0.3**] ✗ |
| residual | **176.9±11.8** | | raw−residual | +4.3 [−3.9,+12.6] ≈0 |
| permuted | 196.9±22.8 | | raw−permuted | −15.6 [−29.1,−2.2] ✓ |
| random_struct | 203.1±24.9 | | logfreq−permuted | +52.9 [+29.8,+76.1] (logfreq WORSE) |
| logfreq | 249.8±34.5 | | logfreq−random | +46.7 [+26.8,+66.5] (logfreq WORSE) |

The pad-fix dropped baseline 742→628 (gap ~450, so NOT mainly a pad artifact — generic regularization is real). `triple_dissociation=False` (the residual−surrogate CIs now touch 0). Artifacts: `outputs/e021/{arms_v3_results.json,g2v3_frozen_probe.json}`; harness `scripts/{run_e021_v3.py,e021_targets_v3.py}`.

**CLEAN v4 (n=10 seeds + learnability-matched covariate adjudication — the RESOLUTION).** Added non-cognitive controls spanning learnability (log-freq, word-length, another-LM surprisal=Qwen2.5-0.5B) + recorded per-arm aux-MSE. Arm AULC (mean, lower=better): baseline 611 · **raw 181.2 · residual 175.1** · permuted 215.9 · random 214.4 · surp_other_lm 221.6 · wlen 240.9 · logfreq 256.3. Paired n=10 contrasts (all exclude 0): residual−permuted −40.8 [−54.7,−26.9]; residual−random −39.3 [−53.3,−25.3]; residual−surp_other_lm −46.5 [−61.6,−31.3]; residual−wlen −65.8; residual−logfreq −81.2; **raw−residual +6.1 [−2.4,+14.5] (≈0 → surprisal-orthogonality NULL).** Artifacts: `outputs/e021/{arms_v4_results.json,arms_v4_shard_*.json,v4_within_seed_learnability.json}`; analysis `scripts/analyze_e021_v4_learnability.py`.

**The learnability adjudication (corrected).** The combine step's auto-verdict said "clean null" off a *pooled-per-seed* regression — but that pooling ignores the large shared seed effect (raw swings 122→270 across seeds) and spuriously inflates the CI. The correct **within-seed** paired test (fit the AULC~aux-MSE trend on the 5 non-cog arms per seed, gap = residual − predicted): **residual −48.3 [−62.4,−34.5], raw −45.9 [−61.6,−31.3], both negative on all 10 seeds.** Residual/raw are significantly BELOW the learnability trend = *better than their learnability predicts.* Clinching qualitative check: permuted (aux-MSE 0.30) and random (0.27) are *less* learnable than residual (0.22) yet probe *worse* — residual wins despite a learnability *disadvantage*, so its edge is content, not low disruption.

## v4 VERDICT (supersedes everything below) — LIKELY POSITIVE, panel-pending
Two claims, honestly separated:
1. **Surprisal-orthogonality: NULL.** raw ≈ residual — stripping the model's-own-surprisal-predictable part of reading time changes nothing. The experiment's *original* novelty is dead. (raw−residual CI crosses 0; consistent across v3 + v4.)
2. **Human reading-time signal is a genuinely better auxiliary-regularization target than every control** — surface features (frequency, length), another LM's surprisal, and shuffled/random twins — significant on every seed, and below the learnability trend. So there is real, learnability-controlled, *human-RT-specific* structure that transfers as useful regularization to a held-out domain.

**This is a likely POSITIVE (Fork-A-adjacent), NOT believed yet.** It is one setup (GPT-2-small / Natural Stories / Wikitext probe), a modest effect within the aux-regularization regime, mechanism unpinned, and the automated verdict was wrong once already this run — so it needs the thinking panel (is "human RT beats other-LM-surprisal, learnability-controlled" real or an artifact? what's the mechanism? what replicates it?) + replication + Erfan before anything is recorded as a finding or flips a rung. **NO rung flip.**

## v5 VERDICT (panel-driven, 2026-06-18) — CLEAN NULL on cognition (supersedes the v4 likely-positive)
The v4 below-trend gap is **real but mis-attributed.** A thinking panel (counter-argument + first-principles, opus — run inside the resolution agent, and independently re-confirmed externally) found the covariate was incomplete: `aux_mse` (learnability) is not the only axis on which RT differs from the controls. **RT is the only target that is jointly heavy-tailed (kurtosis ~13) AND temporally autocorrelated (lag-1 ~0.62);** each v4 control matched at most one (permuted matches the marginal but kills autocorrelation; random_struct matches autocorrelation but is Gaussian). The decisive control = a **phase-randomized twin (`shape_matched`)** carrying RT-residual's full autocorrelation + heavy-tailed marginal but **zero behavioral content.**

**v5 result (n=10):** `shape_matched` AULC = **172.1**, statistically **tied with residual = 177.4** (residual−shape_matched = **+5.3 [−7.9,+18.5]**, tied at every cap, seed-sign split 5/5). **A content-free shape twin reproduces the entire RT advantage** ⇒ the edge is the target's temporal/distributional *shape* regularizing the tiny-corpus fine-tune, NOT cognitive content. (Residual still beats the smoothed-difficulty and nonlinear-nuisance controls, but one matched control tying it is sufficient to attribute the edge to shape.) G2 power-control re-confirmed PASS (planted prior −548.8 [−593,−505], ~12× MDE). Artifacts: `outputs/e021/{arms_v5_results.json,arms_v5_shard_all.json}`; harness `scripts/{run_e021_v5.py,e021_targets_v5.py}`.

**The three honest claims E021 resolves to (final):**
1. **Surprisal-orthogonality: NULL** — raw ≈ residual; the experiment's specific novelty buys nothing.
2. **Generic word-aligned aux-regularization dominates** (~430 AULC baseline→structured gap; MI-bound consistent).
3. **The RT edge over matched-learnability controls is signal-SHAPE regularization, not cognition** — a phase-randomized content-free twin ties it. Human reading time carries no cognition-specific *trainable* structure here beyond its statistical shape.

**Net:** a clean cross-modal NEGATIVE that extends the fMRI null (E008) to behavioral reading-time data, with the mechanism pinned (shape, not content). Strengthens the Path-A negative paper. Exploratory; **no rung flip** (Erfan records the verdict).

## SUPERSEDED v3 verdict (retained for audit; the v5 status at the top is final)

**INCONCLUSIVE at n=3, with one clean sub-result. Exploratory; no rung flip.** Three honest claims the trustworthy data support:
1. **Surprisal-orthogonality is NULL (clean).** raw ≈ residual (+4.3 [−3.9,+12.6]) — removing the surprisal-predictable component changes nothing. The experiment's *specific novelty* (surprisal-residualization) buys nothing. (This is the DPI prediction borne out — though DPI bounds *information*, not training utility, so it was the wrong reason to assert it pre-hoc.)
2. **Generic word-aligned aux-regularization dominates** (~450 AULC baseline→structured gap; the E004 `frozen` effect at scale). Robust.
3. **The cognition question is UNRESOLVED, not closed.** The residual is the best arm and beats both surrogates *on the mean*, but the CIs touch 0 at n=3 (underpowered) — not a clean positive. AND the intended cognition-exclusion control (log-freq) is **confounded**: it is the *most learnable* target yet probes *worst*, i.e. the learnability-disruption mechanism (from G2v1) contaminates it — so it does NOT cleanly show "any real non-cognitive feature regularizes." Resolving this needs (a) more seeds to tighten the residual−surrogate CIs, and (b) a *learnability-matched* non-cognitive control (log-freq is too trivially predictable).

**Bottom line for the program:** the keystone did NOT deliver a clean main-track positive, and it did NOT deliver a clean negative either. The defensible, paper-ready claim is the *narrow* one — surprisal-residualization specifically buys nothing (raw≈residual), consistent with the thesis arc — plus "generic regularization dominates." The broader "does real cognitive signal help beyond surprisal" is left honestly **underpowered/inconclusive**. **Erfan's call** whether the resolve-it experiment (more seeds + learnability-matched control) is worth the compute, or whether to fold the narrow negative into the Path-A paper and move on. Methodological lesson logged: I flip-flopped (v2 bug-positive → an over-strong DPI "refutation" → this) — don't over-read bug-tainted data, and don't assert an empirical ordering from a theorem about information when the quantity at stake is training utility.

## Interpretation (verdict — NEGATIVE; exploratory pending a clean rerun)

**E021 does NOT support a cognition-specific or surprisal-orthogonal training signal.** The triple dissociation fired as a *statistic*, but two converging panels (counter-argument + first-principles, opus) and a Codex review dismantle the cognition reading:

1. **Surprisal-orthogonality is dead — by theory, not just data.** raw ≈ residual (per-seed raw−residual = −17/+15/−19, paired ≈ 0), so removing the surprisal component — the experiment's entire novelty over Deng'24/BabyLM — changed nothing. And **the DPI makes this mandatory**: the residual is a deterministic function of (RT, surprisal, nuisances), so I(residual; useful) ≤ I(raw; useful) — residualization can only *remove* useful word-aligned variance, never isolate a privileged slice. The design's predeclared "residual ≥ raw, raw ≈ permuted" was in tension with the math.
2. **The effect is generic regularization, not cognition.** ~91% of it is the baseline→any-structured-arm gap (the E004 `frozen` non-specific regularizer at scale; consistent with the MI generalization bound — an aux objective lowers I(W;Zⁿ) and shrinks the cross-domain gap of a tiny-corpus fine-tune). The arm ordering (`raw/residual < random < permuted`, seed-stable) tracks **word-alignment fidelity + real linguistic structure**, not cognitive content — `random_struct` (non-cognitive synthetic) beats `permuted` (destroyed alignment).
3. **The numbers are not yet trustworthy.** Codex found a real Stage-A pad-label bug (pads contribute to LM loss, can inflate the baseline gap) + flaws (seed-invariant permuted/random targets; residualization maybe not out-of-fold; probe init not identical across arms). **The qualitative verdict is robust to all of these** (it rests on raw≈residual/DPI + the converging mechanism), but the magnitudes need a clean rerun before they are recorded as final.

**What this IS (the positive framing of a negative):** a clean cross-modal extension of the E008/E004 line — *cognitive/behavioral signals buy nothing beyond generic word-aligned regularization, and the LM's own surprisal already subsumes the predictable part* — now shown on **behavioral reading-time** data, not just fMRI. This **strengthens the Path-A negative paper** (the matched-control thesis, now multi-modal). The main-track *positive* the keystone hoped for did not appear.

**Decisive finishing control (both panels):** a pure **log-frequency** aux arm. If it also beats permuted/random (it will, per DPI/mechanism), cognition is definitively excluded. Cheap; verdict-confirming, not verdict-changing. **Status: exploratory** (post-lock metric switch + the bug both forbid "promotable"). **No rung flipped — Erfan adjudicates the strategic use of this negative.**


## Retained load-bearing artifacts

| Artifact | SHA-256 |
|---|---|
| `outputs/e021/arms_v5_results.json` | `95c05b8d259d82fb83c84d54c595176198a9ba9cfe50a70941c2cddd24d69b5b` |
| `outputs/e021/arms_v5_shard_all.json` | `b53bf1c88de36b397a9be753587e0e3846fde107c648eb496250850a1b7314e1` |

## Related
- [`status.md`](../status.md) — the canonical status board
