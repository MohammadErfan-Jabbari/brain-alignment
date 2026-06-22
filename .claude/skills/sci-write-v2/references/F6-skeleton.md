# F6 — Skeleton (stage 3, Structure). The orchestrator's stage-3 procedure.

Turn the bound claim-lattice + reader-model into a fractal section structure and a claim→section map,
**before any prose**. Structure-first is the single biggest process lever (Whitesides): the skeleton is
what the human gates, not the lines.

**Owns:** producing `sections[]` and assigning every `claim.section`. **Does not own:** judging whether the
structure is *good* — opening-width, CARS-niche, point-sentences are the **F11 structure judge** (a Phase-2
subagent run at the stage-3 site and again at stage 5). F6's only rigid floor is the `lattice_integrity`
coverage rules (orphan-claim, empty-section, bidirectional node↔section), which fire on the lattice write.

## Inputs (read from the lattice, stage ≥ 2)
- `message` — the one-sentence paper message (halt with a gap if null).
- `claims[]` — bound claims from F3 (`claim_id`, `text`, `is_central`, `strength`, `scope`, `acknowledgments`).
- `reader_model` — what the audience knows vs doubts (F1; Phase 2 — may be null in the walking skeleton).
- `warrants[]` — argument edges (F4; Phase 2 — may be empty).

## Procedure
1. **Assert the message.** If `lattice.message` is null, surface a gap and stop — there is nothing to structure around.
2. **Macro structure = OCAR at the whole-paper scale.** Lay the top-level sections as an hourglass:
   Opening + Challenge (Introduction), Action (Methods/Results), Resolution (Discussion) — IMRaD by default.
   **Opening-width = Resolution-width:** every contribution promised in the opening must get a resolution
   section. (F11 *judges* this; F6 *builds toward* it.)
3. **Introduction = CARS three moves.** Give the intro paragraph-roles for Move 1 (territory) → Move 2
   (the niche/gap — must be explicit; this is our "empty cell") → Move 3 (this work). Never skip Move 2.
4. **CCC fractally at the section scale.** Each section opens on context, delivers content, closes on a
   conclusion that links forward. (Paragraph-scale CCC is F11 at stage 5, not here.)
5. **Organize by importance, not chronology** (Whitesides). The most important finding leads; cut the
   history-of-struggles. Every section must carry ≥1 bound claim (else `empty-section` fires). *Ordering
   quality is the F11 judge's call (Phase 2); F6's floor only guarantees coverage, not good order.*
6. **Build the claim→section map, both directions.** For each claim set `claim.section = <section_id>`;
   populate each `sections[].claim_ids[]`. The two must agree (the `node→section` rule checks both ways).
   No claim may stay `section: null` (else `orphan-claim` fires).
7. **Leave room for figures (F7, Phase 2).** Place `is_central` claims in figure-bearing sections
   (Results/Key Findings). Do **not** invent `figures[]` here — that is F7. The `central-figure` rule is
   dormant at stage 3 (skeleton) and becomes mandatory at stage ≥ 4 (drafting): by the time prose is
   written, every central claim must carry a figure. (Gating on stage, not a self-reported flag, means the
   rule cannot die silently if F7 is skipped.)
8. **Advance `meta.stage = 3`** and write the lattice. `lattice_integrity validate` then enforces coverage.
9. **Fluidity, never silent.** CCC/OCAR/CARS are defaults, not laws. If none fits this paper's shape
   (e.g. a pure methodological-negative), stop, diagnose *why*, then adapt/combine/invent — or flag the
   human if the choice is load-bearing — and **log it** in `deviation_log`
   (`{functionality: "F6", method, why, did}`). A silent force-fit is the one thing forbidden (SC-PROC-8/9/10).

## What the methods mean (operational core)
- **OCAR** (Schimel): Opening→Challenge→Action→Resolution; the hourglass; width-match.
- **CARS** (Swales): territory → niche → occupy; the intro's three moves.
- **CCC** (Mensh-Kording): Context→Content→Conclusion at *every* scale; one paper, one message.

## Acceptance (this stage is done when)
- Every claim has a non-null `section` naming a real section; every section has ≥1 claim; the map agrees
  both directions → `lattice_integrity validate` is clean at stage 3.
- A short-but-complete section is fine — **length is not a defect** (SC-STR-10).
- The opening-width and CARS-niche *quality* checks (SC-STR-06/07) are the F11 judge's call (Phase 2).
