#!/usr/bin/env python3
"""Known-truth calibration grid for descriptive periodic-peak admission.

This script never reads clinical or healthy EEG data. It evaluates a finite,
prespecified grid of specparam detection settings against synthetic spectral
truths and reports performance rather than selecting settings by diagnosis or by
an attractive real-data result.

The purpose is to find whether a defensible descriptive operating region exists
before the parameterizer is allowed onto healthy recordings.
"""

from __future__ import annotations

from dataclasses import asdict
import json
import math
from pathlib import Path
import sys

import numpy as np

ENGINE_ROOT = Path(__file__).resolve().parents[1]
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

from nsd_engine.specparam_adapter import SpecparamSettings, fit_specparam_descriptive


FREQS = np.arange(1.0, 45.0 + 0.25, 0.25, dtype=float)
PEAK_THRESHOLDS = (2.0, 2.5, 3.0)
MIN_PEAK_HEIGHTS = (0.05, 0.10, 0.15, 0.20)
MAX_N_PEAKS = (3, 4)
NOISE_SDS = (0.02, 0.04)
SEEDS = tuple(range(202609140, 202609150))
SINGLE_HEIGHTS = (0.10, 0.15, 0.20, 0.30, 0.45)

# Truth-matching tolerances are deliberately declared here rather than tuned to
# observed outputs. These refer only to descriptive Gaussian peak recovery.
CF_TOLERANCE_HZ = 0.75
BW_RELATIVE_TOLERANCE = 0.50
WIDTH_BOUNDARY_ATOL_HZ = 0.02


def _fixed_log_power(freqs: np.ndarray, offset: float = 1.0, exponent: float = 1.2) -> np.ndarray:
    return offset - exponent * np.log10(freqs)


def _knee_log_power(freqs: np.ndarray, offset: float = 2.0, knee: float = 25.0, exponent: float = 2.0) -> np.ndarray:
    return offset - np.log10(knee + freqs**exponent)


def _gaussian(freqs: np.ndarray, cf: float, height: float, sigma: float) -> np.ndarray:
    return height * np.exp(-((freqs - cf) ** 2) / (2.0 * sigma**2))


def _power(log_power: np.ndarray) -> np.ndarray:
    return 10.0**log_power


def _noise(seed: int, sd: float) -> np.ndarray:
    return np.random.default_rng(seed).normal(0.0, sd, size=FREQS.size)


def _near_width_boundary(bw: float, settings: SpecparamSettings) -> bool:
    low, high = settings.peak_width_limits
    return math.isclose(bw, low, abs_tol=WIDTH_BOUNDARY_ATOL_HZ) or math.isclose(
        bw, high, abs_tol=WIDTH_BOUNDARY_ATOL_HZ
    )


def _matches(peak, cf: float, bw: float) -> bool:
    return (
        abs(peak.center_frequency_hz - cf) <= CF_TOLERANCE_HZ
        and abs(peak.bandwidth_hz - bw) / bw <= BW_RELATIVE_TOLERANCE
    )


def _single_truth_class(result, cf: float, bw: float) -> dict[str, object]:
    matching = [peak for peak in result.peaks if _matches(peak, cf, bw)]
    return {
        "recovered": len(matching) >= 1,
        "exactly_one_peak": len(result.peaks) == 1,
        "false_extra_peak_count": max(0, len(result.peaks) - 1),
        "split_or_duplicate_match": len(matching) > 1,
        "width_boundary_hits": sum(_near_width_boundary(peak.bandwidth_hz, result.settings) for peak in result.peaks),
        "max_peak_count_reached": result.settings.max_n_peaks > 0 and len(result.peaks) >= result.settings.max_n_peaks,
    }


