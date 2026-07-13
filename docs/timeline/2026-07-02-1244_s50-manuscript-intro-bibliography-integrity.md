---
title: "S50 - manuscript intro and bibliography integrity"
tags: [timeline, session]
---

# S50 - manuscript intro and bibliography integrity

## Purpose

Prepare the supervisor-facing v0.2 manuscript and email by fixing the final Introduction opening/body and verifying the rendered citation list before Erfan sends the draft.

## Stances

Dominant stance: `/write`.

Also used: `/meta` for the bibliography-integrity repair and session close.

## What happened

- Oriented on the manuscript state and the supervisor-send context.
- Reworked the Introduction opening so it starts from the established brain-alignment literature, then moves to the measurement-to-training inversion and the distillation question.
- Revised the Introduction body to match the new opening: problem, weak-prior hypothesis, positioning, measurement caution, contribution list, and program sequence.
- Added more citations to the Introduction, while keeping the tone and current manuscript style.
- Added the requested `Note.` before the contribution list explaining that the list is intentionally granular in this progress draft and will be curated later.
- Drafted a concise supervisor email for Alex and Pablo, including the submitted title, the requested 14-18 September defense week, the v0.2 attachment note, and the IMDEA external-supervisor explanation.
- Audited the rendered bibliography after Erfan caught that citation [5] had a fake/search-hostile title.
- Corrected shorthand/fake bibliography metadata in `docs/manuscript/extended/references.bib`, including `gao2024`, `hadidi2026`, `jia2026`, `negi2025`, `moussa2025`, `moussa2025b`, `bilgin2026`, `merlin2026`, `oota2026`, `merlin2024`, `alkhamissi2025`, `pirlot2022`, `freteault2025`, `cheng2026`, `yu2026`, `groger2026`, and `lage2019`.
- Moved internal bibliography comments from printed `note` fields to non-printing `annotation` fields, then rebuilt the PDF.

## Decisions made

- Keep the citation keys stable even when the printed metadata changes; for example, the key `gao2024` now prints the real 2025 Nature Computational Science article metadata.
- Use `annotation` rather than `note` for internal bibliography provenance/comments because `note` is rendered in the supervisor-facing reference list.

## Current truth

No experiment ran, no science number was produced, no result was reinterpreted, and no ladder rung changed. Q0-Q5 stand exactly as before.

The current supervisor-facing PDF is `docs/manuscript/extended/main-extended.pdf`. The bibliography now uses searchable titles and DOI/arXiv/ACL metadata where available. The citation registration check found 24 unique cited keys and all 24 are present in the `.bib`, `.bcf`, and `.bbl`.

The final checks run:

- `tectonic --keep-intermediates --keep-logs --reruns 2 main-extended.tex`
- `python3 .claude/skills/sci-write-v2/scripts/consistency_check.py validate docs/manuscript/extended/main-extended.tex`
- log scan for undefined citations/references and Biber warnings
- rendered reference-list spot-check with `mutool draw -F txt`

`consistency_check: PASS`; no missing/undefined citation warnings remain.

## Next session

- Immediate administrative step: send the supervisor email with `docs/manuscript/extended/main-extended.pdf` attached.
- If doing one more prose pass before sending, review the abstract so it matches the new confident Introduction opening.
- After the send, resume the manuscript default: `/write` Section 4.3 / Q2 and Figure 6, keeping the E004 fold-level caveat.

## Friction & improvements

- The wrap start marker is stale: `.claude/state/wrap/start.json` points to `46bca0d`, so `start_sha..HEAD` spans many committed sessions and is too broad for this S50 close. This close used the current conversation plus the post-S49 manuscript commits as the practical scope.
- `.claude/state/register/verdict.json` is missing, so the current manuscript bytes do not have a recorded clean register verdict. This is an open `/write` quality loop, not a citation/build blocker.
- A rendered PDF reference-list audit is necessary before supervisor sends. BibTeX keys resolving is not enough: fake titles and printed internal notes can still ship.

## Related

- `../upspeed.md`
- `../tasks.md`
- [`../manuscript/extended/references.bib`](../manuscript/extended/references.bib)
- [`../manuscript/extended/main-extended.pdf`](../manuscript/extended/main-extended.pdf)
