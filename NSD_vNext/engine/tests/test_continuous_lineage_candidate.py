"""Contracts for the qualification-only one-mode continuous-lineage candidate."""

from __future__ import annotations

import math

import numpy as np
import pytest

from nsd_engine.continuous_lineage_candidate import _build_candidate
from nsd_engine.state_space_adequacy import _build_model


FS = 256.0
FMIN = 1.0
FMAX = 45.0


def _raw_for(A: float, rho: float, fd: float, g: float):
    from nsd_engine.state_space_adequacy import _raw_fraction, _raw_rho, _raw_frequency

    return np.asarray(
        [
            _raw_fraction(A),
            _raw_rho(rho),
            _raw_frequency(fd, FMIN, FMAX),
            np.arctanh(g),
        ],
        dtype=float,
    )


def _output_covariances(F, P, obs, max_lag=8):
    values = []
    power = np.eye(F.shape[0])
    for lag in range(max_lag + 1):
        values.append(float(obs @ power @ P @ obs))
        power = power @ F
    return np.asarray(values)


def test_g_zero_candidate_matches_a1_scalar_covariance():
    A = 0.8
    rho = 0.93
    fd = 10.0

    raw_c = _raw_for(A, rho, fd, 0.0)
    F_c, _, obs_c, _, params_c = _build_candidate(raw_c, FS, FMIN, FMAX)

    # Construct the stationary covariance used by the candidate gauge.
    alpha = -math.log(params_c["rho"]) * FS
    nu = 2.0 * math.pi * params_c["damped_frequency_hz"]
    P_c = np.asarray(
        [
            [params_c["latent_fraction"], 0.0],
            [
                0.0,
                params_c["latent_fraction"] * (2.0 * alpha * alpha + nu * nu),
            ],
        ]
    )

    raw_a1 = raw_c[:3]
    F_a1, _, obs_a1, _, _ = _build_model("A1", raw_a1, FS, FMIN, FMAX)
    P_a1 = params_c["latent_fraction"] * np.eye(2)

    gamma_c = _output_covariances(F_c, P_c, obs_c)
    gamma_a1 = _output_covariances(F_a1, P_a1, obs_a1)
    np.testing.assert_allclose(gamma_c, gamma_a1, rtol=2e-11, atol=2e-11)


@pytest.mark.parametrize("g", [-0.75, -0.3, 0.3, 0.75])
def test_nonzero_g_candidate_builds_psd_discrete_process(g: float):
    A = 0.8
    rho = 0.93
    fd = 10.0
    raw = _raw_for(A, rho, fd, g)
    F, Q, obs, R, params = _build_candidate(raw, FS, FMIN, FMAX)

    assert F.shape == (2, 2)
    assert obs.shape == (2,)
    assert R > 0.0
    assert np.min(np.linalg.eigvalsh(Q)) >= -1e-10
    assert params["g"] == pytest.approx(g, rel=1e-12, abs=1e-12)
    assert params["H"] != pytest.approx(0.0, abs=1e-14)
    assert 0.0 < params["damping_ratio"] < 1.0


def test_candidate_has_exactly_one_more_parameter_than_a1():
    # This is a qualification bookkeeping contract only.
    current_a1_parameter_count = 3
    candidate_parameter_count = 4
    assert candidate_parameter_count == current_a1_parameter_count + 1
