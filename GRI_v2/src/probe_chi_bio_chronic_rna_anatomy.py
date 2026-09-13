from __future__ import annotations

"""Structure-only anatomy probe for GSE98812_GEOExprsData.txt.gz.

The goal is to learn the exact public table orientation and field roles before
any chronic RNA adapter is written. The probe records row/column anatomy,
identifier-looking fields, and numeric/non-numeric structure. It does not
select features, normalize expression, fit a state, or compute Chi_bio.
"""

import csv
import gzip
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE = Path(
    "development_outputs/chi_bio_chronic_source_probe/downloads/GSE98812_GEOExprsData.txt.gz"
)
OUTPUT = Path(
    "development_outputs/chi_bio_chronic_source_probe/GRI_CHI_BIO_GSE98812_RNA_TABLE_ANATOMY.json"
)


def _is_finite_number(text: str) -> bool:
    try:
        value = float(text)
    except (TypeError, ValueError):
        return False
    return math.isfinite(value)


def _preview(values: list[str], n: int = 20) -> dict[str, list[str]]:
    return {
        "first": values[:n],
        "last": values[-n:] if len(values) > n else values[:],
    }


def probe(path: Path = SOURCE) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)

    with gzip.open(path, "rt", encoding="utf-8-sig", errors="strict", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        try:
            header = next(reader)
        except StopIteration as exc:
            raise RuntimeError("processed RNA table is empty") from exc

        row_field_counts: Counter[int] = Counter()
        rows: list[list[str]] = []
        for row in reader:
            if not row:
                continue
            row_field_counts[len(row)] += 1
            rows.append(row)

    row_summaries = []
    first_field_values = []
    for idx, row in enumerate(rows):
        first_field_values.append(row[0] if row else "")
        numeric_flags = [_is_finite_number(value) for value in row]
        numeric_count = sum(numeric_flags)
        row_summaries.append(
            {
                "row_index": idx,
                "field_count": len(row),
                "first_field": row[0] if row else None,
                "second_field": row[1] if len(row) > 1 else None,
                "numeric_field_count": numeric_count,
                "non_numeric_field_count": len(row) - numeric_count,
                "field_preview": _preview(row, 12),
            }
        )

    header_numeric_count = sum(_is_finite_number(value) for value in header)
    header_gsm_tokens = [value for value in header if value.startswith("GSM")]
    row_gsm_tokens = sorted(
        {
            value
            for row in rows
            for value in row
            if isinstance(value, str) and value.startswith("GSM")
        }
    )

    # Purely structural orientation hints. These do not assign biological
    # meaning beyond what the table itself demonstrates.
    orientation_hints: list[str] = []
    if len(rows) in {22, 23} and len(header) > 1000:
        orientation_hints.append(
            "SMALL_ROW_COUNT_WITH_VERY_WIDE_HEADER_CONSISTENT_WITH_SAMPLE_ROWS_AND_FEATURE_COLUMNS"
        )
    if row_field_counts and max(row_field_counts) != len(header):
        orientation_hints.append("ROW_WIDTH_DIFFERS_FROM_HEADER_WIDTH_REQUIRES_SPECIAL_PARSER_OR_MULTIROW_HEADER_CHECK")
    if len(set(row_field_counts)) == 1:
        orientation_hints.append("ALL_DATA_ROWS_SHARE_ONE_FIELD_COUNT")

    report: dict[str, Any] = {
        "probe_version": "0.1",
        "purpose": "TABLE_ANATOMY_ONLY_NO_FEATURE_SELECTION_NO_CHI_BIO",
        "source_filename": path.name,
        "feature_selection_performed": False,
        "normalization_performed": False,
        "state_reduction_fitted": False,
        "chi_bio_outcomes_computed": False,
        "header": {
            "field_count": len(header),
            "numeric_field_count": header_numeric_count,
            "non_numeric_field_count": len(header) - header_numeric_count,
            "preview": _preview(header, 30),
            "gsm_tokens": header_gsm_tokens,
        },
        "data": {
            "row_count": len(rows),
            "row_field_count_distribution": {
                str(k): v for k, v in sorted(row_field_counts.items())
            },
            "first_field_values": first_field_values,
            "row_summaries": row_summaries,
            "gsm_tokens": row_gsm_tokens,
        },
        "orientation_hints": orientation_hints,
        "disposition": "ANATOMY_RECORDED_NO_BIOLOGICAL_ROLE_INFERRED",
    }
    return report


def main() -> int:
    report = probe()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
