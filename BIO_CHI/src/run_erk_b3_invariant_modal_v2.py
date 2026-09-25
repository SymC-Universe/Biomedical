#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import pathlib

import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm

from reproduce_blum_b3_native_v02 import rhs_factory, pool_matrix
from analyze_blum_b3_generator_transport_v02 import (
    stoichiometry, initial_state, analytic_jacobian, measurement_complex,
    measurement_gradient_complex_step, find_equilibrium, lane_params
)

ROOT = pathlib.Path(__file__).resolve().parents[2]
CFG = ROOT / "BIO_CHI" / "config"
OUT = ROOT / "BIO_CHI" / "artifacts" / "generated" / "erk_b3_invariant_modal_v2"
OUT.mkdir(parents=True, exist_ok=True)

PRIMARY_FRACTIONS = (1e-3, 1e-4)
SENSITIVITY_FRACTION = 1e-5


def deterministic_fret_series(p, Y):
    return np.array(
        [float(np.real(measurement_complex(p, Y[:, k]))) for k in range(Y.shape[1])],
        dtype=float,
    )


def relative_error(actual, pred):
    den = float(np.linalg.norm(pred))
    if den <= 1e-14:
        return None
    return float(np.linalg.norm(actual - pred) / den)


def integrate(rhs, x0, t):
    sol = solve_ivp(
        rhs,
        (float(t[0]), float(t[-1])),
        x0,
        t_eval=t,
        method="BDF",
        rtol=1e-10,
        atol=1e-12,
    )
    if not sol.success or sol.y.shape != (15, t.size) or not np.all(np.isfinite(sol.y)):
        return None
    return sol.y


def safe_scale(x, direction):
    d = np.asarray(direction, dtype=float)
    n = float(np.linalg.norm(d))
    if not math.isfinite(n) or n <= 0:
        return None
    d = d / n
    neg = d < 0
    if np.any(neg):
        lim = float(np.min(x[neg] / (-d[neg])))
    else:
        lim = float("inf")
    eqnorm = float(np.linalg.norm(x, 2))
    base = min(eqnorm, 0.5 * lim) if math.isfinite(lim) else eqnorm
    if not math.isfinite(base) or base <= 0:
        return None
    return base, d, lim


def source_key(lane, ctx_id):
    prefix = "primary" if lane == "primary" else "sensitivity"
    suffix = "FGF_2p5" if ctx_id == "SUSTAINED_FGF_2P5" else "FGF_250"
    return f"{prefix}_{suffix}"


def phase_fix_complex(v, Cr):
    proj = Cr @ v
    if abs(proj) > 0:
        return v * np.exp(-1j * np.angle(proj)), "FRET_PHASE"
    k = int(np.argmax(np.abs(v)))
    if abs(v[k]) == 0:
        return None, "ZERO_VECTOR"
    return v * np.exp(-1j * np.angle(v[k])), "LARGEST_COMPONENT_PHASE"


