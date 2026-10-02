#!/usr/bin/env python3
"""Map descriptive specparam rc7 behavior across prespecified known-truth spectra.

This is a P0-Q qualification map, not a clinical analysis and not a model tuning
search. It records where a fixed exact implementation recovers, merges, misses,
or invents descriptive peaks under controlled spectral truths.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
import sys

import numpy as np

ENGINE_ROOT = Path(__file__).resolve().parents[1]
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

from nsd_engine.specparam_adapter import (
    REQUIRED_SPECPARAM_VERSION,
    SpecparamSettings,
    fit_specparam_descriptive,
)


def _fixed_log_power(freqs: np.ndarray, offset: float = 1.0, exponent: float = 1.2) -> np.ndarray:
    return offset - exponent * np.log10(freqs)


def _knee_log_power(freqs: np.ndarray, offset: float = 2.0, knee: float = 25.0, exponent: float = 2.0) -> np.ndarray:
    return offset - np.log10(knee + freqs**exponent)


def _gaussian(freqs: np.ndarray, cf: float, height: float, sigma: float) -> np.ndarray:
    return height * np.exp(-((freqs - cf) ** 2) / (2.0 * sigma**2))


def _power(log_power: np.ndarray) -> np.ndarray:
    return 10.0**log_power


def _result_payload(result) -> dict[str, object]:
    return {
        "aperiodic_parameter_names": list(result.aperiodic_parameter_names),
        "aperiodic_parameters": list(result.aperiodic_parameters),
        "peaks": [
            {
                "cf_hz": peak.center_frequency_hz,
                "pw_log10_above_aperiodic": peak.power_above_aperiodic_log10,
                "bw_hz": peak.bandwidth_hz,
            }
            for peak in result.peaks
        ],
        "n_peaks": len(result.peaks),
        "metrics": dict(result.metrics),
        "zero_peak_state": result.zero_peak_state,
        "licenses_damping": result.licenses_damping,
        "licenses_chi": result.licenses_chi,
    }


def _settings(*, mode: str = "fixed", min_height: float = 0.0, max_peaks: int = 6) -> SpecparamSettings:
    return SpecparamSettings(
        aperiodic_mode=mode,
        periodic_mode="gaussian",
        peak_width_limits=(0.5, 12.0),
        max_n_peaks=max_peaks,
        min_peak_height=min_height,
        peak_threshold=2.0,
        fmin_hz=1.0,
        fmax_hz=45.0,
    )


def main() -> int:
    freqs = np.arange(1.0, 45.0 + 0.25, 0.25, dtype=float)
    output: dict[str, object] = {
        "specparam_version": REQUIRED_SPECPARAM_VERSION,
        "scope": "known-truth descriptive spectral parameterization qualification map",
        "interpretation_ceiling": "descriptive periodic/aperiodic recovery only; no modal, damping, chi, diagnostic, or biological interpretation",
    }

    # 1) Resolution / peak-separation boundary.
    overlap_rows: list[dict[str, object]] = []
    for separation_hz in (0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0):
        logp = _fixed_log_power(freqs)
        logp += _gaussian(freqs, 10.0, 0.45, 0.8)
        logp += _gaussian(freqs, 10.0 + separation_hz, 0.45, 0.8)
        result = fit_specparam_descriptive(freqs, _power(logp), settings=_settings(min_height=0.05, max_peaks=4))
        overlap_rows.append(
            {
                "truth": {
                    "cf_hz": [10.0, 10.0 + separation_hz],
                    "peak_height_log10": [0.45, 0.45],
                    "gaussian_sigma_hz": [0.8, 0.8],
                    "converted_bw_hz": [1.6, 1.6],
                    "separation_hz": separation_hz,
                },
                "fit": _result_payload(result),
            }
        )
    output["overlapping_peak_separation_sweep"] = overlap_rows

    # 2) Detection boundary under deterministic log-power noise.
    weak_rows: list[dict[str, object]] = []
    rng = np.random.default_rng(20260914)
    fixed_noise = rng.normal(0.0, 0.02, size=freqs.size)
    for height in (0.02, 0.05, 0.08, 0.10, 0.15, 0.20, 0.30, 0.45):
        logp = _fixed_log_power(freqs) + _gaussian(freqs, 10.0, height, 1.0) + fixed_noise
        result = fit_specparam_descriptive(freqs, _power(logp), settings=_settings(min_height=0.0, max_peaks=4))
        weak_rows.append(
            {
                "truth": {
                    "cf_hz": 10.0,
                    "peak_height_log10": height,
                    "gaussian_sigma_hz": 1.0,
                    "converted_bw_hz": 2.0,
                    "deterministic_log_noise_sd": 0.02,
                    "noise_seed": 20260914,
                },
                "fit": _result_payload(result),
            }
        )
    output["weak_peak_sweep"] = weak_rows

    # 3) Frequency-resolution sensitivity for the same spectral truth.
    resolution_rows: list[dict[str, object]] = []
    for resolution_hz in (0.125, 0.25, 0.5, 1.0):
        rf = np.arange(1.0, 45.0 + resolution_hz / 2.0, resolution_hz, dtype=float)
        logp = _fixed_log_power(rf) + _gaussian(rf, 10.3, 0.5, 0.9)
        result = fit_specparam_descriptive(rf, _power(logp), settings=_settings(min_height=0.05, max_peaks=3))
        resolution_rows.append(
            {
                "truth": {
                    "cf_hz": 10.3,
                    "peak_height_log10": 0.5,
                    "gaussian_sigma_hz": 0.9,
                    "converted_bw_hz": 1.8,
                    "frequency_resolution_hz": resolution_hz,
                },
                "fit": _result_payload(result),
            }
        )
    output["frequency_resolution_sweep"] = resolution_rows

    # 4) Aperiodic model misspecification: knee truth fitted as knee and fixed.
    knee_truth = _power(_knee_log_power(freqs, offset=2.0, knee=25.0, exponent=2.0))
    knee_fit = fit_specparam_descriptive(freqs, knee_truth, settings=_settings(mode="knee", min_height=0.05, max_peaks=6))
    fixed_fit = fit_specparam_descriptive(freqs, knee_truth, settings=_settings(mode="fixed", min_height=0.05, max_peaks=6))
    output["knee_truth_model_comparison"] = {
        "truth": {"offset": 2.0, "knee": 25.0, "exponent": 2.0, "periodic_peaks": 0},
        "knee_model_fit": _result_payload(knee_fit),
        "fixed_model_fit": _result_payload(fixed_fit),
    }

    # 5) Broad bump remains descriptive by construction.
    broad_logp = _fixed_log_power(freqs) + _gaussian(freqs, 15.0, 0.5, 4.0)
    broad_fit = fit_specparam_descriptive(freqs, _power(broad_logp), settings=_settings(min_height=0.05, max_peaks=3))
    output["broad_bump"] = {
        "truth": {"cf_hz": 15.0, "peak_height_log10": 0.5, "gaussian_sigma_hz": 4.0, "converted_bw_hz": 8.0},
        "fit": _result_payload(broad_fit),
        "dynamical_interpretation": "prohibited even when the descriptive fit is accurate",
    }

    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
