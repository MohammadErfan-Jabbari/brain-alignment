---
title: "Manuscript Agent Guidance"
tags: [manuscript, reference]
aliases: [manuscript-agents]
---

# Manuscript Agent Guidance

## Layout

| Path | Purpose |
|---|---|
| `extended/` | Live LaTeX master and authority for current scientific interpretation |
| `rewrite/` | Independently buildable claim-led candidate; non-authoritative until Erfan explicitly approves replacement |
| `public/vN/` | Immutable sharing/submission cuts derived from the extended master |
| `figures/` | Selected committed figures; generation code lives in `scripts/figures/` |

## Direct writing loop

1. Read the owning E records and current manuscript section.
2. Read the maintained question map below and apply [`question-led-writing`](../../.claude/skills/question-led-writing/SKILL.md) to the active scope.
3. State the intended answer, claim, scope, caveats, and evidence.
4. Edit the extended manuscript directly. Update this question map in the same change when the manuscript's argument changes.
5. Preserve `\evd{Ennn}` and keyed values in `numbers.tex`; a missing value is a `\gap`.
6. Run `uv run python .claude/scripts/manuscript_check.py docs/manuscript/extended`.
7. Run one fresh independent question-chain, prose, and scientific-scope review and obtain Erfan’s approval for load-bearing framing.

Use `--share-ready` only when no gap remains. A contradiction routes to `/interpret` and sets `docs/status.md` to `manuscript-sync-pending`.

The user-authorized `rewrite/` candidate follows its own maintained question tree and review contract in [`rewrite/AGENTS.md`](rewrite/AGENTS.md). Work there must not modify `extended/`, and its prose does not become the current scientific authority merely by compiling or passing review.

## Manuscript-wide terminology

Use the following terms throughout manuscript prose, including abstracts, captions, appendices, and future public cuts:

| Referent | Fixed term |
|---|---|
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
| Retained-student movement | Parameter or representation change that remains after the temporary training head is discarded |
| Exact-target measurability | Whether the exact training target adds controlled, practically relevant predictivity of recorded fMRI responses on the intended biological substrate under the frozen assay |
| Comparator validity | Whether a text-derived control permits attribution to brain-response content rather than geometry, scale, learnability, or optimization pressure |
| Biological transfer | Improvement on independently recorded fMRI responses that were not optimized as the training endpoint |
| Brain-specific advantage | Incremental benefit beyond an appropriate text-derived or permuted control, at comparable language-model quality and the correct biological inference unit |

Avoid unqualified *neural activity*, *neural representation*, *neural response*, and *neural target* when they could refer either to the biological brain or to a neural network. fMRI records a hemodynamic response associated with brain activity, not neuronal firing directly. Use *response* for what is measured, predicted, or evaluated. Reserve *target* for a response used in a training objective; write *recorded brain-response target* or *synthetic brain-response target* only after identifying its source. Do not write the generic phrase *response target*. Name a control by its construction and the alternative explanation it tests: use *text-feature control*, *text-derived control*, or *matched auxiliary target derived from language-model features*, not *nonbrain control*. Precision comes from naming the source, measurement, role, and comparison of an object, not from the adjective *neural* or a negation such as *nonbrain*.

In LaTeX sources, define each recurring acronym once in the manuscript's acronym registry and use `\ac{key}` or its plural/forced variants in prose. Do not manually write either `full term (SHORT)` or a raw registered short form. Reset acronym state after the abstract with `\acresetall` so the abstract and main text each expand their first use independently.

## Reader-first prose

Precision comes from making the relationship among the claim, comparison, evidence, and scope explicit, not from compressing them into technical labels. Open each paragraph with its answer in language available to the intended reader, then add only nonredundant support. When one sentence carries several independent claims, use parallel grammar or separate sentences so that conjunctions and inference boundaries are unmistakable.

Define a technical object locally far enough for the reader to understand its role. If its exact construction or estimator belongs in Methods, add a concise forward reference rather than either duplicating the procedure or leaving the term unexplained. Describe a comparator by what both arms share and the single component that differs; this makes the alternative explanation being tested visible.

After changing prose, recheck the whole active section against the terminology and acronym contracts rather than validating only the edited sentence. Split a paragraph when it serves distinct reader questions, such as reporting findings and stating contributions, and synchronize the maintained question map when that changes the argument's structure.

## Maintained manuscript question map

This map states the reader questions that the extended manuscript must answer. It is a writing and review contract, not a scientific authority: E records still own experimental evidence, and the extended manuscript still owns the current scientific interpretation.

The map was produced on 2026-07-22 with the Plan branch of [`question-led-writing`](../../.claude/skills/question-led-writing/SKILL.md). The complete manuscript and appendices were inspected, then four independent reviews applied the global decision skills `test-claims`, `remove-bottlenecks`, `allocate-for-compounding`, and `coordinate-strategy`. The reconciled map separates the quantity used to evaluate a frozen student, brain alignment, from the recorded fMRI responses or synthetic brain responses generated from text that are used during training.

### Reader and governing question

**Intended reader.** An ML/NLP reviewer or thesis examiner who understands basic machine learning and statistical evaluation but does not know fMRI encoding, this project's datasets, targets, controls, inference units, or experiment history.

**Governing question.** Can recorded fMRI responses or synthetic brain responses generated from text help train a distilled student and provide a reliable, brain-specific advantage over a matched text-derived control?

**Provisional answer.** In the tested settings, trained language-model representations contain linearly accessible information that predicts held-out fMRI beyond the specified controls. However, objectives based on recorded fMRI responses or synthetic brain responses generated from text do not demonstrate a reliable, brain-specific benefit for distilled students at comparable language-model quality.

**Scope.** This answer is limited to the tested models, English stimuli, datasets, participants, recorded and predicted targets, objectives and optimization regimes, nuisance and intervention controls, linear readouts, comparators, inference units, and evaluation endpoints.

### Front matter and main sections

**Abstract.** What problem was tested, how was the measurement-to-intervention chain evaluated, which parts passed, failed, or remained unresolved, and what scoped answer follows?

**Introduction.** What is brain alignment, how does measuring it differ from using neural responses as training targets, why test neural-response supervision in knowledge distillation, and what evidence would justify a reliable, brain-specific advantage?

**Related work.** Why does prior work on measuring alignment, neural-guided optimization, privileged supervision, and compression leave the value of neural targets for controlled distillation unresolved?

**Methods.** How does the study separately test controlled measurability, language-quality preservation, target uptake, retained-student movement, comparator validity, participant-level transfer, and downstream utility using appropriate estimands, controls, and inference units?

**Results.** For each part of the evidence chain, what did the experiments establish, fail to establish, or leave unresolved at its declared inference unit?

**Discussion.** Where does the evidence chain break, which explanations are ruled out or remain possible, and what must future brain-guided training studies demonstrate?

**Limitations.** Which properties of the participants, stimuli, targets, models, controls, readouts, interventions, statistical power, external reproductions, and downstream tasks bound the interpretation?

**Conclusion.** What final, scope-bounded answer follows from the evidence and its limitations?

### Appendices

**Appendix A.** Which experiments support the manuscript, and which earlier interpretations were superseded?

**Appendix B.** What do secondary experiments, diagnostics, and failed instruments contribute to the main evidence chain?

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
- Do not create a README; folder guidance belongs here.

## Figure path

`scripts/figures/ → outputs/figures/ (gitignored) → docs/manuscript/figures/ (selected and committed)`

## Related

- [Authority contract](../03-methodology.md)
- [Current status](../status.md)
