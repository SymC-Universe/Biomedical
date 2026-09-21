from __future__ import annotations

import csv
import json
import math
import os
import subprocess
from pathlib import Path
from statistics import mean, median

SOURCE_REPO = "https://github.com/grabuffo/State_Dependent_Brain_Stimulation.git"
SOURCE_COMMIT = "84afcf934c3798b2a40dc8da22d0840e60a4b0f9"

EXPECTED_BLOBS = {
    "README.md": "b1ae47c41ed9b605896f3786dfc9afe836103e03",
    "data/predictability_salience_to_salience.csv": "58e34f8705e30a08954e1c841f13c2e58529634c",
    "data/radius_sensitivity_salience_to_salience.csv": "16e183720a4708523ac29401c2981b73ce4f1707",
    "notebooks/Figure_2_predictability_5MOIs_SEEG.ipynb": "7de8f66f07df557387dcc478ecce03a1d0cdb289",
    "notebooks/Figure_4C-F_prospective_closed_loop_SEEG.ipynb": "952faa934d7fd2a2f3d270fdf954a03d08892d27",
    "notebooks/Figure_5_radius_dependence_SEEG.ipynb": "b4004b2d45651e37d9641a65f178858ad89e48e0",
}


def run(cmd, cwd=None):
    return subprocess.check_output(cmd, cwd=cwd, text=True).strip()


def f(v):
    return float(v)


def main():
    root = Path(os.environ.get("RUNNER_TEMP", "/tmp")) / "state_dependent_brain_stimulation"
    if root.exists():
        subprocess.run(["rm", "-rf", str(root)], check=True)

    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "remote", "add", "origin", SOURCE_REPO], cwd=root, check=True)
    subprocess.run(["git", "fetch", "-q", "--depth", "1", "origin", SOURCE_COMMIT], cwd=root, check=True)
    subprocess.run(["git", "checkout", "-q", "FETCH_HEAD"], cwd=root, check=True)

    head = run(["git", "rev-parse", "HEAD"], cwd=root)
    blob_check = {}
    for path, expected in EXPECTED_BLOBS.items():
        actual = run(["git", "rev-parse", f"HEAD:{path}"], cwd=root)
        blob_check[path] = {"expected": expected, "actual": actual, "match": actual == expected}

    pred_path = root / "data" / "predictability_salience_to_salience.csv"
    with pred_path.open(newline="") as fh:
        pred = list(csv.DictReader(fh))

    r2 = [f(r["r2_cv"]) for r in pred if r["r2_cv"]]
    null = [f(r["null_r2"]) for r in pred if r["null_r2"]]
    subjects = sorted({r["sub"] for r in pred})
    sessions = {(r["sub"], r["run_is"]) for r in pred}

    effect_delta = [a - b for a, b in zip(r2, null)]
    n_positive = sum(x > 0 for x in r2)
    n_above_null = sum(a > b for a, b in zip(r2, null))

    radius_path = root / "data" / "radius_sensitivity_salience_to_salience.csv"
    with radius_path.open(newline="") as fh:
        radius = list(csv.DictReader(fh))

    def row(pre, post):
        matches = [r for r in radius if int(r["radius_pre"]) == pre and int(r["radius_post"]) == post]
        if len(matches) != 1:
            raise RuntimeError(f"Expected one radius row for {pre},{post}; got {len(matches)}")
        return matches[0]

    r55 = row(5, 5)
    r100 = row(100, 100)

    parsed_ok = (
        head == SOURCE_COMMIT
        and all(v["match"] for v in blob_check.values())
        and len(pred) > 0
        and len(radius) > 0
        and len(sessions) == len(pred)
    )

    result = {
        "schema": "GRI_BRAIN_SOURCE_NATIVE_QUALIFICATION_V01",
        "status": "PASS" if parsed_ok else "FAIL",
        "epistemic_class": "SOURCE_NATIVE_REPRODUCTION_QUALIFICATION",
        "scientific_novelty_claim": False,
        "source": {
            "repository": SOURCE_REPO,
            "commit": SOURCE_COMMIT,
            "head_match": head == SOURCE_COMMIT,
            "blob_checks": blob_check,
        },
        "salience_to_salience_derived_data": {
            "n_rows": len(pred),
            "n_subjects": len(subjects),
            "n_sessions": len(sessions),
            "mean_r2_cv": mean(r2),
            "median_r2_cv": median(r2),
            "fraction_r2_cv_positive": n_positive / len(r2),
            "mean_null_r2": mean(null),
            "median_null_r2": median(null),
            "fraction_r2_cv_above_source_null": n_above_null / len(r2),
            "mean_r2_cv_minus_null": mean(effect_delta),
            "median_r2_cv_minus_null": median(effect_delta),
        },
        "radius_sensitivity_source_summary": {
            "radius_5_5": {
                "correlation_mean": f(r55["correlation_mean"]),
                "r_squared_mean": f(r55["r_squared_mean"]),
                "r2_cv_mean": f(r55["r2_cv_mean"]),
            },
            "radius_100_100": {
                "correlation_mean": f(r100["correlation_mean"]),
                "r_squared_mean": f(r100["r_squared_mean"]),
                "r2_cv_mean": f(r100["r2_cv_mean"]),
            },
            "interpretation_ceiling": (
                "The source's derived summary shows strong spatial-radius dependence. "
                "This qualification does not treat radius as a validated capital-Chi coordinate "
                "and does not infer that larger radius is universally superior."
            ),
        },
        "known_source_method_notes": {
            "figure_2": "source notebook uses K=2 shuffled KFold with OLS for cross-metric out-of-sample prediction",
            "closed_loop": "source notebook uses first 50% of trials for threshold learning and held-out second 50% for state-conditioned testing",
            "scalar_chi_status": "NOT_LICENSED",
        },
        "qualification_ceiling": (
            "This run authenticates and summarizes source-native derived evidence only. "
            "It does not test SymC incremental value, a local chi, or a causal capital-Chi mechanism."
        ),
    }

    out = Path("brain_source_qualification_outputs")
    out.mkdir(exist_ok=True)
    (out / "brain_source_native_qualification_v01.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if not parsed_ok:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
