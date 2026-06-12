# Experiment — E016: TRIBE-v2 synthetic brain targets — can a brain foundation model break the data-scarcity wall, and what is the ceiling on brain-guided LM training?

**Created:** 2026-06-12 · **Status:** QUEUED — the **CAPSTONE (I4, LAST)** of the implementation roadmap; the
new task added at the end of the train, *after* I1 (E015-expand), I2 (external matched-ppl control), I3 (full-FT
door). P0 gate PASS; P1–P3 run once the train reaches it (or earlier if I3 walls on data — I4 sidesteps that
blocker by generating its own fMRI). · **Mode:** working (design→run→judge)
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
