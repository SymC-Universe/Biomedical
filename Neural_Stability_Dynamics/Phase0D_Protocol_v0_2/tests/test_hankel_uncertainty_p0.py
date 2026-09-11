import numpy as np
import pytest

from src.hankel_uncertainty import (
    batch_hankel_covariance_root,
    diagonal_variance_from_root,
    nsd_covariance_hankel,
)
from src.ssi_cov import decompose


def test_nsd_hankel_matches_ssi_decomposition_singular_values():
    rng = np.random.default_rng(101)
    Y = rng.normal(size=(500, 3))
    H = nsd_covariance_hankel(Y, 6)
    _, S, _ = decompose(Y, 6)
    assert np.allclose(np.linalg.svd(H, compute_uv=False), S)


def test_batch_covariance_root_has_expected_shape_and_nonnegative_variance():
    rng = np.random.default_rng(102)
    Y = rng.normal(size=(720, 2))
    T, meta = batch_hankel_covariance_root(Y, 4, 6)
    assert T.shape == ((2 * 4) ** 2, 6)
    assert meta["samples_per_batch"] == 120
    variance = diagonal_variance_from_root(T)
    assert variance.shape == ((2 * 4) ** 2,)
    assert np.all(np.isfinite(variance))
    assert np.all(variance >= 0)


def test_batch_covariance_root_rejects_too_short_batches():
    with pytest.raises(ValueError):
        batch_hankel_covariance_root(np.ones((30, 2)), 6, 6)
