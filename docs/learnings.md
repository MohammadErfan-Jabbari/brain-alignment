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

### L007 — 2026-06-10 — A2 holds on real data: trained LMs carry unique language-network signal; untrained do not

The question synthetic fMRI could not answer (L004) is now answered on real neural data (Tuckute 2024, E002). Trained LM mid-layer representations predict LH-language-network BOLD with **positive unique R²** after length/position/static-embedding subtraction under contiguous splits (gpt2 +0.020, gpt2-medium +0.019, Qwen2.5-0.5B +0.036), while same-architecture **untrained** networks score **negative** across 3 seeds. The trained−untrained gap (+0.030 to +0.050) is the honest signal; NC-normalised it is 5–10% of a 0.35 ceiling. Three durable points: (1) the anti-confound harness discriminates correctly on real data, not just synthetic — it neither rubber-stamps nor erases. (2) Model quality tracks alignment (Qwen > GPT-2), the expected ordering. (3) Absolute ROI-level R² is small *by design*; always report it NC-normalised and against the untrained control, never raw. This is an A2 pass, not an A3 or distillation claim — the ladder (R03 §5) climbs one rung.

### L008 — 2026-06-10 — The inversion idea ("use fMRI to train an LM") is already published, text LMs included

Erfan's overnight idea — invert alignment from measurement to training signal — is real but **largely scooped** as of 2025–26: brain-tuning for speech (Moussa/Toneva ICLR'25, NeurIPS'25) and **for text LMs** (Bilgin/Wehbe ICLR'26, GPT-2 + LLaMA-2), plus causal proof alignment is load-bearing at matched perplexity (Merlin/Toneva ICLR'26). The unscooped slice is narrow and specific: brain alignment as the objective **in distillation/compression at matched student budget**, framed as a *trade-off curve* (because post-hoc compression already preserves alignment — arXiv 2602.07547). Lesson: before committing to a "novel inversion," run the focused prior-art sweep first — the bare idea was three published papers deep. The first-principles info-budget argument (brain = weak regularizer, R03 §2) is what locates the genuinely open corner. Captured in R03.

### L009 — 2026-06-10 — Oota 2023's dataset is the Narratives "21st year" *listening* set, not Harry Potter; verify dataset identity against the repo, not memory

The canonical note for Oota 2023 (`oota-2023_joint-linguistic-processing-brain-lms`) recorded the fMRI dataset as "Harry Potter," and R01 + the R01-explained companion both inherited that. It is wrong. The authors' own repo (`data/paper-repos/linguistic-properties-brain-alignment`) and the arXiv abstract ("participants listened to a story") both confirm the dataset is the **Narratives "21st year" listening** set — 18 subjects, 8,267 words, 2,226 TRs at TR=1.5s. Harry Potter (Wehbe) is a *reading* dataset; conflating the two also mislabels the modality (reading vs listening), which matters because modality changes what the alignment captures (cf. Oota 2024, L003). Lesson: a dataset name in a canonical note is a *claim* — verify it against the paper's repo/README or the abstract before it propagates into reports. Caught only because a downstream understanding-chat instinct ("they listened to the story") contradicted the note. Fixed in the canonical note, R01 G5, and the explainer G5.

### L010 — 2026-06-10 — Recon before extraction: the best preprocessing was to run none

A request framed as "preprocess these PDFs (run the pdf/OCR skill?) and incorporate them" turned out, on inspection, to need *no* extraction at all. The course material already carried Erfan's own `*_study.md` (teaching notes) and `*_OCR.md` (audited formula reconstructions), which are strictly higher quality than a fresh OCR of the sparse, image-heavy slide decks (≈700–1100 chars over 3 pages). Running the obvious tool would have *destroyed* value and burned compute. The move that paid off: spend three cheap recon subagents (2× Sonnet to map concepts→thesis, 1× Haiku to catalog assets) to characterize the material *before* choosing a tool — which reframed the task from "extraction" to "curation + integration." Lesson: when handed material plus a default tool ("run the pdf skill"), first check whether better artifacts already exist; the recon is cheaper than the wasted extraction, and the reframe is often the whole job. (Decision D014; the curation lives in `06-theory-grounding.md`.)

<!-- Add new lessons below as we hit them. Negative results count. -->
