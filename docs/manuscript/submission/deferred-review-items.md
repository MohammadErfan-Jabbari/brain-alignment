---
title: "Deferred submission review items"
tags: [manuscript, submission, deferred]
---

# Deferred submission review items

This working checklist records submission-review items that cannot yet be acted on.
It is not an alternate project status board; [`../../status.md`](../../status.md) remains authoritative for project operations.
Resolve items here only after the stated blocker is cleared, then synchronize any resulting change with the canonical rewrite and the relevant project authorities.

## 1. Confirm whether the registered thesis title may change

**State:** Resolved 2026-08-30 — the professors approved the change and Erfan confirmed it.

**Previous registered title:** *Brain Alignment as a Signal for Language Models: From Measurement to Application*

**Approved title:** *Evaluating Brain Alignment as a Training Signal for Language Models*

**Resolution:** [D066](../../decisions/decisions.md) records the new title without rewriting the historical D064 state. The canonical rewrite, university-template derivative, and project status are synchronized.

## 2. Abstract jargon pass (professor's #1 writing complaint; scheduled last)

**State:** Resolved 2026-09-01.

Both abstracts were replaced with one plain-language text and are now byte-identical, so the canonical tree and the derivative no longer diverge here.

How each flagged item was settled:

- "controlled brain predictivity" is paraphrased, not named: the abstract describes the measurement in plain words and then says both assays supported it. The term keeps its formal definition at its first main-text use in Section 1.
- "the continuation rule inherited from the earlier design" became "did not clear the improvement threshold set beforehand".
- "frozen row-twin control" became "a control that keeps the same target rows but breaks their pairing with the sentences", which is the control's actual construction.
- "50-component linear target-projection measurability assay" became "a 50-component linear projection of the target", introduced as testing one narrow pathway alone.
- "route-specific teacher-student headroom" became "the teacher-student gap available to an intervention".
- "cold-start" and "warm" became "trained from scratch" and "pretrained".
- "target uptake", "retained-student movement" and "brain-response-content attribution" are stated as the three questions they stand for rather than named.
- Passive constructions that lost their agent were made active: we measured, we compared, we did not report.

The abstract also gained a closing sentence naming the contribution, which the derivative had dropped.

## 3. Figure and typography pass on the rendered PDF

**State:** Resolved 2026-09-01, judged on the rendered PDF as supervisor lesson 4 requires.

- **Figure 1.** The canonical tree still carried the version whose context arrow routed over the blocks, which is exactly what the supervisor flagged; the derivative's redesign was adopted canonically. Both trees then received new geometry: equal-sized boxes, wider columns, taller rows. Two dependency arrows had been hidden between touching boxes and are now visible. The one deliberately unconnected box is explained in the caption and in the surrounding prose.
- **Figure 2.** The small-font note block at the bottom was the "bottom block" in the remark. It is removed from the canonical tree and its text now sits in the caption, matching the derivative. The "re-/sponse" break in the top-right node is gone.
- **Figure 10b.** The panel reads its counts from the keyed E026 values, so the figure, Table 22, and Section 4.5 all report 37 checks as 20 passed, 16 failed, 1 unresolved. It is set with `\resizebox{\linewidth}`, so nothing overflows the margin. Verified on the rendered page.
- **Table titles.** Settled once for all tables: captions carry a bold label via `\captionsetup{labelfont=bf}` in `preamble.sty`.
- **One-word paragraph endings.** Twenty in the rendered PDF; none remain in prose or captions. Fixed with `\finalhyphendemerits` so no word is hyphenated into a last line, `\looseness` on six paragraphs, ties on four sentence-final word pairs, and two rewordings. A global `\parfillskip` floor was tried and rejected: it only made final lines loose without re-breaking them.
- **Appendix F overfull hboxes.** The final submission build reports zero overfull hboxes at 67 pages.

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

**State:** All 11 resolved 2026-08-29 by Erfan's decisions, applied to both manuscripts.

