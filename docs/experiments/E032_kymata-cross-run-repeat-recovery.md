---
title: "Experiment E032 - Kymata cross-run repeat recovery"
tags: [experiment]
aliases: [E032, kymata-cross-run-repeat-recovery]
---

# Experiment - E032: Kymata cross-run repeat recovery

**Created:** 2026-07-29 · **Status:** PROPOSED - metadata verified, acquisition integrity unresolved, endpoint sealed · **Mode:** planned

**Hypothesis:** [`H002`](../hypotheses/H002_repeat-stable-biological-supervision.md)

---

## Objective and claim boundary

Test whether one builder-only, repeat-optimized common spatial filter recovers more cross-recording-block repeat-stable signal than a same-dimensional PCA baseline from the Kymata Soto simultaneous MEG and EEG recordings.

A pass supports only this fixed-subject, fixed-story engineering claim:

> For Kymata English participant E2 and the repeated ice-cream conversation, regularized CorrCA recovers a cross-run scalar MEG component that is stable beyond the locked low-level acoustic, visual, linguistic-timing, physiological, and drift model, and more stable than the same-capacity PCA and content-destroyed controls.

It does not establish language specificity, semantic information, multimodal replication, participant-population generalization, an effective biological loss, a useful attachment layer, or a student-training benefit.

`READY-TO-RUN: NO`

No participant neural FIF bytes have been downloaded or opened. The first authorized endpoint transaction is frozen-file acquisition followed by integrity checking, not a denoising score.

## Why this follows E031

[`E031`](E031_biological-target-information-recovery.md) ended with `NO CONSENSUS INCREMENT` for its fixed five-participant Tuckute target and `BUILDER INSTRUMENT FLOOR` for its LeBel whole-cortex repeat assay. The LeBel result does not show that repeat denoising fails generally. Its full-cortex median can dilute a spatially localized response, and every fitted arm selected the largest ridge penalty.

E032 changes both the measurement substrate and the estimator. Kymata supplies repeated, time-resolved, simultaneous MEG and EEG views. CorrCA uses repeat agreement to learn one spatial projection shared by every exposure, while PCA maximizes variance of the builder-exposure mean without CorrCA's within-variance normalization. The held-out test is across different recording blocks so that head position, slow drift, and block-local artifacts cannot create the primary repeat score.

## Fixed sources

### Dataset and participant

