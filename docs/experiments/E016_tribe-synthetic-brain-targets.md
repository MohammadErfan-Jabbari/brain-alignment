---
title: "Experiment — E016: TRIBE-v2 synthetic brain targets — can a brain foundation model break the…"
tags: [experiment]
aliases: [E016]
---

# Experiment — E016: TRIBE-v2 synthetic brain targets — can a brain foundation model break the data-scarcity wall, and what is the ceiling on brain-guided LM training?

**Created:** 2026-06-12 · **Status:** **P0 PASSED (2026-06-13); now the FORWARD-PROGRAM F1 = NEXT TO RUN** (it was
the I4 capstone/last of the original implementation roadmap, but the S12 planning swarm re-sequenced it to the
front — the ceiling is the cheapest decisive next experiment). After I1 (E015-expand ✅), I2 (E017 ✅). P1→P3 design
refined below (see "PHASE 1/2 DESIGN — REFINED"). · **Mode:** working (design→run→judge)
**Trigger:** Meta FAIR's **TRIBE v2** (d'Ascoli et al., ICLR 2026; arXiv 2605.04326; weights `facebook/tribev2`)
— a trimodal (video/audio/text) foundation model that predicts fMRI BOLD for *arbitrary* naturalistic
stimuli, SOTA on Algonauts 2025. Erfan flagged it (2026-06-12) as a possible answer to the data-scarcity
limitation that has bounded E001→E015. This doc reads the paper, analyses the idea against our own theory,
and locks a phased, kill-gated program.

---

## 1. What TRIBE v2 is (deep read)

A deterministic **encoder** Ŷ = f(S): stimulus S (video, audio, text) → predicted fMRI on the fsaverage5
cortical mesh (~20,484 vertices) + 8,802 subcortical voxels.
- **Extractors (frozen):** text → Llama-3.2-3B (timed, k=1024-word context, D=2048); audio → Wav2Vec-Bert-2.0
  (D=1024); video → V-JEPA-2-Giant (D=1280). Concatenated → D_model=1152.
- **Core:** Transformer (8 layers, 8 heads) over T=100 s windows at 2 Hz → pooled to 1 Hz fMRI rate.
  ~1B learnable params. Trained MSE on ~1000 h fMRI / 720 subjects (≈25 deep training subjects).
- **Subject block:** subject-conditional linear readout; **"unseen-subject" mode** (subject-dropout p=0.1)
  predicts the **group-averaged** response zero-shot — and does so *better than any single subject's
  group-predictivity* (Fig 3; HCP R_group≈0.4). Can be fine-tuned per subject on ≤1 h data.
- **Validated:** beats linear/FIR several-fold; recovers FFA/PPA/EBA/VWFA, language localizers, TPJ/MTG
  emotional-vs-physical-pain in-silico; log-linear data scaling, no plateau.
- **Inference API:** `TribeModel.from_pretrained("facebook/tribev2")`; `model.predict(events=df)`. **Text input
  is routed text → gTTS audio → ASR word-timings → text+audio embeddings** (so "text-only" still synthesises
  audio; it remains a deterministic function of the input text). 5 s hemodynamic offset built in.

**The one property that drives everything below:** TRIBE's output is a **deterministic function of the
stimulus**, and its strongest mode estimates the **group-averaged / shared stimulus-evoked response**
Ŷ ≈ E[Y|S].

---

## 2. The information-theoretic spine (why this is the right tool, and its hard ceiling)

