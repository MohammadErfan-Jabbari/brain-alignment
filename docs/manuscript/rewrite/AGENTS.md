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

**Provisional answer.** Trained language-model representations contain information useful for predicting held-out recorded fMRI responses beyond the specified controls. The tested distilled student is less brain-predictive than its teacher, although language-model quality remains a competing explanation. The tested recorded-response objectives do not demonstrate a reliable participant-level benefit. Synthetic brain responses generated from text are learnable and change retained student representations without unacceptable language-quality loss, but incremental target uptake beyond ordinary distillation remains unresolved, the text-derived auxiliary-control arm cannot identify brain-response content, the direct participant-level contrast on recorded fMRI responses is near zero, and the exact synthetic-target measurability criterion is not met. The evidence supports a failure-localization and evaluation framework, not a successful brain-response-guided distillation method.

**Scope.** The answer is limited to the tested models, English stimuli, datasets, participants, targets, objectives, optimization regimes, nuisance and intervention controls, linear readouts, comparators, inference units, and endpoints.

## Structural rules

- Organize the argument by claims and evidence-chain stages, not experiment order. Use *stage* for the conceptual chain and *criterion*, *threshold*, or *check* for operational continuation rules; do not use *gate* for both.
- Keep E identifiers as nonprinting `\evd{Ennn}` source provenance and provenance-appendix navigation, not reader-facing vocabulary. An internal-review build may display them.
- Use formal academic prose: state the claim or procedure directly, and remove meta-commentary about framing or writing unless that framing is itself the claim.
- Apply the unified question-tree and guided-inference method in `question-led-writing`: the tree maps what the reader must understand, and the inference path guides the reader there from shared ground one necessary distinction at a time.
- Guide rather than announce. Keep one principal conceptual move per sentence, explain why a mechanism or comparison matters before relying on it, provide local bridges for required premises, and make each paragraph prepare the next.
- Define an object's role positively and assign adjacent roles to their actual section or evidence owner. Avoid repeated “X rather than Y” or “X is not Y” constructions when two direct statements communicate the distinction more clearly.
- A subsection normally owns three to five related paragraph questions. A two-paragraph subsection is allowed only when it marks a real conceptual boundary. Merge a one-paragraph subsection into its parent.
- Split a subsection if it exceeds about 1,000 to 1,200 words, contains more than six or seven substantive paragraphs, or answers more than one parent question.
- Main-text theory must change the interpretation of an estimand or control. Put non-decisive derivations and analogies in Appendix D.
- Introduce each concept once, operationalize it once, and report its result once. Later sections should synthesize rather than restate.
- Do not present reserved, unexecuted, or precondition-stopped experiments as results.
- Use tables for analysis or evidence-record disposition, many-to-many evidence mappings, and repeated variant results.
- For dense mapping tables, separate compact identifiers such as stage numbers from descriptive labels, allocate the flexible-width column to the substantive comparison, and use the full text width before reducing font size. Split conceptually distinct stages into separate rows even when they share an intervention, assay, or analysis.
- Keep table and figure captions to one rendered line whenever possible. Use the caption to identify the object; place interpretation, caveats, and reading instructions in the surrounding prose.
- In process figures, use equal-sized boxes based on the longest required item. Give parallel box labels that name the claim and the test that supports it; shorten wording before shrinking type or accepting distracting line breaks.
- When color groups related stages in a figure, repeat the grouping with visible text labels and use light fills that preserve contrast; color must reinforce structure rather than carry it alone.

## Thesis-facing scientific-role contract

This rewrite is the thesis content. Organize the narrative by the role a procedure plays in the scientific argument, not by experiment chronology or evidence-record number.

