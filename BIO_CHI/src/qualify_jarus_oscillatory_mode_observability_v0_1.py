#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import math
import pathlib
import numpy as np
from scipy.optimize import least_squares
from scipy.signal import find_peaks

def load_csv(path):
    a = np.loadtxt(path, delimiter=",")
    if a.ndim != 2 or a.shape[1] != 7:
        raise ValueError("trajectory CSV must have 7 columns")
    return a

def get_case(stability, case_id):
    cases = [c for c in stability["cases"] if c["case_id"] == case_id]
    if len(cases) != 1:
        raise ValueError("case not unique")
    roots = cases[0]["roots"]
    roots = roots if isinstance(roots, list) else [roots]
    if len(roots) != 1:
        raise ValueError("accepted root not unique")
    return roots[0]

def extract_pair(stability, case_id):
    root = get_case(stability, case_id)
    step = root["jacobian_steps"][0]
    values = [complex(x, y) for x, y in zip(step["eigenvalues_real"], step["eigenvalues_imag"])]
    nonreal = [z for z in values if abs(z.imag) > 1e-12]
    if len(nonreal) != 2:
        return None, {"nonreal_count": len(nonreal)}
    z1, z2 = nonreal
    conjugate = (
        abs(z1.real - z2.real) <= 1e-10 * max(1.0, abs(z1.real))
        and abs(z1.imag + z2.imag) <= 1e-10 * max(1.0, abs(z1.imag))
    )
    if not conjugate:
        return None, {"nonreal_count": 2, "conjugate": False}
    return (z1 if z1.imag > 0 else z2), {"nonreal_count": 2, "conjugate": True}

def oscillator(par, t, t0):
    c, amp, sigma, omega, phase = par
    return c + amp * np.exp(-sigma * (t - t0)) * np.cos(omega * (t - t0) + phase)

def exponential(par, t, t0):
    c, amp, sigma = par
    return c + amp * np.exp(-sigma * (t - t0))

def fit_oscillator(t, y, t0, sigma_hint, omega_hint):
    c0 = float(np.median(y[-max(5, min(15, len(y))):]))
    amp0 = max(float(np.ptp(y)) / 2.0, 1e-8)
    starts = []
    for sm in [0.5, 1.0, 1.5, 2.0]:
        for om in [0.65, 0.85, 1.0, 1.15, 1.35]:
            for phase in [-math.pi / 2.0, 0.0, math.pi / 2.0]:
                starts.append([c0, amp0, max(sigma_hint * sm, 1e-6), max(omega_hint * om, 1e-6), phase])
                starts.append([c0, -amp0, max(sigma_hint * sm, 1e-6), max(omega_hint * om, 1e-6), phase])
    solutions = []
    for x0 in starts:
        res = least_squares(
            lambda p: oscillator(p, t, t0) - y,
            x0,
            bounds=([-np.inf, -10, 0, 0, -4 * math.pi], [np.inf, 10, 20, 20, 4 * math.pi]),
            max_nfev=30000,
        )
        solutions.append((float(np.sum(res.fun ** 2)), res))
    solutions.sort(key=lambda q: q[0])
    rss, res = solutions[0]
    n = len(y)
    aic = n * math.log(max(rss / n, 1e-300)) + 10
    condition = float(np.linalg.cond(res.jac.T @ res.jac))
    return res.x, rss, aic, condition

def fit_exponential(t, y, t0):
    c0 = float(np.median(y[-max(5, min(15, len(y))):]))
    amp0 = float(y[0] - c0)
    best = None
    for sigma0 in [0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0]:
        res = least_squares(
            lambda p: exponential(p, t, t0) - y,
            [c0, amp0, sigma0],
            bounds=([-np.inf, -10, 0], [np.inf, 10, 20]),
            max_nfev=30000,
        )
        rss = float(np.sum(res.fun ** 2))
        if best is None or rss < best[0]:
            best = (rss, res)
    rss, res = best
    n = len(y)
    aic = n * math.log(max(rss / n, 1e-300)) + 6
    return res.x, rss, aic

