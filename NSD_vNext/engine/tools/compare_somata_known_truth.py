#!/usr/bin/env python3
"""Matched-information NSD vs SOMATA 0.5.6 known-truth comparator.

P0-Q comparator evidence only. This script reuses the existing NSD adequacy
generators, creates one shared 120 Hz standardized signal, and passes the exact
same array to NSD A0/A1/A2 and SOMATA iOsc. It does not analyze EEG or alter
either tool's admission rules.
"""

from __future__ import annotations

import argparse
import importlib.metadata
import importlib.util
import json
import math
from pathlib import Path
import platform
import sys
from typing import Any

import numpy as np
import scipy
from scipy.signal import resample_poly

from somata.oscillator_search import IterativeOscillatorModel

ENGINE_ROOT = Path(__file__).resolve().parents[1]
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

from nsd_engine.state_space_adequacy import compare_state_space_candidates


SOURCE_FS = 256.0
COMPARATOR_FS = 120.0
RESAMPLE_UP = 15
RESAMPLE_DOWN = 32
SOMATA_VERSION = "0.5.6"
SOMATA_NOISE_START_HZ = 40.0
SCENARIOS = (
    "single_valid_truth",
    "two_modes_close",
    "two_modes_separated",
    "colored_observation_noise",
    "frequency_shift_mid_record",
    "finite_bursts",
    "nonoscillatory_ar1",
    "white_noise",
)
SEEDS = (0, 1, 2)


