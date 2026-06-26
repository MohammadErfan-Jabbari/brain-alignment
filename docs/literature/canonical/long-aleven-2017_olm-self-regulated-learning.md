---
title: "Enhancing learning outcomes through self-regulated learning support with an Open Learner Model"
tags: [literature]
aliases: [long-aleven-2017_olm-self-regulated-learning]
---

# Enhancing learning outcomes through self-regulated learning support with an Open Learner Model

**Authors / Year / Venue:** Yanjin Long; Vincent Aleven / 2017 (online 31 Dec 2016) / *User Modeling and User-Adapted Interaction (UMUAI)* 27(1):55–88 · **Link:** https://doi.org/10.1007/s11257-016-9186-6
**Canonical ID:** long-aleven-2017_olm-self-regulated-learning

**Tags:** #literature #canonical #pedagogy #teach-stance #teach-skill-grounding #not-brain-science #OLM #learner-control #SRL

---

## TL;DR

Two in-vivo classroom experiments (total **N = 301** 7th–8th graders) test whether adding a redesigned Open Learner Model (skill bars + self-assessment prompts) to the **Lynnette** linear-equation tutor improves equation-solving learning, crossed 2×2 with whether the student gets **shared control over problem selection** (PS). The result is **not a clean main effect of the OLM**: the small first experiment (N=56) found a significant OLM main effect (d=.56) and no interaction; the larger replication (N=245) found **no main effects but a significant OLM×PS interaction** (F(1,236)=7.535, p=.007) — the OLM raised procedural learning **only in the shared-control arm** (OLM+PS > noOLM+PS, F(1,236)=6.401, p=.012), and shared control **without** the OLM was actually *worse* than full system control. This is the primary-source warrant that opening the learner model helps **when it is wired into a learner-control regulatory loop**, not as a passive display. **Apparatus grounding for `/teach`, NOT thesis science** — no A1/A2/A3, no brain-alignment number, none of our datasets; keep it out of `docs/01-research-landscape.md`'s science tables.

## The system and the design (what was actually built)

**Platform.** *Lynnette*, an example-tracing ITS for solving linear equations (built in CTAT), used here for **five equation levels** (one-step → two-step → multi-step → parentheses → harder parentheses). It gives step-by-step correctness feedback, on-demand hints, and self-explanation drop-downs. Its built-in OLM is a **skill-bar** display (the Bull-et-al. modal OLM; college students in Bull et al. 2016 preferred simple skill meters over treemaps/radar). Mastery is tracked per knowledge component (KC) by **Bayesian Knowledge Tracing** with default Cognitive-Tutor parameters (the four parameters were *not* re-fit from data and the KC model was *not* refined); a bar turns gold at **95% mastery probability**.

**The redesigned OLM (the manipulation).** Three added features layered on the skill bars: (1) **self-assessment prompts** — three questions shown *one at a time* at the end of a problem, *before* the skill bars are revealed (so the student commits a self-judgment first, then sees the model — a predict-then-reveal structure); (2) **delayed/animated skill-bar update**, with a black line marking last-problem mastery so the change is salient as feedback on the self-assessment; (3) a **high-level progress summary** on the problem-selection screen.

**Shared control over problem selection (PS).** After each problem the student **chooses which of the five levels** to draw the next problem from; the system then picks the specific problem and **locks** any level once its skills hit the 95% BKT threshold. So control is shared and bounded: the learner picks the *level/path order* (blocked vs interleaved), the system picks the item and decides when a level is done. The noPS arm is system-controlled ordered blocked practice Level 1→5 (standard ITS practice).

**2×2 factorial, 4 conditions** (randomized within class): **OLM+PS · OLM+noPS · noOLM+PS · noOLM+noPS.** Procedure identical across arms: ~25-min paper pre-test, **five 41-min class periods on five consecutive days** with the tutor, immediate paper post-test (Experiment 2 added a 7-item 7-point enjoyment questionnaire adapted from the IMI). Dependent measures: procedural + conceptual test items (procedural graded 0–1 with partial credit, conceptual T/F 0/1); tutor-log process measures (problems, steps, incorrect attempts/step, hints/step); self-assessment accuracy (absolute-accuracy index = mean squared discrepancy between 1–7 confidence and actual performance, lower = more accurate); enjoyment (Exp 2 only).

## Key ideas (the five hypotheses and which held)

