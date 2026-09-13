from __future__ import annotations

"""Read-only provenance probe for public GEO sources reserved for Chi_bio P0-D work.

This script downloads only published supplementary files, records exact hashes,
compressed/uncompressed sizes, and shallow table structure. It performs no
Chi_bio computation, no feature selection, and no biological outcome analysis.
"""

import csv
import gzip
import hashlib
import io
import json
import urllib.request
from pathlib import Path
from typing import Any


SOURCES = {
    "GSE114446_bulk_rna_counts": {
        "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE114nnn/GSE114446/suppl/GSE114446_STCCountsCG.txt.gz",
        "filename": "GSE114446_STCCountsCG.txt.gz",
        "delimiter": "\t",
        "expected_header_tokens": ["SCC25", "SCC1", "SCC6"],
        "role": "SHORT_TERM_BULK_RNA_SOURCE",
    },
    "GSE135604_atac_peakset": {
        "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE135nnn/GSE135604/suppl/GSE135604_ATACpeakset.csv.gz",
        "filename": "GSE135604_ATACpeakset.csv.gz",
        "delimiter": ",",
        "expected_header_tokens": ["SCC25", "SCC1", "SCC6"],
        "role": "DAY5_ATAC_SUBSTRATE_CONTEXT_SOURCE",
    },
    "GSE137524_scc25_pheno": {
        "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE137nnn/GSE137524/suppl/GSE137524_phenoDataSCC25.csv.gz",
        "filename": "GSE137524_phenoDataSCC25.csv.gz",
        "delimiter": ",",
        "expected_header_tokens": [],
        "role": "DAY5_SCRNA_PHENOTYPE_METADATA",
    },
    "GSE137524_scc25_expression": {
        "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE137nnn/GSE137524/suppl/GSE137524_exprsSCC25Matrix.csv.gz",
        "filename": "GSE137524_exprsSCC25Matrix.csv.gz",
        "delimiter": ",",
        "expected_header_tokens": [],
        "role": "DAY5_SCRNA_EXPRESSION_SOURCE",
    },
    "GSE137524_feature_data": {
        "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE137nnn/GSE137524/suppl/GSE137524_featureData.csv.gz",
        "filename": "GSE137524_featureData.csv.gz",
        "delimiter": ",",
        "expected_header_tokens": [],
        "role": "DAY5_SCRNA_FEATURE_METADATA",
    },
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _download(url: str, *, timeout: int = 120) -> tuple[bytes, dict[str, str]]:
    request = urllib.request.Request(url, headers={"User-Agent": "SymC-GRI-source-probe/0.1"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        data = response.read()
        headers = {str(k): str(v) for k, v in response.headers.items()}
    if not data:
        raise RuntimeError(f"empty download: {url}")
    return data, headers


def _shallow_table_probe(compressed: bytes, delimiter: str) -> dict[str, Any]:
    raw = gzip.decompress(compressed)
    text = raw.decode("utf-8-sig", errors="strict")
    reader = csv.reader(io.StringIO(text), delimiter=delimiter)
    try:
        header = next(reader)
    except StopIteration as exc:
        raise RuntimeError("decompressed table is empty") from exc

    row_count = 0
    min_fields = None
    max_fields = None
    first_row: list[str] | None = None
    for row in reader:
        if not row:
            continue
        row_count += 1
        if first_row is None:
            first_row = row[: min(8, len(row))]
        n = len(row)
        min_fields = n if min_fields is None else min(min_fields, n)
        max_fields = n if max_fields is None else max(max_fields, n)

    return {
        "uncompressed_size_bytes": len(raw),
        "header_field_count": len(header),
        "header_preview": header[: min(30, len(header))],
        "data_row_count": row_count,
        "min_data_field_count": min_fields,
        "max_data_field_count": max_fields,
        "first_data_row_preview": first_row,
    }


def probe_sources(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    report: dict[str, Any] = {
        "probe_version": "0.1",
        "purpose": "READ_ONLY_SOURCE_PROVENANCE_NO_CHI_BIO_COMPUTATION",
        "chi_bio_outcomes_computed": False,
        "feature_selection_performed": False,
        "sources": {},
        "status": "RUNNING",
    }

    all_pass = True
    for source_id, spec in SOURCES.items():
        entry: dict[str, Any] = {
            "url": spec["url"],
            "filename": spec["filename"],
            "role": spec["role"],
        }
        try:
            compressed, headers = _download(spec["url"])
            file_path = output_dir / spec["filename"]
            file_path.write_bytes(compressed)
            table = _shallow_table_probe(compressed, spec["delimiter"])
            header_text = "\n".join(table["header_preview"])
            missing_tokens = [
                token for token in spec["expected_header_tokens"] if token not in header_text
            ]
            entry.update(
                {
                    "download_status": "PASS",
                    "compressed_size_bytes": len(compressed),
                    "sha256": sha256_bytes(compressed),
                    "http_last_modified": headers.get("Last-Modified"),
                    "http_etag": headers.get("ETag"),
                    "table_probe": table,
                    "expected_header_tokens_missing_from_preview": missing_tokens,
                }
            )
            if missing_tokens:
                # Header naming is source-specific; this is a provenance warning,
                # not a scientific failure. Preserve it visibly.
                entry["header_token_disposition"] = "WARNING_SOURCE_HEADER_NEEDS_MAPPING"
            else:
                entry["header_token_disposition"] = "PASS_OR_NOT_REQUIRED"
        except Exception as exc:  # fail loud but keep a complete multi-source report
            all_pass = False
            entry.update(
                {
                    "download_status": "FAIL",
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
            )
        report["sources"][source_id] = entry

    report["status"] = "PASS_ALL_DOWNLOADS" if all_pass else "FAIL_ONE_OR_MORE_DOWNLOADS"
    return report


def main() -> int:
    root = Path("development_outputs/chi_bio_geo_source_probe")
    report = probe_sources(root / "downloads")
    out = root / "GRI_CHI_BIO_GEO_SOURCE_PROBE.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS_ALL_DOWNLOADS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
