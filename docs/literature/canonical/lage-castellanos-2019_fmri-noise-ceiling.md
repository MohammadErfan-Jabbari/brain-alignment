---
title: "Methods for computing the maximum performance of computational models of fMRI responses"
tags: [literature]
aliases: [lage-castellanos-2019_fmri-noise-ceiling]
---

# Methods for computing the maximum performance of computational models of fMRI responses

**Authors:** Agustin Lage-Castellanos, Giancarlo Valente, Elia Formisano, Federico De Martino
**Year / Venue:** 2019 / PLoS Computational Biology 15(3): e1006397
**Link:** https://doi.org/10.1371/journal.pcbi.1006397

---

## TL;DR

The noise ceiling (NC) for voxelwise fMRI encoding models is the maximum correlation any computational model can achieve, bounded by measurement noise in the test data alone. The authors derive a closed-form analytical estimator that equals $\hat{\rho}_\text{NC} = \hat{\sigma}_\beta / \hat{\sigma}_{\hat\beta}$ — the ratio of the estimated noise-free signal standard deviation to the observed response standard deviation — and prove it has the same expected value as the existing Monte Carlo estimator (MCnc) at 800× lower computational cost. Critically, the paper treats this noise ceiling as a strictly single-subject quantity: group-level analysis is explicitly declared out of scope because the methods "only account for the measurement error and not for the variability between subjects."

---

## Key ideas

### The generative model and the ceiling definition

Each voxel's estimated response $\hat{\beta}_i$ to stimulus $i$ is treated as a noisy draw from the true response $\beta_i$:

$$\hat{\beta}_i \sim \mathcal{N}(\beta_i,\; \sigma^2_\varepsilon)$$

with total observed variance $\hat{\sigma}^2_{\hat\beta} = \hat{\sigma}^2_\beta + \hat{\sigma}^2_\varepsilon$ (signal + noise). For infinite training data and no regularization, the noise ceiling is defined as the expected correlation when the model predicts the true responses exactly (Eq. 10):

$$\rho_\text{NC} = \mathrm{E}[\rho]_{\hat{P}=P,\; \lambda=0,\; n_\text{tr}\to\infty}$$

The analytical closed form (Eq. 15–16) follows from independence of measurement error and true signal:

$$\hat{\rho}_\text{NC} = \frac{\hat{\sigma}^2_\beta}{\sqrt{\hat{\sigma}^2_\beta \cdot \hat{\sigma}^2_{\hat\beta}}} = \frac{\hat{\sigma}_\beta}{\hat{\sigma}_{\hat\beta}}$$

where the noise-free signal variance is recovered as $\hat{\sigma}^2_\beta = \hat{\sigma}^2_{\hat\beta} - \frac{1}{n}\sum_i \hat{V}_{\beta_i}$, subtracting the mean per-stimulus variance of the estimated responses (the diagonal of $\hat{V}_\beta$, Eq. 16).

The equivalent in $R^2$ is obtained via the transformation in Eq. 7.

### Estimating $\hat{V}_\beta$: three routes

The diagonal of $\hat{V}_\beta$ (the variance of $\hat\beta$ due to measurement error) can be estimated three ways, each making different assumptions about the fMRI noise covariance $\Omega$:

1. **OLS ($\hat\Omega = I$):** $\hat{V}_\beta = (\Phi^T\Phi)^{-1}$ — assumes i.i.d. noise; overestimates NC when noise is autocorrelated.
2. **AR(1) / NST (SPM-12 / RobustWLS):** parametric models of $\hat\Omega$; unbiased under correct model but fragile.
3. **Run-to-run variance (R2Rnc, Eq. 17):** non-parametric; estimates $\hat{V}_{\beta_i}$ as the variance of per-run response estimates across $n_r$ fMRI runs — requires no assumption on $\hat\Omega$ and is robust across all simulated noise types.

The split-half estimator (SHnc, Eq. 11) is also compared: it correlates $\hat\beta$ estimates from two independent data halves with a Spearman-Brown correction $\rho_\text{SHnc} = \sqrt{2\rho / (\rho+1)}$. It is non-parametric but shows larger variance than R2Rnc and systematically slightly higher NC in real data (explained by few runs or violation of SHnc independence assumption).

### How the noise ceiling rises with averaging (the mechanism the thesis uses)

The paper does not study cross-subject averaging directly, but the formal apparatus makes the consequence immediate. The NC is:

$$\rho_\text{NC} = \sqrt{\frac{\sigma^2_\text{signal}}{\sigma^2_\text{signal} + \sigma^2_\text{noise}}}$$

When $k$ subjects are averaged, the shared stimulus-evoked component $g$ is preserved while each subject's idiosyncratic noise $\varepsilon_i$ shrinks by $\sqrt{k}$: the effective denominator $\sigma^2_\text{noise}$ in the averaged target is $\sigma^2_\varepsilon / k$ (for i.i.d. subject noise). So the averaged-target NC is:

$$\rho_\text{NC}(k) = \sqrt{\frac{\sigma^2_g}{\sigma^2_g + \sigma^2_\varepsilon / k}}$$

