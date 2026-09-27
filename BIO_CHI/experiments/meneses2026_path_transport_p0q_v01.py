#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from scipy.optimize import curve_fit
from scipy.stats import spearmanr
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, confusion_matrix
from sklearn.preprocessing import StandardScaler

UPSTREAM_REPO = "wadhwalab/2026-Meneses-Osmotic"
UPSTREAM_COMMIT = "d14d0caaa07299f13d1b1121d1e4630454fd724b"
SEED = 20260926
N_PERM = 2000
CONCS = [200, 300, 400, 500]
PATHS = ["sucrose", "sorbitol", "sodium_context", "clockwise"]

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "meneses2026_path_transport_raw"
OUT = ROOT / "meneses2026_path_transport_results"
RAW.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

FILES = {
    "sucrose": {
        200: ("data/time-series/bead/sucrose_200mM.parquet", "41c7e7837d7f6e0418180d85ded212a102af0621"),
        300: ("data/time-series/bead/sucrose_300mM.parquet", "78d915b2264dd6fa273ba061e605ee8597a28a06"),
        400: ("data/time-series/bead/sucrose_400mM.parquet", "36ebcaa9c817ba8c11527e69d6f8b49669b1f2d6"),
        500: ("data/time-series/bead/sucrose_500mM.parquet", "dd3b2ef0b1b77c43c02080c88080abb5b0cd3f61"),
    },
    "sorbitol": {
        200: ("data/time-series/bead/sorbitol_200mM.parquet", "f105b4efa5815bff50bbe51ef493550b49c91d36"),
        300: ("data/time-series/bead/sorbitol_300mM.parquet", "cec88379c5da5a07dc444fd25c2f0be8937ec81e"),
        400: ("data/time-series/bead/sorbitol_400mM.parquet", "f3fd7373b2944f01b945b7259661f3fc6a75fc85"),
        500: ("data/time-series/bead/sorbitol_500mM.parquet", "1833accfa1e4405bebfd0e9430008854e3492567"),
    },
    "sodium_context": {
        200: ("data/time-series/bead/sodium_200mM.parquet", "57ec489e1a19cc3a20ea6dea270152b86b359fa0"),
        300: ("data/time-series/bead/sodium_300mM.parquet", "5496ff4a54d4631fd0349d63966926d7ae065b7f"),
        400: ("data/time-series/bead/sodium_400mM.parquet", "fe51858b5cc7b6e6e7d1eb94a4bcb165ce1d312c"),
        500: ("data/time-series/bead/sodium_500mM.parquet", "52ab687a447fb5681492e4a25e7cf7814b2270c2"),
    },
    "clockwise": {
        200: ("data/time-series/bead/clockwise_200mM.parquet", "c09ed5d53afd435097e26d5b10330dfd09e3538e"),
        300: ("data/time-series/bead/clockwise_300mM.parquet", "c38f3e0ccffd884aee46732917233a73cd573212"),
        400: ("data/time-series/bead/clockwise_400mM.parquet", "342d9c3c9164a20b3ec9d9ee7749989221854f41"),
        500: ("data/time-series/bead/clockwise_500mM.parquet", "7a42570406646d9f329f1c9a32c870ffaf6fc56a"),
    },
}

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def fetch(rel: str) -> Path:
    p = RAW / rel.replace("/", "__")
    if p.exists() and p.stat().st_size > 100:
        return p
    url = f"https://raw.githubusercontent.com/{UPSTREAM_REPO}/{UPSTREAM_COMMIT}/{rel}"
    last = None
    for attempt in range(4):
        try:
            r = requests.get(url, timeout=120, headers={"User-Agent": "SymC-BioChi-PathTransport/0.1"})
            if r.status_code == 200 and len(r.content) > 100:
                p.write_bytes(r.content)
                return p
            last = f"HTTP {r.status_code}; bytes={len(r.content)}"
        except Exception as e:
            last = f"{type(e).__name__}: {e}"
        time.sleep(2 ** attempt)
    raise RuntimeError(f"source retrieval failed for {rel}: {last}")

def wide_traces(df: pd.DataFrame):
    if "time_s" not in df.columns:
        raise KeyError("time_s missing")
    t = pd.to_numeric(df["time_s"], errors="coerce").to_numpy(float)
    cols = [c for c in df.columns if c not in {"frame", "time_s"}]
    if not cols:
        raise RuntimeError("no motor trace columns")
    return t, cols

