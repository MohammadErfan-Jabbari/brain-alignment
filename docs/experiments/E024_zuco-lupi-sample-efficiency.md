# Experiment — E024: brain/cognitive signal as train-only PRIVILEGED INFORMATION → sample-efficiency (ZuCo, P1)

**Created:** 2026-06-18 (S25) · **Status:** DESIGN (data staging; pre-oracle) · **Mode:** working
**Direction:** `expansion-program.md` §8 (the S24 privileged-information / sample-efficiency trajectory, P1) — the charter's
**F2** returned to with a theory (LUPI), a higher-SNR regime (EEG+gaze), and the 5-control battery it lacked.
**Theory:** `06-theory-grounding.md` §1 (MI bound), §2 (DPI ceiling); Lopez-Paz 2016 / Vapnik LUPI; Provodin 2024 (LUPI
gains can be artifacts → zeroed-PI mandatory).
**Predecessors:** E009/E017 (the matched-ppl induction nulls — this changes the *metric* from encoding-R² to the learning
curve, the unmeasured channel L041 named). Q4/A3 bounded null is "argued-shut, not measured-shut" on exactly this axis.

---

## The question (estimand-first)
**Does a per-word brain/cognitive signal (ZuCo EEG + eye-tracking), used as TRAIN-ONLY privileged information, improve an
LLM-based classifier's SAMPLE EFFICIENCY** — i.e. shift the learning curve (test accuracy vs number of labeled training
examples) up/left — **on a text task where the signal is never available at test time**, and does any such gain survive
the full 5-control battery (so it is *biosignal-specific*, not "any side-channel helps")?

- **Estimand:** the area between learning curves (or the labeled-example count to reach a fixed accuracy) for
  PI-augmented vs text-only training, on held-out test sentences, as a function of training-set size
  $n \in \{$ small … full $\}$. Primary contrast at the **low-data** end (where LUPI theory predicts the gain, if any, concentrates).
- **Estimator:** repeated stratified subsampling at each $n$ (≥10 resamples), test accuracy/F1 on a fixed held-out split;
  paired across the PI / control arms (same subsamples, same seeds).
- **Identifying assumption:** the only thing that differs across arms at a given $n$ is *what privileged signal shapes
  training* — text, labels, splits, backbone, and budget are byte-identical. A gain attributable to the brain signal
  requires it to beat the matched-information non-brain teacher (control 5), or it is "any-teacher-helps," not biosignal.

## LUPI is the bound to beat, not a promise (grounded prior → predeclared expectation)
Lopez-Paz/Vapnik: train-only information lifts the learning rate $O(1/\sqrt n)\to O(1/n)$ **only when it is low-noise and
hypothesis-space-reducing.** ZuCo EEG/gaze is higher-SNR than fMRI but still noisy. So the honest predeclared prior is:
**a modest low-data gain is plausible (ZuCo is the regime where it *could* appear) but the null is fully expected**, and a
gain is only interesting if it (a) concentrates at low $n$, (b) is biosignal-specific (beats control 5), and (c) the
representation actually moved (control 3). This is the calibration in §8: methodology/negative most likely, positive = tail.

## Task + data (ZuCo 1.0 task1-SR — SST sentiment)
- **Text task:** ternary (or binary) **sentiment** classification of the SST-derived sentences read in ZuCo 1.0 task1-SR.
  Text → label is the learnable task; the gold labels ship with the SST provenance.
- **Privileged signal (train-only):** per-word EEG frequency-band power (theta/alpha/beta/gamma) + eye-tracking
  (gaze duration, fixation count, total reading time, saccades), aggregated to a per-sentence privileged vector
  (the zuco-benchmark `sent_gaze_sacc_eeg_means` family is the reference aggregation).
