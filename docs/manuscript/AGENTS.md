---
title: "Manuscript Agent Guidance"
tags: [manuscript, reference]
aliases: [manuscript-agents]
---

# Manuscript Agent Guidance

## Layout

| Path | Purpose |
| --- | --- |
| `rewrite/` | Canonical LaTeX thesis master and authority for current scientific interpretation |
| `submission/` | Formatting-only supervisor derivative (UC3M cover + NeurIPS body); scientific content unchanged |
| `figures/` | Selected committed figures; generation code lives in `scripts/figures/` |

Legacy layers (`extended/`, `public/v0.9/`) were removed from HEAD on 2026-08-25 and survive only in Git history (last commits `7c445b0` and `6026021`). Do not recreate them; immutable-cut policy applies to any future cut.

## Direct writing loop

1. Read the owning E records and current manuscript section.
2. Read the maintained question map below and apply [`question-led-writing`](../../.claude/skills/question-led-writing/SKILL.md) to the active scope.
3. State the intended answer, claim, scope, caveats, and evidence.
4. Edit `rewrite/` directly. Update this question map in the same change when the manuscript's argument changes.
5. Preserve `\evd{Ennn}` as source-level evidence provenance and keyed values in `numbers.tex`; a missing value is a `\gap`. Evidence identifiers are hidden in the thesis build and may be displayed only for internal review.
6. Run `uv run python .claude/scripts/manuscript_check.py docs/manuscript/rewrite`.
7. Run one fresh independent question-chain, prose, and scientific-scope review and obtain Erfan’s approval for load-bearing framing.

Use `--share-ready` only when no gap remains. A contradiction routes to `/interpret` and sets `docs/status.md` to `manuscript-sync-pending`.

The canonical `rewrite/` manuscript follows its maintained question tree and review contract in [`rewrite/AGENTS.md`](rewrite/AGENTS.md).

## Manuscript-wide terminology

Use the following terms throughout manuscript prose, including abstracts, captions, appendices, and future public cuts:

| Referent | Fixed term |
| --- | --- |
| General biological phenomenon | **brain activity** or **brain responses** |
| Actual measurements | **recorded fMRI responses** |
| Language-model internals | **model representations** or **model activations** |
| TRIBE outputs used in this work | **synthetic brain responses generated from text** |
| Training question | **whether brain responses can help train a smaller model** |
| Brain alignment | Held-out predictivity of recorded fMRI responses from model representations under a declared readout and controls |
| Controlled brain predictivity | Brain alignment after the specified nuisance, split, and control-model checks |
| Recorded brain-response target | A recorded fMRI response when it is used in a training objective |
| Synthetic brain-response target | A synthetic brain response generated from text when it is used in a training objective |
| Target uptake | Recoverability of an optimized training target from retained student representations by a fresh post-training readout |
| Retained-student movement | Parameter or representation difference from the declared training baseline that remains after temporary training components are discarded |
| 50-component linear target-projection measurability | Whether the declared fold-local PCA-50 target representation adds controlled predictivity of recorded fMRI responses beyond nuisance and the frozen row-twin control; this qualifies only that linear pathway |
| Brain-response-specific attribution | Whether the brain-response-target arm outperforms its route-appropriate control on the outcome being claimed: correctly paired versus permuted responses for the recorded-response route, or synthetic brain responses versus a matched text-derived target for the synthetic-response route |
| Biological transfer | Improvement on independently recorded fMRI responses that were not optimized as the training endpoint |
| Brain-specific advantage | Incremental benefit beyond an appropriate text-derived or permuted control, at comparable language-model quality and the correct biological inference unit |
| Claim dependency | Evidence required for one named claim. Do not impose a universal stage order when direct transfer, attribution, linear-pathway evidence, and utility have different dependencies |

Avoid unqualified *neural activity*, *neural representation*, *neural response*, and *neural target* when they could refer either to the biological brain or to a neural network. fMRI records a hemodynamic response associated with brain activity, not neuronal firing directly. Use *response* for what is measured, predicted, or evaluated. Reserve *target* for a response used in a training objective; write *recorded brain-response target* or *synthetic brain-response target* only after identifying its source. Do not write the generic phrase *response target*. Name a control by its construction and the alternative explanation it tests: use *text-feature control*, *text-derived control*, or *matched auxiliary target derived from language-model features*, not *nonbrain control*. Precision comes from naming the source, measurement, role, and comparison of an object, not from the adjective *neural* or a negation such as *nonbrain*.

### Thesis-facing experimental vocabulary

The manuscript rewrite is the thesis content. Organize it by the scientific role that a procedure plays in the argument, never by execution date or evidence-record number.

