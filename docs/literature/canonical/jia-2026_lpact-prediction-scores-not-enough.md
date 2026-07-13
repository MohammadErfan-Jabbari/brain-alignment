---
title: "Do Language Models Align with Brains? Prediction Scores Are Not Enough"
tags: [literature]
aliases: [jia-2026_lpact-prediction-scores-not-enough]
---

# Do Language Models Align with Brains? Prediction Scores Are Not Enough

**Authors:** Xiao Jia (single author)
**Year:** 2026
**Venue:** arXiv preprint (q-bio.NC — Neurons and Cognition); submitted 13 May 2026
**DOI/arXiv:** arXiv:2605.14025 (v1)
**Canonical ID:** jia-2026_lpact-prediction-scores-not-enough

**Tags:** #literature #canonical #novelty-threat #anti-confound

---

## Read Method [REQUIRED]

- [ ] Full PDF read (page-by-page comprehension)
- [x] Full PDF scanned (search + targeted read)
- [ ] Extracted text only

Verified: 2026-06-14 — read via the arXiv HTML rendering (`arxiv.org/html/2605.14025v1`), targeted
across the method (L-PACT gates, control taxonomy in Table S4), the dataset/source-audit section, the
results (146 integrated decision rows), and the limitations/future-work section. The PDF itself was
not rendered page-by-page; all numbers below are quoted from the HTML body and supplementary tables as
surfaced. **Parse note:** the arXiv ID is future-dated (2605 = May 2026); fetch succeeded against the
HTML endpoint, abstract listing, and v1 HTML. No quantitative figure was reproduced from a binary PDF
read, so treat per-row sub-scores as HTML-sourced rather than figure-verified.

Comprehension self-check passed: Y (the framework logic and the headline are unambiguous; what is
*absent* from the paper is as load-bearing for us as what is present, and the absences were confirmed
by direct negative queries).

---

## Comprehension Summary [REQUIRED]

1. **Problem solved:** Brain-alignment claims for LMs rest on linear neural *prediction scores*, which
   the author argues are insufficient — a high encoding R² can be manufactured by temporal
   autocorrelation, dimensionality, and other nuisances. The paper builds an audited decision pipeline
   (L-PACT) and asks whether *any* real LM row clears a conjunction of four evidence gates.

2. **Core insight:** Across 146 integrated decision rows spanning six LMs and three primary
   intracranial/MEG datasets, **not one real-model row passes all four gates** — "All 146 rows are
   classified as control_explained." Apparent alignment positives are reclassified into an
   "auditable control-explained taxonomy." Positive controls (brain-as-model profiles; a synthetic
   implanted signal) *do* pass, so the assay is sensitive — the negative is not a dead pipeline.

3. **If-wrong breakage:** The verdict is bounded to "the locked model-feature stores and controls
   tested here, not to the full space of contemporary or future language models." The gates are
   conjunctive and qualitatively thresholded ("the best severe control" rather than a numeric cutoff),
   so a different control set, a different aggregation, or a larger/instruction-tuned model could in
   principle flip individual rows.

---

## Source Grounding

**Models (frozen, no fine-tuning):** DistilGPT-2, GPT-2, GPT-2 Medium, Pythia-160M,
Qwen2.5-1.5B-Instruct, Qwen3-1.7B. All analyzed as **frozen feature stores** — "the analysis uses
frozen language-model feature stores already present in the locked analysis set; no new model
extraction was performed for this manuscript." Readout is **ridge-regularized linear encoding within
blocked cross-validation**; lag, ridge penalty, and PCA dimensionality are fit "only inside training
data."

**Primary datasets (source-audited as evidence-complete):**

| Dataset | Modality | Subjects | Subject-run units | Brain units |
|---|---|---|---|---|
| Brain Treebank | intracranial (sEEG) | 10 | 26 | 248 |
| Podcast ECoG | ECoG | 9 | 9 | 235 |
| MEG-MASC | MEG | 11 | 84 | 257 |

**Secondary:** Narratives, LPP multilingual. **Excluded:** NaturalStories (stimulus-only — no complete
neural artifact chain). Note: this is an **intracranial/MEG-heavy** corpus — no Pereira/LeBel-style
naturalistic fMRI in the primary set, which is exactly the regime our thesis runs in.

