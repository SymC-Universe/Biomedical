from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

SCHEMA_REL = Path("GRI_v2/config/gri_conglomerate_chi_carrier_schema_v1.json")


class CarrierValidationError(ValueError):
    pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def repo_root_from_here() -> Path:
    return Path(__file__).resolve().parents[2]


def load_schema(repo_root: Path | None = None) -> Dict[str, Any]:
    root = repo_root or repo_root_from_here()
    with (root / SCHEMA_REL).open("r", encoding="utf-8") as f:
        return json.load(f)


def _is_blank(value: str | None) -> bool:
    return value is None or value.strip() == ""


def _parse_finite_number(value: str, field: str, row_number: int) -> float:
    try:
        x = float(value)
    except (TypeError, ValueError) as exc:
        raise CarrierValidationError(
            f"row {row_number}: {field} must be numeric, got {value!r}"
        ) from exc
    if not math.isfinite(x):
        raise CarrierValidationError(
            f"row {row_number}: {field} must be finite, got {value!r}"
        )
    return x


def _parse_bool(value: str, field: str, row_number: int) -> bool:
    v = value.strip().upper()
    if v == "TRUE":
        return True
    if v == "FALSE":
        return False
    raise CarrierValidationError(
        f"row {row_number}: {field} must be TRUE or FALSE, got {value!r}"
    )


def validate_header(fieldnames: Sequence[str] | None, schema: Dict[str, Any], path: Path) -> None:
    if fieldnames is None:
        raise CarrierValidationError(f"{path}: missing CSV header")

    got = list(fieldnames)
    required = list(schema["required_columns"])
    missing = [x for x in required if x not in got]
    if missing:
        raise CarrierValidationError(f"{path}: missing required columns: {missing}")

    forbidden = [x for x in schema["forbidden_columns"] if x in got]
    if forbidden:
        raise CarrierValidationError(f"{path}: forbidden columns present: {forbidden}")


def validate_row(row: Dict[str, str], row_number: int, schema: Dict[str, Any]) -> Tuple[str, ...]:
    required_nonblank = [
        "entity_id",
        "cohort_id",
        "system_id",
        "sample_id",
        "block_id",
        "feature_id",
        "value_status",
        "uncertainty_kind",
        "local_embedded_role",
        "time_order_known",
        "evidence_class",
        "independence_role",
        "source_id",
        "source_digest_or_run",
        "transform_id",
    ]
    for field in required_nonblank:
        if _is_blank(row.get(field)):
            raise CarrierValidationError(f"row {row_number}: {field} may not be blank")

    if row["block_id"] not in schema["allowed_blocks"]:
        raise CarrierValidationError(
            f"row {row_number}: invalid block_id {row['block_id']!r}"
        )
    if row["value_status"] not in schema["allowed_value_status"]:
        raise CarrierValidationError(
            f"row {row_number}: invalid value_status {row['value_status']!r}"
        )
    if row["uncertainty_kind"] not in schema["allowed_uncertainty_kind"]:
        raise CarrierValidationError(
            f"row {row_number}: invalid uncertainty_kind {row['uncertainty_kind']!r}"
        )
    if row["local_embedded_role"] not in schema["allowed_local_embedded_role"]:
        raise CarrierValidationError(
            f"row {row_number}: invalid local_embedded_role {row['local_embedded_role']!r}"
        )
    if row["evidence_class"] not in schema["allowed_evidence_class"]:
        raise CarrierValidationError(
            f"row {row_number}: invalid evidence_class {row['evidence_class']!r}"
        )
    if row["independence_role"] not in schema["allowed_independence_role"]:
        raise CarrierValidationError(
            f"row {row_number}: invalid independence_role {row['independence_role']!r}"
        )

    status = row["value_status"]
    value = row.get("value", "")
    if status in schema["numeric_value_status"]:
        if _is_blank(value):
            raise CarrierValidationError(
                f"row {row_number}: {status} requires a numeric value"
            )
        _parse_finite_number(value, "value", row_number)
    elif status in schema["blank_value_status"]:
        if not _is_blank(value):
            raise CarrierValidationError(
                f"row {row_number}: {status} requires blank value; missing/refused is not zero"
            )

    uncertainty = row.get("uncertainty_value", "")
    if row["uncertainty_kind"] == "NONE":
        if not _is_blank(uncertainty):
            raise CarrierValidationError(
                f"row {row_number}: uncertainty_kind NONE requires blank uncertainty_value"
            )
    else:
        if _is_blank(uncertainty):
            raise CarrierValidationError(
                f"row {row_number}: uncertainty_kind {row['uncertainty_kind']} requires uncertainty_value"
            )
        u = _parse_finite_number(uncertainty, "uncertainty_value", row_number)
        if u < 0:
            raise CarrierValidationError(
                f"row {row_number}: uncertainty_value must be >= 0"
            )

    ordered = _parse_bool(row["time_order_known"], "time_order_known", row_number)
    time_index = row.get("time_index", "")
    if ordered and _is_blank(time_index):
        raise CarrierValidationError(
            f"row {row_number}: time_order_known TRUE requires time_index"
        )
    if (not ordered) and not _is_blank(time_index):
        raise CarrierValidationError(
            f"row {row_number}: time_index populated while time_order_known is FALSE"
        )
    if row["block_id"] == "T" and status in schema["numeric_value_status"] and not ordered:
        raise CarrierValidationError(
            f"row {row_number}: numeric T-block measurement requires directly observed ordering"
        )

    return tuple(row[x] for x in schema["duplicate_key"])


