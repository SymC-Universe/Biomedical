from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

from src.tool_feasibility_kernel import (
    center_columns,
    cross_validated_modal_predictability,
    linear_cka,
    principal_angles,
    residualize_covariates,
    same_module_abs_spearman,
    stable_seed,
)

SEED_NAMESPACE = "GRI_V2_TOOL_FEASIBILITY_20260830_F2"
N_REPLICATES = 24


def _rng(scenario: str, rep: int, token: str = "DATA") -> np.random.Generator:
    return np.random.default_rng(stable_seed(SEED_NAMESPACE, scenario, rep, token))


def _pca_scores(x: np.ndarray, k: int = 5) -> np.ndarray:
    a = center_columns(x)
    u, s, _ = np.linalg.svd(a, full_matrices=False)
    if len(s) == 0:
        raise ValueError("zero rank")
    eps = np.finfo(float).eps * max(a.shape) * float(s[0])
    rank = int(np.sum(s > eps))
    kk = min(int(k), rank)
    if kk < 1:
        raise ValueError("zero rank")
    return u[:, :kk] * s[:kk]


def _inv_sqrt_psd(a: np.ndarray, ridge: float = 1e-8) -> np.ndarray:
    values, vectors = np.linalg.eigh(0.5 * (a + a.T))
    values = np.maximum(values, ridge)
    return (vectors * (1.0 / np.sqrt(values))) @ vectors.T


def pca_cca_top_corr(x: np.ndarray, y: np.ndarray, k: int = 5) -> float:
    xs = _pca_scores(x, k=k)
    ys = _pca_scores(y, k=k)
    n = xs.shape[0]
    sx = (xs.T @ xs) / max(1, n - 1)
    sy = (ys.T @ ys) / max(1, n - 1)
    sxy = (xs.T @ ys) / max(1, n - 1)
    m = _inv_sqrt_psd(sx) @ sxy @ _inv_sqrt_psd(sy)
    singular = np.linalg.svd(m, compute_uv=False)
    return float(np.clip(singular[0], 0.0, 1.0))


def subspace_similarity(x: np.ndarray, y: np.ndarray, k: int = 5) -> float:
    angles = principal_angles(x, y, top_k=k)
    return float(np.mean(np.cos(angles) ** 2))


def baseline_metrics(x: np.ndarray, y: np.ndarray, scenario: str, rep: int, token: str) -> dict[str, float]:
    pred = cross_validated_modal_predictability(
        x,
        y,
        source_modes=5,
        target_modes=5,
        alpha=0.5,
        folds=5,
        seed=stable_seed("F3_SIMPLE_CV", scenario, rep, token),
    )
    return {
        "cka": float(linear_cka(x, y)),
        "subspace_similarity": subspace_similarity(x, y, 5),
        "pca_cca_top_corr": pca_cca_top_corr(x, y, 5),
        "cv_modal_r2": float(pred["cv_modal_r2"]),
    }


def _s0(rep: int):
    rng = _rng("S0_INDEPENDENT", rep)
    n = 80
    zx = rng.normal(size=(n, 3)); zy = rng.normal(size=(n, 4))
    x = 1.2*zx@rng.normal(size=(3,70)) + 0.7*rng.normal(size=(n,70))
    y = 1.2*zy@rng.normal(size=(4,80)) + 0.7*rng.normal(size=(n,80))
    return x, y


def _s1(rep: int):
    rng = _rng("S1_ONE_SHARED_MODE", rep)
    n=80; z=rng.normal(size=(n,1)); px=rng.normal(size=(n,2)); py=rng.normal(size=(n,2))
    x=1.8*z@rng.normal(size=(1,70))+0.55*px@rng.normal(size=(2,70))+0.7*rng.normal(size=(n,70))
    y=1.8*z@rng.normal(size=(1,80))+0.55*py@rng.normal(size=(2,80))+0.7*rng.normal(size=(n,80))
    return x,y


def _s3(rep: int):
    rng=_rng("S3_CONFOUNDER_ONLY",rep); n=80; c=rng.normal(size=(n,2)); px=rng.normal(size=(n,3)); py=rng.normal(size=(n,3))
    x=2.3*c@rng.normal(size=(2,70))+0.8*px@rng.normal(size=(3,70))+0.55*rng.normal(size=(n,70))
    y=2.3*c@rng.normal(size=(2,80))+0.8*py@rng.normal(size=(3,80))+0.55*rng.normal(size=(n,80))
    return x,y,residualize_covariates(x,c),residualize_covariates(y,c)


