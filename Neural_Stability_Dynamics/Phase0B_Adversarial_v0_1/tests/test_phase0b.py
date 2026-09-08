import json
from pathlib import Path
import numpy as np

from src.synthetic_systems import make_linear_system, simulate_linear, make_noise_bases, add_measurement_noise
from src.ssi_cov import decompose, fit_from_decomposition
from src.metrics import subspace_similarity

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "configs" / "phase0b_design.json").read_text())


def system(name):
    return next(x for x in CFG["systems"] if x["name"] == name)


def test_nonnormal_target_spectrum_is_stable():
    rng = np.random.default_rng(1)
    A, C = make_linear_system(system("nonnormal_cond30"), CFG["n_channels"], rng)
    vals = np.linalg.eigvals(A)
    assert np.all(vals.real < 0)
    f = sorted(round(abs(x.imag) / (2 * np.pi), 3) for x in vals)
    assert f == [7.0, 7.0, 14.0, 14.0]


def test_weak_observable_changes_observation_not_pole_truth():
    rng1 = np.random.default_rng(2)
    rng2 = np.random.default_rng(2)
    A1, C1 = make_linear_system(system("separated_normal"), CFG["n_channels"], rng1)
    A2, C2 = make_linear_system(system("weak_observable"), CFG["n_channels"], rng2)
    assert np.allclose(np.sort_complex(np.linalg.eigvals(A1)), np.sort_complex(np.linalg.eigvals(A2)))


def test_paired_noise_scaling_uses_same_base_realization():
    rng = np.random.default_rng(3)
    A, C = make_linear_system(system("separated_normal"), CFG["n_channels"], rng)
    clean = simulate_linear(A, C, CFG["dt_seconds"], 3000, CFG["process_scale"], rng)
    w, c = make_noise_bases(3000, CFG["n_channels"], 0.8, rng)
    low = next(x for x in CFG["noise_profiles"] if x["name"] == "low_white")
    high = next(x for x in CFG["noise_profiles"] if x["name"] == "high_white")
    yl = add_measurement_noise(clean, low, w, c)
    yh = add_measurement_noise(clean, high, w, c)
    assert np.allclose(yh - clean, 15 * (yl - clean), rtol=1e-10, atol=1e-10)


def test_ssi_order_sweep_shapes():
    rng = np.random.default_rng(4)
    A, C = make_linear_system(system("separated_normal"), CFG["n_channels"], rng)
    Y = simulate_linear(A, C, CFG["dt_seconds"], 6000, CFG["process_scale"], rng)
    U, S, p = decompose(Y, CFG["block_rows"])
    for order in CFG["candidate_orders"]:
        vals, shapes = fit_from_decomposition(U, S, p, order, CFG["dt_seconds"])
        assert len(vals) == order
        assert shapes.shape == (CFG["n_channels"], order)


def test_subspace_similarity_invariant_to_basis_rotation():
    rng = np.random.default_rng(5)
    A = rng.normal(size=(8, 2)) + 1j * rng.normal(size=(8, 2))
    R = np.array([[1, 2], [-2, 1]], complex)
    assert subspace_similarity(A, A @ R) > 0.999999999


def test_no_clinical_inputs_named_in_config():
    txt = (ROOT / "configs" / "phase0b_design.json").read_text().lower()
    for forbidden in ["tdbrain", "diagnosis", "mdd", "adhd", "treatment_response"]:
        assert forbidden not in txt
