---
title: "Claim-Led Manuscript Rewrite Contract"
tags: [manuscript, rewrite, question-led-writing]
aliases: [rewrite-contract]
---

# Claim-Led Manuscript Rewrite Contract

## Status and authority

This directory is a from-scratch, claim-led manuscript candidate requested by Erfan on 2026-07-23. It may use the same settled evidence as the extended manuscript, but it must not copy the extended manuscript's chronology or silently change an E-record verdict.

The current scientific authority remains [`../extended/`](../extended/) until Erfan explicitly approves replacing it. The candidate must therefore remain independently buildable, and work here must not modify files under `../extended/`.

## Reader, governing question, and answer

**Intended reader.** An ML/NLP reviewer or thesis examiner who understands basic machine learning and statistical evaluation but does not know fMRI encoding, this project's datasets, targets, controls, inference units, or experiment history.

**Governing question.** Under what conditions can recorded fMRI responses or synthetic brain responses generated from text provide a reliable, brain-specific training advantage to a compressed language model, and where does the tested evidence chain first fail?

**Provisional answer.** Trained language-model representations contain information useful for predicting held-out recorded fMRI responses beyond the specified controls. The tested distilled student is less brain-predictive than its teacher, although language-model quality remains a competing explanation. The tested recorded-response objectives do not demonstrate a reliable participant-level benefit. Synthetic brain responses generated from text are learnable and change retained student representations without unacceptable language-quality loss, but incremental retention remains unresolved, the saved text-derived comparator cannot identify brain-response content, the direct participant-level contrast on recorded fMRI responses is near zero, and the exact target does not pass the prespecified practical linear-measurability rule. The evidence supports a failure-localization and evaluation framework, not a successful brain-response-guided distillation method.

**Scope.** The answer is limited to the tested models, English stimuli, datasets, participants, targets, objectives, optimization regimes, nuisance and intervention controls, linear readouts, comparators, inference units, and endpoints.

## Structural rules

- Organize the argument by claims and evidence gates, not experiment order.
- Keep E identifiers as `\evd{Ennn}` provenance markers and appendix navigation, not reader-facing vocabulary.
- Use formal academic prose: state the claim or procedure directly, and remove meta-commentary about framing or writing unless that framing is itself the claim.
- A subsection normally owns three to five related paragraph questions. A two-paragraph subsection is allowed only when it marks a real conceptual boundary. Merge a one-paragraph subsection into its parent.
- Split a subsection if it exceeds about 1,000 to 1,200 words, contains more than six or seven substantive paragraphs, or answers more than one parent question.
- Main-text theory must change the interpretation of an estimand or control. Put non-decisive derivations and analogies in Appendix D.
- Introduce each concept once, operationalize it once, and report its result once. Later sections should synthesize rather than restate.
- Do not present reserved, unexecuted, or precondition-stopped experiments as results.
- Use tables for experiment disposition, many-to-many evidence mappings, and repeated variant results.

## Attention budget

Target 9,000 to 10,000 main-text words, or roughly 21 to 23 A4 pages excluding references: about 2 pages for the Introduction, 3 for Section 2, 4 to 4.5 for Section 3, 7 to 8 for Results, 2.5 for Discussion, 1 to 1.5 for Limitations, and 0.5 for the Conclusion. Keep Section 2.3 within about 700 to 900 words and Sections 4.3 and 4.5 within about 1,000 to 1,200 words each. Preserve Results as the largest allocation.

Treat roughly 20 to 24 appendix pages as a planning band, not a compression target. Completeness means that every experiment and load-bearing claim is accounted for, not that every stored numerical row or machine-level artifact listing is reproduced. Leave exhaustive grids and artifact metadata in the owning E records and retained artifacts.

Give the three evidence-chain artifacts different jobs. The Section 2 figure defines the conceptual stages and claim meanings. The Section 3 table maps each stage to its estimand, comparator, experiment family, endpoint, inference unit, and E owner. The Results table reports only the verdict and strongest evidence. Do not restate the full chain in the prose around all three.