H1 OLM → better learning · H2 shared control → better learning · H3 OLM helps *more* under shared control (interaction) · H4 shared control → more enjoyment · H5 OLM → better self-assessment accuracy.

| Hypothesis | Experiment 1 (N=56) | Experiment 2 (N=245) |
|---|---|---|
| H1 — OLM main effect on learning | **Confirmed** (d=.56) | **Not** confirmed |
| H2 — shared-control main effect | Not confirmed | Not confirmed |
| H3 — OLM×PS interaction | Not confirmed | **Confirmed** (p=.007) |
| H4 — shared control → enjoyment | N/A (no questionnaire) | Not confirmed |
| H5 — OLM → self-assessment accuracy | Not confirmed | Not confirmed |

The two experiments **disagree on the form of the OLM benefit** — Exp 1 a main effect, Exp 2 an interaction — and the authors lean on the larger Exp 2: *"given the larger N of Experiment 2, we believe that the presence of shared control over problem selection may be key."* Their synthesized claim: *"The presence of shared control amplifies the effect an OLM can have in facilitating active self-assessing and reflecting, and together the two forms of support enhance domain level learning outcomes."*

## Evidence (datasets, metrics, headline numbers — all from the paper's tables)

**Sample.** Total **N = 301** (the abstract and intro say "302"; this is an off-by-one — the participants section and conclusion both report **Experiment 1 = 56** + **Experiment 2 = 245 = 301**, and the experiments-section overview itself states "a total of 301 middle school students"). Exp 1: 56 7th-graders, 3 advanced classes, one teacher, one school. Exp 2: 245 7th- and 8th-graders, 16 classes (8 advanced + 8 mainstream), 3 schools, 6 teachers.

**Experiment 1 (N=56).** Overall pre→post procedural gain across arms was large (F(1,52)=35.239, p<.001, d=1.65). A two-way ANOVA on **overall post-test** found a **significant OLM main effect: F(1,52)=4.903, p=.031, d=.56** — *no* PS main effect, *no* interaction. Process measures (incorrect attempts/step, hints/step) trended lower for the OLM arms but were not significant. No effect on self-assessment accuracy.

**Experiment 2 (N=245) — the load-bearing result.** Analyzed with ANCOVA, **teacher as covariate** (to absorb between-class variance), on pre→post learning *gains* (gains were used because raw scores were non-normal even after log/sqrt transforms). Overall pre→post gains were significant (procedural F(1,236)=81.066, p<.001, d=1.17; conceptual d=1.17). **No significant OLM or PS main effect on either item type.** But a **significant OLM×PS interaction on procedural gains: F(1,236)=7.535, p=.007.**

The two load-bearing planned/pairwise contrasts inside that interaction:
- **OLM helps under shared control:** OLM+PS learned significantly more procedural skill than noOLM+PS, **F(1,236)=6.401, p=.012.** (Quote: *"when students shared control over problem selection with the system … those who had access to an OLM learned significantly more on the procedural skills for equation solving than their counterparts who did not."*)
- **Shared control hurts without the OLM:** noOLM+**noPS** learned significantly more than noOLM+PS, **F(1,236)=6.056, p=.015 (Bonferroni-corrected p=.03).** (Quote: *"when the Open Learner Model was not in effect, the fully system-controlled condition learned significantly more than the shared control condition."*)

Reading Table 7 procedural pre→post gains directly corroborates the pattern: OLM+PS .50→.69 (+.19) and noOLM+noPS .59→.75 (+.16) are the strong arms; **noOLM+PS .57→.63 (+.06) is the weak arm** — shared control with no model to read is the loser; the OLM rescues it.

**Mechanism evidence (Exp 2, OLM arms only, n=119).** Time-on-OLM ↔ learning correlation was significant **only in OLM+PS**: total OLM time × procedural gain r=.33 (p=.02), self-assessment-prompt time × procedural gain r=.30 (p=.03); in OLM+noPS the same correlations were non-significant (.20, .22), and conceptual-gain correlations were null/negative throughout. So the regulatory payoff of looking at the model appears *only* when the learner also controls the path — consistent with the interaction.

**Process efficiency (Exp 2).** OLM produced a clean *main* effect on efficiency: OLM arms needed **fewer problems** (F(1,236)=8.116, p=.005, d=.36) and **steps** (F=3.900, p=.049, d=.25) to reach mastery and made **fewer incorrect attempts/step** (F=13.239, p<.001, d=.47). A separate OLM×PS interaction on hints/step (F(1,187)=4.097, p=.044): noOLM+PS asked more hints than OLM+PS.

