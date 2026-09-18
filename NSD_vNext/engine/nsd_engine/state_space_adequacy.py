"""Likelihood-based state-space adequacy candidates for NSD modal P0-Q.

This module implements the frozen A0/A1/A2 qualification architecture:

A0: one nonoscillatory latent AR(1)-like relaxation state
A1: one latent damped oscillator
A2: two independent latent damped oscillators

All models include explicit white observation noise and are fit to the same
standardized scalar signal. Model comparison uses a steady-state Kalman
innovations likelihood and BIC. This is qualification infrastructure only.
A BIC winner is not an admission decision for real EEG, does not license a
biological mode, and does not license damping or chi.

The likelihood drops an initial innovations burn-in so comparison is not driven
by the arbitrary zero predictor state. Mean and scale normalization are shared
nuisance operations across A0/A1/A2 and therefore are not included in the
model-specific BIC parameter counts.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Literal, Sequence

import numpy as np
from scipy.linalg import block_diag, solve_discrete_are
from scipy.optimize import minimize
from scipy.signal import find_peaks, lfilter, ss2tf, welch


ModelFamily = Literal["A0", "A1", "A2"]

HOLDOUT_NUMERICAL_TIE_ATOL_PER_SAMPLE = 1e-8


@dataclass(frozen=True)
class StateSpaceModelFit:
    family: ModelFamily
    success: bool
    sample_count: int
    effective_sample_count: int
    burn_in_samples: int
    parameter_count: int
    negative_log_likelihood: float
    bic: float
    converged_start_count: int
    candidate_start_count: int
    attempted_start_count: int
    near_optimal_start_count: int
    start_nll_range: float
    parameters: dict[str, float]
    near_optimal_parameter_ranges: dict[str, tuple[float, float]]
    raw_parameters: tuple[float, ...]
    innovation_max_abs_autocorrelation: float
    innovation_rms: float
    optimizer_message: str


@dataclass(frozen=True)
class StateSpaceComparison:
    sampling_rate_hz: float
    fmin_hz: float
    fmax_hz: float
    sample_count: int
    standardization_mean: float
    standardization_sd: float
    fits: tuple[StateSpaceModelFit, ...]
    bic_winner: ModelFamily
    bic_margin_to_second: float

    def by_family(self, family: ModelFamily) -> StateSpaceModelFit:
        for fit in self.fits:
            if fit.family == family:
                return fit
        raise KeyError(family)


def _sigmoid(value: float) -> float:
    clipped = max(-40.0, min(40.0, float(value)))
    return 1.0 / (1.0 + math.exp(-clipped))


def _logit(probability: float) -> float:
    p = max(1e-8, min(1.0 - 1e-8, float(probability)))
    return math.log(p / (1.0 - p))


def _fraction_from_raw(value: float) -> float:
    return 1e-5 + (1.0 - 2e-5) * _sigmoid(value)


def _rho_from_raw(value: float) -> float:
    return 1e-3 + (0.999 - 1e-3) * _sigmoid(value)


def _frequency_from_raw(value: float, fmin_hz: float, fmax_hz: float) -> float:
    return fmin_hz + (fmax_hz - fmin_hz) * _sigmoid(value)


def _raw_fraction(value: float) -> float:
    return _logit((value - 1e-5) / (1.0 - 2e-5))


def _raw_rho(value: float) -> float:
    return _logit((value - 1e-3) / (0.999 - 1e-3))


def _raw_frequency(value: float, fmin_hz: float, fmax_hz: float) -> float:
    return _logit((value - fmin_hz) / (fmax_hz - fmin_hz))


def _oscillator_block(rho: float, frequency_hz: float, sampling_rate_hz: float) -> np.ndarray:
    theta = 2.0 * math.pi * frequency_hz / sampling_rate_hz
    c = math.cos(theta)
    s = math.sin(theta)
    return rho * np.asarray([[c, -s], [s, c]], dtype=np.float64)


def _derived_modal_values(rho: float, damped_frequency_hz: float, sampling_rate_hz: float) -> dict[str, float]:
    decay_rate = -math.log(rho) * sampling_rate_hz
    damped_omega = 2.0 * math.pi * damped_frequency_hz
    natural_omega = math.hypot(decay_rate, damped_omega)
    damping_ratio = decay_rate / natural_omega
    return {
        "decay_rate_per_s": float(decay_rate),
        "damped_frequency_hz": float(damped_frequency_hz),
        "natural_frequency_hz": float(natural_omega / (2.0 * math.pi)),
        "damping_ratio": float(damping_ratio),
    }


def _build_model(
    family: ModelFamily,
    raw: np.ndarray,
    sampling_rate_hz: float,
    fmin_hz: float,
    fmax_hz: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float, dict[str, float]]:
    if family == "A0":
        latent_fraction = _fraction_from_raw(raw[0])
        rho = _rho_from_raw(raw[1])
        transition = np.asarray([[rho]], dtype=np.float64)
        process_cov = np.asarray(
            [[latent_fraction * (1.0 - rho * rho)]],
            dtype=np.float64,
        )
        observation = np.asarray([1.0], dtype=np.float64)
        observation_variance = 1.0 - latent_fraction
        parameters = {
            "latent_fraction": latent_fraction,
            "rho": rho,
            "relaxation_rate_per_s": -math.log(rho) * sampling_rate_hz,
        }
        return transition, process_cov, observation, observation_variance, parameters

    if family == "A1":
        latent_fraction = _fraction_from_raw(raw[0])
        rho = _rho_from_raw(raw[1])
        frequency_hz = _frequency_from_raw(raw[2], fmin_hz, fmax_hz)
        transition = _oscillator_block(rho, frequency_hz, sampling_rate_hz)
        process_cov = latent_fraction * (1.0 - rho * rho) * np.eye(2)
        observation = np.asarray([1.0, 0.0], dtype=np.float64)
        observation_variance = 1.0 - latent_fraction
        parameters = {
            "latent_fraction": latent_fraction,
            "rho": rho,
            **_derived_modal_values(rho, frequency_hz, sampling_rate_hz),
        }
        return transition, process_cov, observation, observation_variance, parameters

    if family == "A2":
        total_latent_fraction = _fraction_from_raw(raw[0])
        split = 1e-4 + (1.0 - 2e-4) * _sigmoid(raw[1])
        first_fraction = total_latent_fraction * split
        second_fraction = total_latent_fraction * (1.0 - split)
        rho1 = _rho_from_raw(raw[2])
        rho2 = _rho_from_raw(raw[3])
        frequency1 = _frequency_from_raw(raw[4], fmin_hz, fmax_hz)
        frequency2 = _frequency_from_raw(raw[5], fmin_hz, fmax_hz)

        first_transition = _oscillator_block(rho1, frequency1, sampling_rate_hz)
        second_transition = _oscillator_block(rho2, frequency2, sampling_rate_hz)
        transition = block_diag(first_transition, second_transition)
        process_cov = block_diag(
            first_fraction * (1.0 - rho1 * rho1) * np.eye(2),
            second_fraction * (1.0 - rho2 * rho2) * np.eye(2),
        )
        observation = np.asarray([1.0, 0.0, 1.0, 0.0], dtype=np.float64)
        observation_variance = 1.0 - total_latent_fraction

        components = [
            (frequency1, first_fraction, rho1),
            (frequency2, second_fraction, rho2),
        ]
        components.sort(key=lambda item: item[0])
        parameters: dict[str, float] = {
            "total_latent_fraction": total_latent_fraction,
            "observation_noise_fraction": observation_variance,
        }
        for index, (frequency, fraction, rho) in enumerate(components, start=1):
            prefix = f"mode{index}_"
            parameters[prefix + "latent_fraction"] = fraction
            parameters[prefix + "rho"] = rho
            for key, value in _derived_modal_values(rho, frequency, sampling_rate_hz).items():
                parameters[prefix + key] = value
        return transition, process_cov, observation, observation_variance, parameters

    raise ValueError(f"unsupported model family {family!r}")


def _steady_state_filter(
    family: ModelFamily,
    raw: np.ndarray,
    sampling_rate_hz: float,
    fmin_hz: float,
    fmax_hz: float,
) -> tuple[np.ndarray, np.ndarray, float, dict[str, float]] | None:
    transition, process_cov, observation, observation_variance, parameters = _build_model(
        family,
        raw,
        sampling_rate_hz,
        fmin_hz,
        fmax_hz,
    )
    try:
        predicted_cov = solve_discrete_are(
            transition.T,
            observation.reshape(-1, 1),
            process_cov,
            np.asarray([[observation_variance]], dtype=np.float64),
        )
    except Exception:
        return None

    innovation_variance = float(
        observation @ predicted_cov @ observation + observation_variance
    )
    if not math.isfinite(innovation_variance) or innovation_variance <= 1e-12:
        return None

    gain = (predicted_cov @ observation) / innovation_variance
    predictor_transition = transition @ (
        np.eye(transition.shape[0]) - np.outer(gain, observation)
    )
    predictor_input = (transition @ gain).reshape(-1, 1)

    numerator, denominator = ss2tf(
        predictor_transition,
        predictor_input,
        observation.reshape(1, -1),
        np.asarray([[0.0]], dtype=np.float64),
    )
    numerator = np.asarray(numerator[0], dtype=np.float64)
    denominator = np.asarray(denominator, dtype=np.float64)
    if not np.isfinite(numerator).all() or not np.isfinite(denominator).all():
        return None
    return numerator, denominator, innovation_variance, parameters


def _innovations(
    standardized_signal: np.ndarray,
    family: ModelFamily,
    raw: np.ndarray,
    sampling_rate_hz: float,
    fmin_hz: float,
    fmax_hz: float,
) -> tuple[np.ndarray, float, dict[str, float]] | None:
    steady = _steady_state_filter(
        family,
        raw,
        sampling_rate_hz,
        fmin_hz,
        fmax_hz,
    )
    if steady is None:
        return None
    numerator, denominator, innovation_variance, parameters = steady
    prediction = lfilter(numerator, denominator, standardized_signal)
    innovation = standardized_signal - prediction
    if not np.isfinite(innovation).all():
        return None
    return innovation, innovation_variance, parameters


def _negative_log_likelihood(
    standardized_signal: np.ndarray,
    family: ModelFamily,
    raw: np.ndarray,
    sampling_rate_hz: float,
    fmin_hz: float,
    fmax_hz: float,
    burn_in_samples: int,
) -> float:
    result = _innovations(
        standardized_signal,
        family,
        raw,
        sampling_rate_hz,
        fmin_hz,
        fmax_hz,
    )
    if result is None:
        return 1e100
    innovation, innovation_variance, _ = result
    used = innovation[burn_in_samples:]
    if used.size < 3:
        return 1e100
    return float(
        0.5 * used.size * (math.log(2.0 * math.pi) + math.log(innovation_variance))
        + 0.5 * np.dot(used, used) / innovation_variance
    )



def _dedupe_frequency_candidates(
    candidates: Sequence[float],
    fmin_hz: float,
    fmax_hz: float,
    *,
    maximum: int,
    minimum_separation_hz: float,
) -> list[float]:
    kept: list[float] = []
    for value in candidates:
        frequency = float(value)
        if not math.isfinite(frequency):
            continue
        if frequency <= fmin_hz or frequency >= fmax_hz:
            continue
        if all(abs(frequency - prior) >= minimum_separation_hz for prior in kept):
            kept.append(frequency)
        if len(kept) >= maximum:
            break
    return kept


def _spectral_seed_frequencies(
    standardized_signal: np.ndarray,
    sampling_rate_hz: float,
    fmin_hz: float,
    fmax_hz: float,
    *,
    maximum: int = 16,
    minimum_separation_hz: float = 0.45,
) -> list[float]:
    """Generate broad deterministic optimizer starts, not scientific evidence."""
    nperseg = min(
        standardized_signal.size,
        max(256, int(round(4.0 * sampling_rate_hz))),
    )
    frequencies, power = welch(
        standardized_signal,
        fs=sampling_rate_hz,
        window="hann",
        nperseg=nperseg,
        noverlap=nperseg // 2,
        detrend="constant",
        scaling="density",
    )
    eligible = np.where(
        (frequencies > fmin_hz) & (frequencies < fmax_hz)
    )[0]
    spectral_candidates: list[float] = []
    if eligible.size:
        local_power = power[eligible]
        resolution = (
            float(np.median(np.diff(frequencies[eligible])))
            if eligible.size > 1
            else fmax_hz - fmin_hz
        )
        distance = max(
            1,
            int(round(minimum_separation_hz / max(resolution, 1e-12))),
        )
        peaks, _ = find_peaks(local_power, distance=distance)
        if peaks.size:
            ranked_peaks = peaks[np.argsort(local_power[peaks])[::-1]]
            spectral_candidates.extend(
                float(frequencies[eligible[index]])
                for index in ranked_peaks[:8]
            )
        ranked_bins = np.argsort(local_power)[::-1]
        spectral_candidates.extend(
            float(frequencies[eligible[index]])
            for index in ranked_bins[:4]
        )

    span = fmax_hz - fmin_hz
    coarse = np.linspace(
        fmin_hz + 0.02 * span,
        fmax_hz - 0.02 * span,
        16,
    )
    interleaved: list[float] = []
    for index in range(max(len(spectral_candidates), coarse.size)):
        if index < len(spectral_candidates):
            interleaved.append(spectral_candidates[index])
        if index < coarse.size:
            interleaved.append(float(coarse[index]))

    seeds = _dedupe_frequency_candidates(
        interleaved,
        fmin_hz,
        fmax_hz,
        maximum=maximum,
        minimum_separation_hz=minimum_separation_hz,
    )
    return seeds or [0.5 * (fmin_hz + fmax_hz)]



def _initial_starts(
    family: ModelFamily,
    standardized_signal: np.ndarray,
    sampling_rate_hz: float,
    fmin_hz: float,
    fmax_hz: float,
) -> list[np.ndarray]:
    seeds = _spectral_seed_frequencies(
        standardized_signal,
        sampling_rate_hz,
        fmin_hz,
        fmax_hz,
    )

    if family == "A0":
        lag1 = float(
            np.corrcoef(standardized_signal[:-1], standardized_signal[1:])[0, 1]
        )
        empirical_rho = (
            min(0.98, max(0.05, abs(lag1)))
            if math.isfinite(lag1)
            else 0.9
        )
        starts = []
        for fraction in (0.5, 0.95):
            for rho in (empirical_rho, 0.9):
                starts.append(
                    np.asarray(
                        [_raw_fraction(fraction), _raw_rho(rho)],
                        dtype=np.float64,
                    )
                )
        return starts

    if family == "A1":
        starts = []
        profiles = (
            (0.90, 0.97),
            (0.75, 0.88),
            (0.60, 0.70),
        )
        for frequency in seeds[:12]:
            for fraction, rho in profiles:
                starts.append(
                    np.asarray(
                        [
                            _raw_fraction(fraction),
                            _raw_rho(rho),
                            _raw_frequency(frequency, fmin_hz, fmax_hz),
                        ],
                        dtype=np.float64,
                    )
                )
        return starts

    pairs: list[tuple[float, float]] = []
    seed_subset = seeds[:10]
    for first_index in range(len(seed_subset)):
        for second_index in range(first_index + 1, len(seed_subset)):
            if abs(seed_subset[first_index] - seed_subset[second_index]) >= 0.45:
                pairs.append((seed_subset[first_index], seed_subset[second_index]))

    for center in seeds[:4]:
        for delta in (0.5, 1.0, 2.0, 5.0, 10.0):
            for sign in (-1.0, 1.0):
                second = center + sign * delta
                if fmin_hz < second < fmax_hz:
                    pairs.append((center, second))

    deduped: list[tuple[float, float]] = []
    for pair in pairs:
        ordered = tuple(sorted(float(value) for value in pair))
        if ordered[1] - ordered[0] < 0.45:
            continue
        if not any(
            abs(ordered[0] - prior[0]) < 0.20
            and abs(ordered[1] - prior[1]) < 0.20
            for prior in deduped
        ):
            deduped.append(ordered)
        if len(deduped) >= 16:
            break

    if not deduped:
        midpoint = 0.5 * (fmin_hz + fmax_hz)
        deduped = [
            (
                max(fmin_hz + 0.05, midpoint - 2.0),
                min(fmax_hz - 0.05, midpoint + 2.0),
            )
        ]

    starts = []
    profiles = (
        (0.90, 0.50, 0.92, 0.92),
        (0.90, 0.20, 0.92, 0.92),
        (0.90, 0.80, 0.92, 0.92),
        (0.80, 0.50, 0.72, 0.92),
        (0.80, 0.50, 0.92, 0.72),
    )
    for first_frequency, second_frequency in deduped:
        for total_fraction, split, rho1, rho2 in profiles:
            starts.append(
                np.asarray(
                    [
                        _raw_fraction(total_fraction),
                        _logit(split),
                        _raw_rho(rho1),
                        _raw_rho(rho2),
                        _raw_frequency(first_frequency, fmin_hz, fmax_hz),
                        _raw_frequency(second_frequency, fmin_hz, fmax_hz),
                    ],
                    dtype=np.float64,
                )
            )
    return starts


def _innovation_diagnostics(innovations: np.ndarray, burn_in_samples: int) -> tuple[float, float]:
    used = np.asarray(innovations[burn_in_samples:], dtype=np.float64)
    rms = float(math.sqrt(float(np.mean(used**2))))
    centered = used - float(np.mean(used))
    variance = float(np.dot(centered, centered))
    if variance <= 0 or used.size < 5:
        return 0.0, rms

    max_lag = min(20, used.size // 10)
    values = []
    for lag in range(1, max_lag + 1):
        numerator = float(np.dot(centered[:-lag], centered[lag:]))
        values.append(numerator / variance)
    max_abs = float(np.max(np.abs(values))) if values else 0.0
    return max_abs, rms


def fit_state_space_candidate(
    signal: Sequence[float],
    sampling_rate_hz: float,
    family: ModelFamily,
    *,
    fmin_hz: float = 1.0,
    fmax_hz: float = 45.0,
    min_samples: int = 1024,
    burn_in_samples: int = 128,
    optimizer_maxiter: int = 80,
) -> StateSpaceModelFit:
    """Fit one A0/A1/A2 candidate with steady-state innovations likelihood."""
    values = np.asarray(signal, dtype=np.float64)
    if values.ndim != 1:
        raise ValueError("signal must be one-dimensional")
    if values.size < min_samples:
        raise ValueError(f"signal requires at least {min_samples} samples")
    if not np.isfinite(values).all():
        raise ValueError("signal contains non-finite samples")
    if not math.isfinite(sampling_rate_hz) or sampling_rate_hz <= 0:
        raise ValueError("sampling_rate_hz must be finite and > 0")
    if not (
        math.isfinite(fmin_hz)
        and math.isfinite(fmax_hz)
        and 0 < fmin_hz < fmax_hz < sampling_rate_hz / 2.0
    ):
        raise ValueError("frequency bounds must satisfy 0 < fmin < fmax < Nyquist")
    if not 0 <= burn_in_samples < values.size - 3:
        raise ValueError("burn_in_samples leaves too few likelihood samples")
    if optimizer_maxiter < 1:
        raise ValueError("optimizer_maxiter must be >= 1")

    mean = float(np.mean(values))
    sd = float(np.std(values))
    if not math.isfinite(sd) or sd <= 0:
        raise ValueError("signal has zero or non-finite standard deviation")
    standardized = (values - mean) / sd

    candidate_starts = _initial_starts(
        family,
        standardized,
        sampling_rate_hz,
        fmin_hz,
        fmax_hz,
    )
    scored_starts: list[tuple[float, np.ndarray]] = []
    for start in candidate_starts:
        initial_nll = _negative_log_likelihood(
            standardized,
            family,
            start,
            sampling_rate_hz,
            fmin_hz,
            fmax_hz,
            burn_in_samples,
        )
        if math.isfinite(initial_nll) and initial_nll < 1e90:
            scored_starts.append((float(initial_nll), start))
    scored_starts.sort(key=lambda item: item[0])

    max_optimized_starts = {"A0": 4, "A1": 12, "A2": 16}[family]
    starts = [start for _, start in scored_starts[:max_optimized_starts]]
    if not starts:
        starts = candidate_starts[:max_optimized_starts]

    solutions = []
    for start in starts:
        fit = minimize(
            lambda raw: _negative_log_likelihood(
                standardized,
                family,
                raw,
                sampling_rate_hz,
                fmin_hz,
                fmax_hz,
                burn_in_samples,
            ),
            start,
            method="L-BFGS-B",
            bounds=[(-8.0, 8.0)] * start.size,
            options={
                "maxiter": optimizer_maxiter,
                "ftol": 1e-8,
                "maxls": 30,
            },
        )
        if math.isfinite(float(fit.fun)):
            solutions.append(fit)

    if not solutions:
        raise RuntimeError(f"{family} optimization produced no finite solution")
    best = min(solutions, key=lambda item: float(item.fun))
    innovation_result = _innovations(
        standardized,
        family,
        np.asarray(best.x, dtype=np.float64),
        sampling_rate_hz,
        fmin_hz,
        fmax_hz,
    )
    if innovation_result is None:
        raise RuntimeError(f"{family} best solution has invalid innovations")
    innovations, _, parameters = innovation_result
    max_abs_ac, innovation_rms = _innovation_diagnostics(
        innovations,
        burn_in_samples,
    )

    parameter_count = {"A0": 2, "A1": 3, "A2": 6}[family]
    finite_nlls = sorted(float(item.fun) for item in solutions)
    near_optimal = [
        item for item in solutions if float(item.fun) <= float(best.fun) + 2.0
    ]
    transformed_near = []
    for item in near_optimal:
        try:
            _, _, _, _, candidate_parameters = _build_model(
                family,
                np.asarray(item.x, dtype=np.float64),
                sampling_rate_hz,
                fmin_hz,
                fmax_hz,
            )
            transformed_near.append(candidate_parameters)
        except Exception:
            continue

    parameter_ranges: dict[str, tuple[float, float]] = {}
    if transformed_near:
        common_keys = set(transformed_near[0])
        for item in transformed_near[1:]:
            common_keys &= set(item)
        for key in sorted(common_keys):
            values_for_key = [
                float(item[key])
                for item in transformed_near
                if math.isfinite(float(item[key]))
            ]
            if values_for_key:
                parameter_ranges[key] = (
                    float(min(values_for_key)),
                    float(max(values_for_key)),
                )

    effective_n = values.size - burn_in_samples
    nll = float(best.fun)
    bic = float(2.0 * nll + parameter_count * math.log(effective_n))
    converged = sum(1 for item in solutions if bool(item.success))
    return StateSpaceModelFit(
        family=family,
        success=bool(best.success),
        sample_count=int(values.size),
        effective_sample_count=int(effective_n),
        burn_in_samples=int(burn_in_samples),
        parameter_count=parameter_count,
        negative_log_likelihood=nll,
        bic=bic,
        converged_start_count=converged,
        candidate_start_count=len(candidate_starts),
        attempted_start_count=len(starts),
        near_optimal_start_count=len(near_optimal),
        start_nll_range=float(finite_nlls[-1] - finite_nlls[0]),
        parameters={key: float(value) for key, value in parameters.items()},
        near_optimal_parameter_ranges=parameter_ranges,
        raw_parameters=tuple(float(value) for value in best.x),
        innovation_max_abs_autocorrelation=max_abs_ac,
        innovation_rms=innovation_rms,
        optimizer_message=str(best.message),
    )


def compare_state_space_candidates(
    signal: Sequence[float],
    sampling_rate_hz: float,
    *,
    fmin_hz: float = 1.0,
    fmax_hz: float = 45.0,
    min_samples: int = 1024,
    burn_in_samples: int = 128,
    optimizer_maxiter: int = 80,
) -> StateSpaceComparison:
    """Fit A0/A1/A2 and report model-comparison diagnostics without admission."""
    values = np.asarray(signal, dtype=np.float64)
    if values.ndim != 1:
        raise ValueError("signal must be one-dimensional")
    if values.size < min_samples:
        raise ValueError(f"signal requires at least {min_samples} samples")
    if not np.isfinite(values).all():
        raise ValueError("signal contains non-finite samples")
    mean = float(np.mean(values))
    sd = float(np.std(values))
    if not math.isfinite(sd) or sd <= 0:
        raise ValueError("signal has zero or non-finite standard deviation")

    fits = tuple(
        fit_state_space_candidate(
            values,
            sampling_rate_hz,
            family,
            fmin_hz=fmin_hz,
            fmax_hz=fmax_hz,
            min_samples=min_samples,
            burn_in_samples=burn_in_samples,
            optimizer_maxiter=optimizer_maxiter,
        )
        for family in ("A0", "A1", "A2")
    )
    ordered = sorted(fits, key=lambda item: item.bic)
    return StateSpaceComparison(
        sampling_rate_hz=float(sampling_rate_hz),
        fmin_hz=float(fmin_hz),
        fmax_hz=float(fmax_hz),
        sample_count=int(values.size),
        standardization_mean=mean,
        standardization_sd=sd,
        fits=fits,
        bic_winner=ordered[0].family,
        bic_margin_to_second=float(ordered[1].bic - ordered[0].bic),
    )




def evaluate_comparison_on_holdout(
    comparison: StateSpaceComparison,
    holdout_signal: Sequence[float],
) -> dict[str, object]:
    """Score frozen fits on holdout data without refitting."""
    values = np.asarray(holdout_signal, dtype=np.float64)
    if values.ndim != 1 or values.size < 16:
        raise ValueError(
            "holdout_signal must be one-dimensional with at least 16 samples"
        )
    if not np.isfinite(values).all():
        raise ValueError("holdout_signal contains non-finite samples")
    if (
        comparison.standardization_sd <= 0
        or not math.isfinite(comparison.standardization_sd)
    ):
        raise ValueError("training comparison has invalid standardization_sd")

    standardized = (
        values - comparison.standardization_mean
    ) / comparison.standardization_sd
    scores: dict[str, float] = {}
    for fit in comparison.fits:
        burn = min(fit.burn_in_samples, max(0, standardized.size // 20))
        nll = _negative_log_likelihood(
            standardized,
            fit.family,
            np.asarray(fit.raw_parameters, dtype=np.float64),
            comparison.sampling_rate_hz,
            comparison.fmin_hz,
            comparison.fmax_hz,
            burn,
        )
        effective_n = standardized.size - burn
        scores[fit.family] = (
            float(nll / effective_n)
            if math.isfinite(nll) and effective_n >= 3
            else float("inf")
        )

    ordered = sorted(scores.items(), key=lambda item: item[1])
    raw_winner = ordered[0][0]
    finite_scores = [
        (family, score)
        for family, score in ordered
        if math.isfinite(score)
    ]
    if finite_scores:
        best_score = finite_scores[0][1]
        tied_families = [
            family
            for family, score in finite_scores
            if score - best_score <= HOLDOUT_NUMERICAL_TIE_ATOL_PER_SAMPLE
        ]
    else:
        tied_families = []

    numerically_indistinguishable = len(tied_families) > 1
    interpretable_winner = (
        None if numerically_indistinguishable else raw_winner
    )
    score_range = (
        float(finite_scores[-1][1] - finite_scores[0][1])
        if finite_scores
        else float("nan")
    )
    margin = (
        float(ordered[1][1] - ordered[0][1])
        if len(ordered) > 1
        and math.isfinite(ordered[0][1])
        and math.isfinite(ordered[1][1])
        else float("nan")
    )
    return {
        "n": int(values.size),
        "negative_log_likelihood_per_sample": scores,
        "raw_winner": raw_winner,
        "interpretable_winner": interpretable_winner,
        "tied_families": tied_families,
        "numerically_indistinguishable": numerically_indistinguishable,
        "numerical_tie_atol_per_sample":
            HOLDOUT_NUMERICAL_TIE_ATOL_PER_SAMPLE,
        "score_range_per_sample": score_range,
        "margin_to_second_per_sample": margin,
        "note": (
            "Training parameters are frozen. Numerical ties are a "
            "computational indeterminate state, not a scientific threshold."
        ),
    }


