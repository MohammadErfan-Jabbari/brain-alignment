---
title: "Extended manuscript synchronized through E026"
tags: [timeline, manuscript, write, review]
aliases: [extended-manuscript-e026-sync]
---

# Extended manuscript synchronized through E026

## Stance

`/write` → `/review`

## What changed

The extended manuscript was revised in four rounds. The abstract and introduction now lead with the identified recorded-fMRI contrast; the related-work section incorporates the latest verified intervention literature; the Results section separates estimands, inference units, proxy uptake, model movement, comparator identification, and biological transfer; and the Discussion, Limitations, and Conclusion now carry the same direct-first interpretation and scope.

The E025 direct TRIBE-minus-KD estimate is presented as the net saved-arm effect on recorded fMRI. The preregistered relative comparison is reported with its internal continuation threshold but is not used to identify neural target content after E026. The E026 comparator audit now precedes any cross-target interpretation, and the failed comparator does not erase E016's within-TRIBE target-learning result.

The revision also replaced internal project jargon, removed promotional or causal wording that exceeded the evidence, clarified that E008's `+0.003` value is a post-run power reference rather than a predeclared effect, and removed every rendered em dash. The frozen public v0.9 cut was not changed.

## Validation

- `uv run python .claude/scripts/manuscript_check.py docs/manuscript/extended` passed after the final revision.
- The repository anti-AI prose linter passed every manuscript section with zero findings or warnings.
- Source, rendered-text, LaTeX-warning, and whitespace scans were clean; the affected PDF pages were visually inspected.
- Each manuscript round received independent Elon, Feynman, and Naval review. Round 4 was revised until all three returned `PASS`.

## Boundary

No scientific number was created or changed during writing. The owning E records remain authoritative. The live manuscript is synchronized, but author approval is still required before `share-ready` is restored.

## Related

- [Project status](../status.md)
- [Extended manuscript](../manuscript/extended/main-extended.tex)
- [E025 participant transfer](../experiments/E025_participant-e016-biological-transfer.md)
- [E026 comparator audit](../experiments/E026_tribe-textfeat-target-comparability.md)
