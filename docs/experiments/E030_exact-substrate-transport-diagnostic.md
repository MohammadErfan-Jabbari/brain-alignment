---
title: "Experiment - E030: exact-substrate TRIBE transport diagnostic"
tags: [experiment]
aliases: [E030]
---

# Experiment - E030: exact-substrate TRIBE transport diagnostic

**Created:** 2026-07-21 · **Status:** COMPLETE; mechanically verified and author-confirmed on 2026-07-22 · **Mode:** working
**Direction:** Cheap mechanism-localization gate for the methodological/falsification conference route in [D057](../decisions/decisions.md). It does not reopen Package C.
**Predecessors:** [E016](E016_tribe-synthetic-brain-targets.md) for the text-only TRIBE target and saved students, [E025](E025_participant-e016-biological-transfer.md) for the exact Tuckute endpoint and participant-first null, and [E026](E026_tribe-textfeat-target-comparability.md) for the failed cross-target identification control.

---

## Objective and claim boundary

Determine whether E025's near-zero recorded-fMRI transfer can be localized on the exact same 1,000 Tuckute sentences. The text-only TRIBE target must predict participant responses beyond the frozen nuisance baseline and one frozen row-deranged target twin, the saved TRIBE-trained students must retain more nuisance-unique held-out predictivity of that target than their seed-matched KD students, and a cross-fitted bridge must show that the student-predictable target component overlaps the target direction that predicts participant responses.

This is a predictive mechanism-localization diagnostic on one fixed sentence set, nine participants, five fixed language ROIs, one TRIBE construction, one student architecture, and six saved seeds. A joint pass would establish held-out predictive overlap between the student-retained and participant-predictive target subspaces on this exact substrate. It would not establish causal mediation, unique biological information, brain specificity, the causal failure mechanism, stimulus-population generality, model-population generality, or downstream utility.

## Claims under test

- **C1, exact-substrate biological measurability:** aligned text-only TRIBE features add held-out predictivity of each participant's five-ROI Tuckute responses beyond the frozen catalog-complete nuisance model, and the aligned-row score exceeds one capacity-matched within-fold deranged target twin.
- **C2, retained target predictivity:** at the trained middle layer, saved TRIBE-trained representations contain positive nuisance-unique held-out predictivity of the exact-sentence TRIBE target and exceed their seed-matched byte-identical KD representations.
- **C3, predictive overlap bridge:** a train-only composition of the participant-predictive target readout and the student-to-target readout adds held-out participant-response predictivity, exceeds the seed-matched KD composition, and shows a larger TRIBE-minus-KD increment for aligned target rows than for the frozen twin.

## Competing explanations

1. **Measurability limit:** the text-only TRIBE target does not add practically relevant participant-response predictivity under the frozen linear assay.
2. **Fixed-control limit:** aligned target rows do not outperform the single frozen capacity-matched twin by a practically relevant amount.
3. **Retention limit:** saved students show no measurable absolute target retention or no incremental retention over KD on this domain.
4. **Overlap limit:** student-predictable target structure does not improve participant prediction, does not exceed KD, or does not exceed the aligned-versus-twin control.
5. **Capacity or leakage artifact:** a high-dimensional target, fold leakage, item-order structure, or nuisance mismatch creates apparent predictivity without aligned target content.

## Outcome seal and authorized order

The new E030 outcomes are any Tuckute-specific TRIBE-to-response score, student-to-TRIBE score, composed bridge score, paired contrast, confidence bound, sign count, or terminal classification. Existing E025 and E026 values are already public inside the repository, but no new E030 target-response, target-retention, or bridge value may be opened before the following order completes:

1. Freeze this E record, one canonical JSON configuration, the runner, analyzer, deterministic fixtures, and the metadata-only design-manifest builder. The builder reads only `cond`, `item_id`, and `sentence`; it may not call an E025 participant loader or touch `response_target`.
2. Pass unit, leakage, fold-local-transform, item-order, hash, and synthetic-recovery tests.
3. Run `anti-confound-designer`, incorporate outcome-blind corrections, then run a fresh `oracle-reviewer` on exact file hashes.
4. Record `DESIGN PASS / READY-TO-RUN: YES` and a canonical bundle SHA-256.
5. Generate the exact text-only TRIBE cache without loading participant responses; verify only schema, shape, order hashes, finite values, vertex identity, runtime identity, and artifact SHA-256.
6. Freeze the generated cache hash into a post-target acquisition manifest. Do not inspect target geometry or any participant score.
7. Run the scorer once, then the analyzer once. After unsealing, review is abort-only; a necessary design change terminates this protocol version.

## Fixed sources

