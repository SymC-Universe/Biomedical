import json
from pathlib import Path

from src import probe_stage_b2_sources as probe


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


def test_metadata_probe_uses_data_endpoint_head_without_download(monkeypatch):
    class Headers(dict):
        def items(self):
            return super().items()

    class Response:
        status = 200
        headers = Headers({
            "Content-Length": "123456",
            "Content-Type": "application/octet-stream",
            "Content-Disposition": "attachment; filename=test.tsv",
        })
        def __enter__(self): return self
        def __exit__(self, *args): return False

    seen = {}
    def fake_urlopen(req, timeout=0):
        seen["method"] = req.get_method()
        seen["url"] = req.full_url
        return Response()

    monkeypatch.setattr(probe.urllib.request, "urlopen", fake_urlopen)
    out = probe.probe_data_endpoint("https://api.gdc.cancer.gov/data/example")
    assert seen["method"] == "HEAD"
    assert "/data/example" in seen["url"]
    assert out["metadata_status"] == "OK_DATA_ENDPOINT_HEAD"
    assert out["content_length"] == 123456
