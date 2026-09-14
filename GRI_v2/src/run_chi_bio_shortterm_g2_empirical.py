from __future__ import annotations

"""Outcome-bearing SCC25 short-term G2 pilot under the frozen D-L design.

This runner is intentionally narrow. It opens only the hash-bound GSE114446
processed bulk-RNA count table, applies the prospectively frozen short-term
state construction, evaluates D1, and evaluates D2 only through the frozen
escalation gate. It does not compute or admit biological Chi.
"""

import argparse
from io import BytesIO
import gzip
import hashlib
import json
from pathlib import Path
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd

from src.chi_bio_empirical_freeze_contract import validate_empirical_freeze


SOURCE_URL = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE114nnn/GSE114446/suppl/GSE114446_STCCountsCG.txt.gz"
DEFAULT_FREEZE = Path("config/gri_Chi_bio_shortterm_g2_r1_A3_empirical_freeze_20260913_v1.json")
DEFAULT_COLUMN_MAP = Path("config/gri_hnscc_shortterm_bulk_rna_column_map_p0d_v0_1.json")
EXPECTED_ROWS = 56_470
EXPECTED_SAMPLE_COLUMNS = 33
FLOAT_EPS = float(np.finfo(np.float64).eps)
COND_CEILING = 67_108_864.0
COMPARE_MULTIPLIER = 32.0


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _hash_strings(values: list[str]) -> str:
    payload = ("\n".join(values) + "\n").encode("utf-8")
    return _sha256_bytes(payload)


def _download_source(attempts: int = 4) -> tuple[bytes, list[dict]]:
    history: list[dict] = []
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        request = Request(SOURCE_URL, headers={"User-Agent": "GRI-Chi-bio-shortterm-G2/1.0"})
        try:
            with urlopen(request, timeout=120) as response:
                payload = response.read()
                status = int(getattr(response, "status", response.getcode()))
            history.append({"attempt": attempt, "status_code": status, "bytes_received": len(payload)})
            if status == 200 and payload:
                return payload, history
            last_error = RuntimeError(f"unexpected HTTP {status} or empty payload")
        except (HTTPError, URLError, TimeoutError) as exc:
            history.append({"attempt": attempt, "error": f"{type(exc).__name__}: {exc}"})
            last_error = exc
        if attempt < attempts:
            time.sleep((2, 5, 10)[min(attempt - 1, 2)])
    raise RuntimeError(f"frozen GSE114446 source unavailable after {attempts} attempts: {last_error}")


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _extract_scc25_columns(column_map: dict) -> tuple[list[str], list[str]]:
    rows = [x for x in column_map["columns"] if x["cell_line"] == "SCC25"]
    pbs = sorted((x for x in rows if x["treatment"] == "PBS"), key=lambda x: int(x["day"]))
    ctx = sorted((x for x in rows if x["treatment"] == "CTX"), key=lambda x: int(x["day"]))
    if [int(x["day"]) for x in pbs] != [0, 1, 2, 3, 4, 5]:
        raise RuntimeError("frozen SCC25 PBS day identity is not exactly day 0-5")
    if [int(x["day"]) for x in ctx] != [1, 2, 3, 4, 5]:
        raise RuntimeError("frozen SCC25 CTX day identity is not exactly day 1-5")
    return [x["column"] for x in pbs], [x["column"] for x in ctx]