- Tuckute condition `B`, ordered item and participant grid, exclusions, ROIs, covariates, text hash, and source hash are inherited byte-for-byte from `outputs/E025/manifest.json`.
- The frozen source identities are E025 manifest SHA-256 `2729c0c97b2f845ccf8f58a13e01ecf87f44029564ca615269230437de46698d`, extraction SHA-256 `b49c2795c55961cae161084afa1d3409dd662b893f9a40fa6a4e9373bc2c84c5`, participant-loader SHA-256 `2357bae93d80457d7971c1ed368a30b15da6341171cb30036f3d2e2b360f1b1f`, Tuckute CSV SHA-256 `a990474e5ecd9bdbbf07c0df81be6f724fc377fe888d07432097a7f7b115cee4`, ordered item SHA-256 `0de41d33d8e41ee4a69e898bcbcc42f7c9e65f7cdce1239a00def95ef7dd206b`, and ordered text SHA-256 `6766e068a2b4f4ad84fad525cdb1f41f60524f1c206139741e9fc22ef1cb5702`.
- Primary nuisance arrays are inherited from `outputs/E025/nuisance_tuckute.npz`: sentence token length, normalized item position, Tuckute imageability, and fixed GPT-2-medium static embeddings. The byte-identical E025 base tier without imageability is the continuity sensitivity. The existing GPT-2XL and PCFG-surprisal expansion is a nonterminal stress test because it overlaps the tested language representation.
- Saved layer-6 and layer-7 representations and their checkpoint aliases are inherited from the 30 hash-verified caches in `outputs/E025/reps/` through `outputs/E025/extraction.json`. E030 uses only the 12 TRIBE-family aliases `kd_only` and `tribe_mse` for seeds `0` through `5`; every cache is rehashed and rebound by metadata rather than filename.
- The generated target must use the E016 text-only TRIBE construction exactly: `features=["text"]`, `unsloth/Llama-3.2-3B`, synthetic-text events, word duration `0.35`, word gap `0.05`, minimum duration `1.0`, TR `1.0`, `batch_items=32`, all `20,484` fsaverage5 vertices, and the vertex order already recorded in `outputs/E016_tribe/kd_targets/text/heldout_start0_n1999_full.npz`.
- The acquisition manifest binds Tuckute item IDs `1` through `1000` to generator item indices `0` through `999` by `item_id = item_index + 1`, records both frozen ordered hashes, and rejects any nonunique, empty, newline-containing, or edge-whitespace text.
- Before either assay, standardize the generated target with the exact E016 Phase-3 float32 `numpy.mean` and population `numpy.std` plus `1e-6` semantics, recomputed from `outputs/E016_tribe/kd_targets/text/train_start0_n95999_full.npz`, SHA-256 `de2f18d4d6ae61659e0f2a9220476a9e8ed23ab10c63d8be2794610d4d7ef7d1`. Never fit global target statistics on Tuckute and never substitute an extracted target array without validating it against the owning source cache.
- Before the 1,000-item generation, replay the retained two-item, dimension-16 E016 smoke cache byte-semantically under the pinned TRIBE environment. Array or metadata disagreement blocks acquisition. The runtime manifest binds the generator, checkout and dirty diff, environment freeze, model snapshots, checkpoint, and shard hashes.
- The replay reference is `outputs/E016_tribe/kd_targets/text/heldout_start0_n2_d16_smoke.npz`, SHA-256 `cba45474a1215afb11680a6b778a94d5753b71d71d1a49e199b525823087ac3c`, with WikiText source SHA-256 `d327c96e204accae6a09bbf760d382f2efa1650a648917f03d207b86a5cc3de2`. Compare semantic array and fixed metadata identities, not the whole generated NPZ, because elapsed time and newer metadata are expected to differ.
- The canonical E030 target path is `outputs/E030/tribe_tuckute_condition-b_n1000_full.npz`. Its ordered text hash must equal E025's frozen hash before scoring.

## Design lock candidate

### Shared split and transform rules

- Preserve the E025 item order and use five contiguous outer folds. Never shuffle items.
- Fit every stimulus-domain scaler, PCA, nuisance model, ridge parameter, and fresh target readout using the outer-training rows only. The externally frozen E016 target standardization is the sole exception. The outer test block is used once.
- For each outer fold, fit target PCA-50 once on the canonical aligned outer-training rows and reuse that exact fitted basis for aligned and twin transforms. The train-row target multiset is identical after the within-block derangement, but scikit-learn's randomized PCA approximation is not row-order invariant; refitting would contaminate the fixed-control contrast. Reuse the same fold-specific representation and static-nuisance transforms across alignment conditions.
- Use ridge alphas `[1, 10, 100, 1000, 10000]`. Select alpha using training data only.
- For C2 multi-output target prediction, use scikit-learn's default single shared ridge alpha across all fixed target coordinates (`alpha_per_target=false`). Per-coordinate alpha selection is forbidden. The config must also freeze the target-coordinate variance floor used only to validate the denominator; no coordinate may be dropped or reweighted after target acquisition.
- Coordinates, folds, seeds, ROIs, and technical repetitions are never treated as population units.
- Missing, nonfinite, hash-mismatched, reordered, or shape-mismatched inputs invalidate the run; they do not trigger substitution or exclusion.

