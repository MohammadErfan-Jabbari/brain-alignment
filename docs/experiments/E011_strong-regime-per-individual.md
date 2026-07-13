---
title: "Experiment — E011: is the per-individual F1 null REGIME-SPECIFIC? (strong-regime per-subject test,…"
tags: [experiment]
aliases: [E011]
---

# Experiment — E011: is the per-individual F1 null REGIME-SPECIFIC? (strong-regime per-subject test, vs Negi)

**Created:** 2026-06-12 · **Status:** COMPLETE (ran 2026-06-12) — per-individual null robust to heavy-LoRA capacity (r64/6ep, +0.0004 [−0.0005,+0.0013], incl 0; the knob that moves the rep wrecks ppl; L019) · **Mode:** working
**Direction:** the manuscript's key open test (§6). E008's per-individual null was under *light* LoRA (r=16, 3 epochs, frozen base → perplexity preserved). The counter-argument's live rebuttal: "you got null because you didn't tune hard enough — [Negi 2025](../literature/canonical/negi-2025_brain-informed-finetuning-multilingual.md) got a *positive* per-individual encoding gain under full fine-tuning." E011 settles whether the null survives a strong regime.
**Predecessors:** [`E008`](E008_per-participant-f1-solidification.md) (light-LoRA per-subject null, +0.0001) · [`E004`](E004_brain-loss-lever-test.md) (full-FT collapses perplexity 226→865) · [`negi-2025`](../literature/canonical/negi-2025_brain-informed-finetuning-multilingual.md) (positive per-individual encoding, full-FT, non-ppl-matched)
**Code:** **no new code** — `run_brain_lever.py` with `--uids` + `--lora-r 64`/`--no-lora` + `--epochs`. Verdict: `analyze_e008.py` (crossed inference).
**Output:** `outputs/E011_heavylora_Qwen.json`, `outputs/E011_fullft_Qwen.json`

## The question
Does a per-individual brain-specific alignment gain (kd_brain − kd_brain_permuted, held-out unique R²) emerge under a **stronger** brain-tuning regime than E008's light LoRA — and if it does, is it **perplexity-confounded** (L011)?

## The design insight (corrected after oracle HOLD) — the twin matches the REGIME, not the outcome perplexity
Both arms run under the **identical regime/objective** (same retention + brain-MSE form, steps, lr, data, seeds), differing only in the brain *target*. **What this matches is tuning intensity — NOT outcome perplexity.** Under light LoRA the brain term is tiny so both arms empirically land at the same ppl (E005: 55.4≈55.3, *measured*, not guaranteed). Under heavier tuning the brain-MSE gradient moves the shared base, and real BOLD (which shares variance with the linguistic structure the LM already encodes) is *less destructive* to the LM than permuted BOLD → **the arms' perplexities can diverge**, and a gap could then be "real target is more learnable → less LM damage → higher uR² via L011," NOT brain-specific. So matched-ppl must be **verified post-hoc per subject**, and the contrast is interpreted via a ppl-covariate read-out (below). This is why we keep a **matched-ppl guardrail** and do NOT run full-FT-to-collapse (E004: ppl 865 = a wrecked model where the L011 confound is maximal and uR² is meaningless).

## Regime (oracle PASS spec) — Regime A only: heavy LoRA, ppl-guardrailed (9 UIDs; crossed subject+fold inference)
- **Heavy LoRA:** `--lora-r 64 --epochs 6` (≈4× the light-LoRA capacity/steps) — moves the representation much more than E008 while keeping ppl bounded. **Predeclared ppl guardrail:** interpret the contrast only where per-arm ppl stays within ~2× base (the E005 band); flag/disqualify cells that exceed it.
- Arms: `mse` (kd_brain) vs `mse_perm` (**n_perm=5**, matched-regime brain-specificity null) + `lm_only` reference. 2 seeds × 5 folds × 9 UIDs.
- **Full-FT dropped** (the oracle's point: it forfeits the matched-ppl control that is the paper's core, and n=3–4 under collapse-variance is the weakest possible null; the real distance from Negi is *loss + data*, not tuning scope — see honest scoping).

## Claim tuple / decision rule (PREDECLARED)
- **Metric:** across-subject mean of per-subject e_u = median over folds×seeds of (uR²(mse) − uR²(mse_perm)), held-out; crossed subject(n=9)+fold inference (conservative fold-clustered CI is the headline, as E008).
- **ppl-confound read-out (oracle fix):** per cell record (uR²_real, ppl_real, uR²_perm, ppl_perm). (a) flag any subject where ppl_real and ppl_perm diverge beyond the guardrail. (b) regress per-cell ΔuR²(real−perm) on per-cell Δlog-ppl(real−perm); **report the intercept (effect at matched ppl) as the brain-specific estimate** — a gap that lives only where ppl diverges is L011, not brain.
- **NULL is REGIME-ROBUST (strengthens the paper):** at matched ppl (the intercept and the guardrailed cells), the per-subject brain-specific gap CI includes 0. → E008's null is not an artifact of *light* tuning; the "you under-tuned" objection is refuted **within our paradigm** (MSE-readout, isolated sentences).
- **Per-individual POSITIVE emerges:** the matched-ppl intercept gap CI excludes 0, brain-specifically, surviving LOO-fold/LOO-subject. → a genuine per-individual brain effect at matched ppl (major positive — rewrite toward Fork-A-with-caveats). If the gap exists only at diverged ppl → L011, reported as such.
- **Anti-confound:** unchanged (rotating folds, static nuisance from untuned base, permuted twin n_perm=5, per-subject).

