from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from src.run_tool_prediction_p0_eligibility import expected_partition, run, split_bucket


def write_manifest(path: Path, rows: list[dict[str, str]]) -> None:
    fields = [
        "cancer_type", "participant_root", "stage_a_sample_id", "stage_a_patient_id",
        "methylation_source_label", "methylation_sample_root", "match_type", "split_bucket", "partition"
    ]
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_split_partition_mapping():
    assert expected_partition(0) == "DISCOVERY"
    assert expected_partition(6) == "REPLICATION"
    assert expected_partition(9) == "FINAL_HOLDOUT"


def test_small_eligibility_run(tmp_path: Path):
    ns = "GRI_V2_PREDICTION_P0_20260830"
    participants = ["TCGA-AA-0001", "TCGA-AA-0002", "TCGA-AA-0003"]
    rows = []
    for pid in participants:
        cancer = "TEST"
        b = split_bucket(ns, cancer, pid)
        rows.append({
            "cancer_type": cancer,
            "participant_root": pid,
            "stage_a_sample_id": pid + "-01A-X",
            "stage_a_patient_id": pid,
            "methylation_source_label": f'"{pid}-01A-X"',
            "methylation_sample_root": pid + "-01A",
            "match_type": "EXACT_UNIQUE_SAMPLE_ROOT",
            "split_bucket": str(b),
            "partition": expected_partition(b),
        })
    manifest = tmp_path / "manifest.csv"
    write_manifest(manifest, rows)

    source = tmp_path / "meth.tsv"
    source.write_text(
        "probe\t\"TCGA-AA-0001-01A-X\"\t\"TCGA-AA-0002-01A-X\"\t\"TCGA-AA-0003-01A-X\"\n"
        "cg1\t0.1\t0.1\tNA\n"
        "cg2\t0.2\t0.2\tNA\n"
        "cg3\t0.3\t0.3\tNA\n"
        "cg4\t0.4\tNA\tNA\n",
        encoding="utf-8",
    )
    part_counts = {}
    for r in rows:
        part_counts[r["partition"]] = part_counts.get(r["partition"], 0) + 1
    cfg = {
        "p0_split_manifest_sha256": sha(manifest),
        "p0_split_records": 3,
        "p0_split_cancers": 1,
        "split_namespace": ns,
        "methylation_source_size_bytes": source.stat().st_size,
        "methylation_source_sha256_locked_from_c0": "synthetic",
        "methylation_header_columns": 4,
        "methylation_sample_columns": 3,
        "primary_probe_count": 4,
        "sample_primary_finite_fraction_min": 0.75,
        "minimum_eligible_per_partition_per_cancer": 1,
        "pan_cancer_promotion_min_cancers": 1,
        "expected_preeligibility_partition_counts": part_counts,
        "partition_reassignment_allowed": False,
        "predictive_target_values_allowed": False,
        "biological_association_allowed": False,
        "stage_c1_science_modified": False,
    }
    cfg_path = tmp_path / "cfg.json"
    cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
    out = tmp_path / "out"
    result = run(cfg_path, manifest, source, out, chunksize=2)
    assert result["status"] == "P0_SAMPLE_ELIGIBILITY_COMPLETE"
    assert result["eligible_records"] == 2
    assert result["ineligible_records"] == 1
    assert result["predictive_target_values_read"] is False
    assert result["biological_association_performed"] is False


def test_manifest_hash_is_enforced(tmp_path: Path):
    cfg = {
        "p0_split_manifest_sha256": "0" * 64,
        "p0_split_records": 0,
        "p0_split_cancers": 0,
        "split_namespace": "x",
        "expected_preeligibility_partition_counts": {},
        "partition_reassignment_allowed": False,
        "predictive_target_values_allowed": False,
        "biological_association_allowed": False,
    }
    cfg_path = tmp_path / "cfg.json"
    cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
    manifest = tmp_path / "manifest.csv"
    manifest.write_text("x\n", encoding="utf-8")
    source = tmp_path / "source.tsv"
    source.write_text("p\n", encoding="utf-8")
    try:
        run(cfg_path, manifest, source, tmp_path / "out")
    except ValueError as exc:
        assert "manifest SHA mismatch" in str(exc)
    else:
        raise AssertionError("manifest SHA mismatch was not enforced")