**"Source-audited" = a closure test run *before* any evidence is interpreted.** A dataset is admitted
to primary neural evidence only if its artifact chain has: brain time series, word/event grids, model
features, severe controls, reliability estimates, and minimum coverage thresholds. "A dataset can have
useful stimulus or model features while still being unsuitable for primary neural evidence if the
artifact chain lacks matchable neural time series, word events, controls, or brain-brain reliability
structure." This is a methodological contribution in itself: gate the *dataset* before gating the
*model*.

**Row accounting (the "414+" the abstract cites):**

- Predictive rows: **414** decision-ready (from 9,036 raw)
- Relational rows: 2,304 delta rows (from 20,736 raw)
- Mechanism-stripping rows: 4,320 delta rows
- Brain-brain ceiling rows: 420 total, **108 valid** (all 108 exceed the configured minimum
  reliability of **0.1**)
- **Integrated decision rows: 146 — all control_explained, zero passes.**

---

## Key Ideas — the L-PACT four-gate hierarchy

L-PACT = **L**anguage **P**rediction **A**lignment **C**ontrol **T**axonomy: a *conjunctive* decision
rule. "A row cannot compensate for an unmet mechanism-stripping or reliability gate by having a larger
local predictive score." All gates must pass (product form).

**Gate 1 — Predictive adequacy.** "The real model score must exceed nuisance baselines and the best
severe control, with finite held-out scores, sufficient train/test samples, and subject-run
aggregation." I.e. beating an intercept is not enough; the model must beat the *strongest* nuisance
control simultaneously.

**Gate 2 — Relational adequacy.** "The model-to-brain profile must exceed the best control profile,
use the same brain-unit ordering as the brain profile, and satisfy brain-pattern reliability
constraints." Tests cross-unit *organization* (RSA / centered-kernel-alignment / Pearson / cosine
profile similarity), not local per-unit score — a representational-geometry gate.

**Gate 3 — Mechanism-stripping adequacy.** "Mechanism stripping must produce a positive and selective
matching deficit within the implemented predictor. The matching drop must exceed nonmatching drops,
survive controls, and not be reducible to generic feature degradation." The stripped mechanisms are
**surprisal, semantic transition, dependency integration, syntactic boundary, discourse boundary, and
context update**. For each stripped mechanism × neural-target mechanism, the held-out score drop is
measured; specificity requires Δ_strip(matching) > Δ_strip(nonmatching). This is a *necessity* /
causal-attribution gate at the level of linguistic mechanisms.

**Gate 4 — Reliability-bounded adequacy.** "Surviving model evidence must reach the configured fraction
of a valid brain-brain reliability estimate. Invalid or missing ceiling estimates cannot be silently
ignored." Model evidence is normalized to a brain-brain ceiling:
$F_\Delta(r) = \Delta_{\text{model}-\text{control}}(r) / R_{BB}(d,m)$. Ceilings come from split-half,
run-to-run, subject-to-subject, and session-to-session reliability "where the derived artifacts
support those comparisons."

**How it reclassifies existing results:** every apparent positive that previously rested on a raw
prediction score is mapped to *which gate it fails* — a control-explained taxonomy rather than a
binary "no alignment." The framing is "prediction scores are not enough," not "LMs are unrelated to
brains."

---

## Evidence — the controls, listed precisely

The "severe controls" (Table S4 — these are the answer to "exactly which controls"):

1. **`random_matched_dim`** — random features matched on dimensionality (tests whether dimensionality
   alone produces the score).
2. **`random_matched_autocorr`** — random features matched on **temporal autocorrelation** (the
   Hadidi/Feghhi OASM analogue — tests whether autocorrelation produces nonspecific structure).
3. **`circular_shift`** — circular time-shift of features (temporal-misalignment control).
4. **`sentence_reset_fresh`** — sentence-local context reset (removes cross-sentence context).
5. **`reversed_context_fresh`** — reversed-context features.
6. **`layer_label_permutation`** — permute layer identity (tests whether the layer-depth profile is
   real, the Gate-2 organization analogue).
7. **`token_order_shuffle`** — shuffle token order (token-order specificity).
8. **`within_story_block_shuffle`** — block-level shuffle *within* a story (the contiguous-split-style
   control against within-block autocorrelation leakage).
9. **`mechanism_mismatch_control`** — mechanism-specificity control for Gate 3.

**Brain-brain reliability / ceiling:** split-half, run-to-run, subject-to-subject, session-to-session;
108 valid rows, all above the 0.1 minimum.

**Positive controls (assay-sensitivity, the part that makes the null credible):**
- **Brain-as-model relational profiles** — "Brain Treebank run-to-run profiles pass this L-PACT-like
  relational gate in all 9 alignment-by-profile metric summaries." A real brain predicting another
  real brain *does* clear Gate 2.