def fit_cell(path_name: str, cond: int, trace: str, t: np.ndarray, y: np.ndarray):
    valid = np.isfinite(t) & np.isfinite(y)
    tt = t[valid]
    yy = y[valid]
    rec = {"path": path_name, "condition_mM": int(cond), "cell": str(trace), "fit_valid": False}

    if len(tt) < 20:
        rec["failure"] = "insufficient_total_finite_samples"
        return rec

    baseline_mask = tt <= 180.0
    if baseline_mask.sum() < 20:
        rec["failure"] = "insufficient_baseline_samples"
        return rec
    baseline = float(np.mean(yy[baseline_mask]))
    if not np.isfinite(baseline) or baseline == 0:
        rec["failure"] = "invalid_baseline"
        return rec
    yn = yy / baseline

    windows = {
        "speed_initial": (155.0, 175.0),
        "speed_final": (215.0, 235.0),
        "speed_increase_min": (240.0, 260.0),
        "speed_increase_max": (330.0, 350.0),
        "collapse_fit": (175.0, 240.0),
        "recovery_fit": (250.0, 360.0),
    }
    masks = {k: (tt >= lo) & (tt <= hi) for k, (lo, hi) in windows.items()}
    if any(masks[k].sum() < 20 for k in ["collapse_fit", "recovery_fit"]):
        rec["failure"] = "insufficient_fit_window_samples"
        return rec
    if any(masks[k].sum() == 0 for k in ["speed_initial", "speed_final", "speed_increase_min", "speed_increase_max"]):
        rec["failure"] = "empty_summary_window"
        return rec

    speed_initial = float(np.mean(yn[masks["speed_initial"]]))
    speed_final = float(np.mean(yn[masks["speed_final"]]))
    A_dec = speed_initial - speed_final
    C_dec = speed_final
    speed_increase_min = float(np.mean(yn[masks["speed_increase_min"]]))
    speed_increase_max = float(np.mean(yn[masks["speed_increase_max"]]))
    G_rec = speed_increase_max - speed_increase_min

    try:
        def dec(x, tau, t0):
            z = np.clip((x - 175.0 - t0) / tau, -700, 700)
            return A_dec / (1.0 + np.exp(z)) + C_dec

        pdec, _ = curve_fit(
            dec,
            tt[masks["collapse_fit"]],
            yn[masks["collapse_fit"]],
            p0=[10.0, 10.0],
            bounds=(0.0, np.inf),
            maxfev=50000,
        )
        tau_dec, t0_dec = [float(v) for v in pdec]

        def inc(x, tau, t0):
            z = np.clip(-(x - 270.0 - t0) / tau, -700, 700)
            return speed_increase_min + (speed_increase_max - speed_increase_min) / (1.0 + np.exp(z))

        pinc, _ = curve_fit(
            inc,
            tt[masks["recovery_fit"]],
            yn[masks["recovery_fit"]],
            p0=[3.0, -10.0],
            maxfev=50000,
        )
        tau_inc, t0_inc = [float(v) for v in pinc]

        vals = [A_dec, tau_dec, tau_inc, G_rec, C_dec, t0_dec, t0_inc, speed_increase_min, speed_increase_max]
        if not np.all(np.isfinite(vals)):
            raise ValueError("nonfinite_fitted_or_summary_value")
        if tau_dec <= 0 or tau_inc <= 0:
            raise ValueError(f"nonpositive_timescale tau_dec={tau_dec} tau_inc={tau_inc}")

        rec.update({
            "fit_valid": True,
            "A_dec": float(A_dec),
            "tau_dec": float(tau_dec),
            "tau_inc": float(tau_inc),
            "G_rec": float(G_rec),
            "C_dec": float(C_dec),
            "t0_dec": float(t0_dec),
            "t0_inc": float(t0_inc),
            "speed_increase_min": float(speed_increase_min),
            "speed_increase_max": float(speed_increase_max),
        })
    except Exception as e:
        rec["failure"] = f"{type(e).__name__}: {e}"
    return rec

def extract_all():
    rows = []
    manifest = []
    for path_name in PATHS:
        for cond in CONCS:
            rel, blob = FILES[path_name][cond]
            p = fetch(rel)
            manifest.append({
                "path_family": path_name,
                "condition_mM": cond,
                "source_path": rel,
                "expected_github_blob_sha1": blob,
                "bytes": int(p.stat().st_size),
                "sha256": sha256(p),
                "upstream_commit": UPSTREAM_COMMIT,
            })
            df = pd.read_parquet(p)
            t, cols = wide_traces(df)
            for c in cols:
                y = pd.to_numeric(df[c], errors="coerce").to_numpy(float)
                rows.append(fit_cell(path_name, cond, c, t, y))
    return pd.DataFrame(rows), pd.DataFrame(manifest)

