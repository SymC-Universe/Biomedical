import numpy as np
import pytest

from src.chi_bio_g1_hardening import (
    g1_hardening_audit,
    is_positive_scalar_identity,
    local_jacobian,
    naive_left_normalized_interaction,
    scalar_restoration_g1_value,
    symmetric_generalized_g1_value,
)
from src.chi_bio_candidate_math import spectral_abscissa, unity_regime


def test_common_restoration_preserves_exact_unity_boundary():
    r = 2.0 * np.eye(2)
    k = np.diag([0.4, 1.8])
    value = scalar_restoration_g1_value(k, r)
    j = local_jacobian(k, r)

    assert value == pytest.approx(0.9)
    assert spectral_abscissa(j) == pytest.approx(2.0 * (value - 1.0))
    assert unity_regime(value) == "BELOW_UNITY"
    assert is_positive_scalar_identity(r)


def test_heterogeneous_restoration_can_make_naive_g1_false_safe():
    # Exact counterexample: alpha(R^-1 K)=0.75 < 1 while alpha(K-R)=0.25 > 0.
    r = np.diag([2.0, 0.5])
    k = np.array([[3.0, -4.0], [1.0, 0.0]])

    m = naive_left_normalized_interaction(k, r)
    assert spectral_abscissa(m) == pytest.approx(0.75)
    assert spectral_abscissa(local_jacobian(k, r)) == pytest.approx(0.25)

    audit = g1_hardening_audit(k, r)
    assert audit.exact_unity_route == "NO_EXACT_UNITY_ROUTE_FROM_NAIVE_NORMALIZATION"
    assert not audit.scalar_restoration_exact
    assert not audit.symmetric_generalized_exact


def test_heterogeneous_restoration_can_make_naive_g1_false_unsafe():
    # Exact counterexample: alpha(R^-1 K)=2 > 1 while J is asymptotically stable.
    r = np.diag([2.0, 0.5])
    k = np.array([[-4.0, -4.0], [4.0, 3.0]])

    m = naive_left_normalized_interaction(k, r)
    assert spectral_abscissa(m) == pytest.approx(2.0, abs=1e-6)
    assert spectral_abscissa(local_jacobian(k, r)) < 0.0

    audit = g1_hardening_audit(k, r)
    assert audit.exact_unity_route == "NO_EXACT_UNITY_ROUTE_FROM_NAIVE_NORMALIZATION"


def test_symmetric_generalized_route_has_exact_unity_boundary():
    r = np.diag([2.0, 0.5])
    k_stable = np.diag([1.8, 0.4])
    k_boundary = np.diag([2.0, 0.4])
    k_unstable = np.diag([2.2, 0.4])

    assert symmetric_generalized_g1_value(k_stable, r) == pytest.approx(0.9)
    assert symmetric_generalized_g1_value(k_boundary, r) == pytest.approx(1.0)
    assert symmetric_generalized_g1_value(k_unstable, r) == pytest.approx(1.1)

    assert spectral_abscissa(local_jacobian(k_stable, r)) < 0.0
    assert spectral_abscissa(local_jacobian(k_boundary, r)) == pytest.approx(0.0)
    assert spectral_abscissa(local_jacobian(k_unstable, r)) > 0.0

    audit = g1_hardening_audit(k_stable, r)
    assert audit.exact_unity_route == "SYMMETRIC_GENERALIZED_EXACT"


def test_directed_operator_cannot_silently_use_symmetric_generalized_route():
    r = np.diag([2.0, 0.5])
    k = np.array([[1.0, 0.4], [-0.1, 0.2]])
    with pytest.raises(ValueError, match="symmetric production Jacobian"):
        symmetric_generalized_g1_value(k, r)


def test_invalid_restoration_fails_loudly():
    k = np.eye(2)
    singular_r = np.diag([1.0, 0.0])
    with pytest.raises(ValueError, match="nonsingular"):
        naive_left_normalized_interaction(k, singular_r)
    with pytest.raises(ValueError, match="positive definite"):
        symmetric_generalized_g1_value(k, singular_r)
    with pytest.raises(ValueError, match="restoration = beta\*I"):
        scalar_restoration_g1_value(k, np.diag([1.0, 2.0]))
