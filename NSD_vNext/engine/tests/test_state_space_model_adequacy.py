import math

import numpy as np
import pytest

from nsd_engine.latent_oscillator_covariance import (
    LatentOscillatorTruth,
    simulate_latent_oscillator,
)
from nsd_engine.state_space_model_adequacy import (
    StateSpaceFamily,
    fit_state_space_candidate,
    kalman_innovations_nll,
)


FS = 128.0


def _ar1(phi: float, seconds: float, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n = int(round(seconds * FS))
    eps = rng.normal(size=n)
    x = np.zeros(n, dtype=float)
    scale = math.sqrt(1.0 - phi * phi)
    for i in range(1, n):
        x[i] = phi * x[i - 1] + scale * eps[i]
    return x


def test_kalman_likelihood_rejects_unstable_transition():
    y = np.ones(128, dtype=float)
    with pytest.raises(ValueError, match="stable"):
        kalman_innovations_nll(
            y,
            np.asarray([[1.01]]),
            np.asarray([[0.1]]),
            np.asarray([1.0]),
            0.1,
        )


def test_a0_beats_a1_on_nonoscillatory_known_truth():
    signal = _ar1(0.96, seconds=10.0, seed=20260918)
    a0 = fit_state_space_candidate(
        signal,
        FS,
        StateSpaceFamily.A0_RELAXATION,
        fmin_hz=1.0,
        fmax_hz=35.0,
        maxiter=100,
    )
    a1 = fit_state_space_candidate(
        signal,
        FS,
        StateSpaceFamily.A1_SINGLE_OSCILLATOR,
        fmin_hz=1.0,
        fmax_hz=35.0,
        maxiter=100,
    )
    assert a0.bic < a1.bic
    assert a0.heldout_negative_log_likelihood_per_sample < a1.heldout_negative_log_likelihood_per_sample


def test_a1_beats_a0_on_single_oscillator_known_truth():
    signal = simulate_latent_oscillator(
        LatentOscillatorTruth(10.0, 0.30, FS),
        seconds=10.0,
        measurement_noise_to_latent_sd=0.45,
        seed=20260918,
    )
    a0 = fit_state_space_candidate(
        signal,
        FS,
        StateSpaceFamily.A0_RELAXATION,
        fmin_hz=1.0,
        fmax_hz=35.0,
        maxiter=100,
    )
    a1 = fit_state_space_candidate(
        signal,
        FS,
        StateSpaceFamily.A1_SINGLE_OSCILLATOR,
        fmin_hz=1.0,
        fmax_hz=35.0,
        maxiter=100,
    )
    assert a1.bic < a0.bic
    assert a1.heldout_negative_log_likelihood_per_sample < a0.heldout_negative_log_likelihood_per_sample
    assert len(a1.modes) == 1
    assert a1.modes[0].natural_frequency_hz == pytest.approx(10.0, rel=0.20)
