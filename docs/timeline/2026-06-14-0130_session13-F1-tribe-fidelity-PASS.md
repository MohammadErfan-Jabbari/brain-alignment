# Session 13 — F1: TRIBE Phase-1 fidelity (E016) — WORKING (autonomous)

**Date:** 2026-06-14 (started ~00:00) · **Mode:** working (autonomous /goal: forward program F1→F4)
**Lane:** 🔬 implementation, forward-program **F1** (E016 TRIBE ceiling). **Ladder:** NO rung flip (Phase 1 is a
tool-validation gate, not a science rung; L3/F1 stays ❌).

## What ran (Phase 1 = FIDELITY, the gate on the synthetic-target line)
Goal: is TRIBE-v2 (Meta's stimulus→fMRI foundation model, predicts group-averaged E[Y|S] on fsaverage5) a
faithful in-pipeline fMRI stand-in? Two blockers solved en route, then the oracle-gated + panel-hardened gate.

**Blocker 1 — voxel-space mapping (D027).** TRIBE outputs fsaverage5; real BOLD is subject voxels. LeBel ships no
precomputed mapper (only pycortex-db → pycortex/FreeSurfer build). **Switched F1/F2 substrate to denizenslab**
(Deniz 2019): ships a turnkey verified `voxel_to_fsaverage` sparse mapper + per-subject functional ROI localizers
(AC/Broca/pSTS/V1.. ), n=6. fsaverage5 = verified sphere-prefix of fsaverage. `scripts/fsaverage_mapping.py`
(93% fsa5 coverage; validating check: listening reliability lang/aud 0.108 ≫ early-vis 0.026).

**Blocker 2 — TRIBE long-audio timestamp bug (L037).** Feeding the 602s story gave preds (1700,20484): TRIBE's
`get_audio_and_text_events` chunks audio at 60s then cross-joins the FULL whisperx transcript onto every chunk and
double-counts chunk position (start+offset) → 591s speech became 1671s of events, 11× word duplication. whisperx
itself was correct (.tsv 0–591s). Diagnosed to root cause; fix = extract words on the UN-chunked audio (correct
absolute 0–591s) then chunk only the audio for w2v-bert (a single huge chunk OOMs w2v-bert's O(T²) attention,
54GB). preds now (700,20484), span 0–591.3s. Also 16kHz-mono resample for clean whisperx/w2v-bert input.

**Phase 1 gate (oracle HOLD→PASS, then counter-argument-hardened).** Oracle killed the bare spatial-specificity
gate as vacuous → adopted a low-level/strong-nuisance floor TRIBE must BEAT in higher-order language, NC-norm,
locked lag-search, E[Y|S] verified. Built `run_tribe_fidelity.py` (group-avg per-vertex map + per-subject ROI-mean
paired n=6). Caught + fixed a real ridge bug pre-verdict (per-fold centering; BOLD-mean leak had forced alpha=1e5,
making the floor look null). **VERDICT: PASS** — TRIBE higher-lang r=0.273 vs strong floor 0.160, **Δ=+0.113, 95%
CI [+0.045,+0.181], 6/6, Wilcoxon p≈0.03**; gradient lang−motor +0.290 [+0.181,+0.398] 6/6; correct spatial
profile (lang/aud high, visual/motor ≈0); lag-search sharp peak at 7 TR (validates timing fix). **Counter-argument
panel HELD one MATERIAL objection** — the floor omitted the lab's own english1000 lexical-semantic features;
rebuilt the strong floor → Δ corrected from inflated +0.165 (rate-only) to honest +0.113 (still PASS). MINOR
objections (lag, 700-TR tail, estimand) verified + dismissed/carried-forward.

## Verdict & state
**TRIBE is a faithful in-pipeline stand-in (Δ≈+0.11 over a strong nuisance floor, 6/6). No ladder flip** (gate, not
rung). Phase 1 closed + hardened. Both TRIBE predictions cached: full + no-text ablation (features_to_use=['audio'],
verified). Forward program: F1-Phase1 ✅ → **F1-Phase2 (the ceiling) NEXT**.

## What's next to run — Phase 2 (THE CEILING), a fresh focused run (load-bearing, Fork-A-capable)
real-LM-alignment − TRIBE-explained-alignment residual on denizenslab, with the **no-text TRIBE as the BINDING
control** (counter-argument: margin over lexical-semantics is modest → residual≈0 must hold vs BOTH full and
no-text TRIBE, else it's Llama-shared-variance not the DPI ceiling). Build: LM word features on denizenslab story
words (reuse `lebel_adapter.lm_word_features`) → fsa5 encoding to real + TRIBE targets → partial-R² residual in
language ROIs. residual≈0 vs both ⇒ strongest Fork-B; residual>0 surviving no-text ⇒ **Fork-A → STOP for Erfan.**
Run the FULL thinking panel + Codex on the Phase-2 verdict (deferred from Phase 1, a gate, per cost discipline —
counter-argument already applied to Phase 1). Then F2 (E019), F3 (I3 n=6), F4 (E015 Q2).

## Process / cost
Long autonomous session (~$165 at checkpoint). Two genuine engineering walls hit + cleared (voxel mapping; TRIBE
audio bug) — both necessary, both recorded (D027, L037). Checkpointed at the Phase-1/2 boundary per the E016 plan's
own "phases deserve a fresh focused session" philosophy + L031 overshoot guard: Phase 2 is the load-bearing
Fork-A-capable verdict and is best run fresh with a full panel, with both TRIBE predictions already cached.
~10+ atomic commits. No rung flips; no analysis-lane edits.
