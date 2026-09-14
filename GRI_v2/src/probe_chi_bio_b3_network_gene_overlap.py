from __future__ import annotations

"""Outcome-free B3 raw-identifier namespace diagnostic.

This module preserves the first exact-match probe as a provenance diagnostic.
GSE98812 stores its raw GENE field as SYMBOL|ENTREZID, whereas CollecTRI and
DoRothEA targets are gene symbols. Direct exact matching of those two raw
namespaces is therefore not a valid regulon-support test and is expected to
produce zero overlap.

The canonical B3 support qualification is
``probe_chi_bio_b3_network_symbol_mapping``. That probe deterministically maps
the frozen GSE98812 namespace before exact matching and is the only B3 overlap
probe that may be used for downstream representation qualification.

This diagnostic never reads expression values, never scores TF activity, never
selects a state dimension, and never fits an operator.
"""

from io import BytesIO
import gzip
import hashlib
import json
from pathlib import Path
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import pandas as pd

from src.probe_chi_bio_collectri_export import (
    _apply_decoupler_220_human_semantics,
    _canonicalize as _canonicalize_collectri,
    _download_exact_source as _download_collectri,
)
from src.probe_chi_bio_dorothea_export import (
    _canonicalize as _canonicalize_dorothea,
    _download_exact_source as _download_dorothea,
    _read_rda,
)


GSE_URL = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE98nnn/GSE98812/suppl/GSE98812_GEOExprsData.txt.gz"
GSE_SHA256 = "1ce13bae71bd38f619261ec0ca5dcef5dd70b967083cee059e94758aaaf6abb5"
EXPECTED_GENE_ROWS = 20_531
TMIN = 5
DOROTHEA_LEVELS = ("A", "B", "C")
DOROTHEA_CONFIDENCE_DENOMINATOR = {"A": 1.0, "B": 2.0, "C": 3.0}
RAW_NAMESPACE_DIAGNOSTIC_STATUS = "DIAGNOSTIC_B3_RAW_IDENTIFIER_NAMESPACE_MISMATCH_EXPECTED"
CANONICAL_B3_OVERLAP_PROBE = "src.probe_chi_bio_b3_network_symbol_mapping"


def _download_gse(attempts: int = 4) -> tuple[bytes, list[dict]]:
    history: list[dict] = []
    last: Exception | None = None
    for attempt in range(1, attempts + 1):
        req = Request(GSE_URL, headers={"User-Agent": "GRI-Chi-bio-B3-overlap/0.1"})
        try:
            with urlopen(req, timeout=120) as response:
                status = int(getattr(response, "status", response.getcode()))
                payload = response.read()
            history.append({"attempt": attempt, "status_code": status, "bytes_received": len(payload)})
            if status == 200 and payload:
                return payload, history
            last = RuntimeError(f"unexpected HTTP {status} or empty GSE98812 payload")
        except (HTTPError, URLError, TimeoutError) as exc:
            history.append({"attempt": attempt, "error": f"{type(exc).__name__}: {exc}"})
            last = exc
        if attempt < attempts:
            time.sleep((2, 5, 10)[min(attempt - 1, 2)])
    raise RuntimeError(f"GSE98812 unavailable after {attempts} bounded attempts: {last}")


def _gse_gene_universe(payload: bytes) -> list[str]:
    digest = hashlib.sha256(payload).hexdigest()
    if digest != GSE_SHA256:
        raise RuntimeError(f"GSE98812 source SHA drift: {digest} != {GSE_SHA256}")
    raw = gzip.decompress(payload)
    # Deliberately parse ONLY the raw identifier column. Expression values are
    # not opened by this diagnostic step.
    genes = pd.read_csv(BytesIO(raw), sep="\t", usecols=["GENE"], dtype=str)["GENE"].str.strip()
    if len(genes) != EXPECTED_GENE_ROWS:
        raise RuntimeError(f"unexpected GSE98812 gene-row count: {len(genes)}")
    if genes.isna().any() or genes.eq("").any() or genes.duplicated().any():
        raise RuntimeError("GSE98812 raw GENE universe contains missing/duplicate identifiers")
    if not genes.str.contains("|", regex=False).all():
        raise RuntimeError("GSE98812 raw GENE namespace no longer matches frozen SYMBOL|ENTREZID grammar")
    return genes.tolist()