## Stable terminology

| Term | Meaning |
|---|---|
| Brain activity or brain responses | The general biological phenomenon. Avoid unqualified *neural* when it could refer to either the brain or a neural network. |
| Recorded fMRI responses | The actual biological measurements used in this work. fMRI does not directly record neuronal firing. |
| Model representations or model activations | Internal quantities of a language model or other neural network. |
| Brain alignment | Held-out predictivity of recorded responses from model representations under a declared readout and controls. |
| Controlled brain predictivity | Brain alignment after the specified nuisance, split, and control-model checks. |
| Recorded brain-response target | A recorded fMRI response when its role as a training target must be explicit. Otherwise write *recorded fMRI response*. |
| Synthetic brain responses generated from text | TRIBE outputs used in this work. Write *synthetic brain-response target* only when their role in a training objective must be explicit. |
| Target uptake | Recoverability of the optimized target from retained student representations by a fresh post-training readout. |
| Retained-student movement | Parameter or representation change that remains after the temporary training head is discarded. |
| Exact-target measurability | Whether the exact training target adds controlled, practically relevant predictivity of recorded responses on the intended biological substrate under the frozen assay. |
| Comparator validity | Whether a text-derived auxiliary target permits attribution to brain-response content rather than geometry, scale, learnability, or optimization pressure. |
| Biological transfer | Improvement on independently recorded responses that were not optimized as the training endpoint. |
| Brain-specific advantage | Incremental benefit beyond an appropriate text-derived or permuted control, at comparable language-model quality and the correct biological inference unit. Reserve this term for identified contrasts. |

Use the acronym definitions in `acronyms.tex`; never define the same acronym manually in prose. Use one term per concept unless the table above marks an intentional distinction.

## Complete main-text question tree

Every prose paragraph must answer one leaf question below. A paragraph may answer two adjacent leaves only when separating them would create two fragments and their evidence owners are compatible.

### Abstract

**Question.** What was tested, what evidence standard was used, where did the chain pass or fail, and what scoped conclusion follows?

One paragraph, in this order:

1. Why is using brain responses to train a smaller model different from measuring brain alignment?
2. What counted as a reliable, brain-specific advantage?
3. Which recorded-fMRI-response and synthetic-brain-response training branches were tested?
4. Which measurement and manipulation checks passed?
5. Where did attribution or participant-level transfer fail?
6. What does the result establish, and what does it leave open?

Use at most one or two estimates if they are necessary to distinguish a passed manipulation check from a failed endpoint. Do not turn the abstract into a numerical ledger.

### 1. Introduction

**Section question.** Why is measurable brain alignment a plausible but insufficient basis for training a smaller model with brain responses, and what exact claim does this study test?

No subsections. Seven paragraphs:

1. Why might brain responses select among language-compatible model representations in a smaller model?
2. What is brain alignment operationally, and which parts of that definition are assay-dependent?
3. Why does a positive brain-alignment score not establish that brain responses can help train a smaller model, a brain-specific advantage, biological transfer, or utility?
4. What remains unresolved after prior encoding, brain-response-guided optimization, privileged-information, and compression work?
5. Which ordered evidence gates would justify a brain-specific training advantage at comparable language-model quality?
6. What scoped answer does this study provide, and where is support lost or unresolved?
7. What three contributions does the study make, and what limits the conclusion?

The three contributions are controlled measurement with quality-aware interpretation, participant-level tests of training with recorded fMRI responses, and localization of the synthetic brain-response training branch across uptake, movement, comparator validity, exact-target measurability, and biological transfer. Do not use internal rung names, experiment history, or E identifiers here.

### 2. From a Brain Score to a Valid Training Claim

**Section question.** What must be true before training with brain responses can be credited with a brain-specific advantage?

