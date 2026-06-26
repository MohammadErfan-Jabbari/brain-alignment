---
title: "Limited but Consistent Gains in Adversarial Robustness by Co-training with Human EEG"
tags: [literature]
aliases: [guo-2024_eeg-cotrain-adversarial-robustness]
---

# Limited but Consistent Gains in Adversarial Robustness by Co-training with Human EEG

**Authors:** Manshan Guo; Bhavin Choksi; Sari Sadiya; Alessandro T. Gifford; Martina G. Vilas; Radoslaw M. Cichy; Gemma Roig
**Year:** 2024
**Venue:** ECCV 2024, HCV Workshop (oral)
**DOI/arXiv:** arXiv:2409.03646
**Canonical ID:** guo-2024_eeg-cotrain-adversarial-robustness

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [ ] Full PDF read (page-by-page comprehension)
- [x] Full PDF scanned (search + targeted read)
- [ ] Extracted text only

PDF verified: 2026-06-11 — HTML version (arXiv:2409.03646v2) read in full across multiple queries;
all sections (Abstract, Methods, Results, Discussion/Conclusion), complete Table 1 (all 24 rows),
and figure descriptions extracted. The HTML render was complete and parseable. Comprehension
self-check passed: Y. The paper did not report clean accuracy or give exact numbers for the
shuffled/random control gains in the text; these absences are noted where relevant.

---

## Comprehension Summary [REQUIRED]

1. Problem solved: Prior work (Safarani 2021, Pirlot 2022) showed modest robustness gains from
   co-training ANNs with invasive monkey neural data; this paper asks whether the same effect holds
   with cheaper, non-invasive human EEG collected on 16,540 natural images (THINGS-EEG2) and extends
   the test across 24 diverse dual-task learning architectures and 3 attack types.

2. Core insight: A dual-task objective — ResNet50 trained jointly for 1,654-way image classification
   and EEG-signal prediction using uncertainty-weighted loss — confers measurable adversarial
   robustness gains. Gains correlate strongly with EEG prediction quality (R² = 0.53–0.61, p < 1e-6
   across 720 models), peak at the 100 ms EEG timepoint, and are positive for real EEG, shuffled
   EEG, and randomly generated EEG alike — though real EEG produces the highest gains.

3. If-wrong breakage: The key empirical fact the paper needs to hold is that real EEG produces a
   larger robustness gain than shuffled or random EEG. This is asserted and shown in Figure 2D, but
   no significance test comparing real vs. shuffled gain is reported; the margin is never quantified.
   If the shuffled-control gain is close in magnitude to the real-EEG gain, the brain-specific
   contribution is near-zero and the result reduces to "multitask learning improves robustness."

---

## Source Grounding

**Dataset.** THINGS-EEG2 (publicly available). EEG from 10 subjects viewing 16,540 natural images
from the THINGS database (1,654 object categories, 10 images/category). Train/val split 9:1 (14,886
training images; 1,654 validation images). EEG preprocessed: epoched −200 to +800 ms, downsampled
to 100 Hz, 17 channels (occipital/parieto-occipital: Pz, P3, P7, O1, Oz, O2, P4, P8, P1, P5,
PO7, PO3, POz, PO4, PO8, P6, P2). EEG shape per subject: 14,886 × 4 trials × 17 channels × 100
timepoints (training); 1,654 × 4 × 17 × 100 (validation).

**Architecture.** Shared ResNet50 backbone (ImageNet-pretrained) with two output branches: a
1,654-way classification head (cross-entropy) and an EEG prediction head (MSE, output dim = 17×100
= 1700). Loss is uncertainty-weighted:

$$L(W, \delta_1, \delta_2) = \frac{1}{2\delta_1^2}L_{\text{EEG}}(W) + \frac{1}{2\delta_2^2}L_{\text{cls}}(W) + \log\delta_1 + \log\delta_2$$

The EEG branch is varied across 24 architectures spanning four clusters: CNN (8 variants), RNN/LSTM
(7 variants), Transformer (4 variants), and Attention (5 variants). All share the frozen ResNet50
backbone; the clusters differ in how they read out and process intermediate backbone features
(concatenation vs. averaging of Blocks 3+4 is generally strongest). Adam, lr = 5e-6, weight decay
= 0.0, 200 epochs, batch = 64.

**Seeds.** 3 independent random initializations per architecture (seeds: 0, 17, 337), EEG branch
only.

**Subjects.** 10. Robustness results are averaged across all subjects and seeds (720 = 24 × 10 × 3
samples total for correlation analyses).

**Adversarial attacks.** Three types, L∞-PGD (40 iterations, 16 strength levels ε ∈ [1e-5, 1e-2]),
L2-PGD (50 iterations, 14 strength levels ε ∈ [1e-3, 1.0]), and L2 C&W (iterative gradient
descent, 22 strength levels). Robustness metric: top-1 accuracy on 1,654 validation images.
Robustness gain is defined as:

$$\text{Gain}_{\text{DTL}}(\epsilon) = \text{acc}_{\text{DTL}}(\epsilon) - \text{acc}_{\text{baseline}}(\epsilon)$$

