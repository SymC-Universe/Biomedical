from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

from src.tool_feasibility_kernel import (
    cross_validated_modal_predictability,
    linear_cka,
    modal_summary,
    predictability_permutation_calibration,
    residualize_covariates,
    row_permute,
    same_module_abs_spearman,
    stable_seed,
)

N_REPLICATES = 24
GLOBAL_NULLS = 39
SEMANTIC_NULLS = 39
AUTONOMY_NULLS = 19
SEED_NAMESPACE = "GRI_V2_TOOL_FEASIBILITY_20260830_F2"


def _rng(scenario: str, replicate: int, token: str = "DATA") -> np.random.Generator:
    return np.random.default_rng(stable_seed(SEED_NAMESPACE, scenario, replicate, token))


def _geometry_stats(x: np.ndarray, y: np.ndarray, scenario: str, replicate: int, token: str) -> dict[str, float | bool]:
    observed = float(linear_cka(x, y))
    null = np.array(
        [
            linear_cka(
                row_permute(x, stable_seed(SEED_NAMESPACE, scenario, replicate, token, "ROW_NULL", i)),
                y,
            )
            for i in range(GLOBAL_NULLS)
        ],
        dtype=float,
    )
    null_median = float(np.median(null))
    effect = float(observed - null_median)
    p = float((1 + np.sum(null >= observed)) / (GLOBAL_NULLS + 1))
    detected = bool((p <= 0.05) and (effect >= 0.05))
    return {
        "cka_observed": observed,
        "cka_null_median": null_median,
        "delta_cka": effect,
        "cka_p_upper": p,
        "global_shared_detected": detected,
    }


def _semantic_stats(a: np.ndarray, b: np.ndarray, scenario: str, replicate: int, token: str) -> dict[str, float | bool]:
    observed, _ = same_module_abs_spearman(a, b)
    null_values = []
    for i in range(SEMANTIC_NULLS):
        rng = np.random.default_rng(stable_seed(SEED_NAMESPACE, scenario, replicate, token, "LABEL_NULL", i))
        perm = rng.permutation(a.shape[1])
        value, _ = same_module_abs_spearman(a[:, perm], b)
        null_values.append(float(value))
    null = np.asarray(null_values, dtype=float)
    null_median = float(np.median(null))
    effect = float(observed - null_median)
    p = float((1 + np.sum(null >= observed)) / (SEMANTIC_NULLS + 1))
    detected = bool((p <= 0.05) and (effect >= 0.10))
    return {
        "semantic_observed": float(observed),
        "semantic_null_median": null_median,
        "delta_semantic": effect,
        "semantic_p_upper": p,
        "semantic_shared_detected": detected,
    }


def _autonomy_stats(source: np.ndarray, target: np.ndarray, scenario: str, replicate: int, token: str) -> dict[str, float | bool]:
    result = predictability_permutation_calibration(
        source,
        target,
        source_modes=5,
        target_modes=5,
        alpha=0.5,
        folds=5,
        permutations=AUTONOMY_NULLS,
        seed=stable_seed(SEED_NAMESPACE, scenario, replicate, token, "AUTONOMY"),
    )
    return {
        "predictability_r2": float(result["observed_cv_modal_r2"]),
        "predictability_null_median": float(result["null_median_cv_modal_r2"]),
        "predictability_excess": float(result["dependence_excess_over_null"]),
        "autonomy": float(result["candidate_autonomy_score"]),
        "predictability_p_upper": float(result["permutation_p_upper"]),
        "predictability_significant": bool(float(result["permutation_p_upper"]) <= 0.05),
    }


def _median_impute(x: np.ndarray) -> np.ndarray:
    a = np.asarray(x, dtype=float).copy()
    for j in range(a.shape[1]):
        finite = np.isfinite(a[:, j])
        if finite.mean() < 0.95:
            raise ValueError("synthetic missingness exceeded frozen 95% feature-completeness floor")
        med = float(np.median(a[finite, j]))
        a[~finite, j] = med
    if not np.isfinite(a).all():
        raise ValueError("median imputation left non-finite values")
    return a


