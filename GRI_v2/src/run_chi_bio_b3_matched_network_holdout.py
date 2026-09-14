from __future__ import annotations

"""Unseen-seed holdout validation for the frozen B3 scoring architecture.

Scientific rules are frozen in
config/gri_Chi_bio_B3_matched_network_holdout_20260913_v0_1.json.
This runner cannot open real SCC25/TCGA expression or normalized G1. It tests
all dimensions 2..5 under both frozen regulon representations and selects only
the smallest dimension that passes every primary-noise gate on every unseen
seed in both representations.
"""

from importlib.metadata import version as package_version
import json
from pathlib import Path

import numpy as np

from src.run_chi_bio_b3_matched_network_pilot import (
    EXPECTED_DECOUPLER_VERSION,
    _control_only_pca_state,
    _network_matrix,
    _prepare_networks,
    _regulator_activity,
    _score,
    _subspace_summary,
    _synthetic_expression,
    _truth_trajectory,
)
from src.run_chi_bio_chronic_g2_empirical import (
    _baseline_errors,
    _diag,
    _fit,
    _loto,
    _make_transitions,
    _strictly_better,
)


CONFIG = Path("config/gri_Chi_bio_B3_matched_network_holdout_20260913_v0_1.json")
OUTPUT = Path(
    "development_outputs/chi_bio_regulon_source/b3_matched_network_holdout_20260913/"
    "GRI_CHI_BIO_B3_MATCHED_NETWORK_HOLDOUT.json"
)


def _validate_config(config: dict) -> None:
    required = {
        "status": "FROZEN_BEFORE_HOLDOUT_EXECUTION",
        "freeze_id": "GRI_CHI_BIO_B3_MATCHED_NETWORK_HOLDOUT_20260913_V0_1",
        "protocol_authority": "General_Cross_Project_Research_Protocol_v0.7.5_FINAL",
        "real_expression_opened_before_holdout": False,
        "real_tf_activity_scored_before_holdout": False,
        "normalized_g1_authorized": False,
        "chi_bio_status": "NOT_ADMITTED",
    }
    for key, expected in required.items():
        if config.get(key) != expected:
            raise RuntimeError(f"B3 holdout freeze mismatch for {key}: {config.get(key)!r}")
    if config.get("candidate_dimensions") != [2, 3, 4, 5]:
        raise RuntimeError("B3 holdout dimension set drift")
    if config.get("holdout_seeds") != [31001, 31003, 31007, 31009, 31013]:
        raise RuntimeError("B3 holdout seed set drift")
    if config.get("pilot_seed_reused") is not False:
        raise RuntimeError("pilot seed must not be reused in holdout")
    if config.get("network_representations") != [
        "COLLECTRI_PRIMARY",
        "DOROTHEA_ABC_SENSITIVITY",
    ]:
        raise RuntimeError("B3 holdout network representation drift")


def _activity_summary(truth_activity: np.ndarray, recovered: np.ndarray) -> dict:
    corrs: list[float] = []
    for j in range(truth_activity.shape[1]):
        a = truth_activity[:, j]
        b = recovered[:, j]
        if np.std(a) <= 1e-12 or np.std(b) <= 1e-12:
            continue
        corr = float(np.corrcoef(a, b)[0, 1])
        if np.isfinite(corr):
            corrs.append(corr)
    if not corrs:
        raise RuntimeError("holdout produced no finite regulator correlations")
    arr = np.asarray(corrs, dtype=float)
    return {
        "finite_regulator_count": int(arr.size),
        "median": float(np.median(arr)),
        "p10": float(np.quantile(arr, 0.10)),
        "fraction_gt_0_5": float(np.mean(arr > 0.5)),
        "fraction_gt_0_8": float(np.mean(arr > 0.8)),
        "fraction_negative": float(np.mean(arr < 0.0)),
    }


