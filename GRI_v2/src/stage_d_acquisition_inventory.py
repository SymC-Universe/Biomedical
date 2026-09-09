#!/usr/bin/env python3
"""Stage D metadata-only GEO inventory.

This program intentionally does NOT open expression, methylation, contact, or other
numeric biological matrices.  It downloads GEO family SOFT metadata and inventories
supplementary file names/URLs so the Stage-D sample design can be frozen before
biological outcome inspection.

Scientific contract:
  GRI_v2/protocol/STAGE_D_PERTURBATION_RECOVERY_TRANSFORMATION_FREEZE_v0.1.md
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

USER_AGENT = "SymC-GRI-StageD/0.1 metadata-only inventory"


def _series_bucket(accession: str) -> str:
    m = re.fullmatch(r"GSE(\d+)", accession.strip().upper())
    if not m:
        raise ValueError(f"Not a GEO series accession: {accession!r}")
    digits = m.group(1)
    if len(digits) <= 3:
        return "GSEnnn"
    return f"GSE{digits[:-3]}nnn"


def _urlopen(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    return urllib.request.urlopen(req, timeout=120)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    with _urlopen(url) as r, tmp.open("wb") as f:
        while True:
            block = r.read(1024 * 1024)
            if not block:
                break
            f.write(block)
    tmp.replace(dest)


def _append(d: Dict[str, List[str]], key: str, value: str) -> None:
    d.setdefault(key, []).append(value.strip())


def parse_soft(path: Path) -> Tuple[dict, List[dict]]:
    opener = gzip.open if path.suffix == ".gz" else open
    series: Dict[str, List[str]] = {}
    samples: List[dict] = []
    current: Dict[str, List[str]] | None = None

    with opener(path, "rt", encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            if line.startswith("^SERIES = "):
                series["geo_accession"] = [line.split("=", 1)[1].strip()]
                current = None
            elif line.startswith("^SAMPLE = "):
                if current is not None:
                    samples.append(current)
                current = {"geo_accession": [line.split("=", 1)[1].strip()]}
            elif line.startswith("^"):
                if current is not None:
                    samples.append(current)
                    current = None
            elif line.startswith("!Series_"):
                key, value = line[1:].split(" = ", 1)
                _append(series, key, value)
            elif line.startswith("!Sample_") and current is not None:
                key, value = line[1:].split(" = ", 1)
                _append(current, key, value)

    if current is not None:
        samples.append(current)

    def scalarize(d: Dict[str, List[str]]) -> dict:
        out = {}
        for k, vals in d.items():
            out[k] = vals[0] if len(vals) == 1 else vals
        return out

    return scalarize(series), [scalarize(s) for s in samples]


def inventory_supplementary(accession: str) -> List[dict]:
    bucket = _series_bucket(accession)
    base = f"https://ftp.ncbi.nlm.nih.gov/geo/series/{bucket}/{accession}/suppl/"
    try:
        html = _urlopen(base).read().decode("utf-8", errors="replace")
    except Exception as exc:  # network/listing failure should be explicit, not fatal metadata corruption
        return [{"accession": accession, "filename": "", "url": base, "listing_error": repr(exc)}]

    names = []
    for href in re.findall(r'href=["\']([^"\']+)["\']', html, flags=re.I):
        if href in ("../", "./") or href.endswith("/"):
            continue
        name = href.split("/")[-1]
        if name and name not in names:
            names.append(name)
    return [
        {"accession": accession, "filename": name, "url": base + name, "listing_error": ""}
        for name in names
    ]


def _json_cell(v) -> str:
    if isinstance(v, list):
        return json.dumps(v, ensure_ascii=False)
    return "" if v is None else str(v)


def write_sample_csv(rows: Iterable[dict], path: Path) -> None:
    rows = list(rows)
    keys = [
        "stage_id",
        "series_accession",
        "geo_accession",
        "Sample_title",
        "Sample_source_name_ch1",
        "Sample_characteristics_ch1",
        "Sample_treatment_protocol_ch1",
        "Sample_growth_protocol_ch1",
        "Sample_extract_protocol_ch1",
        "Sample_data_processing",
        "Sample_platform_id",
        "Sample_supplementary_file",
        "Sample_relation",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow({k: _json_cell(row.get(k, "")) for k in keys})


def run(registry_path: Path, out_dir: Path) -> dict:
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    if registry.get("status") != "FROZEN_BEFORE_STAGE_D_BIOLOGICAL_OUTCOME_INSPECTION":
        raise RuntimeError("Stage-D registry is not in the expected frozen state")

    out_dir.mkdir(parents=True, exist_ok=True)
    all_samples = []
    all_supp = []
    dataset_records = []

    for ds in registry["datasets"]:
        stage_id = ds["stage_id"]
        accessions = [ds["primary_accession"], *ds.get("associated_accessions", [])]
        for accession in accessions:
            accession = accession.upper()
            bucket = _series_bucket(accession)
            soft_url = f"https://ftp.ncbi.nlm.nih.gov/geo/series/{bucket}/{accession}/soft/{accession}_family.soft.gz"
            soft_path = out_dir / "soft" / f"{accession}_family.soft.gz"
            if not soft_path.exists():
                _download(soft_url, soft_path)
            series, samples = parse_soft(soft_path)
            for s in samples:
                s["stage_id"] = stage_id
                s["series_accession"] = accession
                all_samples.append(s)
            supp = inventory_supplementary(accession)
            for row in supp:
                row["stage_id"] = stage_id
                all_supp.append(row)
            dataset_records.append(
                {
                    "stage_id": stage_id,
                    "accession": accession,
                    "soft_url": soft_url,
                    "soft_file": str(soft_path),
                    "soft_bytes": soft_path.stat().st_size,
                    "soft_sha256": _sha256(soft_path),
                    "series_title": series.get("Series_title", ""),
                    "sample_count_from_soft": len(samples),
                    "supplementary_listing_count": sum(1 for r in supp if r.get("filename")),
                    "supplementary_listing_errors": [r["listing_error"] for r in supp if r.get("listing_error")],
                }
            )

    write_sample_csv(all_samples, out_dir / "SAMPLE_MANIFEST_RAW.csv")

    supp_keys = ["stage_id", "accession", "filename", "url", "listing_error"]
    with (out_dir / "SUPPLEMENTARY_FILE_LIST.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=supp_keys)
        w.writeheader()
        w.writerows(all_supp)

    audit = {
        "schema": "gri-stage-d-metadata-inventory-v0.1",
        "scientific_outputs_opened": false,
        "numeric_biological_matrices_opened": false,
        "registry_sha256": _sha256(registry_path),
        "datasets": dataset_records,
        "total_samples_from_soft": len(all_samples),
        "status": "PASS_METADATA_ONLY" if all(r["sample_count_from_soft"] > 0 for r in dataset_records) else "HOLD_METADATA_INCOMPLETE",
    }
    (out_dir / "D0_METADATA_AUDIT.json").write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return audit


def main(argv: List[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--registry", default="GRI_v2/config/stage_d_dataset_registry_v0.1.json")
    p.add_argument("--out", default="GRI_v2/artifacts/stage_d/d0_metadata_inventory")
    args = p.parse_args(argv)
    audit = run(Path(args.registry), Path(args.out))
    print(json.dumps(audit, indent=2, sort_keys=True))
    return 0 if audit["status"] == "PASS_METADATA_ONLY" else 2


if __name__ == "__main__":
    raise SystemExit(main())
