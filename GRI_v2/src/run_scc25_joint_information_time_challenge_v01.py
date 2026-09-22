from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from src import run_scc25_joint_information_p0d_v01 as base

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "config" / "gri_scc25_joint_information_p0d_20260922_v1.json").read_text())


def evaluate_time_pair(rna_scores, meth_scores, r, m, treatment):
    cur = np.array(list(range(0, 10)) + list(range(11, 21)), dtype=int)
    nxt = np.array(list(range(1, 11)) + list(range(12, 22)), dtype=int)

    Y = rna_scores[nxt, :r]
    R = rna_scores[cur, :r]
    M = meth_scores[cur, :m]
    arm = treatment.astype(int)

    week = np.array(list(range(1, 11)) + list(range(1, 11)), dtype=float)
    week = week - week.mean()
    tx_week = treatment * week

    X_local = np.column_stack([R, treatment, week, tx_week, np.ones(len(treatment))])
    X_joint = np.column_stack([R, M, treatment, week, tx_week, np.ones(len(treatment))])

    plocal, ok_local = base.loto_predict(X_local, Y)
    pjoint, ok_joint = base.loto_predict(X_joint, Y)
    if not (ok_local and ok_joint):
        return {"r": r, "m": m, "status": "REFUSE_ILL_CONDITIONED"}

    persist = R.copy()
    mean_pred = base.arm_mean_loto(Y, arm)

    local_sse = base.sse(Y, plocal)
    joint_sse = base.sse(Y, pjoint)
    persistence_sse = base.sse(Y, persist)
    arm_mean_sse = base.sse(Y, mean_pred)
    improvement = 1.0 - joint_sse / local_sse if local_sse > 0 else float("nan")

    local_err = np.sum((Y - plocal) ** 2, axis=1)
    joint_err = np.sum((Y - pjoint) ** 2, axis=1)
    win_fraction = float(np.mean(joint_err < local_err))

    null_improvements = []
    for sp in CFG["alignment_null"]["pbs_shifts"]:
        for sc in CFG["alignment_null"]["ctx_shifts"]:
            shifted = np.empty_like(M)
            shifted[:10] = np.roll(M[:10], int(sp), axis=0)
            shifted[10:] = np.roll(M[10:], int(sc), axis=0)
            Xn = np.column_stack([
                R, shifted, treatment, week, tx_week, np.ones(len(treatment))
            ])
            pn, ok = base.loto_predict(Xn, Y)
            if not ok:
                return {"r": r, "m": m, "status": "REFUSE_ILL_CONDITIONED"}
            nsse = base.sse(Y, pn)
            null_improvements.append(
                1.0 - nsse / local_sse if local_sse > 0 else float("nan")
            )

    null_arr = np.asarray(null_improvements, dtype=float)
    p_alignment = float((1 + np.sum(null_arr >= improvement)) / (1 + len(null_arr)))

    if (
        improvement > 0
        and joint_sse < persistence_sse
        and joint_sse < arm_mean_sse
        and p_alignment <= 0.10
    ):
        label = "CONTEXT_ADDS_BEYOND_TIME"
    elif improvement <= 0:
        label = "TIME_SUBSUMES_CONTEXT_INCREMENT"
    else:
        label = "CONTEXT_INCREMENT_UNRESOLVED_BEYOND_TIME"

    return {
        "r": r,
        "m": m,
        "status": "COMPLETE",
        "label": label,
        "local_time_sse": local_sse,
        "joint_time_sse": joint_sse,
        "persistence_sse": persistence_sse,
        "arm_mean_sse": arm_mean_sse,
        "conditional_improvement_beyond_time": improvement,
        "joint_transition_win_fraction": win_fraction,
        "alignment_null_n": int(len(null_arr)),
        "alignment_null_median_improvement": float(np.median(null_arr)),
        "alignment_null_max_improvement": float(np.max(null_arr)),
        "p_alignment": p_alignment,
    }


def main():
    tmp = Path("joint_information_scc25_time_tmp")
    tmp.mkdir(exist_ok=True)
    rna_path = tmp / "GSE98812_GEOExprsData.txt.gz"
    meth_path = tmp / "GSE98813_series_matrix.txt.gz"

    rna_dl = base.download_verify(base.RNA_SOURCE, base.RNA_SHA256, rna_path)
    meth_dl = base.download_verify(base.METH_SOURCE, base.METH_SHA256, meth_path)

    pbs_records = sorted(
        [x for x in base.MANIFEST["main_timecourse"] if x["arm"] == "PBS"],
        key=lambda x: x["week"],
    )
    ctx_records = sorted(
        [x for x in base.MANIFEST["main_timecourse"] if x["arm"] == "CTX"],
        key=lambda x: x["week"],
    )

    pbs_cols = base.RNA_FREEZE["source_binding"]["pbs_columns"]
    ctx_cols = base.RNA_FREEZE["source_binding"]["ctx_columns"]
    selected_gsms = (
        [x["methylation_gsm"] for x in pbs_records]
        + [x["methylation_gsm"] for x in ctx_records]
    )

    rna_scores, rna_meta = base.load_rna(rna_path, pbs_cols, ctx_cols)
    meth_scores, meth_meta = base.load_methylation_scores(meth_path, selected_gsms)

    treatment = np.array([0.0] * 10 + [1.0] * 10)

    results = []
    for r in CFG["local_representation"]["ranks"]:
        for m in CFG["system_context_representation"]["ranks"]:
            results.append(
                evaluate_time_pair(
                    rna_scores, meth_scores, int(r), int(m), treatment
                )
            )

    labels = [x.get("label", x["status"]) for x in results]
    complete = all(x["status"] == "COMPLETE" for x in results)
    if complete and len(set(labels)) == 1:
        cross_rep = labels[0]
    elif complete:
        cross_rep = "REPRESENTATION_DEPENDENT"
    else:
        cross_rep = "REFUSE_ILL_CONDITIONED"

    out = {
        "schema": "GRI_SCC25_JOINT_INFORMATION_TIME_CHALLENGE_V01",
        "status": "PASS" if complete else "REFUSE",
        "epistemic_class": "P0_Q_RETROSPECTIVE_QUALIFICATION",
        "promotion_effect": "NONE",
        "trigger_run": 35728155463,
        "freeze_doc": "GRI_v2/docs/GRI_SCC25_JOINT_INFORMATION_TIME_CHALLENGE_FREEZE_20260922.md",
        "scalar_chi_assumed": False,
        "question": (
            "Does methylation context improve held-out next-week RNA modal-state "
            "prediction beyond current RNA state, treatment arm, linear week, and "
            "treatment-by-week trend?"
        ),
        "sources": {"rna": rna_dl, "methylation": meth_dl},
        "rna_representation": rna_meta,
        "methylation_representation": meth_meta,
        "rank_pair_results": results,
        "cross_representation_disposition": cross_rep,
        "claim_ceiling": (
            "Retrospective qualification of the P0-D SCC25 result only. A positive "
            "result would show predictive information beyond the tested linear time "
            "terms in this source, not methylation causality, a biological scalar chi, "
            "or cross-system capital-Chi validity."
        ),
    }

    outdir = Path("joint_information_scc25_time_outputs")
    outdir.mkdir(exist_ok=True)
    (outdir / "scc25_joint_information_time_challenge_v01.json").write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(out, indent=2, sort_keys=True))
    if out["status"] != "PASS":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