- Dataset: [Kymata Soto](https://doi.org/10.1038/s41597-026-06579-8), public [OSF node `qdzgh`](https://osf.io/qdzgh/).
- Subset: `english-native-english-conversation`.
- Participant: `sub-E2`.
- Selection rule: the lowest-numbered English participant whose public metadata exposes four task FIFs and exactly two code-3 presentation events in every run.
- E1 is ineligible because the live archive exposes only runs 1 and 2. E2 is the first metadata-complete candidate. If E2 fails the raw acquisition-integrity gate, E032 stops with `ACQUISITION/PREPROCESSING FLOOR`; it does not silently select another participant.
- Primary modality: 204 planar MEG gradiometers after Maxwell filtering of all 306 MEG channels.
- Secondary modality: the 64 recorded EEG channels after common-average rereferencing. EEG is always reported if the acquisition gate passes, but it cannot rescue a failed MEG primary endpoint. Simultaneous EEG and MEG are not independent replication.

### Live-release facts and contradictions

The E2 sidecars report 1,000 Hz sampling, 102 magnetometers, 204 planar gradiometers, 64 EEG channels, 2 EOG channels, 1 ECG channel, 17 trigger channels, five HPI frequencies, continuous head localization, and no premarked bad channels.

The primary descriptor says English used VectorView and 70 EEG electrodes. The same paper's data-record section and the live English archive instead provide Triux calibration and crosstalk files, while every examined English sidecar reports 64 EEG channels. E032 uses the 64 recorded EEG channels and chooses no MEG-machine calibration from prose. Raw coil information, sensor names, and the supplied calibration files must agree before Maxwell filtering.

The paper and OSF page state CC BY 4.0, while `dataset_description.json` states CC0. E032 conservatively treats the dataset as CC BY 4.0. The embedded BBC audio is used locally for analysis and is not redistributed.

### Frozen large-file identities

| Role | Bytes | SHA-256 | Source |
|---|---:|---|---|
| Builder run 1 FIF | `1,552,184,639` | `b3903a2161c61836fce95b0ce4fd3b14ad2e9e3d7ab493dca013fc5ff50c4c44` | [OSF](https://osf.io/download/ynrfv/) |
| Evaluation run 2 FIF | `1,450,292,707` | `7e858fe76be29ecd8dfbe55d2bcf9f6c893c77cd7688c1e8f8a8300b028f35bb` | [OSF](https://osf.io/download/67bd71496eb4b49d239fb1ff/) |
| Builder run 3 FIF | `1,447,108,623` | `070dce614597024275ce51a2d8c0ed28f86cb631167069416fc0adda600c2c93` | [OSF](https://osf.io/download/srbk8/) |
| Evaluation run 4 FIF | `1,445,516,595` | `bdf65d34e9e61b7f29d96e0905f23b61eae2e0015a5257ddf6d102d6eb5c6afe` | [OSF](https://osf.io/download/8me6j/) |
| English fine-calibration file | `39,770` | `1c97bf7076ebda4a9d8dc996b67ce1fe74358a194aa52e2195b0dc631a45eb86` | [OSF](https://osf.io/download/anefc/) |
| English crosstalk file | `26,124` | `293f18b7428a25ade8de2db74a2310bc33b64716a0bac3970ee58ea925b6e7b5` | [OSF](https://osf.io/download/9ujc2/) |
| Stimulus WAV | `154,197,892` | `996e9930e24930bb40602651616412b436964d59d6dc765dbb6c3996ef813972` | [OSF](https://osf.io/download/y9en6/) |
| Visual frame archive | `2,713,442,247` | `93b17643b80fed3dd0a14c5152baa7cc83e927aa9b4c430be7003707abbdcb19` | [OSF](https://osf.io/download/3gh2j/) |

The OSF node is mutable rather than registered. Every acquired file must match both the frozen byte count and SHA-256 before use.

## Acquisition-integrity gate

The public event tables cannot yet define valid neural crops. Their code-3 onsets are:

| Run | Code-3 onsets, seconds | Sidecar `RecordingDuration`, seconds | Second onset plus exact WAV duration |
|---|---|---:|---:|
| 1 | `205.905`, `645.838` | `970.999` | `1047.366` |
| 2 | `66.744`, `512.764` | `906.999` | `914.292` |
| 3 | `73.716`, `513.250` | `904.999` | `914.778` |
| 4 | `74.827`, `521.180` | `903.999` | `922.708` |

The exact WAV duration is `401.5281667` seconds. Every nominal second presentation extends beyond the declared recording duration. A likely explanation is that the event onsets retain the FIF `first_samp / sfreq` offset, but that is an inference and cannot be treated as a repair.

The first authorized work stage must therefore:

1. verify each byte count and SHA-256;
2. open the four FIF headers with `preload=False`;
3. require 1,000 Hz, the frozen channel inventory, `STI101`, HPI information, and enough samples for two complete WAV-duration windows;
4. extract code-3 events from raw `STI101`;
5. compare raw and TSV events under exactly two prospective conventions: raw-relative time and raw-relative time plus `first_samp / sfreq`;
6. accept a convention only if one constant run-level offset aligns every code-3 event within one sample and both complete windows fit inside the raw data;
7. record the selected convention and normalized event table as an acquisition artifact; and
8. stop with `ACQUISITION/PREPROCESSING FLOOR` if no convention passes.

The same stage must verify that the supplied Triux-named calibration and crosstalk files match the raw sensor names and coil information and are accepted by MNE's Maxwell implementation. The prose machine label cannot override the raw header. No fallback calibration or manual repair is allowed after failure.

## Outcome seal and authorized order

Runs 1 and 3 are builder runs. Runs 2 and 4 are evaluation runs.

The executable must enforce:

1. `selftest`: synthetic data only;
2. `manifest`: local and remote metadata only;
3. `acquire`: require explicit E032 authorization, stream only the frozen files to their exact local paths, verify byte counts and SHA-256 values before atomic promotion, and never deserialize participant data;
4. `integrity`: file hashes, raw headers, calibration compatibility, and `STI101` only;
5. `builder`: open neural channels from runs 1 and 3 only;
6. `score`: open neural channels from runs 2 and 4 only after the builder gate passes and a builder seal hash is supplied;
7. `analyze`: aggregate frozen artifacts without reopening raw FIFs.

The `score` stage must fail closed unless its config hash, executable hash, acquisition artifact hash, builder artifact hashes, and builder-seal hash match the predeclared chain.

## Preprocessing

### MEG

Each run is processed independently. Maxwell filtering uses all 306 MEG channels, the raw-verified calibration and crosstalk files, and the head destination defined by builder run 1. Only after Maxwell filtering are the 204 planar gradiometers selected.

Each presentation is cropped independently using the normalized raw trigger. The exact `401.5281667`-second exposure is filtered with a zero-phase `0.5-20 Hz` FIR filter, resampled to 100 Hz, and trimmed by 10 seconds at both ends. Exposures are never concatenated before filtering, artifact processing, nuisance fitting, or spatial-filter fitting. A separate 50 Hz notch is redundant below the 20 Hz low-pass and is forbidden.

### EEG

The 64 recorded EEG channels are rereferenced to their common average after applying the same frozen bad-channel rule. They use the same per-exposure `0.5-20 Hz`, 100 Hz, and 10-second edge-trim path. The analysis does not invent the six electrodes implied by the paper's 70-electrode prose.

### Artifact and scale rules

No evaluation-run trace may be inspected manually. Channel inclusion begins from the BIDS status fields and the raw-integrity inventory.

Artifact thresholds are estimated from builder data only in fixed one-second windows. A window is unusable if its EOG, ECG, or sensor peak-to-peak value exceeds the builder median by 10 builder median absolute deviations. The same numeric thresholds are applied unchanged to evaluation. Pairwise scores use the intersection of valid time samples.

The builder gate requires at least 80% usable samples in every exposure and no builder-run usable-data difference above 10 percentage points. The evaluation stage requires the same 80% floor in every exposure. A failed usable-data gate produces `ACQUISITION/PREPROCESSING FLOOR`, not a denoising verdict.

Scale is diagnosed from per-channel median absolute deviations after builder-fitted nuisance residualization. For every held-out builder or evaluation exposure, the median channel scale ratio relative to the applicable builder reference must lie in `[0.5, 2.0]`, and no more than 5% of channels may fall outside `[0.25, 4.0]`. These fixed plausibility limits detect unit, preprocessing, or gross run-instability failures. They are not tuned on evaluation, and failure produces `ACQUISITION/PREPROCESSING FLOOR`.

EOG and ECG regression coefficients are fit on the applicable builder-training exposures only and applied frozen to their held-out builder exposures or to evaluation. Centering, scaling, nuisance coefficients, covariance regularization, PCA, CorrCA, sign, and scale follow the same builder-only rule.

## Frozen nuisance model

The nuisance model is deliberately stronger than a luminance or speech-envelope control because the same dynamic dot movie and the same conversation repeat on every exposure.

Stimulus-only features are:

- 32-band log-mel audio power;
- broadband envelope and first derivative;
- pitch and voicing;
- exact word-onset and phoneme-onset impulse trains;
- global visual luminance, contrast, and frame-change energy;
- the first 16 stimulus-only image PCs from grayscale frames downsampled to `32 x 24`;
- the first 16 stimulus-only motion PCs from consecutive-frame differences in the same space;
- exposure intercept and linear drift; and
- the recorded EOG and ECG channels.

Audio, visual, word-onset, and phoneme-onset features use eight fixed causal raised-cosine temporal basis functions spanning 0 to 800 ms. Image and motion PC bases are fit to the external stimulus alone and never use neural values.

The nuisance ridge grid is `0.01, 0.1, 1, 10, 100, 1000`. Strength is selected inside each builder-training set using approximately 38-second contiguous validation blocks with a 5-second guard on both sides. The same selected strength and coefficients are frozen for the associated held-out builder exposures or the final evaluation runs.

This model can support "beyond the locked low-level nuisance model." It cannot support "language-specific" because onset features do not exhaust lexical, syntactic, discourse, or semantic information.

## CorrCA estimator

For residualized builder exposure \(i\), let \(X_i \in \mathbb{R}^{T \times D}\) be time by sensor. Let

\[
R_W = \sum_i X_i^\top X_i
\]

and

\[
R_B = \sum_{i \neq j} X_i^\top X_j.
\]

CorrCA solves

\[
R_B w = \lambda \widetilde{R}_W w,
\]

with

\[
\widetilde{R}_W
=
(1-\gamma)R_W
+
\gamma \frac{\operatorname{tr}(R_W)}{D} I.
\]

For \(N\) builder exposures, the regularized training-reliability diagnostic is \(\rho_\gamma=\lambda/(N-1)\). This diagnostic is never substituted for the held-out Pearson correlations in \(Q\). The first generalized eigenvector is the only primary component. It uses one common sensor projection for every exposure and therefore transfers unchanged to sealed runs. This is the repeat-reliability form of CorrCA and is equivalent to a regularized repeat-evoked DSS or joint-decorrelation objective under the same between-repeat and within-repeat covariance definition.

The shrinkage grid is `0, 0.01, 0.05, 0.10, 0.20, 0.40, 0.60, 0.80, 0.95`. Within each builder fold, \(\gamma\) is chosen using only its two training exposures and nested contiguous time blocks; ties within `1e-6` choose the larger \(\gamma\). The final \(\gamma\) is chosen by the mean of the two sealed builder-fold scores, with the same stronger-shrinkage tie rule, and CorrCA is then refit on all four builder exposures.

Normalize every fitted filter so that

\[
w^\top \widetilde{R}_W w = 1.
\]

Fix its sign by making the largest-absolute builder sensor coefficient positive. No evaluation-dependent orientation or rescaling is allowed.

Ordinary unconstrained MCCA is excluded because it learns a separate projection for each exposure and has no unique transform for an unseen exposure. Similarity-constrained MCCA is not excluded on that ground because its shared-\(W\) form belongs to the same estimator family as CorrCA. PCA is retained as the same-dimensional baseline because it learns one transferable direction from the variance of the builder-exposure mean without optimizing the between-repeat/within-repeat reliability ratio. Nonlinear and multi-component estimators are not opened by E032.

An independently coded DSS audit uses the same selected \(\widetilde R_W\) for whitening and the regularized repeat-average bias \(\widetilde R_W+R_B\). This makes the DSS eigenproblem an affine transform of the CorrCA eigenproblem even when \(\gamma>0\). On every synthetic fixture and builder fit, its first one-dimensional subspace must match CorrCA within a principal-angle tolerance of `1e-6` radians, and the two filters' \(\rho_\gamma\) scores, recomputed with the CorrCA covariance ratio, must match within `1e-8`. Failure is an implementation blocker, not a winner-selectable result.

## Cross-run split

Every task run contains two presentations, called exposure 1 and exposure 2.

The two builder folds are:

- Fold A: fit every learned quantity on run 1 exposure 1 plus run 3 exposure 1; score run 1 exposure 2 against run 3 exposure 2.
- Fold B: fit every learned quantity on run 1 exposure 2 plus run 3 exposure 2; score run 1 exposure 1 against run 3 exposure 1.

Within-run repeat correlations are diagnostics only and cannot enter a gate, hyperparameter choice, classification, or claim.

After the builder gate passes, fit the final nuisance model, shrinkage choice, CorrCA filter, PCA filter, artifact rules, centering, and scaling on all four builder exposures. The evaluation score uses only the four cross-run pairs formed by the two run 2 exposures and the two run 4 exposures.

## Baselines and content-destroyed controls

### PCA

PCA uses the first principal component of the residualized, time-aligned builder-exposure mean, receives the same one-component capacity, normalization, sign rule, artifact mask, and evaluation pairs, and is never refit on evaluation.

### Shifted-filter twins

For each \(a\) in

\[
A = \{41,53,67,79,89,101,113,137\}\ \text{seconds},
\]

the four builder exposures are circularly rotated by \([0,a,2a,3a]\) after filtering and trimming. CorrCA is fit with the identical code to each destroyed-alignment builder set and then applied unchanged to unshifted held-out data. The most competitive shifted-filter score is the control.

### Shifted-template twins

For each \(a \in A\), the run 4 component is circularly rotated relative to run 2 before the cross-run score is computed. The most competitive shifted-template score is the control. This preserves the component covariance and autocorrelation while destroying exact content alignment.

## Estimands

For method \(m\), run \(r\), and exposure \(e\), define

\[
s^m_{r,e}(t)
=
Y^{\mathrm{res}}_{r,e}(t)w_m.
\]

The primary held-out score is

\[
Q_m
=
\frac{1}{4}
\sum_{e=1}^{2}
\sum_{e'=1}^{2}
\operatorname{atanh}
\left[
\operatorname{corr}
\left(
s^m_{2,e},
s^m_{4,e'}
\right)
\right].
\]

The method and specificity contrasts are

\[
\Delta_{\mathrm{PCA}}
=
Q_{\mathrm{CorrCA}} - Q_{\mathrm{PCA}},
\]

\[
\Delta_{\mathrm{filter}}
=
Q_{\mathrm{CorrCA}}
-
\max_{a \in A} Q_{\mathrm{shifted-filter},a},
\]

and

\[
\Delta_{\mathrm{template}}
=
Q_{\mathrm{CorrCA}}
-
\max_{a \in A} Q_{\mathrm{shifted-template},a}.
\]

These estimate fixed-E2, fixed-story cross-recording-block temporal stability after the locked nuisance model. They do not estimate a participant-population effect or semantic content.

## Builder gate

Evaluation runs remain sealed unless all conditions hold:

1. both cross-exposure builder folds have aligned CorrCA correlation above zero;
2. mean builder \(Q_{\mathrm{CorrCA}} \ge \operatorname{atanh}(0.10)\);
3. mean \(\Delta_{\mathrm{PCA}}\), \(\Delta_{\mathrm{filter}}\), and \(\Delta_{\mathrm{template}}\) are each at least `0.05` Fisher-\(z\);
4. no builder fold has a negative value for any of the three contrasts; and
5. every builder exposure passes the usable-data and run-imbalance rules.

Failure produces `BUILDER FLOOR` or `ACQUISITION/PREPROCESSING FLOOR`, as applicable. Runs 2 and 4 remain unopened at the neural-channel level.

The `r = 0.10` floor is an allocation threshold, not an estimate from E032. Under independent classical measurement error, averaging four repetitions with reliability `0.10` yields reliability approximately `0.308`. Raising per-repeat reliability from `0.10` to approximately `0.15`, near a `0.05` Fisher-\(z\) increment, raises four-repeat reliability to approximately `0.414`.

## Evaluation gate and terminal classifications

`REPEAT-STABLE MEASUREMENT RECOVERY` requires:

1. \(Q_{\mathrm{CorrCA}} \ge \operatorname{atanh}(0.10)\);
2. every evaluation exposure has positive average correlation with the two exposures in the other evaluation run;
3. \(\Delta_{\mathrm{PCA}}\), \(\Delta_{\mathrm{filter}}\), and \(\Delta_{\mathrm{template}}\) are each at least `0.05` Fisher-\(z\);
4. the paired 95% moving-block-bootstrap lower endpoint exceeds zero for \(Q_{\mathrm{CorrCA}}\) and all three contrasts under every bootstrap seed; and
5. all four evaluation exposures pass the usable-data and scale diagnostics.

Other exact outcomes are:

- `STABLE SIGNAL, NO REPEAT-OPTIMIZER INCREMENT`: the CorrCA aligned-signal and shifted-control conditions pass, but the PCA increment fails.
- `NO HELD-OUT REPEAT SIGNAL`: the evaluation aligned-signal or shifted-control condition fails.
- `BUILDER FLOOR`: the builder gate fails before evaluation.
- `ACQUISITION/PREPROCESSING FLOOR`: raw timing, calibration, channel, usable-data, or scale integrity fails.

Only `REPEAT-STABLE MEASUREMENT RECOVERY` licenses a later content-specific target assay. No E032 classification licenses loss construction, layer selection, a gradient assay, or student training.

## Uncertainty and inference unit

Use 20-second contiguous moving blocks and 10,000 paired resamples for each of bootstrap seeds `3201`, `3202`, and `3203`. Resample aligned time blocks synchronously across methods, controls, runs, and exposures. Report each interval and use the most conservative lower endpoint for the gate.

These intervals describe within-story temporal stability. The scientific inference unit is the participant-story pair, and E032 has \(n=1\). Runs, exposures, and temporal blocks are repeated measurements, not independent participants. Adaptation and session order remain entangled with the fixed acquisition order; exposure-level scores must be reported and no adaptation-invariance claim is allowed.

## EEG secondary arm

The EEG arm repeats the exact builder/evaluation split, nuisance model, CorrCA/PCA capacity, shifted controls, normalization, bootstrap, and reporting with 64 common-average-referenced channels.

EEG receives a separate exact classification using the same numerical rules, labelled secondary. It cannot change the MEG primary classification. Agreement between simultaneous MEG and EEG remains correlated evidence because both modalities share participant, stimulus, time, behavior, and many artifacts.

Cross-modal fusion is forbidden in E032. It becomes eligible only after both modalities independently clear their within-modality gates under their frozen projections.

## Consequences for a future biological loss

An E032 pass would identify one repeat-stable measurement direction, not a training target. The next experiment must first test whether the frozen component retains lexical, contextual, or semantic information beyond stronger text and stimulus controls on untouched participants or stories.

If that later content assay passes, repeated views can define a target posterior with mean \(\mu_s\) and uncertainty \(\Sigma_s\). The candidate loss remains the precision-weighted form recorded in [`H002`](../hypotheses/H002_repeat-stable-biological-supervision.md):

\[
\mathcal{L}_{\mathrm{bio},\ell}
=
\frac{1}{2}
\left(P_\ell h_\ell(s)-\mu_s\right)^\top
\left(\Sigma_s+\tau I\right)^{-1}
\left(P_\ell h_\ell(s)-\mu_s\right)
+
\frac{1}{2}
\log\left|\Sigma_s+\tau I\right|.
\]

The projection must be separately fit and frozen before student training so it cannot absorb the objective. The first licensed layer test, if the target and gradient gates are later passed, remains one upper-middle layer, one late hidden layer, and one builder-fit convex multi-layer mixture. The final-hidden-state option means a projection from that state, not a loss on language logits. Applying the same loss independently at every layer is forbidden because it multiplies correlated tests and can overconstrain representations without identifying which layer carries the useful gradient.

## Planned executable surface

- `configs/e032_kymata_cross_run_repeat_recovery.json`
- `scripts/e032_kymata_repeat_recovery.py`
- `data/kymata_soto/` for selectively acquired, gitignored raw files
- `outputs/E032/` for gitignored acquisition, builder, seal, score, and analysis artifacts

The implementation must provide synthetic fixtures for:

- raw/TSV event-offset reconciliation;
- complete-window and channel-inventory failure;
- calibration mismatch failure;
- cross-run-only fold construction;
- nuisance fit locality;
- CorrCA generalized eigenvectors and normalization;
- nested shrinkage locality;
- PCA capacity equality;
- shifted-filter and shifted-template controls;
- builder-seal enforcement;
- evaluation-run access denial before the builder pass; and
- paired moving-block-bootstrap aggregation.

## Precheck

### Dataset verifier

The metadata review accepted E2 as the lowest metadata-complete English candidate and rejected treating it as endpoint-ready. It identified the event-duration contradiction, the English machine/calibration contradiction, the 64-versus-70 EEG mismatch, the CC BY-versus-CC0 mismatch, and the mutable OSF node. Its verdict requires the raw-header and `STI101` acquisition gate above.

### Anti-confound designer

The first design review returned `REVISE_BEFORE_PRECHECK`. It rejected within-run repeat correlations as a gate because both presentations in a recording block share head position, drift, environmental noise, and preprocessing state. The present design adopts its required cross-run, cross-exposure builder folds, run-2-versus-run-4 evaluation score, common-filter CorrCA estimator, stronger visual nuisance model, MEG-primary/EEG-secondary scope, fixed sign and scale, artifact rules, thresholds, bootstrap, and prohibited claims.

### Method adjudication

The method review recommends shrinkage-regularized, one-component CorrCA with confidence `0.88`. It identifies the common transferable projection as the load-bearing property, fixes \(q=1\), rejects ordinary MCCA because its exposure-specific projections do not define one unique filter for an unseen exposure, retains PCA-1 as the matched baseline, and requires a DSS-equivalence implementation audit. Koskinen and Seppä's SimCCA does use one shared \(W\) and belongs to the same shared-filter generalized-eigenvalue family. CorrCA remains primary because its covariance ratio, shrinkage path, component ordering, and held-out controls are more directly specified and audited under E032's much smaller repeat budget. The review also confirms that a pass can license only a later content-specific target assay and then a pre-training aligned-versus-twin gradient-placement gate.

### Acquisition-precheck implementation

The first exact executable slice is intentionally limited to the smallest transaction that can change the dataset decision. Config SHA-256 `4465031dfe74e68f61e111dbd81329b8391e06a0d74df2bb49c3a6fdc0058109` and executable SHA-256 `b39d928941dfadc3159c4f151ce43bd6afd2e1e446d2f969e31c7c88de66f8ef` compile and pass 14 synthetic tests covering frozen-file identity, event-offset reconciliation, incomplete-window rejection, channel-inventory rejection, calibration-name mismatch, MEG-only crosstalk selection, structured integrity-failure classification, regularized CorrCA/DSS equivalence, shifted controls, PCA capacity, scale pass/fail, moving-block-bootstrap determinism, authorization, and endpoint-stage denial. The metadata-only manifest has SHA-256 `623bc634ad3f1f14161253b4199cd204f9521c8ad2dbb521fdf24206ddb5cbf9` and records `endpoint_values_accessed=false` and `participant_raw_opened=false`.

Only `selftest`, `manifest`, streamed hash-verified `acquire`, and header/trigger/calibration-only `integrity` are implemented. With the frozen authorization flags false, both `acquire` and `integrity` stop before file access. `builder`, `score`, and `analyze` deliberately return `NOT_IMPLEMENTED` before neural-channel access. The remaining nuisance-locality, fold, seal, evaluation-access, and paired-bootstrap endpoint fixtures listed above are therefore requirements for a later implementation, not passed tests. This slice can at most become ready for an explicitly authorized acquisition-integrity transaction. E032 remains `READY-TO-RUN: NO`, and no endpoint score is executable.

### Oracle reviewer

The independent acquisition-precheck oracle returned `PANEL-CLEAN` on config SHA-256 `4465031dfe74e68f61e111dbd81329b8391e06a0d74df2bb49c3a6fdc0058109`, executable SHA-256 `b39d928941dfadc3159c4f151ce43bd6afd2e1e446d2f969e31c7c88de66f8ef`, and manifest SHA-256 `623bc634ad3f1f14161253b4199cd204f9521c8ad2dbb521fdf24206ddb5cbf9`. It independently reran compilation, all 14 selftests, the metadata manifest, both authorization-locked stages, and all three not-implemented endpoint stages. It also injected an authorized integrity failure and verified an atomic artifact with `status=FAILED`, classification `ACQUISITION/PREPROCESSING FLOOR`, exact error and hash provenance, and false endpoint/neural-access flags. The earlier crosstalk-channel and unclassified-failure defects were repaired before this final verdict.

This verdict accepts only a future explicitly authorized `acquire` plus `integrity` transaction. It does not approve builder fitting, endpoint scoring, analysis, loss construction, layer selection, or a scientific result. E032 remains `READY-TO-RUN: NO`.

## Results

No participant neural endpoint has been opened.

## Related

- [`H002`](../hypotheses/H002_repeat-stable-biological-supervision.md) - governing repeat-stable supervision hypothesis
- [`E031`](E031_biological-target-information-recovery.md) - local fMRI information-recovery gate
- [Dataset registry](../05-dataset-registry.md) - external dataset ownership
- [Methodology](../03-methodology.md) - evidence and authority contract
