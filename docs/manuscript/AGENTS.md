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

## Maintained manuscript question map

This map states the reader questions that the extended manuscript must answer. It is a writing and review contract, not a scientific authority: E records still own experimental evidence, and the extended manuscript still owns the current scientific interpretation.

The map was produced on 2026-07-22 with the Plan branch of [`question-led-writing`](../../.claude/skills/question-led-writing/SKILL.md). The complete manuscript and appendices were inspected, then four independent reviews applied the global decision skills `test-claims`, `remove-bottlenecks`, `allocate-for-compounding`, and `coordinate-strategy`. The reconciled map separates the quantity used to evaluate a frozen student, brain alignment, from the recorded or predicted neural-response targets used during training.

### Reader and governing question

**Intended reader.** An ML/NLP reviewer or thesis examiner who understands basic machine learning and statistical evaluation but does not know fMRI encoding, this project's datasets, targets, controls, inference units, or experiment history.

**Governing question.** Can supervision from recorded or predicted neural responses give a distilled student a reliable, brain-specific advantage over matched non-neural training?

**Provisional answer.** In the tested settings, trained language-model representations contain linearly accessible information that predicts held-out fMRI beyond the specified controls. However, the tested recorded- and predicted-neural-target objectives do not demonstrate a reliable, brain-specific benefit for distilled students at comparable language-model quality.

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
