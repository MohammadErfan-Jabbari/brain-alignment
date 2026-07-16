---
title: "Experiment E029 - prospective directional transfer certificate"
tags: [experiment]
aliases: [E029, directional-certificate]
---

# Experiment E029 - prospective directional transfer certificate

**Created:** 2026-07-17

**Status:** DESIGN DRAFT, NOT PRECHECKED, NOT READY TO RUN

**Direction:** Package B feasibility only

**Mode:** prospective only after design lock

> [!CAUTION]
> This record proposes a falsification experiment. No biological endpoint may be opened, no candidate may be selected, and no training run may begin until the substrate, manifests, thresholds, compute budget, anti-confound review, oracle review, and novelty audit are frozen. The deterministic validator is an algebra test only and produces no scientific result.

## Objective

Test whether an endpoint-directional local quadratic certificate predicts the sign and practically meaningful rank of auxiliary-target transfer across a controlled positive/null/harm panel and an independent biological confirmation, while target fit, reliability, spectrum, rank, and movement magnitude fail to identify the sign.

The theory and assumptions are defined in the [Package B directional-boundary draft](../references/package-b-directional-transfer-boundary.md). [E025](E025_participant-e016-biological-transfer.md) is a retrospective failure anchor and cannot count as a prospective prediction. [E028](E028_vaidya-crossmodal-intervention-falsification.md) is the intended external biological collision, but E029 may attach to it only if E028's corrected participant-level result survives its earlier gates.

## Claims under test

- **C1, local identity:** On an exactly quadratic endpoint, the observed mean one-step risk contrast equals the complete directional, curvature, and gradient-covariance expression to numerical tolerance.
- **C2, target-only insufficiency:** Interventions matched on target distribution, learnability, target fit, spectrum, rank, reliability, gradient norm, and movement magnitude can have positive, null, or negative endpoint effects when their update orientations differ.
- **C3, prospective discrimination:** A cross-fitted directional certificate computed without confirmation participants predicts both a predeclared positive regime and a predeclared failure regime better than target-only diagnostics.
- **C4, biological relevance:** If the corrected E028 positive survives, the certificate predicts whether real fMRI supervision beats its phase twin and matched nonbrain target on held-out ECoG participants.

C1 and C2 are implementation and construct-validity claims. They cannot activate Package B alone. C3 is the minimum theory-feasibility claim. C4 is required for a brain-alignment paper identity.

## Estimand and sign convention

For target $B$, control $C$, a common checkpoint $\theta$, and paired complete optimizer-applied directions $\widehat u_s$, the one-step updates are $\theta_s^+=\theta-\eta\widehat u_s$ and the local estimand is

$$
V_{B:C}^{(1)}=\mathbb E\left[R(\theta_C^+)-R(\theta_B^+)\right].
$$

Positive is beneficial. The estimator is the participant-first mean of the exact quadratic terms from the theory note, with technical gradient batches and seeds averaged within participant before biological inference. The confirmation estimand is the final-checkpoint participant mean of the nuisance-subtracted endpoint contrast under the owning external design. The local and final estimands are related by a prospective prediction, not assumed equal.

## Stage 0: algebra and instrumentation

Run [`e029_validate_directional_certificate.py`](../../scripts/e029_validate_directional_certificate.py). It must pass all deterministic assertions at absolute tolerance `1e-12`:

1. exact expected quadratic risk under finite-support stochastic updates equals the mean, curvature, and trace formula for two arms;
2. their exact arm contrast equals the boxed contrast;
3. reflected auxiliary targets have identical Gram matrices, singular values, variances, baseline fit, optimal fit, and post-step target fit;
4. those targets induce equal-magnitude opposite gradients and opposite endpoint effects on the fixed construction;
5. replacing the full optimizer-applied update by the isolated auxiliary gradient fails a constructed common-gradient curvature case, proving that the runner must retain the complete update.

This stage validates algebra and code only. Its printed values are not scientific evidence and must not enter the manuscript.

## Stage 1: controlled prospective panel

### Purpose

Establish that the certificate discriminates sign under known but hidden-to-the-estimator regimes before spending biological compute. This stage must contain at least one positive, one null, and one harmful intervention with target-only diagnostics matched by construction.

### Provisional substrate

Use a linear student with squared endpoint risk so the endpoint is exactly quadratic, then a small nonlinear student as a remainder stress test. The locked linear generator should use independent dataset replicates as the inference units:

$$
X\sim\mathcal N(0,I_d),
\qquad
Y=X_1+\epsilon,
\qquad
\epsilon\sim\mathcal N(0,\sigma^2),
$$

with direct auxiliary targets $S_+=X_1$, $S_0=X_2$, and $S_-=-X_1$. They share the same marginal distribution, rank, reliability, predictability, and target-fit ceiling. The fixed direct auxiliary readout makes their induced update directions positive, orthogonal, and negative relative to the endpoint. A second head-learned version is required to show which target symmetries disappear when an auxiliary head can absorb rotations.