Open with one bridge paragraph: Which links in the measurement-to-intervention chain have prior fields studied, and why must they be connected rather than treated as interchangeable?

#### 2.1 What does controlled brain predictivity establish?

1. How does held-out encoding test whether frozen model representations contain information useful for predicting recorded responses, and what does a positive score establish?
2. Why are nuisance features, architecture-matched untrained-model controls, and contiguous splits required for controlled brain predictivity?
3. Which properties of the assay bound the resulting claim, and why does controlled brain predictivity not establish a shared biological mechanism or causal equivalence?

This subsection owns the conceptual interpretation: what the score licenses, why the controls are necessary, and why the claim remains assay-bounded. Name the readout class, response construction and aggregation, participants, stimulus distribution, response reliability, region selection, and inference unit as bounding properties, but leave their dataset-specific implementation and formulas to Sections 3.1, 3.3, and 3.4 and Appendices B and D.

#### 2.2 Why might a brain-response target help a student, and why might it not?

1. Why can ordinary knowledge distillation preserve output behavior while leaving multiple possible internal model representations?
2. How can recorded fMRI responses or synthetic brain responses generated from text act as training-only targets that select among those representations, and what information can a deterministic synthetic target provide?
3. Why do target predictability, reduced target loss, and retained-student movement show only that the intervention operated, rather than that it produced a brain-specific training advantage?

This subsection owns the conceptual mechanism and its limits: output objectives do not identify internal geometry; training-only targets may select among compatible representations; and manipulation evidence does not identify brain-specific benefit. A deterministic target cannot convey row-specific information independent of the stimulus and fixed generator, although it may convey generator-learned structure and reorganize what the student makes accessible. Leave exact target construction to Section 3.1 and Appendix B, loss and gradient paths to Section 3.2 and Appendix C, the full evidence standard to Section 2.4, formal information-theoretic arguments to Appendix D.4, and empirical verdicts to Sections 4.4--4.5.

#### 2.3 What does prior brain-response-guided training leave unresolved?

1. What positive evidence shows that training with brain responses can alter model representations or task performance?
2. Which differences in modality, temporal resolution, personalization, model budget, endpoints, controls, seeds, and inference units prevent those results from settling compressed-student value?
3. What do privileged-information and feature-distillation studies establish about dense training-only targets, and what generic-target alternative do they create?
4. What do validity and compression studies require concerning nuisance control, split design, language-quality matching, and post-hoc versus training-time alignment?

Compare estimands and designs. Do not claim that positive prior studies are invalid or that they all lack controls for brain-response content.

#### 2.4 What evidence standard supports a brain-specific training advantage?

1. Which stages must pass from controlled measurability and language-quality headroom through exact-target measurability, target uptake, retained-student movement, comparator validity, biological transfer, and utility, and what does each stage establish?
2. Which comparator belongs to each stage, including untrained networks, ordinary distillation, permuted targets, matched text-derived auxiliary targets, matched language quality, and independent recorded-brain endpoints?
3. Which failed prerequisites stop a branch from supporting a brain-specific advantage, and which later descriptive results may still be reported without reviving the claim?

Section 2.2 explains why target uptake, reduced target loss, and retained-student movement are manipulation checks. This subsection must state the additional comparators and transfer endpoints required to move from those checks to a brain-specific advantage. Place the evidence-chain figure here. Do not repeat a second full version in the Introduction or Methods.

### 3. Experimental Framework

**Section question.** How was the claim instantiated without conflating measurement, optimization, attribution, and population inference?

Open with one compact evidence map: Which estimand, experiment family, comparator, endpoint, and inference unit belongs to each evidence stage?

#### 3.1 Which data and targets instantiate the claim?

