---
title: "Manuscript Agent Guidance"
tags: [manuscript, reference]
aliases: [manuscript-agents]
---

# Manuscript Agent Guidance

## Layout

| Path | Purpose |
|---|---|
| `extended/` | Live LaTeX master and authority for current scientific interpretation |
| `public/vN/` | Immutable sharing/submission cuts derived from the extended master |
| `figures/` | Selected committed figures; generation code lives in `scripts/figures/` |

## Direct writing loop

1. Read the owning E records and current manuscript section.
2. State the intended claim, scope, caveats, and evidence.
3. Edit the extended manuscript directly.
4. Preserve `\evd{Ennn}` and keyed values in `numbers.tex`; a missing value is a `\gap`.
5. Run `uv run python .claude/scripts/manuscript_check.py docs/manuscript/extended`.
6. Run one fresh independent prose/scientific-scope review and obtain Erfan’s approval for load-bearing framing.

Use `--share-ready` only when no gap remains. A contradiction routes to `/interpret` and sets `docs/status.md` to `manuscript-sync-pending`.

## Rules

- Do not create a manuscript report, claim lattice, checkpoint log, convergence store, or alternate draft tree.
- Public cuts are frozen. A new milestone creates a new version.
- Every scientific number and figure value traces to an owning E record; only load-bearing artifacts receive recorded paths and SHA-256 values.
- Use the correct inference unit, uncertainty, and named test.
- Keep internal provenance in non-printing BibLaTeX fields such as `annotation`, not printable `note` fields.
- Keep source search-friendly: one sentence or paragraph per line, minimal custom macros, and no deep content nesting.
- Do not create a README; folder guidance belongs here.

## Figure path

`scripts/figures/ → outputs/figures/ (gitignored) → docs/manuscript/figures/ (selected and committed)`

## Related

- [Authority contract](../03-methodology.md)
- [Current status](../status.md)
- [Experiment records](../experiments/AGENTS.md)
