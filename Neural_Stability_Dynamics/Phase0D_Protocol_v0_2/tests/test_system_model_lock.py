import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _git_blob_sha(path: Path) -> str:
    content = path.read_bytes()
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()


def test_system_model_lock_is_architecture_frozen_and_p1_closed():
    data = json.loads((ROOT / "registries" / "SYSTEM_MODEL_LOCK.json").read_text(encoding="utf-8"))
    assert data["status"] == "ARCHITECTURE_FROZEN_P0"
    assert data["system_model_version"] == "1.0"
    assert data["current_implementation_status"]["P1"] == "CLOSED"


def test_locked_system_model_content_matches_canonical_blob_identity():
    data = json.loads((ROOT / "registries" / "SYSTEM_MODEL_LOCK.json").read_text(encoding="utf-8"))
    assert _git_blob_sha(ROOT / data["canonical_definition"]) == data["canonical_definition_git_blob_sha"]


def test_system_model_has_all_four_frozen_views():
    data = json.loads((ROOT / "registries" / "SYSTEM_MODEL_LOCK.json").read_text(encoding="utf-8"))
    assert data["frozen_objects"]["views"] == [
        "SCALAR_SPECTRAL",
        "MODAL_CARRIER",
        "CONGLOMERATE_SYSTEM",
        "OPEN_CHANNEL",
    ]


def test_chi_is_withheld_not_mandatory():
    data = json.loads((ROOT / "registries" / "SYSTEM_MODEL_LOCK.json").read_text(encoding="utf-8"))
    assert data["frozen_objects"]["chi_policy"].startswith("WITHHELD_UNLESS")
    text = (ROOT / "SYSTEM_MODEL.md").read_text(encoding="utf-8")
    assert "`chi` is **WITHHELD by default**" in text
    assert "whole-system scalar is not part" in text


def test_atlas_is_external_to_engine_rule_construction():
    data = json.loads((ROOT / "registries" / "SYSTEM_MODEL_LOCK.json").read_text(encoding="utf-8"))
    assert "EXTERNAL_READ_ONLY" in data["frozen_objects"]["atlas_policy"]


def test_thresholds_are_explicitly_outside_architecture_lock():
    data = json.loads((ROOT / "registries" / "SYSTEM_MODEL_LOCK.json").read_text(encoding="utf-8"))
    mutable = set(data["mutable_without_system_model_version_change"])
    assert "numeric_thresholds" in mutable
    assert "uncertainty_propagation_method_and_confidence_convention" in mutable
    assert "P1_design_and_seeds" in mutable
