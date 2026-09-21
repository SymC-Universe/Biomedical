from src.validate_gri_external_claim_scrutiny import validate

def test_external_claim_scrutiny_ledger():
    d=validate()
    by={x["id"]:x for x in d["claims"]}
    assert by["EC-01"]["status"]=="CORRECTED_NARROWED"
    assert by["EC-09"]["status"]=="UNRESOLVED_METHOD_ROBUSTNESS"
    assert by["EC-15"]["status"]=="NOT_TESTED_AGAINST_STANDARD_TOOLKIT"
    assert by["EC-17"]["status"]=="NOT_ESTABLISHED"
