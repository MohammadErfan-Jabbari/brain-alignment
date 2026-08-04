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
- Introduce every symbol before its equation. Unless the meaning is already unmistakable, follow each claim-bearing equation with one or two plain-language sentences that explain what it computes and why that quantity answers the current reader question.
- Introduce each concept once, operationalize it once, and report its result once. Later sections should synthesize rather than restate.
- Do not present reserved, unexecuted, or precondition-stopped experiments as results.
- Use tables for analysis or evidence-record disposition, many-to-many evidence mappings, and repeated variant results.
- For dense mapping tables, separate compact identifiers such as stage numbers from descriptive labels, allocate the flexible-width column to the substantive comparison, and use the full text width before reducing font size. Split conceptually distinct stages into separate rows even when they share an intervention, assay, or analysis.
- Keep table and figure captions to one rendered line whenever possible. Use the caption to identify the object; place interpretation, caveats, and reading instructions in the surrounding prose.
- In process figures, use equal-sized boxes based on the longest required item. Give parallel box labels that name the claim and the test that supports it; shorten wording before shrinking type or accepting distracting line breaks.
- When color groups related stages in a figure, repeat the grouping with visible text labels and use light fills that preserve contrast; color must reinforce structure rather than carry it alone.
- Treat every arrow as a scientific statement: make its relation explicit through a readable arrow label, adjacent text, or column heading, and never let geometry alone imply causation, mediation, successful attribution, or population generalization.
- Give each figure one relationship to explain. In Section 3, data routing, competing readouts, intervention mechanics, and inference-unit aggregation have separate owners; do not redraw the Section 2 evidence chain or the Results verdict table inside them.

## Thesis-facing scientific-role contract

This rewrite is the thesis content. Organize the narrative by the role a procedure plays in the scientific argument, not by experiment chronology or evidence-record number.

| Level | Definition | Fixed terms |
|---|---|---|
| Route | Major source of training supervision | **recorded-response route**, **synthetic-response route** |
| Intervention | Paired training family defined by the manipulated supervision | **recorded-response intervention**, **synthetic-response intervention** |
| Arm or control | Condition inside an intervention or assay | **ordinary-distillation arm**, **permuted-response control**, **frozen row-twin control**, **text-derived auxiliary-control arm** |
| Assay | Protocol measuring a declared quantity | **controlled regional predictivity assay**, **controlled naturalistic voxelwise predictivity assay**, **exact synthetic-target measurability assay**, **synthetic-target recovery assay**, **saved-student biological-transfer assay** |
| Analysis or audit | Contrast, diagnostic, or validity examination | **quality-aware distillation-headroom analysis**, **retained-student movement audit**, **comparator-adequacy audit and attribution assessment**, **saved-student target-retention analysis**, **composed-path diagnostic**, **response-averaging analysis** |
| Evaluation | Recurring external endpoint | **language-quality evaluation**, **bounded practical-utility evaluation** |
| Evidence record | Internal provenance owner | `E###` appears only in source provenance, an internal-review build, or the provenance appendix |

Use the shortest fixed term after first definition. Dataset, model, layer, target dimension, and response construction are qualifiers used only when they distinguish variants. Participant-specific and participant-averaged identify response construction or inference level, not standalone experiments. TRIBE identifies the generator. The text-derived auxiliary target, frozen row-twin control, and permutations are controls within their owning comparisons.

The main argument order is controlled brain predictivity, quality-aware headroom, exact synthetic-target measurability where applicable, intervention, retained manipulation, comparator adequacy and attribution, biological transfer, and practical utility. Target recovery and retained-student movement are manipulation checks within the synthetic-response intervention. Comparator adequacy may leave attribution non-identifying; do not name an unresolved attribution assessment as if attribution succeeded.

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
| Exact-target measurability | Whether the exact synthetic training target adds controlled, practically relevant predictivity of recorded responses beyond the declared nuisance and frozen row-twin controls. |
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
5. Where did the two intervention routes first lose support, and what happened to attribution, participant-level transfer, and utility?
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

### 2. Evidence Required for a Brain-Specific Training Advantage

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

This subsection owns the study map and the interpretively necessary dataset and split summary. Appendix B owns acquisition, inclusion, response construction, preprocessing, target construction, and exact split definitions. Evidence owners: E002--E006, E008--E009, E013--E017, E025, and E030.

#### 3.2 How are the measurement prerequisites instantiated?