def carrier_inventory(vals, V, Q, Cr):
    scale = max(float(np.max(np.abs(vals))), np.finfo(float).tiny)
    floor = math.sqrt(np.finfo(float).eps) * scale
    real_idx = [i for i, z in enumerate(vals) if abs(float(z.imag)) <= floor]
    pos_idx = [i for i, z in enumerate(vals) if float(z.imag) > floor]
    neg_idx = [i for i, z in enumerate(vals) if float(z.imag) < -floor]

    carriers = []

    for i in real_idx:
        lam = vals[i]
        vr = np.real(V[:, i])
        phys = Q @ vr
        n = float(np.linalg.norm(phys))
        if n <= 0 or not math.isfinite(n):
            carriers.append({
                "carrier_type": "REAL_MODE",
                "mode_indices": [int(i)],
                "status": "INDETERMINATE_ZERO_REAL_EIGENVECTOR",
            })
            continue
        d = phys / n
        carriers.append({
            "carrier_type": "REAL_MODE",
            "mode_indices": [int(i)],
            "lambda_real": float(lam.real),
            "lambda_imag": float(lam.imag),
            "directions": [
                {"id": "REAL_PLUS", "vector": d},
                {"id": "REAL_MINUS", "vector": -d},
            ],
            "analytic_kind": "REAL",
            "analytic_vector": phys,
            "phase_rule": "BOTH_SIGNS",
            "classification_floor": floor,
        })

    used = set()
    for i in pos_idx:
        candidates = [j for j in neg_idx if j not in used]
        if not candidates:
            carriers.append({
                "carrier_type": "COMPLEX_PAIR",
                "mode_indices": [int(i)],
                "status": "INDETERMINATE_UNMATCHED_COMPLEX_MODE",
            })
            continue
        j = min(candidates, key=lambda j: abs(vals[j] - np.conj(vals[i])))
        used.add(j)
        lam = vals[i]
        vf, phase_rule = phase_fix_complex(V[:, i], Cr)
        if vf is None:
            carriers.append({
                "carrier_type": "COMPLEX_PAIR",
                "mode_indices": [int(i), int(j)],
                "status": "INDETERMINATE_ZERO_COMPLEX_EIGENVECTOR",
            })
            continue
        w = Q @ vf
        re = np.real(w)
        im = np.imag(w)
        nr = float(np.linalg.norm(re))
        ni = float(np.linalg.norm(im))
        if nr <= 0 or ni <= 0 or not math.isfinite(nr) or not math.isfinite(ni):
            carriers.append({
                "carrier_type": "COMPLEX_PAIR",
                "mode_indices": [int(i), int(j)],
                "status": "INDETERMINATE_DEGENERATE_REAL_SUBSPACE_BASIS",
            })
            continue
        carriers.append({
            "carrier_type": "COMPLEX_PAIR",
            "mode_indices": [int(i), int(j)],
            "lambda_real": float(lam.real),
            "lambda_imag": float(lam.imag),
            "chi_bio_i": float(-lam.real / abs(lam)),
            "directions": [
                {"id": "PAIR_RE_PLUS", "vector": re / nr, "component": "REAL", "sign": 1},
                {"id": "PAIR_RE_MINUS", "vector": -re / nr, "component": "REAL", "sign": -1},
                {"id": "PAIR_IM_PLUS", "vector": im / ni, "component": "IMAG", "sign": 1},
                {"id": "PAIR_IM_MINUS", "vector": -im / ni, "component": "IMAG", "sign": -1},
            ],
            "analytic_kind": "COMPLEX",
            "analytic_vector": w,
            "phase_rule": phase_rule,
            "classification_floor": floor,
        })

    accounted = len(real_idx) + 2 * len(pos_idx)
    return carriers, {
        "classification_floor": floor,
        "real_mode_count": len(real_idx),
        "complex_pair_count": len(pos_idx),
        "accounted_dimension": accounted,
        "expected_dimension": len(vals),
    }


def analytic_prediction(carrier, direction, amplitude, t):
    lam = complex(carrier["lambda_real"], carrier["lambda_imag"])
    if carrier["analytic_kind"] == "REAL":
        base = np.asarray(carrier["analytic_vector"], dtype=float)
        base = base / np.linalg.norm(base)
        sign = 1.0 if direction["id"].endswith("PLUS") else -1.0
        return np.column_stack([
            sign * amplitude * base * math.exp(float(lam.real) * float(tt))
            for tt in t
        ])

    w = np.asarray(carrier["analytic_vector"], dtype=complex)
    comp = direction["component"]
    sign = float(direction["sign"])
    if comp == "REAL":
        den = float(np.linalg.norm(np.real(w)))
        return np.column_stack([
            sign * amplitude * np.real(w * np.exp(lam * float(tt))) / den
            for tt in t
        ])
    den = float(np.linalg.norm(np.imag(w)))
    return np.column_stack([
        sign * amplitude * np.imag(w * np.exp(lam * float(tt))) / den
        for tt in t
    ])


def horizon_for(carrier):
    lr = float(carrier["lambda_real"])
    li = abs(float(carrier["lambda_imag"]))
    if carrier["carrier_type"] == "REAL_MODE":
        if lr >= 0:
            return None, "NONDECAY_REAL_MODE"
        return 5.0 / abs(lr), "FIVE_EFOLD_DECAY"
    if li <= 0:
        return None, "ZERO_COMPLEX_FREQUENCY"
    return 4.0 * math.pi / li, "TWO_LOCAL_PERIODS"


