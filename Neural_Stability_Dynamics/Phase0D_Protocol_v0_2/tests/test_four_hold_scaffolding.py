import numpy as np
from scipy.linalg import expm
from scipy.optimize import linear_sum_assignment

from src.dmd import fit_dmd
from src.model_adequacy import (
    fit_linear_predictor,
    one_step_residuals,
    normalized_prediction_error,
    residual_autocorrelation_energy,
    surrogate_whiteness_record,
    fit_covariance_markov_parameter,
    covariance_reconstruction_error,
)
from src.ssi_cov import state_space_from_decomposition, fit_from_decomposition
from src.uncertainty import (
    UncertaintyRecord,
    adjudication_from_interval,
    interval_spans_threshold,
    central_empirical_interval,
    known_truth_calibration,
)
from src.mode_tracking import track_modes


def _match_complex_sets(a, b):
    a = np.asarray(a, complex)
    b = np.asarray(b, complex)
    cost = np.abs(a[:, None] - b[None, :])
    ri, cj = linear_sum_assignment(cost)
    return cost[ri, cj]


def test_dmd_recovers_simple_discrete_modes():
    dt = 0.1
    A = np.diag([0.95, 0.8])
    x = np.array([1.0, -0.7])
    Y = []
    for _ in range(80):
        Y.append(x.copy())
        x = A @ x
    vals, modes = fit_dmd(np.asarray(Y), dt=dt, rank=2)
    recovered = np.sort(np.exp(vals * dt).real)
    assert np.allclose(recovered, np.array([0.8, 0.95]), atol=1e-6)
    assert modes.shape == (2, 2)


def test_dmd_recovers_known_complex_modes_when_output_is_full_rank():
    dt = 0.05
    blocks = []
    for decay, hz in [(0.4, 2.0), (0.8, 5.0)]:
        b = 2 * np.pi * hz
        Ac = np.array([[-decay, -b], [b, -decay]])
        blocks.append(expm(Ac * dt))
    F = np.zeros((4, 4))
    F[:2, :2] = blocks[0]
    F[2:, 2:] = blocks[1]

    rng = np.random.default_rng(22)
    Q, _ = np.linalg.qr(rng.normal(size=(4, 4)))
    Fy = Q @ F @ Q.T
    x = rng.normal(size=4)
    Y = []
    for _ in range(500):
        Y.append(x.copy())
        x = Fy @ x

    vals, _ = fit_dmd(np.asarray(Y), dt=dt, rank=4)
    errors = _match_complex_sets(np.exp(vals * dt), np.linalg.eigvals(Fy))
    assert np.max(errors) < 1e-10


def test_adequacy_diagnostics_detect_predictable_linear_process():
    rng = np.random.default_rng(123)
    A = np.array([[0.8, 0.1], [0.0, 0.7]])
    x = np.zeros(2)
    Y = []
    for _ in range(1200):
        x = A @ x + 0.05 * rng.normal(size=2)
        Y.append(x.copy())
    Y = np.asarray(Y)
    fit = fit_linear_predictor(Y[:800])
    resid = one_step_residuals(Y[:800], fit)
    assert resid.shape == (799, 2)
    assert np.isfinite(residual_autocorrelation_energy(resid, 10))
    assert normalized_prediction_error(Y[800:], fit) < 1.0


def test_covariance_markov_reconstruction_separates_true_and_wrong_stable_model():
    F = np.array([[0.9, 0.1], [0.0, 0.7]])
    C = np.array([[1.0, 0.2], [0.3, 1.0]])
    G = np.array([[0.5, 0.1], [0.2, 0.3]])
    covs = [C @ np.linalg.matrix_power(F, lag - 1) @ G for lag in range(1, 21)]

    fitted_G = fit_covariance_markov_parameter(F, C, covs, range(1, 6))
    true_error, _ = covariance_reconstruction_error(
        F, C, fitted_G, covs, range(6, 21)
    )

    wrong_F = np.array([[0.5, 0.0], [0.0, 0.4]])
    wrong_G = fit_covariance_markov_parameter(wrong_F, C, covs, range(1, 6))
    wrong_error, _ = covariance_reconstruction_error(
        wrong_F, C, wrong_G, covs, range(6, 21)
    )

    assert np.max(np.abs(fitted_G - G)) < 1e-12
    assert true_error < 1e-20
    assert wrong_error > 1e-2
    assert np.max(np.abs(np.linalg.eigvals(wrong_F))) < 1.0


