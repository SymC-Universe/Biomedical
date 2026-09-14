from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

import numpy as np

from src.chi_bio_candidate_math import spectral_abscissa, unity_regime
from src.chi_bio_g1_hardening import (
    g1_hardening_audit,
    local_jacobian,
    scalar_restoration_g1_value,
    symmetric_generalized_g1_value,
)
from src.chi_bio_g1_qualification import (
    continuous_time_numerical_abscissa,
    dominant_mode_status,
    g1a_entrywise_noise_pilot,
)


def _diag(values: list[float]) -> np.ndarray:
    return np.diag(np.asarray(values, dtype=float))


def _expected_regime(value: float, atol: float) -> str:
    return unity_regime(value, tolerance=atol)


def run_harness(config: dict) -> dict:
    tol = config["global_tolerances"]
    exact_atol = float(tol["exact_matrix_value_atol"])
    boundary_atol = float(tol["boundary_value_atol"])

    result: dict = {
        "freeze_id": config["freeze_id"],
        "candidate_family": config["candidate_family"],
        "status": "RUNNING",
        "real_cancer_values_used": False,
        "atlas_or_unity_placement_used_for_selection": False,
        "case_results": {},
    }
    all_required_pass = True

    # G1A: common-restoration exact relation.
    g1a_cfg = config["case_families"]["G1A_COMMON_RESTORATION"]
    g1a_rows = []
    groups = [
        ("STABLE", g1a_cfg["stable_diagonal_M"]),
        ("BOUNDARY", g1a_cfg["boundary_diagonal_M"]),
        ("UNSTABLE", g1a_cfg["unstable_diagonal_M"]),
    ]
    expected_regimes = {
        "STABLE": "BELOW_UNITY",
        "BOUNDARY": "AT_UNITY_WITHIN_TOLERANCE",
        "UNSTABLE": "ABOVE_UNITY",
    }
    for beta in g1a_cfg["beta_grid"]:
        beta = float(beta)
        for label, matrices in groups:
            for diag_values in matrices:
                m = _diag(diag_values)
                r = beta * np.eye(m.shape[0])
                k = beta * m
                value = scalar_restoration_g1_value(k, r)
                alpha_j = spectral_abscissa(local_jacobian(k, r))
                relation_error = abs(alpha_j - beta * (value - 1.0))
                regime = _expected_regime(value, boundary_atol)
                passed = relation_error <= exact_atol and regime == expected_regimes[label]
                all_required_pass &= passed
                g1a_rows.append(
                    {
                        "beta": beta,
                        "truth_label": label,
                        "diag_M": [float(x) for x in diag_values],
                        "value": value,
                        "alpha_J": alpha_j,
                        "relation_error": relation_error,
                        "regime": regime,
                        "pass": bool(passed),
                    }
                )
    result["case_results"]["G1A_COMMON_RESTORATION"] = g1a_rows

    # G1B: symmetric generalized exact relation.
    g1b_rows = []
    for case in config["case_families"]["G1B_SYMMETRIC_GENERALIZED"]["cases"]:
        r = _diag(case["R_diag"])
        k = _diag(case["K_diag"])
        value = symmetric_generalized_g1_value(k, r)
        alpha_j = spectral_abscissa(local_jacobian(k, r))
        truth = case["truth"]
        expected_sign = {"STABLE": -1, "BOUNDARY": 0, "UNSTABLE": 1}[truth]
        if expected_sign < 0:
            sign_ok = alpha_j < 0
        elif expected_sign > 0:
            sign_ok = alpha_j > 0
        else:
            sign_ok = abs(alpha_j) <= boundary_atol
        passed = abs(value - float(case["value"])) <= exact_atol and sign_ok
        all_required_pass &= passed
        g1b_rows.append(
            {
                "truth_label": truth,
                "value": value,
                "expected_value": float(case["value"]),
                "alpha_J": alpha_j,
                "pass": bool(passed),
            }
        )
    result["case_results"]["G1B_SYMMETRIC_GENERALIZED"] = g1b_rows

    # G1C: prove naive heterogeneous normalization can fail in both directions.
    g1c_cfg = config["case_families"]["G1C_DIRECTED_HETEROGENEOUS_COUNTEREXAMPLES"]
    g1c_rows = []
    for name in ("false_safe", "false_unsafe"):
        case = g1c_cfg[name]
        r = np.asarray(case["R"], dtype=float)
        k = np.asarray(case["K"], dtype=float)
        audit = g1_hardening_audit(k, r)
        if name == "false_safe":
            passed = (
                abs(audit.naive_left_normalized_abscissa - float(case["alpha_RinvK"])) <= exact_atol
                and abs(audit.jacobian_spectral_abscissa - float(case["alpha_J"])) <= exact_atol
                and audit.naive_left_normalized_abscissa < 1.0
                and audit.jacobian_spectral_abscissa > 0.0
                and audit.exact_unity_route == "NO_EXACT_UNITY_ROUTE_FROM_NAIVE_NORMALIZATION"
            )
        else:
            passed = (
                abs(audit.naive_left_normalized_abscissa - float(case["alpha_RinvK"])) <= 1e-6
                and audit.naive_left_normalized_abscissa > 1.0
                and audit.jacobian_spectral_abscissa < 0.0
                and audit.exact_unity_route == "NO_EXACT_UNITY_ROUTE_FROM_NAIVE_NORMALIZATION"
            )
        all_required_pass &= passed
        row = asdict(audit)
        row.update({"case": name, "pass": bool(passed)})
        g1c_rows.append(row)
    result["case_results"]["G1C_DIRECTED_HETEROGENEOUS_COUNTEREXAMPLES"] = g1c_rows

    # Dominant-mode degeneracy.
    gap_tol = float(tol["near_degenerate_eigenvalue_gap"])
    degeneracy_rows = []
    for matrix in config["case_families"]["G1_MODE_DEGENERACY"]["matrices"]:
        arr = np.asarray(matrix, dtype=float)
        status = dominant_mode_status(arr, gap_tolerance=gap_tol)
        passed = status == "DOMINANT_SUBSPACE_NEAR_DEGENERATE"
        all_required_pass &= passed
        degeneracy_rows.append({"matrix": matrix, "status": status, "pass": bool(passed)})
    result["case_results"]["G1_MODE_DEGENERACY"] = degeneracy_rows

    # Nonnormal stable spectrum with transient-growth warning.
    nonnormal_cfg = config["case_families"]["G1_NONNORMAL_TRANSIENT"]
    m = np.asarray(nonnormal_cfg["M"], dtype=float)
    beta = float(nonnormal_cfg["beta"])
    j = beta * (m - np.eye(m.shape[0]))
    alpha_j = spectral_abscissa(j)
    numerical_alpha = continuous_time_numerical_abscissa(j)
    nonnormal_pass = alpha_j < 0.0 and numerical_alpha > 0.0
    all_required_pass &= nonnormal_pass
    result["case_results"]["G1_NONNORMAL_TRANSIENT"] = {
        "alpha_J": alpha_j,
        "numerical_abscissa_J": numerical_alpha,
        "pass": bool(nonnormal_pass),
    }

    # Frozen deterministic uncertainty/noise pilot. This reports behavior; it
    # does not promote the candidate or tune thresholds.
    noise_cfg = config["noise_and_uncertainty_pilot"]
    truth_m = _diag(noise_cfg["truth_M_diag"])
    seed = int(noise_cfg["seed"])
    reps = int(noise_cfg["replicates_per_cell"])
    noise_rows = []
    for sigma in noise_cfg["entrywise_gaussian_sigma_grid"]:
        summary = g1a_entrywise_noise_pilot(
            truth_m,
            sigma=float(sigma),
            replicates=reps,
            seed=seed,
            boundary_tolerance=boundary_atol,
        )
        noise_rows.append(asdict(summary))
    result["case_results"]["G1_NOISE_PILOT"] = noise_rows

    result["required_exact_cases_pass"] = bool(all_required_pass)
    result["status"] = "PASS_EXACT_AND_FAILURE_CASES_NO_REAL_DATA" if all_required_pass else "FAIL"
    result["promotion_consequence"] = (
        "CB9_SYNTHETIC_MATH_COMPONENT_SUPPORTED_ONLY; CANDIDATE_LOCK_NOT_EARNED"
        if all_required_pass
        else "STOP_AND_REPAIR_OR_REVISE_DERIVATION"
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default="config/gri_Chi_bio_g1_known_truth_harness_v0_1.json",
    )
    parser.add_argument(
        "--output",
        default="development_outputs/chi_bio_g1/GRI_CHI_BIO_G1_KNOWN_TRUTH_RESULT.json",
    )
    args = parser.parse_args()

    config_path = Path(args.config)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    result = run_harness(config)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"].startswith("PASS") else 2


if __name__ == "__main__":
    raise SystemExit(main())
