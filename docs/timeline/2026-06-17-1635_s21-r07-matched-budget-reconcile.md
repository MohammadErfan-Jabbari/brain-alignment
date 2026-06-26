---
title: "S21 — review S20's E003 repair + close R07's one pending edit (analysis; no science changed)"
tags: [timeline]
---

# S21 — review S20's E003 repair + close R07's one pending edit (analysis; no science changed)

**Date:** 2026-06-17 · **Session:** S21 · **Branch:** main · **Mode:** analysis

## Purpose

Erfan asked me to review the S20 working session (the E003 record-provenance repair that this
analysis lane had flagged) and judge whether it resolves everything R07 needed. Then make the one
R07 edit S20 correctly could not (D011: a working session never edits an analysis-lane report).

## What happened

1. **Reviewed S20** against the 7-item acceptance checklist I wrote into [`tasks.md`](../tasks.md) (S19). Verified
   the artifacts directly: `outputs/E003_perplexity.json`, `outputs/E003_dissociation.json`, the two
   new scripts, and the E003.md repairs (Output pointer, untrained→order-of-magnitude, multiplier
   "≈6.4× the teacher (≈4.5× the gpt2 student)", dissociation citations + E015 forward-pointer, the
   epoch-asymmetry note, the Provenance-repair section). All four flagged gaps closed; R07 md5
   confirmed byte-identical in S20. **Verdict: S20 resolved the E003 side fully**, and improved on my
   spec in two places — it refused to force the bootstrap P-values to reproduce within rounding
   (that would be tuning-to-target) and downgraded them to a construction-sensitive qualitative
   claim, and it found a 5th gap I had missed (cold ran 2 epochs vs warm 1 → step count not matched).

2. **The one required R07 edit.** That 5th fact makes R07's "matched optimizer-step budget" / "at
   matched budget" claim false as-run. Fixed both (the only R07 change this session):
   - Stop-rule sentence: now "a matched corpus, batch size, learning-rate schedule and max-length",
     with an explicit clause that the cold arm ran two epochs to the warm arms' one (~2× the steps),
     "which only deepens the under-training caveat rather than flattering it."
   - Last caveat: "at matched budget" → "at a matched corpus and compute budget (and … the cold arm
     in fact ran twice the epochs, so even the step count was not matched)."
   - **Everything else byte-identical**: verdict PARTIAL, Δ=+0.018, ρ′=0.37 [0.14, 0.58], r=−0.88, the
     table. Reference ppls were *confirmed* (74/105/169) by S20, so R07's ppl column needed no change.
   - `run_checks --layer report` on R07: `ai_tell_lint` clean, 0 em-dashes; only the known
     caption-cited table-cell bare-number findings remain (identical to R06's house style). `2b0477b`.

## Verification

- No alignment number, no verdict, no rung changed — Q1 stays ✅ PARTIAL (R07 wrote up an
  already-recorded verdict; this session only corrected one design-description clause).
- Diff since session start (`1b3c8a1`): a single 2-insertion/2-deletion commit to R07.

## Outstanding

- Optional, Erfan's call: R07 could add a half-clause that the dissociation P-values are
  construction-sensitive (now documented in `outputs/E003_dissociation.json`). Left out — the existing
  "marginal, p≈0.09" wording is correct and the caveat is already tight.
- Pre-existing untracked files in the tree ([`docs/manuscript/supervisor-email_2026-06.md`](../manuscript/supervisor-email_2026-06.md),
  `untitled.md`) are from the earlier manuscript work, not this session; left untouched.

## Next session

Analysis lane: **R08** (Q2 — the lever is real but weak and ppl-confounded), or the extended
manuscript (front matter + Methods + Results Q0–Q1 from R06/R07), through `scientific-writing`, full
loop. Working lane has no queued decisive work.


## Related
- [`ladder.md`](../ladder.md) — the canonical status board
- [`map.md`](../map.md) — code system (Q/E/A/D/L) & journey map
