---
title: "Experiment - E028: Vaidya cross-modal intervention falsification"
tags: [experiment]
aliases: [E028]
---

# Experiment - E028: Vaidya cross-modal intervention falsification

**Created:** 2026-07-16 · **Status:** DESIGN HOLD · **READY-TO-RUN:** NO · **Mode:** prospective
**Precheck verdict:** the first independent hostile design review returned HOLD. The ranked blockers are recorded in [Precheck](#precheck); no disaggregated Stage 1 endpoint has been unsealed.
**Direction:** Independent external application of Package A in [D057](../decisions/decisions.md). E027 remains reserved for Package C's internal matched-control branch, so this study uses E028.
**Primary external target:** [Vaidya et al., 2026](../literature/canonical/vaidya-2026_slow-fmri-fast-ecog-transfer.md), arXiv:2605.19224v1.

---

## Objective and claim boundary

Test whether the reported transfer from WavLM Base+ tuned on slow LeBel fMRI to fast Podcast ECoG survives exact reproduction, patient-level inference, nested lag/readout selection with confound subtraction, and comparison against both a phase-randomized fMRI shape twin and one optimization-, geometry-, and learnability-matched nonbrain audio target.

The endpoint population unit is an ECoG patient. The design is conditional on three fixed fMRI source participants, one fixed podcast, one fixed architecture, and the public Podcast cohort. Even a PASS would not identify arbitrary-donor, arbitrary-stimulus, or architecture-general transfer.

This study is scientifically independent of [E016](E016_tribe-synthetic-brain-targets.md) and [E025](E025_participant-e016-biological-transfer.md). It uses another architecture, speech rather than text, LeBel fMRI as the intervention source, and public Podcast ECoG as the endpoint. E025 motivates the gate structure but contributes no E028 target, checkpoint, feature, participant, or outcome.

## Competing explanations

- **Target-specific transfer:** stimulus-aligned fMRI supervision changes WavLM in a way that improves nuisance-subtracted ECoG prediction in unseen patients beyond equally budgeted phase and nonbrain auxiliary interventions.
- **Generic auxiliary training:** a stimulus-derived nonbrain target with comparable geometry, learnability, optimization pressure, representation movement, and generic speech quality yields the same ECoG gain.
- **Target-shape regularization:** a phase-randomized fMRI target preserving complete second-order within-story structure yields the same gain.
- **Selection or inference artifact:** the reported effect depends on flattening electrodes, selecting among 81 lags outside the outer training fold, omitting contiguous buffers, or omitting low-level speech nuisance features.
- **Reproduction failure:** the published aggregate cannot be regenerated from complete, hash-matched author artifacts.

## Primary sources and fixed public identities

- Paper: [arXiv abstract](https://arxiv.org/abs/2605.19224), [HTML](https://arxiv.org/html/2605.19224), and [PDF](https://arxiv.org/pdf/2605.19224). The audited source is v1, submitted 2026-05-19.
- fMRI source: [OpenNeuro ds003020](https://openneuro.org/datasets/ds003020). The live public root exposed `doi:10.18112/openneuro.ds003020.v3.1.1` at audit time. The paper's exact snapshot and story set remain unresolved factual slots.
- ECoG endpoint: [OpenNeuro ds005574 v1.0.2](https://openneuro.org/datasets/ds005574/versions/1.0.2), DOI `10.18112/openneuro.ds005574.v1.0.2`, CC0.
- Dataset-owner ECoG code: [hassonlab/podcast-ecog-paper](https://github.com/hassonlab/podcast-ecog-paper) and [hassonlab/podcast-ecog-tutorials](https://github.com/hassonlab/podcast-ecog-tutorials). These are not the Vaidya implementation.
- Local speech brain-tuning scaffolds: `data/paper-repos/multi-brain-tuning` and `data/paper-repos/brain-tuning`. They may supply implementation components but cannot establish exact reproduction.

The public metadata lists exactly `sub-01` through `sub-09`. The paper reports a 1,268-electrode analysis mask; that mask is not inferred from the public raw-electrode count and remains an author-artifact fact to verify.

## Outcome seal, protocol freeze, and hash boundary

The full scientific protocol is frozen before any disaggregated Stage 1 endpoint is opened. “Stage 1 endpoint” includes an author electrode/patient/fold table, raw out-of-fold predictions, locally computed per-electrode or per-patient scores, and any file from which those values can be recovered. Published aggregate prose and figures already in the public paper are not treated as newly unsealed outcomes.

The authorized order is:

1. Run metadata-only inventory and obtain factual method artifacts. Hash any author result table without parsing it, and keep it encrypted or under an outcome custodian.
2. Fill only the factual slots listed below. Implement the complete Stage 1A reproduction runner, Stage 1B corrected evaluator, Stage 2 phase arm, Stage 3 matched-audio constructor/trainer, and final analyzer.
3. Pass unit tests, leakage tests, deterministic replay tests, and a dimension-scale synthetic benchmark without neural or author-result values.
4. Run anti-confound and oracle design review. Incorporate their outcome-blind corrections.
5. Freeze one canonical protocol bundle containing this E record, canonical JSON configuration, acquisition/source manifests, environment lock, runner, analyzer, test fixtures, expected test outputs, benchmark report, and every executable dependency. Record SHA-256 for every file and a canonical SHA-256 over the ordered bundle manifest.
6. Have a fresh independent reviewer verify that exact bundle and return `DESIGN PASS / READY-TO-RUN: YES` without endpoint access.
7. Only then may the sealed disaggregated Stage 1 values be opened or ECoG payloads be acquired and scored. The predeclared sequential gates may then stop later training, but they may not change its design.

The hash boundary covers **all of Stages 1A, 1B, 2, and 3**, not merely the next executable stage. After endpoint unsealing, every design review is abort-only: a reviewer may invalidate the study, stop compute, or narrow the claim, but may not change arms, candidates, layers, seeds, targets, folds, buffers, nuisance features, metrics, estimands, inference family, thresholds, equivalence margins, exclusions, or robustness rules. A necessary correction creates a terminated protocol version and requires a new outcome-blind study; the already observed endpoint cannot tune its replacement.

### Factual slots that author artifacts may fill before the hash boundary

Only the following paper-implementation facts may be filled without being treated as design adaptation:

- exact WavLM Base+ repository/revision/files, processor, layer indexing, LoRA module names, and checkpoint serialization;
- exact ds003020 snapshot, three source identifiers, story lists, audio-to-TR offsets, voxel masks, response normalization, and paper training/validation split;
- exact ds005574 snapshot confirmation, paper electrode/ROI mask, faithful four-fold boundaries, preprocessing, lag convention, ridge grid, and published aggregation;
- launch commands, dependency lock, random states, principal checkpoints, selected epochs, and full-precision published result/prediction table.

If a factual artifact contradicts a choice that affects the corrected scientific lane, the protocol remains HOLD, is revised while outcomes stay sealed, is rehashed, and is independently re-reviewed. It is not silently patched. Details below that do not depend on the authors are fixed now.

## Stage 0: artifact and metadata gate

### Author artifacts required for the exact lane

Use the unsent [E028 author-artifact request](../references/e028-vaidya-artifact-request-email.md) only after Erfan authorizes communication. The exact lane requires:

1. paper-specific code commit, environment lock, launch commands, and uncommitted patches;
2. exact base-model identifiers/files and all LoRA configuration;
3. source snapshot, source/voxel/story/audio-response manifests, and preprocessing offsets;
4. three principal source-specific checkpoints, epoch-selection records, and validation statistics;
5. endpoint mask, ROI table, fold boundaries, ridge/lag implementation, and random states;
6. full-precision electrode-by-patient-by-source values with chosen lag and fold prediction pointers;
7. SHA-256 and redistribution terms for every supplied item.

An exact lane exists only when the supplied artifacts make the paper analysis deterministic and auditable. Otherwise the work is explicitly an `independent reimplementation`; absence of artifacts is not called a reproduction failure.

### Metadata-only validation completed

The only E028 network/acquisition command executed for this repair was metadata-only:

```bash
cd /home/centcom/data/brain-alignment
uv run python scripts/e028_acquisition_manifest.py
```

The 2026-07-16 validation listed remote object metadata, read a small descriptive allowlist, queried dataset-owner commit metadata, and statted local filenames/sizes. Its scoped ledger also records the script self-read, local repository `rev-parse` metadata reads, and the manifest output write. It downloaded no ECoG, audio, fMRI, weight, checkpoint, or result-table payload; opened no neural value; trained/scored no model; and contacted no author. Those access flags are explicitly scoped to this script invocation, not to other processes.

The validated ds005574 v1.0.2 root contains 159 objects totaling 15,507,131,310 bytes. The exact minimal future set contains eight global keys plus one high-gamma file and four metadata files for each of the nine exact patient IDs: 53 objects totaling 4,992,680,616 bytes. Directory and filename subject IDs agree for every patient. The version-bound canonical listing digest is `d17b3bcaa0c264406a1fe7473ee13eca9e3462a1c16124d397f8cc0517e71c2a`.

- Metadata script SHA-256: `733cbdc7733e2dc4bbee6594a0deefaaa1b6f2aa50b1584073361eff3f574870`.
- Generated manifest SHA-256: `9ffed7d6793f4685a3a015990df530e94fb7e47676057474fca44dc99a951c5c`.
- Dataset-owner code heads observed: `e7ba666e09865b1918c2c7d547784f1eb6d626fe` and `2a984dfc935d5e95111ce573b8061f4a1d6e32ee`.

Remote S3 ETags remain transfer hints, never SHA-256. The local LeBel staging area has 84 fMRI story files for UTS03 and 21 each for UTS01 and UTS02, plus 84 WAV and TextGrid files; this does not match the paper's reported 94–103 stories per source participant and cannot be silently substituted.

## Frozen arm vocabulary

- `F`: untouched pretrained WavLM Base+.
- `B_author(q)`: the supplied principal fMRI-tuned checkpoint for source `q`, used only in Stage 1 reproduction/corrected reanalysis.
- `B_reimpl(q)`: the single source-specific checkpoint produced by a prospectively accepted independent-reimplementation lane when `B_author` is unavailable.
- `B_1(q)`: the Stage 1 checkpoint actually used in the corrected gate: `B_author` in the exact lane or `B_reimpl` in the explicitly labeled reimplementation lane, never a mixture.
- `B(q,s)`: a fresh real-fMRI run for source `q` and seed `s` under the frozen training recipe.
- `P(q,s)`: the paired phase-randomized fMRI run.
- `A(q,s)`: the paired, preselected matched-audio run.

The source set is the paper's three fMRI participants. Fresh-training seeds are exactly `0, 1, 2`. `F` is evaluated once per outer fold and copied as the common paired baseline; it is not retrained or jittered per source/seed.

## Stage 1A: faithful reproduction lane

The faithful lane uses only complete hash-matched author code, masks, preprocessing, checkpoints, and aggregation. It reproduces the paper's electrode-level regression, four folds, lag selection, ROI/all-cortex aggregation, and Pearson-correlation endpoint exactly, even when those choices differ from Stage 1B.

- Regenerate every supplied full-precision electrode and aggregate value. With deterministic stored features/regression, maximum absolute error must be `<= 1e-5`. For an explicitly rounded table, every value must lie inside its rounding interval.
- Reproduce the paper's all-cortex tuned-minus-pretrained direction before inspecting any newly computed control endpoint.
- If complete, hash-matched author artifacts miss the tolerance, classify the **exact reproduction lane** as failed. If the artifacts are incomplete, classify it unavailable. A public-data reconstruction never inherits the word exact.

The faithful lane describes whether the paper can be regenerated. It cannot override failure of the corrected patient-level lane.

## Stage 1B: corrected evaluator frozen before unsealing

### Time support, folds, lag, and features

1. Resample the podcast waveform to mono 16 kHz with the exact library/version locked in the runner. Define audio time zero as the first podcast sample associated with the frozen BIDS stimulus-onset event. The author-supplied acquisition clock/response offset is a factual slot; it is applied once, recorded in samples and seconds, and never estimated by cross-correlation with neural data.
2. Use the supplied `desc-highgamma` derivatives without another band-pass or envelope transform. On the audio clock, define response center `t_k = 4.00 + 0.05k` seconds. For every channel, average all finite derivative samples in `[t_k - 0.025, t_k + 0.025)`; require at least 90% of the nominal source-sample count, exclude any bin intersecting a BIDS bad annotation, and never interpolate a failed bin. If the derivative is already exactly 20 Hz and phase-aligned, this rule yields its one sample per bin. Source sampling frequency, first-sample timestamp, stimulus onset, offset, and resulting bin-index map are bundle-hashed.
3. Each WavLM input is the half-open waveform window `[t_k - 4 s, t_k)`, with no left padding. From the fixed layer-9 hidden tensor, calculate output-frame centers from the hash-matched convolution strides/kernels and average exactly those frames whose centers fall in `[t_k - 0.05 s, t_k)`. Require at least one such frame and a 768-value vector; no whole-window pooling or endpoint-nearest substitution is permitted.
4. Intersect finite response, WavLM, nuisance, and transcript support once; trim support for the full `[-2, 2]` second lag range before constructing folds, so every lag sees identical time samples. Assert that the retained grid is one contiguous sequence with 50 ms spacing; any gap is protocol-invalid rather than silently collapsed.
5. Partition the ordered common support into four chronological blocks with `numpy.array_split` semantics: lengths differ by at most one and earlier blocks receive any remainder. These exact index arrays are saved in the bundle. For outer fold `k`, block `k` is test and the other three blocks are train.
6. Remove 120 samples (6 seconds) from **both sides** of every train/test or inner-train/inner-validation boundary. At a recording edge remove only the existing side. Boundary samples are never predicted. The embargo covers the 4-second representation context plus the maximum 2-second lag.
7. Inner selection rotates the three surviving outer-training blocks: each block is validation once and the other two are training. There is no random split. All means, scales, nuisance transforms, ridge parameters, lag selectors, and zero-variance decisions are fitted inside each inner-training split.
8. The fixed lag grid is `-2.00, -1.95, ..., 1.95, 2.00` seconds. At lag `ell`, `X(t-ell)` predicts `Y(t)`; positive lag therefore means neural response after the representation. For each outer fold/electrode, jointly select the pretrained lag and pretrained full-model penalties on mean inner unique R2. Freeze that lag across `F`, `B_author`, `B`, `P`, and `A`; each arm may retune only its ridge penalties inside the same outer-training data.
9. Ties within `1e-12` are resolved lexicographically by smallest absolute lag, numeric lag, global penalty, then group-ratio penalty. No layer, lag, patient, electrode, ROI, nuisance, or hyperparameter grid is changed from endpoint results.

Layer 9 is fixed. The exact base-model revision and whether the paper labels embeddings as layer 0 are factual slots; the bundle must map the human label to one exact tensor name and shape. Feature extraction is deterministic evaluation mode with no dropout.

### Fixed nuisance construction

All nuisance features are stimulus-derived and computed without neural values.

- Log-mel: 25 ms periodic Hann window, 10 ms hop, 512-point FFT, 64 HTK mel bins from 50 to 8,000 Hz, `log(1e-6 + power)`, averaged within half-open 50 ms bins.
- RMS: the same 25/10 ms frames, averaged within the same bins.
- Pitch/voicing: deterministic YIN, 50–500 Hz; unvoiced pitch is zero and a separate voicing indicator is retained. The exact implementation and numerical version are bundle-hashed.
- Transcript events: word-onset and phoneme-onset counts per 50 ms bin, plus trailing one-second word and phoneme counts using exactly the current and previous 19 bins.
- Position: elapsed valid podcast time divided by total valid podcast time.

The primary nuisance matrix `N` is the 64 log-mel values plus RMS, pitch, voicing, four event/rate values, and position. A strong sensitivity appends frozen GloVe 6B 300-dimensional lowercase word vectors, held from each word onset to the next; punctuation-only and out-of-vocabulary tokens receive zero plus an OOV indicator. The exact GloVe file hash is mandatory before the bundle freezes. Lexical nuisance is a sensitivity because it may remove genuine higher-level signal.

### Fixed regression and score

For every fold, predictor columns are centered/scaled on training samples. Columns with training SD `< 1e-8` are dropped and the mask is reused on validation/test. High-gamma targets remain in native units; the intercept is unpenalized.

The nuisance-only model uses ridge penalties `alpha = 10^k`, `k = -6, -5, ..., 8`. Its alpha maximizes mean inner-validation `R2(N)`. The full model minimizes

`mean((Y - beta0 - N betaN - X betaX)^2) + alpha ||betaN||2^2 + alpha*rho ||betaX||2^2`,

with the same `alpha` grid and `rho in {1e-4, 1e-2, 1, 1e2, 1e4}`. At the pretrained lag-selection step, lag, alpha, and rho maximize mean inner-validation `R2(N + X) - R2(N)`. Once lag is frozen, each arm's alpha/rho maximizes that same inner unique-R2 criterion while reusing the already selected nuisance-only model. Selection is separate per electrode. Solver tolerance, maximum iterations, floating-point dtype, and failure behavior are frozen in the runner; a convergence failure is not rescued by widening the grid.

For outer test fold `k`, define `SST_k = sum_t (Y_t - mean(Y_outer-train))^2`. Pooled cross-validated R2 is `1 - sum_k SSE_k / sum_k SST_k`. The primary electrode score is

`M = R2_cv(N + X) - R2_cv(N)`.

The nuisance-only out-of-fold prediction is fitted once per electrode/fold and shared across arms. A separate paper-facing sensitivity fits `Y ~ X` only at the same frozen pretrained lag, using the same alpha grid and selecting alpha by mean inner Fisher-z Pearson correlation. It concatenates native-scale outer-fold predictions and targets and computes Pearson `r`, clipped to `[-1 + 1e-7, 1 - 1e-7]` before `z = atanh(r)`. Fold scores and fold p-values are not averaged. Any zero target variance, nonfinite prediction, solver failure, or missing outer block makes that patient/arm protocol-invalid and therefore INCONCLUSIVE; it does not license exclusion.

### Electrode and aggregation rules

The exact paper all-cortex mask, reportedly 1,268 electrodes, is primary when supplied and hash-matched. An accepted reimplementation instead uses every channel marked neural and good in the frozen BIDS metadata and reports its different mask explicitly. The two masks cannot be mixed. Destrieux auditory cortex and the paper's Lipkin language-network selection are secondary only when their exact mappings are supplied.

Electrodes are averaged equally within patient; patients are never weighted by electrode count. Source and seed values remain visible but are averaged before patient inference. The four blocks, electrodes, sources, and seeds are crossed/nested robustness axes, not extra biological replications.

## Stage 1 corrected activation gate

Let `x_C(u,q,s)` be the equal-electrode mean of `M` for patient `u`, source `q`, seed `s`, and arm `C`. For `B_1`, omit `s`. Define the Stage 1 corrected contrast

`b_1(u) = mean_q [x_B_1(u,q) - x_F(u)]`.

Stage 2 is licensed only if the exact lane passes (or Erfan explicitly accepts a labeled reimplementation), the Stage 1 Pearson/Fisher-z contrast is positive under its frozen aggregation, the one-sided 95% exact sign-flip lower bound for `mean_u b_1(u)` is above zero, at least 8/9 patient contrasts are positive, all three source aggregates are positive, and every leave-one-patient/source/block point estimate is positive. Failure stops before training. No observed Stage 1 effect is converted into a plug-in margin or used to redesign later arms.

## Stage 2: fresh brain and phase-randomized shape twin

### Paired training matrix

Train `B(q,s)` and `P(q,s)` for the three fixed sources and seeds `0, 1, 2`. Paired arms start from identical WavLM weights and RNG state and use identical example order, batches, optimizer steps, precision, and checkpoint cadence.

The intended paper recipe is rank-4 LoRA on the exact Q/K/V modules, rank-100 output head, spatial-correlation loss, Adam, learning rate `5e-4`, 30 epochs, batch size 10 TRs, paper story split, voxel mask, and audio windows. Every item is verified against author artifacts before the bundle freezes. Each arm selects one of epochs 1–30 by its own target on the same two fixed validation stories without ECoG access. The unseen LeBel test story is untouched.

### Phase target construction and manipulation gate

For each source, story, and paired seed, Fourier-transform the complete time-by-voxel target. Draw one independent phase for each positive non-Nyquist frequency using bundle-recorded `PCG64DXSM` seeds; multiply the full voxel coefficient vector at that frequency by the same unit-modulus complex phase, apply the conjugate at the negative frequency, and leave DC/Nyquist real. Invert per story. This preserves every within-story voxel auto- and cross-spectrum while destroying item alignment; it is a second-order shape twin, not a distribution- or information-matched target.

Before training, synthetic algebra tests require phase-modulus and complex-coefficient-amplitude errors `<= 1e-12`, relative cross-spectrum error `<= 1e-10` on 512 manifest-fixed voxel pairs, and standardized mean/SD error `<= 1e-8`. On real training targets, fixed pretrained WavLM plus the rank-100 head must predict the phase target with held-out R2 `<= max(0, 0.10 * R2_real)`. Any failed source/seed kills the manipulation; phases are not redrawn.

After training and before phase-arm ECoG scoring, the phase arm must have relative LoRA parameter-update norm `> 1e-6`, and layer-9 CKA distance and activation-RMS movement must each exceed `max(1e-6, 10 * duplicate-extraction noise)` for every source/seed. Failure is INCONCLUSIVE control validity, not evidence for brain specificity.

### Stage 2 to Stage 3 licensing gate

Stage 3 training is licensed only when the phase construction, alignment-destruction, training, movement, numerical, and hash gates all pass; simultaneous one-sided 95% max-T lower bounds for both `b_F` and `g_P` are above zero; at least 8/9 patients are positive for each; every source and seed aggregate is positive for each; and every leave-one-patient/source/block point estimate is positive for each. The corresponding fresh-brain Fisher-z direction must also be positive. A failed validity gate is INCONCLUSIVE; a valid statistical failure is classified by the terminal rules below. Neither case may trigger Stage 3 as a rescue analysis.

## Stage 3: one frozen matched nonbrain audio target

Stage 3 is constructed in the protocol bundle and runs only if the Stage 2 gate passes. It uses one lexicographically selected candidate family; ECoG never selects the teacher, layer, projection, multiplier, or replacement.

### Candidate grid and deterministic feature extraction

- Teacher: exact `openai/whisper-medium` revision and file hashes frozen in the bundle.
- Encoder layers: `6, 12, 18, 24`; Haar projection seeds: `0, 1, 2`; auxiliary-loss multipliers: `0.5, 0.75, 1.0, 1.5, 2.0`.
- Candidate order is layer, projection seed, then multiplier. Select the first candidate passing every pretraining gate for every source and paired training seed. If none passes, classify control non-identifiability and stop. Do not widen the grid.
- For each fMRI TR, feed the same mono 16 kHz half-open 4-second waveform window ending at that TR to the frozen Whisper processor, left-zero-padded only where the paper's fMRI grid precedes four seconds. Mean-pool non-padding encoder frames from the fixed layer. Cache exact float32 matrices and hashes before target construction.

### Frozen matched-target construction

For one source and candidate, use training stories only. Let `H` be concatenated Whisper features and let `Y` be the fMRI target after subtracting voxel means fitted on training stories. For `T` training rows and `V` voxels, record the single global scale `s_Y = ||Y||F / sqrt(TV)`; validation fMRI is never used in this construction.

1. Center and scale every `H` column on training stories; floor its covariance eigenvalues at `1e-6` of the largest and whiten. Apply those same transforms to validation stories.
2. Estimate one scalar zero-phase frequency response as follows. For each training story and each matrix separately, use `rfft(norm="ortho")` along time with no window, detrending, or zero-padding. Map frequencies linearly from DC to Nyquist into 128 half-open bins (Nyquist belongs to bin 127), sum squared coefficient magnitude over columns/stories, divide by the coefficient count in each bin, and normalize the 128-bin vector to unit mass. With `eps = 1e-8 * max(power)`, form `log R = 0.5 * [log(P_Y + eps_Y) - log(P_H + eps_H)]`. Smooth with the normalized `numpy.hanning(5)` weights under reflection padding, linearly interpolate log-response from bin centers to each story's Fourier frequencies with endpoint values held constant, multiply every feature coefficient at a frequency by the same positive `exp(log R)`, and use `irfft` at the original length. Any nonfinite response or response outside `[1e-4, 1e4]` fails without clipping. No validation fMRI value enters this filter.
3. SVD the concatenated filtered training matrix. Keep the first 100 right singular vectors. For training, use the corresponding normalized left scores; for validation, project with the training right vectors and divide by the training singular values. A singular value `< 1e-8` of the leader is a construction failure.
4. Let `sigma_Y` be the top 100 singular values of training `Y`. Convert them to the unit-global-SD rank-100 shape `sigma_tilde = sqrt(TV) * sigma_Y / ||sigma_Y||2`. This preserves the normalized top-100 spectrum while making `||sigma_tilde||2 / sqrt(TV) = 1`.
5. Draw a voxel-by-100 standard-normal matrix with the candidate's recorded `PCG64DXSM` seed, project every column orthogonal to the all-ones voxel vector, and take reduced QR. Make QR signs deterministic by requiring the largest-magnitude element of each column positive. This Haar basis may not use a brain spatial basis.
6. Form the standardized target `A_std = U_H diag(sigma_tilde) Q^T`, then restore scale exactly once: `A_train = s_Y A_std`. Use the training Whisper right vectors, singular-value normalization, `sigma_tilde`, `s_Y`, and `Q` unchanged for validation stories. Consequently `||A_train||F = ||Y||F` while the normalized top-100 spectrum matches `Y`; there is no second SD multiplication. No item-wise fMRI coordinate, learned brain readout, validation fMRI value, or ECoG value enters `A`.

All FFT normalization, frequency-bin membership, story padding, covariance/SVD driver, QR sign rule, dtype, eigenvalue ordering, and RNG seed are executable assertions in the bundle. A dimension-scale synthetic benchmark must demonstrate that this construction can run at the planned story-by-voxel dimensions without changing the algorithm.

For the temporal equivalence gate, define trace autocorrelation for lag `l` as `sum_t,v Y[t,v]Y[t+l,v] / sum_t,v Y[t,v]^2`, compute it separately per story, then average stories equally at lags `{1, 2, 4, 8, 16}` TRs. “Binned power” is the 128-bin unit-mass spectrum above, and Jensen-Shannon divergence uses natural logarithms with zero bins replaced by `1e-12` before renormalization.

For learnability, keep training stories in the frozen paper-manifest order and partition them into five contiguous story groups with `numpy.array_split`. Each group is outer validation once; within the other four, rotate one group as inner validation to choose `alpha in {1e-6, 1e-5, ..., 1e8}`. Use frozen pretrained layer-9 WavLM features from the same 4-second/end-50-ms pooling rule, fit ridge from features to each target's training-fitted top-100 score coordinates, reconstruct the rank-100 target, and compute pooled native-scale cross-validated R2 with each outer-training mean. Define headroom as `max(1e-6, 1 - R2)`. Ties choose the smallest alpha. No validation fMRI or paper validation story enters this diagnostic.

### Pretraining equivalence gates

| Diagnostic | Required margin for every source and paired seed |
|---|---|
| Ambient dimension, item identity/order, split, and rank-100 bottleneck | Exact equality |
| Standardized global mean and SD | Mean difference `<= 0.01`; SD ratio in `[0.99, 1.01]` |
| Normalized top-100 spectrum | RMS log-eigenvalue difference `<= 0.10`; sub-`1e-8` components explicitly fail |
| Variance mass at components 1, 8, 32, 64, 100 | Absolute difference `<= 0.02` at every cut |
| Within-story trace autocorrelation and binned power | Difference `<= 0.05` at every fixed lag; Jensen-Shannon divergence `<= 0.05` |
| Pretrained WavLM + rank-100 head target R2/headroom in blocked training-story CV | R2 difference `<= 0.02`; headroom ratio in `[0.90, 1.10]` |
| Initial standardized auxiliary loss and LoRA gradient norm | Loss difference `<= 0.05`; absolute log gradient-norm ratio `<= 0.10` |

Candidate learnability is measured by blocked cross-validation wholly within training stories. The two validation stories remain reserved for checkpoint selection. Passing means comparability only on these measured engineering axes; it does not make Whisper biologically equivalent to fMRI.

Initial loss/gradient diagnostics use the first hash-manifested training batch and paired initialization before any optimizer step. Center and divide each target by its training global SD, multiply the audio arm's mean-reduced auxiliary loss by its candidate multiplier (the brain arm uses the paper multiplier `1.0`), backpropagate once, and concatenate all LoRA-parameter gradients in canonical parameter-name order for the L2 norm. The selected multiplier remains fixed on every audio-training step; it is not only a calibration diagnostic. The output head initialization, batch indices, dtype, and loss implementation are otherwise identical across brain and audio arms and bundle-hashed.

The movement-quality probe is also frozen before unsealing. It uses one hash-manifested TIMIT release, the official TRAIN and CORE TEST speaker-disjoint split, the standard 61-to-39 phoneme mapping with silence retained as one class, and sentence labels `{SA, SX, SI}` from utterance IDs. Extract each arm's layer-9 native-frame features with the same hash-matched processor; use aligned frame features for phonemes and utterance means for sentence type. Standardize on TRAIN, select multinomial L2-logistic `C in {1e-4, 1e-3, ..., 1e4}` by five speaker-grouped folds on TRAIN, refit TRAIN, and report macro-F1 on CORE TEST. Use `lbfgs`, tolerance `1e-8`, maximum 5,000 iterations, seed 0, no class weights, and a hash-locked numerical library. Missing TIMIT files, split/label hashes, convergence, or exact probe implementation makes the quality gate INCONCLUSIVE; it cannot be replaced by another corpus.

Train the single selected `A(q,s)` with the exact `B/P` architecture, examples, batching, optimizer steps, precision, and checkpoint rule. Before ECoG scoring, require brain-versus-audio absolute log parameter-update and RMS-movement ratios `<= 0.10`, CKA-distance difference `<= 0.002`, and absolute TIMIT phoneme and sentence-type linear-probe F1 differences `<= 1.0` percentage point for every source-averaged seed. A mismatch is INCONCLUSIVE and cannot trigger candidate replacement.

## Primary paired estimands

For patient `u`, first compute equal-electrode means within each `x_C(u,q,s)`, then average paired source/seed contrasts:

- Fresh-brain fidelity gain: `b_F(u) = mean_q,s [x_B(u,q,s) - x_F(u)]`.
- Phase contrast: `p(u) = mean_q,s [x_B(u,q,s) - x_P(u,q,s)]`.
- Audio contrast: `a(u) = mean_q,s [x_B(u,q,s) - x_A(u,q,s)]`.
- Half-retention contrasts: `g_P(u) = p(u) - 0.5 b_F(u)` and `g_A(u) = a(u) - 0.5 b_F(u)`.
- Strict full-retention sensitivities: `h_P(u) = p(u) - b_F(u) = mean_q,s[x_F(u) - x_P(u,q,s)]` and `h_A(u) = a(u) - b_F(u) = mean_q,s[x_F(u) - x_A(u,q,s)]`.

Thus `g_P > 0` and `g_A > 0` mean that more than half of the **fresh, paired** brain gain remains beyond each control. No observed `theta`, ratio, or `delta_ref = 0.5 * theta` is plugged into a later test. The contrasts are paired linear functions of the same patient/source/seed cells. `h_P/h_A` ask the stricter sensitivity question of whether the control is no better than frozen WavLM; they cannot rescue a failed primary claim.

Compute analogous Fisher-z contrasts as faithful sensitivities. Report patient values, source values, seed values, patient medians, leave-one-patient/source/block estimates, and exact sign counts, but only the patient vectors enter population inference.

## Simultaneous inference and assumptions

The final primary family is `{b_F, g_P, g_A}`. For a candidate family mean vector `mu0`, form shifted patient residuals `r_uj = d_uj - mu0_j` and `T_j(r) = mean_u(r_uj) / (sd_u(r_uj, ddof=1)/sqrt(9))`. Enumerate all `2^9 = 512` patient sign patterns, applying the **same sign to every component for a patient**. Recompute both numerator and `ddof=1` denominator after every sign pattern and take `T_max = max_j T_j`. The exact p-value is `count(T_max_perm >= T_max_observed - 1e-12) / 512`; ties are included and there is no plus-one or Monte Carlo approximation.

Define the simultaneous one-sided 95% lower confidence region as all `mu0` not rejected by that shifted-null family test at `alpha=0.05`; each reported lower bound is the projection boundary of this region on its coordinate. The analyzer must locate every discrete acceptance boundary, then verify it from both sides to absolute tolerance `1e-10`; a generic optimizer result without the discrete check is invalid. Obtain upper bounds by applying the identical lower-bound procedure to the negated family `-d` and negating the result. Any observed or permuted denominator `< 1e-12`, nonfinite statistic, nonmonotone inversion, or boundary-verification failure makes the family INCONCLUSIVE. These exact rules and synthetic expected bounds are part of the still-missing analyzer blocker.

Stage 2's compute-licensing gate uses the same procedure on the already defined subfamily `{b_F, g_P}`. The final verdict is recomputed once with all three primary contrasts; the smaller interim family never becomes the final claim. The `{h_P, h_A}` sensitivities receive their own simultaneous max-T bounds and are labeled secondary.

Validity requires all of the following identifying assumptions:

- the nine patients are independent sampling units for the scoped patient-population claim;
- after averaging electrodes, sources, and seeds, each patient's paired contrast vector is jointly sign-exchangeable/centrally symmetric under the tested null shift;
- applying one sign across a patient's contrast family preserves the actual within-patient dependence;
- studentized subset pivotality is adequate for strong max-T familywise control;
- missingness, channel eligibility, fold validity, and arm failures are outcome-independent under the frozen rules.

Joint sign-exchangeability is not empirically establishable with nine patients. The analyzer reports sign/magnitude and leave-one-patient diagnostics, but no outcome-dependent “asymmetry threshold” is used. If the design reveals dependent patients, informative missingness, or another concrete violation; a patient is missing; any denominator is invalid; or the exact analyzer cannot invert the family, the result is INCONCLUSIVE rather than rerouted to electrode inference. Two-sided participant t intervals, Wilcoxon, and sign tests are descriptive robustness summaries only and cannot override max-T.

## Stage gates and terminal classifications

All manipulation/equivalence/solver/hash checks are hard validity gates. The classifications below are mutually exclusive and apply to the corrected unique-R2 target-specific claim.

### PASS

Classify target-specific transfer as PASS only if:

1. Stage 1A passes, or an unavailable exact lane has been prospectively replaced by an explicitly approved and labeled reimplementation;
2. every artifact, manipulation, phase-destruction, matched-target, movement, generic-quality, fold, and numerical-validity gate passes without replacement/resampling;
3. final simultaneous one-sided 95% max-T lower bounds are above zero for `b_F`, `g_P`, and `g_A`;
4. at least 8/9 patient values are positive for each primary contrast, every source and seed aggregate is positive, and every leave-one-patient/source/block point estimate is positive; and
5. the faithful Fisher-z direction is positive under the frozen aggregation.

This means a positive fresh fMRI gain exists and more than half of that paired gain remains beyond both controls. It is not a universal brain-specificity claim.

### EXCLUDED

After all validity gates applicable to the reached stage pass, classify the scoped primary claim as EXCLUDED if either:

- the simultaneous one-sided 95% upper bound for `b_F` is `<= 0`, excluding a positive fresh-brain fidelity gain; or
- the simultaneous upper bound for `g_P` or `g_A` is `<= 0`, excluding the proposition that more than half of the fresh gain remains beyond both controls.

If Stage 2 validly stops before `A` exists, apply these rules to the predeclared `{b_F, g_P}` subfamily: an upper bound `<= 0` for either contrast excludes the corresponding fresh-gain or phase-half-retention proposition and therefore prevents the full target-specific claim. If neither Stage 2 lower bound passes and neither upper bound excludes, classify the stopped study INCONCLUSIVE; `g_A` is missing by design and is never imputed.

An exact-lane value mismatch is separately `exact reproduction EXCLUDED/failed` only when all author artifacts are complete and hash-matched. Failure to obtain artifacts is `exact lane unavailable`, not EXCLUDED.

### INCONCLUSIVE

Classify INCONCLUSIVE in every other case: a confidence interval crosses zero; the sign/leave-out robustness conjunction fails without an exclusion bound; the exact lane is unavailable and no reimplementation was prospectively authorized; a manipulation, equivalence, movement, quality, solver, hash, missingness, exchangeability, or dimension benchmark fails; or Stage 3 has no valid predeclared candidate. Control invalidity never counts as evidence for brain specificity.

No post-hoc MDE, achieved power, observed-effect margin, alternative ROI, alternative layer, extra seed, new control, or endpoint-selected subset changes these rules.

## Compute and storage ceiling

- Stage 0 metadata validation: seconds, negligible retained storage, no endpoint payload.
- Stage 1: pretrained plus three supplied checkpoint evaluations, provisionally about 40 GPU-hours after implementation validation.
- Stage 2: `3 sources x 3 seeds x 2 arms = 18` fresh training/evaluation runs, provisionally about 720 GPU-hours.
- Stage 3: nine additional selected-audio runs, provisionally about 360 GPU-hours.
- Full gated ceiling: approximately 1,120 GPU-hours and 14 wall-clock days including calibration/probe overhead. Earlier gate failure releases the remainder.

These are planning ceilings, not authorization. The exact runner/analyzer and synthetic dimension benchmark must establish measured memory, wall time, and storage before any compute lock. Minimal ECoG acquisition is 4,992,680,616 bytes; exact LeBel storage remains unresolved until the source snapshot/story list is known.

## Stop rules and forbidden adaptations

No payload download, neural-value access, endpoint scoring, model training, or author communication is authorized **by this E record alone** while `READY-TO-RUN: NO`. Erfan may separately authorize outcome-blind factual-artifact acquisition or the prepared author request needed to resolve Stage 0; that does not authorize an endpoint payload or make the design READY.

Do not run a broad hyperparameter search, alternate ECoG dataset, best ROI/layer, extra seed, replacement teacher, relaxed equivalence margin, unbuffered split, electrode-level inference, or post-outcome nuisance change. A failed honest gate is a result. After unsealing, the only review actions are continue the exact frozen sequence, stop, invalidate, or narrow scope.

## Precheck

**Ranked verdict: HOLD / READY-TO-RUN: NO.** The first hostile review's corrections are now incorporated at the protocol level, but the revising agent cannot clear its own work. Blockers are ranked by proximity to safe endpoint access:

1. **P0 — executable boundary absent:** no exact Stage 1A/1B/2/3 runner, final analyzer, canonical configuration, dependency lock, unit/leakage fixtures, or ordered bundle SHA-256 exists.
2. **P0 — dimension evidence absent:** the exact evaluator and Stage 3 construction have not passed a synthetic benchmark at planned time-by-feature, time-by-electrode, and story-by-voxel dimensions with recorded peak RAM/VRAM, wall time, dtype, numerical error, and deterministic replay hashes.
3. **P0 — factual artifacts unresolved:** paper-specific code/checkpoints/result table, exact WavLM and Whisper files, ds003020 snapshot/story split, response offsets, exact endpoint mask/folds, and hash-manifested GloVe/TIMIT sensitivity artifacts remain unavailable. The exact-versus-reimplementation lane is not yet locked.
4. **P1 — final independent review absent:** after implementation and factual-slot closure, a fresh anti-confound/oracle review must inspect the exact hashes and return DESIGN PASS. Any new substantive correction requires rehash and another outcome-blind review.

Until all four clear, no E028 evidence-producing command is authorized and no READY claim is permitted.

## Results

`\gap`, not run. No E028 neural endpoint has been downloaded, opened, or scored by the metadata validation documented here.

## Related

- [Project status](../status.md)
- [Methodology and authority contract](../03-methodology.md)
- [D057 conference-package decision](../decisions/decisions.md)
- [Canonical Vaidya et al. note](../literature/canonical/vaidya-2026_slow-fmri-fast-ecog-transfer.md)
- [E028 author-artifact request](../references/e028-vaidya-artifact-request-email.md)