def _transition_metrics(state: np.ndarray, truth_transition: np.ndarray) -> dict:
    control_state = state[:11]
    treated_state = state[11:]
    x0, x1, u, arm = _make_transitions(control_state, treated_state)
    fit = _fit(x0, x1, u, "D1")
    loto = _loto(x0, x1, u, "D1")
    baselines = _baseline_errors(x0, x1, arm)
    record = {
        "status": fit["status"],
        "design_rank": fit.get("design_rank"),
        "design_columns": fit.get("design_columns"),
        "scaled_condition_number": fit.get("scaled_condition_number"),
        "all_loto_refits_admissible": bool(loto["all_refits_admissible"]),
        "loto_aggregate_nrmse": loto["aggregate_nrmse"],
        "persistence_nrmse": baselines["persistence_nrmse"],
        "arm_specific_loto_mean_next_state_nrmse": baselines[
            "arm_specific_loto_mean_next_state_nrmse"
        ],
    }
    if fit["status"] != "PASS" or loto["aggregate_nrmse"] is None:
        record.update(
            {
                "truth_rho": float(np.max(np.abs(np.linalg.eigvals(truth_transition)))),
                "recovered_rho": None,
                "relative_rho_error": None,
                "beats_persistence": False,
                "beats_arm_mean": False,
            }
        )
        return record
    recovered_rho = float(_diag(fit["T"])["rho"])
    truth_rho = float(np.max(np.abs(np.linalg.eigvals(truth_transition))))
    record.update(
        {
            "truth_rho": truth_rho,
            "recovered_rho": recovered_rho,
            "relative_rho_error": float(
                abs(recovered_rho - truth_rho)
                / max(abs(truth_rho), np.finfo(float).eps)
            ),
            "beats_persistence": bool(
                _strictly_better(loto["aggregate_nrmse"], baselines["persistence_nrmse"])
            ),
            "beats_arm_mean": bool(
                _strictly_better(
                    loto["aggregate_nrmse"],
                    baselines["arm_specific_loto_mean_next_state_nrmse"],
                )
            ),
        }
    )
    return record


def _gate_primary(record: dict, config: dict) -> tuple[bool, list[str]]:
    gate = config["primary_noise_pass_gate_per_seed_per_network"]
    failures: list[str] = []
    activity = record["regulator_activity_recovery"]
    subspace = record["latent_subspace_recovery"]
    transition = record["transition_recovery"]

    if activity["median"] < gate["regulator_activity_median_pearson_min"]:
        failures.append("ACTIVITY_MEDIAN_CORRELATION")
    if activity["fraction_gt_0_5"] < gate["regulator_activity_fraction_corr_gt_0_5_min"]:
        failures.append("ACTIVITY_FRACTION_GT_0_5")
    if subspace["minimum_canonical_cosine"] < gate[
        "latent_subspace_minimum_canonical_cosine_min"
    ]:
        failures.append("LATENT_MIN_CANONICAL_COSINE")
    if subspace["maximum_principal_angle_degrees"] > gate[
        "latent_subspace_maximum_principal_angle_degrees_max"
    ]:
        failures.append("LATENT_MAX_PRINCIPAL_ANGLE")
    if transition["status"] != gate["transition_full_fit_status"]:
        failures.append("TRANSITION_FULL_FIT")
    if transition["all_loto_refits_admissible"] is not True:
        failures.append("TRANSITION_LOTO_ADMISSIBILITY")
    if transition["relative_rho_error"] is None or transition["relative_rho_error"] > gate[
        "transition_relative_rho_error_max"
    ]:
        failures.append("TRANSITION_RHO_ERROR")
    if gate["transition_loto_must_strictly_beat_persistence_baseline"] and not transition[
        "beats_persistence"
    ]:
        failures.append("TRANSITION_PERSISTENCE_BASELINE")
    if gate[
        "transition_loto_must_strictly_beat_arm_specific_loto_mean_next_state_baseline"
    ] and not transition["beats_arm_mean"]:
        failures.append("TRANSITION_ARM_MEAN_BASELINE")
    if gate["design_full_rank_required"] and transition["design_rank"] != transition[
        "design_columns"
    ]:
        failures.append("TRANSITION_DESIGN_RANK")
    condition = transition["scaled_condition_number"]
    if condition is None or not np.isfinite(condition) or condition > gate[
        "scaled_condition_number_max"
    ]:
        failures.append("TRANSITION_CONDITION_NUMBER")
    return not failures, failures


def _run_condition(
    *,
    network_name: str,
    network_code: int,
    net,
    sources: list[str],
    genes: list[str],
    row_normalized_w,
    dimension: int,
    seed: int,
    noise_fraction: float,
    config: dict,
    apply_gate: bool,
) -> dict:
    control, treated, transition, _ = _truth_trajectory(dimension, seed)
    truth_state = np.vstack([control, treated])
    activity, _ = _regulator_activity(
        control,
        treated,
        len(sources),
        dimension,
        seed,
        network_code,
    )
    expression, sigma = _synthetic_expression(
        activity,
        row_normalized_w,
        noise_fraction,
        seed,
        network_code,
        dimension,
    )
    recovered = _score(expression, genes, net, sources)
    state, pca = _control_only_pca_state(recovered, dimension)
    record = {
        "network": network_name,
        "dimension": dimension,
        "seed": seed,
        "noise_fraction": noise_fraction,
        "noise_sigma": sigma,
        "regulator_activity_recovery": _activity_summary(activity, recovered),
        "latent_subspace_recovery": _subspace_summary(truth_state, recovered, dimension),
        "control_only_pca": pca,
        "transition_recovery": _transition_metrics(state, transition),
    }
    if apply_gate:
        passed, failures = _gate_primary(record, config)
        record["primary_gate_pass"] = passed
        record["primary_gate_failures"] = failures
    else:
        record["primary_gate_pass"] = None
        record["primary_gate_failures"] = []
    return record


