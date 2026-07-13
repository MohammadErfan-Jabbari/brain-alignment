---
title: "S28 — Pedagogy `\gap` papers ingested (the /teach grounding completed)"
tags: [timeline]
---

# S28 — Pedagogy `\gap` papers ingested (the /teach grounding completed)

**Date:** 2026-06-20 · **Stances:** `/orient` (open) → `/meta` (dominant; scout pipeline run under it) ·
brief `/teach`-tutorial Q&A at the open. **NO experiment ran, NO science number produced, NO Q-rung
changed (Q0–Q5 stand exactly as S25/S27).** **Commits:** `64cbfe6` → `126301d` (5 atomic `docs(scout):`).

## Purpose

Erfan supplied the four papers the S27 pedagogy-grounding work could not download, in two batches. Process
them into canonical notes and close the `\gap`s. All are external pedagogy literature grounding the
`/teach` apparatus — none touches A1/A2/A3, a dataset, or a rung.

## What happened

1. **Orient + tutorial.** Opened with `/orient` (science state unchanged from S25; live next step still Q4
   E024 re-substrate). Answered Erfan's questions on the new stances model and how `/teach` works
   (orient brackets the session open; teach is a stance inside it).
2. **Identified the four supplied PDFs** — two batches. Two identity corrections caught at ingest:
   - `The_correction_of_errors…pdf` = **Butterfield & Metcalfe _2006_** (Metacognition & Learning, the
     attention/tone-detection mechanism follow-up), **not** the 2001 article. → its own new note.
   - Both OLM PDFs = **Bodily et al. _2018_** (LAK'18 OLM/LAD review, preprint + published), **not**
     [Long & Aleven 2017](../literature/canonical/long-aleven-2017_olm-self-regulated-learning.md). → its own new note.
   - `Mind_Your_Errors.pdf` = **[Moser 2011](../literature/canonical/moser-2011_growth-mindset-error-processing.md)** ✓; later `Butterfield20Metcalfe202001.pdf` = **B&M 2001** ✓;
     `s11257-016-9186-6.pdf` = **Long & Aleven 2017** ✓.
3. **Processed (5 commits).** All six PDFs moved to `data/papers/` (gitignored). Two `paper-digest`
   agents (opus) wrote the two new mechanism/RCT notes; the rest done inline by reading the extracted
   text. Notes touched: `moser-2011_*` (filled), `butterfield-metcalfe-2006_*` (new),
   `bodily-2018_*` (new), `butterfield-metcalfe-2001_*` (filled), `long-aleven-2017_*` (new),
   [`open-learner-models_2025-review.md`](../literature/canonical/open-learner-models_2025-review.md) (Long & Aleven correction), [`open-learner-models-and-errorful-learning.md`](../literature/canonical/open-learner-models-and-errorful-learning.md)
   (stale-`\gap`-language fix, at wrap).
4. **Two factual corrections to the repo's carried-over numbers:**
   - **Long & Aleven N = 301, not 302** — the abstract says 302; participants/overview/conclusion all
     report 56 + 245 = 301. The prior synthesis carried the abstract's off-by-one.
   - **The "OLM-only-with-control" finding is the larger Exp 2's OLM×PS interaction** (F(1,236)=7.535,
     p=.007), not an unconditional main effect; the smaller Exp 1 (N=56) found a plain OLM main effect
     (d=.56). Softened across both OLM notes.
   - B&M 2001's own numbers (gamma **+.36**, N=19, 7-point scale) differ from the **.06/.39/.89** gradient
     printed in the 2006 paper — that gradient is from a 2001 *poster* (2001b), not the article.
     Confirms keeping the two notes separate was right.

## Verdicts / numbers

External-literature numbers now recorded first-hand (cite-or-flag, NOT thesis results): Moser 2011
(N=25; ERN-no-mindset Fs<1.24 / Pe-yes F(1,23)=8.64, p<.01, r=.52; mediation indirect-effect 95% CI
[.01,.04]); B&M 2001 (gamma +.36, t(18)=3.07; mediation null .64 vs .63); B&M 2006 (hypercorrection γ
+.13/+.16; tone-attention γ −.22/−.21); [Bodily 2018](../literature/canonical/bodily-2018_olm-lad-systematic-review.md) (102 articles/107 OLMs; 57.9% single-data-type);
Long & Aleven 2017 (N=301; OLM×PS interaction F(1,236)=7.535, p=.007). All trace to the supplied PDFs.

## Current truth

Science **UNCHANGED**: Q0 ✅, Q1 ✅partial, Q2 ❌, Q3 ❌, Q4 ❌bounded, Q5 ⬜ — exactly as S25/S27.
This session completed the `/teach` apparatus's literature grounding only. **No `\gap` remains** in the
pedagogy set (the one genuinely-unavailable number — Long & Aleven's exact per-condition Ns — is not
printed in the paper and is correctly left `\gap`, not invented). The live science next-step is still
**Q4 sample-efficiency / E024 re-substrate**, unchanged.

## Next session

- Science next-step unchanged: **Q4** (E024 re-substrate → synthetic-PI MDE control → build), per
  `expansion-program.md` §8. Stance: `/work` (after `/precheck`), or `/teach` to test the tutor live.
- Pedagogy literature grounding is now complete; nothing further owed on these papers.

## Friction & improvements

- **Wall-of-text answer (Erfan flagged, live).** A pre-swarm status message was a dense paragraph block.
  Standing rule reaffirmed: format scannable (whitespace, short lines, lead with the point) or just do
  the work silently — never a wall of prose. This is the global Presentation rule; the lapse was mine.
- **Subagent model — checked the logs, corrected a wrong in-session claim.** I first asserted the wrap-auditors
  "inherited opus"; the subagent logs (`…/subagents/agent-*.meta.json` + the `model` field) show both auditors ran
  **`claude-sonnet-4-6`** and the three paper-digests ran **`claude-opus-4-8`** — all correctly routed. Reason: an
  agent's `model:` frontmatter default applies when the spawn omits `model`, so it does NOT fall through to the
  session model. The genuine inherit-session-opus hazard is only agents with **no** frontmatter default (generic
  `claude`/`general-purpose`/`Explore`/`Plan`/custom). Discipline: set `model:` explicitly for default-less agents;
  the named fleet agents self-route. (Lesson here is as much "verify before confessing a fault" as the routing rule.)
- **`start.json` re-fire SHA (carried S27 gotcha, recurred).** `start_sha` held `383fd1e`, a mid-session
  commit (`source: "resume"`), not the true start. Used the fallback: parent of the session's first commit
  (`a40aa24`). The S27-documented sanity-check worked.

## Audit swarm (focused, 2 scopes)

Heavy-by-file-count but science-inert, so ran 2 of 5 scopes (number-provenance + continuity-docs, sonnet;
skipped ladder-integrity/records-completeness/git-artifacts as no-ops here). Findings (all applied, none
REQUIRES-ERFAN): Moser "497 ms" → "496 ms" (496.34 rounds to 496); OLM-2025 "F=7.54" → "7.535" (match
primary source); errorful-learning Provenance still called B&M 2001 + Moser 2011 `\gap` (now closed) →
updated. Everything else PASS — all numbers trace, cross-refs resolve, both corrections consistent across
notes, no D011 violation.


## Related
- `ladder.md` — the canonical status board
- `map.md` — code system (Q/E/A/D/L) & journey map
