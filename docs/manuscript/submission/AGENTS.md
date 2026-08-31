# Supervisor submission derivative

This directory is a supervisor-review derivative of [`../rewrite/`](../rewrite/), created under D064 and D065.

- `../rewrite/` remains the sole scientific-interpretation authority. The local section files are a review workspace; accepted scientific changes must be synchronized to `../rewrite/` before they become authoritative.
- Writing methodology (drafting and review protocol, acceptance checks, terminology, prose, structure, table, and figure rules) follows [`../AGENTS.md`](../AGENTS.md); the scientific position and maintained question tree follow [`../rewrite/AGENTS.md`](../rewrite/AGENTS.md).
- The derivative uses the official UC3M cover-page fields and a one-column paper-style body. Its local section copies permit submission-specific restructuring, condensation, and supervisor-feedback edits without silently changing the canonical rewrite.
- Condensation may remove detail or move it to the supplement, but it must not change a result, evidence state, estimator, inference unit, caveat, or scientific claim. Every retained load-bearing result keeps its `\\evd{Ennn}` provenance and keyed values.
- This is not an immutable public cut. Create a public version only after supervisor feedback and Erfan's approval.
- Build from this directory with `latexmk -pdf main-submission.tex`; generated auxiliary files are ignored and the PDF is the supervisor-facing artifact. Run `uv run python scripts/manuscript_check.py docs/manuscript/submission` on edited prose, same as for `rewrite/`.

## Files

- `style/` — official NeurIPS 2025 style package (downloaded from `media.neurips.cc`, 2026-08-25) plus the official UC3M logo for the cover page.
- `preamble.sty` — vendored copy of `../rewrite/preamble.sty` (same pattern as public cuts; a later rewrite edit must not change how this derivative compiles).
- `main-submission.tex` — UC3M cover page (regulation Appendix I fields at the top of the file) + NeurIPS-style body assembled from local section files.
- `sections/` — local review copy of rewrite Sections 01--07 and Appendices A--F; submission-specific edits live here until accepted and synchronized upstream.
- `figures/` — local copy of manuscript figure sources so submission-specific visual fixes do not mutate the canonical rewrite.
- `deferred-review-items.md` — non-authoritative working checklist for submission-review items blocked on authorization or missing information.
- `numbers.tex`, `acronyms.tex`, `references.bib` are NOT vendored: the main file inputs them from `../rewrite/` so keyed values and citations stay single-source.
- The NeurIPS `final` option alone leaves `\@trackname` undefined; the main file empties `\@noticestring` since a thesis is not a NeurIPS track submission.