1. How do the controlled regional and controlled naturalistic voxelwise predictivity assays implement held-out nuisance-controlled prediction with architecture-matched controls?
2. How does the quality-aware distillation-headroom analysis compare teacher and student predictivity while treating \ac{lm} quality as a competing explanation?
3. How does the exact synthetic-target measurability assay compare the target with the nuisance model and frozen row-twin control on recorded responses?
4. How do ordinary and unique \(R^2\), reliability context, fresh ridge readouts, and leakage-safe transformations apply across these prerequisites?

This subsection owns summary-level assay design and the compact formulas for its main estimands. Section 2 owns what each prerequisite licenses, Appendix B owns exact inputs and preprocessing, and Appendix D owns estimator derivations, variants, aggregation, tests, and inference. Evidence owners: E002-E003, E006, E015, and E030.

#### 3.3 How is the recorded-response intervention instantiated?

1. Which teacher, student, initialization, ordinary-\ac{kd} objective, data, and training budget are shared by its paired arms?
2. What is held fixed between the recorded-response arm and permuted-response control, and what manipulation differs?
3. How do participant-averaged and participant-specific response constructions define descriptive and primary estimands within the same intervention?
4. Where does the auxiliary loss attach, which retained parameters receive its gradient, and what components survive evaluation?
5. Which endpoint and inference unit test the participant-general intervention claim?
6. Which study-specific variants retain the paired recorded-versus-permuted design, and which target, loss, language anchor, trainable subset, or evaluation scope does each variant change?

This subsection owns the common intervention design and its study-specific variants. Appendix C owns exact loss paths, schedules, parameter states, and robustness implementations; Appendix D owns formal inference. Evidence owners: E004-E005, E008, E011, E013, and E017.

#### 3.4 How is the synthetic-response intervention connected to manipulation, attribution, transfer, and utility assays?

1. Which components are shared by the synthetic-response, ordinary-distillation, and text-derived auxiliary-control arms, what changes between them, and why are the saved block-permuted arms sensitivity checks rather than peer claim-identifying arms?
2. How do the synthetic-target recovery assay and retained-student movement audit test whether training affected the retained student?
3. How does the comparator-adequacy audit determine whether the available contrast can identify brain-response-specific attribution?
4. How do the saved-student target-retention analysis, direct saved-student biological-transfer assay, and composed-path diagnostic reuse frozen students, synthetic targets, or independently recorded participant responses, and what distinct question does each answer?
5. Which language-quality checks qualify the synthetic-response contrasts, which bounded practical-utility evaluation belongs to the separate recorded-response route, and what prerequisite status limits each interpretation?

This subsection is titled ``Synthetic-Response Intervention and Downstream Assays'' and owns the intervention-to-endpoint design chain. Target recovery and retained-student movement are manipulation checks, not peer interventions. Saved block-permuted arms are sensitivities because their construction does not guarantee an exact row derangement. Appendix B owns target and control construction, Appendix C owns training and retained components, and Appendices D and F own estimators and sensitivities. Evidence owners: E009, E016, E025-E026, and E030.

#### 3.5 What cross-cutting estimands, quality rules, and inference procedures govern the comparisons?

1. What estimand, comparator, endpoint, and inference unit belongs to each canonical scientific role?
2. How is acceptable and comparable \ac{lm} quality defined for each route, and when does mismatch make a contrast descriptive rather than identified?
3. How are folds, coordinates, regions, voxels, seeds, and participants ordered and aggregated?
4. Which uncertainty procedures, named tests, multiplicity corrections, and practical or detectable-effect bounds answer each estimand?
5. How do unmeasured, unresolved, and non-identifying statuses constrain the claims reported later in the Results?

This subsection is titled ``Cross-Cutting Estimands and Decision Rules.'' End with one transition paragraph stating that Results follow these scientific roles rather than evidence-record number or execution date. Appendix D owns estimator derivations, variants, aggregation, and tests. Evidence owners: E003-E006, E008-E009, E015-E017, E025-E026, and E030.

### 4. Results Across the Evidence Chain

**Section question.** Where does each scientific role pass, fail, remain unresolved, or become non-identifying at its declared inference unit, and what narrow claim does each result license?

Open with one compact three-column status table keyed to the exact canonical role names and Section 3 design tuples: **scientific role**, **status**, and **decisive observation**. Use *supported*, *not demonstrated*, *unresolved*, and *non-identifying comparator* consistently. Give every Section 3 scientific role one clearly named Results verdict location.

