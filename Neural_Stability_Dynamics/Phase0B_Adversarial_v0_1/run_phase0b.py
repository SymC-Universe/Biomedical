from __future__ import annotations
from pathlib import Path
import csv, json, hashlib, traceback
import numpy as np

from src.synthetic_systems import (
    make_linear_system, simulate_linear, simulate_switch, generate_1f,
    make_noise_bases, add_measurement_noise, truth_modes
)
from src.ssi_cov import decompose, fit_from_decomposition
from src.metrics import match_modes, mac, subspace_similarity, pole_fields

ROOT = Path(__file__).resolve().parent
CP = ROOT / "configs" / "phase0b_design.json"
OUT = ROOT / "results" / "phase0b"
OUT.mkdir(parents=True, exist_ok=True)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path, rows):
    if not rows:
        path.write_text("")
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def run():
    cfg = json.loads(CP.read_text())
    cfg_hash = sha(CP)
    (OUT / "CONFIG_SHA256.txt").write_text(cfg_hash + "\n")

    maxN = max(cfg["durations_samples"])
    fit_rows = []
    match_rows = []
    trial_rows = []
    failures = []
    master = np.random.SeedSequence(cfg["seed"])
    children = master.spawn(len(cfg["systems"]) * cfg["replicates"])
    ci = 0

    for spec in cfg["systems"]:
        for rep in range(cfg["replicates"]):
            base_rng = np.random.default_rng(children[ci])
            ci += 1
            try:
                ss = base_rng.integers(0, 2**32 - 1, size=4, dtype=np.uint32)
                sys_rng = np.random.default_rng(int(ss[0]))
                proc_rng = np.random.default_rng(int(ss[1]))
                noise_rng = np.random.default_rng(int(ss[2]))

                truth_vals = None
                truth_shapes = None
                if spec["kind"] == "linear":
                    A, C = make_linear_system(spec, cfg["n_channels"], sys_rng)
                    clean = simulate_linear(A, C, cfg["dt_seconds"], maxN, cfg["process_scale"], proc_rng)
                    truth_vals, truth_shapes = truth_modes(A, C)
                elif spec["kind"] == "switch":
                    clean = simulate_switch(spec, cfg["n_channels"], cfg["dt_seconds"], maxN, cfg["process_scale"], proc_rng)
                elif spec["kind"] == "null_1f":
                    clean = generate_1f(maxN, cfg["n_channels"], float(spec["beta"]), proc_rng)
                else:
                    raise ValueError("unknown system kind")

                rho = max(float(p["rho"]) for p in cfg["noise_profiles"])
                white_base, colored_base = make_noise_bases(maxN, cfg["n_channels"], rho, noise_rng)

                for profile in cfg["noise_profiles"]:
                    noisy_full = add_measurement_noise(clean, profile, white_base, colored_base)
                    for N in cfg["durations_samples"]:
                        Y = noisy_full[:N].copy()
                        tid = f"{spec['name']}__r{rep:02d}__{profile['name']}__N{N}"
                        segments = {"full": Y, "first_half": Y[:N // 2], "second_half": Y[N // 2:]}
                        for seg_name, Ys in segments.items():
                            try:
                                U, S, p = decompose(Ys, cfg["block_rows"])
                                for order in cfg["candidate_orders"]:
                                    vals, shapes = fit_from_decomposition(U, S, p, order, cfg["dt_seconds"])
                                    for ei, z in enumerate(vals):
                                        pf = pole_fields(z)
                                        fit_rows.append({
                                            "trial_id": tid, "system": spec["name"], "replicate": rep,
                                            "noise_profile": profile["name"], "n_samples": N,
                                            "segment": seg_name, "order": order, "est_index": ei,
                                            "est_real": pf["real"], "est_imag": pf["imag"],
                                            "est_frequency_hz": pf["frequency_hz"],
                                            "est_decay_per_s": pf["decay_per_s"],
                                            "est_stable": pf["stable"],
                                            "singular_value_at_order": float(S[order - 1]),
                                            "singular_value_next": float(S[order]) if order < len(S) else np.nan,
                                        })

                                    if truth_vals is not None:
                                        matches = match_modes(truth_vals, vals)
                                        for ti, ei, dist in matches:
                                            tf = pole_fields(truth_vals[ti])
                                            ef = pole_fields(vals[ei])
                                            match_rows.append({
                                                "trial_id": tid, "system": spec["name"], "replicate": rep,
                                                "noise_profile": profile["name"], "n_samples": N,
                                                "segment": seg_name, "order": order,
                                                "true_index": ti, "est_index": ei,
                                                "normalized_pole_error": dist,
                                                "mode_shape_MAC": mac(truth_shapes[:, ti], shapes[:, ei]),
                                                "true_real": tf["real"], "true_imag": tf["imag"],
                                                "est_real": ef["real"], "est_imag": ef["imag"],
                                                "abs_frequency_error_hz": abs(ef["frequency_hz"] - tf["frequency_hz"]),
                                                "abs_decay_error_per_s": abs(ef["decay_per_s"] - tf["decay_per_s"]),
                                            })
                                        if matches:
                                            tis = [x[0] for x in matches]
                                            eis = [x[1] for x in matches]
                                            ssim = subspace_similarity(truth_shapes[:, tis], shapes[:, eis])
                                        else:
                                            ssim = np.nan
                                        trial_rows.append({
                                            "trial_id": tid, "system": spec["name"], "replicate": rep,
                                            "noise_profile": profile["name"], "n_samples": N,
                                            "segment": seg_name, "order": order,
                                            "truth_state_dimension": len(truth_vals),
                                            "estimated_state_dimension": len(vals),
                                            "matched_truth_fraction": len(matches) / len(truth_vals),
                                            "observable_subspace_similarity": ssim,
                                            "unstable_estimated_poles": int(np.sum(np.real(vals) >= 0)),
                                        })
                                    else:
                                        trial_rows.append({
                                            "trial_id": tid, "system": spec["name"], "replicate": rep,
                                            "noise_profile": profile["name"], "n_samples": N,
                                            "segment": seg_name, "order": order,
                                            "truth_state_dimension": "",
                                            "estimated_state_dimension": len(vals),
                                            "matched_truth_fraction": "",
                                            "observable_subspace_similarity": "",
                                            "unstable_estimated_poles": int(np.sum(np.real(vals) >= 0)),
                                        })
                            except Exception as e:
                                failures.append({
                                    "trial_id": tid, "system": spec["name"], "segment": seg_name,
                                    "error_type": type(e).__name__, "error": str(e),
                                    "traceback": traceback.format_exc(),
                                })
            except Exception as e:
                failures.append({
                    "trial_id": f"{spec['name']}__r{rep:02d}__BASE",
                    "system": spec["name"], "segment": "BASE",
                    "error_type": type(e).__name__, "error": str(e),
                    "traceback": traceback.format_exc(),
                })

    write_csv(OUT / "estimated_poles.csv", fit_rows)
    write_csv(OUT / "truth_matches.csv", match_rows)
    write_csv(OUT / "trial_diagnostics.csv", trial_rows)
    (OUT / "failures.json").write_text(json.dumps(failures, indent=2))

    m = np.array([r["normalized_pole_error"] for r in match_rows if r["segment"] == "full"], float)
    macs = np.array([r["mode_shape_MAC"] for r in match_rows if r["segment"] == "full"], float)
    summary = {
        "schema": "nsd-phase0b-adversarial-result-v0.1",
        "config_sha256": cfg_hash,
        "epistemic_status": "DEVELOPMENT_CALIBRATION_ONLY_NO_ADMISSION_THRESHOLD",
        "base_system_replicates_expected": len(cfg["systems"]) * cfg["replicates"],
        "condition_trials_expected": len(cfg["systems"]) * cfg["replicates"] * len(cfg["noise_profiles"]) * len(cfg["durations_samples"]),
        "candidate_orders": cfg["candidate_orders"],
        "segments": ["full", "first_half", "second_half"],
        "estimated_pole_rows": len(fit_rows),
        "truth_match_rows": len(match_rows),
        "trial_diagnostic_rows": len(trial_rows),
        "failed_fits": len(failures),
        "full_record_truth_match_median_normalized_pole_error": float(np.nanmedian(m)) if len(m) else None,
        "full_record_truth_match_median_MAC": float(np.nanmedian(macs)) if len(macs) else None,
        "next_gate": "analyze failure boundaries; freeze automatic selector/refusal rules and numeric thresholds; create untouched Phase 0C holdout before EEG",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2))
    (OUT / "WORKING_STATE.json").write_text(json.dumps({
        "status": "COMPLETE" if not failures else "COMPLETE_WITH_FAILURES",
        "config_sha256": cfg_hash,
        "failed_fits": len(failures),
        "next_gate": summary["next_gate"],
    }, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    run()
