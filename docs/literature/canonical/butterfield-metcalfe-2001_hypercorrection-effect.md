# Errors Committed with High Confidence Are Hypercorrected

**Authors / Year / Venue:** Brady Butterfield, Janet Metcalfe / 2001 / *Journal of Experimental Psychology: Learning, Memory, and Cognition* 27(6):1491–1494 · **Link:** https://doi.org/10.1037/0278-7393.27.6.1491
**Canonical ID:** butterfield-metcalfe-2001_hypercorrection-effect

**Tags:** #literature #canonical #metacognition #teach-stance #teach-skill-grounding #not-brain-science

> **Provenance flag (read first):** the full PDF could not be parsed by any tool available here — see the **Provenance** section. The citation is verified against CrossRef and OpenAlex; the substantive claims below are grounded in the title, the established secondary record, and the repo's own S27 synthesis note (`open-learner-models-and-errorful-learning.md`), **not** a first-hand read of the Method/Results. Treat the per-experiment numbers as **`\gap`** — deliberately absent rather than invented.

---

## TL;DR

This is the paper that named and demonstrated the **hypercorrection effect**: when a person answers a general-knowledge question wrong but had been **highly confident** the wrong answer was right, that error is **corrected more reliably** on a later test (after corrective feedback) than an error made with **low** confidence. The direction is counterintuitive — a strict interference account predicts the opposite (a strongly-held wrong answer should compete *more* with the correction) — and the authors read the reversal as evidence that the **surprise of being confidently wrong** recruits attention to the corrective feedback at the moment it arrives. In this repo it is **apparatus grounding for the `/teach` stance**, the empirical warrant for the SCR predict-before-reveal loop; it is **not** thesis science (no A1/A2/A3, no brain-alignment number).

## Key ideas

**The effect.** Hypercorrection = a **positive** relationship between the confidence with which an error was originally committed and the probability that the same item is answered correctly after feedback. High-confidence errors are the *most* likely to be fixed; low-confidence errors (near-guesses) are the *least* likely to be fixed. The name and the demonstration are this 2001 paper's; the larger mechanistic program (the surprise / attention-to-feedback account, error-related encoding) is built out in the authors' follow-ups (Butterfield & Metcalfe 2006; Metcalfe & Finn; Metcalfe 2017 *Annual Review of Psychology* review).

**Why it is counterintuitive — the interference prediction it overturns.** A naive associative-interference view says: the more strongly you hold the wrong answer (high confidence ⇒ strong memory trace for the error), the harder it should be to overwrite with the correct answer, because the old trace competes at retrieval. That predicts high-confidence errors should be *stickier* and *harder* to correct. The data go the other way. So confidence-in-the-error is not acting as trace strength that blocks the correction; something about the high-confidence-error event *helps* the correction stick.