**Nulls worth keeping.** **No** OLM or PS effect on enjoyment (all arms ~4.4–4.5/7). **No** OLM or PS effect on self-assessment-accuracy change (students were already fairly well-calibrated — an absolute-accuracy index of .14 ≈ correctly answering with ~62.6% confidence; the authors flag this as a domain where equation difficulty is unusually easy to judge from surface features). **No** OLM effect on the chosen problem sequence — with shared control, **61/120 (50.8%)** picked the system's ordered-blocked order anyway; the OLM did not push students toward interleaving. Interleaving did *not* beat blocking on learning but produced **significantly lower enjoyment** (blocked 4.96 vs interleaved 3.87, F(1,113)=14.392, p<.001, d=.69).

## Limitations

- **The two experiments disagree, and the headline rests on a post-hoc reading of the second.** Exp 1 said *OLM main effect, no interaction*; Exp 2 said *no main effects, OLM×PS interaction*. The authors privilege Exp 2 for its larger N, but this is a judgment call, not a pre-registered prediction borne out twice — the "OLM helps only under shared control" story is the Exp-2 pattern, and H3 was the interaction hypothesis they then confirmed. The interaction's strength rests on noOLM+PS being anomalously *low*, so the contrast is as much "shared-control-without-a-model is bad" as "OLM is good."
- **OLM evaluated as a single bundled factor.** Self-assessment prompts + delayed/animated bar update + summary view are confounded; the correlation evidence *suggests* the prompts carry most of it, but the design cannot separate components ("teasing apart the effects … remains a goal for future work").
- **Default BKT, unrefined KC model.** The mastery estimates driving both the skill bars and the level-lock used commonly-used default parameters, not data-fit ones — the OLM's *content* may be miscalibrated, which the paper does not probe.
- **Immediate post-test only; no retention/transfer.** Five days of practice, an immediate paper post-test, no delayed test — so the "learning outcome" is short-run skill, not durable learning.
- **Conceptual learning largely untouched.** All the OLM/interaction effects are on **procedural** items; conceptual gains showed no OLM, PS, or interaction effect.
- **Self-assessment-accuracy null may be domain-specific.** The authors concede equation difficulty is unusually legible from surface features, so the OLM's failure to improve calibration here may not generalize to domains where self-assessment is genuinely hard.
- **Modest, bounded "control."** Students chose the level but not the item and not when a level finished; the authors note the control may have felt too thin to move enjoyment.

## Relevance to this thesis

**Apparatus grounding for the agent's `/teach` stance — NOT thesis science.** Touches none of A1/A2/A3, produces no brain-alignment number, uses none of our datasets. **Keep it out of `docs/01-research-landscape.md`'s brain/distillation tables.** It is **external literature** whose sole job is to let `/teach` *cite a primary source* instead of asserting two claims the repo had carried second-hand.

This is the **primary-source warrant** for two claims the other OLM notes carried at one remove:

1. **(a) "OLM access raises outcomes only when paired with learner control over problem selection."** This is *literally Experiment 2's load-bearing finding*: no OLM main effect, a significant **OLM×PS interaction** (p=.007), with the OLM lifting procedural learning **only in the shared-control arm** (OLM+PS > noOLM+PS, p=.012). Cite at: *the model's benefit is conditional on the learner driving problem selection — it is an interaction, not a main effect, in the larger study.* **Caveat to carry honestly:** the *smaller* Experiment 1 found an OLM main effect with no interaction, so the "only-with-control" framing is the larger replication's pattern, not a clean two-for-two result.

2. **(b) "Passive display is weak; the gain is in the regulatory loop."** Two mutually reinforcing pieces: (i) shared control **without** a model to read was *worse* than system control (noOLM+noPS > noOLM+PS, p=.015) — a bare choice with no diagnostic is harmful, not neutral; and (ii) time-on-OLM correlated with learning **only** in the OLM+PS arm (r=.33, p=.02), i.e. looking at the model paid off only when the learner was also acting on a path decision. Cite at: *the value is in the predict-then-see-then-choose loop (self-assessment prompt → revealed skill bars → pick what to revisit), not in the skill bars as a readout.*

