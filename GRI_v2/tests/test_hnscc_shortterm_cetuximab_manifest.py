import json
from pathlib import Path


def _data():
    return json.loads(
        Path("config/gri_hnscc_shortterm_cetuximab_manifest_p0d_v0_1.json").read_text(
            encoding="utf-8"
        )
    )


def test_scc25_and_scc1_have_complete_declared_daily_roles():
    data = _data()["bulk_daily"]
    for cell_line in ("SCC25", "SCC1"):
        block = data[cell_line]
        assert block["status"].startswith("COMPLETE_DAILY")
        assert set(block["PBS"]) == {"0", "1", "2", "3", "4", "5"}
        assert set(block["CTX"]) == {"1", "2", "3", "4", "5"}
        all_gsms = list(block["PBS"].values()) + list(block["CTX"].values())
        assert len(all_gsms) == len(set(all_gsms)) == 11


def test_scc6_metadata_ambiguity_is_preserved_not_silently_fixed():
    block = _data()["bulk_daily"]["SCC6"]
    assert block["status"] == "METADATA_AMBIGUOUS_FOR_ORDERED_DAILY_TRAJECTORY"
    days = [row["day"] for row in block["CTX_GEO_LABELS"]]
    assert days.count(2) == 2
    assert 1 not in days
    assert "no correction inferred" in block["ambiguity"]


def test_scc25_single_cell_role_is_endpoint_not_longitudinal_same_cell():
    block = _data()["single_cell_day5"]["SCC25"]
    assert len(block["CTX"]) == 2
    assert len(block["PBS"]) == 2
    assert "NOT_LONGITUDINAL_SAME_CELL_TRAJECTORY" in block["role"]


def test_cross_timescale_source_is_not_mislabeled_external_independent_replication():
    relation = _data()["cross_source_relations"]
    assert relation["same_named_cell_line"] is True
    assert relation["same_nominal_cetuximab_concentration"] is True
    assert relation["same_experiment"] is False
    assert relation["independent_laboratory"] is False


def test_no_chi_or_proliferation_leakage_in_source_selection():
    firewall = _data()["selection_firewall"]
    assert firewall["chi_bio_outcomes_opened"] is False
    assert firewall["selected_by_candidate_agreement"] is False
    assert firewall["proliferation_used_for_state_selection"] is False
