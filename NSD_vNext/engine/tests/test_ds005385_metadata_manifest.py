import json
from pathlib import Path

from nsd_engine.metadata import MetadataRole, MetadataRoleManifest


MANIFEST_PATH = (
    Path(__file__).resolve().parents[2]
    / "docs"
    / "manifests"
    / "ds005385_metadata_roles_v0.1.json"
)


def _load():
    payload = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    roles = {name: MetadataRole(value) for name, value in payload["roles"].items()}
    return payload, MetadataRoleManifest(roles=roles)


def test_ds005385_role_manifest_is_explicit():
    payload, manifest = _load()
    assert payload["dataset"] == "ds005385"
    assert payload["status"] == "D3_METADATA_ROLE_AND_JOIN_CONTRACT_FROZEN"
    assert len(manifest.roles) == 8
    assert manifest.engine_visible_columns() == ("participant_id",)


def test_ds005385_participant_metadata_cannot_enter_structural_engine():
    payload, manifest = _load()
    manifest.assert_engine_columns_allowed(payload["structural_engine_participant_columns"])

    for prohibited in ("age", "sex", "handedness", "late_ses1", "late_ses2"):
        try:
            manifest.assert_engine_columns_allowed(["participant_id", prohibited])
        except ValueError as exc:
            assert "downstream-only metadata" in str(exc)
        else:
            raise AssertionError(f"{prohibited} should be downstream-only")


def test_ds005385_late_trigger_fields_are_quality_bookkeeping_not_features():
    payload, manifest = _load()
    assert manifest.roles["late_ses1"] is MetadataRole.OTHER
    assert manifest.roles["late_ses2"] is MetadataRole.OTHER
    assert payload["quality_firewall"]["late_trigger_counts_are_signal_features"] is False
    assert payload["quality_firewall"]["late_trigger_counts_may_tune_modal_thresholds"] is False


def test_ds005385_join_invariants_match_frozen_d2():
    payload, _ = _load()
    join = payload["join_contract"]
    assert join["expected_participant_rows"] == 608
    assert join["expected_bids_subjects"] == 608
    assert join["expected_subject_mismatches"] == 0
    assert join["expected_sessions"] == 816
    assert join["expected_repeat_subjects"] == 208
    assert join["silent_first_match_allowed"] is False
