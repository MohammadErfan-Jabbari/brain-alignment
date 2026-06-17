# S20 — E003 record-provenance repair (working; provenance-only, no science changed)

**Date:** 2026-06-17 · **Session:** S20 · **Branch:** main · **Mode:** working

## Purpose

Repair the four provenance gaps the R07 review panel (S19) flagged in E003's record, plus a 5th
found en route — without changing any alignment number, verdict, or rung. Run as an explicit
multi-round orchestration Erfan asked for: gather → counter-critique panel → draft plan → critique
the plan → execute.

## What happened

1. **Round 1 (3 readers, sonnet):** verified all four gaps against the files; found the held-out
   slice (`data/kd_corpus/wikitext103_sentences_heldout.txt`) still cached on disk → recompute is
   byte-reproducible. Mapped every downstream reference (R07, L011, ladder, map) and the D011 lane
   rules (E003 is working-lane editable; R07 is analysis-lane, off-limits except mechanical ppl
   propagation).
2. **Round 2 (4-lens panel, opus — counter-argument/premortem/first-principles/socratic):** overturned
   the first sketch. The original acceptance criterion ("reproduce the bootstrap P-values within
   rounding") was unsatisfiable and would force tuning-to-target — the sin the repair exists to cure.
   Surfaced a **5th gap** (cold ran 2 epochs vs warm 1 → "matched budget" false on step count) and the
   **E015 collision** (E015 retired the within-family r as layer-unstable noise).
3. **Round 3 (plan critique, opus — counter-argument + premortem):** demanded one empirical test first
   — the gpt2 perplexity dry-run.
4. **The decisive dry-run:** reference ppls recompute on the cached slice to teacher **74.03**, gpt2
   **104.88**, distilgpt2 **169.03** — matching the recorded 74/105/169. So they *were* on-slice
   measurements, never written to the JSON (`record()` passed `ppl=None`). Recompute **confirms**,
   does not replace → the fit/multiplier do not move. Killed the panel's chief fear.
5. **Erfan gated three decisions** (all recommended option): P-value acceptance = qualitative claim
   (not within-rounding); dissociation r = annotate + forward-point to E015 (don't harden); scope =
   record the epoch fact in E003, flag R07 for the analysis lane.
6. **Executed:** built `scripts/recompute_e003_reference_ppl.py` → `outputs/E003_perplexity.json` and
   `scripts/reanalyze_e003_dissociation.py` → `outputs/E003_dissociation.json`. Repaired E003.md
   (Output pointer, untrained ppl → order-of-magnitude, multiplier → "≈6.4× the teacher (≈4.5× the
   gpt2 student)", dissociation citations + E015 forward-pointer, epoch-asymmetry note, a Provenance
   repair section) and L011 (multiplier + dissociation citation).

## Key numbers (re-derived, archived)

- Reference ppls: teacher 74.0, gpt2 104.9, distilgpt2 169.0 (match record); untrained ~5.8×10⁴
  (seed-variable 56k–60k, order-of-magnitude only).
- Dissociation: r=−0.8835, slope −0.00791, intercept 0.05036, residuals kd_warm +0.00007 / gpt2
  +0.00623, fold-2 = 44.0% of the gpt2−kd_warm delta — all reproduce the prose.
- Dissociation P-values **construction-sensitive**: fold×seed bootstrap P(gpt2≤kd_warm)=0.091,
  P(lmft≤kd_warm)=0.083 (reproduces the prose 0.092/0.085); fold-only gives 0.000/0.070. Within-family
  r bootstrap CI = [−1.0, +0.31] (wide — consistent with E015 retiring it as noise).

## Verification

- R07 **byte-identical** (md5 `39160c8…` unchanged) — stayed out of the analysis lane.
- No alignment verdict number changed: E003.md unique-R²/ρ′/Δ/CI/p rows not in the diff; only the
  untrained ppl cell + the multiplier label moved.
- All four `outputs/E003*` paths named in E003.md resolve.

## Decisions / learnings

- Three gate decisions (qualitative P-value criterion; annotate-not-harden the within-family r;
  record-epoch-flag-R07) — Erfan-approved via the orchestration.
- **L047** appended (provenance: measured-but-unsaved numbers; acceptance-criteria as a hazard;
  bootstrap construction-sensitivity).

## Outstanding (for the analysis lane, Erfan)

R07 still phrases the screen as "matched budget"; given cold=2/warm=1 epochs that wants a one-line
analysis-lane edit (handoff text produced this session). Not edited from this working session (D011).

## Next session

Analysis lane: R08 (Q2 — the lever is real but weak and ppl-confounded), or the extended manuscript.
Working lane has no queued decisive work (forward program complete).
