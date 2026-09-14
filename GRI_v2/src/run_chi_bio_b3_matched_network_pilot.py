from __future__ import annotations

"""Non-promotable matched-network pilot for the frozen B3 scoring layer.

This pilot uses the exact externally frozen regulon geometries and the exact
GSE98812 identifier universe, but never reads a real expression value. Known
low-dimensional regulatory trajectories are projected through the frozen
network, scored with decoupler 2.2.0 ULM, and audited for state/subspace and
transition recovery. The pilot has no pass threshold and cannot select a final
B3 dimension.
"""

from importlib.metadata import version as package_version
from io import BytesIO
import json
from pathlib import Path

import anndata as ad
import decoupler as dc
import numpy as np
import pandas as pd
from scipy import sparse

from src.probe_chi_bio_b3_network_symbol_mapping import (
    DOROTHEA_CONFIDENCE_DENOMINATOR,
    DOROTHEA_LEVELS,
    TMIN,
    _download_collectri,
    _download_dorothea,
    _download_gse,
    _mapped_gene_universe,
    _read_rda,
    _canonicalize_collectri,
    _canonicalize_dorothea,
    _apply_decoupler_220_human_semantics,
)
from src.run_chi_bio_chronic_g2_empirical import _diag, _fit, _loto, _make_transitions


CONFIG = Path("config/gri_Chi_bio_B3_matched_network_pilot_20260913_v0_1.json")
OUTPUT = Path(
    "development_outputs/chi_bio_regulon_source/b3_matched_network_pilot_20260913/"
    "GRI_CHI_BIO_B3_MATCHED_NETWORK_PILOT.json"
)
EXPECTED_DECOUPLER_VERSION = "2.2.0"


def _rng(seed: int, *keys: int) -> np.random.Generator:
    return np.random.default_rng(np.random.SeedSequence([seed, *keys]))


def _prepare_networks() -> tuple[list[str], dict[str, dict]]:
    gse_payload, _ = _download_gse()
    genes, namespace = _mapped_gene_universe(gse_payload)
    gene_set = set(genes)

    c_payload, _ = _download_collectri()
    c_raw = pd.read_csv(BytesIO(c_payload))
    collectri = _canonicalize_collectri(_apply_decoupler_220_human_semantics(c_raw))
    collectri = collectri.loc[collectri["target"].isin(gene_set), ["source", "target", "weight"]].copy()
    collectri["weight"] = pd.to_numeric(collectri["weight"], errors="raise")
    c_counts = collectri.groupby("source")["target"].nunique()
    c_sources = sorted(c_counts[c_counts >= TMIN].index.astype(str).tolist())
    collectri = collectri.loc[collectri["source"].isin(c_sources)].copy()

    d_payload, _ = _download_dorothea()
    dorothea = _canonicalize_dorothea(_read_rda(d_payload))
    dorothea = dorothea.loc[
        dorothea["confidence"].isin(DOROTHEA_LEVELS) & dorothea["target"].isin(gene_set)
    ].copy()
    dorothea["source"] = dorothea["tf"].astype(str)
    dorothea["weight"] = dorothea.apply(
        lambda row: float(row["mor"]) / float(DOROTHEA_CONFIDENCE_DENOMINATOR[str(row["confidence"])]),
        axis=1,
    )
    d_counts = dorothea.groupby("source")["target"].nunique()
    d_sources = sorted(d_counts[d_counts >= TMIN].index.astype(str).tolist())
    dorothea = dorothea.loc[dorothea["source"].isin(d_sources), ["source", "target", "weight"]].copy()

    return genes, {
        "COLLECTRI_PRIMARY": {
            "net": collectri.reset_index(drop=True),
            "sources": c_sources,
            "namespace": namespace,
        },
        "DOROTHEA_ABC_SENSITIVITY": {
            "net": dorothea.reset_index(drop=True),
            "sources": d_sources,
            "namespace": namespace,
        },
    }


