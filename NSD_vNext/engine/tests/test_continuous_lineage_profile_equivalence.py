import math
import numpy as np
import pytest

from nsd_engine.continuous_lineage_candidate import _build_candidate, _nll
from nsd_engine.continuous_lineage_profile import (
    physical_candidate,
    physical_nll,
    physical_to_c1q_raw,
)


CASES = [
    (0.35, 5.0, 0.20, -0.60),
    (0.80, 10.0, 0.50, 0.00),
    (0.50, 22.0, 0.75, 0.10),
    (0.30, 19.0, 0.50, -0.72),
    (0.80, 15.0, 0.80, 0.65),
]


@pytest.mark.parametrize("fs", [128.0, 256.0])
@pytest.mark.parametrize("A,fn,chi,g", CASES)
def test_physical_coordinate_round_trip(fs, A, fn, chi, g):
    raw = physical_to_c1q_raw(
        A=A,
        natural_frequency_hz=fn,
        chi=chi,
        g=g,
        sampling_rate_hz=fs,
    )
    _, _, _, _, pars = _build_candidate(raw, fs, 1.0, 45.0)

    assert pars["latent_fraction"] == pytest.approx(A, rel=2e-11, abs=2e-11)
    assert pars["natural_frequency_hz"] == pytest.approx(
        fn, rel=2e-11, abs=2e-11
    )
    assert pars["damping_ratio"] == pytest.approx(
        chi, rel=2e-11, abs=2e-11
    )
    assert pars["g"] == pytest.approx(g, rel=2e-11, abs=2e-11)


@pytest.mark.parametrize("fs", [128.0, 256.0])
@pytest.mark.parametrize("A,fn,chi,g", CASES)
def test_physical_wrapper_is_exact_same_nll(fs, A, fn, chi, g):
    rng = np.random.default_rng(20260927)
    standardized = rng.normal(size=4096)
    standardized = (
        standardized - np.mean(standardized)
    ) / np.std(standardized)

    raw = physical_to_c1q_raw(
        A=A,
        natural_frequency_hz=fn,
        chi=chi,
        g=g,
        sampling_rate_hz=fs,
    )
    direct = _nll(standardized, raw, fs, 1.0, 45.0, 128)
    wrapped = physical_nll(
        standardized,
        A=A,
        natural_frequency_hz=fn,
        chi=chi,
        g=g,
        sampling_rate_hz=fs,
        burn_in_samples=128,
    )
    assert wrapped == pytest.approx(direct, rel=1e-13, abs=1e-10)


@pytest.mark.parametrize("fs", [128.0, 256.0])
def test_raw_physical_raw_round_trip_on_interior_coordinates(fs):
    raws = [
        np.asarray([-0.7, 1.2, -0.2, 0.4]),
        np.asarray([1.0, 2.0, 0.5, -0.8]),
        np.asarray([0.2, 3.0, -0.6, 1.1]),
    ]
    for raw in raws:
        _, _, _, _, pars = _build_candidate(raw, fs, 1.0, 45.0)
        reconstructed = physical_to_c1q_raw(
            A=pars["latent_fraction"],
            natural_frequency_hz=pars["natural_frequency_hz"],
            chi=pars["damping_ratio"],
            g=pars["g"],
            sampling_rate_hz=fs,
        )
        np.testing.assert_allclose(reconstructed, raw, rtol=1e-10, atol=1e-10)


def test_physical_candidate_delegates_canonical_builder():
    args = dict(
        A=0.6,
        natural_frequency_hz=12.0,
        chi=0.4,
        g=-0.3,
        sampling_rate_hz=256.0,
    )
    raw = physical_to_c1q_raw(**args)
    canonical = _build_candidate(raw, 256.0, 1.0, 45.0)
    wrapped = physical_candidate(**args)
    for left, right in zip(canonical[:4], wrapped[:4]):
        np.testing.assert_allclose(left, right, rtol=1e-12, atol=1e-12)
    for key, value in canonical[4].items():
        assert wrapped[4][key] == pytest.approx(value, rel=1e-12, abs=1e-12)
