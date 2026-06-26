---
title: "2026-06-10 15:19 — Course material adopted as theory-grounding source (Session 5, analysis)"
tags: [timeline]
---

# 2026-06-10 15:19 — Course material adopted as theory-grounding source (Session 5, analysis)

**Mode:** Analysis (consume + communicate evidence; produce understanding + docs; no new experimental number).
**Branch:** main. **Worktree:** /home/centcom/data/brain-alignment.

## What this session was

Erfan added his MSc coursework (Information Theory for ML + Probabilistic ML, UC3M 2025–26) to `data/course-material/` and asked how best to preprocess it and fuse it into the repo's instructions/docs so future sessions use it as a source of truth alongside the papers and datasets. The explicit ask: run subagents to understand the material, then recommend a preprocessing approach (run the pdf skill? derive cleaned md? something else?), then integrate.

## What was understood

- **It is not an extraction problem.** The material is 125 files / ~292 MB: 57 PDFs (slide decks + paper readings) and 44 markdown notes (~930 KB). The lecture decks already have Erfan's own `*_study.md` (teaching notes) and `*_OCR.md` (audited formula reconstructions) from a `course-lecture-study` workflow. The slide PDFs are sparse (≈700–1100 chars/3pg); the existing notes are *higher quality* than any fresh OCR. So: **no re-OCR.** The job is curation + integration. (→ L010, D014.)
- **The thesis payoff is exact, not thematic.** Three recon subagents (2× Sonnet concept→thesis mappers, 1× Haiku asset auditor) established that the course supplies, in proved form, the math R03 was invoking informally:
  - R03's **weak-prior bound** = the **MI generalization bound** $\overline{\mathrm{gen}}\le\sqrt{2\sigma^2 I(W;Z^n)/n}$ (info-theory L26).
  - R03 §2 Step 4's "already in the text" + the compression brake = the **data-processing inequality** $I(Z_{\text{student}};B)\le I(Y_{\text{teacher}};B)$ (L6); the course note's own "deployment reading" states it.
  - The **"unique R² after nuisance subtraction"** the anti-confound protocol reports = **conditional mutual information** $I(\text{LM};B\mid\text{nuisance})$ (L4).
  - The **F1 alignment-vs-rate trade-off curve** = the **rate-distortion function** $R(D)$ (L1).
  - Prob-ML side: the encoding model (ridge → fMRI) IS a Bayesian Gaussian MAP estimate (Block 1); TabPFN maps to the F2 low-data framing.
- **Gaps (deferred, all adjacent):** info-theory L16–17 (Fisher/Cramér-Rao) and prob-ml Block 4 VAE papers (IWAE/GMVAE/VQ-VAE/NVAE/VampPrior) have no notes. Candidates for `paper-digest` only if they become load-bearing.

## What was written / changed

- **New `docs/06-theory-grounding.md`** — the curated concept→thesis map (load-bearing vs adjacent), condensed syllabus inventory, gap list, storage/preprocessing decision, file-coverage pointers. The committed source of truth for the coursework.
- **New `data/course-material/INDEX.md`** (gitignored) — file-level navigation for direct browsing; points at 06.
- **`docs/reports/R03_brain-as-training-signal.md`** — (a) **fixed line-1 corruption** (a chunk of IT-lecture transcript had been pasted in front of the `# R03` heading in the working tree; HEAD was clean); (b) added **§2 Step 7** grounding the first-principles bounds in the course's exact theorems; (c) §7 note pointing to 06. (Pre-existing uncommitted `$$…$$` multi-line reformatting in the working tree was left intact and is bundled into this commit.)
- **`docs/01-research-landscape.md`** §E — added the formal theory tools (MI bound, DPI, conditional MI, rate-distortion) with a pointer to 06.
- **`CLAUDE.md`** "Read this first" — named the coursework as the third external source (papers / datasets / coursework), with the no-re-OCR rule.
- **`docs/README.md`** — added 06 to the map.
- **D014** logged; **L010** logged.

## What did NOT change (the science)

No experiment ran; no number was produced or altered. The R03 ladder is unchanged: the next *working* step is still Layer 1 (brain-tune Qwen2.5-0.5B / GPT-2 on Tuckute, verify unique R² rises). The course grounding is scaffolding for *writing* the methods/related-work, not new evidence.

## Heads-up for Erfan

- **R03 line-1 corruption** was a stale working-tree artifact at session start (transcript pasted in front of the heading; HEAD was clean). Fixed. The pre-existing `$$…$$` multi-line reformatting in the same working-tree diff was left intact and is bundled into the R03 grounding commit.
- **A concurrent session committed while this one ran:** `9c6dcb7` (full-read digests of the 12 brain-as-training-signal papers), `93db8ae` (landscape-map update after that pass), `d5314b2` (new `reports/R04` gap analysis). So the canonical notes (`moussa-2025`, `oota-2026`, `merlin-2026`, `moussa-2025b`) are **already committed**, not pending. My `01-research-landscape.md` §E edit was applied on top of the post-`93db8ae` version (Read+Edit matched cleanly). Next session: reconcile R03 §2 Step 7 / the new R04 / the updated landscape so the framing is consistent across all three.


## Related
- [`ladder.md`](../ladder.md) — the canonical status board
- [`map.md`](../map.md) — code system (Q/E/A/D/L) & journey map
