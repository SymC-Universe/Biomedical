from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict
from pathlib import Path

import numpy as np

from src.chi_bio_candidate_math import spectral_radius, unity_regime
from src.chi_bio_g2_qualification import (
    exact_shared_transition_exists,
    g2_entrywise_noise_pilot,
    largest_singular_value,
    sampling_interval_consistency,
)


def run_harness(config: dict) -> dict:
    tol = config["tolerances"]
    boundary_tol = float(tol["boundary"])
    semigroup_tol = float(tol["semigroup_consistency"])
    residual_tol = float(tol["exact_transition_residual"])

    result = {
        "freeze_id": config["freeze_id"],
        "candidate_role": config["candidate_role"],
        "real_data_used": False,
        "chi_bio_outcomes_opened": False,
        "case_results": {},
        "status": "RUNNING",
    }
    all_pass = True

    unit_rows = []
    expected_regime = {
        "STABLE": "BELOW_UNITY",
        "BOUNDARY": "AT_UNITY_WITHIN_TOLERANCE",
        "UNSTABLE": "ABOVE_UNITY",
    }
    for case in config["unit_circle_cases"]:
        t = np.diag(np.asarray(case["diag"], dtype=float))
        rho = spectral_radius(t)
        regime = unity_regime(rho, tolerance=boundary_tol)
        passed = (
            abs(rho - float(case["expected_rho"])) <= boundary_tol
            and regime == expected_regime[case["label"]]
        )
        all_pass &= passed
        unit_rows.append(
            {
                "label": case["label"],
                "rho": rho,
                "regime": regime,
                "pass": bool(passed),
            }
        )
    result["case_results"]["UNIT_CIRCLE"] = unit_rows

    semigroup_rows = []
    for case in config["semigroup_cases"]:
        alpha = float(case["alpha_J"])
        intervals = tuple(float(x) for x in case["intervals"])
        radii = tuple(math.exp(alpha * d) for d in intervals)
        values = sampling_interval_consistency(
            radii,
            intervals,
            reference_interval=float(case["reference_interval"]),
            tolerance=semigroup_tol,
        )
        expected = math.exp(alpha * float(case["reference_interval"]))
        passed = max(abs(v - expected) for v in values) <= semigroup_tol
        all_pass &= passed
        semigroup_rows.append(
            {
                "alpha_J": alpha,
                "intervals": list(intervals),
                "radii": list(radii),
                "reference_values": list(values),
                "expected_reference_value": expected,
                "pass": bool(passed),
            }
        )
    result["case_results"]["SEMIGROUP_INTERVAL"] = semigroup_rows

    bad = config["inconsistent_interval_case"]
    refused = False
    try:
        sampling_interval_consistency(
            tuple(float(x) for x in bad["radii"]),
            tuple(float(x) for x in bad["intervals"]),
            tolerance=semigroup_tol,
        )
    except ValueError:
        refused = True
    all_pass &= refused
    result["case_results"]["INCONSISTENT_INTERVAL"] = {
        "refused": refused,
        "pass": refused,
    }

    nn = np.asarray(config["nonnormal_case"]["T"], dtype=float)
    rho_nn = spectral_radius(nn)
    sigma_nn = largest_singular_value(nn)
    nn_pass = rho_nn < 1.0 and sigma_nn > 1.0
    all_pass &= nn_pass
    result["case_results"]["NONNORMAL"] = {
        "rho": rho_nn,
        "largest_singular_value": sigma_nn,
        "pass": bool(nn_pass),
    }

    shared = config["shared_operator_cases"]
    x0 = np.asarray(shared["x_now"], dtype=float)
    good = np.asarray(shared["consistent_x_next"], dtype=float)
    bad_next = np.asarray(shared["inconsistent_x_next"], dtype=float)
    good_exists = exact_shared_transition_exists(
        x0, good, residual_tolerance=residual_tol
    )
    bad_exists = exact_shared_transition_exists(
        x0, bad_next, residual_tolerance=residual_tol
    )
    shared_pass = good_exists and not bad_exists
    all_pass &= shared_pass
    result["case_results"]["SHARED_OPERATOR"] = {
        "consistent_exact_operator_exists": good_exists,
        "inconsistent_exact_operator_exists": bad_exists,
        "pass": bool(shared_pass),
    }

    noise = config["noise_pilot"]
    truth_t = np.diag(np.asarray(noise["truth_diag"], dtype=float))
    noise_rows = []
    for sigma in noise["sigma_grid"]:
        summary = g2_entrywise_noise_pilot(
            truth_t,
            sigma=float(sigma),
            replicates=int(noise["replicates"]),
            seed=int(noise["seed"]),
            boundary_tolerance=boundary_tol,
        )
        noise_rows.append(asdict(summary))
    result["case_results"]["NOISE_PILOT"] = noise_rows

    result["required_cases_pass"] = bool(all_pass)
    result["status"] = (
        "PASS_G2_COMPARATOR_KNOWN_TRUTH_NO_REAL_DATA" if all_pass else "FAIL"
    )
    result["promotion_consequence"] = (
        "G2_COMPARATOR_SYNTHETIC_COMPONENT_SUPPORTED_ONLY; NO_CHI_BIO_PROMOTION"
        if all_pass
        else "STOP_AND_REPAIR_OR_NARROW_G2_ASSUMPTIONS"
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", default="config/gri_Chi_bio_g2_known_truth_harness_v0_1.json"
    )
    parser.add_argument(
        "--output",
        default="development_outputs/chi_bio_g2/GRI_CHI_BIO_G2_KNOWN_TRUTH_RESULT.json",
    )
    args = parser.parse_args()

    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    result = run_harness(cfg)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"].startswith("PASS") else 2


if __name__ == "__main__":
    raise SystemExit(main())