Each result path follows the same order: **observation**, **uncertainty at the declared inference unit**, **canonical verdict**, and **narrow licensed claim**. Retain only the comparator or inference-unit reminder needed to interpret a result. Section 3 owns the design tuple, Section 5 owns cross-stage synthesis and causal interpretation, and Appendices B--F own construction, training detail, formal inference, supporting analyses, and full sensitivities.

Use **synthetic-response arm**, **text-derived auxiliary-control arm**, **ordinary-distillation arm**, and **frozen row-twin control** consistently. Compact contrast notation may appear inside equations, tables, and plot labels when it is defined locally. Evidence-record identifiers remain nonprinting source provenance and never organize the rendered Results.

The route order must remain explicit. Sections 4.1--4.2 report prerequisites shared by both intervention routes, Section 4.3 reports the recorded-response intervention, Sections 4.4--4.6 report the synthetic-response route, and Section 4.7 returns to the recorded-response route for the only completed bounded practical-utility evaluation.

#### 4.1 Controlled brain predictivity under regional and naturalistic assays

1. Do trained representations outperform the specified nuisance features and architecture-matched untrained controls in the controlled regional predictivity assay?
2. Does controlled brain predictivity survive held-out-story evaluation in the controlled naturalistic voxelwise predictivity assay?
3. What common controlled brain predictivity claim do the two assays support without pooling their estimates?
4. Which population, intervention, and mechanistic claims remain unsupported?

Receive both assay designs from Section 3.2. Report their estimates and uncertainty, state the shared narrow claim, and keep their scales and inference units separate. Evidence owners: E002 and scoped E006.

#### 4.2 Observed distillation headroom under language-quality coupling

1. How much controlled brain predictivity separates the teacher, initialized students, and distilled students?
2. How does controlled brain predictivity vary with tokenizer-comparable \ac{lm} quality across model families?
3. What relationship remains within the capable-model range?
4. What headroom is supported, and why does its cause remain unresolved?

Evidence owners: E003 and E015. End with the requirement that intervention comparisons be made at comparable \ac{lm} quality; broader causal interpretation belongs in Section 5.

#### 4.3 Recorded-response intervention at valid inference units

1. What positive trend appears when participant-averaged recorded responses are used during training?
2. Which estimand does that averaged-response design support, and why does averaging not create participant-level evidence?
3. What happens when participant-specific responses are used and participants become the inference units?
4. Do the tested loss, adapter-capacity, naturalistic, or full-fine-tuning variants change the verdict?
5. What participant-general claim survives?

Participant averaging and participant-specific analysis are estimand and inference choices within one intervention, not peer experiments. Evidence owners: E004-E005, E008, E010-E011, E013-E014, and E017. Keep the averaging interpretation concise, summarize robustness variants in one compact table, and move their full detail to Appendix E. End with a handoff to the separate synthetic-response route rather than implying that one intervention follows causally from the other.

#### 4.4 Exact synthetic-target measurability on recorded responses

1. Does the exact synthetic target add controlled linear predictivity of recorded responses beyond the frozen nuisance model?
2. Does its increment exceed the inherited internal continuation threshold?
3. Does the aligned target outperform the frozen row-twin control?
4. Which prerequisite is not demonstrated, and which specificity question remains unresolved?

Keep this prerequisite separate from post-training manipulation. Describe the inherited continuation threshold as an internal decision rule, not as an externally justified practical-importance threshold. Evidence owner: E030.

#### 4.5 Synthetic-response manipulation checks and attribution status

1. Can a fresh post-training readout recover the synthetic target from the saved student on held-out WikiText examples relative to seed-matched ordinary distillation?
2. Did the retained student move while \ac{lm} quality remained acceptable?
3. Is fresh Tuckute incremental target retention supported?
4. Is the text-derived auxiliary-control arm sufficiently matched to identify brain-response-specific attribution?
5. What is supported about manipulation, and why does attribution remain non-identifying?

Give the synthetic-target recovery assay, retained-student movement audit, saved-student target-retention analysis, and comparator-adequacy audit distinct verdict paragraphs. Saved block-permuted arms are sensitivity checks rather than peer attribution controls. Evidence owners: E016, E025-E026, and E030.

#### 4.6 Saved-student biological-transfer assays

1. What does the direct participant-level synthetic-response-versus-ordinary-distillation contrast show?
2. What does the synthetic-response-versus-text-derived auxiliary-control contrast show, and why is it non-identifying?
3. What does the frozen composed-path diagnostic observe?
4. What biological-transfer claim is licensed at the participant inference unit?

