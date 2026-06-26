---
title: "Timeline — 2026-06-11 13:03 — Session 7: the lever (E004), powered A2 (E006), and F1 confirmed…"
tags: [timeline]
---

# Timeline — 2026-06-11 13:03 — Session 7: the lever (E004), powered A2 (E006), and F1 confirmed in-domain (E005)

**Mode:** working (Design → Run → Judge, three full cycles). **Branch:** main. **Autonomous** (long `/goal` run). **Commits:** `888b446` → `7a1375c` (14 atomic commits).

## What ran (three experiments + literature grounding, all oracle-gated)

This session built the keystone (`$\mathcal{L}_{\text{brain}}$`) and climbed three rungs, each design adversarially reviewed *before* compute (the E003 discipline; one HOLD caught a fatal confound each time).

1. **E004 — Layer 1 (is the brain loss a usable lever?) + D010 resolution.** Built `brain_loss.py` (loss family: co-trained MSE / cosine / neg-Pearson / frozen-ridge / linear-CKA + `block_permute`) and `run_brain_lever.py` (LoRA brain-tuning, rotating contiguous Tuckute folds, each readout vs its OWN permuted-fMRI twin + lm_only control). Two oracle reviews (HOLD→PASS) reshaped it: caught a **fatal covariate-shift confound** (imageability A=4.0→B=3.2, p≈1e-21, predicts BOLD r=−0.25, verified in data) → rotating folds; winner's-curse → mse-primary; no power note → MDE sim. Two smoke-driven fixes: full-FT collapsed perplexity (226/865) → **LoRA**; the co-trained readout absorbed MSE non-specifically → **per-kind permuted twins**. **Verdict: PARTIAL** — a brain-SPECIFIC lever exists (Qwen mse − its permuted twin = +0.0032 [+0.0006,+0.0058]) but small/fragile (fold-4-driven) and sub-threshold on the 5-ROI screen. D010 → co-trained MSE leaning.

2. **E006 — Layer 0/A2 at powered voxelwise scale.** Built `lebel_adapter.py` (reuses the official deep-fMRI-dataset pipeline: TextGrid→wordseq→Lanczos→FIR; per-word contextual LM features; staged 84 TextGrids + eng1000 from OpenNeuro) and `run_lebel_encoding.py` (story-CV, capacity-fair PCA, NC-reliable voxel selection from `wheretheressmoke`'s 10 repeats). Oracle HOLD→resolved: caught a repeat of the L012 nuisance hole (→ added phone-tier rates/duration/length + log-freq + eng1000) and that CC_norm was buildable (→ held-out-repeat voxel selection, no double-dip). **Verdict: A2 STRONG PASS** — trained−untrained gap +0.021 (gpt2) / +0.028 (Qwen) on 11.4k NC voxels, 95–99% positive; clears the Hadidi/Feghhi 2026 bar. **But** the mean-over-voxels lever statistic is underpowered (MDE +0.013 ≫ +0.003) → don't build the TR-level lever loop (E007).

3. **Literature grounding.** lit-scout sweep (2024–26) + paper-digest of **Hadidi/Feghhi 2026 (Nature Communications)**: PWR+GloVe explains >80% of GPT-2XL neural variance, trained residual "real but small" (≤10%) — matches our finding and sets the anti-confound bar. Leaned toward the trade-off-curve framing.

4. **E005 — Layer 3 / F1 (the headline), in-domain.** Extended `run_brain_lever` with a KD-teacher term (retention = KL(student‖teacher)); the permuted twin becomes a **matched-perplexity** control by construction. Oracle HOLD-bordering-KILL (judged Fork B more likely) → reordered to Tuckute-in-domain-first (the paired statistic is powered, MDE +0.0035, where the LeBel-mean is not). Ran Qwen2.5-1.5B→0.5B distillation (LoRA, KD-KL), alignment-guided vs perplexity-only, 3 seeds × 5 folds. **Verdict: F1 CONFIRMED in-domain** — paired (kd_brain − kd_brain_permuted) at matched perplexity = **+0.0081 [+0.0023, +0.0171]**, CI excludes 0, 4/5 folds positive (leave-fold-4-out +0.0042), brain-specific, and holds despite slightly-worse ppl (rules out L011). The dissociation E003/E004 couldn't establish. **Small (~1.6% NC) → an A+B synthesis.**

## Verdicts → ladder (Erfan-confirmed)

- L0/A2 → ✅ PASS (powered, E002+E006). L1 → 🟡 PARTIAL (E004). L3/F1 → 🟡 **PARTIAL-PASS** (E005, in-domain confirmed; transfer + magnitude pending).
- **The thesis has its positive headline result** (F1: alignment-guided KD recovers brain-specific alignment beyond perplexity), framed honestly as A+B (confirmed + small + the rate–distortion curve).

## What's next to run (ordered)

1. **LeBel voxelwise TRANSFER test** — does E005's in-domain gain generalize? Needs a *powered* statistic (per-voxel paired / LH-region-restricted; mean-over-voxels MDE +0.013). **Design + oracle-gate first.**
2. **λ-sweep / multi-rate trade-off curve** (in-domain Tuckute powered, then LeBel) — the Fork-B-rigor / "how small" characterization.
3. **Doc-consistency:** dedup feghhi-2024 / hadidi-2024 (same paper); sweep R03/R04/upspeed for stale "E004=headline" (now E005).

## Artifacts (new this session)

- Code: `scripts/brain_loss.py`, `run_brain_lever.py` (+KD-teacher), `lebel_adapter.py`, `run_lebel_encoding.py`, `verify_e004_premises.py`.
- Docs: `experiments/E004,E005,E006_*.md`; `literature/canonical/hadidi-2024_*.md`; learnings **L012, L013, L014**; ladder flipped.
- Brain: `projects/brain-alignment-{e004-lever-test, lit-fork, e006-powered-a2, e005-f1-confirmed}`.
- Data staged: LeBel TextGrids + eng1000 (OpenNeuro). Deps added: peft, accelerate, wordfreq, tables.

## Continuity audit (friction / tooling / consistency)

- **Friction:** zsh `noclobber` rejected `>` redirects (use `>|`) and a compound `nohup ... & ; grep|tail` hit a parse error — launch background jobs as standalone commands. Session cost was high (~$406) for three experiment cycles + 4 oracle reviews + 2 lit subagents.
- **Tooling:** background `nohup &` jobs aren't harness-tracked (used `run_in_background` waiter loops to get completion notifications). LoRA needed (full-FT collapses ppl).
- **Doc consistency:** feghhi-2024/hadidi-2024 duplicate (same paper) and the E004→E005 headline rename need a sweep (logged in tasks + ladder). Ladder is the source of truth and is current.
- **Verdict integrity:** all three rung flips Erfan-confirmed (D015). Raw evidence (`outputs/E00{4,5,6}_*.json`, gitignored) separate from interpretation.


## Related
- [`ladder.md`](../ladder.md) — the canonical status board
- [`map.md`](../map.md) — code system (Q/E/A/D/L) & journey map