| Level | Definition | Fixed terms |
|---|---|---|
| Route | Major source of training supervision | **recorded-response route**, **synthetic-response route** |
| Intervention | Paired training family defined by the manipulated supervision | **recorded-response intervention**, **synthetic-response intervention** |
| Arm or control | Condition inside an intervention or assay | **ordinary-distillation arm**, **permuted-response control**, **frozen row-twin control**, **text-derived auxiliary-control arm** |
| Assay | Protocol measuring a declared quantity | **controlled regional predictivity assay**, **controlled naturalistic voxelwise predictivity assay**, **exact synthetic-target measurability assay**, **synthetic-target recovery assay**, **saved-student biological-transfer assay** |
| Analysis or audit | Contrast, diagnostic, or validity examination | **quality-aware distillation-headroom analysis**, **retained-student movement audit**, **comparator-adequacy audit and attribution assessment**, **response-averaging analysis** |
| Evaluation | Recurring external endpoint | **language-quality evaluation**, **practical-utility evaluation** |
| Evidence record | Internal provenance owner | `E###` appears only in source provenance, an internal-review build, or the provenance appendix |

Use the shortest fixed term after first definition. Dataset, model, layer, target dimension, and response construction are qualifiers used only when they distinguish variants. Participant-specific and participant-averaged identify response construction or inference level, not standalone experiments. TRIBE identifies the generator. The text-derived auxiliary target, frozen row-twin control, and permutations are controls within their owning comparisons.

The main argument order is controlled predictivity, quality-aware headroom, exact synthetic-target measurability where applicable, intervention, retained manipulation, comparator adequacy and attribution, biological transfer, and practical utility. Target recovery and retained-student movement are manipulation checks within the synthetic-response intervention. Comparator adequacy may leave attribution non-identifying; do not name an unresolved attribution assessment as if attribution succeeded.

Supporting robustness analyses remain subordinate to the owning intervention or assay. Pipeline validation, failed instruments, reduced reproductions, stopped feasibility routes, and unexecuted designs belong in descriptively titled appendix or future-work categories. Never present them as completed headline experiments.

Do not expose evidence-record identifiers in ordinary thesis prose, headings, captions, tables, or result statements. Preserve `\evd{E###}` in source. The thesis build suppresses those markers, while Appendix A maps descriptive roles to evidence records, artifacts, and status.

### Layer ownership and handoffs

| Layer | Exclusive responsibility |
|---|---|
| Section 2 | Conceptual evidence standard: what each stage licenses, why it is necessary, and its generic failure boundary |
| Section 3 | One study-specific design tuple per scientific role: data or response construction, intervention or assay, comparator, estimand, endpoint, and inference unit |
| Section 4 | Observations, uncertainty, verdict, and the narrow claim licensed by each Section 3 design |
| Sections 5--7 | Synthesis, scope, implications, and final answer; no new methods or evidence |
| Appendix A | Scientific-role-to-evidence-record, artifact, and status crosswalk |
| Appendix B | Exact data, response, target and control construction, preprocessing, and split definitions |
| Appendix C | Exact training paths, losses, parameter states, schedules, and reproduction |
| Appendix D | Estimator formulas, aggregation, tests, uncertainty, multiplicity, and formal scope |
| Appendix E | Supporting analyses, failed or stopped instruments, and future designs with explicit status |
| Appendix F | Full values and claim-relevant sensitivities; no new headline conclusions |
| E records | Authority for what ran and what it produced |

For each scientific role, retain one Section 3 design summary, one Section 4 verdict location, one Section 5 interpretation when needed, and one appendix detail owner. If two locations answer the same level of question, move or delete one. Section 3 may link a design choice to Section 2 but must not repeat the conceptual argument or report a verdict. Section 4 must receive the named design tuple and must not restart its method description.

Language-quality evaluation is a cross-cutting endpoint and criterion. Section 3 summarizes its protocol, Section 3.5 states acceptability rules, Appendices C and D own implementation, and Section 4 reports route-specific values and verdicts. Exact synthetic-target measurability follows the same handoff: target construction in Appendix B, assay summary in Section 3, estimator in Appendix D, and verdict in Section 4.
- When prose introduces a multi-part figure, explicitly map the figure's groups or stages to the surrounding paragraph questions. Do not make the reader infer whether the figure illustrates one paragraph or the whole subsection.

## Attention budget

Target 9,000 to 10,000 main-text words, or roughly 21 to 23 A4 pages excluding references: about 2 pages for the Introduction, 3 for Section 2, 4 to 4.5 for Section 3, 7 to 8 for Results, 2.5 for Discussion, 1 to 1.5 for Limitations, and 0.5 for the Conclusion. Keep Section 2.3 within about 700 to 900 words and Sections 4.3 and 4.5 within about 1,000 to 1,200 words each. Preserve Results as the largest allocation.