def matrix_from(df: pd.DataFrame, full: bool):
    if full:
        X = np.column_stack([
            df["A_dec"].to_numpy(float),
            np.log(df["tau_dec"].to_numpy(float)),
            np.log(df["tau_inc"].to_numpy(float)),
            df["G_rec"].to_numpy(float),
        ])
        names = ["A_dec", "log_tau_dec", "log_tau_inc", "G_rec"]
    else:
        X = df[["A_dec"]].to_numpy(float)
        names = ["A_dec"]
    return X, names

def cv_balanced_accuracy(df: pd.DataFrame, labels: np.ndarray, full: bool):
    X, _ = matrix_from(df, full=full)
    conc = df["condition_mM"].to_numpy(int)
    pred = np.empty(len(df), dtype=object)
    fold_scores = []
    for held in CONCS:
        tr = conc != held
        te = conc == held
        if not np.any(te) or not np.any(tr):
            raise RuntimeError(f"empty CV fold {held}")
        scaler = StandardScaler()
        xtr = scaler.fit_transform(X[tr])
        if np.any(~np.isfinite(scaler.scale_)) or np.any(scaler.scale_ <= 0):
            raise RuntimeError(f"zero/nonfinite training coordinate scale in fold {held}")
        xte = scaler.transform(X[te])
        model = LogisticRegression(
            C=1.0,
            penalty="l2",
            solver="lbfgs",
            class_weight="balanced",
            max_iter=2000,
            random_state=SEED,
        )
        model.fit(xtr, labels[tr])
        pp = model.predict(xte)
        pred[te] = pp
        fold_scores.append({
            "heldout_condition_mM": int(held),
            "n_test": int(te.sum()),
            "balanced_accuracy": float(balanced_accuracy_score(labels[te], pp)),
        })
    score = float(balanced_accuracy_score(labels, pred))
    cm = confusion_matrix(labels, pred, labels=PATHS)
    return score, pred, fold_scores, cm

def stratified_permutation_null(df: pd.DataFrame, full: bool):
    rng = np.random.default_rng(SEED + (1 if full else 2))
    original = df["path"].to_numpy(object)
    conc = df["condition_mM"].to_numpy(int)
    null = np.empty(N_PERM, dtype=float)
    for i in range(N_PERM):
        lab = original.copy()
        for c in CONCS:
            idx = np.flatnonzero(conc == c)
            lab[idx] = rng.permutation(lab[idx])
        null[i] = cv_balanced_accuracy(df, lab, full=full)[0]
    return null

def medians_and_trends(valid: pd.DataFrame):
    features = ["A_dec", "tau_dec", "tau_inc", "G_rec"]
    out = {}
    for p in PATHS:
        out[p] = {}
        z = valid[valid.path == p]
        for feat in features:
            vals = {}
            for c in CONCS:
                v = z[z.condition_mM == c][feat].to_numpy(float)
                vals[str(c)] = float(np.median(v)) if len(v) else None
            arr = np.array([vals[str(c)] for c in CONCS], dtype=float)
            rho = float(spearmanr(CONCS, arr).statistic) if np.all(np.isfinite(arr)) else None
            out[p][feat] = {"median_by_condition": vals, "spearman_rho": rho}
    return out

def classifier_result(valid: pd.DataFrame, full: bool):
    labels = valid["path"].to_numpy(object)
    observed, pred, folds, cm = cv_balanced_accuracy(valid, labels, full=full)
    null = stratified_permutation_null(valid, full=full)
    q975 = float(np.quantile(null, 0.975))
    p = float((1 + np.sum(null >= observed)) / (N_PERM + 1))
    detected = bool(observed > q975)
    return {
        "representation": "full_vector" if full else "depth_only",
        "observed_balanced_accuracy": observed,
        "null_97_5_percentile": q975,
        "permutation_p_upper_tail": p,
        "n_permutations": N_PERM,
        "detected": detected,
        "folds": folds,
        "confusion_matrix_labels": PATHS,
        "confusion_matrix": cm.tolist(),
        "null_summary": {
            "mean": float(np.mean(null)),
            "sd": float(np.std(null, ddof=1)),
            "min": float(np.min(null)),
            "max": float(np.max(null)),
        },
    }

