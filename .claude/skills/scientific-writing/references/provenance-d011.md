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

## Number freshness: the cite must resolve *and* still match

`check_evd_resolution.py` confirms a cite resolves to a record and that no result-like number is bare. It
does **not** confirm the number in the prose still matches the *current* value in that record. A stale
number that once was right keeps its cite and passes the check — this is exactly how R06 carried a
`CC_norm > 0.05` threshold after the as-run value had changed to split-half reliability `> 0.5` (caught
late, in the R06 precision sweep, S17).

There is no honest *deterministic* freshness check: a record is prose holding many numbers, so matching a
cited value to the current one is a comprehension task, not a regex — a script would give false confidence
(a green check on a stale number). Instead, at a full-loop handoff for manuscript-bound work, spawn a cheap
subagent (sonnet; haiku only when the numbers are cleanly keyed) whose sole task is to verify each
load-bearing/keyed number against the current value in its cited record, and to **flag — never silently
pass —** any mismatch or ambiguous case for you to adjudicate. At session close, the `number-provenance`
`wrap-auditor` already performs this freshness judgment over the changeset, so the writing-handoff
spot-check is the manuscript-bound complement, not a duplicate.
So when you state a keyed or threshold number, verify the prose value against the cited record as it reads
*now*, not as you remember it. A mechanical freshness check (compare each cited value against its record)
is a worthwhile verifier to build; until it exists, this is a manual obligation at every full-loop handoff.

## The orphan discipline

Two directions, both checked. A claim with no cite is an orphan claim (the bare-number flag). A
`\result{key}` or `\evd` with no backing record is an orphan pointer. Both are failures. The point of the
two-way check is that "every number has a tag" and "every tag resolves" are different guarantees, and D011
needs both.
