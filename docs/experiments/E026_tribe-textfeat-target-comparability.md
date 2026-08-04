---
title: "Experiment — E026: TRIBE versus text-feature target comparability"
tags: [experiment]
aliases: [E026]
---

# Experiment — E026: TRIBE versus text-feature target comparability

**Created:** 2026-07-16 · **Status:** COMPLETE — exact-manifest run and independent result audit PASS; saved text-feature comparator fails the corrected identification set; original 55-state engineering audit retained for provenance · **Mode:** working
**Direction:** Retrospective mechanism audit for Package A in [D057](../decisions/decisions.md). E025 did not satisfy its participant-positive `+0.002` activation prerequisite, so E027 construction is not licensed; E026 remains useful for identifying why the E016 proxy endpoints differed.
**Predecessor:** [E016](E016_tribe-synthetic-brain-targets.md), especially the Step 70 scope correction that the existing text-feature target is dimension-matched but not demonstrated information-, geometry-, or learnability-matched.

---

## Objective

Run a predeclared equivalence audit: determine whether the existing E016 TRIBE and text-feature auxiliary targets are equivalent on measurable nonbiological properties that can change training. E026 does not estimate biological transfer, target coordinates are features rather than replication units, and the audit cannot reactivate E027 after E025's failed prerequisite.

## Competing explanations

- **Target-specific content:** after accounting for geometry, scale, headroom, and learnability, TRIBE causes more student movement and target-specific learning than a non-brain target.
- **Headroom/geometry confound:** the large TRIBE synthetic gain and tiny text-feature gain follow from different intrinsic rank, covariance spectrum, baseline predictability, or optimization scale.
- **Control non-identifiability:** no available non-brain construction can match the properties required for a fair E027 without importing the same brain-derived mapping.

## Design lock candidate (must pass `/precheck` before computing new audit outcomes)

### Fixed sources

- TRIBE train/held-out caches: `outputs/E016_tribe/kd_targets/text/train_start0_n95999_full.npz` and `heldout_start0_n1999_full.npz`.
- Text-feature train/held-out caches: `outputs/E016_tribe/kd_targets/text_feature/gpt2-medium/train_start0_n95999_d20484_full.npz` and `heldout_start0_n1999_d20484_full.npz`.
- E016 six-seed run JSONs for target R2, final losses, perplexity, and artifact identities.
- E025's fixed layer-6/layer-7 representation caches for paired representation-movement analysis: WikiText heldout is primary and Tuckute sentences are an out-of-domain sensitivity. E026 revalidates the extraction index, base manifest, all 30 representation caches, ordered texts, aliases, weights, and runtime identities. Invalid or unavailable caches make movement unresolved rather than triggering a substitute stimulus or layer.

### Split, nuisance, and no-endpoint-feedback rules

- The 95,999 training and 1,999 untouched held-out WikiText sentences are the target-audit substrate. Preserve canonical item order and recorded document/context metadata. Tuckute participant outcomes may not be loaded or consulted; outcome-free Tuckute representations are sensitivity inputs only.
- For target predictability, use token length under the GPT-2 tokenizer shared by GPT-2-family models, normalized within-corpus position, nine reference-coded contiguous-decile indicators, and attention-mask-mean frozen GPT-2-medium input embeddings. The local GPT-2-medium snapshot contains the model weights/config but no tokenizer files, so the manifest separately resolves and hashes the local `gpt2-medium` model snapshot and local `gpt2` tokenizer snapshot; geometry loads only those exact snapshots. Imageability, presentation duration/rate, and phone rate are unavailable or inapplicable for arbitrary WikiText sentences and are N/A rather than imputed.
- Target geometry is computed on two frozen item samples. Sample A is the 4,096 canonical row IDs with smallest unsigned BLAKE2b-64 hash under key `E026-A-20260716`; sample B uses key `E026-B-20260716` and excludes A. Save both sorted index arrays and SHA-256 hashes before loading target values. Student/target learnability uses the already frozen E016 train/held-out split. No target dimension, layer, sample, tolerance, or diagnostic can be selected using Tuckute results.
- Every evidence-producing stage must revalidate the frozen script and E-record hashes, `pyproject.toml`/`uv.lock` numerical environment, selected execution device, all four target-cache and sidecar SHA-256 values, the exact load-bearing generator semantics in those sidecars, all three run JSONs, every distinct model weight and artifact manifest, deterministically recomputed row and coordinate samples, context metadata, and the complete E025 extraction chain. Row chunk `512`, static-embedding batch size `64`, and target-coordinate chunk `128` are design-locked. Mutable derived target/static arrays are never trusted: every invocation regenerates them from the full-hash-validated NPZ or frozen model/text inputs and records the derived hashes for audit. `--skip-full-cache-sha256` creates a smoke manifest only and cannot authorize geometry.

