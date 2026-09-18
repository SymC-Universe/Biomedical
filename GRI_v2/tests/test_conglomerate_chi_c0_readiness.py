from pathlib import Path

from src.audit_conglomerate_chi_c0_readiness import build_readiness


def test_conglomerate_c0_compact_provenance_is_complete():
    repo_root = Path(__file__).resolve().parents[2]
    result = build_readiness(repo_root)

    assert result["blocks_total"] == 8
    assert result["blocks_with_compact_provenance_ready"] == 8
    assert result["missing_compact_source_refs"] == []
    assert result["status"] == "C0_READY_C1_HEAVY_MATERIALIZATION_NEXT"


def test_conglomerate_c0_preserves_foundational_firewalls():
    repo_root = Path(__file__).resolve().parents[2]
    result = build_readiness(repo_root)
    s = result["safeguards"]

    assert s["capital_chi_not_universal_scalar"] is True
    assert s["damped_oscillator_not_required"] is True
    assert s["unity_boundary_not_required"] is True
    assert s["master_score_not_required"] is True
    assert s["tcga_final_holdout_marked_opened"] is True
    assert s["new_conglomerate_tcga_role_is_development_only"] is True
    assert s["prior_internal_predictive_summary_present"] is True
    assert s["prior_internal_predictor_closed"] is True
    assert s["prior_final_primary_evaluable_cancers"] == 18
    assert s["prior_all_methylation_better_cancers"] == 17


def test_conglomerate_c0_does_not_pretend_patient_level_data_are_in_repo():
    repo_root = Path(__file__).resolve().parents[2]
    result = build_readiness(repo_root)

    assert result["blocks_with_heavy_materialization_pending"] >= 1
    assert (
        result["execution"]["github_patient_level_conglomerate_compute"]
        == "NOT_YET_MATERIALIZED_FROM_CURRENT_PUBLIC_REPO"
    )
    assert result["execution"]["user_local_compute_required_now"] is False
