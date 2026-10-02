#!/usr/bin/env python3
"""Known-truth calibration of fixed-mode specparam frequency ranges.

The official specparam guidance warns that fixed aperiodic fits can fail over
ranges that contain a knee and recommends choosing ranges where the aperiodic
background is approximately linear in log-log space. This script tests that
principle prospectively on synthetic truth before any real EEG is consulted.

It does not choose a range by diagnostic separation or healthy repeatability.
"""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
import sys

import numpy as np

ENGINE_ROOT = Path(__file__).resolve().parents[1]
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

from nsd_engine.specparam_adapter import SpecparamSettings, fit_specparam_descriptive


FREQS = np.arange(1.0, 45.0 + 0.25, 0.25, dtype=float)
RANGES_HZ = ((1.0, 45.0), (2.0, 40.0), (3.0, 35.0), (3.0, 30.0), (5.0, 35.0))
PEAK_THRESHOLDS = (2.0, 2.5, 3.0)
MAX_N_PEAKS = (3, 4)
MIN_PEAK_HEIGHT = 0.20
NOISE_SDS = (0.02, 0.04)
SEEDS = tuple(range(202609140, 202609150))
SINGLE_HEIGHTS = (0.20, 0.30, 0.45)
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


def _settings(fmin: float, fmax: float, threshold: float, max_peaks: int) -> SpecparamSettings:
    return SpecparamSettings(
        aperiodic_mode="fixed",
        periodic_mode="gaussian",
        peak_width_limits=(0.5, 12.0),
        max_n_peaks=max_peaks,
        min_peak_height=MIN_PEAK_HEIGHT,
        peak_threshold=threshold,
        fmin_hz=fmin,
        fmax_hz=fmax,
    )


def _boundary_hit(result) -> bool:
    low, high = result.settings.peak_width_limits
    return any(
        abs(peak.bandwidth_hz - low) <= WIDTH_BOUNDARY_ATOL_HZ
        or abs(peak.bandwidth_hz - high) <= WIDTH_BOUNDARY_ATOL_HZ
        for peak in result.peaks
    )


def _truth_match(peak, cf: float, bw: float) -> bool:
    return (
        abs(peak.center_frequency_hz - cf) <= CF_TOLERANCE_HZ
        and abs(peak.bandwidth_hz - bw) / bw <= BW_RELATIVE_TOLERANCE
    )


def _mean_bool(rows: list[dict[str, object]], key: str) -> float:
    return float(np.mean([bool(row[key]) for row in rows])) if rows else float("nan")


def _mean_num(rows: list[dict[str, object]], key: str) -> float:
    return float(np.mean([float(row[key]) for row in rows])) if rows else float("nan")


def _eval_background(background_name: str, settings: SpecparamSettings) -> dict[str, object]:
    background = _fixed_log_power if background_name == "fixed" else _knee_log_power

    no_peak: list[dict[str, object]] = []
    for sd in NOISE_SDS:
        for seed in SEEDS:
            result = fit_specparam_descriptive(
                FREQS,
                _power(background(FREQS) + _noise(seed, sd)),
                settings=settings,
            )
            no_peak.append(
                {
                    "false_positive": len(result.peaks) > 0,
                    "peak_count": len(result.peaks),
                    "boundary_hit": _boundary_hit(result),
                }
            )

    single: dict[str, object] = {}
    for height in SINGLE_HEIGHTS:
        rows: list[dict[str, object]] = []
        for sd in NOISE_SDS:
            for seed in SEEDS:
                result = fit_specparam_descriptive(
                    FREQS,
                    _power(
                        background(FREQS)
                        + _gaussian(FREQS, 10.0, height, 1.0)
                        + _noise(seed, sd)
                    ),
                    settings=settings,
                )
                matched = [peak for peak in result.peaks if _truth_match(peak, 10.0, 2.0)]
                rows.append(
                    {
                        "recovered": len(matched) >= 1,
                        "exactly_one": len(result.peaks) == 1,
                        "false_extra": max(0, len(result.peaks) - 1),
                        "boundary_hit": _boundary_hit(result),
                    }
                )
        single[f"{height:.2f}"] = {
            "recovery_rate": _mean_bool(rows, "recovered"),
            "exactly_one_rate": _mean_bool(rows, "exactly_one"),
            "mean_false_extra": _mean_num(rows, "false_extra"),
            "boundary_hit_rate": _mean_bool(rows, "boundary_hit"),
        }

    two_rows: list[dict[str, object]] = []
    for sd in NOISE_SDS:
        for seed in SEEDS:
            result = fit_specparam_descriptive(
                FREQS,
                _power(
                    background(FREQS)
                    + _gaussian(FREQS, 10.0, 0.45, 0.8)
                    + _gaussian(FREQS, 12.0, 0.45, 0.8)
                    + _noise(seed, sd)
                ),
                settings=settings,
            )
            first = any(_truth_match(peak, 10.0, 1.6) for peak in result.peaks)
            second = any(_truth_match(peak, 12.0, 1.6) for peak in result.peaks)
            two_rows.append(
                {
                    "recovered_two": first and second and len(result.peaks) >= 2,
                    "exactly_two": len(result.peaks) == 2,
                    "false_extra": max(0, len(result.peaks) - 2),
                    "boundary_hit": _boundary_hit(result),
                }
            )

    return {
        "truth_background": background_name,
        "no_peak": {
            "false_positive_rate": _mean_bool(no_peak, "false_positive"),
            "mean_peak_count": _mean_num(no_peak, "peak_count"),
            "boundary_hit_rate": _mean_bool(no_peak, "boundary_hit"),
        },
        "single_peak": single,
        "two_peaks_2hz_separation": {
            "recovery_rate": _mean_bool(two_rows, "recovered_two"),
            "exactly_two_rate": _mean_bool(two_rows, "exactly_two"),
            "mean_false_extra": _mean_num(two_rows, "false_extra"),
            "boundary_hit_rate": _mean_bool(two_rows, "boundary_hit"),
        },
    }


