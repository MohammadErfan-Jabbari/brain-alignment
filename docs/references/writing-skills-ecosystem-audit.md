# The writing-skills ecosystem — what 11 repos actually implement

Audit pass (2026-06-22, `/meta`, S35) for the `/write` + `scientific-writing` redesign. Erfan asked: clone the
named skill repos, fan out subagents, and find — unbiased — each repo's **take on how to write a research paper,
or how to convert an idea/experiment into writing.** Goal: get all the juice, miss no detail, then digest one
step at a time.

**Method.** 11 repos cloned to `data/reference-repos/`. 13 sub-agent readers (sonnet) over the writing/
ideation/planning/paper skills in each (the bio-database, office-automation, and dev-tooling skills were skipped
as out of scope). Plus the earlier 7-slice deep audit of `imbad0202/academic-research-skills` (the skill Erfan
actually used). Each reader scored its slice against the established writing canon (Gopen-Swan, Williams, Schimel,
Swales, McEnerney, Mensh-Kording, Whitesides — see `scientific-writing-methodology.md`) AND captured the repo's
own approach, including mechanisms the canon doesn't cover. Companion doc: `scientific-writing-methodology.md`.

---

## The headline finding

1. **The writing canon is almost entirely absent from the tooling ecosystem.** Across ~30 relevant skills, not
   one cites Gopen-Swan, Schimel, Swales, McEnerney, or Mensh-Kording by name. Two name-check something:
   `k-dense/scientific-writing` lists Williams + Whitesides + Strunk-White + Zinsser in a "books" sidebar (does
   not operationalize them); `bahayonghang/academic-writing-skills` uses an "AXES" paragraph model (its own, not
   cited). So the sentence-level reader-expectation theory is real but under-built everywhere — not just in our repo.

