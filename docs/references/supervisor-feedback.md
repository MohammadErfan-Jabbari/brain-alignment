---
title: "Supervisor feedback on the writing (asset for the /write redesign)"
tags: [reference]
---

# Supervisor feedback on the writing (asset for the /write redesign)

The real-world signal that triggered the whole `/write` rework. IMDEA supervisor **Claudio**, on Erfan's first
thesis manuscript draft (the extended-manuscript v0.1), 2026-06-22. Verbatim:

> hi Erfan, while from the technical point of view I won't enter, maybe let me draw your attention on one point
> in the writing. Please do spend some time revising llm-specific sentence constructions such as:
> - "The inverted question only earns a thesis if it survives a hard prior:"
> - "The bare inverted idea, using fMRI to shape a language model, is by 2026 already done, and saying so plainly
>   is what locates the real contribution."
> - "This manuscript reports that ladder"
> - "Alignment is measured with an encoding model: [...]"
>
> Point 1, 2, and 3: all go in the line of telling a story, but you want your thesis to be a scientific document.
> Point 4 uses passive voice without any specific reason and you can easily turn this into active voice.

**What it diagnoses (two defect classes, in Claudio's own grouping):**
- **Points 1–3 — storytelling register in a scientific document.** The flagged sentences attribute agency/stakes
  to abstractions (a *question* "earns"/"survives"; a *manuscript* "reports"), and narrate the thesis as a story.
  Not a banned word — a semantic/register defect a lexical linter cannot catch.
- **Point 4 — unmotivated passive voice** ("Alignment is measured…") that loses the agent and is trivially
  active.

**Why it's the anchor for the redesign:** this is the ground-truth failure. A draft passed every check we had and
still read as story-prose to a real supervisor. The redesign's job is to make this class of defect impossible to
ship — not by listing Claudio's four sentences, but by building the positive model that prevents the whole class.
These observations are retained as direct human-review evidence for future manuscript revisions.
(group C — structural AI-tells), and the S33 "immune system, not a notion of health" diagnosis.


## Related
- [`status.md`](../status.md) — the canonical status board
