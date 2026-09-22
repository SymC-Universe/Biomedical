from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from src import run_scc25_joint_information_p0d_v01 as base

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads(
    (ROOT / "config" / "gri_scc25_reciprocal_joint_information_p0q_20260922_v1.json").read_text()
)
BASE_CFG = json.loads(
    (ROOT / "config" / "gri_scc25_joint_information_p0d_20260922_v1.json").read_text()
)


def evaluate_pair(rna_scores, meth_scores, r, m, treatment):
    cur = np.array(list(range(0, 10)) + list(range(11, 21)), dtype=int)
    nxt = np.array(list(range(1, 11)) + list(range(12, 22)), dtype=int)

    Y = meth_scores[nxt, :m]
    M = meth_scores[cur, :m]
    R = rna_scores[cur, :r]
    arm = treatment.astype(int)

    week = np.array(list(range(1, 11)) + list(range(1, 11)), dtype=float)
    week = week - week.mean()
    tx_week = treatment * week

    X_system = np.column_stack([M, treatment, week, tx_week, np.ones(len(treatment))])
    X_joint = np.column_stack([M, R, treatment, week, tx_week, np.ones(len(treatment))])

    psystem, ok_system = base.loto_predict(X_system, Y)
    pjoint, ok_joint = base.loto_predict(X_joint, Y)
    if not (ok_system and ok_joint):
        return {"r": r, "m": m, "status": "REFUSE_ILL_CONDITIONED"}

    persist = M.copy()
    mean_pred = base.arm_mean_loto(Y, arm)

    system_sse = base.sse(Y, psystem)
    joint_sse = base.sse(Y, pjoint)
    persistence_sse = base.sse(Y, persist)
    arm_mean_sse = base.sse(Y, mean_pred)

    improvement = (
        1.0 - joint_sse / system_sse if system_sse > 0 else float("nan")
    )

    system_err = np.sum((Y - psystem) ** 2, axis=1)
    joint_err = np.sum((Y - pjoint) ** 2, axis=1)
    win_fraction = float(np.mean(joint_err < system_err))

    null_improvements = []
    for sp in CFG["alignment_null"]["pbs_shifts"]:
        for sc in CFG["alignment_null"]["ctx_shifts"]:
            shifted = np.empty_like(R)
            shifted[:10] = np.roll(R[:10], int(sp), axis=0)
            shifted[10:] = np.roll(R[10:], int(sc), axis=0)
            Xn = np.column_stack([
                M, shifted, treatment, week, tx_week, np.ones(len(treatment))
            ])
            pn, ok = base.loto_predict(Xn, Y)
            if not ok:
                return {"r": r, "m": m, "status": "REFUSE_ILL_CONDITIONED"}
            nsse = base.sse(Y, pn)
            null_improvements.append(
                1.0 - nsse / system_sse if system_sse > 0 else float("nan")
            )

    null_arr = np.asarray(null_improvements, dtype=float)
    p_alignment = float(
        (1 + np.sum(null_arr >= improvement)) / (1 + len(null_arr))
    )

    min_baseline = min(persistence_sse, arm_mean_sse)
    support = (
        improvement > 0
        and joint_sse < persistence_sse
        and joint_sse < arm_mean_sse
        and p_alignment <= float(CFG["support_rule"]["exploratory_alpha"])
    )

    if support:
        label = "LOCAL_ADDS_TO_SYSTEM_BEYOND_TIME"
    elif system_sse >= min_baseline and joint_sse >= min_baseline:
        label = "BOTH_INADEQUATE"
    elif improvement <= 0:
        label = "SYSTEM_HISTORY_SUFFICIENT_FOR_THIS_TASK"
    else:
        label = "LOCAL_INCREMENT_UNRESOLVED_BEYOND_TIME"

    return {
        "r": r,
        "m": m,
        "status": "COMPLETE",
        "label": label,
        "system_history_sse": system_sse,
        "joint_reciprocal_sse": joint_sse,
        "persistence_sse": persistence_sse,
        "arm_mean_sse": arm_mean_sse,
        "conditional_improvement_reciprocal": improvement,
        "joint_transition_win_fraction": win_fraction,
        "alignment_null_n": int(len(null_arr)),
        "alignment_null_median_improvement": float(np.median(null_arr)),
        "alignment_null_max_improvement": float(np.max(null_arr)),
        "p_alignment": p_alignment,
    }


def main():
    tmp = Path("joint_information_scc25_reciprocal_tmp")
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
    for r in CFG["rna_ranks"]:
        for m in CFG["methylation_ranks"]:
            results.append(
                evaluate_pair(
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
        "schema": CFG["schema"],
        "status": "PASS" if complete else "REFUSE",
        "epistemic_class": "P0_Q_RECIPROCAL_QUALIFICATION",
        "promotion_effect": "NONE",
        "freeze_doc": CFG["freeze_doc"],
        "scalar_chi_assumed": False,
        "question": (
            "Does current RNA local/modal state improve held-out next-week "
            "methylation-state prediction beyond current methylation state, "
            "treatment arm, linear week, and treatment-by-week trend?"
        ),
        "sources": {"rna": rna_dl, "methylation": meth_dl},
        "rna_representation": rna_meta,
        "methylation_representation": meth_meta,
        "rank_pair_results": results,
        "cross_representation_disposition": cross_rep,
        "claim_ceiling": (
            "Reciprocal P0-Q conditional-information qualification in this SCC25 "
            "source only. No RNA-to-methylation causality, biological scalar chi, "
            "complete capital-Chi ontology, clinical utility, or cross-system "
            "validity is established."
        ),
    }

    outdir = Path("joint_information_scc25_reciprocal_outputs")
    outdir.mkdir(exist_ok=True)
    (outdir / "scc25_reciprocal_joint_information_p0q_v01.json").write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(out, indent=2, sort_keys=True))
    if out["status"] != "PASS":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
