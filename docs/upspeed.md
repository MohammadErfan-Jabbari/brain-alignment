# Upspeed — read first, write last

**Last updated:** 2026-06-14 (Session 13 — autonomous working, forward-program **F1**. **TRIBE Phase-1 FIDELITY =
PASS** (hardened): TRIBE is a faithful in-pipeline fMRI stand-in — beats a strong nuisance floor in higher-order
language Δ=+0.113 [+0.045,+0.181], 6/6. Two blockers solved: voxel-space mapping (D027) + a TRIBE long-audio
timestamp bug (L037). **NO rung flip** (Phase 1 is a tool-gate). Next = **F1 Phase 2, the CEILING** — a fresh
focused run; both TRIBE predictions cached. Erfan to issue the `/goal` or let the autonomous loop continue.)

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

## What to do next — F1 Phase 2 (THE CEILING), a fresh focused run (load-bearing, Fork-A-capable)
real-LM-alignment − TRIBE-explained-alignment residual on denizenslab, with the **no-text TRIBE ablation as the
BINDING control** (the margin over lexical-semantics is modest → a residual≈0 only counts if it holds vs BOTH full
and no-text TRIBE, else it's Llama-shared-variance, not the DPI ceiling). Build: LM word features on the denizenslab
story words (reuse `lebel_adapter.lm_word_features`) → fsa5 encoding to real + TRIBE targets → partial-R² residual in
language ROIs. **residual≈0 vs both ⇒ strongest Fork-B with mechanism; residual>0 surviving no-text ⇒ Fork-A →
STOP for Erfan.** Run the FULL thinking panel + Codex on the Phase-2 verdict (deferred from Phase 1, a gate).
Then **F2 (E019 external reproduce-and-control), F3 (I3 denizenslab n=6 full-FT), F4 (E015 Q2)** per the program.

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
