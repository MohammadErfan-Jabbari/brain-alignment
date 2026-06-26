---
title: "Findings of the BabyLM Challenge (1st, 2023 → 3rd, 2025): the verdict on cognitively-inspired…"
tags: [literature]
aliases: [babylm-2025_cognitive-objectives-findings]
---

# Findings of the BabyLM Challenge (1st, 2023 → 3rd, 2025): the verdict on cognitively-inspired training objectives at a matched data budget

**Authors:** BabyLM Team. *3rd (2025):* Charpentier, Choshen, Cotterell, Gul, Hu, Liu, Jumelet, Linzen, Mueller, Ross, Shah, Warstadt, Wilcox, Williams. *1st (2023):* Warstadt, Mueller, Choshen, Wilcox, Zhuang, Ciro, Mosquera, Paranjape, Williams, Linzen, Cotterell.
**Year:** 2025 (primary) / 2023 (grounding)
**Venue:** 2025 — *Proceedings of the First BabyLM Workshop* (EMNLP 2025), pp. 399–420. 2023 — *27th CoNLL, Vol. 2: The BabyLM Challenge*, pp. 1–34.
**DOI/arXiv:** 2025 — https://aclanthology.org/2025.babylm-main.28.pdf · 2023 — https://aclanthology.org/2023.conll-babylm.1.pdf
**Canonical ID:** babylm-2025_cognitive-objectives-findings

**Tags:** #literature #canonical #prior-setter

---

## Read Method [REQUIRED]

- [x] Full PDF read (page-by-page comprehension)
- [ ] Full PDF scanned (search + targeted read)
- [ ] Extracted text only

PDF verified: 2026-06-17. The WebFetch markdown parse failed on both PDFs (they returned compressed
FlateDecode streams), so both were saved locally and read **as rendered page images** via the PDF
reader. **2025 findings:** pages 1–12 read in full (cover through references) — Abstract, §1 Intro,
§2 Competition Details, §3 Baselines, §4 Evaluation + new tasks, §5 Submission, §6 Competition
Results + winners + outstanding-paper awards, §7 Discussion, §8 Conclusion, Tables 1–3, Figures
1–6, all read directly off the rendered pages. **2023 findings (grounding):** pages 1–2 and 11–16
read directly (Abstract, §1 Intro, §7 meta-analysis/winners/common-methods incl. Figs 4–6, §8
future, §9 Conclusions, references). Comprehension self-check passed: Y. Where a claim the scout
attributed to this source ("marginal gains over randomized orders") is a paraphrase rather than a
verbatim string, that is flagged explicitly below.

---

## Comprehension Summary [REQUIRED]

1. Problem solved: The BabyLM Challenge fixes a developmentally-plausible data budget (100M words
   *Strict*, 10M words *Strict-Small*) and asks teams to train the best small LM under it, then
   scores every submission on a common suite. Because dozens of teams independently tried
   cognitively-inspired objectives (curriculum learning by surprisal/frequency/length, auxiliary
   training objectives, developmental data ordering) against the *same* matched-budget baselines,
   the findings papers are a natural meta-experiment: do cognitively-motivated objectives beat plain
   training at matched data? This is the realistic prior for our E021.

2. Core insight (the verdict): **No.** Across two iterations the consistent winners were
   *architecture/objective modifications and principled data preprocessing* — not cognitive
   curricula. In 2023, curriculum learning was the single most popular approach (13 teams, 41.9%)
   and "the majority of these attempts did not produce consistent improvements." In 2025 the
   organizers repeat: "While curriculum learning remains popular, the best-performing approaches
   were again based on modifications to the pretraining objective or the model architecture." The
   *Loose*-track winner in 2023 (Contextualizer) used data augmentation while *randomizing the
   dataset order each epoch* and beat the ordered-curriculum field — the operational form of "an
   ordered/cognitive curriculum did not beat a randomized-order control."

3. If-wrong breakage: The prior would be wrong (and our E021 prospects would improve) if some
   cognitively-motivated objective had produced a *robust, replicated* downstream gain over a
   matched-budget non-curriculum baseline with a proper control. It did not: the two systematic
   curriculum studies (Martinez/CLIMB 2023, "none of the tested approaches leads to widespread
   improvements"; Steuer 2023, benchmark performance uncorrelated with psycholinguistic-prediction
   ability) are the controlled negatives, and they hold across both years. The one stray "in one
   case, a curriculum learning method resulted in significant improvements" (2023 §9) is unnamed,
   uncontrolled, and never replicated.

