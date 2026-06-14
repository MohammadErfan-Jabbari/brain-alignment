# Upspeed — read first, write last

**Last updated:** 2026-06-14 (Session 13 — autonomous working, forward-program **F1**. **TRIBE Phase-1 FIDELITY =
PASS** (hardened): TRIBE is a faithful in-pipeline fMRI stand-in (beats a strong nuisance floor in higher-order
language Δ=+0.113 [+0.045,+0.181], 6/6). **Phase-2 CEILING = INCONCLUSIVE (real wall):** single-story group-avg
TRIBE explains too little per-vertex real-BOLD variance (LM→TRIBE≈0.03 vs LM→real≈0.18) → the stimulus-subtraction
estimand can't isolate anything; the runner's "Fork-A" flag **FAILED the predeclared vacuity gate ⇒ confirmed
ARTIFACT, NOT escalated** (the oracle warning + vacuity control did their job). A2 reconfirmed on denizenslab.
Two blockers solved (D027 voxel mapping, L037 TRIBE bug). **NO rung flip; NO Fork-A.** Next = **Phase-2 redesign**
(stronger TRIBE target + ≥3 stories + frame-valid estimand), a fresh focused run — then F2/F3/F4.)

> **Canonical state lives in [`ladder.md`](ladder.md)** (rung board + forward program). This is last-session prose.
> With no task, run `/orient`.

## Current state — forward program F1 in progress. Science verdicts UNCHANGED; no rung flipped.

**F1 Phase 1 (E016 TRIBE fidelity) ✅ PASS.** TRIBE-v2 (Meta FAIR; predicts group-averaged E[Y|S] on the
fsaverage5 surface) is validated as a faithful in-pipeline fMRI stand-in for the stimulus-evoked response. On
denizenslab story_11 (n=6 listening), TRIBE-predicted BOLD beats a **strong nuisance floor** (rate + envelope +
phonemes/letters + english1000 PCA-100, FIR, contiguous-CV) in **higher-order language** ROIs (Broca/pSTS/ATFP):
TRIBE r=0.273 vs floor 0.160, **Δ=+0.113, 95% CI [+0.045,+0.181], 6/6 subjects, Wilcoxon p≈0.03**; gradient
lang−motor +0.290 6/6; correct spatial profile (language/auditory high, visual/motor ≈0). Oracle-gated (HOLD→PASS)
+ counter-argument-hardened (the original rate-only floor was a strawman → Δ corrected from inflated +0.165). **This
is a tool-validation gate, NOT a science rung → no ladder flip.**

## Two blockers solved this session (the real work)
1. **Voxel-space mapping (D027).** TRIBE outputs fsaverage5; LeBel ships no precomputed mapper (pycortex-db only).
   Switched F1/F2 substrate to **denizenslab** — turnkey verified `voxel_to_fsaverage` mapper + per-subject
   functional ROI localizers, n=6. fsaverage5 = verified sphere-prefix of fsaverage. `scripts/fsaverage_mapping.py`.
2. **TRIBE long-audio timestamp bug (L037).** `get_audio_and_text_events` cross-joins the full transcript onto each
   60s chunk + double-counts chunk position → 591s speech → 1671s events, preds (1700,20484). Fix: extract words on
   un-chunked audio (correct), then chunk only audio for w2v-bert (single chunk OOMs its O(T²) attention). Now
   preds (700,20484), correct timing. `scripts/tribe_predict_deniz.py` (`_build_events_correct`).

## What to do next — F1-close = E020 (empirical-E[Y|S] ceiling), then F2. REFRAMED S13 (D028, Erfan-agreed).
The S13 TRIBE *stimulus-subtraction* ceiling walled out: TRIBE explains only ~7% of per-vertex real-BOLD variance
on story-listening (LM→TRIBE≈0.03 vs LM→real≈0.18), too weak to subtract — the "Fork-A" flag was a confirmed
artifact caught by the vacuity gate (NOT escalated; L038). **The fix is not to grind a weak TRIBE harder — it is to
use the GROUND-TRUTH empirical E[Y|S]** (cross-subject + cross-repeat average of real fMRI; *is* the stimulus-evoked
expectation by definition; strictly stronger than TRIBE where many subjects heard the same stimulus, which is our
case). → **E020 (NEXT, design LOCKED in `docs/experiments/E020_*.md`):** does the trained LM align to brain signal
beyond E[Y|S]? A_shared=LM→E[Y|S] vs A_resid=LM→ε_s (LOO residual), NC-norm, higher-language, n=6, +untrained floor.
A_resid≈0 within MDE ⇒ Fork-B ceiling; >0 surviving controls ⇒ Fork-A → STOP. **MUST oracle-gate first + handle the
subject-specific-stimulus-deviation leak** (E020 §3) — do NOT rush (two S13 artifacts came from rushing subtle
estimands). Cheap; reuses the S13 machinery. **Then F2 (E019 reproduce-and-control — paper-critical, no TRIBE needed)
→ F3 (I3 n=6 full-FT) → F4 (E015 Q2).** TRIBE kept ONLY for Phase 3 (synthetic-target KD on the no-fMRI corpus) =
optional Fork-B booster, slot after F2 (D028). The matched-ppl spine stands without the ceiling closure.

## Blockers / open loops
- **Both TRIBE predictions cached + ready:** `outputs/E016_tribe/deniz/full/story_11_pred.npz` (text+audio) and
  `.../notext/story_11_pred.npz` (audio-only, features_to_use=['audio'] verified). Per-stimulus → shared across the
  6 subjects. TRIBE env stays isolated in `.venv-tribe`; the operative fixes are in `scripts/tribe_predict_deniz.py`
  (16kHz resample + `_build_events_correct` single-chunk-word + Llama `config_update`); re-apply via the runner,
  not a site-packages patch (tribev2 clone is gitignored).
- **Phase-2 build not started:** needs LM word features on denizenslab + the partial-R² residual + verifying the
  no-text zero-fill path actually drops the text channel inside the model (config says ['audio']; confirm at predict).
- **ANALYSIS-lane flags for Erfan (unchanged, do NOT edit unilaterally):** manuscript r≈−0.92→−0.78; the induction
  null is robust across LoRA+full-FT+objective+capacity; F1 adds TRIBE as a validated stand-in (enables the ceiling).
- **Substrate-switch flag:** F1/F2 now on denizenslab (not LeBel) — D027; Erfan may add LeBel via pycortex-db as a
  robustness substrate on return.

## Key facts
- **Run Python:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache`. TRIBE: `.venv-tribe` (NEVER the thesis
  venv); `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`; ffmpeg installed. GPUs 4× L40S.
- **TRIBE gotchas:** Llama override `config_update={"data.text_feature.model_name":"unsloth/Llama-3.2-3B"}`;
  `average_subjects=True` hardcoded in from_pretrained → output is group-avg E[Y|S], (T,20484); TR=1.0s (real
  2.0045s → resample + lag-align, lag≈7 TR for denizenslab listening). **Always verify the output time-axis length
  against stimulus duration** (L037).
- **Cost:** this session ~$165 at checkpoint. Two engineering walls cleared. Cost discipline: full panel reserved
  for the load-bearing Phase-2 ceiling verdict; Phase-1 (a gate) got counter-argument + empirical controls.
- **Subagent routing (D026):** opus = think/analysis/design (panel, oracle); sonnet = doc-nav/record; haiku =
  mechanical. Codex = code-critic/rescue. fable BANNED.
- **Git:** `main`, push only when asked. ~10+ atomic commits this session.
