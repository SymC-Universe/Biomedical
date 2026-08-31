from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.run_tool_prediction_p0_d2_rna_target import run


def sha(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def build_case(tmp_path: Path, heldout_shift: float = 0.0, drop_discovery_from_cache: bool = False):
    gmt = tmp_path / "Hallmark_Genes.gmt"
    gmt.write_text(
        "HALLMARK_ONE\ttest\tG0\tG1\tG2\tG3\n"
        "HALLMARK_TWO\ttest\tG4\tG5\n",
        encoding="utf-8",
    )

    discovery = [f"D{i:02d}" for i in range(12)]
    heldout = [f"X{i:02d}" for i in range(4)]
    patients = discovery + heldout
    genes = np.array([f"G{i}" for i in range(6)], dtype=object)
    rng = np.random.default_rng(7)
    x = rng.normal(size=(len(patients), len(genes)))
    x[:12, 0] = np.linspace(0.0, 2.0, 12)
    x[:12, 1] = x[:12, 0] * 0.7 + rng.normal(scale=0.05, size=12)
    x[:12, 2] = -x[:12, 0] * 0.4 + rng.normal(scale=0.05, size=12)
    x[:12, 3] = rng.normal(size=12)
    x[12:, :] += float(heldout_shift)
    cache_patients = patients.copy()
    if drop_discovery_from_cache:
        cache_patients[0] = "MISSING_D00"
    cache = tmp_path / "hallmark_profile_cache.npz"
    np.savez(
        cache,
        sample_ids=np.array([p + "-01A" for p in cache_patients], dtype=object),
        patient_ids=np.array(cache_patients, dtype=object),
        cancer_types=np.array(["TEST"] * len(cache_patients), dtype=object),
        gene_symbols=genes,
        expression_log2p1=x,
    )

    d1_scores = tmp_path / "Discovery_Methylation_Scores.csv.gz"
    rows = []
    for track in ["PRIMARY_PUBLICATION", "MASKED_TECHNICAL"]:
        for hallmark in ["HALLMARK_ONE"]:
            for p in discovery:
                rows.append({"cancer_type": "TEST", "participant_root": p, "track": track, "hallmark": hallmark, "methylation_pc1": 0.0})
    pd.DataFrame(rows).to_csv(d1_scores, index=False, compression="gzip")

    d1_h = tmp_path / "Hallmark_Eligibility.csv"
    hrows = []
    for track in ["PRIMARY_PUBLICATION", "MASKED_TECHNICAL"]:
        hrows.extend([
            {"cancer_type": "TEST", "track": track, "hallmark": "HALLMARK_ONE", "mapped_gene_count": 4, "contributing_probe_count": 4, "eligible_by_frozen_mapping_rule": True, "pc1_status": "PC1_EVALUABLE"},
            {"cancer_type": "TEST", "track": track, "hallmark": "HALLMARK_TWO", "mapped_gene_count": 2, "contributing_probe_count": 2, "eligible_by_frozen_mapping_rule": False, "pc1_status": "NOT_ELIGIBLE_MAPPING_RULE"},
        ])
    pd.DataFrame(hrows).to_csv(d1_h, index=False)

    cfg = {
        "schema": "test",
        "stage_a_profile_cache_sha256": sha(cache),
        "hallmark_membership_sha256": sha(gmt),
        "d1_methylation_discovery_scores_sha256": sha(d1_scores),
        "d1_hallmark_eligibility_sha256": sha(d1_h),
        "discovery_participants": 12,
        "fully_evaluable_cancers": ["TEST"],
        "expected_discovery_n_by_cancer": {"TEST": 12},
        "rna_gene_finite_fraction_min": 0.8,
        "rna_gene_finite_samples_min": 3,
        "rna_hallmark_retained_genes_min": 3,
        "minimum_common_hallmarks_for_semantic_branch": 1,
        "expected_hallmark_modules": 2,
        "expected_d1_source_eligible_hallmarks_per_track": 1,
        "heldout_target_scores_allowed": False,
        "partition_reassignment_allowed": False,
        "biological_chi_allowed": False,
        "stage_c1_modification_allowed": False,
    }
    config = tmp_path / "config.json"
    config.write_text(json.dumps(cfg), encoding="utf-8")
    return config, cache, gmt, d1_scores, d1_h


def execute(case, out):
    config, cache, gmt, d1_scores, d1_h = case
    return run(config, cache, gmt, d1_scores, d1_h, out)


def test_discovery_target_contract(tmp_path):
    case = build_case(tmp_path)
    out = tmp_path / "out"
    result = execute(case, out)
    assert result["status"] == "P0_D2_RNA_DISCOVERY_TARGET_COMPLETE"
    assert result["discovery_participants_processed"] == 12
    assert result["replication_target_scores_generated"] is False
    assert result["final_holdout_target_scores_generated"] is False

    elig = pd.read_csv(out / "RNA_Target_Eligibility.csv")
    one = elig[elig.hallmark == "HALLMARK_ONE"].iloc[0]
    two = elig[elig.hallmark == "HALLMARK_TWO"].iloc[0]
    assert bool(one.eligible_by_frozen_mapping_rule)
    assert one.pc1_status == "PC1_EVALUABLE"
    assert not bool(two.eligible_by_frozen_mapping_rule)
    assert two.pc1_status == "NOT_ELIGIBLE_MAPPING_RULE"

    tr = pd.read_csv(out / "RNA_Target_Transforms.csv.gz")
    assert set(tr.hallmark) == {"HALLMARK_ONE"}
    assert abs(float(np.sum(np.square(tr.pc1_loading))) - 1.0) < 1e-12
    assert tr.orientation_method.nunique() == 1

    scores = pd.read_csv(out / "RNA_Discovery_Scores.csv.gz")
    assert len(scores) == 12
    assert set(scores.participant_root) == {f"D{i:02d}" for i in range(12)}
    assert np.isfinite(scores.rna_pc1).all()
    assert abs(float(scores.rna_pc1.mean())) < 1e-12


def test_heldout_mutation_cannot_change_discovery_outputs(tmp_path):
    case1_dir = tmp_path / "a"; case1_dir.mkdir()
    case2_dir = tmp_path / "b"; case2_dir.mkdir()
    out1 = case1_dir / "out"; out2 = case2_dir / "out"
    execute(build_case(case1_dir, heldout_shift=0.0), out1)
    execute(build_case(case2_dir, heldout_shift=1e6), out2)
    for name in ["RNA_Target_Eligibility.csv", "RNA_Target_Transforms.csv.gz", "RNA_Discovery_Scores.csv.gz", "Common_Hallmarks.csv"]:
        if name.endswith(".gz"):
            a = pd.read_csv(out1 / name)
            b = pd.read_csv(out2 / name)
            pd.testing.assert_frame_equal(a, b, check_exact=True)
        else:
            assert (out1 / name).read_bytes() == (out2 / name).read_bytes()


def test_mapping_floor_refuses_small_hallmark_without_substitute(tmp_path):
    case = build_case(tmp_path)
    out = tmp_path / "out"
    execute(case, out)
    elig = pd.read_csv(out / "RNA_Target_Eligibility.csv")
    two = elig[elig.hallmark == "HALLMARK_TWO"].iloc[0]
    assert int(two.retained_discovery_gene_count) == 2
    assert two.pc1_status == "NOT_ELIGIBLE_MAPPING_RULE"
    tr = pd.read_csv(out / "RNA_Target_Transforms.csv.gz")
    sc = pd.read_csv(out / "RNA_Discovery_Scores.csv.gz")
    assert "HALLMARK_TWO" not in set(tr.hallmark)
    assert "HALLMARK_TWO" not in set(sc.hallmark)


def test_missing_discovery_participant_fails_closed(tmp_path):
    case = build_case(tmp_path, drop_discovery_from_cache=True)
    with pytest.raises(ValueError, match="missing from Stage A cache"):
        execute(case, tmp_path / "out")