def qualify(stability, trajectory, semantic, criteria, known_bad=False):
    pair, pair_meta = extract_pair(stability, "FIG8A_NOMINAL_DAMPED")
    out = {"pair_meta": pair_meta, "known_bad": known_bad}
    if pair is None or pair.real >= 0:
        out.update(status="REFUSE_NO_UNIQUE_STABLE_COMPLEX_PAIR", pass_gate=False)
        return out

    sigma_gen = -pair.real * 3600.0
    omega_gen = abs(pair.imag) * 3600.0
    chi_gen = sigma_gen / math.hypot(sigma_gen, omega_gen)

    onset = float(semantic["tnf_onset_h"])
    t = trajectory[:, 0]
    y = trajectory[:, 3]
    post = t > onset
    tp, yp = t[post], y[post]
    minima = find_peaks(-yp)[0]
    if len(minima) == 0:
        out.update(status="REFUSE_NO_POST_ONSET_MINIMUM", pass_gate=False)
        return out

    t0 = float(tp[minima[0]])
    use = t >= t0
    tf, yf = t[use], y[use]
    if len(tf) < 12:
        out.update(status="REFUSE_TOO_FEW_POST_START_POINTS", pass_gate=False)
        return out

    p, rss, aic, condition = fit_oscillator(tf, yf, t0, sigma_gen, omega_gen)
    p_exp, rss_exp, aic_exp = fit_exponential(tf, yf, t0)
    c, amp, sigma, omega, phase = [float(v) for v in p]
    chi_obs = sigma / math.hypot(sigma, omega) if omega > 0 else float("nan")
    post_range = float(np.ptp(yp))
    amplitude_fraction = abs(amp) / post_range if post_range > 0 else 0.0
    cycles = float(tf[-1] - tf[0]) * omega / (2.0 * math.pi)

    def rel(a, b):
        return abs(a - b) / abs(b)

    checks = {
        "unique_complex_pair": pair_meta.get("conjugate", False) and pair_meta.get("nonreal_count") == 2,
        "stable_pair": pair.real < 0,
        "delta_aic": float(aic_exp - aic) >= criteria["minimum_delta_aic_oscillator_vs_exponential"],
        "omega_match": rel(omega, omega_gen) <= criteria["maximum_relative_error_omega"],
        "sigma_match": rel(sigma, sigma_gen) <= criteria["maximum_relative_error_sigma"],
        "chi_match": rel(chi_obs, chi_gen) <= criteria["maximum_relative_error_chi"],
        "amplitude_fraction": amplitude_fraction >= criteria["minimum_oscillatory_amplitude_fraction_of_post_onset_range"],
        "complete_cycles": cycles >= criteria["minimum_post_start_complete_cycles"],
        "finite_condition": math.isfinite(condition) and condition <= criteria["finite_parameter_jacobian_condition_max"],
    }
    passed = all(checks.values())
    out.update(
        status="PASS_P0Q_OSCILLATORY_MODE_OBSERVABILITY" if passed else "REFUSE_P0Q_OSCILLATORY_MODE_OBSERVABILITY",
        pass_gate=passed,
        checks=checks,
        fit_start_h=t0,
        n_fit=int(len(tf)),
        generator={
            "re_s^-1": pair.real,
            "im_s^-1": pair.imag,
            "sigma_h^-1": sigma_gen,
            "omega_h^-1": omega_gen,
            "chi": chi_gen,
        },
        observable_fit={
            "offset": c,
            "amplitude": amp,
            "sigma_h^-1": sigma,
            "omega_h^-1": omega,
            "phase": phase,
            "chi": chi_obs,
            "rss": rss,
            "aic": aic,
            "jtj_condition": condition,
        },
        simple_exponential={"params": [float(v) for v in p_exp], "rss": rss_exp, "aic": aic_exp},
        diagnostics={
            "delta_aic_oscillator_vs_exponential": float(aic_exp - aic),
            "relative_error_omega": rel(omega, omega_gen),
            "relative_error_sigma": rel(sigma, sigma_gen),
            "relative_error_chi": rel(chi_obs, chi_gen),
            "amplitude_fraction": amplitude_fraction,
            "post_start_cycles": cycles,
        },
    )
    return out

def known_bad_test(stability, trajectory, semantic, criteria):
    bad = trajectory.copy()
    onset = float(semantic["tnf_onset_h"])
    t = bad[:, 0]
    base = 0.27
    y = np.zeros_like(t)
    y[t <= onset] = base
    mask = t > onset
    y[mask] = base + 0.70 * np.exp(-0.8 * (t[mask] - onset))
    bad[:, 3] = y
    result = qualify(stability, bad, semantic, criteria, known_bad=True)
    if result["pass_gate"]:
        raise SystemExit("KNOWN_BAD_UNEXPECTED_PASS")
    return result

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stability-json", required=True)
    ap.add_argument("--trajectory-csv", required=True)
    ap.add_argument("--semantic-json", required=True)
    ap.add_argument("--freeze-json", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--self-test-out", required=True)
    args = ap.parse_args()

    stability = json.load(open(args.stability_json, encoding="utf-8"))
    semantic = json.load(open(args.semantic_json, encoding="utf-8"))
    freeze = json.load(open(args.freeze_json, encoding="utf-8"))
    trajectory = load_csv(args.trajectory_csv)
    criteria = dict(freeze["qualification_criteria"])
    criteria.pop("note", None)
    criteria.pop("unique_complex_pair", None)
    criteria.pop("stable_pair_required", None)

    bad = known_bad_test(stability, trajectory, semantic, criteria)
    result = qualify(stability, trajectory, semantic, criteria)
    result.update(
        schema_version="0.1",
        project="Bio Chi Investigation",
        epistemic_status="P0_Q_POSTRESULT_QUALIFICATION",
        freeze="BIO_CHI/config/JARUS_OSCILLATORY_MODE_OBSERVABILITY_P0Q_FREEZE_v0_1.json",
        chi_bio_admitted=False,
        Chi_bio_admitted=False,
        Bio_Chi_constructed=False,
        interpretation="A PASS qualifies the frozen NF-kB oscillatory-mode candidate to face a separately frozen independent test. It does not confirm or admit chi_bio, Chi_bio, or Bio Chi.",
    )
    pathlib.Path(args.out).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    pathlib.Path(args.self_test_out).write_text(json.dumps(bad, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    print("KNOWN_BAD=PASS_REFUSAL")
    print("BIO_CHI_JARUS_OBSERVABILITY_P0Q=" + ("PASS" if result["pass_gate"] else "REFUSE"))

if __name__ == "__main__":
    main()
