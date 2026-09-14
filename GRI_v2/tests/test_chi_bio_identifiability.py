import math

import numpy as np
import pytest

from src.chi_bio_identifiability import (
    formal_state_dimension_rank_ceiling,
    g1a_value_from_known_jacobian_and_beta,
    g1a_values_across_restoration_scales,
    g2_reference_interval_value,
    transition_parameter_count,
)


def test_same_jacobian_does_not_identify_numeric_g1a_without_beta():
    j = np.diag([-0.2, -0.5])
    values = g1a_values_across_restoration_scales(j, (0.5, 1.0, 2.0))

    assert values == pytest.approx((0.6, 0.8, 0.9))
    assert all(v < 1.0 for v in values)
    assert len(set(round(v, 12) for v in values)) == 3


def test_g1a_value_requires_independent_positive_restoration_scale():
    j = np.diag([-0.2, -0.5])
    with pytest.raises(ValueError):
        g1a_value_from_known_jacobian_and_beta(j, beta=0.0)


def test_g2_reference_interval_conversion_preserves_unity_side_and_value():
    alpha_j = -0.2
    for delta in (0.5, 1.0, 2.0):
        rho_delta = math.exp(alpha_j * delta)
        per_unit = g2_reference_interval_value(
            rho_delta, observed_interval=delta, reference_interval=1.0
        )
        assert per_unit == pytest.approx(math.exp(alpha_j))
        assert per_unit < 1.0


def test_scc25_best_case_rank_ceilings_are_small_relative_to_transcriptome():
    # 11 ordered states per arm => 10 transitions per arm.
    # Two arms give 20 transitions if a shared T plus one treatment input is modeled.
    assert formal_state_dimension_rank_ceiling(
        20, exogenous_input_dimension=1, include_intercept=True
    ) == 18
    assert formal_state_dimension_rank_ceiling(
        10, exogenous_input_dimension=0, include_intercept=True
    ) == 9

    assert transition_parameter_count(18, exogenous_input_dimension=1, include_intercept=True) == 360
    assert transition_parameter_count(9, exogenous_input_dimension=0, include_intercept=True) == 90


def test_identifiability_helpers_reject_invalid_dimensions():
    with pytest.raises(ValueError):
        transition_parameter_count(0)
    with pytest.raises(ValueError):
        formal_state_dimension_rank_ceiling(0)
    with pytest.raises(ValueError):
        g2_reference_interval_value(0.0, observed_interval=1.0)
