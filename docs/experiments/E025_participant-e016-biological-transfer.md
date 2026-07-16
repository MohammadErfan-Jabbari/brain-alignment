---
title: "Experiment — E025: participant-level E016 biological transfer"
tags: [experiment]
aliases: [E025]
---

# Experiment — E025: participant-level E016 biological transfer

**Created:** 2026-07-16 · **Status:** DESIGN LOCKED — no E025 endpoint has been scored; `/precheck` passed · **Mode:** working
**Direction:** Conference-extension prerequisite shared by Packages A and C in [D057](../decisions/decisions.md). This resolves the participant-scope limitation in [E016](E016_tribe-synthetic-brain-targets.md) without retraining.
**Predecessors:** [E008](E008_per-participant-f1-solidification.md) for participant/fold inference and UID exclusion; [E016](E016_tribe-synthetic-brain-targets.md) for the six saved TRIBE and text-feature branches.

---

## Objective

Determine whether the E016 intervention that was learnable on its synthetic target produces stable biological transfer across individual Tuckute participants, rather than only on the existing five-participant averaged endpoint. This is a retrospective scope test of saved students, not a brain-specificity experiment: the existing text-feature arm is dimension-matched but is not yet geometry-, information-, or learnability-matched.

## Competing explanations

- **Participant-general transfer:** TRIBE-supervised students improve held-out, nuisance-subtracted alignment to individual recorded brains beyond both their byte-identical KD baselines and the sentence-local text-feature students.
- **Averaged-endpoint or target-specific failure:** the synthetic TRIBE gain does not transfer positively and stably across individual recorded brains.
- **Shared-stimulus fold artifact:** an apparent participant mean is carried by one contiguous stimulus fold shared across participants.
- **Layer displacement:** an effect appears at the synthetic training layer 6 but not at the predeclared biological verdict layer 7.

## Design lock candidate (must pass `/precheck` before scoring)

### Data and artifacts

- Tuckute condition B, five left-hemisphere language sub-ROIs, 1,000 ordered sentences.
- Exclude UID 853 under the E008 incomplete-ROI rule. The valid participant units are `797, 837, 841, 848, 856, 865, 875, 876, 880` (`n=9`).
- The original training-participant subset becomes `848, 865, 875, 876` (`n=4`) after exclusion; the held-out subset is `797, 837, 841, 856, 880` (`n=5`). Report them separately.
- TRIBE saved students: seeds 0–2 from `phase3_rerun_tribe_gpt2_n95999_s0-2_lam0.1_save.json` and seeds 3–5 from `phase3_extra_tribe_gpt2_n95999_s3-5_lam0.1.json`.
- Text-feature saved students: seeds 0–5 from `phase3_combined_textfeat_gpt2_n95999_s0-5_lam0.1.json`.
- Verify the E016 claim that corresponding TRIBE/text-feature KD weights are byte-identical before treating KD as a shared baseline. Score each unique model once and retain aliases for exact duplicates.
- Verify every artifact against its saved metadata and record SHA-256 hashes for the model weights, run JSONs, ordered text list, target arrays, and analysis output.

### Scoring protocol

- Extract each unique saved student's hidden states once on the common ordered sentences, then reuse them for all participant targets.
- Layer 7 is the sole primary layer. Layer 6 is a predeclared mechanistic sensitivity because it was the E016 synthetic training layer. No best-layer selection.
- For every participant, layer, model arm, seed, and contiguous fold, run the established E003 variance partition: contextual features after sentence token length, normalized stimulus position, and fixed GPT-2-medium static-embedding nuisance, train-fold PCA/scaling only, five contiguous folds, capacity-fair rank **50**. Presentation duration, word rate, and phone rate are not variable/applicable for these visually presented isolated sentences.
- Run one predeclared expanded-nuisance sensitivity by adding the available Tuckute imageability column. A second, explicitly non-primary stress test adds the existing GPT-2XL and PCFG surprisal columns symmetrically to every arm; because surprisal overlaps the tested LM representation, collapse under this stress test is reported but cannot alone identify confounding or reverse the primary result.
- Fit nuisance regression, centering, PCA, ridge regularization, and every feature transform on each training fold only. Preserve the ordered five contiguous blocks; never shuffle sentences or tune a layer, nuisance set, rank, or participant subset from E025 outcomes.
- Retain raw fold values. Seeds are crossed technical realizations shared across participants, not biological replications; average seeds before participant inference and report seed-wise robustness separately.
- Save the extracted representation cache under gitignored `outputs/E025/` so E026 can measure representation movement without another model pass.

### Pre-scoring manipulation and language-quality gates

