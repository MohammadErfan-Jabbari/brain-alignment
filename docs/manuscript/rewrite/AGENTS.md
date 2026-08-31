---
title: "Canonical Thesis Manuscript Contract"
tags: [manuscript, rewrite, question-led-writing]
aliases: [rewrite-contract]
---

# Canonical Thesis Manuscript Contract

## Status and authority

This directory is the canonical thesis manuscript. It uses settled evidence from the owning E records and must not silently change an E-record verdict.

This directory owns the current scientific interpretation and must remain independently buildable. The legacy `../extended/` snapshot was removed from HEAD on 2026-08-25 and survives only in Git history (last commit `7c445b0`); any historical consultation reads from there.

Writing methodology — drafting and review protocol, acceptance checks, terminology, prose, structure, table, and figure rules — is unified in [`../AGENTS.md`](../AGENTS.md) and applies to this tree. This file holds only what is specific to the canonical thesis: its scientific position, argument structure, role contract, and attention budget. The question tree itself sits in [`question-tree.md`](question-tree.md).

## Reader, governing question, and answer

**Intended reader.** An ML/NLP reviewer or thesis examiner who understands basic machine learning and statistical evaluation but does not know fMRI encoding, this project's datasets, targets, controls, inference units, or experiment history.

**Governing question.** Under what conditions can recorded fMRI responses or synthetic brain responses generated from text provide a reliable, brain-specific training advantage to a compressed language model, and which route-specific claims are supported, unresolved, non-identifying, or not demonstrated?

**Provisional answer.** Trained language-model representations contain information useful for predicting held-out recorded fMRI responses beyond the implemented nuisance designs. The regional trained-minus-untrained comparison does not isolate learned parameters because its static nuisance block is model-specific. The observed teacher--student gap is coupled to language-model quality and is not route-general. The tested recorded-response objectives do not demonstrate a reliable participant-level benefit. Synthetic brain responses generated from text are learnable and change retained student representations without unacceptable language-quality loss, but the declared 50-component linear target-projection assay does not support the proposed linear pathway, the text-derived auxiliary-control arm cannot identify brain-response content, and direct participant-level biological transfer is not demonstrated. The evidence supports claim-specific measurement, manipulation, attribution, transfer, and utility tests, not a successful brain-response-guided distillation method.

**Scope.** The answer is limited to the tested models, English stimuli, datasets, participants, targets, objectives, optimization regimes, nuisance and intervention controls, linear readouts, comparators, inference units, and endpoints.

## Structural rules

The general prose, structure, table, and figure rules live in [`../AGENTS.md`](../AGENTS.md). The rules below are specific to this tree's argument.

- Organize the argument by claims and their dependencies, not experiment order. Use *role* or the fixed assay name for a scientific test and *criterion*, *threshold*, or *check* for operational continuation rules. Do not imply that every claim follows one universal sequence.
- Main-text theory must change the interpretation of an estimand or control. Put non-decisive derivations and analogies in Appendix D.
- Give each figure one relationship to explain. In Section 3, data routing, competing readouts, intervention mechanics, and inference-unit aggregation have separate owners; do not redraw the Section 2 claim-dependency graph or the Results verdict table inside them.

## Thesis-facing scientific-role contract

This rewrite is the thesis content. Organize the narrative by the role a procedure plays in the scientific argument, not by experiment chronology or evidence-record number.

| Level | Definition | Fixed terms |
| --- | --- | --- |
| Route | Major source of training supervision | **recorded-response route**, **synthetic-response route** |
| Intervention | Paired training family defined by the manipulated supervision | **recorded-response intervention**, **synthetic-response intervention** |
| Arm or control | Condition inside an intervention or assay | **ordinary KD arm**, **permuted-response control**, **frozen row-twin control**, **text-derived auxiliary-control arm** |
| Assay | Protocol measuring a declared quantity | **controlled regional predictivity assay**, **controlled naturalistic voxelwise predictivity assay**, **50-component linear target-projection measurability assay** (short form **target-projection assay**), **synthetic-target recovery assay**, **saved-student biological-transfer assay** |
| Analysis or audit | Contrast, diagnostic, or validity examination | **distillation-headroom analysis**, **retained-student movement audit**, **comparator-adequacy audit and attribution assessment**, **saved-student target-retention analysis**, **composed-path diagnostic**, **response-averaging analysis** |
| Evaluation | Recurring external endpoint | **language-quality evaluation**, **practical-utility evaluation** |
| Evidence record | Internal provenance owner | `E###` appears only in source provenance, an internal-review build, or the provenance appendix |