def direction_roundtrip(p, rhs, xstar, Q, Jr, grad, carrier, direction, samples):
    h, h_rule = horizon_for(carrier)
    if h is None:
        return {
            "direction_id": direction["id"],
            "status": "REFUSE_ERK_NONDECAY_REAL_MODE_V2",
            "horizon_rule": h_rule,
        }

    scale = safe_scale(xstar, direction["vector"])
    if scale is None:
        return {
            "direction_id": direction["id"],
            "status": "INDETERMINATE_POSITIVITY_SCALE",
            "horizon_rule": h_rule,
        }
    base, d, positive_limit = scale
    t = np.linspace(0.0, h, samples)

    check_amp = 1e-4 * base
    delta_check = check_amp * d
    analytic = analytic_prediction(carrier, direction, check_amp, t)
    z0 = Q.T @ delta_check
    full_linear = np.column_stack([Q @ (expm(Jr * float(tt)) @ z0) for tt in t])
    self_den = max(float(np.linalg.norm(analytic, "fro")), np.finfo(float).tiny)
    self_err = float(np.linalg.norm(analytic - full_linear, "fro") / self_den)
    self_pass = bool(self_err <= 1e-9)

    h0 = float(np.real(measurement_complex(p, xstar)))
    amp_records = []
    for frac in (*PRIMARY_FRACTIONS, SENSITIVITY_FRACTION):
        amp = float(frac * base)
        x0 = xstar + amp * d
        if float(np.min(x0)) < -1e-12:
            amp_records.append({
                "fraction": frac,
                "status": "INDETERMINATE_POSITIVITY_SCALE",
            })
            continue
        Y = integrate(rhs, x0, t)
        if Y is None:
            amp_records.append({
                "fraction": frac,
                "status": "INDETERMINATE_NUMERICAL",
            })
            continue
        pred = analytic_prediction(carrier, direction, amp, t)
        actual = Y - xstar[:, None]
        state_err = float(
            np.linalg.norm(actual - pred, "fro")
            / max(float(np.linalg.norm(pred, "fro")), np.finfo(float).tiny)
        )
        fret_actual = deterministic_fret_series(p, Y) - h0
        fret_pred = grad @ pred
        fret_err = relative_error(fret_actual, fret_pred)
        amp_records.append({
            "fraction": frac,
            "absolute_amplitude": amp,
            "all_state_relative_error": state_err,
            "FRET_relative_error": fret_err,
            "minimum_nonlinear_state": float(np.min(Y)),
            "status": "COMPLETE",
        })

    prim = {r["fraction"]: r for r in amp_records if r.get("status") == "COMPLETE"}
    primary_complete = 1e-3 in prim and 1e-4 in prim
    state_pass = (
        primary_complete
        and prim[1e-4]["all_state_relative_error"] < prim[1e-3]["all_state_relative_error"]
    )
    if primary_complete:
        f1 = prim[1e-3]["FRET_relative_error"]
        f2 = prim[1e-4]["FRET_relative_error"]
        fret_pass = True if (f1 is None or f2 is None) else (f2 < f1)
    else:
        fret_pass = False
    primary_pass = bool(primary_complete and state_pass and fret_pass and self_pass)

    return {
        "direction_id": direction["id"],
        "status": "PASS" if primary_pass else "FAIL",
        "horizon_minutes": float(h),
        "horizon_rule": h_rule,
        "safe_scale": float(base),
        "positive_step_limit": float(positive_limit),
        "analytic_vs_full_linear_relative_state_error": self_err,
        "implementation_self_check_pass": self_pass,
        "amplitudes": amp_records,
        "primary_state_convergence_pass": bool(state_pass),
        "primary_FRET_convergence_pass": bool(fret_pass),
        "primary_pass": primary_pass,
    }


