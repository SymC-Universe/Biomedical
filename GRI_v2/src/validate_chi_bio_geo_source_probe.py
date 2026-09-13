from __future__ import annotations

"""Cross-file identity validation for the read-only Chi_bio GEO source probe.

This script validates source naming/shape relationships only. It performs no
feature selection, candidate fitting, Chi_bio calculation, or phenotype test.
"""

import csv
import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Iterable


ROOT = Path("development_outputs/chi_bio_geo_source_probe/downloads")
CONFIG = Path("config")


def _header(path: Path, delimiter: str) -> list[str]:
    with gzip.open(path, "rt", encoding="utf-8-sig", newline="") as handle:
        return next(csv.reader(handle, delimiter=delimiter))


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _first_column(path: Path, delimiter: str) -> list[str]:
    values: list[str] = []
    with gzip.open(path, "rt", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle, delimiter=delimiter)
        next(reader)
        for row in reader:
            if row:
                values.append(row[0])
    return values


def _feature_gene_short_names(path: Path) -> list[str]:
    values: list[str] = []
    with gzip.open(path, "rt", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        try:
            idx = header.index("gene_short_name")
        except ValueError as exc:
            raise RuntimeError("featureData lacks gene_short_name column") from exc
        for row in reader:
            if row:
                values.append(row[idx])
    return values


def _pheno_rows(path: Path) -> tuple[list[str], Counter[tuple[str, str]], set[str]]:
    ids: list[str] = []
    counts: Counter[tuple[str, str]] = Counter()
    cells: set[str] = set()
    with gzip.open(path, "rt", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise RuntimeError("phenoData has no header")
        unnamed = reader.fieldnames[0]
        for row in reader:
            ids.append(row[unnamed])
            counts[(row["treatment"], row["replicate"])] += 1
            cells.add(row["cell"])
            if row[unnamed] != row["samples"]:
                raise RuntimeError("phenoData row name and samples column disagree")
    return ids, counts, cells


def _assert_same_set(actual: Iterable[str], expected: Iterable[str], label: str) -> None:
    a = set(actual)
    e = set(expected)
    if a != e:
        raise RuntimeError(
            f"{label} set mismatch: missing={sorted(e-a)[:10]}, unexpected={sorted(a-e)[:10]}"
        )


def validate() -> dict:
    report: dict = {
        "validation_version": "0.1",
        "purpose": "SOURCE_IDENTITY_AND_CROSS_FILE_PROVENANCE_ONLY",
        "chi_bio_outcomes_computed": False,
        "feature_selection_performed": False,
        "checks": {},
        "status": "RUNNING",
    }

    # GSE114446 processed matrix -> frozen GEO column map.
    bulk_path = ROOT / "GSE114446_STCCountsCG.txt.gz"
    bulk_map = json.loads(
        (CONFIG / "gri_hnscc_shortterm_bulk_rna_column_map_p0d_v0_1.json").read_text(
            encoding="utf-8"
        )
    )
    bulk_header = _header(bulk_path, "\t")
    bulk_columns = bulk_header[1:]
    expected_bulk = [row["column"] for row in bulk_map["columns"]]
    _assert_same_set(bulk_columns, expected_bulk, "GSE114446 processed sample columns")
    bulk_sha = _sha256(bulk_path)
    if bulk_sha != bulk_map["processed_file_sha256"]:
        raise RuntimeError("GSE114446 processed file SHA256 does not match frozen column map")
    report["checks"]["GSE114446_COLUMN_MAP"] = {
        "status": "PASS",
        "processed_sample_columns": len(bulk_columns),
        "mapped_columns": len(expected_bulk),
        "exact_set_match": True,
        "sha256": bulk_sha,
        "header_order_preserved_separately": bulk_columns,
    }

    # GSE135604 processed ATAC header -> nominal manifest minus explicit QC failure.
    atac_path = ROOT / "GSE135604_ATACpeakset.csv.gz"
    atac_manifest = json.loads(
        (CONFIG / "gri_hnscc_day5_atac_manifest_p0d_v0_1.json").read_text(encoding="utf-8")
    )
    atac_header = _header(atac_path, ",")
    coordinate_fields = ["", "seqnames", "start", "end", "width", "strand"]
    if atac_header[:6] != coordinate_fields:
        raise RuntimeError(f"unexpected ATAC coordinate header: {atac_header[:6]!r}")
    processed_atac = atac_header[6:]
    expected_atac: list[str] = []
    for cell, block in atac_manifest["samples"].items():
        for condition, rows in block.items():
            for row in rows:
                if row["processed_peak_status"] == "SAMPLE_RECORD_QC_FAILURE_NO_PROCESSED_PEAK_FILE":
                    continue
                expected_atac.append(f"{cell}{condition}{row['replicate']}")
    _assert_same_set(processed_atac, expected_atac, "GSE135604 processed ATAC sample columns")
    if "SCC1PBS2" in processed_atac:
        raise RuntimeError("SCC1PBS2 unexpectedly present despite frozen QC failure")
    report["checks"]["GSE135604_PROCESSED_PANEL"] = {
        "status": "PASS",
        "processed_sample_columns": len(processed_atac),
        "expected_after_qc": len(expected_atac),
        "excluded_qc_column": "SCC1PBS2",
        "excluded_qc_column_absent": True,
        "sha256": _sha256(atac_path),
        "processed_columns": processed_atac,
    }

    # GSE137524 SCC25 expression <-> pheno <-> feature identity.
    expr_path = ROOT / "GSE137524_exprsSCC25Matrix.csv.gz"
    pheno_path = ROOT / "GSE137524_phenoDataSCC25.csv.gz"
    feature_path = ROOT / "GSE137524_featureData.csv.gz"

    expr_header = _header(expr_path, ",")
    expr_cell_ids = expr_header[1:]
    pheno_ids, pheno_counts, cell_names = _pheno_rows(pheno_path)
    if expr_cell_ids != pheno_ids:
        _assert_same_set(expr_cell_ids, pheno_ids, "GSE137524 expression/pheno cell IDs")
        order_status = "SET_MATCH_ORDER_DIFFERS"
    else:
        order_status = "EXACT_ORDER_MATCH"
    if cell_names != {"SCC25"}:
        raise RuntimeError(f"SCC25 phenoData contains unexpected cell labels: {sorted(cell_names)}")

    expr_genes = _first_column(expr_path, ",")
    feature_genes = _feature_gene_short_names(feature_path)
    if expr_genes != feature_genes:
        _assert_same_set(expr_genes, feature_genes, "GSE137524 expression/feature gene IDs")
        gene_order_status = "SET_MATCH_ORDER_DIFFERS"
    else:
        gene_order_status = "EXACT_ORDER_MATCH"

    report["checks"]["GSE137524_SCC25_MATRIX_IDENTITY"] = {
        "status": "PASS",
        "expression_cells": len(expr_cell_ids),
        "pheno_rows": len(pheno_ids),
        "cell_identity_order_status": order_status,
        "expression_gene_rows": len(expr_genes),
        "feature_rows": len(feature_genes),
        "gene_identity_order_status": gene_order_status,
        "pheno_counts_by_treatment_replicate": {
            f"{treatment}_{replicate}": count
            for (treatment, replicate), count in sorted(pheno_counts.items())
        },
        "expression_sha256": _sha256(expr_path),
        "pheno_sha256": _sha256(pheno_path),
        "feature_sha256": _sha256(feature_path),
    }

    report["status"] = "PASS_ALL_SOURCE_IDENTITY_RELATIONS"
    return report


def main() -> int:
    result = validate()
    out = Path("development_outputs/chi_bio_geo_source_probe/GRI_CHI_BIO_GEO_SOURCE_IDENTITY_VALIDATION.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