Use the shortest fixed term after first definition. Dataset, model, layer, target dimension, and response construction are qualifiers used only when they distinguish variants. Participant-specific and participant-averaged identify response construction or inference level, not standalone experiments. TRIBE identifies the generator. The text-derived auxiliary target, frozen row-twin control, and permutations are controls within their owning comparisons.

The main argument moves from measurement to route-specific opportunity evidence and then to intervention claims. Controlled brain predictivity supports a measurement claim. Distillation headroom is an opportunity diagnostic whose interpretation is route- and quality-dependent. The 50-component target-projection assay licenses only claims about the declared linear synthetic-target pathway. Target recovery and retained-student movement are manipulation checks within the synthetic-response intervention. A direct arm contrast can test biological transfer independently of the target-projection assay or text-derived comparator. Brain-response-specific attribution additionally requires a route-appropriate identifying control. Practical utility requires its own endpoint comparison and cannot be inferred from an MDE alone.

Supporting robustness analyses remain subordinate to the owning intervention or assay. Pipeline validation, failed instruments, reduced reproductions, stopped feasibility routes, and unexecuted designs belong in descriptively titled appendix or future-work categories. Never present them as completed headline experiments.

Do not expose evidence-record identifiers in ordinary thesis prose, headings, captions, tables, or result statements. Preserve `\evd{E###}` in source. The thesis build suppresses those markers, while Appendix A maps descriptive roles to evidence records, artifacts, and status.

### Layer ownership and handoffs

| Layer | Exclusive responsibility |
| --- | --- |
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

Language-quality evaluation is a cross-cutting endpoint and criterion. Section 3 summarizes its protocol, Section 3.5 states acceptability rules, Appendices C and D own implementation, and Section 4 reports route-specific values and verdicts. The 50-component linear target-projection assay follows the same handoff: target construction in Appendix B, assay summary in Section 3, estimator in Appendix D, and verdict in Section 4.

## Attention budget

Target 9,000 to 10,000 main-text words, or roughly 21 to 23 A4 pages excluding references: about 2 pages for the Introduction, 3 for Section 2, 4 to 4.5 for Section 3, 7 to 8 for Results, 2.5 for Discussion, 1 to 1.5 for Limitations, and 0.5 for the Conclusion. Keep Section 2.3 within about 700 to 900 words and Sections 4.3 and 4.5 within about 1,000 to 1,200 words each. Preserve Results as the largest allocation.

Treat roughly 20 to 24 appendix pages as a planning band, not a compression target. Completeness means that every scientific role, supporting analysis, evidence record, and load-bearing claim is accounted for, not that every stored numerical row or machine-level artifact listing is reproduced. Leave exhaustive grids and artifact metadata in the owning E records and retained artifacts.

Give the three evidence-chain artifacts different jobs. The Section 2 figure defines the conceptual stages and claim meanings. The Section 3 table maps each stage to its canonical scientific role, estimand, comparator, endpoint, inference unit, and evidence owner. The Results table reports only the verdict and strongest evidence. Do not restate the full chain in the prose around all three.

## Stable terminology

Terminology and acronym rules follow the [manuscript-wide terminology contract](../AGENTS.md), including its citation-matching and permutation-invariant rules. The scientific-role contract above adds this tree's fixed role terms.

## The maintained question tree

The tree itself lives in [`question-tree.md`](question-tree.md), one leaf question per prose paragraph, main text and appendices. It is a separate file so that a manuscript edit does not load it unasked; read it whenever the argument's structure is in play, and update it in the same change as the prose whenever that structure moves.

A paragraph may answer two adjacent leaves only when separating them would create two fragments and their evidence owners are compatible. A paragraph with no leaf to answer is a signal to fix the tree or to cut the paragraph, never to draft around it.

## Drafting and review protocol

Drafting, review rounds, and section acceptance checks follow the [unified protocol and acceptance checks](../AGENTS.md) in the parent manuscript guidance. The leaf questions that protocol operates on are the ones in [`question-tree.md`](question-tree.md).

## Related

- [Maintained question tree](question-tree.md)
- [Manuscript guidance](../AGENTS.md)
- [Evidence and authority contract](../../03-methodology.md)
- [Operational status](../../status.md)
