import math

import pytest

from nsd_engine.qc import QCThresholds, evaluate_signal_qc


def test_qc_reports_metrics_without_hidden_thresholds():
    report = evaluate_signal_qc(
        {
            "C3": [0.0, 1.0, 0.0, -1.0],
            "C4": [0.0, 0.5, 0.0, -0.5],
        },
        2.0,
    )
    assert report.signal_qc.duration_seconds == 2.0
    assert report.signal_qc.usable_duration_seconds == 2.0
    assert report.signal_qc.passed_signal_integrity is True
    assert report.signal_qc.flags == ()
    assert len(report.channels) == 2


def test_qc_flags_flat_channel_only_when_frozen_rule_requires_it():
    channels = {
        "good": [0.0, 1.0, 0.0, -1.0],
        "flat": [2.0, 2.0, 2.0, 2.0],
    }

    descriptive = evaluate_signal_qc(channels, 4.0)
    assert descriptive.signal_qc.passed_signal_integrity is True
    flat = next(item for item in descriptive.channels if item.channel_name == "flat")
    assert flat.flat is True

    governed = evaluate_signal_qc(
        channels,
        4.0,
        thresholds=QCThresholds(max_flat_channels=0),
    )
    assert governed.signal_qc.passed_signal_integrity is False
    assert "QC_TOO_MANY_FLAT_CHANNELS" in governed.signal_qc.flags


def test_qc_missingness_is_measured_and_can_be_gated():
    channels = {
        "C3": [0.0, 1.0, math.nan, -1.0],
        "C4": [0.0, 0.5, 0.0, -0.5],
    }
    report = evaluate_signal_qc(
        channels,
        4.0,
        thresholds=QCThresholds(max_missing_fraction_per_channel=0.2),
    )
    assert report.signal_qc.passed_signal_integrity is False
    assert "QC_EXCESS_MISSINGNESS" in report.signal_qc.flags
    assert report.signal_qc.usable_duration_seconds == pytest.approx(0.75)


def test_qc_extreme_occupancy_is_indicator_not_proof_of_clipping():
    channels = {"Cz": [-1.0, -1.0, 0.0, 1.0, 1.0]}
    descriptive = evaluate_signal_qc(channels, 5.0)
    channel = descriptive.channels[0]
    assert channel.edge_fraction == pytest.approx(0.8)
    assert descriptive.signal_qc.passed_signal_integrity is True

    governed = evaluate_signal_qc(
        channels,
        5.0,
        thresholds=QCThresholds(max_edge_fraction_per_channel=0.5),
    )
    assert "QC_EXCESS_EXTREME_OCCUPANCY" in governed.signal_qc.flags


def test_qc_rejects_mismatched_channel_lengths():
    with pytest.raises(ValueError, match="same sample count"):
        evaluate_signal_qc({"C3": [0.0, 1.0], "C4": [0.0]}, 100.0)


def test_qc_all_nonfinite_channel_fails_without_extra_threshold():
    report = evaluate_signal_qc(
        {"C3": [math.nan, math.inf], "C4": [0.0, 1.0]},
        2.0,
    )
    assert report.signal_qc.passed_signal_integrity is False
    assert "QC_CHANNEL_NO_FINITE_DATA" in report.signal_qc.flags
    assert report.signal_qc.usable_duration_seconds == 0.0
