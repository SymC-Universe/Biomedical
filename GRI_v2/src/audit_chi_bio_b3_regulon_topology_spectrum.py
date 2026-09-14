from __future__ import annotations

"""Outcome-free spectral audit of the frozen B3 regulon geometries.

The current ULM -> control-only PCA B3 construction failed its unseen-seed
matched-network holdout. A lawful materially different branch would need to be
defined by external network structure rather than empirical expression outcomes.
This audit asks whether the exact frozen regulon graphs themselves exhibit a
compact natural regulator-mode structure.

It reads only:
  * exact frozen CollecTRI / DoRothEA network sources;
  * the GSE98812 GENE identifier column for measured-target support.

It never opens expression values, scores TF activity, fits a temporal operator,
selects a final B3 dimension, or computes G1/Chi_bio.
"""

from io import BytesIO
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import sparse

from src.probe_chi_bio_b3_network_gene_overlap import (
    DOROTHEA_CONFIDENCE_DENOMINATOR,
    DOROTHEA_LEVELS,
    TMIN,
    _download_gse,
)
from src.probe_chi_bio_b3_network_symbol_mapping import _mapped_gene_universe
from src.probe_chi_bio_collectri_export import (
    _apply_decoupler_220_human_semantics,
    _canonicalize as _canonicalize_collectri,
    _download_exact_source as _download_collectri,
)
from src.probe_chi_bio_dorothea_export import (
    _canonicalize as _canonicalize_dorothea,
    _download_exact_source as _download_dorothea,
    _read_rda,
)


OUTPUT = Path(
    "development_outputs/chi_bio_regulon_source/b3_topology_spectrum_20260913/"
    "GRI_CHI_BIO_B3_REGULON_TOPOLOGY_SPECTRUM.json"
)
K_REPORT = (1, 2, 3, 4, 5, 10, 20, 50, 100)


def _eligible_networks() -> tuple[list[str], dict[str, pd.DataFrame]]:
    gse_payload, _ = _download_gse()
    genes, _ = _mapped_gene_universe(gse_payload)
    gene_set = set(genes)

    c_payload, _ = _download_collectri()
    c_raw = pd.read_csv(BytesIO(c_payload))
    collectri = _canonicalize_collectri(_apply_decoupler_220_human_semantics(c_raw))
    collectri = collectri.loc[
        collectri["target"].isin(gene_set), ["source", "target", "weight"]
    ].copy()
    collectri["weight"] = pd.to_numeric(collectri["weight"], errors="raise")
    c_counts = collectri.groupby("source")["target"].nunique()
    c_sources = sorted(c_counts[c_counts >= TMIN].index.astype(str).tolist())
    collectri = collectri.loc[collectri["source"].isin(c_sources)].reset_index(drop=True)

    d_payload, _ = _download_dorothea()
    dorothea = _canonicalize_dorothea(_read_rda(d_payload))
    dorothea = dorothea.loc[
        dorothea["confidence"].isin(DOROTHEA_LEVELS)
        & dorothea["target"].isin(gene_set)
    ].copy()
    dorothea["source"] = dorothea["tf"].astype(str)
    dorothea["weight"] = dorothea.apply(
        lambda row: float(row["mor"])
        / float(DOROTHEA_CONFIDENCE_DENOMINATOR[str(row["confidence"])]),
        axis=1,
    )
    d_counts = dorothea.groupby("source")["target"].nunique()
    d_sources = sorted(d_counts[d_counts >= TMIN].index.astype(str).tolist())
    dorothea = dorothea.loc[
        dorothea["source"].isin(d_sources), ["source", "target", "weight"]
    ].reset_index(drop=True)

    return genes, {
        "COLLECTRI_PRIMARY": collectri,
        "DOROTHEA_ABC_SENSITIVITY": dorothea,
    }


def _row_normalized_matrix(
    net: pd.DataFrame,
    genes: list[str],
    *,
    absolute_weights: bool,
) -> tuple[sparse.csr_matrix, list[str]]:
    sources = sorted(net["source"].astype(str).unique().tolist())
    sidx = {name: i for i, name in enumerate(sources)}
    gidx = {name: i for i, name in enumerate(genes)}
    rows = net["source"].map(sidx).to_numpy(dtype=int)
    cols = net["target"].map(gidx).to_numpy(dtype=int)
    data = pd.to_numeric(net["weight"], errors="raise").to_numpy(dtype=float)
    if absolute_weights:
        data = np.abs(data)
    w = sparse.coo_matrix(
        (data, (rows, cols)), shape=(len(sources), len(genes)), dtype=float
    ).tocsr()
    norms = np.sqrt(np.asarray(w.multiply(w).sum(axis=1)).ravel())
    if np.any(~np.isfinite(norms)) or np.any(norms <= 0):
        raise RuntimeError("eligible regulon row has zero/nonfinite norm")
    return sparse.diags(1.0 / norms) @ w, sources


