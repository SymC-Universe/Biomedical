from __future__ import annotations

import argparse
import csv
import gzip
import json
import inspect
from collections import defaultdict
from pathlib import Path

import numpy as np

from src.tool_feasibility_kernel import center_columns, stable_seed

AJIVE_INIT_RANKS = [5, 5]
AJIVE_WEDIN_SAMPLES = 100
AJIVE_RAND_SAMPLES = 100
MOFA_FACTORS = 5
MOFA_ITERATIONS = 300


def _load_matrix(path: Path) -> np.ndarray:
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        return np.loadtxt(fh, delimiter=",")


def _energy_fraction(part: np.ndarray | None, total_energy: float) -> float:
    if part is None or total_energy <= 0:
        return 0.0
    return float(np.sum(np.asarray(part, dtype=float) ** 2) / total_energy)


def run_ajive(x: np.ndarray, y: np.ndarray) -> dict[str, float | int | str]:
    if not hasattr(inspect, "getargspec"):
        inspect.getargspec = inspect.getfullargspec  # type: ignore[attr-defined]
    from mvdr.ajive.AJIVE import AJIVE

    model = AJIVE(
        init_signal_ranks=AJIVE_INIT_RANKS,
        center=True,
        check_joint_identif=True,
        n_wedin_samples=AJIVE_WEDIN_SAMPLES,
        n_rand_samples=AJIVE_RAND_SAMPLES,
        n_jobs=1,
    ).fit([x, y])

    joint_rank = 0 if model.common_ is None else int(model.common_.n_components)
    indiv_ranks = [int(model.view_specific_[b].indiv_rank_) for b in range(2)]
    out: dict[str, float | int | str] = {
        "ajive_status": "OK",
        "ajive_joint_rank": joint_rank,
        "ajive_source_indiv_rank": indiv_ranks[0],
        "ajive_target_indiv_rank": indiv_ranks[1],
    }
    for b, (name, data) in enumerate((("source", x), ("target", y))):
        view = model.view_specific_[b]
        total = float(np.sum(center_columns(data) ** 2))
        joint = None if view.joint_ is None else view.joint_.full_
        indiv = None if view.individual_ is None else view.individual_.full_
        noise = view.noise_
        out[f"ajive_{name}_joint_energy_fraction"] = _energy_fraction(joint, total)
        out[f"ajive_{name}_indiv_energy_fraction"] = _energy_fraction(indiv, total)
        out[f"ajive_{name}_noise_energy_fraction"] = _energy_fraction(noise, total)
    return out


def run_mofa(x: np.ndarray, y: np.ndarray, scenario: str, representation: str, replicate: int) -> dict[str, float | int | str]:
    from mofapy2.run.entry_point import entry_point

    ent = entry_point()
    ent.set_data_options(scale_groups=False, scale_views=False)
    ent.set_data_matrix(
        [[np.asarray(x, dtype=float)], [np.asarray(y, dtype=float)]],
        likelihoods=["gaussian", "gaussian"],
        views_names=["SOURCE", "TARGET"],
        groups_names=["ALL"],
    )
    ent.set_model_options(
        factors=MOFA_FACTORS,
        spikeslab_factors=False,
        spikeslab_weights=False,
        ard_factors=False,
        ard_weights=True,
    )
    ent.set_train_options(
        iter=MOFA_ITERATIONS,
        convergence_mode="fast",
        verbose=False,
        quiet=True,
        seed=stable_seed("F3_MOFA2", scenario, representation, replicate),
    )
    ent.build()
    ent.run()

    r2 = np.asarray(ent.model.calculate_variance_explained(total=False)[0], dtype=float)
    if r2.ndim != 2 or r2.shape[0] != 2:
        raise RuntimeError(f"unexpected MOFA2 R2 shape: {r2.shape}")
    rx = np.maximum(r2[0], 0.0)
    ry = np.maximum(r2[1], 0.0)
    shared = float(np.sum(np.minimum(rx, ry)))
    source_private = float(np.sum(np.maximum(rx - ry, 0.0)))
    target_private = float(np.sum(np.maximum(ry - rx, 0.0)))
    denom = shared + source_private + target_private
    jointness = float(shared / denom) if denom > 0 else float("nan")
    out: dict[str, float | int | str] = {
        "mofa_status": "OK",
        "mofa_factor_count_final": int(r2.shape[1]),
        "mofa_shared_r2_mass": shared,
        "mofa_source_private_r2_mass": source_private,
        "mofa_target_private_r2_mass": target_private,
        "mofa_jointness_fraction": jointness,
        "mofa_source_total_factor_r2": float(np.sum(rx)),
        "mofa_target_total_factor_r2": float(np.sum(ry)),
    }
    for k in range(r2.shape[1]):
        out[f"mofa_source_r2_factor_{k+1}"] = float(r2[0, k])
        out[f"mofa_target_r2_factor_{k+1}"] = float(r2[1, k])
    return out


