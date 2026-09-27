#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score
from sklearn.preprocessing import StandardScaler

import meneses2026_path_transport_p0q_v01 as base

SEED = 20261027
N_PERM = 1000
OUT = Path(__file__).resolve().parent / "meneses2026_path_signal_diagnostic_results"
OUT.mkdir(parents=True, exist_ok=True)

FEATURES = ["A_dec", "log_tau_dec", "log_tau_inc", "G_rec"]

def feature_matrix(df, names):
    cols = []
    for name in names:
        if name == "A_dec":
            cols.append(df["A_dec"].to_numpy(float))
        elif name == "log_tau_dec":
            cols.append(np.log(df["tau_dec"].to_numpy(float)))
        elif name == "log_tau_inc":
            cols.append(np.log(df["tau_inc"].to_numpy(float)))
        elif name == "G_rec":
            cols.append(df["G_rec"].to_numpy(float))
        else:
            raise KeyError(name)
    return np.column_stack(cols)

def cv_score(df, labels, names):
    X = feature_matrix(df, names)
    conc = df["condition_mM"].to_numpy(int)
    pred = np.empty(len(df), dtype=object)
    folds = []
    for held in base.CONCS:
        tr = conc != held
        te = conc == held
        scaler = StandardScaler()
        xtr = scaler.fit_transform(X[tr])
        xte = scaler.transform(X[te])
        if np.any(~np.isfinite(scaler.scale_)) or np.any(scaler.scale_ <= 0):
            raise RuntimeError(f"zero/nonfinite training scale in fold {held}, features={names}")
        model = LogisticRegression(
            C=1.0, penalty="l2", solver="lbfgs",
            class_weight="balanced", max_iter=2000, random_state=SEED
        )
        model.fit(xtr, labels[tr])
        pp = model.predict(xte)
        pred[te] = pp
        folds.append({
            "heldout_condition_mM": int(held),
            "n_test": int(te.sum()),
            "balanced_accuracy": float(balanced_accuracy_score(labels[te], pp)),
        })
    return float(balanced_accuracy_score(labels, pred)), folds

def perm_test(df, names, seed_offset=0):
    labels = df["path"].to_numpy(object)
    conc = df["condition_mM"].to_numpy(int)
    observed, folds = cv_score(df, labels, names)
    rng = np.random.default_rng(SEED + seed_offset)
    null = np.empty(N_PERM, float)
    for i in range(N_PERM):
        lab = labels.copy()
        for c in base.CONCS:
            idx = np.flatnonzero(conc == c)
            lab[idx] = rng.permutation(lab[idx])
        null[i] = cv_score(df, lab, names)[0]
    q975 = float(np.quantile(null, .975))
    p = float((1 + np.sum(null >= observed)) / (N_PERM + 1))
    return {
        "features": names,
        "observed_balanced_accuracy": observed,
        "null_97_5_percentile": q975,
        "permutation_p_upper_tail": p,
        "detected_at_frozen_97_5_rule": bool(observed > q975),
        "folds": folds,
        "null_mean": float(np.mean(null)),
        "null_sd": float(np.std(null, ddof=1)),
    }

def bh_adjust(pvals):
    p = np.asarray(pvals, float)
    n = len(p)
    order = np.argsort(p)
    ranked = p[order]
    adj = np.empty(n, float)
    running = 1.0
    for i in range(n - 1, -1, -1):
        rank = i + 1
        running = min(running, ranked[i] * n / rank)
        adj[i] = running
    out = np.empty(n, float)
    out[order] = np.clip(adj, 0, 1)
    return out

def main():
    fits, _ = base.extract_all()
    valid = fits[fits["fit_valid"].fillna(False)].copy()
    if len(valid) != 143:
        raise RuntimeError(f"eligible-cell count drift: expected 143, got {len(valid)}")
    valid.to_csv(OUT / "diagnostic_eligible_cells.csv", index=False)

    single = {}
    for i, feat in enumerate(FEATURES):
        single[feat] = perm_test(valid, [feat], seed_offset=100 + i)

    leave_one_out = {}
    for i, omit in enumerate(FEATURES):
        names = [x for x in FEATURES if x != omit]
        leave_one_out[f"without_{omit}"] = perm_test(valid, names, seed_offset=200 + i)

    pairwise = []
    for i, (a, b) in enumerate(combinations(base.PATHS, 2)):
        z = valid[valid["path"].isin([a, b])].copy()
        res = perm_test(z, FEATURES, seed_offset=300 + i)
        res.update({"path_a": a, "path_b": b, "n_cells": int(len(z))})
        pairwise.append(res)

    adj = bh_adjust([r["permutation_p_upper_tail"] for r in pairwise])
    for r, q in zip(pairwise, adj):
        r["bh_adjusted_p_across_six_pairs"] = float(q)

    result = {
        "schema_version": "0.1",
        "experiment_id": "MENESES2026_PATH_SIGNAL_DIAGNOSTIC_V01",
        "status": "EXECUTED_POSTRESULT_ROOT_CAUSE_DIAGNOSTIC",
        "classification": "POST_RESULT_NO_PROMOTION",
        "parent_primary_disposition": "PATH_REORGANIZATION_DETECTED_P0Q",
        "parent_secondary_disposition": "SECONDARY_RULE_UNDERSPECIFIED_FULL_ONLY_LT_0_10",
        "eligible_cells": int(len(valid)),
        "single_coordinate_diagnostics": single,
        "leave_one_coordinate_out_diagnostics": leave_one_out,
        "pairwise_path_diagnostics": pairwise,
        "interpretation_ceiling": "root-cause localization only; cannot alter primary P0-Q or frozen secondary disposition",
    }
    (OUT / "MENESES2026_PATH_SIGNAL_DIAGNOSTIC_V01_RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        fail = {
            "schema_version": "0.1",
            "experiment_id": "MENESES2026_PATH_SIGNAL_DIAGNOSTIC_V01",
            "status": "EXECUTION_FAILURE_PRESERVED",
            "error_type": type(e).__name__,
            "error": str(e),
        }
        (OUT / "MENESES2026_PATH_SIGNAL_DIAGNOSTIC_V01_FAILURE.json").write_text(json.dumps(fail, indent=2) + "\n")
        print(json.dumps(fail, indent=2), file=sys.stderr)
        raise