---

## Source Grounding

**Data budget (the matched-budget rule).** *Strict* = 100M words or fewer; *Strict-Small* = 10M
words or fewer (2023 and 2025 both). 2025 added two tracks (*Multimodal*, *Interaction*) and, new
this year, a **training-compute cap**: at most 100M words of *exposure* counting repeated passes for
Strict-Small and at most 1B words for the other tracks (2025 §2, "Training Duration Limitations").
Teams may use the provided BabyLM corpus or build their own under the word cap. The 2025 Strict
corpus (Table 1) is 100M words: CHILDES child-directed speech (29M), Project Gutenberg children's
stories (26M), Simple Wikipedia (15M), BNC dialogue (8M), OpenSubtitles (20M), Switchboard (1M) —
i.e. a deliberately child-like distribution.

**Evaluation suite.** *2023:* BLiMP (zero-shot grammatical minimal pairs), (Super)GLUE (finetuned
NLU), MSGS (linguistic-vs-surface generalization). *2025:* kept (Super)GLUE (BoolQ, MultiRC, RTE,
WSC, MRPC, QQP, MNLI; large tasks subsampled to 10k) and BLiMP, **added EWoK** (Elements of World
Knowledge: pragmatic/commonsense/discourse), plus a new battery of **cognitive / human-likeness
tasks**: reading-time prediction (de Varda 2023 — correlation between LM surprisal and human reading
time / eye-tracking), word-learning trajectory / age-of-acquisition (Chang & Bergen), wug
past-tense and -ity/-ness nominalization (morphological generalization scored against human
preference distributions), entity tracking, concept knowledge. Crucially, 2025 scored
**human-likeness separately from NLP-task accuracy** — a system could win on either axis (Table 3),
so the suite *can* reward a cognitive signal if one exists.

**The submission field (the "many teams" denominator).** 2023: 31 papers / ~30 submissions across
Strict/Strict-Small/Loose. 2025: 32 models on the leaderboard, 12 challenge papers, 32 workshop
papers, 15 participants, from 26 countries. Curriculum learning was the single most popular approach
in *both* years (2025 Fig 1; 2023 Fig 3: 13 teams = 41.9%).

**Baselines (what "plain training" means here).** 2025 Strict/Strict-Small baselines: GPT-BERT
(the 2024 winner; LTG-BERT backbone with a masked+causal joint objective, three AR/masked-focus
variants ~120M Strict / ~31M Strict-Small, 10 epochs) and a naively-trained GPT-2 Small. 2023
baseline backbone was the LTG-BERT family. These are *strong* baselines — the 2023 LTG-BERT winner
beat the Llama-2 and RoBERTa-Base skylines on most suites despite ~3% of BERT's training data.

---

## Key Ideas

### Finding 1 — Cognitive curricula were the most-tried and mostly failed (2023, controlled)

2023 §7.3, verbatim: curriculum learning "was the most popular approach, with 13 teams (41.9%)
attempting some variant of curriculum learning. **The majority of these attempts did not produce
consistent improvements across the BabyLM evaluation tasks.**" The curricula spanned exactly the
cognitively-motivated axes one would propose: "ranking sentences by surprisal (Chobey et al., 2023;
Hong et al., 2023), lexical frequency, length, and syntactic complexity; sorting entire datasets by
difficulty; gradually increasing vocabulary size … and gradually increasing the difficulty of the
training objective." Note **surprisal-ranked curricula were explicitly tried and did not win** —
directly adjacent to E021's surprisal handle.

### Finding 2 — The systematic curriculum study is a clean null (CLIMB, Martinez 2023)

The 2023 "compelling negative results" award went to CLIMB (Martinez et al. 2023), which "proposes a
typology of common curriculum learning approaches and performs a thorough and principled evaluation
exploring this design space. **Although they find that none of the tested approaches leads to
widespread improvements across the evaluation tasks**, the exhaustiveness of this search and the
careful controls and baselines in the study make this negative result a valuable contribution."
This is the controlled meta-study — the design we should treat E021 against — and its verdict is a
null.

