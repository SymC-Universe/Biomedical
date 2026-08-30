import json
from pathlib import Path

import numpy as np
import sys
sys.path.insert(0, str(Path(__file__).parents[1]))

from src import probe_stage_c0_methylation as c0

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "config" / "stage_c0_methylation_source_plan.json"


def test_plan_freezes_source_without_association():
    p = json.loads(PLAN.read_text())
    assert p["status"] == "frozen_after_stage_b2_static_closure_before_methylation_download_or_association"
    assert p["primary_source"]["gdc_uuid"] == "d82e2c44-89eb-43d9-b6d3-712732bf6a53"
    assert p["primary_source"]["expected_content_length_bytes"] == 5022150019
    assert p["primary_source"]["expected_shared_probe_count"] == 22601
    assert p["primary_source"]["expected_md5"] == "5cec086f0b002d17befef76a3241e73b"
    assert p["constraints"]["chi_allowed"] is False
    assert p["constraints"]["composite_stability_score_allowed"] is False
    assert p["constraints"]["substrate_inheritance_claim_allowed"] is False
    assert p["annotation_gate"]["association_before_annotation_freeze"] is False
    assert set(p["stage_c1_required_architecture"]) == {"modal", "scalar", "conglomeration", "complementarity_rule"}


def test_matrix_inventory_and_stage_a_matching(tmp_path):
    matrix = tmp_path / "m.tsv"
    matrix.write_text(
        "probe\tTCGA-AA-0001-01A\tTCGA-AA-0002-01A\tTCGA-AA-0003-02A\n"
        "cg1\t0.1\t0.2\t0.3\n"
        "cg2\t0.2\t0.3\t0.4\n"
        "cg3\t0.3\t0.4\t0.5\n",
        encoding="utf-8",
    )
    info = c0.inspect_matrix(matrix, expected_probe_count=3)
    assert info["probe_rows"] == 3
    assert info["unique_primary_sample_roots"] == 2
    assert info["duplicate_primary_sample_roots"] == 0

    cache = tmp_path / "cache.npz"
    np.savez(
        cache,
        sample_ids=np.array(["TCGA-AA-0001-01A-01R", "TCGA-AA-0002-01A-01R", "TCGA-AA-0004-01A-01R"], dtype=object),
        patient_ids=np.array(["TCGA-AA-0001", "TCGA-AA-0002", "TCGA-AA-0004"], dtype=object),
        cancer_types=np.array(["X", "X", "Y"], dtype=object),
    )
    cov = c0.stage_a_coverage(cache, info)
    assert cov["matched_stage_a_samples"] == 2
    assert cov["exact_sample_root_matches"] == 2
    assert cov["unique_patient_fallback_matches"] == 0


def test_duplicate_probe_ids_are_rejected(tmp_path):
    matrix = tmp_path / "dup.tsv"
    matrix.write_text(
        "probe\tTCGA-AA-0001-01A\n"
        "cg1\t0.1\n"
        "cg1\t0.2\n",
        encoding="utf-8",
    )
    try:
        c0.inspect_matrix(matrix, expected_probe_count=2)
    except ValueError as exc:
        assert "duplicate probe" in str(exc).lower()
    else:
        raise AssertionError("duplicate probe IDs should fail the frozen source gate")
