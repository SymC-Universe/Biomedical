from __future__ import annotations

"""Outcome-bearing SCC25 chronic G2 test under the frozen weekly design.

The scientific contract is frozen in
config/gri_Chi_bio_chronic_g2_r1_A3_empirical_freeze_20260913_v1.json.
This runner opens the hash-bound GSE98812 processed RNA table once, applies the
PBS-only R1 state construction, and evaluates D1 and D2 at coequal A3 ranks.
It never computes or admits biological Chi.
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

from src.run_chi_bio_shortterm_g2_empirical import (
    COMPARE_MULTIPLIER,
    FLOAT_EPS,
    _baseline_errors,
    _diag,
    _fit,
    _loto,
    _point_record,
    _strictly_better,
    _unit_side,
    _warning_disposition,
)


SOURCE_URL = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE98nnn/GSE98812/suppl/GSE98812_GEOExprsData.txt.gz"
DEFAULT_FREEZE = Path("config/gri_Chi_bio_chronic_g2_r1_A3_empirical_freeze_20260913_v1.json")
EXPECTED_ROWS = 20_531
EXPECTED_SAMPLE_COLUMNS = 36
EXPECTED_RETAINED_GENES = 14_767
EXPECTED_RETAINED_SHA256 = "74dd1945ebb97a148a2a9effc3bbffdc2427d82476c8a461a0ec488f17384318"
PBS_COLUMNS = tuple(f"C{i}.PBS" for i in range(1, 12))
CTX_COLUMNS = tuple(f"C{i}.100nM" for i in range(1, 12))
D2_MIN_WINS = 12


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _hash_gene_ids(values: list[str]) -> str:
    return hashlib.sha256("\n".join(values).encode("utf-8")).hexdigest()


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _validate_freeze(freeze: dict) -> None:
    required = {
        "status": "FROZEN_BEFORE_CHRONIC_CTX_DYNAMICS_OPENED",
        "protocol_authority": "General_Cross_Project_Research_Protocol_v0.7.5_FINAL",
        "freeze_id": "GRI_CHI_BIO_CHRONIC_G2_R1_A3_20260913_V1",
        "chi_bio_status": "NOT_ADMITTED",
        "chronic_ctx_columns_read_by_design_input_probe": False,
        "biological_unity_boundary_admitted": False,
    }
    for key, expected in required.items():
        if freeze.get(key) != expected:
            raise RuntimeError(f"chronic freeze contract mismatch for {key}: {freeze.get(key)!r}")
    source = freeze.get("source_binding", {})
    if source.get("processed_file_sha256") != "1ce13bae71bd38f619261ec0ca5dcef5dd70b967083cee059e94758aaaf6abb5":
        raise RuntimeError("chronic freeze source hash mismatch")
    if source.get("declared_transitions") != 20:
        raise RuntimeError("chronic freeze must declare exactly 20 transitions")
    if freeze.get("robustness_ranks") != [2, 3]:
        raise RuntimeError("chronic freeze must preserve coequal A3 ranks [2,3]")
    q = freeze.get("feature_gate_preoutcome_qualification", {})
    if q.get("retained_gene_count") != EXPECTED_RETAINED_GENES:
        raise RuntimeError("chronic freeze retained-gene count mismatch")
    if q.get("retained_gene_id_sha256") != EXPECTED_RETAINED_SHA256:
        raise RuntimeError("chronic freeze retained-gene hash mismatch")


def _download_source(attempts: int = 4) -> tuple[bytes, list[dict]]:
    history: list[dict] = []
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        request = Request(SOURCE_URL, headers={"User-Agent": "GRI-Chi-bio-chronic-G2/1.0"})
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
    raise RuntimeError(f"frozen GSE98812 source unavailable after {attempts} attempts: {last_error}")


def _open_frozen_source(payload: bytes, freeze: dict) -> dict:
    observed_sha = _sha256_bytes(payload)
    expected_sha = freeze["source_binding"]["processed_file_sha256"]
    if observed_sha != expected_sha:
        raise RuntimeError(f"source hash mismatch: {observed_sha} != {expected_sha}")

    raw = gzip.decompress(payload)
    frame = pd.read_csv(BytesIO(raw), sep="\t", low_memory=False)
    if frame.shape != (EXPECTED_ROWS, EXPECTED_SAMPLE_COLUMNS + 1):
        raise RuntimeError(f"processed table shape mismatch: {frame.shape}")
    if str(frame.columns[0]).strip() != "GENE":
        raise RuntimeError("first chronic processed column must be GENE")
    if len(set(map(str, frame.columns))) != len(frame.columns):
        raise RuntimeError("processed table contains duplicate column names")

    expected_pbs = list(freeze["source_binding"]["pbs_columns"])
    expected_ctx = list(freeze["source_binding"]["ctx_columns"])
    if expected_pbs != list(PBS_COLUMNS) or expected_ctx != list(CTX_COLUMNS):
        raise RuntimeError("freeze weekly column ordering differs from runner contract")
    missing = [x for x in (*PBS_COLUMNS, *CTX_COLUMNS) if x not in frame.columns]
    if missing:
        raise RuntimeError(f"frozen chronic columns missing from source: {missing}")

    gene_ids = frame.iloc[:, 0].astype(str).str.strip()
    if gene_ids.eq("").any() or gene_ids.eq("nan").any() or gene_ids.duplicated().any():
        raise RuntimeError("source gene identifiers are missing or duplicated")

    ordered = list(PBS_COLUMNS) + list(CTX_COLUMNS)
    values = frame.loc[:, ordered].apply(pd.to_numeric, errors="raise").to_numpy(dtype=np.float64)
    if not np.all(np.isfinite(values)) or np.any(values < 0.0):
        raise RuntimeError("chronic selected source values must be finite and nonnegative")

    pbs_raw = values[:, :11]
    keep = np.sum(pbs_raw >= 1.0, axis=1) >= 6
    retained_ids = gene_ids.to_numpy(dtype=str)[keep].tolist()
    retained_count = int(np.sum(keep))
    retained_sha = _hash_gene_ids(retained_ids)
    if retained_count != EXPECTED_RETAINED_GENES:
        raise RuntimeError(f"frozen feature gate count drift: {retained_count} != {EXPECTED_RETAINED_GENES}")
    if retained_sha != EXPECTED_RETAINED_SHA256:
        raise RuntimeError(f"frozen feature-gate ID hash drift: {retained_sha} != {EXPECTED_RETAINED_SHA256}")

    transformed = np.log2(values[keep, :] + 1.0).T
    return {
        "pbs": transformed[:11, :],
        "ctx": transformed[11:, :],
        "gene_rows_total": int(frame.shape[0]),
        "sample_columns_total": EXPECTED_SAMPLE_COLUMNS,
        "retained_gene_count": retained_count,
        "retained_gene_ids_sha256": retained_sha,
        "source_sha256": observed_sha,
        "source_compressed_bytes": len(payload),
        "source_uncompressed_bytes": len(raw),
        "pbs_columns": list(PBS_COLUMNS),
        "ctx_columns": list(CTX_COLUMNS),
    }


def _fit_basis(pbs: np.ndarray, rank: int) -> dict:
    mean = np.mean(pbs, axis=0)
    centered = pbs - mean
    _, singular_values, vt = np.linalg.svd(centered, full_matrices=False)
    numerical_rank = int(np.linalg.matrix_rank(centered))
    if rank > numerical_rank:
        raise RuntimeError(f"rank {rank} exceeds PBS-centered numerical rank {numerical_rank}")
    components = vt[:rank].copy()
    for i in range(components.shape[0]):
        pivot = int(np.argmax(np.abs(components[i])))
        if components[i, pivot] < 0.0:
            components[i] *= -1.0
    return {
        "mean": mean,
        "components": components,
        "singular_values": singular_values[:rank].copy(),
        "numerical_rank": numerical_rank,
    }


def _project(basis: dict, x: np.ndarray) -> np.ndarray:
    return (x - basis["mean"]) @ basis["components"].T


def _make_transitions(pbs_state: np.ndarray, ctx_state: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    if pbs_state.shape[0] != 11 or ctx_state.shape[0] != 11:
        raise RuntimeError("chronic geometry must be exactly 11 PBS + 11 CTX weekly states")
    x0 = np.vstack([pbs_state[:-1], ctx_state[:-1]])
    x1 = np.vstack([pbs_state[1:], ctx_state[1:]])
    u = np.vstack([np.zeros((10, 1)), np.ones((10, 1))])
    arm = np.array([0] * 10 + [1] * 10, dtype=int)
    return x0, x1, u, arm


def _fit_states(pbs: np.ndarray, ctx: np.ndarray, rank: int) -> tuple[dict, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    basis = _fit_basis(pbs, rank)
    ps = _project(basis, pbs)
    cs = _project(basis, ctx)
    x0, x1, u, arm = _make_transitions(ps, cs)
    return basis, x0, x1, u, arm


def _comparison_sign(delta: float, a: float, b: float) -> int:
    tol = COMPARE_MULTIPLIER * FLOAT_EPS * max(1.0, abs(a), abs(b))
    if abs(delta) <= tol:
        return 0
    return 1 if delta > 0.0 else -1


def _d1_sensitivity(pbs: np.ndarray, ctx: np.ndarray, rank: int, main_fit: dict, main_loto: dict) -> dict:
    rho_values: list[float] = []
    warnings: list[bool] = []
    failures: list[str] = []

    def add_fit(fit: dict, label: str) -> None:
        if fit["status"] != "PASS":
            failures.append(label)
            return
        diag = _diag(fit["T"])
        rho_values.append(float(diag["rho"]))
        warnings.append(bool(diag["nonnormal_warning"]))

    add_fit(main_fit, "POINT_FIT")
    for record in main_loto["records"]:
        if record["status"] != "PASS":
            failures.append(f"LOTO_{record['omitted_index']}")
        else:
            rho_values.append(float(record["operator"]["rho"]))
            warnings.append(bool(record["operator"]["nonnormal_warning"]))

    _, x0, x1, u, _ = _fit_states(pbs, ctx, rank)
    keep = np.ones(20, dtype=bool)
    keep[[0, 10]] = False
    block = _fit(x0[keep], x1[keep], u[keep], "D1")
    block_record = _point_record(block, "D1")
    add_fit(block, "EARLIEST_PAIRED_BLOCK")

    basis_loo: list[dict] = []
    for omit in range(11):
        try:
            basis = _fit_basis(np.delete(pbs, omit, axis=0), rank)
            ps = _project(basis, pbs)
            cs = _project(basis, ctx)
            a0, a1, au, _ = _make_transitions(ps, cs)
            fit = _fit(a0, a1, au, "D1")
            rec = _point_record(fit, "D1")
        except Exception as exc:
            fit = {"status": "REFUSE_UNSTABLE_OR_NONTRANSPORTABLE_BASIS"}
            rec = {"status": fit["status"], "reason": f"{type(exc).__name__}: {exc}"}
        rec["omitted_pbs_state_index"] = omit
        basis_loo.append(rec)
        add_fit(fit, f"BASIS_LOO_{omit}")

    admissible = not failures
    return {
        "all_required_sensitivity_refits_admissible": admissible,
        "failure_labels": failures,
        "paired_earliest_transition_block": block_record,
        "leave_one_pbs_basis_refits": basis_loo,
        "rho_min": min(rho_values) if rho_values else None,
        "rho_max": max(rho_values) if rho_values else None,
        "mathematical_unit_circle_side": _unit_side(rho_values, admissible),
        "nonnormal_warning_disposition": _warning_disposition(warnings, admissible),
    }


def _d2_sensitivity(pbs: np.ndarray, ctx: np.ndarray, rank: int, main_fit: dict, main_loto: dict) -> dict:
    control_rho: list[float] = []
    treated_rho: list[float] = []
    control_warn: list[bool] = []
    treated_warn: list[bool] = []
    delta_signs: list[int] = []
    failures: list[str] = []

    def add_operator_pair(cd: dict, td: dict) -> None:
        cr = float(cd["rho"])
        tr = float(td["rho"])
        control_rho.append(cr)
        treated_rho.append(tr)
        control_warn.append(bool(cd["nonnormal_warning"]))
        treated_warn.append(bool(td["nonnormal_warning"]))
        delta_signs.append(_comparison_sign(tr - cr, tr, cr))

    def add_fit(fit: dict, label: str) -> None:
        if fit["status"] != "PASS":
            failures.append(label)
            return
        add_operator_pair(_diag(fit["T_control"]), _diag(fit["T_treated"]))

    add_fit(main_fit, "POINT_FIT")
    for record in main_loto["records"]:
        if record["status"] != "PASS":
            failures.append(f"LOTO_{record['omitted_index']}")
        else:
            add_operator_pair(record["control_operator"], record["treated_operator"])

    _, x0, x1, u, _ = _fit_states(pbs, ctx, rank)
    keep = np.ones(20, dtype=bool)
    keep[[0, 10]] = False
    block = _fit(x0[keep], x1[keep], u[keep], "D2")
    block_record = _point_record(block, "D2")
    add_fit(block, "EARLIEST_PAIRED_BLOCK")

    basis_loo: list[dict] = []
    for omit in range(11):
        try:
            basis = _fit_basis(np.delete(pbs, omit, axis=0), rank)
            ps = _project(basis, pbs)
            cs = _project(basis, ctx)
            a0, a1, au, _ = _make_transitions(ps, cs)
            fit = _fit(a0, a1, au, "D2")
            rec = _point_record(fit, "D2")
        except Exception as exc:
            fit = {"status": "REFUSE_UNSTABLE_OR_NONTRANSPORTABLE_BASIS"}
            rec = {"status": fit["status"], "reason": f"{type(exc).__name__}: {exc}"}
        rec["omitted_pbs_state_index"] = omit
        basis_loo.append(rec)
        add_fit(fit, f"BASIS_LOO_{omit}")

    admissible = not failures
    if not admissible or not delta_signs:
        delta_disposition = "INDETERMINATE"
    elif all(x == 1 for x in delta_signs):
        delta_disposition = "POSITIVE"
    elif all(x == -1 for x in delta_signs):
        delta_disposition = "NEGATIVE"
    elif all(x == 0 for x in delta_signs):
        delta_disposition = "ZERO_WITHIN_NUMERICAL_TOLERANCE"
    else:
        delta_disposition = "INDETERMINATE"

    return {
        "all_required_sensitivity_refits_admissible": admissible,
        "failure_labels": failures,
        "paired_earliest_transition_block": block_record,
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


def _run_rank(pbs: np.ndarray, ctx: np.ndarray, rank: int) -> dict:
    basis, x0, x1, u, arm = _fit_states(pbs, ctx, rank)
    baselines = _baseline_errors(x0, x1, arm)

    d1_fit = _fit(x0, x1, u, "D1")
    d1_loto = _loto(x0, x1, u, "D1")
    d1_adequate = bool(
        d1_fit["status"] == "PASS"
        and d1_loto["all_refits_admissible"]
        and d1_loto["aggregate_nrmse"] is not None
        and _strictly_better(d1_loto["aggregate_nrmse"], baselines["persistence_nrmse"])
        and _strictly_better(d1_loto["aggregate_nrmse"], baselines["arm_specific_loto_mean_next_state_nrmse"])
    )
    d1_sensitivity = _d1_sensitivity(pbs, ctx, rank, d1_fit, d1_loto)

    d2_fit = _fit(x0, x1, u, "D2")
    d2_loto = _loto(x0, x1, u, "D2")
    wins = 0
    if d1_loto["all_refits_admissible"] and d2_loto["all_refits_admissible"]:
        for d2_rec, d1_rec in zip(d2_loto["records"], d1_loto["records"], strict=True):
            if _strictly_better(float(d2_rec["relative_prediction_error"]), float(d1_rec["relative_prediction_error"])):
                wins += 1
    d2_supported = bool(
        d2_fit["status"] == "PASS"
        and d2_loto["all_refits_admissible"]
        and d1_loto["all_refits_admissible"]
        and d2_loto["aggregate_nrmse"] is not None
        and d1_loto["aggregate_nrmse"] is not None
        and _strictly_better(d2_loto["aggregate_nrmse"], baselines["persistence_nrmse"])
        and _strictly_better(d2_loto["aggregate_nrmse"], baselines["arm_specific_loto_mean_next_state_nrmse"])
        and _strictly_better(d2_loto["aggregate_nrmse"], d1_loto["aggregate_nrmse"])
        and wins >= D2_MIN_WINS
    )
    d2_sensitivity = _d2_sensitivity(pbs, ctx, rank, d2_fit, d2_loto)

    return {
        "rank": rank,
        "pbs_centered_numerical_rank": basis["numerical_rank"],
        "basis_singular_values": [float(x) for x in basis["singular_values"]],
        "baselines": baselines,
        "d1": {
            "point_fit": _point_record(d1_fit, "D1"),
            "loto": d1_loto,
            "adequacy": "PASS" if d1_adequate else "REFUSE",
            "sensitivity": d1_sensitivity,
        },
        "d2": {
            "point_fit": _point_record(d2_fit, "D2"),
            "loto": d2_loto,
            "loto_wins_over_d1": wins,
            "minimum_required_wins": D2_MIN_WINS,
            "reorganization_support": "SUPPORTED" if d2_supported else "NOT_SUPPORTED",
            "sensitivity": d2_sensitivity,
        },
    }


def _material(rank_result: dict) -> dict:
    d1 = rank_result["d1"]
    d2 = rank_result["d2"]
    material = {
        "d1_adequacy": d1["adequacy"],
        "d1_mathematical_unit_circle_side": d1["sensitivity"]["mathematical_unit_circle_side"],
        "d1_nonnormal_warning": d1["sensitivity"]["nonnormal_warning_disposition"],
        "d2_reorganization_support": d2["reorganization_support"],
    }
    if d2["reorganization_support"] == "SUPPORTED":
        s = d2["sensitivity"]
        material.update({
            "d2_control_mathematical_unit_circle_side": s["control_mathematical_unit_circle_side"],
            "d2_treated_mathematical_unit_circle_side": s["treated_mathematical_unit_circle_side"],
            "d2_delta_rho_sign": s["delta_rho_sign"],
            "d2_control_nonnormal_warning": s["control_nonnormal_warning_disposition"],
            "d2_treated_nonnormal_warning": s["treated_nonnormal_warning_disposition"],
        })
    return material


def _overall_disposition(material: dict[str, dict]) -> str:
    if material["2"] != material["3"]:
        return "REPRESENTATION_DEPENDENT_NO_TRANSFER"
    m = material["2"]
    if m["d2_reorganization_support"] == "SUPPORTED":
        return "REORGANIZATION_SUPPORTED"
    if m["d1_adequacy"] == "PASS":
        return "SHARED_OPERATOR_ADEQUATE_NO_REORGANIZATION_SUPPORT"
    return "NO_TRANSFER"


def run_empirical() -> dict:
    freeze = _load_json(DEFAULT_FREEZE)
    _validate_freeze(freeze)
    payload, history = _download_source()
    source = _open_frozen_source(payload, freeze)
    pbs = source.pop("pbs")
    ctx = source.pop("ctx")

    by_rank = {str(rank): _run_rank(pbs, ctx, rank) for rank in (2, 3)}
    material = {key: _material(value) for key, value in by_rank.items()}
    overall = _overall_disposition(material)

    return {
        "status": "COMPLETE_FROZEN_CHRONIC_G2_EMPIRICAL_TEST",
        "protocol_authority": freeze["protocol_authority"],
        "freeze_id": freeze["freeze_id"],
        "source_url": SOURCE_URL,
        "source": source,
        "download_attempt_history": history,
        "normalization": "log2(upper-quartile-normalized source value + 1); no CPM renormalization",
        "feature_gate": "source_value>=1 in at least 6/11 PBS states; CTX excluded from selection",
        "shared_day0": False,
        "declared_transition_count": 20,
        "by_rank": by_rank,
        "material_conclusions_by_rank": material,
        "overall_disposition": overall,
        "unit_circle_semantics": "MATHEMATICAL_DISCRETE_TIME_WEEKLY_ONLY",
        "daily_weekly_operator_conversion_performed": False,
        "chi_bio_computed": False,
        "chi_bio_status": "NOT_ADMITTED",
        "biological_unity_boundary_admitted": False,
        "proliferation_opened": False,
        "atac_opened": False,
        "scrna_opened": False,
        "methylation_concatenated_into_state": False,
        "promotion_effect": "NONE_EMPIRICAL_RESULT_REQUIRES_POSTRESULT_AUDIT",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="development_outputs/chi_bio_chronic_g2_empirical")
    args = parser.parse_args()
    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    output = outdir / "GRI_CHI_BIO_CHRONIC_G2_EMPIRICAL_RESULT.json"
    try:
        result = run_empirical()
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except Exception as exc:
        failure = {
            "status": "REFUSE_CHRONIC_G2_EMPIRICAL_EXECUTION",
            "reason": f"{type(exc).__name__}: {exc}",
            "chi_bio_computed": False,
            "chi_bio_status": "NOT_ADMITTED",
            "biological_unity_boundary_admitted": False,
        }
        output.write_text(json.dumps(failure, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(failure, indent=2, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