Treat roughly 20 to 24 appendix pages as a planning band, not a compression target. Completeness means that every scientific role, supporting analysis, evidence record, and load-bearing claim is accounted for, not that every stored numerical row or machine-level artifact listing is reproduced. Leave exhaustive grids and artifact metadata in the owning E records and retained artifacts.

Give the three evidence-chain artifacts different jobs. The Section 2 figure defines the conceptual stages and claim meanings. The Section 3 table maps each stage to its canonical scientific role, estimand, comparator, endpoint, inference unit, and evidence owner. The Results table reports only the verdict and strongest evidence. Do not restate the full chain in the prose around all three.

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
| Retained-student movement | Parameter or representation difference from the declared training baseline that remains after temporary training components are discarded. |
| Exact-target measurability | Whether the exact synthetic training target adds controlled, practically relevant predictivity of recorded responses beyond the declared nuisance and frozen-generator controls. |
| Brain-response-specific attribution | Whether the brain-response-target arm outperforms its route-appropriate control on the outcome being claimed: correctly paired versus permuted responses for the recorded-response route, or synthetic brain responses versus a matched text-derived target for the synthetic-response route. |
| Biological transfer | Improvement on independently recorded responses that were not optimized as the training endpoint. |
| Brain-specific advantage | Incremental benefit beyond an appropriate text-derived or permuted control, at comparable language-model quality and the correct biological inference unit. Reserve this term for identified contrasts. |

Use the acronym definitions in `acronyms.tex`; never define the same acronym manually in prose. Use one term per concept unless the table above marks an intentional distinction.

Match each citation to the mechanism or empirical claim it actually supports. Do not use a general theoretical citation as evidence for easier optimization or learnability unless it studies that relationship; label an untested mechanism as a hypothesis and cite the closest relevant methodological or empirical work. Describe a permutation by its actual invariants: target permutation preserves target values and their marginal distribution while destroying stimulus--target pairing and joint structure.

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
5. Which ordered evidence-chain stages would justify a brain-specific training advantage at comparable language-model quality?
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

This subsection owns the conceptual mechanism and its limits: output objectives do not identify internal geometry; training-only targets may select among compatible representations; and manipulation evidence does not identify brain-specific benefit. A deterministic target cannot convey row-specific information independent of the stimulus and fixed generator, although it may convey generator-learned structure and reorganize what the student makes accessible. Leave exact target and control construction to Appendix B, summary-level prerequisite assay design to Section 3.2, recorded-response loss and gradient paths to Section 3.3, synthetic-response paths to Section 3.4, exact implementations to Appendix C, the full evidence standard to Section 2.4, formal information-theoretic arguments to Appendix D.4, and empirical verdicts to Sections 4.4--4.5.

#### 2.3 What does prior brain-response-guided training leave unresolved?

1. What evidence shows that training with recorded fMRI responses or synthetic brain responses generated from text can change model representations or task performance, and what claim does each result support?
2. Why do differences in modality, temporal resolution, personalization, model budget, endpoint, comparator, training seeds, and inference unit prevent those studies from establishing an incremental benefit for a fixed smaller student at comparable language-model quality?
3. Why do privileged-information and feature-distillation studies create the alternative explanation that any benefit may come from adding a dense, learnable auxiliary target rather than from brain-response content?
4. Which requirements from measurement-validity and compression research must an intervention study satisfy, including nuisance controls, leakage-resistant splits, language-quality matching, and separation of training-time objectives from post-training brain-predictivity evaluation?

This subsection owns the factual pre-results literature comparison and the unresolved intervention gap. Compare estimands and designs, use the table to support Questions 1 and 2 rather than create another argumentative branch, and do not claim that positive prior studies are invalid or that they all lack controls for brain-response content. Section 2.4 converts the gap into this manuscript's evidence standard, Section 3 implements that standard, and Section 5.2 owns only the post-results compatibility judgment.

#### 2.4 What evidence standard supports a brain-specific training advantage?

