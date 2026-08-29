---
title: "Deferred submission review items"
tags: [manuscript, submission, deferred]
---

# Deferred submission review items

This working checklist records submission-review items that cannot yet be acted on.
It is not an alternate project status board; [`../../status.md`](../../status.md) remains authoritative for project operations.
Resolve items here only after the stated blocker is cleared, then synchronize any resulting change with the canonical rewrite and the relevant project authorities.

## 1. Confirm whether the registered thesis title may change

**State:** Deferred — authorization is unknown.

**Current registered title:** *Brain Alignment as a Signal for Language Models: From Measurement to Application*

**Candidate identified during review:** *Evaluating Brain Alignment as a Training Signal for Language Models*

**Why deferred:** It is not yet known whether the thesis title can be changed at this submission stage.
Do not change the title in either manuscript until Erfan confirms the administrative or supervisor requirement.

**To resolve:**

1. Ask the supervisors or the relevant UC3M program contact whether the registered title may still be changed.
2. If permitted, Erfan approves the final replacement title.
3. Record a new decision without rewriting the historical title decision.
4. Synchronize the approved title across the canonical rewrite, submission cover/body, and project status.

## 2. Abstract jargon pass (professor's #1 writing complaint; scheduled last)

**State:** Deferred — scheduled last in the 2026-08-27 section-by-section review (all body sections and appendices first).

The UC3M supervisor's top writing remark targeted the abstract: terms a reader cannot yet grasp at that point.
The abstract has already been de-jargonized once; the surviving spots as of 2026-08-27:

- "The regional and naturalistic assays supported controlled brain predictivity" — names the defined term with no in-abstract gloss (the sentence above describes the same construct in plain words; decide whether to keep the name with a micro-gloss or paraphrase).
- "the projected target did not meet the continuation rule inherited from the earlier design" — "continuation rule" and "the earlier design" are both unexplained at that point.
- Check "frozen row-twin control", "cold-start GPT-2 teacher--student gap", and "warm GPT-2 / Qwen" on a first-time reader; "row-twin" is a fixed contract term defined only in §3.
- Also check the abstract's passive/agent constructions against the same professor's earlier feedback.

**To resolve:** after all other sections are reviewed, apply the same readability standard to `main-submission.tex` (abstract block), then synchronize the canonical rewrite abstract (same sentences in `../rewrite/main-rewrite.tex`), and rebuild both PDFs.

## 3. Figure and typography pass on the rendered PDF

**State:** Deferred — judge on the rendered PDF after content passes, per supervisor lesson 4.

Professor remarks not yet verified or applied:

- Figure 2: "the font in the bottom block looks small" — locate the exact block and bump legibility.
- Table titles: make captions visually distinct (bold/small caps per good typography) — optional suggestion, professor said "feel free to keep them as they are"; decide once for all tables.
- Watch appendix F tables: the source checker's build showed ~9.7 pt overfull hboxes there (converged build reported 0; confirm on the final PDF).
- Confirm on the new PDF that the Figure 1 arrow redesign, Figure 10b count/width fixes, and Figure 6-level clarity hold.

Checked 2026-08-27, no action needed: the §2 evidence-chain figure's node labels use the manuscript's fixed role terms and every coinage (route-specific headroom, target uptake, retained-student movement, biological transfer, declared linear pathway, frozen row-twin control) is glossed in the surrounding §2/§3 prose.

## 4. Repo-wide term unifications (surface during section passes)

**State:** Deferred — settle once, globally; do not fix per-subsection.

Flagged independently by both section-2 judges (2026-08-27):

