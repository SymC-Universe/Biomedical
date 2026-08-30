from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

CHUNK_BYTES = 8 * 1024 * 1024


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(CHUNK_BYTES), b""):
            h.update(block)
    return h.hexdigest()


def split_bucket(namespace: str, cancer: str, participant_root: str) -> int:
    token = f"{namespace}|{cancer}|{participant_root}"
    digest = hashlib.sha256(token.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big", signed=False) % 10


def expected_partition(bucket: int) -> str:
    if 0 <= bucket <= 5:
        return "DISCOVERY"
    if 6 <= bucket <= 7:
        return "REPLICATION"
    if 8 <= bucket <= 9:
        return "FINAL_HOLDOUT"
    raise ValueError(f"invalid split bucket {bucket}")


def read_manifest(path: Path, cfg: dict) -> list[dict[str, str]]:
    actual_sha = sha256_file(path)
    if actual_sha != cfg["p0_split_manifest_sha256"]:
        raise ValueError(f"P0 manifest SHA mismatch: {actual_sha} != {cfg['p0_split_manifest_sha256']}")

    with path.open("r", newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if len(rows) != int(cfg["p0_split_records"]):
        raise ValueError(f"P0 manifest row count drift: {len(rows)} != {cfg['p0_split_records']}")

    required = {
        "cancer_type", "participant_root", "methylation_source_label",
        "methylation_sample_root", "split_bucket", "partition"
    }
    if not rows or not required.issubset(rows[0]):
        raise ValueError("P0 manifest schema missing required fields")

    participants = Counter(r["participant_root"] for r in rows)
    dup_participants = [k for k, v in participants.items() if v != 1]
    if dup_participants:
        raise ValueError(f"duplicate participant roots in P0 manifest: {dup_participants[:10]}")

    source_roots = Counter(r["methylation_sample_root"] for r in rows)
    dup_sources = [k for k, v in source_roots.items() if v != 1]
    if dup_sources:
        raise ValueError(f"duplicate methylation sample roots in P0 manifest: {dup_sources[:10]}")

    cancers = {r["cancer_type"] for r in rows}
    if len(cancers) != int(cfg["p0_split_cancers"]):
        raise ValueError(f"P0 cancer count drift: {len(cancers)} != {cfg['p0_split_cancers']}")

    parts = Counter()
    for r in rows:
        b = int(r["split_bucket"])
        exp_b = split_bucket(cfg["split_namespace"], r["cancer_type"], r["participant_root"])
        if b != exp_b:
            raise ValueError(f"split bucket reconstruction mismatch for {r['participant_root']}: {b} != {exp_b}")
        exp_p = expected_partition(b)
        if r["partition"] != exp_p:
            raise ValueError(f"partition reconstruction mismatch for {r['participant_root']}: {r['partition']} != {exp_p}")
        parts[r["partition"]] += 1
    if dict(parts) != cfg["expected_preeligibility_partition_counts"]:
        raise ValueError(f"pre-eligibility partition count drift: {dict(parts)} != {cfg['expected_preeligibility_partition_counts']}")
    return rows


def read_source_header(source: Path, cfg: dict) -> tuple[list[str], dict[str, int]]:
    if source.stat().st_size != int(cfg["methylation_source_size_bytes"]):
        raise ValueError(
            f"selected methylation source size mismatch: {source.stat().st_size} != {cfg['methylation_source_size_bytes']}"
        )
    with source.open("rb") as fh:
        line = fh.readline()
    if not line:
        raise ValueError("methylation source is empty")
    header = line.decode("utf-8", errors="strict").rstrip("\r\n").split("\t")
    if len(header) != int(cfg["methylation_header_columns"]):
        raise ValueError(f"methylation header column drift: {len(header)} != {cfg['methylation_header_columns']}")
    labels = header[1:]
    if len(labels) != int(cfg["methylation_sample_columns"]):
        raise ValueError("methylation sample-column count drift")
    counts = Counter(labels)
    duplicates = [label for label, n in counts.items() if n != 1]
    if duplicates:
        raise ValueError(f"duplicate exact source labels in methylation header: {duplicates[:10]}")
    index = {label: i + 1 for i, label in enumerate(labels)}
    return header, index


def scan_finiteness(
    source: Path,
    source_indices: list[int],
    expected_probe_rows: int,
    chunksize: int = 128,
) -> tuple[np.ndarray, int]:
    if not source_indices:
        raise ValueError("no methylation columns selected")
    ordered = sorted(source_indices)
    finite_counts = np.zeros(len(ordered), dtype=np.int64)
    rows_seen = 0

    reader = pd.read_csv(
        source,
        sep="\t",
        header=None,
        skiprows=1,
        usecols=ordered,
        dtype=np.float64,
        chunksize=chunksize,
        engine="c",
        keep_default_na=True,
        na_values=["", "NA", "N/A", "NaN", "nan", "NULL", "null"],
        low_memory=False,
    )
    for chunk in reader:
        arr = chunk.to_numpy(dtype=np.float64, copy=False)
        finite_counts += np.isfinite(arr).sum(axis=0, dtype=np.int64)
        rows_seen += int(arr.shape[0])
    if rows_seen != int(expected_probe_rows):
        raise ValueError(f"methylation probe-row count drift while scanning: {rows_seen} != {expected_probe_rows}")
    return finite_counts, rows_seen


def run(config_path: Path, manifest_path: Path, source_path: Path, out_dir: Path, chunksize: int = 128) -> dict:
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    if cfg.get("partition_reassignment_allowed") is not False:
        raise ValueError("eligibility gate may not reassign partitions")
    if cfg.get("predictive_target_values_allowed") is not False:
        raise ValueError("eligibility gate may not read predictive target values")
    if cfg.get("biological_association_allowed") is not False:
        raise ValueError("eligibility gate may not perform biological association")

    rows = read_manifest(manifest_path, cfg)
    _, header_index = read_source_header(source_path, cfg)

    labels = [r["methylation_source_label"] for r in rows]
    missing = [x for x in labels if x not in header_index]
    if missing:
        raise ValueError(f"manifest source labels missing from methylation header: {missing[:10]}")

    source_indices_sorted = sorted(header_index[x] for x in labels)
    if len(set(source_indices_sorted)) != len(rows):
        raise ValueError("manifest does not resolve to unique methylation source columns")
    finite_sorted, probe_rows_seen = scan_finiteness(
        source_path,
        source_indices_sorted,
        int(cfg["primary_probe_count"]),
        chunksize=chunksize,
    )
    finite_by_source_index = {idx: int(n) for idx, n in zip(source_indices_sorted, finite_sorted)}

    threshold = float(cfg["sample_primary_finite_fraction_min"])
    min_finite = int(math.ceil(threshold * int(cfg["primary_probe_count"])))
    sample_rows: list[dict[str, object]] = []
    per_cancer_part: dict[str, Counter] = defaultdict(Counter)
    per_cancer_part_total: dict[str, Counter] = defaultdict(Counter)

    for r in rows:
        src_idx = header_index[r["methylation_source_label"]]
        finite_n = finite_by_source_index[src_idx]
        frac = finite_n / int(cfg["primary_probe_count"])
        eligible = finite_n >= min_finite
        sample_rows.append({
            "cancer_type": r["cancer_type"],
            "participant_root": r["participant_root"],
            "methylation_sample_root": r["methylation_sample_root"],
            "partition": r["partition"],
            "finite_primary_probe_count": finite_n,
            "primary_probe_count": int(cfg["primary_probe_count"]),
            "finite_fraction": f"{frac:.12f}",
            "eligible_primary_95pct": str(bool(eligible)).lower(),
        })
        per_cancer_part_total[r["cancer_type"]][r["partition"]] += 1
        if eligible:
            per_cancer_part[r["cancer_type"]][r["partition"]] += 1

    out_dir.mkdir(parents=True, exist_ok=True)
    sample_path = out_dir / "p0_sample_eligibility.csv"
    sample_fields = [
        "cancer_type", "participant_root", "methylation_sample_root", "partition",
        "finite_primary_probe_count", "primary_probe_count", "finite_fraction", "eligible_primary_95pct"
    ]
    with sample_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=sample_fields)
        w.writeheader()
        w.writerows(sample_rows)

    min_per = int(cfg["minimum_eligible_per_partition_per_cancer"])
    count_rows: list[dict[str, object]] = []
    fully_evaluable = []
    for cancer in sorted(per_cancer_part_total):
        total = per_cancer_part_total[cancer]
        elig = per_cancer_part[cancer]
        ok = all(elig[p] >= min_per for p in ("DISCOVERY", "REPLICATION", "FINAL_HOLDOUT"))
        if ok:
            fully_evaluable.append(cancer)
        count_rows.append({
            "cancer_type": cancer,
            "pre_discovery_n": total["DISCOVERY"],
            "pre_replication_n": total["REPLICATION"],
            "pre_final_holdout_n": total["FINAL_HOLDOUT"],
            "eligible_discovery_n": elig["DISCOVERY"],
            "eligible_replication_n": elig["REPLICATION"],
            "eligible_final_holdout_n": elig["FINAL_HOLDOUT"],
            "fully_evaluable_p0": str(bool(ok)).lower(),
        })

    counts_path = out_dir / "p0_partition_eligibility_counts.csv"
    count_fields = [
        "cancer_type", "pre_discovery_n", "pre_replication_n", "pre_final_holdout_n",
        "eligible_discovery_n", "eligible_replication_n", "eligible_final_holdout_n", "fully_evaluable_p0"
    ]
    with counts_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=count_fields)
        w.writeheader()
        w.writerows(count_rows)

    eligible_total = sum(r["eligible_primary_95pct"] == "true" for r in sample_rows)
    result = {
        "schema": "gri-v2-p0-eligibility-result-v0.1",
        "status": "P0_SAMPLE_ELIGIBILITY_COMPLETE",
        "input_manifest_sha256": sha256_file(manifest_path),
        "methylation_source_sha256_locked_from_c0": cfg["methylation_source_sha256_locked_from_c0"],
        "methylation_source_size_bytes_verified": source_path.stat().st_size,
        "primary_probe_count": int(cfg["primary_probe_count"]),
        "probe_rows_seen": probe_rows_seen,
        "sample_primary_finite_fraction_min": threshold,
        "minimum_finite_primary_probe_count": min_finite,
        "records": len(sample_rows),
        "eligible_records": int(eligible_total),
        "ineligible_records": int(len(sample_rows) - eligible_total),
        "cancers": len(count_rows),
        "fully_evaluable_cancers": len(fully_evaluable),
        "fully_evaluable_cancer_types": fully_evaluable,
        "minimum_eligible_per_partition_per_cancer": min_per,
        "pan_cancer_promotion_min_cancers": int(cfg["pan_cancer_promotion_min_cancers"]),
        "pan_cancer_promotion_possible_under_p0": len(fully_evaluable) >= int(cfg["pan_cancer_promotion_min_cancers"]),
        "sample_eligibility_sha256": sha256_file(sample_path),
        "partition_eligibility_counts_sha256": sha256_file(counts_path),
        "methylation_beta_values_read_for_missingness_eligibility_only": True,
        "predictive_target_values_read": False,
        "rna_hallmark_target_values_read": False,
        "biological_association_performed": False,
        "partition_reassignment_performed": False,
        "biological_chi_used": False,
        "stage_c1_science_modified": False,
        "claim_ceiling": "per-sample methylation missingness eligibility and fixed-partition coverage only",
        "next_gate": "discovery-only probe eligibility, imputation, Hallmark feature construction, and model preprocessing for fully evaluable cancers only"
    }
    summary_path = out_dir / "P0_ELIGIBILITY_SUMMARY.json"
    summary_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--chunksize", type=int, default=128)
    args = ap.parse_args()
    result = run(args.config, args.manifest, args.source, args.out, chunksize=args.chunksize)
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