def _open_frozen_source(payload: bytes, freeze: dict, column_map: dict) -> dict:
    observed_sha = _sha256_bytes(payload)
    expected_sha = freeze["source_binding"]["processed_file_sha256"]
    if observed_sha != expected_sha:
        raise RuntimeError(f"source hash mismatch: {observed_sha} != {expected_sha}")

    raw = gzip.decompress(payload)
    first_line = raw.splitlines()[0].decode("utf-8-sig")
    header = first_line.split("\t")
    if len(header) != EXPECTED_SAMPLE_COLUMNS + 1 or len(set(header)) != len(header):
        raise RuntimeError("processed table header geometry or uniqueness mismatch")

    mapped_columns = [str(x["column"]) for x in column_map["columns"]]
    if len(mapped_columns) != EXPECTED_SAMPLE_COLUMNS or len(set(mapped_columns)) != EXPECTED_SAMPLE_COLUMNS:
        raise RuntimeError("frozen column map does not contain exactly 33 unique sample columns")
    if set(header[1:]) != set(mapped_columns):
        raise RuntimeError("processed sample-column set does not exactly match the frozen map")

    frame = pd.read_csv(BytesIO(raw), sep="\t", low_memory=False)
    if frame.shape != (EXPECTED_ROWS, EXPECTED_SAMPLE_COLUMNS + 1):
        raise RuntimeError(f"processed table shape mismatch: {frame.shape}")

    gene_ids = frame.iloc[:, 0].astype(str).str.strip()
    if gene_ids.eq("").any() or gene_ids.eq("nan").any() or gene_ids.duplicated().any():
        raise RuntimeError("source gene identifiers are missing or duplicated; frozen rule requires refusal")

    pbs_cols, ctx_cols = _extract_scc25_columns(column_map)
    ordered_cols = pbs_cols + ctx_cols
    counts = frame.loc[:, ordered_cols].apply(pd.to_numeric, errors="raise").to_numpy(dtype=np.float64)
    if not np.all(np.isfinite(counts)) or np.any(counts < 0.0):
        raise RuntimeError("SCC25 source counts must be finite and nonnegative")

    library_totals = np.sum(counts, axis=0)
    if not np.all(np.isfinite(library_totals)) or np.any(library_totals <= 0.0):
        raise RuntimeError("SCC25 library totals must be finite and positive")

    cpm = counts * (1_000_000.0 / library_totals.reshape(1, -1))
    keep = np.sum(cpm[:, :6] >= 1.0, axis=1) >= 3
    if int(np.sum(keep)) < 4:
        raise RuntimeError("frozen PBS-only detectability gate retained fewer than four genes")

    retained_ids = gene_ids.to_numpy(dtype=str)[keep].tolist()
    transformed = np.log2(cpm[keep, :] + 1.0).T
    pbs = transformed[:6, :]
    ctx = transformed[6:, :]
    return {
        "pbs": pbs,
        "ctx": ctx,
        "gene_rows_total": int(frame.shape[0]),
        "retained_gene_count": int(np.sum(keep)),
        "retained_gene_ids_sha256": _hash_strings(retained_ids),
        "library_totals": [float(x) for x in library_totals],
        "source_sha256": observed_sha,
        "source_compressed_bytes": len(payload),
        "source_uncompressed_bytes": len(raw),
        "pbs_columns": pbs_cols,
        "ctx_columns": ctx_cols,
    }


def _fit_basis(pbs: np.ndarray, rank: int) -> dict:
    mean = np.mean(pbs, axis=0)
    centered = pbs - mean
    _, singular_values, vt = np.linalg.svd(centered, full_matrices=False)
    numerical_rank = int(np.linalg.matrix_rank(centered))
    if rank > numerical_rank:
        raise RuntimeError(f"rank {rank} exceeds PBS-centered numerical rank {numerical_rank}")
    return {
        "mean": mean,
        "components": vt[:rank].copy(),
        "singular_values": singular_values[:rank].copy(),
        "numerical_rank": numerical_rank,
    }


def _project(basis: dict, x: np.ndarray) -> np.ndarray:
    return (x - basis["mean"]) @ basis["components"].T


