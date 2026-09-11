from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np

from src.rank_gate import evaluate_rank_signal
from src.synthetic_systems import (
    add_measurement_noise,
    generate_1f,
    make_linear_system,
    make_noise_bases,
    simulate_linear,
)


def _load_freeze(path):
    cfg = json.loads(Path(path).read_text(encoding="utf-8"))
    if cfg.get("status") != "FROZEN_P0_PROSPECTIVE_QUALIFICATION_NOT_P1":
        raise ValueError("P0Q1 freeze status is invalid")
    return cfg


def _system_spec(family):
    keys = {
        "modes",
        "similarity",
        "condition_number",
        "weak_block",
        "weak_scale",
    }
    out = {k: family[k] for k in keys if k in family}
    out.setdefault("similarity", "orthogonal")
    return out


def _add_noise(clean, noise, seed):
    if noise is None:
        return clean
    rng = np.random.default_rng(seed)
    rho = float(noise.get("rho", 0.0))
    white, colored = make_noise_bases(clean.shape[0], clean.shape[1], rho, rng)
    return add_measurement_noise(clean, noise, white, colored)


def _oscillatory_record(cfg, family, replicate):
    seed = int(cfg["seed_base"]) + 10000 * replicate + sum(ord(c) for c in family["name"])
    A, C = make_linear_system(
        _system_spec(family),
        int(cfg["n_channels"]),
        np.random.default_rng(seed),
    )
    clean = simulate_linear(
        A,
        C,
        float(cfg["dt"]),
        int(cfg["n_samples"]),
        float(cfg["process_scale"]),
        np.random.default_rng(seed + 1),
    )
    Y = _add_noise(clean, family.get("noise"), seed + 2)
    return Y


def _refusal_record(cfg, family_name, replicate):
    seed = int(cfg["seed_base"]) + 700000 + 10000 * replicate + sum(ord(c) for c in family_name)
    rng = np.random.default_rng(seed)
    n = int(cfg["n_samples"])
    p = int(cfg["n_channels"])

    if family_name == "iid_white":
        return rng.normal(size=(n, p))
    if family_name == "spatially_mixed_white":
        Z = rng.normal(size=(n, p))
        M = rng.normal(size=(p, p))
        Y = Z @ M.T
        Y -= Y.mean(0, keepdims=True)
        return Y / np.maximum(Y.std(0, keepdims=True), 1e-12)
    if family_name in {"ar1_rho0p6", "ar1_rho0p95"}:
        rho = 0.6 if family_name.endswith("0p6") else 0.95
        _, colored = make_noise_bases(n, p, rho, rng)
        M = rng.normal(size=(p, p))
        Y = colored @ M.T
        Y -= Y.mean(0, keepdims=True)
        return Y / np.maximum(Y.std(0, keepdims=True), 1e-12)
    if family_name.startswith("one_over_f_beta"):
        beta = {
            "one_over_f_beta0p7": 0.7,
            "one_over_f_beta1p4": 1.4,
            "one_over_f_beta2p3": 2.3,
        }[family_name]
        return generate_1f(n, p, beta, rng)
    if family_name == "real_pole_only_linear_system":
        A, C = make_linear_system(
            {
                "modes": [
                    {"type": "real", "pole": -0.7},
                    {"type": "real", "pole": -2.4},
                ],
                "similarity": "orthogonal",
            },
            p,
            rng,
        )
        return simulate_linear(
            A,
            C,
            float(cfg["dt"]),
            n,
            float(cfg["process_scale"]),
            np.random.default_rng(seed + 1),
        )
    raise ValueError(f"unknown refusal family: {family_name}")


def _evaluate_methods(cfg, Y):
    rule = cfg["rank_signal_rule"]
    out = {}
    for method in cfg["methods"]:
        try:
            out[method] = evaluate_rank_signal(
                method,
                Y,
                float(cfg["dt"]),
                cfg["candidate_grid"],
                int(cfg["block_rows"]),
                float(rule["gap_ratio_min"]),
                float(rule["complex_frequency_min_hz"]),
            )
        except Exception as exc:
            out[method] = {
                "status": "METHOD_EXCEPTION_PRESERVED",
                "decision": "METHOD_EXCEPTION",
                "exception_type": type(exc).__name__,
                "exception_message": str(exc),
            }
    return out