**The proposed mechanism — surprise drives attention to the feedback.** Being confidently wrong is a large prediction-error event: you expected to be right and you were not. That surprise increases attention to (and deeper encoding of) the corrective feedback at the moment it is delivered, so the correct answer is encoded better precisely when the prior belief was strongest and most violated. This is the through-line the authors develop in later work into an attention/encoding-at-feedback account (and connects, in the broader literature, to error-monitoring signals — see the repo's synthesis note linking the Pe / error-positivity ERP work, Moser et al. 2011).

**The boundary the effect lives inside.** Hypercorrection is established for **errors the learner actually held a belief about** (high vs low confidence in a *wrong* answer that then gets *corrected*). It is a within-error gradient, not a claim that confidence is good in general; the favourable case is a knowledgeable adult who can be confidently wrong, get told, and re-encode. (For the prior-knowledge precondition see `bjork-2011_desirable-difficulties.md`; for the "diagnostic not scorecard" framing of surfacing one's own errors see `open-learner-models-and-errorful-learning.md`.)

## Evidence

**Design (from the established record of this paper; the verbatim numbers are a `\gap` — not reachable here).** Participants answer general-information / general-knowledge questions, rate confidence in each answer on a graded scale, receive corrective feedback on the items they got wrong, and are retested. The load-bearing analysis is the relationship, **within errors**, between original confidence and probability of subsequent correction. The headline finding is that this relationship is **positive**: correction probability rises with the confidence originally placed in the wrong answer.

**What I could not verify first-hand and therefore do not state as a number:** the exact N, the precise confidence-scale range, the gamma (or other) correlation coefficient between confidence and correction, and the per-confidence-bin proportions corrected. These exist in the paper's Method/Results but the full text was not reachable by any tool here (see **Provenance**). They are flagged as `\gap` rather than guessed. If a later session reaches the PDF, fill them in here.

**Citation, fully verified (CrossRef + OpenAlex agree exactly):** *JEP: LMC* vol. 27, issue 6, pp. 1491–1494, 2001; authors Brady Butterfield and Janet Metcalfe; DOI 10.1037/0278-7393.27.6.1491; 144 citations per OpenAlex; open-access status **closed** (Unpaywall and OpenAlex both report no OA full-text location).

## Limitations

- **Single, short report (≈4 pp.) with a specific paradigm.** The effect is shown for general-knowledge facts with explicit confidence ratings and a feedback-then-retest loop; generalisation to other materials, ages, and richer learning is the job of the later literature, not this paper.
- **Confidence and accuracy are correlated, so the "confidently wrong" cell is the interesting-but-thinner one.** People are usually right when confident; truly high-confidence *errors* are comparatively rare, which is exactly the cell the effect rests on — a measurement caveat the mechanistic follow-ups had to manage.
- **The surprise/attention mechanism is an inference in this paper, sharpened later.** The 2001 report establishes the *direction*; the attention-to-feedback / error-encoding account is developed and tested more directly in the authors' subsequent work. Cite the mechanism as their *proposed* explanation, not as measured here.
- **Read-access caveat is real:** the body was not parsed here (Provenance), so the above leans on the secondary record for everything past the title-level claim.

## Relevance to the /teach stance

This is **apparatus grounding for the agent's own `/teach` stance — NOT thesis science.** It touches none of A1/A2/A3, produces no brain-alignment number, uses none of our datasets, and must **not** appear in `docs/01-research-landscape.md`'s brain/distillation tables. Its single job is to let `teach.md` *cite* a mechanism instead of asserting it from parametric memory (the cite-or-flag spine).

**Specifically, it is the evidence behind two `teach.md` design choices:**

1. **The SCR "predict before reveal" loop** (teach.md §"SCR"). The loop asks for the learner's prediction *with its reason* before showing a number or confirming a step, then reveals, then reconciles ("you expected X, the record says Y — how do you square that?"). Hypercorrection is *why this is well-founded, not just nice*: a prediction stated with conviction and then shown wrong is exactly the confident-error event whose correction sticks best. Eliciting the confident commitment first is what manufactures the surprise that makes the correction land. Without the prediction step, a quietly-held or never-surfaced wrong belief gets none of that benefit.

2. **Surfacing high-confidence mistakes on purpose, and keeping mistakes diagnostic.** The stance deliberately draws out where the learner is confidently wrong (rather than smoothing past it) and stores mistakes in the lesson layer as forward-looking "what to re-check," superseded on correction — never as a tally. Hypercorrection grounds the *first* half (confident errors are the high-value correction targets); the "diagnostic not scorecard" framing of the *second* half is grounded in `open-learner-models-and-errorful-learning.md` and the error-framing literature (Moser et al. 2011; Tulis et al. 2024), not here. Keep that split when citing.

**Cite-or-flag guardrails (what this note does NOT support):**
- Do **not** quote a specific gamma, N, scale range, or proportion-corrected from this note — those are `\gap` here (Provenance). Cite the *direction and the mechanism*, not a number, until the PDF is read.
- The **attention/surprise mechanism is the authors' proposed explanation** (sharpened in their later work), not a result measured in this 4-page report; phrase it as such.
- Hypercorrection is a **within-error gradient** (confident *errors* corrected better than unconfident ones). It is **not** a claim that high confidence is generally good, nor a licence to reward confidence — keep it paired with the repo's anti-sycophancy / availability-bias rule.
- This note sits alongside `open-learner-models-and-errorful-learning.md` (the broader errorful-learning synthesis, which already cites this paper at one line), `dunlosky-2013_effective-learning-techniques.md` (retrieval + spacing), and `bjork-2011_desirable-difficulties.md` (the prior-knowledge precondition) as the `/teach` grounding set — it is the dedicated, mechanism-level source for the *predict-before-reveal* choice specifically.

## Provenance

**Citation: verified.** CrossRef (`api.crossref.org/works/10.1037/0278-7393.27.6.1491`) and OpenAlex (`api.openalex.org/works/doi:…`) independently return the identical record — authors Brady Butterfield & Janet Metcalfe, *JEP: LMC* 27(6):1491–1494, 2001, DOI 10.1037/0278-7393.27.6.1491. OpenAlex: 144 citations, `oa_status: closed`. Unpaywall: `is_oa: false`, no OA location.

**Full text: NOT parsed — stated plainly, not papered over.** The only known open full-text copy is the Metcalfe-lab mirror at `columbia.edu/cu/psychology/metcalfe/PDFs/Butterfield Metcalfe 2001.pdf`, which is now behind a **Cloudflare managed challenge** (the publications HTML returns the JS "Just a moment…" interstitial) **and** an **Imperva WAF on the PDF subpath** (the 183 KB response carries the `.WAF` magic header, not a PDF body) — neither yields to `curl` (which cannot solve the JS challenge). The publisher routes are paywalled: APA PsycNet renders only a "Loading…" shell to WebFetch (HTTP 200 but no body), Ovid full-text returns HTTP 402, ResearchGate returns HTTP 403, and the ResearchGate direct-PDF link returns a Cloudflare `error code: 1020`. A reader-proxy (`r.jina.ai`) on the APA and ResearchGate pages returned only the privacy-banner / 403. Unpaywall and OpenAlex both confirm **no OA copy exists anywhere**, so there is no clean route.

**One active hazard recorded for the next session:** WebFetch's 15-minute cache for the `columbia.edu/cu/psychology/metcalfe/PDFs/…2001.pdf` URL is **poisoned** — it repeatedly returns an unrelated 2003 *Los Angeles Times* opinion column ("Hunches Rule Us — and Fool Us"), not the paper. Do not trust a WebFetch on that exact URL; use a real headless browser (the Firecrawl `scrape`/`parse` MCP tools, which were not available to this subagent) or an authenticated library proxy to get the body.

**What this means for the note:** everything past the verified citation is grounded in (a) the paper's title and named effect, and (b) the established secondary/scholarly record plus the repo's own S27 synthesis (`open-learner-models-and-errorful-learning.md`, which cites this paper). The per-experiment numbers (N, scale, gamma, proportions) are deliberately left as `\gap`. **No number in this note was estimated or invented.**

## Verified

Citation verified against CrossRef and OpenAlex (exact agreement); OA-closed status confirmed by Unpaywall and OpenAlex. **Full PDF NOT read** — Columbia mirror is Cloudflare+Imperva gated, all publisher routes paywalled/403/402, no OA copy exists, and the WebFetch cache for the Columbia URL is poisoned (returns an LA Times article). The substantive claims are grounded in the title-level effect and the repo's existing synthesis note, with all per-experiment numbers flagged `\gap` rather than guessed, per the "say so rather than guess" rule.

## Read Date

2026-06-19