1. Which prerequisites establish a valid opportunity for intervention, including controlled brain predictivity, quality-aware headroom, and, for synthetic brain responses, exact-target measurability?
2. What do target uptake and retained-student movement each establish about whether the intervention affected the retained student?
3. Which comparisons are required to establish brain-response-specific attribution, transfer to independently recorded \ac{fmri} responses, and external utility?
4. Why is the evidence chain conjunctive, and how should later results be interpreted when an earlier prerequisite fails or remains unresolved?

Keep four roles distinct: opportunity prerequisites, manipulation checks, attribution, and endpoint evidence. Section 2.2 explains why target uptake, reduced target loss, and retained-student movement are manipulation checks; this subsection must state why they do not establish brain-specific attribution, biological transfer, or utility. Name the comparator needed for each claim, including untrained networks, ordinary distillation, permuted targets, matched text-derived auxiliary targets, matched language quality, and independent recorded-brain endpoints. Place the evidence-chain figure here. The Introduction may preview the chain, Section 3 must map each stage to its estimand and comparison, Section 4 must report each stage separately, Section 5.3 may derive design recommendations from observed failure locations, and Appendix D must formalize the corresponding estimators and decision rules. Do not repeat a second full version of the chain elsewhere.

### 3. Experimental Design and Evaluation

**Section question.** How did the study instantiate each scientific role with a distinct design tuple comprising its data or response construction, intervention or assay, comparator, estimand, endpoint, and inference unit?

Open with one compact evidence map using the exact canonical role names used in Sections 3 and 4. For each role, identify the Section 2.4 stage, comparator, endpoint, and inference unit. Keep the section at design-summary level; Appendices B--D own implementation detail.

#### 3.1 What study design, datasets, response constructions, and data partitions define the analysis?

1. Which scientific roles are instantiated by the Tuckute sentence-level and LeBel naturalistic-story data?
2. How do participant-specific, participant-averaged, \ac{roi}-level, and voxelwise recorded responses change the estimand and population scope?
3. Which corpora and held-out observations support target construction, student training, language-quality evaluation, target recovery, biological transfer, and practical utility?
4. Which role-separated split boundaries prevent target or endpoint leakage?

This subsection owns the study map and the interpretively necessary dataset and split summary. Appendix B owns acquisition, inclusion, response construction, preprocessing, target construction, and exact split definitions. Evidence owners: E002, E006, E008, E014, E016, E025-E026, and E030.

#### 3.2 How are the measurement prerequisites instantiated?

1. How do the controlled regional and controlled naturalistic voxelwise predictivity assays implement held-out nuisance-controlled prediction with architecture-matched controls?
2. How does the quality-aware distillation-headroom analysis compare teacher and student predictivity while treating \ac{lm} quality as a competing explanation?
3. How does the exact synthetic-target measurability assay compare the target with the nuisance model and frozen row-twin control on recorded responses?
4. How do ordinary and unique \(R^2\), reliability context, fresh ridge readouts, and leakage-safe transformations apply across these prerequisites?

This subsection owns summary-level assay design. Section 2 owns what each prerequisite licenses, Appendix B owns exact inputs and preprocessing, and Appendix D owns estimator formulas and aggregation. Evidence owners: E002-E003, E006, E015, and E030.

#### 3.3 How is the recorded-response intervention instantiated?

1. Which teacher, student, initialization, ordinary-\ac{kd} objective, data, and training budget are shared by its paired arms?
2. What is held fixed between the recorded-response arm and permuted-response control, and what manipulation differs?
3. How do participant-averaged and participant-specific response constructions define descriptive and primary estimands within the same intervention?
4. Where does the auxiliary loss attach, which retained parameters receive its gradient, and what components survive evaluation?
5. Which endpoint and inference unit test the participant-general intervention claim?

This subsection owns the common intervention design and its study-specific variants. Appendix C owns exact loss paths, schedules, parameter states, and robustness implementations; Appendix D owns formal inference. Evidence owners: E004-E005, E008, E011, E013, and E017.

#### 3.4 How is the synthetic-response intervention connected to manipulation, attribution, transfer, and utility assays?