def _base_row(scenario: str, rep: int) -> dict[str, object]:
    return {"scenario": scenario, "replicate": int(rep)}


def _s0(rep: int) -> dict[str, object]:
    rng = _rng("S0_INDEPENDENT", rep)
    n = 80
    zx = rng.normal(size=(n, 3))
    zy = rng.normal(size=(n, 4))
    x = 1.2 * zx @ rng.normal(size=(3, 70)) + 0.7 * rng.normal(size=(n, 70))
    y = 1.2 * zy @ rng.normal(size=(4, 80)) + 0.7 * rng.normal(size=(n, 80))
    row = _base_row("S0_INDEPENDENT", rep)
    row.update(_geometry_stats(x, y, "S0_INDEPENDENT", rep, "RAW"))
    row.update(_autonomy_stats(x, y, "S0_INDEPENDENT", rep, "RAW"))
    return row


def _s1(rep: int) -> dict[str, object]:
    rng = _rng("S1_ONE_SHARED_MODE", rep)
    n = 80
    z = rng.normal(size=(n, 1))
    px = rng.normal(size=(n, 2))
    py = rng.normal(size=(n, 2))
    x = 1.8 * z @ rng.normal(size=(1, 70)) + 0.55 * px @ rng.normal(size=(2, 70)) + 0.7 * rng.normal(size=(n, 70))
    y = 1.8 * z @ rng.normal(size=(1, 80)) + 0.55 * py @ rng.normal(size=(2, 80)) + 0.7 * rng.normal(size=(n, 80))
    row = _base_row("S1_ONE_SHARED_MODE", rep)
    row.update(_geometry_stats(x, y, "S1_ONE_SHARED_MODE", rep, "RAW"))
    pred = cross_validated_modal_predictability(
        x,
        y,
        source_modes=5,
        target_modes=5,
        alpha=0.5,
        folds=5,
        seed=stable_seed(SEED_NAMESPACE, "S1_ONE_SHARED_MODE", rep, "CV"),
    )
    row["predictability_r2"] = float(pred["cv_modal_r2"])
    return row


def _s2(rep: int) -> dict[str, object]:
    rng = _rng("S2_SHARED_PLUS_PRIVATE", rep)
    n = 80
    shared = rng.normal(size=(n, 2))
    px = rng.normal(size=(n, 3))
    py = rng.normal(size=(n, 4))
    x = 1.35 * shared @ rng.normal(size=(2, 70)) + 1.15 * px @ rng.normal(size=(3, 70)) + 0.55 * rng.normal(size=(n, 70))
    y = 1.35 * shared @ rng.normal(size=(2, 80)) + 1.35 * py @ rng.normal(size=(4, 80)) + 0.55 * rng.normal(size=(n, 80))
    row = _base_row("S2_SHARED_PLUS_PRIVATE", rep)
    row.update(_geometry_stats(x, y, "S2_SHARED_PLUS_PRIVATE", rep, "RAW"))
    row.update(_autonomy_stats(x, y, "S2_SHARED_PLUS_PRIVATE", rep, "RAW"))
    row["target_effective_rank"] = float(modal_summary(y).effective_rank)
    return row


def _s3(rep: int) -> dict[str, object]:
    rng = _rng("S3_CONFOUNDER_ONLY", rep)
    n = 80
    c = rng.normal(size=(n, 2))
    px = rng.normal(size=(n, 3))
    py = rng.normal(size=(n, 3))
    x = 2.3 * c @ rng.normal(size=(2, 70)) + 0.8 * px @ rng.normal(size=(3, 70)) + 0.55 * rng.normal(size=(n, 70))
    y = 2.3 * c @ rng.normal(size=(2, 80)) + 0.8 * py @ rng.normal(size=(3, 80)) + 0.55 * rng.normal(size=(n, 80))
    xr = residualize_covariates(x, c)
    yr = residualize_covariates(y, c)
    row = _base_row("S3_CONFOUNDER_ONLY", rep)
    raw = _geometry_stats(x, y, "S3_CONFOUNDER_ONLY", rep, "RAW")
    adj = _geometry_stats(xr, yr, "S3_CONFOUNDER_ONLY", rep, "ADJ")
    row.update(raw)
    row.update({f"adj_{k}": v for k, v in adj.items()})
    row["delta_cka_drop"] = float(raw["delta_cka"] - adj["delta_cka"])
    return row