- **Backbone:** a frozen/LoRA LLM (Qwen2.5-0.5B, verdict-layer middle hidden state — the thesis's LLM-middle-layer
  geometry, the differentiation from Hollenstein's bespoke encoders) → sentence embedding → classifier head.
- **Splits:** strict no-sentence-overlap train/test (L003 — sentence-level, so no temporal autocorrelation, but a
  sentence must never appear in both). Cross-subject = secondary, reported separately, never pooled (hidden-averaging).

## The PI mechanism (how train-only signal enters)
Two standard LUPI routes, predeclared, run both:
1. **Distillation / SVM+-style (primary):** the privileged vector trains a *privileged model* (or per-example
   importance/difficulty weights) that reshapes the text-only model's training loss — knowledge transferred at train
   time, dropped at test. Lopez-Paz "generalized distillation."
2. **Auxiliary multi-task head (secondary):** an auxiliary head predicts the privileged signal from the LLM embedding
   during training (shaping the representation), removed at test. CogAlign-style, but with the LLM-middle-layer geometry.

## The 5-control battery (LOAD-BEARING — §8; a gain must beat ALL of them)
1. **Phase-randomized shape-twin** (L049) — privileged signal with its temporal/marginal *shape* preserved but content
   destroyed (FFT→randomize phase→inverse, rank-matched). Catches a regularization-by-shape artifact (the E021-v4 fool).
2. **Zeroed / shuffled-PI** (Provodin TRAM; Pirlot shuffled-label) — privileged vector zeroed, and separately shuffled
   across examples. A LUPI gain that survives shuffling is an artifact of the *mechanism*, not the information.
3. **Representation-move gate** (L042) — the PI must actually change the learned representation (Δ embedding/Δ decision
   boundary above an exhaustion floor); a no-op that "preserves accuracy" is not a manipulation. Fires first.
4. **Matched-budget / matched-ppl** — every arm gets identical compute, identical backbone, identical regularization
   strength; the only difference is the privileged signal's content.
5. **Matched-information non-brain privileged teacher (the decisive one)** — the real biosignal must beat the *best
   non-brain* privileged teacher matched for capacity + reliability: LM surprisal per word, a teacher-LLM hidden state,
   or a text-derived difficulty score. **Only beating this shows the gain is biosignal-specific, not "any teacher helps."**

## Predeclared kill / win criteria
- **Rep-move gate (control 3) FAILS** → "no manipulation"; report and stop; not a null about LUPI.
- **WIN (Fork-A-qualifying for the forward program):** PI-augmented learning curve beats text-only AND beats controls
  1, 2, 5 (paired, CI excludes 0, gain concentrated at low $n$), gate-3 passed, matched budget. → the brain signal buys
  sample-efficiency → a genuine positive, STOP for Erfan (do not flip a rung unilaterally).
- **NULL (the expected outcome):** PI ≈ text-only at all $n$, OR PI's apparent gain is matched by the shape-twin /
  shuffled-PI / non-brain teacher → LUPI's precondition is violated at ZuCo SNR → the methodology contribution (the
  control battery that kills the apparent gain) is the result. The strongest negative/methodology paper.

## Build cost (honest — a multi-day supervised build, lighter than Q3)
1. ZuCo 1.0 task1-SR `.mat` → per-sentence text + sentiment label + privileged feature vector (reuse zuco-benchmark
   `data_loading_helpers.py` / `extract_features.py`; ZuCo 1.0 SR loader differs from the 2.0 NR/TSR path — verify).
2. LLM-embedding sentence classifier + the two PI mechanisms + the 5 control arms.
3. The learning-curve harness (subsampling, paired seeds, CI).
4. anti-confound + oracle gate BEFORE any verdict (this doc → /precheck).

## Status / next
DESIGN written + GATED (S25). anti-confound-designer assembled the operational battery; **oracle-reviewer = HOLD / NOT-YET.**
The gate caught — before compute — that the substrate as locked is underpowered and mis-framed.

### Oracle HOLD (S25) — three locked fixes before /precheck PASS
1. **RE-SUBSTRATE off 400-sentence ZuCo-1.0-SR-sentiment.** 400 sentences (123 neu/137 neg/140 pos) → at n∈{16,32,64}
   with a ~100-sentence test set the MDE (binomial SE ≈5pp) swamps any plausible low-n LUPI gain; R=20 resamples re-draw
   the same ~300 pool (not independent → residual pseudo-replication, C6/L015). A null here would be underpowered, not
   "the battery killed a gain" (the L021/L038 instrument-can't-estimate trap). **Sharper substrate (oracle):**
   (a) **eye-tracking-first** — gaze/reading-time is ~an order more reliable than per-sentence EEG band-power and is the
   ZuCo channel prior work shows actually helps NLP; if clean gaze can't help, EEG is hopeless. (b) a **larger-N reading
   corpus** for a real low-n regime (Provo / GECO / Natural-Stories gaze, or pool ZuCo NR). (c) run the **synthetic-PI
   MDE positive-control FIRST** (plant a known label-correlated signal at the measured biosignal reliability) — one day,
   tells us whether ANY effect is detectable before building five arms.
2. **Control 5 fairness (false-null + false-positive holes):** (a) MEASURE the biosignal's split-half reliability on the
   chosen set *before* setting the noise-injection target — else all teachers degrade to the floor and tie at text-only
   (false null masking a vacuous manipulation). (b) Add a **label-correlated text teacher** (valence-lexicon score),
   rank+reliability-matched — if the biosignal only beats surprisal/hidden-state but ties the valence teacher, the gain
   is affect-leakage (arousal↔valence), not cognition.
3. **Per-word loader decision + leak probe:** the reference `extract_features.py` aggregates to one vector/sentence and
   exposes NO per-word timeseries → the decisive L049 phase-randomized shape-twin can't be built (only a weaker
   covariance twin). Raw `.mat` `word_data` carries per-word signal but needs a NEW loader. Decide: write it, or
   downgrade control-1 and say so in the kill criteria. ALSO add a direct **PI→label MI probe** (train a classifier on
   the PI vector alone) — convergence-at-full-n alone is a weak label-leak detector.

### Data-readiness correction
On disk so far: `data/zuco1/osfstorage/` has only **task3-TSR** (the clone pulls alphabetically; NR/SR arrive later).
The reference loader's `class_task='tasks-cross-subj'` is reading-task classification, **not sentiment** — the sentiment
substrate is NOT staged. ZuCo 2.0 SR EEG assets sit under `data/zuco-benchmark/matlab/` but are 2.0, aggregated.

**NEXT (needs Erfan's substrate call): pick the re-substrate (recommended: eye-tracking-first on a larger-N gaze corpus),
then synthetic-PI MDE positive-control → fix control 5 → per-word loader decision → re-gate → build. No verdict without the gate.**
