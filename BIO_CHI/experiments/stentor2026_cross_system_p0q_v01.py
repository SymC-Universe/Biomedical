#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

SEED = 20260926
N_PERM = 2000
ISIs = [60, 120, 180]
ITIs = [3600, 7200, 10800, 18000]

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "stentor2026_cross_system_results"
FEATURES = ["H1_depth", "Recovery", "H2_depth", "AUC_shift"]

def matrix(df, full=True):
    return df[FEATURES].to_numpy(float) if full else df[["Recovery"]].to_numpy(float)

def cv_score(df, labels, full=True):
    X = matrix(df, full)
    iti = df["iti_s"].to_numpy(int)
    pred = np.empty(len(df), dtype=int)
    folds = []
    for held in ITIs:
        tr = iti != held
        te = iti == held
        if not tr.any() or not te.any():
            raise RuntimeError(f"empty ITI fold {held}")
        scaler = StandardScaler()
        xtr = scaler.fit_transform(X[tr])
        xte = scaler.transform(X[te])
        if np.any(~np.isfinite(scaler.scale_)) or np.any(scaler.scale_ <= 0):
            raise RuntimeError(f"zero/nonfinite training coordinate scale at ITI {held}: {scaler.scale_.tolist()}")
        model = LogisticRegression(
            C=1.0, penalty="l2", solver="lbfgs",
            class_weight="balanced", max_iter=2000, random_state=SEED
        )
        model.fit(xtr, labels[tr])
        pp = model.predict(xte)
        pred[te] = pp
        folds.append({
            "heldout_iti_s": int(held),
            "n_test": int(te.sum()),
            "balanced_accuracy": float(balanced_accuracy_score(labels[te], pp)),
        })
    return float(balanced_accuracy_score(labels, pred)), pred, folds

def permutation_tests(df):
    labels = df["isi_s"].to_numpy(int)
    iti = df["iti_s"].to_numpy(int)
    obs_full, pred_full, folds_full = cv_score(df, labels, True)
    obs_rec, pred_rec, folds_rec = cv_score(df, labels, False)

    rng = np.random.default_rng(SEED)
    null_full = np.empty(N_PERM, float)
    null_rec = np.empty(N_PERM, float)
    for i in range(N_PERM):
        lab = labels.copy()
        for rest in ITIs:
            idx = np.flatnonzero(iti == rest)
            lab[idx] = rng.permutation(lab[idx])
        null_full[i] = cv_score(df, lab, True)[0]
        null_rec[i] = cv_score(df, lab, False)[0]

    qf = float(np.quantile(null_full, .975))
    qr = float(np.quantile(null_rec, .975))
    pf = float((1 + np.sum(null_full >= obs_full)) / (N_PERM + 1))
    pr = float((1 + np.sum(null_rec >= obs_rec)) / (N_PERM + 1))
    full_detect = bool(obs_full > qf)
    rec_detect = bool(obs_rec > qr)

    if full_detect and not rec_detect:
        secondary = "MULTICOORDINATE_PATH_INFORMATION_BEYOND_RECOVERY_ONLY_P0Q"
    elif full_detect and rec_detect:
        secondary = "PATH_INFORMATION_NOT_SEPARATED_FROM_RECOVERY_ONLY_P0Q"
    elif (not full_detect) and rec_detect:
        secondary = "RECOVERY_DOMINANT_PATH_SIGNATURE_P0Q"
    else:
        secondary = "PATH_SIGNATURE_UNRESOLVED_P0Q"

    return {
        "full_vector": {
            "observed_balanced_accuracy": obs_full,
            "null_97_5_percentile": qf,
            "permutation_p_upper_tail": pf,
            "detected": full_detect,
            "folds": folds_full,
            "confusion_matrix_labels": ISIs,
            "confusion_matrix": confusion_matrix(labels, pred_full, labels=ISIs).tolist(),
            "null_mean": float(null_full.mean()),
            "null_sd": float(null_full.std(ddof=1)),
        },
        "recovery_only": {
            "observed_balanced_accuracy": obs_rec,
            "null_97_5_percentile": qr,
            "permutation_p_upper_tail": pr,
            "detected": rec_detect,
            "folds": folds_rec,
            "confusion_matrix_labels": ISIs,
            "confusion_matrix": confusion_matrix(labels, pred_rec, labels=ISIs).tolist(),
            "null_mean": float(null_rec.mean()),
            "null_sd": float(null_rec.std(ddof=1)),
        },
        "secondary_disposition": secondary,
    }

