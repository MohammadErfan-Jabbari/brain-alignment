---
title: "Docs Agent Guidance"
tags: [reference, onboarding]
aliases: [docs-agents]
---

# Docs Agent Guidance

This folder is the persistent research brain for the thesis. If a fact matters past the current session, put it in `docs/`; if it is only collaboration/style preference, put it in `../memories/`.

The governing principle is adaptive semistructure: specify only what is critical for shared truth, keep the rest light. Do not recreate a heavy stage machine here.

## Load Order

When entering `docs/` without a narrower task, orient from:

1. `ladder.md` for canonical current status.
2. `upspeed.md` for last-session continuity.
3. `tasks.md` for granular next work.
4. `map.md` when codes or the research arc are unclear.
5. `repo-orientation.md` for the filesystem and evidence-trail map.
6. `../memories/AGENTS.md` for collaboration and prose preferences.

## Rules

- Do not create new `README.md` files under `docs/`; folder-local agent instructions belong in `AGENTS.md`.
- Use standard Markdown links, not wikilinks.
- Keep numbers tied to recorded experiment evidence. Missing numbers are gaps, not estimates.
- `ladder.md` wins over any conflicting status doc.
- Session logs in `timeline/` are immutable; `upspeed.md` is replaced.
- Reports are written full width: one line per paragraph or bullet unless a table/code block requires structure.
- Use absolute dates, never "today" or "last week".
- Negative results are results. Record them in `learnings.md` and the relevant hypothesis or experiment.

## Map

| Path | Holds | Write cadence |
|---|---|
| `ladder.md` | Canonical status board: which rungs hold, with what verdict, and the single next step. | Each session close after verdict confirmation |
| `map.md` | Code legend and full journey tree. Not a status board; `ladder.md` wins. | When rung set or naming changes |
| `upspeed.md` | Current state, blockers, next action. | Every session, replace |
| `tasks.md` | Backlog, now, done. | As tasks move |
| `repo-orientation.md` | Compact filesystem and evidence-trail map for agents. | When structure changes |
| `00-charter.md` | Idea, scope, success and kill criteria. | Rarely |
| `01-research-landscape.md` | Literature frontier, gap, assumptions, controls, baselines. | When literature shifts |
| `02-environment.md` | Compute, data, cached models, how to run. | When environment changes |
| `03-methodology.md` | How the research process works and why. | Rarely |
| `04-data-benchmarks.md` | Powered survey and committed benchmark choice. | When benchmark choice shifts |
| `05-dataset-registry.md` | Living watchlist of candidate datasets. | When a dataset is found |
| `06-theory-grounding.md` | MSc coursework mapped to thesis concepts and formal tools. | When theory becomes load-bearing |
| `07-concepts-primer.md` | Plain-language reusable primitives. | When a recurring primitive needs a home |
| `decisions/decisions.md` | Append-only decision log. | When a real decision is made |
| `timeline/` | Immutable session logs. | End of each session |
| `hypotheses/` | One falsifiable hypothesis per file. | Claim onward |
| `experiments/` | Experiment designs, run logs, and results. | Design onward |
| `reports/` | Continuous current-truth finding reports. See `reports/AGENTS.md`. | As work touches a topic |
| `manuscript/` | Checkpoint-derived LaTeX manuscript layers. See `manuscript/AGENTS.md`. | Only when Erfan calls a checkpoint |
| `literature/canonical/` | One note per paper actually read. | When a paper is read |
| `literature/_prior-work/` | Frozen provenance. | Never edit |
| `references/` | Reusable reasoning frames and conventions. | Rarely |
| `learnings.md` | Durable lessons and corrected mistakes. | When a lesson is learned |