def compare_complex_pairs_to_pin(carriers, pin_record):
    got = sorted(
        float(c["chi_bio_i"])
        for c in carriers
        if c.get("carrier_type") == "COMPLEX_PAIR" and "chi_bio_i" in c
    )
    exp = sorted(float(x["chi_bio_i"]) for x in pin_record["complex_pairs"])
    if len(got) != len(exp):
        return False, {"reason": "pair_count", "got": len(got), "expected": len(exp)}
    diffs = [abs(a - b) for a, b in zip(got, exp)]
    return max(diffs, default=0.0) <= 1e-9, {"chi_abs_differences": diffs}


def main():
    freeze = json.loads((CFG / "ERK_B3_INVARIANT_MODAL_V2_FREEZE_v0_1.json").read_text())
    src = json.loads((CFG / "BLUM_B3_TRANSPORT_SOURCE_FREEZE_v0_2.json").read_text())
    genpin = json.loads((CFG / "BLUM_B3_GENERATOR_TRANSPORT_V02_RESULT_PIN.json").read_text())
    v1 = json.loads((CFG / "BLUM_B3_LOCAL_NONLINEAR_ROUNDTRIP_V01_RESULT_PIN.json").read_text())
    limit = json.loads((CFG / "ERK_B3_LIMIT_MAP_V01.json").read_text())

    if genpin.get("status") != "PASS_B3_GENERATOR_MODAL_QUALIFICATION":
        raise SystemExit("ERK_MODAL_V2_REQUIRES_GENERATOR_PASS")
    if v1.get("status") != "FAIL_B3_FULL_MODAL_LOCAL_ROUNDTRIP":
        raise SystemExit("ERK_MODAL_V2_REQUIRES_PRESERVED_V1_FAILURE")
    if limit.get("status") != "ESTABLISHED_P0Q_LIMIT":
        raise SystemExit("ERK_MODAL_V2_REQUIRES_FROZEN_V1_LIMIT")

    S = stoichiometry()
    U, _, _ = np.linalg.svd(S, full_matrices=False)
    Q = U[:, :8]
    Cpool = pool_matrix()
    samples = int(freeze["nonlinear_roundtrip"]["samples"])

    contexts = []
    any_real_fail = False
    any_complex_fail = False
    any_self_fail = False
    any_nondecay_real = False
    any_indeterminate = False
    all_contexts_pass = True

    for lane in freeze["parameter_lanes"]:
        p = lane_params(src, lane)
        for ctx in freeze["input_contexts"]:
            ctx_id = ctx["id"]
            fgf = float(ctx["fgf_input"])
            rhs = rhs_factory(p, fgf)
            y0 = initial_state(p)
            xstar, horizon, attempts = find_equilibrium(
                rhs,
                y0,
                Cpool,
                {"candidate_horizons_minutes": [1000, 10000, 100000]},
            )
            if xstar is None:
                contexts.append({
                    "lane": lane,
                    "context": ctx_id,
                    "status": "INDETERMINATE_EQUILIBRIUM",
                    "attempts": attempts,
                })
                any_indeterminate = True
                all_contexts_pass = False
                continue

            J = analytic_jacobian(p, fgf, S, xstar)
            Jr = Q.T @ J @ Q
            vals, V = np.linalg.eig(Jr)
            grad = measurement_gradient_complex_step(p, xstar)
            Cr = grad @ Q

            carriers, inventory = carrier_inventory(vals, V, Q, Cr)
            pin_ok, pin_check = compare_complex_pairs_to_pin(
                carriers,
                genpin["records"][source_key(lane, ctx_id)],
            )
            if not pin_ok:
                contexts.append({
                    "lane": lane,
                    "context": ctx_id,
                    "status": "FAIL_ERK_MODAL_IMPLEMENTATION_SELF_CHECK_V2",
                    "generator_pin_check": pin_check,
                })
                any_self_fail = True
                all_contexts_pass = False
                continue

            carrier_results = []
            context_pass = True
            for ci, carrier in enumerate(carriers):
                if carrier.get("status", "").startswith("INDETERMINATE"):
                    carrier_results.append({
                        "carrier_index": ci,
                        **{k: v for k, v in carrier.items() if k != "directions"},
                    })
                    any_indeterminate = True
                    context_pass = False
                    continue

                dirs = []
                carrier_pass = True
                for direction in carrier["directions"]:
                    dr = direction_roundtrip(
                        p, rhs, xstar, Q, Jr, grad, carrier, direction, samples
                    )
                    dirs.append(dr)
                    if dr["status"] == "REFUSE_ERK_NONDECAY_REAL_MODE_V2":
                        any_nondecay_real = True
                        carrier_pass = False
                    elif dr["status"] != "PASS":
                        carrier_pass = False
                        if dr["status"].startswith("INDETERMINATE"):
                            any_indeterminate = True
                    if not dr.get("implementation_self_check_pass", True):
                        any_self_fail = True

                if carrier["carrier_type"] == "REAL_MODE" and not carrier_pass:
                    any_real_fail = True
                if carrier["carrier_type"] == "COMPLEX_PAIR" and not carrier_pass:
                    any_complex_fail = True
                context_pass = context_pass and carrier_pass

                rec = {
                    "carrier_index": ci,
                    "carrier_type": carrier["carrier_type"],
                    "mode_indices": carrier["mode_indices"],
                    "lambda_real": carrier["lambda_real"],
                    "lambda_imag": carrier["lambda_imag"],
                    "phase_rule": carrier.get("phase_rule"),
                    "primary_pass": bool(carrier_pass),
                    "direction_results": dirs,
                }
                if "chi_bio_i" in carrier:
                    rec["chi_bio_i"] = carrier["chi_bio_i"]
                carrier_results.append(rec)

            all_contexts_pass = all_contexts_pass and context_pass
            contexts.append({
                "lane": lane,
                "context": ctx_id,
                "fgf_input": fgf,
                "status": "PASS" if context_pass else "FAIL",
                "equilibrium_horizon_minutes": horizon,
                "carrier_inventory": inventory,
                "generator_pin_check": pin_check,
                "carrier_results": carrier_results,
                "context_pass": bool(context_pass),
            })

    if any_self_fail:
        status = "FAIL_ERK_MODAL_IMPLEMENTATION_SELF_CHECK_V2"
    elif any_nondecay_real:
        status = "REFUSE_ERK_NONDECAY_REAL_MODE_V2"
    elif any_indeterminate:
        status = "INDETERMINATE_ERK_MODAL_V2"
    elif any_complex_fail:
        status = "FAIL_ERK_COMPLEX_SUBSPACE_ROUNDTRIP_V2"
    elif any_real_fail:
        status = "FAIL_ERK_REAL_MODE_CARRIER_ROUNDTRIP_V2"
    elif all_contexts_pass:
        status = "PASS_ERK_INVARIANT_MODAL_ROUNDTRIP_V2"
    else:
        status = "INDETERMINATE_ERK_MODAL_V2"

    result = {
        "schema_version": "0.1",
        "project": "Bio Chi Investigation",
        "gate": "ERK B3 invariant-modal carrier nonlinear round-trip v2",
        "freeze": "BIO_CHI/config/ERK_B3_INVARIANT_MODAL_V2_FREEZE_v0_1.json",
        "epistemic_mode": "P0-Q",
        "status": status,
        "v1_limit_retained": True,
        "v1_limit_pin": "BIO_CHI/config/ERK_B3_LIMIT_MAP_V01.json",
        "all_contexts_pass": bool(all_contexts_pass),
        "contexts": contexts,
        "ERK_Chi_bio_v2_admissible": bool(status == "PASS_ERK_INVARIANT_MODAL_ROUNDTRIP_V2"),
        "broad_biological_Chi_bio_transport_established": False,
        "Bio_Chi_cross_system_transport_opened": False,
        "P1_confirmation_claimed": False,
        "interpretation_limit": (
            "This v2 gate tests all local invariant modal carriers of the same qualified ERK generator. "
            "It does not erase the v1 arbitrary-direction Limit Map and does not itself establish whole-system Bio Chi transport."
        ),
    }

    out = OUT / "erk_b3_invariant_modal_v2_result.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    print(status)


if __name__ == "__main__":
    main()