### Analyses

1. **Provenance and parity:** verify identical item indices/text hashes, target dimension, train/held-out counts, training budget, seeds, lambda, and standardization implementation. Hash every target, run, model, representation, and metadata dependency. Record that textfeat is a fixed projection of a 1,024-dimensional source and therefore has centered algebraic rank at most 1,024; TRIBE receives only the fixed-sample centered cap 4,095 because its generator is nonlinear.
2. **Raw scale:** full-cache per-dimension mean and standard-deviation quantiles, near-constant dimensions, item-norm distribution, and train-to-held-out shift. Also analyze the E016-formula training-standardized targets because raw scale was normalized before the auxiliary loss.
3. **Standardization, covariance spectrum, and rank:** reconstruct E016's formula `(Y - population mean)/(population SD + 1e-6)` with float64 streaming moments and float32 application; the reconstructed denominator minimum and maximum must reproduce every retained E016 run summary within relative tolerance `1e-5`. For each 4,096-row sample, record pre-centering global scale, then sample-center columns before covariance SVD. Repeat raw-centered geometry as sensitivity. Use the same Gaussian sketch for both families: seed `20260716`, top 512, oversampling 64, four power iterations, QR after every multiply, TF32 disabled, and float64 reductions. Synthetic exact-SVD, repeat-determinism, normalized-scale-invariance, orthogonality, monotonicity, and captured-energy checks are mandatory stop gates. Report trace-normalized covariance eigenvalues, sample stable rank, and captured mass at 1, 8, 32, 128, and 512. Conditional top-512 entropy rank and concentrated/uniform tail allocations are descriptive only: randomized Ritz values do not license rigorous full-spectrum bounds.
4. **Descriptive intrinsic dimension and order structure:** compute 2NN dimension on unwhitened PCA scores at ranks 32, 64, 128, 256, and 512, with duplicate diagnostics and right-censoring at `rank/2`. It is descriptive and never conjunctive. For canonical-order structure, never infer adjacency from the hash samples: within recorded document/context boundaries, stream the full cache to report trace autocorrelation at lags 1, 2, 4, 8, ..., 1024, normalized trace power, spectral entropy, fixed-band mass, and per-feature lag quantiles on two fixed, disjoint 256-coordinate hash samples. If the cache metadata cannot recover valid boundaries, order-shape comparability is unresolved rather than computed across artificial joins.
5. **Baseline/head and nuisance learnability:** summarize the six paired KD-only target-R2 values, corresponding target and defective block-permuted arms, raw improvement, remaining headroom `1-R2_KD`, and headroom-normalized improvement. Raw paired delta-R2 is primary; suppress headroom ratios when either mean remaining headroom is below `0.05`. On both fixed 256-coordinate samples, fit two nuisance tiers: low-level-only, then low-level plus rank-50 train-fit PCA of frozen static embeddings. Select one ridge alpha from `[0.1,1,10,100,1000]` by aggregate static-augmented R2 over both families and both coordinate samples in five contiguous inner validation folds. Fit every predictor transform on each fold's training complement; apply the chosen alpha once to the untouched heldout split. Report variance-weighted aggregate SSE/SST R2, static-unique delta-R2, and target-coordinate chunks of 128. Coordinates receive no p-values or confidence intervals.
6. **Loss and initial-gradient scale:** summarize retained final auxiliary losses only as last-minibatch diagnostics. Initial gradient norms were not retained, so retrospective initial-gradient comparability is **unknown** and blocks any claim that E016 was optimization matched; it does not invalidate the other audit components. Any prospective E027 control must pass a no-update calibration measuring standardized auxiliary loss and gradient norm at each common seed-matched KD initialization.
7. **Post-training manipulation diagnostics:** for each seed, compute float64 relative parameter-update norms from the byte-identical final KD student to each target and block-permuted student, globally and by embeddings, attention, MLP, normalization, output, and other blocks. For each seed, arm, corpus, and layer, compute float64 centered linear-CKA distance, centered activation-RMS change, and centered relative Frobenius change from KD. These outcomes describe how the interventions changed the students; they are not comparator-identification conditions. The load-bearing representation comparison is MSE-arm WikiText-heldout layer 6; WikiText layer 7, both Tuckute layers, and block-permuted arms are sensitivities. E016's retained fresh-head target-R2 is the only target-prediction-change measure; E025 has no training representations from which to fit new layer-specific heads. Report all paired seed values, t-CI95, and the exact `2^6` magnitude-preserving sign-flip test, whose identifying assumption is exchangeability of paired seed contrasts under independent sign reversal under the sharp null.

