# Supervisor submission derivative

This directory is a formatting-only derivative of [`../rewrite/`](../rewrite/), created for supervisor review under D064 and D065.

- `../rewrite/` remains the sole scientific-interpretation authority. Do not edit it from this directory.
- The derivative uses the official UC3M cover-page fields, a one-column paper-style main text, and supplementary material containing the supporting methods, provenance, estimators, stopped routes, and sensitivities moved out of the main paper.
- Condensation may remove detail or move it to the supplement, but it must not change a result, evidence state, estimator, inference unit, caveat, or scientific claim. Every retained load-bearing result keeps its `\\evd{Ennn}` provenance and keyed values.
- This is not an immutable public cut. Create a public version only after supervisor feedback and Erfan's approval.
- Build from this directory with `latexmk -pdf main-submission.tex`; generated auxiliary files are ignored and the PDF is the supervisor-facing artifact.

## Files

- `style/` — official NeurIPS 2025 style package (downloaded from `media.neurips.cc`, 2026-08-25) plus the official UC3M logo for the cover page.
- `preamble.sty` — vendored copy of `../rewrite/preamble.sty` (same pattern as public cuts; a later rewrite edit must not change how this derivative compiles).
- `main-submission.tex` — UC3M cover page (regulation Appendix I fields at the top of the file) + NeurIPS-style body.
- `deferred-review-items.md` — non-authoritative working checklist for submission-review items blocked on authorization or missing information.
- `numbers.tex`, `acronyms.tex`, `references.bib` are NOT vendored: the main file inputs them from `../rewrite/` so keyed values and citations stay single-source.
- The NeurIPS `final` option alone leaves `\@trackname` undefined; the main file empties `\@noticestring` since a thesis is not a NeurIPS track submission.
