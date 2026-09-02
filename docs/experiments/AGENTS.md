---
title: "Experiment Records Agent Guidance"
tags: [agent-contract, experiment]
aliases: [experiments-contract, e-record-contract]
---

# Experiment Records Agent Guidance

This folder is the first of the four authorities: it answers *what was run and what did it produce*. Every scientific number in the thesis is born in `/work` and recorded here, and the manuscript may only report a number this folder already owns. The evidence rules themselves are in the root [`AGENTS.md`](../../AGENTS.md) and [`03-methodology.md`](../03-methodology.md); this file owns the file-level conventions and the traps.

## Naming and identity

`ENNN_kebab-slug.md`, three digits, allocated in order. Start from [`_TEMPLATE.md`](_TEMPLATE.md).

- **An `ENNN` is permanent and never reused**, including for a record that is killed, retracted, or superseded. A retraction stays in place with its verdict corrected; it does not free the number.
- **A gap in the sequence is expected and is not a missing file.** A number can be reserved by a design decision and then deliberately never built: `E007` was not built (D016 part 2, and its power claim is separately retracted in L074), and `E027` was killed before construction because `E025` failed the predeclared participant-general transfer gate. Before treating a gap as an error, grep [`decisions/decisions.md`](../decisions/decisions.md) and [`learnings.md`](../learnings.md) for the identifier.
- The slug names the scientific question, not the script, the model, or the date.

## What a record must carry

The template is the minimum, not the ceiling. Load-bearing entries:

- **Status** on the header line, kept current: `design` / `DESIGN LOCKED` / `running` / `done` / `killed`, plus whether an outcome has been opened.
- **The predeclaration, locked before running:** kill criteria, design, baselines, controls, seeds, stop rule, estimand, estimator, inference unit, and identifying assumptions. A design edited after seeing an outcome is a new record, not a revision of this one.
- **Every quantity the design predeclares reporting must appear in `## Results`.** A design section that says "report X as sensitivity" is a commitment, and the artifact having computed X is not the same as the record stating it. E030 predeclared an MDE and power at its inherited reference, stored both in `analysis.json`, and transcribed neither. Before closing a record, grep its design section for *report* and check that each one landed.
- **Confound controls named explicitly:** contiguous splits, nuisance columns, and confound subtraction for any brain-alignment claim. The reusable battery is [`references/confound-catalog.md`](../references/confound-catalog.md).
- **Results separate from interpretation.** Raw numbers with uncertainty and the named test in `## Results`; what the evidence licenses and what it does not in `## Interpretation`. Do not let a verdict migrate up into the results table.
- **The reason for each non-obvious design choice, recorded when it is made.** Reconstructing it later is how a rationale becomes a guess.
- **Stable paths and SHA-256 values** for the load-bearing gitignored artifacts the manuscript cites, in the record that owns them. Only those; not every intermediate file.

## Traps

- A missing value is a `\gap`, never a guess, and never a number carried over from a sibling record because the pipeline "should be the same".
- A contradiction found while editing a record routes to `/interpret`; it is not resolved here. `/interpret` independently recomputes the load-bearing contrast, and Erfan confirms any changed scientific verdict.
- A verdict that is load-bearing for the manuscript needs an aggregation audit before it is recorded: `stat-aggregation-auditor` re-computes the contrast, and the panel attacks it. A reviewer that shares the working context under-detects (L055).
- Seeds are technical replicates, not biological inference units. Aggregating over seeds when the estimand is participant-level is the failure this project has hit most often; the record must state its inference unit and defend it.
- The `## Iteration log` is append-only. Overwriting a row erases the anomaly that explains the next design.
- Cross-references stay bare identifiers in prose (`E025`) with a relative Markdown link on first mention; `\evd{Ennn}` markers belong in manuscript source, never here.

## Related

- [Docs guidance](../AGENTS.md)
- [Evidence and authority contract](../03-methodology.md)
- [H001 alignment-guided distillation](../hypotheses/H001_alignment-guided-distillation.md)
- [H002 repeat-stable biological supervision](../hypotheses/H002_repeat-stable-biological-supervision.md)
- [Confound catalog](../references/confound-catalog.md)
- [Operational status](../status.md)
