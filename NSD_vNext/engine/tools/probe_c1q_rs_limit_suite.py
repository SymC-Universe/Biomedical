#!/usr/bin/env python3
"""Mandatory C1Q-RS Limit Map requalification suite.

P0-Q only. Uses the exact existing known-truth generators for adversarial,
family-boundary, and paired-sampling semantics, while adding C1Q-RS without
changing the native A0/A1/A2 comparators or truth-family labels.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from nsd_engine.continuous_lineage_candidate import fit_continuous_lineage_candidate
from nsd_engine.continuous_lineage_candidate_rs import fit_continuous_lineage_candidate_rs
from nsd_engine.state_space_adequacy import compare_state_space_candidates

import probe_c1q_refusal_controls as adv
import probe_c1q_family_boundary_controls as fam
import probe_c1q_paired_sampling_semantics as samp


MECH_REL_TOL = 1e-6


def serialize_fit(fit) -> dict[str, Any]:
    return {
        "negative_log_likelihood": float(fit.negative_log_likelihood),
        "bic": float(fit.bic),
        "success": bool(fit.success),
        "parameters": {k: float(v) for k, v in fit.parameters.items()},
    }


def serialize_rs(fit) -> dict[str, Any]:
    return {
        **serialize_fit(fit),
        "winning_start_origin": fit.winning_start_origin,
        "recurrence_seed_status": fit.recurrence_seed_status,
        "recurrence_seed_ready": fit.recurrence_seed_ready,
        "recurrence_seed_A_projected": fit.recurrence_seed_A_projected,
        "recurrence_seed_g_projected": fit.recurrence_seed_g_projected,
        "legacy_best_negative_log_likelihood": float(
            fit.legacy_best_negative_log_likelihood
        ),
        "legacy_best_success": bool(fit.legacy_best_success),
        "legacy_attempted_start_count": int(fit.legacy_attempted_start_count),
        "attempted_start_count": int(fit.attempted_start_count),
    }


def fit_extended(signal, fs: float, optimizer_maxiter: int = 50):
    current = compare_state_space_candidates(
        signal,
        fs,
        optimizer_maxiter=optimizer_maxiter,
    )
    c1q = fit_continuous_lineage_candidate(
        signal,
        fs,
        optimizer_maxiter=optimizer_maxiter,
        max_optimized_starts=8,
    )
    rs = fit_continuous_lineage_candidate_rs(
        signal,
        fs,
        optimizer_maxiter=optimizer_maxiter,
        max_optimized_starts=8,
    )
    tol = MECH_REL_TOL * max(1.0, abs(c1q.negative_log_likelihood))
    if rs.negative_log_likelihood > c1q.negative_log_likelihood + tol:
        raise RuntimeError(
            "C1Q-RS strict non-worsening failed in Limit suite: "
            f"C1Q={c1q.negative_log_likelihood}, RS={rs.negative_log_likelihood}"
        )

    bics = {fit.family: float(fit.bic) for fit in current.fits}
    bics["C1Q"] = float(c1q.bic)
    bics["C1Q-RS"] = float(rs.bic)
    ordered = sorted(bics.items(), key=lambda item: item[1])
    return {
        "current_winner": current.bic_winner,
        "extended_winner": ordered[0][0],
        "extended_margin_to_second": float(ordered[1][1] - ordered[0][1]),
        "bics": bics,
        "C1Q": serialize_fit(c1q),
        "C1Q_RS": serialize_rs(rs),
        "rs_nll_improvement_over_c1q": float(
            c1q.negative_log_likelihood - rs.negative_log_likelihood
        ),
        "strict_nonworsening_pass": True,
    }


def run_adversarial(output: Path, optimizer_maxiter: int):
    rows = []
    seeds = [0, 1]
    for seed in seeds:
        isotropic = adv.simulate_latent_oscillator(
            adv.LatentOscillatorTruth(10.0, 0.30, adv.FS),
            seconds=adv.SECONDS,
            measurement_noise_to_latent_sd=0.50,
            seed=seed,
        )
        rows.append(
            {
                "truth_class": "a1_isotropic_one_mode",
                "seed": seed,
                "expected_role": "nested_simpler_control",
                **fit_extended(isotropic, adv.FS, optimizer_maxiter),
            }
        )
        rows.append(
            {
                "truth_class": "genuine_separated_two_mode",
                "seed": seed,
                "expected_role": "multimodal_control",
                **fit_extended(adv._two_mode_signal(seed), adv.FS, optimizer_maxiter),
            }
        )
        for kind in (
            "anisotropic_white_4_to_1",
            "rank1_white_axis_drive",
            "colored_process_phi_0_7",
        ):
            rows.append(
                {
                    "truth_class": kind,
                    "seed": seed,
                    "expected_role": (
                        "one_mode_white_forcing_shape_control"
                        if kind != "colored_process_phi_0_7"
                        else "colored_process_refusal_control"
                    ),
                    **fit_extended(
                        adv._process_signal(kind, seed),
                        adv.FS,
                        optimizer_maxiter,
                    ),
                }
            )
    payload = {
        "status": "P0Q_C1Q_RS_LIMIT_ADVERSARIAL_COMPLETE",
        "licenses_real_eeg_local_chi": False,
        "promotes_c1q_rs": False,
        "truth_family_labels_are_immutable": True,
        "rows": rows,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"mode": "adversarial", "rows": len(rows), "output": str(output)}, sort_keys=True))


def run_family(output: Path, optimizer_maxiter: int):
    fs = 128.0
    seconds = 30.0
    coord = fam.coordinates(fs, 0.8, 10.0, 0.30)
    A, rho, xi = coord["A"], coord["rho"], coord["xi"]
    positive_S = fam.scalar_positive_bound(A, rho, xi, +1, coord["H_D"])
    negative_S = fam.scalar_positive_bound(A, rho, xi, -1, -coord["H_D"])

    specs = []
    for sign in (-1, 1):
        H_C = sign * coord["H_C"]
        H_D = sign * coord["H_D"]
        H_DC = sign * (
            coord["H_C"] + 0.5 * (coord["H_D"] - coord["H_C"])
        )
        S_bound = negative_S if sign < 0 else positive_S
        H_SD = 0.5 * (H_D + S_bound)
        specs.extend(
            [
                ("D_not_C", sign, H_DC, H_C, H_D, S_bound),
                ("S_not_D", sign, H_SD, H_C, H_D, S_bound),
            ]
        )

    rows = []
    for truth_class, sign, H, H_C, H_D, S_bound in specs:
        implied_g = (H / A) * coord["theta"] / (
            coord["L"] * __import__("math").sin(coord["theta"])
        )
        if fam.spectral_minimum(A, rho, xi, H) <= 0.0:
            raise RuntimeError("constructed family-boundary truth is not scalar positive")
        for seed in (0, 1):
            signal = fam.simulate(
                A,
                rho,
                xi,
                H,
                fs=fs,
                seconds=seconds,
                seed=seed + (1000 if sign > 0 else 0),
            )
            rows.append(
                {
                    "truth_class": truth_class,
                    "sign": sign,
                    "seed": seed,
                    "H": H,
                    "H_C_signed": H_C,
                    "H_D_signed": H_D,
                    "S_boundary_signed": S_bound,
                    "implied_continuous_g": implied_g,
                    "spectral_minimum": fam.spectral_minimum(A, rho, xi, H),
                    **fit_extended(signal, fs, optimizer_maxiter),
                }
            )

    payload = {
        "status": "P0Q_C1Q_RS_LIMIT_FAMILY_COMPLETE",
        "licenses_real_eeg_local_chi": False,
        "promotes_c1q_rs": False,
        "truth_family_labels_are_immutable": True,
        "coordinates": coord,
        "scalar_positive_bounds": {
            "negative": negative_S,
            "positive": positive_S,
        },
        "rows": rows,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"mode": "family", "rows": len(rows), "output": str(output)}, sort_keys=True))


def fit_rs_pair(signal, fs: float, optimizer_maxiter: int):
    old = fit_continuous_lineage_candidate(
        signal,
        fs,
        optimizer_maxiter=optimizer_maxiter,
        max_optimized_starts=8,
    )
    rs = fit_continuous_lineage_candidate_rs(
        signal,
        fs,
        optimizer_maxiter=optimizer_maxiter,
        max_optimized_starts=8,
    )
    tol = MECH_REL_TOL * max(1.0, abs(old.negative_log_likelihood))
    if rs.negative_log_likelihood > old.negative_log_likelihood + tol:
        raise RuntimeError("paired-sampling strict non-worsening failed")
    return {
        "C1Q": serialize_fit(old),
        "C1Q_RS": serialize_rs(rs),
        "rs_nll_improvement": float(
            old.negative_log_likelihood - rs.negative_log_likelihood
        ),
        "strict_nonworsening_pass": True,
    }


def run_paired(output: Path, optimizer_maxiter: int):
    fs = 256.0
    seconds = 30.0
    A = 0.8
    fn = 10.0
    zeta = 0.30
    math = __import__("math")
    omega_n = 2.0 * math.pi * fn
    alpha = zeta * omega_n
    nu = omega_n * math.sqrt(1.0 - zeta * zeta)
    L = alpha / fs
    rho = math.exp(-L)
    theta = nu / fs
    xi = math.cos(theta)
    H_C = A * L * math.sin(theta) / theta
    H_D = A * math.sinh(L)
    S_pos = samp.scalar_positive_bound(A, rho, xi, +1, H_D)
    S_neg = samp.scalar_positive_bound(A, rho, xi, -1, -H_D)

    specs = [
        ("C_g_neg075", "C", None, -0.75),
        ("C_g_pos075", "C", None, +0.75),
        ("D_not_C_negative", "D_not_C", -(H_C + 0.5 * (H_D - H_C)), None),
        ("D_not_C_positive", "D_not_C", +(H_C + 0.5 * (H_D - H_C)), None),
        ("S_not_D_negative", "S_not_D", 0.5 * (-H_D + S_neg), None),
        ("S_not_D_positive", "S_not_D", 0.5 * (H_D + S_pos), None),
    ]

    rows = []
    for label, family, H, g_truth in specs:
        for seed in (0, 1):
            if family == "C":
                fine = samp.continuous_c_signal(
                    fs=fs,
                    seconds=seconds,
                    A=A,
                    fn=fn,
                    zeta=zeta,
                    g=float(g_truth),
                    seed=seed,
                )
            else:
                fine = samp.arma_signal(
                    fs=fs,
                    seconds=seconds,
                    A=A,
                    rho=rho,
                    xi=xi,
                    H=float(H),
                    seed=seed + (1000 if "positive" in label else 0),
                )
            coarse = fine[::2]
            fine_fit = fit_rs_pair(fine, fs, optimizer_maxiter)
            coarse_fit = fit_rs_pair(coarse, fs / 2.0, optimizer_maxiter)
            rows.append(
                {
                    "truth_label": label,
                    "truth_family": family,
                    "seed": seed,
                    "truth_chi": zeta,
                    "truth_g_if_C": g_truth,
                    "truth_H_fine": H,
                    "fine": fine_fit,
                    "coarse": coarse_fit,
                    "rs_abs_chi_shift": abs(
                        coarse_fit["C1Q_RS"]["parameters"]["damping_ratio"]
                        - fine_fit["C1Q_RS"]["parameters"]["damping_ratio"]
                    ),
                    "rs_abs_g_shift": abs(
                        coarse_fit["C1Q_RS"]["parameters"]["g"]
                        - fine_fit["C1Q_RS"]["parameters"]["g"]
                    ),
                }
            )

    payload = {
        "status": "P0Q_C1Q_RS_LIMIT_PAIRED_COMPLETE",
        "licenses_real_eeg_local_chi": False,
        "promotes_c1q_rs": False,
        "defines_sampling_consistency_threshold": False,
        "truth_family_labels_are_immutable": True,
        "rows": rows,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"mode": "paired", "rows": len(rows), "output": str(output)}, sort_keys=True))


def merge(input_dir: Path, output: Path):
    names = {
        "adversarial": "c1q_rs_limit_adversarial.json",
        "family": "c1q_rs_limit_family.json",
        "paired": "c1q_rs_limit_paired.json",
    }
    sections = {}
    for key, name in names.items():
        matches = list(input_dir.rglob(name))
        if len(matches) != 1:
            raise RuntimeError(f"expected one {name}, found {len(matches)}")
        sections[key] = json.loads(matches[0].read_text(encoding="utf-8"))

    all_rows = (
        sections["adversarial"]["rows"]
        + sections["family"]["rows"]
    )
    summary = {
        "strict_nonworsening_pass_count": int(
            sum(r["strict_nonworsening_pass"] for r in all_rows)
            + sum(
                r["fine"]["strict_nonworsening_pass"]
                + r["coarse"]["strict_nonworsening_pass"]
                for r in sections["paired"]["rows"]
            )
        ),
        "adversarial_extended_winners": [
            {
                "truth_class": r["truth_class"],
                "seed": r["seed"],
                "winner": r["extended_winner"],
            }
            for r in sections["adversarial"]["rows"]
        ],
        "family_extended_winners": [
            {
                "truth_class": r["truth_class"],
                "sign": r["sign"],
                "seed": r["seed"],
                "winner": r["extended_winner"],
            }
            for r in sections["family"]["rows"]
        ],
    }
    payload = {
        "status": "P0Q_C1Q_RS_LIMIT_SUITE_COMPLETE",
        "licenses_real_eeg_local_chi": False,
        "promotes_c1q_rs": False,
        "truth_family_labels_are_immutable": True,
        "sections": sections,
        "summary": summary,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"status": payload["status"], "output": str(output)}, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("adversarial", "family", "paired", "merge"),
        required=True,
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--input-dir", type=Path)
    parser.add_argument("--optimizer-maxiter", type=int, default=50)
    args = parser.parse_args()

    if args.mode == "adversarial":
        run_adversarial(args.output, args.optimizer_maxiter)
    elif args.mode == "family":
        run_family(args.output, args.optimizer_maxiter)
    elif args.mode == "paired":
        run_paired(args.output, args.optimizer_maxiter)
    else:
        if args.input_dir is None:
            raise ValueError("merge requires --input-dir")
        merge(args.input_dir, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
