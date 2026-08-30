import json
from pathlib import Path


def test_b2_sources_are_prereserved_and_no_chi():
    p = json.loads((Path(__file__).parents[1] / "config" / "stage_b2_source_plan.json").read_text())
    assert p["constraints"]["chi_allowed"] is False
    assert p["constraints"]["cv2_used"] is False
    assert p["constraints"]["source_selection_from_stage_a_or_b1_outcomes_allowed"] is False
    ids = {s["id"] for s in p["sources"] if s["download_now"]}
    assert ids == {"aneuploidy_loh", "cnv_burden", "rppa_final"}


def test_methylation_is_metadata_only_initially():
    p = json.loads((Path(__file__).parents[1] / "config" / "stage_b2_source_plan.json").read_text())
    methylation = [s for s in p["sources"] if "methylation" in s["id"]]
    assert methylation
    assert all(s["download_now"] is False for s in methylation)
