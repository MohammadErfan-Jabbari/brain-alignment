# Expansion Program — the idea-tree, the literature sweep, and the climb to a top-venue result

**What this is.** The master tracker for the autonomous research-expansion goal Erfan set on 2026-06-17: do a complete analysis of every open/untested idea, build a system to sweep the top AI/ML conferences (2020→now) for related work, build a hierarchical **idea tree** for the whole project, and then *climb the tree* — implementing and experimenting the untested nodes, four-at-a-time on the 4× L40S, questioning the assumptions under every "closed" node, adding nodes as the literature is read — until the project holds a result with a realistic shot at a top-10 AI/ML venue. This file is the persistent state of that program across the autonomous loop. **It does not override `ladder.md`** (canonical science status) — it sits beside it and feeds it: any new evidence still flows through the normal ritual (experiment doc → panel → Erfan-confirmed rung flip). This is a *working*-mode program; it must not edit the analysis-lane docs the D011 rule protects (`reports/R06`–`R14`, the manuscript, the E005–E014 records) except to *add* new experiment records.

**Terminal condition (Erfan's words):** expand/refocus the repo's idea set until we have something with **>75% chance at a top-10 conference**. Until then, do not stop.

**This is the standing dual meta-goal made operational.** D020/D022 already commit the project to "finish the MSc *and* extract ≥1 top-venue AI paper." This program is the execution of the second half.

---

## 0. Honest strategic assessment (read before believing the plan)

Two things must be said plainly, because the whole program depends on not lying to ourselves about them.

**(a) The >75% bar is very high, and "75%" is not a number I can calibrate.** Top-10 venues run ~20–28% acceptance; the *marginal* accepted paper is strong. A clean probability of acceptance is not estimable in advance. I will treat the bar as a *direction* — "get the work to a credible, novel, well-grounded top-venue submission, and say honestly how close it is" — and track a rubric (novelty / rigor / a real baseline beaten or a real confound exposed / writing) rather than pretend a calibrated percentage. When I claim we are "near the bar," it will be against that rubric with the reasoning shown, and Erfan adjudicates.

**(b) We are starting from a robust null, and the path to a venue is NOT re-running dead experiments.** The original program is closed: the brain-alignment *training* signal is real (Q0) but not inducible beyond perplexity via any readout we tried (Q2/Q3, powered) and buys nothing practical at matched perplexity (Q4). Six robustness axes already failed. A top-venue paper comes from one of two paths, and the tree holds both:

- **Path A — the methodology/negative-result paper (we are ~80% there already).** "Cross-subject target-averaging manufactures apparent brain-specificity in alignment-*training* studies; here is the confound, the matched-perplexity + permuted-twin protocol that detects it, and a demonstration that it shrinks an *external published positive*." The premortem (L029) already flagged this as the highest-leverage move. The one missing load-bearing piece is the external demonstration (item O5 below). Venues that take this: NeurIPS D&B, ACL/EMNLP Findings or main, a rigor/repro track, or a strong workshop → main.
- **Path B — a genuinely new positive result.** Question an *assumption* under the null and find a formulation where brain-guidance helps. The nulls are all inside one paradigm (linear-readout alignment of LM internals to *fMRI*, optimized by distillation/FT, scored by *encoding R²*). The assumptions worth attacking are in §3. The literature sweep tells us which are real gaps vs already-scooped.

I am committing to pursue **both in parallel**: harden Path A (it is the floor — a real, defensible paper), and hunt Path B with the tree + compute (it is the ceiling — a stronger paper if a door opens). This is my call as the agent; Erfan can redirect.

---

## 1. Phase plan & status

| Phase | What | Status |
|---|---|---|
| **P1** | Complete analysis of open/untested ideas + assumptions to re-question | ✅ done (§3) |
| **P2** | Conference-scout system: top-10 venues locked + DBLP/OpenReview/OpenAlex/arXiv fetch pipeline → skill | 🔵 in progress (§4, §5) |
| **P3** | Literature sweep 2020→now: metadata pull → abstract-level relevance filter → digest survivors (dedupe vs our 40 canonical notes) | ⬜ blocked on P2 |
| **P4** | Build the idea tree (source = thesis; layers by solution altitude; seeded from our nodes + new lit nodes) | 🔵 scaffolding (§6) |
| **P5** | Climb: implement untested nodes ≤4-parallel on L40S; each closed by the thinking panel → verify → address; record back | ⬜ |
| **P6** | Loop to the terminal condition; each result spawns/prunes nodes; reassess against the venue rubric | ⬜ |

Thinking subagents: the repo already defines the four (`counter-argument`, `socratic-thinker`, `premortem-analyst`, `first-principles-grounder`, all opus) — reused and sharpened, not duplicated. New *operational* agents added only where a gap exists (e.g. an idea-tree maintainer, a conference-sweep worker).

---

## 2. What we already have (so the sweep dedupes and the tree seeds correctly)

- **40 canonical literature notes** (`docs/literature/canonical/`) — strong existing coverage of brain-LM alignment, brain-tuning, KD, scaling/quality laws, anti-confound critiques. The sweep must dedupe against these.
- **22 cloned paper-repos** (`data/paper-repos/`), **19 experiment docs** (E001–E020), **8 reports** (R01–R07 + retired R05), **36 scripts**.
- **Course material** (`data/course-material/`): Information Theory for ML + Probabilistic ML — the math grounding (MI bound, DPI, conditional-MI = unique R², rate-distortion). Ground theory claims here, do not re-derive.
- The science state and journey: `ladder.md` (status), `map.md` (the tree-so-far + codes), `tasks.md` (backlog).

---

## 3. Phase-1 result — the open doors and the assumptions to re-question

### Untested / open doors already in the program
| # | Door | Grounding | Prior |
|---|---|---|---|
| **O1** | Full-FT multi-subject naturalistic voxelwise (denizenslab n=6) — the one untested induction *method* at multi-subject power | I3/F3; data acquired (35G); marked superseded D033 because E017 full-FT null (n=9 LeBel) + E019 corroborate | likely null |
| **O2** | TRIBE-v2 synthetic dense brain targets at KD scale (no fMRI; averaging impossible) | I4 capstone; E016; Phase-1 fidelity already PASS | null = strongest publishable Fork-B |
| **O3** | Architecture-residual beyond quality (≥3 modern families + base-vs-instruct at matched bpb) | F4 / E015; currently p=0.20, underpowered | unknown |
| **O4** | fMRI-free brain-likeness *proxy* (LID / neighborhood-overlap surrogate) | Q5; moot conditioned on a Q3 win — but reframable as a standalone cheap-proxy contribution | sign unsettled (cheng vs yu) |
| **O5** | **Demonstrate matched-ppl control shrinks an EXTERNAL published positive** — the "main-track lift" | premortem L029; the missing piece of Path A | high value, untested |
| **O6** | The DPI **selection/regularization side-channel** (brain-as-prior improves OOD without injecting θ\*-info or moving the alignment metric — a *different* MI object, I(W;Zⁿ)) | L041; argued-shut by E009's ~0 fulcrum, **not measured-shut** | genuinely open |

### Assumptions under the nulls worth attacking (Path-B seeds — the tree's upper layers)
- **A-metric:** we only ever scored *encoding R²*. Alignment might help **robustness / calibration / sample-efficiency / compositional or OOD generalization** in ways encoding-R² cannot see. (Ties O6.)
- **A-signal:** we only ever used **fMRI**. MEG/EEG (faster dynamics; Guo used EEG), ECoG/intracranial, or **behavioral** targets (reading times, eye-tracking, N400) are different couplings with different SNR and confound structure.
- **A-direction:** we only ever asked the LM to **match** the brain. Brain-as-**regularizer / selection prior / auxiliary task** is a different objective (O6).
- **A-ceiling:** the "brain's training-useful signal *is* E[Y|S]" rests on **Y⊥θ\*|S as an assumption** (L041), not a result. If false, residual brain signal exists beyond E[Y|S].
- **A-readout:** only linear-ridge / MSE / InfoNCE. Other couplings (CKA-as-objective at scale, optimal transport, RSA-based losses).
- **A-regime:** only small LMs (0.5–7B) distilled. Scale, multimodal, or instruct-vs-base regimes may behave differently (O3).

The literature sweep (P3) is what decides which of these are *real gaps* versus already-answered, and seeds new tree nodes accordingly.

---

## 4. Conference-scout — architecture (the P2 system)

**Decision (grounded in a live probe 2026-06-17):** OpenAlex conference coverage is partial (its NeurIPS source = 4,138 works total, far below reality — proceedings split across source records), so **no single source is authoritative**. The pipeline is layered:

1. **DBLP = the authoritative paper-list backbone.** Every paper of every venue/year, with title + authors + DOI/ee links. No abstracts. (`dblp.org/search/publ/api` + per-venue TOC streams.)
2. **OpenReview = first-class for ICLR (2013+) & NeurIPS (2021+) + many workshops** — abstracts + PDFs + decisions directly (`api.openreview.net` / `api2`). Use it where it covers a venue; it is the richest source.
3. **Abstract enrichment** for DBLP rows lacking abstracts: **OpenAlex** (by DOI/title) → **Crossref** → **Semantic Scholar** (rate-limited without key; back off). 
4. **PDF fetch:** OpenReview PDF → arXiv (by id/title) → Unpaywall/OA url → DOI landing. Cache under `data/papers/conference-sweep/<venue>/<year>/`.
5. **Relevance filter:** (a) high-recall keyword/regex prefilter on title+abstract (distillation, knowledge distillation, brain alignment, neural encoding, fMRI/MEG/EEG language, representation alignment/similarity, scaling laws of representation, information bottleneck, mutual information training signal, model compression, …); (b) embedding rerank with a local model (add `sentence-transformers`, SPECTER2/bge) on the 4 GPUs; (c) dedupe vs the 40 canonical notes by title/DOI. Output a ranked candidate set → `paper-digest` the survivors.

Scripts land in `scripts/litsweep/` and are wrapped as the **`conference-scout`** skill once proven. Built + tested by a delegated worker against live APIs (acceptance: reproduce DBLP's NeurIPS-2023 count within tolerance; pull ≥1 real abstract via each enrichment path; download ≥1 real PDF).

---

## 5. The top-10 AI/ML venues (locked 2026-06-17)

By h5-index / field consensus (Google Scholar Metrics, research.com, CSRankings). Topical relevance to *this* thesis (LLM distillation, brain–LM alignment, representation learning, information theory) annotated — the sweep weights the relevant ones but covers all ten.

| # | Venue | h5 (≈) | Field | Relevance here | Primary list source |
|---|---|---|---|---|---|
| 1 | **CVPR** | 450 | Vision | low–med (representation alignment, distillation) | DBLP |
| 2 | **NeurIPS** | 371 | ML (general) | **high** | OpenReview (2021+) + DBLP |
| 3 | **ICLR** | 362 | ML (general/rep-learning) | **high** | OpenReview (all) |
| 4 | **ICML** | 272 | ML (general) | **high** | DBLP + PMLR |
| 5 | **ACL** | 236 | NLP | **high** (LM, distillation, probing) | DBLP/ACL Anthology |
| 6 | **EMNLP** | ~200 | NLP | **high** | ACL Anthology |
| 7 | **AAAI** | ~190 | AI (general) | med–high | DBLP |
| 8 | **IJCAI** | ~140 | AI (general) | med | DBLP |
| 9 | **NAACL** | ~130 | NLP | high | ACL Anthology |
| 10 | **KDD** | ~140 | Data mining | low–med | DBLP |

Notes: **SIGMETRICS** (Erfan named it) is systems/performance-measurement — not topically aligned with this thesis, so it is *not* in the relevance-weighted core; can be swept for completeness if asked. Neuro-AI-native venues (CCN, CogSci, *Nature Neuroscience/Communications*) are where much brain-LM work actually lands but are **not "top-10 AI"** — tracked as a secondary relevance pool because they hold the closest prior art, not as acceptance targets.

---

## 6. The idea tree — hierarchy by *solution altitude* (P4)

The tree's root is the thesis bet; layers descend by **how fundamental the choice is** (a "solution altitude" — the higher the layer, the more it re-frames the problem rather than tweaks a method). This beats a flat "topic" grouping because the climb instruction ("start from the highest untested layer") then means "attack the most fundamental untested reframing first," which is where venue-worthy novelty lives.

Proposed layers (refined by critique in P4):
- **L0 root:** the LM↔brain linear map as a *usable training signal*, not just a measurement.
- **L1 — what is the signal?** (real? E[Y|S] vs residual? which modality — fMRI/MEG/EEG/behavior?)
- **L2 — what do we *do* with it?** (match it / use as regularizer-prior / use as selection / use as proxy)
- **L3 — how do we induce it?** (distillation / full-FT / contrastive / CKA-obj / OT; LoRA vs full; readout family)
- **L4 — how do we *measure success*?** (encoding R² / OOD-ppl / robustness / calibration / sample-eff / compositional)
- **L5 — leaves:** concrete experiments (the E-nodes), each tagged tested ✅ / null ❌ / untested ⬜, mapped to the ladder.

The tree file: `docs/idea-tree.md` (built in P4, machine-readable node table + a rendered view). Every node carries: id, layer, claim, status, evidence (E/L refs), prior, and "assumption it rests on." Climbing = pick the highest-altitude ⬜ node whose parent holds, design it, run it, panel it, record it, then re-examine whether the result spawns/prunes nodes.

---

## 6b. Path-A contribution claim (the premortem's pre-GPU gate — written BEFORE the Moussa run)

**The claim, stated honestly.** Brain-guided training of language/speech models is increasingly reported to improve both brain-alignment *and* downstream task performance (Moussa'25, Negi'25, Bilgin'26, Schwartz'19). These gains are confounded: the brain-tuned model is compared against an *un-tuned pretrained baseline*, so any benefit of fine-tuning on an equally-informative *non-brain* target is misattributed to the brain signal — and few add a permuted-brain control on the *downstream* metric (Moussa's permuted arm is encoding-only, and is dead code in the NeurIPS repo). We propose a minimal control protocol — a **quality/perplexity-matched fine-tuned twin** + a **permuted-brain twin** — and show that across (i) our own controlled distillation work (the E005→E008 averaging collapse: apparent +0.0081 brain-specific gain → +0.0001 per-subject), (ii) a re-analysis of Negi'25 (text-LM, encoding half, on-paper), and (iii) a re-run of Moussa'25 (speech, multi-participant, with the matched twin we add), the brain-*specific* increment shrinks substantially or vanishes.

**Honest tier + the lift to main-track.** As a *purely negative* multi-target protocol this is **Findings/workshop-tier** (premortem #1: "correcting others" ≠ "new method"; the Moussa speech-substrate from a text-LM thesis is a coherence risk). The credible path to **main-track** is to make it *constructive, not just destructive*: pair the protocol with a regime where a brain-specific gain **does survive** the control — which is exactly what **T1.3** (non-fMRI signal) would deliver if it works. So Path A and Path B unify: the protocol that re-prices the field's confounded gains *plus* the one regime where a real gain survives = a main-track-shaped story. If T1.3 produces no survivor, Path A ships as a strong Findings/workshop paper and the thesis floor (R08–R14) is the priority. **This is the explicit gate:** run TA.4 to establish the negative across substrates; do NOT over-invest past Findings-tier on the negative alone unless T1.3 gives it a positive to stand on.

### THE SYNTHESIS (the paper, after the T1.3 lit-gate — S22)
The two paths collapse into one coherent contribution: **"Cognitive signals don't teach a language model anything its own surprisal doesn't already know."** The mechanism the T1.3 gate surfaced explains *all* our nulls at once: fMRI E[Y|S], reading-times, and N400 are all largely *predictable from the model's own surprisal*, so optimizing toward them is **circular** — you tell the model what it already knows, and the representation doesn't move (the ~0 fulcrum). The novel, unifying methodological move is **surprisal-residualization**: strip the surprisal-predictable component from the cognitive target and ask whether the *residual* buys anything downstream, under a permuted-twin + matched-budget control. Demonstrated across three modalities (fMRI = our work + Moussa; behavioral = reading-times; EEG = N400), this is a *general* claim, not an fMRI footnote. **A null is the stronger negative (main-track-shaped); a surviving residual arm is the positive that secures main-track.** E021 (T1.3) is the keystone experiment that delivers either way; TA.4 (Moussa) is the external-validation arm of the same protocol.

## 8. S24 EVOLUTION — the privileged-information / sample-efficiency trajectory (Erfan-directed, S24)

**The reframe (grounded, not a reset).** Stop scoring the static encoding-R² metric (the L4-monoculture) and ask: **does the brain/biosignal signal, used as train-only PRIVILEGED INFORMATION (LUPI), let an LLM learn with less data / generalize better** — measured on the LEARNING CURVE. Continuity catch (red-team): this *is* the charter's original **F2** (R03 §4 / R04 §8 / H001), returned to with three things it lacked — a theory (LUPI), higher-SNR regimes, and a control battery that catches the shape-artifact that fooled us at E021-v4. Everything prior stands as the foundation + rigor.

**LUPI, honestly (counter-argument + Codex).** Lopez-Paz 2016 / Vapnik: train-only information *can* lift the learning rate $O(1/\sqrt n)\to O(1/n)$ — **only when it is low-noise + hypothesis-space-reducing.** Weak fMRI (6–9 orders below text; trainable part ≈ $\mathbb E[Y\mid S]$) likely violates that ⇒ for fMRI, LUPI predicts the null (= R03's PAC-Bayes bound). So LUPI is **the bound to beat**, not a promise; the win lives only in higher-SNR / non-fMRI / deep-per-subject regimes. Digest Provodin'24 (LUPI gains can be artifacts → zeroed-PI control mandatory).

**The control battery (predeclared; the contribution even under a full null; run cheapest-first):**
1. **Phase-randomized shape-twin** (E021's killer — beat your own shape or it's a shape artifact).
2. **Zeroed / shuffled-PI** (Provodin TRAM; Pirlot shuffled-label).
3. **Did-the-representation-move gate** (L042 — a ppl-preserving no-op is "no manipulation," not evidence).
4. **Matched-perplexity + per-subject + crossed fold/subject clustering** (inherited rigor).
5. **Matched-information non-brain privileged teacher** (Codex — the load-bearing one): the real biosignal must beat the *best non-brain* privileged teacher (LM surprisal / teacher-hidden-state / difficulty), matched for capacity + reliability. Only this shows a gain is *biosignal-specific*, not "any teacher helps."

**TIER 1 — close EVERY open experimental + theoretical door (WORKING-session; "there is no later," Erfan).** Explicitly NOT the analysis-lane reports R08–R14 or the manuscript number-fixes (Erfan's analysis lane, D011). fMRI-free proxy (O4/T2.3) EXCLUDED — unrelated (Erfan). Run-list:
- **E023a–f** — KD objective-vs-quality identification.
- **O1/T3.4/F3** — denizenslab n=6 full-FT.
- **O2/T3.5** — TRIBE Phase-3 synthetic dense targets at KD scale.
- **O3/F4** — E015 Q2 architecture-residual (≥3 Llama/Mistral sizes + base-vs-instruct at matched bpb).
- **T3.3** — untested objective families (optimal transport / RSA-loss / CKA-at-scale).
- **The deferred THEORY / PROOFS + the "argued-shut by intuition, never measured" nodes:** **T2.2/O6** — brain-as-regularizer / selection prior: *measure* the L041 side-channel, don't argue it; **the A-ceiling assumption $Y\perp\theta^\*\mid S$** — test/bound it rather than assume it; and any claim we asserted-but-never-proved.
- Instrument-limited items (F3 etc.): record the **MDE-vs-effect check** honestly; do not dress a noisy null as a verdict.

**TIER 2 — the 5 method ideas + anything found while working; do it complete.**
1. Weak-signal handling (uncertainty-weighted aux loss, Kendall'18; regularizer/curriculum/selection).
2. fMRI denoising → raise the noise ceiling (GLMsingle, Prince/Kay'22; reliable-component / $\mathbb E[Y\mid S]$ projection).
3. TRIBE synthetic-fMRI at corpus scale (DPI caveat; claimable only with the zeroed/shape controls).
4. Relational / geometry distillation (RKD Park'19; Tung & Mori'19 — distill the brain similarity matrix).
5. Right benchmarks (learning-curve / sample-efficiency, robustness, calibration, compositional, agentic).

**TIER 3 — the 3 paths.**
- **P1 (decisive, Codex-sharpened):** **ZuCo-first** (EEG+eye-tracking), **supervised low-data fine-tuning**, across a learning curve; real PI must beat ALL 5 controls incl. the text-teacher *and* pass the rep-move gate; **CNeuroMod** (~80h/subject) is the fMRI follow-up. Differentiation from Hollenstein/ZuCo prior art: LLM middle-layer geometry + the LUPI learning-curve estimand + the full control battery they lack.
- **P2 (future-work, quarantined):** biosignal → low-data control / robotics. Never a claim the thesis evidence supports.
- **P3 (modality expansion):** EEG/MEG/ECoG/behavioral via Broderick'18, Brennan-Hale, MEG-MASC.

**Datasets to acquire:** ZuCo 1.0/2.0 (top), CNeuroMod, Broderick'18 EEG, Brennan-Hale "Alice" EEG, MEG-MASC; NSD (GLMsingle reference; vision caveat). **paper-digest:** Provodin'24, Lopez-Paz'16, Hollenstein'19/21.

**Prior art / positioning:** closest = Hollenstein/ZuCo (gaze+EEG→NLP, train-only PI — partial scoop + existence proof); CONFIRM we already hold = Freteault'25 (brain-aligned → downstream, *biggest gains on smallest training sets*; its missing matched-non-brain control is our opening).

**Calibration (all three critics converge):** most likely = a strong multi-modal methodology/negative paper (the control battery IS the contribution); a top-venue *positive* is the tail (needs real PI to beat shape + zero + shuffle + text-teacher *and* move the rep *and* bend the curve). Run it as **a methodology paper with upside**; headline deferred to results (Erfan).

**Process:** estimand-first + predeclared kill + the 5-control battery + oracle + thinking panel + Codex per node; matched-ppl + anti-confound (L003) inherited; living tree (branch on results); **rungs flip only on Erfan.**

## 7. Log (append-only; one line per program step)
- **2026-06-17 (S22 start):** Goal set. P1 done (analysis from docs). Inventory grounded (40 notes, 22 repos, E001–E020). Venue list locked. Conference-scout architecture decided (DBLP backbone). Network/APIs probed live. This tracker created.
- **2026-06-17 (S22):** Built `idea-tree.md` (solution-altitude hierarchy) + `litsweep-relevance.md` (sweep taxonomy + digest rubric). Launched conference-scout builder (sonnet, bg) + lit-scout for O5 (opus). **Lit-scout result:** Path-A external target locked — lead = Moussa'25 multi-participant brain-tuning (NeurIPS, clone-and-run repo), companion = Negi'25 (text-LM, on-paper); **no new undiscovered positive exists** (the value is ranking-for-attack). Feasibility gate (Moussa clone-and-run on 4× L40S) launched. gbrain page `projects/brain-alignment-expansion-program` written.
- **2026-06-18 (S23) — B (E022 Moussa Path-A demonstration) PILOT = NON-REPRODUCTION → STOP.** Oracle-gated into a cheap reproduction pilot first (HOLD on the full design: circular matched-quality, learnability confound, no pretrained arm, checkpoint mismatch, TIMIT missing). Pilot (TIMIT acquired, both arms from pretrain, single-subject UTS03 ×24 stories, 3 seeds): brain−pretrained phoneme-F1 = +0.52 [−0.36,+1.40], below the +2 gate → Moussa's downstream gain does NOT reproduce on our data → the matched-twin shrink-test is vacuous, NOT built. Honest scope: non-reproduction in a reduced setup, NOT a refutation. **Net: Path-A's external "main-track lift" is off the table on our data; the negative paper rests on our own evidence + this honest non-reproduction note.** `scripts/e022_pilot.py`, `outputs/e022/pilot_results.json`. No rung flip.
- **2026-06-18 (S23 — DEFINITIVE, supersedes all E021 lines below) — E021 KEYSTONE RESOLVED → CLEAN NULL on cognition.** Erfan directed A (resolve E021 cleanly) + B (Path-A Moussa). A ran to completion: n=10 + learnability-matched controls → v4 looked like a positive (human RT beats all controls incl. another LM's surprisal, below the learnability trend) → BUT a panel + a **phase-randomized shape-matched control** showed the edge is the target's temporal/distributional SHAPE (RT autocorr 0.62 + kurtosis 13), not cognition: a content-free shape twin TIES the residual (172.1 vs 177.4). So: surprisal-orthogonality null, generic regularization dominant, and the RT advantage = signal shape not content. **Clean cross-modal NEGATIVE** (extends E008 to behavioral RT, mechanism pinned) — strengthens Path A; the main-track positive did NOT materialize. New scripts `run_e021_v{4,5}.py` + `analyze_e021_v4_learnability.py`. No rung flip. (Honest arc: v2 bug-positive → v3 inconclusive → v4 likely-positive → v5 clean-null; each step corrected the last — the rigor chain worked.)
- **2026-06-17 (S22, CLEAN v3 — superseded above) — E021 KEYSTONE RESOLVED → INCONCLUSIVE at n=3.** After Codex caught a real harness bug, the clean rerun changed the answer: the v2 "triple-dissociation positive" was a bug artifact, but it did NOT become a clean negative either. Trustworthy verdict: surprisal-orthogonality is **NULL** (raw≈residual — the specific novelty buys nothing), generic regularization dominates (~450 AULC gap), and the broader cognition question is **underpowered** (residual best on mean but CIs touch 0; the log-freq exclusion control is confounded by learnability). The main-track positive did NOT materialize; the *clean* negative is only the narrow surprisal-orthogonality one. **Process lesson:** I flip-flopped (v2 bug-positive → over-strong DPI "refutation" → inconclusive) — the rerun discipline got us to the honest answer, but I over-read twice. Erfan adjudicates: resolve-it experiment (more seeds + learnability-matched control) vs. fold the narrow negative into Path A.
- **2026-06-17 (S22) — [SUPERSEDED by the line above] E021 KEYSTONE RESOLVED → NEGATIVE; the main-track bet did not land.** G2v2(frozen-probe) PASS → 5 arms fired the triple dissociation, but counter-argument + first-principles + Codex converge: **cognition reading refuted.** raw≈residual ⇒ surprisal-orthogonality null (**DPI-mandated**: residual is a function of raw+surprisal, can't exceed raw); ~91% of the effect is generic word-aligned regularization (E004 `frozen` at scale, MI-bound-consistent); Codex found a real pad-label bug + control flaws → numbers need a clean rerun, but the verdict is theory-robust. **This is a clean cross-modal NEGATIVE** (cognitive signals buy nothing beyond generic regularization, now shown on behavioral RT) that **strengthens the Path-A negative paper** — NOT the main-track positive the keystone hoped for. **STRATEGIC FORK for Erfan** (cost-critical): consolidate the negative (Findings + thesis) vs. keep hunting a main-track positive (paradigm looks exhausted). No rung flipped.
- **2026-06-17 (S22) — E021 G0/G1 GATE = PASS (keystone viable).** Natural Stories RT (180 subj, 10k words, on disk): surprisal-orthogonal residual split-half reliability **0.72** ≈ noise ceiling **0.77** → reliable structure, not noise. unique-R²(surprisal in RT)=0.048 (LM explains little of RT). Caveats recorded: reliable≠downstream-useful (G2 decides), and the circularity worry was overstated for RT. → building the aux-training + AULC harness + G2 downstream power positive-control before the 6 arms. `scripts/run_e021_g0g1.py`, `outputs/e021_g0g1/`.
- **2026-06-17 (S22) — E021 designed → oracle HOLD → addressed; lit + tooling landed.** Oracle (opus) HOLD on E021 with 4 must-fixes, all encoded: predeclared MDE + downstream power positive-control (G2), residual-reliability floor (G1 — vacuity guard, the E016 trap), train-fold-only residualization (anti-leakage), and an added **random-structured arm** for a triple dissociation (residualized > permuted AND > random — the E004 `frozen` guard); AULC primary metric; EEG demoted to stretch. **Gating sequence G0→G1→G2 runs before any science arm** — G0 (cheapest) = residual unique-R² of human reading-time beyond base-LM surprisal on a clean corpus; if ≈0 the keystone is vacuous → kill/pivot. **Digests:** Deng'24 (its shuffle control gives +0.33pp → supports our prior) + BabyLM (cognitive aux ≈ randomized-order null; nobody residualized → E021's gap) — both canonical. **Conference-scout BUILT + proven** (`scripts/litsweep/`: DBLP 3540 NeurIPS'23, OpenReview 2260 ICLR'24 w/ abstracts+PDFs) — reusable asset, not blocking the climb. Launched G0/G1 vacuity gate.
- **2026-06-17 (S22) — STRATEGY PREMORTEM (opus) → major re-sequence.** Verdict (verified vs ladder): most Path-B metric nodes (T4.3/4/5) are structural nulls (fulcrum ~0 at matched ppl → frozen rep); T2.2 ≈ the E004 `frozen` arm relabeled; the **one** mechanically-viable new-positive is **T1.3 (non-fMRI signal)**; Path A is Findings-tier as a one-target speech takedown; the sweep-first ordering is procrastination; the thesis floor (R08–R14) is at risk. **Actions:** killed T4.3/4/5, demoted T2.2, promoted T1.3 to lead Path-B; re-sequenced to run load-bearing experiments before scaffolding; wrote the honest venue-bar recalibration (Findings/workshop floor; top-10 main-track conditional on a T1.3 survivor) and the Path-A contribution claim (§6b). **Moussa feasibility = GO-WITH-CAVEATS** (repos cloned, fMRI present, ~35-45 GPU-hr; blockers = story-audio/grids from an Antonello Box link + reimplement the permuted arm). Launched: T1.3 main-track lit-gate (opus) + TA.4 data-acquisition (sonnet).
- **2026-06-18 (S24) — EVOLUTION FOLDED IN (§8).** Erfan directed the **privileged-information / sample-efficiency** reframe. Critique loop ran (counter-argument + lit-scout + Codex): LUPI demoted to *the bound to beat*; the **5-control battery** (shape-twin + zeroed/shuffled-PI + rep-move gate + matched-ppl + matched-information non-brain teacher) is the contribution; **P1 = ZuCo-first supervised low-data learning curve**. Tier 1 = close every open experimental + theoretical door (fMRI-free EXCLUDED; reports/manuscript stay analysis-lane). Datasets: ZuCo / CNeuroMod / Broderick / Brennan-Hale / MEG-MASC. paper-digest: Provodin'24, Lopez-Paz'16, Hollenstein. Calibration: methodology paper most likely, positive = tail. No rung flip. Full spec §8; nodes in `idea-tree.md`.