Separate the direct saved-student biological-transfer assay from the composed-path diagnostic, and report each observation with its uncertainty and verdict. Failure localization and causal explanations belong in Section 5. Evidence owners: E025-E026 and E030.

#### 4.7 Bounded practical-utility evaluation

1. Which recorded-response comparison completed the bounded practical-utility evaluation, and what did it observe?
2. Was the prerequisite contrast in controlled brain predictivity demonstrated, and how do the downstream contrasts compare with their measured sensitivity?
3. What bounded utility claim follows for the tested endpoint?

Classify the prerequisite contrast in controlled brain predictivity as *not demonstrated under the measured minimum detectable effect*, not as absent. Evidence owner: E009. Supporting reproductions, failed instruments, stopped routes, and prospective designs remain in Appendix E.

### 5. Discussion

**Section question.** What does the combined evidence establish about the gap between controlled brain predictivity and a reliable, brain-specific training advantage in the tested systems?

Open Section 5 with one compact synthesis paragraph answering:

1. How can controlled brain predictivity and successful student manipulation coexist with a brain-specific training benefit that is not demonstrated?

The opener owns the thesis-level interpretation and previews localization, compatibility, and design consequences. Do not repeat estimates or enumerate the rows of Table~3.

#### 5.1 Where support is lost across the two intervention routes

1. Where does the recorded-response route first lose support, and how do response averaging, participant-level inference, and the tested variants affect that interpretation?
2. Where does the synthetic-response route first lose support, and why do later target uptake and retained-student movement not change the measurability, attribution, and transfer verdicts?
3. Which explanations are weakened, which remain viable, and why does this pattern support scoped failure localization rather than a causal explanation or universal null?

Treat the two routes separately because they first lose support at different transitions. Do not treat the variant studies as objective- or capacity-invariant failures: E011 did not induce greater effective movement, and E013/E017 close only the tested loss, data, and parameterization regimes. Results Table~4 owns their individual dispositions. Section 6 owns the exhaustive list of untested mechanisms and intervention spaces.

#### 5.2 Compatibility with positive prior studies

1. Why do the intervention and evaluation differences documented in Section 2.3 prevent the present results from directly adjudicating materially different positive studies?
2. How do baseline choice, comparable \ac{lm} quality, comparator validity, endpoint choice, training seeds, and inference unit change what a positive contrast establishes?
3. What does this thesis add without reinterpreting or claiming to refute those prior results?

Section 2.3 owns the factual literature map and unresolved pre-results gap. This subsection owns only the post-results compatibility judgment and must cross-reference, not resummarize, the earlier studies. Design differences establish non-equivalence; do not claim that they caused the different outcomes.

#### 5.3 Design implications for future brain-response-guided training

1. For recorded-response training, how must response construction and the inference unit match the intended participant or population claim?
2. For synthetic targets evaluated through the planned linear assay, what measurability, specificity, and comparator checks should precede training, which diagnostics must be retained, and what would passing these checks still not guarantee?
3. After manipulation succeeds, what matched-control and independent participant-level evidence is required for attribution and biological transfer, and when does a utility test become interpretable within its route?
4. How should supported, not-demonstrated, unresolved, and non-identifying outcomes determine whether a study continues, redesigns its target, control, or assay, or stops downstream testing?

Section 2.4 owns the ex ante evidence standard and comparator catalog. This subsection owns only design changes newly justified by the observed failure locations. Frame them as recommendations supported by the diagnostic logic, not as an experimentally proven universal recipe.
Do not universalize the 50-component \ac{pca} linear measurability screen as a necessary condition for every nonlinear intervention, present comparator matching as sufficient for attribution, or let the recorded-route utility evaluation stand in for an unperformed synthetic-route utility test.

Target one opening paragraph followed by a 3/3/4 paragraph structure across Sections 5.1--5.3, for approximately 1,200--1,300 words in total. Add no new figure unless prose cannot express a genuinely new relationship: Figure~1 already owns the evidence chain and Table~3 owns the role-specific verdicts.

### 6. Limitations

**Section question.** Which populations, constructs, comparisons, and intervention spaces bound the conclusion?

Open with one compact paragraph answering:

1. Why do the route-specific conclusions remain conditional, and which three classes of limitation bound their reach?

The opener must bridge from Section 5 and preview population and measurement coverage, identification and inference, and the intervention and utility space searched. It must not replay results or introduce a new limitation.

#### 6.1 Population, data, and measurement scope