def main() -> int:
    rows: list[dict[str, object]] = []
    for fmin, fmax in RANGES_HZ:
        for threshold in PEAK_THRESHOLDS:
            for max_peaks in MAX_N_PEAKS:
                settings = _settings(fmin, fmax, threshold, max_peaks)
                fixed = _eval_background("fixed", settings)
                knee = _eval_background("knee", settings)

                strong_keys = ("0.20", "0.30", "0.45")
                strong_recovery = float(np.mean(
                    [fixed["single_peak"][key]["recovery_rate"] for key in strong_keys]
                    + [knee["single_peak"][key]["recovery_rate"] for key in strong_keys]
                ))
                strong_exact = float(np.mean(
                    [fixed["single_peak"][key]["exactly_one_rate"] for key in strong_keys]
                    + [knee["single_peak"][key]["exactly_one_rate"] for key in strong_keys]
                ))
                strong_extra = float(np.mean(
                    [fixed["single_peak"][key]["mean_false_extra"] for key in strong_keys]
                    + [knee["single_peak"][key]["mean_false_extra"] for key in strong_keys]
                ))
                minimum_two = min(
                    float(fixed["two_peaks_2hz_separation"]["recovery_rate"]),
                    float(knee["two_peaks_2hz_separation"]["recovery_rate"]),
                )

                criteria = {
                    "fixed_truth_no_peak_fp_le_0_05": fixed["no_peak"]["false_positive_rate"] <= 0.05,
                    "knee_truth_no_peak_fp_le_0_05": knee["no_peak"]["false_positive_rate"] <= 0.05,
                    "cross_background_strong_recovery_ge_0_90": strong_recovery >= 0.90,
                    "cross_background_strong_exact_one_ge_0_80": strong_exact >= 0.80,
                    "cross_background_strong_false_extra_le_0_10": strong_extra <= 0.10,
                    "both_background_two_peak_recovery_ge_0_75": minimum_two >= 0.75,
                }
                rows.append(
                    {
                        "settings": asdict(settings),
                        "fixed_truth": fixed,
                        "knee_truth": knee,
                        "summary": {
                            "strong_recovery": strong_recovery,
                            "strong_exact_one": strong_exact,
                            "strong_false_extra": strong_extra,
                            "minimum_two_peak_recovery": minimum_two,
                        },
                        "criteria": criteria,
                        "candidate_pass": all(criteria.values()),
                    }
                )

    passing = [row for row in rows if row["candidate_pass"]]
    output = {
        "scope": "known-truth fixed-mode frequency-range calibration",
        "rationale": "test official guidance that fixed mode should be limited to ranges where the aperiodic background is approximately log-log linear",
        "candidate_count": len(rows),
        "passing_count": len(passing),
        "passing_settings": [row["settings"] for row in passing],
        "results": rows,
        "selection_rule": "No automatic winner. A passing range is only a candidate until its failure modes and label-blind healthy behavior are inspected.",
        "interpretation_ceiling": "descriptive spectral parameterization only",
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