def _s4(rep: int):
    rng=_rng("S4_GLOBAL_SHARED_LABEL_SCRAMBLED",rep); n=80; z=rng.normal(size=(n,3))
    x=1.5*z@rng.normal(size=(3,80))+0.55*rng.normal(size=(n,80))
    y=1.5*z@rng.normal(size=(3,90))+0.55*rng.normal(size=(n,90))
    modules=rng.normal(size=(n,16)); a=np.roll(modules,5,axis=1)+0.25*rng.normal(size=(n,16)); b=modules+0.25*rng.normal(size=(n,16))
    return x,y,a,b


def _s5(rep: int):
    rng=_rng("S5_MODULE_SPECIFIC_WEAK_GLOBAL",rep); n=80; modules=rng.normal(size=(n,16))
    a=modules+0.30*rng.normal(size=(n,16)); b=modules+0.30*rng.normal(size=(n,16))
    xs=0.28*modules[:,:4]@rng.normal(size=(4,20)); ys=0.28*modules[:,:4]@rng.normal(size=(4,20))
    x=np.column_stack([xs,rng.normal(size=(n,380))]); y=np.column_stack([ys,rng.normal(size=(n,430))])
    return x,y,a,b


def _s6(rep: int):
    rng=_rng("S6_TECHNICAL_FALSE_CONCORDANCE",rep); n=80
    bx=rng.normal(size=(n,100)); by=rng.normal(size=(n,110)); c=rng.normal(size=(n,1))
    cx=7.0*c@rng.normal(size=(1,8))+0.15*rng.normal(size=(n,8)); cy=7.0*c@rng.normal(size=(1,8))+0.15*rng.normal(size=(n,8))
    return np.column_stack([bx,cx]),np.column_stack([by,cy]),bx,by


def _s9_s10(rep: int):
    rng=_rng("S9_S10_PAIRED",rep); n=80; shared=rng.normal(size=(n,3)); private=rng.normal(size=(n,5))
    source=1.5*shared@rng.normal(size=(3,70))+0.45*rng.normal(size=(n,70))
    low=1.8*shared@rng.normal(size=(3,75))+0.35*rng.normal(size=(n,75))
    high=1.4*shared@rng.normal(size=(3,75))+1.9*private@rng.normal(size=(5,75))+0.35*rng.normal(size=(n,75))
    return source,high,low


def _s11(rep: int):
    rng=_rng("S11_CONFOUNDED_FALSE_AUTONOMY_LOSS",rep); n=80; conf=rng.normal(size=(n,2)); private=rng.normal(size=(n,4))
    source=2.7*conf@rng.normal(size=(2,70))+0.45*rng.normal(size=(n,70))
    target=2.7*conf@rng.normal(size=(2,75))+1.15*private@rng.normal(size=(4,75))+0.45*rng.normal(size=(n,75))
    return source,target,residualize_covariates(source,conf),residualize_covariates(target,conf)


def _record(rows, scenario, rep, representation, metrics, semantic=None):
    row={"scenario":scenario,"replicate":rep,"representation":representation,**metrics}
    if semantic is not None:
        row["naive_same_module_abs_spearman"]=float(semantic)
    rows.append(row)


