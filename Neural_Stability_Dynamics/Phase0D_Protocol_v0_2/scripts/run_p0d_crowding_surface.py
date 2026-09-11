from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np

from src.rank_sweep import sweep_ssi_cov, sweep_subspace_dmd, adjacent_rank_stability
from src.selector import subspace_similarity
from src.mode_tracking import track_modes
from src.synthetic_systems import (
    add_measurement_noise,
    make_linear_system,
    make_noise_bases,
    simulate_linear,
    truth_modes,
)


DT = 0.02
N_SAMPLES = 2400
N_CHANNELS = 6
BLOCK_ROWS = 18
PROCESS_SCALE = 0.35
MIN_HZ = 0.25
PLANTED_ORDER = 4
CANDIDATE_GRID = [2, 3, 4, 5, 6]
REPLICATES = 8
SEED_BASE = 202609111700
BASE_FREQUENCY_HZ = 6.0
DECAY = 0.7
SEPARATIONS_HZ = [4.0, 2.0, 1.0, 0.5, 0.30, 0.22, 0.15, 0.10, 0.05, 0.02]
NOISE = {"type": "white", "fraction_channel_sd": 0.05}


def _finite(value):
    try:
        x = float(value)
    except (TypeError, ValueError):
        return None
    return x if np.isfinite(x) else None


def _clean(value):
    if isinstance(value, dict):
        return {str(k): _clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_clean(v) for v in value]
    if isinstance(value, np.ndarray):
        return [_clean(v) for v in value.tolist()]
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return _finite(value)
    if isinstance(value, complex):
        return {"real": float(value.real), "imag": float(value.imag)}
    if isinstance(value, float) and not np.isfinite(value):
        return None
    return value


def _role(separation_hz):
    # P0-D coverage labels only; these are not scientific boundaries.
    if separation_hz >= 2.0:
        return "NOMINAL_FUNCTION"
    if separation_hz >= 0.30:
        return "PERTURBED_FUNCTION"
    return "BOUNDARY_OR_TRANSITION"


def _simulate(separation_hz, replicate):
    spec = {
        "modes": [
            {"type": "complex", "decay": DECAY, "frequency_hz": BASE_FREQUENCY_HZ},
            {"type": "complex", "decay": DECAY, "frequency_hz": BASE_FREQUENCY_HZ + float(separation_hz)},
        ],
        "similarity": "orthogonal",
    }
    seed = SEED_BASE + 10000 * int(replicate) + int(round(float(separation_hz) * 1000))
    rng_sys = np.random.default_rng(seed)
    rng_proc = np.random.default_rng(seed + 1)
    rng_noise = np.random.default_rng(seed + 2)
    A, C = make_linear_system(spec, N_CHANNELS, rng_sys)
    clean = simulate_linear(A, C, DT, N_SAMPLES, PROCESS_SCALE, rng_proc)
    white, colored = make_noise_bases(N_SAMPLES, N_CHANNELS, 0.0, rng_noise)
    Y = add_measurement_noise(clean, NOISE, white, colored)
    true_vals, true_shapes = truth_modes(A, C)
    return Y, true_vals, true_shapes


def _positive(vals):
    vals = np.asarray(vals, complex)
    return np.where(vals.imag / (2 * np.pi) >= MIN_HZ)[0]