### Fixed equivalence margins

The existing text-feature target is classified as comparable on the measured pretraining axes only if **every required** load-bearing margin holds on both fixed samples or untouched held-out summaries:

| Diagnostic | Equivalence margin |
|---|---|
| ambient dimension, item identity/order, standardization, train/held-out counts | exact equality |
| standardized global mean and SD | absolute mean difference `<=0.01`; SD ratio in `[0.99, 1.01]` |
| normalized top-512 covariance spectrum | root-mean-square log difference of trace-normalized covariance eigenvalues `<=0.10`, with values below `1e-8` of the leading value excluded and counted |
| sample stable rank | absolute log-ratio `<=0.10` on A and B; entropy diagnostics are descriptive and nonconjunctive |
| variance mass at components 1, 8, 32, 128, 512 | absolute difference `<=0.02` at every cut |
| valid within-boundary autocorrelation and binned power spectrum | autocorrelation difference `<=0.05` at every fixed lag; Jensen-Shannon divergence `<=0.05` |
| six-seed KD held-out target R2 and remaining headroom | absolute paired-mean R2 difference `<=0.02`; ratio of mean remaining headroom in `[0.90, 1.10]` |
| low-level-only and static-unique held-out target R2 | absolute difference `<=0.02` for each, on both coordinate samples |
| initial standardized auxiliary loss and gradient norm | retrospective status `unknown`; prospective E027 requires absolute standardized loss difference `<=0.05` and absolute log gradient-norm ratio `<=0.10` in every seed |
| post-training global parameter update | descriptive engineering margin only; not part of the identification conjunction |
| post-training layer-6 CKA distance and centered-relative-Frobenius movement from KD | descriptive engineering margins only; not part of the identification conjunction |

The 2NN and entropy-tail estimates are descriptive and absent from the conjunction. These tolerances are engineering margins, not formal equivalence tests or claims of information equivalence. Deterministic targets have no repeated-measure reliability estimate. Ratios are never used below their stated floors. Mechanical logic is three-state: any observed required failure yields `FAIL`; `PASS` requires every required component; missing components yield `UNRESOLVED`. The runner emits this arithmetic classification but never adjudicates a scientific verdict.

### Estimands, uncertainty, and identifying assumptions

- **Retrospective identification check:** target construction, geometry, nuisance predictability, and KD-baseline recoverability and headroom. Initial-gradient comparability remains separately unknown. **Post-training diagnostic check:** whether already-trained MSE students differ in parameter and representation movement on heldout WikiText. These realized outcomes may help explain how the interventions differed, but they do not determine comparator validity.
- Seeds (`n=6`) are technical training realizations and the only randomization unit for trained-model learnability and movement contrasts; report mean, descriptive t-CI95, all seed values, and the exact sign-flip test under its sign-exchangeability assumption. This does not license population inference beyond the frozen training procedure. Target-cache geometry is deterministic; report both fixed samples separately and do not create pseudo-replicated p-values or confidence intervals over dimensions.
- Identifying assumption: if targets differ materially on properties fixed before target-arm outcomes are interpreted, including baseline predictability, remaining headroom, effective dimension, covariance spectrum, nuisance predictability, or initial optimization scale, the between-target contrast cannot isolate target content. Passing comparability is necessary, not sufficient, for brain specificity. Realized movement is a diagnostic outcome, not a matching condition.

### Decision and kill criteria

