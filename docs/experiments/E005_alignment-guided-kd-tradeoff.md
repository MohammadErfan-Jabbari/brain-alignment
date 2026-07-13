---
title: "Experiment — E005: alignment-guided KD vs perplexity-only KD at MATCHED PERPLEXITY (the F1 headline…"
tags: [experiment]
aliases: [E005]
---

# Experiment — E005: alignment-guided KD vs perplexity-only KD at MATCHED PERPLEXITY (the F1 headline / rate–distortion trade-off curve)

**Created:** 2026-06-11 · **Status:** COMPLETE (ran 2026-06-11) — in-domain +0.0081 was OVERSTATED (pseudo-replicated, one outlier fold); honest verdict = a small brain-specific *trend*, NOT a "CI-excludes-0" result; per-individual = NULL, confirmed by E008. **The ADDENDUM below is the lead verdict; the §Interpretation is superseded.** (L014→L015→L016) · **Mode:** working
**Direction:** R03/R04 F1 (Q3) — the headline thesis experiment. Decides A (alignment-guided distillation wins) vs B (honest trade-off-curve / measurement-rigor framing) **on evidence**.
**Predecessors:** [`E003`](E003_kd-alignment-preservation.md) (perplexity-only KD PARTIAL; L011 — alignment co-varies with perplexity) · [`E004`](E004_brain-loss-lever-test.md) (lever real-but-small-fragile, co-trained MSE front-runner) · [`E006`](E006_lebel-voxelwise-feasibility.md) (powered A2 PASS at voxel scale; lever statistically underpowered)
**Theory:** [`../06-theory-grounding.md`](../06-theory-grounding.md) §4 (rate–distortion = the F1 trade-off curve), §2 (DPI ceiling)
**Code:** reuses `scripts/distill.py` (λ_brain), `scripts/brain_loss.py` (co-trained MSE), `scripts/run_kd_alignment.py` (KD harness), `scripts/run_lebel_encoding.py` (powered alignment measurement)
**Output:** `outputs/E005_tradeoff.json`

> **⚠ READ THE ADDENDUM FIRST (bottom of file).** The §Interpretation below records the *original* "F1 CONFIRMED in-domain" read, which the Session-8 panel showed was **overstated** (pseudo-replication + one outlier fold). The honest verdict — a small brain-specific trend, and a **per-individual NULL** confirmed by E008 — is in the ADDENDUM and [`status.md`](../status.md) (Q3 = ❌). The §Interpretation is kept only as a record of what we first thought (L014→L015→L016).

---

## The question (sharpened by E003→E006)

> Does adding a brain-alignment objective to knowledge distillation buy **higher brain alignment at MATCHED PERPLEXITY** than perplexity-only KD — i.e. alignment recovered *beyond* what LM quality alone implies (the dissociation E003 could not establish, L011)? Plotted as a rate–distortion trade-off curve: rate = perplexity (LM quality), distortion = alignment deficit vs teacher.

**Why this is the decider, not a foregone conclusion:** E004 found the brain lever is real-but-small (+0.003, brain-specific) and E006 confirmed A2 powerfully but showed the lever statistic underpowered on the mean-over-voxels axis. E005 asks the *paired* question — alignment-guided vs perplexity-only KD evaluated on the SAME held-out data at the SAME perplexity — which removes the common-mode variance and is the test that detected E004's effect. A clear positive = F1 confirmed (Fork A). A null/tiny effect at matched perplexity = the honest, publishable trade-off-curve result (Fork B): brain-guided compression buys little beyond perplexity, and the contribution is the rigorous characterization + the curve itself.

## Arms

| Arm | Objective | Brain loss |
|---|---|---|
| **kd_ppl** | perplexity-only KD: `λ_kd·KL(student‖teacher)` | none (λ_brain=0) |
| **kd_brain** | alignment-guided KD: `λ_kd·KL + λ_brain·MSE(W·hₛ, fMRI)` | co-trained MSE readout on Tuckute-train sentences (the E004 front-runner form), student L7 |