def _two_truth_class(result, truths: tuple[tuple[float, float], tuple[float, float]]) -> dict[str, object]:
    # Brute-force one-to-one assignment for two truths. A fit succeeds only if
    # two distinct fitted peaks can each match one truth.
    fits = list(result.peaks)
    recovered = False
    if len(fits) >= 2:
        for i, first in enumerate(fits):
            for j, second in enumerate(fits):
                if i == j:
                    continue
                if _matches(first, *truths[0]) and _matches(second, *truths[1]):
                    recovered = True
                    break
            if recovered:
                break
    return {
        "recovered_two_distinct": recovered,
        "exactly_two_peaks": len(result.peaks) == 2,
        "false_extra_peak_count": max(0, len(result.peaks) - 2),
        "width_boundary_hits": sum(_near_width_boundary(peak.bandwidth_hz, result.settings) for peak in result.peaks),
        "max_peak_count_reached": result.settings.max_n_peaks > 0 and len(result.peaks) >= result.settings.max_n_peaks,
    }


def _mean_bool(rows: list[dict[str, object]], key: str) -> float:
    return float(np.mean([bool(row[key]) for row in rows])) if rows else float("nan")


def _mean_numeric(rows: list[dict[str, object]], key: str) -> float:
    return float(np.mean([float(row[key]) for row in rows])) if rows else float("nan")