- **Existing control mechanically non-comparable** if any required measured margin fails. If every measured axis passes, classify it "measured-axis comparable, initial-gradient comparability unresolved," never fully matched. If a required component is absent, classify it unresolved unless another observed margin already fails. E016 remains a within-target learnability result and the raw TRIBE-versus-text-feature gain cannot support brain specificity.
- **No prospective construction is licensed:** E025 did not pass its participant-positive prerequisite. The rules below survive only as a boundary for a hypothetical future reopened program, not as authorization for E027.
- **Kill E027** if matching requires post-outcome adjustment, cannot achieve the frozen pre-outcome tolerances or initial-gradient calibration, or copies item-wise TRIBE coordinates or the brain-derived readout. Post-training movement should be monitored as a diagnostic rather than used as a comparator gate. Do not launch a broad control sweep.
- Regardless of outcome, E026 cannot prove that TRIBE contains unique biological information; it only determines whether the existing comparison is identifiable and records the requirements a later control would have to satisfy.

### Candidate family for a later design, not an active construction

The previously considered family was a text-only target built from the same frozen Llama text representation that enters text-only TRIBE, followed by a seeded nonbrain projection and training-only whitening/coloring. It would be an **optimization/geometry-matched text-only control**, not matched-information. E026 constructs nothing. Because E025 did not activate E027, this paragraph records the non-leakage boundary only: any future reconsideration would require a new E-record and must freeze checkpoint/layer/pooling, projection distribution and seed, whitening/coloring, target rank, calibration grid, selection rule, and margins without item-wise TRIBE coordinates, brain-readout weights/rotations, or Tuckute feedback.

### Five-control battery status

1. **Phase-randomized shape twin:** central to a future training comparison, but no such saved student exists. E026 specifies that a candidate must preserve marginal scale, covariance spectrum, and order/power structure while removing stimulus content; a generic row permutation is not accepted.
2. **Zeroed/shuffled privileged information:** the defective saved E016 block permutation is described but not treated as the shape twin. A correct shuffled/zero channel is mandatory if E027 trains students.
3. **Representation-move gate:** N/A for target-only geometry; mandatory and measured for the already trained E016 students and any E027 student.
4. **Matched bpb/per participant/crossed inference:** bpb and biological inference are N/A for target-only diagnostics; they become mandatory downstream. Existing E016 student bpb is audited in E025.
5. **Optimization/geometry-matched nonbrain teacher:** closed because E025 did not activate E027. Any future reconsideration requires a new design and must freeze the teacher without biological-endpoint feedback before pretraining and one-shot movement gates.

## Compute and stop rule

No student training and no candidate construction. Before target values, `--stage selftest` must pass and `--stage manifest` must freeze full hashes, samples, margins, source parity, generator semantics/rank caps, exact model and tokenizer snapshots, exact execution chunks, the no-derived-cache-reuse policy, and valid E025 caches. The manifest must then receive an independent exact-hash review. `--stage all` consumes that reviewed manifest and never creates or overwrites it; evidence-stage output is rejected if its canonical path aliases the manifest. It may then read the full caches, run the two spectrum samples, regenerate frozen static nuisance features, summarize existing six-seed records, and consume E025 representations. Stop on provenance, text-order, standardization-extrema, item-position, or SVD-validation failure. Missing valid document boundaries makes only order structure unresolved; missing valid E025 caches makes only representation movement unresolved. Heavy derived arrays remain gitignored under `outputs/E026/`; only load-bearing summaries receive hashes in this record.

## Precheck

The first hostile DESIGN review returned **HOLD / READY-TO-RUN: NO** for an incorrect `ddof=1` reconstruction, uncentered and unnormalized spectrum, uncertified entropy-bound language, absent SVD failure gates, missing nuisance learnability, a sign test mislabeled as sign-flip, uncentered movement, incomplete equivalence arithmetic, and a non-frozen execution manifest. A second independent code audit retained **HOLD** because same-shape mutable derived arrays could be reused, row/static chunking was not frozen, `--stage all` could rebuild its own manifest, generator-sidecar semantics were not asserted, and E025 duplicate-noise fields silently defaulted to zero. Smoke preflight then found that the local GPT-2-medium model snapshot lacked tokenizer files, and focused review found that an output-path alias could still overwrite the reviewed manifest. The implementation and design now prohibit all derived-cache reuse, test same-shape tamper recovery, lock all execution chunks, validate exact generator fields and finite nonnegative duplicate-noise measurements, freeze separate model/tokenizer snapshots, make `all` consume-only, and reject manifest/output path aliasing. The focused preliminary oracle then returned **DESIGN PASS / READY-TO-FREEZE-MANIFEST: YES** on script `c1e5bf0f…` and the pre-status-update record `8fcb74cf…`, with 13/13 synthetic tests and real model/tokenizer/static-feature smoke checks passing.

