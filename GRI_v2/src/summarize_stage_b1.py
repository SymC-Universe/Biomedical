from __future__ import annotations

from pathlib import Path

import pandas as pd

METRICS = ["cin_pairwise_median_abs", "cin_pc1_variance_fraction", "cout_eigengene_median_abs"]


def _q05(s):
    return s.quantile(0.05)


def _q95(s):
    return s.quantile(0.95)


_q05.__name__ = "p05"
_q95.__name__ = "p95"


def spearman(x, y):
    x = pd.Series(x, dtype=float)
    y = pd.Series(y, dtype=float)
    good = x.notna() & y.notna()
    if good.sum() < 3:
        return float("nan")
    return float(x[good].rank().corr(y[good].rank(), method="pearson"))


def summarize(raw_path, out_dir):
    """Summarize a completed Stage B1 raw resample table without recomputation.

    Column access is explicit (``rawg["resample"]``) because DataFrame.resample
    is a pandas method and attribute access would collide with the B1 column
    named ``resample``.
    """
    df = pd.read_csv(raw_path, compression="gzip")
    prefixes = ["baseline__", "actual__", "null__", "actual_delta__", "null_delta__", "context_specific_delta__"]
    value_cols = [c for c in df.columns if any(c.startswith(p) for p in prefixes)]
    agg = df.groupby(["model_id", "cancer_type", "module"], sort=True)[value_cols].agg(["median", _q05, _q95])
    agg.columns = [f"{a}__{b}" for a, b in agg.columns]
    module = agg.reset_index()
    module.to_csv(Path(out_dir) / "stage_b1_module_context_effects.csv", index=False)

    cancer_rows = []
    for (model, cancer), g in module.groupby(["model_id", "cancer_type"], sort=True):
        rawg = df[(df["model_id"] == model) & (df["cancer_type"] == cancer)]
        row = {
            "model_id": model,
            "cancer_type": cancer,
            "module_count": len(g),
            "eligible_n": int(rawg["eligible_n"].iloc[0]),
            "valid_resamples": int(rawg["resample"].nunique()),
        }
        for metric in METRICS:
            b = g[f"baseline__{metric}__median"]
            a = g[f"actual__{metric}__median"]
            row[f"baseline_vs_actual_module_rank_rho__{metric}"] = spearman(b, a)
            row[f"median_actual_delta__{metric}"] = float(g[f"actual_delta__{metric}__median"].median())
            row[f"median_null_delta__{metric}"] = float(g[f"null_delta__{metric}__median"].median())
            row[f"median_context_specific_delta__{metric}"] = float(g[f"context_specific_delta__{metric}__median"].median())
        row["baseline_cin_vs_cout_rho"] = spearman(g["baseline__cin_pairwise_median_abs__median"], g["baseline__cout_eigengene_median_abs__median"])
        row["actual_cin_vs_cout_rho"] = spearman(g["actual__cin_pairwise_median_abs__median"], g["actual__cout_eigengene_median_abs__median"])
        row["baseline_pc1_vs_cout_rho"] = spearman(g["baseline__cin_pc1_variance_fraction__median"], g["baseline__cout_eigengene_median_abs__median"])
        row["actual_pc1_vs_cout_rho"] = spearman(g["actual__cin_pc1_variance_fraction__median"], g["actual__cout_eigengene_median_abs__median"])
        cancer_rows.append(row)

    cancer_df = pd.DataFrame(cancer_rows).sort_values(["model_id", "cancer_type"])
    cancer_df.to_csv(Path(out_dir) / "stage_b1_cancer_level_diagnostic.csv", index=False)
    return df, module, cancer_df
