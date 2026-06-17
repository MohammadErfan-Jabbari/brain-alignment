# Experiment E021 — surprisal-residualized cognitive-signal auxiliary training (the keystone, T1.3)

**Created:** 2026-06-17 · **Status:** design (oracle-gate before any compute)
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

## Predeclared kill / decision rule

- **Null (H1/H3):** arm(iii) − arm(iv) within the predeclared MDE on the *downstream* metric. The contribution is then the cross-modal negative + the residualization lens. (A within-modality gain that the permuted twin also shows = H3 = still negative.)
- **Positive (H2):** arm(iii) − arm(iv) > 0, CI excludes 0, ≥3 seeds, survives the thinking panel. → escalate to Erfan; do NOT flip anything autonomously (a surviving positive is the Fork-A-equivalent STOP condition).
- The success metric is **downstream**, never "predicts the cognitive signal better" (that would be circular — the whole point).

## Design (LOCK before running — pending oracle gate)

- **Base LM:** small decoder, our existing family for continuity — **Qwen2.5-0.5B** (primary) and/or **GPT-2** (replication). Reuse `distill.py` / `run_brain_lever.py` scaffolding (co-trained aux head + λ).
- **Cognitive signal + data:** **ZuCo / ZuCo 2.0** (Hollenstein 2018; simultaneous EEG + eye-tracking during natural reading; ~1.1k sentences, word-aligned; public OSF). Behavioral target = total-reading-time / gaze-duration per word; EEG target = N400-window mean amplitude per word. Backstop for behavioral scale: **GECO / Provo / Dundee** (eye-tracking, larger). *Data acquisition is a prerequisite step (not yet on disk).*
- **The residualization (the novelty — operationalized as conditional information / unique R², cf. `../06-theory-grounding.md`):** for each arm's *base* LM, extract per-word surprisal; regress the cognitive signal on [surprisal + nuisances: word length, log-frequency, position] via ridge on contiguous-split folds; the **residual** is the training target. This isolates the cognition component the model does *not* already encode.
- **Arms (predeclared, matched budget):**
  1. **baseline** — no aux objective, matched steps/tokens/params.
  2. **raw-aux** — predict the raw cognitive signal (the Deng'24 / naive form).
  3. **residualized-aux** — predict the surprisal-residualized signal. *(the test arm)*
  4. **permuted-twin** — predict the *shuffled* residualized signal (word-block-permuted) — the cognition-specificity control.
  5. **residualized-EEG-aux** — same as (3) with the N400 residual (cross-modal arm, ZuCo only).
- **Auxiliary objective:** a light co-trained head predicting the (residualized) per-word target, added to the LM loss with weight λ (small λ-grid); LoRA or light full-FT; **identical optimizer/steps/data budget across arms** (the matched-budget parity is explicit).
- **Downstream metrics (predeclare PRIMARY):** (a) **sample-efficiency** — low-data fine-tune on a held-out task / held-out-domain LM perplexity at a small data cap; (b) **OOD perplexity** — domain-shift held-out text. Primary = sample-efficiency (closest to the "unscooped low-data slice", L008). *Never* report signal-prediction as a success.
- **Seeds:** ≥3 (stochastic). Paired contrasts over folds × seeds (the E008 clustering pattern).
- **Confound controls:** contiguous / sentence-block splits (anti-leakage); nuisance baselines already inside the residualization (length, frequency, position); the permuted twin is the specificity control; report arm(iii)−arm(iv) after the residualization. ZuCo is small → **predeclare the MDE and run an E008-style power positive-control**; treat a tight null as informative, not as "underpowered, inconclusive."
- **Stop rule / budget:** small (small LM + small data) — target ≤ a few GPU-hours per arm; ≤4 arms in flight on the 4× L40S. Stop when all arms × ≥3 seeds complete or a predeclared positive triggers the Erfan-escalation.
- **Promotable vs exploratory:** promotable only if the matched-budget parity holds, the power positive-control validates the MDE, and the panel survives. Otherwise exploratory.

## Dependencies / open before running
1. **ZuCo acquisition + word-alignment pipeline** (download OSF; align EEG/ET to word tokens). *Not on disk.*
2. **Surprisal-extraction + residualization script** (per-word surprisal from the base LM; ridge residualization on folds).
3. **Aux-training loop** (adapt `distill.py`/`run_brain_lever.py` for the co-trained residual-prediction head, matched budget).
4. **Oracle gate** (this design) + a positioning check vs **Deng ACL'24** (raw gaze, BERT, in-dist GLUE, no residualization — being digested) and the **BabyLM** null prior (being digested).

## Iteration log

| Date | Run / seed | Command / config | Result (numbers) | Observation / anomaly | Next |
|---|---|---|---|---|---|
| 2026-06-17 | — | design | — | drafted; oracle-gate pending | acquire ZuCo; oracle review |

## Results

_pending_

## Interpretation

_pending — a null generalizes the fMRI negative across modalities (the surprisal-redundancy claim); a surviving residualized arm reopens a cognition-specific positive (escalate to Erfan)._
