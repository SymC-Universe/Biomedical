from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src import run_biosystems_tumor_normal_control as run


def mini_cfg():
    return {
        "seed_namespace": "TEST_TN",
        "primary_paired": {"cancers": ["TEST"], "fixed_n": 20, "resamples": 4},
        "secondary_unpaired_n30": {"cancers": ["TEST"], "fixed_n": 30, "resamples": 4},
        "feature_rules": {
            "methylation_finite_fraction_min": 0.95,
            "rna_finite_fraction_min": 0.95,
            "rna_minimum_finite": 20,
            "rna_minimum_hallmark_genes": 2,
            "methylation_minimum_hallmark_genes": 2,
            "methylation_minimum_hallmark_probes": 2,
            "minimum_common_hallmarks": 1,
            "promoter_core_groups": ["TSS200"],
        },
    }


def write_manifests(tmp_path: Path):
    pair_rows = []
    sample_rows = []
    for i in range(35):
        pid = f"TCGA-ZZ-{i:04d}"
        for st in ("01", "11"):
            sample_rows.append({
                "cancer_type": "TEST",
                "patient_id": pid,
                "sample_type": st,
                "rna_label": f"{pid}-{st}A-RNA",
                "methylation_label": f"{pid}-{st}A-METH",
                "rna_root": f"{pid}-{st}A",
                "methylation_root": f"{pid}-{st}A",
            })
        if i < 25:
            pair_rows.append({
                "cancer_type": "TEST",
                "patient_id": pid,
                "rna_tumor_01_label": f"{pid}-01A-RNA",
                "rna_normal_11_label": f"{pid}-11A-RNA",
                "methylation_tumor_01_label": f"{pid}-01A-METH",
                "methylation_normal_11_label": f"{pid}-11A-METH",
                "rna_tumor_01_root": f"{pid}-01A",
                "rna_normal_11_root": f"{pid}-11A",
                "methylation_tumor_01_root": f"{pid}-01A",
                "methylation_normal_11_root": f"{pid}-11A",
            })
    pair_path = tmp_path / "pairs.csv"
    sample_path = tmp_path / "samples.csv"
    pd.DataFrame(pair_rows).to_csv(pair_path, index=False)
    pd.DataFrame(sample_rows).to_csv(sample_path, index=False)
    return pair_path, sample_path


def test_primary_membership_is_same_participant_and_deterministic(tmp_path):
    cfg = mini_cfg()
    pp, sp = write_manifests(tmp_path)
    pairs, samples, selected, key_index = run.prepare_selected_samples(pp, sp, cfg)
    tp, _ = run.cohort_rows_primary(pairs, key_index, "TEST", "01")
    npids, _ = run.cohort_rows_primary(pairs, key_index, "TEST", "11")
    a = run.draw_memberships("PRIMARY_PAIRED", "TEST", tp, npids, cfg)
    b = run.draw_memberships("PRIMARY_PAIRED", "TEST", tp, npids, cfg)
    assert a == b
    assert len(a) == 4
    for _, tumor, normal in a:
        assert tumor == normal
        assert len(tumor) == 20
        assert len(set(tumor)) == 20


def test_secondary_memberships_are_equal_n_and_source_bound(tmp_path):
    cfg = mini_cfg()
    pp, sp = write_manifests(tmp_path)
    pairs, samples, selected, key_index = run.prepare_selected_samples(pp, sp, cfg)
    tp, _ = run.cohort_rows_secondary(samples, key_index, "TEST", "01")
    npids, _ = run.cohort_rows_secondary(samples, key_index, "TEST", "11")
    rows = run.draw_memberships("SECONDARY_UNPAIRED_N30", "TEST", tp, npids, cfg)
    assert len(rows) == 4
    for _, tumor, normal in rows:
        assert len(tumor) == 30
        assert len(normal) == 30
        assert set(tumor).issubset(set(tp))
        assert set(normal).issubset(set(npids))


def test_shared_feature_carrier_requires_both_tissues():
    cfg = mini_cfg()
    rng = np.random.default_rng(7)
    meth = rng.random((40, 6))
    rna = rng.normal(size=(40, 5))
    tumor = np.arange(0, 20)
    normal = np.arange(20, 40)
    tech = np.array([False, True, False, False, False, False])

    # Probe 2 fails normal 95% rule; RNA gene 3 fails tumor variance.
    meth[20:22, 2] = np.nan
    rna[:20, 3] = 1.0

    tracks, shared_rna, med_t, med_n = run.feature_carriers(meth, rna, tumor, normal, tech, cfg)
    assert tracks["PRIMARY_PUBLICATION"].tolist() == [True, True, False, True, True, True]
    assert tracks["MASKED_TECHNICAL"].tolist() == [True, False, False, True, True, True]
    assert shared_rna.tolist() == [True, True, True, False, True]
    assert np.isfinite(med_t[tracks["PRIMARY_PUBLICATION"]]).all()
    assert np.isfinite(med_n[tracks["PRIMARY_PUBLICATION"]]).all()


def test_hallmark_scores_generalized_n20():
    cfg = mini_cfg()
    rng = np.random.default_rng(11)
    beta = rng.random((20, 4))
    rna = rng.normal(size=(20, 4))
    gene_map = {
        "G1": np.array([0, 1]),
        "G2": np.array([2, 3]),
    }
    modules = {"HALLMARK_X": ["G1", "G2", "R1", "R2"]}
    rna_index = {"G1": 0, "G2": 1, "R1": 2, "R2": 3}
    ms, rs, meta = run.build_hallmark_scores(beta, rna, gene_map, modules, rna_index, cfg)
    assert "HALLMARK_X" in ms
    assert "HALLMARK_X" in rs
    assert ms["HALLMARK_X"].shape == (20,)
    assert rs["HALLMARK_X"].shape == (20,)