### Identifying assumptions and inferential scope

- The 1,000 sentences are a fixed substrate. All item-level folds estimate held-out prediction on this set; no test licenses stimulus-population generalization.
- C1 and C3 use participants as independent biological units. Participant t-intervals target the mean effect among similarly sampled, endpoint-valid participants conditional on this sentence set and require an approximately normal distribution of participant-level effects. Exact sign tests require independent participant signs with probability `0.5` under the sharp zero-median null. Generalization beyond this cohort requires the participant inclusion mechanism to be ignorable for the reported contrasts.
- The excluded participant and all endpoint-valid participants are frozen from E025 before E030 outcomes. No participant, ROI, or response is selected using an E030 score.
- C2's seeds are independent technical realizations of the frozen training procedure, not biological or model-population replications. The exact paired sign-flip test for `B` requires seed-matched contrasts to be sign-exchangeable under the technical null, conditional on their magnitudes. Seed t-intervals are descriptive stability summaries and do not support population claims.
- C3 averages seeds and folds inside each participant before participant inference; those participant claims are conditional on the exact six frozen seed-matched pairs. It also averages participants and folds inside each seed for `D` and `J` and applies the same exact magnitude-preserving sign-flip assumption as C2. These seed gates support technical-realization stability only, not biological or model-population inference.
- Every unique-R2 and bridge quantity is a cross-validated linear predictive contrast under the frozen nuisance model. The identifying assumption for its scoped interpretation is that train-only transforms, fixed item order, and the nuisance/control battery remove the enumerated leakage and capacity alternatives. These quantities are not conditional mutual information, causal effects, or mediation estimates.

### C1: participant-first TRIBE biological measurability

For each participant `u` and outer fold `f`, fit train-only PCA-50 to the aligned `20,484`-coordinate TRIBE feature matrix. Score the participant's five ROI responses with the exact E025 variance partition:

- nuisance model `N`: token length, normalized position, imageability, and train-only PCA-50 static GPT-2-medium embeddings;
- full model `N+T`: the same nuisance block plus train-only PCA-50 aligned TRIBE features;
- fold score `U_aligned(u,f) = R2(N+T) - R2(N)`.

Construct one exact content-null twin by applying a hash-keyed Sattolo derangement separately within each fixed 200-item outer-fold block. The permutation has zero fixed points, preserves the exact target-row multiset inside every block, is generated before target values or participant scores are read, and is stored with a SHA-256. Transform the twin through the identical canonical aligned-train target PCA basis for that fold. For participant `u`, define:

`A(u) = mean_f U_aligned(u,f)`

`Q(u) = mean_f [U_aligned(u,f) - U_twin(u,f)]`.

`A(u)` tests above-nuisance predictivity. `Q(u)` tests row-specific alignment rather than target dimension, marginal distribution, or within-fold geometry. Both are primary C1 participant estimands.

For both `A` and `Q`, report the participant mean, median, SD, two-sided t-CI95, marginal one-sided 95% upper and lower bounds, Bonferroni simultaneous family-95% one-sided bounds across `A/Q`, exact sign test, Wilcoxon signed-rank test where valid, all nine values, train-four and heldout-five means, five shared-block means, every leave-one-participant-out mean, and every leave-one-block-out mean. Folds and ROIs are aggregated within participant before inference. Report observed-variance MDE and power at the inherited `+0.002` unique-R2 reference as sensitivity, not as a newly selected cutoff.

Primary C1 passes only if all validity checks pass and both `A` and `Q` have two-sided participant t-CI95 lower bounds above zero, at least eight of nine participant values positive, exact sign values at most `0.05`, positive heldout-five means, and every participant- and block-leave-out point estimate positive under the imageability-complete nuisance. The E025 base nuisance is reported for continuity and the full-covariate stress test is reported without rescue authority. If a valid nonpass has a simultaneous family-95% one-sided upper bound below `+0.002`, report practical exclusion relative to that inherited reference; otherwise distinguish unresolved or power-limited evidence from contradiction.

### C2: saved-student target retention

Use the same externally standardized TRIBE matrix as the target and the existing Tuckute representations as predictors. Layer 6, the trained middle layer used by E016's fresh-head target metric, is primary. Layer 7 is a locked sensitivity and may not rescue a failed layer-6 result.

Within each outer fold, fit train-only PCA-50 to the saved student representation and score the standardized TRIBE target with the same nuisance partition used in C1:

