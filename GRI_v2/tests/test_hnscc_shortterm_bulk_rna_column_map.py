import json
from collections import Counter
from pathlib import Path


def _data():
    return json.loads(
        Path("config/gri_hnscc_shortterm_bulk_rna_column_map_p0d_v0_1.json").read_text(
            encoding="utf-8"
        )
    )


def test_processed_bulk_rna_map_is_exactly_33_unique_columns_and_gsms():
    data = _data()
    rows = data["columns"]
    assert len(rows) == 33
    assert len({r["column"] for r in rows}) == 33
    assert len({r["gsm"] for r in rows}) == 33
    assert data["processed_dimensions"] == {"genes": 56470, "sample_columns": 33}


def test_scc25_and_scc1_daily_roles_are_complete_without_reordering_by_gsm():
    rows = _data()["columns"]
    for cell in ("SCC25", "SCC1"):
        sub = [r for r in rows if r["cell_line"] == cell]
        counts = Counter((r["treatment"], r["day"]) for r in sub)
        assert all(counts[("PBS", day)] == 1 for day in range(0, 6))
        assert all(counts[("CTX", day)] == 1 for day in range(1, 6))
        assert len(sub) == 11


def test_scc6_source_day_ambiguity_is_preserved_in_mapping():
    rows = [r for r in _data()["columns"] if r["cell_line"] == "SCC6"]
    ctx_days = [r["day"] for r in rows if r["treatment"] == "CTX"]
    assert ctx_days.count(2) == 2
    assert 1 not in ctx_days
    assert _data()["ordered_trajectory_disposition"]["SCC6"].startswith("AMBIGUOUS")


def test_column_map_has_no_chi_outcome_dependency():
    data = _data()
    assert data["chi_bio_outcomes_opened"] is False
    assert data["processed_file_sha256"] == "c1318f5ad3b62d26c043de370cdca7300548337918f4543b13769bbe7a08a6c2"
