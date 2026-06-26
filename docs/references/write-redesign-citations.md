---
title: "/write redesign — design → source citation map"
tags: [reference]
---

# /write redesign — design → source citation map

Every load-bearing decision in the ideal-system design (`write-redesign-design.html` v0.2), grounded in a primary
source, so the protocols we write next can cite rather than assert. Two new primary sources were pulled this
session (Pinker, Toulmin); the rest are in `scientific-writing-methodology.md` and `writing-skills-ecosystem-audit.md`.

## The four concerns

| Concern | Core principle | Primary source(s) |
|---|---|---|
| **Trust** (claims↔evidence, strength-tagged) | A claim's wording must be bounded by its evidence strength; provenance is mandatory | Our D011 number rule; claim-evidence contract + strength ladder (`bahayonghang/academic-writing-skills`); soundness×contribution (ScholarEval, Moussa et al. arXiv:2510.16234); epistemic-status tiers (`imbad0202/deep-research`) |
| **Argument** (warrants between claims) | An argument is claim ← grounds ← **warrant** (the often-implicit license linking evidence to claim); "an argument with a weak warrant is easily disproven" | **Toulmin, *The Uses of Argument* (1958)** — claim/grounds/warrant/backing/qualifier/rebuttal; **Booth, Colomb & Williams, *The Craft of Research*** (claim←reason←evidence + warrant + acknowledgment) |
| **Argument → honesty/scope** (scope ≤ evidence; anti-over-claim) | Opening-width must equal Resolution-width — over/under-claim is a structural defect; calibrate claims | **Schimel, *Writing Science*** (OCAR width-matching); our anti-confound discipline (Feghhi/Oota, L003); epistemic-status calibration (`imbad0202`) |
| **Structure** (reader-expectation, fractal) | Readers decode meaning from structure: old-to-new, topic/stress, context→content→conclusion at every scale | **Gopen & Swan, "The Science of Scientific Writing"** (1990); **Williams, *Style: Lessons in Clarity and Grace*** (given-new contract); **Mensh & Kording, "Ten Simple Rules for Structuring Papers"** (2017, C-C-C fractal) |
| **Voice** (scientific register) | A scientific document, not a story; no agency to abstractions, no metadiscourse/tells, no unmotivated passive | Pinker (metadiscourse/"academese"); our D046 register rules; structural AI-tell detox (`jamditis/ai-writing-detox`); Claudio's feedback (`supervisor-feedback.md`) |

## The six stages

| Stage | Decision | Source |
|---|---|---|
| 1 · Message & **Reader-model** | One message per paper; build an explicit model of what the reader already knows/doubts | **Mensh & Kording** (one message); **McEnerney** (value defined by the reader community); **Pinker, *The Sense of Style* / "Why Academics Stink at Writing" (2014)** — the **Curse of Knowledge** is "the chief contributor to opaque writing"; fix = "show a draft to a representative reader" |
| 2 · Claim & Argument Lattice | Bind claims to evidence (Trust) AND claims to claims via warrants (Argument); novelty/scope are themselves bound claims | D011; **Toulmin**; **Booth** (warrant + acknowledgment); Swales (the niche/novelty as a defended claim) |
| 3 · Architecture **+ figures** | Skeleton-first, fractal; figures are the spine, drawn before prose; reverse-then-forward | **Whitesides, "Writing a Paper"** (outline-first; writing manages the research); **Schimel** (OCAR/hourglass); **Swales** (CARS intro moves); figure-first (`evoskills`, `k-dense`) |
| 4 · Draft | Sentence-level reader-expectation to the reader-model; non-linear order (methods/results first, abstract last); mechanism before metrics | **Gopen-Swan / Williams** (topic/stress, old-to-new); non-linear order + mechanism-before-metrics (`evoskills`, `k-dense`) |
| 5 · Audit ×4 | One independent reader per concern + reviewer-premortem | claim-fidelity = D011 + Claim-Intent-Manifest (`imbad0202`); argument = Toulmin warrant check; structure = Gopen-Swan/Williams; voice = detox + register-auditor; premortem = our thinking-panel (D017) |
| 6 · Revise | Coarse-to-fine (logic→sentence→lexical), never reversed; logic-revision re-enters the gate | coarse-to-fine order (`bahayonghang`); concern-separation rationale = **Pinker** ("too cognitively demanding to assemble a coherent argument and express it clearly at the same time") |

## Cross-cutting decisions

| Decision | Source |
|---|---|
| **Separate the concerns** (don't write argument + prose at once) | **Pinker** (the cognitive-load argument for revising clarity as a separate pass); our S33 "immune system, not a notion of health" diagnosis |
| **Human gates the case + plan, not the lines** | Whitesides (outline as the high-leverage artifact); our D011 (the human owns the verdict) |
| **Gated coupled loop, not a linear pipeline** | message↔figures↔claims co-determine (`evoskills` reverse-then-forward; Whitesides "objectives when finished differ from those at the start") |
| **Trust by gate + audit, not "by construction"** | the critique this session (clean-context opus + Codex); the draft step is generative, so trust is re-checked not preserved |
| **narrative arc (allowed) ≠ storytelling register (banned)** | Schimel (arc = logical problem→resolution) vs Pinker/Claudio (register = drama/agency to abstractions) |

## New primary sources pulled this session
- **Steven Pinker**, *The Sense of Style* (2014) + "Why Academics Stink at Writing" (Chronicle, 2014) — the
  Curse of Knowledge; classic style; revise-for-clarity as a separate pass. https://stevenpinker.com/files/pinker/files/pinker_2014_why_academics_writing_stinks.pdf
- **Stephen Toulmin**, *The Uses of Argument* (1958) — the claim/grounds/warrant/backing/qualifier/rebuttal model;
  the warrant as the implicit evidence→claim license. (overview: utsa.edu TWC Toulmin model PDF)


## Related
- [`ladder.md`](../ladder.md) — the canonical status board
- [`map.md`](../map.md) — code system (Q/E/A/D/L) & journey map