def _make_transitions(pbs_state: np.ndarray, ctx_state: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    if pbs_state.shape[0] != 6 or ctx_state.shape[0] != 5:
        raise RuntimeError("short-term state geometry must be 6 PBS + 5 CTX states")
    pbs_now = pbs_state[:-1]
    pbs_next = pbs_state[1:]
    ctx_sequence = np.vstack([pbs_state[0:1], ctx_state])
    ctx_now = ctx_sequence[:-1]
    ctx_next = ctx_sequence[1:]
    x0 = np.vstack([pbs_now, ctx_now])
    x1 = np.vstack([pbs_next, ctx_next])
    u = np.vstack([np.zeros((5, 1)), np.ones((5, 1))])
    arm = np.array([0] * 5 + [1] * 5, dtype=int)
    return x0, x1, u, arm


def _design(x0: np.ndarray, u: np.ndarray, model: str) -> np.ndarray:
    if model == "D1":
        return np.hstack([x0, u, np.ones((x0.shape[0], 1))])
    if model == "D2":
        return np.hstack([x0, x0 * u, u, np.ones((x0.shape[0], 1))])
    raise ValueError(model)


def _scaled_condition(design: np.ndarray) -> tuple[float, str]:
    norms = np.linalg.norm(design, axis=0)
    if np.any(~np.isfinite(norms)) or np.any(norms == 0.0):
        return float("inf"), "REFUSE_ILL_CONDITIONED_DESIGN"
    scaled = design / norms
    s = np.linalg.svd(scaled, compute_uv=False)
    if np.any(~np.isfinite(s)) or float(s[-1]) <= 0.0:
        return float("inf"), "REFUSE_ILL_CONDITIONED_DESIGN"
    cond = float(s[0] / s[-1])
    if not np.isfinite(cond) or cond > COND_CEILING:
        return cond, "REFUSE_ILL_CONDITIONED_DESIGN"
    return cond, "PASS"


def _fit(x0: np.ndarray, x1: np.ndarray, u: np.ndarray, model: str) -> dict:
    design = _design(x0, u, model)
    columns = int(design.shape[1])
    rank = int(np.linalg.matrix_rank(design))
    cond, cond_status = _scaled_condition(design)
    if rank < columns:
        return {"status": "REFUSE_RANK_DEFICIENT_DESIGN", "design_rank": rank, "design_columns": columns, "scaled_condition_number": cond}
    if cond_status != "PASS":
        return {"status": cond_status, "design_rank": rank, "design_columns": columns, "scaled_condition_number": cond}

    coef, *_ = np.linalg.lstsq(design, x1, rcond=None)
    pred = design @ coef
    residual = float(np.linalg.norm(x1 - pred))
    denom = float(np.linalg.norm(x1))
    result = {
        "status": "PASS",
        "design_rank": rank,
        "design_columns": columns,
        "scaled_condition_number": cond,
        "residual_frobenius": residual,
        "relative_residual_frobenius": residual / denom if denom > 0.0 else (0.0 if residual == 0.0 else float("inf")),
        "coef": coef,
    }
    d = x0.shape[1]
    if model == "D1":
        result["T"] = coef[:d, :].T
        result["B"] = coef[d : d + 1, :].T
        result["c"] = coef[d + 1, :].copy()
    else:
        result["T_control"] = coef[:d, :].T
        delta = coef[d : 2 * d, :].T
        result["DeltaT"] = delta
        result["T_treated"] = result["T_control"] + delta
        result["B"] = coef[2 * d : 2 * d + 1, :].T
        result["c"] = coef[2 * d + 1, :].copy()
    return result


def _predict(fit: dict, x: np.ndarray, u: float, model: str) -> np.ndarray:
    if model == "D1":
        return fit["T"] @ x + fit["B"][:, 0] * u + fit["c"]
    return fit["T_control"] @ x + (fit["DeltaT"] @ x) * u + fit["B"][:, 0] * u + fit["c"]


def _diag(t: np.ndarray) -> dict:
    eig = np.linalg.eigvals(t)
    rho = float(np.max(np.abs(eig)))
    sigma = float(np.linalg.svd(t, compute_uv=False)[0])
    return {"rho": rho, "sigma_max": sigma, "nonnormal_warning": bool(rho < 1.0 and sigma > 1.0)}


def _relative_error(y: np.ndarray, pred: np.ndarray) -> float:
    num = float(np.linalg.norm(y - pred))
    den = float(np.linalg.norm(y))
    return num / den if den > 0.0 else (0.0 if num == 0.0 else float("inf"))


def _aggregate_nrmse(targets: list[np.ndarray], preds: list[np.ndarray]) -> float:
    numer = sum(float(np.dot(y - p, y - p)) for y, p in zip(targets, preds))
    denom = sum(float(np.dot(y, y)) for y in targets)
    return float(np.sqrt(numer / denom)) if denom > 0.0 else (0.0 if numer == 0.0 else float("inf"))


def _loto(x0: np.ndarray, x1: np.ndarray, u: np.ndarray, model: str) -> dict:
    records: list[dict] = []
    targets: list[np.ndarray] = []
    preds: list[np.ndarray] = []
    for omit in range(x0.shape[0]):
        keep = np.ones(x0.shape[0], dtype=bool)
        keep[omit] = False
        fit = _fit(x0[keep], x1[keep], u[keep], model)
        row = {k: v for k, v in fit.items() if k not in {"coef", "T", "B", "c", "T_control", "DeltaT", "T_treated"}}
        row["omitted_index"] = omit
        if fit["status"] == "PASS":
            pred = _predict(fit, x0[omit], float(u[omit, 0]), model)
            row["relative_prediction_error"] = _relative_error(x1[omit], pred)
            if model == "D1":
                row["operator"] = _diag(fit["T"])
            else:
                row["control_operator"] = _diag(fit["T_control"])
                row["treated_operator"] = _diag(fit["T_treated"])
            targets.append(x1[omit])
            preds.append(pred)
        records.append(row)
    all_pass = len(targets) == x0.shape[0]
    return {
        "all_refits_admissible": all_pass,
        "aggregate_nrmse": _aggregate_nrmse(targets, preds) if all_pass else None,
        "records": records,
    }


def _baseline_errors(x0: np.ndarray, x1: np.ndarray, arm: np.ndarray) -> dict:
    persistence = [x.copy() for x in x0]
    arm_mean: list[np.ndarray] = []
    for omit in range(x0.shape[0]):
        peers = (arm == arm[omit]) & (np.arange(x0.shape[0]) != omit)
        arm_mean.append(np.mean(x1[peers], axis=0))
    targets = [x1[i] for i in range(x1.shape[0])]
    return {
        "persistence_nrmse": _aggregate_nrmse(targets, persistence),
        "arm_specific_loto_mean_next_state_nrmse": _aggregate_nrmse(targets, arm_mean),
    }


def _strictly_better(candidate: float, comparator: float) -> bool:
    tol = COMPARE_MULTIPLIER * FLOAT_EPS * max(1.0, abs(float(comparator)))
    return float(candidate) < float(comparator) - tol


def _unit_side(values: list[float], all_admissible: bool) -> str:
    if not all_admissible or not values:
        return "INDETERMINATE"
    below = True
    above = True
    for value in values:
        tol = COMPARE_MULTIPLIER * FLOAT_EPS * max(1.0, abs(float(value)))
        below = below and float(value) < 1.0 - tol
        above = above and float(value) > 1.0 + tol
    if below:
        return "BELOW"
    if above:
        return "ABOVE"
    return "INDETERMINATE"


def _warning_disposition(values: list[bool], all_admissible: bool) -> str:
    if not all_admissible or not values:
        return "INDETERMINATE"
    if all(values):
        return "PRESENT"
    if not any(values):
        return "ABSENT"
    return "INDETERMINATE"


def _point_record(fit: dict, model: str) -> dict:
    row = {k: v for k, v in fit.items() if k not in {"coef", "T", "B", "c", "T_control", "DeltaT", "T_treated"}}
    if fit["status"] == "PASS":
        if model == "D1":
            row["operator"] = _diag(fit["T"])
        else:
            row["control_operator"] = _diag(fit["T_control"])
            row["treated_operator"] = _diag(fit["T_treated"])
            row["delta_transition_frobenius"] = float(np.linalg.norm(fit["DeltaT"]))
    return row


def _d1_sensitivity(pbs: np.ndarray, ctx: np.ndarray, rank: int, main_loto: dict, main_fit: dict) -> dict:
    rho_values: list[float] = []
    warning_values: list[bool] = []
    failures: list[str] = []
    if main_fit["status"] == "PASS":
        d = _diag(main_fit["T"])
        rho_values.append(d["rho"])
        warning_values.append(d["nonnormal_warning"])
    else:
        failures.append("POINT_FIT")
    for record in main_loto["records"]:
        if record["status"] == "PASS":
            rho_values.append(float(record["operator"]["rho"]))
            warning_values.append(bool(record["operator"]["nonnormal_warning"]))
        else:
            failures.append(f"LOTO_{record['omitted_index']}")

    basis = _fit_basis(pbs, rank)
    ps = _project(basis, pbs)
    cs = _project(basis, ctx)
    x0, x1, u, _ = _make_transitions(ps, cs)
    keep = np.ones(10, dtype=bool)
    keep[[0, 5]] = False
    block = _fit(x0[keep], x1[keep], u[keep], "D1")
    block_record = _point_record(block, "D1")
    if block["status"] == "PASS":
        d = _diag(block["T"])
        rho_values.append(d["rho"])
        warning_values.append(d["nonnormal_warning"])
    else:
        failures.append("SHARED_ORIGIN_BLOCK")

    basis_loo: list[dict] = []
    for omit in range(6):
        train = np.delete(pbs, omit, axis=0)
        try:
            b = _fit_basis(train, rank)
            ps2 = _project(b, pbs)
            cs2 = _project(b, ctx)
            a0, a1, au, _ = _make_transitions(ps2, cs2)
            fit = _fit(a0, a1, au, "D1")
            rec = _point_record(fit, "D1")
        except Exception as exc:
            fit = {"status": "REFUSE_UNSTABLE_OR_NONTRANSPORTABLE_BASIS"}
            rec = {"status": fit["status"], "reason": f"{type(exc).__name__}: {exc}"}
        rec["omitted_pbs_state_index"] = omit
        basis_loo.append(rec)
        if fit["status"] == "PASS":
            d = _diag(fit["T"])
            rho_values.append(d["rho"])
            warning_values.append(d["nonnormal_warning"])
        else:
            failures.append(f"BASIS_LOO_{omit}")

    admissible = not failures
    return {
        "all_required_sensitivity_refits_admissible": admissible,
        "failure_labels": failures,
        "shared_origin_block": block_record,
        "leave_one_pbs_basis_refits": basis_loo,
        "rho_min": min(rho_values) if rho_values else None,
        "rho_max": max(rho_values) if rho_values else None,
        "mathematical_unit_circle_side": _unit_side(rho_values, admissible),
        "nonnormal_warning_disposition": _warning_disposition(warning_values, admissible),
    }


def _run_d1_rank(pbs: np.ndarray, ctx: np.ndarray, rank: int) -> dict:
    basis = _fit_basis(pbs, rank)
    ps = _project(basis, pbs)
    cs = _project(basis, ctx)
    x0, x1, u, arm = _make_transitions(ps, cs)
    fit = _fit(x0, x1, u, "D1")
    loto = _loto(x0, x1, u, "D1")
    baselines = _baseline_errors(x0, x1, arm)
    adequate = bool(
        fit["status"] == "PASS"
        and loto["all_refits_admissible"]
        and loto["aggregate_nrmse"] is not None
        and _strictly_better(loto["aggregate_nrmse"], baselines["persistence_nrmse"])
        and _strictly_better(loto["aggregate_nrmse"], baselines["arm_specific_loto_mean_next_state_nrmse"])
    )
    sensitivity = _d1_sensitivity(pbs, ctx, rank, loto, fit)
    return {
        "rank": rank,
        "pbs_centered_numerical_rank": basis["numerical_rank"],
        "basis_singular_values": [float(x) for x in basis["singular_values"]],
        "point_fit": _point_record(fit, "D1"),
        "loto": loto,
        "baselines": baselines,
        "adequacy": "PASS" if adequate else "REFUSE",
        "sensitivity": sensitivity,
        "_states": (x0, x1, u),
    }


def _d2_sensitivity(pbs: np.ndarray, ctx: np.ndarray, rank: int, main_loto: dict, main_fit: dict) -> dict:
    control_rho: list[float] = []
    treated_rho: list[float] = []
    control_warn: list[bool] = []
    treated_warn: list[bool] = []
    delta_sign: list[int] = []
    failures: list[str] = []

    def add_fit(fit: dict, label: str) -> None:
        if fit["status"] != "PASS":
            failures.append(label)
            return
        cd = _diag(fit["T_control"])
        td = _diag(fit["T_treated"])
        control_rho.append(cd["rho"])
        treated_rho.append(td["rho"])
        control_warn.append(cd["nonnormal_warning"])
        treated_warn.append(td["nonnormal_warning"])
        tol = COMPARE_MULTIPLIER * FLOAT_EPS * max(1.0, abs(td["rho"]), abs(cd["rho"]))
        delta = td["rho"] - cd["rho"]
        delta_sign.append(0 if abs(delta) <= tol else (1 if delta > 0 else -1))

    add_fit(main_fit, "POINT_FIT")
    for record in main_loto["records"]:
        if record["status"] != "PASS":
            failures.append(f"LOTO_{record['omitted_index']}")
        else:
            cd = record["control_operator"]
            td = record["treated_operator"]
            control_rho.append(float(cd["rho"]))
            treated_rho.append(float(td["rho"]))
            control_warn.append(bool(cd["nonnormal_warning"]))
            treated_warn.append(bool(td["nonnormal_warning"]))
            tol = COMPARE_MULTIPLIER * FLOAT_EPS * max(1.0, abs(float(td["rho"])), abs(float(cd["rho"])))
            delta = float(td["rho"]) - float(cd["rho"])
            delta_sign.append(0 if abs(delta) <= tol else (1 if delta > 0 else -1))

    basis = _fit_basis(pbs, rank)
    ps = _project(basis, pbs)
    cs = _project(basis, ctx)
    x0, x1, u, _ = _make_transitions(ps, cs)
    keep = np.ones(10, dtype=bool)
    keep[[0, 5]] = False
    block = _fit(x0[keep], x1[keep], u[keep], "D2")
    block_record = _point_record(block, "D2")
    add_fit(block, "SHARED_ORIGIN_BLOCK")

    basis_loo: list[dict] = []
    for omit in range(6):
        try:
            b = _fit_basis(np.delete(pbs, omit, axis=0), rank)
            ps2 = _project(b, pbs)
            cs2 = _project(b, ctx)
            a0, a1, au, _ = _make_transitions(ps2, cs2)
            fit = _fit(a0, a1, au, "D2")
            rec = _point_record(fit, "D2")
        except Exception as exc:
            fit = {"status": "REFUSE_UNSTABLE_OR_NONTRANSPORTABLE_BASIS"}
            rec = {"status": fit["status"], "reason": f"{type(exc).__name__}: {exc}"}
        rec["omitted_pbs_state_index"] = omit
        basis_loo.append(rec)
        add_fit(fit, f"BASIS_LOO_{omit}")

    admissible = not failures
    if not admissible or not delta_sign:
        delta_disposition = "INDETERMINATE"
    elif all(x == 1 for x in delta_sign):
        delta_disposition = "POSITIVE"
    elif all(x == -1 for x in delta_sign):
        delta_disposition = "NEGATIVE"
    elif all(x == 0 for x in delta_sign):
        delta_disposition = "ZERO_WITHIN_NUMERICAL_TOLERANCE"
    else:
        delta_disposition = "INDETERMINATE"
    return {
        "all_required_sensitivity_refits_admissible": admissible,
        "failure_labels": failures,
        "shared_origin_block": block_record,
        "leave_one_pbs_basis_refits": basis_loo,
        "control_rho_min": min(control_rho) if control_rho else None,
        "control_rho_max": max(control_rho) if control_rho else None,
        "treated_rho_min": min(treated_rho) if treated_rho else None,
        "treated_rho_max": max(treated_rho) if treated_rho else None,
        "control_mathematical_unit_circle_side": _unit_side(control_rho, admissible),
        "treated_mathematical_unit_circle_side": _unit_side(treated_rho, admissible),
        "control_nonnormal_warning_disposition": _warning_disposition(control_warn, admissible),
        "treated_nonnormal_warning_disposition": _warning_disposition(treated_warn, admissible),
        "delta_rho_sign": delta_disposition,
    }


def _run_d2_rank(pbs: np.ndarray, ctx: np.ndarray, rank: int, d1: dict) -> dict:
    x0, x1, u = d1["_states"]
    fit = _fit(x0, x1, u, "D2")
    loto = _loto(x0, x1, u, "D2")
    d1_loto = d1["loto"]
    wins = 0
    if loto["all_refits_admissible"] and d1_loto["all_refits_admissible"]:
        for a, b in zip(loto["records"], d1_loto["records"]):
            if _strictly_better(float(a["relative_prediction_error"]), float(b["relative_prediction_error"])):
                wins += 1
    earned = bool(
        fit["status"] == "PASS"
        and loto["all_refits_admissible"]
        and d1_loto["aggregate_nrmse"] is not None
        and loto["aggregate_nrmse"] is not None
        and _strictly_better(loto["aggregate_nrmse"], d1_loto["aggregate_nrmse"])
        and wins >= 6
    )
    result = {
        "rank": rank,
        "point_fit": _point_record(fit, "D2"),
        "loto": loto,
        "loto_wins_over_d1": wins,
        "escalation": "EARNED" if earned else "NOT_EARNED",
    }
    if earned:
        result["sensitivity"] = _d2_sensitivity(pbs, ctx, rank, loto, fit)
    return result


def _material_d1(d1: dict, d2: dict | None) -> dict:
    return {
        "d1_adequacy": d1["adequacy"],
        "d1_mathematical_unit_circle_side": d1["sensitivity"]["mathematical_unit_circle_side"],
        "d1_nonnormal_warning": d1["sensitivity"]["nonnormal_warning_disposition"],
        "d2_escalation": d2["escalation"] if d2 is not None else "NOT_EARNED",
    }


def run_empirical() -> dict:
    freeze = _load_json(DEFAULT_FREEZE)
    validate_empirical_freeze(freeze)
    column_map = _load_json(DEFAULT_COLUMN_MAP)
    if column_map.get("processed_file_sha256") != freeze["source_binding"]["processed_file_sha256"]:
        raise RuntimeError("freeze and frozen column-map source hashes disagree")
    if column_map.get("chi_bio_outcomes_opened") is not False:
        raise RuntimeError("frozen column map is not outcome-blind")

    payload, download_history = _download_source()
    source = _open_frozen_source(payload, freeze, column_map)
    pbs = source.pop("pbs")
    ctx = source.pop("ctx")

    d1_by_rank: dict[str, dict] = {}
    for rank in (2, 3):
        d1_by_rank[str(rank)] = _run_d1_rank(pbs, ctx, rank)

    d1_both_adequate = all(d1_by_rank[str(rank)]["adequacy"] == "PASS" for rank in (2, 3))
    d2_by_rank: dict[str, dict] = {}
    if d1_both_adequate:
        for rank in (2, 3):
            d2_by_rank[str(rank)] = _run_d2_rank(pbs, ctx, rank, d1_by_rank[str(rank)])

    material: dict[str, dict] = {}
    for rank in (2, 3):
        d2 = d2_by_rank.get(str(rank))
        m = _material_d1(d1_by_rank[str(rank)], d2)
        if d2 is not None and d2["escalation"] == "EARNED":
            s = d2["sensitivity"]
            m.update({
                "d2_delta_rho_sign": s["delta_rho_sign"],
                "d2_control_mathematical_unit_circle_side": s["control_mathematical_unit_circle_side"],
                "d2_treated_mathematical_unit_circle_side": s["treated_mathematical_unit_circle_side"],
            })
        material[str(rank)] = m

    if material["2"] != material["3"]:
        a3 = "REPRESENTATION_DEPENDENT_NO_TRANSFER"
    elif any(value == "INDETERMINATE" for value in material["2"].values()):
        a3 = "INDETERMINATE"
    else:
        a3 = "A3_MATERIAL_CONCLUSIONS_AGREE"

    for rank in (2, 3):
        d1_by_rank[str(rank)].pop("_states", None)

    return {
        "status": "COMPLETE_FROZEN_SHORTTERM_G2_EMPIRICAL_PILOT",
        "protocol_authority": freeze["protocol_authority"],
        "freeze_id": freeze["freeze_id"],
        "source_url": SOURCE_URL,
        "source": source,
        "download_attempt_history": download_history,
        "normalization": "log2(CPM+1) with library totals computed before feature filtering",
        "feature_gate": "CPM>=1 in at least 3/6 SCC25 PBS states; CTX excluded from selection",
        "shared_day0": True,
        "declared_transition_count": 10,
        "d1_by_rank": d1_by_rank,
        "d2_evaluated": bool(d2_by_rank),
        "d2_by_rank": d2_by_rank,
        "material_conclusions_by_rank": material,
        "a3_disposition": a3,
        "unit_circle_semantics": "MATHEMATICAL_DISCRETE_TIME_ONLY",
        "chi_bio_computed": False,
        "chi_bio_status": "NOT_ADMITTED",
        "biological_unity_boundary_admitted": False,
        "proliferation_opened": False,
        "atac_opened": False,
        "scrna_opened": False,
        "methylation_concatenated_into_state": False,
        "promotion_effect": "NONE_PILOT_EVIDENCE_REQUIRES_POSTRESULT_AUDIT",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="development_outputs/chi_bio_shortterm_g2_empirical")
    args = parser.parse_args()
    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    output = outdir / "GRI_CHI_BIO_SHORTTERM_G2_EMPIRICAL_RESULT.json"
    try:
        result = run_empirical()
        exit_code = 0
    except Exception as exc:
        result = {
            "status": "REFUSED_OR_FAILED_FROZEN_SHORTTERM_G2_EMPIRICAL_PILOT",
            "reason": f"{type(exc).__name__}: {exc}",
            "chi_bio_computed": False,
            "chi_bio_status": "NOT_ADMITTED",
            "biological_unity_boundary_admitted": False,
            "promotion_effect": "NONE",
        }
        exit_code = 2
    output.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
