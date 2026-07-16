---
title: "Package B directional transfer boundary (draft)"
tags: [reference]
aliases: [package-b-directional-boundary, directional-transfer-certificate]
---

# Package B directional transfer boundary (draft)

**Created:** 2026-07-17

**Status:** DRAFT THEORY FEASIBILITY NOTE, NON-AUTHORITATIVE, NOT A NOVELTY CLAIM

**Current recommendation:** HOLD Package B

> [!IMPORTANT]
> This note is a working derivation, not an experiment result, decision, or manuscript claim. It introduces no thesis number. If the proposal survives mathematical, novelty, and prospective empirical review, accepted content must be routed to the existing authorities rather than treating this note as a new authority.

## Question and evidence boundary

[E016](../experiments/E016_tribe-synthetic-brain-targets.md) and [E025](../experiments/E025_participant-e016-biological-transfer.md) separate three events that a useful theory must not collapse: the auxiliary target was learned, the retained student moved, and language quality was matched, but the fixed individual-brain endpoint did not improve participant-generally. [D058](../decisions/decisions.md#d058-e025-kills-the-participant-positive-continuation-and-sharpens-package-a-2026-07-16-work--interpret) therefore keeps Package B on HOLD until an observable certificate predicts both a failure and a success regime.

The strongest currently identifiable statement is local and algorithm-specific:

> For a fixed learner, optimizer state, step, and endpoint risk, the sign of auxiliary value is determined by the endpoint-directional effect of the induced update, minus curvature and stochastic-update costs. Target reliability, held-out target fit, output geometry, effective rank, and movement magnitude can establish availability and manipulation, but cannot determine that sign without a directional relation to the endpoint.

This is deliberately narrower than a claim that brain supervision cannot help. It is also narrower than a Bayes value-of-information statement. A deterministic target can add no test-time information conditional on the stimulus and still alter a finite learner's optimization path.

## Estimand

Let $\theta$ be a common pre-update parameter vector and let $s\in\{B,C\}$ index a proposed auxiliary target $B$ and a matched control $C$. Let $\widehat u_s$ be the complete stochastic direction actually applied by the optimizer for arm $s$, after the common primary or KD gradient, weighted auxiliary gradient, weight decay, clipping, momentum, preconditioning, and any coupled terms have been combined. Let $\eta>0$ be the common scalar step size:

$$
\theta_s^+=\theta-\eta\widehat u_s.
$$

Let $R(\theta)$ be a lower-is-better endpoint risk on a distribution independent of the auxiliary-training minibatch. Define the one-step incremental value of $B$ over $C$ as

$$
V_{B:C}=\mathbb E\!\left[R(\theta_C^+)-R(\theta_B^+)\mid\theta\right].
$$

Positive $V_{B:C}$ means that the proposed auxiliary target produces a better endpoint after the paired step. This is the estimand of the local certificate. It is not automatically the final-checkpoint unique-$R^2$ estimand used in [E025](../experiments/E025_participant-e016-biological-transfer.md).

## Directional insufficiency result

### Proposition

No collection of target-only diagnostics can universally determine the sign of $V_{B:C}$ if it contains no directional coupling between the induced update and the endpoint.

More precisely, fix any nonzero induced update $d$ and any diagnostic map $\Phi$ that is computed without the endpoint risk. The same target, learner, update, target fit, target covariance, spectrum, effective rank, reliability, sample size, and movement magnitude can be paired with two smooth endpoint risks

$$
R_\pm(\theta+u)=c\pm a^\top u+\tfrac12u^\top H u,
$$

where $a^\top d\ne0$ and the value, Hessian, and every target-side diagnostic are otherwise identical. For a sufficiently small step, the endpoint benefit has opposite signs under $R_+$ and $R_-$. Therefore no decision rule $h(\Phi)$ can be sign-correct over both problems.

### Proof

The target and update are fixed, so every component of $\Phi$ is the same in the two problems. The change in endpoint risk along $d$ is

$$
R_\pm(\theta+d)-R_\pm(\theta)=\pm a^\top d+\tfrac12d^\top H d.
$$

For $d$ scaled small enough, the nonzero linear term dominates the common quadratic term, giving opposite signs. A rule that sees only the identical $\Phi$ must return the same sign for both and is wrong on at least one. $\square$

### Fixed-endpoint isometric construction

The insufficiency is not only an across-endpoint artifact. Consider scalar $x$ with $m_2=\mathbb E[x^2]>0$, a scalar student output $h_\theta(x)=\theta x$ at $\theta=0$, and two auxiliary targets $y_+(x)=x$ and $y_-(x)=-x$. Their Gram matrices, covariance spectra, effective ranks, marginal entropies under reflection, reliability, predictability from $x$, optimal target fit, and mutual information with any variable up to the invertible sign map are equal. Their squared-loss gradients are $q_+=-m_2$ and $q_-=+m_2$, so their step magnitudes and post-step target fits are also equal.

For the fixed endpoint risk $R(\theta)=\tfrac12(\theta-1)^2$ and $a=\eta m_2$, gradient descent gives $\theta_+^+=a$ and $\theta_-^+=-a$. Their endpoint improvements relative to $\theta=0$ are

$$
V_+=a-\tfrac12a^2,
\qquad
V_-=-a-\tfrac12a^2.
$$

For $0<a<2$, the first target helps and the isometric second target harms. The sign-bearing difference is the orientation of the induced parameter update relative to the endpoint, not any target-only geometry or fit statistic. A learned auxiliary head can remove some output-coordinate symmetries, so this construction is an algebraic counterexample rather than a claim about E016's exact architecture.

### Consequences

- Held-out target fit and representation movement are manipulation gates. They reject a no-op explanation but do not imply endpoint benefit.
- Rank, spectrum, intrinsic dimension, entropy, and reliability can constrain estimability, gradient variance, and the possible magnitude of an update. They do not supply its endpoint-facing sign.
- Scalar conditional mutual information can upper-bound or characterize available predictive information under additional assumptions, but it does not determine whether a fixed finite algorithm uses that information beneficially.
- Cauchy-Schwarz gives the first-order magnitude envelope $|r^\top u|\le\|r\|\,\|u\|$. Under a fixed linear preconditioner $u=Mq$, this becomes $|r^\top Mq|\le\|M^\top r\|\,\|q\|$. A target-side diagnostic may help bound the update norm, but the omitted cosine remains the sign-bearing term.

## Exact one-step quadratic certificate

### Assumptions

1. **Common state and update rule.** The two arms start from the same $\theta$ and optimizer state and use the same $\eta$, batching rule, primary objective, regularization, clipping rule, and compute. Only the frozen auxiliary target changes.
2. **Complete applied update.** $\widehat u_s$ is the direction actually returned by the optimizer, not the auxiliary gradient in isolation. Define $\mu_s=\mathbb E[\widehat u_s\mid\theta]$ and $\Gamma_s=\operatorname{Cov}(\widehat u_s\mid\theta)$, with finite second moments. This definition permits a nonlinear optimizer map, provided the complete arm-specific applied direction is measured.
3. **Quadratic endpoint on the step support.** For every realized step in the support,

   $$
   R(\theta+d)=R(\theta)+r^\top d+\tfrac12d^\top H d,
   $$

   where $r=\nabla R(\theta)$ and $H=H^\top$ are fixed. Convexity is not required for the identity.
4. **Independent endpoint measurement.** The data estimating $R$, $r$, and $H$ are independent of the auxiliary minibatch and do not include the locked confirmation participants or stimuli used for the final transfer test.
5. **Transport for prospective use.** Applying a certificate estimated on calibration participants to confirmation participants additionally assumes that the distribution of endpoint-directional and curvature terms is exchangeable or otherwise transportable across those groups. The quadratic identity itself is conditional on the calibration endpoint and does not provide this transport guarantee.

### Identity

Then

$$
\mathbb E[R(\theta_s^+)\mid\theta]
=R(\theta)-\eta r^\top\mu_s
+\frac{\eta^2}{2}\left(\mu_s^\top H\mu_s+\operatorname{tr}(H\Gamma_s)\right).
$$

Therefore the exact expected one-step value contrast is

$$
\boxed{
V_{B:C}
=\eta r^\top(\mu_B-\mu_C)
-\frac{\eta^2}{2}
\left[
\mu_B^\top H\mu_B-\mu_C^\top H\mu_C
+\operatorname{tr}\!\left(H(\Gamma_B-\Gamma_C)\right)
\right].
}
$$

The proof substitutes $d=-\eta\widehat u_s$ into the quadratic expansion and uses $\mathbb E[\widehat u_s^\top H\widehat u_s]=\mu_s^\top H\mu_s+\operatorname{tr}(H\Gamma_s)$.

For a fixed linear preconditioner $M$ and raw complete direction $\widehat q_s$, set $\widehat u_s=M\widehat q_s$, $\mu_s=Mq_s$, and $\Gamma_s=M\Omega_sM^\top$. The identity then becomes

$$
V_{B:C}
=\eta r^\top M(q_B-q_C)
-\frac{\eta^2}{2}
\left[
q_B^\top Kq_B-q_C^\top Kq_C
+\operatorname{tr}\!\left(K(\Omega_B-\Omega_C)\right)
\right],
\qquad K=M^\top H M.
$$

If the step is defined after a common primary update and contains only a weighted auxiliary gradient, set $q_s=\lambda g_s$. For iid per-example gradients with covariance $\Sigma_s$ and minibatch size $b$, $\Omega_s=\lambda^2\Sigma_s/b$. If the primary and auxiliary gradients share a minibatch, their covariance and the curvature cross-term belong in the complete applied update and must not be assumed to cancel. For Adam-like optimizers, using a single common $M$ is valid only if its state and current-step denominator are frozen; otherwise measure $\widehat u_s$ after the arm-specific nonlinear optimizer transform.

### Interpretation

The certificate contains three distinct objects:

- **Directional benefit:** $r^\top\mu_s$, the endpoint gradient applied to the mean optimizer-transformed update.
- **Deterministic curvature cost or benefit:** $\mu_s^\top H\mu_s$.
- **Stochastic curvature cost or benefit:** $\operatorname{tr}(H\Gamma_s)$, which exposes finite-batch update variance and its orientation in endpoint curvature.

When $r^\top(\mu_B-\mu_C)\ne0$, the directional term determines the sign as $\eta\to0$. At finite $\eta$, norm matching is still insufficient because curvature and update-noise orientation can reverse the first-order prediction.

### Smooth nonquadratic lower bound

If $R$ has a $\rho$-Lipschitz Hessian on every line segment reached by either arm, the third-order Taylor remainder gives

$$
V_{B:C}
\ge \widetilde V_{B:C}^{\mathrm{quad}}
-\frac{\rho\eta^3}{6}
\left(
\mathbb E\|\widehat u_B\|^3
+\mathbb E\|\widehat u_C\|^3
\right),
$$

where $\widetilde V_{B:C}^{\mathrm{quad}}$ is the boxed expression. This is useful only if the remainder terms are bounded without inspecting the confirmation endpoint. An unmeasured global smoothness constant would make the bound formally true but empirically vacuous.

## Observable implementation

For a squared-error endpoint with a fixed, calibration-only readout and a linearized retained representation, the surrogate is exactly quadratic in the local update. If $e$ is the fixed endpoint residual and $J$ is the Jacobian of its prediction with respect to retained-student parameters, then

$$
R_{\mathrm{lin}}(\theta+d)=\frac{1}{2m}\|e+Jd\|^2,
\qquad
r=J^\top e/m,
\qquad
H=J^\top J/m.
$$

The certificate can therefore be evaluated with vector-Jacobian and Hessian-vector products without materializing $H$. This surrogate must use nuisance residualization, fold-only preprocessing, a readout fixed before candidate comparison, and calibration participants disjoint from confirmation participants. Its relation to final cross-validated unique $R^2$ is empirical, not an identity.

For participant data, compute one certificate value per calibration participant after averaging technical minibatches and seeds. Participants remain the population inference unit. Seeds and gradient samples quantify optimization variability, not biological replication.

## What the certificate does not prove

- It is exact for one step under a quadratic endpoint, not for a long nonconvex training trajectory.
- A favorable first step is neither necessary nor sufficient for a favorable final checkpoint without path-stability assumptions. Momentum, adaptive optimizer state, basin changes, and representation-readout refitting can reverse the result.
- Estimating an endpoint gradient on the same participants later used for confirmation leaks the answer and converts a prospective test into validation-set optimization.
- A certificate for a differentiable residual-MSE surrogate does not guarantee a sign for the E025 unique-$R^2$ estimand.
- An endpoint-aware target selected using the same calibration data can demonstrate control but cannot establish intrinsic biological specificity.

## Collision audit and novelty boundary

The generic theory neighborhood is already occupied. [Lopez-Paz et al.](../literature/canonical/lopez-paz-2016_unifying-distillation-privileged-information.md) give capacity and approximation-error conditions for generalized distillation. [Saadi and Wang](../literature/canonical/saadi-2026_task-tangent-feature-distillation-llms.md) prioritize task-functional directions over raw representation geometry. [Du et al.](https://arxiv.org/abs/1812.02224) adapt auxiliary losses using primary-auxiliary gradient similarity, [ATTITTUD](https://openreview.net/forum?id=1GTma8HwlYp) decomposes auxiliary updates using the target-task direction, and [Task Affinity Grouping](https://proceedings.neurips.cc/paper/2021/hash/e77910ebb93b511588557806310f78f1-Abstract.html) directly measures how one task's gradient changes another task's loss during training. [ForkMerge](https://proceedings.neurips.cc/paper_files/paper/2023/hash/60f9118a849e8e9a0c67e2a36ad80ebf-Abstract-Conference.html) reports that gradient conflict alone does not predict final negative transfer, and [Moment Alignment](https://proceedings.mlr.press/v286/chen25f.html) develops gradient and Hessian matching theory for domain generalization. Validation-gradient reweighting, bilevel optimization, influence functions, and one-step Taylor data valuation create additional obvious collisions.

Accordingly, neither the insufficiency proposition nor the boxed quadratic identity is claimed as a novel theorem. A publishable contribution would have to be a stronger result or a distinctive, prospectively validated certificate for training-only targets under independent endpoint measurement. A full primary-source collision audit is mandatory before changing Package B from HOLD.

## Decision boundary for Package B

**Current recommendation: HOLD, not GO.** The note supplies a precise estimand and a falsifiable observable, but the mathematical core is elementary, local, and close to existing task-affinity and bilevel ideas. No prospective positive and failure regime has yet been predicted, and the endpoint-gradient terms may be too costly or unstable in the biological setting.

Package B can move to GO only if all of the following occur:

1. An independent mathematical review verifies the identity, the nonquadratic remainder, and the no-go scope.
2. The proposed certificate is estimable with fixed memory and compute, using participant-disjoint calibration and confirmation data.
3. Before outcomes are opened, it predicts at least one failure regime and one positive regime, including uncertainty and an abstention region.
4. The predictions survive final-checkpoint transfer at the correct biological inference unit and beat target-only diagnostics in prospective discrimination.
5. A full collision audit establishes a contribution beyond task affinity, auxiliary-task weighting, hypergradients, influence functions, generalized distillation, and functional feature distillation.

Kill Package B as a paper identity if the certificate cannot predict beyond a one-step synthetic quadratic, if it needs endpoint feedback from the confirmation units, if target-only and directional diagnostics perform indistinguishably, if the result fails on either a predeclared positive or failure regime, or if the novelty audit shows the same certificate and validation design already exists. Package A remains scientifically valid under any of those outcomes.

## Related

- [`status.md`](../status.md) - operational authority
- [`D057 and D058`](../decisions/decisions.md#d057-canonical-three-package-conference-extension-strategy-and-provenance-2026-07-14-plan--meta) - package gates and E025 consequence
- [`E025`](../experiments/E025_participant-e016-biological-transfer.md) - manipulation-success and biological-transfer-failure evidence
- [`E029`](../experiments/E029_directional-transfer-certificate.md) - proposed prospective falsification design
- [`06-theory-grounding.md`](../06-theory-grounding.md) - current theory grounding authority
