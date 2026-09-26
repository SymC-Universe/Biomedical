#!/usr/bin/env python3
# workflow trigger after registration
from __future__ import annotations
import json, traceback
from pathlib import Path
import numpy as np
import pandas as pd
import meneses2026_path_transport_p0q_v01 as base

SEED=20260925
RNG=np.random.default_rng(SEED)
OUT=Path(__file__).resolve().parent/"meneses2026_depth_conditioned_results"
OUT.mkdir(parents=True,exist_ok=True)
PATHS=["sucrose","sorbitol","sodium","clockwise"]
ALTS=["sorbitol","sodium","clockwise"]
OUTCOMES=["log_tau_dec","log_abs_tau_inc","recovery_fraction"]

def build_source_df():
    rows=[];fails=[];inventory=[]
    for path_name,items in base.FILES.items():
        for c,(rel,blob) in items.items():
            p,_=base.fetch(rel,blob)
            rr,ff,n=base.fit_file(p,path_name,c)
            rows+=rr;fails+=ff
            inventory.append({"path":path_name,"condition_mM":c,"source_trace_count":n,
                              "valid_fit_count":len(rr),"failure_count":len(ff)})
    df=pd.DataFrame(rows)
    if df.empty: raise RuntimeError("no valid source fits")
    df["log_tau_dec"]=np.log(df["tau_dec"].to_numpy(float))
    df["log_abs_tau_inc"]=np.log(np.abs(df["tau_inc"].to_numpy(float)))
    for p in PATHS:
        for c in base.CONCS:
            if len(df[(df.path==p)&(df.condition_mM==c)])<3:
                raise RuntimeError(f"SOURCE_LIMITED:{p}:{c}")
    return df,pd.DataFrame(fails),pd.DataFrame(inventory)

def design(depth,path,rich):
    depth=np.asarray(depth,float)
    cols=[np.ones(len(depth)),depth,depth**2]
    if rich:
        for p in ALTS:
            d=(np.asarray(path)==p).astype(float)
            cols.append(d)
        for p in ALTS:
            d=(np.asarray(path)==p).astype(float)
            cols.append(d*depth)
    return np.column_stack(cols)

def loco(df):
    all_r0=[];all_r1=[]
    folds=[]
    for hold in base.CONCS:
        tr=df.condition_mM.to_numpy(int)!=hold
        te=~tr
        train=df.iloc[np.where(tr)[0]]
        test=df.iloc[np.where(te)[0]]
        Atrain=train.A_dec.to_numpy(float)
        am=float(Atrain.mean()); asd=float(Atrain.std(ddof=1))
        if not np.isfinite(asd) or asd<=0: raise RuntimeError(f"zero depth scale fold {hold}")
        ztr=(Atrain-am)/asd
        zte=(test.A_dec.to_numpy(float)-am)/asd
        X0tr=design(ztr,train.path.to_numpy(),False)
        X0te=design(zte,test.path.to_numpy(),False)
        X1tr=design(ztr,train.path.to_numpy(),True)
        X1te=design(zte,test.path.to_numpy(),True)
        R0=[];R1=[]
        for yname in OUTCOMES:
            ytr=train[yname].to_numpy(float); yte=test[yname].to_numpy(float)
            ym=float(ytr.mean()); ysd=float(ytr.std(ddof=1))
            if not np.isfinite(ysd) or ysd<=0: raise RuntimeError(f"zero outcome scale {yname} fold {hold}")
            zytr=(ytr-ym)/ysd; zyte=(yte-ym)/ysd
            b0=np.linalg.lstsq(X0tr,zytr,rcond=None)[0]
            b1=np.linalg.lstsq(X1tr,zytr,rcond=None)[0]
            r0=zyte-X0te@b0; r1=zyte-X1te@b1
            R0.append(r0);R1.append(r1)
        R0=np.column_stack(R0);R1=np.column_stack(R1)
        all_r0.append(R0);all_r1.append(R1)
        folds.append({"holdout_mM":hold,"n_train":int(tr.sum()),"n_test":int(te.sum()),
                      "m0_mse":float(np.mean(R0**2)),"m1_mse":float(np.mean(R1**2))})
    R0=np.vstack(all_r0);R1=np.vstack(all_r1)
    m0=float(np.mean(R0**2));m1=float(np.mean(R1**2))
    improvement=float((m0-m1)/m0) if m0>0 else float("nan")
    per={}
    for j,n in enumerate(OUTCOMES):
        a=float(np.mean(R0[:,j]**2));b=float(np.mean(R1[:,j]**2))
        per[n]={"m0_mse":a,"m1_mse":b,"fractional_improvement":float((a-b)/a) if a>0 else float("nan")}
    return {"m0_mse":m0,"m1_mse":m1,"fractional_improvement":improvement,
            "per_coordinate":per,"folds":folds}

