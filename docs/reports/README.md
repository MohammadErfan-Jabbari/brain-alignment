---
title: "Reports — living topic syntheses"
tags: [report]
---

# Reports — living topic syntheses

A **report** is a single-topic synthesis that we keep current. It is *not* a per-paper note
(`docs/literature/canonical/`), *not* the frontier map (`docs/01-research-landscape.md`), and *not*
thesis prose (`docs/manuscript/`). When new information lands on a topic, we **rewrite/update the
report in place** and bump its `Last updated` line.

Reports are the **continuous** write-layer (D035): the syntheses we iterate as work happens, and the
source the extended manuscript is consolidated from at checkpoints. The `sci-write-v2` pipeline governs
how they are written (voice, the `[E0nn]` cite rule, the verifiers).

Rules:

- **Flat, append-only IDs.** A report is `R<NN>_<slug>.md`; numbers are assigned in creation order and
  never renumbered (the same "issue-number" rule the `E`/`D`/`L` artifacts use, D036). **One finding (one
  durable claim) per file**, tagged with the ladder question `Q0`–`Q5` it answers.
- **Reading order and the Q→report map live in the index below, not in the filename** (the flat-IDs-plus-
  separate-view pattern D036 uses for the ladder). A finding may carry more than one `Q` tag; one `Q` may
  own several reports (Q3 is fanned across many, because that is where the paper lives).
- **Current truth only** (D036): rewrite in place, no chronological spoilers, no "obsolete/frontier"
  scaffolding. The history (wrong turns, the order they happened) lives in [`map.md`](../map.md), `timeline/`, and
  `decisions/`. There is no chronological-narrative exception: [`R05`](R05_thesis-narrative-from-first-principles.md), the old teaching companion, is
  retired (frozen for history; see the index).
- State sources and **flag gaps**; **only numbers a working session actually recorded** (D011). Literature
  numbers cite their canonical note. Route all report writing through the `sci-write-v2` pipeline (voice,
  the `[E0nn]` cite rule, the verifiers).
- **Math-grounded, in LaTeX.** Formalize the report's core quantity and any foundational concept in real LaTeX
  (`$…$` / `$$…$$`, which Markdown renders); cite the course note (`docs/06-theory-grounding.md`) for any
  definition or bound rather than re-deriving. Prose explains; the formula pins it down.

## Index

**Background / framing** (topic syntheses, not findings):

- [`R01_llm-brain-mapping.md`](R01_llm-brain-mapping.md) — the linear map between LLM internals and brain activation: what it is,
  what drives it, how it behaves under scale/compression, and how to measure it without fooling yourself.
- [`R02_datasets-and-code.md`](R02_datasets-and-code.md) — datasets & code provenance across the reading list.
- [`R03_brain-as-training-signal.md`](R03_brain-as-training-signal.md) — the early direction doc: the first-principles case, the literature
  scoop, the surviving slice, and the kill-gated ladder. Stops at E003.
- [`R04_gap-analysis.md`](R04_gap-analysis.md) — full-PDF re-read of the literature: what is genuinely scooped vs open.
- [`R05_thesis-narrative-from-first-principles.md`](R05_thesis-narrative-from-first-principles.md) — **RETIRED (2026-06-16).** The old pedagogical
  narrative of the arc, frozen for history and no longer maintained. Superseded by the finding-reports
  (R06+) and `map.md`.

**Findings** (read in this order; each maps 1:1 to a manuscript Results section):

| Read # | Report | Q | Claim | Status |
|---|---|---|---|---|
| 1 | [`R06_alignment-signal-is-real-beyond-confounds.md`](R06_alignment-signal-is-real-beyond-confounds.md) | Q0 / A2 | the alignment signal is real beyond confounds (defines the measurement apparatus) | ✅ written |
| 2 | [`R07_plain-kd-does-not-preserve-alignment.md`](R07_plain-kd-does-not-preserve-alignment.md) | Q1 | plain KD does not preserve alignment by default | ✅ written |
| 3 | R08 (to write) | Q2 | the lever is real but weak and perplexity-confounded | ⬜ |
| 4 | R09 (to write) | Q3 | no per-individual gain; the averaging confound | parked draft `_pending-Q3_*.md` |
| 5 | R10 (to write) | Q3 | the null is method-general (every door closed) | ⬜ |
| 6 | R11 (to write) | Q3 | the quality law — matched-perplexity is the missing control | ⬜ |
| 7 | R12 (to write) | Q3 | the stimulus-predictability ceiling, scoped honestly (keystone) | ⬜ |
| 8 | R13 (to write) | Q3 | an external reproduction corroborates the failure | ⬜ |
| 9 | R14 (to write) | Q4 / A3 | no practical payoff | ⬜ |

We are writing in reading order, so the filename number tracks it for now (R06 = read-position 1). The
parked [`_pending-Q3_no-per-individual-gain-and-averaging-confound.md`](_pending-Q3_no-per-individual-gain-and-averaging-confound.md) is the existing finished Q3 draft;
it reclaims a number (R09) when we reach read-position 4. The flat-ID rule still protects any *future*
out-of-order finding: it takes the next free number and the index shows where it reads.


## Related
- [`ladder.md`](../ladder.md) — the canonical status board
- [`map.md`](../map.md) — code system (Q/E/A/D/L) & journey map