def run_holdout(config: dict) -> dict:
    _validate_config(config)
    observed_version = package_version("decoupler")
    if observed_version != EXPECTED_DECOUPLER_VERSION:
        raise RuntimeError(
            f"decoupler version drift: {observed_version} != {EXPECTED_DECOUPLER_VERSION}"
        )
    genes, network_data = _prepare_networks()
    primary_noise = float(config["primary_noise_fraction_of_global_signal_sd"])
    diagnostic_noise = float(config["diagnostic_noise_fraction_of_global_signal_sd"])

    by_dimension: dict[str, dict] = {}
    passing_dimensions: list[int] = []
    for dimension in config["candidate_dimensions"]:
        dimension = int(dimension)
        network_results: dict[str, dict] = {}
        dimension_pass = True
        for network_code, network_name in enumerate(config["network_representations"], start=1):
            entry = network_data[network_name]
            net = entry["net"]
            sources = entry["sources"]
            row_normalized_w = _network_matrix(net, sources, genes)
            primary_records: list[dict] = []
            diagnostic_records: list[dict] = []
            for seed in config["holdout_seeds"]:
                seed = int(seed)
                primary_record = _run_condition(
                    network_name=network_name,
                    network_code=network_code,
                    net=net,
                    sources=sources,
                    genes=genes,
                    row_normalized_w=row_normalized_w,
                    dimension=dimension,
                    seed=seed,
                    noise_fraction=primary_noise,
                    config=config,
                    apply_gate=True,
                )
                primary_records.append(primary_record)
                diagnostic_records.append(
                    _run_condition(
                        network_name=network_name,
                        network_code=network_code,
                        net=net,
                        sources=sources,
                        genes=genes,
                        row_normalized_w=row_normalized_w,
                        dimension=dimension,
                        seed=seed,
                        noise_fraction=diagnostic_noise,
                        config=config,
                        apply_gate=False,
                    )
                )
            network_pass = all(r["primary_gate_pass"] for r in primary_records)
            if not network_pass:
                dimension_pass = False
            network_results[network_name] = {
                "eligible_regulator_count": len(sources),
                "eligible_edge_count": int(net.shape[0]),
                "all_primary_seed_gates_pass": network_pass,
                "primary_noise_records": primary_records,
                "diagnostic_0_30_noise_records": diagnostic_records,
            }
        if dimension_pass:
            passing_dimensions.append(dimension)
        by_dimension[str(dimension)] = {
            "dimension": dimension,
            "passes_both_networks_all_primary_seeds": dimension_pass,
            "networks": network_results,
        }

    selected = min(passing_dimensions) if passing_dimensions else None
    status = (
        "PASS_B3_MATCHED_NETWORK_IDENTIFIABILITY"
        if selected is not None
        else "REFUSE_B3_MATCHED_NETWORK_IDENTIFIABILITY"
    )
    return {
        "status": status,
        "freeze_id": config["freeze_id"],
        "protocol_authority": config["protocol_authority"],
        "decoupler_version": observed_version,
        "mapped_feature_count": len(genes),
        "candidate_dimensions": config["candidate_dimensions"],
        "holdout_seeds": config["holdout_seeds"],
        "primary_noise_fraction": primary_noise,
        "diagnostic_noise_fraction": diagnostic_noise,
        "passing_dimensions": passing_dimensions,
        "selected_smallest_fully_passing_dimension": selected,
        "dimension_selection_rule_applied_exactly": True,
        "results_by_dimension": by_dimension,
        "real_expression_opened": False,
        "real_tf_activity_scored": False,
        "real_data_opening_authorized_by_this_output": False,
        "normalized_g1_computed": False,
        "normalized_g1_authorized": False,
        "restoration_status": "UNRESOLVED_SEPARATE_GATE",
        "chi_bio_computed": False,
        "chi_bio_status": "NOT_ADMITTED",
        "promotion_effect": (
            "B3_DIMENSION_ELIGIBLE_FOR_SEPARATE_FINAL_EMPIRICAL_STATE_FREEZE"
            if selected is not None
            else "NONE_B3_IDENTIFIABILITY_REFUSED"
        ),
    }


def main() -> int:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    try:
        result = run_holdout(config)
        rc = 0 if result["status"].startswith("PASS") else 3
    except Exception as exc:
        result = {
            "status": "REFUSE_B3_HOLDOUT_EXECUTION",
            "reason": f"{type(exc).__name__}: {exc}",
            "real_expression_opened": False,
            "normalized_g1_authorized": False,
            "chi_bio_status": "NOT_ADMITTED",
            "promotion_effect": "NONE_MECHANICAL_OR_HOLDOUT_EXECUTION_FAILURE",
        }
        rc = 2
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
