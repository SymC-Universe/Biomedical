import pytest

from nsd_engine import CandidateMode, ModalEstimateBatch


def test_modal_batch_accepts_matching_method_lineage():
    batch = ModalEstimateBatch(
        method_name="dmd_fixture",
        method_version="0.0",
        modes=(
            CandidateMode(
                mode_id="m1",
                source_method="dmd_fixture",
                frequency_hz=10.0,
                pole_real_per_s=-1.0,
                pole_imag_rad_s=62.0,
                identifiable=False,
            ),
        ),
        diagnostics={"note": "interface fixture only"},
        qualified_for_scalar_admission=False,
    )
    assert batch.method_name == "dmd_fixture"
    assert not batch.qualified_for_scalar_admission


def test_modal_batch_rejects_method_lineage_mismatch():
    with pytest.raises(ValueError, match="does not match batch method"):
        ModalEstimateBatch(
            method_name="oma_fixture",
            method_version="0.0",
            modes=(CandidateMode("m1", "different_method", 10.0),),
            diagnostics={},
        )


def test_modal_batch_rejects_duplicate_mode_ids():
    with pytest.raises(ValueError, match="mode_id values must be unique"):
        ModalEstimateBatch(
            method_name="state_space_fixture",
            method_version="0.0",
            modes=(
                CandidateMode("m1", "state_space_fixture", 8.0),
                CandidateMode("m1", "state_space_fixture", 12.0),
            ),
            diagnostics={},
        )
