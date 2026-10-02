from nsd_engine.specparam_adapter import DescriptivePeak, SpecparamDescriptiveResult, SpecparamSettings
from nsd_engine.spectral_parameterization_qc import (
    ParameterizationFlag,
    compare_aperiodic_models,
    diagnose_parameterization,
)


def _result(mode="fixed", peaks=(), max_n_peaks=4):
    names = ("offset", "exponent") if mode == "fixed" else ("offset", "knee", "exponent")
    params = (1.0, 1.0) if mode == "fixed" else (1.0, 25.0, 2.0)
    return SpecparamDescriptiveResult(
        package_version="2.0.0rc7",
        settings=SpecparamSettings(
            aperiodic_mode=mode,
            peak_width_limits=(0.5, 12.0),
            max_n_peaks=max_n_peaks,
            min_peak_height=0.1,
            peak_threshold=2.5,
            fmin_hz=1.0,
            fmax_hz=45.0,
        ),
        aperiodic_parameters=params,
        aperiodic_parameter_names=names,
        peaks=tuple(peaks),
        metrics=(("error_mae", 0.01), ("gof_rsquared", 0.99)),
        frequency_resolution_hz=0.25,
        zero_peak_state=len(peaks) == 0,
    )


def test_diagnostics_expose_width_boundaries_and_max_count_without_auto_refusal():
    result = _result(
        peaks=(
            DescriptivePeak(8.0, 0.2, 0.5),
            DescriptivePeak(12.0, 0.3, 12.0),
        ),
        max_n_peaks=2,
    )
    diagnostics = diagnose_parameterization(result)

    assert diagnostics.lower_width_limit_hit_count == 1
    assert diagnostics.upper_width_limit_hit_count == 1
    assert diagnostics.max_peak_count_reached is True
    assert diagnostics.flags == (
        ParameterizationFlag.PEAK_AT_LOWER_WIDTH_LIMIT,
        ParameterizationFlag.PEAK_AT_UPPER_WIDTH_LIMIT,
        ParameterizationFlag.MAX_PEAK_COUNT_REACHED,
    )


def test_diagnostics_are_clean_for_interior_nonmaximal_peak_set():
    result = _result(peaks=(DescriptivePeak(10.0, 0.4, 2.0),), max_n_peaks=4)
    diagnostics = diagnose_parameterization(result)
    assert diagnostics.flags == ()
    assert diagnostics.has_boundary_hit is False


def test_aperiodic_model_comparison_flags_peak_count_and_location_disagreement():
    fixed = _result(
        mode="fixed",
        peaks=(
            DescriptivePeak(7.0, 0.3, 5.0),
            DescriptivePeak(16.0, 0.2, 12.0),
        ),
    )
    knee = _result(mode="knee", peaks=())

    comparison = compare_aperiodic_models(fixed, knee, center_tolerance_hz=1.0)
    assert comparison.matched_peak_count == 0
    assert comparison.unmatched_first_peak_count == 2
    assert comparison.unmatched_second_peak_count == 0
    assert ParameterizationFlag.APERIODIC_MODEL_PEAK_COUNT_DISAGREEMENT in comparison.flags
    assert ParameterizationFlag.APERIODIC_MODEL_PEAK_LOCATION_DISAGREEMENT in comparison.flags


def test_aperiodic_model_comparison_matches_nearby_peaks_without_false_flag():
    fixed = _result(mode="fixed", peaks=(DescriptivePeak(10.0, 0.4, 2.0),))
    knee = _result(mode="knee", peaks=(DescriptivePeak(10.4, 0.35, 2.1),))

    comparison = compare_aperiodic_models(fixed, knee, center_tolerance_hz=0.5)
    assert comparison.matched_peak_count == 1
    assert comparison.flags == ()
