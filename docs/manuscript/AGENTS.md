---
title: "Manuscript Agent Guidance"
tags: [manuscript, reference]
aliases: [manuscript-agents]
---

# Manuscript Agent Guidance

This folder holds the LaTeX manuscript layers derived from recorded evidence. A manuscript is not a report: reports are the continuous Markdown synthesis layer, while manuscript cuts are checkpoint-derived.

## Layout

| Path | Holds | Cadence |
|---|---|---|
| `extended/` | Internal LaTeX master: current paper body plus append-only checkpoint log. | Only at a checkpoint Erfan calls |
| `public/vN/` | Frozen submission/share cuts, compressed from the extended; each cut vendors its own preamble and bib. | Submission/share milestone |
| `figures/` | Final selected figures committed for the thesis. | When a figure is chosen |

## Rules

- Do not create a `README.md` here. Folder guidance belongs in `AGENTS.md`.
- Write or edit manuscript prose only through the `sci-write-v2` pipeline.
- Never auto-update `extended/` or `public/vN/`; Erfan calls checkpoints.
- Every number in prose and every figure value must trace to a recorded working-session result in `docs/`.
- If a needed number is missing, mark it as a gap and add a `/work` task. Do not invent, estimate, or promote synthetic stand-ins.
- Use specific numbers with uncertainty and named tests.
- Cite experiments and reports; do not restate derivations if the report already owns them.
- In `references.bib`, use non-printing `annotation` for internal provenance or critique notes. Do not use `note` for repo-internal comments because it prints in the rendered reference list.

## Figure Pipeline

| Path | Role |
|---|---|
| `../../scripts/figures/` | Committed figure-generation code, reproducible from recorded data. |
| `../../outputs/figures/` | Gitignored rendered outputs, disposable and regenerable. |
| `figures/` | Chosen final figures copied here and committed. |

## Related

- `../reports/AGENTS.md`
- `../03-methodology.md`
- `../ladder.md`
- `../map.md`