2. **Every repo has the same shape as ours: structure + integrity machinery is thick; writing *craft* is thin.**
   The skill Erfan used (`imbad0202`) is the extreme case — measured at ≈72% process+integrity, ~20% craft, canon
   absent; its only IRON RULEs are anti-fabrication gates, its drafting phase is five words ("section-by-section
   draft, register adjustment"). This is the "immune system, not a notion of health" pattern, confirmed as an
   ecosystem-wide default, not a local failure.

3. **But the serious repos converge on a real positive model** — just at a *different scale* than the canon. The
   canon is micro (sentence/paragraph reader-expectation). The repos are macro (paper/section structure +
   claim-evidence binding + reviewer psychology). They are **complementary, not competing** (see §"The
   complementarity").

4. **Two repos are worth deep mining; most of the rest contribute one or two sharp ideas; two are out of scope.**

---

## Per-repo scorecard

| Repo | What it actually is | Craft depth | Canon cited | Single best mechanism |
|---|---|---|---|---|
| **evoscientist/evoskills** | Full idea→experiment→paper pipeline (16 skills) | **Highest** | No | Reverse-then-forward story design + claim-to-experiment mapping |
| **bahayonghang/academic-writing-skills** | Section-level LaTeX writer + reviewer-sim audit | **Highest (craft)** | No (own AXES) | Claim-evidence contract with a 4-level strength ladder + over-claim guard |
| **k-dense-ai/scientific-agent-skills** | 150+ science skills; writing+thinking cluster | Medium | Names books only | Per-venue register templates + reviewer-expectations + non-linear draft order |
| **imbad0202/academic-research-skills** | The one Erfan used: paper/pipeline/reviewer/deep-research | Low (craft); high integrity | No | Claim Intent Manifest + Epistemic-Status tags + Knowledge Isolation + Temporal-Integrity rule |
| **jamditis/claude-skills-journalism** | Journalism toolkits; ai-writing-detox + story-pitch | Medium (voice) | No | Structural AI-tell detox (tricolon, em-dash-join, authority-grab) + verbal-tic read-aloud test |
| **lllllllama/RigorPilot-Skills** | Rigor-preserving reproduction/exploration | N/A (not writing) | No | SCIENTIFIC_CHANGELOG + frozen anchors + verified/partial/blocked state lattice |
| **anthropics/life-sciences** | scientific-problem-selection (idea front-end) | N/A (ideation) | No | Optimization-function framing (name the evaluation game) + "I can't imagine" gap test |
| **shubhamsaboo/awesome-llm-apps** | General agent skills; academic-researcher, editor | Low | No | Four-level editing decomposition (developmental→line→copy→proof) |
| **claude-office-skills** | Commercial productivity skills | Low | No | Argument-mapping tree (claim→evidence→counter→rebuttal) before prose |
| **google-deepmind/science-skills** | Bioinformatics DB + literature-search toolkit | **Out of scope** | No | (retrieval only) |
| **yorkeccak/scientific-skills** | Valyu-API search wrappers | **Out of scope** | No | (retrieval only) |

---

## The convergent model (what the serious repos agree on — unbiased)

Read across evoskills, academic-writing-skills, k-dense, imbad0202, RigorPilot, life-sciences, a consistent
"how to turn work into a paper" emerges. Six points, none of which our current `/write` encodes as a positive model:

1. **Structure/plan before prose — and often figure before prose.** Universal. evoskills draws the pipeline
   figure as step 1 ("highlights novelty, not just explanation"); k-dense drafts figures/tables first as "the core
   data story"; academic-writing-skills answers 4 backward-planning questions before any sentence. Outline-first is
   the one thing they all share.

2. **Non-linear draft order: Methods/Results first, Abstract and Title last.** Stated explicitly by k-dense and
   evoskills ("abstract last, because by then the story is clear"). Prevents writing a frame the results don't support.

3. **Claim↔evidence binding is the spine — and several make it a pre-commit + audit loop.** This is the most
   important convergence. evoskills requires a claim-to-experiment table (every claim → ≥1 figure/ablation row)
   before drafting; imbad0202 emits a *Claim Intent Manifest* (pre-commit every claim + "must not" constraints,
   then a downstream agent diffs intended∩emitted∩supported and flags drift); academic-writing-skills runs a
   *claim-evidence contract* with a strength ladder (unsupported / observed / supported / strong) feeding an
   over-claim guard that sets the wording. **This is the direct mechanization of our D011 number rule — extended
   to qualitative claims and turned from a final check into a plan-then-audit loop.**

4. **Name the contribution and declare the evaluation frame.** life-sciences: state the *optimization function*
   (basic-science vs technology vs invention) before writing, because reviewers reject work evaluated in the wrong
   frame. k-dense (ScholarEval): score on **soundness × contribution** as two axes (sound-but-not-new ≠
   new-but-not-sound). scientific-agent thinking + research-grants: a 5-type innovation taxonomy so "novel" is
   named precisely. evoskills + academic-writing-skills: the intro is a funnel that *earns* its gap claim (the CARS
   move structure, operationalized but never named).

5. **Reviewer-anticipation drives revision, not last-pass polish.** evoskills "Start from Rejection, not from
   Story" — design to survive the strongest objection; "Delete the Most Impressive Unsupported Sentence before
   submission." academic-writing-skills ranks issues by *reviewer psychology* (what a reviewer is most likely to
   catch and sink the paper on: #1 = numbers that don't match claims). imbad0202 + ARS run a Devil's-Advocate gate
   at three checkpoints, not once.

6. **Defect-removal (AI-tells, over-hedging, fabrication) is a floor everyone has** — but the good repos pair it
   with the positive structure above. Ours currently has *only* the floor.

---

## The complementarity (the key reframe)

The canon I found and the repos operate at **different scales and are additive:**

| Scale | The canon (papers/books) | The repos (tooling) |
|---|---|---|
| Sentence | topic/stress position, old-to-new, subject→verb (Gopen-Swan, Williams) | **mostly silent** |
| Paragraph | one-point, point-sentence, given-new chain (Williams) | AXES (academic-writing-skills); "one message per paragraph" (evoskills) — partial |
| Section | CARS moves, C-C-C (Swales, Mensh-Kording) | funnel templates, per-venue intro structures (k-dense, evoskills, academic-writing-skills) — **strong** |
| Paper | OCAR narrative, hourglass (Schimel) | story-design, figure-first, non-linear order — **strong** |
| Claim | (implicit) | **Claim Intent Manifest, claim-evidence contract, epistemic-status tags — strongest in the repos** |
| Reader/value | value-to-reader (McEnerney) | optimization-function, reviewer-expectations, soundness×contribution — **strong** |

The repos are strong exactly where the canon is silent (macro structure, claim grounding, venue register,
reviewer psychology) and silent exactly where the canon is strong (micro sentence-level information flow). **A
`/write` that combined both scales as positive models, with the defect-linter demoted to a floor, would cover the
whole ladder from message down to sentence.**

---

## The juice — ranked catalog of transferable mechanisms

Grouped by what problem they solve. Each tagged with its source. The ★ ones most directly attack Erfan's trust
problem (can't trust the prose without reading every line).

### A. Claim-grounding / trust (the direct answer to "I can't trust what you wrote")
- ★ **Claim Intent Manifest** (imbad0202/deep-research). Before any claim-bearing prose, emit a structured list of
  every claim you intend to make + planned evidence + "must not" constraints. A downstream auditor diffs
  intended∩emitted∩supported and flags `EMITTED_NOT_INTENDED` (drift). Catches claims that crept in *during*
  drafting — which a final-product check misses.
- ★ **Claim-evidence contract + strength ladder** (bahayonghang). Every result sentence is auditable against
  unsupported / observed / supported / strong; a separate over-claim guard sets the wording from the strength.
  "Strong evidence earns strong wording; weak evidence must use weak wording." Sharper vocabulary for our D011 hook.
- ★ **Epistemic-status tags** (imbad0202). Five tiers (Established / Supported / Preliminary / Speculative /
  Contested) with prescribed hedge language per tier. Makes "used Established language for a Preliminary finding"
  a detectable defect.
- ★ **Claim-to-experiment mapping table** (evoskills). Every claimed contribution → ≥1 table/figure ID + ≥1
  ablation row, filled *before* prose. A "no" = a `\gap`. Also predetermines the Results structure.
- **Knowledge Isolation** (imbad0202). The writer may not supplement from parametric memory; unknowns become
  explicit `[MATERIAL GAP]` markers. (We have the spirit in D011; the marker discipline is cleaner.)
- **Temporal-Integrity rule** (imbad0202). Relative time words ("currently", "recently", "best known") must
  anchor to a date/version or be cut. "Temporal claims are arithmetic, not stylistic."
- **SCIENTIFIC_CHANGELOG + comparability report + verified/partial/blocked lattice** (RigorPilot). A dedicated
  artifact tracking what changed in *scientific meaning* and whether a result is comparable to its anchor; a
  4-state epistemic label per result (tighter than our done/gap binary).

### B. Macro structure / process (turn evidence into a paper)
- ★ **Reverse-then-forward story design** (evoskills). Phase 1: reverse-engineer the story from recorded results
  (problem ← contributions ← evidence). Phase 2: write forward. Guards against a story the numbers don't support.
- **Figure-first, abstract-last ordering** (evoskills + k-dense). Draw/lock the key figure before the prose that
  describes it; write the abstract only after the result story is settled.
- **Module-motivation table** (evoskills). Per contribution: What | Why needed | Technical advantage — one table
  that generates the intro contributions paragraph, the method subsection structure, AND the ablation design.
- **CARS funnel templates per venue** (k-dense, academic-writing-skills, evoskills). Concrete intro skeletons
  (ML: problem→limitations→approach→contribution bullets; Nature: big-picture→known→gap→"here we present").
- **Literature rewrite chain** (bahayonghang): Consensus → Disagreement → Limitations → Gap → This-Paper. Earns
  the gap claim instead of asserting it.
- **Insight sentence in the abstract** (evoskills): Challenge → **Insight** → Contribution. The one-sentence
  mechanistic bridge most abstracts omit.

### C. Micro craft / voice (the residual taste, made checkable)
- ★ **Structural AI-tell detox** (jamditis/ai-writing-detox). Goes beyond banned words into *patterns*: tricolon
  abuse (reflexive 3-item lists), em-dash joining two independent clauses (AI paste signal), "The reality is…/
  The truth is…" authority-grab openers, passive-voice-hiding-agency ("it was determined" — by whom?). These pass
  a lexical linter but are real tells — exactly the `prose-register-auditor`'s territory.
- ★ **Verbal-tic read-aloud test** (jamditis). Read it aloud; does it sound like a TED-talk intro / LinkedIn post
  / press release? Name the wrong register. Pass condition: "how you'd explain it to a colleague."
- **AXES paragraph model** (bahayonghang): Assertion → eXample → Explanation → Significance — a checkable
  paragraph skeleton.
- **Mechanism-before-metrics** (evoskills): state challenge → mechanism → design → *then* the number. Default
  authoring instinct is to lead with the number.
- **Four-question deletion gate** (jamditis): can I delete this without losing meaning? simplest form? would I say
  it to a colleague? does it add info or just sound impressive?
- **Coarse-to-fine revision order, enforced** (bahayonghang): logic → sentence → lexical, never reversed
  (polishing a sentence you later delete is wasted).
- **Four-level editing as distinct passes** (awesome-llm-apps/editor): developmental → line → copy → proof, not
  one undifferentiated "make it better."

### D. Review / anticipation (catch holes before the reader does)
- **Reviewer-psychology issue ranking** (bahayonghang): prioritize by what a reviewer will catch and sink you on
  (#1 numbers≠claims, #2 undisclosed params, #3 weak citation support, #4 over-claim, #5 story doesn't close).
- **Devil's-Advocate at three checkpoints** (imbad0202/ARS) with an anti-sycophancy concession protocol (log every
  concession; never concede to emotional pushback). — close to our thinking-panel discipline.
- **Soundness × contribution dual axis** (k-dense/ScholarEval). Two separate questions per result.
- **What-if Contrarian + Second-Order branches** (k-dense/what-if-oracle) as a pre-submission self-stress-test:
  "what if the framing we challenge is right and our result is the artifact?"
- **Reviewer-expectations per venue** (k-dense): ML weights ablations; medical weights evidence grading — tells
  you where to spend space.

### E. Idea front-end (convert idea/experiment → defensible contribution)
- **Optimization-function framing** (life-sciences): declare basic-science vs technology vs invention before
  writing. Directly relevant — our thesis blends a basic-science finding (the linear map) with a technology claim
  (alignment-guided distillation), and they need different evaluation frames named.
- **Competing-hypotheses structure** (k-dense/hypothesis-generation): 3-5 mechanistically distinct hypotheses,
  each with evidence/assumptions — a template for a defensible Discussion (matches our multiple-hypotheses spine).
- **Claim-type classification before critique** (k-dense): causal vs associational vs descriptive, before
  evaluating support — guards the most common over-reach (causal language from correlational data).
- **Innovation taxonomy** (research-grants): Conceptual / Methodological / Integrative / Translational / Scale —
  name the contribution type precisely instead of "novel".
- **"I can't imagine" gap test** + problem statement "general enough to be interesting, specific enough to be
  distinctive" (life-sciences).
- **ELO tournament for idea selection** (evoskills): pairwise Swiss-system ranking on Novelty/Feasibility/
  Relevance/Clarity — for when there are many candidate directions.

---

## What's notably ABSENT everywhere (gaps even the best leave)

- **Sentence-level reader-expectation** (topic/stress, old-to-new) — essentially nobody operationalizes it. This
  is the one place our redesign would have to bring the canon itself, not borrow from a repo.
- **A unified positive model.** Even evoskills and academic-writing-skills are collections of strong tactics, not
  one coherent theory of "what good writing is." The canon (especially Williams + Mensh-Kording) supplies the
  theory the tactics lack.
- **Reader-value at the sentence level** (McEnerney). The repos do value-to-reader at the abstract/intro scale
  (significance, optimization function) but not as a per-sentence discipline.

---

## Implications for our `/write` (proposal — NOT decided; for digestion)

The audit confirms the S33 diagnosis and points to a concrete rebuild. Stated as a hypothesis to test, not a plan:

- **The trust problem has a known solution in the ecosystem: claim-grounding machinery (group A).** A
  Claim-Intent-Manifest + claim-evidence-contract loop, extended from numbers (our D011) to qualitative claims,
  is what lets Erfan stop reading every line — because every claim is pre-committed and audited against recorded
  evidence, and its *wording* is bounded by its evidence strength.
- **The engine should be structure + claim-grounding (macro, from the repos) on top of reader-expectation (micro,
  from the canon), with the defect-linter demoted to a floor.** This is the "notion of health" the S33 session
  found missing — and now we have ~20 concrete mechanisms to build it from instead of inventing it.
- **Erfan's gate moves to the structure + claim-manifest** (cheap, high-leverage), not the prose lines.

## Suggested digestion order (one step at a time, per Erfan's ask)

1. **Claim-grounding (group A)** — the trust spine; closest to our D011; highest leverage. Start here.
2. **Macro structure/process (group B)** — reverse-then-forward, figure-first, claim-to-experiment, CARS funnel.
3. **Micro craft + voice (group C)** — fold the canon (Gopen-Swan/Williams) + the structural detox into the
   `prose-register-auditor` / taste-reader.
4. **Review/anticipation (group D)** — reviewer-psychology ranking, dual-axis, contrarian self-test.
5. **Idea front-end (group E)** — optimization-function framing for the thesis contribution; lower urgency.

Source detail for every claim above lives in the sub-agent findings (this session's transcript) and in the named
repo files under `data/reference-repos/`.
