from src.validate_conglomerate_v01_source_bindings import validate

def test_conglomerate_source_bindings():
    d=validate()
    assert set(d["blocks"]) == {"R","S","E","G","P","M","T","Q"}
    assert d["global_firewalls"]["tcga_final_holdout_is_external_for_new_conglomerate_version"] is False
