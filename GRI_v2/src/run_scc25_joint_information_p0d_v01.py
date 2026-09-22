from __future__ import annotations

import csv
import gzip
import hashlib
import io
import json
import math
import urllib.request
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "config" / "gri_scc25_joint_information_p0d_20260922_v1.json").read_text())
MANIFEST = json.loads((ROOT / "config" / "gri_scc25_paired_timecourse_manifest_p0d_v0_1.json").read_text())
RNA_FREEZE = json.loads((ROOT / "config" / "gri_Chi_bio_chronic_g2_r1_A3_empirical_freeze_20260913_v1.json").read_text())

RNA_SOURCE = RNA_FREEZE["source_binding"]["processed_file_url"]
RNA_SHA256 = RNA_FREEZE["source_binding"]["processed_file_sha256"]
METH_BIND = MANIFEST["processed_source_bindings"]["methylation_processed_matrix"]
METH_SOURCE = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE98nnn/GSE98813/matrix/GSE98813_series_matrix.txt.gz"
METH_SHA256 = METH_BIND["sha256"]

BATCH = 4096


def download_verify(url: str, expected_sha256: str, dest: Path) -> dict:
    h = hashlib.sha256()
    n = 0
    with urllib.request.urlopen(url, timeout=120) as r, dest.open("wb") as out:
        while True:
            chunk = r.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)
            h.update(chunk)
            n += len(chunk)
    observed = h.hexdigest()
    if observed != expected_sha256:
        raise RuntimeError(f"SHA256 mismatch for {url}: {observed} != {expected_sha256}")
    return {"url": url, "sha256": observed, "size_bytes": n}


def stripq(s: str) -> str:
    return s.strip().strip('"')


def load_rna(path: Path, pbs_cols: list[str], ctx_cols: list[str]) -> tuple[np.ndarray, dict]:
    wanted = pbs_cols + ctx_cols
    features = []
    retained_ids = []

    with gzip.open(path, "rt", encoding="utf-8", errors="strict", newline="") as fh:
        reader = csv.reader(fh, delimiter="\t")
        header = next(reader)
        index = {stripq(v): i for i, v in enumerate(header)}
        missing = [c for c in wanted if c not in index]
        if missing:
            raise RuntimeError(f"RNA columns missing: {missing}")
        gene_idx = index.get("GENE", 0)
        col_idx = [index[c] for c in wanted]

        for row in reader:
            if not row:
                continue
            gene = stripq(row[gene_idx])
            try:
                vals = np.array([float(stripq(row[i])) for i in col_idx], dtype=float)
            except (ValueError, IndexError):
                continue
            if not np.all(np.isfinite(vals)) or np.any(vals < 0):
                continue
            if np.sum(vals[:11] >= 1.0) < 6:
                continue

            tr = np.log2(vals + 1.0)
            centered = tr - tr[:11].mean()
            features.append(centered)
            retained_ids.append(gene)

    X = np.asarray(features, dtype=float).T
    if X.shape[0] != 22:
        raise RuntimeError(f"Unexpected RNA state count {X.shape}")
    expected = int(RNA_FREEZE["feature_gate_preoutcome_qualification"]["retained_gene_count"])
    if X.shape[1] != expected:
        raise RuntimeError(f"RNA retained gene count {X.shape[1]} != frozen {expected}")

    U, S, Vt = np.linalg.svd(X[:11], full_matrices=False)

    # Canonicalize each loading sign by the frozen max-absolute-loading rule.
    for j in range(Vt.shape[0]):
        k = int(np.argmax(np.abs(Vt[j])))
        if Vt[j, k] < 0:
            Vt[j] *= -1.0
            U[:, j] *= -1.0

    scores = X @ Vt.T
    return scores, {
        "retained_gene_count": int(X.shape[1]),
        "pbs_singular_values_first5": [float(x) for x in S[:5]],
    }


def process_methylation_batch(rows, pbs_count, G, H):
    if not rows:
        return 0
    A = np.asarray(rows, dtype=float)
    mu = A[:, :pbs_count].mean(axis=1, keepdims=True)
    C = A - mu
    P = C[:, :pbs_count]
    G += P.T @ P
    H += C.T @ P
    return A.shape[0]