def _s4(rep: int) -> dict[str, object]:
    rng = _rng("S4_GLOBAL_SHARED_LABEL_SCRAMBLED", rep)
    n = 80
    z = rng.normal(size=(n, 3))
    x = 1.5 * z @ rng.normal(size=(3, 80)) + 0.55 * rng.normal(size=(n, 80))
    y = 1.5 * z @ rng.normal(size=(3, 90)) + 0.55 * rng.normal(size=(n, 90))
    modules = rng.normal(size=(n, 16))
    a_mod = np.roll(modules, 5, axis=1) + 0.25 * rng.normal(size=(n, 16))
    b_mod = modules + 0.25 * rng.normal(size=(n, 16))
    row = _base_row("S4_GLOBAL_SHARED_LABEL_SCRAMBLED", rep)
    row.update(_geometry_stats(x, y, "S4_GLOBAL_SHARED_LABEL_SCRAMBLED", rep, "RAW"))
    row.update(_semantic_stats(a_mod, b_mod, "S4_GLOBAL_SHARED_LABEL_SCRAMBLED", rep, "SEM"))
    return row


def _s5(rep: int) -> dict[str, object]:
    rng = _rng("S5_MODULE_SPECIFIC_WEAK_GLOBAL", rep)
    n = 80
    modules = rng.normal(size=(n, 16))
    a_mod = modules + 0.30 * rng.normal(size=(n, 16))
    b_mod = modules + 0.30 * rng.normal(size=(n, 16))
    # Only a small weak feature subset carries the module signal; the complete
    # assay matrices are dominated by independent high-dimensional structure.
    a_signal = 0.28 * modules[:, :4] @ rng.normal(size=(4, 20))
    b_signal = 0.28 * modules[:, :4] @ rng.normal(size=(4, 20))
    x = np.column_stack([a_signal, rng.normal(size=(n, 380))])
    y = np.column_stack([b_signal, rng.normal(size=(n, 430))])
    row = _base_row("S5_MODULE_SPECIFIC_WEAK_GLOBAL", rep)
    row.update(_geometry_stats(x, y, "S5_MODULE_SPECIFIC_WEAK_GLOBAL", rep, "RAW"))
    row.update(_semantic_stats(a_mod, b_mod, "S5_MODULE_SPECIFIC_WEAK_GLOBAL", rep, "SEM"))
    return row


def _s6(rep: int) -> dict[str, object]:
    rng = _rng("S6_TECHNICAL_FALSE_CONCORDANCE", rep)
    n = 80
    base_x = rng.normal(size=(n, 100))
    base_y = rng.normal(size=(n, 110))
    contam = rng.normal(size=(n, 1))
    contam_x = 7.0 * contam @ rng.normal(size=(1, 8)) + 0.15 * rng.normal(size=(n, 8))
    contam_y = 7.0 * contam @ rng.normal(size=(1, 8)) + 0.15 * rng.normal(size=(n, 8))
    x = np.column_stack([base_x, contam_x])
    y = np.column_stack([base_y, contam_y])
    row = _base_row("S6_TECHNICAL_FALSE_CONCORDANCE", rep)
    raw = _geometry_stats(x, y, "S6_TECHNICAL_FALSE_CONCORDANCE", rep, "RAW")
    masked = _geometry_stats(base_x, base_y, "S6_TECHNICAL_FALSE_CONCORDANCE", rep, "MASKED")
    row.update(raw)
    row.update({f"masked_{k}": v for k, v in masked.items()})
    row["delta_cka_drop"] = float(raw["delta_cka"] - masked["delta_cka"])
    return row


