from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from src.run_stage_c0_1_sample_identity import (
    normalize_barcode,
    patient_id,
    read_header_inventory,
    sample_root,
    sha256_file,
    validate_locked_inputs,
)

SPLIT_NAMESPACE = "GRI_V2_PREDICTION_P0_20260830"
PARTITION_BY_BUCKET = {
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


def split_bucket(cancer: str, participant_root: str) -> int:
    token = f"{SPLIT_NAMESPACE}|{cancer}|{participant_root}"
    digest = hashlib.sha256(token.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big", signed=False) % 10


def split_partition(cancer: str, participant_root: str) -> tuple[int, str]:
    bucket = split_bucket(cancer, participant_root)
    return bucket, PARTITION_BY_BUCKET[bucket]


def _normalized_participant_root(value: str) -> str:
    pid = patient_id(value)
    if pid is None:
        raise ValueError(f"cannot parse TCGA participant root from {value!r}")
    return normalize_barcode(pid)


def match_records_from_arrays(
    sample_ids: np.ndarray,
    patient_ids: np.ndarray,
    cancer_types: np.ndarray,
    inventory: dict,
) -> tuple[list[dict[str, object]], dict[str, int]]:
    if not (len(sample_ids) == len(patient_ids) == len(cancer_types)):
        raise ValueError("Stage A cache identity arrays differ in length")

    root_to_labels = inventory["root_to_labels"]
    patient_to_labels = inventory["patient_to_labels"]
    records: list[dict[str, object]] = []
    excluded = Counter()

    for sample_id_raw, patient_id_raw, cancer_raw in zip(sample_ids, patient_ids, cancer_types):
        stage_a_sample_id = str(sample_id_raw)
        stage_a_patient_id = normalize_barcode(str(patient_id_raw))
        cancer = str(cancer_raw)
        stage_a_root = sample_root(stage_a_sample_id)

        source_label: str | None = None
        source_root: str | None = None
        match_type: str | None = None

        root_labels = root_to_labels.get(stage_a_root, []) if stage_a_root else []
        if len(root_labels) == 1:
            source_label = str(root_labels[0])
            source_root = stage_a_root
            match_type = "EXACT_UNIQUE_SAMPLE_ROOT"
        elif len(root_labels) > 1:
            excluded["duplicate_source_sample_root"] += 1
            continue
        else:
            patient_labels = patient_to_labels.get(stage_a_patient_id, [])
            if len(patient_labels) == 1:
                source_label = str(patient_labels[0])
                source_root = sample_root(source_label)
                match_type = "UNIQUE_PATIENT_FALLBACK"
            elif len(patient_labels) > 1:
                excluded["nonunique_patient_fallback"] += 1
                continue
            else:
                excluded["no_source_match"] += 1
                continue

        if source_root is None or source_label is None or match_type is None:
            raise AssertionError("matched record missing source identity")

        participant_root = _normalized_participant_root(stage_a_patient_id)
        source_participant = _normalized_participant_root(source_root)
        if participant_root != source_participant:
            raise ValueError(
                f"participant mismatch after C0.1 matching: Stage A {participant_root} vs methylation {source_participant}"
            )

        bucket, partition = split_partition(cancer, participant_root)
        records.append(
            {
                "cancer_type": cancer,
                "participant_root": participant_root,
                "stage_a_sample_id": stage_a_sample_id,
                "stage_a_patient_id": stage_a_patient_id,
                "methylation_source_label": source_label,
                "methylation_sample_root": source_root,
                "match_type": match_type,
                "split_bucket": bucket,
                "partition": partition,
            }
        )

    participant_counts = Counter(str(r["participant_root"]) for r in records)
    duplicates = sorted(pid for pid, count in participant_counts.items() if count != 1)
    if duplicates:
        raise ValueError(
            "participant-level leakage firewall failed; matched universe contains duplicate participant roots: "
            + ", ".join(duplicates[:20])
        )

    return records, dict(excluded)


def load_matched_records(cache_path: Path, inventory: dict) -> tuple[list[dict[str, object]], dict[str, int]]:
    z = np.load(cache_path, allow_pickle=True)
    sample_ids = z["sample_ids"].astype(str)
    patient_ids_arr = z["patient_ids"].astype(str)
    cancer_types = z["cancer_types"].astype(str)
    return match_records_from_arrays(sample_ids, patient_ids_arr, cancer_types, inventory)


def _validate_freezes(config: dict, identity_plan: dict) -> None:
    src = config["sources"]
    frozen = identity_plan["frozen_inputs"]
    checks = {
        "methylation_source_sha256": src["methylation_sha256"],
        "stage_a_profile_cache_sha256": src["rna_cache_sha256"],
    }
    for plan_key, expected in checks.items():
        actual = frozen[plan_key]
        if actual != expected:
            raise ValueError(f"P0/C0.1 frozen identity mismatch for {plan_key}: {actual} != {expected}")

    part = config["partition"]
    if part["unit"] != "participant_root":
        raise ValueError("P0 partition unit drift")
    if part["reassignment_allowed"] is not False:
        raise ValueError("P0 split reassignment must remain forbidden")
    if list(part["discovery_buckets"]) != [0, 1, 2, 3, 4, 5]:
        raise ValueError("P0 discovery bucket drift")
    if list(part["replication_buckets"]) != [6, 7]:
        raise ValueError("P0 replication bucket drift")
    if list(part["final_holdout_buckets"]) != [8, 9]:
        raise ValueError("P0 final-holdout bucket drift")


def _partition_counts(records: list[dict[str, object]]) -> tuple[list[dict[str, object]], dict[str, int]]:
    per_cancer: dict[str, Counter] = defaultdict(Counter)
    overall = Counter()
    for row in records:
        cancer = str(row["cancer_type"])
        partition = str(row["partition"])
        per_cancer[cancer][partition] += 1
        overall[partition] += 1

    rows: list[dict[str, object]] = []
    for cancer in sorted(per_cancer):
        counts = per_cancer[cancer]
        rows.append(
            {
                "cancer_type": cancer,
                "preeligibility_total": sum(counts.values()),
                "discovery_n": counts["DISCOVERY"],
                "replication_n": counts["REPLICATION"],
                "final_holdout_n": counts["FINAL_HOLDOUT"],
            }
        )
    return rows, dict(overall)


def run(
    config_path: Path,
    identity_plan_path: Path,
    cache_path: Path,
    source_path: Path,
    c0_summary_path: Path,
    out_dir: Path,
) -> dict[str, object]:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    identity_plan = json.loads(identity_plan_path.read_text(encoding="utf-8"))
    _validate_freezes(config, identity_plan)

    locked = validate_locked_inputs(identity_plan, cache_path, source_path, c0_summary_path)
    inventory = read_header_inventory(source_path)
    expected_schema = identity_plan["observed_c0_schema_facts"]
    for key in (
        "methylation_sample_columns",
        "primary_sample_columns",
        "unique_primary_sample_roots",
        "duplicate_primary_sample_roots",
    ):
        if int(inventory[key]) != int(expected_schema[key]):
            raise ValueError(f"C0 header schema drift for {key}: {inventory[key]} != {expected_schema[key]}")

    records, excluded = load_matched_records(cache_path, inventory)
    expected_samples = int(config["sources"]["matched_universe_samples"])
    expected_cancers = int(config["sources"]["matched_universe_cancers"])
    cancers = sorted({str(r["cancer_type"]) for r in records})
    if len(records) != expected_samples:
        raise ValueError(f"P0 matched-universe count drift: {len(records)} != {expected_samples}")
    if len(cancers) != expected_cancers:
        raise ValueError(f"P0 matched cancer count drift: {len(cancers)} != {expected_cancers}")

    records.sort(key=lambda r: (str(r["cancer_type"]), str(r["participant_root"])))
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = out_dir / "p0_preeligibility_split_manifest.csv"
    fields = [
        "cancer_type",
        "participant_root",
        "stage_a_sample_id",
        "stage_a_patient_id",
        "methylation_source_label",
        "methylation_sample_root",
        "match_type",
        "split_bucket",
        "partition",
    ]
    with manifest_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)

    counts_rows, overall = _partition_counts(records)
    counts_path = out_dir / "p0_preeligibility_partition_counts.csv"
    with counts_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["cancer_type", "preeligibility_total", "discovery_n", "replication_n", "final_holdout_n"],
        )
        writer.writeheader()
        writer.writerows(counts_rows)

    manifest_sha = sha256_file(manifest_path)
    counts_sha = sha256_file(counts_path)
    partition_check = Counter(str(r["partition"]) for r in records)
    if partition_check != Counter(overall):
        raise AssertionError("partition count reconstruction mismatch")
    if set(partition_check) != {"DISCOVERY", "REPLICATION", "FINAL_HOLDOUT"}:
        raise ValueError(f"one or more P0 partitions are empty: {dict(partition_check)}")

    summary: dict[str, object] = {
        "status": "P0_PREELIGIBILITY_SPLIT_MANIFEST_COMPLETE",
        "schema": "gri-v2-p0-preeligibility-split-manifest-v0.1",
        "split_namespace": SPLIT_NAMESPACE,
        "records": len(records),
        "cancers": len(cancers),
        "partition_counts": dict(sorted(partition_check.items())),
        "excluded_stage_a_records": excluded,
        "manifest_sha256": manifest_sha,
        "counts_sha256": counts_sha,
        "stage_a_profile_cache_sha256": locked["cache_sha256"],
        "c0_summary_sha256": locked["c0_summary_sha256"],
        "methylation_source_sha256_locked_from_c0": identity_plan["frozen_inputs"]["methylation_source_sha256"],
        "methylation_rows_read": False,
        "beta_value_rows_read_for_biological_analysis": False,
        "predictive_target_values_read": False,
        "partition_reassignment_performed": False,
        "stage_c1_science_modified": False,
        "biological_chi_used": False,
        "claim_ceiling": "participant identity and pre-eligibility P0 split assignment only",
        "next_gate": "apply frozen P0 eligibility and discovery-only preprocessing only after this manifest is hash-verified",
    }
    summary_path = out_dir / "P0_SPLIT_MANIFEST_SUMMARY.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=Path, required=True)
    ap.add_argument("--identity-plan", type=Path, required=True)
    ap.add_argument("--cache", type=Path, required=True)
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--c0-summary", type=Path, required=True)
    ap.add_argument("--out", type=Path, default=Path("tool_prediction_p0_split_outputs"))
    args = ap.parse_args()
    result = run(
        args.config,
        args.identity_plan,
        args.cache,
        args.source,
        args.c0_summary,
        args.out,
    )
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
