from __future__ import annotations

from typing import Mapping, Sequence
import numpy as np

from src.module_network import ModuleMetrics


def _coverage_valid_columns(x: np.ndarray, minimum_finite_fraction: float, minimum_finite_samples: int):
    finite = np.isfinite(x)
    counts = finite.sum(axis=0)
    required = max(int(minimum_finite_samples), int(np.ceil(float(minimum_finite_fraction) * x.shape[0])))
    with np.errstate(invalid="ignore", divide="ignore"):
        sd = np.nanstd(x, axis=0, ddof=1)
    valid = (counts >= required) & np.isfinite(sd) & (sd > 0)
    return valid, counts, finite


def _pairwise_complete_corr_matrix(x: np.ndarray, minimum_overlap_samples: int):
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
        corr = cov_num / np.sqrt(var_x * var_x.T)
    corr[(n < minimum_overlap_samples) | ~np.isfinite(corr)] = np.nan
    np.fill_diagonal(corr, 1.0)
    return corr


def _pc1_from_sample_gram(z_filled: np.ndarray):
    # Mathematically equivalent to the left singular vector/value from SVD,
    # but much cheaper for Stage B's fixed n=30 resamples.
    gram = z_filled @ z_filled.T
    eigenvalues, eigenvectors = np.linalg.eigh(gram)
    j = int(np.argmax(eigenvalues))
    lam = max(float(eigenvalues[j]), 0.0)
    eig = eigenvectors[:, j] * np.sqrt(lam)
    denom = float(np.trace(gram))
    frac = float(lam / denom) if denom > 0 else float("nan")
    mean_state = np.mean(z_filled, axis=1)
    if np.std(eig, ddof=1) > 0 and np.std(mean_state, ddof=1) > 0:
        if np.corrcoef(eig, mean_state)[0, 1] < 0:
            eig = -eig
    return eig, frac


def compute_module_metrics_accelerated(
    expression_samples_by_genes: np.ndarray,
    gene_symbols: Sequence[str],
    modules: Mapping[str, Sequence[str]],
    minimum_mapped_genes: int = 15,
    minimum_gene_finite_fraction: float = 0.95,
    minimum_gene_finite_samples: int = 20,
    minimum_pairwise_overlap_fraction: float = 0.80,
    minimum_pairwise_overlap_samples: int = 20,
):
    """Numerically equivalent accelerated implementation of frozen Stage A metrics."""
    x = np.asarray(expression_samples_by_genes, dtype=float)
    if x.ndim != 2 or x.shape[1] != len(gene_symbols):
        raise ValueError("expression matrix or gene symbol dimensions are invalid")
    if x.shape[0] < 3:
        raise ValueError("at least three samples required")

    symbols = np.asarray([str(s) for s in gene_symbols], dtype=object)
    valid, finite_counts, finite = _coverage_valid_columns(
        x, minimum_gene_finite_fraction, minimum_gene_finite_samples
    )
    means = np.nanmean(x, axis=0)
    sds = np.nanstd(x, axis=0, ddof=1)
    z = np.full_like(x, np.nan, dtype=float)
    z[:, valid] = (x[:, valid] - means[valid]) / sds[valid]
    z_filled = z.copy()
    z_filled[:, valid] = np.where(np.isfinite(z_filled[:, valid]), z_filled[:, valid], 0.0)

    min_pair_n = max(
        int(minimum_pairwise_overlap_samples),
        int(np.ceil(float(minimum_pairwise_overlap_fraction) * x.shape[0])),
    )

    symbol_index = {str(g): i for i, g in enumerate(symbols)}
    module_base_idx = {
        name: np.asarray([symbol_index[g] for g in modules[name] if g in symbol_index], dtype=int)
        for name in sorted(modules)
    }

    module_info = []
    eigengenes = []
    for module_name in sorted(modules):
        base_idx = module_base_idx[module_name]
        idx = base_idx[valid[base_idx]]
        if len(idx) < minimum_mapped_genes:
            continue
        corr = _pairwise_complete_corr_matrix(x[:, idx], min_pair_n)
        iu = np.triu_indices(len(idx), k=1)
        pair_vals = np.abs(corr[iu])
        pair_vals = pair_vals[np.isfinite(pair_vals)]
        cin_pair = float(np.median(pair_vals)) if len(pair_vals) else float("nan")
        eig, pc1_frac = _pc1_from_sample_gram(z_filled[:, idx])
        eigengenes.append(eig)
        module_info.append((
            str(module_name), idx, cin_pair, pc1_frac,
            float(np.median(finite_counts[idx] / float(x.shape[0]))),
            float((~finite[:, idx]).sum() / float(x.shape[0] * len(idx))),
        ))

    if not module_info:
        return []

    E = np.column_stack(eigengenes)
    m = finite.astype(float)
    x0 = np.where(finite, x, 0.0)
    n_obs = m.sum(axis=0)
    se = E.T @ m
    sx = x0.sum(axis=0)[None, :]
    sxe = E.T @ x0
    se2 = (E * E).T @ m
    sx2 = (x0 * x0).sum(axis=0)[None, :]
    with np.errstate(invalid="ignore", divide="ignore"):
        cov_num = sxe - (se * sx) / n_obs[None, :]
        var_e = se2 - (se * se) / n_obs[None, :]
        var_x = sx2 - (sx * sx) / n_obs[None, :]
        corr_all = cov_num / np.sqrt(var_e * var_x)
    corr_all[:, n_obs < min_pair_n] = np.nan
    corr_all[~np.isfinite(corr_all)] = np.nan

    results = []
    for k, (module_name, idx, cin_pair, pc1_frac, med_finite, imputed_frac) in enumerate(module_info):
        outside = valid.copy()
        outside[idx] = False
        vals = corr_all[k, outside]
        overlaps = n_obs[outside]
        good = np.isfinite(vals)
        results.append(ModuleMetrics(
            module=module_name,
            n_samples=int(x.shape[0]),
            n_genes=int(len(idx)),
            cin_pairwise_median_abs=cin_pair,
            cin_pc1_variance_fraction=pc1_frac,
            cout_eigengene_median_abs=float(np.median(np.abs(vals[good]))) if np.any(good) else float("nan"),
            median_gene_finite_fraction=med_finite,
            pc1_imputed_fraction=imputed_frac,
            cout_background_genes=int(np.sum(good)),
            cout_median_overlap_n=float(np.median(overlaps[good])) if np.any(good) else float("nan"),
        ))
    return results
