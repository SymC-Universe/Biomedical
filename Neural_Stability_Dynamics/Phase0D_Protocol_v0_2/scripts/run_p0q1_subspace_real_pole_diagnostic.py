from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np

from src.dmd import fit_subspace_dmd, subspace_dmd_projected_singular_values
from src.rank_sweep import adjacent_rank_stability, sweep_subspace_dmd
from scripts.run_p0q1_rank_signal_holdout import _load_freeze, _refusal_record


def _complex(z):
    z = complex(z)
    return {"real": float(z.real), "imag": float(z.imag)}


def _rank_detail(sweep, rank, dt):
    fit = sweep["fits"][rank]
    out = {
        "rank": int(rank),
        "status": fit.get("status"),
        "singular_gap_ratio": (
            float(fit["singular_gap_ratio"])
            if np.isfinite(fit.get("singular_gap_ratio", np.nan))
            else None
        ),
    }
    if fit.get("status") != "OK":
        out["exception_type"] = fit.get("exception_type")
        out["exception_message"] = fit.get("exception_message")
        return out
    vals = np.asarray(fit["vals"], complex)
    out["continuous_poles"] = [_complex(z) for z in vals]
    out["discrete_eigenvalues"] = [_complex(np.exp(z * dt)) for z in vals]
    out["frequencies_hz"] = [float(abs(z.imag) / (2 * np.pi)) for z in vals]
    out["decay_rates"] = [float(-z.real) for z in vals]
    out["unstable_poles"] = int(np.sum(vals.real >= 0.0))
    out["positive_complex_modes_gt_0p25Hz"] = int(
        np.sum(vals.imag / (2 * np.pi) >= 0.25)
    )
    return out


def _one_frozen_record(cfg, replicate):
    Y = _refusal_record(cfg, "real_pole_only_linear_system", replicate)
    sq = subspace_dmd_projected_singular_values(Y)
    sweep = sweep_subspace_dmd(Y, float(cfg["dt"]), cfg["candidate_grid"])
    gaps = {
        str(rank): (
            float(sweep["fits"][rank]["singular_gap_ratio"])
            if np.isfinite(sweep["fits"][rank].get("singular_gap_ratio", np.nan))
            else None
        )
        for rank in cfg["candidate_grid"]
    }
    max_rank = max(
        (r for r in cfg["candidate_grid"] if gaps[str(r)] is not None),
        key=lambda r: gaps[str(r)],
    )
    matrix_rank = int(np.linalg.matrix_rank(np.diag(sq)))
    return {
        "replicate": int(replicate),
        "n_samples": int(cfg["n_samples"]),
        "projected_singular_values": [float(x) for x in sq],
        "projected_singular_values_relative_to_first": [
            float(x / max(float(sq[0]), 1e-300)) for x in sq
        ],
        "cumulative_singular_value_fraction": [
            float(x) for x in np.cumsum(sq) / max(float(np.sum(sq)), 1e-300)
        ],
        "numpy_matrix_rank_of_projected_spectrum": matrix_rank,
        "official_default_r_after_min_channel_cap": min(int(cfg["n_channels"]), matrix_rank),
        "gap_by_rank": gaps,
        "argmax_gap_rank": int(max_rank),
        "rank_details": {
            str(r): _rank_detail(sweep, r, float(cfg["dt"]))
            for r in cfg["candidate_grid"]
        },
        "adjacent_rank_stability": adjacent_rank_stability(sweep, min_hz=0.25),
    }


def _duration_diagnostic(cfg, multiplier, replicate):
    local = dict(cfg)
    local["n_samples"] = int(cfg["n_samples"] * multiplier)
    Y = _refusal_record(local, "real_pole_only_linear_system", replicate)
    sq = subspace_dmd_projected_singular_values(Y)
    sweep = sweep_subspace_dmd(Y, float(local["dt"]), local["candidate_grid"])
    finite = [
        (r, float(sweep["fits"][r]["singular_gap_ratio"]))
        for r in local["candidate_grid"]
        if np.isfinite(sweep["fits"][r].get("singular_gap_ratio", np.nan))
    ]
    rank, gap = max(finite, key=lambda x: x[1])
    return {
        "multiplier": int(multiplier),
        "n_samples": int(local["n_samples"]),
        "replicate": int(replicate),
        "argmax_gap_rank": int(rank),
        "max_gap": float(gap),
        "relative_singular_values_first_8": [
            float(x / max(float(sq[0]), 1e-300)) for x in sq[:8]
        ],
        "rank2": _rank_detail(sweep, 2, float(local["dt"])),
        "rank4": _rank_detail(sweep, 4, float(local["dt"])),
        "rank8": _rank_detail(sweep, 8, float(local["dt"])),
    }


def build_record(cfg):
    frozen = [_one_frozen_record(cfg, r) for r in range(int(cfg["replicates_per_family"]))]
    duration = []
    for mult in [1, 2, 4]:
        for rep in range(3):
            duration.append(_duration_diagnostic(cfg, mult, rep))
    return {
        "schema": "nsd-phase0d-v0.2-p0q1-subspace-real-pole-retrospective-v1",
        "status": "POST_RESULT_DIAGNOSTIC_DO_NOT_RESCORE_P0Q1",
        "protocol": cfg["protocol"],
        "p0q1_freeze_schema": cfg["schema"],
        "p0q1_result":"SUBSPACE_DMD_FAILS_P0Q1",
        "family":"real_pole_only_linear_system",
        "truth_for_diagnosis_only": {
            "continuous_generator_poles": [-0.7, -2.4],
            "latent_state_order": 2,
            "oscillatory_modes": 0,
        },
        "frozen_p0q1_records": frozen,
        "duration_sensitivity_post_result": duration,
        "questions": [
            "Does the rank-4 projected singular gap persist as record length increases?",
            "Does the rank-2 fit retain the planted real-pole structure while rank-4 introduces complex artifacts?",
            "Does the authors' default matrix-rank route approach the observable channel cap rather than the planted generator order in finite stochastic data?"
        ],
        "nonclaims": [
            "This diagnostic cannot rescue, rescore, or retune P0Q1.",
            "Duration sensitivity is new post-result development evidence, not prospective qualification.",
            "No new Subspace-DMD rank selector is defined here.",
            "No P1, EEG, chi, phenotype, regime, mechanism, or clinical claim is tested."
        ]
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", default="configs/P0Q1_RANK_SIGNAL_FREEZE.json")
    parser.add_argument("--output", default="results/p0_diagnostics/p0q1_subspace_real_pole.json")
    args = parser.parse_args()
    cfg = _load_freeze(args.freeze)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(build_record(cfg), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out.resolve())
    print("P0Q1 SUBSPACE REAL-POLE RETROSPECTIVE COMPLETE. P0Q1 result remains unchanged.")


if __name__ == "__main__":
    main()
