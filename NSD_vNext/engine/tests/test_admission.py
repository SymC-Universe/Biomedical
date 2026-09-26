import pytest

from nsd_engine import (
    AdmissionEvidence,
    CandidateMode,
    RefusalCode,
    ScalarProposal,
    decide_scalar_admission,
)


def mode(*, identifiable=True):
    return CandidateMode(
        mode_id="m1",
        source_method="qualified_fixture",
        frequency_hz=10.0,
        decay_rate_per_s=2.0,
        identifiable=identifiable,
    )


def proposal():
    return ScalarProposal(
        name="chi_mode_m1",
        value=0.2,
        uncertainty=0.02,
        derivation="fixture-only second-order mapping",
        dependencies=("omega0", "decay_rate"),
    )


def evidence(**overrides):
    values = dict(
        estimator_qualified=True,
        natural_frequency_mapping_verified=True,
        damping_or_decay_mapping_verified=True,
        broadening_resolved=True,
        uncertainty_acceptable=True,
        in_domain=True,
    )
    values.update(overrides)
    return AdmissionEvidence(**values)


def test_fully_qualified_mode_is_admitted():
    decision = decide_scalar_admission(mode(), proposal(), evidence())
    assert decision.admitted
    assert decision.licensed is not None
    assert decision.licensed.source_mode_id == "m1"
    assert decision.refusal is None


@pytest.mark.parametrize(
    "overrides, expected",
    [
        ({"in_domain": False}, RefusalCode.OUT_OF_DOMAIN),
        ({"estimator_qualified": False}, RefusalCode.MODE_NONIDENTIFIABLE),
        ({"natural_frequency_mapping_verified": False}, RefusalCode.FREQ_NOT_OMEGA0),
        ({"damping_or_decay_mapping_verified": False}, RefusalCode.WIDTH_NOT_DAMPING),
        ({"broadening_resolved": False}, RefusalCode.BROADENING_UNRESOLVED),
        ({"uncertainty_acceptable": False}, RefusalCode.UNCERTAINTY_TOO_LARGE),
    ],
)
def test_each_firewall_condition_refuses_without_substitute(overrides, expected):
    decision = decide_scalar_admission(mode(), proposal(), evidence(**overrides))
    assert not decision.admitted
    assert decision.licensed is None
    assert decision.refusal is not None
    assert decision.refusal.code is expected


def test_nonidentifiable_mode_refuses_even_if_boolean_evidence_is_otherwise_positive():
    decision = decide_scalar_admission(mode(identifiable=False), proposal(), evidence())
    assert decision.refusal is not None
    assert decision.refusal.code is RefusalCode.MODE_NONIDENTIFIABLE
