import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CFG = ROOT / "config" / "stage_c1_annotation_feature_plan.json"


def load_cfg():
    return json.loads(CFG.read_text(encoding="utf-8"))


def test_c1_annotation_plan_is_frozen_pre_association():
    cfg = load_cfg()
    assert cfg["status"] == "FROZEN_AFTER_USER_APPROVAL_BEFORE_ANY_C1_BETA_VALUE_ASSOCIATION"
    assert cfg["frozen_upstream"]["stage_c0_1_unique_one_to_one_samples"] == 9460
    assert cfg["frozen_upstream"]["stage_c0_1_cancers_passing_n30"] == 32
    assert cfg["c1_analysis_constraints"]["chi_allowed"] is False
    assert cfg["c1_analysis_constraints"]["cv2_used"] is False
    assert cfg["c1_analysis_constraints"]["master_stability_score_allowed"] is False
    assert cfg["c1_analysis_constraints"]["substrate_inheritance_claim_allowed"] is False


def test_primary_annotation_lineage_is_exactly_pinned():
    cfg = load_cfg()["primary_annotation_source"]
    assert cfg["package"] == "IlluminaHumanMethylation450kanno.ilmn12.hg19"
    assert cfg["bioconductor_release"] == "3.8"
    assert cfg["package_version"] == "0.6.0"
    assert cfg["underlying_manifest"] == "HumanMethylation450_15017482_v.1.2.csv"
    assert "hg19" in cfg["lineage"]
    assert len(cfg["candidate_urls"]) >= 2


def test_many_to_many_mapping_and_strata_cannot_collapse_silently():
    cfg = load_cfg()
    mapping = cfg["gene_mapping"]
    assert mapping["first_gene_selection_allowed"] is False
    assert mapping["result_driven_mapping_allowed"] is False
    assert mapping["on_tuple_length_mismatch"].startswith("exclude")
    strata = cfg["regulatory_strata"]
    assert strata["PROMOTER_CORE"] == ["TSS200"]
    assert strata["PROMOTER_PROXIMAL"] == ["TSS1500"]
    assert set(strata["PROMOTER_TRANSCRIBED_EDGE"]) == {"5'UTR", "1stExon"}
    assert strata["GENE_BODY"] == ["Body"]
    assert strata["THREE_PRIME_UTR"] == ["3'UTR"]


def test_technical_robustness_mask_is_pre_result_and_dual_component():
    tech = load_cfg()["technical_mask_robustness"]
    chen = tech["cross_reactive_component"]
    snp = tech["common_snp_component"]
    assert chen["commit"] == "eac47812dce5d4d1340caeafb92d80dd4d8273a5"
    assert chen["github_blob_sha1"] == "f5bff6dee26f8d05ccd2d0bcfaf8ff1c0afb6e11"
    assert "TargetID" in chen["rule"]
    assert "CpG_rs" in snp["rule"] and "SBE_rs" in snp["rule"]
    assert "Probe_rs alone does not trigger" in snp["rule"]
    assert "union" in tech["union_rule"].lower()
    assert "both" in tech["promotion_rule"].lower()


def test_c1a_source_gate_forbids_biological_association():
    gate = load_cfg()["c1a_source_gate"]
    forbidden = " ".join(gate["forbidden"]).lower()
    assert "beta values for biological analysis" in forbidden
    assert "methylation-rna" in forbidden
    assert "outcome" in forbidden