def _aggregate(rows: list[dict[str, object]], prefix: str) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[(str(row["scenario"]), str(row["representation"]))].append(row)
    metric_names = sorted(
        {
            key
            for row in rows
            for key, value in row.items()
            if key.startswith(prefix) and isinstance(value, (int, float)) and not isinstance(value, bool)
        }
    )
    summary: list[dict[str, object]] = []
    for (scenario, representation), group in sorted(grouped.items()):
        rec: dict[str, object] = {"scenario": scenario, "representation": representation, "n": len(group)}
        for metric in metric_names:
            vals = []
            for row in group:
                value = row.get(metric)
                if isinstance(value, (int, float)) and np.isfinite(float(value)):
                    vals.append(float(value))
            if vals:
                rec[f"median_{metric}"] = float(np.median(vals))
                rec[f"q25_{metric}"] = float(np.quantile(vals, 0.25))
                rec[f"q75_{metric}"] = float(np.quantile(vals, 0.75))
        summary.append(rec)
    return summary


def run(inputs: Path, out: Path) -> None:
    manifest = json.loads((inputs / "manifest.json").read_text(encoding="utf-8"))
    rows: list[dict[str, object]] = []
    failures: list[dict[str, object]] = []

    for rec in manifest["records"]:
        scenario = str(rec["scenario"])
        representation = str(rec["representation"])
        replicate = int(rec["replicate"])
        x = _load_matrix(inputs / str(rec["source_file"]))
        y = _load_matrix(inputs / str(rec["target_file"]))
        row: dict[str, object] = {
            "scenario": scenario,
            "representation": representation,
            "replicate": replicate,
        }
        try:
            row.update(run_ajive(x, y))
        except Exception as exc:  # preserved for audit; workflow will fail after writing outputs
            row["ajive_status"] = "ERROR"
            row["ajive_error"] = repr(exc)
            failures.append({"method": "AJIVE", "scenario": scenario, "representation": representation, "replicate": replicate, "error": repr(exc)})
        try:
            row.update(run_mofa(x, y, scenario, representation, replicate))
        except Exception as exc:
            row["mofa_status"] = "ERROR"
            row["mofa_error"] = repr(exc)
            failures.append({"method": "MOFA2", "scenario": scenario, "representation": representation, "replicate": replicate, "error": repr(exc)})
        rows.append(row)
        print(json.dumps({"scenario": scenario, "representation": representation, "replicate": replicate, "ajive": row.get("ajive_status"), "mofa": row.get("mofa_status")}), flush=True)

    out.mkdir(parents=True, exist_ok=True)
    keys = sorted({k for row in rows for k in row})
    with (out / "f3_established_python_replicates.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)

    ajive_summary = _aggregate(rows, "ajive_")
    mofa_summary = _aggregate(rows, "mofa_")
    for name, summary in (("f3_ajive_summary.csv", ajive_summary), ("f3_mofa2_summary.csv", mofa_summary)):
        fields = sorted({k for row in summary for k in row})
        with (out / name).open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fields)
            writer.writeheader()
            writer.writerows(summary)

    payload = {
        "status": "F3_ESTABLISHED_PYTHON_COMPLETE" if not failures else "F3_ESTABLISHED_PYTHON_MECHANICAL_FAILURE",
        "records": len(rows),
        "failures": failures,
        "ajive": {
            "mvdr_commit": "ab04895a04a8f4e1b40e332591c736ba18bf8fd7",
            "ya_pca_commit": "77f633643e9b9e092fe6f62266e21129393d08f7",
            "init_signal_ranks": AJIVE_INIT_RANKS,
            "n_wedin_samples": AJIVE_WEDIN_SAMPLES,
            "n_rand_samples": AJIVE_RAND_SAMPLES,
        },
        "mofa2": {"version": "0.7.5", "factors": MOFA_FACTORS, "iterations": MOFA_ITERATIONS},
        "claim_ceiling": "synthetic established-method comparison only",
        "c1_beta_value_biology_read": False,
        "biological_chi_used": False,
    }
    (out / "F3_ESTABLISHED_PYTHON_SUMMARY.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)
    if failures:
        raise SystemExit(2)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs", type=Path, required=True)
    ap.add_argument("--out", type=Path, default=Path("tool_feasibility_f3_established_python_outputs"))
    args = ap.parse_args()
    run(args.inputs, args.out)


if __name__ == "__main__":
    main()
