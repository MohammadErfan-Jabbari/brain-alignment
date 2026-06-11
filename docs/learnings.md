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

### L011 — 2026-06-10 — Brain alignment co-varies with LM quality, so any "X sheds/preserves alignment" claim must control perplexity, not just budget

E003 (the perplexity-only-KD kill-test) measured a clean monotone alignment gradient — conventional gpt2 ≈ teacher > warm-KD > distilgpt2 > from-scratch cold-KD ≈ floor — and the preliminary read was "KD sheds alignment, F1 confirmed." An Opus skeptic, tasked to *refute* it, showed the load-bearing causal claim ("sheds alignment *beyond* the perplexity it costs") was not supported: across the trained/distilled models, unique-R² alignment is predicted by log-perplexity at **Pearson r=−0.88**, with the pure-logit-KD point sitting *exactly* on the ppl curve and off-the-shelf gpt2 the lone outlier. The two dissociations that would separate "KD-specific shedding" from "alignment just tracks LM quality" (KD-student < gpt2 at matched ppl; KD < LM-finetune at matched budget) were both only **p≈0.09** — and the from-scratch arm was under-trained (ppl 4.5× the teacher), so its near-floor alignment partly just means "a worse LM." Two lessons. (1) **Alignment is confounded with capability**: you cannot attribute an alignment drop to a training *objective* unless you hold perplexity (or another capability axis) fixed — "matched budget" is not "matched perplexity," and a from-scratch student must be trained to *matched perplexity* before its alignment is a verdict, not a budget artifact. (2) **Run the adversarial refutation on your own positive results, not just on the design** — the pre-run oracle/counter-argument caught the initialization trap; the *post-run* skeptic caught the perplexity confound that would have over-claimed the thesis. The fix it forces is elegant: the resolving experiment (E004, alignment-guided vs perplexity-only KD) must compare **at matched perplexity** — the only design that can show alignment recovered *beyond* what the LM objective implies. Negative/qualified result; the kill-test eliminated both the "F1 confirmed" over-read and the "preserve-by-default" kill, leaving one precise next experiment.

### L012 — 2026-06-11 — The brain loss IS a small brain-specific lever on the strong aligner, but the 5-ROI screen is underpowered to confirm it absolutely — and the *co-trained* MSE readout (not the frozen one) is what transmits it

E004 (R03 Layer 1 / D010) brain-tuned gpt2 (L7) and Qwen2.5-0.5B (L12) with a differentiable brain-alignment loss (LoRA; co-trained-MSE / cosine / neg-Pearson / frozen-ridge / CKA), each readout form tested against its OWN block-permuted-fMRI twin and a plain-LM-finetune control, on rotating contiguous Tuckute folds (3 seeds × 5 folds). Five durable lessons:

(1) **The lever is real but small and brain-specific on the strong aligner.** No arm *raised* held-out unique R² above the untuned base (every Δ-vs-base CI included 0 — fine-tuning on 800 isolated sentences mildly degrades alignment). BUT the matched paired contrast — arm minus its own permuted twin — is **significant for Qwen co-trained MSE: +0.0032 [+0.0006, +0.0058]**, i.e. tuning toward *real* BOLD beats tuning toward *shuffled* BOLD. That is a genuine optimizable brain-specific signal, just below the absolute-test threshold.

(2) **Power, not absence, gates the screen.** MDE(80%) on Qwen ≈ +0.006; the effect ≈ +0.003. The absolute lever (vs base) and the coarse unpaired `>perm95` test both fail; the paired specificity contrast succeeds. A null on a 5-ROI screen is therefore NOT a kill — it routes to the powered LeBel voxelwise benchmark (predeclared). Always state the MDE and decide significance on the matched paired contrast, not the unpaired one.

(3) **The co-trained readout is NOT inert at scale — reversing the smoke hypothesis.** A short gpt2 smoke showed `mse ≈ mse_perm` (the readout absorbs the loss, pirlot-2022 worry). But the full Qwen run shows the co-trained MSE *does* transmit brain-specific structure that generalizes to held-out stimuli. Lesson: do not lock a loss-form verdict on an underpowered smoke; the absorption was a small-data/weak-aligner artifact. The **frozen** readout, by contrast, is *not* brain-specific (≈ its permuted twin) — it only acts as a gentle regularizer (beats `lm_only` non-specifically). So the theory-preferred co-trained MSE on the strongest aligner is the D010 front-runner, unconfirmed pending LeBel.

