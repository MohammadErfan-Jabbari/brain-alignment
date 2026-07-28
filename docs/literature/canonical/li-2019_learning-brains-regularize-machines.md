---
title: "Learning from brains how to regularize machines"
tags: [literature]
aliases: [li-2019_learning-brains-regularize-machines]
---

# Learning from brains how to regularize machines

**Zhe Li, Wieland Brendel, Edgar Y. Walker, Erick Cobos, Taliah Muhammad, Jacob Reimer, Matthias Bethge, Fabian H. Sinz, Xaq Pitkow, and Andreas S. Tolias / 2019 / arXiv preprint** · **Link:** [arXiv:1911.05072](https://arxiv.org/abs/1911.05072)

## TL;DR

Li et al. do not regularize a classifier with raw neural responses. They first train a stimulus-to-neural-response system-identification CNN, use its deterministic predictions to construct a reliability-weighted mouse-V1 representational-similarity target, and then regularize a ResNet toward that target through a learned mixture of intermediate-layer similarities.

The decisive ablation is that a similarity target built directly from noisy single-trial neural data did not reproduce the robustness gain, whereas the learned predictive-model target did. This makes the paper a direct precedent for [`H002`](../../hypotheses/H002_repeat-stable-biological-supervision.md), but not yet a recipe for [`E031`](../../experiments/E031_biological-target-information-recovery.md): the denoiser is a learned stimulus model whose biological information must be separated from image statistics, model inductive bias, and in-sample target reconstruction.

## Key ideas

### Neural recording and reliability weighting

The authors used two-photon recordings from primary visual cortex in awake, head-fixed mice passively viewing grayscale ImageNet images while able to run on a treadmill. Each scan contained 5,100 distinct images at 64 by 36 pixels: 5,000 images appeared once and 100 "oracle" images appeared 10 times, producing 6,000 trials. The paper reports roughly 8,000 simultaneously recorded units as the motivation for using mice and averages the final target over eight scans collected across animals and days; the exact number of animals is `\gap` in the paper text inspected.

For neuron \(a\), response reliability is estimated from the repeated oracle images:

\[
w_a = \frac{\sigma_a}{\eta_a},
\]

where \(\sigma_a^2\) is stimulus-driven variance of the repeat mean and \(\eta_a^2\) is average within-stimulus trial variance. Population responses are weighted by \(w_a\), centered across images, normalized to unit length, and compared by cosine similarity. Noisy neurons therefore contribute less to the representational target.

### The system-identification model is the denoiser

Most images were presented once, making direct single-trial similarities too noisy. The authors trained a three-layer CNN with skip connections to predict each neuron's response from the image through a linear readout. Pupil position, pupil size, and treadmill-running speed enter the model so its shifter and modulator components can account for nonvisual state.

The predicted response for neuron \(a\) is additionally weighted by \(v_a\), the correlation between that neuron's predicted and observed response:

\[
\hat r_{ai} = w_a v_a \hat\rho_{ai}.
\]

This makes the final target depend both on neural repeat reliability and on how well the system-identification model predicts each neuron. The model output is deterministic, heavily regularized, and conditioned on measured behavioral covariates. The exact regularization terms and complete training split for this system-identification model are delegated to prior model papers and are `\gap` in this paper's self-contained method description.

The main regularization target is the average across eight scan-specific \(5{,}000 \times 5{,}000\) similarity matrices computed from predictions for the non-oracle images. The 100 repeated oracle images are used to estimate neuron weights, evaluate the predictive target, and illustrate the geometry; their \(100 \times 100\) matrix is not the main classifier-training target.

### The classifier loss acts on a learned intermediate-layer mixture

The classifier objective is

\[
L = L_{\mathrm{task}} + \alpha L_{\mathrm{similarity}},
\]

with cross-entropy as \(L_{\mathrm{task}}\). For a pair of neural-stimulus images \(i,j\), the auxiliary term is the squared difference between Fisher-like transforms of the classifier and neural similarities:

\[
L_{\mathrm{similarity}} =
\left[
\operatorname{arctanh}\!\left(S_{ij}^{\mathrm{CNN}}\right)
-
\operatorname{arctanh}\!\left(S_{ij}^{\mathrm{neural}}\right)
\right]^2.
\]

For each selected classifier layer, the authors center flattened feature vectors across images and compute cosine similarity. Five ResNet18 convolutional layers, numbered 1, 5, 9, 13, and 17, contribute through trainable non-negative softmax weights \(\gamma_k\) that sum to one:

\[
S_{ij}^{\mathrm{CNN}} = \sum_k \gamma_k S_{ij}^{\mathrm{CNN},k}.
\]

The learned weights usually collapse onto one layer, typically layer 5 at the end of the first residual-block group, but the selected layer is stochastic and nearby layers sometimes win. This is evidence for competitive learned placement, not proof that one universal layer is optimal.

Training alternates a CIFAR classification batch with a batch of pairs from the mouse-stimulus images through the same convolutional trunk. Thus the neural loss changes shared features even though the classification and neural-image datasets differ.

## Evidence

### Does the predictive model recover repeat-stable geometry?

On the 100 repeated oracle images, single-trial measured similarity correlated \(r=0.39\) with the repeat-averaged oracle similarity, whereas predictive-model similarity correlated \(r=0.73\) with the oracle target and spanned a wider range. The authors also report that between-scan variation in oracle similarity was smaller than within-image variation across repeats.

These values support the narrow claim that the learned response predictor better approximates repeat-averaged geometry than a single measured trial on the same oracle stimulus set. They do not by themselves show that the predictor retains biological information beyond a matched stimulus model.

### Does the denoised target change classifier behavior?

- A ResNet18 trained on grayscale CIFAR10 with the model-derived neural target retained roughly 50% accuracy at the highest plotted Gaussian-noise level, compared with roughly 20% for the unregularized model. Exact clean and per-noise-level values are figure-read only and remain `\gap` here.
- The model-derived target outperformed the no-regularizer, shuffled-target, pretrained-VGG-similarity, and raw-neural-data target conditions under Gaussian corruption. The figure caption notes a small sacrifice in clean-image performance.
- The same qualitative pattern was reported for ResNet34 on grayscale CIFAR100 against the no-regularizer and shuffled-target conditions.
- Main Gaussian-noise curves report means and SEM over five random seeds. Training used SGD for 40 epochs with batch size 64; the main text used \(\alpha=20\).
- On 1,000 CIFAR10 test images, the median minimum adversarial perturbation was \(0.0034\) in \(L_\infty\) and \(0.13\) in \(L_2\) for the model-derived neural target, compared with \(0.0025\) and \(0.09\) for no regularization. Shuffled-target results were \(0.0030\) and \(0.11\); VGG-target results were \(0.0028\) and \(0.11\). The raw-neural-data target was not included in this adversarial comparison.

All values in this section are results reported by Li et al., not thesis measurements.

## Controls and what they establish

1. **No auxiliary regularization:** establishes the baseline effect of adding an auxiliary geometry loss.
2. **Shuffled neural-similarity target:** shows that generic auxiliary pressure contributes some robustness but does not reproduce the model-derived neural target. The exact shuffling operation and whether it preserves covariance spectrum or local structure are not sufficiently specified in the inspected body text, so it is not an E031-style matched twin.
3. **Pretrained VGG19 conv3-1 similarity:** tests a non-neural but vision-trained feature geometry reported to resemble animal V1. It improves robustness less than the model-derived neural target, but is not matched in dimension, predictability, spectrum, or loss difficulty.
4. **Raw measured neural similarity:** the most relevant ablation. Replacing model-predicted similarity with direct single-trial neural similarity did not yield the same robustness boost. The authors attribute the failure to response variability and conclude that a strong predictive system-identification denoiser is necessary.
5. **Oracle repeats:** validate whether raw and predicted similarities approximate repeat-averaged neural geometry. They are not used as the main \(5{,}000\)-image regularization target.
6. **ResNet18/CIFAR10 and ResNet34/CIFAR100:** provide an architecture and task replication within grayscale image classification.

Together, these comparisons show that denoising and target construction matter. They do not isolate which information in the predictive model is uniquely biological.

## Limitations

1. **Stimulus-model substitution is unresolved.** A CNN trained to predict V1 responses may amplify ordinary image features that are already sufficient for robustness. Shuffle and VGG controls are informative but are not geometry-, predictability-, capacity-, or optimization-matched to the neural system-identification target.
2. **The main target is not described as cross-fitted by stimulus.** The system-identification model is trained from neural responses to the 5,000 non-oracle images and then produces the main target for those images. Oracle repeats validate the model family, but the paper does not report an E031-style outer stimulus fold in which every target prediction is produced by a denoiser that did not train on that stimulus.
3. **The system-identification model is not fully self-contained in the paper.** Key architecture and regularization details point to prior work, limiting exact reproduction from this paper alone.
4. **Biological scope is narrow.** The source is mouse V1 under passive grayscale image viewing, while the intervention is a vision classifier. This does not establish transfer to human language fMRI, EEG, ECoG, or LLM hidden states.
5. **Animal and scan dependence is incompletely reported.** The paper gives eight scan-level targets across animals and days but does not state the exact number of animals in the inspected text.
6. **Layer selection is unstable.** The softmax mixture usually collapses to one of several nearby layers, and the authors state that more simulations are needed. There is no matched fixed-layer versus learned-mixture factorial.
7. **Inference is limited.** Main corruption results use five seeds and SEM, while the supplementary regularization-strength sweep uses only two or three seeds per setting. The paper does not report a participant- or animal-level inferential test for the classifier gain.
8. **Raw-target failure is outcome-specific.** The direct neural-data target failed to reproduce the Gaussian-noise robustness boost and was not tested in the adversarial analysis. It should not be generalized to every neural target or endpoint.
9. **Preprint status.** The cited artifact is an arXiv preprint; a peer-reviewed venue is `\gap`.

## Relevance to this thesis

### Relevance to H002

This is the clearest precedent for the stronger form of H002: biological measurements can supervise a target builder, and the resulting model-derived latent can be a better intervention target than the raw measurements. The paper combines three reliability operations that H002 can separate prospectively: neuron weighting from repeats, predictive-reliability weighting, and averaging across scan-specific geometries.

The paper also identifies the central attribution danger. Once a stimulus-to-brain model replaces the measurement, the target contains the model's inductive bias and stimulus information as well as neural information. H002 therefore needs untouched-participant or untouched-repeat prediction, nuisance subtraction, matched text or stimulus targets, content-destroyed twins, and scale/spectrum/headroom matching before calling a denoiser output biological.

### Relevance to E031

E031 correctly places target-information recovery before student training. The Li et al. result suggests a bounded nonlinear follow-on only if E031's simpler source-mean, residual-mean, reliability-weighted, and shared-linear builders fail despite adequate repeat reliability.

The eligible nonlinear analogue would fit a system-identification model inside each outer training fold, produce predictions for untouched stimuli and participants, weight outputs using fold-local repeat reliability, and compare the resulting target with raw, unweighted, deranged, nuisance-only, and matched nonbiological targets. Training the denoiser on the same stimuli later used to score target recovery would not reproduce E031's estimand.

E031 does not select an LM loss layer, and this paper does not settle that question. It supplies one concrete candidate for a later placement gate: compare a predeclared middle layer, a late hidden layer, and a learned non-negative multi-layer mixture under matched gradient scale. Because Li et al.'s mixture often collapsed stochastically to one nearby layer, layer identity must be selected only within training folds and evaluated on sealed units.

## Verified

Read in body from the complete arXiv paper and supplementary material, with canonical metadata checked against arXiv. The denoiser, raw-target ablation, target construction, layer-mixture loss, controls, outcomes, and stated limitations were verified from the paper body. All numerical values are external-paper evidence only and do not become thesis numbers.

## Related

- [`H002`](../../hypotheses/H002_repeat-stable-biological-supervision.md) - repeat-stable, participant-preserving biological supervision
- [`E031`](../../experiments/E031_biological-target-information-recovery.md) - prospective target-information recovery gate
- [Pirlot et al. 2022](pirlot-2022_dcca-neural-regularizer-cnns.md) - neural representational regularization with a shuffled-label control
- [`literature/AGENTS.md`](../AGENTS.md) - canonical literature-note contract