def condition_representation(df):
    med = df.groupby(["isi_s","iti_s"], as_index=False)[FEATURES].median().sort_values(["isi_s","iti_s"])
    X = med[FEATURES].to_numpy(float)
    scaler = StandardScaler()
    Z = scaler.fit_transform(X)
    pca = PCA(n_components=min(Z.shape), svd_solver="full").fit(Z)
    z1 = pca.inverse_transform(np.column_stack([
        pca.transform(Z)[:,0],
        np.zeros((len(Z), pca.n_components_-1))
    ]))
    max_resid = float(np.max(np.abs(Z-z1)))
    pc1 = float(pca.explained_variance_ratio_[0])
    adequate = bool(pc1 >= .95 and max_resid <= .10)
    return med, {
        "singular_values": [float(x) for x in pca.singular_values_],
        "pc1_variance_fraction": pc1,
        "max_abs_standardized_1d_reconstruction_residual": max_resid,
        "one_dimensional_adequacy": adequate,
        "disposition": "ONE_DIMENSIONAL_CONDITION_REPRESENTATION_ADEQUATE_P0Q" if adequate else "MULTICOORDINATE_CONDITION_REPRESENTATION_REQUIRED_P0Q",
    }

def main():
    features_path = OUT / "stentor_cell_features.csv"
    if not features_path.exists():
        raise FileNotFoundError(features_path)
    df = pd.read_csv(features_path)
    if df.empty:
        raise RuntimeError("no eligible Stentor cells")
    if not set(FEATURES).issubset(df.columns):
        raise RuntimeError("feature columns missing")
    if sorted(df["isi_s"].unique().tolist()) != ISIs:
        raise RuntimeError(f"ISI coverage mismatch: {sorted(df.isi_s.unique().tolist())}")
    if sorted(df["iti_s"].unique().tolist()) != ITIs:
        raise RuntimeError(f"ITI coverage mismatch: {sorted(df.iti_s.unique().tolist())}")

    coverage = df.groupby(["isi_s","iti_s"]).size()
    if len(coverage) != 12 or (coverage <= 0).any():
        result = {
            "schema_version":"0.1",
            "experiment_id":"STENTOR2026_CROSS_SYSTEM_PATH_P0Q_V01",
            "status":"VALID_REFUSAL_INSUFFICIENT_SOURCE_COVERAGE",
            "coverage": {f"ISI{a}_ITI{b}":int(v) for (a,b),v in coverage.items()},
            "primary_disposition":"INSUFFICIENT_SOURCE_COVERAGE",
            "chi_bio":"NOT_OPENED_NOT_LICENSED",
        }
        (OUT/"STENTOR2026_CROSS_SYSTEM_PATH_P0Q_V01_RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
        print(json.dumps(result,indent=2))
        return

    tests = permutation_tests(df)
    med, adequacy = condition_representation(df)
    med.to_csv(OUT/"stentor_condition_medians.csv", index=False)

    primary = "CROSS_SYSTEM_PATH_ORGANIZATION_DETECTED_P0Q" if tests["full_vector"]["detected"] else "CROSS_SYSTEM_PATH_ORGANIZATION_NOT_DETECTED_P0Q"

    result = {
        "schema_version":"0.1",
        "experiment_id":"STENTOR2026_CROSS_SYSTEM_PATH_P0Q_V01",
        "status":"EXECUTED_VALID_DIRECT_BEHAVIOR_CROSS_SYSTEM_P0Q",
        "evidence_class":"P0-Q_LITERATURE_OPEN_DIRECT_BEHAVIOR_CROSS_SYSTEM_TRANSPORT_QUALIFICATION",
        "source":{
            "repository":"tejasramdas/stentor_habituation",
            "commit":"8704c114555af3477a1dd7471beedde205fed263",
            "collated_lfs_sha256":"b84054675f8a608471da1d9cccd051c1fb9503d35b3c9b5b9f6ebc378e75054f"
        },
        "n_cells_eligible":int(len(df)),
        "cells_by_condition":{f"ISI{a}_ITI{b}":int(v) for (a,b),v in coverage.items()},
        "representation":FEATURES,
        "primary_test":tests["full_vector"],
        "recovery_only_control":tests["recovery_only"],
        "primary_disposition":primary,
        "secondary_disposition":tests["secondary_disposition"],
        "condition_representation_adequacy":adequacy,
        "biological_chi":primary,
        "Chi_bio":adequacy["disposition"],
        "chi_bio":"NOT_OPENED_NOT_LICENSED",
        "cross_system_interpretation":"Architecture-level comparison only; no numerical or mechanistic identity with E. coli is claimed.",
        "claim_ceiling":"Stentor source-controlled behavioral P0-Q path transport across unseen recovery interval; no molecular mechanism, universal learning law, consciousness claim, common mechanism, or scalar chi_bio."
    }
    (OUT/"STENTOR2026_CROSS_SYSTEM_PATH_P0Q_V01_RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    try:
        main()
    except Exception as e:
        fail={"schema_version":"0.1","experiment_id":"STENTOR2026_CROSS_SYSTEM_PATH_P0Q_V01","status":"EXECUTION_FAILURE_PRESERVED","error_type":type(e).__name__,"error":str(e)}
        OUT.mkdir(parents=True,exist_ok=True)
        (OUT/"STENTOR2026_CROSS_SYSTEM_PATH_P0Q_V01_FAILURE.json").write_text(json.dumps(fail,indent=2)+"\n")
        print(json.dumps(fail,indent=2),file=sys.stderr)
        raise