def load_methylation_scores(path: Path, selected_gsms: list[str]) -> tuple[np.ndarray, dict]:
    G = np.zeros((11, 11), dtype=float)
    H = np.zeros((22, 11), dtype=float)
    complete = 0
    batch = []
    header_seen = False

    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as fh:
        col_idx = None
        for line in fh:
            if not header_seen:
                if line.startswith('"ID_REF"') or line.startswith("ID_REF"):
                    header = [stripq(x) for x in line.rstrip("\n").split("\t")]
                    index = {v: i for i, v in enumerate(header)}
                    missing = [g for g in selected_gsms if g not in index]
                    if missing:
                        raise RuntimeError(f"Methylation GSM columns missing: {missing}")
                    col_idx = [index[g] for g in selected_gsms]
                    header_seen = True
                continue

            if line.startswith("!series_matrix_table_end"):
                break
            if not line.strip() or line.startswith("!"):
                continue
            row = line.rstrip("\n").split("\t")
            try:
                vals = np.array([float(stripq(row[i])) for i in col_idx], dtype=float)
            except (ValueError, IndexError):
                continue
            if not np.all(np.isfinite(vals)):
                continue
            batch.append(vals)
            if len(batch) >= BATCH:
                complete += process_methylation_batch(batch, 11, G, H)
                batch = []

    complete += process_methylation_batch(batch, 11, G, H)

    if not header_seen or complete == 0:
        raise RuntimeError("No complete methylation matrix rows were parsed")

    evals, U = np.linalg.eigh(G)
    order = np.argsort(evals)[::-1]
    evals = evals[order]
    U = U[:, order]
    positive = evals > np.finfo(float).eps * max(1.0, float(evals[0]))
    if int(np.sum(positive)) < 3:
        raise RuntimeError("Methylation PBS basis has fewer than 3 positive modes")
    S = np.sqrt(np.maximum(evals, 0.0))

    # Deterministic sample-space orientation.
    for j in range(U.shape[1]):
        k = int(np.argmax(np.abs(U[:, j])))
        if U[k, j] < 0:
            U[:, j] *= -1.0

    scores = H @ U
    for j in range(scores.shape[1]):
        if S[j] > 0:
            scores[:, j] /= S[j]
        else:
            scores[:, j] = 0.0

    return scores, {
        "complete_cpg_count": int(complete),
        "pbs_eigenvalues_first5": [float(x) for x in evals[:5]],
    }


def loto_predict(X: np.ndarray, Y: np.ndarray) -> tuple[np.ndarray | None, bool]:
    n, p = X.shape
    pred = np.empty_like(Y, dtype=float)
    for i in range(n):
        keep = np.arange(n) != i
        Xt = X[keep]
        Yt = Y[keep]
        if np.linalg.matrix_rank(Xt) < p:
            return None, False
        beta, _, _, _ = np.linalg.lstsq(Xt, Yt, rcond=None)
        pred[i] = X[i] @ beta
    return pred, True


def sse(y, pred) -> float:
    return float(np.sum((np.asarray(y) - np.asarray(pred)) ** 2))


def arm_mean_loto(Y: np.ndarray, arm: np.ndarray) -> np.ndarray:
    out = np.empty_like(Y)
    for i in range(len(Y)):
        keep = (np.arange(len(Y)) != i) & (arm == arm[i])
        out[i] = Y[keep].mean(axis=0)
    return out


def evaluate_pair(rna_scores, meth_scores, r, m, treatment):
    cur = np.array(list(range(0, 10)) + list(range(11, 21)), dtype=int)
    nxt = np.array(list(range(1, 11)) + list(range(12, 22)), dtype=int)

    Y = rna_scores[nxt, :r]
    R = rna_scores[cur, :r]
    M = meth_scores[cur, :m]
    arm = treatment.astype(int)

    X_local = np.column_stack([R, treatment, np.ones(len(treatment))])
    X_joint = np.column_stack([R, M, treatment, np.ones(len(treatment))])

    plocal, ok_local = loto_predict(X_local, Y)
    pjoint, ok_joint = loto_predict(X_joint, Y)
    if not (ok_local and ok_joint):
        return {"r": r, "m": m, "status": "REFUSE_ILL_CONDITIONED"}

    persist = R.copy()
    mean_pred = arm_mean_loto(Y, arm)

    local_sse = sse(Y, plocal)
    joint_sse = sse(Y, pjoint)
    persistence_sse = sse(Y, persist)
    arm_mean_sse = sse(Y, mean_pred)
    improvement = 1.0 - joint_sse / local_sse if local_sse > 0 else float("nan")

    local_err = np.sum((Y - plocal) ** 2, axis=1)
    joint_err = np.sum((Y - pjoint) ** 2, axis=1)
    win_fraction = float(np.mean(joint_err < local_err))

    # Independent nonzero circular shifts of current methylation within each arm.
    null_improvements = []
    for sp in CFG["alignment_null"]["pbs_shifts"]:
        for sc in CFG["alignment_null"]["ctx_shifts"]:
            shifted = np.empty_like(M)
            shifted[:10] = np.roll(M[:10], int(sp), axis=0)
            shifted[10:] = np.roll(M[10:], int(sc), axis=0)
            Xn = np.column_stack([R, shifted, treatment, np.ones(len(treatment))])
            pn, ok = loto_predict(Xn, Y)
            if not ok:
                return {"r": r, "m": m, "status": "REFUSE_ILL_CONDITIONED"}
            nsse = sse(Y, pn)
            null_improvements.append(1.0 - nsse / local_sse if local_sse > 0 else float("nan"))

    null_arr = np.asarray(null_improvements, dtype=float)
    p_alignment = float((1 + np.sum(null_arr >= improvement)) / (1 + len(null_arr)))

    support = (
        improvement > 0
        and joint_sse < persistence_sse
        and joint_sse < arm_mean_sse
        and p_alignment <= float(CFG["support_rule"]["exploratory_alpha"])
    )
    min_baseline = min(persistence_sse, arm_mean_sse)

    if support:
        label = "SYSTEM_CONTEXT_ADDS_INFORMATION"
    elif local_sse >= min_baseline and joint_sse >= min_baseline:
        label = "BOTH_INADEQUATE"
    elif improvement <= 0:
        label = "LOCAL_MODAL_SUFFICIENT_FOR_THIS_TASK"
    else:
        label = "ALIGNMENT_DEPENDENT_UNRESOLVED"

    return {
        "r": r,
        "m": m,
        "status": "COMPLETE",
        "label": label,
        "local_sse": local_sse,
        "joint_sse": joint_sse,
        "persistence_sse": persistence_sse,
        "arm_mean_sse": arm_mean_sse,
        "conditional_improvement": improvement,
        "joint_transition_win_fraction": win_fraction,
        "alignment_null_n": int(len(null_arr)),
        "alignment_null_median_improvement": float(np.median(null_arr)),
        "alignment_null_max_improvement": float(np.max(null_arr)),
        "p_alignment": p_alignment,
    }


