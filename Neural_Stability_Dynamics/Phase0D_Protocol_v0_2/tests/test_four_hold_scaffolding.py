import numpy as np

from src.dmd import fit_dmd
from src.model_adequacy import fit_linear_predictor, one_step_residuals, normalized_prediction_error, residual_autocorrelation_energy
from src.uncertainty import UncertaintyRecord, adjudication_from_interval
from src.mode_tracking import track_modes


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


def test_uncertainty_interval_can_return_indeterminate():
    rec = UncertaintyRecord(estimate=0.95, lower=0.93, upper=0.97, method="TEST")
    assert adjudication_from_interval(rec, 0.95) == "INDETERMINATE_SPANS_BOUNDARY"


def test_unequal_order_tracking_preserves_added_mode():
    va = np.array([-1+2j, -1-2j])
    vb = np.array([-1.01+2.01j, -1.01-2.01j, -0.5+4j, -0.5-4j])
    sa = np.eye(4, 2, dtype=complex)
    sb = np.eye(4, 4, dtype=complex)
    out = track_modes(va, sa, vb, sb, min_hz=0.0)
    assert out["status"] == "P0_ASSIGNMENT_NOT_ADJUDICATED"
    assert len(out["shared"]) == 1
    assert len(out["added"]) == 1
