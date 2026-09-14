from __future__ import annotations

import numpy as np

from scripts.run_p0d22_identifiability_null_floor import (
    WEAK_SCALES,
    _base_observation,
    _latent_generator,
    _observation_map,
    _truth_summary,
)


def test_latent_truth_is_stable_and_well_defined():
    A = _latent_generator()
    truth = _truth_summary(A)
    assert A.shape == (4, 4)
    assert truth["spectral_abscissa"] < 0
    assert truth["tau"] is not None and truth["tau"] > 0
    assert len(truth["positive_mode_chi"]) == 2


def test_only_weak_observation_columns_are_scaled():
    C0 = _base_observation(np.random.default_rng(123))
    C = _observation_map(C0, 0.1)
    assert np.allclose(C[:, :2], C0[:, :2])
    assert np.allclose(C[:, 2:4], 0.1 * C0[:, 2:4])


def test_weak_scale_grid_is_monotone_and_positive():
    assert all(x > 0 for x in WEAK_SCALES)
    assert all(a > b for a, b in zip(WEAK_SCALES[:-1], WEAK_SCALES[1:]))


def test_observation_manipulation_does_not_change_latent_generator():
    A = _latent_generator()
    before = A.copy()
    C0 = _base_observation(np.random.default_rng(456))
    for scale in WEAK_SCALES:
        C = _observation_map(C0, scale)
        assert np.all(np.isfinite(C))
        assert np.array_equal(A, before)


def test_truth_summary_is_deterministic():
    a = _truth_summary(_latent_generator())
    b = _truth_summary(_latent_generator())
    assert a == b
