from __future__ import annotations

"""Outcome-free B3 overlap qualification after namespace diagnosis.

The raw GSE98812 GENE field is SYMBOL|ENTREZID. This versioned probe preserves
that raw source, deterministically extracts the left SYMBOL token, excludes only
the literal unmapped token '?', and requires every remaining mapped symbol to be
unique before exact regulon matching. It never reads expression values.

One frozen legacy-symbol exception is required by the source namespace audit:
GSE98812 uses the historical symbol SLC35E2 for two distinct Entrez genes.
Current NCBI/HGNC identity resolves Entrez 728661 -> SLC35E2B and Entrez 9906
-> SLC35E2A. No other source row is renamed and no fuzzy mapping is permitted.
"""

from io import BytesIO
import gzip
import hashlib
import json
from pathlib import Path

import pandas as pd

from src.probe_chi_bio_b3_network_gene_overlap import (
    DOROTHEA_CONFIDENCE_DENOMINATOR,
    DOROTHEA_LEVELS,
    EXPECTED_GENE_ROWS,
    GSE_SHA256,
    TMIN,
    _download_gse,
    _eligibility,
)
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


LEGACY_SYMBOL_ENTREZ_EXCEPTIONS = {
    ("SLC35E2", "728661"): "SLC35E2B",
    ("SLC35E2", "9906"): "SLC35E2A",
}


def _mapped_gene_universe(payload: bytes) -> tuple[list[str], dict]:
    if hashlib.sha256(payload).hexdigest() != GSE_SHA256:
        raise RuntimeError("GSE98812 source SHA drift")
    raw = gzip.decompress(payload)
    genes = pd.read_csv(BytesIO(raw), sep="\t", usecols=["GENE"], dtype=str)["GENE"].astype(str).str.strip()
    if len(genes) != EXPECTED_GENE_ROWS:
        raise RuntimeError(f"unexpected GSE98812 gene-row count: {len(genes)}")
    if not genes.str.contains("|", regex=False).all():
        raise RuntimeError("not every GSE98812 GENE identifier contains the frozen pipe delimiter")

    split = genes.str.split("|", n=1, regex=False, expand=True)
    if split.shape[1] != 2:
        raise RuntimeError("GSE98812 GENE split did not produce exactly two fields")
    symbol = split.iloc[:, 0].str.strip()
    entrez = split.iloc[:, 1].str.strip()
    if symbol.eq("").any() or not entrez.str.fullmatch(r"\d+").all():
        raise RuntimeError("GSE98812 SYMBOL|ENTREZID grammar drift")

    mapped_mask = symbol.ne("?")
    mapped_symbols: list[str] = []
    applied_exceptions: list[dict] = []
    for raw_symbol, raw_entrez in zip(symbol[mapped_mask], entrez[mapped_mask], strict=True):
        key = (str(raw_symbol), str(raw_entrez))
        mapped_symbol = LEGACY_SYMBOL_ENTREZ_EXCEPTIONS.get(key, str(raw_symbol))
        mapped_symbols.append(mapped_symbol)
        if mapped_symbol != raw_symbol:
            applied_exceptions.append(
                {
                    "raw_symbol": str(raw_symbol),
                    "entrez_id": str(raw_entrez),
                    "mapped_symbol": mapped_symbol,
                }
            )

    if len(applied_exceptions) != len(LEGACY_SYMBOL_ENTREZ_EXCEPTIONS):
        raise RuntimeError(
            "legacy SLC35E2 exception set did not match the frozen GSE98812 namespace exactly"
        )
    if sorted((x["raw_symbol"], x["entrez_id"], x["mapped_symbol"]) for x in applied_exceptions) != sorted(
        (raw_symbol, entrez_id, mapped_symbol)
        for (raw_symbol, entrez_id), mapped_symbol in LEGACY_SYMBOL_ENTREZ_EXCEPTIONS.items()
    ):
        raise RuntimeError("legacy SLC35E2 exception application drift")

    mapped_series = pd.Series(mapped_symbols, dtype=str)
    if mapped_series.duplicated().any():
        dup = sorted(mapped_series[mapped_series.duplicated(keep=False)].unique().tolist())
        raise RuntimeError(f"mapped GSE98812 symbols are not unique after frozen exceptions: {dup[:20]}")

    unknown_count = int((~mapped_mask).sum())
    if unknown_count != 29:
        raise RuntimeError(f"frozen unmapped '?' row count drift: {unknown_count} != 29")

    return mapped_symbols, {
        "raw_gene_rows": int(len(genes)),
        "unknown_question_mark_rows_excluded": unknown_count,
        "mapped_symbol_rows": int(len(mapped_symbols)),
        "mapped_symbols_unique": True,
        "mapped_symbol_sha256": hashlib.sha256(
            "\n".join(mapped_symbols).encode("utf-8")
        ).hexdigest(),
        "entrez_ids_all_numeric": True,
        "mapping_rule": (
            "split raw GENE exactly once on first pipe; exclude literal '?' only; "
            "retain exact left SYMBOL except frozen Entrez-backed legacy exceptions "
            "SLC35E2|728661->SLC35E2B and SLC35E2|9906->SLC35E2A"
        ),
        "legacy_symbol_exceptions": applied_exceptions,
        "entrez_used_only_for_frozen_legacy_disambiguation": True,
        "fuzzy_mapping_used": False,
        "external_bulk_annotation_table_used": False,
    }


def run_probe(output_dir: Path) -> dict:
    collectri_payload, collectri_history = _download_collectri()
    collectri_raw = pd.read_csv(BytesIO(collectri_payload))
    collectri = _canonicalize_collectri(_apply_decoupler_220_human_semantics(collectri_raw))

    dorothea_payload, dorothea_history = _download_dorothea()
    dorothea = _canonicalize_dorothea(_read_rda(dorothea_payload))
    dorothea_abc = dorothea.loc[dorothea["confidence"].isin(DOROTHEA_LEVELS)].copy()

    gse_payload, gse_history = _download_gse()
    symbols, namespace = _mapped_gene_universe(gse_payload)
    universe = set(symbols)

    ctri = _eligibility(collectri, "source", "target", universe)
    doro = _eligibility(dorothea_abc, "tf", "target", universe)
    overlap = sorted(set(ctri["eligible_sources_tmin5"]) & set(doro["eligible_sources_tmin5"]))

    result = {
        "status": "PASS_B3_SYMBOL_MAPPED_NETWORK_GSE98812_OVERLAP",
        "gse98812_source_sha256": GSE_SHA256,
        "namespace": namespace,
        "exact_case_sensitive_symbol_matching": True,
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
        "state_coordinates_computed": False,
        "operator_fit": False,
        "chi_bio_computed": False,
        "promotion_effect": "NONE",
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "GRI_CHI_BIO_B3_SYMBOL_MAPPED_OVERLAP.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> int:
    result = run_probe(Path("development_outputs/chi_bio_regulon_source/b3_symbol_mapping_20260913"))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