def run(out: Path):
    rows=[]
    for rep in range(N_REPLICATES):
        x,y=_s0(rep); _record(rows,"S0",rep,"raw",baseline_metrics(x,y,"S0",rep,"raw"))
        x,y=_s1(rep); _record(rows,"S1",rep,"raw",baseline_metrics(x,y,"S1",rep,"raw"))
        x,y,xr,yr=_s3(rep); _record(rows,"S3",rep,"raw",baseline_metrics(x,y,"S3",rep,"raw")); _record(rows,"S3",rep,"adjusted",baseline_metrics(xr,yr,"S3",rep,"adjusted"))
        x,y,a,b=_s4(rep); sem,_=same_module_abs_spearman(a,b); _record(rows,"S4",rep,"raw",baseline_metrics(x,y,"S4",rep,"raw"),sem)
        x,y,a,b=_s5(rep); sem,_=same_module_abs_spearman(a,b); _record(rows,"S5",rep,"raw",baseline_metrics(x,y,"S5",rep,"raw"),sem)
        x,y,xm,ym=_s6(rep); _record(rows,"S6",rep,"raw",baseline_metrics(x,y,"S6",rep,"raw")); _record(rows,"S6",rep,"masked",baseline_metrics(xm,ym,"S6",rep,"masked"))
        source,high,low=_s9_s10(rep); _record(rows,"S9",rep,"raw",baseline_metrics(source,high,"S9",rep,"raw")); _record(rows,"S10",rep,"raw",baseline_metrics(source,low,"S10",rep,"raw"))
        s,t,sr,tr=_s11(rep); _record(rows,"S11",rep,"raw",baseline_metrics(s,t,"S11",rep,"raw")); _record(rows,"S11",rep,"adjusted",baseline_metrics(sr,tr,"S11",rep,"adjusted"))

    grouped=defaultdict(list)
    for r in rows: grouped[(r["scenario"],r["representation"])].append(r)
    summary=[]
    metric_names=["cka","subspace_similarity","pca_cca_top_corr","cv_modal_r2","naive_same_module_abs_spearman"]
    for (scenario,representation), group in sorted(grouped.items()):
        row={"scenario":scenario,"representation":representation,"n":len(group)}
        for name in metric_names:
            vals=[float(g[name]) for g in group if name in g and np.isfinite(float(g[name]))]
            if vals:
                row[f"median_{name}"]=float(np.median(vals))
                row[f"q25_{name}"]=float(np.quantile(vals,0.25))
                row[f"q75_{name}"]=float(np.quantile(vals,0.75))
        summary.append(row)

    # Paired directional contrasts, intentionally descriptive rather than a new pass/fail gate.
    def paired_win(scenario_a, rep_a, scenario_b, rep_b, metric, direction="gt"):
        a={int(r["replicate"]):float(r[metric]) for r in grouped[(scenario_a,rep_a)] if metric in r}
        b={int(r["replicate"]):float(r[metric]) for r in grouped[(scenario_b,rep_b)] if metric in r}
        common=sorted(set(a)&set(b))
        if direction=="gt": wins=[a[i]>b[i] for i in common]; diffs=[a[i]-b[i] for i in common]
        else: wins=[a[i]<b[i] for i in common]; diffs=[b[i]-a[i] for i in common]
        return {"win_rate":float(np.mean(wins)),"median_margin":float(np.median(diffs)),"n":len(common)}

    contrasts={
        "S1_gt_S0":{m:paired_win("S1","raw","S0","raw",m) for m in ["cka","subspace_similarity","pca_cca_top_corr","cv_modal_r2"]},
        "S3_raw_gt_adjusted":{m:paired_win("S3","raw","S3","adjusted",m) for m in ["cka","subspace_similarity","pca_cca_top_corr","cv_modal_r2"]},
        "S6_raw_gt_masked":{m:paired_win("S6","raw","S6","masked",m) for m in ["cka","subspace_similarity","pca_cca_top_corr","cv_modal_r2"]},
        "S10_predictability_gt_S9":{m:paired_win("S10","raw","S9","raw",m) for m in ["cka","subspace_similarity","pca_cca_top_corr","cv_modal_r2"]},
        "S11_raw_gt_adjusted":{m:paired_win("S11","raw","S11","adjusted",m) for m in ["cka","subspace_similarity","pca_cca_top_corr","cv_modal_r2"]},
    }
    s4_sem=[float(r["naive_same_module_abs_spearman"]) for r in grouped[("S4","raw")]]
    s5_sem=[float(r["naive_same_module_abs_spearman"]) for r in grouped[("S5","raw")]]
    contrasts["naive_semantic_S5_gt_S4"]={"win_rate":float(np.mean([a>b for a,b in zip(s5_sem,s4_sem)])),"median_margin":float(np.median(np.asarray(s5_sem)-np.asarray(s4_sem))),"n":len(s4_sem)}

    out.mkdir(parents=True,exist_ok=True)
    keys=sorted({k for r in rows for k in r});
    with (out/"f3_simple_replicates.csv").open("w",newline="",encoding="utf-8") as fh:
        w=csv.DictWriter(fh,fieldnames=keys); w.writeheader(); w.writerows(rows)
    keys2=sorted({k for r in summary for k in r});
    with (out/"f3_simple_summary.csv").open("w",newline="",encoding="utf-8") as fh:
        w=csv.DictWriter(fh,fieldnames=keys2); w.writeheader(); w.writerows(summary)
    payload={
        "status":"F3_SIMPLE_BASELINES_COMPLETE",
        "replicates":N_REPLICATES,
        "seed_namespace":SEED_NAMESPACE,
        "baselines":["raw_linear_CKA","top5_principal_angle_similarity","PCA5_CCA_top_correlation","cross_validated_modal_predictive_R2","naive_same_module_abs_Spearman"],
        "contrasts":contrasts,
        "claim_ceiling":"synthetic baseline comparison only",
        "c1_beta_value_biology_read":False,
        "biological_chi_used":False,
    }
    (out/"F3_SIMPLE_SUMMARY.json").write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(payload,indent=2,sort_keys=True),flush=True)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out",type=Path,default=Path("tool_feasibility_f3_simple_outputs")); args=ap.parse_args(); run(args.out)

if __name__=="__main__": main()
