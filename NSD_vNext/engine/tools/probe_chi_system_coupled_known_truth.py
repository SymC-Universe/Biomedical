#!/usr/bin/env python3
"""Execute exact local-chi / embedded-system known-truth fixtures."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ENGINE_ROOT = Path(__file__).resolve().parents[1]
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

from nsd_engine.coupled_second_order import (
    locally_stable_globally_unstable_second_order_fixture,
    same_local_different_embedding_fixture,
    same_local_same_spectrum_different_transient_fixture,
)


def _system_record(system):
    t_peak, gain = system.max_transient_gain(t_max=20.0, samples=2001)
    return {
        "name": system.name,
        "local_natural_frequencies_rad_s":
            list(system.local_natural_frequencies_rad_s),
        "local_damping_ratios": list(system.local_damping_ratios),
        "isolated_local_stability": list(system.isolated_local_stability),
        "full_eigenvalues": [
            {"real": z.real, "imag": z.imag} for z in system.eigenvalues
        ],
        "spectral_abscissa": system.spectral_abscissa,
        "asymptotically_stable": system.asymptotically_stable,
        "numerical_abscissa": system.numerical_abscissa,
        "reactive": system.reactive,
        "nonnormality_commutator_norm_sq":
            system.nonnormality_commutator_norm_sq,
        "eigenvector_condition_number": system.eigenvector_condition_number,
        "max_transient_gain": gain,
        "time_of_max_transient_gain": t_peak,
        "sustained_return_time_gain_le_1_05":
            system.sustained_return_time(
                gain_threshold=1.05,
                t_max=30.0,
                samples=3001,
            ),
    }


def run():
    base_same, transient = same_local_same_spectrum_different_transient_fixture()
    base_embed, embedded = same_local_different_embedding_fixture()
    unstable = locally_stable_globally_unstable_second_order_fixture()

    return {
        "schema": "NSD_CHI_CHI_COUPLED_SECOND_ORDER_KNOWN_TRUTH_V0_1",
        "maturity": "P0-Q KNOWN TRUTH",
        "fixtures": {
            "same_local_same_spectrum_different_transient": {
                "same_local_modes":
                    base_same.same_local_modes(transient),
                "same_full_eigenspectrum":
                    base_same.same_eigenspectrum(transient),
                "baseline": _system_record(base_same),
                "coupled": _system_record(transient),
                "question": (
                    "Can identical local damping ratios and identical asymptotic "
                    "eigenvalues coexist with materially different transient "
                    "amplification and recovery?"
                ),
            },
            "same_local_different_embedding": {
                "same_local_modes":
                    base_embed.same_local_modes(embedded),
                "same_full_eigenspectrum":
                    base_embed.same_eigenspectrum(embedded),
                "baseline": _system_record(base_embed),
                "coupled": _system_record(embedded),
                "question": (
                    "Can coupling reorganize embedded modes while the isolated "
                    "local damping ratios remain unchanged?"
                ),
            },
            "locally_stable_globally_unstable": {
                "system": _system_record(unstable),
                "question": (
                    "Can stable isolated local modes become globally unstable "
                    "under coupling?"
                ),
            },
        },
        "interpretation": {
            "local_scalar_sufficient_for_full_system": False,
            "single_asymptotic_spectrum_sufficient_for_transient_behavior": False,
            "whole_system_scalar_created": False,
            "native_descriptors_retained": [
                "local modal damping ratios",
                "full eigenspectrum",
                "spectral abscissa",
                "numerical abscissa",
                "transient gain",
                "sustained return time",
            ],
        },
        "claim_ceiling": (
            "Exact linear-system known truth only. Demonstrates mathematical "
            "non-equivalence of local damping, embedded asymptotic structure, "
            "transient amplification and recovery. It does not establish that "
            "any specific neural recording instantiates these fixtures."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
