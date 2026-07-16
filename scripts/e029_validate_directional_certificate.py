#!/usr/bin/env python3
"""Deterministic algebra checks for E029.

This script validates identities and counterexamples only. It does not load research
data, train a model, or produce a scientific result.
"""

from __future__ import annotations

import itertools

import numpy as np


ATOL = 1e-12


def quadratic_risk(theta: np.ndarray, r: np.ndarray, hessian: np.ndarray) -> float:
    return float(r @ theta + 0.5 * theta @ hessian @ theta)


def finite_support(mean: np.ndarray, scales: np.ndarray) -> tuple[list[np.ndarray], np.ndarray]:
    """Return equally weighted mean plus independent Rademacher perturbations."""
    directions = []
    for signs in itertools.product((-1.0, 1.0), repeat=mean.size):
        directions.append(mean + scales * np.asarray(signs))
    covariance = np.diag(scales**2)
    return directions, covariance


def expected_post_step_risk(
    directions: list[np.ndarray],
    eta: float,
    preconditioner: np.ndarray,
    r: np.ndarray,
    hessian: np.ndarray,
) -> float:
    values = [
        quadratic_risk(-eta * preconditioner @ direction, r, hessian)
        for direction in directions
    ]
    return float(np.mean(values))


def certificate_arm_risk(
    mean: np.ndarray,
    covariance: np.ndarray,
    eta: float,
    preconditioner: np.ndarray,
    r: np.ndarray,
    hessian: np.ndarray,
) -> float:
    curvature = preconditioner.T @ hessian @ preconditioner
    return float(
        -eta * r @ preconditioner @ mean
        + 0.5
        * eta**2
        * (mean @ curvature @ mean + np.trace(curvature @ covariance))
    )


def check_exact_stochastic_identity() -> None:
    rng = np.random.default_rng(29)
    dimension = 4
    r = rng.normal(size=dimension)
    a = rng.normal(size=(dimension, dimension))
    hessian = a.T @ a + 0.2 * np.eye(dimension)
    preconditioner = np.diag(np.array([0.5, 0.8, 1.1, 1.4]))
    eta = 0.07

    means = [rng.normal(size=dimension), rng.normal(size=dimension)]
    scales = [
        np.array([0.03, 0.06, 0.02, 0.04]),
        np.array([0.05, 0.01, 0.07, 0.02]),
    ]

    exact_risks = []
    formula_risks = []
    for mean, scale in zip(means, scales, strict=True):
        support, covariance = finite_support(mean, scale)
        exact_risks.append(
            expected_post_step_risk(support, eta, preconditioner, r, hessian)
        )
        formula_risks.append(
            certificate_arm_risk(
                mean, covariance, eta, preconditioner, r, hessian
            )
        )

    np.testing.assert_allclose(exact_risks, formula_risks, atol=ATOL, rtol=0.0)
    exact_value = exact_risks[1] - exact_risks[0]
    formula_value = formula_risks[1] - formula_risks[0]
    np.testing.assert_allclose(exact_value, formula_value, atol=ATOL, rtol=0.0)


def check_isometric_targets_opposite_transfer() -> None:
    x = np.linspace(-2.0, 2.0, 101)
    y_positive = x.copy()
    y_negative = -x

    np.testing.assert_allclose(
        np.outer(y_positive, y_positive),
        np.outer(y_negative, y_negative),
        atol=ATOL,
        rtol=0.0,
    )
    np.testing.assert_allclose(
        np.linalg.svd(y_positive[:, None], compute_uv=False),
        np.linalg.svd(y_negative[:, None], compute_uv=False),
        atol=ATOL,
        rtol=0.0,
    )
    np.testing.assert_allclose(
        [np.mean(y_positive), np.var(y_positive)],
        [np.mean(y_negative), np.var(y_negative)],
        atol=ATOL,
        rtol=0.0,
    )

    theta0 = 0.0
    gradient_positive = float(np.mean((theta0 * x - y_positive) * x))
    gradient_negative = float(np.mean((theta0 * x - y_negative) * x))
    np.testing.assert_allclose(
        gradient_positive, -gradient_negative, atol=ATOL, rtol=0.0
    )

    baseline_fit_positive = float(np.mean((theta0 * x - y_positive) ** 2))
    baseline_fit_negative = float(np.mean((theta0 * x - y_negative) ** 2))
    np.testing.assert_allclose(
        baseline_fit_positive, baseline_fit_negative, atol=ATOL, rtol=0.0
    )
    optimal_fit_positive = float(np.mean((1.0 * x - y_positive) ** 2))
    optimal_fit_negative = float(np.mean((-1.0 * x - y_negative) ** 2))
    np.testing.assert_allclose(
        optimal_fit_positive, optimal_fit_negative, atol=ATOL, rtol=0.0
    )
    np.testing.assert_allclose(optimal_fit_positive, 0.0, atol=ATOL, rtol=0.0)

    eta = 0.2 / float(np.mean(x**2))
    theta_positive = theta0 - eta * gradient_positive
    theta_negative = theta0 - eta * gradient_negative
    np.testing.assert_allclose(
        abs(theta_positive - theta0),
        abs(theta_negative - theta0),
        atol=ATOL,
        rtol=0.0,
    )

    post_fit_positive = float(np.mean((theta_positive * x - y_positive) ** 2))
    post_fit_negative = float(np.mean((theta_negative * x - y_negative) ** 2))
    np.testing.assert_allclose(
        post_fit_positive, post_fit_negative, atol=ATOL, rtol=0.0
    )

    endpoint = lambda theta: 0.5 * (theta - 1.0) ** 2
    value_positive = endpoint(theta0) - endpoint(theta_positive)
    value_negative = endpoint(theta0) - endpoint(theta_negative)
    assert value_positive > 0.0
    assert value_negative < 0.0


def check_complete_update_is_required() -> None:
    r = np.array([0.4, -0.2])
    hessian = np.array([[2.0, 0.6], [0.6, 1.0]])
    preconditioner = np.eye(2)
    eta = 0.1
    common = np.array([1.2, -0.7])
    auxiliary_b = np.array([0.3, 0.8])
    auxiliary_c = np.array([-0.2, 0.5])

    total_b = common + auxiliary_b
    total_c = common + auxiliary_c
    zero = np.zeros((2, 2))
    full_value = certificate_arm_risk(
        total_c, zero, eta, preconditioner, r, hessian
    ) - certificate_arm_risk(total_b, zero, eta, preconditioner, r, hessian)
    isolated_value = certificate_arm_risk(
        auxiliary_c, zero, eta, preconditioner, r, hessian
    ) - certificate_arm_risk(
        auxiliary_b, zero, eta, preconditioner, r, hessian
    )
    assert not np.isclose(full_value, isolated_value, atol=1e-6, rtol=0.0)
    assert np.sign(full_value) != np.sign(isolated_value)


def main() -> None:
    check_exact_stochastic_identity()
    check_isometric_targets_opposite_transfer()
    check_complete_update_is_required()
    print("PASS: E029 directional-certificate algebra and counterexamples")


if __name__ == "__main__":
    main()