1. What do the Tuckute sentence-level fMRI data contribute, and which participants, stimuli, regions, response constructions, and reliability rules instantiate the assay described conceptually in Section 2.1?
2. What does the LeBel naturalistic-story substrate contribute, and why can its deeply sampled participants not support a broad population claim?
3. How do participant-specific, participant-averaged, ROI-level, and voxelwise recorded fMRI responses differ, and how does using each as a training target or evaluation endpoint change the estimand?
4. How are the exact TRIBE target, its frozen row twin, the projected text-derived auxiliary target, and permuted controls constructed; what information source does each contain; and which properties are or are not matched?

This subsection owns the concrete data and response choices whose interpretive importance Section 2.1 establishes. Do not repeat the general validity argument or mix dataset description with result interpretation. Evidence owners: E002, E006, E008, E014, E016, E025-E026, and E030.

#### 3.2 How are students trained, and what survives deployment?

1. Which teacher, student, ordinary-distillation objective, and initialization are shared across arms, and which auxiliary objective differs?
2. Where is the temporary target head attached, which loss reaches which part of the student, and which parameters are trainable in each main regime?
3. Which heads and parameters are retained, frozen, merged, or discarded before evaluation?
4. How do recorded-brain-response, permuted-target, ordinary-distillation, text-derived-target, and TRIBE arms differ while preserving the intended comparison?

This subsection operationalizes the conceptual mechanism in Section 2.2: identify the shared language objective, the changing auxiliary target, the gradient path, and what remains after the temporary head is removed. Do not repeat the theoretical argument that output matching leaves multiple compatible representations. Use one architecture diagram to show both losses, gradient paths, and deployment-time components. State implementation variants in Appendix C rather than pretending all experiment families share one exact parameterization. Evidence owners: E003-E005, E008, E011, E013, E016-E017, and E025-E026, verified against source code.

#### 3.3 How is brain predictivity measured?

1. What does ordinary held-out \(R^2\) measure, why can it be negative, and which denominator and held-out recorded responses are used?
2. How do nuisance-only and full models operationalize the controlled-predictivity comparison introduced in Section 2.1 to obtain semipartial unique \(R^2\)?
3. Why is a fresh ridge readout fitted to frozen retained-student representations instead of reusing the temporary training head?
4. How are layers, contiguous folds, fold-only transformations, ridge regularization, response aggregation, and reliability filtering implemented without leakage?

This subsection owns the estimator and implemented readout protocol, not the general argument that assay choices bound interpretation. Introduce ordinary \(R^2\) before unique \(R^2\), state which response aggregation each endpoint uses, and connect each implementation choice to the corresponding conceptual requirement in Section 2.1. Keep the two defining equations in the main text and move derivations to Appendix D. Evidence owners: E001-E006, E008, E014-E016, E025, and E030.

#### 3.4 What are the estimands, controls, and inference units?

1. Which contrast tests recorded-brain-response-target specificity, and what independent unit supports its uncertainty statement?
2. Which distinct contrasts test synthetic-brain-response-target uptake, retained-student movement, comparator identification, exact-target validity, and biological transfer?
3. Why are participants biological inference units while folds, voxels, seeds, layers, and checkpoints usually quantify technical variation or robustness?
4. How is comparable language-model quality defined, measured, and enforced for each intervention contrast, and when does a mismatch make the comparison descriptive rather than identified?
5. How are confidence intervals, named tests, multiplicity, minimum detectable effects, practical thresholds, and prospective stop rules used without turning internal thresholds into universal biological constants?

Section 2.1 explains why the inference unit bounds a brain-predictivity claim; this subsection must name the estimand, comparator, aggregation order, and independent unit for each actual contrast. End with one transition paragraph explaining that Results follow the evidence chain rather than experiment number or execution date. Evidence owners: E003-E006, E008, E015-E017, E025-E026, and E030.

### 4. Results

**Section question.** Which links in the evidence chain hold, where does each branch first lose support, and what remains unresolved?

Open with one compact status table: What is the verdict, strongest evidence, and interpretation at each stage? Use *supported*, *not demonstrated*, *unresolved*, and *non-identifying comparator* consistently.

