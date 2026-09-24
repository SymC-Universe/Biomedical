#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import pathlib
import sys

OBS = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

raw = json.loads(OBS.read_text())
if raw.get("status") != "PASS_LOCAL_OBSERVABILITY":
    raise SystemExit("BIO_CHI_SCALAR_REQUIRES_PASSED_OBSERVABILITY")

case_results = []
overall_pass = True

for case in raw.get("cases", []):
    steps_out = []
    signs = []
    pair_ok_all = True
    finite_all = True
    chis = []

    for step in case.get("steps", []):
        vals = [
            complex(float(r), float(i))
            for r, i in zip(step["eigenvalues_real"], step["eigenvalues_imag"])
        ]
        positive = [z for z in vals if z.imag > 0]
        negative = [z for z in vals if z.imag < 0]
        pair_ok = len(positive) == 1 and len(negative) == 1
        if pair_ok:
            lam = positive[0]
            mate = negative[0]
            pair_residual = abs(mate - lam.conjugate())
        else:
            lam = complex(float("nan"), float("nan"))
            pair_residual = float("nan")

        omega0 = abs(lam)
        gamma = -2.0 * lam.real
        omega_d = abs(lam.imag)
        chi = -lam.real / omega0 if omega0 > 0 and math.isfinite(omega0) else float("nan")
        identity_residual = abs(omega0**2 - ((gamma / 2.0) ** 2 + omega_d**2))
        finite = all(math.isfinite(x) for x in [omega0, gamma, omega_d, chi, identity_residual])

        pair_ok_all = pair_ok_all and pair_ok
        finite_all = finite_all and finite
        signs.append(0 if lam.real == 0 else (1 if lam.real > 0 else -1))
        chis.append(chi)

        steps_out.append({
            "multiplier": step["multiplier"],
            "lambda_real": lam.real,
            "lambda_imag": lam.imag,
            "conjugate_pair_residual": pair_residual,
            "gamma": gamma,
            "omega0": omega0,
            "omega_d": omega_d,
            "chi_bio": chi,
            "factor_identity_residual": identity_residual,
            "complex_pair_output_visibility": next(
                (
                    float(v)
                    for v, im in zip(step["mode_output_visibility"], step["eigenvalues_imag"])
                    if float(im) > 0
                ),
                None,
            ),
            "full_observability_rank": step["observability_rank"],
            "finite": finite,
        })

    sign_invariant = len(set(signs)) == 1
    finite_chis = [x for x in chis if math.isfinite(x)]
    if finite_chis:
        chi_mean = sum(finite_chis) / len(finite_chis)
        chi_range = max(finite_chis) - min(finite_chis)
        chi_relative_spread = chi_range / abs(finite_chis[0]) if finite_chis[0] != 0 else None
    else:
        chi_mean = chi_range = chi_relative_spread = None

    full_rank_all = bool(case.get("full_rank_all_steps"))
    case_pass = pair_ok_all and finite_all and sign_invariant and full_rank_all
    overall_pass = overall_pass and case_pass

    if chi_mean is None:
        local_interpretation = "INDETERMINATE"
    elif chi_mean > 0:
        local_interpretation = "LOCALLY_DAMPED_OSCILLATORY_FACTOR"
    elif chi_mean < 0:
        local_interpretation = "LOCALLY_AMPLIFYING_OSCILLATORY_FACTOR"
    else:
        local_interpretation = "ZERO_REAL_PART_OSCILLATORY_FACTOR"

    case_results.append({
        "case_id": case["case_id"],
        "case_status": "PASS_MODEL_SPECIFIC_FACTOR" if case_pass else "REFUSE_MODEL_SPECIFIC_FACTOR",
        "local_interpretation": local_interpretation,
        "chi_bio_mean": chi_mean,
        "chi_bio_range_across_frozen_steps": chi_range,
        "chi_bio_relative_spread_across_frozen_steps": chi_relative_spread,
        "real_part_sign_invariant": sign_invariant,
        "full_rank_observability_all_steps": full_rank_all,
        "steps": steps_out,
    })

status = (
    "CHI_BIO_P0Q_SUPPORTED_MODEL_SPECIFIC"
    if overall_pass and len(case_results) == 3
    else "CHI_BIO_P0Q_REFUSED_NONIDENTIFIABLE"
)

result = {
    "schema_version": "0.1",
    "project": "Bio Chi Investigation",
    "gate": "generator-derived chi_bio scalar qualification",
    "freeze": "BIO_CHI/config/JARUS_CHI_BIO_SCALAR_P0Q_FREEZE_v0_1.json",
    "epistemic_mode": "P0-Q",
    "status": status,
    "native_comparator_disposition": "CHI_BIO_P0Q_EQUIVALENT_TO_NATIVE_POLE_DESCRIPTION",
    "candidate_provenance": "post-result P0-D discovery; not P1 confirmation",
    "model_specific_chi_bio_admissible": status == "CHI_BIO_P0Q_SUPPORTED_MODEL_SPECIFIC",
    "broad_biological_chi_bio_admitted": False,
    "system_scalar_claimed": False,
    "chi_equal_1_boundary_claimed": False,
    "full_state_representation_scope_only": True,
    "scalar_information_loss": [
        "absolute modal timescale omega0",
        "absolute oscillation frequency omega_d",
        "absolute growth or decay rate gamma",
        "remaining real modes and their participation",
    ],
    "cases": case_results,
    "Chi_bio_admitted": False,
    "Bio_Chi_constructed": False,
    "interpretation": (
        "Within the source-native six-state NF-kB model, the unique observable complex-conjugate "
        "invariant factor licenses the canonical mode-specific scalar chi_bio = -Re(lambda)/|lambda|. "
        "This is a P0-Q model-specific admission only. The scalar is an interpretable compression of "
        "the native pole pair and does not add mathematical information beyond it. Negative values "
        "are retained as local amplification. No biological chi=1 boundary or system-level scalar is inferred."
    ),
}

path = OUT / "jarus_chi_bio_scalar_p0q_v0_1.json"
path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))
print(status)
