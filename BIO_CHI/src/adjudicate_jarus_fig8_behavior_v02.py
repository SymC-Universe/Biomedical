#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
import pathlib
import sys
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[2]
BIO = ROOT / "BIO_CHI"
IN = BIO / "artifacts" / "generated" / "jarus_fig8_execution_v02"
OUT = BIO / "artifacts" / "generated" / "jarus_fig8_behavior_v02"
OUT.mkdir(parents=True, exist_ok=True)

CASES = [
    "FIG8A_NOMINAL_DAMPED",
    "FIG8B_LIMIT_CYCLE",
    "FIG8C_RELAXATION_OSCILLATION",
]


def load_primary(case_id: str) -> list[tuple[float, float]]:
    p = IN / case_id / "trajectory_raw.csv"
    if not p.exists():
        raise SystemExit(f"BIO_CHI_JARUS_BEHAVIOR_MISSING_{case_id}")
    rows: list[tuple[float, float]] = []
    with p.open(newline="", encoding="utf-8") as fh:
        for row in csv.reader(fh):
            if not row:
                continue
            vals = [float(x) for x in row]
            # time_h, IKKn, IKKa, free nuclear NF-kappaB, A20, IkBa, IkBat
            rows.append((vals[0], vals[3]))
    return rows


def extrema_and_amplitudes(rows: list[tuple[float, float]]) -> dict:
    window = [(t, y) for t, y in rows if t > 1.0]
    if len(window) < 3:
        return {"noise_floor": None, "extrema": [], "amplitudes": []}
    maxabs = max(abs(y) for _, y in window)
    noise_floor = 1000.0 * sys.float_info.epsilon * max(1.0, maxabs)

    extrema: list[dict] = []
    for i in range(1, len(window) - 1):
        d1 = window[i][1] - window[i - 1][1]
        d2 = window[i + 1][1] - window[i][1]
        if d1 > 0.0 and d2 < 0.0:
            extrema.append({"type": "peak", "time_h": window[i][0], "value": window[i][1]})
        elif d1 < 0.0 and d2 > 0.0:
            extrema.append({"type": "trough", "time_h": window[i][0], "value": window[i][1]})

    amplitudes: list[dict] = []
    for i, ex in enumerate(extrema[:-1]):
        nxt = extrema[i + 1]
        if ex["type"] != "peak" or nxt["type"] != "trough":
            continue
        amp = float(ex["value"] - nxt["value"])
        if amp <= noise_floor:
            continue
        amplitudes.append({
            "peak_time_h": ex["time_h"],
            "trough_time_h": nxt["time_h"],
            "peak_value": ex["value"],
            "trough_value": nxt["value"],
            "peak_to_trough_amplitude": amp,
        })
    return {"noise_floor": noise_floor, "extrema": extrema, "amplitudes": amplitudes}


def adjudicate(case_id: str, amps: list[dict]) -> tuple[str, str]:
    values = [x["peak_to_trough_amplitude"] for x in amps]
    if len(values) < 2:
        return "INDETERMINATE", "fewer than two complete peak-to-trough amplitudes survived the frozen numerical floor"
    strictly_decreasing = all(values[i + 1] < values[i] for i in range(len(values) - 1))
    if case_id == "FIG8A_NOMINAL_DAMPED":
        if strictly_decreasing:
            return "PASS_DAMPED_COMPATIBLE", "all successive complete amplitudes are strictly smaller under the frozen rule"
        return "FAIL_NATIVE_BEHAVIOR", "the complete amplitude sequence is not strictly decreasing under the frozen rule"
    if strictly_decreasing:
        return "FAIL_NATIVE_BEHAVIOR", "the full complete-amplitude sequence is strictly decreasing under the frozen sustained-compatibility rule"
    if case_id == "FIG8B_LIMIT_CYCLE":
        return "PASS_SUSTAINED_OSCILLATION_COMPATIBLE", "at least two complete amplitudes survive and the sequence is not strictly decreasing"
    return "PASS_SUSTAINED_PERIODIC_COMPATIBLE", "at least two complete amplitudes survive and the sequence is not strictly decreasing"


results = []
failures = []
for case_id in CASES:
    rows = load_primary(case_id)
    times = [t for t, _ in rows]
    ys = [y for _, y in rows]
    monotone = all(times[i + 1] > times[i] for i in range(len(times) - 1))
    finite = all(math.isfinite(t) and math.isfinite(y) for t, y in rows)
    features = extrema_and_amplitudes(rows)
    status, reason = adjudicate(case_id, features["amplitudes"])
    morphology = None
    if case_id == "FIG8C_RELAXATION_OSCILLATION":
        morphology = "NOT_QUANTITATIVELY_ADJUDICATED"
    rec = {
        "case_id": case_id,
        "row_count": len(rows),
        "time_monotone": monotone,
        "all_primary_values_finite": finite,
        "noise_floor": features["noise_floor"],
        "extrema": features["extrema"],
        "complete_peak_to_trough_amplitudes": features["amplitudes"],
        "finite_window_status": status,
        "reason": reason,
        "relaxation_like_morphology_status": morphology,
    }
    results.append(rec)
    if not monotone or not finite:
        failures.append(f"{case_id}: trajectory integrity failure")

result = {
    "schema_version": "0.2",
    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    "audit_type": "prospectively_frozen_figure8_behavior_adjudication",
    "execution_freeze": "BIO_CHI/config/JARUS_FIG8_EXECUTION_FREEZE_v0_2.json",
    "adjudication_freeze": "BIO_CHI/config/JARUS_FIG8_BEHAVIOR_ADJUDICATION_FREEZE_v0_2.json",
    "method_source": "BIO_CHI/config/JARUS_FIG8_BEHAVIOR_ADJUDICATION_FREEZE_v0_1.json",
    "primary_observable": "free nuclear NF-kappaB",
    "behavior_classified": True,
    "chi_bio_constructed": False,
    "Chi_bio_constructed": False,
    "Bio_Chi_constructed": False,
    "cases": results,
    "integrity_failures": failures,
    "interpretation_limits": [
        "Finite-window compatibility does not by itself prove asymptotic stability or a mathematically stable limit cycle.",
        "Figure 8C relaxation-like/spiky morphology is refused quantitative adjudication because the paper supplies no numerical threshold and none may be invented post-view.",
        "No result in this gate licenses chi_bio, Chi_bio, or Bio Chi."
    ],
}
path = OUT / "behavior_adjudication_v0_2.json"
path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))
if failures:
    raise SystemExit("BIO_CHI_JARUS_FIG8_BEHAVIOR_INTEGRITY_FAIL")
print("BIO_CHI_JARUS_FIG8_BEHAVIOR_ADJUDICATION_COMPLETE")