- "50-component linear target-projection **measurability** assay" (full contract form) vs "50-component linear target-projection assay" (short form) — **Resolved 2026-08-28** by policy: full contract form is reserved for the abstract and the §2 definition (professor's first-mention rule); the operative form in §3 onward is the short form "target-projection assay" (Table 1's compact form), and "the naturalistic assay" is the declared short form for the LeBel assay after its §3.1 full name. Applied in §3 (03:67 endpoint sentence, 03:93, rewrite 03:89 brought into lockstep). Remaining full-form sites (rewrite abstract, §7, figure nodes) normalize in their own passes.
- "brain-response-**specific** attribution" (prose) vs "brain-response-**content** attribution" (figure node, abstract) — a visible same-page mismatch in §2.
- "brain-specific benefit" survives at `06_limitations.tex:31` — unify to "brain-specific training advantage" when §6 is reviewed.
- "auxiliary-target family" — **Resolved 2026-08-28** (GPT-5.6 Sol, repo-verified): the recovery rule's Δ_s^rec iterates only over the two aligned target arms (synthetic-response, text-derived auxiliary-control; each vs its seed-matched ordinary \ac{kd} student, per `e025_participant_transfer.py` and E025's predeclared rule). The coinage was deleted; the sentence now names the two arms directly (03:420).
- "scaled synthetic-target family" — **Resolved 2026-08-28** (code/records + GPT-5.6 Sol, consistent): "scaled" = the full-corpus execution; the family comprises all target arms of the synthetic-response route trained on the 95,999-sentence corpus (synthetic, saved block-permutation, text-derived — Appendix C's shared optimization grid). Defined in place at 03:609; line 641's 5% rule remains truthful for all family members (E016's analyzer gated both target labels). Block-permuted arms are inside the family but remain sensitivity checks, not uptake-rule arms.
- Utility-row endpoint naming — **Resolved 2026-08-28**: "held-out language or task endpoint" → "held-out out-of-domain perplexity endpoint" (the only practical endpoint ever executed per E009; robustness-slope and sample-efficiency axes were designed but not run). Applied to Table `tab:evidence-map` in both manuscripts.
- Recorded-response vs permuted-response WikiText quality match — **Resolved 2026-08-28**: no tolerance exists and none is needed; E005's design matches perplexity by construction (matched-ppl-by-construction permuted-twin design). Methods now states the shared scoring implementation and by-construction matching instead of a phantom "declared approximate quality match"; Results 04's no-formal-margin caveat stays consistent.
- NEW (from the same GPT-5.6 Sol pass, for the appendix review): Appendix C's arms table (`tab:synthetic-training-arms`) declares a block-permutation row only for the synthetic target, but E016's runner and records attest a `textfeat_perm` grid as well; check during the appendix pass whether the executed text-derived block-permutation arm must be declared or was only exploratory.
- RESOLVED 2026-08-28 (surgical): Appendix C's `tab:synthetic-training-arms` block-permutation row now declares both executed arms (saved block-permuted synthetic target and saved block-permuted text-derived target, same runner grid, seeds 0--5, per E016's Step-43 textfeat control and E026's audit usage). The row was the only under-declaration; §3.4's plural "block-permuted targets" and Appendix F's defective-sensitivity verdict already covered both.
- Deliberately NOT variants: "under the **studied** assay" (§2.3, refers to the cited aw2023/gao2024 studies' assay, not ours); the submission's section title "Background and Related Work" vs rewrite's "Evidence Required for a Brain-Specific Training Advantage" (deliberate restructure).

## 5. Section 4 review: owner-confirm items (from the 2026-08-29 evidence judge)

**State:** Open — all need Erfan's call; none blocks the current prose. The swarm's evidence judge (kimi-k3, repo-verified) produced these after verifying against E records and `numbers.tex`.

1. **Cold-start gap test naming** — `e003_kd_cold_delta` carries no uncertainty interval or test; E003:112 records bootstrap p(no-drop)=0.000 over the arm's seeds. Add a `numbers.tex` macro (`e003_kd_cold_p`) so §4.2 and the status table can name the test, or keep the bare estimate?
2. **Model-count literals** — "Across 22 decoder-only LMs from six families" (§4.2 prose + figure caption): no macro exists (`e015_capable_n` is n=10, a different count). The literals are verified correct. Add `e015_model_n` / family-count macros, or keep literals for one-off counts?
3. **"quality-aware headroom" standing** — §4.2 now uses it consistently (glossed at first use, this review). Evidence judge asks whether it should unify with the fixed term "route-specific teacher--student headroom", and what standing the modifiers have — a repo-wide naming call.
4. **§4.2 evd anchoring** — the sentence "for which we did not measure route-matched teacher--student headroom" carries only `\evd{E009}`; the status-table row attributes the unmeasured status to E003 and E015. Re-anchor as `\evd{E003}\evd{E015}` for the not-measured clause, or restructure so each clause carries its own record?
5. **One convention for literal counts** — do not patch occurrence by occurrence. Options: words ("nine participants"), `$n=9$`-style macros (`e025_participant_n`, `e030_participant_n` exist), or `$9$`-style macros (`e008_participant_count` exists; `e017_participant_n` and `e030_target_dim` (20,484) do not). Applies to §4.3 "nine participants", §4.4 "20,484-coordinate target", §4.6 "nine direct participant effects", §4.3 "three-participant analysis" (E017), and the status table's "Nine-participant mean". Four accepted edits held for this decision.
6. **Retention-increment verdict register** — §4.5: "the analysis does not establish that synthetic-response training increased its recoverability beyond ordinary KD" reads not-demonstrated, but E030:245 classifies the increment "unresolved" and the status-table row says **Unresolved**. Reword to the unresolved register ("whether ... remains unresolved") or adjudicate "does not establish" as acceptable?
7. **Never-measured components: "unknown" vs "unresolved"** — §4.5's "Initial auxiliary-loss and gradient comparability remain unresolved because those quantities were not retained": E026's narrative says "unknown" (E026:48/132), its mechanical rule says "unresolved" (E026:79). Both record words exist; pick one.
8. **Composed-path row label** — the status-table row says "Not demonstrated" while E030:247 labels the bridge estimands "unresolved"; does the C1-first ordered-failure logic license the manuscript-level "Not demonstrated"?
9. **"frozen row twin" vs "frozen row-twin control"** — canonical form repo-wide after first definition (applies to §3 and §4 together).
10. **"practical-endpoint analysis" descriptor** — §4.6's closing pointer uses it while the subsection is "Practical-utility evaluation"; unify or keep as a generic descriptor?
11. **Unsurfaced exclusion bound** — E025's one-sided 95% upper bound (`e025_participant_ucb`) excludes a mean effect of +0.002 unique-R² for the cohort; add this supported practical exclusion sentence to §4.6, or keep the current scope?

Note: the status-key gap behind item 12 of the evidence judge's list (Inconclusive/Unmeasured key entries) is already resolved by this review (entries added to `tab:results-status` in both manuscripts); remap-vs-key is thereby settled unless Erfan prefers remapping the two cells.

## Related

- [Submission manuscript](main-submission.tex)
- [Canonical rewrite](../rewrite/main-rewrite.tex)
- [Project status](../../status.md)
