from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path

import numpy as np

from src.run_tool_feasibility_f3_simple import (
    _s0,
    _s1,
    _s3,
    _s4,
    _s5,
    _s6,
    _s9_s10,
    _s11,
    _rng,
)

N_REPLICATES = 8


def _s2(rep: int) -> tuple[np.ndarray, np.ndarray]:
    """Exact S2 generator frozen in run_tool_feasibility_f2.py."""
    rng = _rng("S2_SHARED_PLUS_PRIVATE", rep)
    n = 80
    shared = rng.normal(size=(n, 2))
    px = rng.normal(size=(n, 3))
    py = rng.normal(size=(n, 4))
    x = 1.35 * shared @ rng.normal(size=(2, 70)) + 1.15 * px @ rng.normal(size=(3, 70)) + 0.55 * rng.normal(size=(n, 70))
    y = 1.35 * shared @ rng.normal(size=(2, 80)) + 1.35 * py @ rng.normal(size=(4, 80)) + 0.55 * rng.normal(size=(n, 80))
    return x, y


def _write_matrix(path: Path, matrix: np.ndarray) -> None:
    with gzip.open(path, "wt", encoding="utf-8", newline="") as fh:
        np.savetxt(fh, np.asarray(matrix, dtype=float), delimiter=",", fmt="%.17g")


def _add(records: list[dict[str, object]], root: Path, scenario: str, representation: str, rep: int, x: np.ndarray, y: np.ndarray) -> None:
    token = f"{scenario}__{representation}__rep{rep:02d}"
    x_name = f"{token}__SOURCE.csv.gz"
    y_name = f"{token}__TARGET.csv.gz"
    _write_matrix(root / x_name, x)
    _write_matrix(root / y_name, y)
    records.append(
        {
            "token": token,
            "scenario": scenario,
            "representation": representation,
            "replicate": rep,
            "source_file": x_name,
            "target_file": y_name,
            "source_shape": list(x.shape),
            "target_shape": list(y.shape),
        }
    )


def run(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, object]] = []
    for rep in range(N_REPLICATES):
        x, y = _s0(rep)
        _add(records, out, "S0", "raw", rep, x, y)

        x, y = _s1(rep)
        _add(records, out, "S1", "raw", rep, x, y)

        x, y = _s2(rep)
        _add(records, out, "S2", "raw", rep, x, y)

        x, y, xr, yr = _s3(rep)
        _add(records, out, "S3", "raw", rep, x, y)
        _add(records, out, "S3", "adjusted", rep, xr, yr)

        x, y, _, _ = _s4(rep)
        _add(records, out, "S4", "raw", rep, x, y)

        x, y, _, _ = _s5(rep)
        _add(records, out, "S5", "raw", rep, x, y)

        x, y, xm, ym = _s6(rep)
        _add(records, out, "S6", "raw", rep, x, y)
        _add(records, out, "S6", "masked", rep, xm, ym)

        source, high_autonomy, low_autonomy = _s9_s10(rep)
        _add(records, out, "S9", "raw", rep, source, high_autonomy)
        _add(records, out, "S10", "raw", rep, source, low_autonomy)

        source, target, sr, tr = _s11(rep)
        _add(records, out, "S11", "raw", rep, source, target)
        _add(records, out, "S11", "adjusted", rep, sr, tr)

    payload = {
        "status": "F3_ESTABLISHED_INPUTS_EXPORTED",
        "replicates": N_REPLICATES,
        "records": records,
        "source_generator": "same deterministic F2/F3-simple generators",
        "c1_beta_value_biology_read": False,
        "biological_chi_used": False,
    }
    (out / "manifest.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "records": len(records), "replicates": N_REPLICATES}, indent=2), flush=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("tool_feasibility_f3_established_inputs"))
    args = ap.parse_args()
    run(args.out)


if __name__ == "__main__":
    main()