def _load_existing_generators() -> Any:
    source = Path(__file__).with_name("probe_state_space_model_adequacy.py")
    spec = importlib.util.spec_from_file_location("nsd_existing_adequacy_generators", source)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load existing adequacy generator file: {source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if float(module.FS) != SOURCE_FS:
        raise RuntimeError(f"source generator Fs changed: {module.FS} != {SOURCE_FS}")
    if tuple(module.SEEDS) != SEEDS:
        raise RuntimeError(f"source generator seeds changed: {module.SEEDS} != {SEEDS}")
    if tuple(module.GENERATORS.keys()) != SCENARIOS:
        raise RuntimeError(
            "source generator scenario order/content changed: "
            f"{tuple(module.GENERATORS.keys())!r}"
        )
    return module


def _shared_signal(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=np.float64).reshape(-1)
    if not np.isfinite(values).all():
        raise ValueError("source generator produced non-finite values")
    resampled = resample_poly(values, RESAMPLE_UP, RESAMPLE_DOWN)
    resampled = np.asarray(resampled, dtype=np.float64)
    resampled -= float(np.mean(resampled))
    sd = float(np.std(resampled))
    if not math.isfinite(sd) or sd <= 0:
        raise ValueError("shared comparator signal has invalid standard deviation")
    return resampled / sd


def _jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        if isinstance(value, float) and not math.isfinite(value):
            return None
        return value
    if isinstance(value, np.generic):
        return _jsonable(value.item())
    if isinstance(value, np.ndarray):
        return [_jsonable(v) for v in value.tolist()]
    if hasattr(value, "to_dict"):
        return _jsonable(value.to_dict())
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    try:
        arr = np.asarray(value)
        if arr.ndim == 0:
            return _jsonable(arr.item())
        return _jsonable(arr.tolist())
    except Exception:
        return str(value)


def _modal_values(radius: float, damped_frequency_hz: float) -> dict[str, float]:
    radius = float(abs(radius))
    if not (0.0 < radius < 1.0):
        return {
            "damping_radius": radius,
            "damped_frequency_hz": float(abs(damped_frequency_hz)),
            "decay_rate_per_s": float("nan"),
            "natural_frequency_hz": float("nan"),
            "damping_ratio": float("nan"),
        }
    decay = -math.log(radius) * COMPARATOR_FS
    damped_frequency_hz = float(abs(damped_frequency_hz))
    omega_d = 2.0 * math.pi * damped_frequency_hz
    omega_n = math.hypot(decay, omega_d)
    return {
        "damping_radius": radius,
        "damped_frequency_hz": damped_frequency_hz,
        "decay_rate_per_s": decay,
        "natural_frequency_hz": omega_n / (2.0 * math.pi),
        "damping_ratio": decay / omega_n if omega_n > 0 else float("nan"),
    }


def _run_somata(signal: np.ndarray, seed: int) -> dict[str, Any]:
    np.random.seed(20260922 + int(seed))
    y = np.asarray(signal, dtype=np.float64).reshape(1, -1)
    search = IterativeOscillatorModel(
        y,
        COMPARATOR_FS,
        noise_start=SOMATA_NOISE_START_HZ,
        osc_range=2,
    )
    search.iterate(
        freq_res=1,
        keep_param=(),
        reiterate=False,
        sigma2_method="eig",
        freq_hp=0,
        R_hp=0.1,
        Q_hp=None,
        R_sigma2="constant",
        Q_sigma2="MLE",
        no_priors=False,
        track_params=False,
        plot_fit=False,
        verbose=False,
    )
    selected = search.get_knee_osc()
    radii = np.asarray(selected.a, dtype=np.float64).reshape(-1)
    frequencies = np.asarray(selected.freq, dtype=np.float64).reshape(-1)
    if radii.size != frequencies.size:
        raise RuntimeError("SOMATA radius/frequency component lengths differ")

    components = [
        _modal_values(radius, frequency)
        for radius, frequency in zip(radii, frequencies)
    ]
    components.sort(key=lambda item: item["natural_frequency_hz"])

    residual = search.diagnose_residual_acf()
    return {
        "selected_oscillator_count": int(selected.ncomp),
        "selected_components": components,
        "knee_index": int(search.knee_index),
        "log_likelihood_path": _jsonable(search.ll),
        "aic_path": _jsonable(search.AIC),
        "selected_observation_noise_R": _jsonable(selected.R),
        "residual_acf_diagnostics": _jsonable(residual),
        "manual_selection_used": False,
    }


def _truth_error(scenario: str, nsd: dict[str, Any], somata: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {
        "semantic_comparability": (
            "NOT_DIRECTLY_COMPARABLE_ZERO_OSCILLATOR_ABSENT_IN_IOSC"
            if scenario in {"nonoscillatory_ar1", "white_noise"}
            else "DIRECT_MODAL_COMPARISON_WITH_NATIVE_MODEL_DIFFERENCES_PRESERVED"
        )
    }
    if scenario == "single_valid_truth":
        nsd_a1 = next(f for f in nsd["fits"] if f["family"] == "A1")
        out["truth_natural_frequencies_hz"] = [10.0]
        out["truth_damping_ratios"] = [0.30]
        out["nsd_a1_frequency_relative_error"] = abs(
            nsd_a1["parameters"]["natural_frequency_hz"] - 10.0
        ) / 10.0
        out["nsd_a1_damping_absolute_error"] = abs(
            nsd_a1["parameters"]["damping_ratio"] - 0.30
        )
        if somata["selected_components"]:
            closest = min(
                somata["selected_components"],
                key=lambda x: abs(x["natural_frequency_hz"] - 10.0),
            )
            out["somata_closest_frequency_relative_error"] = abs(
                closest["natural_frequency_hz"] - 10.0
            ) / 10.0
            out["somata_closest_damping_absolute_error"] = abs(
                closest["damping_ratio"] - 0.30
            )
    elif scenario in {"two_modes_close", "two_modes_separated"}:
        truth = [10.0, 12.0 if scenario == "two_modes_close" else 20.0]
        out["truth_natural_frequencies_hz"] = truth
        estimated = [x["natural_frequency_hz"] for x in somata["selected_components"]]
        if len(estimated) >= 2:
            estimated = sorted(estimated)[:2]
            out["somata_sorted_frequency_relative_errors"] = [
                abs(est - true) / true for est, true in zip(estimated, truth)
            ]
    return out


def run() -> dict[str, Any]:
    version = importlib.metadata.version("somata")
    if version != SOMATA_VERSION:
        raise RuntimeError(f"somata version mismatch: {version} != {SOMATA_VERSION}")

    generators = _load_existing_generators()
    rows = []
    for scenario in SCENARIOS:
        generator = generators.GENERATORS[scenario]
        for seed in SEEDS:
            source = generator(seed)
            shared = _shared_signal(source)
            nsd_cmp = compare_state_space_candidates(
                shared,
                COMPARATOR_FS,
                fmin_hz=1.0,
                fmax_hz=45.0,
                optimizer_maxiter=80,
            )
            nsd = {
                "bic_winner": nsd_cmp.bic_winner,
                "bic_margin_to_second": nsd_cmp.bic_margin_to_second,
                "fits": [
                    {
                        "family": fit.family,
                        "success": fit.success,
                        "bic": fit.bic,
                        "negative_log_likelihood": fit.negative_log_likelihood,
                        "innovation_max_abs_autocorrelation":
                            fit.innovation_max_abs_autocorrelation,
                        "parameters": dict(fit.parameters),
                    }
                    for fit in nsd_cmp.fits
                ],
            }
            somata = _run_somata(shared, seed)
            rows.append(
                {
                    "scenario": scenario,
                    "seed": seed,
                    "source_sample_count_256hz": int(np.asarray(source).size),
                    "shared_sample_count_120hz": int(shared.size),
                    "shared_signal_mean": float(np.mean(shared)),
                    "shared_signal_sd": float(np.std(shared)),
                    "nsd": nsd,
                    "somata": somata,
                    "truth_mapping": _truth_error(scenario, nsd, somata),
                }
            )

    summaries = {}
    for scenario in SCENARIOS:
        subset = [row for row in rows if row["scenario"] == scenario]
        summaries[scenario] = {
            "n": len(subset),
            "nsd_bic_winner_counts": {
                family: sum(row["nsd"]["bic_winner"] == family for row in subset)
                for family in ("A0", "A1", "A2")
            },
            "somata_selected_oscillator_count_counts": {
                str(count): sum(
                    row["somata"]["selected_oscillator_count"] == count
                    for row in subset
                )
                for count in (1, 2)
            },
            "semantic_comparability": subset[0]["truth_mapping"]["semantic_comparability"],
        }

    return {
        "schema": "NSD_SOMATA_KNOWN_TRUTH_COMPARATOR_V0_1",
        "purpose": "matched-information standard-toolkit P0-Q comparison",
        "maturity": "P0-Q",
        "source_sampling_rate_hz": SOURCE_FS,
        "shared_sampling_rate_hz": COMPARATOR_FS,
        "resample_poly": {"up": RESAMPLE_UP, "down": RESAMPLE_DOWN},
        "shared_preprocessing": ["demean", "population_sd_standardize"],
        "somata_version": version,
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
        "scenarios": list(SCENARIOS),
        "seeds": list(SEEDS),
        "summaries": summaries,
        "rows": rows,
        "interpretation_ceiling": (
            "P0-Q comparator evidence only. No overall winner, ADDS/EQUIVALENT/"
            "SUBTRACTS verdict, real-EEG modal damping, local chi, diagnosis, "
            "prognosis, or biological mode interpretation is licensed."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(_jsonable(result), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result["summaries"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