#### 4.1 Is controlled brain predictivity present?

1. Do trained middle layers satisfy the Section 2.1 standard by predicting held-out sentence-level fMRI beyond the specified nuisance features and architecture-matched untrained controls?
2. Does controlled predictivity survive held-out-story evaluation in the naturalistic voxelwise substrate?
3. What does this pass license, and why is it only an existence result under the tested participants, responses, controls, and linear readout?

Report whether the declared assays satisfy the conceptual standard from Section 2.1; do not redefine that standard or generalize beyond the implemented choices in Sections 3.1, 3.3, and 3.4. Evidence owners: E002 and scoped E006.

#### 4.2 Does compression leave interpretable alignment headroom?

1. How do the teacher, initialized student, and distilled student differ in controlled brain alignment?
2. How does alignment covary with tokenizer-comparable language-model quality across model families and in the operative quality band?
3. Why does the observed headroom motivate quality matching without identifying quality as the cause of alignment or distillation as the cause of the gap?

Evidence owners: E003 and E015.

End with an explicit branch handoff: controlled predictivity passes and observed headroom motivates intervention, but quality coupling requires matched intervention tests.

#### 4.3 Recorded-response branch: Does training with recorded fMRI responses create a participant-level advantage?

1. What apparent averaged-target positive trend appeared, and what estimand did that design actually support?
2. Why did valid-fold and participant-level reanalysis weaken the original positive interpretation?
3. What happens when participant responses are targets and participants are the inference units?
4. Do alternative losses, increased adapter capacity, voxelwise objectives, or full fine-tuning rescue a reliable effect?
5. What narrow conclusion survives, and what does the averaging diagnostic prevent us from claiming about encoding measurements generally?

Evidence owners: E004-E005, E008, E010-E011, E013-E014, and E017. Summarize intervention variants in one table and move their full detail to Appendix E.

#### 4.4 Synthetic-response branch I: Is the target measurable, learnable, and attributable?

1. Does the exact PCA-50 TRIBE target add controlled, practically relevant linear predictivity beyond the frozen nuisance model on the intended recorded-brain substrate, and does it beat the frozen row twin?
2. Can a fresh post-training readout recover the target from retained student representations beyond seed-matched ordinary distillation and target permutations, thereby testing target uptake as defined in Section 2.2?
3. Do target retention, parameter displacement, retained-student movement, and language-quality checks show only that the intervention changed the retained student without unacceptable quality loss, or do they license any stronger claim?
4. Is the saved text-derived auxiliary target sufficiently matched to attribute the larger TRIBE proxy gain to brain-response content?

Apply the distinction established in Section 2.2: target uptake and retained-student movement are manipulation checks, while attribution requires a valid comparator and transfer requires independent recorded responses. Evidence owners: E016, E025-E026, and E030. Exact-target measurability misses the frozen practical rule, while twin specificity remains unresolved. The later manipulation checks pass descriptively, but they cannot revive the brain-specific claim after the earlier prerequisite fails. Content attribution is not identified because the saved comparator differs on measured baseline headroom, covariance geometry, nuisance predictability, parameter displacement, and retained representation movement; initial-gradient comparability remains unresolved.

#### 4.5 Synthetic-response branch II: Does target uptake transfer to recorded fMRI responses?

1. Given the earlier failed or unresolved prerequisites, what can later biological-transfer results still establish descriptively?
2. What does the direct participant-level TRIBE-minus-ordinary-distillation contrast show?
3. What does the TRIBE-minus-text-derived-target contrast show numerically, and why can it not identify brain-response content?
4. Does student-predictable target structure overlap with independently recorded responses under the frozen bridge test?
5. Where is the first defensible predictive failure localized, and why does that localization not causally explain the later near-zero transfer result?

Evidence owners: E025, E026, and E030. State that direct transfer is near zero in the tested cohort, the relative control contrast is non-identifying, the exact target misses the frozen practical linear-measurability rule, and twin specificity plus later bridge contrasts remain unresolved.

