from __future__ import annotations

"""Acquire and canonically fingerprint a CollecTRI human regulon export.

This is provenance-only P0-D machinery. It is deliberately prohibited from
loading SCC25/TCGA expression, estimating TF activity, choosing a regulon panel,
fitting an operator, or computing G1/G2/Chi_bio.
"""

import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path

import pandas as pd


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _canonicalize(frame: pd.DataFrame) -> pd.DataFrame:
    required = {"source", "target", "weight"}
    missing = required - set(frame.columns)
    if missing:
        raise RuntimeError(f"CollecTRI export missing required columns: {sorted(missing)}")
    out = frame.copy()
    # Canonical row order is independent of provider/API return ordering.
    sort_cols = ["source", "target", "weight"] + [
        c for c in out.columns if c not in {"source", "target", "weight"}
    ]
    return out.sort_values(sort_cols, kind="mergesort", na_position="last").reset_index(drop=True)


def run_probe(output_dir: Path) -> dict:
    import decoupler as dc

    version = importlib.metadata.version("decoupler")
    frame = dc.op.collectri(organism="human")
    if not isinstance(frame, pd.DataFrame) or frame.empty:
        raise RuntimeError("decoupler CollecTRI human export was empty or not a DataFrame")
    canonical = _canonicalize(frame)

    output_dir.mkdir(parents=True, exist_ok=True)
    tsv = output_dir / "collectri_human_canonical.tsv"
    canonical.to_csv(tsv, sep="\t", index=False, lineterminator="\n")

    weights = pd.to_numeric(canonical["weight"], errors="coerce")
    if weights.isna().any():
        raise RuntimeError("CollecTRI weight column contains nonnumeric values")

    duplicated_exact = int(canonical.duplicated().sum())
    duplicated_pair = int(canonical.duplicated(subset=["source", "target"], keep=False).sum())
    pair_sign_counts = (
        canonical.assign(_sign=weights.map(lambda x: -1 if x < 0 else (1 if x > 0 else 0)))
        .groupby(["source", "target"], dropna=False)["_sign"]
        .nunique()
    )
    contradictory_signed_pairs = int((pair_sign_counts > 1).sum())

    result = {
        "status": "PASS_COLLECTRI_EXPORT_PROVENANCE_ONLY",
        "provider_call": "decoupler.op.collectri(organism='human')",
        "decoupler_version": version,
        "output_file": str(tsv),
        "sha256": _sha256(tsv),
        "rows": int(canonical.shape[0]),
        "columns": list(canonical.columns),
        "unique_sources_tf": int(canonical["source"].nunique(dropna=True)),
        "unique_targets": int(canonical["target"].nunique(dropna=True)),
        "positive_edges": int((weights > 0).sum()),
        "negative_edges": int((weights < 0).sum()),
        "zero_weight_edges": int((weights == 0).sum()),
        "exact_duplicate_rows": duplicated_exact,
        "rows_in_duplicated_source_target_pairs": duplicated_pair,
        "source_target_pairs_with_multiple_signs": contradictory_signed_pairs,
        "real_expression_files_opened": False,
        "tf_activity_scored": False,
        "state_dimension_selected": False,
        "regulon_panel_selected": False,
        "operator_fit": False,
        "g1_computed": False,
        "g2_computed": False,
        "chi_bio_computed": False,
        "promotion_effect": "NONE",
        "note": "This fingerprints the provider export returned at execution time. Repository commit identity alone does not freeze OmniPath/provider bytes; the exact TSV hash is the relevant future source lock if scientifically selected.",
    }
    report = output_dir / "collectri_human_export_provenance.json"
    report.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        default="development_outputs/chi_bio_regulon_source/collectri_20260913",
    )
    args = parser.parse_args()
    result = run_probe(Path(args.output_dir))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
