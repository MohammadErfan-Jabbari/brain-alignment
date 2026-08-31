---
title: "Methodology — how we work in this repo"
tags: [methodology]
---

# Methodology — how we work in this repo

## The one principle

**Specify only what is critical for shared truth; keep everything else adaptable.** This is a single-paper research workspace. New process earns its place only by preventing a demonstrated scientific or continuity failure.

## Epistemic path

| Phase    | Converts                             | Owner                                                  |
| -------- | ------------------------------------ | ------------------------------------------------------ |
| Notice   | signal → question                    | working note                                           |
| Commit   | question → bounded problem           | [`00-charter.md`](00-charter.md)                       |
| Map      | unknown landscape → frontier         | [`01-research-landscape.md`](01-research-landscape.md) |
| Claim    | uncertainty → falsifiable hypotheses | `hypotheses/HNNN_*.md`                                 |
| Design   | claim → locked fair test             | `experiments/ENNN_*.md`                                |
| Run      | protocol → raw evidence              | artifacts plus the owning E record                     |
| Judge    | evidence → adjudicated verdict       | owning E record, decision, or learning                 |
| Argue    | settled verdicts → paper             | canonical rewrite manuscript                           |
| Compound | finished work → reusable lesson      | [`learnings.md`](learnings.md) and Git                 |

The non-negotiables are competing hypotheses, predeclared kill criteria, a locked design, raw evidence separated from interpretation, at least three seeds for stochastic experiments, contiguous splits and nuisance controls for brain-alignment claims, and uncertainty reported at the correct inference unit.

## Four authorities

| Question                                 | Authority                                                                                                               |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| What was run and what did it produce?    | The owning `experiments/ENNN_*.md` record plus retained load-bearing artifacts                                          |
| What does the thesis currently conclude? | The live body in [`manuscript/rewrite/`](manuscript/rewrite/main-rewrite.tex)                                           |
| Where are we and what happens next?      | [`status.md`](status.md)                                                                                                |
| Why did the project change?              | [`decisions/decisions.md`](decisions/decisions.md), [`learnings.md`](learnings.md), selected durable timelines, and Git |

No other document may compete with these owners. Q/E handles remain the project’s identifiers; there is no separate claim database or global artifact registry.

## Evidence transaction

The normal transaction is:

`artifact → E record → canonical rewrite manuscript when settled and paper-relevant → status when operations change`

- The E record owns the design, provenance, artifact pointers, statistics, and adjudicated experiment verdict.
- The canonical rewrite manuscript owns current scientific interpretation and is corrected when a settled paper-relevant verdict changes.
- `manuscript/submission/` is a supervisor-review derivative of `manuscript/rewrite/`. Accepted scientific changes are synchronized upstream to the rewrite before they are authoritative; never review or apply against the derivative.
- An interrupted manuscript correction immediately sets `manuscript-sync-pending` in `status.md`.
- Corrections append or supersede upstream first. Recording evidence never waits for prose work.
- A newly discovered scientific contradiction routes to `/interpret`; cleanup and writing do not silently adjudicate it.
- Only manuscript-load-bearing gitignored artifacts receive stable paths and SHA-256 values, recorded in their owning E records.

## Numbers and provenance

A scientific number is born in a truth-producing session and recorded in an E record. Manuscript prose may only report values present upstream. A missing value is a `\gap`, never an estimate. Every manuscript evidence marker must resolve to an E record, and deterministic checks enforce unsourced-number, unresolved-evidence, number-consistency, citation, and LaTeX-build rules.

## Interaction stances

The eight stances remain a lightweight vocabulary, not a stage machine. State the active stance and switch when the work changes.

- `/work`: lock, run, and record evidence. Explicit-only.
- `/interpret`: recompute the load-bearing contrast and adjudicate recorded evidence.
- `/write`: draft directly into the canonical rewrite manuscript from E records and the current manuscript.
- `/teach`: transfer understanding without creating scientific truth.
- `/scout`: bring external literature or data into canonical records.
- `/plan`: choose direction without touching numbers.
- `/review`: stress-test a result, claim, design, or manuscript.
- `/meta`: maintain the apparatus.

Strict independent review remains at the two load-bearing boundaries: before a design consumes compute, and after a result or manuscript claim becomes consequential.

## Direct manuscript loop

The writing method is **question-led** and is owned by one skill; the repository gates are owned by one folder contract. Neither is restated here.

- Method: [`question-led-writing`](../.claude/skills/question-led-writing/SKILL.md) (question tree, inference path, Plan/Draft/Review/Revise branches, evidence states, audits).
- Gates and protocol: [`manuscript/AGENTS.md`](manuscript/AGENTS.md) (active tree, provenance, review set, deterministic checks, approval routing).
- Maintained question tree: [`manuscript/rewrite/question-tree.md`](manuscript/rewrite/question-tree.md).

What this contract fixes, and a procedure may not weaken: manuscript prose reports only values recorded upstream; a missing value is a `\gap`; every evidence marker resolves to an E record; deterministic checks and one fresh *independent* review run before a candidate is complete; and Erfan approves a changed scientific verdict, a material change in claim scope, new governing terminology, or a genuinely preference-dependent choice. Reviewed evidence-grounded clarity edits that preserve scientific meaning do not require item-by-item approval ([D067](decisions/decisions.md)).

## Start and close

- `/orient` reads `status.md`, checks Git, and follows only the E/manuscript links required for the first next action.
- During `/work` and `/interpret`, update the owning E record when evidence or its adjudication changes.
- `/wrap` updates only authorities that changed, then commits and pushes scoped changes. A no-op session produces no documentation churn.
- Create a timeline only for a result, adjudication, correction, durable decision or learning, manuscript or submission milestone, or lasting failure. Routine orientation, monitoring, continuation, and formatting work need no timeline.

## Working preferences

- Direct, no ceremony; challenge weak reasoning.
- Use the strongest baseline and name the estimand, estimator, inference unit, uncertainty, and test.
- Fix root causes rather than bypassing blockers.
- Use scoped staging, atomic conventional commits, no amend, and no destructive Git operations without explicit approval. Push completed work to `origin` by default.
- Update the nearest `AGENTS.md` when a folder’s structure, commands, or traps change.

## Reasoning frame

Use the Elon/Feynman/Naval frame in [`references/reasoning-frame.md`](references/reasoning-frame.md): delete false constraints, explain the mechanism and failure boundary plainly, and prefer the smallest durable change that compounds.

## Related

- [`status.md`](status.md) — current operational state
- [`decisions/decisions.md`](decisions/decisions.md) — durable changes and reversals
