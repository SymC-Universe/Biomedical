from nsd_engine.v02_frozen_contract import validate_frozen_science


def test_frozen_v02_identity_guard():
    result = validate_frozen_science()
    assert result['status'] == 'PASS'
    assert result['execution_authorized'] is False
    assert result['scientific_outcomes_opened'] is False
