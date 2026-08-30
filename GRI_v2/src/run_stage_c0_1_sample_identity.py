from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

TCGA_PATIENT_RE = re.compile(r"TCGA[-.][A-Z0-9]{2}[-.][A-Z0-9]{4}", re.I)
TCGA_ROOT_RE = re.compile(r"TCGA[-.][A-Z0-9]{2}[-.][A-Z0-9]{4}[-.][0-9]{2}[A-Z]", re.I)
CHUNK = 8 * 1024 * 1024


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(CHUNK), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_barcode(value: str) -> str:
    return value.upper().replace(".", "-")


def sample_root(value: str) -> str | None:
    m = TCGA_ROOT_RE.search(value)
    return normalize_barcode(m.group(0)) if m else None


def patient_id(value: str) -> str | None:
    m = TCGA_PATIENT_RE.search(value)
    return normalize_barcode(m.group(0)) if m else None


def is_primary_root(root: str | None) -> bool:
    if not root:
        return False
    parts = root.split("-")
    return len(parts) >= 4 and parts[3][:2] == "01"


def read_header_inventory(source_path: Path) -> dict:
    with source_path.open("rb") as fh:
        header_b = fh.readline()
    if not header_b:
        raise ValueError("Methylation source is empty")
    header = header_b.decode("utf-8", errors="strict").rstrip("\r\n").split("\t")
    if len(header) < 2:
        raise ValueError("Methylation source header has fewer than two columns")
    labels = header[1:]
    roots = [sample_root(x) for x in labels]
    parsed = sum(r is not None for r in roots)
    if parsed != len(labels):
        raise ValueError(f"Only {parsed}/{len(labels)} source columns have parseable TCGA sample roots")

    primary_pairs = [(label, root) for label, root in zip(labels, roots) if is_primary_root(root)]
    root_to_labels: dict[str, list[str]] = defaultdict(list)
    for label, root in primary_pairs:
        assert root is not None
        root_to_labels[root].append(label)
    patient_to_labels: dict[str, list[str]] = defaultdict(list)
    for label, root in primary_pairs:
        pid = patient_id(root or label)
        if pid:
            patient_to_labels[pid].append(label)

    duplicate_roots = {root: values for root, values in root_to_labels.items() if len(values) > 1}
    return {
        "header_columns": len(header),
        "methylation_sample_columns": len(labels),
        "tcga_sample_roots_parsed": parsed,
        "primary_sample_columns": len(primary_pairs),
        "unique_primary_sample_roots": len(root_to_labels),
        "duplicate_primary_sample_roots": len(duplicate_roots),
        "unique_primary_patients": len(patient_to_labels),
        "root_to_labels": dict(root_to_labels),
        "patient_to_labels": dict(patient_to_labels),
        "duplicate_roots": duplicate_roots,
    }


def validate_locked_inputs(plan: dict, cache_path: Path, source_path: Path, c0_summary_path: Path) -> dict:
    frozen = plan["frozen_inputs"]
    cache_sha = sha256_file(cache_path)
    if cache_sha != frozen["stage_a_profile_cache_sha256"]:
        raise ValueError(f"Stage A cache SHA mismatch: {cache_sha} != {frozen['stage_a_profile_cache_sha256']}")

    summary_sha = sha256_file(c0_summary_path)
    if summary_sha != frozen["c0_summary_sha256"]:
        raise ValueError(f"C0 summary SHA mismatch: {summary_sha} != {frozen['c0_summary_sha256']}")
    c0 = json.loads(c0_summary_path.read_text(encoding="utf-8"))
    if c0.get("source_sha256") != frozen["methylation_source_sha256"]:
        raise ValueError("C0 summary source SHA-256 does not match frozen C0 source")
    if c0.get("source_md5") != frozen["methylation_source_md5"]:
        raise ValueError("C0 summary source MD5 does not match frozen C0 source")
    if int(c0.get("expected_content_length_bytes", -1)) != int(frozen["methylation_source_size_bytes"]):
        raise ValueError("C0 summary source size does not match frozen C0 source")
    if source_path.stat().st_size != int(frozen["methylation_source_size_bytes"]):
        raise ValueError("Selected methylation source size does not match frozen C0 source")
    return {"cache_sha256": cache_sha, "c0_summary_sha256": summary_sha, "c0_summary": c0}


