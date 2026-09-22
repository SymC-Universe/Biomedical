#!/usr/bin/env python3
"""Metadata-only TCGA tumor/normal source inventory.

Reads only header/sample annotation strings. It never reads molecular values.
"""
from __future__ import annotations
import argparse, csv, gzip, json, re
from collections import defaultdict
from pathlib import Path

TCGA_SAMPLE_RE = re.compile(r"^(TCGA-[A-Z0-9]{2}-[A-Z0-9]{4})-([0-9]{2})[A-Z]?")


def open_text(path: str):
    return gzip.open(path, "rt", newline="") if path.endswith(".gz") else open(path, "r", newline="")


def parse_barcode(value: str):
    value = value.strip().strip('\"').upper().replace('.', '-')
    m = TCGA_SAMPLE_RE.match(value)
    if not m:
        return None
    participant = m.group(1)
    sample_type = m.group(2)
    parts = value.split("-")
    sample = "-".join(parts[:4]) if len(parts) >= 4 else f"{participant}-{sample_type}"
    return participant, sample_type, sample


def read_header_samples(path: str):
    with open_text(path) as fh:
        first = fh.readline().rstrip("\n\r")
    if not first:
        raise ValueError(f"empty source: {path}")
    cols = first.split("\t")
    parsed = []
    for raw in cols[1:]:
        p = parse_barcode(raw)
        if p:
            participant, stype, sample = p
            parsed.append({"raw": raw, "participant": participant, "sample_type": stype, "sample": sample})
    return parsed


def read_annotation(path: str):
    with open_text(path) as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        fields = {f.lower().strip(): f for f in (reader.fieldnames or [])}
        barcode_col = next((fields[x] for x in fields if x in {"aliquot_barcode","sample","sample_barcode","barcode"}), None)
        cancer_col = next((fields[x] for x in fields if x in {"cancer type","cancer_type","project","project_id"}), None)
        dnu_col = next((fields[x] for x in fields if x.replace(" ","_") in {"do_not_use","donotuse"}), None)
        if not barcode_col or not cancer_col:
            raise ValueError(f"annotation requires barcode and cancer columns; found {reader.fieldnames}")
        mapping = {}
        conflicts = []
        for row in reader:
            p = parse_barcode(row.get(barcode_col, "") or "")
            if not p:
                continue
            participant, stype, sample = p
            if dnu_col and str(row.get(dnu_col,"")).strip().lower() in {"true","1","yes","y"}:
                continue
            cancer = str(row.get(cancer_col,"")).strip()
            if not cancer:
                continue
            old = mapping.get(sample)
            if old and old != cancer:
                conflicts.append({"sample": sample, "cancer_a": old, "cancer_b": cancer})
            else:
                mapping[sample] = cancer
        return mapping, conflicts


def unique_participants(records, sample_to_cancer):
    out = defaultdict(lambda: defaultdict(set))
    unmatched = []
    for r in records:
        cancer = sample_to_cancer.get(r["sample"])
        if cancer is None:
            unmatched.append(r["sample"])
            continue
        if r["sample_type"] in {"01","11"}:
            out[cancer][r["sample_type"]].add(r["participant"])
    return out, sorted(set(unmatched))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rna", required=True)
    ap.add_argument("--methylation", required=True)
    ap.add_argument("--annotation", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    annotation, conflicts = read_annotation(args.annotation)
    rna = read_header_samples(args.rna)
    meth = read_header_samples(args.methylation)
    if not rna:
        raise RuntimeError("parsed zero TCGA RNA samples from source header")
    if not meth:
        raise RuntimeError("parsed zero TCGA methylation samples from source header")
    rna_counts, rna_unmatched = unique_participants(rna, annotation)
    meth_counts, meth_unmatched = unique_participants(meth, annotation)

    cancers = sorted(set(rna_counts) | set(meth_counts))
    rows = []
    for cancer in cancers:
        rr = rna_counts[cancer]
        mm = meth_counts[cancer]
        row = {
            "cancer": cancer,
            "rna_tumor_01_n": len(rr["01"]),
            "rna_normal_11_n": len(rr["11"]),
            "meth_tumor_01_n": len(mm["01"]),
            "meth_normal_11_n": len(mm["11"]),
            "rna_meth_tumor_overlap_n": len(rr["01"] & mm["01"]),
            "rna_meth_normal_overlap_n": len(rr["11"] & mm["11"]),
        }
        row["eligible_rna_tn_a1_n30"] = row["rna_tumor_01_n"] >= 30 and row["rna_normal_11_n"] >= 30
        row["eligible_multiomic_tn_c1_n30"] = row["rna_meth_tumor_overlap_n"] >= 30 and row["rna_meth_normal_overlap_n"] >= 30
        rows.append(row)

    payload = {
        "schema": "gri-biosystems-tumor-normal-metadata-inventory-v1",
        "outcome_sealed": True,
        "molecular_values_read": False,
        "sample_types": {"01": "Primary Solid Tumor", "11": "Solid Tissue Normal"},
        "eligibility_floor": 30,
        "annotation_conflicts": conflicts,
        "rna_header_tcga_samples": len(rna),
        "methylation_header_tcga_samples": len(meth),
        "rna_unmatched_sample_count": len(rna_unmatched),
        "methylation_unmatched_sample_count": len(meth_unmatched),
        "cancers": rows,
    }
    Path(args.out).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
