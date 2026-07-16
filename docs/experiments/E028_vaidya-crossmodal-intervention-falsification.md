---
title: "Experiment - E028: Vaidya cross-modal intervention falsification"
tags: [experiment]
aliases: [E028]
---

# Experiment - E028: Vaidya cross-modal intervention falsification

**Created:** 2026-07-16 · **Status:** DESIGN DRAFT, exact-artifact access gate pending; no E028 endpoint has been opened or computed · **Mode:** prospective
**Direction:** Independent external application of Package A in [D057](../decisions/decisions.md). E027 remains reserved for Package C's internal matched-control branch, so this study uses E028.
**Primary external target:** [Vaidya et al., 2026](../literature/canonical/vaidya-2026_slow-fmri-fast-ecog-transfer.md), arXiv:2605.19224v1.

---

## Objective

Test whether the reported transfer from WavLM Base+ tuned on slow LeBel fMRI to fast Podcast ECoG survives four successively stronger requirements: exact reproduction, endpoint-participant inference, nested lag and readout selection with confound subtraction, and comparison against both a phase-randomized fMRI shape twin and one optimization-, geometry-, and learnability-matched nonbrain audio target.

This study is scientifically independent of [E016](E016_tribe-synthetic-brain-targets.md) and [E025](E025_participant-e016-biological-transfer.md). It uses a different architecture, speech rather than text, public LeBel fMRI as the intervention source, and public Podcast ECoG as the endpoint. E025 motivates the gate structure but contributes no target, checkpoint, feature, participant, or outcome to E028.

## Competing explanations

- **Target-specific cross-modal transfer:** stimulus-aligned fMRI supervision changes WavLM in a way that improves nuisance-subtracted ECoG prediction in unseen patients beyond equally budgeted shuffled and nonbrain auxiliary interventions.
- **Generic auxiliary-training effect:** a stimulus-derived nonbrain target with comparable geometry, learnability, optimization pressure, and representation movement yields the same ECoG gain.
- **Target-shape or regularization effect:** a phase-randomized fMRI target that preserves multivariate temporal and spatial structure yields the same gain.
- **Selection or inference artifact:** the reported electrode-level effect depends on treating nested electrodes as replications, selecting the best of 81 lags outside an outer training fold, or omitting contiguous buffers and low-level speech nuisance features.
- **Reproduction failure:** the published aggregate cannot be regenerated from the authors' own code, checkpoints, masks, and table, or cannot be faithfully reimplemented from public artifacts.

## Primary sources and fixed dataset identities

