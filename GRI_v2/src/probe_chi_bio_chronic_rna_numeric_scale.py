from __future__ import annotations

"""Read-only numeric-scale probe for the frozen GSE98812 processed RNA table.

This source-qualification probe records distributional anatomy needed to decide
whether the public table is already log-scale or remains on a normalized count-
like scale. It does not select genes, compare treated/control biology, fit a
state/operator, inspect Chi placement, or compute Chi_bio.
"""

import csv
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np


SOURCE = Path(
    "development_outputs/chi_bio_chronic_source_probe/downloads/GSE98812_GEOExprsData.txt.gz"
)
OUTPUT = Path(
    "development_outputs/chi_bio_chronic_source_probe/GRI_CHI_BIO_GSE98812_RNA_NUMERIC_SCALE.json"
)

MAIN_COLUMNS = tuple(
    [f"C{i}.PBS" for i in range(1, 12)]
    + [f"C{i}.100nM" for i in range(1, 12)]
)


def _quantiles(values: np.ndarray) -> dict[str, float]:
    return {
        "q00": float(np.quantile(values, 0.00)),
        "q25": float(np.quantile(values, 0.25)),
        "q50": float(np.quantile(values, 0.50)),
        "q75": float(np.quantile(values, 0.75)),
        "q90": float(np.quantile(values, 0.90)),
        "q95": float(np.quantile(values, 0.95)),
        "q99": float(np.quantile(values, 0.99)),
        "q999": float(np.quantile(values, 0.999)),
        "max": float(np.max(values)),
    }


def probe(path: Path = SOURCE) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)

    compressed = path.read_bytes()
    with gzip.open(path, "rt", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        header = next(reader)
        header = [x.strip('"') for x in header]
        if not header or header[0] != "GENE":
            raise RuntimeError("unexpected chronic RNA header")
        missing = sorted(set(MAIN_COLUMNS) - set(header))
        if missing:
            raise RuntimeError(f"missing frozen main-trajectory columns: {missing}")
        idx = {name: header.index(name) for name in MAIN_COLUMNS}

        per_column_values: dict[str, list[float]] = {name: [] for name in MAIN_COLUMNS}
        gene_rows = 0
        for row in reader:
            if not row:
                continue
            gene_rows += 1
            if len(row) != len(header):
                raise RuntimeError(
                    f"nonrectangular processed RNA row {gene_rows}: {len(row)} != {len(header)}"
                )
            for name, j in idx.items():
                value = float(row[j])
                if not np.isfinite(value):
                    raise RuntimeError(f"nonfinite value in {name} row {gene_rows}")
                if value < 0:
                    raise RuntimeError(f"negative value in {name} row {gene_rows}")
                per_column_values[name].append(value)

    column_reports: dict[str, Any] = {}
    q75s: list[float] = []
    maxima: list[float] = []
    noninteger_fractions: list[float] = []
    for name in MAIN_COLUMNS:
        values = np.asarray(per_column_values[name], dtype=float)
        nonzero = values[values > 0]
        noninteger = np.abs(values - np.round(values)) > 1e-9
        qs_all = _quantiles(values)
        qs_nonzero = _quantiles(nonzero) if nonzero.size else None
        q75s.append(qs_all["q75"])
        maxima.append(qs_all["max"])
        noninteger_fractions.append(float(np.mean(noninteger)))
        column_reports[name] = {
            "n_values": int(values.size),
            "zero_fraction": float(np.mean(values == 0)),
            "noninteger_fraction": float(np.mean(noninteger)),
            "sum": float(np.sum(values)),
            "all_value_quantiles": qs_all,
            "nonzero_value_quantiles": qs_nonzero,
        }

    # Mechanical scale flags only. They are descriptive and not a substitute
    # for source documentation about the normalization pipeline.
    global_max = max(maxima)
    median_q75 = float(np.median(np.asarray(q75s)))
    median_noninteger_fraction = float(np.median(np.asarray(noninteger_fractions)))
    scale_hints: list[str] = []
    if global_max > 100.0:
        scale_hints.append("VALUES_EXCEED_TYPICAL_LOG2_EXPRESSION_RANGE")
    if median_q75 > 20.0:
        scale_hints.append("MEDIAN_SAMPLE_Q75_EXCEEDS_TYPICAL_LOG2_EXPRESSION_RANGE")
    if median_noninteger_fraction > 0.10:
        scale_hints.append("SUBSTANTIAL_FRACTIONAL_VALUES_PRESENT")
    if max(q75s) / max(min(q75s), 1e-12) < 1.25:
        scale_hints.append("SAMPLE_Q75_VALUES_ARE_TIGHTLY_ALIGNED")

    return {
        "probe_version": "0.1",
        "purpose": "NUMERIC_SCALE_AND_SOURCE_ANATOMY_ONLY_NO_FEATURE_SELECTION_NO_BIOLOGICAL_COMPARISON_NO_CHI_BIO",
        "source_filename": path.name,
        "compressed_sha256": hashlib.sha256(compressed).hexdigest(),
        "main_trajectory_columns": list(MAIN_COLUMNS),
        "gene_rows": gene_rows,
        "column_reports": column_reports,
        "cross_column_summary": {
            "sample_q75_min": float(min(q75s)),
            "sample_q75_median": median_q75,
            "sample_q75_max": float(max(q75s)),
            "sample_max_value_min": float(min(maxima)),
            "sample_max_value_max": float(global_max),
            "median_noninteger_fraction": median_noninteger_fraction,
        },
        "scale_hints": scale_hints,
        "feature_selection_performed": False,
        "normalization_performed": False,
        "treatment_control_comparison_performed": False,
        "state_reduction_fitted": False,
        "operator_fit": False,
        "chi_bio_outcomes_computed": False,
        "disposition": "NUMERIC_SCALE_RECORDED_SOURCE_DOCUMENTATION_STILL_CONTROLS_SEMANTIC_INTERPRETATION",
    }


def main() -> int:
    report = probe()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
