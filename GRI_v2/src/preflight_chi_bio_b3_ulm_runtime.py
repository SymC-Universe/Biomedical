from __future__ import annotations

"""Mechanical preflight for the frozen B3 ULM scoring layer.

This uses only tiny known synthetic data. It verifies that decoupler 2.2.0,
`decoupler.mt.ulm`, signed weights, t-value output, and score extraction behave
as expected in the execution environment. It does not qualify the biological
representation, choose a dimension, or open real SCC25/TCGA expression.
"""

import json
from pathlib import Path

import anndata as ad
import decoupler as dc
import numpy as np
import pandas as pd


EXPECTED_DECOUPLER_VERSION = "2.2.0"
OUTPUT = Path(
    "development_outputs/chi_bio_regulon_source/b3_ulm_runtime_20260913/"
    "GRI_CHI_BIO_B3_ULM_RUNTIME_PREFLIGHT.json"
)


def run_preflight() -> dict:
    observed_version = str(getattr(dc, "__version__", ""))
    if observed_version != EXPECTED_DECOUPLER_VERSION:
        raise RuntimeError(
            f"decoupler version drift: {observed_version!r} != {EXPECTED_DECOUPLER_VERSION!r}"
        )

    genes = ["g1", "g2", "g3", "g4", "g5", "g6"]
    samples = ["A_pos", "A_neg", "B_pos", "B_neg"]
    matrix = np.asarray(
        [
            [2.0, 1.1, -0.7, 0.05, 0.10, 0.00],
            [-1.8, -0.9, 0.8, 0.00, -0.05, 0.10],
            [0.05, 0.00, 0.10, 1.7, -0.8, 1.2],
            [0.00, 0.10, -0.05, -1.6, 0.9, -1.1],
        ],
        dtype=float,
    )
    adata = ad.AnnData(matrix)
    adata.obs_names = samples
    adata.var_names = genes

    net = pd.DataFrame(
        {
            "source": ["TF_A", "TF_A", "TF_A", "TF_B", "TF_B", "TF_B"],
            "target": ["g1", "g2", "g3", "g4", "g5", "g6"],
            "weight": [1.0, 0.5, -1.0, 1.0, -0.5, 1.0],
        }
    )

    dc.mt.ulm(
        data=adata,
        net=net,
        tmin=3,
        tval=True,
        raw=False,
        empty=True,
        verbose=False,
    )
    scores = dc.pp.get_obsm(adata, key="score_ulm")
    score_frame = pd.DataFrame(
        scores.X,
        index=scores.obs_names.astype(str),
        columns=scores.var_names.astype(str),
    )

    required_sources = {"TF_A", "TF_B"}
    if set(score_frame.columns) != required_sources:
        raise RuntimeError(f"unexpected ULM score columns: {list(score_frame.columns)}")
    if not np.all(np.isfinite(score_frame.to_numpy(dtype=float))):
        raise RuntimeError("ULM synthetic preflight produced nonfinite scores")

    sign_checks = {
        "A_pos_TF_A_positive": float(score_frame.loc["A_pos", "TF_A"]) > 0.0,
        "A_neg_TF_A_negative": float(score_frame.loc["A_neg", "TF_A"]) < 0.0,
        "B_pos_TF_B_positive": float(score_frame.loc["B_pos", "TF_B"]) > 0.0,
        "B_neg_TF_B_negative": float(score_frame.loc["B_neg", "TF_B"]) < 0.0,
    }
    if not all(sign_checks.values()):
        raise RuntimeError(f"ULM signed synthetic checks failed: {sign_checks}")

    result = {
        "status": "PASS_B3_ULM_RUNTIME_PREFLIGHT",
        "decoupler_version": observed_version,
        "method": "decoupler.mt.ulm",
        "score_key": "score_ulm",
        "tval": True,
        "signed_weights_used": True,
        "tmin": 3,
        "synthetic_samples": samples,
        "synthetic_features": genes,
        "scores": {
            sample: {source: float(score_frame.loc[sample, source]) for source in score_frame.columns}
            for sample in score_frame.index
        },
        "sign_checks": sign_checks,
        "real_expression_opened": False,
        "real_regulatory_activity_scored": False,
        "dimension_selected": False,
        "operator_fit": False,
        "normalized_g1_computed": False,
        "chi_bio_computed": False,
        "promotion_effect": "NONE_MECHANICAL_SCORING_PREFLIGHT_ONLY",
    }
    return result


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    try:
        result = run_preflight()
        rc = 0
    except Exception as exc:
        result = {
            "status": "REFUSE_B3_ULM_RUNTIME_PREFLIGHT",
            "reason": f"{type(exc).__name__}: {exc}",
            "real_expression_opened": False,
            "chi_bio_computed": False,
        }
        rc = 2
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
