from pathlib import Path
import importlib.util


def _load():
    path = Path(__file__).resolve().parents[1] / "tools" / "verify_v02_cd05_profile.py"
    spec = importlib.util.spec_from_file_location("v02_cd05_profile", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_cd05_profile_reproduction_contract():
    out = _load().verify()
    assert out["status"] == "PASS"
    assert out["mechanical_probe_only"] is True
    assert out["truth_parameter_used_in_profile_interface"] is False
    assert out["scientific_adjudication"] == "NOT_PERFORMED_BY_GITHUB"
