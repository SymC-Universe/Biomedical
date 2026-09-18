from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


_TOOL = Path(__file__).resolve().parents[1] / "tools" / "aggregate_ds003775_repeat_population.py"
_SPEC = importlib.util.spec_from_file_location("repeat_population_aggregate", _TOOL)
assert _SPEC is not None and _SPEC.loader is not None
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)


def test_icc_a1_absolute_agreement_is_one_for_identical_repeats():
    pairs = [[1.0, 1.0], [2.0, 2.0], [3.0, 3.0], [4.0, 4.0]]
    assert _MODULE._icc_a1(pairs) == pytest.approx(1.0)


def test_icc_a1_penalizes_constant_session_offset():
    pairs = [[1.0, 2.0], [2.0, 3.0], [3.0, 4.0], [4.0, 5.0]]
    assert _MODULE._icc_a1(pairs) == pytest.approx(10.0 / 13.0)


def _session(session_id: str, exponent: float, peak_count: int, zero_peak: bool):
    return {
        "session_id": session_id,
        "summary": {
            "channel_count": 1,
            "aperiodic_model_disagreement_channel_fraction": 0.0,
            "fixed_max_peak_count_channel_count": int(peak_count == 3),
            "fixed_zero_peak_channel_fraction": float(zero_peak),
            "fixed_total_width_boundary_hits": 0,
        },
        "channels": [
            {
                "channel": "Cz",
                "frozen_fixed": {
                    "aperiodic_parameter_names": ["offset", "exponent"],
                    "aperiodic_parameters": [0.0, exponent],
                    "peak_count": peak_count,
                    "zero_peak_state": zero_peak,
                },
            }
        ],
    }


def _spec(subject: str, first: float, second: float, first_count: int, second_count: int):
    return {
        "subject_id": subject,
        "repeat_summary": {
            "aperiodic_exponent_absolute_difference": {
                "median": abs(first - second)
            },
            "same_peak_count_fraction": float(first_count == second_count),
            "same_zero_peak_state_fraction": 1.0,
            "first_listed_peak_nearest_center_difference_hz": {"median": 0.1},
        },
        "sessions": [
            _session("ses-t1", first, first_count, False),
            _session("ses-t2", second, second_count, False),
        ],
    }


def _psd(subject: str):
    return {
        "subject_id": subject,
        "repeat_comparison": {
            "global_median_psd_correlation": 0.95,
            "channel_correlation_median": 0.90,
            "channel_correlation_minimum": 0.80,
        },
    }


def test_aggregate_keeps_subject_hierarchy_and_computes_channel_repeatability(tmp_path):
    values = [
        ("sub-001", 1.0, 2.0, 1, 1),
        ("sub-002", 2.0, 3.0, 1, 2),
        ("sub-003", 3.0, 4.0, 2, 2),
        ("sub-004", 4.0, 5.0, 2, 3),
    ]
    for subject, first, second, first_count, second_count in values:
        (tmp_path / f"{subject}_specparam.json").write_text(
            json.dumps(_spec(subject, first, second, first_count, second_count)),
            encoding="utf-8",
        )
        (tmp_path / f"{subject}_psd.json").write_text(
            json.dumps(_psd(subject)),
            encoding="utf-8",
        )
        (tmp_path / f"{subject}_d4.json").write_text(
            json.dumps({"subject_id": subject}),
            encoding="utf-8",
        )

    result = _MODULE.aggregate(tmp_path, expected_subject_count=4)

    assert result["subject_count"] == 4
    assert result["d4_subject_count_recoverable_from_reports"] == 4
    assert len(result["channel_repeatability"]) == 1

    channel = result["channel_repeatability"][0]
    assert channel["channel"] == "Cz"
    assert channel["subject_pair_count"] == 4
    assert channel["aperiodic_exponent_icc_a1"] == pytest.approx(10.0 / 13.0)
    assert channel["peak_count_exact_agreement_fraction"] == pytest.approx(0.5)
    assert channel["zero_peak_state_exact_agreement_fraction"] == pytest.approx(1.0)

    population = result["population"]
    assert population["channelwise_aperiodic_exponent_icc_a1"]["n"] == 1
    assert population["channelwise_peak_count_exact_agreement_fraction"]["median"] == pytest.approx(0.5)
    assert population["channelwise_zero_peak_state_exact_agreement_fraction"]["median"] == pytest.approx(1.0)