def main():
    fits, manifest = extract_all()
    manifest.to_csv(OUT / "source_manifest.csv", index=False)
    fits.to_csv(OUT / "all_cell_fit_records.csv", index=False)

    failures = fits[~fits["fit_valid"].fillna(False)].copy()
    valid = fits[fits["fit_valid"].fillna(False)].copy()
    failures.to_csv(OUT / "fit_failure_ledger.csv", index=False)
    valid.to_csv(OUT / "eligible_representation_cells.csv", index=False)

    coverage = {}
    complete = True
    for p in PATHS:
        coverage[p] = {}
        for c in CONCS:
            n = int(((valid.path == p) & (valid.condition_mM == c)).sum())
            coverage[p][str(c)] = n
            if n == 0:
                complete = False

    result = {
        "schema_version": "0.1",
        "experiment_id": "MENESES2026_PATH_TRANSPORT_P0Q_V01",
        "evidence_class": "P0-Q_LITERATURE_OPEN_DIRECT_EXPERIMENTAL_PATH_TRANSPORT_QUALIFICATION",
        "source": {
            "repository": UPSTREAM_REPO,
            "commit": UPSTREAM_COMMIT,
            "n_files": int(len(manifest)),
        },
        "fit_record_counts": {
            "total": int(len(fits)),
            "eligible": int(len(valid)),
            "failures": int(len(failures)),
        },
        "eligible_cells_by_path_and_concentration": coverage,
        "descriptive_condition_medians": medians_and_trends(valid) if len(valid) else {},
        "chi_bio_disposition": "NOT_OPENED_NOT_LICENSED",
    }

    if not complete:
        result.update({
            "status": "VALID_REFUSAL_INSUFFICIENT_PATH_COVERAGE",
            "primary_disposition": "INSUFFICIENT_PATH_COVERAGE",
            "secondary_disposition": "NOT_OPENED",
            "Bio_Chi_disposition": "PATH_TRANSPORT_GATE_REFUSED_INSUFFICIENT_COVERAGE",
            "Chi_bio_disposition": "NO_NEW_PATH_TRANSPORT_CLASSIFICATION",
            "claim_ceiling": "direct experimental P0-Q path-transport gate refused for incomplete frozen coverage",
        })
    else:
        full = classifier_result(valid, full=True)
        depth = classifier_result(valid, full=False)
        increment = float(full["observed_balanced_accuracy"] - depth["observed_balanced_accuracy"])

        if full["detected"]:
            primary = "PATH_REORGANIZATION_DETECTED_P0Q"
        else:
            primary = "NO_DETECTABLE_PATH_REORGANIZATION_P0Q"

        if full["detected"] and increment >= 0.10:
            secondary = "DYNAMICAL_PATH_INFORMATION_BEYOND_DEPTH_P0Q"
        elif full["detected"] and depth["detected"] and increment < 0.10:
            secondary = "PATH_INFORMATION_NOT_SEPARATED_FROM_DEPTH_P0Q"
        elif (not full["detected"]) and depth["detected"]:
            secondary = "DEPTH_DOMINANT_PATH_SIGNATURE_P0Q"
        elif (not full["detected"]) and (not depth["detected"]):
            secondary = "PATH_SIGNATURE_UNRESOLVED_P0Q"
        else:
            secondary = "SECONDARY_RULE_UNDERSPECIFIED_FULL_ONLY_LT_0_10"

        result.update({
            "status": "EXECUTED_VALID_DIRECT_EXPERIMENTAL_PATH_TRANSPORT_P0Q",
            "full_vector_classifier": full,
            "depth_only_classifier": depth,
            "full_minus_depth_balanced_accuracy": increment,
            "primary_disposition": primary,
            "secondary_disposition": secondary,
            "Bio_Chi_disposition": primary,
            "Chi_bio_disposition": secondary,
            "claim_ceiling": "detectable path encoding or lack thereof in one released E. coli motor-recovery dataset; not equivalence, universal law, or causal mechanism",
        })

    (OUT / "MENESES2026_PATH_TRANSPORT_P0Q_V01_RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        fail = {
            "schema_version": "0.1",
            "experiment_id": "MENESES2026_PATH_TRANSPORT_P0Q_V01",
            "status": "EXECUTION_FAILURE_PRESERVED",
            "error_type": type(e).__name__,
            "error": str(e),
        }
        (OUT / "MENESES2026_PATH_TRANSPORT_P0Q_V01_FAILURE.json").write_text(json.dumps(fail, indent=2) + "\n")
        print(json.dumps(fail, indent=2), file=sys.stderr)
        raise
