import pandas as pd
import pytest

from src.probe_chi_bio_collectri_export import _canonicalize


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
