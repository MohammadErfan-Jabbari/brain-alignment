---
title: "Confound catalog — the single source of truth for the control battery"
tags: [reference]
---

# Confound catalog — the single source of truth for the control battery

**What this is.** The one place the repo's confounds, controls, and the matched-perplexity / 5-control
battery live. `counter-argument`, `oracle-reviewer`, and `anti-confound-designer` all **read this file**
instead of each hard-listing the catalog (which used to drift between prompts — D-fix B, S24). When a new
confound lesson lands, add it **here** and the agents inherit it. Each row: the confound, how it fools you,
the control that neutralizes it, the lesson it came from.

## The confounds (and their controls)

| # | Confound | How it fools you | Control | Source |
|---|---|---|---|---|
| C1 | **Split leakage / temporal autocorrelation** | adjacent timepoints share signal; a random split lets train leak into eval → inflated unique R². | **Contiguous** (story/block-level) folds; never random-shuffle timepoints. | L003 |
| C2 | **Low-level nuisance** (sentence length, position, phone/word-rate) | the LM feature correlates with a surface property the brain also tracks → "alignment" that is really length/rate. | Regress out the full nuisance tier **before** scoring; report **unique** R² after subtraction. | L003 |
| C3 | **Imageability / lexical semantics** | a static-embedding/imageability axis eats a large share of apparent unique variance. | Add eng1000 / static-embedding nuisance columns; L012 showed it ate ⅓–⅔ of a "unique" R². | L012 |
| C4 | **LM-quality (perplexity) masquerading as brain-specific** | a better LM aligns better for free; a gain vs a *non-ppl-matched* baseline is a quality effect, not a brain effect. | **Matched-perplexity** baseline (not just matched compute/budget); use **bpb**, not per-token ppl, on an **in-distribution** probe. | L011, L030 |
| C5 | **Cross-subject target averaging** | averaging a group fMRI target amplifies the shared stimulus-evoked component at an inflated noise ceiling → an apparent "brain-specific" gain that no individual shows. | Per-subject inference; a per-kind **permuted-twin** null; never read brain-specificity off a group-averaged target. | E008 / L016 |
| C6 | **Pseudo-replication** | `n` counted as cells that share a stimulus/fold → CI too tight; "power 1.0" that is a group-mean property, not per-brain. | Bootstrap over the **independent unit** (subject/fold); report honest effective n; crossed subject×fold clustering. | L015 / L016 / L029 |
| C7 | **One-unit dominance** | a single fold / voxel-cluster / seed carries the whole effect. | Leave-one-unit-out; report the swing (the E004 fold-4 problem). | E004 |
| C8 | **Invalid permuted-twin null** | the "null" leaks signal or differs from the real arm in a second way besides brain structure. | Confirm the twin matches everything but the tested structure; phase-randomized shape-twin for aux targets (matches autocorr+marginal, zero content). | E021 / L049 |
| C9 | **Garden-of-forking-paths** | the verdict-bearing contrast was chosen *after* seeing the data. | Predeclare the estimand + contrast + kill criterion **before** running (D003). | D003 |
| C10 | **Magnitude vacuity** | the effect is real but too small for the sentence written. | Check vs the noise floor and the **Hadidi/Feghhi residual ≤10%** bound before claiming. | hadidi-2024 |

## The 5-control battery (S24 — for privileged-information / aux-target experiments)

Apply only the applicable arms; mark the rest **N/A** with the reason.

1. **Phase-randomized shape-twin** — a content-free twin matching the target's autocorrelation + marginal; if the real signal doesn't beat its shape twin, it's a shape artifact (C8).
2. **Zeroed / shuffled privileged-information** — replace the signal with zeros/shuffle; if performance holds, it's not the signal (Provodin TRAM; Pirlot shuffled-label).
3. **Did-the-representation-move gate** — a ppl-preserving no-op is "no manipulation," not evidence; confirm Δrep above the exhaustion floor before scoring (L042).
4. **Matched-perplexity + per-subject + crossed fold/subject clustering** — inherited rigor (C4–C6).
5. **Matched-information non-brain privileged teacher** — the signal must beat the best non-brain teacher (LM surprisal / teacher-hidden-state / difficulty) at matched capacity+reliability; only this shows a gain is *biosignal-specific*, not "any teacher helps."

> Maintenance: add new confound rows here as `L`-entries land; do not re-list the catalog inside agent prompts.


## Related
- [`ladder.md`](../ladder.md) — the canonical status board
- [`map.md`](../map.md) — code system (Q/E/A/D/L) & journey map
