---
title: "Reasoning toolkit — frames and lenses for how we think"
tags: [reference]
---

# Reasoning toolkit — frames and lenses for how we think

Not hero worship, a small catalog of thinking tools Erfan asks for. Use them when designing methods,
deciding what to build, framing a question, or explaining why a change is worth it. The Elon/Feynman/Naval
frame (below) is the original entry; the toolkit grows as new ways of approaching problems prove themselves
(see "Keeping this frame alive"). The E/F/N part is a domain-neutral rewrite of the Nexus
`elon-feynman-naval` reference, which was resume-specific.

## Elon — first-principles reduction, constraint deletion

When drifting under inherited convention, ask:
- What is the real goal? (For us: produce one truthful, falsifiable result — not a tidy pipeline.)
- Which constraints are physically real, and which are leftovers from how it's usually done?
- What is the smallest intervention that gets the result?
- What should be **removed** instead of optimized?

Applied here: don't add a baseline, a loss term, or an artifact type because papers usually have it.
Add it only if a named bottleneck or confound requires it.

## Feynman — plain mechanism, honest limits

When deciding or explaining, ask:
- Can this be explained in plain language?
- Can we trace the mechanism step by step?
- **Where does the claim break?**
- What do we know, what do we infer, and what is still a guess?

Applied here: every claim is labeled by evidence status. State where a result would fail to
reproduce *before* running it. A number without a mechanism and a breaking point is not yet knowledge.

## Naval — leverage, compounding, elegant simplicity

When choosing between a local fix and a durable system, ask:
- What choice compounds across the rest of the thesis?
- What reduces repeated work later?
- What keeps the system simple enough to stay honest?
- Where is complexity pretending to be sophistication?

Applied here: prefer one reusable evaluation harness over bespoke per-experiment scripts; prefer the
`docs/` brain over reconstructing context in chat; delete machinery that isn't earning its keep.

## Estimand-first — separate the quantity, the measure, and the assumption

When a question rests on a measurement (a metric, a score, a correlation), do not let the measure stand in
for the thing you care about. Ask, in order:
- **Estimand:** what population quantity do I actually want? Name it before any procedure.
- **Estimator:** what concrete computation estimates it?
- **Identifying assumption:** under what condition does the estimator recover the estimand, i.e. when does
  the number mean what I want it to mean? (The resulting value is the *estimate*.)

Three companion lenses sharpen the same instinct:
- **Real or common-cause?** A dependence between $X$ and $Y$ can be genuine, or an artifact of a shared
  parent $Z$. Condition on $Z$ and ask whether it survives (conditional mutual information; Reichenbach's
  common-cause principle; its conditional-independence form, d-separation; "controlling for a confounder").
- **Marr's three levels.** Separate what is being computed and why (the computational level) from how it is
  computed (the algorithmic level); most confusion is a level-mix.
- **Characterization.** When a practical metric *equals* a principled quantity, prove the equality and lead
  with it ("unique R² is exactly the partial $\rho^2$, a conditional mutual information"), not an analogy.

Applied here: A2 is exactly this shape, with estimand $I(\text{LM};B\mid\text{nuisance})$, estimator unique
R² from ridge, identifying assumption linearity; and the averaging confound and the stimulus-predictability
ceiling are both "is the dependence real or common-cause, under a stronger $Z$?". Plain-language anchors:
operationalization, construct validity, concrete-to-abstract grounding. The full *writing* form lives in
the `scientific-writing` skill (writing-style §2, "presenting a measured quantity"); this entry is the
*thinking* form.

## Combined operating rule

1. Reduce to the real goal; delete false constraints.
2. Inspect what already exists before inventing new work (the docs, brain-jepa, cached models).
3. Explain the gap mechanically and plainly.
4. Prefer the smallest durable change.
5. Use the deeper evidence bank only when the current state truly lacks the needed proof.
6. When the question rests on a measurement, name the estimand, the estimator, and the assumption that ties
   them; ask whether a dependence is real or common-cause.

This frame is a guardrail against drift into duplicated work, fake sophistication, sprawl, and vague
justifications.

## Keeping this frame alive (how to record and add a new way of thinking)

This file is a living, small catalog of thinking tools, not a fixed list. When a way of framing a problem
proves its worth on real work (it cracked a confound, clarified a design, caught an over-claim), record it
here as a named lens, in the same shape as the others:
- a **name**, plus any standard or alternative names, so we reach for the literature behind it;
- **when to reach for it** (the trigger);
- **a worked instance from our own work**, not a textbook toy;
- **where its detailed form lives**, if it has one (a skill section, a methodology rule), with this file
  carrying the thinking form and pointing there.

Two guardrails so the toolkit stays sharp instead of sprawling (the D001 "adaptive semistructure" restraint):
- **Add a lens only when it has recurred or clearly generalizes** beyond the one problem. No lens for a
  one-off.
- **Split by purpose.** A tool mainly about *writing* lives in the `scientific-writing` skill and is only
  pointed to here; a tool about *approaching* a problem lives here. **Prune** a lens that stops earning its keep.


## Related
- [`ladder.md`](../ladder.md) — the canonical status board
- [`map.md`](../map.md) — code system (Q/E/A/D/L) & journey map