1. Which components are shared by the synthetic-response, ordinary-distillation, row-permuted, and text-derived auxiliary-control arms, and what changes between them?
2. How do the synthetic-target recovery assay and retained-student movement audit test whether training affected the retained student?
3. How does the comparator-adequacy audit determine whether the available contrast can identify brain-response-specific attribution?
4. How does the saved-student biological-transfer assay reuse frozen students and independently recorded participant responses without further student training?
5. Which language-quality and practical-utility endpoints apply, and what prerequisite status limits their interpretation?

This subsection owns the intervention-to-endpoint design chain. Target recovery and retained-student movement are manipulation checks, not peer interventions. Appendix B owns target and control construction, Appendix C owns training and retained components, and Appendices D and F own estimators and sensitivities. Evidence owners: E009, E016, E025-E026, and E030.

#### 3.5 What cross-cutting estimands, quality rules, and inference procedures govern the comparisons?

1. What estimand, comparator, endpoint, and inference unit belongs to each canonical scientific role?
2. How is acceptable and comparable \ac{lm} quality defined for each route, and when does mismatch make a contrast descriptive rather than identified?
3. How are folds, coordinates, regions, voxels, seeds, and participants ordered and aggregated?
4. Which uncertainty procedures, named tests, multiplicity corrections, and practical or detectable-effect bounds answer each estimand?
5. Which stages were unmeasured, unresolved, or non-identifying, and how does that status constrain later results?

End with one transition paragraph stating that Results follow these scientific roles rather than evidence-record number or execution date. Appendix D owns exact formulas and tests. Evidence owners: E003-E006, E008-E009, E015-E017, E025-E026, and E030.

### 4. Results

**Section question.** Which scientific roles in the evidence chain are supported, not demonstrated, unresolved, or non-identifying at their declared inference units?

Open with one compact status table keyed to the exact canonical role names and Section 3 design tuples. Use *supported*, *not demonstrated*, *unresolved*, and *non-identifying comparator* consistently.

#### 4.1 Controlled regional and naturalistic predictivity

1. Do trained middle layers satisfy the Section 2.1 standard by predicting held-out sentence-level fMRI beyond the specified nuisance features and architecture-matched untrained controls?
2. Does controlled predictivity survive held-out-story evaluation in the naturalistic voxelwise substrate?
3. What does this pass license, and why is it only an existence result under the tested participants, responses, controls, and linear readout?

Receive the two predictivity assay designs from Section 3.2, report their estimates and uncertainty, and state the narrow claim licensed without restarting the method. Evidence owners: E002 and scoped E006.

#### 4.2 Quality-aware distillation headroom

1. How do the teacher, initialized student, and distilled student differ in controlled brain alignment?
2. How does alignment covary with tokenizer-comparable language-model quality across model families and in the operative quality band?
3. Why does the observed headroom motivate quality matching without identifying quality as the cause of alignment or distillation as the cause of the gap?

Evidence owners: E003 and E015.

End with an explicit route handoff: controlled predictivity passes and observed headroom motivates intervention, but quality coupling requires matched intervention tests.

#### 4.3 Recorded-response intervention

1. What apparent averaged-target positive trend appeared, and what estimand did that design actually support?
2. Why did valid-fold and participant-level reanalysis weaken the original positive interpretation?
3. What happens when participant responses are targets and participants are the inference units?
4. Do alternative losses, increased adapter capacity, voxelwise objectives, or full fine-tuning rescue a reliable effect?
5. What narrow conclusion survives, and what does the averaging diagnostic prevent us from claiming about encoding measurements generally?

Participant averaging and participant-specific analysis are estimand and inference choices within one intervention, not peer experiments. Evidence owners: E004-E005, E008, E010-E011, E013-E014, and E017. Summarize robustness variants in one table and move their full detail to Appendix E.

#### 4.4 Exact synthetic-target measurability

1. Does the exact PCA-50 TRIBE target add controlled, practically relevant linear predictivity beyond the frozen nuisance model on the intended recorded-response substrate?
2. Does the exact target outperform the frozen row-twin control?
3. Which part of the practical measurability criterion fails, which specificity question remains unresolved, and what narrow prerequisite verdict follows?

Keep this prerequisite separate from post-training manipulation. Evidence owner: E030.

#### 4.5 Synthetic-response manipulation and attribution status

