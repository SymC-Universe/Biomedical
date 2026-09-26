from nsd_engine import RefusalCode, ScalarRefusal, to_canonical_json


def test_serialization_is_deterministic_and_serializes_enums():
    record = ScalarRefusal("chi_mode", RefusalCode.NO_PEAK, "no qualifying peak")
    text = to_canonical_json(record)
    assert text == '{"code":"REF_NO_PEAK","detail":"no qualifying peak","requested_scalar":"chi_mode","source_mode_id":null}'
