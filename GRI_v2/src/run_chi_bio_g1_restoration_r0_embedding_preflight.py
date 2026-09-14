from __future__ import annotations

"""R0 restoration-identifiability embedding preflight for chronic SCC25 G1.

This runner does not compute normalized G1 and does not assign a restoration
operator. It re-materializes only the already-frozen chronic-G2 D1 point
operators, verifies their published point diagnostics against the immutable G2
artifact, and characterizes principal-branch discrete-to-continuous embedding
readiness. The frozen G2 result remains the source of record.
"""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

import numpy as np

from src.run_chi_bio_chronic_g2_empirical import (
    DEFAULT_FREEZE,
    _diag,
    _download_source,
    _fit,
    _fit_states,
    _load_json,
    _open_frozen_source,
    _validate_freeze,
)


DEFAULT_CONTRACT = Path("config/gri_Chi_bio_G1_restoration_r0_embedding_preflight_v0_1.json")
EXPECTED_G2_RUNNER_BLOB = "636c2132649a42ffc26feaefd47aa9a056c78b75"
EXPECTED_G2_FREEZE_BLOB = "b63cc3b8af6135247fdeb4c9e68be4275dd108cf"
EXPECTED_G2_ARTIFACT_DIGEST = "sha256:4ad76198657cbb4f5a5839b5ad4068625ccb0801fe050d16b83006d2ef8a5687"
EXPECTED_G2_RUN_ID = 34769901215
EXPECTED_G2_ARTIFACT_ID = 10321342847
EXPECTED_G2_FREEZE_ID = "GRI_CHI_BIO_CHRONIC_G2_R1_A3_20260913_V1"
EXPECTED_SOURCE_SHA256 = "1ce13bae71bd38f619261ec0ca5dcef5dd70b967083cee059e94758aaaf6abb5"
MECHANICAL_RTOL = 1e-12
MECHANICAL_ATOL = 1e-12


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _git_blob(path: Path) -> str:
    proc = subprocess.run(
        ["git", "hash-object", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    return proc.stdout.strip()


def _validate_r0_contract(contract: dict) -> None:
    required = {
        "status": "FROZEN_BEFORE_R0_EXECUTION",
        "expected_epistemic_output": "R0_EMBEDDING_DIAGNOSTIC_ONLY",
        "chi_bio_status": "NOT_ADMITTED",
        "biological_unity_boundary_admitted": False,
        "normalized_g1_authorized": False,
        "restoration_operator_authorized": False,
    }
    for key, expected in required.items():
        if contract.get(key) != expected:
            raise RuntimeError(f"R0 contract mismatch for {key}: {contract.get(key)!r}")
    frozen = contract.get("frozen_input", {})
    if frozen.get("workflow_run_id") != EXPECTED_G2_RUN_ID:
        raise RuntimeError("R0 contract G2 run identity mismatch")
    if frozen.get("artifact_id") != EXPECTED_G2_ARTIFACT_ID:
        raise RuntimeError("R0 contract G2 artifact identity mismatch")
    if frozen.get("artifact_digest") != EXPECTED_G2_ARTIFACT_DIGEST:
        raise RuntimeError("R0 contract G2 artifact digest mismatch")
    if frozen.get("g2_freeze_id") != EXPECTED_G2_FREEZE_ID:
        raise RuntimeError("R0 contract G2 freeze identity mismatch")
    if frozen.get("ranks") != [2, 3]:
        raise RuntimeError("R0 contract must preserve coequal ranks [2,3]")


def _validate_lineage_files() -> dict:
    runner = Path("src/run_chi_bio_chronic_g2_empirical.py")
    freeze = DEFAULT_FREEZE
    runner_blob = _git_blob(runner)
    freeze_blob = _git_blob(freeze)
    if runner_blob != EXPECTED_G2_RUNNER_BLOB:
        raise RuntimeError(f"frozen G2 runner drift: {runner_blob} != {EXPECTED_G2_RUNNER_BLOB}")
    if freeze_blob != EXPECTED_G2_FREEZE_BLOB:
        raise RuntimeError(f"frozen G2 freeze drift: {freeze_blob} != {EXPECTED_G2_FREEZE_BLOB}")
    return {
        "g2_runner_git_blob_sha1": runner_blob,
        "g2_freeze_git_blob_sha1": freeze_blob,
    }


def _validate_frozen_result(result: dict) -> None:
    required = {
        "status": "COMPLETE_FROZEN_CHRONIC_G2_EMPIRICAL_TEST",
        "freeze_id": EXPECTED_G2_FREEZE_ID,
        "declared_transition_count": 20,
        "chi_bio_computed": False,
        "chi_bio_status": "NOT_ADMITTED",
        "biological_unity_boundary_admitted": False,
        "daily_weekly_operator_conversion_performed": False,
    }
    for key, expected in required.items():
        if result.get(key) != expected:
            raise RuntimeError(f"frozen G2 result contract mismatch for {key}: {result.get(key)!r}")
    source = result.get("source", {})
    if source.get("source_sha256") != EXPECTED_SOURCE_SHA256:
        raise RuntimeError("frozen G2 result source hash mismatch")
    if sorted(result.get("by_rank", {}).keys()) != ["2", "3"]:
        raise RuntimeError("frozen G2 result rank set mismatch")


def _same_float(observed: float, expected: float) -> bool:
    return bool(np.isclose(float(observed), float(expected), rtol=MECHANICAL_RTOL, atol=MECHANICAL_ATOL))


def _principal_log_diagnostic(t: np.ndarray) -> dict:
    matrix = np.asarray(t, dtype=np.complex128)
    eigvals, eigvecs = np.linalg.eig(matrix)
    if not np.all(np.isfinite(eigvals.real)) or not np.all(np.isfinite(eigvals.imag)):
        return {"status": "REFUSE_NONFINITE_EIGENSYSTEM"}
    if np.any(np.abs(eigvals) == 0.0):
        return {
            "status": "REFUSE_SINGULAR_TRANSITION_OPERATOR",
            "eigenvalues": [[float(x.real), float(x.imag)] for x in eigvals],
        }
    try:
        inv_vecs = np.linalg.inv(eigvecs)
    except np.linalg.LinAlgError:
        return {
            "status": "REFUSE_NONDIAGONALIZABLE_BY_NUMPY_EIG",
            "eigenvalues": [[float(x.real), float(x.imag)] for x in eigvals],
        }

    logs = np.log(eigvals)
    j = eigvecs @ np.diag(logs) @ inv_vecs
    reconstructed = eigvecs @ np.diag(np.exp(logs)) @ inv_vecs
    denom = float(np.linalg.norm(matrix))
    reconstruction_error = float(np.linalg.norm(reconstructed - matrix) / denom) if denom > 0.0 else None
    imag_norm = float(np.linalg.norm(j.imag))
    real_norm = float(np.linalg.norm(j.real))
    return {
        "status": "PRINCIPAL_BRANCH_CANDIDATE_COMPUTED",
        "transition_interval": "1 week",
        "generator_units": "per_week_under_time_homogeneous_embedding_assumption",
        "embedding_admitted": False,
        "matrix_log_uniqueness_established": False,
        "branch_note": "Principal complex logarithm candidate only; other logarithm branches are not excluded or selected in R0.",
        "eigenvalues": [[float(x.real), float(x.imag)] for x in eigvals],
        "eigenvalue_moduli": [float(abs(x)) for x in eigvals],
        "eigenvalue_arguments_radians": [float(np.angle(x)) for x in eigvals],
        "eigenvector_condition_number": float(np.linalg.cond(eigvecs)),
        "principal_log_real": [[float(x) for x in row] for row in j.real],
        "principal_log_imag": [[float(x) for x in row] for row in j.imag],
        "principal_log_real_frobenius": real_norm,
        "principal_log_imag_frobenius": imag_norm,
        "principal_log_imag_to_real_ratio": imag_norm / real_norm if real_norm > 0.0 else None,
        "reconstruction_relative_frobenius_error": reconstruction_error,
        "restoration_decomposition_performed": False,
        "normalized_g1_computed": False,
        "chi_bio_computed": False,
    }


def run_preflight(frozen_result_path: Path) -> dict:
    contract = _load_json(DEFAULT_CONTRACT)
    _validate_r0_contract(contract)
    lineage = _validate_lineage_files()

    frozen_result = _load_json(frozen_result_path)
    _validate_frozen_result(frozen_result)

    freeze = _load_json(DEFAULT_FREEZE)
    _validate_freeze(freeze)
    payload, history = _download_source()
    source = _open_frozen_source(payload, freeze)
    pbs = source.pop("pbs")
    ctx = source.pop("ctx")

    by_rank: dict[str, dict] = {}
    for rank in (2, 3):
        _, x0, x1, u, _ = _fit_states(pbs, ctx, rank)
        fit = _fit(x0, x1, u, "D1")
        if fit.get("status") != "PASS":
            raise RuntimeError(f"frozen D1 point fit no longer admissible at rank {rank}: {fit.get('status')}")
        t = np.asarray(fit["T"], dtype=np.float64)
        observed = _diag(t)
        expected = frozen_result["by_rank"][str(rank)]["d1"]["point_fit"]["operator"]
        rho_match = _same_float(observed["rho"], expected["rho"])
        sigma_match = _same_float(observed["sigma_max"], expected["sigma_max"])
        warning_match = bool(observed["nonnormal_warning"]) == bool(expected["nonnormal_warning"])
        if not (rho_match and sigma_match and warning_match):
            raise RuntimeError(
                f"re-materialized rank-{rank} D1 diagnostics do not reproduce frozen G2 point diagnostics"
            )
        by_rank[str(rank)] = {
            "rank": rank,
            "transition_matrix_T": [[float(x) for x in row] for row in t],
            "frozen_point_diagnostic": expected,
            "rematerialized_point_diagnostic": observed,
            "mechanical_reproduction": {
                "rho_match": rho_match,
                "sigma_max_match": sigma_match,
                "nonnormal_warning_match": warning_match,
                "rtol": MECHANICAL_RTOL,
                "atol": MECHANICAL_ATOL,
                "status": "PASS",
            },
            "embedding_diagnostic": _principal_log_diagnostic(t),
        }

    return {
        "status": "COMPLETE_R0_EMBEDDING_DIAGNOSTIC_ONLY",
        "epistemic_class": "P0_D_PRECOMPUTE_MATERIALIZATION_AND_EMBEDDING_DIAGNOSTIC",
        "protocol_authority": contract["protocol_authority"],
        "r0_contract_schema": contract["schema"],
        "frozen_g2_input": contract["frozen_input"],
        "frozen_result_file_sha256": _sha256_file(frozen_result_path),
        "lineage": lineage,
        "source_reproduction": {
            "source_sha256": source["source_sha256"],
            "retained_gene_count": source["retained_gene_count"],
            "retained_gene_ids_sha256": source["retained_gene_ids_sha256"],
            "download_attempt_history": history,
        },
        "by_rank": by_rank,
        "g2_result_superseded": False,
        "g2_result_reinterpreted": False,
        "restoration_operator_assigned": False,
        "restoration_decomposition_performed": False,
        "normalized_g1_computed": False,
        "chi_bio_computed": False,
        "chi_bio_status": "NOT_ADMITTED",
        "biological_unity_boundary_admitted": False,
        "next_gate": "Evaluate embedding ambiguity and source-supported restoration constraints prospectively before any normalized G1 computation.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frozen-result", required=True)
    parser.add_argument("--output-dir", default="development_outputs/chi_bio_g1_restoration_r0")
    args = parser.parse_args()
    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    output = outdir / "GRI_CHI_BIO_G1_RESTORATION_R0_EMBEDDING_PREFLIGHT_RESULT.json"
    try:
        result = run_preflight(Path(args.frozen_result))
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except Exception as exc:
        failure = {
            "status": "REFUSE_R0_EMBEDDING_PREFLIGHT",
            "reason": f"{type(exc).__name__}: {exc}",
            "restoration_operator_assigned": False,
            "normalized_g1_computed": False,
            "chi_bio_computed": False,
            "chi_bio_status": "NOT_ADMITTED",
            "biological_unity_boundary_admitted": False,
        }
        output.write_text(json.dumps(failure, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(failure, indent=2, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