- nuisance model `N`: the fixed imageability-complete nuisance with train-only static-embedding PCA;
- full model `N+H`: the same nuisance plus train-only PCA-50 of the saved layer-6 representation;
- `V(arm,s,f) = R2(N+H -> TRIBE) - R2(N -> TRIBE)`.

Aggregate target prediction as one variance-weighted `1 - total_SSE / total_SST` across all `20,484` coordinates, so coordinates are never treated as replications and near-constant coordinates cannot dominate an equal-coordinate mean. Also report E016's equal-coordinate mean R2 as a frozen, non-rescuing continuity sensitivity. All coordinates remain fixed; nonfinite values, zero segment counts, or a failed external-standardization check invalidate the run rather than triggering coordinate selection.

For seed `s`, define absolute extractability `M(s) = mean_f V(tribe_mse,s,f)` and the target-trained increment `B(s) = mean_f [V(tribe_mse,s,f) - V(kd_only,s,f)]`. Require the recorded E025 in-domain quality, target-learning, and layer-6 movement prerequisites after exact hash revalidation; Tuckute data may not replace the fixed 1,999-sentence WikiText language-quality endpoint.

Report all `M(s)` and `B(s)` values, their six-seed means, medians, SDs, descriptive two-sided t-CI95, marginal one-sided 95% bounds, Bonferroni simultaneous family-95% one-sided bounds across `M/B`, the exact `2^6` magnitude-preserving sign-flip test for `B`, all five shared-block values, every leave-one-seed-out mean, and every leave-one-block-out mean. Seeds are technical intervention realizations, not biological replications.

Primary C2 passes only if all validity and inherited quality/movement gates pass, all six `M(s)` and all six `B(s)` values are positive, both two-sided t-CI95 lower bounds are above zero, the exact two-sided sign-flip value for `B` is at most `0.05`, and every block- and seed-leave-out mean remains positive. Layer 7 and equal-coordinate aggregation are reported as sensitivities only.

### C3: cross-fitted student-target-brain overlap bridge

C1 and C2 are necessary but not sufficient for overlap: the participant-predictive target direction and the student-retained target direction could be disjoint. C3 therefore composes the two train-only linear paths and scores the composition only on the untouched outer-test block.

For each participant `u`, seed `s`, arm `a`, alignment `r` in `{aligned, twin}`, layer, nuisance variant, and outer fold `f`:

1. Reuse the fold's canonical aligned-train target PCA-50 basis, representation PCA-50, nuisance block, and C1 nuisance-only response prediction. Apply the same target basis to aligned and twin rows.
2. Fit the C1 full response model `Y_u ~ [N,T_r]` on outer-training rows and retain the standardized target-PC coefficient block `beta_TY(u,r,f)` and its train-fold target scale.
3. Fit shared-alpha ridge `T_r ~ [N,H(a,s)]` on the same outer-training rows and retain the standardized representation coefficient block `beta_HT(a,s,r,f)`.
4. On the outer-test block, compute only the representation-specific target-PC contribution `delta_T = standardized(H_test) beta_HT`. Convert that contribution through the C1 target scale and target coefficient block to obtain `delta_Y = (delta_T / target_scale) beta_TY`.
5. Add `delta_Y` to the separately fitted C1 nuisance-only prediction and define `G(r,a,s,u,f)` as the mean five-ROI held-out R2 of that composed prediction minus the mean five-ROI held-out R2 of the nuisance-only prediction.

The isolated coefficient blocks must algebraically reproduce their corresponding linear-model feature contributions. Changing any outer-test target or response value must not change either fitted path. The aligned and twin paths are refit independently; the twin is the single frozen within-block derangement, not a sample from a permutation distribution.

Average seeds and folds inside participant:

`O(u) = mean_(s,f) G(aligned,tribe_mse,s,u,f)`

`D(u) = mean_(s,f) [G(aligned,tribe_mse,s,u,f) - G(aligned,kd_only,s,u,f)]`

`J(u) = mean_(s,f) [(G(aligned,tribe_mse,s,u,f) - G(aligned,kd_only,s,u,f)) - (G(twin,tribe_mse,s,u,f) - G(twin,kd_only,s,u,f))]`.

`O` tests absolute aligned predictive overlap. `D` tests incremental overlap over seed-matched KD. `J` tests whether that increment is larger for aligned rows than for the exact frozen twin. These are participant-level predictive path-product estimands, not causal mediation effects.

Report all nine participant values for `O`, `D`, and `J`; participant mean, median, SD, two-sided t-CI95, marginal one-sided 95% bounds, Bonferroni simultaneous family-95% one-sided bounds across `O/D/J`, exact sign and Wilcoxon tests where valid; train-four and heldout-five means; shared-block means; every participant- and block-leave-out mean; all six seed-level `D` and `J` values averaged over participants and folds; exact `2^6` magnitude-preserving sign-flip tests for those seed-level contrasts; and leave-one-seed-out grand means. Primary C3 uses layer 6 and the imageability-complete nuisance. Layer 7 and the other nuisance variants are non-rescuing sensitivities.