def read_and_validate_csv(
    path: Path,
    schema: Dict[str, Any],
    existing_keys: set[Tuple[str, ...]] | None = None,
) -> Tuple[List[Dict[str, str]], set[Tuple[str, ...]]]:
    keys = existing_keys if existing_keys is not None else set()
    rows: List[Dict[str, str]] = []

    opener = gzip.open if path.name.endswith(".gz") else open
    with opener(path, "rt", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        validate_header(reader.fieldnames, schema, path)
        for i, row in enumerate(reader, start=2):
            key = validate_row(row, i, schema)
            if key in keys:
                raise CarrierValidationError(
                    f"{path}: row {i}: duplicate carrier key {key}"
                )
            keys.add(key)
            rows.append({k: row.get(k, "") for k in schema["required_columns"]})

    return rows, keys


def write_csv(path: Path, rows: Iterable[Dict[str, str]], columns: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def materialize(inputs: Sequence[Path], outdir: Path, repo_root: Path | None = None) -> Dict[str, Any]:
    root = repo_root or repo_root_from_here()
    schema = load_schema(root)

    all_rows: List[Dict[str, str]] = []
    keys: set[Tuple[str, ...]] = set()
    input_records: List[Dict[str, Any]] = []

    for input_path in inputs:
        p = input_path.resolve()
        rows, keys = read_and_validate_csv(p, schema, keys)
        all_rows.extend(rows)
        input_records.append({
            "path": str(p),
            "sha256": sha256_file(p),
            "rows": len(rows),
        })

    carrier_path = outdir / "conglomerate_carrier_long.csv"
    manifest_path = outdir / "conglomerate_carrier_manifest.json"
    write_csv(carrier_path, all_rows, schema["required_columns"])

    by_block = Counter(row["block_id"] for row in all_rows)
    by_status = Counter(row["value_status"] for row in all_rows)
    by_evidence = Counter(row["evidence_class"] for row in all_rows)
    ordered_rows = sum(row["time_order_known"].upper() == "TRUE" for row in all_rows)

    manifest = {
        "schema": "gri-conglomerate-chi-c1-materialization-manifest-v1",
        "carrier_schema": schema["schema"],
        "inputs": input_records,
        "rows_total": len(all_rows),
        "entities_total": len({row["entity_id"] for row in all_rows}),
        "blocks_present": sorted(by_block),
        "rows_by_block": dict(sorted(by_block.items())),
        "rows_by_value_status": dict(sorted(by_status.items())),
        "rows_by_evidence_class": dict(sorted(by_evidence.items())),
        "time_order_known_rows": ordered_rows,
        "duplicate_key_violations": 0,
        "forbidden_columns_present": [],
        "cross_block_aggregation_performed": False,
        "master_score_created": False,
        "diagnostic_or_predictive_model_fit": False,
        "carrier_sha256": sha256_file(carrier_path),
        "carrier_file": carrier_path.name,
        "status": "C1_CARRIER_MATERIALIZED_SCHEMA_VALID",
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate and concatenate capital-Chi block rows without cross-block aggregation."
    )
    parser.add_argument("--input", action="append", required=True, help="Input block CSV; repeat as needed.")
    parser.add_argument("--outdir", required=True, help="Output directory.")
    args = parser.parse_args()

    manifest = materialize(
        [Path(p) for p in args.input],
        Path(args.outdir),
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
