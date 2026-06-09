# Learnings — the anti-amnesia file

Hard-won lessons, corrected mistakes, and dead ends worth remembering. The rule (from Nexus):
*"If the system does not remember the lesson, the same pain will return disguised as a new problem."*

Each entry: date, the lesson, and the evidence/why. Newest at the bottom.

---

### L001 — 2026-06-08 — Inherit the thinking from Nexus, not the machinery

Nexus failed twice in opposite directions: v1 over-specified (constitutional sprawl), v2 over-coupled
(a stage-machine demanding constant cross-surface synchronization). The durable lesson is *adaptive
semistructure* — add structure only when its absence costs truth. Applied here: no stage gates, no
dual-surface mirror; a plain `docs/` brain instead.

### L002 — 2026-06-08 — Brain-alignment is literature-strong but execution-light, and held a HOLD

The prior oracle review returned **HOLD, not PASS**: excellent Stage-2 reasoning, but zero
operational specificity (no named benchmark + power analysis, no concrete $\mathcal{L}_{\text{brain}}$,
no compute budget, no pilot, no deployment scenario). The fix is not more reading — it is a toy-scale
pilot. Don't repeat the literature loop; build the pipeline.

### L003 — 2026-06-08 — The dominant risk is measurement, not modeling

Two counter-evidence papers (Feghhi 2024, Oota 2024) show brain-alignment scores are easy to inflate
(split leakage, nuisance features, low-level confounds). Any result that doesn't survive contiguous
splits + nuisance subtraction is not a result. Bake the anti-confound protocol in from day one, not
at review time.

### L004 — 2026-06-09 — Synthetic fMRI tests the plumbing, never the science; and the nuisance must be capacity-matched

Two lessons from building E001. (1) A synthetic stand-in built as a linear map of *teacher* features
cannot test whether brain alignment is preservable under distillation: plain KD already pulls the
student toward the teacher, so it is near-optimal for that synthetic target and any extra brain loss
can only distract (we saw a small, monotonic-in-λ *negative* Δ). Synthetic validates the pipeline and
the anti-confound machinery — that they run and don't rubber-stamp a positive — and nothing more. The
real verdict needs neural data whose structure is not trivially teacher-derived (LeBel ds003020).
(2) In a variance partition, the nuisance block and the contextual block must get **equal capacity**:
a raw 768-dim static-embedding nuisance silently absorbed the signal and drove unique_r2 to ≈0 until
both blocks were PCA-reduced to the same rank per fold. An unfair partition can manufacture *or* erase
an effect — match the dimensionality.

### L005 — 2026-06-09 — Pereira's OSF node (crwz7) is stimuli-only; "open benchmark" ≠ "neural data in hand"

The SPOF survey cleared the data-access risk (LeBel/Narratives/Pereira all open, no-login), but the
Pereira OSF bundle `Pereira_Materials.zip` turned out to contain only sentences + GloVe + ROI masks,
**not** the per-subject voxel responses (those live on a separate host). Verify what a download
actually contains before treating a benchmark as "ready" — an open license and a 276 MB zip are not
the same as having the fMRI matrix. This is why E001 ran on the hybrid path, not real responses.

### L006 — 2026-06-09 — Cited "datasets" in the alignment literature routinely fail basic in-scope checks; verify before assuming anything

Three related sub-lessons from building the dataset registry:

(1) Two datasets cited in alignment papers turned out not to be usable neural data on inspection: zhu-2025 is monkey motor / mouse visual cortex data (non-language, out of scope), and yin-2025 "Association" is a synthetic GPT-4 NLP fine-tuning set whose neural ground truth is just Narratives — not a new neural dataset at all. Do not assume a dataset cited in an alignment paper is (a) in scope, (b) a real neural dataset, or (c) not already covered by a benchmark you have. Check modality and source first.

(2) Packaged benchmarks (neural-nlp/brain-score) routinely differ from original papers on subject count. Multiple registries showed n_packaged < n_paper. Always record which subset a number refers to and note the discrepancy; a brain-score leaderboard number may not reflect full-cohort power.

(3) License is often NOT STATED for OSF-hosted data (Fedorenko, Blank, Tuckute, Le Petit Prince all had no explicit license on their OSF nodes). "Open" access does not mean "known license." Treat license as unverified until the actual data files are inspected; record it as NOT STATED, not assumed.

<!-- Add new lessons below as we hit them. Negative results count. -->