def _network_matrix(net: pd.DataFrame, sources: list[str], genes: list[str]) -> sparse.csr_matrix:
    source_index = {name: i for i, name in enumerate(sources)}
    gene_index = {name: i for i, name in enumerate(genes)}
    rows = net["source"].map(source_index).to_numpy(dtype=int)
    cols = net["target"].map(gene_index).to_numpy(dtype=int)
    data = pd.to_numeric(net["weight"], errors="raise").to_numpy(dtype=float)
    w = sparse.coo_matrix((data, (rows, cols)), shape=(len(sources), len(genes))).tocsr()
    norms = np.sqrt(np.asarray(w.multiply(w).sum(axis=1)).ravel())
    if np.any(~np.isfinite(norms)) or np.any(norms <= 0.0):
        raise RuntimeError("eligible network contains zero/nonfinite regulator norm")
    return sparse.diags(1.0 / norms) @ w


def _truth_trajectory(dimension: int, seed: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    rng = _rng(seed, 101, dimension)
    q, _ = np.linalg.qr(rng.normal(size=(dimension, dimension)))
    eigs = np.linspace(0.55, 0.90, dimension)
    transition = q @ np.diag(eigs) @ q.T

    z0 = rng.normal(size=dimension)
    z0 = z0 / np.linalg.norm(z0)
    forcing = rng.normal(size=dimension)
    forcing = 0.35 * forcing / np.linalg.norm(forcing)

    control = [z0.copy()]
    treated = [z0.copy()]
    for _ in range(10):
        control.append(transition @ control[-1])
        treated.append(transition @ treated[-1] + forcing)
    return np.asarray(control), np.asarray(treated), transition, forcing


def _regulator_activity(
    control: np.ndarray,
    treated: np.ndarray,
    regulator_count: int,
    dimension: int,
    seed: int,
    network_code: int,
) -> tuple[np.ndarray, np.ndarray]:
    rng = _rng(seed, 202, network_code, dimension)
    loadings = rng.normal(size=(regulator_count, dimension))
    norms = np.linalg.norm(loadings, axis=1)
    if np.any(norms <= 0.0):
        raise RuntimeError("synthetic regulator loading row has zero norm")
    loadings = loadings / norms[:, None]
    z = np.vstack([control, treated])
    activity = z @ loadings.T
    return activity, loadings


def _synthetic_expression(
    activity: np.ndarray,
    row_normalized_network: sparse.csr_matrix,
    noise_fraction: float,
    seed: int,
    network_code: int,
    dimension: int,
) -> tuple[np.ndarray, float]:
    signal = np.asarray((row_normalized_network.T @ activity.T).T, dtype=float)
    signal_sd = float(np.std(signal))
    if not np.isfinite(signal_sd) or signal_sd <= 0.0:
        raise RuntimeError("synthetic network signal has zero/nonfinite global SD")
    sigma = float(noise_fraction) * signal_sd
    if sigma == 0.0:
        return signal, sigma
    rng = _rng(seed, 303, network_code, dimension, int(round(noise_fraction * 10000)))
    noise = rng.normal(loc=0.0, scale=sigma, size=signal.shape)
    return signal + noise, sigma


def _score(expression: np.ndarray, genes: list[str], net: pd.DataFrame, sources: list[str]) -> np.ndarray:
    adata = ad.AnnData(expression)
    adata.obs_names = [f"state_{i:02d}" for i in range(expression.shape[0])]
    adata.var_names = genes
    dc.mt.ulm(
        data=adata,
        net=net,
        tmin=TMIN,
        tval=True,
        raw=False,
        empty=True,
        verbose=False,
    )
    scores = dc.pp.get_obsm(adata, key="score_ulm")
    frame = pd.DataFrame(
        scores.X,
        index=scores.obs_names.astype(str),
        columns=scores.var_names.astype(str),
    )
    missing = sorted(set(sources) - set(frame.columns))
    extra = sorted(set(frame.columns) - set(sources))
    if missing or extra:
        raise RuntimeError(f"ULM source identity drift; missing={missing[:10]} extra={extra[:10]}")
    arr = frame.loc[:, sources].to_numpy(dtype=float)
    if not np.all(np.isfinite(arr)):
        raise RuntimeError("ULM matched-network pilot produced nonfinite scores")
    return arr


def _correlation_summary(truth_activity: np.ndarray, recovered: np.ndarray) -> dict:
    values: list[float] = []
    for j in range(truth_activity.shape[1]):
        a = truth_activity[:, j]
        b = recovered[:, j]
        if np.std(a) <= 1e-12 or np.std(b) <= 1e-12:
            continue
        corr = float(np.corrcoef(a, b)[0, 1])
        if np.isfinite(corr):
            values.append(corr)
    if not values:
        raise RuntimeError("no finite per-regulator activity correlations")
    arr = np.asarray(values, dtype=float)
    return {
        "finite_regulator_count": int(arr.size),
        "median": float(np.median(arr)),
        "p10": float(np.quantile(arr, 0.10)),
        "p90": float(np.quantile(arr, 0.90)),
        "fraction_gt_0_5": float(np.mean(arr > 0.5)),
        "fraction_gt_0_8": float(np.mean(arr > 0.8)),
        "fraction_negative": float(np.mean(arr < 0.0)),
    }


def _left_subspace(x: np.ndarray, dimension: int) -> np.ndarray:
    centered = x - np.mean(x, axis=0, keepdims=True)
    u, s, _ = np.linalg.svd(centered, full_matrices=False)
    rank = int(np.sum(s > (np.max(s) * max(centered.shape) * np.finfo(float).eps))) if s.size else 0
    if rank < dimension:
        raise RuntimeError(f"matrix rank {rank} < requested subspace dimension {dimension}")
    return u[:, :dimension]


def _subspace_summary(true_state: np.ndarray, recovered_scores: np.ndarray, dimension: int) -> dict:
    q_true = _left_subspace(true_state, dimension)
    q_rec = _left_subspace(recovered_scores, dimension)
    cosines = np.linalg.svd(q_true.T @ q_rec, compute_uv=False)
    cosines = np.clip(cosines, 0.0, 1.0)
    angles = np.degrees(np.arccos(cosines))
    return {
        "canonical_cosines": [float(x) for x in cosines],
        "minimum_canonical_cosine": float(np.min(cosines)),
        "principal_angles_degrees": [float(x) for x in angles],
        "maximum_principal_angle_degrees": float(np.max(angles)),
    }


def _control_only_pca_state(scores: np.ndarray, dimension: int) -> tuple[np.ndarray, dict]:
    control = scores[:11]
    mean = np.mean(control, axis=0, keepdims=True)
    centered_control = control - mean
    _, singular_values, vt = np.linalg.svd(centered_control, full_matrices=False)
    numerical_rank = int(np.linalg.matrix_rank(centered_control))
    if numerical_rank < dimension:
        raise RuntimeError(f"control ULM score rank {numerical_rank} < {dimension}")
    components = vt[:dimension].copy()
    for i in range(dimension):
        pivot = int(np.argmax(np.abs(components[i])))
        if components[i, pivot] < 0.0:
            components[i] *= -1.0
    state = (scores - mean) @ components.T
    return state, {
        "control_centered_rank": numerical_rank,
        "leading_singular_values": [float(x) for x in singular_values[:dimension]],
    }


def _transition_summary(state: np.ndarray, truth_transition: np.ndarray) -> dict:
    control_state = state[:11]
    treated_state = state[11:]
    x0, x1, u, _ = _make_transitions(control_state, treated_state)
    fit = _fit(x0, x1, u, "D1")
    loto = _loto(x0, x1, u, "D1")
    if fit["status"] != "PASS":
        return {
            "status": fit["status"],
            "design_rank": fit.get("design_rank"),
            "design_columns": fit.get("design_columns"),
            "scaled_condition_number": fit.get("scaled_condition_number"),
            "loto": loto,
        }
    recovered_diag = _diag(fit["T"])
    truth_rho = float(np.max(np.abs(np.linalg.eigvals(truth_transition))))
    recovered_rho = float(recovered_diag["rho"])
    relative_error = abs(recovered_rho - truth_rho) / max(abs(truth_rho), np.finfo(float).eps)
    return {
        "status": "PASS",
        "truth_rho": truth_rho,
        "recovered_rho": recovered_rho,
        "relative_rho_error": float(relative_error),
        "recovered_sigma_max": float(recovered_diag["sigma_max"]),
        "design_rank": int(fit["design_rank"]),
        "design_columns": int(fit["design_columns"]),
        "scaled_condition_number": float(fit["scaled_condition_number"]),
        "relative_residual_frobenius": float(fit["relative_residual_frobenius"]),
        "loto_aggregate_nrmse": loto["aggregate_nrmse"],
        "all_loto_refits_admissible": bool(loto["all_refits_admissible"]),
    }


def _truth_transition_geometry(control: np.ndarray, treated: np.ndarray, transition: np.ndarray) -> dict:
    x0, x1, u, _ = _make_transitions(control, treated)
    fit = _fit(x0, x1, u, "D1")
    if fit["status"] != "PASS":
        return {
            "status": fit["status"],
            "design_rank": fit.get("design_rank"),
            "design_columns": fit.get("design_columns"),
        }
    diag = _diag(fit["T"])
    return {
        "status": "PASS",
        "truth_declared_rho": float(np.max(np.abs(np.linalg.eigvals(transition)))),
        "truth_geometry_fitted_rho": float(diag["rho"]),
        "truth_geometry_design_rank": int(fit["design_rank"]),
        "truth_geometry_design_columns": int(fit["design_columns"]),
        "truth_geometry_scaled_condition_number": float(fit["scaled_condition_number"]),
        "truth_geometry_relative_residual_frobenius": float(fit["relative_residual_frobenius"]),
    }


def run_pilot(config: dict) -> dict:
    observed_version = package_version("decoupler")
    if observed_version != EXPECTED_DECOUPLER_VERSION:
        raise RuntimeError(f"decoupler version drift: {observed_version}")
    genes, network_data = _prepare_networks()
    seed = int(config["seed"])
    results: dict[str, dict] = {}

    for network_code, network_name in enumerate(config["network_representations"], start=1):
        entry = network_data[network_name]
        net = entry["net"]
        sources = entry["sources"]
        row_normalized_w = _network_matrix(net, sources, genes)
        network_results: dict[str, dict] = {}

        for dimension in config["candidate_dimensions"]:
            dimension = int(dimension)
            control, treated, transition, _ = _truth_trajectory(dimension, seed)
            true_state = np.vstack([control, treated])
            activity, _ = _regulator_activity(
                control,
                treated,
                len(sources),
                dimension,
                seed,
                network_code,
            )
            truth_geometry = _truth_transition_geometry(control, treated, transition)
            dim_results: dict[str, dict] = {}

            for noise_fraction in config["noise_fraction_of_global_signal_sd"]:
                noise_fraction = float(noise_fraction)
                expression, sigma = _synthetic_expression(
                    activity,
                    row_normalized_w,
                    noise_fraction,
                    seed,
                    network_code,
                    dimension,
                )
                recovered = _score(expression, genes, net, sources)
                state, pca = _control_only_pca_state(recovered, dimension)
                dim_results[f"{noise_fraction:.6g}"] = {
                    "noise_fraction": noise_fraction,
                    "noise_sigma": sigma,
                    "regulator_activity_recovery": _correlation_summary(activity, recovered),
                    "latent_subspace_recovery": _subspace_summary(true_state, recovered, dimension),
                    "control_only_pca": pca,
                    "transition_recovery": _transition_summary(state, transition),
                }

            network_results[str(dimension)] = {
                "dimension": dimension,
                "truth_geometry": truth_geometry,
                "noise_results": dim_results,
            }

        results[network_name] = {
            "eligible_regulator_count": len(sources),
            "eligible_edge_count": int(net.shape[0]),
            "results_by_dimension": network_results,
        }

    return {
        "status": "COMPLETE_B3_MATCHED_NETWORK_NONPROMOTABLE_PILOT",
        "freeze_id": config["freeze_id"],
        "protocol_authority": config["protocol_authority"],
        "decoupler_version": observed_version,
        "mapped_feature_count": len(genes),
        "candidate_dimensions": config["candidate_dimensions"],
        "noise_fraction_of_global_signal_sd": config["noise_fraction_of_global_signal_sd"],
        "results": results,
        "real_expression_opened": False,
        "real_tf_activity_scored": False,
        "dimension_selected": False,
        "operator_promoted": False,
        "normalized_g1_computed": False,
        "chi_bio_computed": False,
        "promotion_effect": config["promotion_effect"],
    }


def main() -> int:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    try:
        report = run_pilot(config)
        rc = 0
    except Exception as exc:
        report = {
            "status": "REFUSE_B3_MATCHED_NETWORK_PILOT_EXECUTION",
            "reason": f"{type(exc).__name__}: {exc}",
            "real_expression_opened": False,
            "chi_bio_computed": False,
            "promotion_effect": "NONE_MECHANICAL_OR_PILOT_FAILURE",
        }
        rc = 2
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
