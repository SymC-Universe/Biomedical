import json
from pathlib import Path


def _load(name):
    return json.loads(Path("config", name).read_text(encoding="utf-8"))


def _manifest():
    return _load("gri_scc25_paired_timecourse_manifest_p0d_v0_1.json")


def _lock():
    return _load("gri_scc25_chronic_source_provenance_lock_v0_2.json")


def test_chronic_source_hashes_match_machine_provenance_lock():
    bindings = _manifest()["processed_source_bindings"]
    locks = _lock()["source_locks"]
    assert bindings["rna_sample_metadata"]["sha256"] == locks["rna_series_matrix"]["sha256"]
    assert bindings["rna_processed_molecular_source"]["sha256"] == locks["rna_processed_molecular_source"]["sha256"]
    assert bindings["methylation_processed_matrix"]["sha256"] == locks["methylation_series_matrix"]["sha256"]
    assert bindings["methylation_raw_file_index"]["sha256"] == locks["methylation_raw_file_index"]["sha256"]


def test_machine_provenance_repeated_without_source_projection_drift():
    evidence = _lock()["machine_evidence"]
    assert evidence["source_projection_identical_across_runs"] is True
    assert evidence["source_projection_sha256"] == "fa8772da77054785ff2fb384d336ff6821ed32e65172708a92a975ba1321e70b"
    assert [run["run_number"] for run in evidence["runs"]] == [3, 13]


def test_rna_container_and_main_trajectory_roles_remain_separate():
    data = _manifest()
    binding = data["processed_source_bindings"]["rna_sample_metadata"]
    assert binding["sample_title_count"] == 36
    assert binding["sample_geo_accession_count"] == 36
    assert binding["value_table_status"] == "VALUE_TABLE_HEADER_FOUND"
    assert binding["table_header_field_count"] == 37
    assert len(data["main_timecourse"]) == 22


def test_rna_processed_table_anatomy_is_machine_verified_without_selection():
    binding = _manifest()["processed_source_bindings"]["rna_processed_molecular_source"]
    assert binding["anatomy_status"] == "GENE_BY_SAMPLE_TABLE_ANATOMY_MACHINE_VERIFIED_NO_FEATURE_SELECTION"
    assert binding["header_field_count"] == 37
    assert binding["first_data_field_count"] == 37
    assert binding["data_rows"] == 20531
    assert binding["decompressed_sha256"] == "1f718bc27a93d6520cc2966bb8dbe1a87e9e3a29db2021ade6242cad230696f5"


def test_methylation_main_trajectory_stays_inside_full_container():
    data = _manifest()
    binding = data["processed_source_bindings"]["methylation_processed_matrix"]
    main_meth = {row["methylation_gsm"] for row in data["main_timecourse"]}
    assert binding["sample_title_count"] == 36
    assert binding["table_header_field_count"] == 37
    assert binding["baseline_gsm"] == "GSM2612501"
    assert binding["baseline_gsm"] not in main_meth
    assert main_meth == {f"GSM{x}" for x in range(2612502, 2612524)}


def test_raw_methylation_tar_not_downloaded_for_processed_source_gate():
    raw = _manifest()["processed_source_bindings"]["methylation_raw_tar"]
    assert raw["preflight_size_bytes"] == 499036160
    assert raw["downloaded"] is False


def test_source_acquisition_did_not_open_chi_or_fit_state():
    firewall = _manifest()["selection_firewall"]
    lock_firewall = _lock()["selection_firewall"]
    assert firewall["chi_bio_outcomes_opened"] is False
    assert firewall["feature_selection_performed_in_source_probe"] is False
    assert firewall["state_reduction_fitted_in_source_probe"] is False
    assert lock_firewall["candidate_chi_bio_computed"] is False
    assert lock_firewall["transition_model_fit"] is False
