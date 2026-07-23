---
title: "Claim-led manuscript rewrite completed"
tags: [timeline, manuscript, write, review]
aliases: [claim-led-rewrite-complete]
---

# Claim-led manuscript rewrite completed

## Stance

`/write` with a bounded `/interpret` correction, followed by `/review`.

## What changed

A new manuscript was written from scratch in `docs/manuscript/rewrite/` while the extended manuscript and frozen public v0.9 cut were preserved unchanged.
The candidate organizes the study around the evidence needed to turn a controlled brain score into a valid training claim: controlled measurability, quality-aware headroom, exact-target measurability where applicable, target uptake, retained-student movement, comparator validity, participant-level biological transfer, and external utility.
It distinguishes recorded-response targets from predicted neural targets, keeps participant, fold, story, voxel, coordinate, and technical-seed inference roles separate, and carries one scoped verdict from the abstract through the conclusion and Appendices A--F.

Repeated four-skill structure, section, and whole-paper reviews converged with the same senior research-writer agent applying each accepted revision.
The final manuscript adds two conceptual diagrams, one participant-level evidence figure, comparison and verdict tables, explicit data and target construction, gradient-path and retained-component documentation, estimator and inference definitions, a complete experiment-disposition ledger, verified artifact hashes, and participant and technical-seed tables.

During figure verification, E008's owning record was corrected from stale within-person mean wording to the participant median actually used by the predeclared procedure and all retained values.
Independent recomputation reproduced every reported E008 participant effect and the cohort interval; no scientific number or verdict changed.
The rewrite uses the corrected estimator, while the extended manuscript remains intentionally untouched and is therefore `manuscript-sync-pending` for that wording.

## Validation

- `uv run python .claude/scripts/manuscript_check.py docs/manuscript/rewrite --share-ready` passes for all 16 source files.
- An uncontended clean `latexmk -pdf main-rewrite.tex` build produces a 47-page A4 PDF with no LaTeX/package errors, undefined citations or references, rerun warnings, or overfull boxes.
- The final PDF was rendered with Poppler and every page was visually inspected for clipping, overlap, table and figure legibility, typography, page numbering, section transitions, and reference formatting.
- Four independent whole-manuscript reviewers converged, and focused post-read checks confirmed the E008 median wording, WikiText-versus-Tuckute retention scope, acronym pluralization, and cross-references.
- `git diff --check` passes, and `docs/manuscript/extended/` has no changes.

## Boundary

The rewrite is a share-ready candidate, not an automatic authority cutover.
The owning E records remain authoritative for experiments and values; the extended manuscript remains the current manuscript authority until Erfan approves promotion or synchronization; creating a new public cut remains a separate explicit decision.

## Related

- [Project status](../status.md)
- [Claim-led rewrite source](../manuscript/rewrite/main-rewrite.tex)
- [Claim-led rewrite PDF](../manuscript/rewrite/main-rewrite.pdf)
- [Extended manuscript](../manuscript/extended/main-extended.tex)
- [E008 participant intervention](../experiments/E008_per-participant-f1-solidification.md)