def _fit_metrics(sweep, true_vals, true_shapes):
    fit = sweep["fits"].get(PLANTED_ORDER)
    if fit is None or fit.get("status") != "OK":
        return {
            "fit_status": None if fit is None else fit.get("status"),
            "exception": None if fit is None else fit.get("exception_message"),
            "complete_stable_two_mode_candidate_set": False,
        }

    est_vals = np.asarray(fit["vals"], complex)
    est_shapes = np.asarray(fit["shapes"], complex)
    ti = _positive(true_vals)
    ei = _positive(est_vals)
    unstable_fraction = float(np.mean(est_vals.real >= 0.0)) if len(est_vals) else None
    complete = len(ti) == 2 and len(ei) >= 2 and unstable_fraction == 0.0

    tracking = track_modes(
        np.asarray(true_vals)[ti],
        np.asarray(true_shapes)[:, ti],
        est_vals[ei],
        est_shapes[:, ei],
        min_hz=MIN_HZ,
    ) if len(ti) and len(ei) else None

    pairs = [] if tracking is None else tracking["candidate_pairs"]
    macs = np.asarray([p["MAC"] for p in pairs], float)
    pole_distances = np.asarray([p["pole_distance"] for p in pairs], float)
    margins = np.asarray([p["assignment_margin"] for p in pairs], float)
    finite_margins = margins[np.isfinite(margins)]

    sub = None
    if len(ti) and len(ei) >= len(ti):
        # Use the estimator columns present in candidate pairs so joint carrier
        # recovery can be compared with individual-pair stability.
        est_cols = [p["b_index"] for p in pairs]
        truth_cols = [p["a_index"] for p in pairs]
        if len(est_cols) == len(ti):
            sub = subspace_similarity(
                np.asarray(true_shapes)[:, ti][..., truth_cols],
                est_shapes[:, ei][..., est_cols],
            )

    est_positive = est_vals[ei]
    est_sep = None
    if len(est_positive) >= 2:
        freqs = np.sort(est_positive.imag / (2 * np.pi))
        est_sep = float(np.min(np.diff(freqs)))

    return {
        "fit_status": "OK",
        "complete_stable_two_mode_candidate_set": bool(complete),
        "estimated_positive_complex_modes": int(len(ei)),
        "estimated_unstable_fraction": unstable_fraction,
        "estimated_minimum_positive_mode_separation_hz": est_sep,
        "truth_to_est_candidate_pairs": int(len(pairs)),
        "individual_MAC_median_P0_ONLY": float(np.median(macs)) if len(macs) else None,
        "individual_MAC_minimum_P0_ONLY": float(np.min(macs)) if len(macs) else None,
        "relative_pole_distance_median_P0_ONLY": float(np.median(pole_distances)) if len(pole_distances) else None,
        "relative_pole_distance_maximum_P0_ONLY": float(np.max(pole_distances)) if len(pole_distances) else None,
        "assignment_margin_minimum_P0_ONLY": float(np.min(finite_margins)) if len(finite_margins) else None,
        "carrier_subspace_similarity_P0_ONLY": _finite(sub),
        "tracking_status": None if tracking is None else tracking["status"],
    }


def _med(group, field):
    vals = [float(r[field]) for r in group if r.get(field) is not None and np.isfinite(r[field])]
    return float(np.median(vals)) if vals else None


