from __future__ import annotations

"""Hard preflight for the first outcome-bearing G2/R1 empirical execution.

Ordering is deliberate:
1. validate the explicit scientific freeze;
2. validate frozen source-manifest semantics and hash bindings;
3. only after both pass may an eventual execution adapter be allowed to open
   real molecular matrices.

This module itself performs no state reduction, transition fit, or Chi_bio
calculation.
"""

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from src.chi_bio_empirical_freeze_contract import (
    EmpiricalFreezeContractError,
    validate_empirical_freeze,
)


DEFAULT_FREEZE = Path("config/gri_Chi_bio_first_empirical_g2_r1_freeze_TEMPLATE_v0_1.json")
SHORT_MANIFEST = Path("config/gri_hnscc_shortterm_cetuximab_manifest_p0d_v0_1.json")
SHORT_COLUMN_MAP = Path("config/gri_hnscc_shortterm_bulk_rna_column_map_p0d_v0_1.json")
CHRONIC_MANIFEST = Path("config/gri_scc25_paired_timecourse_manifest_p0d_v0_1.json")


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def validate_source_manifests() -> dict[str, Any]:
    short = _load_json(SHORT_MANIFEST)
    colmap = _load_json(SHORT_COLUMN_MAP)
    chronic = _load_json(CHRONIC_MANIFEST)

    if short["selection_firewall"]["chi_bio_outcomes_opened"] is not False:
        raise RuntimeError("short-term manifest says Chi_bio outcomes were opened")
    if colmap["chi_bio_outcomes_opened"] is not False:
        raise RuntimeError("short-term processed column map says Chi_bio outcomes were opened")
    if chronic["selection_firewall"]["chi_bio_outcomes_opened"] is not False:
        raise RuntimeError("chronic manifest says Chi_bio outcomes were opened")

    if len(short["bulk_daily"]["SCC25"]["PBS"]) != 6:
        raise RuntimeError("short-term SCC25 PBS source identity is incomplete")
    if len(short["bulk_daily"]["SCC25"]["CTX"]) != 5:
        raise RuntimeError("short-term SCC25 CTX source identity is incomplete")

    main = chronic["main_timecourse"]
    if len(main) != 22:
        raise RuntimeError("chronic main trajectory is not exactly 22 frozen states")
    if {row["week"] for row in main} != set(range(1, 12)):
        raise RuntimeError("chronic week identity mismatch")
    if {row["arm"] for row in main} != {"PBS", "CTX"}:
        raise RuntimeError("chronic arm identity mismatch")

    bindings = chronic.get("processed_source_bindings", {})
    required_bindings = {
        "rna_sample_metadata": "36fe26fb75134f05cabbf63fb3e18859204748e166963a7f34a27576fff304f0",
        "rna_processed_molecular_source": "8b69cab4612f4787bedbc9ce9414ba321fc1c4bcba7ac63d50687e42d8a1b474",
        "methylation_processed_matrix": "2bc72da999dfcd4601909979ce0559948f445915484b6b3a35c386ca71c1e885",
    }
    for key, expected in required_bindings.items():
        actual = bindings.get(key, {}).get("sha256")
        if actual != expected:
            raise RuntimeError(f"chronic source binding mismatch for {key}: {actual!r}")

    expected_short_sha = "c1318f5ad3b62d26c043de370cdca7300548337918f4543b13769bbe7a08a6c2"
    if colmap.get("processed_file_sha256") != expected_short_sha:
        raise RuntimeError("short-term processed RNA source hash binding mismatch")

    return {
        "status": "PASS_FROZEN_SOURCE_MANIFESTS",
        "short_term_scc25_states": 11,
        "chronic_scc25_states": 22,
        "short_term_processed_rna_sha256": expected_short_sha,
        "chronic_rna_processed_sha256": required_bindings["rna_processed_molecular_source"],
        "chronic_methylation_processed_sha256": required_bindings["methylation_processed_matrix"],
        "real_molecular_files_opened": False,
    }


def verify_local_source_files(source_root: Path) -> dict[str, Any]:
    """Verify exact files only after the scientific freeze already passed."""

    required = {
        "GSE114446_STCCountsCG.txt.gz": "c1318f5ad3b62d26c043de370cdca7300548337918f4543b13769bbe7a08a6c2",
        "GSE98812_GEOExprsData.txt.gz": "8b69cab4612f4787bedbc9ce9414ba321fc1c4bcba7ac63d50687e42d8a1b474",
        "GSE98812_series_matrix.txt.gz": "36fe26fb75134f05cabbf63fb3e18859204748e166963a7f34a27576fff304f0",
        "GSE98813_series_matrix.txt.gz": "2bc72da999dfcd4601909979ce0559948f445915484b6b3a35c386ca71c1e885",
    }
    result: dict[str, Any] = {"status": "PASS", "files": {}}
    for filename, expected in required.items():
        path = source_root / filename
        if not path.exists():
            result["status"] = "FAIL"
            result["files"][filename] = {"status": "MISSING", "expected_sha256": expected}
            continue
        actual = _sha256(path)
        ok = actual == expected
        if not ok:
            result["status"] = "FAIL"
        result["files"][filename] = {
            "status": "PASS" if ok else "HASH_MISMATCH",
            "expected_sha256": expected,
            "actual_sha256": actual,
        }
    if result["status"] != "PASS":
        raise RuntimeError("one or more local empirical source files are missing or hash-mismatched")
    return result


def run_preflight(freeze_path: Path, source_root: Path | None = None) -> dict[str, Any]:
    freeze = _load_json(freeze_path)

    # Critical ordering: no real source path is touched before this passes.
    validate_empirical_freeze(freeze)

    source_manifest = validate_source_manifests()
    local = None
    if source_root is not None:
        local = verify_local_source_files(source_root)

    return {
        "status": "PASS_EMPIRICAL_EXECUTION_PREFLIGHT_NO_ANALYSIS_RUN",
        "freeze_id": freeze["freeze_id"],
        "freeze_path": str(freeze_path),
        "source_manifest_validation": source_manifest,
        "local_source_validation": local,
        "state_reduction_run": False,
        "transition_model_fit": False,
        "chi_bio_value_computed": False,
        "message": "Preflight passed. A separate outcome-bearing runner is still required and is not invoked here.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", default=str(DEFAULT_FREEZE))
    parser.add_argument("--source-root", default=None)
    parser.add_argument(
        "--output",
        default="development_outputs/chi_bio_empirical_preflight/GRI_CHI_BIO_FIRST_EMPIRICAL_PREFLIGHT.json",
    )
    args = parser.parse_args()

    freeze_path = Path(args.freeze)
    source_root = Path(args.source_root) if args.source_root else None
    try:
        result = run_preflight(freeze_path, source_root)
        exit_code = 0
    except EmpiricalFreezeContractError as exc:
        result = {
            "status": "REFUSED_INCOMPLETE_OR_INVALID_SCIENTIFIC_FREEZE",
            "freeze_path": str(freeze_path),
            "reason": str(exc),
            "real_source_files_opened": False,
            "state_reduction_run": False,
            "transition_model_fit": False,
            "chi_bio_value_computed": False,
        }
        exit_code = 3
    except Exception as exc:
        result = {
            "status": "REFUSED_PREFLIGHT_FAILURE",
            "freeze_path": str(freeze_path),
            "reason": f"{type(exc).__name__}: {exc}",
            "state_reduction_run": False,
            "transition_model_fit": False,
            "chi_bio_value_computed": False,
        }
        exit_code = 2

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
