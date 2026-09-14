from __future__ import annotations

"""Read-only acquisition probe for manageable processed chronic SCC25 GEO files.

The probe downloads only public processed/metadata files whose sizes were
preflighted first. It hash-binds them and inspects table headers/sample counts.
It does not select features, read candidate outcomes, fit a state reduction, or
compute Chi_bio. The ~499 MB raw methylation TAR is explicitly excluded.
"""

import gzip
import hashlib
import json
import urllib.request
from pathlib import Path
from typing import Any


SOURCES = {
    "GSE98812_RNA_PROCESSED": {
        "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE98nnn/GSE98812/suppl/GSE98812_GEOExprsData.txt.gz",
        "filename": "GSE98812_GEOExprsData.txt.gz",
        "kind": "plain_gzip_table",
        "preflight_bytes": 2430267,
    },
    "GSE98812_RNA_SERIES_MATRIX": {
        "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE98nnn/GSE98812/matrix/GSE98812_series_matrix.txt.gz",
        "filename": "GSE98812_series_matrix.txt.gz",
        "kind": "geo_series_matrix",
        "preflight_bytes": 5495,
    },
    "GSE98813_METHYLATION_SERIES_MATRIX": {
        "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE98nnn/GSE98813/matrix/GSE98813_series_matrix.txt.gz",
        "filename": "GSE98813_series_matrix.txt.gz",
        "kind": "geo_series_matrix",
        "preflight_bytes": 143991614,
    },
    "GSE98813_METHYLATION_FILELIST": {
        "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE98nnn/GSE98813/suppl/filelist.txt",
        "filename": "GSE98813_filelist.txt",
        "kind": "plain_text",
        "preflight_bytes": 6234,
    },
}

RAW_EXCLUDED = {
    "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE98nnn/GSE98813/suppl/GSE98813_RAW.tar",
    "preflight_bytes": 499036160,
    "reason": "RAW_IDAT_ARCHIVE_NOT_NEEDED_FOR_CURRENT_SOURCE_IDENTITY_GATE",
}


def _download(url: str, path: Path, timeout: int = 180) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": "SymC-GRI-chronic-source-probe/0.1"})
    h = hashlib.sha256()
    total = 0
    with urllib.request.urlopen(request, timeout=timeout) as response, path.open("wb") as out:
        headers = {str(k): str(v) for k, v in response.headers.items()}
        while True:
            block = response.read(1024 * 1024)
            if not block:
                break
            out.write(block)
            h.update(block)
            total += len(block)
    if total == 0:
        raise RuntimeError(f"empty download: {url}")
    return {
        "sha256": h.hexdigest(),
        "compressed_or_file_size_bytes": total,
        "http_last_modified": headers.get("Last-Modified"),
        "http_content_length": headers.get("Content-Length"),
    }


def _split_tab(line: str) -> list[str]:
    return line.rstrip("\r\n").split("\t")


def _probe_plain_gzip_table(path: Path) -> dict[str, Any]:
    with gzip.open(path, "rt", encoding="utf-8-sig", errors="strict") as handle:
        first = handle.readline()
        second = handle.readline()
        if not first:
            raise RuntimeError("empty gzip table")
        header = _split_tab(first)
        first_data = _split_tab(second) if second else []
    return {
        "header_field_count": len(header),
        "header_preview": header[:40],
        "first_data_field_count": len(first_data),
        "first_data_preview": first_data[:8],
    }


def _probe_geo_series_matrix(path: Path) -> dict[str, Any]:
    metadata_titles: list[str] = []
    metadata_accessions: list[str] = []
    metadata_characteristics: list[list[str]] = []
    table_header: list[str] | None = None
    with gzip.open(path, "rt", encoding="utf-8-sig", errors="replace") as handle:
        in_table = False
        for line in handle:
            if line.startswith("!Sample_title"):
                metadata_titles = _split_tab(line)[1:]
            elif line.startswith("!Sample_geo_accession"):
                metadata_accessions = _split_tab(line)[1:]
            elif line.startswith("!Sample_characteristics_ch1"):
                metadata_characteristics.append(_split_tab(line)[1:])
            elif line.startswith("!series_matrix_table_begin"):
                in_table = True
                continue
            elif in_table:
                table_header = _split_tab(line)
                break
    if table_header is None:
        # Some metadata-only series matrices legitimately have no value table.
        table_status = "NO_VALUE_TABLE_HEADER_FOUND"
        table_header = []
    else:
        table_status = "VALUE_TABLE_HEADER_FOUND"
    return {
        "sample_title_count": len(metadata_titles),
        "sample_titles": metadata_titles,
        "sample_geo_accession_count": len(metadata_accessions),
        "sample_geo_accessions": metadata_accessions,
        "sample_characteristics_rows": len(metadata_characteristics),
        "sample_characteristics_preview": [row[:6] for row in metadata_characteristics[:8]],
        "table_status": table_status,
        "table_header_field_count": len(table_header),
        "table_header_preview": table_header[:40],
    }


def _probe_plain_text(path: Path) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    return {
        "line_count": len(lines),
        "preview": lines[:40],
    }


def probe(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    report: dict[str, Any] = {
        "probe_version": "0.1",
        "purpose": "CHRONIC_PROCESSED_SOURCE_IDENTITY_HASH_AND_HEADER_ONLY",
        "chi_bio_outcomes_computed": False,
        "feature_selection_performed": False,
        "state_reduction_fitted": False,
        "raw_methylation_tar_downloaded": False,
        "raw_excluded": RAW_EXCLUDED,
        "sources": {},
        "status": "RUNNING",
    }
    all_pass = True

    for source_id, spec in SOURCES.items():
        path = output_dir / spec["filename"]
        entry: dict[str, Any] = {
            "url": spec["url"],
            "filename": spec["filename"],
            "kind": spec["kind"],
            "preflight_bytes": spec["preflight_bytes"],
        }
        try:
            entry.update(_download(spec["url"], path))
            if entry["compressed_or_file_size_bytes"] != spec["preflight_bytes"]:
                entry["preflight_size_disposition"] = "SIZE_CHANGED_SINCE_PREFLIGHT"
            else:
                entry["preflight_size_disposition"] = "EXACT_SIZE_MATCH"

            if spec["kind"] == "plain_gzip_table":
                entry["structure"] = _probe_plain_gzip_table(path)
            elif spec["kind"] == "geo_series_matrix":
                entry["structure"] = _probe_geo_series_matrix(path)
            elif spec["kind"] == "plain_text":
                entry["structure"] = _probe_plain_text(path)
            else:
                raise RuntimeError(f"unknown source kind: {spec['kind']}")
            entry["status"] = "PASS"
        except Exception as exc:
            all_pass = False
            entry.update(
                {
                    "status": "FAIL",
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
            )
        report["sources"][source_id] = entry

    report["status"] = "PASS_ALL_SELECTED_PROCESSED_SOURCES" if all_pass else "FAIL_ONE_OR_MORE_SOURCES"
    return report


def main() -> int:
    root = Path("development_outputs/chi_bio_chronic_source_probe")
    report = probe(root / "downloads")
    out = root / "GRI_CHI_BIO_CHRONIC_PROCESSED_SOURCE_PROBE.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"].startswith("PASS") else 2


if __name__ == "__main__":
    raise SystemExit(main())