1. What do the tested English stimuli, fMRI cohorts, deeply sampled participants, regions, and response summaries cover?
2. Which modalities, populations, stimulus types, temporal scales, and nonlinear readouts remain untested?

#### 6.2 Identification and inference limitations

1. How do the specified nuisance sets, comparator mismatch, restricted linear readout, 50-component \ac{pca} target assay, unresolved twin contrast, and dependence structures bound identification?
2. Which tested participant-level contrasts and target-measurability increments are disfavored at the internal continuation scales, and which smaller effects, heterogeneous participant effects, or effects in other cohorts remain compatible with the data?

Section 4 owns the exact estimates and intervals. This subsection must cross-reference the relevant Results subsections and state only the scope those bounds support. Appendix D owns estimator and dependence details.

#### 6.3 Intervention and utility scope

1. Relative to the executed model and objective search, which student scales, architectures, objectives, schedules, data scales, target constructions, and personalization strategies remain untested?
2. Why do limited language-quality and downstream endpoints, narrow supporting reproductions, and routes that did not satisfy the requirements for an interpretable utility test leave broader practical utility unresolved?

Keep the recorded-response and synthetic-response utility boundaries separate. Section 4 owns the completed utility and prerequisite verdicts, while Appendix E owns named supporting reproductions and stopped-study details. Section 6 may summarize why those limits leave broader utility unresolved but must not create a second results narrative.

### 7. Conclusion

**Section question.** What final answer should the reader retain?

Two paragraphs:

1. What is the direct, scope-bounded answer for the tested systems?
2. What durable methodological lesson follows about the evidence needed to turn a brain score into a training signal?

## Complete appendix question tree

### Appendix A. Evidence records and provenance

Use a compact disposition index, an argument-ordered scientific-role ledger, a supersession table, and a verified artifact table rather than one prose subsection per record.
Evidence records remain the authority for execution, verdicts, and path--hash bindings; Appendix A provides the reader-facing crosswalk.
Appendix C owns training settings, Appendix D owns estimators and inference, and Appendix F owns complete numerical and sensitivity tables.

1. Which evidence records were executed, unexecuted, precondition-stopped, superseded, or used only for engineering?
2. Which final evidence-record verdict owns each main-text scientific role and claim?
3. Which earlier interpretations were corrected, and which final verdict supersedes them?
4. Which retained artifacts, paths, hashes, and tables are load-bearing for reproduction?

### Appendix B. Data, responses, targets, and controls

#### B.1 Data inclusion and response construction

1. What exact acquisition, inclusion, exclusion, alignment, region, voxel, and reliability rules implement the bounding assay choices introduced in Section 2.1 and summarized in Section 3.1?
2. How are participant-level and averaged responses constructed, and which estimand changes when responses are aggregated?

#### B.2 Stimulus, nuisance, and fold-local preprocessing

1. Which exact low-level, static, and model-derived nuisance features instantiate the control rationale from Section 2.1 in each analysis?
2. Which transforms are fitted inside folds, and which implementation checks realize the contiguous-split and leakage requirements specified in Sections 2.1 and 3.3?

#### B.3 Synthetic brain responses and text-derived auxiliary targets

1. How are the exact TRIBE target, PCA representation, frozen row-twin control, text-derived auxiliary target, and permutations generated?
2. Which construction properties does each control preserve or break, and which attribution question can it answer?

### Appendix C. Training interventions and reproduction

#### C.1 Ordinary distillation and language-quality rules

1. What output-distillation loss, masking, temperature, weighting, data, initialization, schedule, and tokenizer-compatible quality evaluation define the shared language objective?
2. Which model pairs, seeds, saved students, and quality rules are shared or differ across the intervention arms?

#### C.2 Recorded-response intervention

1. What forward and gradient paths, target head, loss, trainable parameter set, and retained student define the common recorded-response intervention?
2. Which implementation element changes in the frozen-readout, contrastive, increased-capacity, naturalistic voxelwise, and full-parameter variants, and which components remain fixed?

#### C.3 Synthetic-response intervention

1. What forward and gradient paths connect the middle-layer representation, temporary target head, KD loss, target loss, later student blocks, and tied output components?
2. What initialization, corpus, schedule, target-loss implementation, and saved-student handling are shared by the synthetic-response, ordinary-distillation, and text-derived auxiliary-control arms?
3. Which saved block-permuted arm is retained only as a sensitivity, and which frozen row twin is evaluation-only rather than a trained arm?