This monotonically rises toward 1 as $k$ increases. The paper itself does not write this formula for cross-subject averaging — it writes it only for within-subject repetitions (the denominator shrinks by $n_r$ in Eq. 17's motivation). But the mathematics is structurally identical: averaging suppresses denominator noise by $k$, raising the achievable ceiling. The paper explicitly states (Discussion, p. 23): "For group level analysis the approaches we have described here are **not directly suitable** because they only account for the measurement error and **not for the variability between subjects**."

### Regularization penalty on ceiling-approaching

A separate finding: regularization (ridge) prevents the true model from reaching the noise ceiling even with infinite data, because the bias-variance tradeoff deflates $\rho$ relative to $\rho_\text{NC}$. In simulations with $n_\text{tr}=126$ and 128 features, no value of $\lambda$ reached the NC (Fig. 8 right panel). This is independent of which NC estimator is used.

---

## Evidence

**Simulations:** 168 stimuli (126 training, 42 test), 128-feature computational model, 6 runs, 100 replications per scenario. Four noise scenarios: i.i.d., AR(1) autocorrelated, non-stationary, AR(1)+run-to-run variability. Key finding: analytical NC and MCnc produce identical mean and variance across all scenarios; analytical NC is $7\times10^{-5}$ sec/voxel vs MCnc $0.06$ sec/voxel (800× faster). All estimators agree when noise is i.i.d.; OLS and NST estimators are upward-biased under autocorrelated noise; R2Rnc and SHnc are unbiased across all conditions.

**Real fMRI data:** 10 healthy subjects, 7-Tesla auditory cortex fMRI, 168 sounds presented 6 times across 24 runs (fast event-related design, TR=2.6s, 1.1mm isotropic). NC estimated on 50,000 randomly selected voxels per subject. SHnc showed systematically slightly higher NC than R2Rnc across all 10 subjects (Fig. 11). Both methods converged at high SNR voxels; diverged at low SNR.

**Typical NC values (7T auditory cortex):** voxel-level NC distributions peaked around 0.4–0.6 (correlation) depending on parametrization and subject (Fig. 9 histograms), with broad right tails toward 0.8–0.9 in the highest-SNR voxels.

---

## Limitations

1. **Single-subject only.** The paper explicitly declines to treat group-level noise ceilings. It notes that Carlin et al. 2017 (ref [15]) proposed a group NC for RSA, which "can be extended to encoding approaches," but this is not developed here.

2. **Two-level GLM assumption.** The framework assumes responses $\hat\beta$ are first estimated from the time series (GLM step 1) and then the encoding model fits to them (step 2). Direct fitting to the BOLD time series (e.g. pRF models) is acknowledged but not covered; the NC at the time-series level requires the SHnc extension mentioned in the Discussion.

3. **No between-subject variance in the NC definition.** The NC as defined here is the maximum performance conditioned on test-data noise only — it does not account for inter-subject variability, which means a group-averaged target has a *different* (higher) NC by construction, and this paper's estimators will underestimate that higher ceiling if applied naively to the averaged data.

4. **Regularization ceiling gap is characterized but not resolved.** The paper shows a true model cannot reach NC under ridge regression, but offers no corrected NC estimator that adjusts for the regularization bias.

5. **N=10 subjects, 7T auditory cortex.** Real-data validation is on one lab's dataset; the NC characteristics for language cortex at 3T (lower SNR, different ROI) are not reported.

---

## Relevance to this thesis

**Which assumption/claim this grounds:**

This paper provides the formal definition and estimation procedure for the voxelwise fMRI noise ceiling — the object the thesis's 1.7× inflation argument ($\S$4.2, draft v0) rests on. The thesis's claim is: tuning toward a $k=5$ subject-averaged target measures performance against an inflated ceiling NC$(k=5) \approx 0.83$ rather than the per-subject ceiling NC$\approx 0.49$, and this inflation (ratio $\approx 1.7\times$) explains why the apparent optimization gain (+0.0081) does not survive per-subject inference. Lage-Castellanos et al. 2019 establishes the mechanism: NC is $\sigma_\text{signal}/\sigma_{\hat\beta}$, and averaging $k$ subjects shrinks the effective noise variance by $k$, raising the ceiling monotonically. The paper itself does not derive the cross-subject averaging formula or study its consequences for optimization claims — it only states that group-level analysis requires separate treatment. Our contribution is therefore not the mechanism (averaging raises the ceiling), but its specific consequence: a model optimized against an averaged target cannot be evaluated with per-subject inference without correcting for the inflated ceiling, and failing to make this correction produces an apparent brain-specific optimization gain that vanishes per individual.

**Anchor / counter-evidence / baseline / theory:** This is the **formal anchor** for the noise ceiling concept and the mathematical basis for the $\mathrm{NC}(k)$ formula in the draft $\S$4.2. It is not counter-evidence.

**How it should change our design or guardrails:** The paper's explicit recommendation to "report both the observed accuracies and the noise ceiling" (not just noise-normalized scores) aligns with our protocol of reporting absolute unique-R² gaps rather than NC-normalized ratios. The regularization-NC gap finding also supports why the encoding model performance in E005/E008 sits well below NC ≈ 0.49: ridge regression on 1000 stimuli with ~768-dim features is exactly the high-regularization, finite-data regime where Fig. 8 shows the true model cannot reach the ceiling.

---

## How we cite it

Cite as the **formal definition of the voxelwise fMRI noise ceiling** and the mathematical basis for the averaging-inflation mechanism (NC rises monotonically as $k^{-1}$ noise shrinkage), grounding our $\S$4.2 "1.7× inflation" calculation; concede that the paper establishes the mechanism at the level of within-subject repetitions and explicitly declines to extend it to cross-subject averaging — our novelty is the consequence of that mechanism for brain-tuning optimization validity claims.

---

## Verified

Full PDF read, all 25 pages, page-by-page via the Read tool (pages 1–25 in three passes). No parse issues — the PLoS HTML page and the printable PDF were both accessible. All equations confirmed directly from the PDF images. The paper does not contain any explicit cross-subject averaging formula; the statement that group-level analysis is out of scope appears verbatim on p. 23 (Discussion paragraph beginning "For group level analysis..."). No figures were inaccessible.


## Related
- [`ladder.md`](../../ladder.md) — the canonical status board
- [`map.md`](../../map.md) — code system (Q/E/A/D/L) & journey map
