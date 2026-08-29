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


def _zscore_columns(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    x = np.asarray(x, dtype=float)
    mean = np.nanmean(x, axis=0)
    sd = np.nanstd(x, axis=0, ddof=1)
    valid = np.isfinite(sd) & (sd > 0) & np.isfinite(mean)
    z = np.full_like(x, np.nan, dtype=float)
    z[:, valid] = (x[:, valid] - mean[valid]) / sd[valid]
    return z, valid


def _pairwise_abs_median(z: np.ndarray) -> float:
    if z.shape[1] < 2:
        return float("nan")
    corr = (z.T @ z) / (z.shape[0] - 1)
    iu = np.triu_indices(corr.shape[0], k=1)
    return float(np.median(np.abs(corr[iu])))


def _pc1_eigengene(z: np.ndarray) -> tuple[np.ndarray, float]:
    u, s, _ = np.linalg.svd(z, full_matrices=False)
    eig = u[:, 0] * s[0]
    denom = float(np.sum(s * s))
    frac = float((s[0] * s[0]) / denom) if denom > 0 else float("nan")
    mean_state = np.mean(z, axis=1)
    if np.std(eig, ddof=1) > 0 and np.std(mean_state, ddof=1) > 0:
        if np.corrcoef(eig, mean_state)[0, 1] < 0:
            eig = -eig
    return eig, frac


def compute_module_metrics_with_eigengenes(
    expression_samples_by_genes: np.ndarray,
    gene_symbols: Sequence[str],
    modules: Mapping[str, Sequence[str]],
    minimum_mapped_genes: int = 15,
) -> tuple[list[ModuleMetrics], dict[str, np.ndarray]]:
    """Compute static organization primitives and oriented module eigengenes.

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
    if not np.isfinite(x).all():
        raise ValueError("A1 module metrics currently require a finite matrix after preprocessing")

    z_all, valid = _zscore_columns(x)
    symbols = np.asarray([str(s) for s in gene_symbols], dtype=object)
    results: list[ModuleMetrics] = []
    eigengenes: dict[str, np.ndarray] = {}

    for module_name in sorted(modules):
        wanted = set(map(str, modules[module_name]))
        in_mask = valid & np.isin(symbols, list(wanted))
        idx = np.flatnonzero(in_mask)
        if len(idx) < minimum_mapped_genes:
            continue
        zin = z_all[:, idx]
        cin_pair = _pairwise_abs_median(zin)
        eig, pc1_frac = _pc1_eigengene(zin)
        eigengenes[str(module_name)] = eig.copy()

        eig_z = (eig - eig.mean()) / eig.std(ddof=1)
        outside = np.flatnonzero(valid & ~in_mask)
        if len(outside):
            corr_out = (eig_z[:, None] * z_all[:, outside]).sum(axis=0) / (x.shape[0] - 1)
            cout = float(np.median(np.abs(corr_out)))
        else:
            cout = float("nan")

        results.append(ModuleMetrics(
            module=str(module_name),
            n_samples=int(x.shape[0]),
            n_genes=int(len(idx)),
            cin_pairwise_median_abs=cin_pair,
            cin_pc1_variance_fraction=pc1_frac,
            cout_eigengene_median_abs=cout,
        ))
    return results, eigengenes


def compute_module_metrics(
    expression_samples_by_genes: np.ndarray,
    gene_symbols: Sequence[str],
    modules: Mapping[str, Sequence[str]],
    minimum_mapped_genes: int = 15,
) -> list[ModuleMetrics]:
    return compute_module_metrics_with_eigengenes(
        expression_samples_by_genes,
        gene_symbols,
        modules,
        minimum_mapped_genes,
    )[0]
