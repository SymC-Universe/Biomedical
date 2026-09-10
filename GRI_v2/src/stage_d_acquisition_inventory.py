#!/usr/bin/env python3
"""Stage D metadata-only GEO inventory.

This program intentionally does NOT open expression, methylation, contact, or other
numeric biological matrices. It retrieves GEO *brief* SOFT views, which contain
metadata only, plus supplementary file names/URLs. It does not download family SOFT,
series matrices, supplementary data, raw data, or numeric assay tables.

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
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

USER_AGENT = "SymC-GRI-StageD/0.2 metadata-only inventory"


def _series_bucket(accession: str) -> str:
    m = re.fullmatch(r"GSE(\d+)", accession.strip().upper())
    if not m:
        raise ValueError(f"Not a GEO series accession: {accession!r}")
    digits = m.group(1)
    if len(digits) <= 3:
        return "GSEnnn"
    return f"GSE{digits[:-3]}nnn"


def _geo_metadata_url(accession: str, target: str) -> str:
    if target not in {"self", "gsm"}:
        raise ValueError(f"Unsupported GEO metadata target: {target}")
    params = urllib.parse.urlencode(
        {
            "acc": accession.strip().upper(),
            "targ": target,
            "view": "brief",
            "form": "text",
        }
    )
    return f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?{params}"


def _urlopen(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    return urllib.request.urlopen(req, timeout=120)


def _fetch_text(url: str) -> str:
    with _urlopen(url) as r:
        return r.read().decode("utf-8", errors="replace")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _append(d: Dict[str, List[str]], key: str, value: str) -> None:
    d.setdefault(key, []).append(value.strip())


def parse_soft_text(text: str) -> Tuple[dict, List[dict]]:
    series: Dict[str, List[str]] = {}
    samples: List[dict] = []
    current: Dict[str, List[str]] | None = None

    for raw in text.splitlines():
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


def parse_soft(path: Path) -> Tuple[dict, List[dict]]:
    """Compatibility wrapper used by unit tests and local metadata files."""
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8", errors="replace") as fh:
        return parse_soft_text(fh.read())


def inventory_supplementary(accession: str) -> List[dict]:
    bucket = _series_bucket(accession)
    base = f"https://ftp.ncbi.nlm.nih.gov/geo/series/{bucket}/{accession}/suppl/"
    try:
        html = _fetch_text(base)
    except Exception as exc:
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
            series_url = _geo_metadata_url(accession, "self")
            samples_url = _geo_metadata_url(accession, "gsm")

            series_text = _fetch_text(series_url)
            samples_text = _fetch_text(samples_url)
            series, _ = parse_soft_text(series_text)
            _, samples = parse_soft_text(samples_text)

            for s in samples:
                s["stage_id"] = stage_id
                s["series_accession"] = accession
                all_samples.append(s)

            supp = inventory_supplementary(accession)
            for row in supp:
                row["stage_id"] = stage_id
                all_supp.append(row)

            series_bytes = series_text.encode("utf-8")
            sample_bytes = samples_text.encode("utf-8")
            dataset_records.append(
                {
                    "stage_id": stage_id,
                    "accession": accession,
                    "series_metadata_url": series_url,
                    "sample_metadata_url": samples_url,
                    "metadata_view": "brief",
                    "series_metadata_bytes": len(series_bytes),
                    "sample_metadata_bytes": len(sample_bytes),
                    "series_metadata_sha256": _sha256_bytes(series_bytes),
                    "sample_metadata_sha256": _sha256_bytes(sample_bytes),
                    "series_title": series.get("Series_title", ""),
                    "sample_count_from_brief_metadata": len(samples),
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
        "schema": "gri-stage-d-metadata-inventory-v0.2",
        "scientific_outputs_opened": False,
        "numeric_biological_matrices_opened": False,
        "full_geo_family_soft_downloaded": False,
        "series_matrix_downloaded": False,
        "supplementary_numeric_files_downloaded": False,
        "registry_sha256": _sha256(registry_path),
        "datasets": dataset_records,
        "total_samples_from_brief_metadata": len(all_samples),
        "status": "PASS_METADATA_ONLY"
        if all(r["sample_count_from_brief_metadata"] > 0 for r in dataset_records)
        else "HOLD_METADATA_INCOMPLETE",
    }
    (out_dir / "D0_METADATA_AUDIT.json").write_text(
        json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
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
