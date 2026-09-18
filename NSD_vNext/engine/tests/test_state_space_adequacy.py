import numpy as np
import pytest

from nsd_engine.latent_oscillator_covariance import (
    LatentOscillatorTruth,
    simulate_latent_oscillator,
)
from nsd_engine.state_space_adequacy import (\n    compare_state_space_candidates,\n    evaluate_comparison_on_holdout,\n)


FS = 256.0
SECONDS = 15.0


def _standardize(values):
    values = np.asarray(values, dtype=float)
    return (values - np.mean(values)) / np.std(values)


def _ar1(phi, seed):
    rng = np.random.default_rng(seed)
    epsilon = rng.normal(size=int(FS * SECONDS))
    values = np.zeros_like(epsilon)
    scale = np.sqrt(1.0 - phi * phi)
    for index in range(1, values.size):
        values[index] = phi * values[index - 1] + scale * epsilon[index]
    return _standardize(values)


def test_single_oscillator_known_truth_prefers_a1():
    signal = simulate_latent_oscillator(
        LatentOscillatorTruth(10.0, 0.30, FS),
        seconds=SECONDS,
        measurement_noise_to_latent_sd=0.5,
        seed=0,
    )
    result = compare_state_space_candidates(
        signal,
        FS,
        optimizer_maxiter=60,
    )

    assert result.bic_winner == "A1"
    assert result.by_family("A1").bic < result.by_family("A0").bic
    assert result.by_family("A1").bic < result.by_family("A2").bic


def test_nonoscillatory_ar1_known_bad_for_single_oscillator_prefers_a0():
    signal = _ar1(0.97, seed=600)
    result = compare_state_space_candidates(
        signal,
        FS,
        optimizer_maxiter=60,
    )

    assert result.bic_winner == "A0"
    assert result.by_family("A0").bic < result.by_family("A1").bic


def test_separated_two_mode_known_bad_for_single_oscillator_prefers_a2():
    first = simulate_latent_oscillator(
        LatentOscillatorTruth(10.0, 0.25, FS),
        seconds=SECONDS,
        measurement_noise_to_latent_sd=0.0,
        seed=0,
    )
    second = simulate_latent_oscillator(
        LatentOscillatorTruth(20.0, 0.35, FS),
        seconds=SECONDS,
        measurement_noise_to_latent_sd=0.0,
        seed=100,
    )
    rng = np.random.default_rng(200)
    signal = _standardize(
        0.8 * _standardize(first)
        + 0.8 * _standardize(second)
        + rng.normal(0.0, 0.35, size=first.size)
    )
    result = compare_state_space_candidates(
        signal,
        FS,
        optimizer_maxiter=60,
    )

    assert result.bic_winner == "A2"
    assert result.by_family("A2").bic < result.by_family("A1").bic


def test_state_space_candidates_reject_nonfinite_input():
    signal = np.ones(1500)
    signal[25] = np.nan
    with pytest.raises(ValueError, match="non-finite"):
        compare_state_space_candidates(signal, FS)


def test_state_space_candidates_reject_too_short_input():
    with pytest.raises(ValueError, match="at least"):
        compare_state_space_candidates(np.arange(100.0), FS)



def test_stationary_single_oscillator_holdout_prefers_a1():
    signal = simulate_latent_oscillator(
        LatentOscillatorTruth(10.0, 0.30, FS),
        seconds=30.0,
        measurement_noise_to_latent_sd=0.5,
        seed=3,
    )
    midpoint = signal.size // 2
    training = compare_state_space_candidates(
        signal[:midpoint],
        FS,
        optimizer_maxiter=60,
    )
    holdout = evaluate_comparison_on_holdout(training, signal[midpoint:])

    assert holdout["winner"] == "A1"
    assert (
        holdout["negative_log_likelihood_per_sample"]["A1"]
        < holdout["negative_log_likelihood_per_sample"]["A0"]
    )
