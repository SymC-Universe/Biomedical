import json
from pathlib import Path


def _data():
    return json.loads(
        Path("config/gri_hnscc_day5_scrna_scc25_manifest_p0d_v0_1.json").read_text(
            encoding="utf-8"
        )
    )


def test_scrna_verified_dimensions_are_cross_file_consistent():
    data = _data()
    expr = data["files"]["expression"]
    pheno = data["files"]["pheno"]
    feature = data["files"]["feature"]
    assert expr["cell_columns"] == pheno["rows"] == 8920
    assert expr["gene_rows"] == feature["rows"] == 33538
    assert sum(pheno["counts"].values()) == 8920


def test_scrna_treatment_replicate_counts_are_frozen_exactly():
    counts = _data()["files"]["pheno"]["counts"]
    assert counts == {
        "CTX_R1": 1999,
        "CTX_R2": 2027,
        "PBS_R1": 2318,
        "PBS_R2": 2576,
    }


def test_scrna_gene_case_difference_is_visible_not_silently_normalized():
    identity = _data()["cross_file_identity"]
    assert identity["expression_cell_ids_vs_pheno_ids"] == "EXACT_ORDER_MATCH"
    assert identity["expression_gene_symbols_vs_feature_gene_short_name"] == "CASE_ONLY_ORDER_MATCH"
    assert identity["case_only_gene_symbol_differences"] == 404
    assert identity["source_strings_rewritten"] is False


def test_scrna_source_probe_did_not_select_chi_features():
    firewall = _data()["selection_firewall"]
    assert firewall["chi_bio_outcomes_opened"] is False
    assert firewall["feature_selection_performed_in_source_probe"] is False
    assert firewall["bulk_state_dimension_selected_using_scrna"] is False
    assert firewall["unity_used_for_scrna_selection"] is False
