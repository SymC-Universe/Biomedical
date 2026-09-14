from __future__ import annotations

"""Post-result bounded robustness audit for the frozen chronic G2 test.

The primary threshold (source_value >= 1 in >=6/11 PBS states) is immutable.
This script evaluates only the two thresholds that were recorded before chronic
CTX opening by the PBS-only design-input probe: 0.1 and 10. Both are reported;
neither may replace, rescue, or demote the primary result.
"""

from io import BytesIO
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.run_chi_bio_chronic_g2_empirical import (
    CTX_COLUMNS,
    DEFAULT_FREEZE,
    EXPECTED_ROWS,
    EXPECTED_SAMPLE_COLUMNS,
    PBS_COLUMNS,
    _download_source,
    _material,
    _overall_disposition,
    _run_rank,
    _validate_freeze,
)


OUTPUT = Path(
    "development_outputs/chi_bio_chronic_g2_feature_gate_robustness/"
    "GRI_CHI_BIO_CHRONIC_G2_FEATURE_GATE_ROBUSTNESS.json"
)

DIAGNOSTIC_GATES = {
    "0.1": {
        "threshold": 0.1,
        "retained_gene_count": 15_830,
        "retained_gene_ids_sha256": "79b594d3e0ff808ac9a428230dc9810f7db61153eb4a20b4b033f0f16c97de2b",
    },
    "10.0": {
        "threshold": 10.0,
        "retained_gene_count": 12_865,
        "retained_gene_ids_sha256": "b565fb09aac42b98d11436a629356bed418f24cf34a3dda1d443b5642ceacc25",
    },
}

PRIMARY_REFERENCE = {
    "threshold": 1.0,
    "overall_disposition": "REPRESENTATION_DEPENDENT_NO_TRANSFER",
    "material_conclusions_by_rank": {
        "2": {
            "d1_adequacy": "PASS",
            "d1_mathematical_unit_circle_side": "BELOW",
            "d1_nonnormal_warning": "ABSENT",
            "d2_reorganization_support": "NOT_SUPPORTED",
        },
        "3": {
            "d1_adequacy": "PASS",
            "d1_mathematical_unit_circle_side": "BELOW",
            "d1_nonnormal_warning": "INDETERMINATE",
            "d2_reorganization_support": "NOT_SUPPORTED",
        },
    },
}


def _gene_hash(values: list[str]) -> str:
    return hashlib.sha256("\n".join(values).encode("utf-8")).hexdigest()


def _load_source_for_gate(payload: bytes, freeze: dict, gate: dict) -> tuple[np.ndarray, np.ndarray, dict]:
    observed_sha = hashlib.sha256(payload).hexdigest()
    expected_sha = freeze["source_binding"]["processed_file_sha256"]
    if observed_sha != expected_sha:
        raise RuntimeError(f"source hash mismatch: {observed_sha} != {expected_sha}")

    raw = gzip.decompress(payload)
    frame = pd.read_csv(BytesIO(raw), sep="\t", low_memory=False)
    if frame.shape != (EXPECTED_ROWS, EXPECTED_SAMPLE_COLUMNS + 1):
        raise RuntimeError(f"processed table shape mismatch: {frame.shape}")
    genes = frame.iloc[:, 0].astype(str).str.strip()
    if genes.eq("").any() or genes.eq("nan").any() or genes.duplicated().any():
        raise RuntimeError("invalid GENE identifiers")

    columns = list(PBS_COLUMNS) + list(CTX_COLUMNS)
    values = frame.loc[:, columns].apply(pd.to_numeric, errors="raise").to_numpy(dtype=np.float64)
    if not np.all(np.isfinite(values)) or np.any(values < 0.0):
        raise RuntimeError("nonfinite or negative chronic source value")

    threshold = float(gate["threshold"])
    keep = np.sum(values[:, :11] >= threshold, axis=1) >= 6
    ids = genes.to_numpy(dtype=str)[keep].tolist()
    count = int(np.sum(keep))
    digest = _gene_hash(ids)
    if count != int(gate["retained_gene_count"]):
        raise RuntimeError(f"diagnostic gate count drift at {threshold}: {count}")
    if digest != gate["retained_gene_ids_sha256"]:
        raise RuntimeError(f"diagnostic gate gene-ID hash drift at {threshold}")

    transformed = np.log2(values[keep, :] + 1.0).T
    metadata = {
        "threshold": threshold,
        "retained_gene_count": count,
        "retained_gene_ids_sha256": digest,
    }
    return transformed[:11], transformed[11:], metadata


def run_audit() -> dict:
    freeze = json.loads(DEFAULT_FREEZE.read_text(encoding="utf-8"))
    _validate_freeze(freeze)
    if freeze["feature_gate_preoutcome_qualification"]["diagnostic_thresholds_not_eligible_for_postprobe_switch"] != [0.1, 10.0]:
        raise RuntimeError("pre-outcome diagnostic threshold contract drift")

    payload, history = _download_source()
    results: dict[str, dict] = {}
    for label, gate in DIAGNOSTIC_GATES.items():
        pbs, ctx, metadata = _load_source_for_gate(payload, freeze, gate)
        by_rank = {str(rank): _run_rank(pbs, ctx, rank) for rank in (2, 3)}
        material = {key: _material(value) for key, value in by_rank.items()}
        results[label] = {
            "gate": metadata,
            "by_rank": by_rank,
            "material_conclusions_by_rank": material,
            "overall_disposition": _overall_disposition(material),
        }

    primary_core = {
        rank: {
            "d1_adequacy": values["d1_adequacy"],
            "d1_mathematical_unit_circle_side": values["d1_mathematical_unit_circle_side"],
            "d2_reorganization_support": values["d2_reorganization_support"],
        }
        for rank, values in PRIMARY_REFERENCE["material_conclusions_by_rank"].items()
    }
    core_match: dict[str, bool] = {}
    for label, result in results.items():
        diag_core = {
            rank: {
                "d1_adequacy": values["d1_adequacy"],
                "d1_mathematical_unit_circle_side": values["d1_mathematical_unit_circle_side"],
                "d2_reorganization_support": values["d2_reorganization_support"],
            }
            for rank, values in result["material_conclusions_by_rank"].items()
        }
        core_match[label] = diag_core == primary_core

    return {
        "status": "COMPLETE_POSTRESULT_BOUNDED_FEATURE_GATE_ROBUSTNESS",
        "protocol_authority": freeze["protocol_authority"],
        "freeze_id": freeze["freeze_id"],
        "primary_result_immutable": True,
        "primary_threshold_retested_or_reselected": False,
        "diagnostic_thresholds_predeclared_before_ctx_opening": [0.1, 10.0],
        "all_diagnostic_thresholds_reported": True,
        "primary_reference": PRIMARY_REFERENCE,
        "diagnostic_results": results,
        "core_conclusions_match_primary": core_match,
        "source_sha256": freeze["source_binding"]["processed_file_sha256"],
        "download_attempt_history": history,
        "chi_bio_computed": False,
        "chi_bio_status": "NOT_ADMITTED",
        "biological_unity_boundary_admitted": False,
        "promotion_effect": "NONE_DIAGNOSTIC_ROBUSTNESS_ONLY",
    }


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    try:
        report = run_audit()
        OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    except Exception as exc:
        failure = {
            "status": "REFUSE_POSTRESULT_BOUNDED_FEATURE_GATE_ROBUSTNESS",
            "reason": f"{type(exc).__name__}: {exc}",
            "primary_result_immutable": True,
            "chi_bio_status": "NOT_ADMITTED",
        }
        OUTPUT.write_text(json.dumps(failure, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(failure, indent=2, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
