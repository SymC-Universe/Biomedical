#!/usr/bin/env python3
"""Summarize the portable frozen Stage C1A annotation artifact.

Source/schema only. No methylation beta values are read.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import re
from pathlib import Path


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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", required=True)
    args = ap.parse_args()
    out = Path(args.outdir)

    acquisition_path = out / "STAGE_C1A_SOURCE_ACQUISITION.json"
    ann_path = out / "stage_c1a_annotation_export.tsv.gz"
    chen_ids_path = out / "stage_c1a_chen_crossreactive_probe_ids.txt"
    inv_path = out / "stage_c1a_annotation_object_inventory.txt"
    for path in [acquisition_path, ann_path, chen_ids_path, inv_path]:
        if not path.exists():
            raise SystemExit(f"missing required C1A source-gate output: {path}")

    acquisition = json.loads(acquisition_path.read_text(encoding="utf-8"))
    ids: set[str] = set()
    duplicate_ids = 0
    rows = 0
    refgene_mapped = 0
    cpg_snp = 0
    sbe_snp = 0
    common_snp_union = 0
    with gzip.open(ann_path, "rt", encoding="utf-8", newline="") as fh:
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
            rows += 1
            pid = (row.get("probe_id") or "").strip()
            if not pid:
                raise SystemExit(f"blank probe_id at export row {rows}")
            if pid in ids:
                duplicate_ids += 1
            ids.add(pid)
            if nonblank(row.get("UCSC_RefGene_Name")):
                refgene_mapped += 1
            has_cpg = nonblank(row.get("CpG_rs"))
            has_sbe = nonblank(row.get("SBE_rs"))
            cpg_snp += int(has_cpg)
            sbe_snp += int(has_sbe)
            common_snp_union += int(has_cpg or has_sbe)

    if duplicate_ids:
        raise SystemExit(f"annotation export contains {duplicate_ids} duplicate probe IDs")
    if rows != len(ids):
        raise SystemExit("annotation export row/unique-ID mismatch")

    chen_ids = [x.strip() for x in chen_ids_path.read_text(encoding="utf-8").splitlines() if x.strip()]
    if len(chen_ids) != len(set(chen_ids)):
        raise SystemExit("cross-reactive exported ID list is not unique")

    inventory_text = inv_path.read_text(encoding="utf-8")
    m = re.search(r"^selected_common_snp_object=(.+)$", inventory_text, flags=re.MULTILINE)
    if not m:
        raise SystemExit("selected common-SNP object missing from inventory")
    selected_snp_object = m.group(1).strip()

    summary = {
        "status": "STAGE_C1A_ANNOTATION_SOURCE_GATE_READY_FOR_LOCAL_PROBE_INTERSECTION",
        "biological_association_performed": False,
        "methylation_beta_values_read": False,
        "claim_ceiling": "annotation source identity, portable schema, and technical-mask source identity only",
        "acquisition": acquisition,
        "annotation_export": {
            "rows": rows,
            "unique_probe_ids": len(ids),
            "duplicate_probe_ids": duplicate_ids,
            "refgene_mapped_rows": refgene_mapped,
            "selected_common_snp_object": selected_snp_object,
            "cpg_common_snp_rows": cpg_snp,
            "sbe_common_snp_rows": sbe_snp,
            "cpg_or_sbe_common_snp_rows": common_snp_union,
            "sha256": sha256(ann_path),
        },
        "cross_reactive_export": {
            "unique_probe_ids": len(chen_ids),
            "sha256": sha256(chen_ids_path),
        },
        "object_inventory_sha256": sha256(inv_path),
    }
    summary_path = out / "STAGE_C1A_ANNOTATION_SOURCE_SUMMARY.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
