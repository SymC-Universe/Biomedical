from pathlib import Path
import importlib.util


def _load_module():
    path = Path(__file__).resolve().parents[1] / "src" / "stage_d_acquisition_inventory.py"
    spec = importlib.util.spec_from_file_location("stage_d_acquisition_inventory", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_geo_bucket_mapping():
    m = _load_module()
    assert m._series_bucket("GSE216989") == "GSE216nnn"
    assert m._series_bucket("GSE20945") == "GSE20nnn"
    assert m._series_bucket("GSE231780") == "GSE231nnn"
    assert m._series_bucket("GSE91071") == "GSE91nnn"


def test_geo_metadata_url_is_brief_only():
    m = _load_module()
    series_url = m._geo_metadata_url("GSE216989", "self")
    samples_url = m._geo_metadata_url("GSE216989", "gsm")
    assert "view=brief" in series_url
    assert "view=brief" in samples_url
    assert "form=text" in series_url
    assert "form=text" in samples_url
    assert "targ=self" in series_url
    assert "targ=gsm" in samples_url
    for url in (series_url, samples_url):
        assert "view=full" not in url
        assert "view=data" not in url
        assert "view=quick" not in url


def test_soft_parser_minimal(tmp_path):
    m = _load_module()
    text = """^SERIES = GSE1\n!Series_title = Demo\n^SAMPLE = GSM1\n!Sample_title = Control\n!Sample_characteristics_ch1 = treatment: vehicle\n!Sample_characteristics_ch1 = time: day 0\n!Sample_platform_id = GPL1\n^DATABASE = GeoMiame\n"""
    p = tmp_path / "demo.soft"
    p.write_text(text, encoding="utf-8")
    series, samples = m.parse_soft(p)
    assert series["geo_accession"] == "GSE1"
    assert series["Series_title"] == "Demo"
    assert len(samples) == 1
    assert samples[0]["geo_accession"] == "GSM1"
    assert samples[0]["Sample_title"] == "Control"
    assert samples[0]["Sample_characteristics_ch1"] == ["treatment: vehicle", "time: day 0"]
