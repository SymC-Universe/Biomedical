from src.derive_external_geo_identity_tables import (
    canonical_breast_state,
    normalize_melanoma_state,
    melanoma_title_record,
)


def test_breast_state_normalization():
    assert canonical_breast_state("primary tumor") == "PRIMARY"
    assert canonical_breast_state("lymph node metastasis") == "METASTASIS"


def test_melanoma_state_normalization():
    assert normalize_melanoma_state("baseline2") == "BASELINE"
    assert normalize_melanoma_state("DD-DP1") == "DDP1"
    assert normalize_melanoma_state("DP3") == "DP3"


def test_melanoma_patient_conflict_is_quarantined():
    sample = {
        "gsm": "GSMX",
        "title": "Pt22-DDP1",
        "description": "Patient 21 melanoma, post BRAFi+MEKi resistance, 1st biopsy",
        "characteristics": [
            {"tag": "mapki sensitivity", "value": "resistant"},
            {"tag": "mapki treatment", "value": "BRAFi+MEKi"},
        ],
    }
    record = melanoma_title_record(sample, modality="rna_seq")
    assert record["patient_id_from_title"] == 22
    assert record["patient_id_from_description"] == 21
    assert record["identity_anomaly"] == "TITLE_DESCRIPTION_PATIENT_CONFLICT"