- **Synthetic implanted signal** — "A deterministic latent mechanism was implanted into synthetic
  neural targets and matched synthetic model features." It **passes all four gates**: predictive
  0.9867, relational 0.8985, mechanism-stripping delta 0.2659, fraction-of-ceiling 0.9911. This is the
  proof the pipeline *can* return a positive — so the all-146-fail result is a property of real LM↔brain
  data, not a broken gate.
- Low-level neural gates (word-onset, word-rate detection) and standalone acoustic-envelope readouts
  (where WAV available) — sanity that the neural side carries decodable structure.

**Headline:** "All 146 rows are classified as control_explained." "No row passes the predictive,
relational, mechanism-stripping, or reliability-bounded gate."

---

## Limitations

1. **Bounded negative.** Explicit: "The negative result applies to the locked model-feature stores and
   controls tested here, not to the full space of contemporary or future language models." Future work
   is to "test larger, instruction-tuned, and more diverse language models, prospective neural
   datasets, richer language-event annotations, and repeated subject-run designs."

2. **No naturalistic fMRI in the primary set.** Primary evidence is sEEG / ECoG / MEG (Brain Treebank,
   Podcast ECoG, MEG-MASC). The fMRI BOLD regime our thesis runs in (Pereira, LeBel) is not where the
   verdict was produced; NaturalStories was *excluded* for lacking a complete chain. Whether the all-fail
   verdict transfers to high-autocorrelation BOLD is untested here.

3. **Qualitative thresholds.** Gates compare against "the best severe control" rather than a fixed
   numeric cutoff; "No explicit numeric thresholds for predictive gates are stated." The conjunctive
   rule is strict, but the per-gate bar is data-relative, so a different control library could move
   individual verdicts.

4. **Frozen-feature only.** No fine-tuning, no brain-tuning, no training-on-brain anywhere in the paper
   (see Relevance). The framework evaluates *whether frozen LM features already encode brain structure*,
   not whether a *training intervention* on brain data does something causal.

5. **Per-individual statistical power not formalized.** The pipeline tracks subject-run units and
   requires "subject-run aggregation," but "No explicit statements found regarding ... per-individual
   statistical power limitations." It is an aggregation requirement, not a powered per-subject null with
   a stated MDE.