| Level | Meaning | Canonical terms |
| --- | --- | --- |
| Route | Major source of training supervision | **recorded-response route**, **synthetic-response route** |
| Intervention | Paired training family defined by the manipulated supervision | **recorded-response intervention**, **synthetic-response intervention** |
| Arm or control | Condition within an intervention or assay | **ordinary-distillation arm**, **permuted-response control**, **frozen row-twin control**, **text-derived auxiliary-control arm** |
| Assay | Protocol that measures a declared quantity | **controlled regional predictivity assay**, **controlled naturalistic voxelwise predictivity assay**, **50-component linear target-projection measurability assay**, **synthetic-target recovery assay**, **saved-student biological-transfer assay** |
| Analysis or audit | Contrast, diagnostic, or validity examination | **distillation-headroom analysis**, **retained-student movement audit**, **comparator-adequacy audit and attribution assessment**, **response-averaging analysis** |
| Evaluation | Recurring external endpoint | **language-quality evaluation**, **practical-utility evaluation** |
| Evidence record | Internal provenance owner | `E###` appears only in source provenance, an internal-review build, or the provenance appendix |

Use the shortest canonical term after its first definition. Dataset, model, layer, target dimension, and response construction are qualifiers used only when they distinguish variants. Participant-specific and participant-averaged identify response construction or inference level, not standalone experiments. TRIBE identifies the generator. A text-derived auxiliary target, frozen row twin, or permutation is a control within its owning comparison.

The main thesis argument uses claim-specific dependencies. Controlled predictivity supplies measurement context; route-specific headroom describes opportunity. The 50-component linear target-projection assay qualifies only the declared linear pathway. Direct transfer compares the synthetic-response arm with ordinary KD independently of the text-derived comparator, while brain-response-content attribution additionally requires an adequate nonbrain comparator. Practical utility has its own matched endpoint and, when framed as the payoff of improved controlled predictivity, requires a reliable prerequisite change. Post-training movement is diagnostic, not a comparator-matching condition.

Do not expose evidence-record identifiers in ordinary thesis prose, headings, captions, tables, or result statements. Preserve `\evd{E###}` in source and suppress it in the thesis build. A single provenance appendix may map descriptive scientific roles to evidence records, artifacts, and status.

In LaTeX sources, define each recurring acronym once in the manuscript's acronym registry and use `\ac{key}` or its plural/forced variants in prose. Do not manually write either `full term (SHORT)` or a raw registered short form. Reset acronym state after the abstract with `\acresetall` so the abstract and main text each expand their first use independently.

## Reader-first prose

Precision comes from making the relationship among the claim, comparison, evidence, and scope explicit, not from compressing them into technical labels. Open each paragraph with its answer in language available to the intended reader, then add only nonredundant support. When one sentence carries several independent claims, use parallel grammar or separate sentences so that conjunctions and inference boundaries are unmistakable.

Define a technical object locally far enough for the reader to understand its role. If its exact construction or estimator belongs in Methods, add a concise forward reference rather than either duplicating the procedure or leaving the term unexplained. Describe a comparator by what both arms share and the single component that differs; this makes the alternative explanation being tested visible.

Use mathematical notation when it clarifies an estimand, comparison, aggregation, constraint, or dependency. Introduce symbols before a display. Unless its meaning is already unmistakable, follow each claim-bearing equation with one or two plain-language sentences that state what it computes and why the resulting quantity matters for the current question. Keep compact claim-bearing formulas in the main text when they help the reader follow the argument; place standard machinery, derivations, estimator variants, and implementation details in their owning technical section or appendix. Avoid decorative mathematics and notation that is used only once without improving precision.

Define an object's role positively and assign adjacent roles to their actual section or evidence owner. Avoid repeated “X rather than Y” or “X is not Y” constructions when two direct statements communicate the distinction more clearly.

Match each citation to the claim it actually supports. A general theoretical source does not support an optimization or learnability claim unless it analyzes that mechanism; present an untested mechanism as a hypothesis and cite the closest empirical or methodological literature. Describe permutations by their actual invariants: target permutation preserves target values and their marginal distribution while destroying stimulus--target pairing and joint structure.

After changing prose, recheck the whole active section against the terminology and acronym contracts rather than validating only the edited sentence. Split a paragraph when it serves distinct reader questions, such as reporting findings and stating contributions, and synchronize the maintained question map when that changes the argument's structure.

## Maintained manuscript question map

This map states the reader questions that the canonical rewrite manuscript must answer. It is a writing and review contract, not a scientific authority: E records still own experimental evidence, and `rewrite/` owns the current scientific interpretation.

