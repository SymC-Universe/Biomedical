#!/usr/bin/env python3
# workflow trigger after registration
"""Post-result source-method reconciliation for Meneses 2026 E. coli PMF data.

Uses the manuscript-facing sucrose fitting method frozen in
MENESES2026_SOURCE_METHOD_RECONCILIATION_FREEZE_20260925.md.
This script cannot promote the primary P0-Q result.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.stats import spearmanr
import meneses2026_ecoli_pmf_recovery_p0q_v01 as base

OUT = Path(__file__).resolve().parent / "meneses2026_reconciliation_results"
OUT.mkdir(parents=True, exist_ok=True)

def fit_immediate_manuscript(path, conc):
    df=pd.read_parquet(path)
    t,cols=base.wide_traces(df)
    rows=[]
    for c in cols:
        y=pd.to_numeric(df[c],errors="coerce").to_numpy(float)
        valid=np.isfinite(t)&np.isfinite(y)
        tt=t[valid]; yy=y[valid]
        baseline=float(np.average(yy[tt<=180]))
        rec={"condition_mM":conc,"trace":c,"baseline":baseline,"fit_valid":False}
        if not np.isfinite(baseline) or baseline==0:
            rec["failure"]="invalid_baseline"; rows.append(rec); continue
        yn=yy/baseline
        speed_initial=float(np.average(yn[(tt>=155)&(tt<=175)]))
        speed_final=float(np.average(yn[(tt>=215)&(tt<=235)]))
        A_dec=speed_initial-speed_final
        C_dec=speed_final
        speed_increase_min=float(np.average(yn[(tt>=240)&(tt<=260)]))
        speed_increase_max=float(np.average(yn[(tt>=330)&(tt<=350)]))
        md=(tt>=175)&(tt<=240)
        mi=(tt>250)&(tt<=360)
        try:
            def dec(x,tau,t0):
                z=np.clip((x-175.0-t0)/tau,-700,700)
                return A_dec/(1+np.exp(z))+C_dec
            pdec,_=curve_fit(dec,tt[md],yn[md],p0=[10,10],bounds=(0,np.inf),maxfev=50000)
            tau_dec,t0_dec=pdec
            def inc(x,tau,t0):
                z=np.clip(-(x-270.0-t0)/tau,-700,700)
                return speed_increase_min+(speed_increase_max-speed_increase_min)/(1+np.exp(z))
            pinc,_=curve_fit(inc,tt[mi],yn[mi],p0=[3,-10],maxfev=50000)
            tau_inc,t0_inc=pinc
            if not all(np.isfinite([A_dec,C_dec,tau_dec,t0_dec,tau_inc,t0_inc,speed_increase_min,speed_increase_max])):
                raise RuntimeError("nonfinite_source_fit")
            rec.update({"fit_valid":True,"A_dec":float(A_dec),"C_dec":float(C_dec),
                        "tau_dec":float(tau_dec),"t0_dec":float(t0_dec),
                        "tau_inc":float(tau_inc),"t0_inc":float(t0_inc),
                        "speed_increase_min":speed_increase_min,"speed_increase_max":speed_increase_max,
                        "tau_inc_positive":bool(tau_inc>0)})
        except Exception as e:
            rec["failure"]=f"{type(e).__name__}:{e}"
        rows.append(rec)
    return rows

def med_by_cond(df,col):
    out={}
    for c in base.CONCS:
        z=df[(df.condition_mM==c)&(df.fit_valid)][col].to_numpy(float)
        z=z[np.isfinite(z)]
        out[c]=float(np.median(z)) if len(z) else float("nan")
    return out

def rho(vals):
    a=np.array([vals[c] for c in base.CONCS],float)
    return float(spearmanr(base.CONCS,a).statistic) if np.all(np.isfinite(a)) else float("nan")

def ratio(vals):
    a=np.array([vals[c] for c in base.CONCS],float)
    a=a[np.isfinite(a)&(a>0)]
    return float(np.max(a)/np.min(a)) if len(a)==4 else float("nan")

def main():
    paths={}
    for family,items in base.FILES.items():
        paths[family]={}
        for c,(path,blob) in items.items():
            paths[family][c]=base.fetch(path,blob)

    immediate=[]
    sustained=[]
    for c in base.CONCS:
        immediate += fit_immediate_manuscript(paths["immediate"][c],c)
        sustained += base.fit_sustained(paths["sustained"][c],c)
    idf=pd.DataFrame(immediate); sdf=pd.DataFrame(sustained)
    idf.to_csv(OUT/"immediate_motor_manuscript_method_fits.csv",index=False)
    sdf.to_csv(OUT/"sustained_motor_fits.csv",index=False)

    tmrm={c:base.long_summary(paths["tmrm"][c],"tmrm") for c in [0]+base.CONCS}
    area={c:base.long_summary(paths["area"][c],"area") for c in [0]+base.CONCS}

    A=med_by_cond(idf,"A_dec")
    td=med_by_cond(idf,"tau_dec")
    ti=med_by_cond(idf,"tau_inc")
    ta=med_by_cond(sdf,"tau_adapt")
    pl=med_by_cond(sdf,"plateau")
    trends={
      "A_dec":{"values":A,"rho":rho(A)},
      "plateau":{"values":pl,"rho":rho(pl)},
      "tau_dec":{"values":td,"rho":rho(td),"max_min_ratio":ratio(td)},
      "tau_inc":{"values":ti,"rho":rho(ti),"max_min_ratio":ratio(ti)},
      "tau_adapt":{"values":ta,"rho":rho(ta),"max_min_ratio":ratio(ta)}
    }
    rate_depth=(
      trends["A_dec"]["rho"]>=0.8 and trends["plateau"]["rho"]<=-0.8 and
      all(abs(trends[k]["rho"])<=0.4 and trends[k]["max_min_ratio"]<=1.5 for k in ["tau_dec","tau_inc","tau_adapt"])
    )

    rows=[]
    for c in base.CONCS:
        rows.append([A[c],td[c],ti[c],ta[c],pl[c],tmrm[c]["min"],tmrm[c]["post"],area[c]["min"],area[c]["post"]])
    X=np.asarray(rows,float)
    features=["A_dec","tau_dec","tau_inc","tau_adapt","adaptation_plateau","TMRM_min","TMRM_postrecovery","Area_min","Area_postrecovery"]
    if not np.all(np.isfinite(X)):
        raise RuntimeError("nonfinite condition summary in reconciliation matrix")
    sd=X.std(axis=0,ddof=1)
    if np.any(sd==0):
        raise RuntimeError("zero-variance coordinate in reconciliation matrix")
    Z=(X-X.mean(axis=0))/sd
    U,S,Vt=np.linalg.svd(Z,full_matrices=False)
    var=S*S
    pc1=float(var[0]/var.sum())
    recon=np.outer(U[:,0]*S[0],Vt[0,:])
    maxres=float(np.max(np.abs(Z-recon)))
    oned=bool(pc1>=0.95 and maxres<=0.10)

    result={
      "schema_version":"0.1",
      "experiment_id":"MENESES2026_SOURCE_METHOD_RECONCILIATION_V01",
      "status":"EXECUTED_POSTRESULT_SOURCE_METHOD_RECONCILIATION",
      "evidence_class":"POST_RESULT_SOURCE_METHOD_RECONCILIATION",
      "upstream_commit":base.COMMIT,
      "method":"manuscript-facing sucrose_shock_analysis lane",
      "fit_failures":{"immediate":int((~idf.fit_valid).sum()),"sustained":int((~sdf.fit_valid).sum())},
      "fit_diagnostics":{"immediate_nonpositive_tau_inc":int(((idf.fit_valid)&(~idf["tau_inc_positive"].fillna(False))).sum())},
      "condition_medians":trends,
      "rate_depth_dissociation":{"frozen_rule_pass":bool(rate_depth),
        "disposition":"RATE_STABLE_DEPTH_VARIABLE_SENSITIVITY_PASS_POSTRESULT" if rate_depth else "FROZEN_RATE_DEPTH_RULE_NOT_MET_POSTRESULT_RECONCILIATION"},
      "joint_representation":{"features":features,"matrix":X.tolist(),"singular_values":[float(x) for x in S],
        "pc1_variance_fraction":pc1,"max_abs_standardized_1d_reconstruction_residual":maxres,
        "one_dimensional_adequacy":oned,
        "Chi_bio_disposition":"ONE_DIMENSIONAL_CONDITION_COMPRESSION_ADEQUATE_POSTRESULT" if oned else "MULTICOORDINATE_RECOVERY_ARCHITECTURE_REQUIRED_POSTRESULT"},
      "chi_bio":{"disposition":"NOT_OPENED_NOT_LICENSED"},
      "claim_ceiling":"post-result source-method reconciliation; cannot promote the primary P0-Q evidence"
    }
    (OUT/"MENESES2026_SOURCE_METHOD_RECONCILIATION_V01_RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    try:
        main()
    except Exception as e:
        fail={"schema_version":"0.1","experiment_id":"MENESES2026_SOURCE_METHOD_RECONCILIATION_V01",
              "status":"EXECUTION_FAILURE_PRESERVED","error_type":type(e).__name__,"error":str(e)}
        (OUT/"MENESES2026_SOURCE_METHOD_RECONCILIATION_V01_FAILURE.json").write_text(json.dumps(fail,indent=2)+"\n")
        print(json.dumps(fail,indent=2),file=sys.stderr)
        raise