def evaluate_settings(settings: SpecparamSettings) -> dict[str, object]:
    no_peak_rows: list[dict[str, object]] = []
    for noise_sd in NOISE_SDS:
        for seed in SEEDS:
            logp = _fixed_log_power(FREQS) + _noise(seed, noise_sd)
            result = fit_specparam_descriptive(FREQS, _power(logp), settings=settings)
            no_peak_rows.append(
                {
                    "noise_sd": noise_sd,
                    "seed": seed,
                    "false_positive": len(result.peaks) > 0,
                    "peak_count": len(result.peaks),
                    "width_boundary_hits": sum(
                        _near_width_boundary(peak.bandwidth_hz, settings) for peak in result.peaks
                    ),
                    "max_peak_count_reached": settings.max_n_peaks > 0 and len(result.peaks) >= settings.max_n_peaks,
                }
            )

    single_by_height: dict[str, dict[str, object]] = {}
    for height in SINGLE_HEIGHTS:
        rows: list[dict[str, object]] = []
        for noise_sd in NOISE_SDS:
            for seed in SEEDS:
                logp = _fixed_log_power(FREQS) + _gaussian(FREQS, 10.0, height, 1.0) + _noise(seed, noise_sd)
                result = fit_specparam_descriptive(FREQS, _power(logp), settings=settings)
                classified = _single_truth_class(result, 10.0, 2.0)
                classified["noise_sd"] = noise_sd
                classified["seed"] = seed
                rows.append(classified)
        single_by_height[f"{height:.2f}"] = {
            "n": len(rows),
            "recovery_rate": _mean_bool(rows, "recovered"),
            "exactly_one_peak_rate": _mean_bool(rows, "exactly_one_peak"),
            "split_or_duplicate_match_rate": _mean_bool(rows, "split_or_duplicate_match"),
            "mean_false_extra_peaks": _mean_numeric(rows, "false_extra_peak_count"),
            "mean_width_boundary_hits": _mean_numeric(rows, "width_boundary_hits"),
            "max_peak_count_reached_rate": _mean_bool(rows, "max_peak_count_reached"),
        }

    separated_rows: list[dict[str, object]] = []
    unresolved_rows: list[dict[str, object]] = []
    for noise_sd in NOISE_SDS:
        for seed in SEEDS:
            noise = _noise(seed, noise_sd)
            separated_log = (
                _fixed_log_power(FREQS)
                + _gaussian(FREQS, 10.0, 0.45, 0.8)
                + _gaussian(FREQS, 12.0, 0.45, 0.8)
                + noise
            )
            separated = fit_specparam_descriptive(FREQS, _power(separated_log), settings=settings)
            row = _two_truth_class(separated, ((10.0, 1.6), (12.0, 1.6)))
            row["noise_sd"] = noise_sd
            row["seed"] = seed
            separated_rows.append(row)

            unresolved_log = (
                _fixed_log_power(FREQS)
                + _gaussian(FREQS, 10.0, 0.45, 0.8)
                + _gaussian(FREQS, 11.5, 0.45, 0.8)
                + noise
            )
            unresolved = fit_specparam_descriptive(FREQS, _power(unresolved_log), settings=settings)
            unresolved_rows.append(
                {
                    "noise_sd": noise_sd,
                    "seed": seed,
                    "returned_peak_count": len(unresolved.peaks),
                    "returned_one_peak": len(unresolved.peaks) == 1,
                    "returned_two_or_more": len(unresolved.peaks) >= 2,
                    "width_boundary_hits": sum(
                        _near_width_boundary(peak.bandwidth_hz, settings) for peak in unresolved.peaks
                    ),
                }
            )

    # Model-family misspecification test. The fixed model should not be trusted
    # just because R^2 is high when knee truth exists. Run the same peak settings
    # under both aperiodic families.
    knee_fixed_rows: list[dict[str, object]] = []
    knee_model_rows: list[dict[str, object]] = []
    knee_settings = SpecparamSettings(
        aperiodic_mode="knee",
        periodic_mode=settings.periodic_mode,
        peak_width_limits=settings.peak_width_limits,
        max_n_peaks=settings.max_n_peaks,
        min_peak_height=settings.min_peak_height,
        peak_threshold=settings.peak_threshold,
        fmin_hz=settings.fmin_hz,
        fmax_hz=settings.fmax_hz,
    )
    for noise_sd in NOISE_SDS:
        for seed in SEEDS:
            logp = _knee_log_power(FREQS) + _noise(seed, noise_sd)
            power = _power(logp)
            fixed_result = fit_specparam_descriptive(FREQS, power, settings=settings)
            knee_result = fit_specparam_descriptive(FREQS, power, settings=knee_settings)
            knee_fixed_rows.append(
                {
                    "false_positive": len(fixed_result.peaks) > 0,
                    "peak_count": len(fixed_result.peaks),
                    "error_mae": dict(fixed_result.metrics).get("error_mae"),
                }
            )
            knee_model_rows.append(
                {
                    "false_positive": len(knee_result.peaks) > 0,
                    "peak_count": len(knee_result.peaks),
                    "error_mae": dict(knee_result.metrics).get("error_mae"),
                }
            )

    strong_single_keys = ("0.20", "0.30", "0.45")
    strong_recovery = float(np.mean([single_by_height[key]["recovery_rate"] for key in strong_single_keys]))
    strong_exact = float(np.mean([single_by_height[key]["exactly_one_peak_rate"] for key in strong_single_keys]))
    strong_extra = float(np.mean([single_by_height[key]["mean_false_extra_peaks"] for key in strong_single_keys]))

    # These qualification criteria are prespecified here only as a conservative
    # filter for a *candidate operating region*. Passing does not automatically
    # promote real-data use; failure-mode inspection and healthy pilot behavior
    # remain required.
    criteria = {
        "fixed_no_peak_false_positive_rate_le_0_05": _mean_bool(no_peak_rows, "false_positive") <= 0.05,
        "strong_single_mean_recovery_ge_0_90": strong_recovery >= 0.90,
        "strong_single_mean_exactly_one_ge_0_80": strong_exact >= 0.80,
        "strong_single_mean_false_extra_peaks_le_0_10": strong_extra <= 0.10,
        "separated_two_peak_recovery_ge_0_80": _mean_bool(separated_rows, "recovered_two_distinct") >= 0.80,
        "knee_model_no_peak_false_positive_rate_le_0_10": _mean_bool(knee_model_rows, "false_positive") <= 0.10,
    }

    return {
        "settings": asdict(settings),
        "fixed_no_peak": {
            "n": len(no_peak_rows),
            "false_positive_rate": _mean_bool(no_peak_rows, "false_positive"),
            "mean_peak_count": _mean_numeric(no_peak_rows, "peak_count"),
            "mean_width_boundary_hits": _mean_numeric(no_peak_rows, "width_boundary_hits"),
            "max_peak_count_reached_rate": _mean_bool(no_peak_rows, "max_peak_count_reached"),
        },
        "single_peak": single_by_height,
        "strong_single_summary": {
            "truth_peak_heights": [0.20, 0.30, 0.45],
            "mean_recovery_rate": strong_recovery,
            "mean_exactly_one_peak_rate": strong_exact,
            "mean_false_extra_peaks": strong_extra,
        },
        "two_peaks_separated_2_hz": {
            "n": len(separated_rows),
            "recovery_rate": _mean_bool(separated_rows, "recovered_two_distinct"),
            "exactly_two_peak_rate": _mean_bool(separated_rows, "exactly_two_peaks"),
            "mean_false_extra_peaks": _mean_numeric(separated_rows, "false_extra_peak_count"),
            "mean_width_boundary_hits": _mean_numeric(separated_rows, "width_boundary_hits"),
        },
        "two_peaks_separation_1_5_hz_ambiguity": {
            "n": len(unresolved_rows),
            "one_peak_rate": _mean_bool(unresolved_rows, "returned_one_peak"),
            "two_or_more_rate": _mean_bool(unresolved_rows, "returned_two_or_more"),
            "mean_width_boundary_hits": _mean_numeric(unresolved_rows, "width_boundary_hits"),
            "interpretation": "known-truth ambiguity/failure-boundary descriptor; no required peak-count target",
        },
        "knee_truth": {
            "fixed_model_false_positive_rate": _mean_bool(knee_fixed_rows, "false_positive"),
            "fixed_model_mean_peak_count": _mean_numeric(knee_fixed_rows, "peak_count"),
            "fixed_model_mean_mae": _mean_numeric(knee_fixed_rows, "error_mae"),
            "knee_model_false_positive_rate": _mean_bool(knee_model_rows, "false_positive"),
            "knee_model_mean_peak_count": _mean_numeric(knee_model_rows, "peak_count"),
            "knee_model_mean_mae": _mean_numeric(knee_model_rows, "error_mae"),
        },
        "candidate_region_criteria": criteria,
        "candidate_region_pass": all(criteria.values()),
    }


