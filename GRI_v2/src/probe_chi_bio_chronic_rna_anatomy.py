from __future__ import annotations

"""Structure-only anatomy probe for GSE98812_GEOExprsData.txt.gz.

The goal is to learn the exact public table orientation and field roles before
any chronic RNA adapter is written. The probe records physical-line anatomy,
separator counts, newline style, and conservative parsed-field structure. It
does not select features, normalize expression, fit a state, or compute
Chi_bio.
"""

import csv
import gzip
import hashlib
import io
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


def _text_edges(text: str, n: int = 220) -> dict[str, str]:
    clean = text.replace("\r", "\\r").replace("\n", "\\n")
    return {
        "first": clean[:n],
        "last": clean[-n:] if len(clean) > n else clean,
    }


def _physical_line_summary(line: str, index: int) -> dict[str, Any]:
    stripped = line.rstrip("\r\n")
    return {
        "line_index": index,
        "character_count_without_newline": len(stripped),
        "tab_count": stripped.count("\t"),
        "comma_count": stripped.count(","),
        "double_quote_count": stripped.count('"'),
        "semicolon_count": stripped.count(";"),
        "space_count": stripped.count(" "),
        "starts_with_quote": stripped.startswith('"'),
        "ends_with_quote": stripped.endswith('"'),
        "text_edges": _text_edges(stripped),
    }


def _parse_with_delimiter(text: str, delimiter: str) -> dict[str, Any]:
    reader = csv.reader(io.StringIO(text, newline=""), delimiter=delimiter)
    rows = [row for row in reader if row]
    field_counts = Counter(len(row) for row in rows)
    preview_rows = []
    for i, row in enumerate(rows[:25]):
        numeric = sum(_is_finite_number(value) for value in row)
        preview_rows.append(
            {
                "parsed_row_index": i,
                "field_count": len(row),
                "numeric_field_count": numeric,
                "non_numeric_field_count": len(row) - numeric,
                "field_preview": _preview(row, 12),
            }
        )
    return {
        "parsed_row_count": len(rows),
        "field_count_distribution": {str(k): v for k, v in sorted(field_counts.items())},
        "first_25_parsed_rows": preview_rows,
    }


def probe(path: Path = SOURCE) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)

    compressed = path.read_bytes()
    raw = gzip.decompress(compressed)
    text = raw.decode("utf-8-sig", errors="strict")
    physical_lines = text.splitlines(keepends=True)
    nonempty_lines = [line for line in physical_lines if line.rstrip("\r\n")]

    newline_counts = {
        "CRLF": raw.count(b"\r\n"),
        "LF_total": raw.count(b"\n"),
        "CR_total": raw.count(b"\r"),
    }
    newline_counts["LF_not_preceded_by_CR"] = newline_counts["LF_total"] - newline_counts["CRLF"]
    newline_counts["CR_not_followed_by_LF"] = newline_counts["CR_total"] - newline_counts["CRLF"]

    physical_summaries = [
        _physical_line_summary(line, idx) for idx, line in enumerate(nonempty_lines)
    ]
    length_distribution = Counter(x["character_count_without_newline"] for x in physical_summaries)
    tab_distribution = Counter(x["tab_count"] for x in physical_summaries)
    comma_distribution = Counter(x["comma_count"] for x in physical_summaries)

    # Parse both likely separators without assigning biological semantics.
    tab_parse = _parse_with_delimiter(text, "\t")
    comma_parse = _parse_with_delimiter(text, ",")

    # Extra structural check: if the first physical line is much wider than the
    # remaining lines, preserve that fact explicitly rather than assuming it is
    # a conventional header.
    orientation_hints: list[str] = []
    if physical_summaries:
        first_len = physical_summaries[0]["character_count_without_newline"]
        later_lengths = [x["character_count_without_newline"] for x in physical_summaries[1:]]
        if later_lengths and first_len > 10 * max(later_lengths):
            orientation_hints.append("FIRST_PHYSICAL_LINE_IS_MORE_THAN_10X_WIDER_THAN_EVERY_LATER_LINE")
        if len(physical_summaries) in {23, 24}:
            orientation_hints.append("PHYSICAL_LINE_COUNT_IS_COMPATIBLE_WITH_ONE_WIDE_FEATURE_AXIS_PLUS_22_OR_23_SAMPLE_ROWS")
    if len(tab_parse["field_count_distribution"]) > 1:
        orientation_hints.append("TAB_PARSE_HAS_NONRECTANGULAR_ROW_WIDTHS")
    if len(comma_parse["field_count_distribution"]) > 1:
        orientation_hints.append("COMMA_PARSE_HAS_NONRECTANGULAR_ROW_WIDTHS")

    # Physical lines are small enough here that first/last 30 is safe. If a
    # future file is large, keep only the edges.
    if len(physical_summaries) <= 60:
        line_edge_sample = physical_summaries
    else:
        line_edge_sample = physical_summaries[:30] + physical_summaries[-30:]

    report: dict[str, Any] = {
        "probe_version": "0.2",
        "purpose": "PHYSICAL_AND_PARSED_TABLE_ANATOMY_ONLY_NO_FEATURE_SELECTION_NO_CHI_BIO",
        "source_filename": path.name,
        "compressed_sha256": hashlib.sha256(compressed).hexdigest(),
        "decompressed_sha256": hashlib.sha256(raw).hexdigest(),
        "compressed_size_bytes": len(compressed),
        "decompressed_size_bytes": len(raw),
        "feature_selection_performed": False,
        "normalization_performed": False,
        "state_reduction_fitted": False,
        "chi_bio_outcomes_computed": False,
        "source_text_rewritten": False,
        "newline_counts": newline_counts,
        "physical_lines": {
            "total_with_empty": len(physical_lines),
            "nonempty": len(nonempty_lines),
            "character_length_distribution": {
                str(k): v for k, v in sorted(length_distribution.items())
            },
            "tab_count_distribution": {str(k): v for k, v in sorted(tab_distribution.items())},
            "comma_count_distribution": {str(k): v for k, v in sorted(comma_distribution.items())},
            "first_last_line_summaries": line_edge_sample,
        },
        "tab_parse": tab_parse,
        "comma_parse": comma_parse,
        "orientation_hints": orientation_hints,
        "disposition": "PHYSICAL_ANATOMY_RECORDED_NO_BIOLOGICAL_ROLE_INFERRED",
    }
    return report


def main() -> int:
    report = probe()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    # Print a compact but sufficient summary; the complete report is archived.
    compact = {
        "probe_version": report["probe_version"],
        "compressed_sha256": report["compressed_sha256"],
        "decompressed_sha256": report["decompressed_sha256"],
        "compressed_size_bytes": report["compressed_size_bytes"],
        "decompressed_size_bytes": report["decompressed_size_bytes"],
        "newline_counts": report["newline_counts"],
        "physical_lines": report["physical_lines"],
        "tab_parse": report["tab_parse"],
        "comma_parse": report["comma_parse"],
        "orientation_hints": report["orientation_hints"],
        "disposition": report["disposition"],
    }
    print(json.dumps(compact, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