The final full manifest received an independent exact-hash **DESIGN PASS / READY-TO-RUN: YES** on the immutable triple: runner `c1e5bf0faf4a1fe942e7c0e5062279db388d0fa475157ba79d1bd440debd88ce`, pre-result E-record `9d422f8ddfc1de81f44ecc4f4afc94218284097c9eb0a1d139d4db3f22ece3fa`, and manifest `a2bbf93f839b8e787716e325b198062e159dd7089e5725249647d806f425ad1f`. The pre-result runner and E-record remain recoverable exactly at Git commit `5b2a251`; the current E-record necessarily changes when this result is appended. The manifest verifies four full target caches, the exact 36-row seed/arm grid and 30 distinct weights, the complete E025 extraction chain, separate frozen GPT-2-medium model and GPT-2 tokenizer snapshots, row and coordinate samples, generator semantics, execution chunks, and all parity and integrity gates.

## Results

### Execution and provenance

The authorized evidence command was:

```bash
CUDA_VISIBLE_DEVICES=3 uv run python scripts/e026_audit_target_comparability.py --stage all --device cuda --manifest-in outputs/E026/e026_manifest.json --out outputs/E026/e026_audit.json --keep-extracted
```

It consumed the reviewed manifest without modifying it, passed all stop gates, and produced `outputs/E026/e026_audit.json` with SHA-256 `dfac7498d89d488483f129ebd30f36013d98778a8304f0d3d97d9e0a8c1932ad`. The frozen runner, pre-result record, and manifest hashes remained unchanged.

An independent checker, `scripts/e026_independent_result_audit.py` (SHA-256 `cf701aa8bab3016701ac7a6575ea58c36d9153ae048dae5e4fb3dd6580635f26`), does not import the main runner. It reconstructed all 35 geometry and 20 trained-model check states from lower-level fields, verified the reported summaries and conjunctions, and rehashed 128 bound dependencies totaling 34,958,676,977 bytes. Its retained output, `outputs/E026/e026_independent_result_audit.json` (SHA-256 `b2dca54c87efeca60c78a0de8287b4571991dcf3e653ce17dacc60583d2fda9f`), returned **PASS**, zero arithmetic mismatches, and zero dependency-hash failures.

### Mechanical outcome

The frozen engineering conjunction is **FAIL / `AT_LEAST_ONE_MEASURED_AXIS_FAILS`**: 30 of 55 checks fail, 24 pass, and one is unresolved. Geometry contributes 14 failures, 20 passes, and the single unresolved lag; trained-model checks contribute 16 failures and four passes. This arithmetic is a measured-axis classification, not a population-equivalence test or scientific verdict by itself.

The load-bearing failures are large and reproduce across the two fixed samples or all six seeds:

- **Baseline difficulty and headroom:** mean KD-only target $R^2$ is `0.595327` for TRIBE and `0.911687` for textfeat, an absolute paired-mean gap of `0.316360` against margin `0.02`. The mean remaining-headroom ratio is `4.582` against permitted interval `[0.90,1.10]`. TRIBE target training gains `+0.078298` (descriptive CI95 `[+0.077198,+0.079398]`), whereas textfeat gains `+0.000903` (`[+0.000649,+0.001157]`).
- **Covariance geometry:** normalized top-512 spectrum log-RMS differences are `5.524` and `5.535` against margin `0.10`. TRIBE versus textfeat sample stable ranks are `2.657587` versus `1.410062` and `2.636620` versus `1.423594`, giving absolute log-ratios `0.634` and `0.616` against margin `0.10`. Cumulative variance-mass differences fail at components 1, 8, 32, and 128 on both samples and pass at 512; PC1 alone carries approximately `0.376/0.379` of TRIBE variance versus `0.709/0.702` for textfeat.
- **Nuisance predictability:** low-level-only held-out $R^2$ is `0.233/0.217` for TRIBE versus `0.425/0.399` for textfeat, giving gaps `0.192/0.183` against margin `0.02`. Static-unique delta-$R^2$ gaps are `0.0077/0.0126` and pass. The frozen ridge selection chose alpha `1000`, the upper edge of its candidate grid, which is retained as a caveat rather than retuned.
- **Parameter movement:** mean global relative displacement from the common KD checkpoints is `0.017222` for TRIBE and `0.014223` for textfeat. The paired mean difference is `+0.002999`, and every seed's absolute log-ratio (`0.148`--`0.210`) exceeds margin `0.10`; the descriptive sign-flip value is `p=0.03125`.
- **Representation movement:** on primary WikiText-heldout layer 6, centered relative-Frobenius movement is `0.215076` for TRIBE and `0.134836` for textfeat. The paired difference is `+0.080240`, descriptive CI95 `[+0.070328,+0.090151]`, with every seed's absolute log-ratio (`0.300`--`0.612`) exceeding margin `0.10`. Centered-CKA distance is not directionally different overall: four of six seed margins pass, paired mean difference `-0.000299`, sign-flip `p=0.78125`. Any statement that TRIBE “moves more” is therefore metric-specific.