def main():
    tmp = Path("joint_information_scc25_tmp")
    tmp.mkdir(exist_ok=True)
    rna_path = tmp / "GSE98812_GEOExprsData.txt.gz"
    meth_path = tmp / "GSE98813_series_matrix.txt.gz"

    rna_dl = download_verify(RNA_SOURCE, RNA_SHA256, rna_path)
    meth_dl = download_verify(METH_SOURCE, METH_SHA256, meth_path)

    pbs_records = sorted([x for x in MANIFEST["main_timecourse"] if x["arm"] == "PBS"], key=lambda x: x["week"])
    ctx_records = sorted([x for x in MANIFEST["main_timecourse"] if x["arm"] == "CTX"], key=lambda x: x["week"])

    pbs_cols = RNA_FREEZE["source_binding"]["pbs_columns"]
    ctx_cols = RNA_FREEZE["source_binding"]["ctx_columns"]
    selected_gsms = [x["methylation_gsm"] for x in pbs_records] + [x["methylation_gsm"] for x in ctx_records]

    rna_scores, rna_meta = load_rna(rna_path, pbs_cols, ctx_cols)
    meth_scores, meth_meta = load_methylation_scores(meth_path, selected_gsms)

    treatment = np.array([0.0] * 10 + [1.0] * 10)
    results = []
    for r in CFG["local_representation"]["ranks"]:
        for m in CFG["system_context_representation"]["ranks"]:
            results.append(evaluate_pair(rna_scores, meth_scores, int(r), int(m), treatment))

    labels = [x.get("label", x["status"]) for x in results]
    complete = all(x["status"] == "COMPLETE" for x in results)
    if complete and len(set(labels)) == 1:
        cross_rep = labels[0]
    elif complete:
        cross_rep = "REPRESENTATION_DEPENDENT"
    else:
        cross_rep = "REFUSE_ILL_CONDITIONED"

    out = {
        "schema": CFG["schema"],
        "status": "PASS" if complete else "REFUSE",
        "epistemic_class": "P0_D_EXPLORATORY_POSTRESULT_JOINT_INFORMATION",
        "promotion_effect": "NONE",
        "freeze_commit_precedes_execution": True,
        "scalar_chi_assumed": False,
        "question": "Does current methylation context improve held-out next-week RNA modal-state prediction beyond current RNA state and treatment arm?",
        "sources": {"rna": rna_dl, "methylation": meth_dl},
        "rna_representation": rna_meta,
        "methylation_representation": meth_meta,
        "rank_pair_results": results,
        "cross_representation_disposition": cross_rep,
        "claim_ceiling": (
            "Exploratory conditional predictive information in this paired SCC25 weekly source only. "
            "No methylation causality, biological scalar chi, capital-Chi ontology, clinical utility, "
            "or cross-system transport is established."
        ),
    }

    outdir = Path("joint_information_scc25_outputs")
    outdir.mkdir(exist_ok=True)
    (outdir / "scc25_joint_information_p0d_v01.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))
    if out["status"] != "PASS":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