- Recompute held-out NLL and bits per byte directly from every distinct saved checkpoint on the exact 1,999-sentence WikiText-103 corpus, masking and truncating exactly as E016 did and dividing scored NLL bits by decoded UTF-8 bytes of the same scored token span. Retained per-token perplexity is a reproducibility cross-check, not the bpb estimator.
- Quality equivalence requires, within every seed, maximum absolute `delta-bpb <= 0.005` for TRIBE-MSE versus text-feature-MSE and for each target arm versus its byte-identical KD arm. If any pair fails, biological scores remain descriptive and cannot activate Package C.
- Before opening participant scores, require **target-directed learning** from the retained E016 held-out target-R2 records: all six target-minus-KD seed differences must be positive and their seed-mean two-sided t-CI95 lower bound must exceed zero, separately for TRIBE and text-feature. Then measure in-distribution WikiText representation movement from each seed-matched KD artifact. A target arm passes generic movement only if, in every seed, both centered relative Frobenius change exceeds `1e-4` and linear-CKA distance exceeds `max(1e-6, 10 * duplicate-extraction noise)`, where duplicate noise is measured by two deterministic extractions of the same seed-0 KD artifact with identical batching. If either target-direction or movement fails, label the manipulation failed; do not interpret its biological endpoint as evidence that the target has no value. Tuckute movement and layer-7 movement are reported as sensitivities; layer-6 WikiText movement is the gate.

### Estimands

Let `A(u,s,k,l,a)` be nuisance-subtracted unique R2 for participant `u`, seed `s`, fold `k`, layer `l`, and arm `a`.

- **Primary retrospective contrast:** `D(u,s,k) = [A(tribe_mse)-A(kd)] - [A(textfeat_mse)-A(kd)]` at layer 7. Once KD identity is verified this equals `A(tribe_mse)-A(textfeat_mse)`, but both gain terms remain explicit. This estimates transfer relative to the saved dimension-matched control, not biosignal specificity.
- **Participant estimand:** first average each participant-fold cell equally over six seeds, then average the five folds equally: `e_u = mean_k mean_s D(u,s,k)`. The population-facing estimate is `mean_u(e_u)` with participant as the sole population inference unit.
- **Block robustness:** `f_k = mean_{u,s} D(u,s,k)` preserves the five shared stimulus blocks for descriptive and leave-one-block-out robustness. The overlapping ridge-training sets make the five fold estimates dependent, so no fold t-CI or fold-population claim is made.
- **Seed robustness:** `g_s = mean_{u,k} D(u,s,k)`. Report all six; seeds do not increase the biological degrees of freedom.
- **Secondary:** TRIBE-minus-KD and text-feature-minus-KD, each paired by seed. The existing `[TRIBE MSE - TRIBE block-permuted] - [text-feature MSE - text-feature block-permuted]` is defective-control sensitivity only: E016's block permutation leaves 0--30% of rows in place and duplicated/omitted one row in five of six seeds, so it is neither a complete shuffle nor a phase-preserving shape twin.
- **Sensitivity only:** repeat the same contrasts at layer 6. It cannot rescue a layer-7 failure.

### Uncertainty and tests

- Participant mean with two-sided t-CI95 (`n=9`), one-sided 95% upper bound for SESOI exclusion, participant median, exact two-sided sign test, and Wilcoxon signed-rank where nonzero pairs permit it.
- Report the five block values and six seed values descriptively. Do not compute a fold t-CI or flatten participant-by-seed or participant-by-fold cells.
- Leave-one-participant-out and leave-one-block-out estimates.
- Separate valid train-participant and held-out-participant means.
- Spearman association between each participant's effect and that participant's KD-only alignment (the available SNR proxy), plus the estimate after dropping the highest-baseline participant. A positive effect that exists only in the highest-SNR brain is not participant-general transfer.
- Report all nine participant values and all five fold values, not only aggregates.

### Prospective power and MDE

E008's same nine-participant substrate had between-participant SD approximately `0.00062` unique-R2 for its participant aggregate. Using that external-to-E025 variance proxy, a two-sided one-sample t test with `n=9` has an approximate 80% MDE of `0.00065`, well below the `+0.002` SESOI. This is a planning calculation, not an assumption that E025 has the same variance. After scoring, report the exact one-sample noncentral-t power at `+0.002` and the observed-variance 80% MDE. If the observed MDE exceeds `+0.002`, classify failure to activate as power-limited unless the one-sided participant upper bound is already below `+0.002`.

### Predeclared activation and kill criteria

The minimally meaningful participant-general effect is `+0.002` unique-R2, inherited from E008's uniform-effect sensitivity target rather than chosen from E025 outcomes.

Package C may proceed only to E026's matched-control construction gate if, at layer 7, all of the following hold: the bpb, target-direction, and representation-movement gates pass; the primary participant t-CI95 lower bound exceeds the `+0.002` SESOI; at least 8/9 participants and all six seed aggregates are positive; every leave-one-participant-out and leave-one-block-out point estimate remains positive; the held-out-five mean is positive; TRIBE-minus-KD itself is positive; after dropping the highest-KD-alignment participant the primary mean remains at least `+0.002`; and under the imageability-expanded nuisance the participant mean remains at least `+0.002` with t-CI95 lower bound above zero. Layer 6 must not be the sole positive layer. Passing licenses a prospective matched-control design; it does not establish brain specificity.