Erfan's Markov chain (R05): **θ\* → S → R(S) → Y**, with **Y ⊥ θ\* | S**.
(θ\* = the LM's params/task; S = stimulus; Y = fMRI.)

**(a) No information beyond the stimulus — a theorem, not an experiment.** TRIBE's Ŷ = f(S) is a deterministic
function of S, so by the data-processing inequality I(Ŷ; Z) ≤ I(S; Z) for any Z. The synthetic fMRI carries
**zero** information not already in the stimulus. So idea-2's "does it contain info beyond the stimulus?" is,
at the level of Shannon information about the stimulus, answered *a priori*: **no.**

**(b) The operative ceiling (the genuinely useful insight).** The Markov chain says, *given the stimulus*, the
real brain response Y is independent of θ\*. Decompose Y = E[Y|S] + ε. The residual ε (subject-specific
state, attention, priors, scanner noise) is — by Y ⊥ θ\* | S — **independent of the LM task**: it is noise for
our purposes. Therefore **the entire θ\*-relevant content of the brain response lives in E[Y|S], the
stimulus-predictable part — which is exactly what TRIBE estimates.** Consequence:

> **TRIBE-synthetic fMRI is an UPPER BOUND on the utility of brain alignment for training a stimulus-trained
> LM.** If distilling toward TRIBE's (dense, denoised, unlimited) target buys ~0 at matched perplexity, then
> *no* brain signal — real or synthetic — can buy more, because the rest of the brain response is
> θ\*-independent noise. A null at the ceiling closes the direction with a clean mechanism (strongest Fork-B).
> A *positive* at the ceiling reopens Fork-A and tells us how much head-room real (noisier) data forfeits.

**(c) What "unique" means — three baselines, three answers.** Idea-2 must not conflate them:
- beyond the stimulus S → **0** (theorem, (a)).
- beyond *linear* language nuisances (word-rate/length/static-embeddings — the E006 nuisance set) → **likely >0**,
  because f is a *nonlinear, brain-derived* transform that linear features don't span. This is measurable and
  is the "re-coordinatization" the brain target could in principle teach (the distillation "dark-knowledge"
  channel: no new info, possibly-useful structure).
- beyond *the LM-being-distilled's own representation* → **the quantity that matters**; our nulls
  (E008/E011/E013b/E013) predict ≈0 in the *useful* sense. Phase 2 measures it directly.

This is the course-grounded version (06-theory-grounding.md): conditional-MI = unique-R², DPI, rate-distortion.
TRIBE turns the abstract DPI argument into a *measurable* stimulus-subtraction.

---

## 3. The three ideas (Erfan's), adjudicated

1. **"Solve data scarcity by generating fMRI for all training text."** *Partly — with a catch.* It removes the
   real limitation that bounded E001→E015: we can now build a **dense per-token brain target for arbitrary
   training text**, at unlimited scale. But TRIBE predicts E[Y|S] = the **shared stimulus-evoked response** —
   exactly the group-averaged target that E008/L016 showed *manufactures apparent-but-not-real per-individual
   brain-specificity* (the +0.0081→+0.00010 ~80× collapse). So scaling it most likely **re-creates the
   averaging-confound regime at scale** — i.e. predicts a null. Value = it removes the *scarcity excuse*, making
   that null far stronger and publishable; it does **not** add unique brain signal (it can't, by §2a).
2. **"Does the synthetic fMRI contain info beyond the stimulus?"** *No, beyond S (theorem); yes, beyond linear
   language baselines; ≈0 in the useful sense beyond the LM's own rep.* This is the **theoretical spine** —
   formalised in §2 and measured in Phase 2. Erfan's instinct is exactly right; the rigor is in choosing the
   baseline.
3. **"Does it fix what made E1→E15 fail?"** *It fixes scarcity and the weak/noisy-target problem; it cannot fix
   the fundamental null if the null is real.* Specifically it gives a **denoised, dense, high-SNR** target that
   could let the induction lever *grip* where real single-subject BOLD couldn't (E013's manipulation failed its
   precondition — real-target tuning never rose above base). TRIBE is the cleanest candidate to finally meet
   that precondition. If, even so, the matched-ppl gain is null → the strongest possible Fork-B.

## 4. Additional angles (agent-proposed)

- **D (crown jewel — the upper-bound / stimulus-subtraction):** real-fMRI alignment − TRIBE-fMRI alignment =
  the **non-stimulus-predictable** component of brain alignment, i.e. the genuine "unique brain" signal the
  whole thesis hunts. By §2b that residual is θ\*-noise, so the *prediction* is ≈0; measuring it ≈0 on real
  LeBel voxelwise data is the sharpest statement of Fork-B we can make. >0 would be a genuine surprise
  (Fork-A reopens). **This is the highest-leverage, lowest-cost experiment.**
- **A (the empirical clincher):** scaled synthetic-target distillation — KD vs KD+TRIBE-brain vs
  KD+TRIBE-permuted at **matched perplexity**, on a real corpus. Arm-equality → null at scale, scarcity removed.
- **B (the positive-result long shot):** use TRIBE not as a *target* but as a **brain-salience weighting** over
  tokens/data (a curriculum / data-selection signal). Different use of the same chain: not adding info, using
  brain-derived weighting. Higher-risk, higher-novelty; only if A/D leave a door open.
- **C (mandatory fidelity gate):** before trusting any of the above, verify TRIBE behaves like real fMRI *in our
  pipeline* — re-run A2 (trained vs untrained LM unique-R²) against TRIBE targets. If the trained-LM advantage
  replicates, TRIBE is a faithful stand-in; if not, the synthetic-target line is moot.

**Novelty / scoop check:** TRIBE is an *encoding* paper; it does not train LMs from synthetic fMRI. Toneva-Wehbe
2019 / Vattikonda 2025 brain-tune models but against *real* data and without the matched-ppl control. "Use a
brain foundation model as a denoised dense target + establish the information-theoretic ceiling on brain-guided
LM training" is unclaimed. TRIBE dropped days ago → **speed matters** (others will try the obvious thing).

---

## 5. The program — phased, dependency-ordered, kill-gated

Each phase has a **predeclared decision rule**; the autonomous loop executes the next phase only if the gate
passes. All alignment numbers use the locked protocol (contiguous/story-CV splits, per-kind permuted twin,
matched-ppl intercept, nuisance baselines — L003). **No rung flips without Erfan.**

### Phase 0 — GATE: get TRIBE running text-only (in flight, `outputs/E016_tribe/install.log`)
- Isolated venv `data/paper-repos/tribev2/.venv-tribe` (must NOT perturb the thesis env: TRIBE wants
  numpy==2.2.6, torch 2.5–2.7, custom deps neuralset/neuraltrain/exca).
- Confirm `TribeModel.from_pretrained("facebook/tribev2")` loads + `predict` runs on a sample text → (T, ~20k)
  BOLD. Risks: gated Llama-3.2-3B (HF token at `~/.cache/huggingface/token`); gTTS needs network; extractor
  weights are many GB.
- **WALL condition (predeclared):** if TRIBE cannot be made to run on a sample within a focused effort
  (deps unresolvable / gated weights inaccessible / OOM on 1×L40S), **document the wall in this doc + the
  timeline, fall back to the IMPLEMENTATION-lane alternatives** (denizenslab full-FT door, E013 §"two routes";
  or E015 family-expansion), and do NOT spin on it. Codex (`codex:codex-rescue`) is the second-implementation
  resort for a gnarly install/inference bug.

### Phase 1 — FIDELITY (idea C): is TRIBE a faithful fMRI stand-in *in our pipeline*?
- Generate TRIBE targets for the LeBel stories (and/or Tuckute sentences) we already have real fMRI for.
- Re-run the A2 contrast: trained-LM vs untrained-LM unique-R² **against TRIBE targets**, same nuisance set.
- **Decision:** trained > untrained replicates (the E002/E006 signature, sign + rough magnitude) → TRIBE
  faithful → proceed. Replicates weakly/not at all → TRIBE doesn't carry the structure our thesis is about;
  record as a bounded result and stop the synthetic-target line (do not build Phase 3).
- *Bonus contribution:* correlate TRIBE-vs-real on the same voxels (does TRIBE predict the voxels our pipeline
  finds informative?).

### Phase 2 — THE CEILING (idea D + idea 2): stimulus-subtraction on real data
- On real LeBel voxelwise (UTS01/02/03, the E006 harness): compute (i) real-fMRI unique-R² of the trained LM;
  (ii) alignment of the same LM rep to **TRIBE-predicted** BOLD; (iii) the **residual** = real − TRIBE-explained
  = the non-stimulus-predictable brain alignment. Also the conditional-info decomposition: unique variance of
  TRIBE targets over (a) linear language nuisances, (b) the LM's own hidden states.
- **Predeclared interpretation:** residual ≈ 0 (within MDE) → the brain's unique-beyond-stimulus signal is
  empirically null → the *ceiling* on brain-guided training is the stimulus-predictable part → **strongest
  Fork-B, with mechanism.** Residual clearly > 0 → a real non-stimulus brain signal exists → **Fork-A reopens**
  (high-value surprise; escalate to Erfan before building on it).
- Pure analysis (TRIBE inference + ridge); **no training** → the cheapest decisive experiment. **Run before Phase 3.**

### Phase 3 — THE CLINCHER (idea A): scaled synthetic-target distillation, matched perplexity
- Only if Phase 1 passes AND Phase 2 is informative. Three arms at matched ppl on a real KD corpus:
  (1) KD-only; (2) KD + TRIBE-brain-MSE (student hidden → TRIBE BOLD readout); (3) KD + TRIBE-permuted twin.
- **Predeclared kill:** arm2 ≈ arm3 ≈ arm1 at matched ppl (paired, powered, ≥3 seeds) → the dense synthetic
  brain target adds nothing beyond a stimulus-correlated regularizer → **null at scale, scarcity excuse
  removed** (the publishable null). arm2 > arm3 at matched ppl, CI excludes 0 → a real brain-specific training
  gain emerges only at scale/SNR → **Fork-A-qualifying** (escalate). Multi-day GPU build.

## 6. What a publishable result looks like (the target Erfan set: A\*-workshop/main-track-grade)
Either outcome is a paper, because the ceiling argument (§2b) makes the *null informative*:
- **Most likely (null):** *"Brain foundation models let us put an upper bound on brain-guided LM training — and
  it is null: even unlimited, denoised, dense synthetic brain targets do not improve a language model beyond a
  stimulus-correlated regularizer at matched perplexity, because the brain's training-useful signal is its
  stimulus-predictable component, which a text-trained LM already captures (DPI). We give the matched-ppl +
  permuted-twin + stimulus-subtraction protocol and the information-theoretic explanation."* Subsumes our whole
  Fork-B program and removes its biggest reviewer objection (scarcity/SNR).
- **Surprise (positive):** Phase 2 residual > 0 or Phase 3 arm2>arm3 → a non-stimulus-predictable, training-useful
  brain signal exists → reframes the thesis toward Fork-A; escalate immediately.

## 7. Feasibility snapshot (2026-06-12, as set up)
Repo cloned → `data/paper-repos/tribev2`. Clean inference API confirmed. Deps: custom Meta `neuralset==0.0.2`/
`neuraltrain==0.0.2`/`exca==0.5.20` + x_transformers + gtts (network) + transformers. HF token file present;
Llama-3.2-3B not cached + likely gated. GPUs 4×L40S free. Isolated install launched (Phase 0 in flight).
**Hard line unchanged:** TRIBE produces no science number that flips a rung; verdicts are Erfan's, numbers come
from this brain. TRIBE is a *tool* (a denoised stimulus→brain oracle), not an adjudicator.

## P0 STATUS UPDATE (2026-06-13, S12 autonomous — main blocker SOLVED, predict-verify is the next step)
Reached I4 after completing I1 (E015 law r≈−0.78) + I2 (E017 full-FT induction null). P0 diagnosis + de-risk:
- **`import` OK** (S11 install + this session re-confirmed: `IMPORT OK` in `.venv-tribe`).
- **The gated-Llama blocker is REAL and now PATCHED.** TRIBE's text extractor is `meta-llama/Llama-3.2-3B`
  (`tribev2/grids/defaults.py:28`), which is **HF-gated for our token** (download "Access denied. requires
  approval") and the cache is **incomplete** (76K — config/README only, no weights → can't load offline). This is
  the same gate hit in I1. **Workaround applied:** patched `grids/defaults.py:28` → **`unsloth/Llama-3.2-3B`**
  (the identical *base* weights, non-gated, already cached from I1; vocab 128256, 28 layers — a faithful
  substitution since it is the same model re-uploaded). `.bak` saved. **[SUPERSEDED — see P0 reproducibility
  below: the defaults.py patch is NOT the operative fix; the working override is the `config_update` runtime
  argument, which needs no re-apply after a re-clone. The defaults.py patch is harmless but redundant.]**
- **Remaining P0 (the next session's first step):** build a text-events DataFrame (`tribe_demo.ipynb` /
  `get_events_dataframe` is the template), then `TribeModel.from_pretrained("facebook/tribev2")` + `.predict(...)`
  on a sample → expect (T, ~29k) BOLD. This pulls **facebook/tribev2 weights + Wav2Vec-Bert-2.0 (audio) + possibly
  V-JEPA-2-Giant (video) + gTTS (NETWORK)** — multi-GB downloads + a network round-trip (text→gTTS audio→ASR
  word-timings→text+audio embeddings, per §1). Predeclared P0 WALL (§Phase 0) still applies if these are
  unresolvable. **Then Phase 1 (fidelity) → Phase 2 (the ceiling — cheapest decisive, run first).**
- **→ P0 GATE PASSED (2026-06-13 02:16).** `TribeModel.from_pretrained("facebook/tribev2", config_update=...)`
  + `get_events_dataframe(text_path=...)` + `predict()` ran end-to-end on a sample sentence →
  **`preds shape (11, 20484)`** (11 event-bearing segments × 20,484 fsaverage5 cortical vertices; BOLD mean
  0.011, std 0.103, range [−0.36, 0.76] — sane). Verified in `outputs/E016_tribe/p0_verify2.log` (+ `/tmp/tribe_p0_verify.py`).

### P0 reproducibility — the ACTUAL fixes (supersedes the defaults.py note above)
1. **The operative Llama override is `config_update`, NOT the grids/defaults.py patch.** The pretrained extractor
   spec comes from facebook/tribev2's **downloaded `config.yaml`** (`data.text_feature.model_name = meta-llama/
   Llama-3.2-3B`), which overrides grids/defaults.py. The working fix:
   `TribeModel.from_pretrained("facebook/tribev2", config_update={"data.text_feature.model_name": "unsloth/Llama-3.2-3B"})`
   (identical base weights, non-gated, cached). The other 3 extractors are non-gated: `facebook/dinov2-large`
   (image), `facebook/w2v-bert-2.0` (audio), `facebook/vjepa2-vitg-fpc64-256` (video; auto-skipped for text-only
   input — "Removing extractor video as there are no corresponding events").
2. **System dep: `ffmpeg` required** (whisperx/torchcodec decode the gTTS mp3 for ASR word-timings). Installed via
   `sudo apt-get install -y ffmpeg` (passwordless sudo works in this container; ffmpeg 6.1.1 at /usr/bin/ffmpeg).
3. **Auto-downloads on first predict:** spaCy `en_core_web_lg` (400MB), the 4 extractor weights, tribev2 `best.ckpt`.
   gTTS needs general network (works). cache_folder = `/home/centcom/data/tribe_cache`.
4. Text path = text→gTTS audio→whisperx ASR→word events→text+audio embeddings (deterministic fn of input text).

**→ Phase 1 (FIDELITY) is the next step** (a fresh focused run): generate TRIBE targets for the LeBel/Tuckute
stimuli we have real fMRI for, re-run the A2 trained-vs-untrained unique-R² contrast against TRIBE targets
(same nuisance set), decide if TRIBE is a faithful in-pipeline stand-in → then Phase 2 (the ceiling, cheapest
decisive). **Why checkpoint here:** P0 is a clean gate boundary; Phases 1–3 are substantial experiments
deserving a fresh focused session (the capstone is a multi-day build). Session S12 cost ~$310; blocker fully
solved + verified.

## PHASE 1/2 DESIGN — REFINED by the planning swarm + Codex (2026-06-13, S12). Adopted into the program.
A 4-lens panel (counter-argument/premortem/first-principles/lit-scout) + a Codex feasibility pass hardened the
Phase 1/2 design. **Three changes are now part of the locked program:**
1. **[PREREQUISITE — the real blocker, do FIRST] Voxel-space mapping.** TRIBE outputs **fsaverage5 cortical
   surface** (20,484 vtx); LeBel real BOLD is **volumetric subject-space** (~80–93k voxels per subject, verified).
   There is NO existing bridge in our pipeline. Phase 1/2 cannot produce a number until this is solved — either
   [NOTE: the earlier `grids/defaults.py:28` patch is SUPERSEDED — the operative Llama override is the
  **`config_update={"data.text_feature.model_name": "unsloth/Llama-3.2-3B"}`** *runtime argument* to
  `from_pretrained` (see "P0 reproducibility" below); it needs no re-apply after a re-clone, just use the argument.]
  (a) map LeBel voxels → fsaverage5 (the LeBel/deep-fMRI-dataset preprocessing likely already has a pycortex/
   FreeSurfer surface transform — look there first), or (b) project TRIBE vertices → volume. Resolve before any
   fidelity/residual computation. (Codex: this is the #1 MUST-DO.)
2. **[Phase 1 fidelity — use SPATIAL-SPECIFICITY, the naive check is circular] (counter-argument).** Do NOT use
   "trained-LM > untrained-LM unique-R² against TRIBE targets" as the fidelity gate — a trained LM and TRIBE
   *both* encode the stimulus, so that comparison passes even if TRIBE predicts text-structure, not brain. **Use
   instead: per-voxel/region spatial correlation of TRIBE-predicted vs REAL BOLD — expect language regions HIGH,
   early-visual LOW** (spatial specificity). Temporal alignment reuses `lebel_adapter.py`'s TR-trim logic; region
   labels from an fsaverage5 parcellation once in common space.
3. **[Phase 2 — the NO-TEXT-EXTRACTOR ablation is a REQUIRED control] (counter-argument, the sharpest hole).**
   TRIBE's text extractor IS **Llama-3.2-3B**. So "alignment to TRIBE-predicted BOLD" is partly "alignment to
   Llama features" — a residual ≈ 0 in Phase 2 could be a **Llama-shared-variance artifact**, NOT the DPI
   ceiling. **Required control:** run a **no-text TRIBE variant** (audio+video only) — Codex confirms feasible via
   `config_update={"data.features_to_use": ["audio","video"]}` (verify the zero-fill path in `model.py` is hit,
   not assumed; a graded random-text-extractor ablation is the cleaner-but-optional upgrade). **The ceiling claim
   (residual ≈ 0 ⇒ Fork-B) is only valid if the residual collapses against BOTH the text-augmented AND the no-text
   TRIBE.** If only the text-augmented collapses → it's the Llama confound, not the DPI mechanism.
**Theory caveats to carry (first-principles):** (a) state **Y ⊥ θ\* | S as an assumption**, not a derivation;
(b) the DPI ceiling I(Ŷ;Z) ≤ I(S;Z) is sound (Ŷ=f(S) deterministic); (c) "residual ≈ 0" decisiveness depends on
the fidelity gate (#2) + the no-text control (#3) both passing. **A clean Fork-B needs all three; a residual > 0
that survives the no-text control = a genuine Fork-A surprise → STOP for Erfan.**

---

## F1 EXECUTION LOG (S13, 2026-06-14, autonomous working)

### Step 1 — voxel-space blocker RESOLVED (substrate = denizenslab; D027)
The #1 prerequisite is solved. **LeBel ships no precomputed mapper** (only `pycortex-db/` + `freesurfer_subjdir/`
on OpenNeuro → a pycortex+FreeSurfer build). **denizenslab ships the existing transform**: per-subject sparse
`voxel_to_fsaverage` CSR (327684×n_vox), local + verified, **plus per-subject functional ROI localizers**
(V1–V4/AC/Broca/pSTS/FFA/EBA/…) in the same voxel space. fsaverage5 = the verified sphere-prefix of fsaverage
(nilearn sphere coords, max diff **0**) → a direct 20,484-col subset matching TRIBE's output layout
(LH 0:10242, RH 10242:20484). `scripts/fsaverage_mapping.py` builds + verifies it: 93% fsa5 coverage, and the
validating check — **listening split-half reliability lang/aud=0.108 ≫ early-vis=0.026** (correct spatial pattern).
Substrate decision (D027): F1/F2 on denizenslab, n=6 (subjects 01/02/03/05/07/08), reusing the F3 dataset.

### Step 2 — Phase 1 FIDELITY: locked design (spatial specificity, non-circular)
**Question:** Is TRIBE a faithful in-pipeline fMRI stand-in? (gate on the synthetic-target line.)
**Test (NOT trained>untrained — that is circular per the refined design):** per-vertex temporal correlation of
TRIBE-predicted vs REAL BOLD, summarized by **spatial specificity** — language/auditory ROIs HIGH, early-visual LOW.

- **Stimuli → TRIBE:** feed each denizenslab story's REAL `story_NN.wav` (audio path → w2v-bert audio + Llama-from-ASR
  text extractors; the faithful multimodal prediction, no gTTS). `average_subjects=True` → TRIBE predicts the
  group-averaged E[Y|S] (the §2 quantity). Output (T_tribe, 20484) fsaverage5, in `.venv-tribe`, handed off as `.npy`.
- **Real BOLD → fsa5:** denizenslab listening responses (T, n_vox) → (T, 20484) via `voxels_to_fsa5`.
- **Temporal alignment (the main engineering risk):** TRIBE TR vs denizenslab TR (2.0045 s) differ; `predict` drops
  empty segments. Use the returned segment timings to build TRIBE's time grid, resample onto the real `tr_times`
  (Lanczos window=3, the lebel_adapter convention), trim edges. **Verify alignment empirically** by a lag-search
  (max cross-correlation on high-reliability auditory vertices should peak at ~0 lag); record the chosen lag.
- **Metric:** per-vertex r_v = corr(Ŷ_v, Y_v) over TRs; spatial-specificity = mean r_v in {AC,Broca,pSTS,sPMv,ATFP}
  vs {V1,V2,V3,V3A,V3B,V4,V7}, per subject; paired contrast across n=6 (mean, 95% CI, sign test). Cross-check ROI
  labels against a standard fsaverage5 atlas (nilearn Destrieux) as an independent specificity readout.
- **Decision rule (predeclared):** TRIBE faithful ⇒ lang/aud correlation clearly >0 AND clearly > early-visual,
  consistent across subjects (paired CI excludes 0). Faithful → proceed to Phase 2. Weak/no specificity → record
  bounded result; do NOT build Phase 3. **No rung flips; this is a tool-validation gate, not a science verdict.**
- **Controls/caveats:** raw corr is bounded by sqrt(noise-ceiling) — fine for the *contrast* (visual is noisy too);
  report noise-ceiling-normalized specificity as a secondary. Listening is primary (audio drives TRIBE's strongest
  modality); reading (text-only path) is a secondary fidelity check.

### Step 3 — Oracle gate on Phase 1 = HOLD → revised to PASS (2026-06-14)
The pre-compute oracle (opus) returned **HOLD**: the bare spatial-specificity gate (lang/aud > early-visual on
listening) is **vacuous** — auditory cortex tracks any audio envelope and early-visual is near-zero reliability
(0.026), so the contrast is guaranteed regardless of TRIBE fidelity (the same envelope-confound the refined design
rejected for trained>untrained, reintroduced in spatial clothing). Four must-fixes, **all adopted**:

1. **[F1, the killer] Low-level-encoder positive control + higher-order gradient + NC-normalization as PRIMARY.**
   The gate must be able to FAIL. New decision rule: TRIBE's per-vertex fidelity must beat **(a)** a low-level
   ridge encoder floor — (audio envelope + word-rate + phoneme-rate + word-length + log-frequency) → real BOLD,
   contiguous-block CV — **(b)** in *higher-order* language ROIs (Broca/pSTS/ATFP/sPMv, NOT just AC which is
   envelope-trackable), with **(c)** a within-cortex gradient (higher-order language HIGH vs somatomotor M1/S1 LOW,
   both non-visual), on **NC-normalized** per-vertex r (r_v/√NC_v) as the primary metric. lang/aud-vs-early-visual
   is demoted to a sanity check. **KILL** if TRIBE ≈ the low-level encoder in higher-order language (then TRIBE is
   just a fancy stimulus regressor and the synthetic-target line is dead).
2. **[F2] Noise ceiling exists ONLY for story_11** (the 2-repeat val; trn stories are single-repeat). Protocol
   locked: **fidelity computed on story_11** ("wheretheressmoke", 311 TRs, 2 reps → NC + mean-of-reps target),
   **n=6 subjects** paired (TRIBE pred is per-stimulus → ONE prediction shared across subjects). trn stories =
   optional secondary *unnormalized* replication.
3. **[F3] E[Y|S] verified:** `from_pretrained` hardcodes `average_subjects=True` (demo_utils.py:218); output is
   (T,20484) with no subject axis = the group-averaged estimand. Asserted in the runner so a config change can't
   silently swap it. (Oracle examined only the runner, which inherits this from from_pretrained.)
4. **[F4] Temporal alignment locked.** TRIBE 1.0 Hz contiguous-from-t=0 (remove_empty_segments=False) → resample
   onto the real 2.0045 s TR grid. **Pre-registered lag-search:** global integer-TR lag chosen by max mean-corr on
   high-NC auditory (AC) vertices, **constrained to [−2,+2] TR**; argmax outside the window ⇒ ABORT (pipeline bug),
   do NOT accept silently. Both signals are already hemodynamic (TRIBE bakes in a 5 s offset) → a small residual
   lag is expected; we accept a vertex-constant lag and report it. Silence-TR mismatch (story_11 audio 627.7 s vs
   311 TR×2.0045=623 s ⇒ ~3 TR) handled by trimming to the overlap after lag alignment.

**Plus two confound controls carried in:** (i) **mapper-smoothing** — the voxel→fsaverage projection low-passes
spatially, which can inflate ROI correlations; re-check the higher-order-language-vs-floor contrast restricted to
fsa5 vertices with single-voxel support. (ii) **group-avg-TRIBE vs per-subject-real** does NOT bias Phase 1 (it
attenuates all r uniformly by √NC → safe direction) but **pre-biases the Phase-2 residual toward an OVER-estimate
of unique signal** (conservative for declaring Fork-B, but could manufacture a false Fork-A) — so in Phase 2 the
residual is explicitly framed as *against E[Y|S] = an upper bound on non-stimulus brain signal*; a Fork-A surprise
must survive that framing + the no-text ablation. Recorded now, actioned at Phase 2.

**Verdict: design revised → PASS.** Implemented in `scripts/run_tribe_fidelity.py`. TRIBE story_11 prediction
generating (`outputs/E016_tribe/deniz/full/`).

### Step 4 — Phase 2 (THE CEILING) design skeleton (drafted while Phase 1 runs; oracle-gate after Phase-1 PASS)
**Only run if Phase 1 PASSES.** Quantity: the **non-stimulus-predictable** component of brain alignment =
real-fMRI LM-alignment − TRIBE-fMRI LM-alignment. By the spine (Y⊥θ\*|S), the prediction is **≈0** (strongest
Fork-B); a residual >0 surviving the no-text ablation = Fork-A surprise → STOP for Erfan.

- **Substrate/space:** denizenslab story_11 (+ optionally more stories), fsaverage5, group-avg real BOLD (the
  estimand-matched, high-SNR target; Phase-1 machinery reused: `fsaverage_mapping`, lab-aligned grid, the locked
  lag for TRIBE). LM = the GPT-2/Qwen rep used through E006/E013 (verdict-layer hidden states via the
  `lebel_adapter.lm_word_features` logic, ported to denizenslab textgrids/words).
- **Three encoding fits (per vertex, contiguous-CV, ridge), unique-R² style:**
  (i) real-BOLD unique-R² of the LM rep over the low-level nuisance (the E006 protocol) = "real alignment";
  (ii) TRIBE-BOLD unique-R² of the same LM rep over the same nuisance = "TRIBE-explained alignment";
  (iii) **residual** = variance in real-BOLD–LM-alignment NOT captured by the TRIBE target. Operationalize as:
  align the LM rep to real BOLD after partialling out the TRIBE-predicted BOLD (TRIBE preds as additional
  regressors), vs the LM-alignment to TRIBE itself. Report the residual unique-R² with CI, in language ROIs.
- **REQUIRED no-text ablation (oracle F3 of the refined design):** TRIBE's text extractor IS Llama-3.2-3B, so
  "LM-alignment to TRIBE" is partly Llama-shared-variance. Re-run with a **no-text TRIBE** (audio-only:
  `config_update={"data.features_to_use":["audio"]}` for the audio input; verify the zero-fill path is hit). The
  ceiling/Fork-B claim (residual≈0) is valid ONLY if it holds vs BOTH full and no-text TRIBE; a residual that
  collapses only against full-TRIBE = the Llama confound, not the DPI ceiling.
- **Estimand caveat (carry from Step 3):** the residual is computed against group-avg E[Y|S] → it is an UPPER
  BOUND on unique non-stimulus signal (conservative for Fork-B; a Fork-A must survive this + the no-text ablation).
- **Decision:** residual CI includes 0 (within the E006-scale MDE) vs both TRIBE variants ⇒ the ceiling is the
  stimulus-predictable part ⇒ strongest Fork-B with mechanism. residual CI excludes 0 surviving no-text ⇒ Fork-A
  → STOP for Erfan. Panel (D017) + Codex after the verdict.

### Step 5 — Phase 1 FIDELITY VERDICT: PASS (2026-06-14). TRIBE is a faithful in-pipeline stand-in.
After the TRIBE long-audio timestamp bug (L037; events now span 0–591.3 s, preds (700,20484)) and the
ridge-centering fix, the locked gate ran on denizenslab story_11, n=6 listening.
- **Timing fix validated:** the TRIBE↔BOLD lag-search on AC is sharply unimodal, peak at **lag=7 TR**
  (AC corr 0.251, sharpness 0.193; profile rises 0.03→0.08→0.11→0.18→0.25 then falls) — a true interior
  peak (≈5 TR lead silence + HRF), exactly the oracle's pre-registered sanity check.
- **GATE (per-subject ROI-mean, n=6 paired):** TRIBE beats the low-level floor in **higher-order language**
  (Broca/pSTS/ATFP/sPMv): **Δ = +0.142, 95% CI [+0.053, +0.232], 6/6 subjects positive.** PASS.
- **Gradient:** higher-order-language − somatomotor = **+0.290 [+0.181, +0.398], 6/6.** PASS.
- **Group per-vertex (high-SNR, estimand-matched to E[Y|S]):** higher_lang TRIBE 0.222 vs floor 0.057
  (Δ+0.165, ~4×); auditory 0.251 vs 0.167; early_vis 0.003 vs −0.118; somatomotor 0.007 vs −0.067 — TRIBE
  predicts language/auditory HIGH and visual/motor ≈0, the correct listening profile, and beats the
  envelope/word-rate floor *specifically* in higher-order language (not just envelope-trackable AC).
- **Mapper-smoothing robustness (oracle control, by design):** TRIBE (native fsa5) and the floor are both
  scored against the SAME mapper-smoothed real BOLD per vertex, so smoothing cancels in the TRIBE−floor
  contrast; and smoothing can only BLUR the lang-vs-visual distinction (TRIBE 0.222 vs 0.003), so the strong
  specificity is conservative, not an artifact.
**Verdict: PASS — TRIBE is a faithful in-pipeline fMRI stand-in for the stimulus-evoked response.** This is a
TOOL-VALIDATION gate, NOT a science rung — **no ladder flip.** Licenses Phase 2 (the ceiling). Results:
`outputs/E016_tribe/fidelity/fidelity_results.json`. Panel note: per the repo cost-discipline norm (reserve
the full panel for surprising/load-bearing *science* verdicts), Phase 1 (expected PASS, a gate) gets a focused
counter-argument adversarial pass + the empirical controls above; the FULL thinking panel + Codex is reserved
for the Phase-2 ceiling verdict (the load-bearing claim that could read as Fork-A).

### Step 6 — counter-argument panel on Phase-1 PASS → objection HELD, number corrected (still PASS) (2026-06-14)
The counter-argument agent (opus) re-ran the pipeline and landed one **MATERIAL** objection (the rest MINOR):
**the floor was a strawman** — it used only rate/acoustic features and omitted the lab's own lexical-semantic
`english1000` (985-d) + articulatory `phonemes`/`letters`, which ship in the SAME `features_val_NEW.hdf`. Adopted:
rebuilt the floor as the **strong nuisance stack** (rate + envelope + phonemes + letters + english1000 PCA-100).
**Re-run result — PASS holds, magnitude honestly halved:** TRIBE higher-order-language r=0.273 vs **strong
floor 0.160** → **Δ = +0.113, 95% CI [+0.045, +0.181], 6/6 subjects, Wilcoxon p≈0.03** (was +0.165/~4× vs the
rate-only floor — that framing is dropped). Group per-vertex higher_lang: TRIBE 0.222, strong-floor 0.137,
weak-floor 0.057. So TRIBE carries real spatial-specificity fidelity *beyond lexical-semantics*, but the margin
is modest. MINOR objections verified and dismissed: the AC-chosen lag=7 is NOT language-ROI-overfit (higher_lang
also peaks at lag=7); the 700-vs-602-TR tail lands in silence (conservative); estimand asymmetry is logged for
Phase 2. **The agent's key carry-forward: because the margin over lexical-semantics is modest, the Phase-2
no-text-extractor ablation (Llama-shared-variance control) is now the BINDING concern** — a residual≈0 that only
holds vs full-TRIBE would be the Llama confound, not the ceiling. **Corrected verdict: PASS (faithful stand-in,
Δ≈+0.11 over a strong nuisance floor); no ladder flip; Phase 2 gated hard on the no-text ablation.**

### Step 7 — Phase 2 (THE CEILING) LOCKED DESIGN (S13, for oracle gate)
**Estimand:** the LM representation's alignment to real BOLD that is NOT explained by TRIBE (= E[Y|S], the
stimulus-predictable part). By the spine (Y⊥θ\*|S) this residual should be ≈0 (the LM, a θ\*-derived rep, can't
align to the θ\*-independent residual ε = Y − E[Y|S]). Operationalized as the **unique variance**
ΔR²_LM|TRIBE = R²(real | nuisance + TRIBE + LM) − R²(real | nuisance + TRIBE), in higher-order language ROIs.
- **LM:** Qwen2.5-0.5B (trained), verdict layer (the E006 powered aligner). Words from the whisperx TSV (the same
  words TRIBE saw), +5 TR lead (lab-grid alignment), lanczos→306-TR grid, PCA-100, FIR(1..4). [untrained-LM control optional.]
- **Targets:** real fsa5 BOLD (group-avg + per-subject, story_11); TRIBE regressor = the lag-aligned TRIBE
  prediction (full AND no-text), per vertex / per ROI-mean.
- **Levels:** PRIMARY = per-subject ROI-mean-timecourse partition, n=6 paired, higher-order language; descriptive =
  group per-vertex. CV = contiguous TR-block 5-fold (single story — autocorrelation-leakage limitation noted).
- **Sanity gate:** confirm A_real = ΔR²_LM|nuisance > 0 (the LM DOES align to real BOLD over nuisance) — else the
  residual test is vacuous.
- **REQUIRED no-text control:** repeat with no-text TRIBE (features_to_use=['audio'], cached). The Fork-B ceiling
  claim (residual≈0) is valid ONLY if it holds vs BOTH full and no-text TRIBE; collapse only vs full = Llama-shared
  variance, not the DPI ceiling. (Counter-argument: this is now the BINDING control given Phase 1's modest margin.)
- **Estimand caveat (Phase-1 carry):** residual is computed against group-avg E[Y|S] → an UPPER BOUND on unique
  non-stimulus signal (conservative for Fork-B; a Fork-A must survive this).
- **DECISION:** residual CI includes 0 vs BOTH ⇒ the ceiling is the stimulus-predictable part ⇒ **strongest Fork-B
  with mechanism.** residual CI excludes 0 surviving no-text ⇒ **Fork-A → STOP for Erfan.** Full panel + Codex on
  the verdict; no rung flip without Erfan.

### Step 8 — Oracle gate on Phase 2 = HOLD → revised (the ΔR² partition was primed for a FALSE Fork-A) (S13)
Oracle (opus) HOLD: the bare ΔR²_LM|TRIBE partition has THREE independent upward biases all pushing toward a
false Fork-A — (a) capacity: the 400-d LM block beats 1-d-per-vertex TRIBE by dimensionality alone; (b) TRIBE is a
weak encoder (Phase-1 margin modest) so partialling it leaves un-removed stimulus variance the LM mops up =
*stimulus-predictable*, mis-scored as residual; (c) group-TRIBE vs per-subject-real leaks subject-specific
*stimulus* deviation into the residual. A single biased CI would fire Fork-A (the expensive thesis-reopening
branch). **All must-fixes ADOPTED:**
1. **Untrained-LM floor is the VERDICT, not optional** (≥3 seeds): estimand = **(trained residual − untrained
   residual)**, on BOTH TRIBE variants. Absorbs capacity bias + no-text-is-weak + most of the group leak.
2. **Capacity-fair estimand (B) as headline:** score the SAME LM block (same dim) → two targets, real-BOLD vs
   TRIBE-BOLD, NC-normalized; capacity bias cancels by construction. residual = NC-norm A_real − A_tribe.
3. **Pre-register the MDE** (E006 fold-variance machinery). A CI⊇0 = "residual < MDE, with DPI as the mechanism",
   NOT a clean null (E006 MDE was +0.013/+0.015 on the POWERED substrate; 1 story will be weaker).
4. **Primary target = group-avg real BOLD** (estimand-matched to group-TRIBE); per-subject n=6 = consistency.
5. **Asymmetric decision rule:** Fork-A requires the trained−untrained residual gap to exclude 0 vs **BOTH** full
   AND no-text TRIBE (and ideally replicate on a 2nd story); anything less = Fork-B/HOLD, not a STOP. Currently
   primed to fire false Fork-A → flipped.
6. **Vacuity check:** confirm TRIBE-real R² in higher-language ≫ nuisance floor *in the Phase-2 fits* (else the
   subtraction is near-vacuous). Single-story = a residual *bound*, not a null; n=1 stimulus (pseudo-replication
   across 6 subjects) — frame honestly; ≥2-3 stories is the nice-to-have that breaks it.
**Verdict: design revised → build `scripts/run_tribe_ceiling.py` with estimand (B) + untrained floor + MDE.**

### Step 9 — Phase 2 (ceiling) ATTEMPT = INCONCLUSIVE / methodological wall; apparent "Fork-A" is a CONFIRMED ARTIFACT (NOT escalated) (S13, 2026-06-14)
Built `scripts/run_tribe_ceiling.py` (capacity-fair estimand B + untrained-LM floor, oracle Step 8). Ran trained
Qwen2.5-0.5B + 3 untrained seeds × {real, TRIBE-full, TRIBE-notext}, group-avg, higher-language. The runner flagged
"FORK-A CANDIDATE" — **but it FAILS the predeclared vacuity gate, so per the Step-8 decision rule it is NOT a
Fork-A and is NOT escalated.** Why it is an artifact (diagnosed, not assumed):
- **The vacuity check fired both times:** trained LM→TRIBE-full alignment in higher-language = **+0.030** (and −0.16
  in the v1 nuisance-residualized variant). Diagnostic confirmed it is not a frame issue: LM→TRIBE = +0.030 (real
  frame, lag 7) / −0.011 (stimulus frame), while **LM→real = +0.177** (same LM, same pipeline). The trained LM
  predicts REAL BOLD but barely predicts TRIBE's predicted BOLD.
- **Mechanism (oracle Q1, now empirically confirmed):** TRIBE explains only ~5–7% of per-vertex real-BOLD variance
  in higher-language (Phase-1 r≈0.22). TRIBE and the LM both predict real BOLD, but via representations that don't
  align with *each other* → "real-alignment beyond TRIBE" is large simply because TRIBE is a WEAK per-vertex
  predictor, not because of non-stimulus signal. The "residual" gap (trained 0.33 vs untrained −0.21) is dominated
  by the **A2 effect** (trained Qwen aligns to real BOLD, A_real_NC=0.355; untrained ~0) minus TRIBE-as-noise — NOT
  by non-stimulus brain structure. Both ΔR²-partition and matched-encoding(B) estimands are compromised by TRIBE's
  weakness as a regression target here.
- **The controls WORKED:** the predeclared vacuity gate + untrained floor + the oracle's pre-compute warning
  correctly caught a design primed for false Fork-A. No false alarm reaches Erfan.

**Solid sub-finding (defensible):** A2 reconfirmed on denizenslab — trained Qwen2.5-0.5B aligns to real story_11
BOLD in higher-language (NC-norm 0.355; raw 0.177), untrained same-arch ~0. (Consistent with E006 on LeBel.)

**This is a real WALL for the session.** The TRIBE-ceiling stimulus-subtraction, as operationalized, does not work
on a single story with a group-averaged TRIBE that explains only ~7% of per-vertex variance. **Phase-2 redesign
(next focused session):** (i) a STRONGER TRIBE target — TRIBE's per-subject fine-tuned readout (≤1h, §1) or more
stimulus data, so TRIBE actually captures E[Y|S] well enough to subtract; (ii) ≥3 stories for story-grouped CV
(breaks the n=1-stimulus pseudo-replication); (iii) a frame-consistent estimand where the "ceiling" reference is a
VALID measure of the stimulus-predictable part (LM→TRIBE must be ≫0 first). **No rung flip; no Fork-A escalation.**

### Step 10 — REFRAME (D028, Erfan-agreed): the ceiling moves to empirical E[Y|S] (E020); TRIBE → Phase 3 only
The Phase-2 wall (Step 9) is not a tuning problem to grind away — TRIBE is the *wrong instrument* for the ceiling on
data where many subjects heard the same stimulus, because the **cross-subject/repeat average of real fMRI IS the
ground-truth E[Y|S]** and is strictly stronger than TRIBE's ~7% estimate. So:
- **The ceiling question → `docs/experiments/E020_*.md`** (empirical-E[Y|S], TRIBE-free, NEXT). This is the rigorous
  F1-close; it states the spine as a ground-truth result (close to E008 + L016).
- **TRIBE's irreplaceable role is Phase 3 only** (§5): dense synthetic brain targets for the REAL KD corpus where no
  fMRI exists and empirical averaging is impossible. Phase 1 (PASS) already validated TRIBE is faithful enough to BE
  such a target. Phase 3 = optional Fork-B booster (null at scale removes the scarcity excuse), NOT a blocker.
- **Do NOT** pursue per-subject-fine-tuned TRIBE or a video-stimulus ceiling (abandons the language substrate).
Forward order (D028): **F1-close (E020) → F2 (E019, paper-critical) → F3 (I3) → F4 (E015 Q2)**; TRIBE Phase 3 after F2 if pursued.

### Step 11 — S48 Phase-3 launch preflight: NO-GO for this work session (2026-07-02)
Priority-3 work-session audit asked whether Phase 3 can be run now as a scaled synthetic-target KD experiment.
Verdict: **NO-GO for valid Phase-3 compute.**

Reasons:
- The existing Phase-2 artifact is explicitly inconclusive/walled: `outputs/E016_tribe/ceiling/ceiling_results.json`
  records the failed LM→TRIBE target-alignment diagnostic (`trained.A_tribe_full_hl=+0.030`; the JSON helper flag
  `vacuity_check.tribe_full_aligns_above_chance=false`). That keeps the Phase-2 ceiling claim walled/inconclusive;
  it is not itself the original Phase-3 launch gate.
- Independently, Phase 3 requires dense TRIBE targets on the KD corpus, but no such target cache exists in
  `outputs/E016_tribe/`.
- There is no Phase-3 runner implementing the required three-arm matched-perplexity design:
  KD-only / KD+TRIBE-MSE / KD+TRIBE-block-permuted, with ≥3 seeds, matched ppl, train-only normalization/PCA,
  and a fixed heldout corpus. A no-text/TRIBE variant should be inherited as an added confound-control from the
  Phase-2 audit, but it was not part of the original Phase-3 gate.
- The available distillation code can accept `fmri_train`, but `scripts/run_kd_alignment.py` is the old pure-KD
  GPT-2/E003 harness (`lambda_brain=0`), and `scripts/run_brain_lever.py` targets the 5-UID Tuckute averaged
  target rather than dense TRIBE predictions.

**Decision:** do not run Phase 3 in this work session. The valid next action is a Phase-3 PRD/build gate: produce
the dense synthetic target cache, add the matched-ppl three-arm runner, pre-register the permuted control plus any
inherited no-text/TRIBE confound control, then run a smoke + reviewer gate before any multi-day training. This is a
gate-fired completion, not a science null and not a ladder move.

### Step 12 — Phase-3 infrastructure scaffold BUILT + smoke-tested; still NOT a Phase-3 result (2026-07-02)
Follow-up work-session action filled the Step-11 mechanical gaps. Built:
- `scripts/tribe_predict_kd_corpus.py` — KD-corpus TRIBE target-cache builder. The cache path uses direct
  synthetic `Word` events with `features_to_use=["text"]`, avoiding 96k gTTS/ASR calls; dense target generation
  remains compute work. The old public `text_path` route remains as `--event-mode tts-single` for debug/fidelity
  checks. Cache schema:
  `targets`, `texts`, `item_indices`, `vertex_index`, `segment_counts`, and JSON metadata.
- `scripts/run_tribe_phase3.py` — three-arm matched-budget runner over a cache:
  KD-only / KD+TRIBE-MSE / KD+TRIBE-block-permuted, with train-only target standardization, fixed heldout-PPL
  probe, lambda grid support, and optional heldout target-R² if a heldout TRIBE cache exists.
- `scripts/analyze_tribe_phase3.py` — gate/analyzer that refuses interpretation unless the run has ≥3 seeds,
  PPL-matched brain/permuted arms, heldout target metrics, and intended-scale train/heldout/full-dimension
  target coverage. It labels small runs as smoke/incomplete.

Smoke artifacts (pipeline check only, not evidence): direct TRIBE text-event cache succeeded for 2 train and
2 heldout WikiText sentences at 16 vertices:
`outputs/E016_tribe/kd_targets/text/train_start0_n2_d16_smoke.npz` and
`outputs/E016_tribe/kd_targets/text/heldout_start0_n2_d16_smoke.npz`. A tiny-gpt2 1-seed runner smoke completed
all three arms and analyzer correctly returned `science_ready=false`:
`outputs/E016_tribe/phase3/phase3_smoke_tiny.json` +
`outputs/E016_tribe/phase3/phase3_smoke_tiny.analysis.json`.

**Status:** the missing infra is no longer the blocker. What remains before any Phase-3 claim is actual target
generation at the intended scale/dimension, a predeclared full run (≥3 seeds, matched PPL, permuted twin), and a
review gate before interpretation. No science verdict, no rung flip.

### Step 13 — Cache-throughput pilot PASS; still NOT a Phase-3 result (2026-07-02)
Ran the first post-infra calibration step: direct synthetic-text TRIBE target caching on WikiText KD sentences,
with `features_to_use=["text"]`, requested `batch_items=32`, `target_dim=512`, GPU 1, and no model training.
Artifacts:
- `outputs/E016_tribe/kd_targets/text/train_start0_n256_d512_pilot.npz`
- `outputs/E016_tribe/kd_targets/text/heldout_start0_n128_d512_pilot.npz`

Validation:
- Train pilot: `targets=(256, 512)`, elapsed 83.914 s, 3.051 items/s, segment-counts min/mean/max =
  2/9.28/19, zero missing items, finite targets.
- Heldout pilot: `targets=(128, 512)`, elapsed 49.644 s, 2.578 items/s, segment-counts min/mean/max =
  2/10.88/21, zero missing items, finite targets.

Projection from this pilot: the full 95,999-train + 1,999-heldout cache is about 8.96 GPU-hours at the 512-vertex
pilot throughput. This is only a throughput extrapolation. TRIBE still predicts the full 20,484 cortical vertices
before the builder slices `target_dim`, so full-dimension cache generation should mostly preserve forward-pass
cost but increase saved array size and write/I/O time.

**Decision:** cache-throughput gate = **PASS**. Do not launch the full Phase-3 science run yet. The next valid
step is a mini real-model Phase-3 runner check on a modest cached subset, verifying matched-PPL behavior,
lambda/permuted control wiring, and analyzer gates before spending the full cache + >=3-seed compute.

### Step 14 — Mini real-model Phase-3 runner check PASS; still NOT a Phase-3 result (2026-07-02)
Ran the next gate on the pilot caches with a real GPT-2-family pair: teacher `gpt2-medium`, student `gpt2`,
seed 0, 256 train items, 128 heldout items, one epoch, `max_length=64`, `lambda_brain_grid=0.1,1.0`. Artifacts:
- `outputs/E016_tribe/phase3/phase3_mini_real_gpt2_n256_s0.json`
- `outputs/E016_tribe/phase3/phase3_mini_real_gpt2_n256_s0.analysis.json`

Runner health:
- Completed 5 arms in 50.531 s: KD-only plus TRIBE/permuted twins at λ=0.1 and λ=1.0.
- Heldout target-R² path worked for every arm.
- Analyzer gate worked and returned `science_ready=false`, with target metrics present but failures for seed count,
  all-lambda PPL matching, and scale/dimension readiness.

Calibration read:
- KD-only: PPL 92.647, heldout target-R² +0.3060.
- λ=0.1: TRIBE PPL 96.238 and permuted PPL 96.171; both within the default 5% PPL-match tolerance
  (relative deltas 3.88% and 3.80%). TRIBE−permuted target-R² was +0.00002 in this one-seed check.
- λ=1.0: TRIBE PPL 106.919 and permuted PPL 107.362; both outside the 5% tolerance (15.4% and 15.9%), so
  λ=1.0 is too strong for the matched-PPL spec at this configuration.

During the gate check, hardened `scripts/analyze_tribe_phase3.py` so a small three-seed toy/subset run cannot
accidentally label itself science-ready: default science thresholds now require at least 50,000 train items,
1,000 heldout items, and 20,484 target dimensions, in addition to ≥3 seeds, PPL matching, and heldout target
metrics. These thresholds can be overridden explicitly only by CLI argument.

**Decision:** mini real-model runner gate = **PASS** as infrastructure. The plausible predeclared λ for the full
run is λ=0.1, not λ=1.0. What remains is full-dimension target-cache generation, then an at-scale ≥3-seed run
using only PPL-matchable λ settings, followed by the analyzer/review gate. No science verdict, no rung flip.

### Step 15 - Analyzer grid-completeness hardening while full Phase-3 cache runs (2026-07-02)
While the full Phase-3 pipeline was still building the train TRIBE cache, hardened `scripts/analyze_tribe_phase3.py` against a partial-run false-ready mode. The previous analyzer required ≥3 observed seeds and PPL-matched common paired seeds, but a malformed runner output could in principle include three KD-only seeds while missing one or more TRIBE/permuted rows and still let the paired checks run on the smaller common subset. The analyzer now reads the expected seed list and lambda grid from the run config, constructs the full expected arm grid (`kd_only` plus `tribe_mse` and `tribe_perm` for every seed/lambda), records missing/duplicate/extra rows, requires `has_lambda_grid=true`, requires `arm_seed_grid_complete=true`, and requires each paired contrast to contain all expected seeds before `science_ready` can pass.

Verification:
- `uv run python -m py_compile scripts/analyze_tribe_phase3.py` passed.
- Existing mini real-model artifact remains blocked as intended: `science_ready=false`, with `enough_seeds=false`, `ppl_matched_all_lambdas=false`, and scale/dimension gates false.
- A deliberately incomplete temporary copy with expected seeds `0,1,2` and a missing `tribe_perm` row now returns `arm_seed_grid_complete=false` and `all_paired_common_seeds=false`.

**Status:** analyzer hardening only. No new science number, no Phase-3 result, no rung flip. The active full run is still cache-building and will use this stricter analyzer when it reaches the analysis step.

### Step 16 - Read-only Phase-3 status helper added while full cache runs (2026-07-02)
Added `scripts/e016_phase3_status.py`, a read-only helper for monitoring the full Phase-3 pipeline without loading the large cache arrays. It reports process state, expected artifact presence, log markers, latest cache-builder batch, train-cache progress from log parsing, and analyzer gate contents once the analyzer JSON exists. It reads only the log plus small JSON sidecars.

Verification:
- `uv run python -m py_compile scripts/e016_phase3_status.py` passed.
- `uv run python scripts/e016_phase3_status.py --pretty` reported `phase=train_cache_building`, no train/heldout/run/analyzer artifact yet, and a live latest-batch marker from the train-cache log.

**Status:** monitoring utility only. No new science number, no Phase-3 result, no rung flip. Use this before hand-parsing the long run log.

### Step 17 - Post-CoNLL control implication for Phase 3 (2026-07-02)
The full CoNLL 2026 paper "What Brain Data Adds to Language Model Training" was digested in [`merlin-2026_what-brain-data-adds`](../literature/canonical/merlin-2026_what-brain-data-adds.md). It directly compares Brain-Tuned, Stimulus-Tuned, and Jointly-Tuned BERT/GPT-2 LoRA arms, so the broad "brain data adds beyond stimulus text" claim is no longer ours. Phase 3 remains the right gateway because CoNLL does not test compression, KD-only students, matched perplexity, or a fixed student budget.

Design implication:
- If the active full run is null (`kd_only` ≈ `tribe_mse` ≈ `tribe_perm` at matched PPL), the result is still informative: dense synthetic neural targets did not move a KD student even after the scarcity/SNR objection was removed.
- If the active full run is positive (`tribe_mse` beats `tribe_perm` and `kd_only` at matched PPL), it is not yet enough for a top-tier brain-specific claim. The next control should be a matched-information non-brain privileged target or stimulus-derived teacher target with the same student budget, so the claim is not merely "a dense text-derived auxiliary target helps."

**Status:** design interpretation only. No new science number, no Phase-3 result, no rung flip.

### Step 18 - Matched-information non-brain control tooling added (2026-07-02)
Added `scripts/build_text_feature_target_cache.py` to support the post-CoNLL control implied by Step 17. The builder creates target caches with the same schema as the TRIBE cache, but the targets are frozen LM hidden states projected to the requested dimensionality and therefore contain only stimulus-text information, not brain-derived predictions. The Phase-3 runner now accepts `--target-label`, so the same KD-only / target-MSE / target-permuted design can be run as either the default `tribe_mse`/`tribe_perm` comparison or a `textfeat_mse`/`textfeat_perm` matched-information control.

Verification:
- `uv run python -m py_compile scripts/build_text_feature_target_cache.py scripts/run_tribe_phase3.py scripts/analyze_tribe_phase3.py` passed.
- Existing default analyzer behavior remains backward compatible on `phase3_mini_real_gpt2_n256_s0.json`: default arms still resolve to `tribe_mse` and `tribe_perm`, and the smoke artifact remains `science_ready=false`.
- A relabeled temporary smoke artifact with `target_label=textfeat` resolved to `textfeat_mse` and `textfeat_perm`, kept `arm_seed_grid_complete=true`, and still returned `science_ready=false`.
- A tiny text-feature cache smoke completed with `distilgpt2`, 4 train items, and 16 dimensions at `outputs/E016_tribe/kd_targets/text_feature/smoke_train_textfeat_d16.npz`. This is a plumbing check only.
- A tiny end-to-end runner smoke with `--target-label textfeat`, `sshleifer/tiny-gpt2`, one seed, 4 train items, 4 heldout items, and lambda 0.1 produced the expected `kd_only`, `textfeat_mse`, and `textfeat_perm` rows at `outputs/E016_tribe/phase3/phase3_smoke_textfeat_tiny.json`; the analyzer output at `outputs/E016_tribe/phase3/phase3_smoke_textfeat_tiny.analysis.json` kept `science_ready=false`, with the scale/seed gates closed.

**Status:** matched-information control infrastructure only. No new Phase-3 science result, no top-tier claim, no rung flip. If the active TRIBE full run is positive, this control is the next required comparison before treating the gain as brain-specific rather than a dense auxiliary-target effect.

### Step 19 - Analyzer paired-effect audit fields added while full cache runs (2026-07-02)
Hardened the post-run analyzer output for the eventual `/interpret` pass without changing the science-readiness gate. `scripts/analyze_tribe_phase3.py` now records the per-seed paired deltas for target-vs-permuted and target-vs-KD heldout target-R2 contrasts, whether all paired seed deltas are positive, and a deterministic two-sided sign-flip p-value for the paired mean. This is meant to make the post-result audit less brittle when the active full run finally writes its analyzer JSON.

Verification:
- `uv run python -m py_compile scripts/analyze_tribe_phase3.py` passed.
- Existing default mini-real artifact analysis still returns `science_ready=false`.
- The tiny text-feature smoke analysis still returns `science_ready=false` and now includes paired delta values plus sign-flip p-values in the JSON artifact.

**Status:** analyzer reporting only. No new Phase-3 science result, no top-tier claim, no rung flip.

### Step 20 - Text-feature control launcher prepared, not run (2026-07-03)
Added `scripts/e016_make_textfeat_control_script.py` to write the exact full matched-information control launcher for the post-CoNLL burden of proof. The generated launcher builds full train and heldout frozen-LM text-feature caches, validates their schema and finite targets, runs the same GPT-2-medium to GPT-2 Phase-3 setup with `--target-label textfeat`, then sends the result through the analyzer. It mirrors the active TRIBE full-run seeds, lambda, student, teacher, epoch count, heldout limit, and analyzer path shape, while changing only the target source and arm label.

Verification:
- `uv run python -m py_compile scripts/e016_make_textfeat_control_script.py` passed.
- `uv run python scripts/e016_make_textfeat_control_script.py --force` wrote `outputs/E016_tribe/phase3/run_textfeat_control_20260703.sh` and did not launch it.
- `bash -n outputs/E016_tribe/phase3/run_textfeat_control_20260703.sh` passed.

**Status:** queued control launcher only. It must not be run while the active TRIBE full run is still building, and it is required only if the TRIBE result is positive enough to need a brain-specificity check.

### Step 21 - Status helper ETA fields added while full cache runs (2026-07-03)
Extended `scripts/e016_phase3_status.py` with ETA fields for the long train-cache build, derived from the latest parsed cache-builder batch and the elapsed time of the active full-run process. This makes the monitor useful without hand-parsing the long log or loading cache arrays.

Verification:
- `uv run python -m py_compile scripts/e016_phase3_status.py` passed.
- `git diff --check` passed.
- `uv run python scripts/e016_phase3_status.py --pretty` reported `phase=train_cache_building` at `2026-07-02T22:13:47.136566+00:00`, with no train/heldout/run/analyzer artifact yet. The monitor parsed latest batch `84000:84032`, lower-bound progress `84032/95999`, and an ETA projection to `2026-07-02T23:58:08.136530+00:00`.

**Status:** monitoring utility only. No Phase-3 result, no analyzer verdict, no science claim, and no rung flip.

### Step 22 - Status helper made cache-stage-aware before heldout build (2026-07-03)
Hardened `scripts/e016_phase3_status.py` before the active run reaches the heldout-cache stage. The helper now parses train and heldout cache-builder sections separately, reports `active_cache_stage`, uses the correct denominator for each stage (`95999` train items, `1999` heldout items), and attaches ETA fields only to the active cache stage. This prevents heldout `=== batch a:b ===` lines from being misread as train progress after the train cache finishes.

Verification:
- `uv run python -m py_compile scripts/e016_phase3_status.py` passed.
- `git diff --check` passed.
- `uv run python scripts/e016_phase3_status.py --pretty` reported `active_cache_stage=train`, train latest batch `84192:84224`, lower-bound train progress `84224/95999`, and no heldout/run/analyzer artifact yet.

**Status:** monitoring correction only. No Phase-3 result, no analyzer verdict, no science claim, and no rung flip.

### Step 23 - Full target caches validated and training-progress monitor added (2026-07-03)
The active full Phase-3 launcher completed both target-cache stages and advanced into the GPT-2 training arms. `scripts/e016_phase3_status.py` now also parses the training-arm markers from the log, reporting the latest `seed`/`arm`/`lambda` marker and the number of arm markers seen out of the expected 9 arms.

Cache/status snapshot at `2026-07-03T01:06:08.080057+00:00`:
- Train target cache exists at `outputs/E016_tribe/kd_targets/text/train_start0_n95999_full.npz`, with sidecar `n_items=95999`, `target_dim=20484`, `elapsed_s=52654.695`, and `science_status="target-cache artifact only; not a Phase-3 result"`.
- Heldout target cache exists at `outputs/E016_tribe/kd_targets/text/heldout_start0_n1999_full.npz`, with sidecar `n_items=1999`, `target_dim=20484`, `elapsed_s=1001.696`, and the same target-cache-only science status.
- The launcher validation printed train shape `(95999, 20484)`, heldout shape `(1999, 20484)`, `missing=0`, and `finite=True` for both caches.
- Training began at `2026-07-03T01:01:14Z`; the latest parsed arm marker was `seed=0`, `arm=kd_only`, `lambda=0.0`, with `1/9` arm markers seen.

Verification:
- `uv run python -m py_compile scripts/e016_phase3_status.py` passed.
- `git diff --check` passed.
- `uv run python scripts/e016_phase3_status.py --pretty` reported `phase=training_running_or_interrupted`, both caches present, `run_json.exists=false`, and `analysis_json.exists=false`.

**Status:** target-cache artifact and monitoring update only. Training is running, but there is still no run JSON, no analyzer verdict, no science claim, and no rung flip.

### Step 24 - Status helper now discovers the Phase-3 runner process (2026-07-03)
Extended `scripts/e016_phase3_status.py` process discovery to include the active `run_tribe_phase3.py` runner, not only the shell parent and cache builders. This matters during training because the trainer is quiet after printing an arm marker; the process table, not log mtime alone, is the live-health check.

Verification:
- `uv run python -m py_compile scripts/e016_phase3_status.py` passed.
- `git diff --check` passed.
- `uv run python scripts/e016_phase3_status.py --pretty` showed the launcher parent plus the `uv run python scripts/run_tribe_phase3.py` process and its `.venv/bin/python3` child. The Python child was running under the first full arm (`seed=0`, `arm=kd_only`, `lambda=0.0`), with `run_json.exists=false` and `analysis_json.exists=false`.

**Status:** monitoring correction only. The full run is alive in training, but no run JSON, analyzer verdict, science claim, or rung flip exists yet.

### Step 25 - Status helper health block added for quiet training (2026-07-03)
Extended `scripts/e016_phase3_status.py` with a `health` block that separates a quiet training log from a stopped run. The helper now reports `status`, total process count, runner-process count, maximum runner elapsed time, and `log_quiet_s`. In the current full run this is expected to read as `runner_alive_log_quiet` while `run_tribe_phase3.py` is fitting/evaluating an arm without emitting new log lines.

Verification:
- `uv run python -m py_compile scripts/e016_phase3_status.py` passed.
- `git diff --check` passed.
- `uv run python scripts/e016_phase3_status.py --pretty` reported `health.status=runner_alive_log_quiet`, `runner_process_count=2`, `runner_elapsed_s_max=1346`, `log_quiet_s=1222`, latest parsed arm `seed=0`, `arm=kd_only`, `lambda=0.0`, and no run/analyzer JSON.

**Status:** monitoring correction only. The full run is alive in training, but no run JSON, analyzer verdict, science claim, or rung flip exists yet.

### Step 26 - Analyzer paper-branch hint added while full training runs (2026-07-03)
Extended `scripts/analyze_tribe_phase3.py` with a conservative `paper_branch_hint` block. The hint is downstream of `gate.science_ready`: incomplete or smoke artifacts map to `not_ready`, TRIBE-ready positives map to `tribe_positive_needs_textfeat`, TRIBE null/negative effects map to `controlled_null_candidate`, and non-TRIBE targets map to `matched_information_control_ready`. This is a paper-plan routing aid, not a verdict engine.

Verification:
- `uv run python -m py_compile scripts/analyze_tribe_phase3.py` passed.
- `git diff --check` passed.
- Running the analyzer on `outputs/E016_tribe/phase3/phase3_mini_real_gpt2_n256_s0.json` still returned `science_ready=false` and wrote `paper_branch_hint.branch="not_ready"`.
- A direct function smoke over synthetic summaries returned the expected route labels: `tribe_positive_needs_textfeat`, `controlled_null_candidate`, and `matched_information_control_ready`.

**Status:** analyzer reporting only. The active full run is still training, with no run JSON, no analyzer verdict, no science claim, and no rung flip.

### Step 27 - Interpretation manifest precommitted before full-run numbers (2026-07-03)
Added [`e016-interpretation-protocol-2026-07-03.md`](../e016-interpretation-protocol-2026-07-03.md), a pre-result post-run protocol for the active full Phase-3 run. It records the branch-specific claim-intent manifests, overturn criteria, gate fields, commands, and branch actions to use once the run JSON and analyzer JSON exist. The protocol makes the conservative pre-result prior explicit: the controlled-null or dense-target-generic branch is more likely than a brain-specific positive given the recorded Q2-Q4 state, but E016 can overturn that only by passing the analyzer gate and the paired audits.

**Status:** interpretation precommitment only. The active full run is still training, with no run JSON, no analyzer verdict, no science claim, and no rung flip.

### Step 28 - TRIBE-vs-textfeat comparator prepared while full training runs (2026-07-03)
Added `scripts/e016_compare_target_controls.py`, a read-only comparator for the post-positive branch where both the full TRIBE analyzer JSON and a later text-feature analyzer JSON are science-ready. The comparator refuses non-ready or mislabeled analyzer outputs, then compares within-target paired gains over KD-only and permuted controls. Its branch labels are `tribe_not_positive`, `dense_privileged_target_generic`, `tribe_stronger_than_textfeat_needs_review`, `mixed_requires_interpretation`, or `not_ready`.

Verification:
- `uv run python -m py_compile scripts/e016_compare_target_controls.py` passed.
- Running the comparator on existing smoke/incomplete analyzer JSONs returned `ready=false` and `branch_hint.branch="not_ready"`.
- Temporary ready-analysis fixtures exercised the three post-ready route labels: `tribe_stronger_than_textfeat_needs_review`, `dense_privileged_target_generic`, and `tribe_not_positive`.

**Status:** post-positive comparison tooling only. The active full run is still training, with no run JSON, no analyzer verdict, no science claim, and no rung flip.

### Step 29 - Status helper now separates started-arm markers from completed-arm diagnostics (2026-07-03)
Extended `scripts/e016_phase3_status.py` so the training-progress block distinguishes arm markers from completed arm metrics. It now reports `arm_markers_seen`, `completed_arm_count`, `latest_completed_arm`, `active_arm`, and `completed_arms`, with completed-arm metric records labeled `science_status="partial arm diagnostic only; not a Phase-3 result"`.

Verification:
- `uv run python -m py_compile scripts/e016_phase3_status.py` passed.
- `uv run python scripts/e016_phase3_status.py --pretty` reported `arm_markers_seen=2`, `completed_arm_count=1`, latest completed arm `seed=0`, `arm=kd_only`, and active arm `seed=0`, `arm=tribe_mse`, while `run_json.exists=false` and `analysis_json.exists=false`.

**Status:** monitoring correction only. The active full run is still training, with no run JSON, no analyzer verdict, no science claim, and no rung flip.

### Step 30 - Readiness packet helper added for the post-analyzer handoff (2026-07-03)
Added `scripts/e016_make_readiness_packet.py`, a read-only post-analyzer helper that converts an E016 analyzer JSON into a compact `/interpret` handoff packet. The packet extracts `gate`, failed gate fields, `paper_branch_hint`, grid/scale fields, paired target-vs-KD/permuted contrasts, reviewer-burden flags, and next actions. It also repeats the claim boundary: the packet is not a verdict, does not prove brain specificity, and cannot flip a rung.

The helper can also attach a ready TRIBE-vs-textfeat comparator JSON after the matched-information control exists, so the positive branch has one stable handoff artifact instead of scattered analyzer/comparator fields.

Verification:
- `uv run python -m py_compile scripts/e016_make_readiness_packet.py` passed.
- Running the helper on existing incomplete smoke analyzer JSONs wrote readiness packets with `science_ready=false`, failed gate fields listed, and `paper_branch_hint.branch="not_ready"`.
- Temporary ready-analysis fixtures exercised the controlled-null, TRIBE-positive-needs-textfeat, and matched-information-control-ready action routes.

**Status:** post-analyzer handoff tooling only. The active full run is still training, with no run JSON, no analyzer verdict, no science claim, and no rung flip.

### Step 31 - Guarded Phase-3 finalizer added (2026-07-03)
Added `scripts/e016_finalize_phase3.py`, a guarded post-run helper for the active full Phase-3 path. If the full run JSON is absent, it prints a status packet with `status="run_json_missing"` and exits cleanly. If the run JSON exists, it runs or refreshes `scripts/analyze_tribe_phase3.py`, then `scripts/e016_make_readiness_packet.py`, and prints a compact status packet pointing to the analyzer/readiness artifacts. It repeats the boundary that the finalizer output is not a verdict and cannot flip a rung.

Verification:
- `uv run python -m py_compile scripts/e016_finalize_phase3.py` passed.
- Missing-run fixture returned `run_json_missing` and `next_action="Stay in /work and monitor with scripts/e016_phase3_status.py."`
- Existing smoke run fixture regenerated a smoke analyzer/readiness pair and preserved `science_ready=false`, `paper_branch_hint.branch="not_ready"`, and the failed gate fields.
- Default full-run invocation returned `run_json_missing`, because the active full run has still not written `phase3_full_gpt2_n95999_s0-1-2_lam0.1.json`.

**Status:** guarded post-run automation only. The active full run is still training, with no run JSON, no analyzer verdict, no science claim, and no rung flip.

### Step 32 - Finalizer made cwd-independent (2026-07-03)
Hardened `scripts/e016_finalize_phase3.py` so it resolves the repo root from `scripts/e016_phase3_status.py`, passes absolute analyzer/readiness script paths to subprocesses, and resolves user-supplied artifact paths before changing subprocess cwd. This prevents a future handoff failure if the command is launched from a subdirectory rather than the repo root.

Verification:
- `uv run python -m py_compile scripts/e016_finalize_phase3.py` passed.
- Default invocation from the repo root returned `run_json_missing` for the still-incomplete active full run.
- Default invocation from `docs/` via `uv run python ../scripts/e016_finalize_phase3.py` also returned the same full-run `run_json_missing` packet.
- Existing smoke run fixture still regenerated a smoke analyzer/readiness pair using absolute script paths and preserved `science_ready=false` plus `paper_branch_hint.branch="not_ready"`.

**Status:** robustness hardening only. The active full run is still training, with no run JSON, no analyzer verdict, no science claim, and no rung flip.

### Step 33 - Status helper now reports node-level GPU activity (2026-07-03)
Extended `scripts/e016_phase3_status.py` with a top-level `gpu` block from `nvidia-smi`. It reports per-GPU memory, GPU utilization, memory utilization, active GPU count, and a note that compute-app PIDs may be host-namespace PIDs, so the block is node-level activity rather than strict E016 attribution. This makes a quiet training log easier to distinguish from an idle or dead runner without running separate manual GPU commands.

Verification:
- `uv run python -m py_compile scripts/e016_phase3_status.py` passed.
- `uv run python scripts/e016_phase3_status.py --pretty` reported `gpu.available=true`, `active_gpu_count=2`, and nonzero GPU utilization while the active full run remained `run_json.exists=false` and `analysis_json.exists=false`.

**Status:** monitoring hardening only. The active full run is still training, with no run JSON, no analyzer verdict, no science claim, and no rung flip.

### Step 34 - Watch-finalize helper added for the active full run (2026-07-03)
Added `scripts/e016_watch_finalize_phase3.py`, a thin wrapper around the guarded finalizer. By default it checks once and exits with `status="waiting_for_run_json"` if the full run JSON is absent. With `--watch`, it polls until the run JSON appears or `--max-wait-s` expires, then calls `scripts/e016_finalize_phase3.py` with the same artifact arguments. It does not run training, does not interpret analyzer values, and cannot flip a rung.

Verification:
- `uv run python -m py_compile scripts/e016_watch_finalize_phase3.py` passed.
- Default invocation returned `status="waiting_for_run_json"` for the still-incomplete active full run.
- `uv run python scripts/e016_watch_finalize_phase3.py --watch --interval-s 300 --max-wait-s 0` returned immediately with `status="waiting_for_run_json"`, confirming the max-wait guard bounds polling.
- A smoke-run invocation using `outputs/E016_tribe/phase3/phase3_smoke_tiny.json` called the guarded finalizer and preserved `science_ready=false` plus `paper_branch_hint.branch="not_ready"`.

**Status:** post-run handoff automation only. The active full run is still training, with no run JSON, no analyzer verdict, no science claim, and no rung flip.

### Step 35 - Branch-decision router added for the post-finalizer handoff (2026-07-03)
Added `scripts/e016_branch_decision.py`, a conservative router that reads the full run JSON, analyzer JSON, readiness JSON, and prepared text-feature launcher path, then prints the next safe command or stance. It returns `waiting_for_run_json` while the active full artifact is absent, `needs_finalizer` if analyzer/readiness artifacts are missing or stale, `ready_for_interpret_controlled_null` for a controlled-null candidate, `textfeat_control_required` for a TRIBE-positive branch, and `ready_for_target_control_comparison` for a matched-information control branch.

The router never launches training, never interprets analyzer values, and cannot flip a rung. Its purpose is to reduce handoff error when the long E016 run finishes: the user or agent should be able to run one command and see whether to monitor, finalize, switch to `/interpret`, or manually launch the queued text-feature control after confirming resources are free.

Verification:
- `uv run python -m py_compile scripts/e016_branch_decision.py` passed.
- Default invocation during the active incomplete full run returned `status="waiting_for_run_json"`, with monitor/watch commands and no science claim.
- A smoke-run invocation using existing smoke artifacts returned a non-ready branch from the readiness packet rather than treating smoke output as a result.
- In-memory route smokes exercised the post-ready labels `ready_for_interpret_controlled_null`, `textfeat_control_required`, `ready_for_target_control_comparison`, and `mixed_or_manual_interpretation_required`.

**Status:** post-finalizer routing automation only. The active full run is still training, with no run JSON, no analyzer verdict, no science claim, and no rung flip.

### Step 36 - Post-positive reviewer-burden routing hardened (2026-07-03)
Threaded the 2026-07-03 privileged-signal adjacency audit into the E016 handoff helpers. `scripts/e016_compare_target_controls.py` now attaches explicit post-positive reviewer-burden metadata when ready TRIBE and text-feature analyses yield the `tribe_stronger_than_textfeat_needs_review` branch: TRIBE > textfeat clears only the weakest dense-text-target alternative, not the broader context/self-distillation, rich-feedback, or cognitive-supervision adjacency. The next action is `/interpret`, with seed-level margin audit, PPL/gate/code/stat review, and a decision on whether the paper needs extra seeds, a stronger non-brain/context-distillation comparator, a real-brain follow-up, or a narrower claim.

`scripts/e016_make_readiness_packet.py` and `scripts/e016_branch_decision.py` now carry the same warning in their `must_not_claim`, burden, and route metadata. This keeps the future one-command handoff from treating the matched-information control as brain-specific clearance. The analyzer science gate itself is unchanged.

Verification:
- `uv run python -m py_compile scripts/e016_compare_target_controls.py scripts/e016_make_readiness_packet.py scripts/e016_branch_decision.py` passed.
- In-memory route smokes for readiness and control-comparison helpers exercised the post-positive metadata paths.
- Default branch-router invocation during the active incomplete full run still returned `status="waiting_for_run_json"`.

**Status:** post-positive burden-routing automation only. The active full run is still training, with no run JSON, no analyzer verdict, no science claim, and no rung flip.

### Step 37 - Target-control scope metadata added (2026-07-03)
Refined the post-positive control ladder without launching any compute. `scripts/analyze_tribe_phase3.py` now preserves `target_cache`, `heldout_target_cache`, and `target_cache_meta` in analyzer JSONs, so downstream packets can identify which target source actually produced a control. `scripts/e016_make_readiness_packet.py` now exposes a `target_cache_scope` block; for `textfeat` it records the control as sentence-local frozen-LM hidden-state supervision and lists what it clears (non-brain hidden-state/dense-feature target under the same KD budget) versus what it does not clear (long-document context distillation, on-policy/self-distillation with privileged rationales/answers, or real-brain evaluation). `scripts/e016_compare_target_controls.py` now emits the same scope for both TRIBE and textfeat analyses under `target_scopes`.

This narrows the reviewer-burden language from "stronger comparator" to the actual ladder: if TRIBE is positive, first run textfeat; if TRIBE also beats textfeat, the unresolved follow-up is extra seeds plus long-context/on-policy distillation, real-brain evaluation, or a deliberately narrower claim. The current sentence-level WikiText corpus is not sufficient by itself for a clean long-context control, because the prepared KD inputs are already sentence-split.

Verification:
- `uv run python -m py_compile scripts/analyze_tribe_phase3.py scripts/e016_compare_target_controls.py scripts/e016_make_readiness_packet.py scripts/e016_branch_decision.py` passed.
- In-memory metadata smokes confirmed analyzer metadata propagation, readiness `target_cache_scope`, and comparator `target_scopes`.
- Default branch-router invocation during the active incomplete full run still returned `status="waiting_for_run_json"`.

**Status:** control-scope metadata and paper-branch clarification only. The active full run is still training, with no run JSON, no analyzer verdict, no science claim, and no rung flip.

### Step 38 - WikiText context metadata recovered for a possible `contextfeat` control (2026-07-03)
Refined the Step 37 statement that the current sentence-level WikiText corpus is insufficient by itself for a clean long-context control. The target caches themselves are sentence-local, but the original WikiText row/header provenance is recoverable exactly by replaying the E003 corpus extraction.

Added `scripts/e016_recover_kd_context_metadata.py`, a CPU-only helper that replays the original `Salesforce/wikitext` extraction used by `scripts/run_kd_alignment.py`: skip raw rows beginning with `=`, split rows into sentences, keep 4-45 word sentences, deduplicate, and exclude Tuckute stimuli. The helper verifies exact equality against `data/kd_corpus/wikitext103_sentences_train.txt` and `data/kd_corpus/wikitext103_sentences_heldout.txt`, then writes gitignored JSONL metadata under `outputs/E016_tribe/kd_context_metadata/` with `split_index` as the join key for target-cache `item_indices`.

Verification:
- `uv run python -m py_compile scripts/e016_recover_kd_context_metadata.py` passed.
- `HF_HOME=/home/centcom/data/hf-cache uv run python scripts/e016_recover_kd_context_metadata.py --overwrite` returned `corpus_replay="exact_match"`.
- The replay verified 96,000 train rows and 2,000 heldout rows. The active launcher uses the prefixes 95,999 and 1,999.
- Context availability in the recovered metadata: train `doc_title_available=96000`, `same_doc_previous_available=95163`, `same_row_previous_available=73716`, `unique_doc_titles=837`; heldout `doc_title_available=2000`, `same_doc_previous_available=1988`, `same_row_previous_available=1487`, `unique_doc_titles=13`.

Design implication: if E016 is positive and survives the prepared sentence-local `textfeat` control, a long-context non-brain target-cache family is mechanically feasible as `contextfeat_mse` / `contextfeat_perm`. It should condition a frozen teacher on recovered preceding same-document context, keep the same Phase-3 budget and target dimension, and include a block-permuted twin. This does **not** solve the on-policy comparator; student-rollout teacher supervision remains a separate runner protocol.

**Status:** context-control feasibility and metadata recovery only. No target cache was built, no training was launched, no run JSON exists yet for the active E016 full run, no analyzer verdict exists, no science claim exists, and no rung flipped.

### Step 39 - `contextfeat` target-cache builder added and CPU-smoked (2026-07-03)
Added `scripts/build_context_feature_target_cache.py`, the possible long-context non-brain target builder for a future post-positive burden. It loads the recovered WikiText context metadata, verifies selected corpus lines against metadata text, follows `previous_same_doc_global_index` to recover preceding same-document context, conditions a frozen LM on context plus target sentence, pools hidden states over the target sentence tokens, projects to the requested target dimension, and writes the same target-cache schema consumed by `scripts/run_tribe_phase3.py`.

Verification:
- `uv run python -m py_compile scripts/build_context_feature_target_cache.py scripts/e016_recover_kd_context_metadata.py` passed.
- CPU smoke command: `HF_HOME=/home/centcom/data/hf-cache uv run python scripts/build_context_feature_target_cache.py --split train --start 0 --limit 4 --model sshleifer/tiny-gpt2 --target-dim 16 --max-length 64 --batch-size 2 --device cpu --out outputs/E016_tribe/kd_targets/context_feature/smoke_train_contextfeat_d16.npz --overwrite`.
- Smoke output: `shape=(4, 16)`, `context_items_with_previous=3`, saved under `outputs/E016_tribe/kd_targets/context_feature/smoke_train_contextfeat_d16.npz`.

Design implication: if E016 is positive, survives textfeat, and reviewers still need a long-context non-brain control, the next target label should be `contextfeat` with arms `contextfeat_mse` and `contextfeat_perm`. Do **not** run the full contextfeat cache or training while the active TRIBE run is incomplete; this is only plumbing.

**Status:** contextfeat target-cache plumbing only. No full contextfeat cache was built, no training was launched, no run JSON exists yet for the active E016 full run, no analyzer verdict exists, no science claim exists, and no rung flipped.

### Step 40 - Future control runs can retain trained student artifacts (2026-07-03)
Found a post-positive branch fragility while the active full TRIBE run was still training: `scripts/run_tribe_phase3.py` computed metrics, appended a row, and deleted each trained student without saving it. That is sufficient for the predeclared synthetic-target E016 gate, but it makes later probe or real-brain follow-up more expensive because selected arms would need to be rerun.

Added opt-in trained-student artifact retention to `scripts/run_tribe_phase3.py`:

- `--save-model-dir DIR` saves each per-arm student under `DIR/seed{seed}_{arm}_lambda{lambda}` using Hugging Face `save_pretrained`.
- The tokenizer and an `e016_model_artifact.json` metadata sidecar are saved with each artifact.
- `--overwrite-model-artifacts` is required to overwrite an existing arm artifact directory.
- Each run row records `model_artifact_dir` when saving is enabled.

Updated `scripts/e016_make_textfeat_control_script.py` so the queued post-positive textfeat control will save trained students under `outputs/E016_tribe/phase3/model_artifacts/textfeat_gpt2_n95999_s0-1-2_lam0.1/` if it is ever launched.

Verification:
- `uv run python -m py_compile scripts/run_tribe_phase3.py scripts/e016_make_textfeat_control_script.py` passed.
- A tiny CPU smoke with `sshleifer/tiny-gpt2`, the 2-item smoke TRIBE cache, `--skip-target-r2`, and `--save-model-dir outputs/E016_tribe/phase3/model_artifacts/smoke_save_model_test` saved all three expected arm artifacts and wrote non-null `model_artifact_dir` fields in the run JSON.
- `uv run python scripts/e016_make_textfeat_control_script.py --force` regenerated `outputs/E016_tribe/phase3/run_textfeat_control_20260703.sh`.
- `bash -n outputs/E016_tribe/phase3/run_textfeat_control_20260703.sh` passed.

Design implication: future textfeat/contextfeat or rerun-selected TRIBE arms can preserve trained students for post-hoc probes or real-brain evaluation. The currently active TRIBE full run was already in flight before this option existed, so it should still be treated as metrics-only unless selected arms are rerun with artifact saving. This is infrastructure only, not a result.

**Status:** model-artifact retention plumbing only. No active run was stopped or modified, no new full control was launched, no analyzer verdict exists, no science claim exists, and no rung flipped.

### Step 41 - Saved students can be scored on the real Tuckute endpoint (2026-07-03)
Added `scripts/e016_eval_saved_student_alignment.py`, a post-hoc helper for the positive-branch burden where synthetic-target gains must be separated from real-brain alignment. It reads an E016-style run JSON, loads rows with `model_artifact_dir`, and scores each saved student on Tuckute 2024 with the E003 anti-confound protocol: contiguous 5-fold variance partition, unique contextual R2 over length, position, and fixed static-embedding nuisance, plus verdict-layer PCA robustness.

Intended use:

- Run only after selected full-scale students exist from `--save-model-dir` runs.
- Use the same fixed nuisance reference model across arms, normally `gpt2-medium`.
- Treat the output JSON as a diagnostic input to `/interpret`; it does not establish an E016 verdict or a real-brain paper claim by itself.

Verification:

- `uv run python -m py_compile scripts/e016_eval_saved_student_alignment.py` passed.
- CPU smoke on the tiny artifact-retention run loaded one saved `sshleifer/tiny-gpt2` student, scored Tuckute with `--reference-model sshleifer/tiny-gpt2 --limit-rows 1 --n-pca 2 --pca-robust 2`, and wrote `outputs/E016_tribe/phase3/phase3_smoke_save_model_test.tuckute_alignment.json` with `artifact_rows_scored=1`.

Design implication: the top-venue positive branch now has a concrete real-brain probe path for artifacted students. The active TRIBE full run is still metrics-only unless selected arms are rerun with artifact saving, so this does not change the current E016 gate.

**Status:** real-brain evaluation plumbing only. No active run was stopped or modified, no new full control was launched, no analyzer verdict exists, no science claim exists, and no rung flipped.

### Step 42 - Full TRIBE Phase-3 artifact reached analyzer-ready handoff (2026-07-03)
The full GPT-2-medium to GPT-2 TRIBE Phase-3 run completed after the S76 close and produced the expected 9-row grid at `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.json`. The guarded finalizer refreshed the analyzer and readiness packet at `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.analysis.json` and `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.readiness.json`.

Gate state:

- `gate.science_ready=true`
- `arm_seed_grid_complete=true`
- `all_paired_common_seeds=true`
- `ppl_matched_all_lambdas=true`
- `has_heldout_target_metric=true`
- `train_size_ready=true`, `heldout_size_ready=true`, `target_dim_ready=true`
- `paper_branch_hint.branch="tribe_positive_needs_textfeat"`

The independent `/interpret` recompute audit at `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.interpret_audit.json` matched the analyzer on the complete grid, paired deltas, and PPL checks. At lambda 0.1, the TRIBE target arm exceeded the permuted target arm on the synthetic target endpoint on all three paired seeds: mean target-R2 delta `+0.071871`, seed values `[+0.067040, +0.075710, +0.072863]`, sign-flip `p=0.25`. It also exceeded KD-only on all three paired seeds: mean delta `+0.077492`, seed values `[+0.077134, +0.076934, +0.078409]`, sign-flip `p=0.25`. Mean relative PPL deltas versus KD-only were `0.004973` for TRIBE-target and `0.004875` for TRIBE-permuted, with all per-seed deltas below the 0.05 matching tolerance.

The branch router returned `status="textfeat_control_required"` and `route="run_textfeat_after_resource_check"`, with `active_runner_process_count=0` for the completed TRIBE job. The reason is explicit: a TRIBE-only positive cannot support brain specificity, so the matched-information text-feature control is required next.

**Status:** analyzer-ready handoff and branch routing only. This records a TRIBE-positive synthetic-target route, not a final E016 verdict and not a brain-specific claim. No ladder rung flipped.

### Step 43 - Full `textfeat` matched-information control launched (2026-07-03)
After confirming the TRIBE runner was complete and resources were free, the prepared matched-information control launcher was started as a detached background job:

- launcher: `outputs/E016_tribe/phase3/run_textfeat_control_20260703.sh`
- active process group root at launch: PID `3428588`
- GPU: `GPU=1`, with `HF_HOME=/home/centcom/data/hf-cache`
- log: `outputs/E016_tribe/phase3/phase3_full_textfeat_gpt2_n95999_s0-1-2_lam0.1.log`
- target run JSON: `outputs/E016_tribe/phase3/phase3_full_textfeat_gpt2_n95999_s0-1-2_lam0.1.json`
- target analyzer JSON: `outputs/E016_tribe/phase3/phase3_full_textfeat_gpt2_n95999_s0-1-2_lam0.1.analysis.json`
- saved-student artifact root: `outputs/E016_tribe/phase3/model_artifacts/textfeat_gpt2_n95999_s0-1-2_lam0.1/`

The clean active run began at `2026-07-03T07:21:00Z`. The log also contains an earlier diagnostic/trace prelude from failed supervision attempts; the active detached run is the `setsid` launch with PID `3428588`.

The launcher built and validated both full text-feature caches before entering training:

- train cache: `outputs/E016_tribe/kd_targets/text_feature/gpt2-medium/train_start0_n95999_d20484_full.npz`, shape `(95999, 20484)`, `elapsed_s=176.718`, finite, `missing=0`
- heldout cache: `outputs/E016_tribe/kd_targets/text_feature/gpt2-medium/heldout_start0_n1999_d20484_full.npz`, shape `(1999, 20484)`, `elapsed_s=9.014`, finite, `missing=0`

At the latest monitored sample, the control had entered `scripts/run_tribe_phase3.py` for the full GPT-2 textfeat arms, with seed 0 `kd_only` active. GPU 1 was using about 5.4-5.6 GiB and nonzero utilization. No textfeat run JSON or analyzer JSON existed yet.

**Status:** matched-information control running. No textfeat result exists yet, no TRIBE-vs-textfeat comparison exists, no brain-specific claim exists, and no rung flipped.


## Related
- [`ladder.md`](../ladder.md) — the canonical status board
- [`map.md`](../map.md) — code system (Q/E/A/D/L) & journey map
