from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.validate_atlas import (
    declared_coordinate_ids,
    load_json,
    validate_entry,
)


def _prov(source_location, extraction_method, code_version="A2_SRM_CSD_SVD_v0.1"):
    return {
        "source_location": source_location,
        "extraction_method": extraction_method,
        "code_version": code_version,
    }


def _independence(kind: str):
    temporal_reason = (
        "P0-D Atlas pilot evidence is visible before any later scoring/adjudication rule is frozen; "
        "it cannot independently confirm a rule developed from this pilot."
    )
    if kind == "session":
        data_reason = (
            "SRM recordings were not used in the current synthetic Structural-Engine development, "
            "but a future Engine comparison on the same recordings would share the data pathway."
        )
    else:
        data_reason = (
            "The t1/t2 comparison uses the same frozen participant pair on both Atlas coordinates; "
            "it is independent of current synthetic Engine development but not a separate-data validation "
            "of an Engine result on these same recordings."
        )
    return {
        "data": {"grade": "PARTIALLY_INDEPENDENT", "reason": data_reason},
        "cohort_system": {"grade": "PARTIALLY_INDEPENDENT", "reason": "SRM is external to current synthetic Engine development, but paired Atlas comparisons reuse the same source cohort/system."},
        "outcome_label": {"grade": "INDEPENDENT", "reason": "No diagnosis, phenotype, cognitive score, age, sex, or desired state label entered subject selection or CSD-SVD reconstruction."},
        "parameter_tuning": {"grade": "INDEPENDENT", "reason": "Subject roster, frequency grid, reconstruction method, split rule, and no-threshold policy were frozen before EEG value inspection."},
        "method_estimator": {"grade": "INDEPENDENT", "reason": "Atlas CSD-SVD reconstruction does not import SSI-COV, Subspace DMD, or the NSD Structural Engine."},
        "atlas_engine": {"grade": "INDEPENDENT", "reason": "No Structural-Engine output or target value entered Atlas reconstruction; engine_selector_eligible is false."},
        "source_literature": {"grade": "PARTIALLY_INDEPENDENT", "reason": "The source publication/sidecars define acquisition and preprocessing context; numerical Atlas coordinates are reconstructed from pinned derivative bytes rather than copied from a reported effect."},
        "temporal_decisive_evidence": {"grade": "NON_INDEPENDENT_FOR_ENGINE_VALIDATION", "reason": temporal_reason},
    }


def _base(entry_id, source_id, context, native_model, kind):
    return {
        "atlas_entry_id": entry_id,
        "source_id": source_id,
        "research_role": "NOMINAL_FUNCTION",
        "evidence_tier": "A_FULL_NUMERIC_PROVENANCE",
        "native_model": native_model,
        "context": context,
        "coordinates": [],
        "chi": {
            "status": "CHI_WITHHELD_NO_SECOND_ORDER_LICENSE",
            "value": None,
            "derivation": None,
            "frequency_semantics": None,
            "uncertainty": None,
        },
        "independence": _independence(kind),
        "scope": "SUPPORTED_IN_TESTED_REGIME",
        "engine_selector_eligible": False,
        "function_limit_state": "NOT_YET_ASSIGNED",
        "notes": "Atlas coordinate record only. No healthy-range, Engine-validation, or chi claim is implied.",
    }


