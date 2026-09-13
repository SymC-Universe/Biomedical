from __future__ import annotations

"""Identifier-only diagnostic for the hash-bound GSE98812 RNA table.

This probe reads only the GENE column and reports namespace structure needed to
map the externally frozen B3 regulons. It never parses expression values.
"""

from io import BytesIO
import gzip
import hashlib
import json
from pathlib import Path

import pandas as pd

from src.probe_chi_bio_b3_network_gene_overlap import _download_gse, GSE_SHA256, EXPECTED_GENE_ROWS


def run_probe() -> dict:
    payload, history = _download_gse()
    if hashlib.sha256(payload).hexdigest() != GSE_SHA256:
        raise RuntimeError("GSE98812 hash drift")
    raw = gzip.decompress(payload)
    genes = pd.read_csv(BytesIO(raw), sep="\t", usecols=["GENE"], dtype=str)["GENE"].astype(str).str.strip()
    if len(genes) != EXPECTED_GENE_ROWS:
        raise RuntimeError("unexpected gene-row count")

    pipe = genes.str.contains(r"\|", regex=True)
    left = genes.str.split("|", n=1, regex=False).str[0]
    right = genes.str.split("|", n=1, regex=False).str[1]
    numeric = genes.str.fullmatch(r"\d+")
    ensembl = genes.str.fullmatch(r"ENSG\d+(?:\.\d+)?")
    symbolish = genes.str.fullmatch(r"[A-Za-z0-9_.-]+")
    right_numeric = right.fillna("").str.fullmatch(r"\d+")
    duplicate_mask = left.duplicated(keep=False)
    duplicate_tokens = sorted(left[duplicate_mask].unique().tolist())
    named_duplicate_tokens = [x for x in duplicate_tokens if x != "?"]

    result = {
        "status": "PASS_GSE98812_GENE_NAMESPACE_DIAGNOSTIC",
        "source_sha256": GSE_SHA256,
        "gene_rows": int(len(genes)),
        "expression_values_opened": False,
        "raw_gene_examples_first_20": genes.head(20).tolist(),
        "raw_gene_examples_last_20": genes.tail(20).tolist(),
        "contains_pipe_count": int(pipe.sum()),
        "raw_all_numeric_count": int(numeric.sum()),
        "raw_ensembl_count": int(ensembl.sum()),
        "raw_symbolish_count": int(symbolish.sum()),
        "pipe_left_unique_count": int(left[pipe].nunique()),
        "pipe_right_numeric_count": int(right_numeric[pipe].sum()),
        "pipe_left_duplicate_count": int(left[pipe].duplicated().sum()),
        "pipe_left_blank_count": int(left[pipe].eq("").sum()),
        "question_mark_symbol_row_count": int(left.eq("?").sum()),
        "duplicate_left_tokens": duplicate_tokens,
        "named_duplicate_left_tokens": named_duplicate_tokens,
        "named_duplicate_left_token_count": len(named_duplicate_tokens),
        "pipe_left_examples_first_20": left[pipe].head(20).tolist(),
        "pipe_right_examples_first_20": right[pipe].head(20).tolist(),
        "download_attempt_history": history,
        "mapping_applied": False,
        "tf_activity_scored": False,
        "operator_fit": False,
        "chi_bio_computed": False,
        "promotion_effect": "NONE",
    }
    out = Path("development_outputs/chi_bio_regulon_source/gse98812_namespace_20260913")
    out.mkdir(parents=True, exist_ok=True)
    (out / "GRI_CHI_BIO_GSE98812_GENE_NAMESPACE.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return result


def main() -> int:
    result = run_probe()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