Teacher gpt2-medium → student gpt2 (the E003 lineage; warm-start student, since E003 established cold-init is a separate question and warm is the realistic distillation setting). KD corpus = wikitext (E003's `data/kd_corpus/`); brain loss trains on Tuckute-train sentences (sentence-level — NO TR-loop; the powered LeBel axis is *measurement-only*, see below).

## Matched-perplexity protocol (L011 — the load-bearing design)

Compare alignment **at equal held-out perplexity**, not equal budget. Trace each arm's (perplexity, alignment) operating points by sweeping training (λ_brain ∈ a grid for kd_brain; checkpoints / step counts for both) → two Pareto frontiers on the (perplexity, alignment) plane. The F1 claim is **a better frontier for kd_brain** (higher alignment at matched perplexity), not a single number. Primary comparison: interpolate both arms to a common perplexity and take the paired alignment difference.

## Alignment measurement (two axes; the powered one is the headline)

1. **LeBel UTS03 voxelwise (powered, headline):** measure each KD student's unique R² on the E006 protocol (story-CV, expanded phone-tier+eng1000 nuisance, NC-reliable voxels) — measurement-only (`run_lebel_encoding.py` on the student), no further training. This is where A2 is powerfully resolved.
2. **Tuckute 5-ROI (screen, comparability):** the E002/E004 protocol, for ladder continuity.

## Claim tuple / decision rule (predeclared)

- **Metric:** paired (kd_brain − kd_ppl) alignment **at matched perplexity**, on LeBel voxelwise (primary) + Tuckute (secondary); bootstrap CI over seeds (×folds/voxels); ≥3 seeds.
- **F1 CONFIRMED (Fork A):** kd_brain alignment > kd_ppl at matched perplexity, CI excludes 0, on the powered LeBel axis, surviving the E006 anti-confound. The brain term recovers alignment beyond perplexity.
- **F1 NULL → trade-off-curve result (Fork B, the literature-leaning outcome):** the paired difference CI includes 0 at matched perplexity. → Brain-guided KD buys nothing beyond perplexity; the honest contribution is the rigorously-characterized trade-off curve (perplexity vs alignment under compression, with the strongest anti-confound) + the measurement-rigor finding that alignment tracks LM quality (L011/L012, Hadidi-2024). Still a real, publishable thesis.
- **Anti-confound (mandatory):** LeBel = E006 protocol (story-CV, expanded nuisance, NC voxels, untrained reference); Tuckute = E002 protocol. Report perplexity per arm/point (the matched axis). ≥3 seeds.

## Open design questions (resolve at lock / oracle review)

- The exact matched-perplexity mechanism (λ-sweep vs checkpoint-matching vs early-stop to a target ppl) — the cleanest is checkpoint-matching: save students at several ppl levels, compare alignment at equal ppl.
- Power: E006 showed the mean-over-voxels lever MDE ≈ +0.013; the *paired* kd_brain−kd_ppl contrast at matched ppl should be better-powered (common-mode removed), but a power note is required before committing (the same MDE discipline as E004/E006).
- Whether to also run a *region-restricted* (LH-language) LeBel axis where the brain effect may concentrate (vs whole-cortex NC voxels).
- Compression aggressiveness: gpt2-medium→gpt2 (2.9×) is one rate; a second rate (→distilgpt2-size) would trace more of the curve (defer unless the first rate is informative).

## Results — in-domain (Tuckute), ran 2026-06-11

**Setup (oracle-vetted, reordered):** Qwen2.5-0.5B student ← **Qwen2.5-1.5B teacher** (real 3× distillation), LoRA, KD-KL retention; arms = `mse` (alignment-guided KD) / `lm_only` (=kd_ppl, perplexity-only KD) / `mse_perm` (the matched-ppl brain-specific null), 3 seeds × 5 rotating Tuckute folds, λ_brain=10. KD keeps the LM strong (ppl ~52–55, vs ~200 for brain-tune-without-KD). Base unique R²=+0.0102.

| Arm | ppl | unique R² Δ vs base [CI] | NC-norm uR² |
|---|---|---|---|
| kd_ppl (lm_only) | 51.5 | −0.0021 [−0.0068, +0.0019] | 0.017 |
| **kd_brain (mse)** | 55.4 | +0.0047 [−0.0034, +0.0148] | 0.030 |
| kd_brain_permuted (mse_perm) | 55.3 | −0.0034 [−0.0089, +0.0012] | 0.014 |

**PRIMARY statistic — paired (kd_brain − kd_brain_permuted) at MATCHED PERPLEXITY (55.4 vs 55.3): +0.0081 [CI +0.0023, +0.0171], CI excludes 0.** 73% of 15 pairs positive. Per-fold [+0.0033, +0.0067, +0.0020, +0.0047, +0.0239]; **leave-fold-4-out = +0.0042 (4/5 folds positive)** — robust, unlike E004's fold-4-dependent lever. Reference (ppl-confounded): kd_brain − kd_ppl = +0.0068, *despite kd_brain having worse ppl* (55 vs 51) — so the gain is NOT from being a better LM (rules out the L011 confound).

## Interpretation

> **⚠ SUPERSEDED — historical record only.** Everything in this section was the *first* read; it is overstated. See the ADDENDUM and [`status.md`](../status.md) for the honest verdict (small trend → per-individual NULL, E008/L016). Kept un-edited so the correction is traceable (per the repo's record-don't-rewrite convention).

**F1 CONFIRMED in-domain (Fork A supported).** Alignment-guided KD recovers **brain-specific** alignment **beyond** perplexity-only KD **at matched perplexity** — the dissociation E003 (L011) and E004 could not cleanly establish. The KD-KL anchor + the matched-ppl-by-construction permuted-twin design cleaned up E004's fragility (4/5 folds positive, robust to the fold-4 outlier, and the gain holds despite slightly-worse ppl). This flips the oracle's "Fork B more likely" prior: the in-domain matched-ppl test is positive.

**But the effect is SMALL — an A+B synthesis, not a triumphal A.** The brain-specific gain is +0.0081 (NC-norm ~1.6% of ceiling; kd_brain 0.030 vs permuted 0.014 NC-norm). This is exactly the "real but small residual" regime the literature predicts (Hadidi/Feghhi 2026 ≤10%; L011/L012). The honest framing is: **F1 holds — the brain objective buys a real, brain-specific, perplexity-independent alignment gain in distillation — and the contribution includes the rigorous characterization of *how small* it is (the rate–distortion trade-off curve).** Both the positive (A) and the honest magnitude/curve (B) are the result.

**Caveats:** (1) in-domain Tuckute (5-ROI, the training domain) — the powered **LeBel voxelwise TRANSFER** test is the next gate (does the in-domain gain generalize cross-dataset/granularity). NOTE: the LeBel mean-over-voxels statistic is underpowered (E006 MDE +0.013); the transfer test needs a **powered statistic** (per-voxel paired, or LH-language-region-restricted), to be designed + oracle-gated. (2) Single λ=10; the full trade-off curve (λ-sweep, multiple compression rates) is the Fork-B-framing follow-up. (3) Qwen-0.5B student / single subject (Tuckute 5-UID avg); scope claims accordingly. (4) Fold-4 still inflates — report the leave-one-out as the conservative estimate.

## Status / next

F1 in-domain = **POSITIVE** (recorded). Next gates (predeclared): **(a)** LeBel voxelwise **transfer** test with a *powered* statistic (per-voxel paired / region-restricted — design + oracle-gate first); **(b)** the λ-sweep / multi-rate **trade-off curve** for the Fork-B-rigor framing. Ladder: **Q3/F1 → 🟡 PARTIAL-PASS (in-domain confirmed, transfer + magnitude pending)** — **pending Erfan's confirmation** (D015).

---

## ⚠ ADDENDUM — Session-8 honest re-analysis (2026-06-11, `scripts/reanalyze_e005_e006.py`)

A thinking-panel audit (counter-argument + premortem + first-principles, fable) re-derived the result
from the raw JSON *before* the next compute. **The "CI excludes 0" headline above does not survive
honest inference and should be read as overstated.** See L015. Specifics (pure re-analysis, no new run):

- **Inference unit.** The +0.0081 [+0.0023,+0.0171] CI is a **15-cell flat bootstrap** (3 seeds × 5
  folds) over **one subject-average** (Tuckute 5-UID mean), same 1000 sentences → pseudo-replication.
- **Honest fold-level (n=5):** mean +0.0081, sd 0.0090, **t-CI95 = [−0.0030, +0.0193] → INCLUDES 0.**
  Cluster-bootstrap over folds = [+0.0031,+0.0162] (excludes 0) — they disagree because **one run
  (fold4/seed0, uR²=0.073, ~7× outlier) = 52% of the signal**; mean is 2.4× the **median +0.0034**;
  leave-fold-4-out = +0.0042.
- **Harness's own flag:** `beats_permuted_null=False` (mse 0.00474 < perm p95 0.00737); `n_perm=1`.
- **Transfer feasibility:** paired-LeBel MDE (from E006 fold_sd) needs arm-correlation ρ≥0.9 to resolve
  even +0.0081; honest +0.0042 below noise for ~all ρ. → transfer underpowered on the valid statistic.

**Honest verdict (supersedes the §Interpretation framing for inference):** a **small brain-specific
trend** (4/5 folds positive, median ~+0.003–0.004), brain-specific-leaning, **not** a significant
"CI excludes 0" result. **Next = solidify in-domain per-participant (E008) before any transfer.** The
ladder Q3/F1 verdict needs revisiting with Erfan (D015) — not flipped unilaterally.

## S48 addendum — Qwen averaged-target λ-sweep / rate-distortion context (2026-07-02)

Ran the optional averaged-target λ-sweep with λ-matched permuted twins after patching
`scripts/run_brain_lever.py` so every `--lambda-grid` MSE arm gets its own `null_key`/`perm_draw` control:

```bash
HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1 CUDA_VISIBLE_DEVICES=1 \
uv run python scripts/run_brain_lever.py \
  --model Qwen/Qwen2.5-0.5B \
  --kd-teacher Qwen/Qwen2.5-1.5B \
  --arms mse lm_only \
  --permute-kinds mse \
  --seeds 0 1 2 \
  --folds 5 \
  --lambda-grid 1 3 10 30 \
  --n-perm 1 \
  --out outputs/E005_lambda_sweep_avg_Qwen.json

uv run python scripts/analyze_lambda_sweep.py \
  outputs/E005_lambda_sweep_avg_Qwen.json \
  --out outputs/E005_lambda_sweep_avg_Qwen_analysis.json
```

Fold-level analysis (n=5 fold means; seed-fold flat bootstrap is descriptive only):

| Arm | PPL | Δ vs base, fold-t CI | vs `lm_only`, fold-t CI | vs matched permuted, fold-t CI | Read |
|---|---:|---:|---:|---:|---|
| `lm_only` | 51.5 | +0.0007 [-0.0011,+0.0024] | n/a | n/a | KD-only anchor. |
| `mse_l1` | 51.6 | +0.0032 [-0.0009,+0.0073] | +0.0025 [-0.0010,+0.0060] | +0.0030 [-0.0025,+0.0085] | Small near-rate trend; not fold-level significant. |
| `mse_l3` | 51.9 | +0.0046 [-0.0021,+0.0112] | +0.0039 [-0.0028,+0.0106] | +0.0063 [-0.0092,+0.0218] | Best near-rate mean, but fold-4/control dominated; leave-fold-4-out vs perm = +0.0010. |
| `mse_l10` | 55.4 | +0.0038 [-0.0011,+0.0088] | +0.0031 [-0.0014,+0.0077] | +0.0072 [-0.0044,+0.0188] | Similar to original λ=10 trend; worse PPL and fold-4-sensitive. |
| `mse_l30` | 67.4 | +0.0043 [+0.0020,+0.0065] | +0.0036 [+0.0009,+0.0062] | +0.0060 [+0.0002,+0.0119] | Only fold-level-positive arm, but it buys the gain by degrading PPL materially. |

**Interpretation:** the sweep supports the original honest magnitude read: averaged-target brain loss can nudge
Tuckute in-domain alignment by a few `unique_R2` points, but the useful near-rate arms (`λ=1,3,10`) do **not**
survive fold-level CIs. The only arm that clears fold-level CIs (`λ=30`) moves from `lm_only` PPL ≈51.5 to ≈67.4,
so it is a rate-distortion trade, not a practical free improvement. This is **context for "how small / how costly"**,
not new per-individual evidence and not a ladder move.


## Retained load-bearing artifacts

| Artifact | SHA-256 |
|---|---|
| `outputs/E005_Qwen.json` | `e9b7be5b739370ed224de1bd8c6d4fa34d33881db308d3508e1edba66ddfcf6e` |
| `outputs/E005_lambda_sweep_avg_Qwen_analysis.json` | `85013e6ff961aa88bd40e9e16dd19aaab3c89656f0dac8cd74c64560469f7938` |

## Related
- [`status.md`](../status.md) — the canonical status board
