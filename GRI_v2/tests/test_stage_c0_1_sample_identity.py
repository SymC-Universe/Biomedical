import json
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).parents[1]))
from src import run_stage_c0_1_sample_identity as c01

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "config" / "stage_c0_1_sample_identity_plan.json"


def test_c0_1_contract_excludes_duplicate_roots_without_value_selection():
    p = json.loads(PLAN.read_text(encoding="utf-8"))
    rule = p["primary_sample_identity_rule"]
    assert p["status"] == "frozen_after_c0_schema_inventory_before_any_methylation_biological_association"
    assert rule["exact_root_admitted_only_if_source_column_count_equals"] == 1
    assert rule["duplicate_exact_root_action"] == "EXCLUDE_FROM_PRIMARY_C1"
    assert rule["duplicate_exact_root_beta_averaging_allowed"] is False
    assert rule["duplicate_exact_root_select_first_or_last_allowed"] is False
    assert rule["duplicate_exact_root_platform_selection_allowed"] is False
    assert rule["duplicate_exact_root_value_based_selection_allowed"] is False
    assert p["allowed_operations"]["read_beta_value_rows"] is False
    assert p["allowed_operations"]["biological_association"] is False
    assert p["constraints"]["chi_allowed"] is False


def test_header_inventory_and_duplicate_exclusion(tmp_path):
    source = tmp_path / "methyl.tsv"
    # The intentionally invalid payload after the first line demonstrates that
    # the C0.1 inventory reads the header only and does not need beta-value rows.
    source.write_bytes(
        b"probe\tTCGA-AA-0001-01A-X\tTCGA-AA-0002-01A-X\tTCGA-AA-0002-01A-Y\tTCGA-AA-0003-01A-X\tTCGA-AA-0004-01B-X\n"
        b"THIS_IS_NOT_A_VALID_BETA_MATRIX_AND_MUST_NOT_BE_READ"
    )
    inv = c01.read_header_inventory(source)
    assert inv["methylation_sample_columns"] == 5
    assert inv["primary_sample_columns"] == 5
    assert inv["unique_primary_sample_roots"] == 4
    assert inv["duplicate_primary_sample_roots"] == 1
    assert len(inv["duplicate_roots"]["TCGA-AA-0002-01A"]) == 2

    cache = tmp_path / "cache.npz"
    np.savez(
        cache,
        sample_ids=np.array([
            "TCGA-AA-0001-01A-01R",
            "TCGA-AA-0002-01A-01R",
            "TCGA-AA-0003-01A-01R",
            "TCGA-AA-0004-01A-01R",
        ], dtype=object),
        patient_ids=np.array([
            "TCGA-AA-0001",
            "TCGA-AA-0002",
            "TCGA-AA-0003",
            "TCGA-AA-0004",
        ], dtype=object),
        cancer_types=np.array(["X", "X", "Y", "Y"], dtype=object),
    )
    summary, rows = c01.calculate_stage_a_coverage(cache, inv)
    assert summary["unique_one_to_one_matched_stage_a_samples"] == 3
    assert summary["exact_unique_root_matches"] == 2
    assert summary["unique_patient_fallback_matches"] == 1
    assert summary["duplicate_root_stage_a_samples_excluded"] == 1
    assert summary["no_source_match_stage_a_samples"] == 0


def test_duplicate_root_is_not_rescued_by_patient_fallback(tmp_path):
    source = tmp_path / "methyl.tsv"
    source.write_text(
        "probe\tTCGA-AA-0002-01A-X\tTCGA-AA-0002-01A-Y\n",
        encoding="utf-8",
    )
    inv = c01.read_header_inventory(source)
    cache = tmp_path / "cache.npz"
    np.savez(
        cache,
        sample_ids=np.array(["TCGA-AA-0002-01A-01R"], dtype=object),
        patient_ids=np.array(["TCGA-AA-0002"], dtype=object),
        cancer_types=np.array(["X"], dtype=object),
    )
    summary, _ = c01.calculate_stage_a_coverage(cache, inv)
    assert summary["unique_one_to_one_matched_stage_a_samples"] == 0
    assert summary["duplicate_root_stage_a_samples_excluded"] == 1
    assert summary["unique_patient_fallback_matches"] == 0
