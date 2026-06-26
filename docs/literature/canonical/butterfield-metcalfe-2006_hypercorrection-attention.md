---
title: "The Correction of Errors Committed with High Confidence"
tags: [literature]
aliases: [butterfield-metcalfe-2006_hypercorrection-attention]
---

# The Correction of Errors Committed with High Confidence

**Authors / Year / Venue:** Brady Butterfield, Janet Metcalfe / 2006 / *Metacognition and Learning* 1(1):69–84 (Springer) · **Link:** https://doi.org/10.1007/s11409-006-6894-z
**Canonical ID:** butterfield-metcalfe-2006_hypercorrection-attention
**Sibling note:** this is the *mechanism* follow-up to the original effect paper [`butterfield-metcalfe-2001_hypercorrection-effect.md`](butterfield-metcalfe-2001_hypercorrection-effect.md) (JEP:LMC 27(6):1491–1494) — read that note for the discovery; read this one for *why* it happens.

**Tags:** #literature #canonical #metacognition #attention #teach-stance #teach-skill-grounding #not-brain-science

---

## TL;DR

This paper tests *why* high-confidence errors are hypercorrected (corrected more reliably after feedback than low-confidence errors), pitting the **enhanced-attention** account against mediation and familiarity explanations. Across two experiments it runs a concurrent **tone-detection** secondary task during the corrective feedback and finds tone detection is **selectively impaired** exactly when feedback follows a high-confidence error — and that **missing the tone predicts better later correction** — which is the signature of attention being pulled onto the feedback. The reading: the *surprise* of being confidently wrong captures attention at the moment the correction arrives, encoding it better; in this repo it is **apparatus grounding for the `/teach` stance** (the cognitive basis for surfacing confident mistakes diagnostically), **not** thesis science.

## Key ideas

