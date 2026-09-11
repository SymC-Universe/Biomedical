import numpy as np

from src.csd_svd import (
    carrier_mac,
    compare_surfaces,
    csd_svd_surface,
    participation_total_variation,
    subspace_similarity,
)


def _synthetic_epochs():
    sfreq = 1024.0
    n_times = 4096
    t = np.arange(n_times) / sfreq
    rng = np.random.default_rng(20260911)
    epochs = []
    for e in range(8):
        phase = 0.2 * e
        s10 = np.sin(2 * np.pi * 10.0 * t + phase)
        s18 = np.sin(2 * np.pi * 18.0 * t - 0.5 * phase)
        x = np.vstack([
            2.0 * s10 + 0.2 * s18,
            1.2 * s10 - 0.7 * s18,
            0.4 * s10 + 1.5 * s18,
            -0.8 * s10 + 0.9 * s18,
        ])
        x += 0.05 * rng.normal(size=x.shape)
        epochs.append(x)
    return np.asarray(epochs), sfreq


def test_frozen_frequency_grid_is_exact_for_four_second_1024hz_epochs():
    x, sfreq = _synthetic_epochs()
    out = csd_svd_surface(x, sfreq, 1.0, 45.0)
    f = out["frequency_hz"]
    assert f[0] == 1.0
    assert f[-1] == 45.0
    assert len(f) == 177
    assert np.allclose(np.diff(f), 0.25, rtol=0, atol=1e-12)


def test_csd_surface_is_finite_and_numerically_psd():
    x, sfreq = _synthetic_epochs()
    out = csd_svd_surface(x, sfreq, 1.0, 45.0)
    assert np.all(np.isfinite(out["singular_values_first4"]))
    assert np.all(out["singular_values_first4"] >= 0)
    assert np.max(out["hermitian_relative_error"]) < 1e-12
    assert np.min(out["minimum_eigenvalue"]) > -1e-10 * np.max(out["singular_values_first4"][:, 0])
    assert np.allclose(np.sum(out["participation_u1"], axis=1), 1.0, atol=1e-12)


def test_carrier_mac_is_invariant_to_arbitrary_complex_phase():
    rng = np.random.default_rng(2)
    u = rng.normal(size=(10, 6)) + 1j * rng.normal(size=(10, 6))
    phases = np.exp(1j * np.linspace(0.0, 2.0, 10))
    v = u * phases[:, None]
    assert np.allclose(carrier_mac(u, v), 1.0, atol=1e-12)


def test_subspace_similarity_is_invariant_to_basis_rotation():
    rng = np.random.default_rng(3)
    U = []
    V = []
    rotation = np.array([[0.8, -0.6], [0.6, 0.8]], dtype=complex)
    for _ in range(7):
        q, _ = np.linalg.qr(rng.normal(size=(8, 2)) + 1j * rng.normal(size=(8, 2)))
        U.append(q)
        V.append(q @ rotation)
    sim = subspace_similarity(np.asarray(U), np.asarray(V))
    assert np.allclose(sim, 1.0, atol=1e-12)


def test_participation_total_variation_is_zero_for_identical_vectors():
    rng = np.random.default_rng(4)
    p = rng.random(size=(12, 5))
    p /= p.sum(axis=1, keepdims=True)
    assert np.allclose(participation_total_variation(p, p), 0.0, atol=1e-15)


def test_identical_surface_comparison_is_exactly_self_consistent():
    x, sfreq = _synthetic_epochs()
    out = csd_svd_surface(x, sfreq, 1.0, 45.0)
    cmp = compare_surfaces(out, out)
    assert np.allclose(cmp["leading_carrier_MAC_per_frequency"], 1.0, atol=1e-12)
    assert np.allclose(cmp["two_dimensional_subspace_similarity_per_frequency"], 1.0, atol=1e-12)
    assert np.allclose(cmp["participation_total_variation_per_frequency"], 0.0, atol=1e-15)
    assert np.isclose(cmp["leading_share_curve_correlation"], 1.0)
    assert np.isclose(cmp["log_total_cross_spectral_power_curve_correlation"], 1.0)
