# Open Learner Models and Learning Analytics Dashboards: A Systematic Review

**Authors / Year / Venue:** Robert Bodily; Judy Kay; Vincent Aleven; Ioana Jivet; Dan Davis; Franceska Xhakaj; Katrien Verbert / 2018 / *LAK '18: Proceedings of the 8th International Conference on Learning Analytics and Knowledge* (Sydney, NSW, Australia, Mar 7–9, 2018), ACM, pp. 41–50 · **Link:** https://doi.org/10.1145/3170358.3170409
**Canonical ID:** bodily-2018_olm-lad-systematic-review

**Tags:** #literature #canonical #pedagogy #teach-stance #teach-skill-grounding #not-brain-science #OLM #LAD

---

## TL;DR

A systematic review of **102 articles introducing 107 Open Learner Models (OLMs)** that maps the OLM design space and bridges it to student-facing **Learning Analytics Dashboards (LADs)** — the two communities share the goal of "learner awareness tools" but grew up apart (ITS/AIED for OLMs, the LAK community for LADs) with "very limited cross-fertilization." The headline characterization of a typical new OLM: it is built on a single data type (57.9%), assessment-based, interactive, and well-evaluated, but rarely aggregates across applications (5.6%). This is the **foundational map of the OLM design space** that `/teach`'s learner-visible mastery ledger sits inside — **apparatus grounding for `/teach`, NOT thesis science** (no A1/A2/A3, no brain-alignment number, none of our datasets).

## What an OLM is (and how it relates to a LAD)