Important passes prevent a blanket non-parity claim. Training-standardized global mean and scale pass on both samples, autocorrelation differences pass every lag with valid pairs through 512, both power-spectrum Jensen--Shannon checks pass, static-unique nuisance predictability passes, and four CKA-distance checks pass. Lag 1024 is **UNRESOLVED** because no valid within-document pairs exist. Initial standardized auxiliary-loss and gradient comparability is **UNKNOWN** because those quantities were not retained.

### Scientific adjudication

The saved projected text-feature arm is **non-comparable on the frozen measured pretraining and trained-movement axes**. E016 therefore remains valid as a within-TRIBE target-learnability result, but its larger TRIBE-versus-textfeat synthetic gain cannot isolate brain-derived content. The most plausible recorded mechanism hypothesis is same-teacher redundancy: textfeat is a Gaussian projection of the GPT-2-medium teacher representation already used for KD, consistent with its `0.912` KD baseline and little remaining headroom. E026 does not establish that this redundancy, covariance geometry, or any other measured mismatch caused the gain.

E026 also does not establish information inequivalence, show that TRIBE contains unique biological information, explain E025's transfer failure, or generalize beyond the frozen E016 targets and students. E025's direct TRIBE-minus-KD biological contrast remains the cleaner endpoint result and is near zero. E027 remains unauthorized because E025 failed its prospective participant-positive activation gate; the audit cannot reopen it retrospectively.

**Publication consequence:** the internally defensible finding is a dissociation among target learnability, retained-student movement, control identifiability, and participant-general biological transfer. The first two pass, the saved control fails identification, and the participant transfer gate fails for the tested cohort. Package A is strengthened as a methodological/falsification case; Package B remains HOLD because no prospective directional certificate exists; Package C remains closed. E028 is the binding prospective external gate.

## Identification correction (2026-08-04) — pre-treatment comparability and post-training diagnostics

The frozen 55-check engineering audit mixed two roles that must remain separate for scientific identification.  Target geometry, scale, covariance, effective rank, nuisance predictability, baseline recoverability, remaining headroom, shared training conditions, and initial loss or gradient scale are pre-treatment properties of the comparison.  Parameter displacement, target uptake, centered relative-Frobenius movement, and CKA distance are realized post-training outcomes or mediators.  Requiring the latter quantities to match can remove a genuine target-content effect by definition.  They therefore remain useful dose and mechanism diagnostics but no longer determine comparator identification.

The original `30/55` arithmetic remains a correct description of the frozen engineering audit and is retained for provenance.  It is not a count of independent scientific identification conditions and must not be used as the reason the comparator is non-identifying.  The scientific disposition is unchanged because the saved text-derived target already fails several pre-treatment comparisons, including KD-only baseline recovery and remaining headroom, covariance geometry and effective rank, and low-level nuisance predictability; initial gradient comparability is also unresolved.  These failures are sufficient to prevent the raw TRIBE-versus-text-derived difference from isolating brain-response content.

Reclassifying the frozen states gives 37 identification checks: 20 pass, 16 fail, and one is unresolved. The remaining 18 states are post-training diagnostics: 14 fall outside the original engineering margins and four fall within them. The superseded `30/55` count remains an arithmetic description of the original combined audit only.

The corrected adjudication is: **the saved text-derived auxiliary-control arm is non-identifying because it is not matched on the measured pre-treatment target and optimization conditions; post-training movement differences diagnose unequal realized interventions but do not themselves determine identification**.  E025's direct synthetic-response-minus-KD biological-transfer contrast remains interpretable as the total effect of adding the tested synthetic-response objective.  The text-derived comparator is required only to attribute a difference specifically to brain-response content.

## Related

- [Project status](../status.md)
- [Methodology](../03-methodology.md)
- [Conference-package decision](../decisions/decisions.md)