#### C.4 Replay scope and provenance handoff

1. Which hyperparameters, seeds, checkpoints, scripts, and software pins are retained for replaying each load-bearing training family?
2. Which missing revision pins, checkpoints, or historical environment manifests limit exact replay, and where are verified artifact paths, hashes, and evidence dispositions recorded?

### Appendix D. Estimators, aggregation, and inferential scope

#### D.1 Predictive estimands and ridge estimation

1. How are ordinary, nuisance-only, full, semipartial, and population partial \(R^2\) related?
2. How do equal-coordinate averaging and pooled \(\mathrm{SSE}/\mathrm{SST}\) answer different recovery questions?
3. Under which assumptions is ridge a maximum a posteriori estimator, and why is it still only a predictive estimator?

#### D.2 Cross-validation, aggregation, and inference units

1. Which operations are fixed beforehand, and which data-adaptive operations must be learned within each training complement?
2. In what order are coordinates, seeds, folds, stories, and participants aggregated for each scientific role?
3. Why can seeds, folds, voxels, regions, or target coordinates not replace participants as biological inference units?

#### D.3 Uncertainty, multiplicity, and decision rules

1. Which interval, bootstrap, exact test, or sensitivity belongs to each estimand, and what assumptions support it?
2. How are inference units, multiplicity families, and conservative conjunctive decision rules kept distinct?
3. How do minimum detectable effects, language-quality criteria, and prospective continuation thresholds differ, and why can none be promoted into a universal biological-importance criterion?

#### D.4 Information-theoretic boundaries

1. Under which population linear-Gaussian assumptions can partial \(R^2\) be related to conditional mutual information, and why is cross-validated ridge semipartial \(R^2\) not itself a mutual-information estimate?
2. Which conditional-independence relation would be required for a data-processing claim when a synthetic brain-response target is generated deterministically from text?
3. Why do neither output \(\ac{kl}\) matching nor low auxiliary loss determine retained-student movement, brain-response attribution, or biological transfer?

This appendix formalizes the limits introduced conceptually in Section 2.2; it must not turn those limits into empirical explanations or repeat the intervention results.

### Appendix E. Supporting analyses and stopped routes

#### E.1 Pipeline validation and scientific scope

1. Which pipeline components worked when the expected signal was known?
2. Which implementation failures did the diagnostics rule out?
3. Why does synthetic validation establish plumbing rather than scientific evidence?

#### E.2 Response averaging and recorded-response robustness

1. Why do intervention-target averaging and fixed-representation response averaging answer different questions?
2. Which objection did each recorded-response robustness analysis test?
3. What remains supported or open after each test?

#### E.3 Reduced external and cross-modal probes

1. What did each local external-protocol probe test?
2. Which population, substrate, architecture, language, training-scale, or control differences limit comparison with its source study?
3. What is the narrowest supported local conclusion?

#### E.4 Failed instruments and precondition-stopped routes

1. Which prerequisite failed for the shared-response, reading-time, and gaze routes?
2. Was the failure about signal, reference reliability, attribution, leakage, or evaluation substrate?
3. Why did the failure require stopping before intervention or interpretation, and what remains untested?

#### E.5 Prospective designs without empirical evidence

1. What identifying question would each proposed design answer?
2. Which activation, data, or review prerequisite prevented execution?
3. Why do analysis-only screens, validators, reserved designs, and outcome-blind development contribute no empirical evidence?

### Appendix F. Claim-relevant sensitivities and verification tables

#### F.1 Claim-relevant analysis choices

1. Which analyses changed an interpretation or inference unit?
2. Which sensitivities bounded the scope of a main claim?
3. Which checks confirmed local stability or exposed a design limitation?
4. Why can no favorable sensitivity replace a failed frozen primary decision rule?

#### F.2 Participant-level intervention contrasts

1. How is each participant estimand calculated?
2. Why must the recorded-response and biological-transfer assays remain separate?
3. What do mixed signs and participant-deletion checks establish?

#### F.3 Participant-level mechanism diagnostics

1. Which target-measurability and composed-path quantities are reported?
2. Which prerequisite fails first, and which later quantities remain unresolved?
3. What do participant patterns verify without supplying a causal explanation?

#### F.4 Technical-seed diagnostics

1. What does each seed summary measure and aggregate?
2. Which manipulations are stable, and which incremental quantities have mixed signs?
3. Why are seeds not biological inference units?
4. Why is no seed-only table valid for the nonlinear participant-first estimator?

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