1. **Cold-start gap test naming** — RESOLVED: added `\result{e003_kd_cold_nodrop_p}` (bootstrap no-drop p = 0.000 over the cold arm's seeds, E003:112) to numbers.tex; the §4.2 gap sentence now names the test.
2. **Model-count literals** — RESOLVED: added `\result{e015_full_n}` (=22) and rerendered both occurrences (§4.2 prose + caption); "six families" stays a word (single occurrence).
3. **"quality-aware headroom" standing** — RESOLVED: kept as the quality-matched variant of the fixed term "route-specific headroom"; §4.2 glosses it at first use. No rename.
4. **§4.2 evd anchoring** — RESOLVED: anchors split (model pair ← `\evd{E009}`, not-measured clause ← `\evd{E003}\evd{E015}`, matching the status-table row).
5. **One convention for literal counts** — RESOLVED: words in prose, macros only where a count feeds a formula. The four parked macro-conversion edits (§4.3 "nine participants", §4.3 "three-participant", §4.6 "nine direct participant effects", §4.4 "20,484-coordinate target") are rejected under this convention; the text stays as words.
6. **Retention-increment verdict register** — RESOLVED: §4.5 prose reworded to the unresolved register ("whether synthetic-response training increased its recoverability beyond ordinary KD remains unresolved"), matching E030:245 and the status-table row.
7. **Never-measured components** — RESOLVED: keep "unresolved" (matches E026's rule language and the keyed status). No text change.
8. **Composed-path row label** — RESOLVED: status-table row changed to **Unresolved** (E030:247 is explicit that the bridge quantities are unresolved and cannot generate a downstream ordered-failure label); the §4.6 prose moved to the same register ("leaves ... unresolved under participant inference"), and Appendix A's evidence-provenance row was aligned ("remain unresolved across participants").
9. **"frozen row twin" convention** — RESOLVED: full contract form "frozen row-twin control" at first use; the bare "frozen row twin" is allowed afterward (same pattern as the assay short forms). No text change.
10. **"practical-endpoint analysis" descriptor** — RESOLVED: unified to "practical-utility evaluation" (the subsection's name) in §4.6's closing pointer.
11. **Exclusion bound in §4.6** — RESOLVED: added the verified sentence "The one-sided 95\% participant upper bound \result{e025_participant_ucb} lies below the internal continuation threshold \result{e030_practical_threshold}, so a participant-mean effect of at least that size is excluded."

## 6. Discussion-through-conclusion argument-review hold

**State:** RESOLVED before the Section-5 prose swarm — 2026-08-30.

The fresh GPT-5.6 scientific-scope review identified argument and evidence-scope defects rather than prose-polish suggestions. All were corrected in the canonical rewrite and then synchronized to the submission derivative. No recorded scientific verdict or number changed.

Resolved repairs:

1. **ARG-5-1 — participant-general estimator wording:** narrow the universal claim that effects must always be calculated separately per participant. The requirement is participant-supported population inference; dependence-aware hierarchical estimators are not ruled out by E008/E025.
2. **ARG-5-2 — placement of unmeasured Qwen headroom:** restructure the sentence so missing opportunity context is not presented as the point where the recorded intervention loses support. The identifying paired intervention contrast is the failed support transition.
3. **ARG-6-1 — inference-unit collapse:** narrow the statement that folds, stories, voxels, and seeds must all be aggregated within participants. Section 3 also defines fixed-stimulus inference tracks; preserve the biological/fixed-stimulus/technical distinction.
4. **ARG-6-2 — MDE versus continuation thresholds:** separate E008's sensitivity MDE from E025/E030 threshold-based exclusions; do not imply that E008 established practical-effect exclusion under a continuation criterion it did not use.
5. **ARG-7-1 — endpoint closure:** make the Conclusion land explicitly on the settled overall endpoint, `inconclusive`, while distinguishing that endpoint from the supported controlled-measurement and staged-evidence-framework contribution.
6. **ARG-7-2 — dependency-graph wording:** narrow “ordered set of separately supported steps” so it cannot be read as a universal linear gate; preserve route-specific dependencies and independently interpretable endpoints.

Nonblocking Section-6 clarification:

- **ARG-6-3 — variant scope:** state that the naturalistic and full-parameter variants were mechanism or three-participant existence probes and do not broaden participant-general inference (E013/E017).

**Resolution:** The six blocking repairs and ARG-6-3 were applied under [D067](../../decisions/decisions.md): they improve scope accuracy and reader understanding while preserving the settled scientific meaning. The Section-5 prose swarm is unblocked.

## Related

- [Submission manuscript](main-submission.tex)
- [Canonical rewrite](../rewrite/main-rewrite.tex)
- [Project status](../../status.md)
