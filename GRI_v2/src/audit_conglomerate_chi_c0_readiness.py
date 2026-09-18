from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

CONFIG_REL = Path("GRI_v2/config/gri_conglomerate_chi_tool_v1_development_20260918.json")
OUTPUT_REL = Path("GRI_v2/artifacts/GRI_CONGLOMERATE_CHI_C0_READINESS_20260918.json")


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def evaluate_block(repo_root: Path, block: Dict[str, Any]) -> Dict[str, Any]:
    refs = list(block.get("source_refs", []))
    ref_rows: List[Dict[str, Any]] = []
    missing: List[str] = []

    for ref in refs:
        p = repo_root / ref
        exists = p.is_file()
        ref_rows.append({"path": ref, "present": exists})
        if not exists:
            missing.append(ref)

    patient_state = block.get("patient_level_repo_state", "UNSPECIFIED")
    compact_ready = len(missing) == 0

    if not compact_ready:
        readiness = "BLOCKED_MISSING_COMPACT_PROVENANCE"
    elif patient_state in {
        "HEAVY_SOURCE_OR_CACHE_REQUIRED",
        "EXISTING_C1_HEAVY_ARTIFACT_OR_SOURCE_REMATERIALIZATION_REQUIRED",
        "CURRENT_COMPACT_RESULT_PRESENT_PATIENT_LEVEL_SOURCE_REQUIRED_FOR_REBUILD",
    }:
        readiness = "COMPACT_PROVENANCE_READY_HEAVY_MATERIALIZATION_PENDING"
    elif patient_state == "SYSTEM_SPECIFIC_ORDERED_DATA_ONLY":
        readiness = "SYSTEM_SPECIFIC_ORDERED_DATA_READY_BY_SYSTEM"
    else:
        readiness = "COMPACT_PROVENANCE_READY_REVIEW_PATIENT_MATERIALIZATION"

    return {
        "block_id": block["id"],
        "name": block["name"],
        "source_refs": ref_rows,
        "missing_source_refs": missing,
        "patient_level_repo_state": patient_state,
        "readiness": readiness,
    }


def build_readiness(repo_root: Path) -> Dict[str, Any]:
    config_path = repo_root / CONFIG_REL
    if not config_path.is_file():
        raise FileNotFoundError(f"Missing freeze config: {CONFIG_REL}")

    cfg = load_json(config_path)
    blocks = [evaluate_block(repo_root, b) for b in cfg["blocks"]]

    missing_refs = sorted(
        {
            ref
            for block in blocks
            for ref in block["missing_source_refs"]
        }
    )

    compact_ready_count = sum(not b["missing_source_refs"] for b in blocks)
    heavy_pending_count = sum(
        b["readiness"] == "COMPACT_PROVENANCE_READY_HEAVY_MATERIALIZATION_PENDING"
        for b in blocks
    )

    final_summary_rel = Path("GRI_v2/config/tool_prediction_p0_final_internal_summary_20260906.json")
    final_summary_path = repo_root / final_summary_rel
    final_summary = load_json(final_summary_path) if final_summary_path.is_file() else None

    safeguards = {
        "capital_chi_not_universal_scalar": cfg["definition"]["universal_scalar_required"] is False,
        "damped_oscillator_not_required": cfg["definition"]["damped_oscillator_required"] is False,
        "unity_boundary_not_required": cfg["definition"]["unity_boundary_required"] is False,
        "master_score_not_required": cfg["definition"]["master_score_required"] is False,
        "tcga_final_holdout_marked_opened": cfg["tcga_status"]["prior_final_holdout_opened"] is True,
        "new_conglomerate_tcga_role_is_development_only":
            cfg["tcga_status"]["role_for_new_conglomerate_v1"]
            == "DEVELOPMENT_AND_INTERNAL_QUALIFICATION_ONLY",
        "prior_internal_predictive_summary_present": final_summary is not None,
    }

    if final_summary is not None:
        safeguards["prior_internal_predictor_closed"] = (
            final_summary.get("status") == "INTERNAL_P0_CLOSED"
        )
        safeguards["prior_final_primary_evaluable_cancers"] = (
            final_summary.get("final_holdout", {}).get("primary_evaluable_cancers")
        )
        safeguards["prior_all_methylation_better_cancers"] = (
            final_summary.get("p1", {}).get("all_methylation_better_cancers")
        )

    all_boolean_safeguards_pass = all(
        value is True for value in safeguards.values() if isinstance(value, bool)
    )

    if missing_refs:
        overall = "BLOCKED_COMPACT_PROVENANCE_GAPS"
    elif not all_boolean_safeguards_pass:
        overall = "BLOCKED_SAFEGUARD_FAILURE"
    else:
        overall = "C0_READY_C1_HEAVY_MATERIALIZATION_NEXT"

    return {
        "schema": "gri-conglomerate-chi-c0-readiness-v1",
        "date": "2026-09-18",
        "status": overall,
        "definition": "capital-Chi biological stability architecture; no universal scalar or oscillator premise",
        "config": str(CONFIG_REL),
        "blocks_total": len(blocks),
        "blocks_with_compact_provenance_ready": compact_ready_count,
        "blocks_with_heavy_materialization_pending": heavy_pending_count,
        "missing_compact_source_refs": missing_refs,
        "blocks": blocks,
        "safeguards": safeguards,
        "execution": {
            "github_lightweight_c0": "READY",
            "github_patient_level_conglomerate_compute": (
                "NOT_YET_MATERIALIZED_FROM_CURRENT_PUBLIC_REPO"
            ),
            "heavy_compute_package": "NEXT_AFTER_EXACT_ARTIFACT_SOURCE_RESOLUTION",
            "kaggle_or_equivalent_heavy_compute": "SUITABLE_AFTER_PACKAGE_FREEZE",
            "user_local_compute_required_now": False,
        },
        "next_actions": [
            "resolve exact heavy artifact/source path for each patient-level block",
            "build environment-independent C1 materialization package",
            "materialize long-form block table without cross-block aggregation",
            "freeze C3 internal ablation only after C1/C2 carrier schema validation",
            "freeze external diagnostic and predictive tasks only after carrier materialization",
        ],
    }


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    result = build_readiness(repo_root)
    output_path = repo_root / OUTPUT_REL
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, indent=2, sort_keys=True)
        f.write("\n")

    print(json.dumps({
        "status": result["status"],
        "blocks_total": result["blocks_total"],
        "compact_ready": result["blocks_with_compact_provenance_ready"],
        "heavy_pending": result["blocks_with_heavy_materialization_pending"],
        "missing_compact_source_refs": result["missing_compact_source_refs"],
        "output": str(OUTPUT_REL),
    }, indent=2))


if __name__ == "__main__":
    main()