#### 4.6 Does any tested route establish external utility?

1. Does training with recorded fMRI responses improve the selected out-of-domain language endpoint when its prerequisite brain-specific representation change is absent?
2. Do reduced external reproductions or cognitive and privileged-target branches establish a positive result under their declared controls?
3. What does stopping at failed prerequisites license us to conclude, and why does it not establish a universal utility null?

Evidence owners: E009, E019-E022, and E024. Keep only E009 and a compact synthesis in the main text. Do not present E023 or E027-E029 as completed evidence.

### 5. Discussion

**Section question.** What do the results change about how brain alignment should be used as a training signal?

#### 5.1 What exactly failed?

1. Which links passed, failed, or remained unresolved in the recorded-response and synthetic-response branches?
2. Which explanations are weakened by the measurement controls and intervention variants?
3. Which explanations remain viable, including target information, target geometry, modality, temporal precision, optimization, model scale, nonlinear transfer, and participant heterogeneity?
4. Why is this a scoped failure localization rather than a universal null or a causal explanation of failure?

Do not treat the variant studies as objective- or capacity-invariant failures. E011 did not induce greater effective movement, and E013/E017 close only the tested loss, data, and parameterization regimes.

#### 5.2 How can the result coexist with positive prior studies?

1. How do modality, temporal resolution, personalization, model budget, and endpoint choice change the intervention being tested?
2. How do language-quality matching, baseline choice, training seeds, controls, and inference units change the claim supported by a positive contrast?
3. What does this study add without claiming to refute materially different positive results?

Section 2.3 owns the factual literature map and unresolved pre-results gap. This subsection owns only the post-results compatibility judgment and must cross-reference, not resummarize, the earlier studies.

#### 5.3 How should the observed failure modes change future study design?

1. How does the comparator failure imply a design that matches information, geometry, scale, learnability, and optimization pressure before content attribution?
2. How does the exact-target measurability failure change the order of checks before expensive student training?
3. How does the gap between uptake and transfer change the required participant-level and independent-endpoint evidence after successful manipulation?
4. How should the observed failure location determine whether a program continues, redesigns its target or control, or stops downstream testing?

Section 2.4 owns the ex ante evidence standard and comparator catalog. This subsection owns only design changes newly justified by the observed failure locations. Frame them as recommendations supported by the diagnostic logic, not as an experimentally proven universal recipe.

### 6. Limitations

**Section question.** Which populations, constructs, comparisons, and intervention spaces bound the conclusion?

1. What do the tested English stimuli, fMRI cohorts, deeply sampled participants, regions, and response summaries cover?
2. Which modalities, populations, stimulus types, temporal scales, and nonlinear readouts remain untested?
3. How do the specified nuisance sets, comparator mismatch, restricted linear readout, PCA-50 target assay, unresolved twin contrast, and dependence structures bound identification?
4. Which effects at the preregistered continuation thresholds are disfavored, and which small effects or individual differences remain compatible with the data?
5. Which student scales, architectures, objectives, schedules, data scales, target constructions, and personalization strategies were not searched?
6. Why do perplexity, reduced reproductions, failed prerequisites, and limited downstream endpoints not exhaust practical utility?

### 7. Conclusion

**Section question.** What final answer should the reader retain?

Two paragraphs:

1. What is the direct, scope-bounded answer for the tested systems?
2. What durable methodological lesson follows about the evidence needed to turn a brain score into a training signal?

## Complete appendix question tree

### Appendix A. Evidence provenance and experiment disposition

Use one ledger rather than one prose subsection per experiment.

1. Which E001-E030 identifiers were executed, unexecuted, precondition-stopped, superseded, or used only for engineering?
2. Which final E-record verdict owns each main-text claim?
3. Which earlier interpretations were corrected, and which final verdict supersedes them?
4. Which retained artifacts, paths, hashes, and tables are load-bearing for reproduction?

