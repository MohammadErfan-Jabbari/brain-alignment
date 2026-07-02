---
title: "Reports Agent Guidance"
tags: [report, reference]
aliases: [reports-agents]
---

# Reports Agent Guidance

A report is a single-topic synthesis kept current. It is not a per-paper note, not the frontier map, and not thesis prose. Reports are the continuous write layer that feeds the extended manuscript at checkpoints.

## Rules

- Do not create a `README.md` here. Folder guidance belongs in `AGENTS.md`.
- Route all report writing through `sci-write-v2`.
- Use flat append-only IDs: `R<NN>_<slug>.md`. Never renumber.
- One durable finding per report, tagged with the ladder question it answers.
- Keep current truth only. Rewrite in place when evidence changes; history lives in `../map.md`, `../timeline/`, and `../decisions/`.
- Only state numbers recorded by a working session or cited from a canonical literature note. Missing numbers are gaps.
- Formalize the core quantity in LaTeX and cite `../06-theory-grounding.md` for formal definitions/bounds where relevant.
- Reports are written full width: one line per paragraph or bullet unless structure requires otherwise.

## Background Reports

| Report | Role |
|---|---|
| `R01_llm-brain-mapping.md` | Linear map between LLM internals and brain activation. |
| `R02_datasets-and-code.md` | Dataset and code provenance across the reading list. |
| `R03_brain-as-training-signal.md` | Early first-principles direction doc through E003. |
| `R04_gap-analysis.md` | Full-PDF re-read of the literature and open gap. |
| `R05_thesis-narrative-from-first-principles.md` | Retired chronological narrative, frozen for history. |

## Finding Reports

Read and write findings in this order:

| Read # | Report | Q | Claim | Status |
|---|---|---|---|---|
| 1 | `R06_alignment-signal-is-real-beyond-confounds.md` | Q0 / A2 | Alignment signal is real beyond artifacts and defines the apparatus. | Written |
| 2 | `R07_plain-kd-does-not-preserve-alignment.md` | Q1 | Plain KD does not preserve alignment by default. | Written |
| 3 | `R08_alignment-objective-has-no-demonstrated-lever.md` | Q2 | The brain-alignment objective has not shown a reliable held-out alignment gain. | Written |
| 4 | R09 | Q3 | No per-individual gain; averaging artifact. | Parked draft `_pending-Q3_*.md` |
| 5 | R10 | Q3 | Null is method-general. | To write |
| 6 | R11 | Q3 | Quality law; matched-perplexity is the missing control. | To write |
| 7 | R12 | Q3 | Stimulus-predictability ceiling, scoped honestly. | To write |
| 8 | R13 | Q3 | External reproduction corroborates failure. | To write |
| 9 | R14 | Q4 / A3 | No practical payoff. | To write |

## Related

- `../ladder.md`
- `../map.md`
- `../manuscript/AGENTS.md`
