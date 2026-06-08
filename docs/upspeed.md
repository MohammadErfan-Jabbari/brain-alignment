# Upspeed — read first, write last

**Last updated:** 2026-06-09 (Session 2 — benchmark survey + toy pilot harness)

## ☀️ Morning decision points (read these first)

1. **Get the real neural data, then re-run E001 for the actual verdict.** The harness is built and
   validated but ran on **synthetic** fMRI — it answers nothing about the thesis yet. Decision: pull
   **LeBel `ds003020`, one subject (UTS03)** via anonymous S3 (`aws s3 cp --no-sign-request`, check
   size first, keep under a few GB), OR source the **Pereira neural responses** (crwz7 had stimuli
   only). Which path? LeBel is the powered primary (D008); Pereira is the fastest to wire.
2. **Decide the $\mathcal{L}_{\text{brain}}$ form on real data.** The current trainable head is a
   placeholder that overfits (D010). Frozen teacher-encoding-map loss vs CKA proxy vs head — pick once
   real data is staged.
3. **Reframe check (not urgent, but real):** Merlin & Toneva 2026 already proved alignment is
   functionally load-bearing (our A3 premise) via fine-tuning. Confirm we differentiate hard on
   **compression/distillation at matched budget** before writing the contribution. See `04` flags.

## ⚙️ What I actually ran vs scaffolded (Session 2)

- **RAN (real):** benchmark survey; Pereira download + inspection; the full distillation + encoding +
  anti-confound pipeline on **real Pereira sentences + synthetic fMRI**, 3 seeds + λ-sweep, on L40S.
- **SCAFFOLDED (ready, not run on real data):** the `load_pereira` neural-response loader and
  `--backend pereira`. No real neural responses were in the clean download, so **no thesis result was
  produced** — only the plumbing is validated. Nothing synthetic is presented as evidence.

## Current state

Phase = **Map → Claim/Design**. The #1 SPOF (an open, powered language-fMRI benchmark) is **resolved**
(D008): LeBel/Narratives/Pereira are all open and no-login. The make-or-break pilot harness exists,
runs end-to-end on GPU with the full Feghhi/L003 anti-confound protocol, and is one config swap from
real neural data. The feasibility question itself is **still open** — synthetic fMRI cannot answer it.

## What was done (Session 2)

1. **Benchmark survey** → `docs/04-data-benchmarks.md`. Recommendation: LeBel `ds003020` primary,
   Narratives generalisation, Pereira plumbing. SPOF cleared; reframe flag raised (Merlin & Toneva 2026).
2. **Toy pilot harness** → `scripts/{pilot_lib,distill,data_adapters,run_toy_pilot}.py`,
   `configs/toy_pilot.json`, `scripts/README.md`. Anti-confound baked in (contiguous CV, nuisance
   baselines, capacity-fair variance partition, ≥3 seeds, no-leakage split).
3. **Validated** on real Pereira sentences + synthetic fMRI: baseline unique_r2 0.0265±0.0007 vs brain
   0.0254±0.0010, Δ=−0.0011±0.0007; λ-sweep monotonic. Documented in `docs/experiments/E001`.
4. Deps added (`uv add torch transformers …`); Pereira `Pereira_Materials.zip` staged under `data/`.
5. Records: D008–D010, L004–L005, timeline log, this upspeed.

## What to do next

1. **Stage real neural responses + re-run E001** (`--backend pereira`/lebel) — the real verdict on
   A1/A2. This is the highest-value action.
2. **Decide $\mathcal{L}_{\text{brain}}$** (frozen map / CKA / head) on real data.
3. **`paper-digest`** LeBel 2023, Merlin & Toneva 2026, Narratives → `docs/literature/canonical/`.
4. Then lock the baseline matrix (perplexity-only KD, structure-aware KD, alignment-guided, hybrid).

## Blockers

- **Real neural data not yet on disk.** Pereira crwz7 was stimuli-only (L005). LeBel ds003020 is the
  recommended pull (anonymous S3, ~few GB for one subject) — not yet fetched.
- Exact thesis deadline still TBD (tentative end of August 2026).

## Key facts

- **Run Python:** always `uv run` (`.venv`, Python 3.11). `export HF_HOME=/home/centcom/data/hf-cache`.
- **Pilot:** `uv run python scripts/run_toy_pilot.py --config configs/toy_pilot.json [--smoke]`.
  See `scripts/README.md`.
- **Compute:** 4× L40S, single node, background processes for long runs. GPU run of E001 is < ~10 min.
- **Data staged:** `data/pereira/Pereira_Materials/` (stimuli, GloVe, ROI masks — no neural responses).
- **Git:** `main`. Commit continuously and atomically (D007); push only when asked. Heavy artifacts
  (`data/`, `outputs/`) are gitignored — results live in `docs/experiments/E001`, not git.
- **Heads-up logged:** a GateGuard hook fact-forces before each tool call; consider disabling for long
  autonomous runs (timeline "Friction").
