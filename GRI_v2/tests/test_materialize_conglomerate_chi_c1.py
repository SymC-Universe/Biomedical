import csv
from pathlib import Path

import pytest

from src.materialize_conglomerate_chi_c1 import (
    CarrierValidationError,
    load_schema,
    materialize,
    read_and_validate_csv,
)


def base_row(**updates):
    row = {
        "entity_id": "TCGA-XX-0001",
        "cohort_id": "TCGA_PANCAN",
        "system_id": "BRCA",
        "sample_id": "TCGA-XX-0001-01A",
        "block_id": "R",
        "feature_id": "HALLMARK_A",
        "value": "0.25",
        "value_status": "DERIVED_FROZEN",
        "uncertainty_value": "",
        "uncertainty_kind": "NONE",
        "local_embedded_role": "LOCAL",
        "time_index": "",
        "time_order_known": "FALSE",
        "evidence_class": "P0-Q",
        "independence_role": "DEVELOPMENT",
        "source_id": "STAGE_A_PROFILE_CACHE",
        "source_digest_or_run": "sha256:test",
        "transform_id": "STAGE_A_FROZEN",
    }
    row.update(updates)
    return row


def write_rows(path: Path, rows, columns=None):
    schema = load_schema()
    fields = columns or schema["required_columns"]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def test_materializer_preserves_blocks_without_master_score(tmp_path):
    a = tmp_path / "static.csv"
    b = tmp_path / "temporal.csv"

    write_rows(
        a,
        [
            base_row(),
            base_row(
                block_id="E",
                feature_id="ABSOLUTE_PURITY",
                value="0.71",
                local_embedded_role="CONTEXT",
                source_id="ABSOLUTE_PURITY",
                transform_id="RAW",
            ),
            base_row(
                block_id="S",
                feature_id="METHYLATION_HALLMARK_A",
                value_status="MISSING",
                value="",
                local_embedded_role="EMBEDDED",
                source_id="STAGE_C1",
                transform_id="C1_FROZEN",
            ),
        ],
    )
    write_rows(
        b,
        [
            base_row(
                entity_id="SCC25",
                cohort_id="SCC25_CHRONIC",
                system_id="SCC25",
                sample_id="WEEK_01",
                block_id="T",
                feature_id="G2_SPECTRAL_RADIUS",
                value="0.91",
                value_status="DERIVED_FROZEN",
                local_embedded_role="TEMPORAL",
                time_index="1",
                time_order_known="TRUE",
                source_id="G2_CHRONIC",
                source_digest_or_run="run:34769901215",
                transform_id="G2_R2_FROZEN",
            )
        ],
    )

    outdir = tmp_path / "out"
    manifest = materialize([a, b], outdir)

    assert manifest["status"] == "C1_CARRIER_MATERIALIZED_SCHEMA_VALID"
    assert manifest["rows_total"] == 4
    assert manifest["rows_by_block"] == {"E": 1, "R": 1, "S": 1, "T": 1}
    assert manifest["cross_block_aggregation_performed"] is False
    assert manifest["master_score_created"] is False
    assert manifest["diagnostic_or_predictive_model_fit"] is False

    header = (outdir / "conglomerate_carrier_long.csv").read_text(encoding="utf-8").splitlines()[0]
    assert "master_score" not in header
    assert "Chi_bio_value" not in header


def test_missing_value_cannot_be_numeric_zero(tmp_path):
    p = tmp_path / "bad_missing.csv"
    write_rows(p, [base_row(value_status="MISSING", value="0")])
    with pytest.raises(CarrierValidationError, match="requires blank value"):
        read_and_validate_csv(p, load_schema())


def test_duplicate_key_is_hard_error(tmp_path):
    p = tmp_path / "duplicate.csv"
    row = base_row()
    write_rows(p, [row, dict(row)])
    with pytest.raises(CarrierValidationError, match="duplicate carrier key"):
        read_and_validate_csv(p, load_schema())


def test_forbidden_master_score_column_is_hard_error(tmp_path):
    schema = load_schema()
    p = tmp_path / "forbidden.csv"
    fields = list(schema["required_columns"]) + ["master_score"]
    row = base_row()
    row["master_score"] = "1.0"
    write_rows(p, [row], fields)
    with pytest.raises(CarrierValidationError, match="forbidden columns"):
        read_and_validate_csv(p, schema)


def test_numeric_temporal_block_requires_observed_order(tmp_path):
    p = tmp_path / "bad_temporal.csv"
    write_rows(
        p,
        [
            base_row(
                block_id="T",
                feature_id="TEMP",
                time_order_known="FALSE",
                time_index="",
                local_embedded_role="TEMPORAL",
            )
        ],
    )
    with pytest.raises(CarrierValidationError, match="requires directly observed ordering"):
        read_and_validate_csv(p, load_schema())


def test_time_index_cannot_exist_without_known_order(tmp_path):
    p = tmp_path / "bad_time_index.csv"
    write_rows(p, [base_row(time_index="1", time_order_known="FALSE")])
    with pytest.raises(CarrierValidationError, match="time_index populated"):
        read_and_validate_csv(p, load_schema())