def main() -> int:
    rows: list[dict[str, object]] = []
    for peak_threshold in PEAK_THRESHOLDS:
        for min_height in MIN_PEAK_HEIGHTS:
            for max_peaks in MAX_N_PEAKS:
                settings = SpecparamSettings(
                    aperiodic_mode="fixed",
                    periodic_mode="gaussian",
                    peak_width_limits=(0.5, 12.0),
                    max_n_peaks=max_peaks,
                    min_peak_height=min_height,
                    peak_threshold=peak_threshold,
                    fmin_hz=1.0,
                    fmax_hz=45.0,
                )
                rows.append(evaluate_settings(settings))

    passing = [row for row in rows if row["candidate_region_pass"]]
    output = {
        "scope": "known-truth descriptive peak-admission calibration only",
        "grid": {
            "peak_thresholds": list(PEAK_THRESHOLDS),
            "min_peak_heights": list(MIN_PEAK_HEIGHTS),
            "max_n_peaks": list(MAX_N_PEAKS),
            "noise_sds_log10_power": list(NOISE_SDS),
            "seeds": list(SEEDS),
            "frequency_resolution_hz": 0.25,
            "cf_tolerance_hz": CF_TOLERANCE_HZ,
            "bandwidth_relative_tolerance": BW_RELATIVE_TOLERANCE,
        },
        "setting_count": len(rows),
        "candidate_region_pass_count": len(passing),
        "passing_settings": [row["settings"] for row in passing],
        "results": rows,
        "selection_rule": "No automatic winner. Any surviving settings remain candidates pending failure-mode inspection and label-blind healthy repeat evaluation.",
        "interpretation_ceiling": "descriptive spectral qualification; no biological, modal, damping, chi, diagnostic, or prognostic meaning",
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
