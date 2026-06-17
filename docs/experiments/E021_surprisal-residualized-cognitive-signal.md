# Experiment E021 — surprisal-residualized cognitive-signal auxiliary training (the keystone, T1.3)

**Created:** 2026-06-17 · **Status:** running — **G0/G1 PASS (S22); building harness + G2 power gate before the 6 science arms**
**Tree node:** T1.3 (lead Path-B bet) · **Program:** `../expansion-program.md` §6b synthesis · **Mode:** promotable

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
- **The residualization (the novelty — operationalized as conditional information / unique R², cf. `../06-theory-grounding.md`):** for each arm's *base* LM, extract per-word surprisal; regress the cognitive signal on [surprisal + nuisances: word length, log-frequency, position] via ridge; the **residual** is the training target. This isolates the cognition component the model does *not* already encode. **Leakage control (oracle §2a):** the surprisal→signal ridge is fit on **train folds only** and applied to held-out folds — never fit on eval-fold data.
- **Arms (predeclared, matched budget — 6 arms; oracle §3 added the random-structured arm for the triple dissociation):**
  1. **baseline** — no aux objective, matched steps/tokens/params.
  2. **raw-aux** — predict the raw cognitive signal (the Deng'24 / naive form). Predeclared reading: raw ≈ permuted (surprisal-redundant) ⇒ only the residual can differ.
  3. **residualized-aux** — predict the surprisal-residualized signal. *(the test arm)*
  4. **permuted-twin** — predict the *block-permuted* residualized signal — controls for the residual's marginal distribution.
  5. **random-structured** — predict a *fresh* smooth random regressor matched in scale + autocorrelation to the residual (NOT a permutation of the real signal) — the **E004 `frozen` analog**; controls for "any structured aux head regularizes optimization." Cognition-specificity requires (iii) > (iv) **and** (iii) > (v).
  6. **residualized-EEG-aux** — same as (3) with the N400 residual. **Demoted to a cross-modal STRETCH arm (oracle §3):** single-word N400 at 12 subjects is the noisiest target; the **behavioral (eye-tracking) arm is primary**, EEG runs only if it clears the reliability floor.
- **Auxiliary objective:** a light co-trained head predicting the (residualized) per-word target, added to the LM loss with weight λ (small λ-grid); LoRA or light full-FT; **identical optimizer/steps/data budget across arms** (the matched-budget parity is explicit).
- **Downstream metric — PRIMARY = AULC (oracle §4):** area-under-the-learning-curve of held-out-**domain** LM perplexity across a **predeclared** sequence of small data caps (100 / 300 / 1k / 3k tokens), paired per seed. Rationale: integrates the whole low-data regime (no cap-cherry-picking), needs no task-head (no extra variance), and is where a tiny representational prior shows up if anywhere (helps most when data is scarce, washes out as it grows — the *shape* is the signal). **Predeclare the held-out domain + the caps now** (locked: domain = TBD-in-gating, caps = {100,300,1k,3k}). Drop full-data OOD-ppl (E009 showed it inert). *Never* report signal-prediction as a success.
- **Seeds:** ≥3 (stochastic). Paired contrasts over folds × seeds (the E008 clustering pattern).
- **Confound controls:** contiguous / sentence-block splits (anti-leakage); nuisance baselines already inside the residualization (length, frequency, position); the permuted twin is the specificity control; report arm(iii)−arm(iv) after the residualization. ZuCo is small → **predeclare the MDE and run an E008-style power positive-control**; treat a tight null as informative, not as "underpowered, inconclusive."
- **Stop rule / budget:** small (small LM + small data) — target ≤ a few GPU-hours per arm; ≤4 arms in flight on the 4× L40S. Stop when all arms × ≥3 seeds complete or a predeclared positive triggers the Erfan-escalation.
- **Promotable vs exploratory:** promotable only if the matched-budget parity holds, the power positive-control validates the MDE, and the panel survives. Otherwise exploratory.

## Gating sequence — run BEFORE any science arm (oracle HOLD→PASS path)

These cheap measurements decide whether the full 6-arm × ≥3-seed matrix is worth running at all. Run **in order**; abort at the first failure (each abort is a result, recorded).

- **G0 — residual-existence (cheapest; before touching ZuCo).** On a **clean, large** eye-tracking corpus (GECO / Dundee / Provo — bigger N than ZuCo), compute the **unique R² of the cognitive signal NOT explained by base-LM surprisal + nuisances** (length, log-freq, position), train-fold-fit. *If this residual unique-R² is ≈ 0 on clean behavioral data, the whole keystone is vacuous on behavior → KILL the behavioral instantiation (and EEG is hopeless a fortiori); pivot or stop.* This is the single highest-value check and needs no training — just surprisal + ridge.
- **G1 — residual reliability floor (oracle §2b).** For the chosen corpus, report the residual target's split-half / noise-ceiling-normalized reliability. Predeclare the floor: if the residual's reliable variance is statistically indistinguishable from noise at the available N → the test is **vacuous, not null**. Pass required before training.
- **G2 — downstream power positive-control (oracle §1).** Inject a *synthetic* per-word target known to carry learnable, downstream-predictive structure; confirm arm(iii)−arm(iv) **detects it** at the predeclared MDE with the available N. The MDE is computed from the run's own seed variance (L017(3)), NOT borrowed. If the pipeline can't detect a strong injected downstream effect → unpowered by construction → do not run the science arms.

Only if **G0, G1, G2 all pass** do the 6 science arms run.

## Build dependencies (after the gates pass)
1. **Behavioral corpus acquisition + word-alignment** (GECO/Dundee/Provo for scale → ZuCo for the EEG cross-modal arm). *Not on disk.*
2. **Surprisal-extraction + train-fold residualization script** (per-word surprisal from the base LM; ridge fit train-only).
3. **Aux-training loop** (adapt `distill.py`/`run_brain_lever.py` for the co-trained residual-prediction head, matched budget; the AULC eval harness over the predeclared caps).

**Positioning (done S22):** canonical notes written for **Deng'24** (`deng-2024_gaze-supervised-finetuning` — raw synthetic-scanpath order, BERT, in-dist GLUE, no residualization; its own shuffle control gives only +0.33pp over shuffled → supports our prior) and **BabyLM** (`babylm-2025_cognitive-objectives-findings` — cognitive aux ≈ randomized-order null; no submission ever residualized → E021's gap). E021 owns: surprisal-residualization, decoder LM, AULC/sample-efficiency, matched-budget, the random-structured + permuted triple dissociation, the EEG cross-modal arm.

