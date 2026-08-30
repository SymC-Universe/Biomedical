#!/usr/bin/env python3
"""Stage C1A local exact-probe annotation inventory.

The 5.02 GB methylation source is streamed only to hash it and recover the first
(tab-delimited) probe-ID field from each row. Beta-value fields are never parsed
or converted to numbers in this gate.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path

EXPECTED_SOURCE_SHA256 = "5934c497882fbe8178d128a3a7f71e765480af6bbd460e0398de3428cd075b77"
EXPECTED_PROBES = 22601

STRATA = {
    "PROMOTER_CORE": {"TSS200"},
    "PROMOTER_PROXIMAL": {"TSS1500"},
    "PROMOTER_TRANSCRIBED_EDGE": {"5'UTR", "1stExon"},
    "GENE_BODY": {"Body"},
    "THREE_PRIME_UTR": {"3'UTR"},
}
BROAD_PROMOTER = {"TSS200", "TSS1500", "5'UTR", "1stExon"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def nonblank(v: str | None) -> bool:
    if v is None:
        return False
    s = str(v).strip()
    return bool(s) and s.upper() not in {"NA", "NAN", "NONE"}


def stream_source_probe_ids(path: Path) -> tuple[list[str], str, int]:
    h = hashlib.sha256()
    ids: list[str] = []
    header_columns = 0
    with path.open("rb") as fh:
        header = fh.readline()
        if not header:
            raise RuntimeError("methylation TSV is empty")
        h.update(header)
        header_columns = header.count(b"\t") + 1
        for raw in fh:
            h.update(raw)
            first = raw.split(b"\t", 1)[0].strip().strip(b'"')
            if not first:
                raise RuntimeError(f"blank probe ID at source row {len(ids) + 1}")
            ids.append(first.decode("utf-8", errors="strict"))
    return ids, h.hexdigest(), header_columns


def split_tokens(s: str | None) -> list[str]:
    if s is None:
        return [""]
    return [x.strip() for x in str(s).split(";")]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--methylation-tsv", required=True)
    ap.add_argument("--annotation-export", required=True)
    ap.add_argument("--chen-ids", required=True)
    ap.add_argument("--source-summary", required=True)
    ap.add_argument("--outdir", required=True)
    args = ap.parse_args()

    methylation = Path(args.methylation_tsv)
    annotation_export = Path(args.annotation_export)
    chen_ids_path = Path(args.chen_ids)
    source_summary_path = Path(args.source_summary)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    source_summary = json.loads(source_summary_path.read_text(encoding="utf-8"))
    expected_ann_export_sha = source_summary["annotation_export"]["sha256"]
    expected_chen_export_sha = source_summary["cross_reactive_export"]["sha256"]
    observed_ann_export_sha = sha256(annotation_export)
    observed_chen_export_sha = sha256(chen_ids_path)
    if observed_ann_export_sha != expected_ann_export_sha:
        raise SystemExit("annotation export SHA-256 does not match frozen C1A source summary")
    if observed_chen_export_sha != expected_chen_export_sha:
        raise SystemExit("Chen ID export SHA-256 does not match frozen C1A source summary")

    probe_ids, source_sha, header_columns = stream_source_probe_ids(methylation)
    if source_sha != EXPECTED_SOURCE_SHA256:
        raise SystemExit(
            f"methylation source SHA-256 mismatch: expected {EXPECTED_SOURCE_SHA256}, observed {source_sha}"
        )
    if len(probe_ids) != EXPECTED_PROBES:
        raise SystemExit(f"expected {EXPECTED_PROBES} probe rows, observed {len(probe_ids)}")
    if len(set(probe_ids)) != EXPECTED_PROBES:
        raise SystemExit("methylation source probe IDs are not unique")
    target = set(probe_ids)

    chen_ids = {x.strip() for x in chen_ids_path.read_text(encoding="utf-8").splitlines() if x.strip()}

    selected: dict[str, dict[str, str]] = {}
    with gzip.open(annotation_export, "rt", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        required = {
            "probe_id",
            "UCSC_RefGene_Name",
            "UCSC_RefGene_Accession",
            "UCSC_RefGene_Group",
            "CpG_rs",
            "SBE_rs",
        }
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise SystemExit(f"annotation export missing columns: {sorted(missing)}")
        for row in reader:
            pid = (row.get("probe_id") or "").strip()
            if pid in target:
                if pid in selected:
                    raise SystemExit(f"duplicate annotation row for source probe {pid}")
                selected[pid] = row

    missing_annotation = sorted(target.difference(selected))
    annotation_overlap = len(selected)

    flags_rows: list[dict[str, object]] = []
    map_rows: list[dict[str, str]] = []
    stratum_probe_sets = {name: set() for name in STRATA}
    broad_promoter_probes: set[str] = set()
    refgene_mapped_probes: set[str] = set()
    tuple_mismatch_probes: set[str] = set()
    unstratified_refgene_probes: set[str] = set()
    common_snp_probes: set[str] = set()

    for pid in probe_ids:
        row = selected.get(pid)
        if row is None:
            flags_rows.append({
                "probe_id": pid,
                "annotation_present": 0,
                "refgene_mapped": 0,
                "tuple_length_mismatch": 0,
                "cross_reactive_chen": int(pid in chen_ids),
                "common_snp_cpg_or_sbe": 0,
                "technical_mask_union": int(pid in chen_ids),
            })
            continue

        genes = split_tokens(row.get("UCSC_RefGene_Name"))
        accessions = split_tokens(row.get("UCSC_RefGene_Accession"))
        groups = split_tokens(row.get("UCSC_RefGene_Group"))
        mismatch = not (len(genes) == len(accessions) == len(groups))
        if mismatch:
            tuple_mismatch_probes.add(pid)
        else:
            seen_tuples: set[tuple[str, str, str]] = set()
            for gene, accession, group in zip(genes, accessions, groups):
                if not gene:
                    continue
                tup = (gene, accession, group)
                if tup in seen_tuples:
                    continue
                seen_tuples.add(tup)
                refgene_mapped_probes.add(pid)
                matched_strata = [name for name, vals in STRATA.items() if group in vals]
                if group in BROAD_PROMOTER:
                    broad_promoter_probes.add(pid)
                if not matched_strata:
                    unstratified_refgene_probes.add(pid)
                else:
                    for stratum in matched_strata:
                        stratum_probe_sets[stratum].add(pid)
                map_rows.append({
                    "probe_id": pid,
                    "gene_symbol": gene,
                    "refgene_accession": accession,
                    "refgene_group": group,
                    "regulatory_stratum": "|".join(matched_strata) if matched_strata else "UNSTRATIFIED_REFGENE",
                })

        has_common_snp = nonblank(row.get("CpG_rs")) or nonblank(row.get("SBE_rs"))
        if has_common_snp:
            common_snp_probes.add(pid)
        chen = pid in chen_ids
        flags_rows.append({
            "probe_id": pid,
            "annotation_present": 1,
            "refgene_mapped": int(pid in refgene_mapped_probes),
            "tuple_length_mismatch": int(pid in tuple_mismatch_probes),
            "cross_reactive_chen": int(chen),
            "common_snp_cpg_or_sbe": int(has_common_snp),
            "technical_mask_union": int(chen or has_common_snp),
        })

    chen_overlap = target.intersection(chen_ids)
    union_mask = chen_overlap.union(common_snp_probes)
    robust_remaining = target.difference(union_mask)

    map_path = outdir / "stage_c1a_probe_gene_region_map.csv.gz"
    with gzip.open(map_path, "wt", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["probe_id", "gene_symbol", "refgene_accession", "refgene_group", "regulatory_stratum"],
        )
        writer.writeheader()
        writer.writerows(map_rows)

    flags_path = outdir / "stage_c1a_probe_flags.csv.gz"
    with gzip.open(flags_path, "wt", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(flags_rows[0].keys()))
        writer.writeheader()
        writer.writerows(flags_rows)

    stratum_path = outdir / "stage_c1a_regulatory_stratum_counts.csv"
    with stratum_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["stratum", "unique_source_probes"])
        for name in STRATA:
            writer.writerow([name, len(stratum_probe_sets[name])])
        writer.writerow(["BROAD_PROMOTER_SECONDARY", len(broad_promoter_probes)])
        writer.writerow(["REFGENE_MAPPED_ANY", len(refgene_mapped_probes)])
        writer.writerow(["REFGENE_UNSTRATIFIED", len(unstratified_refgene_probes)])

    status = "STAGE_C1A_PROBE_INVENTORY_PASS" if annotation_overlap == EXPECTED_PROBES else "STAGE_C1A_PROBE_INVENTORY_FAIL"
    summary = {
        "status": status,
        "claim_ceiling": "exact probe annotation/mask inventory only; no methylation biological association",
        "biological_association_performed": False,
        "methylation_beta_values_parsed_for_biological_analysis": False,
        "methylation_source_sha256": source_sha,
        "methylation_header_columns": header_columns,
        "source_probe_rows": len(probe_ids),
        "source_unique_probe_ids": len(target),
        "annotation_overlap": annotation_overlap,
        "missing_annotation_count": len(missing_annotation),
        "missing_annotation_probe_ids": missing_annotation,
        "refgene_mapped_probe_count": len(refgene_mapped_probes),
        "refgene_unmapped_probe_count": EXPECTED_PROBES - len(refgene_mapped_probes),
        "tuple_length_mismatch_probe_count": len(tuple_mismatch_probes),
        "unstratified_refgene_probe_count": len(unstratified_refgene_probes),
        "gene_region_tuple_rows": len(map_rows),
        "technical_mask": {
            "chen_cross_reactive_overlap": len(chen_overlap),
            "common_snp_cpg_or_sbe_overlap": len(common_snp_probes),
            "union_overlap": len(union_mask),
            "robustness_remaining_probe_count": len(robust_remaining),
        },
        "regulatory_strata_unique_probe_counts": {
            **{name: len(stratum_probe_sets[name]) for name in STRATA},
            "BROAD_PROMOTER_SECONDARY": len(broad_promoter_probes),
        },
        "portable_source_summary_sha256": sha256(source_summary_path),
        "annotation_export_sha256": observed_ann_export_sha,
        "chen_id_export_sha256": observed_chen_export_sha,
        "probe_gene_region_map_sha256": sha256(map_path),
        "probe_flags_sha256": sha256(flags_path),
        "regulatory_stratum_counts_sha256": sha256(stratum_path),
    }
    summary_path = outdir / "STAGE_C1A_PROBE_INVENTORY_SUMMARY.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if status != "STAGE_C1A_PROBE_INVENTORY_PASS":
        raise SystemExit("C1A probe inventory failed exact annotation-overlap gate")


if __name__ == "__main__":
    main()