def _spectral_summary(w: sparse.csr_matrix) -> dict:
    gram = np.asarray((w @ w.T).toarray(), dtype=float)
    gram = 0.5 * (gram + gram.T)
    eigvals = np.linalg.eigvalsh(gram)[::-1]
    tiny = max(gram.shape) * np.finfo(float).eps * max(1.0, float(eigvals[0]))
    eigvals[np.abs(eigvals) < tiny] = 0.0
    if np.any(eigvals < -1e-10):
        raise RuntimeError("regulon Gram matrix is materially non-PSD")
    eigvals = np.maximum(eigvals, 0.0)
    total = float(np.sum(eigvals))
    if total <= 0.0:
        raise RuntimeError("regulon Gram spectrum has zero trace")
    p = eigvals / total
    positive = p[p > 0.0]
    effective_rank = float(np.exp(-np.sum(positive * np.log(positive))))
    participation_ratio = float((np.sum(eigvals) ** 2) / np.sum(eigvals**2))
    numerical_rank = int(np.sum(eigvals > tiny))

    cumulative: dict[str, float] = {}
    reconstruction_residual: dict[str, float] = {}
    csum = np.cumsum(eigvals) / total
    for k in K_REPORT:
        if k <= len(eigvals):
            cumulative[str(k)] = float(csum[k - 1])
            reconstruction_residual[str(k)] = float(1.0 - csum[k - 1])

    gaps: list[dict] = []
    max_k = min(20, len(eigvals) - 1)
    for k in range(1, max_k + 1):
        gap = float(eigvals[k - 1] - eigvals[k])
        gaps.append(
            {
                "k": k,
                "lambda_k": float(eigvals[k - 1]),
                "lambda_k_plus_1": float(eigvals[k]),
                "absolute_gap": gap,
                "gap_over_lambda1": float(gap / max(eigvals[0], np.finfo(float).eps)),
                "ratio_lambda_k_to_next": float(
                    eigvals[k - 1] / max(eigvals[k], np.finfo(float).eps)
                ),
            }
        )

    offdiag = gram[np.triu_indices_from(gram, k=1)]
    return {
        "regulator_count": int(gram.shape[0]),
        "numerical_rank": numerical_rank,
        "trace": total,
        "effective_rank_entropy": effective_rank,
        "participation_ratio": participation_ratio,
        "leading_eigenvalues": [float(x) for x in eigvals[: min(25, len(eigvals))]],
        "cumulative_spectral_mass": cumulative,
        "best_rank_k_reconstruction_residual": reconstruction_residual,
        "eigengaps_k1_to_k20": gaps,
        "largest_gap_k1_to_k20": max(gaps, key=lambda x: x["absolute_gap"]),
        "offdiagonal_similarity_quantiles": {
            "min": float(np.min(offdiag)) if offdiag.size else None,
            "p01": float(np.quantile(offdiag, 0.01)) if offdiag.size else None,
            "p10": float(np.quantile(offdiag, 0.10)) if offdiag.size else None,
            "median": float(np.median(offdiag)) if offdiag.size else None,
            "p90": float(np.quantile(offdiag, 0.90)) if offdiag.size else None,
            "p99": float(np.quantile(offdiag, 0.99)) if offdiag.size else None,
            "max": float(np.max(offdiag)) if offdiag.size else None,
            "fraction_abs_lt_1e_12": float(np.mean(np.abs(offdiag) < 1e-12))
            if offdiag.size
            else None,
        },
    }


def run_audit() -> dict:
    genes, networks = _eligible_networks()
    results: dict[str, dict] = {}
    for name, net in networks.items():
        signed_w, signed_sources = _row_normalized_matrix(
            net, genes, absolute_weights=False
        )
        unsigned_w, unsigned_sources = _row_normalized_matrix(
            net, genes, absolute_weights=True
        )
        if signed_sources != unsigned_sources:
            raise RuntimeError("signed/unsigned source-order mismatch")
        source_hash = hashlib.sha256(
            "\n".join(signed_sources).encode("utf-8")
        ).hexdigest()
        results[name] = {
            "eligible_regulator_count": len(signed_sources),
            "eligible_regulator_sha256": source_hash,
            "matched_edge_count": int(net.shape[0]),
            "signed_cosine_gram": _spectral_summary(signed_w),
            "unsigned_support_gram": _spectral_summary(unsigned_w),
        }

    return {
        "status": "COMPLETE_B3_OUTCOME_FREE_REGULON_TOPOLOGY_SPECTRUM_AUDIT",
        "purpose": "Assess whether frozen external regulon topology itself supplies a compact natural mode basis after the ULM-control-PCA B3 holdout refusal.",
        "mapped_feature_count": len(genes),
        "expression_values_opened": False,
        "tf_activity_scored": False,
        "real_state_dimension_selected": False,
        "operator_fit": False,
        "normalized_g1_computed": False,
        "chi_bio_computed": False,
        "results": results,
        "interpretation_rule": "Descriptive topology audit only. No eigengap, cumulative spectral mass, or effective-rank value is prospectively defined as an admission threshold in this audit. Any graph-defined B3 candidate requires a separate pre-outcome candidate freeze and known-truth falsification program.",
        "promotion_effect": "NONE_TOPOLOGY_AUDIT_ONLY",
    }


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    try:
        result = run_audit()
        rc = 0
    except Exception as exc:
        result = {
            "status": "REFUSE_B3_REGULON_TOPOLOGY_SPECTRUM_AUDIT",
            "reason": f"{type(exc).__name__}: {exc}",
            "expression_values_opened": False,
            "chi_bio_computed": False,
            "promotion_effect": "NONE",
        }
        rc = 2
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
