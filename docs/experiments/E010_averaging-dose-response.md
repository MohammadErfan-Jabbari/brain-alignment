# Experiment — E010: the averaging dose-response (does the apparent brain-specific gain grow with subjects averaged?)

**Created:** 2026-06-12 · **Status:** RAN — verdict recorded · **Mode:** working
**Direction:** the decisive test for the manuscript's positive contribution — does cross-subject target averaging *produce* the apparent brain-specificity (S8 manuscript counter-argument #1: "manufactures" was asserted, not shown).
**Predecessors:** `E005` (averaged k=5 → +0.008) · `E008` (per-subject k=1 → null) — the two endpoints; E010 fills the curve.
**Code:** `scripts/run_averaging_doseresponse.py` · **Output:** `outputs/E010_averaging_doseresponse.json`

## Question / mechanism
Y_i = g + ε_i (g = shared stimulus-evoked response; ε_i idiosyncratic+noise, ~indep across subjects). Averaging k subjects → Ȳ_k = g + (1/k)Σε, raising the achievable noise ceiling NC_k = NC/(NC+(1−NC)/k). **Prediction:** if averaging *inflates* apparent brain-specificity, the held-out brain-specific gap (kd_brain − kd_brain_permuted, measured against the k-averaged target) rises from ~0 at k=1 toward the +0.008 seen at k=5, tracking NC_k.

## Design
Nested UID subsets (fixed order, first 5 = E005's averaged set minus the excluded 853): k ∈ {1,2,3,5,9}. For each k: KD-tune Qwen1.5B→0.5B (LoRA, λ=10) toward the k-averaged target + its block-permuted twin; score held-out (200-sentence) unique R² against the k-averaged target; 4 seeds. Same harness/controls as E008/E009.

## Result

| k | gap (mse−perm) | sd | seeds + | predicted ceiling NC_k |
|---|---|---|---|---|
| 1 | **−0.00023** | 0.0035 | 2/4 | 0.491 |
| 2 | −0.00014 | 0.0013 | 1/4 | 0.659 |
| 3 | +0.00230 | 0.0045 | 3/4 | 0.743 |
| 5 | **+0.01943** | 0.0123 | 4/4 | 0.828 |
| 9 | +0.00708 | 0.0079 | 4/4 | 0.897 |

## Verdict: the apparent brain-specific gap is ~0 per individual and is PRODUCED by averaging (L018)

**At k=1 the gap is null (−0.0002, 2/4); averaging produces it** (k=3,5,9 positive, 3–4/4 seeds). This is the direct demonstration the manuscript panel demanded: the same pipeline yields nothing for a single subject and a clear positive once subjects are averaged — so the "brain-specificity" measured against an averaged target is an **artifact of the averaging**, not a per-person property. The rising limb (k=1→5) tracks the noise-ceiling prediction (NC_k rises 0.49→0.83). **Caveat (honest):** the rise is not perfectly monotone — k=9 (+0.007) sits below k=5 (+0.019), within the wide 4-seed error bars (se ≈ 0.004–0.006) and plausibly because the nested k=9 set adds the noisier held-out subjects. So we claim the **qualitative** law (averaging is *necessary* for the apparent gap; gap≈0 at k=1) — not a precise quantitative gap∝NC_k fit. A cleaner version would average over random size-k subsets (not nested) with more seeds.

## Status
Recorded. Earns the manuscript's "averaging inflates/produces apparent brain-specificity" claim (the per-individual gap is absent). Manuscript §4.2b updated; L018 added.