## Honest scope vs Negi (oracle fix)
E011 varies only **tuning intensity** within our paradigm. Negi 2025 differs on **three** axes — loss (NT-Xent contrastive vs our co-trained MSE), data (continuous naturalistic narrative + FIR/Lanczos temporal model vs our isolated decontextualized sentences), and optimizer scope (full-FT vs LoRA). E011 therefore **cannot reproduce or refute Negi**; it answers "is our per-individual null robust to tuning intensity?" The remaining distance from Negi (loss + data) is left untested and stated as such in the manuscript.

## Compute / scope
Heavy LoRA: 9 UIDs × 5 folds × 2 seeds × (mse + 5×perm + lm_only = 7) = 630 trains (heavier per-train than E008 via r=64/6ep). Stage across the 4 L40S by UID. Pure in-domain; no new data. Verdict via `analyze_e008.py` + the ppl-covariate read-out.

## Results (ran 2026-06-12; heavy LoRA r=64/6ep, 9 UIDs, 2 seeds, n_perm=5, 4-GPU split)

Per-subject brain-specific gap (mse − mse_perm, held-out unique R²): **mean +0.00043, t-CI [−0.0005,+0.0013] (incl 0), n=9, sign 6/9**; fold-clustered CI incl 0, fails LOO-fold; held-out-5 mean **−0.00012**; ppl matched (mse ≈ perm ≈ 60 ≈ 1.33× base, within guardrail); ppl-intercept +0.00048; SNR control collapses it (drop top-2 → +0.00008).

## Verdict: the per-individual null HOLDS — but it is robustness to LoRA *capacity*, NOT to a stronger manipulation (counter-argument-corrected, L019)

The counter-argument panel (fable) caught that **heavy LoRA did NOT actually move the representation more than E008's light LoRA**: mse absolute held-out uR² **+0.00076 (E008) → +0.00082 (E011)**, ppl rise **1.32× → 1.35×** base — statistically identical on both the optimized quantity and the LM-damage proxy. At fixed λ_brain=10 on isolated sentences the alignment gradient is exhausted early, so 4× rank/epochs buys ~zero extra effective movement. So this is **the same operating point run twice**, not a stronger regime. Also: the +0.00043 (vs E008's +0.00010) is **one subject — uid 875 = 79% of the across-subject sum; LOO-subject → +0.00010, identical to E008** (the L015/L016/L018 outlier pathology, 4th occurrence). It fails its own permuted null (gap ~18× below p95; `beats_permuted_null=False`). The ppl-intercept read-out is *vacuous here* — the arms barely diverge in ppl (Δlog-ppl −0.013), so there was no confound to adjust.

**The honest, complete claim (no new run needed):** within the matched-perplexity regime the per-individual brain-specific null **cannot be escaped** — raising LoRA *capacity* (r, epochs) at fixed λ does not move the representation (E011); raising the knob that *does* (λ_brain) **wrecks perplexity** (E009/L017: λ=30 → ppl 92) *and still does not grow the gap*. So we claim "robust to LoRA capacity at fixed λ and matched ppl," NOT "robust to stronger tuning." The genuinely different regime (Negi's full-FT + NT-Xent contrastive loss + naturalistic narrative data) is on the **loss+data axes** E011 does not touch — the real, honestly-stated open boundary (needs data/objective we don't have).

## Status
COMPLETE — verdict recorded (capacity-robust null; honest framing). Manuscript §6 + L019 updated. No further per-individual-at-matched-ppl experiment is informative (capacity exhausted, λ breaks the control); the only open direction is a different objective+data regime (future work / new data).


## Retained load-bearing artifacts

| Artifact | SHA-256 |
|---|---|
| `outputs/E011_g0.json` | `299ca57c7733932d9272a44d06fe3cb6976ec535a887b5ad27072002426ea9e2` |
| `outputs/E011_g1.json` | `f3963b67cc01e0fae3807de354b613d4e6a3ca6ff8c6e55e1eed6b7c8b719bd3` |
| `outputs/E011_g2.json` | `136449382dc627d5007df84b248b3c63d8b9bd4e2d1164c7399afbb9b867b4ce` |
| `outputs/E011_g3.json` | `4da6639f3943c931beab6b7189fd6a03248161c846180a225e0e9c17af5b0745` |

## Related
- [`status.md`](../status.md) — the canonical status board
