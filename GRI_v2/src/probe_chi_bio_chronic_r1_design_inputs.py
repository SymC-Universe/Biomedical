from __future__ import annotations

"""Outcome-blind chronic SCC25 R1 design-input qualification.

This probe is deliberately restricted to the 11 PBS weekly states from the
frozen GSE98812 processed RNA source. It verifies that the prospectively chosen
control-only detectability gate and the already-approved A3 ranks (r=2,3) are
numerically viable before any cetuximab trajectory is read by an empirical
transition runner.

The source study reports RSEM gene counts followed by upper-quartile
normalization and log transformation for analysis. The public processed table
has already been machine-qualified as a fractional, large count-like normalized
matrix. Therefore this probe uses log2(value + 1) directly and never recomputes
CPM/library-size normalization.

Primary feature gate (chosen before this probe is run):
    normalized source value >= 1 in at least 6 of 11 PBS states.

Bounded robustness diagnostics (not eligible to replace the primary gate after
inspection):
    thresholds 0.1 and 10, also in at least 6 of 11 PBS states.

Hard pre-outcome viability requirement for the primary gate:
    >= 100 retained genes and PBS-centered numerical rank >= 3.

The probe does NOT read CTX columns, fit a temporal operator, compare arms,
compute a unit-circle result, select a rank winner, or compute Chi_bio.
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
    "development_outputs/chi_bio_chronic_source_probe/GRI_CHI_BIO_GSE98812_R1_DESIGN_INPUTS.json"
)

EXPECTED_SOURCE_SHA256 = "1ce13bae71bd38f619261ec0ca5dcef5dd70b967083cee059e94758aaaf6abb5"
PBS_COLUMNS = tuple(f"C{i}.PBS" for i in range(1, 12))
PRIMARY_THRESHOLD = 1.0
ROBUSTNESS_THRESHOLDS = (0.1, 10.0)
MIN_PRESENT_STATES = 6
MIN_RETAINED_GENES = 100
MIN_CENTERED_RANK = 3


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _load_pbs(path: Path) -> tuple[list[str], np.ndarray]:
    if not path.exists():
        raise FileNotFoundError(path)
    observed_sha = _sha256(path)
    if observed_sha != EXPECTED_SOURCE_SHA256:
        raise RuntimeError(
            f"chronic RNA source SHA mismatch: {observed_sha} != {EXPECTED_SOURCE_SHA256}"
        )

    genes: list[str] = []
    rows: list[list[float]] = []
    with gzip.open(path, "rt", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        header = [x.strip('"') for x in next(reader)]
        if not header or header[0] != "GENE":
            raise RuntimeError("unexpected chronic RNA header")
        missing = sorted(set(PBS_COLUMNS) - set(header))
        if missing:
            raise RuntimeError(f"missing frozen PBS columns: {missing}")
        indices = [header.index(name) for name in PBS_COLUMNS]

        for row_number, row in enumerate(reader, start=2):
            if not row:
                continue
            if len(row) != len(header):
                raise RuntimeError(
                    f"nonrectangular processed RNA row {row_number}: {len(row)} != {len(header)}"
                )
            gene = row[0].strip('"')
            values = [float(row[j]) for j in indices]
            if not np.all(np.isfinite(values)):
                raise RuntimeError(f"nonfinite PBS value at row {row_number}")
            if np.any(np.asarray(values) < 0):
                raise RuntimeError(f"negative PBS value at row {row_number}")
            genes.append(gene)
            rows.append(values)

    if len(set(genes)) != len(genes):
        raise RuntimeError("duplicate GENE identifiers in chronic processed source")
    matrix = np.asarray(rows, dtype=float)
    if matrix.shape != (20531, 11):
        raise RuntimeError(f"unexpected PBS matrix shape: {matrix.shape}")
    return genes, matrix


def _gate_summary(genes: list[str], raw: np.ndarray, threshold: float) -> dict[str, Any]:
    keep = np.count_nonzero(raw >= threshold, axis=1) >= MIN_PRESENT_STATES
    kept_genes = [gene for gene, flag in zip(genes, keep, strict=True) if bool(flag)]
    kept_raw = raw[keep, :]
    transformed = np.log2(kept_raw + 1.0)

    # A3 basis orientation is genes x PBS states; center each gene using PBS only.
    centered = transformed - transformed.mean(axis=1, keepdims=True)
    state_matrix = centered.T  # 11 states x retained genes
    singular_values = np.linalg.svd(state_matrix, full_matrices=False, compute_uv=False)
    numerical_rank = int(np.linalg.matrix_rank(state_matrix))
    total_ss = float(np.sum(singular_values**2))
    explained = (
        (singular_values**2 / total_ss).tolist() if total_ss > 0 else [0.0] * len(singular_values)
    )

    gene_blob = "\n".join(kept_genes).encode("utf-8")
    return {
        "threshold": threshold,
        "minimum_present_pbs_states": MIN_PRESENT_STATES,
        "retained_gene_count": int(np.count_nonzero(keep)),
        "retained_gene_id_sha256": hashlib.sha256(gene_blob).hexdigest(),
        "pbs_state_count": 11,
        "pbs_centered_numerical_rank": numerical_rank,
        "singular_values": [float(x) for x in singular_values.tolist()],
        "explained_variance_fraction": [float(x) for x in explained],
        "cumulative_explained_r2": float(sum(explained[:2])),
        "cumulative_explained_r3": float(sum(explained[:3])),
        "a3_rank2_algebraically_available": numerical_rank >= 2,
        "a3_rank3_algebraically_available": numerical_rank >= 3,
    }


def probe(path: Path = SOURCE) -> dict[str, Any]:
    genes, raw = _load_pbs(path)
    thresholds = (PRIMARY_THRESHOLD,) + ROBUSTNESS_THRESHOLDS
    summaries = {str(t): _gate_summary(genes, raw, t) for t in thresholds}
    primary = summaries[str(PRIMARY_THRESHOLD)]
    primary_pass = (
        primary["retained_gene_count"] >= MIN_RETAINED_GENES
        and primary["pbs_centered_numerical_rank"] >= MIN_CENTERED_RANK
    )

    return {
        "probe_version": "0.1",
        "purpose": "CHRONIC_R1_PBS_ONLY_PREOUTCOME_DESIGN_INPUT_QUALIFICATION",
        "source_filename": path.name,
        "source_sha256": _sha256(path),
        "source_semantics": "RSEM_GENE_COUNTS_UPPER_QUARTILE_NORMALIZED_PUBLIC_PROCESSED_TABLE",
        "transformation": "log2(source_value + 1)",
        "library_size_or_cpm_renormalization": False,
        "pbs_columns": list(PBS_COLUMNS),
        "ctx_columns_read": False,
        "temporal_operator_fit": False,
        "arm_comparison_performed": False,
        "unit_circle_result_computed": False,
        "chi_bio_computed": False,
        "rank_winner_selected": False,
        "feature_gate": {
            "primary_threshold": PRIMARY_THRESHOLD,
            "minimum_present_pbs_states": MIN_PRESENT_STATES,
            "primary_gate_frozen_before_probe": True,
            "robustness_thresholds_diagnostic_only": list(ROBUSTNESS_THRESHOLDS),
            "post_probe_threshold_switch_allowed": False,
            "minimum_retained_genes_for_viability": MIN_RETAINED_GENES,
            "minimum_pbs_centered_rank_for_viability": MIN_CENTERED_RANK,
        },
        "gate_summaries": summaries,
        "primary_gate_disposition": (
            "PASS_PRIMARY_GATE_A3_RANKS_NUMERICALLY_AVAILABLE"
            if primary_pass
            else "REFUSE_PRIMARY_GATE_REQUIRES_NEW_PROSPECTIVE_DESIGN"
        ),
    }


def main() -> int:
    report = probe()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["primary_gate_disposition"].startswith("PASS") else 2


if __name__ == "__main__":
    raise SystemExit(main())