(4) **"Beats aimless LM-finetune" ≠ "is a brain lever."** Brain objectives degraded alignment less than plain `lm_only` (gpt2 frozen −lm_only +0.0028 sig; Qwen mse −lm_only +0.0056 sig), but for `frozen` this is non-specific regularization (gentler perturbation than next-token CE on tiny data), not brain signal. The permuted twin is what separates the two — without it, `frozen` would have read as a false lever.

(5) **Full fine-tuning destroys the LM (→ confounds alignment via L011); use LoRA.** Full-FT at λ=10 sent perplexity to 226 (gpt2) / 865 (Qwen) before LoRA fixed it (~180–256, base ~105). Even LoRA at lr 2e-4 × 3 epochs on 800 sentences degrades ppl ~2× — a gentler / perplexity-matched regime is worth testing. Two adjacent factual finds recorded the same day: E002/E003 NC-normalised by the **wrong** ceiling (anatomical `anatglasser_LHRH_LangNetw`=0.353 vs the functional `lang_LH_*` targets' mean 0.491 / network 0.559 — understated the NC-fraction); and ~⅓–⅔ of E002's unique R² co-varies with imageability+surprisal that length+position+static nuisance never subtracted (surprisal is LM-derived, so it is handled via rotating splits + paired controls, not folded into the metric — over-subtraction risk).

### L013 — 2026-06-11 — A2 holds POWERFULLY at voxel scale, but the lever line is structurally underpowered — the evidence (and the literature) pivots the thesis toward the rate–distortion trade-off curve / measurement rigor

E006 ran the powered LeBel UTS03 voxelwise A2-feasibility (the E002 question at ~11.4k NC-reliable voxels, story-level CV, full expanded nuisance = phone-tier rates/duration/length + log-freq + eng1000, capacity-fair PCA, held-out-repeat voxel selection). Three durable lessons:

(1) **A2 is a strong, powered PASS at voxel scale.** Trained−untrained gap = +0.0207 [+0.0205,+0.0209] (gpt2, 95% voxels positive) and +0.0277 [+0.0274,+0.0280] (Qwen, 99%), Qwen>gpt2 as expected. The trained LM robustly predicts UTS03 BOLD beyond a random net after the strongest anti-confound — clearing the Hadidi/Feghhi (2026) bar (untrained explains ~0 unique variance). The alignment signal is unambiguously REAL and MEASURABLE. This is the powered confirmation Tuckute's 5-ROI screen could only hint at.

(2) **But the lever (optimization) line is structurally underpowered for the effect size that exists.** The empirical E007-lever MDE(80%) on the mean-over-voxels unique-R² statistic is +0.013 (gpt2)/+0.015 (Qwen) — ~4–5× the +0.003 brain-specific lever E004 found. (The paired arm-vs-permuted contrast that detected E004's effect could be better-powered, but confirming it would BE E007, a gamble against a fragile +0.003.) Per the predeclared "quiet kill" branch, do NOT build the TR-level E007 lever loop.

(3) **Synthesis → pivot the headline (the idea is not holy text).** Measuring alignment is robust (A2); *optimizing* it gives only a small, fragile, hard-to-resolve gain (E004 +0.003; L011/L012 it co-varies with perplexity). The published anti-confound literature agrees: Hadidi/Feghhi 2026 (NatComms) finds positional-word-rate + GloVe explains >80% of GPT-2XL neural variance and the trained-LLM residual is "real but small" (≤10%); the lit-fork sweep leans B. So the defensible, novel, literature-consistent contribution is **a rigorous characterization of the alignment signal and its rate–distortion trade-off against compression** (no one has done alignment-guided compression at matched budget — the gap is open), NOT "alignment-guided distillation wins big." The deciding experiment is E005 (alignment-guided vs perplexity-only KD at *matched perplexity*): a big brain-term win confirms F1; a small/null IS the honest trade-off-curve result. Either way the thesis stands on rigor. Powered-substrate methods (`scripts/lebel_adapter.py`, `run_lebel_encoding.py`) are built and validated for the voxelwise trade-off-curve work.

### L014 — 2026-06-11 — F1 CONFIRMED in-domain: alignment-guided KD recovers brain-specific alignment beyond perplexity-only KD at matched perplexity (small but real; the dissociation E003/E004 couldn't establish)

E005 distilled Qwen2.5-1.5B → Qwen2.5-0.5B (LoRA, KD-KL retention) with vs without a co-trained-MSE brain loss, on Tuckute, 3 seeds × 5 rotating folds. The primary statistic — paired (kd_brain − kd_brain_permuted) at **matched perplexity** (55.4 vs 55.3, matched by construction since the permuted twin shares the KD+MSE objective) — is **+0.0081 [CI +0.0023, +0.0171], CI excludes 0**. Lessons:

(1) **F1 holds in-domain.** The brain objective buys a real, **brain-specific** (beats its permuted twin), **perplexity-independent** (matched ppl) alignment gain in distillation. This is the dissociation E003 (L011, alignment co-varies with ppl) and E004 (fragile, matched-budget-not-ppl) could not cleanly show. It flips the oracle's "Fork B more likely" prior.

(2) **The KD setting + matched-ppl-permuted-twin design CLEANED UP E004's fragility.** E004's +0.0032 lever was fold-4-dependent (CE retention, full-budget). E005's +0.0081 is 4/5 folds positive and robust to fold-4 removal (leave-one-out +0.0042). Two design reasons: the KD-KL teacher anchor is a cleaner/stronger LM retention than CE on tiny data (so the brain MSE gradient shapes the representation more cleanly), and the permuted twin shares the exact objective → matched ppl by construction (removing the L011 perplexity confound that diluted E004). Lesson: the permuted-twin-at-matched-ppl paired contrast is the right, powered (MDE +0.0035), confound-clean statistic for this question.

(3) **The gain is despite a slightly WORSE LM** (kd_brain ppl 55 vs kd_ppl 51) — so it is not the "better LM → more aligned" confound (L011); it is the brain objective adding alignment the LM objective doesn't.

(4) **But the effect is SMALL → an A+B synthesis, not triumphal A.** +0.0081 ≈ 1.6% of the NC ceiling (kd_brain 0.030 vs permuted 0.014 NC-norm). This is exactly the "real but small residual" regime (Hadidi/Feghhi 2026 ≤10%). The honest, strong thesis = F1 confirmed (A) + the rigorous characterization of how small it is / the rate–distortion trade-off curve (B). Next gates: LeBel voxelwise TRANSFER (needs a *powered* statistic — per-voxel paired / region-restricted, since the mean-over-voxels MDE +0.013 ≫ the effect; design + oracle-gate first) and the λ-sweep/multi-rate trade-off curve.

### L015 — 2026-06-11 — The E005 in-domain "CI excludes 0" was pseudo-replication; at the honest inference unit (folds, one subject) it is a borderline TREND, not a significant result — revises L014's inference claim

A Session-8 thinking-panel audit (counter-argument + premortem + first-principles, all fable, run *before* spending the next compute) re-derived E005 from the raw JSON (`scripts/reanalyze_e005_e006.py`, pure re-analysis). The headline "+0.0081 [+0.0023, +0.0171], CI excludes 0" (L014) used a **15-cell flat bootstrap** (3 seeds × 5 folds) over **one subject-average** (Tuckute 5-UID mean) on the same 1000 sentences. The 15 cells are not independent — seeds reuse identical data; folds are one 5-way partition of one subject. Lessons:

(1) **At the honest unit (5 disjoint folds), the brain-specific contrast is NOT significant.** Fold-level t-CI95 = **[−0.0030, +0.0193] (includes 0)**; mean +0.0081, sd 0.0090, n=5. A cluster-bootstrap over folds *excludes* 0 ([+0.0031,+0.0162]) — the two disagree because the distribution is right-skewed by **one outlier run (fold4/seed0, uR²=0.073, ~7× the next cell, 52% of the total signal)**. Mean +0.0081 is 2.4× the **median +0.0034**; leave-fold-4-out = +0.0042. Honest verdict: a **small brain-specific trend** (4/5 folds positive, median ~+0.003–0.004), not a confirmed "CI excludes 0" effect.

(2) **Choose the inference unit by what is independent, not by what maximizes n.** Folds and seeds on one subject are correlated; the legitimate replication units are *subjects*. Tuckute ships per-participant data (`target_UID`; 5 train UIDs currently averaged) — the fix for the n=1 hole is to run the contrast **per participant** and treat subjects as independent units (in-domain, cheap). Also: `n_perm=1` made the matched null a single noisy draw — use n_perm ≥ 10. The harness's own coded `beats_permuted_null=False` flag should always be reported alongside the paired statistic.

(3) **The LeBel voxelwise TRANSFER test is underpowered on the valid statistic.** The paired-contrast MDE (derived from E006 fold_sd) needs arm-correlation ρ ≥ 0.9 to resolve even the inflated +0.0081; the honest +0.0042 is below noise for nearly all ρ. The effect is smaller than the instrument's floor *before* cross-dataset attenuation. Per-voxel-paired buys power only by ignoring spatial autocorrelation (the spatial twin of L003). → don't make transfer the next compute; solidify in-domain (per-subject) first, then pursue A3 (practical payoff — the real, unexplored gap).

(4) **Process lesson: run the post-step adversarial panel BEFORE building on a verdict, not after.** The panel caught a pseudo-replicated CI, a missing decider number (paired MDE), and an ungrounded citation in one pass — for ~3 fable subagent calls, before any wasted compute. This is the D017 loop working as intended.

### L016 — 2026-06-11 — The in-domain F1 effect is a GROUP-AVERAGED-TARGET phenomenon that VANISHES per individual — a well-powered null (E008 confirms L015 empirically)

E008 re-ran the E005 brain-specific contrast (kd_brain mse − kd_brain_permuted at matched ppl) **per individual participant** (9 Tuckute UIDs as independent replication units; uid 853 excluded for incomplete ROI) instead of on the 5-UID average. The panel (counter-argument + first-principles-grounder, fable) adjudicated the verdict. Lessons:

(1) **The effect collapses ~80×: from E005's averaged +0.0081 to a per-subject mean +0.00010** (t-CI95 [−0.0004,+0.0006], n=9, sign 5/9, fold-clustered CI includes 0 and fails LOO-fold). The 4 subjects E005 literally averaged (848,865,875,876) individually show **−0.00010**. The effect is a property of the average, not those brains.

(2) **It is a WELL-POWERED null, not low power.** Subject-axis MDE(80%) ≈ +0.0006–0.0013, 6–12× below +0.0081. The averaging-SNR steelman (Fork B: averaging legitimately denoises the target → higher achievable R²) is theoretically real but *quantitatively rejected* — NC≈0.49 implies only ~1.7× inflation (noise-ceiling math), predicting ~+0.002 per subject, which E008 was powered to detect (3.3× above MDE) and did not. Estimand note: effect-on-averaged-target ≠ mean-of-per-subject-effects (unique-R² doesn't commute with averaging); the averaged-target effect is alignment to the *shared stimulus-evoked response*, not per-person brain alignment.

(3) **Methodological lesson (the big one): averaging fMRI targets across subjects manufactures apparent brain-specificity.** A gain measured against a group-averaged target is a gain toward the shared, stimulus-driven component at an inflated noise ceiling — and reads as "brain-specific" against a permuted twin even when no individual shows it. Always test brain-alignment claims at the individual-subject inference unit, or explicitly scope the claim to the averaged target. This generalizes L003/L015: the inference unit must be the independent biological replicate (the person), and shared stimuli still correlate "independent" subjects (the E008 oracle HOLD).

(4) **Thesis consequence:** the in-domain F1 "headline" (L3) does not hold per-individual. Honest contribution = A2 (real, powered) + this well-powered null + the anti-confound characterization + A3 (practical payoff, the central open question). A per-individual positive would need higher per-subject SNR (within-subject repeats) or surprisal/imageability conditioned into the nuisance — not more averaging. This is a clean, publishable Fork-B result; the rigor (panel before compute, then E008) is what caught an overclaim that would otherwise have been the thesis headline.

<!-- Add new lessons below as we hit them. Negative results count. -->
