# F17 — register & exemplar pin (the standard F8b/F12 measure against)

The exemplar set is the **positive** voice standard: real venue prose that F8b (voice-realize) writes toward and
F12 (voice audit) measures against. Voice is judged against *this*, not against an abstract rulebook alone.

**The pin (the gate).** Before the voice pass runs, the lattice must carry a `register` object —
`{venue, exemplars: [<section:paper>, ...]}` — chosen for the paper's venue. `lattice_integrity` blocks at
**stage ≥ 4** if `register.exemplars` is empty (SC-VOICE-10: no exemplar pinned → no voice pass). The register is
set at stage 1 (a voice-concern stage-1 output, like the reader-model and frame).

**The anchors, by section** (real prose in `data/papers/`, graded against OUR constraints — see the caution
below). Each is the *target register* for that section; pin the ones matching the venue:

| Section | Anchor (paper) | What it exemplifies |
|---|---|---|
| **Abstract** (clean, mechanism-first) | `2602.14486` — "We show that the existing metrics… are confounded by network scale…" | active, mechanism-first, scoped |
| **Intro / CARS gap** | `bilgin-2026` — "brain activity serves only as a dependent variable… leaving open whether…"; `2209.02582` — "previous work leaves it unclear whether…"; `2510.21520` — "Existing methods are data inefficient, requiring…" | territory→gap, no throat-clearing |
| **Results / mechanism-before-metric** | `tribev2` — "…reflects the architectural advantage… rather than differences in input features…"; `2511.16849` — "…is a byproduct of the model learning to reconstruct…"; `2506.03832` — "appears to reduce alignment…, suggesting…" | mechanism named before the number |
| **Numbers + named test** | `tribev2` — "q(FDR) < 1e-4, t-test across subjects… two- to four-fold improvement"; `2511.16849` — "r = 0.71 and r = 0.70… even when excluding…" | test named, range not point estimate |
| **Limitations** | `tribev2` — "constrained by the inherent spatio-temporal resolution of fMRI…"; `bilgin-2026` — "fMRI has slow hemodynamics…"; `2602.14486` — "valid under Assumption 3.1… validity is recovered by…" | limitation + its mechanism named |

The fully-graded corpus (each anchor tagged with the constraint it satisfies, plus the published-but-NONcompliant
contrasts) is the **`SC-EX-*` / `SC-VIO-*` set in `docs/references/write-redesign-scenarios.md`** — this table is
the lifted, per-section index into it; do not re-mine.

**The caution (encode it).** **"From a good paper" ≠ "passes our rules."** Top venues tolerate mild
storytelling / over-claim that this thesis would not. Each anchor here was graded against *our* constraints
(scope ≤ evidence, no agency-to-abstraction, no unmotivated passive). The danger zone is the **opening/closing
framing paragraphs** (Abstract / Discussion / Conclusion), where violations cluster — F8b/F12 weight them. The
`SC-VIO-*` rows are real published prose that **fails** our rules, kept as contrast, never as a target.
