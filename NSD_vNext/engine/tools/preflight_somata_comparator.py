#!/usr/bin/env python3
"""Mechanical preflight for the pinned SOMATA standard-toolkit comparator.

This does not compare scientific performance and does not analyze EEG.
It verifies only that the exact pinned comparator version installs and that
the planned public API required by the frozen comparator design is available.
"""

from __future__ import annotations

import importlib.metadata
import json
from pathlib import Path
import argparse

import numpy as np

from somata import OscillatorModel
from somata.oscillator_search import IterativeOscillatorModel


PINNED_VERSION = "0.5.6"


def run() -> dict[str, object]:
    version = importlib.metadata.version("somata")
    if version != PINNED_VERSION:
        raise RuntimeError(f"somata version mismatch: {version} != {PINNED_VERSION}")

    model = OscillatorModel(
        a=[0.95],
        freq=[10.0],
        sigma2=[0.2],
        R=0.5,
        Fs=100.0,
    )
    np.random.seed(20260921)
    _, y = model.simulate(duration=2)

    search = IterativeOscillatorModel(y, 100.0, noise_start=None, osc_range=2)

    required_search_attrs = ("iterate", "get_knee_osc", "diagnose_residual_acf")
    missing = [name for name in required_search_attrs if not hasattr(search, name)]
    if missing:
        raise RuntimeError(f"missing planned SOMATA API: {missing}")

    return {
        "purpose": "standard-toolkit comparator mechanical/API preflight",
        "maturity": "P0-Q PREFLIGHT ONLY",
        "somata_version": version,
        "planned_comparator_class": "somata.oscillator_search.IterativeOscillatorModel",
        "oscillator_model_class": "somata.OscillatorModel",
        "api_present": list(required_search_attrs),
        "smoke_signal_shape": list(np.asarray(y).shape),
        "scientific_comparison_executed": False,
        "eeg_analyzed": False,
        "admission_rule_changed": False,
        "sampling_rate_fairness_decision_frozen": False,
        "next_gate": (
            "freeze fair sampling-rate / preprocessing mapping between NSD and SOMATA "
            "before any known-truth performance comparison"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
