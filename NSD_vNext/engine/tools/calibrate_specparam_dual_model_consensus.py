#!/usr/bin/env python3
"""Known-truth calibration of a conservative fixed/knee consensus policy.

Rationale
---------
The first failure map showed that a misspecified fixed aperiodic model can invent
periodic peaks on knee truth even with excellent R-squared. Rather than choosing
an aperiodic family from clinical or healthy data, this script asks whether a
more conservative descriptive policy can be qualified on known truth:

    admit a descriptive periodic component only when fixed and knee fits both
    return a center-frequency-matched peak and neither matched peak is pinned to
    the allowed width boundary.

This is a candidate *descriptive* admission rule. It does not license a neural
mode, damping, natural frequency, Q, chi, diagnosis, or prognosis.
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

from nsd_engine.specparam_adapter import DescriptivePeak, SpecparamSettings, fit_specparam_descriptive


FREQS = np.arange(1.0, 45.0 + 0.25, 0.25, dtype=float)
PEAK_THRESHOLDS = (2.0, 2.5, 3.0)
MAX_N_PEAKS = (3, 4)
MIN_PEAK_HEIGHT = 0.20
NOISE_SDS = (0.02, 0.04)
SEEDS = tuple(range(202609140, 202609150))
SINGLE_HEIGHTS = (0.20, 0.30, 0.45)
CENTER_CONSENSUS_TOLERANCE_HZ = 0.75
TRUTH_CF_TOLERANCE_HZ = 0.75
TRUTH_BW_RELATIVE_TOLERANCE = 0.50
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


def _settings(mode: str, peak_threshold: float, max_n_peaks: int) -> SpecparamSettings:
    return SpecparamSettings(
        aperiodic_mode=mode,
        periodic_mode="gaussian",
        peak_width_limits=(0.5, 12.0),
        max_n_peaks=max_n_peaks,
        min_peak_height=MIN_PEAK_HEIGHT,
        peak_threshold=peak_threshold,
        fmin_hz=1.0,
        fmax_hz=45.0,
    )


def _at_width_boundary(peak: DescriptivePeak, settings: SpecparamSettings) -> bool:
    lower, upper = settings.peak_width_limits
    return math.isclose(peak.bandwidth_hz, lower, abs_tol=WIDTH_BOUNDARY_ATOL_HZ) or math.isclose(
        peak.bandwidth_hz, upper, abs_tol=WIDTH_BOUNDARY_ATOL_HZ
    )


def _consensus_peaks(fixed_result, knee_result) -> list[dict[str, float]]:
    """Greedy one-to-one center matching, excluding width-boundary fits."""
    fixed_candidates = [
        peak for peak in fixed_result.peaks if not _at_width_boundary(peak, fixed_result.settings)
    ]
    knee_candidates = [
        peak for peak in knee_result.peaks if not _at_width_boundary(peak, knee_result.settings)
    ]
    remaining = set(range(len(knee_candidates)))
    matches: list[dict[str, float]] = []
    for fixed_peak in sorted(fixed_candidates, key=lambda peak: peak.center_frequency_hz):
        possible = [
            index
            for index in remaining
            if abs(fixed_peak.center_frequency_hz - knee_candidates[index].center_frequency_hz)
            <= CENTER_CONSENSUS_TOLERANCE_HZ
        ]
        if not possible:
            continue
        best = min(
            possible,
            key=lambda index: abs(
                fixed_peak.center_frequency_hz - knee_candidates[index].center_frequency_hz
            ),
        )
        knee_peak = knee_candidates[best]
        remaining.remove(best)
        matches.append(
            {
                "center_frequency_hz": 0.5
                * (fixed_peak.center_frequency_hz + knee_peak.center_frequency_hz),
                "fixed_center_frequency_hz": fixed_peak.center_frequency_hz,
                "knee_center_frequency_hz": knee_peak.center_frequency_hz,
                "fixed_bandwidth_hz": fixed_peak.bandwidth_hz,
                "knee_bandwidth_hz": knee_peak.bandwidth_hz,
                "center_disagreement_hz": abs(
                    fixed_peak.center_frequency_hz - knee_peak.center_frequency_hz
                ),
            }
        )
    return matches


def _truth_match(consensus: dict[str, float], cf: float, bw: float) -> bool:
    cf_ok = abs(consensus["center_frequency_hz"] - cf) <= TRUTH_CF_TOLERANCE_HZ
    fixed_bw_ok = abs(consensus["fixed_bandwidth_hz"] - bw) / bw <= TRUTH_BW_RELATIVE_TOLERANCE
    knee_bw_ok = abs(consensus["knee_bandwidth_hz"] - bw) / bw <= TRUTH_BW_RELATIVE_TOLERANCE
    return cf_ok and fixed_bw_ok and knee_bw_ok


def _fit_both(log_power: np.ndarray, peak_threshold: float, max_n_peaks: int):
    linear = _power(log_power)
    fixed = fit_specparam_descriptive(
        FREQS, linear, settings=_settings("fixed", peak_threshold, max_n_peaks)
    )
    knee = fit_specparam_descriptive(
        FREQS, linear, settings=_settings("knee", peak_threshold, max_n_peaks)
    )
    return fixed, knee, _consensus_peaks(fixed, knee)


def _mean_bool(rows: list[dict[str, object]], key: str) -> float:
    return float(np.mean([bool(row[key]) for row in rows])) if rows else float("nan")


def _mean_num(rows: list[dict[str, object]], key: str) -> float:
    return float(np.mean([float(row[key]) for row in rows])) if rows else float("nan")


def _evaluate_background(background_name: str, peak_threshold: float, max_n_peaks: int) -> dict[str, object]:
    background = _fixed_log_power if background_name == "fixed" else _knee_log_power

    no_peak_rows: list[dict[str, object]] = []
    for noise_sd in NOISE_SDS:
        for seed in SEEDS:
            fixed, knee, consensus = _fit_both(
                background(FREQS) + _noise(seed, noise_sd), peak_threshold, max_n_peaks
            )
            no_peak_rows.append(
                {
                    "false_positive": len(consensus) > 0,
                    "consensus_count": len(consensus),
                    "fixed_peak_count": len(fixed.peaks),
                    "knee_peak_count": len(knee.peaks),
                }
            )

    single: dict[str, object] = {}
    for height in SINGLE_HEIGHTS:
        rows: list[dict[str, object]] = []
        for noise_sd in NOISE_SDS:
            for seed in SEEDS:
                fixed, knee, consensus = _fit_both(
                    background(FREQS)
                    + _gaussian(FREQS, 10.0, height, 1.0)
                    + _noise(seed, noise_sd),
                    peak_threshold,
                    max_n_peaks,
                )
                matching = [peak for peak in consensus if _truth_match(peak, 10.0, 2.0)]
                rows.append(
                    {
                        "recovered": len(matching) >= 1,
                        "exactly_one_consensus": len(consensus) == 1,
                        "false_extra_consensus": max(0, len(consensus) - 1),
                    }
                )
        single[f"{height:.2f}"] = {
            "recovery_rate": _mean_bool(rows, "recovered"),
            "exactly_one_rate": _mean_bool(rows, "exactly_one_consensus"),
            "mean_false_extra": _mean_num(rows, "false_extra_consensus"),
        }

    two_rows: list[dict[str, object]] = []
    for noise_sd in NOISE_SDS:
        for seed in SEEDS:
            _, _, consensus = _fit_both(
                background(FREQS)
                + _gaussian(FREQS, 10.0, 0.45, 0.8)
                + _gaussian(FREQS, 12.0, 0.45, 0.8)
                + _noise(seed, noise_sd),
                peak_threshold,
                max_n_peaks,
            )
            truth1 = [peak for peak in consensus if _truth_match(peak, 10.0, 1.6)]
            truth2 = [peak for peak in consensus if _truth_match(peak, 12.0, 1.6)]
            # There must be two distinct consensus objects. Center separation
            # makes accidental reuse impossible under the 0.75-Hz truth tolerance.
            recovered_two = bool(truth1) and bool(truth2) and len(consensus) >= 2
            two_rows.append(
                {
                    "recovered_two": recovered_two,
                    "exactly_two": len(consensus) == 2,
                    "false_extra": max(0, len(consensus) - 2),
                }
            )

    return {
        "background_truth": background_name,
        "no_peak": {
            "false_positive_rate": _mean_bool(no_peak_rows, "false_positive"),
            "mean_consensus_peak_count": _mean_num(no_peak_rows, "consensus_count"),
            "mean_fixed_peak_count": _mean_num(no_peak_rows, "fixed_peak_count"),
            "mean_knee_peak_count": _mean_num(no_peak_rows, "knee_peak_count"),
        },
        "single_peak": single,
        "two_peaks_2hz_separation": {
            "recovery_rate": _mean_bool(two_rows, "recovered_two"),
            "exactly_two_rate": _mean_bool(two_rows, "exactly_two"),
            "mean_false_extra": _mean_num(two_rows, "false_extra"),
        },
    }


def main() -> int:
    rows: list[dict[str, object]] = []
    for threshold in PEAK_THRESHOLDS:
        for max_peaks in MAX_N_PEAKS:
            fixed = _evaluate_background("fixed", threshold, max_peaks)
            knee = _evaluate_background("knee", threshold, max_peaks)

            strong_keys = ("0.20", "0.30", "0.45")
            strong_recovery = float(
                np.mean(
                    [
                        fixed["single_peak"][key]["recovery_rate"]
                        for key in strong_keys
                    ]
                    + [
                        knee["single_peak"][key]["recovery_rate"]
                        for key in strong_keys
                    ]
                )
            )
            strong_exact = float(
                np.mean(
                    [
                        fixed["single_peak"][key]["exactly_one_rate"]
                        for key in strong_keys
                    ]
                    + [
                        knee["single_peak"][key]["exactly_one_rate"]
                        for key in strong_keys
                    ]
                )
            )
            strong_extra = float(
                np.mean(
                    [
                        fixed["single_peak"][key]["mean_false_extra"]
                        for key in strong_keys
                    ]
                    + [
                        knee["single_peak"][key]["mean_false_extra"]
                        for key in strong_keys
                    ]
                )
            )
            two_recovery = min(
                float(fixed["two_peaks_2hz_separation"]["recovery_rate"]),
                float(knee["two_peaks_2hz_separation"]["recovery_rate"]),
            )

            criteria = {
                "fixed_no_peak_fp_le_0_05": fixed["no_peak"]["false_positive_rate"] <= 0.05,
                "knee_no_peak_fp_le_0_05": knee["no_peak"]["false_positive_rate"] <= 0.05,
                "cross_background_strong_recovery_ge_0_85": strong_recovery >= 0.85,
                "cross_background_strong_exact_one_ge_0_80": strong_exact >= 0.80,
                "cross_background_strong_false_extra_le_0_10": strong_extra <= 0.10,
                "both_background_two_peak_recovery_ge_0_75": two_recovery >= 0.75,
            }
            rows.append(
                {
                    "settings": {
                        "min_peak_height": MIN_PEAK_HEIGHT,
                        "peak_threshold": threshold,
                        "max_n_peaks": max_peaks,
                        "fixed_and_knee_both_required": True,
                        "center_consensus_tolerance_hz": CENTER_CONSENSUS_TOLERANCE_HZ,
                        "width_boundary_peaks_excluded": True,
                    },
                    "fixed_truth": fixed,
                    "knee_truth": knee,
                    "cross_background_summary": {
                        "strong_single_recovery_rate": strong_recovery,
                        "strong_single_exact_one_rate": strong_exact,
                        "strong_single_mean_false_extra": strong_extra,
                        "minimum_two_peak_recovery_rate": two_recovery,
                    },
                    "criteria": criteria,
                    "candidate_pass": all(criteria.values()),
                }
            )

    passing = [row for row in rows if row["candidate_pass"]]
    output = {
        "scope": "known-truth fixed/knee consensus descriptive peak-admission calibration",
        "policy": {
            "both_aperiodic_models_required": True,
            "min_peak_height": MIN_PEAK_HEIGHT,
            "center_consensus_tolerance_hz": CENTER_CONSENSUS_TOLERANCE_HZ,
            "width_boundary_peaks_excluded": True,
            "no_clinical_or_real_eeg_data_used": True,
        },
        "candidate_count": len(rows),
        "passing_count": len(passing),
        "passing_settings": [row["settings"] for row in passing],
        "results": rows,
        "selection_rule": "No automatic winner; any passing setting remains a candidate for a label-blind healthy repeat pilot. Failure does not justify relaxing criteria after viewing healthy data.",
        "interpretation_ceiling": "descriptive spectral admission only",
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
