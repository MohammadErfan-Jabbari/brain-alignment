# Provenance and D011: every number defensible

D011 is the hard line of this repo: a number appears in writing only if a working session recorded it.
This reference is the doctrine behind the `check_evd_resolution.py` verifier. Read it the first time you
tag a number or hit one you cannot source.

## The results-prose standard (what an empirical sentence must carry)

Empirical prose reports the effect with its uncertainty and the named test, on contiguous splits, with
the nuisance or confound subtraction shown, over the recorded seeds. These are fixed repo standards, not
per-section choices. Treat them as a checklist the section must satisfy, not a ritual to perform before
you look at the data (you usually already know the numbers, since writing is downstream of the run). A
sentence that states an effect without its uncertainty and test is incomplete, not just terse.

Good: "the trained minus untrained unique-R² gap was +0.021 [95% CI +0.0205, +0.0209], 95% of reliable
voxels positive, contiguous story split (E006)."

Not enough: "the trained model was better."

## Tagging: `\evd` and `[E0nn]`

Every empirical claim carries its source. In LaTeX use `\evd{E006}` or `\evd{L016}`; in a Markdown report
use an inline `[E006]`. The key resolves to a record: `Ennn` to a file under `docs/experiments/`, `Lnnn`
to an entry in `docs/learnings.md`. The verifier fails on a key that does not resolve, and it fails on a
result-like number that has no cite on its line. A missing tag is the real D011 failure, because a
cite-only check would read it as clean.

Do not cite a planned or killed experiment as if it produced the number. A record has to actually contain
the result you are citing.

## Gaps: `\gap`, never a guess

When the prose needs a number that no working session recorded, write `\gap{what is missing}`, not a
plausible value. A gap is an honest open slot and a candidate working-session task. It is allowed (often
expected) in a report or the extended manuscript. It must never survive into a public cut, which is why
`check_gap_survival.py` blocks a public cut that still contains one. This is the "[MATERIAL GAP], never
interpolate" discipline: when the evidence does not cover what the outline wants, flag it rather than
filling from memory.

## Keyed numbers: which numbers go in the registry

The load-bearing numbers (the headline effects, the CIs, the figures a committee will quote) live once in
`assets/numbers.tex` as `\result{key}` macros, and both the extended manuscript and every public cut
reference them by key. One source means a number cannot drift between layers, and the key doubles as the
provenance handle. One-off contextual numbers (a sample count in passing) can be written inline, but they
still need an `\evd` cite. Rule of thumb: if a number would be wrong to get wrong in a public cut, it is
load-bearing, so key it.

## The orphan discipline

Two directions, both checked. A claim with no cite is an orphan claim (the bare-number flag). A
`\result{key}` or `\evd` with no backing record is an orphan pointer. Both are failures. The point of the
two-way check is that "every number has a tag" and "every tag resolves" are different guarantees, and D011
needs both.