## Iteration log

| Date | Run / seed | Command / config | Result (numbers) | Observation / anomaly | Next |
|---|---|---|---|---|---|
| 2026-06-17 | — | design | — | drafted; oracle HOLD addressed | run gating sequence |
| 2026-06-17 | G0/G1 | `scripts/run_e021_g0g1.py` → `outputs/e021_g0g1/` | residual split-half reliability **0.72** (SB) vs noise ceiling **0.77**; unique-R²(surprisal in RT)=**0.048±0.020**; residual = 77% of RT var | **PASS** — surprisal-orthogonal RT residual is reliable, not noise (Natural Stories, 180 subj, 10k words; GPT-2≈Qwen) | build harness + G2 power control |

## Results (running)

**G0/G1 (residual existence + reliability) — PASS.** On Natural Stories self-paced RT (180 subjects, 10,256 words; GPT-2-small surprisal, by-item 10-fold CV ridge, 25 subject half-splits SB-corrected):
- unique R² of surprisal (+spillover) in RT = **0.048 ± 0.020** — the LM explains *little* of RT (full model incl. nuisances R²=0.226).
- residual fraction of RT variance = **0.765**.
- **residual split-half reliability = 0.720 (SB)** vs by-word RT noise ceiling **0.767** → the surprisal-orthogonal residual is ~94% as reliable as the raw signal: **reliable structure, not noise.** Qwen2.5-0.5B materially identical (0.722 vs 0.767).
- Cross-checks pass: GPT-2/Qwen surprisal agree r=0.91; surprisal↔RT r=+0.20 (canonical positive effect).

**G2 (downstream power positive-control) + the 6 arms — pending** (harness building).

## Interpretation (interim)

The keystone is **viable on behavioral data**: a reliable surprisal-orthogonal training target exists. **Two honest caveats carried forward** (recorded, not buried): (1) surprisal explains only ~5% of RT, so most of the reliable residual is higher-order psycholinguistic structure (integration cost, working memory), not narrowly "the cognition the LM lacks" — the *circularity* worry was overstated for RT; (2) **reliable ≠ downstream-useful** — G0 clears only the noise floor; whether predicting this residual buys anything downstream is what G2 + the triple-dissociation arms decide. A null there still generalizes the fMRI negative; a surviving residualized arm (> permuted AND > random-structured) reopens a cognition-specific positive → escalate to Erfan.