Primary C3 passes only if C1 and C2 pass, all validity gates pass, and each of `O`, `D`, and `J` has a two-sided participant t-CI95 lower bound above zero, at least eight of nine participant values positive, an exact two-sided sign value at most `0.05`, a positive heldout-five mean, and positive participant- and block-leave-out means. All six seed-level `D` and `J` values must be positive, both exact magnitude-preserving sign-flip values must be at most `0.05`, and every leave-one-seed-out grand mean must be positive. Synthetic shared-subspace recovery, disjoint-subspace rejection, outer-test leakage, and coefficient-contribution tests must pass before readiness.

### Terminal classifications

For ordered classification, an endpoint "positively passes" when its own frozen CI, sign, subgroup, and leave-out conditions pass; a stage passes only when every endpoint and inherited validity condition for that stage passes. Never inspect a downstream failure label through an unresolved upstream endpoint.

- **JOINT PASS / predictive overlap supported:** C1, C2, and C3 all pass. E030 then supports held-out predictive overlap between participant-predictive and student-retained target subspaces on this exact substrate. It does not license causal, mediation, brain-specific, downstream-utility, or population-general claims.
- **NO PRACTICALLY RELEVANT LINEAR MEASURABILITY:** C1 does not pass and `A` has a simultaneous family-95% one-sided upper bound below the inherited `+0.002` reference under the primary assay.
- **NO PRACTICALLY RELEVANT ADVANTAGE OVER THE FROZEN TWIN:** `A` positively passes its primary rules, C1 does not pass, and `Q` has a simultaneous family-95% one-sided upper bound below `+0.002`. This concerns the exact frozen twin only, not a derangement distribution.
- **NO MEASURABLE ABSOLUTE RETENTION:** C1 passes, C2 does not pass, and `M` has a simultaneous family-95% one-sided upper bound at or below zero.
- **NO INCREMENTAL RETENTION OVER KD:** C1 passes, `M` positively passes its primary rules, C2 does not pass, and `B` has a simultaneous family-95% one-sided upper bound at or below zero.
- **NO MEASURABLE ABSOLUTE PREDICTIVE OVERLAP:** C1 and C2 pass, C3 does not pass, and `O` has a simultaneous family-95% one-sided upper bound at or below zero.
- **NO INCREMENTAL PREDICTIVE OVERLAP OVER KD:** C1 and C2 pass, `O` positively passes its primary rules, C3 does not pass, and `D` has a simultaneous family-95% one-sided upper bound at or below zero.
- **NO ALIGNED-ROW ADVANTAGE OVER THE FROZEN TWIN:** C1 and C2 pass, `O` and `D` positively pass their primary rules, C3 does not pass, and `J` has a simultaneous family-95% one-sided upper bound at or below zero. This concerns the exact frozen twin only.
- **INCONCLUSIVE:** a validity gate fails, a primary pass rule fails without its corresponding exclusion bound, numerical stability fails, or required evidence is missing.

A valid failure is not rescued. None of these classifications reopens Package C or licenses new training.

## Confound and control battery

- exact E025 participant, item, ROI, text, nuisance, exclusion, and checkpoint identities;
- contiguous outer folds and train-fold-only transforms;
- capacity-fair PCA-50 for TRIBE and static nuisance features;
- one frozen within-fold zero-fixed-point row-deranged target twin for C1 and C3, with claims limited to that fixed control;
- seed-matched byte-identical KD controls for C2 and C3;
- layer 6 fixed before outcomes, layer 7 sensitivity only;
- E025 base continuity, imageability-complete primary, and nonterminal full-covariate stress nuisance variants;
- deterministic item-order, vertex-order, target-cache, representation-cache, runtime, and source hashing;
- synthetic positive, null, misalignment, shared-subspace, and disjoint-subspace fixtures plus explicit leakage and coefficient-contribution tests;
- participant-first scoped inference for C1 and C3, paired-seed technical inference for C2, and no stimulus-population inference.

## Compute and stop rule