1. Can a fresh post-training readout recover the synthetic target beyond seed-matched ordinary distillation and target permutations?
2. Do target retention, parameter displacement, and retained-student movement show that the intervention changed the retained student?
3. Did these manipulation checks pass at acceptable \ac{lm} quality?
4. Is the text-derived auxiliary-control arm sufficiently matched to identify brain-response-specific attribution?
5. Which attribution questions therefore remain non-identifying or unresolved?

Target recovery and retained-student movement are manipulation checks within the synthetic-response intervention. The comparator-adequacy audit assesses whether attribution is identified; it is not itself a successful attribution result. Evidence owners: E016, E025-E026, and E030.

#### 4.6 Saved-student biological transfer

1. Given the failed or unresolved earlier stages, what can later biological-transfer results still establish descriptively?
2. What does the direct participant-level synthetic-response-minus-ordinary-distillation contrast show?
3. What does the synthetic-response-minus-text-derived-control contrast show, and why can it not identify brain-response content?
4. Does student-predictable target structure overlap with independently recorded responses under the frozen bridge test?
5. Where is the first defensible predictive failure localized, and why does that localization not causally explain the later near-zero transfer result?

Evidence owners: E025-E026 and E030.

#### 4.7 Bounded practical-utility evaluation

1. Does the completed out-of-domain evaluation establish a practical benefit when its prerequisite brain-specific representation change is absent?
2. How does the unreliable mediator limit interpretation of the bounded null?
3. What does the result leave open about other tasks, modalities, and successfully identified interventions?

Evidence owner: E009. Supporting reproductions, failed instruments, stopped routes, and prospective designs remain in Appendix E and enter the Discussion only when they change interpretation.

### 5. Discussion

**Section question.** What do the results change about how brain alignment should be used as a training signal?

#### 5.1 Failure localization across the evidence chain

1. Which links passed, failed, or remained unresolved in the recorded-response and synthetic-response branches?
2. Which explanations are weakened by the measurement controls and intervention variants?
3. Which explanations remain viable, including target information, target geometry, modality, temporal precision, optimization, model scale, nonlinear transfer, and participant heterogeneity?
4. Why is this a scoped failure localization rather than a universal null or a causal explanation of failure?

Do not treat the variant studies as objective- or capacity-invariant failures. E011 did not induce greater effective movement, and E013/E017 close only the tested loss, data, and parameterization regimes.

#### 5.2 Relation to positive prior studies

1. How do modality, temporal resolution, personalization, model budget, and endpoint choice change the intervention being tested?
2. How do language-quality matching, baseline choice, training seeds, controls, and inference units change the claim supported by a positive contrast?
3. What does this study add without claiming to refute materially different positive results?

Section 2.3 owns the factual literature map and unresolved pre-results gap. This subsection owns only the post-results compatibility judgment and must cross-reference, not resummarize, the earlier studies.

#### 5.3 Implications for future brain-guided training

1. How does the comparator failure imply a design that matches information, geometry, scale, learnability, and optimization pressure before content attribution?
2. How does the exact-target measurability failure change the order of checks before expensive student training?
3. How does the gap between uptake and transfer change the required participant-level and independent-endpoint evidence after successful manipulation?
4. How should the observed failure location determine whether a program continues, redesigns its target or control, or stops downstream testing?

Section 2.4 owns the ex ante evidence standard and comparator catalog. This subsection owns only design changes newly justified by the observed failure locations. Frame them as recommendations supported by the diagnostic logic, not as an experimentally proven universal recipe.

### 6. Limitations

**Section question.** Which populations, constructs, comparisons, and intervention spaces bound the conclusion?

#### 6.1 Population, data, and measurement scope

1. What do the tested English stimuli, fMRI cohorts, deeply sampled participants, regions, and response summaries cover?
2. Which modalities, populations, stimulus types, temporal scales, and nonlinear readouts remain untested?

#### 6.2 Identification and inference limitations

1. How do the specified nuisance sets, comparator mismatch, restricted linear readout, PCA-50 target assay, unresolved twin contrast, and dependence structures bound identification?
2. Which effects at the declared continuation thresholds are disfavored, and which small effects or individual differences remain compatible with the data?

#### 6.3 Intervention and utility scope

