---
title: "Manuscript Typesetting Preferences"
tags: [memory, feedback, writing]
aliases: [manuscript-typesetting-preferences]
origin_session: "45dd7665-6d83-4be4-a44f-3b94b3bb570d"
source_memory: "/home/centcom/.claude/projects/-home-centcom-data-brain-alignment/memory/manuscript-typesetting-preferences.md"
---

# Manuscript Typesetting Preferences

Two standing rules, both given while reading the submission PDF (2026-09-02):

1. **"there are so many pages that we are wasting a lot of space"**: blank vertical space on a page is a defect, not a cosmetic matter.
2. **"I prefer to keep the tables in one page if they fit in one page. I don't want tables to be broken into multiple pages."**

He also asked the right diagnostic question himself: *should we move content before the figures to fill the pages?* **No.** Hand-moving text is manual repagination; it works once and breaks on the next edit. Every one of these was a one-line structural cause.

**The four causes, and the fixes that held (66 to 61 pages, no prose changed):**
- **`[H]` floats.** 34 of 36 were `[H]`, which forbids the float from moving, so a tall one that does not fit ends the page early. All are `[tbp]` now.
- **NeurIPS sets `\flushbottom`**, which then stretches the slack into mid-page gaps instead of leaving it at the foot. This is the only part the format contributed, and it makes the symptom uglier rather than causing it. `\raggedbottom` plus relaxed float fractions (`\textfraction` 0.07, `\topfraction` 0.9, `\floatpagefraction` 0.85).
- **`\FloatBarrier` immediately after a float.** Harmless while the float was `[H]` and already placed, actively harmful once it can move: it forbids following text from flowing back onto the previous page. This alone stranded a page at 40% full. Removed; `placeins[section]` does the containment, which is load-bearing because without it a table drifted five pages past its successor.
- **`longtable` for a table that fits.** A longtable breaks at a page boundary by design even when the content would fit on a fresh page. Seven of eight became `table[tbp]`; one genuinely overflows by 1515pt and must stay.

**The trap worth remembering: `\@floatboxreset` resets the font to `\normalsize` inside a float.** These tables set their type size in a `\begingroup` *before* `\begin{longtable}`. A longtable is not a float and inherits it; a float does not. Converting therefore silently rendered them at full size. It surfaced only because three tables reported byte-identical overflow after being set to `\scriptsize` (see [Verify the Premise, Not the Logic](verify-the-premise-not-the-logic.md)). Put size and spacing setup **inside** the float.

**A per-paragraph typographic hint goes stale when the paragraph changes.** A `\looseness=-1` placed to save a line on a ten-sentence paragraph was still there after a cut reduced that paragraph to three sentences. Removing it changed nothing: identical page count *and* identical box count, which is how you tell a hint is inert rather than merely small. Delete a `\looseness`, `\enlargethispage`, or manual break whose paragraph has been rewritten, instead of leaving a no-op that the next pass has to re-diagnose.

**One `latexmk -pdf` run does not converge float placement after a reflow (2026-09-02).** A single build reported 60 pages three times for a tree that converges to 58; the count only settles when two consecutive runs agree. Read a page count only after that. And do not attribute a page change to your own edit without isolating it: `git worktree add --detach <commit>` plus a two-pass build per commit is the only honest test. A two-page drop was briefly credited to a Section 3 pass that turned out to have **zero** page effect (60 to 60), because five other sections had been cut in the same window by a parallel session. This is the measurement discipline in [Verify the Premise, Not the Logic](verify-the-premise-not-the-logic.md) applied to page counts: when a number moves, check what else moved with it.

**How to apply:** after any change that reflows the document, rebuild until the page count is stable across two runs, then check four things: page count, `Float too large for page` warnings, zero `continued` markers in `pdftotext` output, and that every float is still in page order (parse `\newlabel` from the `.aux`). Never add `\FloatBarrier`, `\newpage`, or `\enlargethispage` to fix a layout symptom.

**Never verify a build with `latexmk -outdir` pointed away from the source directory (2026-09-02).** It does not read the pinned biber setting the same way, falls back to bibtex, and **truncates the tracked `main-submission.bbl` in the source directory to zero bytes** while writing its own outputs elsewhere. The repo commits the `.bbl` alongside the source on purpose, so this silently destroys a tracked file; `git checkout --` restores it. To check that an edit compiles without touching a tree another session has open, copy the whole submission directory with `cp -rL` into scratch **and create a sibling `rewrite/` holding `numbers.tex`, `acronyms.tex`, and `references.bib`**, because the sources read those across the tree boundary and the build dies with "File `../rewrite/numbers.tex' not found" otherwise. Then run `latexmk -pdf` twice there and read the page count only when two consecutive runs agree.

## Related

- [Verify the Premise, Not the Logic](verify-the-premise-not-the-logic.md)
