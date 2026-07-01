---
title: "Upspeed - last-session state (read first)"
tags: [reference]
aliases: [upspeed]
---

# Upspeed - read first, write last

**Last updated:** 2026-07-02 (S46 - retroactive close for the recent `/write` + `/review` + `/meta` manuscript sessions. Dominant stance: `/write`. **NO experiment, NO science number, NO rung change - Q0-Q5 stand exactly as S25.**)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md).** With no task, run `/orient`.

## Current state

The recent unwrapped sessions moved the extended manuscript forward rather than the experiment ladder. Section 4.1 (Q0) and Section 4.2 (Q1) have been rewritten in the reader-facing pattern mined from the prior Claude/OpenCode sessions: verdict first, numbers separated from interpretation, caveats kept local, and no compliance-list prose.

Figure 5 is finalized for the KD/Q1 story. The source and rendered artifact now match the current manuscript: Panel B is titled "Quality entanglement," the x-axis is held-out perplexity on the log scale, the non-teacher fit label is separated from nearby points, and `distilgpt2` is named consistently.

## What was done

- Reviewed the prior session material and the existing manuscript-readability lesson list. Root cause: the prose kept treating each paragraph as a container for obligations instead of as a guided argument for a reader.
- Finalized Figure 5 in [`manuscript/figures/fig05_kd_retention.tikz`](manuscript/figures/fig05_kd_retention.tikz) and regenerated [`manuscript/figures/fig05_kd_retention.png`](manuscript/figures/fig05_kd_retention.png).
- Rebuilt [`manuscript/extended/main-extended.pdf`](manuscript/extended/main-extended.pdf). The build succeeds; the remaining overfull warnings at `main-extended.tex:54` are pre-existing.
- Polished [`manuscript/extended/sections/04_results.tex`](manuscript/extended/sections/04_results.tex): Section 4.1 now separates confidence intervals from voxel-positivity percentages, and Section 4.2 now presents Q1 as headroom plus a quality caveat rather than as a stronger causal KD claim.
- Committed the manuscript work as `fd92346 docs(manuscript): polish results q0 q1 prose and figure 5`.
- Changed the repo's wrap rule: close-session commits should now be pushed to `origin` by default unless Erfan says not to or the push is blocked (D054).

## What to do next

- Continue the Results pass with Section 4.3 (Q2 / E004): apply the same pattern as 4.1 and 4.2, especially around the pseudo-replication caveat and the "undemonstrated, not proven zero" wording.
- Keep the parked `/interpret` item visible: E006's voxelwise CI unit remains a separate adjudication task if the manuscript needs inferential wording beyond the current descriptive treatment.
- On every wrap from now on: commit scoped changes, then push `main` to `origin` by default and report the push result.

## Blockers / open loops

- `docs/manuscript/README.md:34` still has a pre-existing bare `+0.06` with no cite; fix on the next manuscript README touch.
- The build warning at `docs/manuscript/extended/main-extended.tex:54` remains pre-existing.
- Before this wrap, `main` was 83 commits ahead of `origin/main`; this close is expected to push the accumulated history.

## Key facts

- `docs/manuscript/extended/main-extended.pdf` builds with Tectonic from `docs/manuscript/extended/`.
- Section 4.2's supported Q1 claim is: plain perplexity-only KD leaves alignment headroom below the teacher, but the loss is entangled with model quality; matched-perplexity causal recovery moves to the powered voxelwise substrate.
- Git close rule is now D054: scoped commit first, push to `origin` at wrap by default.