### Appendix B. Data, targets, and preprocessing

#### B.1 Data inclusion and response construction

1. What exact acquisition, inclusion, exclusion, alignment, region, voxel, and reliability rules implement the bounding assay choices introduced in Section 2.1 and summarized in Section 3.1?
2. How are participant-level and averaged responses constructed, and which estimand changes when responses are aggregated?

#### B.2 Stimulus and nuisance features

1. Which exact low-level, static, and model-derived nuisance features instantiate the control rationale from Section 2.1 in each analysis?
2. Which transforms are fitted inside folds, and which implementation checks realize the contiguous-split and leakage requirements specified in Sections 2.1 and 3.3?

#### B.3 Synthetic brain responses and text-derived auxiliary targets

1. How are the exact TRIBE target, PCA representation, frozen row twin, text-feature target, and permutations generated?
2. How are dimensions, scaling, covariance, baseline headroom, and learnability compared, and where does matching remain inadequate?

### Appendix C. Training architecture and objectives

#### C.1 Ordinary distillation and language-quality control

1. What output loss, temperature, weighting, data, initialization, schedule, and quality criteria define ordinary distillation?
2. Which checkpoints and seed-matched comparisons are used across intervention arms?

#### C.2 Recorded-brain-response interventions

1. What forward path, target head, loss, trainable parameter set, and retained component define each recorded-brain-response-target regime?
2. How do MSE, contrastive, adapter-capacity, voxelwise, and full-fine-tuning variants depart from the common design?

#### C.3 Synthetic-brain-response interventions

1. What forward and gradient paths connect the middle-layer representation, temporary target head, KD loss, target loss, later student blocks, and tied output components?
2. Which parameters and heads are saved or discarded, and how are matched ordinary-distillation, text-feature, and permuted controls constructed?

#### C.4 Reproducibility

1. Which hyperparameters, seeds, software versions, checkpoints, artifacts, and hashes reproduce every load-bearing result?
2. Which artifacts are diagnostic only, and which receive stable manuscript-cited paths?

### Appendix D. Estimators, inference, and formal scope

#### D.1 Encoding estimators

1. How are the ordinary, nuisance-only, full, semipartial, and partial \(R^2\) quantities used in Section 3.3 formally related?
2. How does ridge regression correspond to a MAP estimator under its assumptions, and why does that interpretation not make the empirical score a causal or mechanistic quantity?

#### D.2 Cross-validation and inference units

1. How are folds, regularization, layers, transforms, repeated technical measurements, seeds, voxels, regions, and participants ordered and aggregated for the estimands named in Section 3.4?
2. Why are spatial voxels, shared folds, seeds, and participants not interchangeable independent units, and how does that formal distinction enforce the interpretive boundary introduced in Section 2.1?

#### D.3 Uncertainty, power, and decision thresholds

1. Which confidence intervals, tests, multiplicity corrections, sensitivities, minimum detectable effects, and practical thresholds answer each estimand?
2. Which thresholds were prospective continuation rules, and why must they not be universalized as biological importance criteria?

#### D.4 What information theory does and does not imply

1. Under which population linear-Gaussian assumptions can partial \(R^2\) be related to conditional mutual information, and why is cross-validated ridge unique \(R^2\) not itself an MI estimate?
2. Which Markov chain would be required for a data-processing claim about synthetic brain responses generated deterministically from text?
3. Why are mutual-information generalization bounds and rate-distortion arguments organizing constraints rather than guarantees or explanations of the empirical result?
4. Why do neither output KL matching nor low target loss determine retained-student movement, brain-response attribution, biological transfer, or internal biological alignment?

This appendix formalizes the limits introduced conceptually in Section 2.2; it must not convert those organizing constraints into empirical explanations or repeat the intervention results.

### Appendix E. Secondary experiments and failed instruments

#### E.1 Measurement and apparatus checks