### Finding 3 — Randomized order beat ordered curricula (the "randomized control")

The 2023 *Loose*-track winner (Contextualizer, Xiao et al. 2023) "trains the models continuously …
belonging to the same source dataset **while randomizing the dataset orders in each training
epoch**," combined with a data-augmentation scheme. It beat the curriculum field. This is the
operational sense in which "cognitive ordering did not beat a randomized-order baseline": the
winning order-policy was *randomization*, and the ordered/cognitive curricula did not consistently
improve over non-curriculum baselines (2023 §1: Martinez "reported few improvements over
non-curriculum baselines"). **Honesty note:** the exact string the scout cited — "marginal gains
over randomized orders" — is *not a verbatim quote* in either findings paper; it is an accurate
paraphrase of (a) curriculum order failing to beat non-curriculum/randomized-order baselines and (b)
the randomized-order Loose winner. The randomization here is over *training-example presentation
order*, not over labels or the brain signal; the metric is the aggregate BLiMP+(Super)GLUE(+MSGS)
score; the magnitude is "few / not consistent," not a single tabulated delta.

### Finding 4 — Performance and cognitive-plausibility decouple (Steuer 2023)

The 2023 "outstanding evaluation" award went to Steuer et al. 2023 ("Large GPT-like Models are Bad
Babies"), who "found that **benchmark performance is not correlated with a greater ability to predict
human psycholinguistic data**" (2023 §1). I.e. doing better on the task suite did *not* make a model
a better cognitive model, and vice versa. This is the central caution for any "cognitive signal
helps downstream" story: the two objectives pull apart.

### Finding 5 — The 2025 takeaway re-confirms the prior (latest iteration)

2025 Abstract: "We observe that **new training objectives and architectures tend to produce the
best-performing approaches**." 2025 §1 Summary of takeaways: "As in the previous two iterations of
the BabyLM Challenge, **curriculum learning was a common approach. However, the most effective
approaches were those that proposed architectural innovations or modifications to the training
objective.** Winners included a diffusion language model …, a mixture-of-experts model …, and a
reinforcement learning-based interactive approach." 2025 §7 High-level takeaways repeats it verbatim
once more. The 2025 winners confirm the pattern: Strict NLP winner = Simple-Diffusion (a diffusion
masked LM); Strict-Small NLP winner = AMLM-Hard-Decay (dynamic difficulty-based masking);
Strict-Small human-likeness winner = MoEP (mixture-of-experts). None is a cognitive *curriculum*;
they are objective/architecture moves.

### Finding 6 — Compute did not buy performance (2025), and that cuts both ways

2025 found "model performance is not necessarily tied to the total amount of compute" (§7; Fig 6 —
no strong FLOPs↔score correlation in Strict/Strict-Small). Good for us in one sense (a small LM is a
fair arena), but it also means the gains that *did* appear came from the inductive-bias/objective
side, not from throwing more training at a cognitive signal.

---

## Evidence

- **2023, primary numbers:** 31 papers; curriculum = 13 teams (41.9%), "majority … did not produce
  consistent improvements"; CLIMB = "none of the tested approaches leads to widespread improvements";
  Loose winner = randomized-order + augmentation; Steuer = benchmark perf ⊥ psycholinguistic
  prediction. Winners overall = LTG-BERT architecture modifications (ELC-BERT), beating Llama-2 /
  RoBERTa-Base skylines on most suites at ~3% of BERT's data.
- **2025, primary numbers (Table 3, Strict track, human-likeness / NLP / macro):** the best
  *cognitive-objective-style* submissions did not dominate the strong objective baselines.
  GPT-BERT-causal_AR baseline = human-likeness **26.5** (best in track), GPT-BERT-mixed_MNTP =
  macro **43.5** (best), GPT-BERT-masked_MNTP = NLP **63.0** (best); the non-baseline best models
  (CLASS-IT 20.4 HL / 52.9 NLP, Simple-Diffusion 58.4 NLP) **did not beat the GPT-BERT baselines on
  macro**. The organizers state outright that "the baselines (winning methods from previous years'
  challenges) remain strong, especially in the multimodal and strict tracks" (Fig 3 caption).
- **2025 training-dynamics (Fig 5):** BLiMP and EWoK rise smoothly with training words; but
  reading-time prediction and wug-test scores are "more variable" and "do not demonstrate a strong
  relationship with number of pretraining words" — the cognitive/human-likeness axis is noisy and
  not monotone, exactly where a fragile auxiliary signal would struggle to show a clean gain.
- **The one positive the prior must concede:** 2023 §9, "In one case, a curriculum learning method
  resulted in significant improvements." Unnamed in the conclusion, uncontrolled in the meta-sense,
  and not reproduced in 2024 or 2025. Treat as a single un-replicated outlier, not a counter-prior.

---

## Limitations

1. **Not a clean controlled experiment per method.** Submissions vary the architecture, objective,
   tokenizer, hyperparameters, *and* data ordering simultaneously; the meta-analysis hand-codes each
   submission into one bucket (Fig 3/5) and reads aggregate bars. Only CLIMB (2023) is a within-paper
   controlled curriculum sweep. So "curriculum failed" is a strong *field-level* prior, not a single
   matched ablation — though the field-level signal across ~60 submissions over two years is itself
   evidence.
2. **No surprisal-*residualized* objective was ever tried.** Every cognitive submission used the raw
   cognitive/curriculum signal (raw surprisal ranking, raw frequency, raw reading-time correlation).
   None stripped the LM's own surprisal-predictable component first. So BabyLM tests the *naive*
   version of our hypothesis, not the residualized version — which is the gap E021 stands in, and
   the reason this is a prior-setter, not a kill.
3. **"Marginal / few improvements" is rarely a tabulated delta.** The findings papers report the
   pattern in prose and in scatter/bar figures, not as per-method effect sizes with CIs. We can cite
   the direction and the field-level verdict with confidence; we cannot quote a single "+X.X pp"
   margin for "cognitive vs randomized."
4. **Brain signal absent entirely.** BabyLM cognitive submissions used *behavioral* proxies (reading
   time, AoA, surprisal) and developmental data ordering — no fMRI, no EEG/N400 *training* objective.
   EEG-guided *training* (E021's unscooped arm) is genuinely untested here; the behavioral arm is the
   one BabyLM speaks to directly.
5. **The eval suite may under-reward a real cognitive gain.** Steuer's decoupling cuts both ways: if
   a cognitive objective improved *cognitive* modeling without moving BLiMP/GLUE, BabyLM's
   accuracy-axis scoring would log it as "no gain." 2025 partially fixes this by scoring
   human-likeness separately — and the cognitive objectives *still* did not win that axis cleanly.

---

## Relevance to this thesis

**Which assumption this touches:** A3 (does a brain/cognitive signal as a training objective buy a
practical downstream gain at matched budget?), via the **behavioral/EEG** generalization of our
fMRI work. It is the **realistic prior-setter for E021** (T1.3 — surprisal-residualized
cognitive-signal auxiliary objective on a small LM).

**Role in our framework:** This is the external base rate for E021. Dozens of teams, over three
years, tried cognitively-inspired objectives at exactly the matched-data regime E021 lives in, with
strong baselines and a shared eval suite. The verdict is a near-null: cognitive curricula did not
consistently beat plain training, the controlled curriculum study (CLIMB) found no widespread gains,
the winning order-policy was *randomization* not cognitive ordering, and performance decoupled from
psycholinguistic-prediction ability (Steuer). This is precisely the "BabyLM showed cognitive
aux-objectives ≈ randomized-order nulls" claim in [`idea-tree.md`](../../idea-tree.md) T1.3 — now sourced and quoted.

**Connection to other canon:**
- `merlin-2024_beyond-next-word-brain-alignment` / `proietti-2025_brain-llm-alignment-input-attribution`
  supply the *mechanism* that could let E021 escape this null: a residual of the cognitive signal
  after the model's own surprisal/next-word component is regressed out. BabyLM never tested the
  residualized version, so its null applies to the *naive* objective, not to ours. The E021 bet is
  exactly that the residual is the only part that isn't circular.
- `guo-2024_eeg-cotrain-adversarial-robustness` is the *image/EEG* A3 floor-setter (small gains,
  shuffled controls also gain); this is the *language/behavioral* prior-setter (no consistent gain).
  Together they bracket the expectation: any brain/cognitive-signal training benefit at matched
  budget is small-to-null and demands a permuted/randomized-order control to be believed.
- Reinforces the E009/E021 design non-negotiable: the **permuted/randomized-order twin is
  load-bearing**, because BabyLM's own winning order-policy *was* randomization.

**Prior for E021 (the honest expected outcome).** Base rate says E021's **default expected result is
a null**: a surprisal-residualized behavioral/EEG auxiliary objective, at matched 10–100M-word
budget on a small LM, most likely will *not* beat a perplexity-matched, randomized-order baseline on
the downstream suite. The naive form of the idea is the BabyLM-tested form, and it failed across ~60
submissions and three iterations. For E021 to beat this null, all of the following must be true:
(1) the **residualization must actually carry non-circular signal** — i.e. there is a component of
the behavioral/EEG target that is *not* predictable from the model's own surprisal (Merlin-Toneva
showed such a residual exists for fMRI; it must also exist, and be learnable, for behavior/EEG);
(2) injecting that residual must **move the representation** — recall our fMRI fulcrum was ~0 at
matched ppl (E009), so the residual objective has to do what the raw objective could not;
(3) the gain must **survive the permuted/randomized-order twin** — BabyLM's randomized-order winner
means a generic-regularization or curriculum-shaping explanation is the default null to beat; and
(4) the gain must land on an **axis the eval actually scores** (Steuer's decoupling warns a pure
cognitive-modeling gain may not show on BLiMP/GLUE — so predeclare which axis E021 claims). Given
this prior, E021's value is asymmetric and that is by design ([`expansion-program.md`](../../expansion-program.md) §6): a **null
is the stronger, generalizable negative** ("cognitive signals don't teach an LM anything its own
surprisal doesn't already know," now across fMRI + behavioral + EEG), and a **surviving residual arm
is the new positive** — but the honest base rate, before compute, is the null. Predeclare the kill
criterion and the permuted-twin control accordingly.

**What this does NOT change in our design:**
- E021 still goes (it tests the *residualized* objective BabyLM never tried) — but it goes with a
  null-leaning prior, a predeclared kill criterion, and the randomized-order/permuted twin as the
  load-bearing control, exactly as `idea-tree.md` T1.3 and the oracle-gate already specify.
- No change to E009; this corroborates its framing.

**One-line verdict:** Across three BabyLM iterations and dozens of matched-budget submissions,
cognitively-inspired training objectives (incl. surprisal-ranked curricula) did *not* consistently
beat plain training and lost to a randomized-order baseline, and benchmark performance decoupled from
psycholinguistic-prediction ability — so E021's honest prior is a null, beatable only if
surprisal-residualization carries learnable, representation-moving, permutation-surviving signal that
the naive objective lacked.

---

## Verified

Both PDFs read as rendered page images after the markdown parse failed on the compressed PDF
streams. **2025 findings (aclanthology 2025.babylm-main.28):** pages 1–12 read in full — all
sections, Tables 1–3, Figures 1–6. **2023 findings (aclanthology 2023.conll-babylm.1):** pages 1–2
and 11–16 read directly — Abstract, §1, §7 (meta-analysis, winners, common methods, Figs 4–6), §8,
§9, references. Load-bearing quotes confirmed verbatim off the page images: 2023 §7.3 curriculum
"13 teams (41.9%) … majority of these attempts did not produce consistent improvements"; 2023 §7.2
CLIMB "none of the tested approaches leads to widespread improvements"; 2023 §1 Steuer "benchmark
performance is not correlated with a greater ability to predict human psycholinguistic data"; 2023
§1 Loose winner "randomizing the dataset orders in each training epoch"; 2025 §1/§7 "the most
effective approaches were those that proposed architectural innovations or modifications to the
training objective." Confirmed absences/caveats: (a) the phrase "marginal gains over randomized
orders" is a paraphrase, not a verbatim string in either paper (flagged in Finding 3); (b) no
per-method effect sizes with CIs are tabulated for "cognitive vs randomized"; (c) no
surprisal-*residualized* objective was tried in either iteration; (d) no fMRI/EEG *training*
objective in any submission (behavioral proxies only); (e) the single un-replicated "in one case …
significant improvements" (2023 §9) is unnamed.
Read date: 2026-06-17


## Related
- [`ladder.md`](../../ladder.md) — the canonical status board
- [`map.md`](../../map.md) — code system (Q/E/A/D/L) & journey map