then averaged across attack strengths (selecting high-strength ε values) to give Avg_Gain_DTL per
model.

**Baseline.** Standard ResNet50 trained for image classification only (no EEG branch). Clean
(unattacked) accuracy is not reported for either the baseline or the DTL model.

**Controls.** Three control conditions trained identically but with corrupted EEG:
- DTL-shuffled: EEG trials shuffled across images (preserves firing-rate statistics, destroys
  image-specific tuning).
- DTL-random: EEG drawn from a geometric distribution.
- DTL-random-normal: EEG drawn from a normal distribution.

---

## Key Ideas

### Finding 1 — The core effect: EEG co-training improves adversarial robustness

All 24 DTL architectures show positive robustness gains on all three attacks relative to the
classification-only baseline. The best single model (CNN_concat_Bk34, Avg_PCC_tps = 0.296) gains
+0.080 on L2-PGD, +0.044 on L∞-PGD, and +0.076 on C&W. The worst model (CNN_Bk4) gains +0.019
(L2-PGD), +0.012 (L∞-PGD), +0.013 (C&W). Across all 24 architectures:

| Attack | Mean gain | Min | Max |
|---|---|---|---|
| L2-PGD | 0.042 | 0.019 | 0.080 |
| L∞-PGD | 0.023 | 0.011 | 0.044 |
| L2-C&W | 0.042 | 0.013 | 0.076 |

These are absolute accuracy differences (percentage-point fractions, i.e. 0.042 = 4.2 pp). The
paper explicitly labels the gains "modest — a clear limitation of our results." No clean-accuracy
comparison is reported; it is unknown whether DTL also changes clean accuracy.

### Finding 2 — Gain correlates with EEG prediction quality, peaking at 100 ms

Across all 720 models (24 × 10 × 3), the correlation (R²) between Avg_Gain_DTL and Avg_PCC_tps
(EEG prediction Pearson correlation across timepoints) is 0.53–0.61 (p < 1e-6) for all three
attacks. When EEG prediction is computed per timepoint, the channel-level correlation peaks at
~100 ms post-stimulus (Pearson r = 0.32, p < 0.05 Bonferroni-corrected across 17 channels), the
time of highest EEG discriminability.

### Finding 3 — Controls show gains too, but smaller

The shuffled, random-geometric, and random-normal EEG controls also produce positive robustness
gains relative to the baseline, which the authors acknowledge: "these also showed some gains in
robustness (as also reported in previous works), the model trained with the real EEG showed the
highest robustness gains." The exact magnitude of control-condition gains is not tabulated. No
significance test comparing real vs. shuffled gains is reported; Figure 2D shows the ordering
visually. The authors note the control gains are "consistent observation across intra- and
extracranial neural activity" and flag it as deserving future investigation.

This is the key structural weakness: the shuffled-control gain is unquantified, so the
brain-specific increment (real EEG minus shuffled) cannot be read directly from the paper.

### Finding 4 — Consistency across seeds and architectures

All 24 architectures across 4 clusters (CNN, RNN, Transformer, Attention) show positive gains on
all three attacks. The 3-seed variation is reported as standard error in figures (small shaded
bands). The abstract states: "effects were consistent across different random initializations and
robust for architectural variants."

### Finding 5 — Parieto-occipital channels, not early visual, drive robustness

Early occipital channels (Oz, O1, O2) predict EEG best, but the correlation between per-channel
prediction accuracy and robustness gain is highest for parieto-occipital channels (PO7, PO3, PO4,
PO8, POz), implicating mid-level visual processing over low-level V1-like features.

---

## Evidence

**Primary result:** Positive robustness gains (Table 1, 24 rows × 3 attacks) for all DTL
architectures on all attacks. Mean absolute gain ~4.2 pp (L2-PGD), ~2.3 pp (L∞-PGD), ~4.2 pp
(C&W). Best case: +8.0 pp (L2-PGD), +4.4 pp (L∞-PGD), +7.6 pp (C&W) for CNN_concat_Bk34.

**EEG-robustness correlation:** R² = 0.53–0.61, p < 1e-6 across 720 models × 3 attacks.

**Temporal peak:** EEG prediction at 100 ms correlates with robustness gain at r = 0.32 (p < 0.05,
Bonferroni).

**Control conditions:** Real EEG > shuffled/random EEG gains (Figure 2D), but the margin is
unquantified in the text and no significance test is run for this comparison.

**No adversarially trained baseline** is included. The comparison is real-EEG DTL vs.
classification-only ResNet50 only; adversarially trained (PGD-AT) would presumably show much larger
gains, making the DTL gains look even smaller in relative terms.

**Clean accuracy** on the 1,654-way task is not reported for either model.

---

## Limitations

1. **Unquantified shuffled-control margin.** The paper asserts real EEG > shuffled EEG in Figure
   2D but does not report the numerical margin or a significance test. The brain-specific increment
   is therefore unknown.

2. **No adversarially trained comparison.** Adversarial training typically yields robustness gains
   of 20–40 pp at moderate ε; the 2–8 pp DTL gains are modest even without this comparison.