def build_surface():
    records = []
    for separation_hz in SEPARATIONS_HZ:
        truth_crowding_ratio = float(2 * np.pi * separation_hz / (2 * DECAY))
        for replicate in range(REPLICATES):
            Y, true_vals, true_shapes = _simulate(separation_hz, replicate)
            sweeps = {
                "SSI_COV": sweep_ssi_cov(Y, DT, BLOCK_ROWS, CANDIDATE_GRID),
                "SUBSPACE_DMD": sweep_subspace_dmd(Y, DT, CANDIDATE_GRID),
            }
            for method, sweep in sweeps.items():
                metrics = _fit_metrics(sweep, true_vals, true_shapes)
                records.append(
                    {
                        "research_mode": "P0-D",
                        "coverage_role": _role(separation_hz),
                        "method": method,
                        "separation_hz": float(separation_hz),
                        "replicate": int(replicate),
                        "truth_crowding_ratio_delta_omega_over_sum_decay_P0_ONLY": truth_crowding_ratio,
                        "planted_order_P0_ONLY": PLANTED_ORDER,
                        **metrics,
                        "adjacent_rank_stability_data_only": adjacent_rank_stability(sweep, min_hz=MIN_HZ),
                        "singular_values_first_12_data_only": [float(x) for x in np.asarray(sweep["singular_values"])[:12]],
                    }
                )

    summary = []
    by = defaultdict(list)
    for record in records:
        by[(record["separation_hz"], record["method"])].append(record)
    for (separation_hz, method), group in sorted(by.items(), key=lambda x: (-x[0][0], x[0][1])):
        summary.append(
            {
                "separation_hz": float(separation_hz),
                "truth_crowding_ratio_delta_omega_over_sum_decay_P0_ONLY": group[0]["truth_crowding_ratio_delta_omega_over_sum_decay_P0_ONLY"],
                "coverage_role": group[0]["coverage_role"],
                "method": method,
                "records": len(group),
                "complete_stable_two_mode_candidate_set_count": int(sum(bool(r["complete_stable_two_mode_candidate_set"]) for r in group)),
                "individual_MAC_median_of_records_P0_ONLY": _med(group, "individual_MAC_median_P0_ONLY"),
                "individual_MAC_minimum_median_P0_ONLY": _med(group, "individual_MAC_minimum_P0_ONLY"),
                "carrier_subspace_similarity_median_P0_ONLY": _med(group, "carrier_subspace_similarity_P0_ONLY"),
                "assignment_margin_minimum_median_P0_ONLY": _med(group, "assignment_margin_minimum_P0_ONLY"),
                "relative_pole_distance_median_P0_ONLY": _med(group, "relative_pole_distance_median_P0_ONLY"),
                "estimated_mode_separation_hz_median": _med(group, "estimated_minimum_positive_mode_separation_hz"),
            }
        )

    return _clean(
        {
            "schema": "nsd-phase0d-v0.2-p0d3-crowding-surface-v1",
            "status": "P0_D_RESPONSE_SURFACE_NOT_CONFIRMATORY",
            "protocol": "General Cross-Project Research Protocol v0.7.1 FINAL + v0.7.1A Addendum",
            "p1_authorized": False,
            "scientific_question": "As two fully observed oscillatory modes approach one another in frequency, how do individual carrier identity, joint carrier-subspace recovery, pole recovery and rank stability reorganize for the current estimators?",
            "control": {
                "base_frequency_hz": BASE_FREQUENCY_HZ,
                "second_frequency_hz": [BASE_FREQUENCY_HZ + x for x in SEPARATIONS_HZ],
                "separations_hz": SEPARATIONS_HZ,
                "decay_each": DECAY,
                "measurement_noise": NOISE,
                "replicates_per_separation": REPLICATES,
                "seed_base": SEED_BASE,
                "planted_order": PLANTED_ORDER,
                "candidate_grid_data_only": CANDIDATE_GRID,
            },
            "claim_objects_kept_separate": [
                "complete stable two-mode candidate-set generation at planted order",
                "individual truth-to-estimator carrier assignment quality",
                "joint two-mode carrier-subspace recovery",
                "pole recovery",
                "data-only adjacent-rank stability",
            ],
            "summary": summary,
            "records": records,
            "nonclaims": [
                "No crowding boundary is frozen from this surface.",
                "No individual-mode MAC, assignment-margin, pole-error or subspace threshold is selected here.",
                "Coverage-role labels are P0-D mapping labels, not claims that nature changes regime at those labels.",
                "A high joint subspace similarity does not by itself validate individual carrier identity.",
                "A low individual assignment quality does not by itself invalidate the joint carrier subspace.",
                "No P0Q1 status, P1 design, EEG claim, chi coordinate or biological mechanism is changed."
            ],
        }
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/p0d_mapping/crowding_surface_v1.json")
    args = parser.parse_args()
    record = build_surface()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out.resolve())
    for row in record["summary"]:
        print(json.dumps(row, sort_keys=True))
    print("P0-D CROWDING RESPONSE SURFACE COMPLETE. No threshold or P1 science was frozen.")


if __name__ == "__main__":
    main()