**The puzzle and the three candidate mechanisms.** Standard interference theory predicts a *strong* (high-confidence) wrong answer should be the *hardest* to overwrite, because the dominant trace competes most at retrieval (the paper's "first hypothesis," p.70). The data go the other way — high-confidence errors are corrected *more* often. The 2006 paper lays out and adjudicates three explanations for that reversal:

1. **Mediation** — maybe the original error itself serves as a retrieval cue for the correct answer (you remember the right answer *via* your memorable wrong one). Tested by reanalyzing the 2001 data.
2. **Semantic neighborhood / familiarity** — maybe high-confidence errors come from *familiar domains* where the correct feedback is also familiar and so easier to encode. Tested via normative item difficulty (Nelson & Narens 1980 norms) as a proxy and via Butterfield & Mangels (2003) familiarity ratings.
3. **Enhanced attentional capture** — being confidently wrong is a *surprise* (a large expectation violation), and surprising events capture attention and are better encoded (von Restorff; novelty-P3). This is the account the two new experiments test directly.

The paper's verdict: mediation contributes little; familiarity is a real, substantial covariate but does not fully explain the effect; **attention is the load-bearing second factor**, leaving familiarity + attention as the two contributors named in the Conclusion (p.82).

**The dual-task logic.** A to-be-detected tone is played *during* the 1.5 s corrective feedback. If feedback to a high-confidence error grabs extra attention, less attention is left for the tone, so the participant should *miss* the tone more often on exactly those trials — and, if the missed attention is what drives learning, **missing the tone should predict getting the item right at retest.** Both predictions are the test of the attention account, and both hold in both experiments. The same logic predicts (and finds) the *mirror* pattern for correct answers: a **low-confidence correct** is also an expectation violation ("I wasn't sure, but I was right"), so its feedback should also capture attention — and tone detection is impaired there too.

**The surprise → attention → encoding chain, and its ERP anchor.** The mechanism is framed as novelty/surprise driving an attention-and-encoding boost at feedback. The paper leans on Butterfield & Mangels (2003), who recorded a **fronto-central positivity peaking ≈350 ms after feedback** that (a) was **larger for high-confidence than low-confidence errors** and (b) **predicted error correction at retest** (larger for items later corrected). The authors read this as a novelty-P3/P3a analogue — a signal of attention to rare/surprising feedback — and connect it to the monitoring/feedback loop of the CHARM memory model (Metcalfe 1993a/b). This is the bridge to error-monitoring ERPs that the repo's errorful-learning synthesis also touches.

## Evidence

**Two new experiments, plus a reanalysis of the 2001 data.** All participants were Columbia undergraduates answering general-information questions (a pool of **619 questions**, e.g. "What igneous rock makes up the bulk of Devils Tower?" → "basalt"; all answers single words), rating confidence on an **analog slider coded −50 (sure wrong) to +50 (sure right)**, then shown the correct answer as 1.5 s feedback (green if matched, red if not), then given a surprise retest on items missed initially. Confidence was binned **low (< −17), medium (−17 to +17 inclusive), high (> +17)**.

**Experiment 1 — N, demographics, design:**
- **39 Columbia undergraduates (23 women, 16 men, mean age 21)**, intro-psych credit; **3 excluded** for neglecting the tone task (detected < 8% of feedback tones), leaving **36** analyzed.
- Tone: 250 Hz, 100 ms, presented 100–500 ms after feedback onset. **Feedback-tone probability was deliberately varied by trial type** to get enough rare trials: p = .25 for frequent responses (low-conf errors, high-conf corrects, omits), .75 for medium-frequency, and **1.0 for the rare critical trials (high-conf errors and low-conf corrects).** Initial test lasted 25 min; 2-min interpolated task before retest.

**Experiment 1 — headline numbers (verbatim from Results):**
- *Basic accuracy:* 25% of all questions correct at first test; 38% omits (excluded); among non-omits, **41% correct at first test**; **average retest accuracy for non-omits = 77%** ("most errors of commission were corrected").
- *Confidence tracks accuracy:* mean within-participant gamma between confidence and initial accuracy = **.63, t(35)=29.2, p<.001**.
- *Hypercorrection (the effect replicated):* mean gamma between confidence-in-error and retest accuracy = **+.13, t(35)=2.5, p<.05** (significantly positive — high-confidence errors corrected *more*). Per-bin retest correction from Table 2: **low .73, medium .76, high .82** (SEM .03–.04).
- *Tone × confidence (the attention signature):* for **errors**, gamma between error confidence and tone detection = **−.22, t(35)=−3.7, p<.001** (higher-confidence error → tone missed more = feedback captured attention). For **correct** responses the relation reversed sign as predicted, gamma = **+.35, t(35)=3.8, p<.001** (low-confidence corrects captured more attention than high-confidence corrects).
- *Tone × final accuracy (the causal link):* mean gamma between tone detection and retest performance = **−.31, t(33)=−3.2, p<.005** — **missing the tone predicted correcting the item**, i.e. attention diverted from the tone was engaged on the feedback. (Two participants who corrected every error were dropped from this analysis.)
- *Feedback vs question tones:* detection was worse during feedback than during the question (92% question vs 73% feedback, t(35)=6.5, p<.001) — consistent with feedback being the attention-demanding event.

**Experiment 2 — the confound fix.** Experiment 1's tone probability *varied by trial type*, so participants might have strategically adjusted responding. Experiment 2 **equalized feedback-tone probability across all response types** (tone on a random 75% of questions and 75% of feedback stimuli, regardless of type), added a constant background fan noise to stabilize hearing, and lengthened the initial test to 35 min (5-min interpolation).
- **45 Columbia undergraduates (25 women, 20 men, mean age 23)**, paid \$10; **6 excluded** for aberrant tone performance (4 detected < 3% of tones; 2 had tone autocorrelations of .93 and .79, i.e. they forgot/remembered the task in runs), leaving **39** analyzed.
- *Basic accuracy:* 29% correct first test overall; 29% omits; **42% correct among non-omits**; **retest accuracy for non-omits = 71%**.
- *Confidence tracks accuracy:* mean gamma = **.63, t(38)=18.5, p<.001**.
- *Hypercorrection:* mean gamma between error confidence and retest accuracy = **+.16, t(38)=4.7, p<.001**. Per-bin retest correction (Table 3): **low .67, medium .71, high .77** (SEM .03–.04).
- *Tone × confidence:* errors gamma = **−.21, t(38)=−4.2, p<.001**; corrects gamma = **+.38, t(38)=5.0, p<.001** (one participant dropped for detecting every correct-feedback tone). Both replicate Experiment 1 in sign and magnitude.
- *Tone × final accuracy:* mean gamma between tone detection and retest = **−.30, t(38)=−3.6, p=.001** — missing the tone again predicted correcting the item.
- *Feedback vs question tones:* 80% question vs 72% feedback, t(38)=2.7, p<.01.

**The 2001-data reanalysis (ruling out the rival mechanisms):**
- *Mediation contributes little.* A performance-adjusted contingency score showed participants were on average **14% more likely** to get an item right at retest when their original error appeared in the retest response set, t(72)=2.4, p<.05 — so the error *does* weakly cue the answer. But holding mediation constant did **not** remove hypercorrection: overall γ=.33, t(28)=3.4, p<.005; error-absent trials γ=.41, t(28)=3.2, p<.005; error-present trials γ=.37, t(28)=2.3, p<.05 (the two contrasts differed by t<1). "If mediation is playing a role … it is likely a small one."
- *Familiarity is real but insufficient.* Normative ease correlated with error confidence (r=.21, t(71)=5.67, p<.001) and with correction likelihood (r=.19, t(68)=6.08, p<.001); partialing out item difficulty, the confidence→correction relation **survived** but shrank (partial r=.11, t(68)=3.70, p<.001). An across-participant within-item gamma also stayed significant (γ=.22, t(63)=2.08, p<.05). So difficulty/familiarity is "a substantial and significant covariate" but "does not sufficiently explain" the effect.

## Limitations

- **The attention measure is indirect, and so is the surprise construct.** Attention is inferred from a *failure* to press the spacebar for a tone; "surprise" is never measured per trial, only assumed to scale with confidence-in-error. The chain surprise → attention → encoding is an inference licensed by the dual-task and the cited ERP, not a within-subject manipulation of surprise.
- **Correlational throughout — gammas, not an experimental contrast.** Every key result is a within-participant gamma correlation over naturally-occurring trial types; nothing is randomly assigned to "high vs low confidence." The authors cannot manipulate how confident a wrong answer is, only observe it, so confidence remains confounded with whatever produces confidence (familiarity, fluency, domain knowledge).
- **High-confidence *errors* are rare,** which is why Experiment 1 had to force tone probability to 1.0 on those trials and why bin counts are small; the effect lives in a thin cell of the data. Several analyses run on subsets (participants "with data in all cells"), e.g. tone×accuracy on 33/25/28 participants depending on the contrast.
- **Familiarity is not fully removed.** The Conclusion explicitly keeps familiarity as a *co-contributor*; this is not a clean "attention alone" result. The two factors are entangled (familiar domains both raise error confidence and make feedback easier to encode).
- **Population narrowness + a noted boundary.** All participants are Columbia undergraduates; the paper's own footnote flags that the surprise-encoding boost "may not override pre-existing memory strength for all populations" and that **elders show a reduced hypercorrection effect** (Butterfield & Stern, in preparation) — so generalization across age is unestablished here.
- **The ERP evidence is borrowed.** The ≈350 ms fronto-central positivity that anchors the surprise/novelty-P3 story comes from Butterfield & Mangels (2003), not measured in these experiments; cite it as supporting plausibility, not as a result of this paper.

## Relevance to the /teach stance

This is **apparatus grounding for the agent's own `/teach` stance — NOT thesis science.** It touches none of A1/A2/A3, produces no brain-alignment number, uses none of our datasets, and must **not** appear in [`docs/01-research-landscape.md`](../../01-research-landscape.md)'s brain/distillation tables. Its single job is to let `teach.md` (`.claude/skills/stances/modes/teach.md`) *cite a mechanism* rather than assert it from parametric memory (the cite-or-flag spine).

**Why it specifically grounds "the tutor logs and surfaces mistakes diagnostically."** The 2001 sibling note establishes the *direction* (confident errors are corrected best) and is the warrant for the **SCR predict-before-reveal loop** (elicit a committed prediction, then reveal, then reconcile — manufacturing the confident-error event whose correction sticks). This 2006 note adds the *mechanism* underneath that warrant: a confident error → surprise → **attentional capture of the correction** → better encoding. That mechanism is the cognitive basis for **desirable-difficulty / errorful learning** and, concretely, for `/teach`'s rule that the tutor draws out where the learner is confidently wrong and stores it as a **forward-looking, diagnostic "what to re-check"** note (superseded on correction), never a tally. The attentional-capture story is *why* surfacing a confident mistake at the point of correction is high-value, not just tidy bookkeeping: the correction lands hardest exactly when a confidently-held belief has just been violated.

**Pairs with, and is distinguished from, the sibling notes:**
- `butterfield-metcalfe-2001_hypercorrection-effect.md` — the discovery (effect + direction). This 2006 paper is its mechanism test; cite 2001 for *that confident errors are corrected best*, cite 2006 for *why (attention to surprising feedback)*.
- [`open-learner-models-and-errorful-learning.md`](open-learner-models-and-errorful-learning.md) — the synthesis index that already lists hypercorrection under "high-confidence errors are corrected best"; this note is the dedicated mechanism source behind that line and behind the "diagnostic, not scorecard" framing.
- [`bjork-2011_desirable-difficulties.md`](bjork-2011_desirable-difficulties.md) — the prior-knowledge precondition (the favorable case is a knowledgeable adult who *can* be confidently wrong). [`dunlosky-2013_effective-learning-techniques.md`](dunlosky-2013_effective-learning-techniques.md) — retrieval + spacing.

**Cite-or-flag guardrails (what this note does NOT support):**
- The gammas, t-values, and per-bin proportions above are **this paper's measured numbers** — they may be quoted (this is external literature evidence, not a thesis result). But they are correlational and live in a thin data cell; do not present hypercorrection as a manipulated causal effect or hand a single gamma the weight of a controlled contrast.
- The **surprise/attention mechanism is the authors' supported-but-inferred account**, anchored on a *borrowed* ERP (Butterfield & Mangels 2003). Phrase it as the explanation the dual-task supports, not as a directly measured encoding boost.
- Hypercorrection is a **within-error gradient** (confident *errors* corrected better than unconfident ones), with a noted **age boundary** (reduced in elders). It is **not** a claim that high confidence is generally good, nor a licence to reward confidence — keep it paired with the repo's anti-sycophancy / availability-bias rule (warmth from content, never praise).

**Suggested edit to `docs/01-research-landscape.md`:** none in the A/B/C/D/E science tables. If the landscape doc carries the apparatus-only `/teach`-grounding footnote used for the other pedagogy notes, add a one-line companion entry (Butterfield & Metcalfe 2006 = the *attentional-capture mechanism* behind hypercorrection / the diagnostic-mistake-logging design), flagged apparatus-only, no A1/A2/A3 weight. Left for the main session to apply.

## Provenance

**Citation: verified.** CrossRef (`api.crossref.org/works/10.1007/s11409-006-6894-z`) and OpenAlex (`api.openalex.org/works/doi:…`) independently return the identical record — authors Brady Butterfield & Janet Metcalfe, *Metacognition and Learning* 1(1):69–84, 2006, DOI 10.1007/s11409-006-6894-z. OpenAlex: 142 citations, `oa_status: closed`, `is_oa: false`.

**Full text: READ first-hand from the PDF.** The full paper (`data/papers/butterfield-metcalfe-2006_hypercorrection-attention.pdf`, journal pp. 69–84) was read via the pypdf text extraction supplied for cross-checking (`bm2006.txt`), which rendered the complete body, both Method/Results sections, Tables 1–3, and the reference list cleanly. (The harness `Read` tool's PDF *image* renderer was unavailable — poppler/`pdftoppm` not installed — so the page-image path could not be used; the text-layer extraction was complete and is what was read.) Every number in this note was taken directly from that text. **This corrects the prior unreachability flagged on the 2001 sibling note — that one remains unread; this 2006 paper was read in full.**

**One rendering caveat, resolved.** pypdf substituted the Goodman–Kruskal **gamma (γ)** symbol with `+` throughout the Results (e.g. the printed "+ = .13" / "+ = −.22"). These are unambiguously the within-participant **gamma correlations** the Method and figure captions describe; reported here as gamma. The Tables also rendered minus signs as "j" (e.g. confidence scale "j50") and a few ligatures oddly (FstrengthG, Bxxx'') — cosmetic OCR-of-font artifacts, not value errors; the numeric cells are intact.

## 2006 restates of B&M 2001 (for the 2001 note's `\gap` slots — reported to the main session, NOT applied here)

The 2006 paper restates and reanalyzes specific values from the original study. **Caveat:** in this paper the citations are split — the *named effect* is cited as **[Butterfield & Metcalfe (2001a)](butterfield-metcalfe-2001_hypercorrection-effect.md)** = the JEP:LMC 27(6):1491–1494 paper (the subject of the 2001 note), while the **data table and all reanalysis statistics are attributed to Butterfield & Metcalfe (2001b)**, a *conference poster* ("Updating the egregious," APS annual meeting), not the JEP article. So these restated numbers may be from the poster dataset, which may or may not be identical to the published 2001 article's data. Treat as candidate fills, verify against the 2001 article before landing:
- **Table 1 (attributed to 2001b)** — confidence-bin conditional probabilities. P(correct at retest | incorrect at 1st test & resp. conf.): **low .06, medium .39, high .89** (the original hypercorrection gradient). P(response confidence): low .52, med .08, high .41. P(error in retest response set): low .61, med .81, high .87. P(correct at 1st test | conf.): low .51, med .86, high .77. (Asterisk footnotes: "mean from the 71 participants with data in all three cells" and "mean from the 23 participants" — i.e. **N≈71–73** in the source dataset, not the published article's N unless they coincide.)
- **Reanalysis statistics (2001b data):** mediation contingency +14%, t(72)=2.4, p<.05; hypercorrection holding mediation constant γ=.33, t(28)=3.4, p<.005; normative-ease × error-confidence r=.21, t(71)=5.67, p<.001; partial r=.11, t(68)=3.70, p<.001; within-item gamma .22, t(63)=2.08, p<.05.
- **No verbatim restatement of the *published 2001 article's own* N or its headline gamma** appears in this 2006 paper — the 2001a citation is named only as the source of the effect, with the numbers carried by the 2001b poster. So the 2001 note's `\gap` for the article's exact N and article-reported gamma is **not cleanly fillable from this paper**; the Table 1 values above are the closest available and are poster-attributed.

## Verified

Full PDF read first-hand (text-layer extraction; image renderer unavailable, noted in Provenance). Citation verified against CrossRef and OpenAlex (exact agreement); `oa_status: closed`. All per-experiment statistics (N, demographics, the −50/+50 slider, confidence bins, retest accuracies, every gamma/t/p and per-bin proportion) were read verbatim from this paper's Results and Tables 2–3; the 2001-reanalysis figures from Table 1 and the reanalysis paragraphs. The gamma symbol rendered as `+` in extraction and is reported as gamma (caveat in Provenance). No number was estimated or invented; nothing in the paper's body was left unread.

## Read Date

2026-06-20


## Related
- [`ladder.md`](../../ladder.md) — the canonical status board
- [`map.md`](../../map.md) — code system (Q/E/A/D/L) & journey map