3. **No clean accuracy reported.** It is unknown whether EEG co-training improves or degrades
   clean classification accuracy; this is the most common trade-off in robustness literature.

4. **Task mismatch with language.** The brain signal is EEG (scalp, millisecond-scale visual
   responses) to image stimuli; the shared backbone is ResNet50. None of this transfers directly to
   text LMs or fMRI.

5. **No power analysis.** No predeclared MDE or sample-size justification for the real-vs-shuffled
   comparison. The 720-model correlation analysis is sufficiently powered to detect r ≈ 0.10, but
   the gain ordering (real > shuffled) has no formal test.

6. **Uncertainty-weighted loss is not ablated.** It is unclear whether robustness gains arise from
   the EEG signal itself or from the uncertainty-weighting mechanism as a generic multi-task
   regularizer.

---

## Relevance to this thesis

**Which assumption this touches:** A3 (preserved brain-alignment buys practical downstream benefit).

**Role in our framework:** Primary floor-setter for E009 (A3 / Q4). This paper is the only
published study that directly optimizes for brain-alignment *and* measures adversarial robustness
with shuffled-brain controls. Its findings establish the magnitude of the practical benefit we
should expect and the design requirements for a credible test.

**The three things this paper does for us:**

1. **Floor for the MDE predeclaration in E009.** The mean absolute robustness gain from EEG
   co-training at best is ~4.2 pp (L2-PGD, averaged across 24 architectures); the maximum is
   +8.0 pp. The authors call these gains "modest." For E009's power analysis, the brain-specific
   increment (real EEG minus shuffled) is smaller still — somewhere below 8.0 pp and unquantified.
   A conservative MDE of 2–4 pp (absolute robustness accuracy) is the sensible floor to predeclare.
   Anything smaller is not meaningful; anything larger is likely to be an overestimate given the
   vision/EEG domain. Our LM/fMRI setting may be weaker (noisier brain signal, more indirect task
   coupling), suggesting the lower end of that range is appropriate.

2. **Confirms the shuffled-control design is mandatory.** Shuffled EEG also gives robustness
   gains. If we ran E009 without the `kd_brain_permuted` arm we would not be able to attribute any
   robustness gain to brain-specific signal vs. generic multi-task regularization. This is already
   in the E009 design and is reinforced here.

3. **Does NOT threaten A3 as a hypothesis, but tightens what "confirmed" means.** The gains are
   small but real and consistent across 24 architectures, 10 subjects, 3 seeds, and 3 attack types.
   A3 is not killed by this paper — it is framed. If E009 finds a brain-specific robustness
   increment (kd_brain > kd_brain_permuted) of even 1–2 pp, the Guo floor confirms that is in the
   expected range. If the gain is zero we report a clean null in the language domain.

**Connection to other canon:**

- `pirlot-2022_dcca-neural-regularizer-cnns` found that a brain-data regularizer's accuracy gain
  was nearly fully reproduced by a shuffled-label control; only adversarial robustness survived as
  a brain-specific effect. Guo et al. replicate the same structure (shuffled controls gain too, real
  EEG gains more) in the EEG-image domain, but still cannot quantify the brain-specific increment.
  Together these papers say: if any brain-specific practical benefit exists, robustness is its most
  likely expression, and it is small.

- The `pirlot-2022` + Guo joint reading is why E009's primary outcome is robustness/OOD (not
  accuracy) and why the permuted-brain twin is the load-bearing control, not just the perplexity-
  matched baseline.

- `hadidi-2024_case-against-brainscore-reliance` and `feghhi-2024_case-against-over-reliance-brain-scores`
  provide the methodological protocol Guo et al. partially violate (no significance test for real
  vs. shuffled). E009 should close this gap for the language domain.

**What this does NOT change in our design:**
- E009's primary outcome (robustness/OOD at matched perplexity, vs. permuted twin) is already
  calibrated to this floor. No structural change is needed.
- The MDE predeclaration for E009 should land at 2–4 pp (or the language-domain equivalent) and
  must be stated explicitly before running.

**One-line verdict:** The gains Guo et al. report are real, consistent, and modest (mean ~4 pp,
peak 8 pp absolute robustness improvement); the brain-specific increment above shuffled controls
is positive but unquantified — this threatens A3 with a signal-to-noise problem, not with
falsification, and makes a careful power analysis mandatory before E009 is run.

---

## Verified

HTML full text (arXiv:2409.03646v2, ECCV 2024 HCV workshop oral) read across four targeted queries
covering all sections, Table 1 complete (24 rows × 4 columns), and all figure descriptions. Table 1
numbers confirmed by independent computation (means: L2-PGD 0.042, L∞-PGD 0.023, C&W 0.042).
The PDF was not separately fetched; the HTML render was complete and consistent across queries.
Key absences confirmed: (a) shuffled-control gains are not tabulated numerically; (b) clean
accuracy is not reported; (c) no significance test for real vs. shuffled comparison; (d) no power
analysis.
Read date: 2026-06-11


## Related
- [`ladder.md`](../../ladder.md) — the canonical status board
- [`map.md`](../../map.md) — code system (Q/E/A/D/L) & journey map
