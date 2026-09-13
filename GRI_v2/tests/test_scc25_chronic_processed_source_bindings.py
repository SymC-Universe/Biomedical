import json
from pathlib import Path


def _manifest():
    return json.loads(
        Path("config/gri_scc25_paired_timecourse_manifest_p0d_v0_1.json").read_text(
            encoding="utf-8"
        )
    )


def test_chronic_processed_source_hashes_are_bound():
    bindings = _manifest()["processed_source_bindings"]
    assert bindings["rna_sample_metadata"]["sha256"] == (
        "36fe26fb75134f05cabbf63fb3e18859204748e166963a7f34a27576fff304f0"
    )
    assert bindings["rna_processed_molecular_source"]["sha256"] == (
        "8b69cab4612f4787bedbc9ce9414ba321fc1c4bcba7ac63d50687e42d8a1b474"
    )
    assert bindings["methylation_processed_matrix"]["sha256"] == (
        "2bc72da999dfcd4601909979ce0559948f445915484b6b3a35c386ca71c1e885"
    )
    assert bindings["methylation_raw_file_index"]["sha256"] == (
        "efd1f17880389cf1eda6fde3b85f0c174ef8e79700a8b2f404271b36d06e0fca"
    )


def test_rna_series_matrix_is_not_mislabeled_value_matrix():
    binding = _manifest()["processed_source_bindings"]["rna_sample_metadata"]
    assert binding["sample_title_count"] == 22
    assert binding["sample_geo_accession_count"] == 22
    assert binding["value_table_status"] == "NO_VALUE_TABLE_HEADER_FOUND"
    assert "METADATA" in binding["role"]


def test_rna_processed_table_remains_blocked_until_anatomy_verified():
    binding = _manifest()["processed_source_bindings"]["rna_processed_molecular_source"]
    assert binding["anatomy_status"] == "OPEN_DO_NOT_ASSUME_GENE_BY_SAMPLE_ORIENTATION"
    assert binding["shallow_header_field_count"] == 20532
    assert binding["shallow_first_data_field_count"] == 23


def test_methylation_matrix_preserves_baseline_outside_main_trajectory():
    data = _manifest()
    binding = data["processed_source_bindings"]["methylation_processed_matrix"]
    main_meth = {row["methylation_gsm"] for row in data["main_timecourse"]}
    assert binding["sample_title_count"] == 23
    assert binding["table_header_field_count"] == 24
    assert binding["baseline_gsm"] == "GSM2612501"
    assert binding["baseline_gsm"] not in main_meth
    assert main_meth == {f"GSM{x}" for x in range(2612502, 2612524)}


def test_raw_methylation_tar_not_downloaded_for_processed_source_gate():
    raw = _manifest()["processed_source_bindings"]["methylation_raw_tar"]
    assert raw["preflight_size_bytes"] == 499036160
    assert raw["downloaded"] is False


def test_source_acquisition_did_not_open_chi_or_fit_state():
    firewall = _manifest()["selection_firewall"]
    assert firewall["chi_bio_outcomes_opened"] is False
    assert firewall["feature_selection_performed_in_source_probe"] is False
    assert firewall["state_reduction_fitted_in_source_probe"] is False
