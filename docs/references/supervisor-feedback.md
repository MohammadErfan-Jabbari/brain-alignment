---
title: "Supervisor feedback on the writing (asset for the /write redesign)"
tags: [reference]
---

# Supervisor feedback on the writing (asset for the /write redesign)

The real-world signal that triggered the whole `/write` rework. IMDEA supervisor **Claudio**, on Erfan's first
thesis manuscript draft (the extended-manuscript v0.1), 2026-06-22. Verbatim:

> hi Erfan, while from the technical point of view I won't enter, maybe let me draw your attention on one point
> in the writing. Please do spend some time revising llm-specific sentence constructions such as:
>
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

## UC3M supervisor feedback on the submission-format thesis (received 2026-08-27)

Second direct human-review record, received via chat from a UC3M supervisor (professor name as Erfan confirms),
on the submission-format thesis draft. Verbatim:

> the thesis is overall very well structured with a clear sectioning structure and flow; the figures and tables
> are overall good with minor remarks later; you have several instances of paragraphs ending in one word, which
> should be avoided
>
> you use some wording that I'm not sure whether fits the expert in the domain or not; I've focused on the
> abstract, where it seems there a few terms that a reader may have difficulty to grasp at that point:
> "controlled brain predictivity," "route-specific teacher-student headroom," "target uptake," "retained-student
> movement," "brain-response-content attribution," "50-component linear target-projection measurability assay,"
> "internal continuation criterion," "non-identifying comparator." - Even if this is clear for an expert
> reading, simplifying some passages should help
>
> The title promises something that the thesis explicitly does not deliver: "From Measurement to Application"
> sounds you really turn measurement data into something ready application-level, which is not really the case,
> at least from what Section 7 delivers as main message
>
> Figure 10b and Table 22 contradict one another. The figure annotates 24 passed, 30 failed, 1 unresolved (55 in
> total), while Table 22 (p.63) records 37 checks as 20 passed, 16 failed, 1 unresolved and notes that 30/55 is
> a superseded count. Section 4.5 says 16/37.
>
> Figures and tables: the titles of tables are usually made visible either with italic/bold/small caps/underline
> or a combination thereof. This is just good typography suggestions, feel free to keep them as they are
>
> Figure 1: the arrow over the blocks and the overlapped blocks look ugly; not very clear why not all blocks are
> either all connected or all disconnected (in contrast, figure 2 is very clear)
>
> Figure 2: the font in the bottom block looks small
>
> Figure 10b has text overflowing the margin
>
> Some of your results like that in Figure 6 are very clear and neat: well done

**Mined lessons carried into the 2026-08-27 section-by-section writing review:**

1. **No undefined coinage before its definition.** The eight flagged abstract terms are compound coinages a
   first-time reader cannot parse. Every abstract/intro sentence must parse without forward references; gloss
   each coined term in plain language at first use and keep early sections free of undefined coinages.
2. **Promises must match delivery.** "From Measurement to Application" promises application-level delivery that
   Section 7 does not deliver. Calibrate title/abstract/intro/conclusion claims to the thesis's actual endpoint.
   Strengthens the title-change case in `submission/deferred-review-items.md` (admin permission still needed).
3. **Repeated numbers render from one source.** Figure annotations, tables, and prose counts must share the same
   `numbers.tex` key; a superseded count must not survive anywhere. (Figure 10b verified macro-driven on
   2026-08-27: `\result{e026_plot_check_*}`; Table 22 and Section 4.5 agree at 37 = 20 + 16 + 1.)
4. **Layout polish is part of the review.** No one-word paragraph last lines; distinct table-title typography
   (bold/small caps); legible fonts inside figure blocks; nothing overflowing the margin. Judge on the rendered
   PDF, not the source.
5. **Figure 6 is the praised standard.** One message, clean arrows, legible fonts, self-explanatory caption;
   judge other figures against it.
6. **Structure is approved.** Sectioning, flow, and overall figure/table quality are praised; the review is
   prose- and polish-level. Do not restructure sections.

## Related

- [`status.md`](../status.md) — the canonical status board
