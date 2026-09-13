from __future__ import annotations

from src.audit_chi_bio_chronic_g2_feature_gate_robustness import (
    DIAGNOSTIC_GATES,
    PRIMARY_REFERENCE,
)


def test_bounded_robustness_reports_both_predeclared_nonprimary_gates() -> None:
    assert set(DIAGNOSTIC_GATES) == {"0.1", "10.0"}
    assert {x["threshold"] for x in DIAGNOSTIC_GATES.values()} == {0.1, 10.0}
    assert all(x["threshold"] != PRIMARY_REFERENCE["threshold"] for x in DIAGNOSTIC_GATES.values())


def test_primary_reference_cannot_be_relabelled_as_diagnostic_gate() -> None:
    assert PRIMARY_REFERENCE["threshold"] == 1.0
    assert PRIMARY_REFERENCE["material_conclusions_by_rank"]["2"]["d1_adequacy"] == "PASS"
    assert PRIMARY_REFERENCE["material_conclusions_by_rank"]["3"]["d1_adequacy"] == "PASS"
    assert PRIMARY_REFERENCE["material_conclusions_by_rank"]["2"]["d2_reorganization_support"] == "NOT_SUPPORTED"
    assert PRIMARY_REFERENCE["material_conclusions_by_rank"]["3"]["d2_reorganization_support"] == "NOT_SUPPORTED"