The map was produced on 2026-07-22 with the Plan branch of [`question-led-writing`](../../.claude/skills/question-led-writing/SKILL.md). The complete manuscript and appendices were inspected, then four independent reviews applied the global decision skills `test-claims`, `remove-bottlenecks`, `allocate-for-compounding`, and `coordinate-strategy`. The reconciled map separates the quantity used to evaluate a frozen student, brain alignment, from the recorded fMRI responses or synthetic brain responses generated from text that are used during training.

### Reader and governing question

**Intended reader.** An ML/NLP reviewer or thesis examiner who understands basic machine learning and statistical evaluation but does not know fMRI encoding, this project's datasets, targets, controls, inference units, or experiment history.

**Governing question.** Can recorded fMRI responses or synthetic brain responses generated from text help train a distilled student and provide a reliable, brain-specific advantage over a matched text-derived control?

**Provisional answer.** In the tested settings, trained language-model representations contain linearly accessible information that predicts held-out fMRI beyond the specified controls. However, objectives based on recorded fMRI responses or synthetic brain responses generated from text do not demonstrate a reliable, brain-specific benefit for distilled students at comparable language-model quality.

**Scope.** This answer is limited to the tested models, English stimuli, datasets, participants, recorded and predicted targets, objectives and optimization regimes, nuisance and intervention controls, linear readouts, comparators, inference units, and evaluation endpoints.

### Front matter and main sections

**Abstract.** What problem was tested, how was the measurement-to-intervention chain evaluated, which parts passed, failed, or remained unresolved, and what scoped answer follows?

**Introduction.** What is brain alignment, how does measuring it differ from using brain responses as training targets, why test brain-response supervision in knowledge distillation, and what evidence would justify a reliable, brain-specific advantage?

**Related work.** Why does prior work on measuring alignment, brain-response-guided optimization, privileged supervision, and compression leave the value of brain-response targets for controlled distillation unresolved?

**Methods.** How does the study instantiate each scientific role with one study-specific design tuple comprising its data or response construction, intervention or assay, comparator, estimand, endpoint, and inference unit?

**Results by Scientific Claim.** Which scientific roles are supported, not demonstrated, unresolved, or non-identifying at their declared inference units, and what narrow claim does each result license?

**Discussion.** Which route-specific claims are supported or limited, which explanations are ruled out or remain possible, and what must future brain-guided training studies demonstrate?

**Limitations.** Which properties of the participants, stimuli, targets, models, controls, readouts, interventions, statistical power, external reproductions, and downstream tasks bound the interpretation?

**Conclusion.** What final, scope-bounded answer follows from the evidence and its limitations?

### Appendices

**Appendix A.** Which evidence records and artifacts support each thesis-facing scientific role, and which earlier interpretations were superseded?

**Appendix B.** What do supporting analyses, diagnostics, failed instruments, stopped routes, and future designs contribute to the main evidence chain?

**Appendix C.** Which formal assumptions, estimators, inference units, and sensitivity analyses are required to interpret the main claims?

### Maintenance rule

Treat this as a maintained reverse outline. Every main-text paragraph must answer a leaf question that contributes to its section question and ultimately to the governing question. Whenever a manuscript edit changes a section's purpose, evidentiary role, scope, or conclusion, update the affected question here in the same commit. When a changed E-record verdict alters the argument, correct the E record first, route the change through `/interpret`, update the manuscript, and then synchronize this map. Remove questions that no longer serve the governing question and add a question when the manuscript gains a necessary argumentative dependency. Review the complete map before declaring the manuscript share-ready.

## Rules

- Do not create a manuscript report, claim lattice, checkpoint log, convergence store, or any additional alternate draft tree beyond the explicitly authorized `rewrite/` candidate.
- Public cuts are frozen. A new milestone creates a new version.
- Every scientific number and figure value traces to an owning E record; only load-bearing artifacts receive recorded paths and SHA-256 values.
- Use the correct inference unit, uncertainty, and named test.
- Keep internal provenance in non-printing BibLaTeX fields such as `annotation`, not printable `note` fields.
- Keep source search-friendly: one sentence or paragraph per line, minimal custom macros, and no deep content nesting.
- For dense mapping tables, separate compact identifiers from descriptive labels, give the flexible-width column to the substantive comparison, and use the full text width before reducing font size. Keep conceptually distinct evidence stages in separate rows.
- Do not create a README; folder guidance belongs here.

## Figure path

`scripts/figures/ → outputs/figures/ (gitignored) → docs/manuscript/figures/ (selected and committed)`

## Related

- [Authority contract](../03-methodology.md)
- [Current status](../status.md)