def calculate_stage_a_coverage(cache_path: Path, inventory: dict) -> tuple[dict, list[dict]]:
    z = np.load(cache_path, allow_pickle=True)
    sample_ids = z["sample_ids"].astype(str)
    patient_ids = z["patient_ids"].astype(str)
    cancer_types = z["cancer_types"].astype(str)
    if not (len(sample_ids) == len(patient_ids) == len(cancer_types)):
        raise ValueError("Stage A cache identity arrays differ in length")

    root_counts = {root: len(labels) for root, labels in inventory["root_to_labels"].items()}
    patient_counts = {pid: len(labels) for pid, labels in inventory["patient_to_labels"].items()}

    matched = np.zeros(len(sample_ids), dtype=bool)
    exact_unique = 0
    fallback_unique = 0
    duplicate_root_excluded = 0
    no_source_match = 0
    for i, (sid, pid_raw) in enumerate(zip(sample_ids, patient_ids)):
        root = sample_root(sid)
        pid = normalize_barcode(pid_raw)
        rc = root_counts.get(root, 0) if root else 0
        if rc == 1:
            matched[i] = True
            exact_unique += 1
        elif rc > 1:
            duplicate_root_excluded += 1
        elif patient_counts.get(pid, 0) == 1:
            matched[i] = True
            fallback_unique += 1
        else:
            no_source_match += 1

    rows: list[dict] = []
    for cancer in sorted(set(cancer_types.tolist())):
        mask = cancer_types == cancer
        n_match = int((mask & matched).sum())
        rows.append({
            "cancer_type": str(cancer),
            "stage_a_n": int(mask.sum()),
            "unique_one_to_one_matched_n": n_match,
            "excluded_or_unmatched_n": int(mask.sum()) - n_match,
            "passes_n30": bool(n_match >= 30),
        })

    summary = {
        "stage_a_samples": int(len(sample_ids)),
        "unique_one_to_one_matched_stage_a_samples": int(matched.sum()),
        "exact_unique_root_matches": int(exact_unique),
        "unique_patient_fallback_matches": int(fallback_unique),
        "duplicate_root_stage_a_samples_excluded": int(duplicate_root_excluded),
        "no_source_match_stage_a_samples": int(no_source_match),
        "cancers": len(rows),
        "cancers_passing_n30": sum(int(r["passes_n30"]) for r in rows),
    }
    return summary, rows


def run(plan_path: Path, cache_path: Path, source_path: Path, c0_summary_path: Path, out_dir: Path) -> dict:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    locked = validate_locked_inputs(plan, cache_path, source_path, c0_summary_path)
    inventory = read_header_inventory(source_path)

    expected = plan["observed_c0_schema_facts"]
    for key in ("methylation_sample_columns", "primary_sample_columns", "unique_primary_sample_roots", "duplicate_primary_sample_roots"):
        if int(inventory[key]) != int(expected[key]):
            raise ValueError(f"Header schema drift for {key}: {inventory[key]} != C0-locked {expected[key]}")

    coverage, coverage_rows = calculate_stage_a_coverage(cache_path, inventory)
    if coverage["cancers_passing_n30"] != coverage["cancers"]:
        failed = [r["cancer_type"] for r in coverage_rows if not r["passes_n30"]]
        raise ValueError(f"Frozen n>=30 sample-identity gate failed for: {', '.join(failed)}")

    out_dir.mkdir(parents=True, exist_ok=True)
    coverage_path = out_dir / "stage_c0_1_unique_match_coverage.csv"
    with coverage_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["cancer_type", "stage_a_n", "unique_one_to_one_matched_n", "excluded_or_unmatched_n", "passes_n30"])
        writer.writeheader()
        writer.writerows(coverage_rows)

    duplicate_path = out_dir / "stage_c0_1_duplicate_primary_roots.csv"
    with duplicate_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["sample_root", "source_column_count", "source_labels_json"])
        for root in sorted(inventory["duplicate_roots"]):
            labels = inventory["duplicate_roots"][root]
            writer.writerow([root, len(labels), json.dumps(labels, separators=(",", ":"))])

    result = {
        "status": "STAGE_C0_1_SAMPLE_IDENTITY_GATE_PASS",
        "plan_version": plan["version"],
        "stage_a_profile_cache_sha256": locked["cache_sha256"],
        "c0_summary_sha256": locked["c0_summary_sha256"],
        "methylation_source_sha256_locked_from_c0": plan["frozen_inputs"]["methylation_source_sha256"],
        "header_schema": {k: v for k, v in inventory.items() if k not in {"root_to_labels", "patient_to_labels", "duplicate_roots"}},
        "coverage": coverage,
        "duplicate_root_action": "EXCLUDE_FROM_PRIMARY_C1",
        "beta_value_rows_read_for_biological_analysis": False,
        "biological_association_performed": False,
        "chi_present": False,
        "composite_score_present": False,
        "substrate_inheritance_claim": False,
        "claim_ceiling": "one-to-one sample identity and coverage only",
    }
    summary_path = out_dir / "STAGE_C0_1_SAMPLE_IDENTITY_SUMMARY.json"
    summary_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", type=Path, required=True)
    ap.add_argument("--cache", type=Path, required=True)
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--c0-summary", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    result = run(args.plan, args.cache, args.source, args.c0_summary, args.out)
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
