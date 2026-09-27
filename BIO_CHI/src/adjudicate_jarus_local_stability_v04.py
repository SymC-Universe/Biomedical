#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
BIO = ROOT / "BIO_CHI"
FREEZE_PATH = BIO / "config" / "JARUS_LOCAL_STABILITY_POSTPROCESS_FREEZE_v0_4.json"
OUTDIR = BIO / "artifacts" / "generated" / "jarus_local_stability_v04"
OUT = OUTDIR / "local_stability_v0_4.json"

EXPECTED = {
    "FIG8A_NOMINAL_DAMPED": "STABLE",
    "FIG8B_LIMIT_CYCLE": "UNSTABLE",
    "FIG8C_RELAXATION_OSCILLATION": "UNSTABLE",
}
REQUIRED_MULTIPLIERS = [1.0, 0.5, 0.25]


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def as_list(value):
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        return [value]
    if value in (None, []):
        return []
    raise TypeError(f"unexpected JSON container: {type(value).__name__}")


def classify(values: list[float]) -> str:
    if all(v < 0 for v in values):
        return "STABLE"
    if all(v > 0 for v in values):
        return "UNSTABLE"
    return "INDETERMINATE_NUMERICAL_SIGN"


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: adjudicate_jarus_local_stability_v04.py <v03-artifact.zip>")

    artifact_zip = pathlib.Path(sys.argv[1]).resolve()
    freeze = json.loads(FREEZE_PATH.read_text(encoding="utf-8"))
    expected_digest = freeze["source_artifact_zip_sha256"]
    actual_digest = sha256_file(artifact_zip)
    if actual_digest != expected_digest:
        raise SystemExit(
            f"SOURCE_ARTIFACT_DIGEST_MISMATCH expected={expected_digest} actual={actual_digest}"
        )

    with zipfile.ZipFile(artifact_zip) as zf:
        matches = [n for n in zf.namelist() if pathlib.PurePosixPath(n).name == "local_stability_v0_3.json"]
        if len(matches) != 1:
            raise SystemExit(f"SOURCE_ARTIFACT_MEMBER_ERROR matches={matches}")
        raw = json.loads(zf.read(matches[0]).decode("utf-8"))

    if raw.get("schema_version") != "0.3":
        raise SystemExit(f"SOURCE_SCHEMA_MISMATCH {raw.get('schema_version')!r}")
    if raw.get("audit_type") != "bounded_residual_TR1_local_stability_crosscheck":
        raise SystemExit(f"SOURCE_AUDIT_TYPE_MISMATCH {raw.get('audit_type')!r}")

    source_cases = {c["case_id"]: c for c in raw.get("cases", [])}
    if set(source_cases) != set(EXPECTED):
        raise SystemExit(f"SOURCE_CASE_SET_MISMATCH {sorted(source_cases)}")

    adjudicated = []
    for case_id, expected_class in EXPECTED.items():
        source = source_cases[case_id]
        roots = as_list(source.get("roots"))
        accepted_count = int(source.get("accepted_distinct_root_count", len(roots)))
        if accepted_count != len(roots):
            raise SystemExit(
                f"ROOT_COUNT_INCONSISTENCY {case_id} accepted={accepted_count} encoded={len(roots)}"
            )

        record = {
            "case_id": case_id,
            "expected_paper_local_stability": expected_class,
            "accepted_distinct_root_count": accepted_count,
            "source_v03_paper_local_stability_status": source.get("paper_local_stability_status"),
        }

        if accepted_count != 1:
            record.update(
                {
                    "adjudicated_local_stability": "INDETERMINATE_ROOT_MULTIPLICITY",
                    "paper_local_stability_status": "INDETERMINATE_ROOT_MULTIPLICITY",
                    "mechanical_summary_mismatch_detected": False,
                }
            )
            adjudicated.append(record)
            continue

        root = roots[0]
        steps = as_list(root.get("jacobian_steps"))
        if len(steps) != 3:
            raise SystemExit(f"JACOBIAN_STEP_COUNT_MISMATCH {case_id} count={len(steps)}")
        multipliers = [float(s["multiplier"]) for s in steps]
        if multipliers != REQUIRED_MULTIPLIERS:
            raise SystemExit(
                f"JACOBIAN_MULTIPLIER_MISMATCH {case_id} got={multipliers} expected={REQUIRED_MULTIPLIERS}"
            )
        step_max = [float(s["max_real_eigenvalue"]) for s in steps]
        stored_summary = [float(v) for v in root.get("max_real_eigenvalues", [])]
        local = classify(step_max)
        if local == expected_class:
            paper_status = "PASS"
        elif local == "INDETERMINATE_NUMERICAL_SIGN":
            paper_status = "INDETERMINATE_NUMERICAL_SIGN"
        else:
            paper_status = "FAIL_NATIVE_LOCAL_STABILITY"

        record.update(
            {
                "root": root.get("root"),
                "residual_inf": root.get("residual_inf"),
                "jacobian_step_multipliers": multipliers,
                "jacobian_step_max_real_eigenvalues": step_max,
                "source_v03_stored_summary_max_real_eigenvalues": stored_summary,
                "mechanical_summary_mismatch_detected": stored_summary != step_max,
                "adjudicated_local_stability": local,
                "paper_local_stability_status": paper_status,
            }
        )
        adjudicated.append(record)

    all_pass = all(c["paper_local_stability_status"] == "PASS" for c in adjudicated)
    all_mismatch = all(c.get("mechanical_summary_mismatch_detected", False) for c in adjudicated)
    result = {
        "schema_version": "0.4",
        "audit_type": "immutable_v03_artifact_postprocess_repair",
        "authority": "SymC GOM v0.8.4",
        "freeze": "BIO_CHI/config/JARUS_LOCAL_STABILITY_POSTPROCESS_FREEZE_v0_4.json",
        "source_result_pin": "BIO_CHI/config/JARUS_LOCAL_STABILITY_V03_RESULT_PIN.json",
        "source_workflow_run_id": freeze["source_workflow_run_id"],
        "source_artifact_id": freeze["source_artifact_id"],
        "source_artifact_zip_sha256": actual_digest,
        "root_solver_rerun": False,
        "jacobian_recomputed": False,
        "mechanical_summary_mismatch_confirmed_all_three_cases": all_mismatch,
        "cases": adjudicated,
        "native_local_stability_gate": (
            "PASS_ALL_FROZEN_FIG8_CASES" if all_pass else "NOT_ALL_FROZEN_FIG8_CASES_PASS"
        ),
        "finite_window_results_preserved": True,
        "limit_cycle_proved": False,
        "chi_bio_constructed": False,
        "Chi_bio_constructed": False,
        "Bio_Chi_constructed": False,
        "mode_selected": False,
        "interpretation": (
            "This artifact repairs only the v0.3 summary/classification path by applying the prospectively frozen sign rule to the immutable per-step Jacobian maxima already stored in the v0.3 artifact. It does not rerun root finding, recompute Jacobians, prove a limit cycle, select a mode, or construct chi_bio/Chi_bio/Bio Chi."
        ),
    }

    OUTDIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    print("BIO_CHI_JARUS_LOCAL_STABILITY_V04_POSTPROCESS_COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
