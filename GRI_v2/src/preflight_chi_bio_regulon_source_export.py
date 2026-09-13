from __future__ import annotations

"""Read-only provenance preflight for candidate regulon exports.

This utility hashes and inventories an already exported interaction table. It
must not score TF activity, select TFs, reduce state dimension, fit an operator,
or compute G1/G2/Chi_bio.
"""

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


REQUIRED_SOURCE_IDS = {"COLLECTRI_CANDIDATE", "DOROTHEA_CANDIDATE"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _delimiter_for(path: Path, explicit: str | None) -> str:
    if explicit is not None:
        if explicit not in {",", "\t"}:
            raise ValueError("delimiter must be comma or tab")
        return explicit
    name = path.name.lower()
    if name.endswith((".tsv", ".tsv.gz", ".txt", ".txt.gz")):
        return "\t"
    return ","


def inventory_export(
    path: Path,
    *,
    source_id: str,
    delimiter: str | None = None,
    expected_columns: tuple[str, ...] | list[str] = (),
) -> dict[str, Any]:
    if source_id not in REQUIRED_SOURCE_IDS:
        raise ValueError(f"unrecognized source_id: {source_id}")
    if not path.is_file():
        raise FileNotFoundError(path)
    if path.suffix.lower() == ".gz":
        raise ValueError(
            "compressed exports must be decompressed to a byte-stable tabular file before this preflight"
        )

    delim = _delimiter_for(path, delimiter)
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle, delimiter=delim)
        try:
            header = next(reader)
        except StopIteration as exc:
            raise ValueError("export is empty") from exc
        if not header or any(not str(x).strip() for x in header):
            raise ValueError("export header contains empty column names")
        if len(header) != len(set(header)):
            raise ValueError("export header contains duplicate column names")

        rows = 0
        bad_width_rows = 0
        for row in reader:
            if not row:
                continue
            rows += 1
            if len(row) != len(header):
                bad_width_rows += 1

    if rows == 0:
        raise ValueError("export has no interaction rows")
    if bad_width_rows:
        raise ValueError(f"export contains {bad_width_rows} rows with wrong field count")

    expected = tuple(expected_columns)
    missing = sorted(set(expected) - set(header))
    if missing:
        raise ValueError("missing expected column(s): " + ", ".join(missing))

    return {
        "status": "PASS_SOURCE_EXPORT_PROVENANCE_ONLY",
        "source_id": source_id,
        "path_name": path.name,
        "sha256": sha256_file(path),
        "delimiter": "TAB" if delim == "\t" else "COMMA",
        "header": header,
        "column_count": len(header),
        "interaction_row_count": rows,
        "expected_columns_checked": list(expected),
        "tf_activity_scored": False,
        "state_coordinates_computed": False,
        "state_dimension_selected": False,
        "operator_fit": False,
        "g1_computed": False,
        "g2_computed": False,
        "chi_bio_computed": False,
        "promotion_effect": "NONE",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("export")
    parser.add_argument("--source-id", required=True, choices=sorted(REQUIRED_SOURCE_IDS))
    parser.add_argument("--delimiter", choices=["comma", "tab"], default=None)
    parser.add_argument("--expected-column", action="append", default=[])
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    delim = None if args.delimiter is None else ("," if args.delimiter == "comma" else "\t")
    result = inventory_export(
        Path(args.export),
        source_id=args.source_id,
        delimiter=delim,
        expected_columns=tuple(args.expected_column),
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
