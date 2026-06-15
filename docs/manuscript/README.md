# manuscript/ — the thesis, built from recorded evidence

This is the home for the LaTeX manuscripts in two sublayers (D035): `extended/` (the internal,
supervisor-facing master, an always-current paper body plus an append-only checkpoint log) and
`public/vN/` (frozen submission cuts, derived by compression from the extended). A manuscript is **not**
the same document as a report (`../reports/`, Markdown, the continuous layer that feeds these). Write here
through the `scientific-writing` skill; full spec in `../03-methodology.md` ("Deliverable layers") and
decision D035 (D011 still binds every number).

## What goes here

| Path | Holds | Cadence |
|---|---|---|
| `*.md` | Manuscript sections — drafted prose (intro, related work, methods, results, discussion). | Analysis sessions |
| `figures/` | **Final, selected** figures committed for the thesis (PNG/PDF/SVG). | When a figure is chosen |

The figure pipeline (keeps "the script is the source of truth, the render is a disposable artifact"):

- **Generating code** lives in `../../scripts/figures/` (committed, reproducible from recorded data).
- **All rendered output** goes to `../../outputs/figures/` (gitignored — regenerate any time).
- Only the **chosen** figures are copied into `figures/` here and committed.

## The one rule (D011)

Every number in a sentence and every value in a figure must trace to a result a **working session
actually recorded** in `docs/` (an `experiments/ENNN` entry, a decision, a learning). Cite the source.
If the manuscript needs a number that isn't recorded, that is a **gap to flag** — write it as an open
slot and add a working-session task to produce it. Never invent, estimate, or carry a synthetic
stand-in (e.g. E001's synthetic-fMRI numbers, L004) into the manuscript as if it were evidence.

## Conventions (inherit from `../README.md`)

- Specific numbers with uncertainty and the named test — "Δ = +0.06 ± 0.01, n=3, contiguous split".
- One source of truth: cite `experiments/`, don't restate derivations.
- Dates absolute. The extended manuscript is one living doc (git is its history; tag it when shared); each public `vN` is a frozen snapshot, never rewritten.
