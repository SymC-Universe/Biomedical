import pandas as pd
import pytest

from src.probe_chi_bio_collectri_export import (
    _apply_decoupler_220_human_semantics,
    _canonicalize,
)


def test_collectri_canonicalization_is_order_independent():
    a = pd.DataFrame(
        {
            "source": ["TFB", "TFA", "TFA"],
            "target": ["G2", "G2", "G1"],
            "weight": [1.0, -1.0, 1.0],
        }
    )
    b = a.iloc[[2, 0, 1]].reset_index(drop=True)
    ca = _canonicalize(a)
    cb = _canonicalize(b)
    pd.testing.assert_frame_equal(ca, cb)


def test_collectri_canonicalization_requires_signed_edge_core_columns():
    bad = pd.DataFrame({"source": ["TFA"], "target": ["G1"]})
    with pytest.raises(RuntimeError, match="weight"):
        _canonicalize(bad)


def test_collectri_220_human_semantics_match_resource_reference_cleanup_and_dedup():
    raw = pd.DataFrame(
        {
            "source": ["TFA", "TFA", "TFB"],
            "target": ["G1", "G1", "G2"],
            "weight": [1.0, 1.0, -1.0],
            "resources": [
                "CollecTRI;TRRUST_A;SIGNOR",
                "CollecTRI;TRRUST_A;SIGNOR",
                "CollecTRI;DoRothEA_A",
            ],
            "references": ["CollecTRI:1;2", "CollecTRI:1;2", "CollecTRI:3"],
        }
    )
    out = _apply_decoupler_220_human_semantics(raw)
    assert out.shape[0] == 2
    row_a = out[out["source"] == "TFA"].iloc[0]
    assert row_a["resources"] == "SIGNOR;TRRUSTA"
    assert row_a["references"] == "1;2"
    row_b = out[out["source"] == "TFB"].iloc[0]
    assert row_b["resources"] == "DoRothEAA"
    assert row_b["references"] == "3"


def test_collectri_220_human_semantics_preserve_null_until_dropna():
    raw = pd.DataFrame(
        {
            "source": ["TFA", "TFB"],
            "target": ["G1", "G2"],
            "weight": [1.0, -1.0],
            "resources": ["CollecTRI;SIGNOR", None],
            "references": ["CollecTRI:1", "CollecTRI:2"],
        }
    )
    out = _apply_decoupler_220_human_semantics(raw)
    assert out.shape[0] == 1
    assert out.iloc[0]["source"] == "TFA"