1. Which student scales, architectures, objectives, schedules, data scales, target constructions, and personalization strategies were not searched?
2. Why do language-quality evaluation, reduced reproductions, failed prerequisites, and limited downstream endpoints not exhaust practical utility?

### 7. Conclusion

**Section question.** What final answer should the reader retain?

Two paragraphs:

1. What is the direct, scope-bounded answer for the tested systems?
2. What durable methodological lesson follows about the evidence needed to turn a brain score into a training signal?

## Complete appendix question tree

### Appendix A. Evidence provenance and analysis disposition

Use one compact scientific-role-to-evidence-record ledger rather than one prose subsection per record.

1. Which evidence records were executed, unexecuted, precondition-stopped, superseded, or used only for engineering?
2. Which final evidence-record verdict owns each main-text scientific role and claim?
3. Which earlier interpretations were corrected, and which final verdict supersedes them?
4. Which retained artifacts, paths, hashes, and tables are load-bearing for reproduction?

### Appendix B. Data, responses, targets, and controls

#### B.1 Data inclusion and response construction

1. What exact acquisition, inclusion, exclusion, alignment, region, voxel, and reliability rules implement the bounding assay choices introduced in Section 2.1 and summarized in Section 3.1?
2. How are participant-level and averaged responses constructed, and which estimand changes when responses are aggregated?

#### B.2 Stimulus and nuisance features

1. Which exact low-level, static, and model-derived nuisance features instantiate the control rationale from Section 2.1 in each analysis?
2. Which transforms are fitted inside folds, and which implementation checks realize the contiguous-split and leakage requirements specified in Sections 2.1 and 3.3?

#### B.3 Synthetic brain responses and text-derived auxiliary targets

1. How are the exact TRIBE target, PCA representation, frozen row-twin control, text-derived auxiliary target, and permutations generated?
2. How are dimensions, scaling, covariance, baseline headroom, and learnability compared, and where does matching remain inadequate?

### Appendix C. Training interventions and reproduction

#### C.1 Ordinary distillation and language-quality control

1. What output loss, temperature, weighting, data, initialization, schedule, and quality criteria define ordinary distillation?
2. Which checkpoints and seed-matched comparisons are used across intervention arms?

#### C.2 Recorded-response intervention

1. What forward path, target head, loss, trainable parameter set, and retained component define each recorded-brain-response-target regime?
2. How do MSE, contrastive, adapter-capacity, voxelwise, and full-fine-tuning variants depart from the common design?

#### C.3 Synthetic-response intervention

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

1. Which confidence intervals, tests, multiplicity corrections, sensitivities, minimum detectable effects, and practical thresholds answer each opportunity, manipulation, attribution, transfer, and utility estimand?
2. Which thresholds were prospective continuation rules for a particular stage, and why must they not be promoted into evidence for a later stage or universalized as biological importance criteria?

#### D.4 What information theory does and does not imply

1. Under which population linear-Gaussian assumptions can partial \(R^2\) be related to conditional mutual information, and why is cross-validated ridge unique \(R^2\) not itself an MI estimate?
2. Which Markov chain would be required for a data-processing claim about synthetic brain responses generated deterministically from text?
3. Why are mutual-information generalization bounds and rate-distortion arguments organizing constraints rather than guarantees or explanations of the empirical result?
4. Why do neither output KL matching nor low target loss determine retained-student movement, brain-response attribution, biological transfer, or internal biological alignment?

This appendix formalizes the limits introduced conceptually in Section 2.2; it must not convert those organizing constraints into empirical explanations or repeat the intervention results.

### Appendix E. Supporting analyses, failed instruments, and future designs

#### E.1 Pipeline validation and apparatus checks

1. What did the synthetic pipeline validation establish without producing a thesis result?
2. Which diagnostics checked plumbing, split integrity, target stability, and analysis behavior?

#### E.2 Response averaging and intervention robustness

1. What do the response-averaging analyses establish, and what do they not establish?
2. Which mechanism objection did each recorded-response robustness analysis test, and why did none change the participant-level conclusion?

#### E.3 External and cross-modal probes

1. What did the external brain-tuning and reduced speech-transfer probes reproduce locally?
2. Why are their outcomes reduced reproductions, corroborations, or non-reproductions rather than faithful refutations of the source papers?