def test_residual_whiteness_known_bad_serial_process_is_detected_directionally():
    rng = np.random.default_rng(100)
    white = rng.normal(size=(1500, 3))
    innovations = rng.normal(size=(1500, 3))
    serial = np.zeros_like(innovations)
    for t in range(1, len(serial)):
        serial[t] = 0.9 * serial[t - 1] + innovations[t]

    white_energy = residual_autocorrelation_energy(white, 10)
    serial_record = surrogate_whiteness_record(
        serial, 10, 99, np.random.default_rng(101)
    )
    assert serial_record["observed_energy"] > 20.0 * white_energy
    assert serial_record["observed_energy"] > serial_record["surrogate_q95_energy"]
    assert serial_record["monte_carlo_upper_tail_p"] <= 0.02


def test_state_space_exposure_preserves_original_pole_calculation():
    rng = np.random.default_rng(7)
    U, _ = np.linalg.qr(rng.normal(size=(12, 12)))
    S = np.geomspace(20.0, 0.01, 12)
    p = 3
    order = 4
    dt = 0.01

    F, C, O = state_space_from_decomposition(U, S, p, order)
    vals, shapes = fit_from_decomposition(U, S, p, order, dt)
    expected = np.log(np.linalg.eigvals(F).astype(complex)) / dt
    assert np.max(_match_complex_sets(vals, expected)) < 1e-10
    assert C.shape == (p, order)
    assert O.shape == (12, order)
    assert shapes.shape == (p, order)


def test_uncertainty_interval_can_return_indeterminate():
    rec = UncertaintyRecord(
        estimate=0.95, lower=0.93, upper=0.97, method="TEST"
    )
    assert adjudication_from_interval(rec, 0.95) == "INDETERMINATE_SPANS_BOUNDARY"


def test_uncertainty_rejects_invalid_reversed_interval():
    rec = UncertaintyRecord(estimate=1.0, lower=1.1, upper=0.9, method="TEST")
    assert interval_spans_threshold(rec, 1.0) is None
    assert adjudication_from_interval(rec, 1.0) == "INDETERMINATE_NO_INTERVAL"


def test_empirical_uncertainty_helpers_are_descriptive_not_p1_frozen():
    values = np.array([0.91, 0.94, 0.95, 0.96, 0.99])
    rec = central_empirical_interval(values, confidence=0.8)
    cal = known_truth_calibration(values, truth=0.95)
    assert rec.status == "P0_CALIBRATION_NOT_P1_UNCERTAINTY"
    assert rec.lower < rec.upper
    assert cal["status"] == "P0_KNOWN_TRUTH_CALIBRATION"
    assert cal["n"] == len(values)


def test_unequal_order_tracking_preserves_only_candidate_semantics():
    va = np.array([-1.0 + 2.0j, -0.8 + 4.0j])
    vb = np.array([-1.01 + 2.01j, -0.81 + 4.01j, -0.5 + 7.0j])
    sa = np.eye(3, 2, dtype=complex)
    sb = np.eye(3, 3, dtype=complex)
    out = track_modes(va, sa, vb, sb, min_hz=0.0)

    assert out["status"] == "P0_ASSIGNMENT_NOT_ADJUDICATED"
    assert len(out["candidate_pairs"]) == 2
    assert out["unmatched_a"] == []
    assert out["unmatched_b"] == [2]
    assert "shared" not in out and "lost" not in out and "added" not in out
    assert all(
        p["status"] == "CANDIDATE_PAIR_NOT_ADJUDICATED"
        for p in out["candidate_pairs"]
    )


def test_mode_assignment_exposes_exact_ambiguity_without_resolving_it():
    va = np.array([-1.0 + 2.0j])
    vb = np.array([-1.0 + 2.0j, -1.0 + 2.0j])
    sa = np.array([[1.0], [0.0]], dtype=complex)
    sb = np.array([[1.0, 1.0], [0.0, 0.0]], dtype=complex)
    out = track_modes(va, sa, vb, sb, min_hz=0.0)
    assert len(out["candidate_pairs"]) == 1
    assert out["candidate_pairs"][0]["assignment_margin"] == 0.0
    assert len(out["unmatched_b"]) == 1
