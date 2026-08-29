from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

import numpy as np


@dataclass(frozen=True)
class ModuleMetrics:
    module: str
    n_samples: int
    n_genes: int
    cin_pairwise_median_abs: float
    cin_pc1_variance_fraction: float
    cout_eigengene_median_abs: float
    median_gene_finite_fraction: float
    pc1_imputed_fraction: float
    cout_background_genes: int
    cout_median_overlap_n: float


def _coverage_valid_columns(
    x: np.ndarray,
    minimum_finite_fraction: float,
    minimum_finite_samples: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Return eligible columns and finite counts under the frozen missingness rule."""
    x = np.asarray(x, dtype=float)
    finite = np.isfinite(x)
    counts = finite.sum(axis=0)
    required = max(int(minimum_finite_samples), int(np.ceil(float(minimum_finite_fraction) * x.shape[0])))
    valid = counts >= required
    with np.errstate(invalid="ignore", divide="ignore"):
        sd = np.nanstd(x, axis=0, ddof=1)
    valid &= np.isfinite(sd) & (sd > 0)
    return valid, counts


def _zscore_columns_mean_impute(
    x: np.ndarray,
    valid: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Z-score finite values and fill missing standardized cells with 0."""
    x = np.asarray(x, dtype=float)
    mean = np.nanmean(x, axis=0)
    sd = np.nanstd(x, axis=0, ddof=1)
    z_nan = np.full_like(x, np.nan, dtype=float)
    z_nan[:, valid] = (x[:, valid] - mean[valid]) / sd[valid]
    z_filled = z_nan.copy()
    z_filled[:, valid] = np.where(np.isfinite(z_filled[:, valid]), z_filled[:, valid], 0.0)
    return z_filled, z_nan, np.isfinite(x)


def _pairwise_complete_corr_matrix(
    x: np.ndarray,
    minimum_overlap_samples: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Exact Pearson correlations using only finite overlap for each gene pair."""
    x = np.asarray(x, dtype=float)
    finite = np.isfinite(x)
    m = finite.astype(float)
    x0 = np.where(finite, x, 0.0)
    x2 = x0 * x0

    n = m.T @ m
    sx = x0.T @ m
    sx2 = x2.T @ m
    sxy = x0.T @ x0

    with np.errstate(invalid="ignore", divide="ignore"):
        sy = sx.T
        cov_num = sxy - (sx * sy) / n
        var_x = sx2 - (sx * sx) / n
        var_y = var_x.T
        denom = np.sqrt(var_x * var_y)
        corr = cov_num / denom

    corr[(n < minimum_overlap_samples) | ~np.isfinite(corr)] = np.nan
    np.fill_diagonal(corr, 1.0)
    return corr, n


def _pairwise_abs_median_complete(x: np.ndarray, minimum_overlap_samples: int) -> float:
    if x.shape[1] < 2:
        return float("nan")
    corr, _ = _pairwise_complete_corr_matrix(x, minimum_overlap_samples)
    iu = np.triu_indices(corr.shape[0], k=1)
    vals = np.abs(corr[iu])
    vals = vals[np.isfinite(vals)]
    return float(np.median(vals)) if len(vals) else float("nan")


def _pc1_eigengene(z_filled: np.ndarray) -> tuple[np.ndarray, float]:
    u, s, _ = np.linalg.svd(z_filled, full_matrices=False)
    eig = u[:, 0] * s[0]
    denom = float(np.sum(s * s))
    frac = float((s[0] * s[0]) / denom) if denom > 0 else float("nan")
    mean_state = np.mean(z_filled, axis=1)
    if np.std(eig, ddof=1) > 0 and np.std(mean_state, ddof=1) > 0:
        if np.corrcoef(eig, mean_state)[0, 1] < 0:
            eig = -eig
    return eig, frac


def _eigengene_outside_correlations(
    eig: np.ndarray,
    outside_x: np.ndarray,
    minimum_overlap_samples: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Pearson correlation of a complete eigengene with partially observed genes."""
    eig = np.asarray(eig, dtype=float)
    outside_x = np.asarray(outside_x, dtype=float)
    finite = np.isfinite(outside_x)
    m = finite.astype(float)
    x0 = np.where(finite, outside_x, 0.0)
    n = m.sum(axis=0)

    se = eig @ m
    sx = x0.sum(axis=0)
    sxe = eig @ x0
    se2 = (eig * eig) @ m
    sx2 = (x0 * x0).sum(axis=0)

    with np.errstate(invalid="ignore", divide="ignore"):
        cov_num = sxe - (se * sx) / n
        var_e = se2 - (se * se) / n
        var_x = sx2 - (sx * sx) / n
        corr = cov_num / np.sqrt(var_e * var_x)
    corr[(n < minimum_overlap_samples) | ~np.isfinite(corr)] = np.nan
    return corr, n


def compute_module_metrics_with_eigengenes(
    expression_samples_by_genes: np.ndarray,
    gene_symbols: Sequence[str],
    modules: Mapping[str, Sequence[str]],
    minimum_mapped_genes: int = 15,
    minimum_gene_finite_fraction: float = 0.95,
    minimum_gene_finite_samples: int = 20,
    minimum_pairwise_overlap_fraction: float = 0.80,
    minimum_pairwise_overlap_samples: int = 20,
) -> tuple[list[ModuleMetrics], dict[str, np.ndarray]]:
    """Compute static organization primitives and oriented module eigengenes.

    Missing-data policy is explicit and deterministic:
    - source non-finite cells remain missing, never zero-expression;
    - genes require >= minimum_gene_finite_fraction finite coverage and a hard
      minimum finite sample count within each cancer;
    - pairwise correlations use only overlapping finite observations;
    - PCA/eigengenes z-score finite values and impute remaining standardized
      missing cells to 0, the within-gene mean in standardized units.

    The outside universe is the supplied gene universe. No chi or composite
    criticality score is produced.
    """
    x = np.asarray(expression_samples_by_genes, dtype=float)
    if x.ndim != 2:
        raise ValueError("expression array must be samples x genes")
    if x.shape[0] < 3:
        raise ValueError("at least three samples are required")
    if x.shape[1] != len(gene_symbols):
        raise ValueError("gene symbol count does not match matrix width")

    valid, finite_counts = _coverage_valid_columns(
        x,
        minimum_finite_fraction=minimum_gene_finite_fraction,
        minimum_finite_samples=minimum_gene_finite_samples,
    )
    z_filled_all, _, finite_mask = _zscore_columns_mean_impute(x, valid)
    symbols = np.asarray([str(s) for s in gene_symbols], dtype=object)
    results: list[ModuleMetrics] = []
    eigengenes: dict[str, np.ndarray] = {}

    pairwise_min_n = max(
        int(minimum_pairwise_overlap_samples),
        int(np.ceil(float(minimum_pairwise_overlap_fraction) * x.shape[0])),
    )

    for module_name in sorted(modules):
        wanted = set(map(str, modules[module_name]))
        in_mask = valid & np.isin(symbols, list(wanted))
        idx = np.flatnonzero(in_mask)
        if len(idx) < minimum_mapped_genes:
            continue

        xin = x[:, idx]
        zin_filled = z_filled_all[:, idx]
        cin_pair = _pairwise_abs_median_complete(xin, pairwise_min_n)
        eig, pc1_frac = _pc1_eigengene(zin_filled)
        eigengenes[str(module_name)] = eig.copy()

        gene_finite_fraction = finite_counts[idx] / float(x.shape[0])
        module_missing = ~finite_mask[:, idx]
        pc1_imputed_fraction = float(module_missing.sum() / module_missing.size) if module_missing.size else 0.0

        outside = np.flatnonzero(valid & ~in_mask)
        if len(outside):
            corr_out, overlap_n = _eigengene_outside_correlations(eig, x[:, outside], pairwise_min_n)
            good = np.isfinite(corr_out)
            cout = float(np.median(np.abs(corr_out[good]))) if np.any(good) else float("nan")
            cout_background_genes = int(np.sum(good))
            cout_median_overlap_n = float(np.median(overlap_n[good])) if np.any(good) else float("nan")
        else:
            cout = float("nan")
            cout_background_genes = 0
            cout_median_overlap_n = float("nan")

        results.append(ModuleMetrics(
            module=str(module_name),
            n_samples=int(x.shape[0]),
            n_genes=int(len(idx)),
            cin_pairwise_median_abs=cin_pair,
            cin_pc1_variance_fraction=pc1_frac,
            cout_eigengene_median_abs=cout,
            median_gene_finite_fraction=float(np.median(gene_finite_fraction)),
            pc1_imputed_fraction=pc1_imputed_fraction,
            cout_background_genes=cout_background_genes,
            cout_median_overlap_n=cout_median_overlap_n,
        ))
    return results, eigengenes


def compute_module_metrics(
    expression_samples_by_genes: np.ndarray,
    gene_symbols: Sequence[str],
    modules: Mapping[str, Sequence[str]],
    minimum_mapped_genes: int = 15,
    **kwargs,
) -> list[ModuleMetrics]:
    return compute_module_metrics_with_eigengenes(
        expression_samples_by_genes,
        gene_symbols,
        modules,
        minimum_mapped_genes,
        **kwargs,
    )[0]