def _s7(rep: int) -> dict[str, object]:
    rng = _rng("S7_FEATURE_IMBALANCE_MISSINGNESS", rep)
    n = 80
    z = rng.normal(size=(n, 3))
    x = 1.3 * z @ rng.normal(size=(3, 70)) + 0.7 * rng.normal(size=(n, 70))
    y = 1.3 * z @ rng.normal(size=(3, 220)) + 0.7 * rng.normal(size=(n, 220))
    complete = _geometry_stats(x, y, "S7_FEATURE_IMBALANCE_MISSINGNESS", rep, "COMPLETE")

    xm = x.copy()
    ym = y.copy()
    miss_x = _rng("S7_FEATURE_IMBALANCE_MISSINGNESS", rep, "MISS_X").random(xm.shape) < 0.04
    miss_y = _rng("S7_FEATURE_IMBALANCE_MISSINGNESS", rep, "MISS_Y").random(ym.shape) < 0.04
    xm[miss_x] = np.nan
    ym[miss_y] = np.nan
    xi = _median_impute(xm)
    yi = _median_impute(ym)
    imputed = _geometry_stats(xi, yi, "S7_FEATURE_IMBALANCE_MISSINGNESS", rep, "IMPUTED")

    row = _base_row("S7_FEATURE_IMBALANCE_MISSINGNESS", rep)
    row.update(complete)
    row.update({f"imputed_{k}": v for k, v in imputed.items()})
    row["abs_delta_cka_change"] = float(abs(complete["delta_cka"] - imputed["delta_cka"]))
    return row


def _s8(rep: int) -> dict[str, object]:
    rng = _rng("S8_NONLINEAR_ONLY", rep)
    n = 120
    z = rng.normal(size=(n, 2))
    nonlinear = z * z
    nonlinear = nonlinear - nonlinear.mean(axis=0, keepdims=True)
    x = 1.4 * z @ rng.normal(size=(2, 90)) + 0.55 * rng.normal(size=(n, 90))
    y = 1.4 * nonlinear @ rng.normal(size=(2, 100)) + 0.55 * rng.normal(size=(n, 100))
    row = _base_row("S8_NONLINEAR_ONLY", rep)
    row.update(_geometry_stats(x, y, "S8_NONLINEAR_ONLY", rep, "RAW"))
    return row


def _s9_s10(rep: int) -> tuple[dict[str, object], dict[str, object]]:
    rng = _rng("S9_S10_PAIRED", rep)
    n = 80
    shared = rng.normal(size=(n, 3))
    private = rng.normal(size=(n, 5))
    source = 1.5 * shared @ rng.normal(size=(3, 70)) + 0.45 * rng.normal(size=(n, 70))
    target_low_autonomy = 1.8 * shared @ rng.normal(size=(3, 75)) + 0.35 * rng.normal(size=(n, 75))
    target_high_autonomy = (
        1.4 * shared @ rng.normal(size=(3, 75))
        + 1.9 * private @ rng.normal(size=(5, 75))
        + 0.35 * rng.normal(size=(n, 75))
    )

    high = _base_row("S9_HIGH_COUPLING_HIGH_AUTONOMY", rep)
    high.update(_geometry_stats(source, target_high_autonomy, "S9_HIGH_COUPLING_HIGH_AUTONOMY", rep, "RAW"))
    high.update(_autonomy_stats(source, target_high_autonomy, "S9_HIGH_COUPLING_HIGH_AUTONOMY", rep, "RAW"))

    low = _base_row("S10_HIGH_COUPLING_LOW_AUTONOMY", rep)
    low.update(_geometry_stats(source, target_low_autonomy, "S10_HIGH_COUPLING_LOW_AUTONOMY", rep, "RAW"))
    low.update(_autonomy_stats(source, target_low_autonomy, "S10_HIGH_COUPLING_LOW_AUTONOMY", rep, "RAW"))
    return high, low