- No new student training or representation extraction is permitted.
- Target generation ceiling: one L40S, four GPU-hours, and 10 GB retained storage.
- Scoring and analysis are separate guarded stages; each has its own ceiling of 24 process CPU-hours and 64 GB RAM. The retained `outputs/E030/` tree must remain below 10 GB throughout both stages.
- Enforce the target wall timeout from the GPU-hour ceiling. Enforce scoring/analyzer CPU time, address-space and live-RSS limits, and retained `outputs/E030/` bytes mechanically; record observed resource use in the sealed artifacts.
- Before readiness, enumerate the exact v2 factor grids and model/PCA/composition counts at `n=100`, target dimension `512`, nine synthetic participants, and six seeds. Separately measure production-shape primitives for C1 five-output ridge, the `20,484`-output target ridge, 50-output bridge-retention ridge, bridge composition plus response scoring, and worst-case target-coordinate PCA. Project total process CPU and wall time as each exact category count times its own measured primitive. This is a bounded production-cost projection, not a timed full-grid run.
- Stop on the first failed hash, order, finite-value, fold-locality, deterministic-replay, memory, or numerical-equivalence gate. Stop after the frozen analysis; do not add layers, target projections, participants, ROIs, shifts, nuisance variants, alphas, seeds, or alternative aggregations.

## Forbidden adaptations

Do not inspect target geometry to choose a projection, change the frozen derangement, select participants or ROIs, replace the target generator, change event timing, use E025 participant effects to choose a layer or threshold, pool folds or ROIs as independent units, add a favorable target subset, or retrain a student. After unsealing, a correction may only invalidate or narrow the study; it cannot change the design.

## Planned executable surface

- `configs/e030_exact_substrate_transport.json`: canonical frozen configuration.
- `scripts/e030_exact_substrate_transport.py`: metadata manifest, exact target generation, raw C1/C2/C3 scoring, and deterministic fixtures.
- `scripts/e030_analyze_exact_substrate.py`: frozen aggregation, uncertainty, robustness, and terminal classification.
- `outputs/E030/`: gitignored manifests, generated target, raw score, analysis, benchmark, logs, and independent audit.

## Precheck

**Current verdict:** DESIGN PASS MAINTAINED. Execution is authorized only when the live readiness artifact reports `ready: true` and binds this exact prospective bundle.

Completed outcome-blind gates:

1. The `anti-confound-designer`, counterargument, mathematical, statistical, and repeated code/provenance reviews are incorporated in the fixed twin, shared aligned/twin target basis, C3 bridge, participant/seed inference, simultaneous exclusion bounds, ordered terminal rules, exact source chain, and resource guards. The final independent statistical and code panels are clean.
2. Runner self-test schema `e030-selftest.v2` passes all `12/12` synthetic checks, including the bound target-generator argument contract, shared- versus disjoint-subspace recovery, train-only leakage, exact coefficient composition, aligned/twin PCA-basis reuse, same-size source-mutation rejection, E025 ridge equivalence, external standardization, and deterministic Sattolo identity. Analyzer self-test passes all `29/29` arithmetic, inference, familywise-bound, ordered-classification, schema, basis, resource, runtime, and identity checks.
3. The exact v2 grids enumerate uniquely and completely to `270` C1 rows, `360` C2 rows, and `6,480` C3 rows. Benchmark schema `e030-benchmark.v3` projects `4,089.144` process-CPU seconds and `626.506` wall seconds from category-specific production-shape primitives, below the `86,400`-second scoring CPU ceiling; observed peak RSS is `1,140,252` KiB, below `67,108,864` KiB.
4. Exact E016 float32 standardizer reconstruction passes in `36.393` seconds at peak RSS `15,549,528` KiB, below the 64 GiB ceiling.
5. The two-item, dimension-16 TRIBE runtime replay matches every frozen semantic array hash and stable metadata field under the bound checkout and isolated environment in `25.526` seconds.
6. Current SHA-256 identities are configuration `00dc123ae56a6c93608a6ebc88dce27af62340fb12b842835ff65d2092dce773`, runner `1fd1d4693b07c2a5e73647dfae1c00114c2e261c64f97dffa615a902b153e407`, analyzer `f65efea6217e45f00d5c0eabc11b2ddbae52da148b3e542d0debf78a03335a3e`, and design manifest `02f83ce168a3d59582cb94e90b1ab81c0f7fdbf5b2a5f1835df28d4ea0d0d254`.

The earlier oracle candidate and final approvals were panel-clean but are superseded because the runner interface correction changes the executable bundle hash. No scientific design setting changed.

Mechanical gate: the runner requires exact oracle approval of the current semantic bundle and a current readiness seal before target acquisition. The live readiness artifact, rather than prose in this record, determines whether that gate is open. At prospective bundle freeze, no Tuckute-specific TRIBE target, participant score, bridge score, or target geometry had been generated.

The first post-seal acquisition attempt stopped at batch `0:32` before publishing any target because the isolated worker omitted the bound generator's `quiet` argument. No canonical target, target manifest, acquisition manifest, participant score, or target geometry was created. The correction adds only the missing interface flag; it changes no scientific setting, target input, estimator, or claim. All runner-bound prechecks, bundle hashes, oracle approval, and readiness must be regenerated before retry.

## Results

### Evidence identity and validity

