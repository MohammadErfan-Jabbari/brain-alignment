# Session 8 (continuation) — per-individual null robustified across all axes; manuscript completed as an artifact

**Date:** 2026-06-12 · **Mode:** working → analysis (long autonomous `/goal` run) · **Cost:** ~$1217 (authorized)

This log covers the continuation of Session 8 after the panel-audit/E008 reframe (prior log `2026-06-11-2301`). The arc: take the Fork-B result and (a) stress every remaining axis the per-individual null could be escaped on, (b) turn the manuscript from content-complete into a complete artifact. The session's *method* — run the thinking panel after every result and let it correct me — is itself the durable lesson.

## What ran (each followed by a panel pass)

1. **E011 — heavy LoRA (tuning intensity).** r=64/6ep, 4× capacity, n=9. Per-subject +0.0004 [−0.0005,+0.0013], incl 0. Heavy LoRA did *not* move the representation more (mse abs uR² +0.0008 in both regimes; ppl ~1.33× base both) → robustness to LoRA *capacity*, not to a stronger manipulation. The knob that moves the rep (λ) wrecks ppl. **Null holds.** (L019)

2. **E013b — contrastive/InfoNCE objective.** Added symmetric InfoNCE to `brain_loss.py`; ran per-individual n=9 (same crossed inference). Mean −0.0002 [−0.0008,+0.0005], ppl-intercept −0.0003 at matched ppl. Switching MSE→contrastive (Negi's loss family) **does not change the per-individual verdict** at ROI granularity. (L025)

3. **E013 — voxelwise same-substrate (the substrate-mismatch test).** Built the voxelwise per-individual tuning loop (`run_lebel_tune.py`, the tractable "E007"): per-segment HRF-delayed BOLD target + brain-MSE readout/LoRA + held-out-story unique-R² eval (E006 protocol) + permuted twin. **v1 (n=3, no KD anchor, λ=10): FAILED MANIPULATION** — counter-argument caught that real-target tuning *reduced* held-out alignment below base in all 6 subject×seed runs (the rep was degraded, not made brain-specific) → the ~0 gap compared two degraded reps → uninformative. **Retracted the v1 claim.** v2 λ-sweep on UTS03 with KD anchor: at NO λ does the brain-MSE lever improve held-out alignment over base (neutral at λ=1, monotonically degrading above), and it never beats its permuted twin. **The voxelwise distillation-readout lever does not take hold** — a single-subject *mechanism* failure, so n≥5 is moot (more subjects can't rescue a manipulation that fails on one). Reinforces the per-individual null; not a clean same-substrate null. (L026/L027)

4. **E014 — averaging on the ENCODING brain-score (attempted "main-track lift").** `run_averaging_encoding.py`: ridge unique-R² per-subject vs k-averaged Tuckute target, n=9. Per-subject mean +0.0069 (7/9 positive), 5-UID-avg +0.0357 → ~5×, monotone dose-response. **Panel (counter-argument + first-principles, fable) DEFLATED the confound-lift claim:** per-subject scores are *positive* (unlike E008's well-powered zero), so "averaging manufactures a gap absent per-person" does NOT transfer to the encoding side — the signal is present per-individual, averaging just measures it with less noise. The ~5× is mostly legitimate (NC rise ~1.7× + ridge approaching the raised ceiling + near-zero denominator) — an estimand shift, not a confound. **Verdict: E014 is NOT a main-track lift; the headline stays on E005-vs-E008.** Found+fixed an unseeded-PCA determinism bug (`pilot_lib.py` — no random_state; headline results robust as they aggregate over many PCA calls). **Verified BEFORE folding into the paper → manuscript correctly unchanged.** (L028)

## Manuscript → v0.9, COMPLETE-AS-ARTIFACT

- Added a **References section** (19 from canonical notes via a paper-digest sub-agent + 2 added after the completeness check = 21; `[VERIFY]` flags on the 5 memory-sourced entries).
- A **completeness-critic pass** (sonnet) found orphan citations (Hoak 2025, Li/Brendel 2019 — added) and dangling `§6.5`/`§6.6` pointers (→ `§6(5)`/`§6(6)`). Fixed.
- Every in-text citation now resolves to a reference; every cross-ref resolves. Gate = READY (thesis/workshop).

## The methodological result (the session's spine)

The thinking panel corrected **three** of my own overclaims this session: E005 pseudo-replication (L015), E013 v1 failed-manipulation (retracted), E014 confound-lift (deflated). Each time I generated an exciting result and the panel bounded it to the honest one — and the honest core (well-powered per-individual null + the averaging confound where per-individual *is* zero + A2-real) held every time. The E014 case is the loop working *as designed*: verified before publishing, so nothing had to be retracted from the paper.

## State at close

Experimental program **complete and panel-bounded**; per-individual null **robust across light/heavy LoRA, MSE/contrastive, ROI/voxelwise**. Manuscript artifact-complete + gate-READY. Everything captured to gbrain (`projects/brain-alignment-s8-paper-artifact-complete`).

**Two genuine decision points remain for Erfan:** (1) confirm the ladder flip (experimental program complete → write-up); (2) choose between submitting v0.9 (measurement-validity contribution) and committing a fresh session to the one untested door — full-FT (not a distillation readout) on multi-subject naturalistic voxelwise targets (denizenslab n=6; mechanism evidence suggests likely-null but it's the only path that could move the verdict).
