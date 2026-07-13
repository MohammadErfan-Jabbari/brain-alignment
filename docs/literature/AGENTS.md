---
title: "Literature Agent Guidance"
tags: [literature, reference]
aliases: [literature-agents]
---

# Literature Agent Guidance

This folder holds self-contained copies of papers actually read for the thesis. The organized role map lives in `../01-research-landscape.md`; read that first before adding or interpreting paper notes.

## Layout

| Path | Use |
|---|---|
| `canonical/` | One note per paper actually read. Add new notes here through the `paper-digest` agent. |
| `_prior-work/` | Frozen provenance: original idea, early dossier, and adversarial review. Do not edit. |

## Rules

- Do not create a `README.md` here. Folder guidance belongs in `AGENTS.md`.
- A paper's claim is not this repo's result. Cite it, but do not turn it into a project number.
- Canonical notes should be self-contained enough that the repo stands alone.
- Use standard Markdown links and frontmatter per `../references/obsidian-conventions.md`.
- If a dataset or paper role changes, update `../01-research-landscape.md` and the relevant report, not only the canonical note.

## Paper Roles

Use the landscape doc for the authoritative map. The old folder index grouped papers as:

| Role | Examples |
|---|---|
| Alignment anchors | Gao 2024, Oota 2023/2026, Aw 2023, Merlin 2024, Alkhamissi 2025, Yin 2025, Zhu 2025 |
| Brakes/counter-evidence | Feghhi 2024, Oota 2024 |
| Distillation baselines | MiniLM, MGSKD, LRC-BERT, AlignDistil, MetaDistil, Jia 2024 |
| Systems constraints | Ji 2025, RazorAttention |
| Measurement/theory | CKA, Platonic Representation |

## Fresh-Search Gaps

- Language-fMRI datasets and their power: Pereira, Narratives, LeBel, Fedorenko.
- Any 2026 brain-alignment-for-compression work; verify the gap is still open before making novelty claims.

## Related

- `../01-research-landscape.md`
- `../status.md`