**Direct design mapping for `/teach`.** Lynnette's redesigned OLM *is* the structural template `/teach` already runs: a learner-visible mastery ledger (the skill bars / records layer) **paired with** a predict-before-reveal self-assessment prompt and a learner choice of what to revisit. This paper is the controlled evidence that this exact pairing — model + learner control — is what carries the learning gain, and that the ledger-as-passive-scorecard (or control-without-the-ledger) does not. It also supplies a guardrail: the OLM did *not* improve self-assessment accuracy or change what students chose to practice, so `/teach` should claim the loop drives *engagement/efficiency/procedural gain*, not automatic calibration improvement.

**Cite-or-flag guardrails (what this note does NOT support):**
- It does **not** show the OLM improves **self-assessment accuracy** (H5 not confirmed in either experiment) or **motivation/enjoyment** (H4 not confirmed). Do not cite it for those.
- It does **not** show durable/transfer learning — immediate post-test only.
- The "only-with-control" claim is **Experiment 2's pattern**; Experiment 1 (N=56) found an OLM main effect with no interaction. Cite the conditional claim with that asymmetry stated.
- The effect is on **procedural** equation-solving, not conceptual knowledge.

This note pairs with `open-learner-models_2025-review.md` (Robles Mucho et al. 2025 — the *pedagogical-alignment-beats-visualization* meta-synthesis, which cites this paper as a supporting source), `open-learner-models-and-errorful-learning.md` (the `/teach` synthesis index that carries the scorecard-drives-avoidance + learner-control framing), and `bodily-2018_olm-lad-systematic-review.md` (Aleven a coauthor — the OLM design-space census that lists this paper in its references). It does **not** clobber any of them; it is the missing primary source under their second-hand "n≈302 / OLM-only-with-control" citation.

## Verified

**Primary paper read in full, first-hand.** The complete published UMUAI text was read end to end via the pypdf extraction of the on-disk PDF (`data/papers/long-aleven-2017_olm-self-regulated-learning.pdf`, cross-checked against `scratchpad/longaleven.txt`): abstract, full introduction + theoretical background (§1.1.1–1.1.2), research questions, the research-platform description (Lynnette, BKT, the three redesigned-OLM features, the shared-control mechanism), the methods (design, procedure, participants, measurements, hypotheses Table 3), **all of Experiment 1's results (Tables 4–6) and Experiment 2's results (Tables 7–16)**, the full Discussion (§4.1–4.6), the Conclusions, and the complete reference list. Every number above is quoted from the paper's own tables/text; quoted passages are marked. **Parse note:** no `pdftotext`/`pdftoppm` renderer is installed in this container, so figures were not visually inspected — but all load-bearing quantities live in the text and tables, which extracted cleanly; no figure-only number is relied on.

**Sample-size correction (the repo's flagged `n≈302`):** the abstract and intro say "302," but the participants section, the experiments-section overview, and the conclusion all report **56 + 245 = 301**. The verified total is **N = 301**; the "302" is an internal off-by-one in the abstract. Per-condition Ns are not tabulated arm-by-arm in the text (`\gap`, below), but two anchors are given: the **two PS arms together = 120 students** (OLM+PS = 53, noOLM+PS = 67), and the **two OLM arms together = 119 students** (in Exp 2). With ~equal randomization within class the four Exp-2 arms are ≈61 each; the exact four-cell counts are not printed.

**Citation verified** via CrossRef (`api.crossref.org/works/10.1007/s11257-016-9186-6`): title, both authors in order (Yanjin Long, Vincent Aleven), *User Modeling and User-Adapted Interaction*, vol. 27, iss. 1, pp. 55–88, DOI 10.1007/s11257-016-9186-6, published online 31 Dec 2016 (2017 print) — all match the PDF. This **corrects a prior unreachability**: the paper was publisher-closed (Springer) and the repo carried its numbers second-hand; it is now read first-hand from the PDF on disk.

**Open `\gap`s:** (1) the **exact four-cell per-condition Ns for both experiments are not printed** in the text — only the PS-pair total (120: 53+67) and the OLM-pair total (119) are given, so the noPS/no-OLM cell counts and all of Experiment 1's per-arm Ns are unstated (do **not** invent them; ~61/arm is an inference from equal within-class randomization, not a reported figure); (2) figures were not visually rendered (no PDF renderer), but no figure-only number is load-bearing.

## Read Date

2026-06-20


## Related
- [`ladder.md`](../../ladder.md) — the canonical status board
- [`map.md`](../../map.md) — code system (Q/E/A/D/L) & journey map