- Paper: [arXiv abstract](https://arxiv.org/abs/2605.19224), [HTML](https://arxiv.org/html/2605.19224), and [PDF](https://arxiv.org/pdf/2605.19224). The audited source is v1 submitted 2026-05-19.
- fMRI source: [OpenNeuro ds003020](https://openneuro.org/datasets/ds003020). The live public root reported `doi:10.18112/openneuro.ds003020.v3.1.1` during the metadata audit, but the exact snapshot used by Vaidya et al. is unresolved and must come from the authors before acquisition.
- ECoG endpoint: [OpenNeuro ds005574 v1.0.2](https://openneuro.org/datasets/ds005574/versions/1.0.2), DOI `10.18112/openneuro.ds005574.v1.0.2`, CC0.
- Official ECoG code: [hassonlab/podcast-ecog-paper](https://github.com/hassonlab/podcast-ecog-paper) and [hassonlab/podcast-ecog-tutorials](https://github.com/hassonlab/podcast-ecog-tutorials). These are dataset-owner resources, not the Vaidya implementation.
- Existing local speech brain-tuning scaffolds: `data/paper-repos/multi-brain-tuning` and `data/paper-repos/brain-tuning`. They contain useful LoRA, spatial-correlation, Lanczos, and encoding components, but use different model and training implementations and cannot establish exact reproduction.

The metadata-only audit found 159 objects and 14.44 GiB in the ds005574 public root. A minimal future acquisition comprises the nine supplied high-gamma FIF files, the podcast WAV and transcript, dataset metadata, and per-patient channel/electrode metadata. The nine high-gamma files total 4.354 GiB and the audio is 317,520,626 bytes, so the selected set is under 4.7 GiB before filesystem overhead. These are access-planning facts, not E028 endpoint measurements.

The local LeBel staging area currently has 84 fMRI story files for UTS03 and 21 each for UTS01 and UTS02, plus 84 WAV and TextGrid files. This does not match the paper's reported 94 to 103 stories per source participant. No existing local LeBel slice may be silently treated as the paper's training set.

## Stage 0: artifact and acquisition gate

### Author artifacts required before an exact reproduction

Use the unsent request template in [the E028 author artifact request](../references/e028-vaidya-artifact-request-email.md). Receive and hash all of the following before opening the electrode-by-participant values:

1. The paper-specific code commit, clean environment lock, launch commands, and any uncommitted patch.
2. The exact WavLM Base+ repository, revision, configuration, processor, weight files, and SHA-256 values, including LoRA target modules, rank, alpha, dropout, trainable-layer scope, and feature-layer indexing.
3. The exact ds003020 and ds005574 snapshots, source-participant mapping, voxel masks, train/validation/test story lists, audio preprocessing manifest, and response alignment offsets.
4. The three principal subject-specific LoRA checkpoints, selected epoch per checkpoint, every epoch-selection statistic, and any downsampled or data-scaling checkpoint needed to reproduce a paper panel.
5. The ECoG electrode inclusion and ROI table, preprocessing manifest, four-fold boundaries, ridge grid, lag grid, lag-selection scope, and any random state.
6. An electrode-by-ECoG-participant table with pretrained and each source-model score, chosen lag, ROI, fold-level score or out-of-fold prediction pointer, and the numeric values behind every load-bearing figure.
7. SHA-256 values and redistribution terms for every supplied artifact.

An exact lane exists only if these artifacts make the published analysis deterministic and auditable. If any load-bearing item is unavailable, label the work `independent reimplementation`; never call it an exact reproduction.

### Metadata-only manifest

Run only the following before design precheck:

```bash
cd /home/centcom/data/brain-alignment
uv run python scripts/e028_acquisition_manifest.py
```

The script may list remote objects, read small descriptive metadata, record official code heads, and stat local filenames and sizes. It must not download fMRI, ECoG, audio, weights, checkpoints, or result tables, and it must not open a neural value. The provisional output is `outputs/E028/acquisition_manifest.json`. Remote S3 ETags are recorded only as transfer hints and are never mislabeled SHA-256.

The metadata smoke completed without endpoint access on 2026-07-16. It selected 53 future acquisition objects totaling 4,992,680,616 bytes, verified nine participants and nine high-gamma files under ds005574 v1.0.2, and recorded dataset-owner code heads `e7ba666e09865b1918c2c7d547784f1eb6d626fe` and `2a984dfc935d5e95111ce573b8061f4a1d6e32ee`. Manifest SHA-256 is `c215b9fa69c23a659c32434c0626be77d808e305e707e6a063f52f3ccbfa2e62`; script SHA-256 is `fb6e1bfd69696a7af6f57635ca3cce2a1f4445bcb63c173254661e7bcb1f59e4`. This is acquisition metadata only and does not make the design ready.

### Hashes that must be filled after authorization and acquisition

The acquisition manifest and this E record must eventually contain SHA-256 values for:

- Every acquired high-gamma FIF, Podcast WAV/transcript, BIDS channel/electrode file, and dataset-description file.
- Every acquired LeBel fMRI response, audio file, TextGrid/TR file, voxel mask, and exact story-list manifest.
- The WavLM Base+ processor, configuration, and weight files.
- Paper-specific and dataset-owner source archives at frozen commits.
- Every author checkpoint, selected-epoch record, and disaggregated result table.
- The frozen E028 configuration, source manifest, raw outer-fold predictions, and final analysis artifact if the study runs.

Acquisition halts if a downloaded file differs from a supplied SHA-256, if only a mutable dataset root is known, if the paper's story counts cannot be reconstructed, or if the 1,268-electrode analysis mask cannot be mapped to the 1,330-electrode public dataset.

## Stage 1: faithful reproduction and corrected no-training reanalysis

Stage 1 is the cheapest decisive external test. It uses the frozen pretrained WavLM Base+ model and the three author-supplied principal fMRI-tuned checkpoints. It performs no new fMRI tuning.

### Stage 1A: faithful paper analysis

- Reproduce the authors' preprocessing, layer-9 feature extraction, four-fold split, 81 lags from -2 to +2 seconds, ridge grid, electrode mask, source-model aggregation, ROI aggregation, and Pearson-correlation endpoint without correction.
- A 4-second waveform window ending at each sample, 0.05-second feature stride, and 20 Hz high-gamma response are expected from the paper, but author code and metadata take precedence where the prose is incomplete.
- Regenerate all supplied electrode and aggregate values. With identical stored features and deterministic regression, the maximum absolute difference from a supplied full-precision table must be at most `1e-5`. If the authors can supply only rounded values, every regenerated value must fall inside its stated rounding interval.
- Reproduce the published all-cortex tuned-minus-pretrained direction before examining any new control. ROI results are secondary.

Failure of the exact lane is recorded as an exact-reproduction failure only when code, inputs, and masks are complete and hash-matched. A public-data reimplementation that misses the result has weaker scope and is labeled accordingly.

### Stage 1B: corrected analysis

- The biological endpoint units are the nine ECoG patients `sub-01` through `sub-09`. Electrodes, fMRI source models, technical folds, lags, and time samples are nested observations, not biological replications.
- Use four equal-duration contiguous outer time folds. Exclude a 6-second buffer on both sides of every outer and inner boundary, covering the 4-second WavLM context plus the maximum 2-second lag. Fit all standardization, nuisance transforms, ridge penalties, and selectors on training data only.
- Within each outer fold and electrode, select one common lag from the 81-lag grid using only pretrained WavLM and blocked inner cross-validation on that outer training set. Freeze that lag across pretrained, brain-tuned, and all later control arms. Select each arm's ridge penalty inside the same outer training set. This prevents an intervention from winning through a separate noisy best-lag search.
- Form out-of-fold predictions for every electrode, invert any training-fitted response standardization back to native high-gamma units, and concatenate the four held-out blocks before calculating one electrode score. Never average four fold-level `p`-values or use fold count as degrees of freedom.
- The faithful metric is Fisher-transformed Pearson correlation. The corrected primary metric is cross-validated unique R2, `R2(N + X) - R2(N)`, where `N` is a fixed low-level nuisance group and `X` is the arm's layer-9 WavLM representation. Fit the nuisance-only and full models with the same outer folds and nested banded-ridge selection.
- The primary nuisance group contains a 64-bin log-mel spectrogram, RMS envelope, pitch/voicing, word-onset and phoneme-onset impulses, local word and phoneme rate, and normalized podcast position. All features are derived without neural data and fit or standardized on the outer training side. A fixed static lexical embedding is an additional strong sensitivity because it may absorb genuine higher-level representation signal; it is not part of the primary nuisance group.
- All-cortex good electrodes under the authors' exact 1,268-electrode mask are primary. Destrieux auditory cortex and the Lipkin language-network selection are predeclared secondary ROIs. The public dataset's 1,330 raw electrodes are not substituted for the paper mask.
- Layer 9 is fixed. No layer search, patient exclusion, electrode threshold, ROI choice, nuisance choice, or lag protocol may be changed from ECoG outcomes.

### Stage 1 estimands

For endpoint patient `u`, fMRI source participant `q`, training seed `s`, electrode `e`, and arm `a`, let `M(u,q,s,e,a)` be the unique-R2 score from concatenated outer-fold predictions. Let `Z(u,q,s,e,a)` be Fisher `z` of the corresponding faithful Pearson correlation.

- First average electrodes equally within patient, then average the three fixed fMRI sources and technical seeds. The corrected patient score is `m(u,a) = mean_q mean_s mean_e M(u,q,s,e,a)`.
- The reproduction contrast is `d0(u) = m(u,brain) - m(u,pretrained)`. Stage 1 has one supplied checkpoint per fMRI source and therefore no seed dimension; source-model values remain visible.
- The primary population-facing estimand is `theta0 = mean_u d0(u)` over the nine endpoint patients. It is conditional on these three fMRI source participants and this one podcast. No arbitrary-source or arbitrary-stimulus population claim is licensed.
- Compute the same aggregation for the faithful Fisher-z endpoint. Pearson correlation answers whether the paper reproduces; nuisance unique R2 measures how much intervention-related improvement remains after low-level speech controls.

### Stage 1 inference and activation gate

- Report all nine patient values, all three fMRI-source values, patient median, two-sided participant t-CI95, exact two-sided sign-flip test over the `2^9` participant sign patterns, exact sign test, and Wilcoxon signed-rank where nonzero pairs permit it.
- Report leave-one-patient-out, leave-one-source-out, and leave-one-stimulus-block-out point estimates. Blocks and sources are robustness axes, not extra population degrees of freedom.
- A participant-supported positive requires the unique-R2 participant t-CI95 lower bound above zero, the exact sign-flip `p < 0.05`, at least 8/9 positive patients, all three source-model aggregates positive, and every leave-one-patient-out and leave-one-block-out point estimate positive. The faithful Pearson-z analysis must also remain positive.
- At the end of Stage 1, before any control target is built, freeze the practical specificity margin `delta_ref = 0.5 * theta0`. Compute exact noncentral-t 80% MDE at `n=9` from the observed participant SD. Control training is not authorized if `theta0 <= 0`, if the Stage 1 activation conjunction fails, or if the 80% MDE exceeds `delta_ref`.
- If the one-sided participant upper bound is below zero, classify the corrected gain as excluded for this endpoint. If the interval crosses zero and the power gate fails, classify it as power-limited rather than null.

Any Stage 1 failure stops E028 before training. Exact reproduction followed by failure under participant inference or nested confound-subtracted evaluation is a completed prospective Package A application, not a reason to search for a friendlier endpoint.

## Stage 2: phase-randomized fMRI shape twin

Stage 2 runs only if Stage 1 activates it and a fresh anti-confound and oracle design precheck returns `READY-TO-RUN: YES`.

### Fixed training matrix

- Train separate models for the three paper fMRI source participants and seeds `0, 1, 2`.
- Arms are `brain` and `phase`. Both start from the exact same WavLM Base+ weights and paired seed state.
- Match the paper's rank-4 LoRA on the exact Q/K/V modules, rank-100 output head, spatial-correlation loss, Adam optimizer, learning rate `5e-4`, 30 epochs, batch size 10 TRs, audio windows, story split, voxel mask, minibatch order, checkpoint frequency, and total examples.
- Select one checkpoint among epochs 1 to 30 using each arm's own target on the fixed two validation stories, with the paper's supplied validation encoder and no ECoG access. Brain validates on real fMRI and phase validates on its frozen phase target. The unseen LeBel test story remains untouched.

### Shape-twin construction

For each source participant, story, and target seed, apply a multivariate Fourier phase randomization to the complete voxel matrix. At each positive temporal frequency, multiply the full complex voxel vector by one seeded unit-modulus phase shared across voxels, enforce the conjugate phase at the negative frequency, and leave DC and Nyquist real. A separate deterministic phase sequence is used for each story.

This transform preserves every within-story voxel auto-spectrum and cross-spectrum, hence the complete second-order spatial and temporal structure, while breaking alignment to the audio. It does not preserve higher-order marginal distributions and is therefore called a second-order shape twin, not an information-matched target.

Before training, verify the algebra on synthetic matrices, require phase-modulus and full complex-coefficient amplitude errors at most `1e-12`, and require relative cross-spectrum error at most `1e-10` on 512 voxel pairs fixed by the design manifest. Because one common scalar phase multiplies the complete voxel vector at each frequency, these checks imply preservation of the full cross-spectrum without materializing an infeasible voxel-by-voxel matrix. Also require absolute standardized mean/SD differences at most `1e-8`. The fixed pretrained WavLM plus rank-100 head must predict the phase target with held-out R2 no greater than `max(0, 0.10 * R2_real)`. If geometry preservation or alignment destruction fails for any source/seed, stop as a failed manipulation without resampling.

### Stage 2 endpoint and decision

Use the frozen Stage 1B ECoG evaluator. Define `dP(u) = m(u,brain) - m(u,phase)`. Fresh brain runs, not the single author checkpoints, enter this paired contrast.

Report the same participant inference and robustness battery as Stage 1. Beating the shape twin requires a one-sided 95% participant lower bound above zero, a point estimate at least `delta_ref`, at least 8/9 positive patients, all three source aggregates and all three seed aggregates positive, and positive leave-one-patient/source/block estimates. This licenses Stage 3 but does not yet establish target specificity because learnability and movement are intentionally not matched by the phase target.

After one training pass, measure LoRA parameter-update norm, layer-9 linear-CKA distance from pretrained, and activation-RMS movement on a disjoint fixed LibriSpeech audio sample. The phase arm must itself move: relative parameter update must exceed `1e-6`, and CKA and RMS movement must each exceed `max(1e-6, 10 * duplicate-extraction noise)` in every source/seed. Report brain-versus-phase movement and fixed TIMIT phoneme and sentence-type linear-probe F1 descriptively. Movement and quality need not be equivalent here because destroyed stimulus alignment is the intended manipulation; only Stage 3 may support a movement- and quality-matched claim.

Stop after Stage 2 if the phase twin absorbs the practical gain, if the phase manipulation or movement gate fails, or if the shape-twin contrast is power-limited. Proceed to Stage 3 only when the full Stage 2 conjunction passes; do not reinterpret a failed shape twin through a nonbrain target.

## Stage 3: one optimization-, geometry-, and learnability-matched nonbrain target

Stage 3 runs only if Stage 2 passes. It trains exactly one frozen control family, not a sweep selected from ECoG.

### Frozen candidate family

- Use the exact `openai/whisper-medium` encoder revision and files frozen in the Stage 3 manifest. Candidate layers are `6, 12, 18, 24`, fixed projection seeds are `0, 1, 2`, and auxiliary-loss multipliers are `0.5, 0.75, 1.0, 1.5, 2.0`. No other layer, teacher, seed, or multiplier may be tried.
- Extract Whisper features from the same fMRI-story audio and align them to the same TR grid using training-fitted transforms only.
- For each source participant and candidate layer, standardize and whiten the training-story Whisper matrix. Fit one scalar frequency-domain filter from aggregate training-target trace power only, apply it within story boundaries to match fMRI temporal power without using item-wise fMRI values, then decompose the filtered teacher matrix. Keep its first 100 left-score directions, replace their singular values with the top-100 singular values of the centered fMRI training target, and rotate them into voxel space using a seeded Haar basis constrained to be orthogonal to the all-ones spatial vector.
- Extend the training-fitted Whisper transform to validation stories without using validation fMRI values. Candidate head learnability is measured by blocked cross-validation wholly inside the training stories, so the two paper validation stories remain untouched for checkpoint selection. The construction may use aggregate fMRI training-target spectrum and scale, but it may not copy item-wise fMRI coordinates, a brain-derived spatial basis, a learned brain readout, or any ECoG quantity.
- Select the lexicographically first candidate that passes every pretraining margin below, ordered by layer, projection seed, and multiplier. If no candidate passes, Stage 3 is killed as control non-identifiability. Do not widen the grid.

### Pretraining equivalence margins

| Diagnostic | Required margin for every source and paired seed |
|---|---|
| Ambient dimension, item identity/order, split, and rank-100 bottleneck | Exact equality |
| Standardized global mean and SD | Absolute mean difference `<= 0.01`; SD ratio in `[0.99, 1.01]` |
| Normalized top-100 target spectrum | RMS log-eigenvalue difference `<= 0.10`, excluding and counting eigenvalues below `1e-8` of the leader |
| Variance mass at components 1, 8, 32, 64, 100 | Absolute difference `<= 0.02` at every cut |
| Within-story trace autocorrelation and binned power | Difference `<= 0.05` at every fixed lag; Jensen-Shannon divergence `<= 0.05` |
| Pretrained WavLM plus rank-100 head target R2 and headroom under blocked cross-validation within training stories | Absolute R2 difference `<= 0.02`; headroom ratio in `[0.90, 1.10]` |
| Initial standardized auxiliary loss and LoRA gradient norm | Loss difference `<= 0.05`; absolute log gradient-norm ratio `<= 0.10` |

These margins establish comparability on measured engineering axes only. They do not make Whisper information biologically equivalent to fMRI.

### Stage 3 training and endpoint

Train one matched-audio model for every source and seed with the exact Stage 2 architecture, examples, optimizer, steps, batching, checkpoint selection rule, and compute. No ECoG result may be loaded until all checkpoints and one-shot movement diagnostics are frozen.

Define `dA(u) = m(u,brain) - m(u,matched_audio)`. Require absolute log parameter-update and RMS-movement ratios at most `0.10`, CKA-distance difference at most `0.002`, and absolute TIMIT phoneme and sentence-type F1 differences at most 1.0 percentage point between brain and matched-audio arms in every source-averaged seed. A mismatch kills interpretation and cannot trigger candidate replacement.

The target-specific conclusion requires both `dP` and `dA` to have simultaneous one-sided 95% participant lower bounds above zero under an exact max-T sign-flip procedure, both point estimates at least `delta_ref`, at least 8/9 patient signs positive for each contrast, all source and seed aggregates positive, and all leave-one-patient/source/block estimates positive. The simultaneous null distribution uses the same `2^9` participant sign flips for both contrasts and the maximum studentized statistic.

- If both controls are beaten, E028 supplies unusually strong positive evidence for source-target-specific fMRI supervision transferring to ECoG across fixed source participants, unseen patients, different content, and a different recording modality.
- If the faithful result reproduces but either control absorbs it, E028 supplies the prospective top-venue falsification Package A is designed to make.
- If a one-sided 95% upper bound for `dP` or `dA` falls below `delta_ref`, at least half of the reproduced practical gain is excluded as target-specific for this endpoint.
- If intervals overlap the margin while the MDE exceeds it, the result is power-limited. It is not converted into a null.

## Inference hierarchy and scope

- ECoG patient is the sole population inference unit for the main claim, `n=9`.
- Technical training seeds are crossed realizations and averaged before patient inference.
- The three fMRI source participants are a fixed source set. Report all values and leave-one-source-out sensitivity, but do not claim population generalization over fMRI donors from `n=3`.
- Electrodes are averaged within patient and never flattened across patients. Unequal electrode counts therefore do not reweight the biological population.
- The four outer time blocks assess stimulus robustness. They are dependent held-out segments of one podcast and do not create a story-population claim.
- Exact tests, t intervals, medians, and leave-one-out summaries are reported together. A small electrode-level `p`-value cannot override patient-level failure.

## Five-control battery

1. **Phase-randomized shape twin:** Stage 2, preserving complete within-story second-order target structure.
2. **Shuffled privileged information:** Stage 2 breaks stimulus-to-fMRI alignment. A zero target is invalid under spatial-correlation loss and is not fabricated.
3. **Representation-movement gate:** mandatory one-shot parameter, CKA, and RMS checks before ECoG results are opened.
4. **Matched generic quality, participant inference, and crossed robustness:** Stage 3 fixed speech-probe parity, nine endpoint patients, three sources, three technical seeds, and four contiguous stimulus blocks.
5. **Optimization/geometry-matched nonbrain teacher:** one frozen Whisper-derived target in Stage 3, explicitly not matched-information.

## Compute and storage budget

- Stage 0 metadata check: seconds, negligible storage, no endpoint bytes.
- Stage 1: pretrained plus three supplied tuned checkpoint evaluations. The paper reports about 10 A6000 GPU-hours per model, so budget approximately 40 GPU-hours and 10 to 20 wall-clock hours on four L40S GPUs after implementation validation.
- Stage 2: 3 sources x 3 seeds x 2 trained arms gives 18 training runs. At the paper's reported 30 GPU-hours per fMRI model plus 10 GPU-hours per ECoG evaluation, budget approximately 720 additional GPU-hours after reusing Stage 1's pretrained evaluation, or 7.5 ideal four-GPU days before overhead.
- Stage 3: 9 additional trained/evaluated models add approximately 360 GPU-hours, or 3.75 ideal four-GPU days.
- Full gated program: approximately 1,120 GPU-hours and 11.7 ideal four-GPU days, including Stage 1's three author-checkpoint evaluations and all fresh paired training runs. Cap authorization at 14 wall-clock days, including calibration and speech-probe overhead. A failed earlier gate ends the program and releases the remaining budget.
- Minimal ECoG acquisition is under 4.7 GiB. Completing the exact LeBel three-source slice may require substantially more than the 36 GiB already staged. The exact amount remains unresolved until the authors identify their ds003020 snapshot and story list.

## Stop rules and access boundary

Do not download data, inspect endpoint values, train, or mark this design ready until:

1. The exact-artifact request has either succeeded or the reimplementation lane has been explicitly accepted.
2. A metadata manifest freezes all available object identities, commits, expected hashes, dataset snapshots, source mappings, and acquisition paths.
3. An anti-confound designer and independent oracle reviewer have returned a final design verdict.
4. The frozen runner passes synthetic tests for fold buffering, nested lag selection, patient aggregation, phase-spectrum preservation, target-construction leakage, and hash rejection.
5. The E record says `READY-TO-RUN: YES` and cites the frozen design and runner hashes.

No broad hyperparameter search, alternative ECoG dataset, best ROI, best layer, extra seed, or replacement nonbrain teacher is licensed by a failed result. A failure at any honest gate is the result.

## Precheck

Pending. No evidence-producing E028 command is authorized.

## Results

`\gap`, not run. No E028 neural endpoint has been downloaded, opened, or scored.

## Related

- [Project status](../status.md)
- [Methodology and authority contract](../03-methodology.md)
- [D057 conference-package decision](../decisions/decisions.md)
- [Canonical Vaidya et al. note](../literature/canonical/vaidya-2026_slow-fmri-fast-ecog-transfer.md)
- [E028 author artifact request](../references/e028-vaidya-artifact-request-email.md)
