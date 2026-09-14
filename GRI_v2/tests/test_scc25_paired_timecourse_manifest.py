import json
from collections import Counter
from pathlib import Path


def _manifest():
    return json.loads(
        Path("config/gri_scc25_paired_timecourse_manifest_p0d_v0_1.json").read_text(
            encoding="utf-8"
        )
    )


def test_scc25_main_manifest_is_exactly_11_weeks_by_2_arms():
    data = _manifest()
    rows = data["main_timecourse"]
    assert len(rows) == 22
    assert {row["week"] for row in rows} == set(range(1, 12))
    counts = Counter((row["week"], row["arm"]) for row in rows)
    assert set(row["arm"] for row in rows) == {"PBS", "CTX"}
    assert all(counts[(week, arm)] == 1 for week in range(1, 12) for arm in ("PBS", "CTX"))


def test_scc25_rna_and_methylation_accessions_are_unique_and_one_to_one():
    rows = _manifest()["main_timecourse"]
    rna = [row["rna_gsm"] for row in rows]
    meth = [row["methylation_gsm"] for row in rows]
    assert len(rna) == len(set(rna)) == 22
    assert len(meth) == len(set(meth)) == 22
    assert all(x.startswith("GSM") for x in rna + meth)


def test_scc25_accession_sequence_matches_geo_week_arm_order():
    rows = _manifest()["main_timecourse"]
    by_key = {(r["week"], r["arm"]): r for r in rows}
    for week in range(1, 12):
        pbs = by_key[(week, "PBS")]
        ctx = by_key[(week, "CTX")]
        assert pbs["rna_gsm"] == f"GSM{2612464 + 2 * week}"
        assert ctx["rna_gsm"] == f"GSM{2612465 + 2 * week}"
        assert pbs["methylation_gsm"] == f"GSM{2612500 + 2 * week}"
        assert ctx["methylation_gsm"] == f"GSM{2612501 + 2 * week}"


def test_scc25_main_trajectory_excludes_all_declared_baselines_and_stable_clones():
    data = _manifest()
    used = {
        gsm
        for row in data["main_timecourse"]
        for gsm in (row["rna_gsm"], row["methylation_gsm"])
    }
    excluded = {
        gsm
        for group in data["excluded_source_samples"].values()
        for gsm in group
    }
    assert used.isdisjoint(excluded)
    assert data["selection_firewall"]["main_timecourse_only"] is True
    assert data["selection_firewall"]["chi_bio_outcomes_opened"] is False
    assert data["selection_firewall"]["selected_by_chi_bio_agreement"] is False
