import numpy as np
from scipy.linalg import block_diag

from src.chi_conglomerate import second_order_generator
from src.participation_balance import (
    balanced_block_process_scales,
    block_participation_units,
    simulate_block_process,
)


def _setup():
    blocks = [
        second_order_generator(0.4, 2.0 * np.pi * 2.0),
        second_order_generator(0.6, 2.0 * np.pi * 7.0),
    ]
    rng = np.random.default_rng(20260911)
    C = rng.normal(size=(6, 4))
    C /= np.maximum(np.linalg.norm(C, axis=1, keepdims=True), 1e-12)
    return blocks, C


def test_balance_modes_preserve_their_incumbent_total():
    blocks, C = _setup()
    for mode, total_key, incumbent_key in [
        ("latent_trace", "latent_total", "incumbent_latent_total"),
        ("output_trace", "output_total", "incumbent_output_total"),
    ]:
        out = balanced_block_process_scales(blocks, C, 0.01, 0.3, mode)
        assert np.isclose(out[total_key], out[incumbent_key], rtol=1e-10, atol=1e-12)


def test_latent_and_output_balance_equalize_requested_participation():
    blocks, C = _setup()
    latent = balanced_block_process_scales(blocks, C, 0.01, 0.3, "latent_trace")
    output = balanced_block_process_scales(blocks, C, 0.01, 0.3, "output_trace")
    assert np.allclose(latent["latent_fractions"], [0.5, 0.5], atol=1e-10)
    assert np.allclose(output["output_fractions"], [0.5, 0.5], atol=1e-10)


def test_equal_state_noise_matches_unit_participation_ratios():
    blocks, C = _setup()
    units = block_participation_units(blocks, C, 0.01)
    out = balanced_block_process_scales(blocks, C, 0.01, 0.3, "equal_state_noise")
    expected = units["output_trace_units"] / np.sum(units["output_trace_units"])
    assert np.allclose(out["output_fractions"], expected)


def test_block_process_simulator_shapes_and_centers_output():
    blocks, C = _setup()
    A = block_diag(*blocks)
    out = balanced_block_process_scales(blocks, C, 0.01, 0.3, "output_trace")
    Y = simulate_block_process(
        A,
        C,
        0.01,
        2000,
        out["scales"],
        np.random.default_rng(42),
        burn=200,
    )
    assert Y.shape == (2000, 6)
    assert np.max(np.abs(Y.mean(axis=0))) < 1e-10
    assert np.all(np.isfinite(Y))