Before precheck, freeze $d$, $\sigma$, train sizes, step sizes, number of independent replicates, and at least five optimization seeds. Use one calibration split to estimate the certificate and a disjoint confirmation split to estimate endpoint effect. Candidate definitions and hyperparameters cannot use confirmation outcomes.

### Primary Stage 1 tests

- **Exact panel test:** for the linear fixed-readout panel, the two-sided CI for prediction error `observed V - certificate V` must lie within a predeclared numerical and Monte Carlo equivalence margin.
- **Sign test:** the one-sided confidence bounds must classify $S_+$ as positive, $S_0$ as an abstention/null, and $S_-$ as harmful on held-out replicates.
- **Matched-diagnostic test:** a model receiving only target fit, reliability, rank, spectrum, gradient norm, and movement magnitude must not separate $S_+$ from $S_-$; the directional certificate must.
- **Remainder stress test:** in the nonlinear panel, the predeclared third-order remainder envelope must cover the observed certificate error. Failure kills extrapolation beyond the quadratic assay.

The independent unit is the generated dataset replicate, not minibatch, seed, example, or target coordinate. Seeds are crossed technical realizations.

## Stage 2: retrospective feasibility anchor

Use E016 and E025 only to determine whether the required gradients, optimizer state, common checkpoints, fixed readouts, nuisance residuals, and Jacobian-vector products can be reconstructed. E026 is a retrospective diagnostic showing that the saved TRIBE and text-feature targets are non-comparable on measured geometry, headroom, nuisance-predictability, and trained-movement axes; those mismatched arms cannot satisfy Stage 1's matched-diagnostic C2 test. Any certificate computed here is explicitly retrospective because the E025 endpoint is already known. It may diagnose why transfer failed and set memory or numerical tolerances, but it cannot satisfy C3, select a target, tune a threshold, or count as prospective evidence.

If the required pre-update checkpoint or optimizer state does not exist, do not approximate it from final weights. Either reproduce the frozen intervention from a newly declared common checkpoint under a separate prechecked run or mark Stage 2 unavailable.

## Stage 3: prospective biological confirmation

### Activation gate

Stage 3 exists only if all of the following hold:

1. Stage 1 passes without threshold revision;
2. E028's exact reproduction and corrected participant-level reanalysis survive;
3. E028 has frozen real-fMRI, phase-twin, and optimization/geometry/learnability-matched nonbrain arms without ECoG outcome feedback;
4. a full primary-source collision audit and independent theory review still justify testing Package B;
5. an anti-confound designer and an oracle reviewer return DESIGN PASS and `READY-TO-RUN: YES` on a frozen manifest and runner.

If E028 does not retain a credible positive candidate, Stage 3 is not replaced by tuning a positive target on Tuckute. Package B remains HOLD or is killed.

### Cross-fitting and blinding

Use the nine ECoG patients as the sole population inference units. Before any certificate or intervention outcome is computed, freeze three patient folds of three patients each using metadata-only balancing variables. For each fold:

- fit nuisance transforms and a differentiable endpoint readout using only the six calibration patients and their permitted training blocks;
- compute participant-specific endpoint gradients and Hessian-vector products only on calibration validation blocks;
- average technical batches and seeds within each calibration participant;
- issue a signed prediction and abstention decision for each frozen E028 target arm before opening the three confirmation patients;
- score final biological transfer on the three confirmation patients under E028's nested lag, nuisance, contiguous-block, and quality controls.

Concatenate the nine out-of-fold confirmation effects only after every fold's prediction is frozen. No patient's outcome can influence the certificate used to predict that patient. Patients, not source-fMRI subjects, seeds, timepoints, electrodes, layers, or folds, remain the biological inference units.

The identifying assumption is transport of the calibration patients' endpoint-gradient and curvature distribution to the confirmation patients. Cross-fitting prevents direct outcome leakage but does not prove this transport. Because the three calibration fits overlap and $n=9$ is small, the final design must freeze a dependence-aware uncertainty procedure that resamples patients and recomputes the complete cross-fit; it must not treat the three folds, nine predictions, source subjects, or target arms as independent replications.

### Candidate arms

Use only E028 arms that passed their own manipulation gates:

1. real fMRI auxiliary target;
2. second-order Fourier phase twin;
3. frozen matched nonbrain audio target;
4. the common pretrained or task-only baseline needed by E028.

Do not add a certificate-optimized biological target. That would test endpoint-guided target construction, not prediction of an independently proposed target.

### Primary comparison

The primary Stage 3 question is whether the cross-fitted certificate correctly predicts the signed participant-mean final-checkpoint contrast for real fMRI versus the strongest surviving control and abstains when its uncertainty overlaps the predeclared SESOI. The exact SESOI, bounded calibration loss, confidence procedure, and familywise treatment of the two real-versus-control contrasts must be inherited from or frozen jointly with E028 before compute.

