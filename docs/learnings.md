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

### L017 — 2026-06-11 — A3 (practical payoff) is a bounded NULL: brain-tuning at matched perplexity buys no brain-specific OOD value — because the fulcrum (a reliable brain-specific representational change at matched ppl) itself ~0 at this scale

E009 A3 pilot: KD Qwen1.5B→0.5B (LoRA) toward the group-averaged Tuckute target, 4 arms (kd_ppl / kd_brain / kd_brain_permuted / **text-feature pseudo-target control**), outcome = OOD-perplexity ratio (Pereira + LeBel) + held-out representational gap; powered to n=8 seeds. Two-panel-adjudicated (counter-argument + premortem). Lessons:

(1) **The fulcrum is ~0 at matched ppl.** The brain-specific representational gap (mse − mse_perm held-out uR²) is mean +0.011 but **median +0.004, 5/8 positive, MDE80 0.023 ≈ mean → within noise**, and **seed-0 (+0.063) is a lone outlier** carrying it (the other 7 avg +0.004 — the L015/L016 outlier pathology, third occurrence). You cannot reliably induce a brain-specific representational change at matched perplexity at this scale, and λ can't grow it without collapsing ppl (λ=30 → ppl 92, one seed 148). So A3 is **null-by-construction**: there is no reliable manipulation whose downstream value to test.

(2) **No brain-specific downstream OOD effect.** At n=8 every contrast is within the measured MDE — kd_brain ≈ kd_brain_permuted ≈ textfeat ≈ kd_ppl on OOD-perplexity ratio. (The n=3 "kd_brain worse than kd_ppl" was noise; it vanished with seeds — and was non-brain-specific anyway, the permuted twin matched it.)

(3) **Measure the MDE, don't borrow it.** The design initially carried Guo 2024's 2–4pp as the MDE; the oracle (correctly) demanded it be measured from the run's own seed variance. The measured OOD-ratio MDEs (0.029–0.13) are what bound the null — borrowing Guo's number would have mis-stated the power.

(4) **The text-feature pseudo-target control matters.** Averaged-target + permuted-twin only tests structure-vs-shuffle; the text-feature arm (ridge[surprisal,imageability,length]→BOLD, held-out R²=0.086) separates "brain-derived" from "any smooth text-correlated regressor." kd_brain ≈ textfeat downstream → no evidence the brain-derived target beats a cheap text-feature target.

(5) **The Negi-2025 reconciliation (positive prior vs our null):** Negi got positive downstream gains, but baselines against a *non-perplexity-matched* vanilla model — the L011 LM-quality confound. Our null is the brain-*specific* increment at matched ppl + permuted twin. The control is the contribution.

(6) **Strategic (the dominant premortem risk): don't write the thesis as "a string of nulls."** The positive contribution is **L016 — cross-subject target-averaging manufactures apparent brain-specificity, and the matched-ppl + permuted-twin + per-subject protocol detects it** (the +0.0081→+0.00010 collapse). Frame A2 + L016-method + the two characterized nulls as a coherent Fork-B paper: *a confound that inflates a class of alignment-training overclaims, and the clean protocol that catches it.*

### L018 — 2026-06-12 — The averaging dose-response: the apparent brain-specific gap is ~0 per individual and is PRODUCED by averaging subjects (earns the manuscript's positive claim)

E010 ran the brain-specific contrast (kd_brain − kd_brain_permuted, held-out unique R²) against targets averaged over k ∈ {1,2,3,5,9} subjects (nested), 4 seeds. Gap by k: **−0.0002 (k=1), −0.0001 (k=2), +0.0023 (k=3), +0.0194 (k=5), +0.0071 (k=9)**; seeds-positive 2/4, 1/4, 3/4, 4/4, 4/4. Lessons:

(1) **The demonstration the manuscript panel demanded.** A single subject (k=1) shows ~0; averaging produces the apparent gap (k≥3 positive). So the "brain-specificity" measured against an averaged fMRI target is an *artifact of averaging*, not a per-person property — this is the direct, causal evidence that upgrades "the per-subject effect is null" (E008) to "averaging inflates/produces apparent brain-specificity." The rising limb (k=1→5) tracks the noise-ceiling prediction NC_k = NC/(NC+(1−NC)/k) (0.49→0.83).

(2) **Honest caveat — not perfectly monotone.** k=9 (+0.007) < k=5 (+0.019), within the wide 4-seed error bars (se≈0.004–0.006), plausibly because the nested k=9 set adds the noisier held-out subjects. Claim the **qualitative** law (gap≈0 at k=1; averaging is necessary for the gap), not a precise gap∝NC_k fit. A cleaner version: random size-k subsets + more seeds.

