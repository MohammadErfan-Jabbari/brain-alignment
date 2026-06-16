# Upspeed — read first, write last

**Last updated:** 2026-06-16 (Session 17 — analysis. **R06 precision sweep complete via the thinking panel (8 fixes).** No science rung changed; the analysis lane is active. Next: R07.)

> **Canonical state lives in [`ladder.md`](ladder.md).** This is last-session prose. With no task, run `/orient`.

## What got understood / written / figured this session

1. **R06 is now precision-clean.** Three parallel opus agents (counter-argument, socratic-thinker, first-principles-grounder) found 8 real issues; all fixed:
   - Tables replacing inline numbers for both E002 and E006 evidence
   - Semipartial vs partial R² corrected: unique R² = semipartial (raw increment), NOT partial ρ² (normalized). The biconditional unique R² > 0 ↔ I(LM; B | Z_nuis) > 0 holds for both; the error was in "exactly."
   - Untrained sign mechanism rewritten: strong nuisance (eng1000 + phone tier) absorbs the shared-cause floor → untrained unique R² = −0.017 (negative) in E006; gap statistic justified as isolating training from architecture
   - "gpt2-medium in between" → "comparable" (data: +0.019 ≈ +0.020 << +0.036)
   - "mid-layer-peaked" → "broad plateau, not a sharp peak"
   - Temporal leakage and voxel-selection-bias paragraphs rewritten with explicit mechanisms
   - Language-network caveat added (E006 uses reliability-based selection, not a language localizer)
   - "Two controls" → "Three controls"; "most capable" → "most recent model and strongest aligner of the three"
   - CC_norm > 0.05 stale threshold in E006 design section corrected to split-half reliability > 0.5, as-run

2. **Architecture sections added to E002 and E006.** Last-sub-token rationale (causal LM standard), Lanczos resampling, FIR delays, capacity-fair PCA, and the two-arm gap structure documented with Mermaid flowcharts.

3. **Pipeline explainer created.** `docs/explainer_pipeline.html` — dark-mode HTML with color-coded diagrams and the full text→brain pipeline in plain language.

## What's next — analysis lane

**NEXT: R07** (Q1 — plain KD does not preserve alignment). Source: `experiments/E003_*.md`. Reading order and self-checks in `docs/analysis-roadmap.md`. Write through the `scientific-writing` skill.

## Blockers / open loops

- **Uncommitted work in the tree** (all this session's output — commit before next session):
  - `docs/reports/R06_alignment-signal-is-real-beyond-confounds.md` (M) — R06 precision sweep
  - `docs/experiments/E002_tuckute-encoding-feasibility.md` (M) — architecture section
  - `docs/experiments/E006_lebel-voxelwise-feasibility.md` (M) — architecture section + CC_norm fix
  - `docs/explainer_pipeline.html` (new) — pipeline explainer
  - `untitled.md` (untracked, pre-existing scratch) — harmless, intentionally not committed
- `projects/brain-alignment` gbrain hub is still a bare stub (enrich when convenient).
- No background jobs running.

## Key facts

- **Run Python:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1`. 4× L40S.
- **Codes (D036):** `Q`n = ladder rung (Q0→Q5, climb order); `E`/`D`/`L`/`A` = flat immutable artifact IDs. Legend + journey tree in `docs/map.md`; canonical status in `docs/ladder.md`.
- **Writing:** route all report/manuscript prose through the `scientific-writing` skill (D035/D036). Reports = `docs/reports/R<NN>_*.md` (one claim per file, continuous); manuscripts = `docs/manuscript/{extended,public}/` (LaTeX, checkpoint-derived only on Erfan's call).
- **Subagent routing (D026):** opus = think/analysis/design; sonnet = doc-nav; haiku = mechanical. fable BANNED.
- **Git:** `main`, push only when asked.
