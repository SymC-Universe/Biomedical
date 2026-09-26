#!/usr/bin/env python3
"""Post-result root-cause diagnostics for Meneses context transport."""
from __future__ import annotations
import itertools, json, sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist
from scipy.stats import spearmanr

import meneses2026_ecoli_pmf_recovery_p0q_v01 as base
from meneses2026_source_method_reconciliation_v01 import fit_immediate_manuscript
from meneses2026_immediate_context_transport_p0q_v01 import CONTEXTS, CONCS, FEATURES, zwithin, geom_vec

OUT=Path(__file__).resolve().parent/"meneses2026_context_transport_diagnostics"
OUT.mkdir(parents=True,exist_ok=True)
SEED=20260925
B=2000
RNG=np.random.default_rng(SEED)

def matrix_from_df(df, agg="median", cols=FEATURES):
    rows=[]
    for c in CONCS:
        z=df[(df.condition_mM==c)&(df.fit_valid)]
        if len(z)==0: raise RuntimeError(f"no valid fit for {c}")
        vals=[]
        for f in cols:
            a=z[f].to_numpy(float)
            a=a[np.isfinite(a)]
            if not len(a): raise RuntimeError(f"no finite {f} for {c}")
            vals.append(float(np.median(a) if agg=="median" else np.mean(a)))
        rows.append(vals)
    return np.asarray(rows,float)

def exact_rho(ref,target):
    rv=geom_vec(ref); tv=geom_vec(target)
    obs=float(spearmanr(rv,tv).statistic)
    vals=[]
    for perm in itertools.permutations(range(4)):
        vals.append(float(spearmanr(rv,geom_vec(target[list(perm),:])).statistic))
    return obs,float(np.mean(np.asarray(vals)>=obs-1e-15))

def build_fits():
    dfs={}
    for ctx,items in CONTEXTS.items():
        parts=[]
        for c,(path,blob,nexp) in items.items():
            p=base.fetch(path,blob)
            d=pd.DataFrame(fit_immediate_manuscript(p,c))
            d["context"]=ctx
            if len(d)!=nexp: raise RuntimeError(f"trace count mismatch {ctx} {c}")
            parts.append(d)
        dfs[ctx]=pd.concat(parts,ignore_index=True)
    return dfs

def bootstrap_matrix(df):
    rows=[]
    for c in CONCS:
        z=df[(df.condition_mM==c)&(df.fit_valid)]
        idx=RNG.integers(0,len(z),size=len(z))
        b=z.iloc[idx]
        rows.append([float(np.median(b[f].to_numpy(float))) for f in FEATURES])
    return np.asarray(rows,float)

def root_class(primary_rho, loo, mean_rho, boot):
    vals=list(loo.values())
    n_hi=sum(v>=0.8 for v in vals)
    if n_hi==1 and all(v<0.5 for v in vals if v<0.8):
        return "SINGLE_COORDINATE_LEVERAGE"
    lo=float(np.quantile(boot,.025)); hi=float(np.quantile(boot,.975))
    if mean_rho>=0.8 and primary_rho<0.5 and lo<=0 and hi>=0.8:
        return "CENTRAL_TENDENCY_SENSITIVE"
    if float(np.median(boot))<0.5 and float(np.mean(boot<=0))>=0.25 and max(vals)<0.8:
        return "DISTRIBUTED_CONTEXT_REORGANIZATION"
    return "MULTIFACTOR_OR_UNRESOLVED_CONTEXT_REORGANIZATION"

