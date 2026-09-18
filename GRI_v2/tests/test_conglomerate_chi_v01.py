import numpy as np
import pandas as pd
import pytest

from src.conglomerate_chi_v01 import BlockProfile, ConglomerateChiV01


def _carrier():
    ids = ["a", "b", "c", "d"]
    r = pd.DataFrame({"x": [1., 2., 3., 4.], "y": [4., 1., 3., 2.]}, index=ids)
    s = pd.DataFrame({"m": [0.2, 0.4, 0.7, 0.9]}, index=ids)
    return ConglomerateChiV01(ids, {"R": BlockProfile(r), "S": BlockProfile(s)})


def test_manifest_refuses_scalar_premise():
    m = _carrier().manifest()
    assert m["universal_scalar_required"] is False
    assert m["damped_oscillator_assumed"] is False
    assert m["unity_boundary_assumed"] is False
    assert m["scalar_chi_bio_value"] is None


def test_missing_blocks_are_explicit():
    c = _carrier()
    assert set(c.present_blocks()) == {"R", "S"}
    assert set(c.missing_blocks()) == {"E", "G", "P", "M", "T", "Q"}


def test_row_identity_firewall():
    ids = ["a", "b"]
    bad = pd.DataFrame({"x": [1., 2.]}, index=["b", "a"])
    with pytest.raises(ValueError):
        ConglomerateChiV01(ids, {"R": BlockProfile(bad)})


def test_affine_rescaling_preserves_standardized_geometry():
    c = _carrier()
    base = c.block_geometries()["R"]
    r = c.blocks["R"].values
    scaled = r * 17.0 + 101.0
    c2 = ConglomerateChiV01(c.sample_ids, {"R": BlockProfile(scaled), "S": c.blocks["S"]})
    np.testing.assert_allclose(base, c2.block_geometries()["R"], atol=1e-12)


def test_concordance_is_symmetric_and_bounded():
    g = _carrier().geometry_concordance()
    np.testing.assert_allclose(g.to_numpy(), g.to_numpy().T, equal_nan=True)
    finite = g.to_numpy()[np.isfinite(g.to_numpy())]
    assert np.all(finite >= -1.0)
    assert np.all(finite <= 1.0)


def test_leave_one_block_out_does_not_create_scalar():
    loo = _carrier().leave_one_block_out()
    assert set(loo) == {"R", "S"}
    assert all(v["scalar_output_created"] is False for v in loo.values())
