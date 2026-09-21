from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold

SOURCE_REPO = "https://github.com/grabuffo/State_Dependent_Brain_Stimulation.git"
SOURCE_COMMIT = "84afcf934c3798b2a40dc8da22d0840e60a4b0f9"
TRIAL_FILE = "data/SEEG/df_values_5MOIs_ieeg.csv"
TRIAL_BLOB = "6853d1311ab77dd7b4ae71902889c122aebf0a54"
SUMMARY_FILE = "data/predictability_salience_to_salience.csv"
SUMMARY_BLOB = "58e34f8705e30a08954e1c841f13c2e58529634c"


def run(cmd, cwd=None):
    return subprocess.check_output(cmd, cwd=cwd, text=True).strip()


def cv_r2(pre_vals, post_vals):
    pre_vals = np.asarray(pre_vals, dtype=float).reshape(-1)
    post_vals = np.asarray(post_vals, dtype=float).reshape(-1)
    mask = np.isfinite(pre_vals) & np.isfinite(post_vals)
    x = pre_vals[mask]
    y = post_vals[mask]
    if len(x) < 3:
        return None
    scores = []
    kf = KFold(n_splits=2, shuffle=True, random_state=42)
    for train, test in kf.split(x):
        model = LinearRegression()
        model.fit(x[train].reshape(-1, 1), y[train])
        pred = model.predict(x[test].reshape(-1, 1))
        ss_res = float(np.sum((y[test] - pred) ** 2))
        ss_tot = float(np.sum((y[test] - np.mean(y[test])) ** 2))
        scores.append(float(1.0 - ss_res / ss_tot) if ss_tot != 0 else float("nan"))
    return float(np.mean(scores))


def main():
    root = Path(os.environ.get("RUNNER_TEMP", "/tmp")) / "brain_trial_reproduction"
    if root.exists():
        subprocess.run(["rm", "-rf", str(root)], check=True)
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "remote", "add", "origin", SOURCE_REPO], cwd=root, check=True)
    subprocess.run(["git", "fetch", "-q", "--depth", "1", "origin", SOURCE_COMMIT], cwd=root, check=True)
    subprocess.run(["git", "checkout", "-q", "FETCH_HEAD"], cwd=root, check=True)

    head = run(["git", "rev-parse", "HEAD"], cwd=root)
    trial_blob = run(["git", "rev-parse", f"HEAD:{TRIAL_FILE}"], cwd=root)
    summary_blob = run(["git", "rev-parse", f"HEAD:{SUMMARY_FILE}"], cwd=root)

    df = pd.read_csv(root / TRIAL_FILE)
    summary = pd.read_csv(root / SUMMARY_FILE)

    required = {
        "sub", "run_is", "trial_id", "metric_name",
        "metric_value_pre", "metric_value_post",
        "radius_pre", "radius_post",
    }
    missing = sorted(required - set(df.columns))

    result = {
        "schema": "GRI_BRAIN_SOURCE_NATIVE_TRIAL_REPRODUCTION_PREFLIGHT_V01",
        "source_commit_match": head == SOURCE_COMMIT,
        "trial_blob_match": trial_blob == TRIAL_BLOB,
        "summary_blob_match": summary_blob == SUMMARY_BLOB,
        "trial_shape": [int(df.shape[0]), int(df.shape[1])],
        "trial_columns": list(map(str, df.columns)),
        "required_columns_missing": missing,
        "summary_shape": [int(summary.shape[0]), int(summary.shape[1])],
        "source_native_filter": {
            "metric": "salience",
            "radius_pre": 100,
            "radius_post": 100,
            "cv": "KFold(n_splits=2, shuffle=True, random_state=42) + OLS",
        },
        "scientific_novelty_claim": False,
    }

    if missing:
        result["status"] = "PREFLIGHT_ONLY_SCHEMA_INCOMPATIBLE"
        result["reproduction_status"] = "NOT_RUN"
    else:
        filt = df[
            (df["metric_name"].astype(str) == "salience")
            & (df["radius_pre"] == 100)
            & (df["radius_post"] == 100)
        ].copy()

        records = []
        for (sub, run_id), g in filt.groupby(["sub", "run_is"], sort=True):
            per_trial = g.groupby("trial_id", as_index=False).agg(
                metric_value_pre=("metric_value_pre", "mean"),
                metric_value_post=("metric_value_post", "mean"),
            )
            score = cv_r2(per_trial["metric_value_pre"], per_trial["metric_value_post"])
            if score is not None:
                records.append({
                    "sub": str(sub),
                    "run_is": str(run_id),
                    "r2_cv_reproduced": score,
                    "n_trials": int(len(per_trial)),
                })

        rep = pd.DataFrame(records)
        keys = {"sub", "run_is"}
        summary_cols = set(summary.columns)
        can_join = keys.issubset(summary_cols) and "r2_cv" in summary_cols

        result["filtered_rows"] = int(len(filt))
        result["reproduced_sessions"] = int(len(rep))
        result["reproduced_subjects"] = int(rep["sub"].nunique()) if len(rep) else 0
        result["reproduced_mean_r2_cv"] = float(rep["r2_cv_reproduced"].mean()) if len(rep) else None
        result["reproduced_median_r2_cv"] = float(rep["r2_cv_reproduced"].median()) if len(rep) else None
        result["can_join_to_source_summary"] = bool(can_join)

        if can_join and len(rep):
            cmp = rep.merge(summary[["sub", "run_is", "r2_cv"]], on=["sub", "run_is"], how="inner")
            cmp["abs_diff"] = (cmp["r2_cv_reproduced"] - cmp["r2_cv"]).abs()
            result["joined_sessions"] = int(len(cmp))
            result["max_abs_r2_difference_vs_source_summary"] = (
                float(cmp["abs_diff"].max()) if len(cmp) else None
            )
            result["median_abs_r2_difference_vs_source_summary"] = (
                float(cmp["abs_diff"].median()) if len(cmp) else None
            )
            exact = bool(
                len(cmp) == len(summary)
                and len(cmp) == len(rep)
                and float(cmp["abs_diff"].max()) <= 1e-10
            ) if len(cmp) else False
            result["exact_source_summary_reproduction"] = exact
            result["status"] = "PASS_EXACT_SOURCE_NATIVE_REPRODUCTION" if exact else "PASS_COMPUTATION_NONIDENTICAL_SOURCE_SUMMARY"
        else:
            result["status"] = "PASS_SOURCE_NATIVE_RECOMPUTATION_NO_DIRECT_SUMMARY_JOIN"

        result["reproduction_status"] = "COMPLETE"

    result["interpretation_ceiling"] = (
        "Reproduction of the source-native Salience-to-Salience predictor only. "
        "No scalar chi is licensed and no SymC incremental-value claim is tested."
    )

    out = Path("brain_source_qualification_outputs")
    out.mkdir(exist_ok=True)
    (out / "brain_salience_source_native_reproduction_v01.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