Kill participant-positive Package C activation if any required condition fails, including a sub-SESOI lower bound, dependence on one participant/block, held-out-participant failure, a layer-6-only effect, quality mismatch, or failed manipulation. The only predeclared subgroup checks are the train-four and held-out-five partitions. A subgroup is "stable positive" only if its mean is at least `+0.002`, its own participant t-CI95 lower bound exceeds zero, and every within-subgroup leave-one-participant-out mean is positive. If the one-sided 95% full-cohort upper bound lies below `+0.002` and neither subgroup is stable positive, classify a practically meaningful positive as excluded for this cohort. If the interval overlaps `+0.002` while the observed MDE exceeds it, return power-limited. A quality or manipulation failure instead yields "uninformative for biological benefit." A killed positive branch remains informative evidence for Package A; it is not a universal claim that brain supervision can never help.

### Controls and boundaries

- Contiguous folds and fold-only PCA/scaling; no random stimulus splits.
- Fixed length, position, and static-embedding nuisance across arms.
- Same sentences, target ROIs, PCA ranks, seeds, and language-quality records across arms.
- The saved students were selected by the prior E016 program, not by E025 participant results.
- The inference generalizes only over these nine Tuckute participants and this sentence/ROI substrate. Participant inference does not imply new-stimulus, new-dataset, or mechanistic generalization.
- E025 does not establish brain-specific information even if positive; E026 and a matched-control E027 would still be required.

### Five-control battery status

1. **Phase-randomized shape twin: missing.** No such saved E016 student exists. The generic block-permuted arms do not fill this role, so E025 cannot support a target-shape-specific claim.
2. **Zeroed/shuffled privileged information: limited.** The saved block-permuted arms are reported with the documented permutation defect and are never load-bearing.
3. **Representation-move gate: required.** It is run before participant inference as specified above.
4. **Matched bpb, per participant, crossed participants by blocks: required.** All are load-bearing.
5. **Optimization/geometry-matched nonbrain teacher: missing.** Text-feature is dimension-matched only. E026 audits the mismatch; only a prospective E027 could test a fixed control.

## Compute and stop rule

No retraining. Process 30 expected unique GPT-2 students (six shared KD, 12 TRIBE target/control, 12 text-feature target/control), two fixed layers, nine participant targets, and five folds. Extract representations once, run artifact/bpb/target-direction/movement gates, then score the fixed biological endpoint. Stop before inference if artifact identity, the complete seed/arm grid, text ordering, ROI completeness, quality equivalence, manipulation, or fold-only preprocessing fails; failed quality/manipulation gates may still receive clearly labeled descriptive scores for Package A. A manifest-only smoke must validate all run JSONs, the exact arm/seed grid, artifact readability, hashes, UID/ROI completeness, text identity, and planned cache keys without loading model weights or computing scores. It cannot enter the result.

## Precheck

`anti-confound-designer` assembly and two independent code/design reviews completed on 2026-07-16. The first oracle returned HOLD because the metadata manifest was not yet execution-binding. After binding every scientific argument and source hash, rejecting stale representation/nuisance caches, binding the analyzer to the exact manifest/extraction/grid, freezing the canonical-scorer hash, suppressing inference on gate failure, and validating target-cache headers/text identity, the final oracle verdict was **PASS**.

- `READY-TO-RUN: YES`
- Frozen metadata-only manifest SHA-256: `2729c0c97b2f845ccf8f58a13e01ecf87f44029564ca615269230437de46698d`
- Runner SHA-256: `2357bae93d80457d7971c1ed368a30b15da6341171cb30036f3d2e2b360f1b1f`
- Analyzer SHA-256: `c529f670df1eb142be03d5e07572f128ed925b5ba10eab2b8ce92da6d17730be`
- Canonical scorer SHA-256: `1fd971c07028c27c89225c3b997fb536f31fb62bd288c4442ca1abb13598ba02`
- Optimized-versus-canonical scorer maximum absolute error: `8.85e-17` (tolerance `1e-10`).
- Manifest smoke: 36 logical aliases, 30 unique checkpoints, six byte-identical shared-KD pairs, nine complete participant units, one frozen GPT-2 runtime, hidden size 768, and matching TRIBE/text-feature target-cache row/text identities. No model weights were loaded and no E025 biological endpoint was computed during precheck.

## Results

`\gap` — not run.

## Related

- [Project status](../status.md)
- [Methodology](../03-methodology.md)
- [Conference-package decision](../decisions/decisions.md)
