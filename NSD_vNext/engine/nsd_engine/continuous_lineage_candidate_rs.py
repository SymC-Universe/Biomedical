"""Qualification-only recurrence-seeded search augmentation for C1Q.

C1Q-RS changes search coverage only. It preserves the C1Q likelihood,
parameterization, transforms, bounds, burn-in, parameter count, and BIC. The
exact legacy optimized-start set is obtained from the shared canonical helper.
When an observable recurrence/covariance seed is admissible, that seed is
optimized in addition to every legacy start.

This module does not license real EEG, C-family membership, production
promotion, or a scientific threshold.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any, Sequence

import numpy as np
from scipy.optimize import minimize

from .continuous_lineage_candidate import (
    _nll,
    _select_legacy_optimized_starts,
    _steady_state,
)
from .state_space_adequacy import (
    _fraction_from_raw,
    _frequency_from_raw,
    _raw_fraction,
    _raw_frequency,
    _raw_rho,
    _rho_from_raw,
)


@dataclass(frozen=True)
class ContinuousLineageRSCandidateFit:
    success: bool
    sample_count: int
    effective_sample_count: int
    burn_in_samples: int
    parameter_count: int
    negative_log_likelihood: float
    bic: float
    parameters: dict[str, float]
    raw_parameters: tuple[float, ...]
    attempted_start_count: int
    converged_start_count: int
    optimizer_message: str

    legacy_attempted_start_count: int
    legacy_converged_start_count: int
    legacy_best_negative_log_likelihood: float
    legacy_best_success: bool
    legacy_best_raw_parameters: tuple[float, ...]
    winning_start_origin: str

    recurrence_seed_status: str
    recurrence_seed_ready: bool
    recurrence_seed_A_unprojected: float | None
    recurrence_seed_g_unprojected: float | None
    recurrence_seed_A_projected: bool
    recurrence_seed_g_projected: bool
    recurrence_seed_raw_parameters: tuple[float, ...] | None
    recurrence_seed_start_nll: float | None
    recurrence_seed_condition_number: float | None
    recurrence_seed_covariance_residual_rms: float | None

    next_ranked_legacy_raw_parameters: tuple[float, ...] | None


def _standardize(values: np.ndarray) -> np.ndarray:
    mean = float(np.mean(values))
    sd = float(np.std(values))
    if not math.isfinite(sd) or sd <= 0.0:
        raise ValueError("signal has zero or non-finite standard deviation")
    return (values - mean) / sd


def _recurrence_covariance_seed(
    standardized: np.ndarray,
    sampling_rate_hz: float,
    fmin_hz: float,
    fmax_hz: float,
    *,
    max_lag: int = 12,
) -> dict[str, Any]:
    """Construct the frozen truth-blind recurrence/covariance C1Q start."""
    variance = float(np.mean(standardized * standardized))
    if not math.isfinite(variance) or variance <= 0.0:
        return {"status": "REFUSE_ZERO_VARIANCE"}

    gamma = np.asarray(
        [
            float(np.mean(standardized[:-lag] * standardized[lag:])) / variance
            for lag in range(1, max_lag + 1)
        ],
        dtype=np.float64,
    )
    if not np.isfinite(gamma).all():
        return {"status": "REFUSE_NONFINITE_COVARIANCE"}

    Xr = np.asarray(
        [[gamma[i + 1], -gamma[i]] for i in range(max_lag - 2)],
        dtype=np.float64,
    )
    yr = np.asarray([gamma[i + 2] for i in range(max_lag - 2)], dtype=np.float64)
    rank = int(np.linalg.matrix_rank(Xr))
    condition = float(np.linalg.cond(Xr))
    if rank < 2:
        return {
            "status": "REFUSE_RANK_DEFICIENT",
            "recurrence_rank": rank,
            "recurrence_condition_number": condition,
        }

    coeff, _, _, _ = np.linalg.lstsq(Xr, yr, rcond=None)
    a = float(coeff[0])
    b = float(coeff[1])
    recurrence_residual_rms = float(
        math.sqrt(float(np.mean((yr - Xr @ coeff) ** 2)))
    )
    if not (math.isfinite(a) and math.isfinite(b) and 0.0 < b < 1.0):
        return {
            "status": "REFUSE_NONSTABLE_RECURRENCE",
            "a": a,
            "b": b,
            "recurrence_rank": rank,
            "recurrence_condition_number": condition,
            "recurrence_residual_rms": recurrence_residual_rms,
        }

    rho = math.sqrt(b)
    xi = a / (2.0 * rho)
    if not (-1.0 < xi < 1.0):
        return {
            "status": "REFUSE_NOT_UNDERDAMPED",
            "a": a,
            "b": b,
            "rho": rho,
            "xi": xi,
            "recurrence_rank": rank,
            "recurrence_condition_number": condition,
            "recurrence_residual_rms": recurrence_residual_rms,
        }

    theta = math.acos(xi)
    L = -math.log(rho)
    fd_hz = theta * sampling_rate_hz / (2.0 * math.pi)

    rho_lo = _rho_from_raw(-8.0)
    rho_hi = _rho_from_raw(8.0)
    fd_lo = _frequency_from_raw(-8.0, fmin_hz, fmax_hz)
    fd_hi = _frequency_from_raw(8.0, fmin_hz, fmax_hz)
    if not (rho_lo <= rho <= rho_hi):
        return {
            "status": "REFUSE_RHO_OUTSIDE_C1Q_DOMAIN",
            "rho": rho,
            "rho_domain": [rho_lo, rho_hi],
            "recurrence_condition_number": condition,
        }
    if not (fd_lo <= fd_hz <= fd_hi):
        return {
            "status": "REFUSE_FREQUENCY_OUTSIDE_C1Q_DOMAIN",
            "fd_hz": fd_hz,
            "frequency_domain_hz": [fd_lo, fd_hi],
            "recurrence_condition_number": condition,
        }

    k = np.arange(1, max_lag + 1, dtype=np.float64)
    Xamp = np.column_stack(
        [
            (rho**k) * np.cos(k * theta),
            (rho**k) * (L / theta) * np.sin(k * theta),
        ]
    )
    amp_coeff, _, _, _ = np.linalg.lstsq(Xamp, gamma, rcond=None)
    A_unprojected = float(amp_coeff[0])
    Ag_unprojected = float(amp_coeff[1])
    if not math.isfinite(A_unprojected) or abs(A_unprojected) <= 1e-12:
        return {
            "status": "REFUSE_NONFINITE_AMPLITUDE_SEED",
            "A_unprojected": A_unprojected,
            "Ag_unprojected": Ag_unprojected,
            "recurrence_condition_number": condition,
        }
    g_unprojected = float(Ag_unprojected / A_unprojected)
    if not math.isfinite(g_unprojected):
        return {
            "status": "REFUSE_NONFINITE_AMPLITUDE_SEED",
            "A_unprojected": A_unprojected,
            "Ag_unprojected": Ag_unprojected,
            "g_unprojected": g_unprojected,
            "recurrence_condition_number": condition,
        }

    covariance_residual_rms = float(
        math.sqrt(float(np.mean((gamma - Xamp @ amp_coeff) ** 2)))
    )
    A_lo = _fraction_from_raw(-8.0)
    A_hi = _fraction_from_raw(8.0)
    A_seed = float(np.clip(A_unprojected, A_lo, A_hi))
    g_seed = float(np.clip(g_unprojected, -1.0 + 1e-6, 1.0 - 1e-6))

    raw = np.asarray(
        [
            _raw_fraction(A_seed),
            _raw_rho(rho),
            _raw_frequency(fd_hz, fmin_hz, fmax_hz),
            float(np.arctanh(g_seed)),
        ],
        dtype=np.float64,
    )
    if not np.isfinite(raw).all() or np.any(raw < -8.0) or np.any(raw > 8.0):
        return {
            "status": "REFUSE_RAW_SEED_OUTSIDE_BOX",
            "raw_parameters": [float(v) for v in raw],
            "A_unprojected": A_unprojected,
            "g_unprojected": g_unprojected,
            "A_seed": A_seed,
            "g_seed": g_seed,
            "recurrence_condition_number": condition,
            "covariance_fit_residual_rms": covariance_residual_rms,
        }

    return {
        "status": "SEED_READY",
        "raw_parameters": raw,
        "A_unprojected": A_unprojected,
        "g_unprojected": g_unprojected,
        "A_seed": A_seed,
        "g_seed": g_seed,
        "A_projected": bool(A_seed != A_unprojected),
        "g_projected": bool(g_seed != g_unprojected),
        "rho": rho,
        "theta": theta,
        "fd_hz": fd_hz,
        "recurrence_rank": rank,
        "recurrence_condition_number": condition,
        "recurrence_residual_rms": recurrence_residual_rms,
        "covariance_fit_residual_rms": covariance_residual_rms,
    }


def fit_continuous_lineage_candidate_rs(
    signal: Sequence[float],
    sampling_rate_hz: float,
    *,
    fmin_hz: float = 1.0,
    fmax_hz: float = 45.0,
    min_samples: int = 1024,
    burn_in_samples: int = 128,
    optimizer_maxiter: int = 80,
    max_optimized_starts: int = 18,
) -> ContinuousLineageRSCandidateFit:
    values = np.asarray(signal, dtype=np.float64)
    if values.ndim != 1:
        raise ValueError("signal must be one-dimensional")
    if values.size < min_samples:
        raise ValueError(f"signal requires at least {min_samples} samples")
    if not np.isfinite(values).all():
        raise ValueError("signal contains non-finite samples")
    if not 0.0 < fmin_hz < fmax_hz < sampling_rate_hz / 2.0:
        raise ValueError("frequency bounds must satisfy 0 < fmin < fmax < Nyquist")
    if not 0 <= burn_in_samples < values.size - 3:
        raise ValueError("burn_in_samples leaves too few likelihood samples")

    standardized = _standardize(values)
    selection = _select_legacy_optimized_starts(
        standardized,
        sampling_rate_hz,
        fmin_hz,
        fmax_hz,
        burn_in_samples,
        max_optimized_starts,
    )
    legacy_starts = selection["selected"]
    seed_info = _recurrence_covariance_seed(
        standardized, sampling_rate_hz, fmin_hz, fmax_hz
    )

    starts: list[tuple[str, np.ndarray]] = [
        ("legacy", np.asarray(start, dtype=np.float64))
        for start in legacy_starts
    ]
    recurrence_start_nll = None
    if seed_info["status"] == "SEED_READY":
        recurrence_raw = np.asarray(seed_info["raw_parameters"], dtype=np.float64)
        recurrence_start_nll = float(
            _nll(
                standardized,
                recurrence_raw,
                sampling_rate_hz,
                fmin_hz,
                fmax_hz,
                burn_in_samples,
            )
        )
        starts.append(("recurrence", recurrence_raw))

    solutions: list[tuple[str, Any]] = []
    for origin, start in starts:
        result = minimize(
            lambda raw: _nll(
                standardized,
                raw,
                sampling_rate_hz,
                fmin_hz,
                fmax_hz,
                burn_in_samples,
            ),
            start,
            method="L-BFGS-B",
            bounds=[(-8.0, 8.0)] * 4,
            options={"maxiter": optimizer_maxiter, "ftol": 1e-8, "maxls": 30},
        )
        if math.isfinite(float(result.fun)):
            solutions.append((origin, result))

    if not solutions:
        raise RuntimeError("C1Q-RS produced no finite solution")

    legacy_solutions = [
        result for origin, result in solutions if origin == "legacy"
    ]
    if not legacy_solutions:
        raise RuntimeError("C1Q-RS produced no finite legacy solution")

    legacy_best = min(legacy_solutions, key=lambda item: float(item.fun))
    winning_origin, best = min(
        solutions, key=lambda item: float(item[1].fun)
    )
    steady = _steady_state(
        np.asarray(best.x, dtype=np.float64),
        sampling_rate_hz,
        fmin_hz,
        fmax_hz,
    )
    if steady is None:
        raise RuntimeError("best C1Q-RS solution is invalid")
    _, _, _, parameters = steady

    effective_n = int(values.size - burn_in_samples)
    nll = float(best.fun)
    parameter_count = 4
    bic = float(2.0 * nll + parameter_count * math.log(effective_n))

    next_ranked = selection["next_ranked"]
    raw_seed = (
        tuple(float(v) for v in seed_info["raw_parameters"])
        if seed_info["status"] == "SEED_READY"
        else None
    )
    return ContinuousLineageRSCandidateFit(
        success=bool(best.success),
        sample_count=int(values.size),
        effective_sample_count=effective_n,
        burn_in_samples=int(burn_in_samples),
        parameter_count=parameter_count,
        negative_log_likelihood=nll,
        bic=bic,
        parameters={k: float(v) for k, v in parameters.items()},
        raw_parameters=tuple(float(v) for v in best.x),
        attempted_start_count=len(starts),
        converged_start_count=sum(
            1 for _, result in solutions if bool(result.success)
        ),
        optimizer_message=str(best.message),
        legacy_attempted_start_count=len(legacy_starts),
        legacy_converged_start_count=sum(
            1 for result in legacy_solutions if bool(result.success)
        ),
        legacy_best_negative_log_likelihood=float(legacy_best.fun),
        legacy_best_success=bool(legacy_best.success),
        legacy_best_raw_parameters=tuple(
            float(v) for v in legacy_best.x
        ),
        winning_start_origin=winning_origin,
        recurrence_seed_status=str(seed_info["status"]),
        recurrence_seed_ready=bool(seed_info["status"] == "SEED_READY"),
        recurrence_seed_A_unprojected=(
            float(seed_info["A_unprojected"])
            if "A_unprojected" in seed_info
            and math.isfinite(float(seed_info["A_unprojected"]))
            else None
        ),
        recurrence_seed_g_unprojected=(
            float(seed_info["g_unprojected"])
            if "g_unprojected" in seed_info
            and math.isfinite(float(seed_info["g_unprojected"]))
            else None
        ),
        recurrence_seed_A_projected=bool(
            seed_info.get("A_projected", False)
        ),
        recurrence_seed_g_projected=bool(
            seed_info.get("g_projected", False)
        ),
        recurrence_seed_raw_parameters=raw_seed,
        recurrence_seed_start_nll=recurrence_start_nll,
        recurrence_seed_condition_number=(
            float(seed_info["recurrence_condition_number"])
            if "recurrence_condition_number" in seed_info
            else None
        ),
        recurrence_seed_covariance_residual_rms=(
            float(seed_info["covariance_fit_residual_rms"])
            if "covariance_fit_residual_rms" in seed_info
            else None
        ),
        next_ranked_legacy_raw_parameters=(
            tuple(float(v) for v in next_ranked)
            if next_ranked is not None
            else None
        ),
    )