def bootstrap(df,n=2000):
    vals=[]
    blocks={(p,c):df[(df.path==p)&(df.condition_mM==c)].copy() for p in PATHS for c in base.CONCS}
    for _ in range(n):
        parts=[]
        for (p,c),g in blocks.items():
            idx=RNG.integers(0,len(g),size=len(g))
            parts.append(g.iloc[idx].copy())
        bdf=pd.concat(parts,ignore_index=True)
        try:
            vals.append(loco(bdf)["fractional_improvement"])
        except Exception:
            continue
    if len(vals)<int(.9*n): raise RuntimeError(f"bootstrap success too low {len(vals)}/{n}")
    a=np.asarray(vals,float)
    return {"requested":n,"successful":len(vals),"seed":SEED,
            "median":float(np.median(a)),
            "ci95":[float(np.quantile(a,.025)),float(np.quantile(a,.975))]}

def main():
    df,fails,inventory=build_source_df()
    df.to_csv(OUT/"depth_conditioned_cell_features.csv",index=False)
    fails.to_csv(OUT/"depth_conditioned_fit_failures.csv",index=False)
    inventory.to_csv(OUT/"depth_conditioned_inventory.csv",index=False)
    obs=loco(df)
    boot=bootstrap(df,2000)
    I=obs["fractional_improvement"]; lo,hi=boot["ci95"]
    if I>=0.25 and lo>0:
        disp="DEPTH_INSUFFICIENT_PATH_CONTEXT_REQUIRED_P0Q"
    elif I<=0.10 and hi<=0.10:
        disp="DEPTH_MEDIATED_REORGANIZATION_P0Q"
    else:
        disp="DEPTH_CONDITIONING_UNRESOLVED_P0Q"
    result={
      "schema_version":"0.1","experiment_id":"MENESES2026_DEPTH_CONDITIONED_PATH_P0Q_V01",
      "status":"EXECUTED_VALID_POSTRESULT_CONDITIONAL_P0Q",
      "evidence_class":"P0-Q_POSTRESULT_CONDITIONAL_TRANSPORT_QUALIFICATION",
      "upstream_commit":base.COMMIT,
      "n_valid_cells":int(len(df)),"n_fit_failures":int(len(fails)),
      "models":{"M0":"quadratic collapse-depth only","M1":"quadratic depth plus path intercepts and path-by-depth interactions"},
      "cross_validation":obs,
      "bootstrap":boot,
      "disposition":disp,
      "biological_chi":disp,
      "Chi_bio":"MULTICOORDINATE_MOTOR_RESPONSE_ORGANIZATION_CONDITIONED_ON_COLLAPSE_DEPTH",
      "chi_bio":"NOT_OPENED_NOT_LICENSED",
      "claim_ceiling":"same-source post-result conditional qualification; path information beyond collapse depth if frozen predictive rule passes"
    }
    (OUT/"MENESES2026_DEPTH_CONDITIONED_PATH_P0Q_V01_RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    try:main()
    except Exception as e:
        fail={"schema_version":"0.1","experiment_id":"MENESES2026_DEPTH_CONDITIONED_PATH_P0Q_V01",
              "status":"EXECUTION_FAILURE_PRESERVED","error_type":type(e).__name__,"error":str(e),
              "traceback":traceback.format_exc()}
        (OUT/"MENESES2026_DEPTH_CONDITIONED_PATH_P0Q_V01_FAILURE.json").write_text(json.dumps(fail,indent=2)+"\n")
        print(json.dumps(fail,indent=2))
        raise