6. **Averaging-as-confound not raised.** The paper does not argue that group-averaging brain targets
   manufactures apparent specificity (see Relevance #4 — this absence is load-bearing for us).

---

## Relevance to this thesis

**Which assumption it touches:** A2 (brain alignment is real, not a confound artifact). This is the
**strongest single 2026 challenge to A2 to date** — a 146-row, four-gate, all-fail result — and it is a
**direct novelty-threat to scope**, because it is the most complete "prediction scores are not enough"
statement now in the literature.

**The six diagnostic questions, answered:**

1. **Controls (exact):** `random_matched_dim`, `random_matched_autocorr` (autocorr-matched random
   features — our permuted/nuisance analogue), `circular_shift`, `sentence_reset_fresh`,
   `reversed_context_fresh`, `layer_label_permutation`, `token_order_shuffle`,
   `within_story_block_shuffle`, `mechanism_mismatch_control`; plus brain-brain reliability
   (split-half / run-to-run / subject-to-subject / session-to-session, min 0.1). Yes to
   autocorrelation-matched random features, circular shifts, token-order shuffle, within-story block
   shuffle, and brain-to-brain reliability — **all the controls we listed in the question are present.**

2. **Frozen vs. fine-tuning/brain-tuning:** **FROZEN-ONLY.** "No new model extraction was performed";
   "no brain-tuning or fine-tuning on neural data occurs." This is the decisive line for us — L-PACT
   audits *encoding of frozen features*, and says **nothing** about a brain-TUNING intervention. Our
   central critique (brain-tuning gains are an LM-quality/FT-regime artifact) is in a regime L-PACT does
   not enter.

3. **Perplexity / bits-per-byte-matched control:** **NO.** "The paper does not employ perplexity,
   bits-per-byte, or language-modeling-quality-matched baselines." Confirmed. Its controls are temporal /
   structural / dimensionality, not model-capability. Our matched-perplexity control is **not pre-empted.**

4. **Cross-subject averaging confound:** **NO.** It requires "subject-run aggregation" but "does not
   explicitly debate whether group averaging of brain targets inflates apparent alignment"; "no
   detailed discussion of whether group-averaging across subjects artificially inflates specificity."
   Confirmed. Our averaging-confound contribution is **not pre-empted.**

5. **The four-level hierarchy:** Predictive (beat best severe control, not just intercept) →
   Relational (cross-unit profile geometry matches, same brain-unit ordering) → Mechanism-stripping
   (selective necessity: stripping surprisal/syntax/discourse/etc. hurts the matching neural target more
   than nonmatching) → Reliability-bounded (normalized to a valid brain-brain ceiling). Conjunctive:
   a big predictive score cannot rescue a failed mechanism or reliability gate. It classifies existing
   alignment results by *which gate they fail*, converting positives into a control-explained taxonomy.

**6. BOTTOM LINE — does it threaten our novelty?**

**It threatens our *framing*, not our *contribution*.** L-PACT is the new high-water-mark for the
generic claim "raw LM↔brain encoding scores are confound-explained." After this paper, we can **no
longer present that generic claim as novel** — it must be cited as established, and our intro must
position our work *downstream* of it. But all three of our differentiators survive intact:

- **Per-individual powered null — SURVIVES.** L-PACT aggregates subject-run units and explicitly does
  *not* formalize per-individual statistical power or a stated MDE. Our powered per-individual null is
  distinct and complementary.
- **Averaging confound — SURVIVES (clean).** L-PACT does not raise group-averaging as a manufacturer of
  apparent specificity at all. This remains genuinely novel.
- **E[Y|S] training-ceiling (brain-tuning is an FT-regime/LM-quality artifact) — SURVIVES (cleanest).**
  L-PACT is **frozen-encoding only**; it never trains on brain data, so it cannot speak to whether a
  *brain-tuning gradient* adds anything beyond the stimulus-predictable part. Our matched-perplexity +
  permuted-brain critique of the *training intervention* is in a regime L-PACT does not touch. And L-PACT
  uses **no perplexity-matched control** — the exact lever our critique turns on.

**The clean handoff:** L-PACT proves the *measurement* (frozen encoding) is confound-explained on
intracranial/MEG. We prove the *intervention* (brain-tuning a text LM on fMRI) is FT-regime/LM-quality-
explained and aligns only to E[Y|S], with the three controls L-PACT lacks (matched perplexity,
averaging confound, powered per-individual null). Same epistemology, non-overlapping target.

**What our paper must cite / concede to L-PACT:**
- **Cite it as the canonical "prediction-scores-are-not-enough" result** and as prior art for the
  conjunctive-gate / source-audit idea. Do not re-claim the generic encoding-confound point as ours.
- **Concede** that on intracranial/MEG frozen encoding, the confound case is now made at scale (146 rows,
  positive-control-validated) — we inherit it rather than re-litigate it.
- **Borrow** two design moves: (a) the `random_matched_autocorr` severe control as a named complement to
  our OASM/permuted baselines, and (b) the **source-audit closure test** (gate the dataset's artifact
  chain before interpreting any model row) as a checklist for our LeBel/Pereira runs.
- **Differentiate explicitly** on the three axes above — and lean on L-PACT's own scope caveats (frozen-
  only; no fMRI in primary set; no perplexity/capability control; no per-individual power) as the precise
  seams where our contribution lives.

**Counter-evidence vs. anchor:** primarily an **anchor** for the measurement-skeptic half of our story
(strongest available support that raw scores ≠ alignment), and a **scope-fence** that sharpens — not
erases — our brain-TUNING novelty. It is not counter-evidence to our positive results (we run a
different intervention in a different modality with controls it lacks).

---

## Verified

Read 2026-06-14 via arXiv HTML (`arxiv.org/html/2605.14025v1`) — method, Table S4 control list, source-
audit / closure-test section, results (146 integrated rows, all control_explained), positive-control
sub-scores (synthetic implanted: pred 0.9867 / rel 0.8985 / strip 0.2659 / ceiling 0.9911), and
limitations/future-work. Single author (Xiao Jia); submitted 13 May 2026; q-bio.NC. **Parse caveat:** the
binary PDF was not rendered page-by-page; per-row numeric sub-scores are HTML-sourced, not figure-
verified. The four absences load-bearing for our novelty (no fine-tuning/brain-tuning, no perplexity-
matched control, no averaging confound, no powered per-individual null) were each confirmed by direct
negative query against the v1 HTML.


## Related
- [`status.md`](../../status.md) — the canonical status board
