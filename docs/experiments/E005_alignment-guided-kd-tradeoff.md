# Experiment — E005: alignment-guided KD vs perplexity-only KD at MATCHED PERPLEXITY (the F1 headline / rate–distortion trade-off curve)

**Created:** 2026-06-11 · **Status:** DESIGN (pre-lock; oracle review pending; framing confirmation pending Erfan) · **Mode:** working
**Direction:** R03/R04 F1 (L3) — the headline thesis experiment. Decides A (alignment-guided distillation wins) vs B (honest trade-off-curve / measurement-rigor framing) **on evidence**.
**Predecessors:** `E003` (perplexity-only KD PARTIAL; L011 — alignment co-varies with perplexity) · `E004` (lever real-but-small-fragile, co-trained MSE front-runner) · `E006` (powered A2 PASS at voxel scale; lever statistically underpowered)
**Theory:** `../06-theory-grounding.md` §4 (rate–distortion = the F1 trade-off curve), §2 (DPI ceiling)
**Code:** reuses `scripts/distill.py` (λ_brain), `scripts/brain_loss.py` (co-trained MSE), `scripts/run_kd_alignment.py` (KD harness), `scripts/run_lebel_encoding.py` (powered alignment measurement)
**Output:** `outputs/E005_tradeoff.json`

---

## The question (sharpened by E003→E006)

> Does adding a brain-alignment objective to knowledge distillation buy **higher brain alignment at MATCHED PERPLEXITY** than perplexity-only KD — i.e. alignment recovered *beyond* what LM quality alone implies (the dissociation E003 could not establish, L011)? Plotted as a rate–distortion trade-off curve: rate = perplexity (LM quality), distortion = alignment deficit vs teacher.

**Why this is the decider, not a foregone conclusion:** E004 found the brain lever is real-but-small (+0.003, brain-specific) and E006 confirmed A2 powerfully but showed the lever statistic underpowered on the mean-over-voxels axis. E005 asks the *paired* question — alignment-guided vs perplexity-only KD evaluated on the SAME held-out data at the SAME perplexity — which removes the common-mode variance and is the test that detected E004's effect. A clear positive = F1 confirmed (Fork A). A null/tiny effect at matched perplexity = the honest, publishable trade-off-curve result (Fork B): brain-guided compression buys little beyond perplexity, and the contribution is the rigorous characterization + the curve itself.

## Arms

| Arm | Objective | Brain loss |
|---|---|---|
| **kd_ppl** | perplexity-only KD: `λ_kd·KL(student‖teacher)` | none (λ_brain=0) |
| **kd_brain** | alignment-guided KD: `λ_kd·KL + λ_brain·MSE(W·hₛ, fMRI)` | co-trained MSE readout on Tuckute-train sentences (the E004 front-runner form), student L7 |

Teacher gpt2-medium → student gpt2 (the E003 lineage; warm-start student, since E003 established cold-init is a separate question and warm is the realistic distillation setting). KD corpus = wikitext (E003's `data/kd_corpus/`); brain loss trains on Tuckute-train sentences (sentence-level — NO TR-loop; the powered LeBel axis is *measurement-only*, see below).

## Matched-perplexity protocol (L011 — the load-bearing design)

Compare alignment **at equal held-out perplexity**, not equal budget. Trace each arm's (perplexity, alignment) operating points by sweeping training (λ_brain ∈ a grid for kd_brain; checkpoints / step counts for both) → two Pareto frontiers on the (perplexity, alignment) plane. The F1 claim is **a better frontier for kd_brain** (higher alignment at matched perplexity), not a single number. Primary comparison: interpolate both arms to a common perplexity and take the paired alignment difference.

## Alignment measurement (two axes; the powered one is the headline)

1. **LeBel UTS03 voxelwise (powered, headline):** measure each KD student's unique R² on the E006 protocol (story-CV, expanded phone-tier+eng1000 nuisance, NC-reliable voxels) — measurement-only (`run_lebel_encoding.py` on the student), no further training. This is where A2 is powerfully resolved.
2. **Tuckute 5-ROI (screen, comparability):** the E002/E004 protocol, for ladder continuity.

## Claim tuple / decision rule (predeclared)

- **Metric:** paired (kd_brain − kd_ppl) alignment **at matched perplexity**, on LeBel voxelwise (primary) + Tuckute (secondary); bootstrap CI over seeds (×folds/voxels); ≥3 seeds.
- **F1 CONFIRMED (Fork A):** kd_brain alignment > kd_ppl at matched perplexity, CI excludes 0, on the powered LeBel axis, surviving the E006 anti-confound. The brain term recovers alignment beyond perplexity.
- **F1 NULL → trade-off-curve result (Fork B, the literature-leaning outcome):** the paired difference CI includes 0 at matched perplexity. → Brain-guided KD buys nothing beyond perplexity; the honest contribution is the rigorously-characterized trade-off curve (perplexity vs alignment under compression, with the strongest anti-confound) + the measurement-rigor finding that alignment tracks LM quality (L011/L012, Hadidi-2024). Still a real, publishable thesis.
- **Anti-confound (mandatory):** LeBel = E006 protocol (story-CV, expanded nuisance, NC voxels, untrained reference); Tuckute = E002 protocol. Report perplexity per arm/point (the matched axis). ≥3 seeds.

## Open design questions (resolve at lock / oracle review)

- The exact matched-perplexity mechanism (λ-sweep vs checkpoint-matching vs early-stop to a target ppl) — the cleanest is checkpoint-matching: save students at several ppl levels, compare alignment at equal ppl.
- Power: E006 showed the mean-over-voxels lever MDE ≈ +0.013; the *paired* kd_brain−kd_ppl contrast at matched ppl should be better-powered (common-mode removed), but a power note is required before committing (the same MDE discipline as E004/E006).
- Whether to also run a *region-restricted* (LH-language) LeBel axis where the brain effect may concentrate (vs whole-cortex NC voxels).
- Compression aggressiveness: gpt2-medium→gpt2 (2.9×) is one rate; a second rate (→distilgpt2-size) would trace more of the curve (defer unless the first rate is informative).

## Status

Design drafted. Pending: oracle review (the E004/E006 Design→Run gate), a power note for the paired matched-ppl contrast, and Erfan's confirmation of the thesis-headline framing (A vs B — though E005 is framing-robust and decides it empirically). Harness pieces all exist (`distill.py` λ_brain, `brain_loss.py` co-trained MSE, `run_kd_alignment.py`, `run_lebel_encoding.py`); E005 is mostly orchestration + the matched-ppl protocol + the powered LeBel measurement on KD students.