def _s11(rep: int) -> dict[str, object]:
    rng = _rng("S11_CONFOUNDED_FALSE_AUTONOMY_LOSS", rep)
    n = 80
    conf = rng.normal(size=(n, 2))
    private = rng.normal(size=(n, 4))
    source = 2.7 * conf @ rng.normal(size=(2, 70)) + 0.45 * rng.normal(size=(n, 70))
    target = (
        2.7 * conf @ rng.normal(size=(2, 75))
        + 1.15 * private @ rng.normal(size=(4, 75))
        + 0.45 * rng.normal(size=(n, 75))
    )
    sr = residualize_covariates(source, conf)
    tr = residualize_covariates(target, conf)

    row = _base_row("S11_CONFOUNDED_FALSE_AUTONOMY_LOSS", rep)
    raw = _autonomy_stats(source, target, "S11_CONFOUNDED_FALSE_AUTONOMY_LOSS", rep, "RAW")
    adj = _autonomy_stats(sr, tr, "S11_CONFOUNDED_FALSE_AUTONOMY_LOSS", rep, "ADJ")
    row.update(raw)
    row.update({f"adj_{k}": v for k, v in adj.items()})
    row["autonomy_gain_after_adjustment"] = float(adj["autonomy"] - raw["autonomy"])
    row["raw_predictability_exceeds_null"] = bool(raw["predictability_excess"] > 0.0)
    return row


def _rate(rows: list[dict[str, object]], key: str, truth: bool = True) -> float:
    return float(np.mean([bool(r[key]) is truth for r in rows]))


def _median(rows: list[dict[str, object]], key: str) -> float:
    return float(np.median([float(r[key]) for r in rows]))