#### E.4 Cognitive and privileged-target routes

1. What failed in the shared-response, reading-time, and gaze-first routes: signal, control, reference reliability, attribution, or substrate precondition?
2. Why were downstream builds or interpretations correctly stopped?

#### E.5 Unexecuted future designs

1. What would the objective-specific shedding, matched-target, cross-modal falsification, and directional-certificate designs have identified if authorized and executed?
2. Why do reserved, outcome-blind development, or unexecuted designs provide no manuscript evidence?

### Appendix F. Sensitivity analyses and full numerical tables

1. Which layer, lambda, quality-band, nuisance-set, participant, block, seed, and checkpoint sensitivities could change a main claim?
2. Which complete participant and seed tables let a reader verify aggregation and heterogeneity?
3. Which sensitivity results are claim-changing and belong in prose, and which are confirmatory detail suited to tables?

## Drafting and review protocol

1. Read the active leaf questions, their parent question, the owning evidence records, and the relevant canonical literature notes.
2. Apply `question-led-writing` to state the reader's starting understanding, the intended answer and scope, and the shortest supported inference path for each active leaf.
3. Locate every existing paragraph that answers the active leaf, then draft one complete proposed replacement. Propose moving overlapping prose instead of appending a duplicate.
4. Draft adjacent leaf questions together only when they form one natural argumentative unit. Do not draft across a section boundary.
5. Use `\evd{Ennn}` as nonprinting source provenance and keyed values from `numbers.tex`. A missing value is a `\gap`, never a reconstruction or guess.
6. Use the smallest applicable review set during ordinary paragraph work. Run all four independent reviews at load-bearing subsection or section boundaries, or when framing, scope, ownership, or attention allocation changes materially:
   - claim support and scope using `test-claims`;
   - reader and argument bottlenecks using `remove-bottlenecks`;
   - attention, length, and opportunity cost using `allocate-for-compounding`;
   - terminology, handoffs, ownership, and whole-manuscript fit using `coordinate-strategy`.
7. When multiple reviews run, reconcile them into one proposed revision. Address each accepted item or explain concretely why it conflicts with evidence or a higher-level question.
8. Erfan approves load-bearing wording and verdict framing. Edit manuscript source only after approval.
9. At subsection close, reverse-outline both structures: every leaf is answered once, every paragraph has one owner, every inference is supported before use, and every transition prepares the next reader question.
10. Apply the skeptical-reader test: the prose must be understandable sentence by sentence without an unsupported jump, an unexplained result, or dependence on project history.
11. Repeat for at most four rounds, stopping earlier when no reviewer identifies a material claim, structure, prose, citation, terminology, density, or handoff defect.
12. After all units are complete, run the same four reviews over the whole manuscript and revise until the remaining findings are non-material.
13. Run `uv run python .claude/scripts/manuscript_check.py docs/manuscript/rewrite`, build the PDF, and inspect every rendered page before calling the candidate complete.

## Section acceptance checks

- **Introduction:** A reader can state the exact tested claim, the evidence chain, and the scoped answer without knowing an E identifier.
- **Section 2:** A reader can distinguish measurement, manipulation, attribution, transfer, and utility, and can name the comparator required for each.
- **Section 3:** Every canonical scientific role has one design tuple, and the reader can identify its data or response construction, intervention or assay, comparator, estimand, endpoint, and inference unit without reading implementation detail.
- **Section 4:** Every canonical scientific role has one result and verdict location, carries the correct evidence status, and avoids causal or universal claims unsupported by its evidence record.
- **Section 5:** The discussion explains the pattern without replaying Results or turning failure localization into a causal explanation.
- **Section 6:** Limitations bound the conclusion without inventing a new results narrative or repeating all caveats.
- **Section 7:** The conclusion answers the governing question directly and contains no new evidence.
- **Appendices:** A technical reader can reconstruct provenance, data and target construction, interventions, estimators, variants, and sensitivities without forcing the main text back into evidence-record chronology.

## Related

- [Manuscript guidance](../AGENTS.md)
- [Current extended manuscript](../extended/)
- [Evidence and authority contract](../../03-methodology.md)
- [Operational status](../../status.md)