(3) **Verb discipline.** "Manufactures/produces" is now defensible *in the specific sense that the gap is absent at k=1 and appears only on averaging* — but report the actual curve and the caveat; don't claim a clean monotone quantitative law the data don't show.

### L019 — 2026-06-12 — The per-individual null is robust to LoRA CAPACITY (not to a stronger manipulation): heavy LoRA didn't move the representation; the knob that does (λ) wrecks perplexity

E011 brain-tuned per-individual (9 UIDs) with heavy LoRA (r=64/6 epochs ≈ 4× E008's capacity) to test the "you under-tuned" objection (vs Negi 2025). Per-subject gap +0.00043 (CI incl 0, fold-clustered incl 0, sign 6/9, held-out-5 −0.0001). Lessons:

(1) **"Stronger regime" must be verified by effect, not hyperparameters.** The counter-argument panel showed heavy LoRA produced the *same* representational movement as E008's light LoRA: mse absolute held-out uR² +0.00076→+0.00082, ppl 1.32×→1.35× base — indistinguishable on both the optimized quantity and the LM-damage proxy. At fixed λ_brain on isolated sentences the alignment gradient is exhausted; extra rank/epochs change nothing. Lesson: always confirm a manipulation actually got stronger (measure the absolute change) before claiming robustness to it.

(2) **The matched-ppl regime structurally bounds the per-individual test.** Capacity (r, epochs) doesn't move the representation; λ_brain does but wrecks perplexity (E009/L017: λ=30→ppl 92) and *still* doesn't grow the gap. So within matched-ppl the per-individual brain-specific null cannot be escaped — this is the honest, complete boundary (no further matched-ppl experiment is informative). The only open direction is a different objective+data regime (Negi's contrastive loss + naturalistic data), which we don't have.

(3) **Outlier pathology, 4th occurrence (L015/L016/L018).** The slightly-larger +0.00043 (vs +0.00010) is one subject (uid 875 = 79% of the sum); LOO-subject → +0.00010. Always report LOO-subject; one unit keeps carrying these tiny effects.

(4) **A vacuous covariate read-out is not a passed control.** The ppl-intercept "matched-ppl" read-out only means something if the arms diverge in ppl; here they didn't (Δlog-ppl −0.013), so the intercept just reproduced the raw gap — report it as "no divergence to adjust," not as evidence of brain-specificity at matched ppl.

### L020 — 2026-06-12 — The clean (random-subset) dose-response is NOISY and non-monotone: the nested E010 curve was partly a design artifact; the headline rests on E005-vs-E008, not the dose-response

The socratic capstone flagged that E010's clean monotone gap(k) curve used NESTED subsets (k=1=uid 848; the high-leverage uid 875 entered at k=3), confounding subject-count with subject-identity. E010b re-ran with RANDOM size-k subsets (flagging 875-in/out): gap(k) = +0.0015 (k=1), **−0.0013 (k=3)**, +0.0088 (k=5), +0.0094 (k=9); sd 0.005–0.015; 875-in vs 875-out inconsistent (875 alone gives +0.0038 at k=1, but at k=5 the 875-OUT subsets give the bigger gap, +0.0125). Lessons:

(1) **The nested dose-response overstated the cleanliness of the mechanism.** With random subsets the curve is non-monotone and very noisy — the clean 0→+0.019 nested rise was partly an artifact of which subjects entered at each k. The *causal/monotone* "averaging produces the gap" claim is NOT cleanly established at this sampling (2 seeds × 3 subsets/k → huge variance). Don't claim a clean dose-response law.

(2) **The headline does NOT need the dose-response.** "Averaging inflates apparent brain-specificity" is established directly by **E005 (averaged target → +0.008) vs E008 (per-individual, n=9, well-powered → ~0)**: the averaged measurement shows a gap the individual reality doesn't. That contrast is the solid evidence; the dose-response is at most suggestive corroboration (averaged targets at high k tend to show a gap, consistent with the noise-ceiling mechanism, but noisily).

(3) **Process lesson:** a single clean-looking curve from a confounded design (nested subsets) is a trap; the random-subset control is what revealed the noise. This is the L015/L016/L018/L019 pattern again — clean-looking small effects keep dissolving under the proper control. The rigor (socratic capstone → clean re-run) caught it before it shipped as a headline figure.

### L021 — 2026-06-12 — The LeBel substrate-mismatch gap is feasible+data-ready but POWER-LIMITED at n=3; the per-voxel "huge N" is a pseudo-replication illusion (E012 deferred by the gate)

Corrected an earlier-session error: I declared the multi-subject naturalistic test "blocked by data we lack." A data audit (Explore) found the deep subjects UTS01/UTS02 are on **public OpenNeuro S3** (reachable; boto3 available); I downloaded them (20 stories each) → n=3 deep subjects (E006 had 1). So the data was never the blocker. But the oracle gate on E012 returned **DEFER-POWER-LIMITED**:

(1) **Per-voxel-paired across ~11k voxels is NOT a powered statistic.** The voxels are read from a single (mse, perm) model-pair per fold and are spatially autocorrelated → effective independent units ≈ resel count O(10²), and a per-voxel CI is pseudo-replicated/anti-conservative (the spatial twin of the L003 temporal-autocorr and L015 single-target traps). The valid replication unit is the **subject**.

(2) **At n=3 (df=2) the across-subject MDE ≈ +0.003** — ~10× the +0.0001–0.0004 per-individual effect — and between-subject biological variance does NOT shrink with more TRs/subject. So more data *per subject* (LeBel's deep sampling) does not help; only more *subjects* do. n=3 → at most a per-subject existence demo, never a generalization claim.

(3) **The L011 ppl-confound recurs harder at TR-voxel scale** (richer regime → real BOLD more learnable than permuted → ppl divergence), and its control (ppl-covariate intercept) needs an n that n=3 can't support.

(4) **Lesson — distinguish "blocked by data" from "blocked by N."** The honest constraint isn't missing data (acquired) — it's that a powered per-individual claim needs n≳8–10 within-subject-repeat subjects, which the available deep-sampling datasets (LeBel: 3 deep subjects) don't provide. Building the heavy E007 voxelwise-tuning loop for an n=3 underpowered test is not justified; the gate (quantitative MDE), not a unilateral read, made the call. Manuscript §6.5 states it as feasible/data-ready/power-limited.

### L022 — 2026-06-12 — Grounding the novelty REFRAMED the paper: the averaging confound hits real targets (Tuckute, RSA) but is narrow; the PROTOCOL is the headline (premortem + lit-scout converged)

A final premortem on the complete manuscript returned NEEDS-REFRAME: the "averaging inflates apparent brain-specificity" headline risked having *no live target* (it was demonstrated only on our own E005 artifact). A decisive lit-scout pass on "who uses cross-subject-AVERAGED fMRI targets?" settled it:

(1) **The confound DOES hit live targets — but narrowly.** **Tuckute 2024** (the benchmark we optimize against) explicitly averages BOLD across participants ("averaged across participants to yield an average language network response") → our confound applies directly. **RSA group-average-RDM** practice (Nili 2014) is structurally exposed too. BUT the dominant encoding lineage (Schrimpf, Caucheteux, Antonello/Huth) and **all** per-participant brain-tuning works (Schwartz 2019, Negi 2025, Bilgin 2026, Moussa 2025a/b, Aw 2023) fit per-subject (scores averaged *post-hoc*) — NOT touched. So "reframes a class of optimistic brain-tuning results" overclaimed; the confound's real scope is averaged-target *benchmarks* (Tuckute, RSA), not per-subject tuning.

(2) **REFRAME to the protocol as the headline (Option 2).** The defensible, broad contribution is the **matched-perplexity + permuted-twin + per-individual protocol** — which NO prior brain-tuning paper runs end-to-end (per-subject works lack a permuted-brain control on downstream claims; benchmark works lack matched-ppl + per-individual). The protocol *bites* (the gains we sought are well-powered nulls under it). The averaging confound becomes the concrete *motivating instance* (real, on Tuckute + RSA), not the sole headline. Retitled the paper accordingly; this survives all three premortem reviewers.

(3) **Process lesson (the hook was right):** I'd declared the work "done" without grounding two load-bearing claims — whether the data was truly unavailable (it wasn't; downloaded UTS01/02) and whether the confound had a live target (lit-scout: yes-but-narrow). Grounding (data audit + 2 lit-scout passes + a methods digest) materially changed the data-availability story (E012), the novelty scope (Lage-Castellanos/Nili known mechanism), AND the paper's headline (protocol, not confound). Ground before declaring done.

### L023 — 2026-06-12 — Second reframe (panel-converged): lead with the well-powered per-individual NULL, not the protocol; the null is sensitivity-confirmed (power 1.0 at δ=+0.003); only per-individual inference caught the averaging artifact

A panel pass on the reframed v0.7 (first-principles + counter-argument, fable) found the *protocol-headline* was an over-correction. Two findings, both acted on:

(1) **"No prior runs the 3-control protocol end-to-end" was OVERCLAIMED** and rested on a factual error: I wrote "per-subject works lack a permuted-brain downstream control" — but **Moussa 2025 (per-subject) runs exactly that on downstream** (its block-permuted-fMRI ablation). The real residual gap is *one* control — matched-perplexity. Fixed in abstract/§1/§5.

(2) **The protocol-headline is circular** ("a protocol shown only to reject is not validated") AND — the sharp point — **two of the three controls were FOOLED by the averaging artifact**: the +0.008 averaged-target gain *beats* its permuted twin and *is* matched-ppl by construction; **only per-individual inference caught it.** So the operative corrective is subject-level inference, not a 3-part instrument. Stated honestly now.

→ **Reframed (2nd time) to the empirical finding as headline:** "a brain-tuning gain against a cross-subject-averaged target vanishes per individual." This is a falsifiable result (not a methodological promise), has a live target (Tuckute/RSA), and is distinct from Moussa (we show *zero* per-individual, not merely *suboptimal* → artifactual not attenuated). The protocol is demoted to method (§3).

(3) **Sensitivity demo closes the "just underpowered" attack** (`scripts/sensitivity_e008.py`): on E008's observed between-subject sd (0.00062), the t-CI test has **power 1.00 to detect a +0.003 per-individual effect, 0.99 at +0.001, 0.72 at +0.0006** → the observed +0.0001 is a TRUE null, not a power failure. Converts the analytic MDE into a demonstrated power curve.

(4) **Process lesson:** reframes can over-correct. The protocol frame fixed "no live target" but introduced circularity; the panel caught it and converged on the empirical-null frame, which survives both. Run the panel on the REFRAMED artifact, not just the original. (Also: still no `tuckute-2024` canonical note — the live-target claim is grounded by the lit-scout's direct quote + our data (load_tuckute averages over UIDs), but a digest would fully ground it — flagged.)

### L024 — 2026-06-12 — The open-frontier data requirement is precise and modest: ~5 deep subjects power a +0.003 per-individual test (not the oracle's conservative n≳8–10)

A power-vs-n simulation (`scripts/sensitivity_e008.py`, extending the E008 sensitivity sim) quantifies how many deep subjects a powered per-individual test needs, instead of hand-waving "more": at the voxelwise between-subject variance the E012 oracle estimated (σ≈0.001), detecting a +0.003 per-individual effect (the averaged-target magnitude) reaches **power 1.00 at n=5** (0.76 at n=3); n=8 if σ is 2× larger (0.002); n≈10 for a smaller δ=+0.001. So the open-frontier / substrate-matched per-individual test (E012, and the full-FT+naturalistic regime) needs only **~2–5 additional deep subjects** beyond the 3 we have (UTS01/02/03) — a modest, identifiable acquisition (OpenNeuro/LeBel has more deep subjects), not an impossibility. This refines L021's "n≥8–10" to an evidence-based ~5–8 depending on variance, and makes the data-acquisition decision concrete. Folded into manuscript §6.5.

### L025 — 2026-06-12 — The contrastive objective (Negi's NT-Xent family) also gives a per-individual null at matched ppl → "wrong loss" ruled out (at ROI granularity); the open frontier is the DATA/voxelwise axis, not the objective axis

E013b added an InfoNCE/NT-Xent contrastive brain-loss (`brain_loss.contrastive`) and ran it per-individual on Tuckute (n=9, the E008 crossed-inference design) — the tractable slice of the open frontier (Negi's objective axis on data we have). Result: contrastive brain-specific gap = mean −0.00019, t-CI [−0.0008,+0.0005] (incl 0), sign 4/9, ppl-intercept −0.0003 — a well-powered ~0 (slightly negative), same as the MSE result (E008). Lessons:

(1) **The per-individual null is not an artifact of the MSE objective.** A contrastive/ranking objective (Negi's loss family) doesn't rescue it — switching the loss at ROI granularity changes nothing. This closes one of Negi's two axes (objective) as the explanation for our null. Caveat: the 5-ROI Tuckute target is low-dim for contrastive, so this is a weaker test of the objective axis than a voxelwise contrastive would be.

(2) **The open frontier narrows to the DATA/voxelwise axis.** With both MSE and contrastive giving per-individual nulls at ROI granularity, the only remaining route to a per-individual positive is high-dim naturalistic voxelwise targets (the full E013: denizenslab n=6 + the voxelwise tuning loop) — a heavy build. The cheap objective-axis substitution did NOT rescue it, so it doesn't shortcut the heavy build.

(3) **For the manuscript:** this tightens the "regime-specific" concession — we now show the null holds across *two objectives* (MSE, contrastive) at matched ppl, not just MSE, leaving only the data/voxelwise axis untested. A stronger, more complete negative.

### L026 (CORRECTED) — 2026-06-12 — E013 v1 was a FAILED MANIPULATION (tuning DEGRADED held-out alignment), caught by the panel; NOT a same-substrate null. Always verify the manipulation moved the rep the RIGHT way before interpreting a null.

**Correction:** my first E013 writeup claimed "the per-individual null holds on the powered voxelwise substrate → closes substrate-mismatch." The counter-argument panel showed this was WRONG: in all 6 subject×seed runs the real-target tuning **reduced** held-out alignment below the untuned base (`real_u < base_u`: UTS02 0.0085→0.0044, UTS01 0.0058→−0.0017, UTS03 0.0077→0.0033). The ~0 real-minus-permuted gap compares two *degraded* representations → uninformative. The ~10M-param 11k-voxel readout over ~1k segments at λ=10 (no KD anchor) damaged the general features the held-out ridge needs. **The substrate-mismatch limitation REMAINS OPEN.** Lessons:

(1) **The L019 lesson, sharper: verify the manipulation moved the rep the RIGHT direction.** E011 was "hollow" (rep didn't move); E013 v1 was *anti*-verified (rep moved the WRONG way — alignment dropped). A null from a manipulation that degrades the target metric is meaningless. **Mandatory check: real-target tuning must beat the untuned base on the held-out metric before any real-minus-control gap is interpreted.** I should have built this check in (and the design predeclared a ppl-intercept + spatial-blocking it then skipped — protocol drift).

(2) **The panel is the safeguard against my own overclaim.** I recorded "closes substrate-mismatch" + updated the manuscript before panel-verifying — and it was wrong. The fix was the counter-argument reading the raw base_u-vs-real_u from the JSON. Run the panel BEFORE the claim lands, every time (the whole point of D017).

(3) → E013 v2: re-run with a manipulation that takes hold (KD anchor + lower λ + fewer high-NC voxels + the real_u>base_u check). The n≥5 decision is deferred until a valid n=3 manipulation exists. (Earlier "null is convergent across all axes" was overstated for the voxelwise axis — E013 v1 doesn't count; E008 ROI / E011 / E013b stand.)

### L026-orig (SUPERSEDED by the correction above) — claimed E013 closed substrate-mismatch; retracted

E013 built the voxelwise per-individual brain-tuning loop (the deferred "E007", `run_lebel_tune.py`: per-segment tune target + brain_tune MSE/LoRA + held-out-story unique-R² eval via the E006 protocol + permuted twin) and ran it on the 3 LeBel deep subjects (UTS01/02/03 — acquired UTS01/02 + their wheretheressmoke repeats from OpenNeuro). Per-subject brain-specific gap: −0.0010 / +0.0010 / +0.0004 (mean +0.0001), sign-flipping across seeds in 2/3 → **no robust per-subject voxelwise gain** (existence probe, n=3, not population). Lessons:

(1) **Closes the substrate-mismatch limitation (the oracle's secondary weakness).** The per-individual null now holds on the *same* powered naturalistic voxelwise substrate where A2 is real (E006/LeBel) — not just on Tuckute ROI. So "real in aggregate, not optimizable per-individual" is now shown *on one substrate*, removing the cross-substrate caveat.

(2) **The null is convergent across every axis tested:** ROI (E008) + voxelwise (E013); MSE (E008) + contrastive (E013b); light (E008) + heavy (E011) tuning; isolated-sentence + naturalistic. Five experiments, all per-individual ~0.

(3) **n≥5 is recommended-against (the data-acquisition decision, informed by n=3):** the n=3 gaps are centered at exactly 0 and seed-unstable — not a small-positive trend that more subjects would resolve. The power sim's "n=5 detects δ=+0.003" is moot because the effect is ~0, not +0.003. A multi-day denizenslab n≥5 build would be an expensive confirmation of an already-robust, multi-substrate null. The convergent evidence closes the per-individual line.

(4) **Process:** built the deferred heavy pipeline (E007) tractably by reusing brain_tune (per-segment target) + the E006 eval — the differentiable Lanczos/FIR loop wasn't needed for a valid test. When a "multi-day build" blocks, look for the reuse that makes it a one-script build.

<!-- Add new lessons below as we hit them. Negative results count. -->