def _family_summary(records, method, expected):
    decisions = [r["methods"][method]["decision"] for r in records]
    exceptions = sum(d == "METHOD_EXCEPTION" for d in decisions)
    admits = sum(d == "ADMIT_RANK_SIGNAL" for d in decisions)
    n = len(decisions)
    if expected == "ADMIT_RANK_SIGNAL":
        score = admits / n
    else:
        score = (n - admits) / n
    return {
        "records": n,
        "mechanical_exceptions": exceptions,
        "admit_fraction": admits / n,
        "expected_direction_fraction": score,
        "decision_counts": {d: decisions.count(d) for d in sorted(set(decisions))},
        "candidate_ranks": [
            r["methods"][method].get("candidate_rank") for r in records
        ],
    }


def _method_survival(cfg, oscillatory, refusal, method):
    rule = cfg["prospective_survival_rule"]
    total_exceptions = 0
    oscillatory_ok = True
    refusal_ok = True

    for group in oscillatory:
        s = group["summary"][method]
        total_exceptions += s["mechanical_exceptions"]
        if s["admit_fraction"] < float(rule["oscillatory_family_min_admit_fraction"]):
            oscillatory_ok = False
    for group in refusal:
        s = group["summary"][method]
        total_exceptions += s["mechanical_exceptions"]
        false_admits = int(round(s["admit_fraction"] * s["records"]))
        if false_admits > int(rule["each_refusal_family_false_admits_max"]):
            refusal_ok = False

    survives = (
        total_exceptions <= int(rule["mechanical_exceptions_max"])
        and oscillatory_ok
        and refusal_ok
    )
    return {
        "status": "SURVIVES_P0Q1" if survives else "FAILS_P0Q1",
        "mechanical_exceptions": total_exceptions,
        "all_oscillatory_families_meet_admit_floor": oscillatory_ok,
        "all_refusal_families_meet_false_admit_ceiling": refusal_ok,
    }


def build_record(cfg):
    reps = int(cfg["replicates_per_family"])
    oscillatory = []
    for family in cfg["oscillatory_families_expected_rank_signal"]:
        records = []
        for rep in range(reps):
            Y = _oscillatory_record(cfg, family, rep)
            records.append({"replicate": rep, "methods": _evaluate_methods(cfg, Y)})
        oscillatory.append({
            "family": family["name"],
            "expected": "ADMIT_RANK_SIGNAL",
            "summary": {
                method: _family_summary(records, method, "ADMIT_RANK_SIGNAL")
                for method in cfg["methods"]
            },
            "records": records,
        })

    refusal = []
    for family_name in cfg["refusal_families"]:
        records = []
        for rep in range(reps):
            Y = _refusal_record(cfg, family_name, rep)
            records.append({"replicate": rep, "methods": _evaluate_methods(cfg, Y)})
        refusal.append({
            "family": family_name,
            "expected": "REFUSE_RANK_SIGNAL",
            "summary": {
                method: _family_summary(records, method, "REFUSE_RANK_SIGNAL")
                for method in cfg["methods"]
            },
            "records": records,
        })

    survival = {
        method: _method_survival(cfg, oscillatory, refusal, method)
        for method in cfg["methods"]
    }
    return {
        "schema": "nsd-phase0d-v0.2-p0q1-rank-signal-result-v1",
        "status": "P0_PROSPECTIVE_QUALIFICATION_RESULT_NOT_P1",
        "protocol": cfg["protocol"],
        "freeze_schema": cfg["schema"],
        "hypothesis_provenance": cfg["hypothesis_provenance"],
        "promotion_debt_id": cfg["promotion_debt_id"],
        "p1_authorized": False,
        "rule": cfg["rank_signal_rule"],
        "survival_rule": cfg["prospective_survival_rule"],
        "oscillatory_families": oscillatory,
        "refusal_families": refusal,
        "method_survival": survival,
        "all_methods_survive": all(v["status"] == "SURVIVES_P0Q1" for v in survival.values()),
        "nonclaims": cfg["nonclaims"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--freeze",
        default="configs/P0Q1_RANK_SIGNAL_FREEZE.json",
    )
    parser.add_argument(
        "--output",
        default="results/p0q1/rank_signal_result.json",
    )
    args = parser.parse_args()
    cfg = _load_freeze(args.freeze)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    record = build_record(cfg)
    out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out.resolve())
    for method, status in record["method_survival"].items():
        print(method, status["status"])
    print("P0Q1 RANK-SIGNAL PROSPECTIVE QUALIFICATION COMPLETE. No P1 science was executed.")


if __name__ == "__main__":
    main()
