---
title: "Session Log: 2026-06-09 00:54 CEST — Benchmark survey + toy pilot harness"
tags: [timeline]
---

# Session Log: 2026-06-09 00:54 CEST — Benchmark survey + toy pilot harness

**Project:** brain-alignment (MSc thesis, UC3M)
**Phase:** Map → Claim/Design boundary. SPOF resolved; feasibility harness built (synthetic-validated).

---

## Purpose

Run the two overnight tasks back to back: (1) the language-fMRI benchmark survey that gates everything,
and (2) the toy GPT-2-medium → GPT-2 brain-alignment distillation pilot — the make-or-break feasibility
test — with the anti-confound protocol baked in. Be adaptive about the data dependency; do not block.

## What I actually ran vs scaffolded

- **Ran for real:** the benchmark survey (lit-scout); the Pereira download + inspection; the full
  distillation + encoding + anti-confound pipeline on **real Pereira sentences + synthetic fMRI**, 3
  seeds + a λ-sweep, on one L40S.
- **Scaffolded, ready for real data:** the `load_pereira` neural-response loader and the `--backend
  pereira` path. No real neural responses were available in the clean download, so the scientific
  question is **not** answered — only the pipeline is validated. Nothing synthetic is presented as a
  thesis result.

## Task 1 — language-fMRI benchmark survey (→ `docs/04-data-benchmarks.md`)

- Surveyed Pereira 2018, Narratives, LeBel 2023, Petit Prince, and EvLab/Fedorenko releases: license,
  N, noise ceiling, English/multilingual, modality/TR, and +0.05 R² power for each.
- **SPOF resolved.** Three open, no-login English benchmarks. **Recommendation: LeBel `ds003020`
  primary** (powered within-subject, noise ceiling, CC0/CC-BY, anonymous S3/DataLad), **Narratives
  `ds002345`** generalisation, **Pereira `crwz7`** plumbing. Charter data-access kill not triggered.
- **Reframe flag (not a kill):** Merlin & Toneva 2026 ("When LMs Lose Their Mind") already proved the
  A3 premise via fine-tuning; we must differentiate on **compression/distillation at matched budget**.

## Task 2 — toy distillation pilot (→ `scripts/`, `configs/`, `docs/experiments/E001`)

- Built `pilot_lib.py` (encoding + capacity-fair variance partition + contiguous CV), `distill.py`
  (logit-KD + brain-head loss), `data_adapters.py` (synthetic / real-sentences / Pereira), and
  `run_toy_pilot.py` orchestrator. Added torch/transformers/sklearn/scipy/nibabel/nilearn via `uv add`.
- Pulled Pereira `Pereira_Materials.zip` (276 MB, OSF crwz7, no login) → **stimuli only, no neural
  responses** (L005). Took the hybrid path: real 384 Pereira sentences + synthetic fMRI.
- **Canonical run (3 seeds, λ=1.0):** baseline unique_r2 0.0265±0.0007 vs brain 0.0254±0.0010,
  **Δ = −0.0011 ± 0.0007**; teacher ref 0.0424 > students. λ-sweep monotonic (−0.0004 / −0.0010 /
  −0.0069 at 0.1/0.5/5.0). Plumbing validated; the brain head slightly *hurts* on synthetic — exactly
  as expected when the target is a linear map of teacher features (L004). Not evidence about H001.

## Decisions made

- **D008** — Benchmark choice (LeBel primary / Narratives generalisation / Pereira plumbing).
- **D009** — E001 ran the hybrid path (real sentences + synthetic fMRI), labelled plumbing-only.
- **D010** — $\mathcal{L}_{\text{brain}}$ form still open; trainable head is a placeholder.

## Learnings

- **L004** — Synthetic tests plumbing not science; nuisance and contextual blocks must be capacity-matched.
- **L005** — Pereira crwz7 is stimuli-only; an open license + a zip ≠ the fMRI matrix in hand.

## Friction & improvements

- A `GateGuard` fact-forcing hook fired before every Bash/Write/Edit, adding overhead to an autonomous
  run. Worked through it by stating facts each time. If future overnight runs are common, consider
  `ECC_GATEGUARD=off` or disabling `pre:edit-write:gateguard-fact-force` for the session.
- JSON duplicate-key bug (`n_items`) silently capped the first run at 240 sentences — caught and fixed;
  re-ran at 384. Lesson folded into care with config edits.

## Next session (see [`upspeed.md`](../upspeed.md) for the decision points)

- Source the **real neural responses** (LeBel ds003020 one subject via anonymous S3, or Pereira
  responses from the separate host), then re-run E001 with `--backend pereira`/lebel for the real verdict.
- Decide the $\mathcal{L}_{\text{brain}}$ form (frozen encoding map vs CKA vs head) on real data.
- Hand LeBel 2023 + Merlin & Toneva 2026 + Narratives to `paper-digest`.


## Related
- [`ladder.md`](../ladder.md) — the canonical status board
- [`map.md`](../map.md) — code system (Q/E/A/D/L) & journey map