def _session_entry(result, summary):
    prefix = summary["array_key_prefix"]
    arrays = result["arrays_file"]
    source_loc = f"{summary['subject']} {summary['session']} source-cleaned derivative; byte SHA256 {summary['input_set_sha256']}"
    native_model = {
        "name": "Observational cross-spectral density matrix SVD / spectral principal decomposition",
        "source_symbols_preserved": True,
        "equations_or_reference": result["method_spec"],
        "assumptions": [
            "Source-provided cleaned epochs are analyzed without additional Atlas filtering/rereferencing/channel rejection.",
            "CSD singular vectors are observational spectral principal directions, not asserted physical eigenmodes.",
            "No damping, pole-real-part, second-order, or chi interpretation is licensed in this lane.",
        ],
    }
    context = {
        "modality": "EEG",
        "species_population": "healthy human control participant in SRM source",
        "recording_state_task": "eyes-closed resting state",
        "perturbation_intervention": None,
        "sampling_rate_hz": summary["sampling_frequency_hz"],
        "duration_s": "source nominal 240 s before source cleaning; retained cleaned epoch count recorded separately",
        "channel_sensor_count": summary["n_channels"],
        "montage": "source 64-channel BioSemi / source derivative channel basis",
        "preprocessing": {
            "input_layer": "source-provided cleaned_epochs derivative",
            "source_reference": summary["source_reference"],
            "source_filters": summary["source_software_filters"],
            "retained_epochs": summary["n_epochs"],
            "source_bad_interpolated_channels": summary["source_bad_interpolated_channels"],
            "atlas_additional_filtering": "none",
        },
    }
    e = _base(
        f"SRM-{summary['subject']}-{summary['session']}-CSD-SVD",
        result["source_id"], context, native_model, "session"
    )
    e["coordinates"] = [
        {
            "coordinate_id": "frequency_hz",
            "eligibility_status": "DERIVED_EXACT",
            "value": {"artifact": arrays, "array_key": f"{prefix}__frequency_hz", "grid": result["frequency_grid"]},
            "unit": "Hz",
            "uncertainty": None,
            "derivation": "exact rFFT frequency bins from frozen 4-second epochs at 1024 Hz",
            "provenance": _prov(source_loc, "frozen FFT grid"),
        },
        {
            "coordinate_id": "observable_strength_descriptor",
            "eligibility_status": "NATIVE_RECONSTRUCTED_FROM_PINNED_DERIVATIVE",
            "value": {
                "artifact": arrays,
                "singular_values_key": f"{prefix}__singular_values_first4",
                "singular_shares_key": f"{prefix}__singular_shares_first4",
                "trace_power_key": f"{prefix}__trace_power",
            },
            "unit": "cross-spectral density / dimensionless share",
            "uncertainty": {"split_half": summary["split_half"]},
            "derivation": None,
            "provenance": _prov(source_loc, "observational CSD-SVD"),
        },
        {
            "coordinate_id": "carrier_representation_type",
            "eligibility_status": "NATIVE_RECONSTRUCTED_FROM_PINNED_DERIVATIVE",
            "value": "LEADING_CSD_SPECTRAL_PRINCIPAL_DIRECTION_PER_FREQUENCY",
            "unit": None,
            "uncertainty": None,
            "derivation": None,
            "provenance": _prov(source_loc, "observational CSD-SVD"),
        },
        {
            "coordinate_id": "carrier_vector_or_reference",
            "eligibility_status": "NATIVE_RECONSTRUCTED_FROM_PINNED_DERIVATIVE",
            "value": {"artifact": arrays, "u1_key": f"{prefix}__u1", "u2_key": f"{prefix}__u2"},
            "unit": "unit-norm complex spectral direction",
            "uncertainty": {"split_half": summary["split_half"]},
            "derivation": None,
            "provenance": _prov(source_loc, "Hermitian CSD eigendecomposition"),
        },
        {
            "coordinate_id": "channel_participation_vector",
            "eligibility_status": "NATIVE_RECONSTRUCTED_FROM_PINNED_DERIVATIVE",
            "value": {"artifact": arrays, "array_key": f"{prefix}__participation_u1"},
            "unit": "normalized fraction vector",
            "uncertainty": {"split_half": summary["split_half"]},
            "derivation": "abs(u1)^2 normalized to unit sum",
            "provenance": _prov(source_loc, "CSD-SVD leading-carrier participation"),
        },
        {
            "coordinate_id": "uncertainty_status",
            "eligibility_status": "DERIVED_EXACT",
            "value": "PARTIAL",
            "unit": None,
            "uncertainty": {"split_half": summary["split_half"]},
            "derivation": "split-half repeatability mapped; no calibrated sampling interval",
            "provenance": _prov(source_loc, "predeclared odd/even source-epoch split"),
        },
    ]
    return e


