---
title: "Errors Committed with High Confidence Are Hypercorrected"
tags: [literature]
aliases: [butterfield-metcalfe-2001_hypercorrection-effect]
---

# Errors Committed with High Confidence Are Hypercorrected

**Authors / Year / Venue:** Brady Butterfield, Janet Metcalfe / 2001 / *Journal of Experimental Psychology: Learning, Memory, and Cognition* 27(6):1491–1494 · **Link:** https://doi.org/10.1037/0278-7393.27.6.1491
**Canonical ID:** butterfield-metcalfe-2001_hypercorrection-effect

**Tags:** #literature #canonical #metacognition #teach-stance #teach-skill-grounding #not-brain-science

> **Provenance (read first):** the full PDF of *this* (JEP:LMC) article is **now read first-hand** (2026-06-20, publisher PDF Erfan supplied → `data/papers/butterfield-metcalfe-2001_hypercorrection-effect.pdf`). The earlier version of this note was secondary-record-only because every full-text route was blocked; the per-experiment `\gap` numbers below are now **filled from the article's own Method, Results, and Table 1**. The mechanism follow-up is the sibling note [`butterfield-metcalfe-2006_hypercorrection-attention`](butterfield-metcalfe-2006_hypercorrection-attention.md) — and note the **.06/.39/.89** gradient that 2006 paper prints comes from a 2001 *poster* (2001b), **not** this article: this article's own per-bin proportions (Table 1, below) are different and noisier.

---

## TL;DR

This is the paper that named and demonstrated the **hypercorrection effect**: when a person answers a general-knowledge question wrong but had been **highly confident** the wrong answer was right, that error is **corrected more reliably** on a later test (after corrective feedback) than an error made with **low** confidence. The direction is counterintuitive — a strict interference account predicts the opposite (a strongly-held wrong answer should compete *more* with the correction) — and the authors read the reversal as evidence that the **surprise of being confidently wrong** recruits attention to the corrective feedback at the moment it arrives. In this repo it is **apparatus grounding for the `/teach` stance**, the empirical warrant for the SCR predict-before-reveal loop; it is **not** thesis science (no A1/A2/A3, no brain-alignment number).

## Key ideas

**The effect.** Hypercorrection = a **positive** relationship between the confidence with which an error was originally committed and the probability that the same item is answered correctly after feedback. High-confidence errors are the *most* likely to be fixed; low-confidence errors (near-guesses) are the *least* likely to be fixed. The name and the demonstration are this 2001 paper's; the larger mechanistic program (the surprise / attention-to-feedback account, error-related encoding) is built out in the authors' follow-ups (Butterfield & Metcalfe 2006; Metcalfe & Finn; Metcalfe 2017 *Annual Review of Psychology* review).

**Why it is counterintuitive — the interference prediction it overturns.** A naive associative-interference view says: the more strongly you hold the wrong answer (high confidence ⇒ strong memory trace for the error), the harder it should be to overwrite with the correct answer, because the old trace competes at retrieval. That predicts high-confidence errors should be *stickier* and *harder* to correct. The data go the other way. So confidence-in-the-error is not acting as trace strength that blocks the correction; something about the high-confidence-error event *helps* the correction stick.

