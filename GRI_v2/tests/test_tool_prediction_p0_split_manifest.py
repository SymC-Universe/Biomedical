from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from src.build_tool_prediction_p0_split_manifest import (
    PARTITION_BY_BUCKET,
    _validate_freezes,
    match_records_from_arrays,
    split_bucket,
    split_partition,
)

ROOT = Path(__file__).resolve().parents[1]


def test_split_bucket_known_frozen_examples() -> None:
    assert split_bucket("BRCA", "TCGA-A1-A0SB") == 1
    assert split_partition("BRCA", "TCGA-A1-A0SB") == (1, "DISCOVERY")

    assert split_bucket("LUAD", "TCGA-05-4244") == 7
    assert split_partition("LUAD", "TCGA-05-4244") == (7, "REPLICATION")

    assert split_bucket("GBM", "TCGA-02-0001") == 3
    assert split_partition("GBM", "TCGA-02-0001") == (3, "DISCOVERY")


def test_exact_and_unique_patient_fallback_preserve_participant_split_unit() -> None:
    inventory = {
        "root_to_labels": {
            "TCGA-A1-A0SB-01A": ["TCGA-A1-A0SB-01A"],
            "TCGA-02-0001-01A": ["TCGA-02-0001-01A", "TCGA-02-0001-01A.extra"],
        },
        "patient_to_labels": {
            "TCGA-A1-A0SB": ["TCGA-A1-A0SB-01A"],
            "TCGA-05-4244": ["TCGA-05-4244-01B"],
            "TCGA-02-0001": ["TCGA-02-0001-01A", "TCGA-02-0001-01B"],
        },
    }
    sample_ids = np.array([
        "TCGA-A1-A0SB-01A",
        "TCGA-05-4244-01A",
        "TCGA-02-0001-01A",
    ])
    patient_ids = np.array([
        "TCGA-A1-A0SB",
        "TCGA-05-4244",
        "TCGA-02-0001",
    ])
    cancers = np.array(["BRCA", "LUAD", "GBM"])

    records, excluded = match_records_from_arrays(sample_ids, patient_ids, cancers, inventory)
    assert len(records) == 2
    by_patient = {str(r["participant_root"]): r for r in records}

    assert by_patient["TCGA-A1-A0SB"]["match_type"] == "EXACT_UNIQUE_SAMPLE_ROOT"
    assert by_patient["TCGA-A1-A0SB"]["partition"] == "DISCOVERY"

    assert by_patient["TCGA-05-4244"]["match_type"] == "UNIQUE_PATIENT_FALLBACK"
    assert by_patient["TCGA-05-4244"]["methylation_sample_root"] == "TCGA-05-4244-01B"
    assert by_patient["TCGA-05-4244"]["partition"] == "REPLICATION"

    assert excluded == {"duplicate_source_sample_root": 1}


def test_duplicate_participant_roots_fail_closed() -> None:
    inventory = {
        "root_to_labels": {
            "TCGA-A1-A0SB-01A": ["TCGA-A1-A0SB-01A"],
            "TCGA-A1-A0SB-01B": ["TCGA-A1-A0SB-01B"],
        },
        "patient_to_labels": {
            "TCGA-A1-A0SB": ["TCGA-A1-A0SB-01A", "TCGA-A1-A0SB-01B"],
        },
    }
    sample_ids = np.array(["TCGA-A1-A0SB-01A", "TCGA-A1-A0SB-01B"])
    patient_ids = np.array(["TCGA-A1-A0SB", "TCGA-A1-A0SB"])
    cancers = np.array(["BRCA", "BRCA"])

    with pytest.raises(ValueError, match="participant-level leakage firewall failed"):
        match_records_from_arrays(sample_ids, patient_ids, cancers, inventory)


def test_p0_config_is_bound_to_c0_1_frozen_sources_and_partition_rule() -> None:
    config = json.loads((ROOT / "config" / "tool_prediction_p0_holdout_freeze_20260830.json").read_text())
    identity_plan = json.loads((ROOT / "config" / "stage_c0_1_sample_identity_plan.json").read_text())

    _validate_freezes(config, identity_plan)
    assert config["status"] == "FROZEN_BEFORE_P0_TARGET_VALUES"
    assert config["partition"]["reassignment_allowed"] is False
    assert config["partition"]["unit"] == "participant_root"
    assert config["c1_beta_value_biology_read"] is False
    assert config["biological_chi_used"] is False


def test_bucket_to_partition_map_is_exactly_the_frozen_60_20_20_rule() -> None:
    assert PARTITION_BY_BUCKET == {
        0: "DISCOVERY",
        1: "DISCOVERY",
        2: "DISCOVERY",
        3: "DISCOVERY",
        4: "DISCOVERY",
        5: "DISCOVERY",
        6: "REPLICATION",
        7: "REPLICATION",
        8: "FINAL_HOLDOUT",
        9: "FINAL_HOLDOUT",
    }