1. What did E001 validate without producing a thesis result?
2. Which diagnostics checked plumbing, split integrity, target stability, and analysis behavior?

#### E.2 Averaging and intervention variants

1. What do E010 and E014 establish about response averaging and what do they not establish?
2. Which mechanism objection did each of E005, E011, E013, and E017 test, and why did none change the participant-level conclusion?

#### E.3 External and cross-modal probes

1. What did E019 and E022 reproduce locally?
2. Why are their outcomes reduced reproductions, corroborations, or non-reproductions rather than faithful refutations of the source papers?

#### E.4 Cognitive and privileged-target routes

1. What failed in E020, E021, and E024: signal, control, reference reliability, attribution, or substrate precondition?
2. Why were downstream builds or interpretations correctly stopped?

#### E.5 Prospective but unexecuted programs

1. What would E023, E027, E028, and E029 have identified if authorized and executed?
2. Why do reserved, outcome-blind development, or unexecuted designs provide no manuscript evidence?

### Appendix F. Sensitivities and full numerical tables

1. Which layer, lambda, quality-band, nuisance-set, participant, block, seed, and checkpoint sensitivities could change a main claim?
2. Which complete participant and seed tables let a reader verify aggregation and heterogeneity?
3. Which sensitivity results are claim-changing and belong in prose, and which are confirmatory detail suited to tables?

## Drafting and review protocol

1. Read the active leaf questions, their parent question, the owning E records, and the relevant canonical literature notes.
2. State the intended answer, claim type, scope, caveat, and evidence before drafting.
3. Draft adjacent leaf questions together only when they form one natural argumentative unit. Do not draft across a section boundary.
4. Use `\evd{Ennn}` and keyed values from `numbers.tex`. A missing value is a `\gap`, never a reconstruction or guess.
5. Run four independent reviews after each substantive drafting unit:
   - claim support and scope using `test-claims`;
   - reader and argument bottlenecks using `remove-bottlenecks`;
   - attention, length, and opportunity cost using `allocate-for-compounding`;
   - terminology, handoffs, ownership, and whole-manuscript fit using `coordinate-strategy`.
6. Reconcile the four reviews into one actionable brief. The drafting agent must either apply each accepted item or explain concretely why it conflicts with evidence or a higher-level question.
7. Repeat for at most four rounds, stopping earlier when no reviewer identifies a material claim, structure, prose, citation, terminology, or handoff defect.
8. After all units are complete, run the same four reviews over the whole manuscript and revise until the remaining findings are non-material.
9. Run `uv run python .claude/scripts/manuscript_check.py docs/manuscript/rewrite`, build the PDF, and inspect every rendered page before calling the candidate complete.

## Section acceptance checks

- **Introduction:** A reader can state the exact tested claim, the evidence chain, and the scoped answer without knowing an E identifier.
- **Section 2:** A reader can distinguish measurement, manipulation, attribution, transfer, and utility, and can name the comparator required for each.
- **Section 3:** A reader can say what is optimized, where gradients flow, what is retained, how alignment is freshly measured, which language-quality endpoint and matching rule apply to each intervention contrast, and which unit supports each inference.
- **Section 4:** Every result answers one declared gate, carries the correct evidence status, and avoids causal or universal claims unsupported by the E record.
- **Section 5:** The discussion explains the pattern without replaying Results or turning failure localization into a causal explanation.
- **Section 6:** Limitations bound the conclusion without inventing a new results narrative or repeating all caveats.
- **Section 7:** The conclusion answers the governing question directly and contains no new evidence.
- **Appendices:** A technical reader can reconstruct provenance, architecture, estimators, variants, and sensitivities without forcing the main text back into experiment chronology.

## Related

- [Manuscript guidance](../AGENTS.md)
- [Current extended manuscript](../extended/)
- [Evidence and authority contract](../../03-methodology.md)
- [Operational status](../../status.md)
