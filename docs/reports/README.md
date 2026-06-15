# Reports — living topic syntheses

A **report** is a single-topic synthesis that we keep current. It is *not* a per-paper note
(`docs/literature/canonical/`), *not* the frontier map (`docs/01-research-landscape.md`), and *not*
thesis prose (`docs/manuscript/`). When new information lands on a topic, we **rewrite/update the
report in place** and bump its `Last updated` line.

Reports are the **continuous** write-layer (D035): the syntheses we iterate as work happens, and the
source the extended manuscript is consolidated from at checkpoints. The `scientific-writing` skill governs
how they are written (voice, the `[E0nn]` cite rule, the verifiers).

Rules:

- One topic per file. Name `R<NN>_<slug>.md`.
- State sources and **flag gaps** explicitly — a report is honest about where it is thin.
- Analysis-session discipline applies: **only numbers a working session actually produced/recorded.**
  Literature numbers are cited to their canonical note; we do not invent or estimate.

## Index

- `R01_llm-brain-mapping.md` — the linear map between LLM internals and brain activation: what it is,
  what drives it, how it behaves under scale/compression, and how to measure it without fooling
  yourself.
- `R02_datasets-and-code.md` — datasets & code provenance across the reading list: which fMRI/ECoG
  sets are open and where to pull them, and which encoding/distillation repos we can reuse.
- `R03_brain-as-training-signal.md` — the early direction doc: first-principles case that the brain is
  a weak prior, the literature scoop, the surviving slice (F1), and the kill-gated ladder. Stops at E003.
- `R04_gap-analysis.md` — full-PDF re-read of the literature: what is genuinely scooped vs open, and
  the corrected per-paper claims that re-weight the framing toward F1.
- `R05_thesis-narrative-from-first-principles.md` — **LIVING.** The pedagogical, course-grounded
  narrative of the whole experimental arc, told step-by-step for understanding (distinct from the
  terse manuscript). Built incrementally across sessions; current frontier = end of Layer 1.