def _pair_entry(result, pair):
    prefix = pair["array_key_prefix"]
    arrays = result["arrays_file"]
    source_loc = f"{pair['subject']} ses-t1 versus ses-t2 CSD-SVD comparison; exact elapsed-time axis withheld"
    native_model = {
        "name": "Paired observational CSD-SVD coordinate comparison",
        "source_symbols_preserved": True,
        "equations_or_reference": result["method_spec"],
        "assumptions": [
            "t1 and t2 use the same source-declared 64-channel basis.",
            "Frequency bins are compared exactly without peak shifting.",
            "Exact elapsed time is not used because source timestamps are not fully reconciled.",
        ],
    }
    context = {
        "modality": "EEG",
        "species_population": "healthy human control participant in SRM repeat-session subset",
        "recording_state_task": "eyes-closed resting state test-retest",
        "perturbation_intervention": "source-defined repeat session; exact elapsed-time coordinate withheld",
        "sampling_rate_hz": 1024,
        "duration_s": "source nominal 240 s per recording before source cleaning",
        "channel_sensor_count": 64,
        "montage": "matched source derivative channel basis",
        "preprocessing": "source-provided cleaned_epochs derivative; no additional Atlas filtering/rereferencing/channel rejection",
    }
    e = _base(f"SRM-{pair['subject']}-T1-T2-CSD-SVD", result["source_id"], context, native_model, "pair")
    e["coordinates"] = [
        {
            "coordinate_id": "MAC",
            "eligibility_status": "DERIVED_EXACT",
            "value": {"artifact": arrays, "array_key": f"{prefix}__leading_carrier_MAC_per_frequency", "median": pair["median_leading_carrier_MAC"]},
            "unit": "dimensionless",
            "uncertainty": None,
            "derivation": "squared magnitude inner product of unit leading CSD spectral directions at matched frequency bins",
            "provenance": _prov(source_loc, "paired CSD-SVD carrier comparison"),
        },
        {
            "coordinate_id": "subspace_similarity",
            "eligibility_status": "DERIVED_EXACT",
            "value": {"artifact": arrays, "array_key": f"{prefix}__two_dimensional_subspace_similarity_per_frequency", "median": pair["median_two_dimensional_subspace_similarity"]},
            "unit": "dimensionless",
            "uncertainty": None,
            "derivation": "mean squared singular value of Q_t1^H Q_t2 for the leading two-dimensional CSD subspaces",
            "provenance": _prov(source_loc, "paired CSD-SVD subspace comparison"),
        },
        {
            "coordinate_id": "participation_distance",
            "eligibility_status": "DERIVED_EXACT",
            "value": {"artifact": arrays, "array_key": f"{prefix}__participation_total_variation_per_frequency", "median": pair["median_participation_total_variation"]},
            "unit": "dimensionless total-variation distance",
            "uncertainty": None,
            "derivation": "0.5*sum(abs(p_t1-p_t2)) at matched frequency bins",
            "provenance": _prov(source_loc, "paired leading-carrier participation comparison"),
        },
        {
            "coordinate_id": "uncertainty_status",
            "eligibility_status": "DERIVED_EXACT",
            "value": "PARTIAL",
            "unit": None,
            "uncertainty": {
                "leading_share_curve_correlation": pair["leading_share_curve_correlation"],
                "log_total_cross_spectral_power_curve_correlation": pair["log_total_cross_spectral_power_curve_correlation"],
            },
            "derivation": "repeat-session variability mapped without a calibrated interval or pass threshold",
            "provenance": _prov(source_loc, "source-defined t1/t2 repeat comparison"),
        },
    ]
    return e


def build(result_path: Path, output_dir: Path):
    result = json.loads(result_path.read_text(encoding="utf-8"))
    if result.get("status") != "P0_D_ATLAS_COORDINATE_RECONSTRUCTION_NOT_ENGINE_VALIDATION":
        raise RuntimeError("A2 result is not eligible for Atlas-entry construction")
    if result.get("engine_selector_eligible") is not False:
        raise RuntimeError("A2 result violated Atlas/Engine firewall")
    if result.get("chi", {}).get("status") != "CHI_WITHHELD_NO_SECOND_ORDER_LICENSE":
        raise RuntimeError("A2 result violated frozen chi-withholding policy")

    defs = load_json(ROOT / "registries" / "COORDINATE_DEFINITIONS.json")
    coordinate_ids = declared_coordinate_ids(defs)
    entries = []
    entries.extend(_session_entry(result, x) for x in result["session_summaries"])
    entries.extend(_pair_entry(result, x) for x in result["pair_summaries"])
    output_dir.mkdir(parents=True, exist_ok=True)
    for entry in entries:
        validate_entry(entry, coordinate_ids)
        path = output_dir / f"{entry['atlas_entry_id']}.json"
        path.write_text(json.dumps(entry, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    index = {
        "schema": "neurostability-atlas-a2-srm-entry-index-v0.1",
        "status": "P0_D_ATLAS_ENTRIES_VALIDATED_NOT_P0Q_QUALIFIED",
        "source_id": result["source_id"],
        "entry_count": len(entries),
        "session_entry_count": len(result["session_summaries"]),
        "repeat_pair_entry_count": len(result["pair_summaries"]),
        "entries": [f"{e['atlas_entry_id']}.json" for e in entries],
        "chi_values_populated": 0,
        "engine_selector_eligible_entries": 0,
    }
    (output_dir / "INDEX.json").write_text(json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return index


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", default="results/a2_srm/csd_svd_result.json")
    parser.add_argument("--output-dir", default="results/a2_srm/atlas_entries")
    args = parser.parse_args()
    index = build(ROOT / args.result, ROOT / args.output_dir)
    print(json.dumps(index, sort_keys=True))
    print("A2 SRM SPARSE ATLAS ENTRY BUILD PASS")


if __name__ == "__main__":
    main()
