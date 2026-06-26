---
title: "Session 14 — autonomous working: F1-close (E020) + F2 (E019) + idea refinement"
tags: [timeline]
---

# Session 14 — autonomous working: F1-close (E020) + F2 (E019) + idea refinement

**Date:** 2026-06-14 · **Mode:** working (autonomous /goal: implement forward-program layers, continuous subagent
verification, literature grounding, gbrain, iterative idea refinement). **Ladder:** NO rung flips (L3/F1 stays ❌);
the spine is fully supported by POWERED evidence; the implementation lane's decisive work is COMPLETE.

## What ran (chronological)

### F1-close = E020 (empirical-E[Y|S] ceiling) — DONE, panel-survived
- Oracle HOLD on the locked design → hardened (ratio claim, repeat-split G1, reference-reliability gate G2,
  story=replication-unit G3). Pre-lock socratic + first-principles caught the claim was over-scoped → corrected to the
  linear-channel + convergence framing (L039: a shared-LM probe of LOO residuals is ~0 by construction).
- Built `run_eys_ceiling.py` + `run_eys_diagnose{,2}.py`. Ran story_11 (n=6, Qwen2.5-0.5B L12). Naive flag fired:
  A_resid (LM→ε) = +0.090, ρ=0.51 (apparent Fork-A). **NOT escalated — diagnosed.** Two diagnostic rounds +
  counter-argument + premortem: after fold-gaps + eng1000-partial the trained−untrained residual gap = **−0.018 ≈ 0**
  ⇒ confirmed ARTIFACT (leaked stimulus via too-noisy n=5 reference + HRF autocorrelation). The eng1000 nuisance-partial
  is partly vacuous (symmetric partial collapses A_shared +0.176→+0.033 too — L040).
- **Verdict: NO Fork-A; ceiling bounded-not-closed** (2nd instrument to wall at n=6 after TRIBE: ref-rel 0.33, ε-NC 0.17).
  Demoted to convergent corroboration. D029/D030, L039/L040.

### F2 = E019 (external reproduce-and-control) — DONE, panel+positive-control-survived
- Grounded the target (first-principles design-grounding): Negi-2025 ENCODING gain. Oracle HOLD → **moved substrate
  denizenslab→LeBel** (D031; denizenslab walled twice). Built the **faithful Negi head** (`run_e019_negi.py`:
  differentiable Lanczos (verified vs lanczosinterp2D, max|Δ|=2e-6) + FIR + NT-Xent full-FT). Smoke-validated.
- Ran 3 GPUs in parallel: gentle 3×3 (GPU0), strong probe (GPU1), intermediate-lr sweep (GPU2). **No positive gain at
  any lr** (gentle gain_r −0.0006±0.0027 n=9; sweep 2e-5/3e-5/5e-5 monotone-negative; 1e-4 catastrophic ppl→11.5k).
- Counter-argument + premortem + an **eval positive-control** demolished the over-claim: the raw-mean-r ruler is
  quality-INSENSITIVE (enc_r 0.5B+0.150 ≈ 3B+0.143), the gentle regime didn't move the LM (Δppl≈0), decoder≠Negi's BERT.
- **Verdict: E019 = corroboration of the E008/E011/E017 lever-failure spine, NOT the external clincher.** "NON-NEGOTIABLE"
  framing RETIRED. D032, L042.

### Idea refinement + literature grounding (lit-scout + first-principles + paper-digest)
- **SCOPE correction (L041):** evidence supports the OPERATIONAL claim ("no brain-specific gain is INDUCIBLE beyond
  perplexity via the readouts tried"), not the information-theoretic "ε is task-independent noise"; Y⊥θ\*|S is an
  ASSUMPTION. Applied to the ladder spine wording.
- **DPI selection side-channel** = the remaining hole (argued-shut by E009 ~0 fulcrum, not measured-shut).
- **Negi passes the permuted twin (Δr=0.133)** → for encoding the missing control is matched-ppl (clincher = b−c).
- **Lit positioning:** NOT scooped. New must-cites — Jia-2026 L-PACT (frozen-only scope-fence; canonical note written),
  Raugel/King NeurIPS-spotlight (size+context ≠ bpb-quality), Hadidi/Feghhi → Nature Comms 2026. Refocused headline locked.

### Forward-program completion (D033)
F3 (denizenslab n=6 full-FT) = SUPERSEDED/moot (powered full-FT null in hand via E017 + corroborated by E019;
denizenslab walled + blind-ruler). F4 (E015 Q2) = analysis-lane. **The implementation lane's decisive work is COMPLETE;**
the spine rests on POWERED evidence (E006 · E008/E011/E013/E017 · L016 · E020 · E015 · E019-corroboration).

## What's next (analysis lane — Erfan)
Scope correction in the manuscript (L041); reframe to the refocused headline; lit positioning; figures. No new compute
needed to write the paper. F3 only if Erfan wants literal 100%-rule coverage.

## Process / cost
~12 subagent runs (oracle×2, socratic, first-principles×3, counter-argument×2, premortem×2, lit-scout, paper-digest,
Explore). 3 gbrain writes + reads. ~19 atomic commits. 3 L40S GPUs in parallel. No rung flips; no Fork-A; no
analysis-lane edits beyond the ladder spine-wording scope correction (flagged for Erfan's manuscript pass).


## Related
- [`ladder.md`](../ladder.md) — the canonical status board
- [`map.md`](../map.md) — code system (Q/E/A/D/L) & journey map
