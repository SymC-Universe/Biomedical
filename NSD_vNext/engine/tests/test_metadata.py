import pytest

from nsd_engine import MetadataRole, MetadataRoleManifest, conservative_role_guess


def manifest():
    return MetadataRoleManifest(
        {
            "participant_id": MetadataRole.IDENTITY,
            "recording_condition": MetadataRole.RECORDING_STATE,
            "device": MetadataRole.ACQUISITION,
            "age": MetadataRole.DEMOGRAPHIC_COVARIATE,
            "group": MetadataRole.CLINICAL_LABEL,
            "ados_css": MetadataRole.CLINICAL_OUTCOME,
        }
    )


def test_engine_visible_columns_exclude_demographics_and_clinical_fields():
    roles = manifest()
    assert roles.engine_visible_columns() == (
        "participant_id",
        "recording_condition",
        "device",
    )
    assert roles.clinical_columns() == ("group", "ados_css")


def test_structural_engine_rejects_clinical_label_columns():
    roles = manifest()
    with pytest.raises(ValueError, match="downstream-only metadata"):
        roles.assert_engine_columns_allowed(["participant_id", "group"])


def test_structural_engine_rejects_unreviewed_columns():
    roles = manifest()
    with pytest.raises(ValueError, match="missing explicit metadata roles"):
        roles.assert_engine_columns_allowed(["participant_id", "mystery_column"])


def test_structural_engine_accepts_identity_and_recording_context():
    roles = manifest()
    roles.assert_engine_columns_allowed(["participant_id", "recording_condition", "device"])


def test_conservative_guess_does_not_auto_admit_unknown_fields():
    assert conservative_role_guess("group") is MetadataRole.CLINICAL_LABEL
    assert conservative_role_guess("diagnosis") is MetadataRole.CLINICAL_LABEL
    assert conservative_role_guess("age") is MetadataRole.DEMOGRAPHIC_COVARIATE
    assert conservative_role_guess("participant_id") is MetadataRole.IDENTITY
    assert conservative_role_guess("custom_metric") is MetadataRole.OTHER