Target-only baselines are frozen before outcomes and may use held-out target fit, reliability, effective rank, covariance spectrum, intrinsic dimension, gradient norm, CKA movement, and centered Frobenius movement. They may not use any endpoint gradient, endpoint Jacobian, ECoG readout, or held-out ECoG score.

## Prospective success, failure, and kill criteria

### Minimum C3 pass

C3 passes only if, without post-outcome threshold changes:

- the controlled panel contains correctly classified positive and harmful regimes plus a correct null abstention;
- the directional certificate's held-out sign decisions are all correct;
- its prediction error satisfies the frozen equivalence rule;
- its prospective discrimination exceeds every frozen target-only baseline under the predeclared paired test;
- the nonlinear remainder stress test passes.

### Biological C4 pass

C4 passes only if a positive E028 regime exists, the certificate prospectively issues a positive lower-confidence-bound prediction for real fMRI over the strongest control, the final participant-level effect clears E028's SESOI and robustness gates, and all nine out-of-fold predictions were frozen before their confirmation outcomes were opened.

### Falsification

The directional proposal is falsified for its intended use if any of the following occurs:

- the exact implementation identity fails after algebra review;
- target-only diagnostics separate the isometric sign pair because the construction accidentally leaks orientation;
- the certificate misclassifies either controlled sign regime or its bound misses the nonlinear observed change;
- estimates are numerically unstable across permitted calibration folds, batch partitions, or optimizer-state reconstructions;
- a prediction requires confirmation-patient feedback;
- the prospective biological sign is wrong or the certificate confidently predicts a positive when final participant-level transfer fails;
- only the synthetic quadratic panel passes and no independent positive biological or established privileged-information regime can be predicted.

One correct failure prediction is not enough. One correct positive prediction is not enough. A wide interval that always abstains is calibrated but not useful and does not activate Package B.

## Confound and control battery

- **Contiguous folds and nuisance subtraction:** mandatory for every biological endpoint and inherited from E028.
- **Participant inference:** patients are the only population units; technical axes are averaged first.
- **Quality and compute parity:** candidate interventions share model, checkpoint, optimizer state, step schedule, language or speech quality gate, and compute.
- **Manipulation:** target-directed learning and retained-representation movement must pass before endpoint interpretation.
- **Phase twin and matched nonbrain target:** mandatory in Stage 3.
- **No endpoint feedback:** confirmation units are sealed until signed predictions and abstentions are frozen.
- **Complete gradients:** primary, auxiliary, regularization, optimizer preconditioning, and covariance terms are retained. An auxiliary-gradient-only proxy is insufficient.
- **Surrogate boundary:** calibration residual MSE is the differentiable certificate endpoint; final nuisance-subtracted ECoG prediction is the confirmation endpoint. Their relation is tested, not assumed.

## Compute and stopping

No compute budget is authorized in this draft. Precheck must first inventory checkpoint availability and benchmark Jacobian-vector and Hessian-vector memory on one non-scientific microbatch. Freeze a hard wall-clock, GPU-hour, storage, and numerical-failure budget before Stage 1. Stage 3 uses E028 artifacts rather than duplicating its training matrix whenever possible.

Stop immediately after a failed stage. Do not tune the certificate on the failed confirmation outcomes, add candidate targets, change patient folds, enlarge steps until a sign appears, or substitute E025 as prospective evidence.

## Required reviews before readiness

- independent mathematical proof review;
- primary-source novelty collision audit covering task affinity, auxiliary-task weighting, hypergradients, influence functions, generalized distillation, functional feature KD, and gradient/Hessian transfer measures;
- `anti-confound-designer` review of cross-fitting, nuisance handling, and target construction;
- `oracle-reviewer` review of the frozen design, manifest, implementation, thresholds, and result suppression;
- `stat-aggregation-auditor` after aggregated results, before any verdict.

## Current recommendation

**HOLD / READY-TO-RUN: NO.** The exact local identity is testable and the failure mode is clear, but the generic mathematical idea collides with established task-affinity and bilevel methods. The biological positive substrate is conditional on E028, the long-horizon link is unproved, thresholds and compute are not frozen, and no independent precheck has occurred.

## Results

No result. The deterministic validator is an algebra check and not an experiment outcome.

## Related

- [`status.md`](../status.md) - operational authority
- [`Package B directional transfer boundary`](../references/package-b-directional-transfer-boundary.md) - draft derivation and novelty boundary
- [`E025`](E025_participant-e016-biological-transfer.md) - retrospective failure anchor
- [`E028`](E028_vaidya-crossmodal-intervention-falsification.md) - conditional external biological substrate
- [`D057 and D058`](../decisions/decisions.md#d057-canonical-three-package-conference-extension-strategy-and-provenance-2026-07-14-plan--meta) - package activation and kill gates