def main():
    dfs=build_fits()
    med={c:matrix_from_df(dfs[c],"median") for c in dfs}
    mean={c:matrix_from_df(dfs[c],"mean") for c in dfs}
    ref="sucrose_MB_CCW"
    targets=["sorbitol_MB_CCW","sucrose_SPB_CCW","sucrose_CW_lock"]
    out={}
    for target in targets:
        primary_rho,_=exact_rho(med[ref],med[target])
        loo={}
        for omit in FEATURES:
            keep=[i for i,f in enumerate(FEATURES) if f!=omit]
            rr,_=exact_rho(med[ref][:,keep],med[target][:,keep])
            loo[omit]=rr
        mean_rho,mean_p=exact_rho(mean[ref],mean[target])
        boots=np.empty(B,float)
        for i in range(B):
            rb=bootstrap_matrix(dfs[ref])
            tb=bootstrap_matrix(dfs[target])
            boots[i]=float(spearmanr(geom_vec(rb),geom_vec(tb)).statistic)
        out[target]={
          "primary_median_geometry_rho":primary_rho,
          "leave_one_coordinate_out_rho":loo,
          "mean_based_geometry_rho":mean_rho,
          "mean_based_exact_p_24_permutations":mean_p,
          "bootstrap":{
            "B":B,"seed":SEED,
            "median_rho":float(np.median(boots)),
            "q025":float(np.quantile(boots,.025)),
            "q975":float(np.quantile(boots,.975)),
            "fraction_rho_ge_0_5":float(np.mean(boots>=0.5)),
            "fraction_rho_ge_0_8":float(np.mean(boots>=0.8)),
            "fraction_rho_le_0":float(np.mean(boots<=0))
          }
        }
    spb=out["sucrose_SPB_CCW"]
    # reconstruct bootstrap array deterministically for classification values is not needed; use summary-compatible proxy:
    # rerun once for SPB to preserve exact rule calculation.
    RNG2=np.random.default_rng(SEED)
    # consume bootstrap draws for sorbitol first because main loop did so
    for _ in range(B):
        for df in (dfs[ref],dfs["sorbitol_MB_CCW"]):
            for c in CONCS:
                z=df[(df.condition_mM==c)&(df.fit_valid)]
                RNG2.integers(0,len(z),size=len(z))
    # simpler exact classification from saved bootstrap requires full array; recompute SPB with isolated fixed seed documented separately.
    rng=np.random.default_rng(SEED+1)
    spb_boot=np.empty(B,float)
    def bootmat_with_rng(df,r):
        rows=[]
        for c in CONCS:
            z=df[(df.condition_mM==c)&(df.fit_valid)]
            idx=r.integers(0,len(z),size=len(z))
            b=z.iloc[idx]
            rows.append([float(np.median(b[f].to_numpy(float))) for f in FEATURES])
        return np.asarray(rows,float)
    for i in range(B):
        spb_boot[i]=float(spearmanr(geom_vec(bootmat_with_rng(dfs[ref],rng)),
                                      geom_vec(bootmat_with_rng(dfs["sucrose_SPB_CCW"],rng))).statistic)
    spb["classification_bootstrap_seed"]=SEED+1
    spb["classification_bootstrap_summary"]={
      "median_rho":float(np.median(spb_boot)),
      "q025":float(np.quantile(spb_boot,.025)),
      "q975":float(np.quantile(spb_boot,.975)),
      "fraction_rho_le_0":float(np.mean(spb_boot<=0))
    }
    spb["root_cause_disposition"]=root_class(
      spb["primary_median_geometry_rho"],
      spb["leave_one_coordinate_out_rho"],
      spb["mean_based_geometry_rho"],
      spb_boot
    )
    result={
      "schema_version":"0.1",
      "experiment_id":"MENESES2026_CONTEXT_TRANSPORT_ROOT_CAUSE_V01",
      "status":"EXECUTED_POSTRESULT_ROOT_CAUSE_DIAGNOSTIC",
      "evidence_class":"POST_RESULT_ROOT_CAUSE_STABILITY_DIAGNOSTIC",
      "diagnostics":out,
      "primary_transport_unchanged":true if False else True,
      "chi_bio":"NOT_OPENED_NOT_LICENSED",
      "claim_ceiling":"diagnostic only; cannot promote or replace primary transport classifications"
    }
    (OUT/"MENESES2026_CONTEXT_TRANSPORT_ROOT_CAUSE_V01_RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    try: main()
    except Exception as e:
        fail={"schema_version":"0.1","experiment_id":"MENESES2026_CONTEXT_TRANSPORT_ROOT_CAUSE_V01",
              "status":"EXECUTION_FAILURE_PRESERVED","error_type":type(e).__name__,"error":str(e)}
        (OUT/"MENESES2026_CONTEXT_TRANSPORT_ROOT_CAUSE_V01_FAILURE.json").write_text(json.dumps(fail,indent=2)+"\n")
        print(json.dumps(fail,indent=2),file=sys.stderr)
        raise
