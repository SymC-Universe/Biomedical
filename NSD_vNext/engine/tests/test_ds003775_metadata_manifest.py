import json
from pathlib import Path

from nsd_engine.metadata import MetadataRole, MetadataRoleManifest


MANIFEST_PATH = (
    Path(__file__).resolve().parents[2]
    / "docs"
    / "manifests"
    / "ds003775_metadata_roles_v0.1.json"
)


def _load_manifest():
    payload = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    roles = {name: MetadataRole(value) for name, value in payload["roles"].items()}
    return payload, MetadataRoleManifest(roles=roles)


def test_ds003775_manifest_is_parseable_and_explicit():
    payload, manifest = _load_manifest()

    assert payload["dataset"] == "ds003775"
    assert payload["status"] == "D3_ROLE_MAP_FROZEN_JOIN_AUDIT_PENDING"
    assert set(manifest.roles) == set(payload["roles"])
    assert len(manifest.roles) == 24


def test_ds003775_engine_sees_only_subject_identity_from_participants_table():
    payload, manifest = _load_manifest()

    assert manifest.engine_visible_columns() == ("participant_id",)
    manifest.assert_engine_columns_allowed(payload["structural_engine_participant_columns"])


def test_ds003775_demographics_and_cognitive_outcomes_are_downstream_only():
    payload, manifest = _load_manifest()

    downstream = set(manifest.downstream_only_columns())
    assert downstream == set(payload["downstream_only_participant_columns"])
    assert manifest.roles["age"] is MetadataRole.DEMOGRAPHIC_COVARIATE
    assert manifest.roles["sex"] is MetadataRole.DEMOGRAPHIC_COVARIATE
    assert manifest.roles["ravlt_tot"] is MetadataRole.CLINICAL_OUTCOME
    assert manifest.roles["ds_tot"] is MetadataRole.CLINICAL_OUTCOME
    assert manifest.roles["vf_3"] is MetadataRole.CLINICAL_OUTCOME


def test_ds003775_manifest_rejects_outcome_leakage_into_structural_engine():
    _, manifest = _load_manifest()

    try:
        manifest.assert_engine_columns_allowed(["participant_id", "ravlt_tot"])
    except ValueError as exc:
        assert "downstream-only metadata" in str(exc)
    else:
        raise AssertionError("clinical outcome leakage should have been rejected")
