#!/usr/bin/env python3
"""NSD long-run evidence conveyor v0.1.

Execution plumbing only. Scientific authority remains with the researcher and
ChatGPT. This runner never promotes/refuses a scientific claim and terminates
at SCIENTIFIC_REVIEW_READY after generating frozen known-truth evidence.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
from typing import Any

import numpy as np
import scipy
from scipy.linalg import expm

HERE = Path(__file__).resolve()
ENGINE_ROOT = HERE.parents[1]
NSD_ROOT = HERE.parents[2]
REPO_ROOT = HERE.parents[3]
TOOLS_ROOT = HERE.parent
for p in (ENGINE_ROOT, TOOLS_ROOT):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from nsd_engine.continuous_lineage_candidate_rs import fit_continuous_lineage_candidate_rs
from nsd_engine.coupled_second_order import CoupledSecondOrder2Mode
from nsd_engine.state_space_adequacy import compare_state_space_candidates
from probe_combined_structural_predictive_refusal import (
    arma_second_order_signal,
    colored_process_signal,
    continuous_c_signal,
    scalar_positive_bound,
    structural_metrics,
    two_mode_signal,
)
from probe_single_series_uncertainty_methods import (
    hessian_diagnostic,
    profile_case,
    standardize,
)

CONTROL = NSD_ROOT / "control"
PACKET = CONTROL / "LONG_RUN_PACKET_v0.1.json"
NB2_CONFIG = CONTROL / "NB2NB3_EXACT_MATCHED_CONFIG_v0.1.json"
CEILING = CONTROL / "LONG_RUN_CEILING_v0.1.md"
APQ = CONTROL / "LONG_RUN_PACKET_APQ_v0.1.md"
EXTERNAL_APQ = CONTROL / "LONG_RUN_EXTERNAL_APQ_STATUS_v0.1.json"
CHECKPOINT = CONTROL / "LONG_RUN_CHECKPOINT_v0.1.json"
RESULTS = NSD_ROOT / "results" / "long_run_v0_1"
NB1_DIR = RESULTS / "nb1"
NB2_DIR = RESULTS / "nb2_nb3"
MANIFEST = RESULTS / "evidence_manifest.json"

START = time.time()
DEFAULT_RUNTIME_MIN = 330
DEFAULT_RESERVE_MIN = 15
CHECKPOINT_COMMIT_EVERY = 4


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_digest(obj: Any) -> str:
    return sha256_bytes(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode())


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


PACK = load_json(PACKET)
NB2CFG = load_json(NB2_CONFIG)
PACKET_DIGEST = canonical_digest(PACK)
NB2_DIGEST = canonical_digest(NB2CFG)
RUNTIME_MIN = int(PACK.get("runtime_minutes", DEFAULT_RUNTIME_MIN))
RESERVE_MIN = int(PACK.get("runtime_reserve_minutes", DEFAULT_RESERVE_MIN))


def env_record() -> dict[str, Any]:
    return {
        "python_version": sys.version,
        "platform": platform.platform(),
        "numpy_version": np.__version__,
        "scipy_version": scipy.__version__,
        "github_sha": os.environ.get("GITHUB_SHA"),
        "github_run_id": os.environ.get("GITHUB_RUN_ID"),
        "github_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
        "packet_digest": PACKET_DIGEST,
        "nb2_config_digest": NB2_DIGEST,
    }


def fresh_checkpoint() -> dict[str, Any]:
    return {
        "schema": "NSD_LONG_RUN_CHECKPOINT_V0_1",
        "packet_digest": PACKET_DIGEST,
        "nb2_config_digest": NB2_DIGEST,
        "stage": "PACKET_BOUND",
        "started_unix": START,
        "updated_unix": time.time(),
        "completed_nb1_cases": [],
        "completed_nb2_families": [],
        "completed_stages": [],
        "stop_reason": None,
        "next_exact_mechanical_action": "validate frozen inputs",
        "scientific_verdict": "FORBIDDEN",
        "environment": env_record(),
    }


def read_checkpoint() -> dict[str, Any]:
    if not CHECKPOINT.exists():
        return fresh_checkpoint()
    cp = load_json(CHECKPOINT)
    if cp.get("packet_digest") != PACKET_DIGEST or cp.get("nb2_config_digest") != NB2_DIGEST:
        raise RuntimeError("FROZEN_CONTRACT_VIOLATION: checkpoint/config digest mismatch")
    return cp


CP = read_checkpoint()


def write_checkpoint(stage: str, next_action: str, stop_reason: str | None = None) -> None:
    CP["stage"] = stage
    CP["updated_unix"] = time.time()
    CP["next_exact_mechanical_action"] = next_action
    CP["stop_reason"] = stop_reason
    CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)
    CHECKPOINT.write_text(json.dumps(CP, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def git_checkpoint(message: str) -> None:
    if os.environ.get("GITHUB_ACTIONS") != "true":
        return
    paths = [str(CHECKPOINT.relative_to(REPO_ROOT))]
    if RESULTS.exists() and any(p.is_file() for p in RESULTS.rglob("*")):
        paths.append(str(RESULTS.relative_to(REPO_ROOT)))
    subprocess.run(["git", "add", "--"] + paths, cwd=REPO_ROOT, check=True)
    staged = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=REPO_ROOT)
    if staged.returncode == 0:
        return
    subprocess.run(["git", "commit", "-m", message], cwd=REPO_ROOT, check=True)
    subprocess.run(
        ["git", "push", "origin", "HEAD:nsd-rebuild-gom-v0.8.0"],
        cwd=REPO_ROOT,
        check=True,
    )


def near_runtime_reserve() -> bool:
    elapsed = (time.time() - START) / 60.0
    return elapsed >= max(1, RUNTIME_MIN - RESERVE_MIN)


def runtime_checkpoint_if_needed(next_action: str) -> bool:
    if not near_runtime_reserve():
        return False
    write_checkpoint("CHECKPOINTED_RUNTIME_RESERVE", next_action, "RUNTIME_RESERVE")
    git_checkpoint("NSD conveyor: runtime-reserve checkpoint")
    return True


def validate_contract() -> None:
    required = [PACKET, NB2_CONFIG, CEILING, APQ, EXTERNAL_APQ]
    for p in required:
        if not p.exists():
            raise RuntimeError(f"FROZEN_CONTRACT_VIOLATION: missing {p}")
    gate = load_json(EXTERNAL_APQ)
    if gate.get("status") != "QUALIFIED" or not gate.get("execution_authorized"):
        raise RuntimeError("SCIENTIFIC_GATE: independent APQ status is not QUALIFIED")
    if PACK.get("ceiling") != "SCIENTIFIC_REVIEW_READY":
        raise RuntimeError("FROZEN_CONTRACT_VIOLATION: unexpected ceiling")
    if not PACK["lanes"]["NB1"].get("scientific_verdict_forbidden"):
        raise RuntimeError("FROZEN_CONTRACT_VIOLATION: NB1 verdict firewall absent")
    if not PACK["lanes"]["NB2NB3"].get("scientific_verdict_forbidden"):
        raise RuntimeError("FROZEN_CONTRACT_VIOLATION: NB2 verdict firewall absent")
    if not NB2CFG.get("scientific_verdict_forbidden"):
        raise RuntimeError("FROZEN_CONTRACT_VIOLATION: NB2 config verdict firewall absent")


def run_tests() -> None:
    cmd = [
        sys.executable, "-m", "pytest", "-q",
        "tests/test_continuous_lineage_rs_contracts.py",
        "tests/test_coupled_second_order.py",
        "tests/test_state_space_adequacy.py",
        "tests/test_structural_order_refusal_contracts.py",
        "tests/test_substrate_closure_contracts.py",
    ]
    subprocess.run(cmd, cwd=ENGINE_ROOT, check=True)


def nb1_geometry(spec: dict[str, Any], fs: float) -> dict[str, float]:
    A = float(spec["base_A"])
    fn = float(spec["base_fn_hz"])
    zeta = float(spec["base_chi"])
    omega_n = 2.0 * math.pi * fn
    alpha = zeta * omega_n
    nu = omega_n * math.sqrt(1.0 - zeta * zeta)
    L = alpha / fs
    rho = math.exp(-L)
    theta = nu / fs
    xi = math.cos(theta)
    H_C = A * L * math.sin(theta) / theta
    H_D = A * math.sinh(L)
    S_pos = scalar_positive_bound(A, rho, xi, +1, H_D)
    S_neg = scalar_positive_bound(A, rho, xi, -1, H_D)
    return dict(A=A, fn=fn, zeta=zeta, rho=rho, xi=xi, H_C=H_C, H_D=H_D, S_pos=S_pos, S_neg=S_neg)


def generate_nb1_fine(spec: dict[str, Any], seed: int, fs: float, seconds: float) -> tuple[np.ndarray, dict[str, Any]]:
    gen = spec["generator"]
    if gen == "CONTINUOUS_C":
        sig = continuous_c_signal(
            fs=fs, seconds=seconds, A=float(spec["A"]), fn=float(spec["fn_hz"]),
            zeta=float(spec["chi"]), g=float(spec["g"]), seed=seed,
        )
        return sig, {
            "semantic_truth": "C_MEMBER",
            "true_chi_defined": True,
            "true_chi": float(spec["chi"]),
            "truth_coordinates": spec,
        }
    if gen in {"D_NOT_C_POS", "D_NOT_C_NEG", "S_NOT_D_POS", "S_NOT_D_NEG"}:
        g = nb1_geometry(spec, fs)
        if gen == "D_NOT_C_POS":
            H = g["H_C"] + 0.5 * (g["H_D"] - g["H_C"])
        elif gen == "D_NOT_C_NEG":
            H = -(g["H_C"] + 0.5 * (g["H_D"] - g["H_C"]))
        elif gen == "S_NOT_D_POS":
            H = 0.5 * (g["H_D"] + g["S_pos"])
        else:
            H = 0.5 * (-g["H_D"] + g["S_neg"])
        sig = arma_second_order_signal(
            fs=fs, seconds=seconds, A=g["A"], rho=g["rho"], xi=g["xi"], H=H,
            seed=seed + 17000,
        )
        return sig, {
            "semantic_truth": gen,
            "true_chi_defined": False,
            "true_chi": None,
            "truth_coordinates": {**g, "H": H},
        }
    if gen == "COLORED_MEMORY":
        return colored_process_signal(fs=fs, seconds=seconds, seed=seed + 23000), {
            "semantic_truth": "COLORED_MEMORY",
            "true_chi_defined": False,
            "true_chi": None,
            "truth_coordinates": {"generator": gen},
        }
    if gen == "GENUINE_TWO_MODE":
        return two_mode_signal(fs=fs, seconds=seconds, seed=seed + 29000), {
            "semantic_truth": "GENUINE_TWO_MODE",
            "true_chi_defined": False,
            "true_chi": None,
            "truth_coordinates": {"generator": gen},
        }
    raise ValueError(gen)


def raw_edge_distance(raw: Any) -> float:
    return float(min(8.0 - abs(float(v)) for v in raw))


def run_nb1_case(truth: dict[str, Any], seed: int, rate: str) -> dict[str, Any]:
    lane = PACK["lanes"]["NB1"]
    fine_fs = float(lane["sampling_rates_hz"][0])
    seconds = float(lane["duration_seconds"])
    fine, meta = generate_nb1_fine(truth, seed, fine_fs, seconds)
    if rate == "fine":
        signal = fine
        fs = fine_fs
    elif rate == "coarse":
        signal = fine[::2]
        fs = float(lane["sampling_rates_hz"][1])
    else:
        raise ValueError(rate)

    fit = fit_continuous_lineage_candidate_rs(
        signal, fs, optimizer_maxiter=80, max_optimized_starts=18
    )
    true_arg = float(meta["true_chi"]) if meta["true_chi_defined"] else float(fit.parameters["damping_ratio"])
    prof = profile_case(signal, fs, fit, true_arg)
    if not meta["true_chi_defined"]:
        prof["truth_chi"] = None
        prof["truth_chi_profile_delta_nll"] = None
    hess = hessian_diagnostic(standardize(signal), fs, fit)
    structural = structural_metrics(signal)
    family = compare_state_space_candidates(signal, fs, optimizer_maxiter=60)

    return {
        "schema": "NSD_NB1_LONG_RUN_CASE_V0_1",
        "packet_digest": PACKET_DIGEST,
        "truth_id": truth["id"],
        "generator": truth["generator"],
        "seed": seed,
        "rate": rate,
        "sampling_rate_hz": fs,
        "duration_seconds": seconds,
        **meta,
        "c1q_rs_fit": {
            "nll": float(fit.negative_log_likelihood),
            "bic": float(fit.bic),
            "parameters": {k: float(v) for k, v in fit.parameters.items()},
            "raw_parameters": [float(v) for v in fit.raw_parameters],
            "winning_start_origin": fit.winning_start_origin,
            "raw_box_edge_distance": raw_edge_distance(fit.raw_parameters),
            "recurrence_seed_status": fit.recurrence_seed_status,
        },
        "profile": prof,
        "hessian": hess,
        "structural_metrics": structural,
        "native_family_comparator": {
            "bic_winner": family.bic_winner,
            "bic_margin_to_second": float(family.bic_margin_to_second),
            "fits": [
                {"family": f.family, "bic": float(f.bic), "nll": float(f.negative_log_likelihood)}
                for f in family.fits
            ],
        },
        "scientific_verdict": "NOT_PERFORMED_BY_GITHUB",
        "licenses_real_eeg_local_chi": False,
        "environment": env_record(),
    }


def nb1_truths() -> list[dict[str, Any]]:
    lane = PACK["lanes"]["NB1"]
    return list(lane["function_truths"]) + list(lane["limit_truths"])


def nb1_case_id(truth_id: str, seed: int, rate: str) -> str:
    return f"{truth_id}__{seed}__{rate}"


def run_nb1_all() -> bool:
    NB1_DIR.mkdir(parents=True, exist_ok=True)
    seeds = [int(x) for x in PACK["lanes"]["NB1"]["seeds"]]
    completed = set(CP.get("completed_nb1_cases", []))
    since_commit = 0
    for truth in nb1_truths():
        for seed in seeds:
            for rate in ("fine", "coarse"):
                cid = nb1_case_id(truth["id"], seed, rate)
                out = NB1_DIR / f"{cid}.json"
                if cid in completed and out.exists():
                    continue
                if runtime_checkpoint_if_needed(f"resume NB1 case {cid}"):
                    return False
                payload = run_nb1_case(truth, seed, rate)
                out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
                completed.add(cid)
                CP["completed_nb1_cases"] = sorted(completed)
                write_checkpoint("FULL_EXECUTION_ACTIVE", f"next unfinished NB1/NB2 evidence case after {cid}")
                since_commit += 1
                if since_commit >= CHECKPOINT_COMMIT_EVERY:
                    git_checkpoint(f"NSD conveyor: checkpoint after {len(completed)} NB1 cases")
                    since_commit = 0
    if since_commit:
        git_checkpoint("NSD conveyor: checkpoint NB1 evidence")
    return True


def sqrt_metric(G: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    vals, vecs = np.linalg.eigh(0.5 * (G + G.T))
    if np.min(vals) <= 0:
        raise ValueError("metric must be SPD")
    root = vecs @ np.diag(np.sqrt(vals)) @ vecs.T
    invroot = vecs @ np.diag(1.0 / np.sqrt(vals)) @ vecs.T
    return root, invroot


def system_from_spec(name: str, spec: dict[str, Any]) -> np.ndarray:
    s = CoupledSecondOrder2Mode(
        float(spec["omega1"]), float(spec["zeta1"]),
        float(spec["omega2"]), float(spec["zeta2"]),
        position_coupling_12=float(spec["k12"]),
        position_coupling_21=float(spec["k21"]),
        velocity_coupling_12=float(spec["c12"]),
        velocity_coupling_21=float(spec["c21"]),
        name=name,
    )
    return s.matrix


def cpx(z: complex) -> dict[str, float]:
    return {"real": float(z.real), "imag": float(z.imag)}


def static_response_record(name: str, A: np.ndarray, B: np.ndarray, C: np.ndarray, G: np.ndarray) -> dict[str, Any]:
    horizon = float(NB2CFG["horizon_seconds"])
    n = int(NB2CFG["time_samples"])
    times = np.linspace(0.0, horizon, n)
    root, invroot = sqrt_metric(G)
    gains = []
    io_norm = []
    best_dir = None
    best_gain = -1.0
    best_t = 0.0
    response_curve = []
    for t in times:
        Phi = expm(A * float(t))
        weighted = root @ Phi @ invroot
        u, s, vh = np.linalg.svd(weighted)
        gain = float(s[0])
        gains.append(gain)
        if gain > best_gain:
            best_gain = gain
            best_t = float(t)
            best_dir = (invroot @ vh[0, :].reshape(-1, 1)).reshape(-1)
        Y = C @ Phi @ B
        io_norm.append(float(np.linalg.norm(Y, ord=2)))
    x0 = np.asarray(best_dir, dtype=float)
    xnorm = math.sqrt(float(x0 @ G @ x0))
    x0 = x0 / xnorm
    for t in times:
        x = expm(A * float(t)) @ x0
        response_curve.append(float(math.sqrt(max(0.0, x @ G @ x))))

    eig = np.linalg.eigvals(A)
    numerical = float(np.max(np.linalg.eigvalsh(0.5 * (A + A.T))))
    _, V = np.linalg.eig(A)
    return {
        "name": name,
        "A": A.tolist(),
        "B": B.tolist(),
        "C": C.tolist(),
        "G": G.tolist(),
        "eigenvalues": [cpx(complex(z)) for z in eig],
        "spectral_abscissa": float(np.max(eig.real)),
        "numerical_abscissa_euclidean": numerical,
        "eigenvector_condition_number_euclidean": float(np.linalg.cond(V)),
        "times_seconds": times.tolist(),
        "physical_metric_propagator_gain": gains,
        "peak_gain": best_gain,
        "peak_time_seconds": best_t,
        "peak_initial_direction_physical_coordinates": x0.tolist(),
        "peak_direction_response_curve": response_curve,
        "integrated_peak_direction_response_burden": float(np.trapz(response_curve, times)),
        "input_output_impulse_norm": io_norm,
        "integrated_input_output_impulse_norm": float(np.trapz(io_norm, times)),
    }


def time_varying_record() -> dict[str, Any]:
    cfg = NB2CFG["time_varying"]
    base = cfg["base"]
    specs = []
    for k12, k21 in zip(cfg["k12_sequence"], cfg["k21_sequence"]):
        specs.append({
            "omega1":base["omega1"], "zeta1":base["zeta1"],
            "omega2":base["omega2"], "zeta2":base["zeta2"],
            "k12":k12, "k21":k21, "c12":0.0, "c21":0.0
        })
    As = [system_from_spec(f"tv_{i}", s) for i,s in enumerate(specs)]
    Abar = sum(As) / len(As)
    horizon = float(NB2CFG["horizon_seconds"])
    n = int(NB2CFG["time_samples"])
    times = np.linspace(0.0, horizon, n)
    dt = float(times[1] - times[0])
    seg = float(cfg["segment_seconds"])
    Phi = np.eye(4)
    gains = [1.0]
    io = [0.0]
    B = np.asarray(NB2CFG["B"]["both_velocity"], dtype=float)
    C = np.asarray(NB2CFG["C"]["both_positions"], dtype=float)
    for i,t in enumerate(times[1:], start=1):
        idx = int(math.floor(float(times[i-1]) / seg)) % len(As)
        Phi = expm(As[idx] * dt) @ Phi
        gains.append(float(np.linalg.svd(Phi, compute_uv=False)[0]))
        io.append(float(np.linalg.norm(C @ Phi @ B, ord=2)))
    surrogate = static_response_record("stationary_arithmetic_mean_surrogate", Abar, B, C, np.eye(4))
    return {
        "name":"TIME_VARYING_VS_STATIONARY_SURROGATE",
        "operator_matrices":[A.tolist() for A in As],
        "segment_seconds":seg,
        "stationary_surrogate_A":Abar.tolist(),
        "times_seconds":times.tolist(),
        "time_varying_propagator_gain":gains,
        "time_varying_input_output_norm":io,
        "stationary_surrogate":surrogate,
    }


def build_nb2_evidence() -> dict[str, Any]:
    systems = {k: system_from_spec(k,v) for k,v in NB2CFG["systems"].items()}
    B1 = np.asarray(NB2CFG["B"]["first_velocity"], dtype=float)
    B2 = np.asarray(NB2CFG["B"]["second_velocity"], dtype=float)
    Bb = np.asarray(NB2CFG["B"]["both_velocity"], dtype=float)
    C1 = np.asarray(NB2CFG["C"]["first_position"], dtype=float)
    C2 = np.asarray(NB2CFG["C"]["second_position"], dtype=float)
    Cb = np.asarray(NB2CFG["C"]["both_positions"], dtype=float)
    Cfull = np.asarray(NB2CFG["C"]["full_state"], dtype=float)
    I = np.eye(4)

    records = {}
    records["NORMAL_DECOUPLED"] = static_response_record("NORMAL_DECOUPLED", systems["normal_decoupled"], Bb, Cfull, I)
    records["NORMAL_RECIPROCAL"] = static_response_record("NORMAL_RECIPROCAL", systems["reciprocal_coupled"], Bb, Cfull, I)
    records["SAME_SPECTRUM_BASE"] = static_response_record("SAME_SPECTRUM_BASE", systems["same_spectrum_base"], Bb, Cfull, I)
    records["SAME_SPECTRUM_NONNORMAL"] = static_response_record("SAME_SPECTRUM_NONNORMAL", systems["same_spectrum_nonnormal"], Bb, Cfull, I)

    Aio = systems["io_base"]
    records["SAME_A_DIFFERENT_B_FIRST"] = static_response_record("SAME_A_DIFFERENT_B_FIRST", Aio, B1, Cb, I)
    records["SAME_A_DIFFERENT_B_SECOND"] = static_response_record("SAME_A_DIFFERENT_B_SECOND", Aio, B2, Cb, I)
    records["SAME_AB_DIFFERENT_C_FIRST"] = static_response_record("SAME_AB_DIFFERENT_C_FIRST", Aio, Bb, C1, I)
    records["SAME_AB_DIFFERENT_C_SECOND"] = static_response_record("SAME_AB_DIFFERENT_C_SECOND", Aio, Bb, C2, I)
    records["PARTIAL_OBSERVATION"] = static_response_record("PARTIAL_OBSERVATION", Aio, Bb, C1, I)

    S = np.asarray(NB2CFG["similarity_S"], dtype=float)
    Sinv = np.linalg.inv(S)
    Aprime = S @ Aio @ Sinv
    Bprime = S @ Bb
    Cprime = Cb @ Sinv
    Gprime = Sinv.T @ I @ Sinv
    records["SIMILARITY_BASE"] = static_response_record("SIMILARITY_BASE", Aio, Bb, Cb, I)
    records["SIMILARITY_TRANSFORMED_WITH_METRIC"] = static_response_record("SIMILARITY_TRANSFORMED_WITH_METRIC", Aprime, Bprime, Cprime, Gprime)
    records["TIME_VARYING"] = time_varying_record()

    return {
        "schema":"NSD_NB2NB3_LONG_RUN_EVIDENCE_V0_1",
        "packet_digest":PACKET_DIGEST,
        "config_digest":NB2_DIGEST,
        "records":records,
        "scientific_verdict":"NOT_PERFORMED_BY_GITHUB",
        "environment":env_record(),
    }


def run_nb2_all() -> bool:
    NB2_DIR.mkdir(parents=True, exist_ok=True)
    out = NB2_DIR / "matched_family_evidence.json"
    if "NB2NB3_MATCHED_FAMILIES" in set(CP.get("completed_nb2_families", [])) and out.exists():
        return True
    if runtime_checkpoint_if_needed("resume N-B2/N-B3 matched-family evidence"):
        return False
    payload = build_nb2_evidence()
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    CP["completed_nb2_families"] = ["NB2NB3_MATCHED_FAMILIES"]
    write_checkpoint("FULL_EXECUTION_ACTIVE", "finish remaining NB1 evidence or merge")
    git_checkpoint("NSD conveyor: checkpoint N-B2 N-B3 evidence")
    return True


def merge_nb1() -> dict[str, Any]:
    files = sorted(NB1_DIR.glob("*.json"))
    rows = [load_json(p) for p in files]
    expected = len(nb1_truths()) * len(PACK["lanes"]["NB1"]["seeds"]) * 2
    if len(rows) != expected:
        raise RuntimeError(f"expected {expected} NB1 rows, found {len(rows)}")
    by_truth = {}
    for truth in sorted({r["truth_id"] for r in rows}):
        rr = [r for r in rows if r["truth_id"] == truth]
        by_truth[truth] = {
            "row_count":len(rr),
            "semantic_truth":rr[0]["semantic_truth"],
            "fitted_chi":[float(r["c1q_rs_fit"]["parameters"]["damping_ratio"]) for r in rr],
            "profile_edge_min_count":sum(
                1 for r in rr
                if r["profile"].get("lowest_profile_chi") in {
                    r["profile"]["profile_points"][0]["chi"],
                    r["profile"]["profile_points"][-1]["chi"],
                }
            ),
            "hessian_statuses":[r["hessian"].get("status") for r in rr],
            "native_family_winners":[r["native_family_comparator"]["bic_winner"] for r in rr],
        }
    pairs=[]
    for truth in nb1_truths():
        for seed in PACK["lanes"]["NB1"]["seeds"]:
            f=next(r for r in rows if r["truth_id"]==truth["id"] and r["seed"]==seed and r["rate"]=="fine")
            c=next(r for r in rows if r["truth_id"]==truth["id"] and r["seed"]==seed and r["rate"]=="coarse")
            pairs.append({
                "truth_id":truth["id"],"seed":seed,
                "fitted_chi_rate_drift":abs(float(f["c1q_rs_fit"]["parameters"]["damping_ratio"])-float(c["c1q_rs_fit"]["parameters"]["damping_ratio"])),
            })
    return {
        "schema":"NSD_NB1_LONG_RUN_MERGED_EVIDENCE_V0_1",
        "packet_digest":PACKET_DIGEST,
        "row_count":len(rows),
        "pair_count":len(pairs),
        "summary_by_truth":by_truth,
        "paired_rate_evidence":pairs,
        "scientific_verdict":"NOT_PERFORMED_BY_GITHUB",
    }


def build_manifest() -> dict[str, Any]:
    files = sorted(p for p in RESULTS.rglob("*") if p.is_file() and p != MANIFEST)
    return {
        "schema":"NSD_LONG_RUN_EVIDENCE_MANIFEST_V0_1",
        "packet_digest":PACKET_DIGEST,
        "nb2_config_digest":NB2_DIGEST,
        "files":[
            {"path":str(p.relative_to(REPO_ROOT)), "sha256":sha256_file(p), "bytes":p.stat().st_size}
            for p in files
        ],
        "checkpoint":load_json(CHECKPOINT),
        "scientific_verdict":"NOT_PERFORMED_BY_GITHUB",
        "review_state":"SCIENTIFIC_REVIEW_READY",
        "environment":env_record(),
    }


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)

    if CP.get("stage") == "SCIENTIFIC_REVIEW_READY":
        print(json.dumps({
            "status": "SCIENTIFIC_REVIEW_READY",
            "message": "Frozen evidence packet is already complete; no recomputation performed."
        }, indent=2))
        return 0

    validate_contract()
    if "PACKET_BOUND" not in CP["completed_stages"]:
        CP["completed_stages"].append("PACKET_BOUND")
    write_checkpoint("PACKET_BOUND", "validate frozen input digests")
    git_checkpoint("NSD conveyor: packet bound")

    validate_contract()
    if "FROZEN_INPUT_VALIDATED" not in CP["completed_stages"]:
        CP["completed_stages"].append("FROZEN_INPUT_VALIDATED")
    write_checkpoint("FROZEN_INPUT_VALIDATED", "run implementation contract tests")
    git_checkpoint("NSD conveyor: frozen input validated")

    if "IMPLEMENTATION_TESTED" not in CP["completed_stages"]:
        run_tests()
        CP["completed_stages"].append("IMPLEMENTATION_TESTED")
        write_checkpoint("IMPLEMENTATION_TESTED", "execute frozen preflight/evidence packet")
        git_checkpoint("NSD conveyor: implementation tests pass")

    if "PREFLIGHT_PASS" not in CP["completed_stages"]:
        # Preflight uses the first frozen NB1 Function row and one exact NB2 record.
        t = PACK["lanes"]["NB1"]["function_truths"][0]
        seed = int(PACK["lanes"]["NB1"]["seeds"][0])
        pre = run_nb1_case(t, seed, "coarse")
        if pre["packet_digest"] != PACKET_DIGEST:
            raise RuntimeError("FROZEN_CONTRACT_VIOLATION: NB1 preflight packet mismatch")
        A = system_from_spec("preflight", NB2CFG["systems"]["same_spectrum_nonnormal"])
        _ = static_response_record(
            "preflight", A,
            np.asarray(NB2CFG["B"]["both_velocity"], dtype=float),
            np.asarray(NB2CFG["C"]["full_state"], dtype=float),
            np.eye(4),
        )
        CP["completed_stages"].append("PREFLIGHT_PASS")
        write_checkpoint("PREFLIGHT_PASS", "run all frozen evidence cases")
        git_checkpoint("NSD conveyor: mechanical preflight pass")

    if not run_nb2_all():
        return 0
    if not run_nb1_all():
        return 0

    if "FULL_EXECUTION_COMPLETE" not in CP["completed_stages"]:
        CP["completed_stages"].append("FULL_EXECUTION_COMPLETE")
    write_checkpoint("FULL_EXECUTION_COMPLETE", "merge evidence without scientific adjudication")
    git_checkpoint("NSD conveyor: full frozen execution complete")

    merged = merge_nb1()
    (NB1_DIR / "merged_evidence.json").write_text(json.dumps(merged, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    if "MERGED_EVIDENCE_COMPLETE" not in CP["completed_stages"]:
        CP["completed_stages"].append("MERGED_EVIDENCE_COMPLETE")
    write_checkpoint("MERGED_EVIDENCE_COMPLETE", "build reproducibility hashes and evidence manifest")
    git_checkpoint("NSD conveyor: merged evidence complete")

    if "REPRODUCIBILITY_CHECK_COMPLETE" not in CP["completed_stages"]:
        # Deterministic integrity: all evidence files must bind to the frozen packet.
        for p in NB1_DIR.glob("*.json"):
            obj=load_json(p)
            if p.name != "merged_evidence.json" and obj.get("packet_digest") != PACKET_DIGEST:
                raise RuntimeError(f"FROZEN_CONTRACT_VIOLATION: {p} packet digest mismatch")
        nb2=load_json(NB2_DIR/"matched_family_evidence.json")
        if nb2.get("packet_digest") != PACKET_DIGEST or nb2.get("config_digest") != NB2_DIGEST:
            raise RuntimeError("FROZEN_CONTRACT_VIOLATION: N-B2 evidence digest mismatch")
        CP["completed_stages"].append("REPRODUCIBILITY_CHECK_COMPLETE")
        write_checkpoint("REPRODUCIBILITY_CHECK_COMPLETE", "package final scientific-review evidence")
        git_checkpoint("NSD conveyor: reproducibility checks complete")

    write_checkpoint("SCIENTIFIC_REVIEW_READY", "researcher + ChatGPT review evidence; GitHub must not adjudicate")
    MANIFEST.write_text(json.dumps(build_manifest(), indent=2, sort_keys=True)+"\n", encoding="utf-8")
    if "SCIENTIFIC_REVIEW_READY" not in CP["completed_stages"]:
        CP["completed_stages"].append("SCIENTIFIC_REVIEW_READY")
    write_checkpoint("SCIENTIFIC_REVIEW_READY", "researcher + ChatGPT scientific review", None)
    git_checkpoint("NSD conveyor: evidence complete and scientific review ready")
    print(json.dumps({
        "status":"SCIENTIFIC_REVIEW_READY",
        "nb1_cases":len(CP["completed_nb1_cases"]),
        "nb2_families":CP["completed_nb2_families"],
        "manifest":str(MANIFEST.relative_to(REPO_ROOT)),
    }, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        try:
            write_checkpoint("MECHANICAL_FAILURE", "repair mechanical failure without changing frozen packet", repr(exc))
            git_checkpoint("NSD conveyor: mechanical failure checkpoint")
        finally:
            raise
