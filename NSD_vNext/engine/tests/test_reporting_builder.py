from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


_BUILDER = (
    Path(__file__).resolve().parents[2]
    / "reporting"
    / "build_research_structure_report.py"
)
_SPEC = importlib.util.spec_from_file_location("nsd_reporting_builder", _BUILDER)
assert _SPEC is not None and _SPEC.loader is not None
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)


def _d4():
    return {
        "passed": True,
        "subject_id": "sub-001",
        "dataset": "ds-test",
        "task": "rest",
        "source_release": {"release": "pinned"},
        "recordings": [
            {
                "session_id": "ses-a",
                "passed": True,
                "acquisition_time": "2026-01-01T00:00:00",
                "actual_md5": "abc",
                "header": {
                    "signal_count": 2,
                    "unique_sampling_rates_hz": [256.0],
                    "recording_duration_seconds": 60.0,
                },
            }
        ],
    }


def _specparam():
    return {
        "subject_id": "sub-001",
        "frozen_candidate": {"model": "descriptive"},
        "sessions": [
            {
                "session_id": "ses-a",
                "summary": {
                    "channel_count": 2,
                    "fixed_mean_peak_count": 0.5,
                    "fixed_zero_peak_channel_fraction": 0.5,
                    "aperiodic_model_disagreement_channel_count": 1,
                    "aperiodic_model_disagreement_channel_fraction": 0.5,
                    "fixed_max_peak_count_channel_count": 0,
                    "fixed_total_width_boundary_hits": 0,
                },
                "channels": [
                    {
                        "channel": "Cz",
                        "frozen_fixed": {
                            "aperiodic_parameter_names": [
                                "offset",
                                "exponent",
                            ],
                            "aperiodic_parameters": [0.1, 1.2],
                            "peak_count": 1,
                            "peaks": [
                                {
                                    "center_frequency_hz": 10.0,
                                    "power_above_aperiodic_log10": 0.5,
                                    "descriptive_bandwidth_hz": 2.0,
                                }
                            ],
                        },
                    },
                    {
                        "channel": "Pz",
                        "frozen_fixed": {
                            "aperiodic_parameter_names": [
                                "offset",
                                "exponent",
                            ],
                            "aperiodic_parameters": [0.2, 1.4],
                            "peak_count": 0,
                            "peaks": [],
                        },
                    },
                ],
            }
        ],
    }


def _atlas_manifest():
    return {
        "atlas_version": "atlas-p0d-test",
        "maturity": "ATLAS_P0_D",
        "reference_family_independence": [
            {
                "independence_grade": (
                    "NON_INDEPENDENT_FOR_ENGINE_VALIDATION"
                )
            }
        ],
    }


def _atlas_reference():
    return {
        "dataset": "ds-test",
        "population": {
            "channelwise_aperiodic_exponent_icc_a1": {"median": 0.65},
            "channelwise_peak_count_exact_agreement_fraction": {
                "median": 0.50
            },
            "channelwise_zero_peak_state_exact_agreement_fraction": {
                "median": 0.90
            },
        },
    }


def test_research_report_builder_cannot_emit_clinical_results():
    report = _MODULE.build_report(
        d4=_d4(),
        spec=_specparam(),
        atlas_manifest=_atlas_manifest(),
        atlas_reference=_atlas_reference(),
        session_id="ses-a",
        engine_version="test-engine",
    )

    assert report["report_maturity"] == "RESEARCH_STRUCTURE_ONLY"
    assert report["clinical_models_run"] == []
    assert report["forecasts"] == []
    assert report["atlas_deviations"] == []
    assert report["out_of_domain_status"] == "NOT_EVALUATED"
    assert report["signal_quality_status"] == "PARTIALLY_USABLE"

    spectral = report["structural_profile"]["spectral_state"]
    assert spectral["dynamical_interpretation"] == "PROHIBITED"
    assert spectral["first_listed_peak_descriptive_bandwidth_hz"]["median"] == 2.0
    assert report["structural_profile"]["licensed_local_scalars"] == []

    refusal_codes = {item["code"] for item in report["refusals"]}
    assert "REF_REFERENCE_DEVIATION_NOT_QUALIFIED" in refusal_codes
    assert "REF_MODAL_ROUTE_NOT_QUALIFIED" in refusal_codes
    assert "REF_FULL_QC_NOT_RUN" in refusal_codes


def test_research_report_builder_requires_d4_pass():
    d4 = _d4()
    d4["passed"] = False
    with pytest.raises(ValueError, match="D4"):
        _MODULE.build_report(
            d4=d4,
            spec=_specparam(),
            atlas_manifest=_atlas_manifest(),
            atlas_reference=_atlas_reference(),
            session_id="ses-a",
            engine_version="test-engine",
        )


def test_research_report_builder_rejects_subject_mismatch():
    spec = _specparam()
    spec["subject_id"] = "sub-other"
    with pytest.raises(ValueError, match="subject mismatch"):
        _MODULE.build_report(
            d4=_d4(),
            spec=spec,
            atlas_manifest=_atlas_manifest(),
            atlas_reference=_atlas_reference(),
            session_id="ses-a",
            engine_version="test-engine",
        )