The corrected prospective bundle had semantic SHA-256 `2666505f679f5737f3d5c723fd791304b3965435ee4b6e91bdb05d431f40bf71` and file SHA-256 `624fc21368f71c6272bebc94c4cf7b2865fe79745481895ee94c77d6da0b2167`. The exact oracle report SHA-256 was `4db7efb9ff675c53fadc313d59c7a41a58a91dfb9f67881d8f1cb75a2eab0158`; readiness v2 passed every pre-result gate at SHA-256 `119eb3d2e92f51ac858f56b17feb94ac5c670b343b2e57e835477a62e92ac4a3`.

The successful retry generated the finite float32 target at frozen shape `1000 x 20484`. The canonical target path is `outputs/E030/tribe_tuckute_condition-b_n1000_full.npz`, with SHA-256 `a1fb8667e5c27a7e9bde35cb5f3a4f24622ad13c3b79e91a884c119ef3b65233`. The target-manifest SHA-256 was `c17784f13ca9675c5696703986d5f645b4f6966b02ccffa79626d4a0f4377f08`, and the acquisition-manifest SHA-256 was `c594c0d3f3e5478253054d229bc2fe664f71af231e63b1e61d810ba2e8fc8c17`. Target generation used `551.892` process-CPU seconds, `385.204` worker wall seconds, and peak RSS `9,372,592` KiB.

The one-shot scorer produced exactly `270` C1, `360` C2, and `6,480` C3 fold rows. Raw-score SHA-256 was `cebea58cd7f7d82908b26a25714a1d256ab674a7b08d9a18d94835b0f7fcb6e4`; frozen-analysis SHA-256 was `43a4f3b01641072345149e651cdd0b1ae0c903bb74366db2006f31b89d8dd818`. Every hash, source, grid, finite-value, coordinate-floor, participant-grid, inherited-gate, target-PCA-reuse, and student-PCA-reuse validity check passed. Scoring used `2,667.244` process-CPU seconds, `371.145` wall seconds, and peak RSS `1,366,092` KiB, within every frozen limit.

The canonical result paths are `outputs/E030/raw_scores.json`, SHA-256 `cebea58cd7f7d82908b26a25714a1d256ab674a7b08d9a18d94835b0f7fcb6e4`, and `outputs/E030/analysis.json`, SHA-256 `43a4f3b01641072345149e651cdd0b1ae0c903bb74366db2006f31b89d8dd818`. This sentence is a mechanical path binding; it changes no result or verdict.

### C1 primary biological-measurability result

Under layer-independent target PCA-50, the imageability-complete nuisance model, five fixed ROIs, and participant inference at `n=9`, the aligned target's unique increment above nuisance was:

| Estimand | Mean | Two-sided 95% t interval (unadjusted) | Signs and exact test | Status |
|---|---:|---:|---:|---|
| `A`, aligned above nuisance | `-0.00449438` | `[-0.01069542,+0.00170665]` | `3/9` positive; exact sign `p=0.5078` | nonpass; simultaneous upper bound `+0.00170665 < +0.002` |
| `Q`, aligned minus frozen twin | `+0.00175820` | `[-0.00357480,+0.00709120]` | `5/9` positive; exact sign `p=1.0` | unresolved |

Every leave-one-block and leave-one-participant mean for `A` was negative. The train-four mean was `-0.00046685`; the prospectively held-out-five mean was `-0.00771641`. The inherited `+0.002` reference is an internal continuation threshold carried from E025, not an externally established practical-importance threshold for this different estimand.

**Sensitivity, recorded 2026-09-02.** The design at line 97 predeclared an observed-variance MDE and power at the inherited `+0.002` reference. Both were computed and stored in `outputs/E030/analysis.json` under `c1.cells.imageability_primary.A_aligned_above_nuisance.statistics.observed_variance_sensitivity`, but were never transcribed into this record; they are recorded here. The observed-variance 80% MDE is `0.00860754`, and power at the `+0.002` reference is `0.10093467`. Per line 97 these are sensitivity, not a cutoff, and per E009 line 178 an MDE is not a null, an equivalence margin, or a bound on the true effect. Two things follow, and they pull in opposite directions. The low power concerns *detecting* a `+0.002` effect; the nonpass here is an *exclusion*, and it holds because the observed upper bound `+0.00170665` fell below `+0.002`, which it did because the point estimate is negative (`-0.00449438`, `3/9` positive, every leave-one-out mean negative), not because the design is precise. But that exclusion clears the reference by `0.00033`, roughly a twentieth of the MDE, so the classification is not robust to small perturbations of the estimator, the nuisance model, or the participant set, and the narrow phrasing already used above is the register this result supports. This paragraph transcribes predeclared sensitivity values; it changes no result, bound, or verdict.


