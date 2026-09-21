from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.linalg import expm

SEED = 20260921
N = 4
K_LOCAL = 1.0
MASS = 1.0
CHI_ISOLATED = 0.15
C_LOCAL = 2.0 * CHI_ISOLATED * np.sqrt(MASS * K_LOCAL)
K_COUPLING = 0.65
DT = 0.05
HORIZON_STEPS = 20
N_TRIALS_PER_TOPOLOGY = 600
TRAIN_FRACTION = 0.75

TOPOLOGIES = {
    "chain": [(0, 1), (1, 2), (2, 3)],
    "ring": [(0, 1), (1, 2), (2, 3), (3, 0)],
    "star": [(0, 1), (0, 2), (0, 3)],
}


def laplacian(edges):
    L = np.zeros((N, N), dtype=float)
    for i, j in edges:
        L[i, i] += 1.0
        L[j, j] += 1.0
        L[i, j] -= 1.0
        L[j, i] -= 1.0
    return L


def adjacency(edges):
    A = np.zeros((N, N), dtype=float)
    for i, j in edges:
        A[i, j] = A[j, i] = 1.0
    return A


def ridge_fit(X, y, lam=1e-8):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    mu = X.mean(axis=0)
    sd = X.std(axis=0)
    sd[sd == 0] = 1.0
    Z = np.column_stack([np.ones(len(X)), (X - mu) / sd])
    penalty = np.eye(Z.shape[1])
    penalty[0, 0] = 0.0
    beta = np.linalg.solve(Z.T @ Z + lam * penalty, Z.T @ y)
    return mu, sd, beta


def predict(model, X):
    mu, sd, beta = model
    X = np.asarray(X, dtype=float)
    Z = np.column_stack([np.ones(len(X)), (X - mu) / sd])
    return Z @ beta


def r2(y, pred):
    y = np.asarray(y, dtype=float)
    pred = np.asarray(pred, dtype=float)
    return float(1.0 - np.sum((y - pred) ** 2) / np.sum((y - y.mean()) ** 2))


def build_rows():
    rng = np.random.default_rng(SEED)
    rows = []
    for topology_name, edges in TOPOLOGIES.items():
        L = laplacian(edges)
        K = K_LOCAL * np.eye(N) + K_COUPLING * L
        C = C_LOCAL * np.eye(N)
        A = np.block([[np.zeros((N, N)), np.eye(N)], [-K / MASS, -C / MASS]])
        horizon = np.linalg.matrix_power(expm(A * DT), HORIZON_STEPS)
        adj = adjacency(edges)
        focal_neighbors = adj[0] > 0
        degree = float(adj[0].sum())

        for trial in range(N_TRIALS_PER_TOPOLOGY):
            x = rng.normal(0.0, 0.40, size=N)
            v = rng.normal(0.0, 0.20, size=N)
            x[0] += rng.normal(0.0, 0.80)
            z = np.concatenate([x, v])
            future = horizon @ z

            local = [x[0], v[0], CHI_ISOLATED]
            topology_onehot = [float(topology_name == k) for k in TOPOLOGIES]
            system = local + [
                degree,
                float(x[focal_neighbors].mean()),
                float(v[focal_neighbors].mean()),
                float(x.mean()),
                float(v.mean()),
            ] + topology_onehot

            rows.append({
                "topology": topology_name,
                "trial": trial,
                "local": local,
                "system": system,
                "target": float(future[0]),
            })
    return rows


def main():
    rows = build_rows()
    split = int(TRAIN_FRACTION * N_TRIALS_PER_TOPOLOGY)
    train = [r for r in rows if r["trial"] < split]
    test = [r for r in rows if r["trial"] >= split]

    y_train = np.asarray([r["target"] for r in train])
    y_test = np.asarray([r["target"] for r in test])
    local_model = ridge_fit([r["local"] for r in train], y_train)
    joint_model = ridge_fit([r["system"] for r in train], y_train)
    local_pred = predict(local_model, [r["local"] for r in test])
    joint_pred = predict(joint_model, [r["system"] for r in test])

    r2_local = r2(y_test, local_pred)
    r2_joint = r2(y_test, joint_pred)
    delta = r2_joint - r2_local

    by_topology = {}
    for name in TOPOLOGIES:
        idx = np.asarray([i for i, r in enumerate(test) if r["topology"] == name], dtype=int)
        yy = y_test[idx]
        a = r2(yy, local_pred[idx])
        b = r2(yy, joint_pred[idx])
        by_topology[name] = {
            "n_test": int(len(idx)),
            "r2_local_only": a,
            "r2_local_plus_system": b,
            "delta_r2": b - a,
        }

    result = {
        "schema": "GRI_JOINT_INFORMATION_MECHANICAL_KNOWN_TRUTH_V01",
        "status": "PASS" if delta >= 0.10 else "FAIL",
        "epistemic_class": "SYNTHETIC_KNOWN_TRUTH",
        "scientific_novelty_claim": False,
        "isolated_chi": CHI_ISOLATED,
        "isolated_chi_identical_across_topologies": True,
        "prediction_target": "focal displacement 1.0 s ahead",
        "r2_local_only": r2_local,
        "r2_local_plus_system": r2_joint,
        "delta_r2_system_information": delta,
        "predeclared_gate": "delta_r2_system_information >= 0.10",
        "by_topology": by_topology,
        "interpretation_ceiling": (
            "Known-truth implementation check only. Network state/coupling contains "
            "predictive information about embedded focal response beyond isolated "
            "chi and focal state. This is not a cross-domain discovery."
        ),
    }

    out = Path("joint_information_known_truth_outputs")
    out.mkdir(exist_ok=True)
    (out / "mechanical_known_truth_v01.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