def _eligibility(frame: pd.DataFrame, source_col: str, target_col: str, genes: set[str]) -> dict:
    supported = frame.loc[frame[target_col].isin(genes)].copy()
    target_counts = supported.groupby(source_col, sort=True)[target_col].nunique()
    eligible = target_counts[target_counts >= TMIN].sort_index()
    all_sources = sorted(frame[source_col].astype(str).unique())
    eligible_sources = eligible.index.astype(str).tolist()
    return {
        "source_count_total": len(all_sources),
        "target_count_total": int(frame[target_col].nunique()),
        "edge_count_total": int(frame.shape[0]),
        "edges_with_exact_gse_target_match": int(supported.shape[0]),
        "unique_targets_with_exact_gse_match": int(supported[target_col].nunique()),
        "eligible_source_count_tmin5": len(eligible_sources),
        "eligible_sources_tmin5": eligible_sources,
        "eligible_source_sha256": hashlib.sha256("\n".join(eligible_sources).encode("utf-8")).hexdigest(),
        "eligible_target_count_min": int(eligible.min()) if len(eligible) else None,
        "eligible_target_count_median": float(eligible.median()) if len(eligible) else None,
        "eligible_target_count_max": int(eligible.max()) if len(eligible) else None,
    }


def run_probe(output_dir: Path) -> dict:
    collectri_payload, collectri_history = _download_collectri()
    collectri_raw = pd.read_csv(BytesIO(collectri_payload))
    collectri = _canonicalize_collectri(_apply_decoupler_220_human_semantics(collectri_raw))

    dorothea_payload, dorothea_history = _download_dorothea()
    dorothea = _canonicalize_dorothea(_read_rda(dorothea_payload))
    dorothea_abc = dorothea.loc[dorothea["confidence"].isin(DOROTHEA_LEVELS)].copy()

    gse_payload, gse_history = _download_gse()
    genes_list = _gse_gene_universe(gse_payload)
    genes = set(genes_list)

    ctri = _eligibility(collectri, "source", "target", genes)
    doro = _eligibility(dorothea_abc, "tf", "target", genes)
    overlap = sorted(set(ctri["eligible_sources_tmin5"]) & set(doro["eligible_sources_tmin5"]))

    # This raw-namespace diagnostic is expected to be empty. If that changes,
    # stop rather than silently turning a historical diagnostic back into a
    # scientific qualification route.
    if (
        ctri["edges_with_exact_gse_target_match"] != 0
        or doro["edges_with_exact_gse_target_match"] != 0
        or overlap
    ):
        raise RuntimeError(
            "raw SYMBOL|ENTREZID namespace unexpectedly overlaps symbol-only regulon targets; "
            "inspect source/schema drift before continuing"
        )

    result = {
        "status": RAW_NAMESPACE_DIAGNOSTIC_STATUS,
        "canonical_b3_overlap_probe": CANONICAL_B3_OVERLAP_PROBE,
        "superseded_for_regulon_support_qualification": True,
        "raw_identifier_matching_is_valid_regulon_support_test": False,
        "gse98812_source_sha256": GSE_SHA256,
        "gse98812_gene_rows": len(genes_list),
        "gse98812_gene_universe_sha256": hashlib.sha256(
            "\n".join(genes_list).encode("utf-8")
        ).hexdigest(),
        "raw_namespace": "SYMBOL|ENTREZID",
        "exact_case_sensitive_raw_identifier_matching": True,
        "expression_values_opened": False,
        "ulm_minimum_measured_targets": TMIN,
        "collectri": ctri,
        "dorothea_abc": doro,
        "dorothea_confidence_levels": list(DOROTHEA_LEVELS),
        "dorothea_future_weight_rule": "mor / confidence_denominator",
        "dorothea_confidence_denominator": DOROTHEA_CONFIDENCE_DENOMINATOR,
        "eligible_regulator_overlap_count": len(overlap),
        "eligible_regulator_overlap": overlap,
        "eligible_regulator_overlap_sha256": hashlib.sha256(
            "\n".join(overlap).encode("utf-8")
        ).hexdigest(),
        "download_attempt_history": {
            "collectri": collectri_history,
            "dorothea": dorothea_history,
            "gse98812": gse_history,
        },
        "tf_activity_scored": False,
        "tf_panel_selected_by_expression": False,
        "state_coordinates_computed": False,
        "state_dimension_selected": False,
        "operator_fit": False,
        "g1_computed": False,
        "g2_computed": False,
        "chi_bio_computed": False,
        "promotion_effect": "NONE_DIAGNOSTIC_ONLY",
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "GRI_CHI_BIO_B3_RAW_NAMESPACE_DIAGNOSTIC.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> int:
    result = run_probe(Path("development_outputs/chi_bio_regulon_source/b3_raw_namespace_diagnostic_20260913"))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