**Label correction (2026-09-02).** The interval column in the three tables above was headed "Bonferroni family-95% two-sided t interval". That label is wrong: every interval reported is the *unadjusted* two-sided 95% t interval (`two_sided_t_ci95` in `outputs/E030/analysis.json`), and the headers are corrected accordingly. The adjustment enters only through the separate `simultaneous_family_one_sided_t_upper95` field, which is the quantity the predeclared rules at lines 97, 115, 143 and 152 name and the quantity `scripts/e030_analyze_exact_substrate.py:2912` classifies from. For the C1 and C2 families (size 2) the simultaneous one-sided bound is numerically identical to the reported two-sided upper endpoint, because Bonferroni one-sided alpha `0.05/2` equals the unadjusted two-sided endpoint alpha `0.025`; for the C3 bridge family (size 3, endpoint alpha `0.0167`) it is not, so the C3 table's endpoints are two-sided values and the simultaneous bounds are `O +0.00306982`, `D +0.00015505`, `J +0.00014858`. **No classification moves under any construction:** C1 is nonpass on `+0.00170665 < +0.002` (and on the marginal one-sided `+0.00050610`), C2 `M` has a positive lower bound throughout, and every C3 quantity spans zero throughout. The label mattered because a reader applying it literally would compute a Bonferroni two-sided upper endpoint of `+0.00290469` for `A`, above `+0.002`, and reach INCONCLUSIVE. The predeclared rule governs: it is in freeze commit `26bb912` at 00:27 UTC, the raw result was created at 00:41 UTC, and the table header first appears in the later result commit.

### C2 target retention and C3 bridge diagnostics

The TRIBE-trained students retained the exact target absolutely, but did not show a reliable incremental retention advantage over KD:

| Estimand | Mean | Two-sided 95% t interval (unadjusted) | Stability evidence | Status |
|---|---:|---:|---:|---|
| `M`, absolute TRIBE target extractability | `+0.04072547` | `[+0.03905273,+0.04239820]` | `6/6` positive; exact sign `p=0.03125` | supported positive interval |
| `B`, TRIBE minus KD retention | `-0.00085451` | `[-0.00224613,+0.00053712]` | `2/6` positive; exact magnitude-preserving sign-flip `p=0.1875` | unresolved |

The bridge quantities were all unresolved under participant inference and cannot generate a downstream ordered failure label because C1 failed first:

| Estimand | Mean | Two-sided 95% t interval (unadjusted) | Stability evidence |
|---|---:|---:|---|
| `O`, absolute aligned predictive overlap | `+0.00124221` | `[-0.00040020,+0.00288463]` | `7/9` positive; exact sign `p=0.1797` |
| `D`, TRIBE minus KD bridge | `+0.00003100` | `[-0.00008049,+0.00014248]` | `5/9` positive; seed sign-flip `p=0.375` |
| `J`, aligned-minus-twin increment | `+0.00002937` | `[-0.00007777,+0.00013650]` | `5/9` positive; seed sign-flip `p=0.375` |

### Independent recomputation and scoped mechanical verdict

An independent `/interpret` recomputation from the raw rows matched all `748` load-bearing leaves, pass gates, diagnostics, simultaneous bounds, seed sensitivities, and the ordered classification with zero exact or tolerance-only mismatches. A separate provenance audit rehashed all `40` referenced files, covering `14,707,003,958` bytes, and found the readiness-to-analysis chain, schemas, grids, semantic hashes, one-shot guards, atomic writes, and resource limits panel-clean. The adversarial interpretation review agreed with the mechanical trigger and required narrower prose.

**Mechanical classification:** `NO PRACTICALLY RELEVANT LINEAR MEASURABILITY`. Read only within the frozen scope, this means that the PCA-50 text-only TRIBE target did not add a participant-mean unique linear predictivity increment of at least `+0.002` beyond the specified nuisance model on these 1,000 sentences, nine participants, and five ROIs. It does not exclude total or nuisance-redundant target predictivity, information outside the top 50 target PCs, nonlinear readouts, other endpoints, other cohorts, or a row-specific aligned-versus-twin advantage. `Q` remains unresolved.

**Author-confirmed project consequence:** E030 localizes the first observed failure before student-to-brain overlap: the target is strongly recoverable from TRIBE students, but its unique recorded-fMRI measurability fails the frozen C1 practical-exclusion rule. This does not change the thesis verdict that the tested distillation regimes show no reliable brain-guided benefit, and it does not causally explain E025. Erfan confirmed this scoped framing on 2026-07-22 for synchronization into the extended manuscript.

## Related

- [`status.md`](../status.md): operational authority
- [E016](E016_tribe-synthetic-brain-targets.md): target construction and saved-student intervention
- [E025](E025_participant-e016-biological-transfer.md): participant-level biological endpoint
- [E026](E026_tribe-textfeat-target-comparability.md): comparator-identification boundary
- [E028](E028_vaidya-crossmodal-intervention-falsification.md): binding external conference-extension gate