**The proposed mechanism — surprise drives attention to the feedback.** Being confidently wrong is a large prediction-error event: you expected to be right and you were not. That surprise increases attention to (and deeper encoding of) the corrective feedback at the moment it is delivered, so the correct answer is encoded better precisely when the prior belief was strongest and most violated. This is the through-line the authors develop in later work into an attention/encoding-at-feedback account (and connects, in the broader literature, to error-monitoring signals — see the repo's synthesis note linking the Pe / error-positivity ERP work, [Moser et al. 2011](moser-2011_growth-mindset-error-processing.md)).

**The boundary the effect lives inside.** Hypercorrection is established for **errors the learner actually held a belief about** (high vs low confidence in a *wrong* answer that then gets *corrected*). It is a within-error gradient, not a claim that confidence is good in general; the favourable case is a knowledgeable adult who can be confidently wrong, get told, and re-encode. (For the prior-knowledge precondition see [`bjork-2011_desirable-difficulties.md`](bjork-2011_desirable-difficulties.md); for the "diagnostic not scorecard" framing of surfacing one's own errors see [`open-learner-models-and-errorful-learning.md`](open-learner-models-and-errorful-learning.md).)

## Evidence

**Design (now read first-hand from the article).** **19 Columbia undergraduates** (10 women, 9 men, mean age 19.1) answered **150 general-information questions** (Nelson & Narens 1980 norms), rating confidence on each on a **7-point scale from −3 (sure wrong) through 0 (unsure) to +3 (sure correct)**. Wrong answers got 2 s of correct-answer feedback ("Actually, the answer is X"); the procedure ran until each participant had given ≥15 correct and ≥15 incorrect answers. After a 5-min interpolated logic problem, a surprise **retest** asked for the **first three responses** that came to mind, each rated for confidence, with the final answer **starred** (scored correct only if the correct answer was starred — the three-response design doubles as a measure of whether the *original error* still reappears). The load-bearing analysis is the **within-subject gamma** between original confidence-in-an-error and the probability of correcting it at retest.

**The numbers (now read first-hand from Results + Table 1).**
- **Sample / basics:** N = 19. Initial accuracy **.45**, retest accuracy **.82**. P(correct at retest | correct at first) = **.99**; P(correct at retest | *wrong* at first) = **.64** — about two-thirds of errors were corrected after one feedback exposure.
- **The hypercorrection effect (headline):** the within-subject **gamma between confidence-in-the-error and correcting it at retest = +.36** (SEM .116), **t(18) = 3.07, p < .05** — significantly *positive*, the reverse of the interference prediction the authors set out to confirm.
- **Errors are genuinely strong, not just absent:** gamma between initial confidence and the original error *reappearing* among the three retest responses = **+.39** (SEM .124), t(18) = 3.15 — high-confidence errors are *more* available in memory, yet still corrected more often.
- **Mediation ruled out:** the correct answer was no more likely to appear when the original error also appeared (.64) than when it did not (.63), **t < 1** — so the correction is not the error cueing the answer.
- **Per-confidence-bin correction (Table 1, P(C2|W1) by rating −3…+3):** .60, .79, .65, .84, .67, .60, **1.00** — noisy across bins because **high-confidence *errors* are rare** (the +3 cell rests on very few trials/participants, which the paper explicitly flags); the effect is carried by the within-subject gamma, not a clean monotone marginal.

**Citation, fully verified (CrossRef + OpenAlex agree exactly):** *JEP: LMC* vol. 27, issue 6, pp. 1491–1494, 2001; authors Brady Butterfield and Janet Metcalfe; DOI 10.1037/0278-7393.27.6.1491; 144 citations per OpenAlex; open-access status **closed** (Unpaywall and OpenAlex both report no OA full-text location).

## Limitations

- **Single, short report (≈4 pp.) with a specific paradigm.** The effect is shown for general-knowledge facts with explicit confidence ratings and a feedback-then-retest loop; generalisation to other materials, ages, and richer learning is the job of the later literature, not this paper.
- **Confidence and accuracy are correlated, so the "confidently wrong" cell is the interesting-but-thinner one.** People are usually right when confident; truly high-confidence *errors* are comparatively rare, which is exactly the cell the effect rests on — a measurement caveat the mechanistic follow-ups had to manage.
- **The surprise/attention mechanism is an inference in this paper, sharpened later.** The 2001 report establishes the *direction*; the attention-to-feedback / error-encoding account is developed and tested more directly in the authors' subsequent work. Cite the mechanism as their *proposed* explanation, not as measured here.
- **Small N (19), single short session, no manipulation of confidence.** The effect is a within-subject gamma over naturally-occurring confidence levels; confidence is observed, not assigned, so it stays confounded with whatever produces it (familiarity, fluency, domain knowledge — the very covariates the 2006 follow-up then probes).

## Relevance to the /teach stance

This is **apparatus grounding for the agent's own `/teach` stance — NOT thesis science.** It touches none of A1/A2/A3, produces no brain-alignment number, uses none of our datasets, and must **not** appear in [`docs/01-research-landscape.md`](../../01-research-landscape.md)'s brain/distillation tables. Its single job is to let `teach.md` *cite* a mechanism instead of asserting it from parametric memory (the cite-or-flag spine).

**Specifically, it is the evidence behind two `teach.md` design choices:**

1. **The SCR "predict before reveal" loop** (teach.md §"SCR"). The loop asks for the learner's prediction *with its reason* before showing a number or confirming a step, then reveals, then reconciles ("you expected X, the record says Y — how do you square that?"). Hypercorrection is *why this is well-founded, not just nice*: a prediction stated with conviction and then shown wrong is exactly the confident-error event whose correction sticks best. Eliciting the confident commitment first is what manufactures the surprise that makes the correction land. Without the prediction step, a quietly-held or never-surfaced wrong belief gets none of that benefit.

2. **Surfacing high-confidence mistakes on purpose, and keeping mistakes diagnostic.** The stance deliberately draws out where the learner is confidently wrong (rather than smoothing past it) and stores mistakes in the lesson layer as forward-looking "what to re-check," superseded on correction — never as a tally. Hypercorrection grounds the *first* half (confident errors are the high-value correction targets); the "diagnostic not scorecard" framing of the *second* half is grounded in `open-learner-models-and-errorful-learning.md` and the error-framing literature (Moser et al. 2011; Tulis et al. 2024), not here. Keep that split when citing.

**Cite-or-flag guardrails (what this note does NOT support):**
- The gamma (**+.36**), N (**19**), the 7-point −3…+3 scale, and the Table 1 proportions are now read first-hand and quotable — but as **external literature, not a thesis number**, and with the small-N caveat (N = 19; high-confidence-error cells sparse). Cite the *direction + the gamma* as the durable claim, not the noisy per-bin marginals.
- The **attention/surprise mechanism is the authors' proposed explanation** (sharpened in their later work), not a result measured in this 4-page report; phrase it as such.
- Hypercorrection is a **within-error gradient** (confident *errors* corrected better than unconfident ones). It is **not** a claim that high confidence is generally good, nor a licence to reward confidence — keep it paired with the repo's anti-sycophancy / availability-bias rule.
- This note sits alongside `open-learner-models-and-errorful-learning.md` (the broader errorful-learning synthesis, which already cites this paper at one line), [`dunlosky-2013_effective-learning-techniques.md`](dunlosky-2013_effective-learning-techniques.md) (retrieval + spacing), and `bjork-2011_desirable-difficulties.md` (the prior-knowledge precondition) as the `/teach` grounding set — it is the dedicated, mechanism-level source for the *predict-before-reveal* choice specifically.

## Provenance

**Citation: verified.** CrossRef (`api.crossref.org/works/10.1037/0278-7393.27.6.1491`) and OpenAlex (`api.openalex.org/works/doi:…`) independently return the identical record — authors Brady Butterfield & Janet Metcalfe, *JEP: LMC* 27(6):1491–1494, 2001, DOI 10.1037/0278-7393.27.6.1491. OpenAlex: 144 citations, `oa_status: closed`. Unpaywall: `is_oa: false`, no OA location.

**Full text: NOW READ first-hand (2026-06-20).** The prior version of this note was secondary-record-only — the closed-access routes were all blocked (Columbia Metcalfe-lab mirror behind Cloudflare + Imperva WAF, APA PsycNet "Loading…" shell, Ovid 402, ResearchGate 403/1020, no OA copy per Unpaywall/OpenAlex, and a WebFetch cache that was poisoned to an unrelated LA Times column). Erfan supplied the **publisher PDF**, now at `data/papers/butterfield-metcalfe-2001_hypercorrection-effect.pdf` (4-page JEP:LMC article, pp. 1491–1494). Text extracted via `pypdf` and read end to end — Method (N, scale, procedure), Results (the two gammas, basic accuracies, the mediation null), Table 1, and Discussion. Every number in the Evidence section is quoted directly from that body. The `\gap` is now **closed**.

## Verified

Citation verified against CrossRef and OpenAlex (exact agreement); the article's masthead matches (JEP:LMC 2001, 27(6):1491–1494, DOI 10.1037//0278-7393.27.6.1491). **Full PDF now read first-hand** from the publisher copy Erfan supplied (`data/papers/`); all per-experiment numbers (N = 19, the −3…+3 scale, gamma +.36 / +.39, the .45/.82/.99/.64 accuracies, the mediation null, Table 1 proportions) are read verbatim from the body. No number estimated or invented; `\gap` closed.

## Read Date

2026-06-19 (secondary-record only) → **full text read first-hand 2026-06-20** (publisher PDF supplied by Erfan; all `\gap` numbers filled).


## Related
- [`ladder.md`](../../ladder.md) — the canonical status board
- [`map.md`](../../map.md) — code system (Q/E/A/D/L) & journey map