An **Open Learner Model** "makes a machine's representation of the learner available as an important means of support for learning" (the review's quote of Bull & Kay 2010). The model "might represent variables regarding 'student's knowledge, interests, affect, or other cognitive dimensions,' which typically are 'inferred based on the learner's interactions with the system.'" OLMs are usually embedded in intelligent tutoring systems (ITSs) and shown to the learner as skill bars / progress views. A **LAD** is "a single display that aggregates multiple visualizations of different indicators about learners, learning processes, and/or learning contexts." The two overlap heavily in goal but differ in roots: OLMs are grounded in **student/learner modeling**, LADs in **data-driven decision making**. The review's contribution is the bridge plus the proposal of an umbrella term, **student-facing learning analytics**.

The review names the historical roles OLMs were built for, which is the menu `/teach` is choosing from: (i) improving the **accuracy** of the learner model; (ii) supporting **metacognition** — reflection, self-monitoring, planning; (iii) **navigation** / deciding what to learn next; (iv) **assessment**; (v) the learner's **right of access to and control of** their own learning data. It also flags the **negotiable** student model (Bull & Pain 1995) — the learner can "appeal" the system's modeling decisions, and the ensuing negotiation yields more accurate models and better learner self-understanding.

## Key ideas (the five comparison dimensions)

The review answers five research questions — the same five dimensions the task asked for:

1. **Data use & modeling** (RQ1) — what data each OLM uses and how sophisticated the model is (Table 2, below).
2. **Key publication venues** (RQ2) — top OLM venues are **AIED (13), IJAIED (12), ITS (9), UMAP (9)**; top LAD venue is **LAK (16)**. The lists barely overlap (only EC-TEL, AIED, LAK, IEEE TECT recur in both), illustrating the community gap. UMUAI appears with 2 OLM papers.
3. **Authors / articles** (RQ2) — top OLM author is **Bull, S. with 31 OLM publications (but only 2 LAD)**, then Brusilovsky (13 OLM / 1 LAD), Johnson (7/1), Hsiao (7/0). The OLM↔LAD publication counts (Table 4) are the concrete evidence of the gap: prolific OLM authors are nearly invisible in LAD reviews. Top-cited OLM article: **STyLE-OLM (215 citations)**.
4. **Key themes** (RQ3) — top keywords across the corpus are **intelligent tutoring systems, learning analytics, self-regulated learning**, then self-assessment, learner model, reflection, visualization, trust, learner independence, metacognition. SRL and reflection recurring signals "a key purpose of opening the model to the learner."
5. **System evaluation** (RQ4) and **LAD-vs-OLM contrast** (RQ5) — below.

**Method / scope.** Keyword search ("Open Learner Model*", "Open Social Learner Model*", "Open Student Model*", "Open Social Student Model") in title/abstract across **five sources: Computers and Applied Sciences, ERIC, IEEE Xplore, ACM Digital Library, and Google Scholar** → 190 articles. An author-expansion step (publication lists of the top-10 authors + author lists hand-curated by two domain experts, Judy Kay and Vincent Aleven) added 44 → **234 articles**. **Inclusion criterion: only articles introducing a new OLM or a new version of an OLM** (papers merely citing a prior OLM were excluded) → four coders screened to **114** → seven more dropped during coding → **102 articles / 107 OLMs** for final analysis (five articles introduced two OLMs each). Interrater reliability across four coders: **Fleiss' κ = 0.78, Krippendorff's α = 0.78, 89% pairwise percent agreement** ("acceptable" by the >0.67 threshold for four coders, just under the 0.80 "excellent" bar).

## Evidence (datasets, metrics, headline numbers)

**Data use & modeling — Table 2** (n = 107 OLMs; published exact figures, abstract rounds them):

| Category | # of OLMs | % of OLMs |
|---|---|---|
| Single type of data | 62 | **57.9%** ("almost 60%") |
| Behavioral metrics | 35 | **32.7%** ("33%") |
| Input provided by the user | 42 | **39.3%** ("39%") |
| Complex modelling | 40 | **37.2%** ("37%") |
| Multiple applications | 6 | **5.6%** ("just 6%") |

Reading: "about half of OLMs used a single type of data" (typically MCQ scores or ITS/cognitive-tutor mastery), "about one third … included behavioral metrics," and OLMs "rarely use data from multiple applications" — unsurprising since most are embedded in a single ITS. The 37.2% "complex modelling" figure is read as **under-reporting of method, not simplicity of method**: "authors were not discussing their modelling techniques in OLM papers," which the review ties to **trust** ("being more explicit about the method used to infer the learner model has potential to advance OLM research").

**Evaluation — Table 8** (% of all 107 OLMs):

| Category | # | % |
|---|---|---|
| Evaluation (any validation study) | 80 | **74.8%** |
| Authentic evaluation (real classroom, not lab) | 42 | **39.3%** |
| Formal/STEM domain | 53 | **49.5%** |
| Tertiary (higher-ed) | 58 | **54.2%** |
| Secondary | 12 | **11.2%** |
| Multiple evaluations | 11 | **10.3%** |

So **three-quarters of new OLMs were evaluated at all**, and **>1/3 in an authentic classroom setting** ("indicates that many OLMs may be close to classroom-ready"). "Evaluation" was defined broadly — usability tests, perception surveys, or RCTs all counted. STEM-domain and higher-ed contexts each appeared only ~half the time, less concentrated than the authors predicted. Sample sizes shown only as a histogram (Figure 2); no central tendency reported in the text (`\gap`: no mean/median sample size stated).

**OLM-vs-LAD contrast — Table 9** (the bridge; LAD figures recomputed from Bodily & Verbert 2017, which covered LADs Jan 2005 – Jun 2016):

| Category | LAD | OLM |
|---|---|---|
| Evaluation percentage | 59% | **75%** |
| Behavioral metrics | **75%** | 33% |
| Assessment data | 37% | **100%** |
| Comparison standard for students | 38% | **52%** |
| Interactive | 31% | **81%** |

The pattern: OLMs are **more evaluated, more interactive, universally assessment-based, and more often give a peer/course comparison**; LADs lean far harder on **behavioral / resource-use metrics**. The review attributes the evaluation gap partly to OLMs being the older field (first term-using publications ~1997; the first LAK conference was 2011). Its standing claim: **"In OLM work, there was a heightened focus on learner control and access to their own data."** The note that "the majority of LADs (69%) rely on a static representation of behavioral metrics" is the contrast point that motivates importing OLM interactivity into LAD design.

## Limitations

- **Scope is narrow by construction.** Only papers *introducing* a new OLM (or new version) were included; theoretical OLM papers and comparison/survey papers were excluded. The authors explicitly "do not claim the results … to represent the entire body of work on OLMs."
- **Keyword-driven search misses untagged work.** Articles discussing an OLM without the keywords in title/abstract could be missed; the expert spot-check (Kay, Aleven) is the only mitigation, and it is a judgment patch, not exhaustive.
- **The LAD comparison is cross-review, not re-coded.** RQ5 compares this review against a *previously published* LAD review (Bodily & Verbert 2017) using "a slightly modified version of that review's methodology" — the authors concede "these differences could potentially affect the conclusions." The LAD review is also older (through Jun 2016), so some LAD venue/author counts are stale.
- **"Evaluation" is a very loose bin.** A usability test and an RCT both count as "Evaluation," so the 74.8% figure is presence-of-any-validation, **not** evidence of rigorous controlled outcome testing. The review separately notes that in the broader field, "close the loop" studies that actually test effect on learning "rarely make it into educational software, and their effect … is rarely rigorously tested" — i.e. the corpus is well-*studied* but not necessarily shown to *cause learning gains*.
- **No effect-size synthesis at all.** This is a descriptive/bibliometric review (counts, percentages, keyword frequencies, citation ranks). It reports *what OLMs are and how often they are evaluated*, never a pooled estimate of whether they improve learning.

## Relevance to this thesis

**Apparatus grounding for the agent's `/teach` stance — NOT thesis science.** It touches none of A1/A2/A3, produces no brain-alignment number, and uses none of our datasets. **Keep it out of `docs/01-research-landscape.md`'s brain/distillation tables.** Its sole job is to let `/teach` *cite* rather than assert.

`/teach` keeps a **learner-visible mastery ledger** in `docs/learning/records/` — that ledger *is* an Open Learner Model in this review's exact sense: a machine's representation of the learner, opened to the learner as a means of support. This paper is the **foundational map of that design space** — the canonical census of *what OLMs are, how they model the learner, and how the field evaluates them*. Three things `/teach` may now cite this note for:

1. **The ledger is an OLM, and the field's modal design is single-data-type + assessment-based.** 57.9% of OLMs use one data type; 100% (vs 37% of LADs) use assessment data. `/teach`'s mastery-on-demonstrated-performance ledger is squarely in the dominant lineage, not an oddity. Cite at: *positions the ledger inside the named, surveyed OLM design space.*
2. **Interactivity and learner control over the model are the OLM tradition's distinguishing strengths** — 81% of OLMs are interactive (vs 31% of LADs), with "a heightened focus on learner control and access to their own data," and the negotiable-model lineage (the learner can appeal/challenge the system's assessment). This is the structural warrant for `/teach`'s supersede-on-correction, learner-can-contest design — it is the OLM tradition, not an invention.
3. **The under-reporting-of-method → trust link.** Only 37.2% of OLM papers explained their modeling method, which the review ties to *trust*: being explicit about how the learner model is inferred advances the field. Maps to `/teach` making its mastery inference legible to the learner rather than an opaque score.

