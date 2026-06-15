# LaTeX conventions for the extended and public manuscripts

The layer model itself (what each manuscript is, its cadence, its triggers) is defined once in
`docs/03-methodology.md` ("Deliverable layers"), which is the source of truth. This reference holds only
the LaTeX-specific conventions: how the source is written, what the shared assets are, and how a frozen
cut stays frozen. Read it when writing or consolidating an extended or public manuscript.

## Search-friendly source style

Write one sentence per source line. Do not hard-wrap a sentence across lines, and do not pack several
sentences onto one line. This single habit claws back most of the search penalty of LaTeX versus Markdown:
a grep for a concept returns a whole thought, and a git diff is sentence-level rather than a reflowed
paragraph. It costs nothing and it makes the source behave like the Markdown reports the manuscript is
consolidated from.

Keep content out of deep environment nesting where you can. Prose belongs in the document body, not buried
three environments down.

## The shared preamble and semantic macros

Both manuscripts build on `assets/preamble.sty`. It defines the recurring objects as macros so they read
identically everywhere and stay greppable:

- Concepts: `\Lbrain` (the brain loss), `\uniqueR` (unique R²), `\Eys` (E[Y|S]), and the small set of
  others the work actually repeats. Keep the set small; a sprawling macro library hurts both grep and a
  new reader.
- Provenance: `\evd{Ennn}` (renders a light inline tag in the extended draft), `\gap{...}` (renders a
  visible flag), `\result{key}` (pulls a keyed number from `assets/numbers.tex`).
- Figures: `\safeimage`, which renders a labelled placeholder box when a figure file is missing instead of
  failing silently. Our figure renders are gitignored and regenerated, so this prevents blank gaps.

A small, semantic macro set is also what makes the extended-to-public compression lexical rather than a
re-port: a section copied down compiles unchanged.

## The vendored-frozen-cut rule

A public `vN` is a frozen snapshot. It must carry its own copy of the preamble and the `.bib`, not
`\input` a living shared file, because a frozen cut that imports a changing preamble is not frozen: a
later edit would silently change how a year-old cut compiles. So at cut time, vendor (copy) the preamble,
`numbers.tex`, and `references.bib` into the `vN` directory. The extended manuscript, which is living,
tracks the shared assets directly.

## Provenance in a public cut

A public cut drops the extended manuscript's derivations and mechanics, but a reviewer still needs the
number-to-evidence trail. Keep the `\evd` tags and render them into an evidence-map appendix (the v0 draft
already uses this pattern: an "Evidence map, every results number to its source" section). Do not strip
provenance for readability; move it to the appendix.

## Build

Build with `latexmk` via the committed `assets/latexmkrc`, which pins the engine and the bib backend so a
supervisor never hand-runs the multi-pass or picks the wrong backend. Commit the compiled PDF and the
`.bbl` alongside the source so sharing never depends on the recipient's toolchain.
