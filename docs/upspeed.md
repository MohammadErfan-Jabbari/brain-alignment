---
title: "Upspeed - last-session state (read first)"
tags: [reference]
aliases: [upspeed]
---

# Upspeed - read first, write last

**Last updated:** 2026-07-02 (S47 - `/write` manuscript cleanup + Figure 6 deferral. **NO experiment, NO science number, NO rung change - Q0-Q5 stand exactly as S25.**)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md).** With no task, run `/orient`.

## Current state

Results Section 4.1 and 4.2 are current for this checkpoint. Section 4.2 now avoids the weak handles Erfan flagged: `screen` became the specific Tuckute ROI benchmark/comparison, and the old "same screen also narrows the verdict" sentence now states the actual logic: the E003 comparison limits the claim because alignment tracks log-perplexity across the five non-teacher arms.

The manuscript tree has no remaining standalone `screen` and no `prose`/`verdict` strings after the cleanup. The skills were deliberately not changed; Erfan said those should be rewritten from scratch later, not patched here.

Figure 6 is not final. It is the placeholder figure inside Section 4.3 (`fig:lever`, currently `../figures/fig_lever.png`) and belongs to Q2/E004, not to Section 4.2. It should be finalized only when Section 4.3/R08 is written.

## What was done

- Rewrote the unclear Section 4.2 sentence to: "That same E003 comparison also limits the claim..." with the quality/perplexity caveat stated directly.
- Replaced weak manuscript wording across `docs/manuscript/`: `prose`, `verdict`, and standalone `screen` were removed or made specific.
- Rebuilt `docs/manuscript/extended/main-extended.pdf`; the build succeeds with only the pre-existing overfull warnings at `main-extended.tex:54`.
- Committed and pushed the cleanup as `f7cd1e2 docs(manuscript): replace weak result wording`.
- Confirmed Figure 6 maps to Q2/E004: the "no demonstrated usable lever" question, with the honest fold-level interval including zero and the dominant-fold caveat.

## What to do next

- Write Section 4.3 (Q2 / E004) next.
- Finalize Figure 6 as part of that Section 4.3 pass, using the E004 record and the honest inference unit: folds, not pooled seed-fold cells; interval includes zero; fold 4 carries much of the old apparent signal; wording must say "undemonstrated, not proven zero."
- Keep the parked E006 CI-unit `/interpret` item separate unless the manuscript needs inferential wording the current records do not support.

## Blockers / open loops

- Figure 6 is intentionally deferred until Section 4.3/R08.
- `docs/manuscript/README.md:34` still has a pre-existing bare `+0.06` with no cite; fix on the next manuscript README touch.
- The build warning at `docs/manuscript/extended/main-extended.tex:54` remains pre-existing.

## Key facts

- `docs/manuscript/extended/main-extended.pdf` builds with Tectonic from `docs/manuscript/extended/`.
- Section 4.2's supported Q1 claim is: plain perplexity-only KD leaves alignment headroom below the teacher, but the loss is entangled with model quality; matched-perplexity causal recovery moves to the powered voxelwise substrate.
- Figure 6 belongs to Q2/E004 and should not be finalized as part of Q1/Section 4.2.
- Git close rule D054 remains active: scoped commit first, push to `origin` at wrap by default.