def _summarize(rows: list[dict[str, object]]) -> tuple[list[dict[str, object]], dict[str, object]]:
    by = defaultdict(list)
    for r in rows:
        by[str(r["scenario"])].append(r)

    summaries: list[dict[str, object]] = []
    behavior_pass: dict[str, bool] = {}

    s0 = by["S0_INDEPENDENT"]
    s0_pass = _rate(s0, "global_shared_detected", False) >= 0.90 and _median(s0, "autonomy") >= 0.85
    behavior_pass["S0"] = bool(s0_pass)
    summaries.append({"behavior": "S0", "pass": s0_pass, "global_nondetection_rate": _rate(s0, "global_shared_detected", False), "median_autonomy": _median(s0, "autonomy")})

    s1 = by["S1_ONE_SHARED_MODE"]
    s1_pass = _rate(s1, "global_shared_detected", True) >= 0.80 and _median(s1, "delta_cka") > 0.0 and _median(s1, "predictability_r2") > _median(s0, "predictability_r2")
    behavior_pass["S1"] = bool(s1_pass)
    summaries.append({"behavior": "S1", "pass": s1_pass, "global_detection_rate": _rate(s1, "global_shared_detected", True), "median_delta_cka": _median(s1, "delta_cka"), "median_predictability_r2": _median(s1, "predictability_r2"), "s0_median_predictability_r2": _median(s0, "predictability_r2")})

    s2 = by["S2_SHARED_PLUS_PRIVATE"]
    s10 = by["S10_HIGH_COUPLING_LOW_AUTONOMY"]
    s2_pass = _rate(s2, "global_shared_detected", True) >= 0.80 and _median(s2, "target_effective_rank") > 2.0 and _median(s2, "autonomy") > _median(s10, "autonomy")
    behavior_pass["S2"] = bool(s2_pass)
    summaries.append({"behavior": "S2", "pass": s2_pass, "global_detection_rate": _rate(s2, "global_shared_detected", True), "median_target_effective_rank": _median(s2, "target_effective_rank"), "median_autonomy": _median(s2, "autonomy"), "s10_median_autonomy": _median(s10, "autonomy")})

    s3 = by["S3_CONFOUNDER_ONLY"]
    s3_pass = _rate(s3, "global_shared_detected", True) >= 0.80 and _rate(s3, "adj_global_shared_detected", False) >= 0.90 and _median(s3, "delta_cka_drop") >= 0.10
    behavior_pass["S3"] = bool(s3_pass)
    summaries.append({"behavior": "S3", "pass": s3_pass, "raw_detection_rate": _rate(s3, "global_shared_detected", True), "adjusted_nondetection_rate": _rate(s3, "adj_global_shared_detected", False), "median_delta_cka_drop": _median(s3, "delta_cka_drop")})

    s4 = by["S4_GLOBAL_SHARED_LABEL_SCRAMBLED"]
    s4_pass = _rate(s4, "global_shared_detected", True) >= 0.80 and _rate(s4, "semantic_shared_detected", False) >= 0.90
    behavior_pass["S4"] = bool(s4_pass)
    summaries.append({"behavior": "S4", "pass": s4_pass, "global_detection_rate": _rate(s4, "global_shared_detected", True), "semantic_nondetection_rate": _rate(s4, "semantic_shared_detected", False), "median_delta_semantic": _median(s4, "delta_semantic")})

    s5 = by["S5_MODULE_SPECIFIC_WEAK_GLOBAL"]
    s5_pass = _rate(s5, "semantic_shared_detected", True) >= 0.80 and _rate(s5, "global_shared_detected", True) <= 0.30
    behavior_pass["S5"] = bool(s5_pass)
    summaries.append({"behavior": "S5", "pass": s5_pass, "semantic_detection_rate": _rate(s5, "semantic_shared_detected", True), "global_detection_rate": _rate(s5, "global_shared_detected", True), "median_delta_semantic": _median(s5, "delta_semantic")})

    s6 = by["S6_TECHNICAL_FALSE_CONCORDANCE"]
    s6_pass = _rate(s6, "global_shared_detected", True) >= 0.80 and _rate(s6, "masked_global_shared_detected", False) >= 0.90 and _median(s6, "delta_cka_drop") >= 0.10
    behavior_pass["S6"] = bool(s6_pass)
    summaries.append({"behavior": "S6", "pass": s6_pass, "raw_detection_rate": _rate(s6, "global_shared_detected", True), "masked_nondetection_rate": _rate(s6, "masked_global_shared_detected", False), "median_delta_cka_drop": _median(s6, "delta_cka_drop")})

    s7 = by["S7_FEATURE_IMBALANCE_MISSINGNESS"]
    s7_pass = _rate(s7, "global_shared_detected", True) >= 0.80 and _rate(s7, "imputed_global_shared_detected", True) >= 0.80 and _median(s7, "abs_delta_cka_change") <= 0.10
    behavior_pass["S7"] = bool(s7_pass)
    summaries.append({"behavior": "S7", "pass": s7_pass, "complete_detection_rate": _rate(s7, "global_shared_detected", True), "imputed_detection_rate": _rate(s7, "imputed_global_shared_detected", True), "median_abs_delta_cka_change": _median(s7, "abs_delta_cka_change")})

    s8 = by["S8_NONLINEAR_ONLY"]
    s8_pass = _rate(s8, "global_shared_detected", True) <= 0.30
    behavior_pass["S8"] = bool(s8_pass)
    summaries.append({"behavior": "S8", "pass": s8_pass, "linear_global_detection_rate": _rate(s8, "global_shared_detected", True), "median_delta_cka": _median(s8, "delta_cka")})

    s9 = by["S9_HIGH_COUPLING_HIGH_AUTONOMY"]
    paired_diffs = []
    paired_wins = []
    for a, b in zip(sorted(s9, key=lambda r: int(r["replicate"])), sorted(s10, key=lambda r: int(r["replicate"]))):
        diff = float(a["autonomy"]) - float(b["autonomy"])
        paired_diffs.append(diff)
        paired_wins.append(diff > 0.0)
    paired_win_rate = float(np.mean(paired_wins))
    median_diff = float(np.median(paired_diffs))
    s9s10_pass = paired_win_rate >= 0.80 and median_diff >= 0.20 and _rate(s9, "global_shared_detected", True) >= 0.80 and _rate(s10, "global_shared_detected", True) >= 0.80
    behavior_pass["S9_S10"] = bool(s9s10_pass)
    summaries.append({"behavior": "S9_S10", "pass": s9s10_pass, "paired_autonomy_win_rate": paired_win_rate, "median_paired_autonomy_difference": median_diff, "s9_global_detection_rate": _rate(s9, "global_shared_detected", True), "s10_global_detection_rate": _rate(s10, "global_shared_detected", True), "s9_median_autonomy": _median(s9, "autonomy"), "s10_median_autonomy": _median(s10, "autonomy")})

    s11 = by["S11_CONFOUNDED_FALSE_AUTONOMY_LOSS"]
    raw_excess_rate = _rate(s11, "raw_predictability_exceeds_null", True)
    adjusted_nonsig_rate = _rate(s11, "adj_predictability_significant", False)
    s11_pass = raw_excess_rate >= 0.80 and _median(s11, "autonomy_gain_after_adjustment") >= 0.20 and adjusted_nonsig_rate >= 0.80
    behavior_pass["S11"] = bool(s11_pass)
    summaries.append({"behavior": "S11", "pass": s11_pass, "raw_predictability_exceeds_null_rate": raw_excess_rate, "median_autonomy_gain_after_adjustment": _median(s11, "autonomy_gain_after_adjustment"), "adjusted_predictability_nonsignificant_rate": adjusted_nonsig_rate})

    safety = {k: behavior_pass[k] for k in ("S0", "S3", "S6", "S11")}
    passes = int(sum(bool(v) for v in behavior_pass.values()))
    safety_pass = bool(all(safety.values()))
    if safety_pass and passes >= 10:
        gate = "F2_GO_CANDIDATE"
    elif safety_pass and 7 <= passes <= 9:
        gate = "F2_NARROW_CANDIDATE"
    else:
        gate = "F2_STOP_SIGNAL"

    summary = {
        "status": gate,
        "plan": "tool_feasibility_plan_v0_1.json",
        "evaluation_freeze": "TOOL_FEASIBILITY_F2_EVALUATION_FREEZE_20260830.md",
        "preresult_repairs": [
            "TOOL_FEASIBILITY_F2_PRERESULT_PROTOCOL_REPAIR_20260830.md",
            "TOOL_FEASIBILITY_F2_PRERESULT_BEHAVIOR_COUNT_REPAIR_20260830.md",
        ],
        "seed_namespace": SEED_NAMESPACE,
        "replicates_per_scenario": N_REPLICATES,
        "global_nulls_per_replicate": GLOBAL_NULLS,
        "semantic_nulls_per_replicate": SEMANTIC_NULLS,
        "autonomy_nulls_per_calibration": AUTONOMY_NULLS,
        "scored_behaviors": len(behavior_pass),
        "behaviors_passed": passes,
        "mandatory_safety": safety,
        "behavior_pass": behavior_pass,
        "c1_beta_value_biology_read": False,
        "biological_chi_used": False,
        "historical_cv2_used": False,
        "claim_ceiling": "synthetic engineering feasibility only; no biomedical association, mechanism, clinical, or C1 result claim",
    }
    return summaries, summary


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    keys = sorted({k for row in rows for k in row.keys()})
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def run(out_dir: Path) -> dict[str, object]:
    rows: list[dict[str, object]] = []
    for rep in range(N_REPLICATES):
        rows.append(_s0(rep))
        rows.append(_s1(rep))
        rows.append(_s2(rep))
        rows.append(_s3(rep))
        rows.append(_s4(rep))
        rows.append(_s5(rep))
        rows.append(_s6(rep))
        rows.append(_s7(rep))
        rows.append(_s8(rep))
        s9, s10 = _s9_s10(rep)
        rows.extend([s9, s10])
        rows.append(_s11(rep))
        print(f"F2 replicate {rep + 1:02d}/{N_REPLICATES} complete", flush=True)

    scenario_summary, summary = _summarize(rows)
    out_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(out_dir / "f2_replicate_metrics.csv", rows)
    _write_csv(out_dir / "f2_scenario_summary.csv", scenario_summary)
    (out_dir / "F2_SUMMARY.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)
    return summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("tool_feasibility_f2_outputs"))
    args = ap.parse_args()
    run(args.out)


if __name__ == "__main__":
    main()
