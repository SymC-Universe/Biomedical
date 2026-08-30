from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from src import run_tool_feasibility_f2 as f2


def _fixed_count_missingness(x: np.ndarray, scenario: str, replicate: int, token: str) -> np.ndarray:
    """Place exactly 3 missing cells per 80-sample feature (3.75%).

    This implements the already-frozen S7 condition that missingness remain below
    the 5% per-feature ceiling. The earlier Bernoulli(0.04) generator could
    exceed 5% in individual columns by chance and therefore failed before any F2
    scenario result was emitted.
    """
    a = np.asarray(x, dtype=float).copy()
    if a.shape[0] != 80:
        raise ValueError("S7 repaired generator expects the frozen n=80")
    rng = f2._rng(scenario, replicate, token)
    for j in range(a.shape[1]):
        rows = rng.choice(a.shape[0], size=3, replace=False)
        a[rows, j] = np.nan
    return a


def _s7_repaired(rep: int) -> dict[str, object]:
    scenario = "S7_FEATURE_IMBALANCE_MISSINGNESS"
    rng = f2._rng(scenario, rep)
    n = 80
    z = rng.normal(size=(n, 3))
    x = 1.3 * z @ rng.normal(size=(3, 70)) + 0.7 * rng.normal(size=(n, 70))
    y = 1.3 * z @ rng.normal(size=(3, 220)) + 0.7 * rng.normal(size=(n, 220))
    complete = f2._geometry_stats(x, y, scenario, rep, "COMPLETE")

    xm = _fixed_count_missingness(x, scenario, rep, "MISS_X")
    ym = _fixed_count_missingness(y, scenario, rep, "MISS_Y")
    xi = f2._median_impute(xm)
    yi = f2._median_impute(ym)
    imputed = f2._geometry_stats(xi, yi, scenario, rep, "IMPUTED")

    row = f2._base_row(scenario, rep)
    row.update(complete)
    row.update({f"imputed_{k}": v for k, v in imputed.items()})
    row["abs_delta_cka_change"] = float(abs(complete["delta_cka"] - imputed["delta_cka"]))
    return row


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("tool_feasibility_f2_outputs"))
    args = ap.parse_args()
    f2._s7 = _s7_repaired
    f2.run(args.out)


if __name__ == "__main__":
    main()
