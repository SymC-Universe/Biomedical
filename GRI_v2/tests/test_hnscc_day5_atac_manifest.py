import json
from pathlib import Path


def _data():
    return json.loads(
        Path("config/gri_hnscc_day5_atac_manifest_p0d_v0_1.json").read_text(
            encoding="utf-8"
        )
    )


def test_nominal_atac_design_is_three_cell_lines_two_conditions_three_replicates():
    data = _data()
    samples = data["samples"]
    assert set(samples) == {"SCC1", "SCC6", "SCC25"}
    gsms = []
    for cell_line in samples.values():
        assert set(cell_line) == {"CTX", "PBS"}
        for condition in cell_line.values():
            assert len(condition) == 3
            assert {row["replicate"] for row in condition} == {1, 2, 3}
            gsms.extend(row["gsm"] for row in condition)
    assert len(gsms) == len(set(gsms)) == 18


def test_scc25_atac_accessions_are_exact():
    block = _data()["samples"]["SCC25"]
    assert [r["gsm"] for r in block["CTX"]] == [
        "GSM4021925", "GSM4021926", "GSM4021927"
    ]
    assert [r["gsm"] for r in block["PBS"]] == [
        "GSM4021928", "GSM4021929", "GSM4021930"
    ]


def test_scc1_pbs2_qc_failure_is_explicit_and_unique():
    data = _data()
    failures = [
        row
        for cell_line in data["samples"].values()
        for condition in cell_line.values()
        for row in condition
        if row["processed_peak_status"] == "SAMPLE_RECORD_QC_FAILURE_NO_PROCESSED_PEAK_FILE"
    ]
    assert len(failures) == 1
    assert failures[0]["gsm"] == "GSM4021917"
    assert data["known_qc_exceptions"][0]["gsm"] == "GSM4021917"


def test_atac_is_context_not_naive_state_concatenation():
    role = _data()["approved_architecture_role"]
    assert role["state"] == "RNA_TRANSCRIPTOMIC_REGULATORY_STATE"
    assert role["atac"] == "SUBSTRATE_CONTEXT_ENDPOINT"
    assert role["naive_concatenation_allowed"] is False
    assert role["longitudinal_atac_claim_allowed"] is False


def test_source_selection_has_no_chi_or_unity_leakage():
    firewall = _data()["selection_firewall"]
    assert firewall["chi_bio_outcomes_opened"] is False
    assert firewall["selected_by_candidate_agreement"] is False
    assert firewall["rna_state_dimension_selected_using_atac"] is False
    assert firewall["unity_used_for_atac_feature_selection"] is False