**Cite-or-flag guardrails (what this note does NOT support):**
- It does **not** demonstrate that exposing the learner model *improves learning outcomes*. It is descriptive/bibliometric; "Evaluation = 75%" means *a validation study of some kind existed*, not *a positive controlled effect*. For the conditional-effectiveness and "visualization alone is weak" claims, route to **`open-learner-models_2025-review.md`** (Robles Mucho et al. 2025 meta-synthesis). For "scorecard-drives-avoidance / diagnostic-not-scorecard," route to **`open-learner-models-and-errorful-learning.md`**. This 2018 paper is the *map of the space*; those two carry the *does-it-work-and-when*.
- The Table-9 OLM-vs-LAD numbers are a **cross-review comparison the authors flag as methodologically imperfect** — cite as a characterization of the two communities, not as a like-for-like measured contrast.

**Long & Aleven 2017 corroboration check (the repo's flagged number) — NEGATIVE.** This review lists **[39] Long, Y. and Aleven, V. 2017. "Enhancing learning outcomes through self-regulated learning support with an open learner model." *User Modeling and User-Adapted Interaction*, 27, 1 (2017), 55–88** in its reference list. That confirms the **citation metadata** (authors, title, venue UMUAI, vol 27 iss 1, pp. 55–88, year 2017) — useful, since Vincent Aleven coauthors this review. **But the body of the paper never cites [39] inline, never reports a sample size (the string "302" does not appear anywhere in the text), and never restates the OLM-only-with-control finding.** So this 2018 review **does not corroborate** the repo's carried-over "n≈302, OLM-only-with-control" result — it only confirms the bibliographic shell. The number remains an open `\gap` against the primary Long & Aleven 2017 PDF.

## Verified

**Primary paper read in full, first-hand, from the published ACM version.** The full extracted text of the published PDF (`data/papers/bodily-2018_olm-lad-systematic-review.pdf`) was read end to end — abstract, all five research-question sections, every table (Tables 1–9), the methods/coding pipeline, the limitations, the merge recommendations, the conclusion, and the complete 56-item reference list. The text is confirmed to be the **published** version (ACM page numbers 41–50, ACM ISBN 978-1-4503-6400-3/18/03, the LAK '18 conference header, and the DOI block all present), not the preprint.

**Published vs preprint.** Two PDFs are on disk: `bodily-2018_olm-lad-systematic-review.pdf` (published, 785 KB) and `bodily-2018_olm-lad-systematic-review_preprint.pdf` (preprint, 6.2 MB). Per the task, the **published version's numbers are used throughout**; where the abstract rounds (e.g. "almost 60%", "33%", "just 6%"), the **exact** Table 2 figures are recorded (57.9%, 32.7%, 5.6%). The preprint PDF was **not** separately re-extracted — no `pdftotext`/`pdftoppm` is installed in this container, so PDF page rendering and a fresh preprint extraction were unavailable; the published-version extracted text (`scratchpad/bodily.txt`) is authoritative and was relied on directly.

**Citation verified** via CrossRef (`api.crossref.org/works/10.1145/3170358.3170409`): title, all seven authors in order (Bodily, Kay, Aleven, Jivet, Davis, Xhakaj, Verbert), 2018, *Proceedings of the 8th International Conference on Learning Analytics and Knowledge (LAK '18)*, ACM, DOI 10.1145/3170358.3170409 — all match the PDF.

**Open `\gap`s:** (1) no mean/median evaluation sample size is stated in the text (only a histogram, Figure 2); (2) the Long & Aleven 2017 n≈302 / OLM-only-with-control result is **not** restated here and remains unverified against its own PDF.

## Read Date

2026-06-20
