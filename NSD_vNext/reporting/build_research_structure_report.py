#!/usr/bin/env python3
"""Build a research-only neurophysiology structure report.

This builder intentionally cannot emit diagnostic or prognostic results. It is
for T0/T1 contract development from already-generated label-blind Engine
outputs. Individual normative deviation scoring remains disabled until a
qualified reference model explicitly licenses it.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from statistics import median
from typing import Any


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def _finite(values):
    return [
        float(value)
        for value in values
        if value is not None and math.isfinite(float(value))
    ]


def _summary(values):
    vals = sorted(_finite(values))
    if not vals:
        return {"n": 0, "median": None, "minimum": None, "maximum": None}
    return {
        "n": len(vals),
        "median": median(vals),
        "minimum": vals[0],
        "maximum": vals[-1],
    }


def _session(data: dict[str, Any], session_id: str) -> dict[str, Any]:
    matches = [
        item
        for item in data.get("sessions", [])
        if str(item.get("session_id")) == session_id
    ]
    if len(matches) != 1:
        raise ValueError(
            f"expected one specparam session {session_id}, found {len(matches)}"
        )
    return matches[0]


def build_report(
    *,
    d4: dict[str, Any],
    spec: dict[str, Any],
    atlas_manifest: dict[str, Any],
    atlas_reference: dict[str, Any],
    session_id: str,
    engine_version: str,
    source_run_id: int | None = None,
    source_run_head: str | None = None,
    input_hashes: dict[str, str] | None = None,
) -> dict[str, Any]:
    if not d4.get("passed"):
        raise ValueError("D4 input did not pass")
    if str(d4.get("subject_id")) != str(spec.get("subject_id")):
        raise ValueError("subject mismatch between D4 and specparam")

    subject_id = str(spec["subject_id"])
    recordings = [
        item
        for item in d4.get("recordings", [])
        if str(item.get("session_id")) == session_id
    ]
    if len(recordings) != 1 or not recordings[0].get("passed"):
        raise ValueError("requested session lacks one passed D4 recording")

    recording = recordings[0]
    session = _session(spec, session_id)

    exponents = []
    centers = []
    powers = []
    widths = []
    for row in session.get("channels", []):
        fixed = row["frozen_fixed"]
        names = list(fixed["aperiodic_parameter_names"])
        parameters = list(fixed["aperiodic_parameters"])
        if "exponent" not in names:
            raise ValueError(f"channel {row.get('channel')} lacks exponent")
        exponents.append(parameters[names.index("exponent")])
        if int(fixed.get("peak_count", 0)) > 0:
            peak = fixed["peaks"][0]
            centers.append(peak["center_frequency_hz"])
            powers.append(peak["power_above_aperiodic_log10"])
            widths.append(peak["descriptive_bandwidth_hz"])

    summary = session["summary"]
    population = atlas_reference.get("population", {})
    independence = atlas_manifest.get("reference_family_independence", [])
    independence_grade = (
        independence[0].get("independence_grade")
        if independence
        else "NOT_RECORDED"
    )

    return {
        "report_id": (
            f"{atlas_reference.get('dataset', 'dataset')}-"
            f"{subject_id}-{session_id}-structure-v0.1"
        ),
        "subject_id": subject_id,
        "session_id": session_id,
        "acquisition_scope": {
            "dataset": atlas_reference.get("dataset", d4.get("dataset")),
            "pinned_release": d4.get("source_release"),
            "task": d4.get("task"),
            "acquisition_time": recording.get("acquisition_time"),
            "channel_count": recording.get("header", {}).get("signal_count"),
            "sampling_rate_hz": (
                recording.get("header", {}).get("unique_sampling_rates_hz")
                or [None]
            )[0],
            "duration_seconds": recording.get("header", {}).get(
                "recording_duration_seconds"
            ),
            "source_payload_md5": recording.get("actual_md5"),
        },
        "engine_version": engine_version,
        "atlas_version": atlas_manifest.get("atlas_version"),
        "signal_quality_status": "PARTIALLY_USABLE",
        "out_of_domain_status": "NOT_EVALUATED",
        "structural_profile": {
            "spectral_state": {
                "status": "DESCRIPTIVE_ONLY",
                "frozen_candidate": spec.get("frozen_candidate"),
                "aperiodic_exponent_across_channels": _summary(exponents),
                "fixed_mean_peak_count": summary.get("fixed_mean_peak_count"),
                "fixed_zero_peak_channel_fraction": summary.get(
                    "fixed_zero_peak_channel_fraction"
                ),
                "first_listed_peak_center_frequency_hz": _summary(centers),
                "first_listed_peak_power_above_aperiodic_log10": _summary(
                    powers
                ),
                "first_listed_peak_descriptive_bandwidth_hz": _summary(widths),
                "dynamical_interpretation": "PROHIBITED",
            },
            "modal_state": {
                "status": "NOT_ADMITTED",
                "reason": (
                    "Real-EEG modal route has not passed the frozen "
                    "model-adequacy program."
                ),
            },
            "licensed_local_scalars": [],
            "spatial_system_state": {
                "status": "DESCRIPTIVE_CHANNEL_STRUCTURE_PRESERVED",
                "channel_count": summary.get("channel_count"),
                "interpretation": (
                    "No biological regional claim is licensed from this report."
                ),
            },
            "open_channel": {
                "fixed_vs_knee_model_disagreement_channel_count": summary.get(
                    "aperiodic_model_disagreement_channel_count"
                ),
                "fixed_vs_knee_model_disagreement_channel_fraction": summary.get(
                    "aperiodic_model_disagreement_channel_fraction"
                ),
                "fixed_max_peak_count_channel_count": summary.get(
                    "fixed_max_peak_count_channel_count"
                ),
                "fixed_total_width_boundary_hits": summary.get(
                    "fixed_total_width_boundary_hits"
                ),
                "full_recording_qc_status": "NOT_RUN_IN_THIS_INPUT_CHAIN",
                "reference_context": {
                    "atlas_maturity": atlas_manifest.get("maturity"),
                    "atlas_independence_for_engine_validation": (
                        independence_grade
                    ),
                    "atlas_channelwise_exponent_icc_a1_median": population.get(
                        "channelwise_aperiodic_exponent_icc_a1", {}
                    ).get("median"),
                    "atlas_peak_count_exact_agreement_median": population.get(
                        "channelwise_peak_count_exact_agreement_fraction", {}
                    ).get("median"),
                    "atlas_zero_peak_state_exact_agreement_median": (
                        population.get(
                            "channelwise_zero_peak_state_exact_agreement_fraction",
                            {},
                        ).get("median")
                    ),
                },
            },
        },
        "atlas_deviations": [],
        "refusals": [
            {
                "code": "REF_REFERENCE_DEVIATION_NOT_QUALIFIED",
                "layer": "atlas",
                "reason": (
                    "Current builder exposes P0-D reference context but no "
                    "qualified individual abnormality score."
                ),
                "scope": "individual reference deviation",
            },
            {
                "code": "REF_MODAL_ROUTE_NOT_QUALIFIED",
                "layer": "modal",
                "reason": (
                    "Real-EEG modal parameters remain disabled pending "
                    "model-adequacy qualification."
                ),
                "scope": "modal damping / local chi",
            },
            {
                "code": "REF_FULL_QC_NOT_RUN",
                "layer": "signal_quality",
                "reason": (
                    "D4 identity/readability passed, but this input chain does "
                    "not include the full artifact/QC stack required for an "
                    "unqualified USABLE status."
                ),
                "scope": "clinical-quality signal admission",
            },
        ],
        "clinical_models_run": [],
        "longitudinal_change": None,
        "forecasts": [],
        "provenance_hashes": input_hashes or {},
        "software_build": {
            "source_run_id": source_run_id,
            "source_run_head": source_run_head,
            "report_builder": "build_research_structure_report.py",
            "reporting_contract": (
                "neurophysiology_assessment_report_schema_v0.1"
            ),
        },
        "report_maturity": "RESEARCH_STRUCTURE_ONLY",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--d4", type=Path, required=True)
    parser.add_argument("--specparam", type=Path, required=True)
    parser.add_argument("--atlas-manifest", type=Path, required=True)
    parser.add_argument("--atlas-reference", type=Path, required=True)
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--engine-version", required=True)
    parser.add_argument("--source-run-id", type=int)
    parser.add_argument("--source-run-head")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    paths = {
        "d4": args.d4,
        "specparam": args.specparam,
        "atlas_manifest": args.atlas_manifest,
        "atlas_reference": args.atlas_reference,
    }
    data = {
        key: json.loads(path.read_text(encoding="utf-8"))
        for key, path in paths.items()
    }
    report = build_report(
        d4=data["d4"],
        spec=data["specparam"],
        atlas_manifest=data["atlas_manifest"],
        atlas_reference=data["atlas_reference"],
        session_id=args.session_id,
        engine_version=args.engine_version,
        source_run_id=args.source_run_id,
        source_run_head=args.source_run_head,
        input_hashes={key: _sha256(path) for key, path in paths.items()},
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "report_id": report["report_id"],
                "maturity": report["report_maturity"],
                "clinical_models_run": len(report["clinical_models_run"]),
                "forecasts": len(report["forecasts"]),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
