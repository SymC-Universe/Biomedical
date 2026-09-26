#!/usr/bin/env python3
# workflow trigger after registration
from __future__ import annotations
import hashlib, json, math, traceback, urllib.request
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

COMMIT="d14d0caaa07299f13d1b1121d1e4630454fd724b"
BASE=f"https://raw.githubusercontent.com/wadhwalab/2026-Meneses-Osmotic/{COMMIT}"
SEED=20260925
RNG=np.random.default_rng(SEED)
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"meneses2026_path_transport_results"; OUT.mkdir(parents=True,exist_ok=True)
SRC=OUT/"source"; SRC.mkdir(parents=True,exist_ok=True)
CONCS=[200,300,400,500]
FILES={
 "sucrose":{
  200:("data/time-series/bead/sucrose_200mM.parquet","41c7e7837d7f6e0418180d85ded212a102af0621"),
  300:("data/time-series/bead/sucrose_300mM.parquet","78d915b2264dd6fa273ba061e605ee8597a28a06"),
  400:("data/time-series/bead/sucrose_400mM.parquet","36ebcaa9c817ba8c11527e69d6f8b49669b1f2d6"),
  500:("data/time-series/bead/sucrose_500mM.parquet","dd3b2ef0b1b77c43c02080c88080abb5b0cd3f61")},
 "sorbitol":{
  200:("data/time-series/bead/sorbitol_200mM.parquet","f105b4efa5815bff50bbe51ef493550b49c91d36"),
  300:("data/time-series/bead/sorbitol_300mM.parquet","cec88379c5da5a07dc444fd25c2f0be8937ec81e"),
  400:("data/time-series/bead/sorbitol_400mM.parquet","f3fd7373b2944f01b945b7259661f3fc6a75fc85"),
  500:("data/time-series/bead/sorbitol_500mM.parquet","1833accfa1e4405bebfd0e9430008854e3492567")},
 "sodium":{
  200:("data/time-series/bead/sodium_200mM.parquet","57ec489e1a19cc3a20ea6dea270152b86b359fa0"),
  300:("data/time-series/bead/sodium_300mM.parquet","5496ff4a54d4631fd0349d63966926d7ae065b7f"),
  400:("data/time-series/bead/sodium_400mM.parquet","fe51858b5cc7b6e6e7d1eb94a4bcb165ce1d312c"),
  500:("data/time-series/bead/sodium_500mM.parquet","52ab687a447fb5681492e4a25e7cf7814b2270c2")},
 "clockwise":{
  200:("data/time-series/bead/clockwise_200mM.parquet","c09ed5d53afd435097e26d5b10330dfd09e3538e"),
  300:("data/time-series/bead/clockwise_300mM.parquet","c38f3e0ccffd884aee46732917233a73cd573212"),
  400:("data/time-series/bead/clockwise_400mM.parquet","342d9c3c9164a20b3ec9d9ee7749989221854f41"),
  500:("data/time-series/bead/clockwise_500mM.parquet","7a42570406646d9f329f1c9a32c870ffaf6fc56a")}
}

def git_blob_sha(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def fetch(path,blob):
    p=SRC/path.replace("/","__")
    if not p.exists():
        req=urllib.request.Request(f"{BASE}/{path}",headers={"User-Agent":"SymC-BioChi-Transport/0.1"})
        with urllib.request.urlopen(req,timeout=120) as r:p.write_bytes(r.read())
    data=p.read_bytes()
    got=git_blob_sha(data)
    if got!=blob: raise RuntimeError(f"blob mismatch {path}: {got} != {blob}")
    return p,hashlib.sha256(data).hexdigest()

def dec_model(x,A,C,tau,t0):
    z=np.clip((x-175.0-t0)/tau,-700,700)
    return A/(1.0+np.exp(z))+C

def inc_model(x,ymin,ymax,tau,t0):
    z=np.clip(-(x-270.0-t0)/tau,-700,700)
    return ymin+(ymax-ymin)/(1.0+np.exp(z))

def fit_file(path,path_name,conc):
    df=pd.read_parquet(path)
    if "time_s" not in df.columns: raise RuntimeError(f"time_s missing {path_name} {conc}")
    t=pd.to_numeric(df["time_s"],errors="coerce").to_numpy(float)
    cols=[c for c in df.columns if c not in ("frame","time_s")]
    rows=[];fails=[]
    for c in cols:
        rec={"path":path_name,"condition_mM":conc,"cell":str(c),"fit_valid":False}
        try:
            y=pd.to_numeric(df[c],errors="coerce").to_numpy(float)
            v=np.isfinite(t)&np.isfinite(y); tt=t[v]; yy=y[v]
            base=yy[tt<=180]
            if len(base)<20: raise ValueError("insufficient_baseline")
            b=float(np.mean(base))
            if not np.isfinite(b) or b==0: raise ValueError("invalid_baseline")
            yn=yy/b
            msi=(tt>=155)&(tt<=175); msf=(tt>=215)&(tt<=235)
            mlo=(tt>=240)&(tt<=260); mhi=(tt>=330)&(tt<=350)
            md=(tt>=175)&(tt<=240); mi=(tt>250)&(tt<=360)
            if min(msi.sum(),msf.sum(),mlo.sum(),mhi.sum(),md.sum(),mi.sum())<20:
                raise ValueError("insufficient_frozen_window")
            speed_initial=float(np.mean(yn[msi])); speed_final=float(np.mean(yn[msf]))
            A=speed_initial-speed_final; C=speed_final
            def fdec(x,tau,t0): return dec_model(x,A,C,tau,t0)
            pdec,_=curve_fit(fdec,tt[md],yn[md],p0=[10,10],bounds=(0,np.inf),maxfev=50000)
            tau_dec,t0_dec=[float(x) for x in pdec]
            ymin=float(np.mean(yn[mlo])); ymax=float(np.mean(yn[mhi]))
            def finc(x,tau,t0): return inc_model(x,ymin,ymax,tau,t0)
            pinc,_=curve_fit(finc,tt[mi],yn[mi],p0=[3,-10],maxfev=50000)
            tau_inc,t0_inc=[float(x) for x in pinc]
            denom=1-ymin
            if not all(np.isfinite([A,tau_dec,tau_inc,ymin,ymax])): raise ValueError("nonfinite_fit")
            if tau_dec<=0: raise ValueError("nonpositive_tau_dec")
            if abs(tau_inc)<1e-12: raise ValueError("zero_tau_inc")
            if abs(denom)<1e-12: raise ValueError("undefined_recovery_fraction")
            rf=(ymax-ymin)/denom
            rec.update({"fit_valid":True,"A_dec":A,"tau_dec":tau_dec,"tau_inc":tau_inc,
                        "tau_inc_positive":bool(tau_inc>0),"t0_dec":t0_dec,"t0_inc":t0_inc,
                        "recovery_fraction":float(rf),"speed_low":ymin,"speed_high":ymax})
            rows.append(rec)
        except Exception as e:
            rec.update({"failure_type":type(e).__name__,"failure":str(e)})
            fails.append(rec)
    return rows,fails,len(cols)

def robust_scale(x):
    x=np.asarray(x,float)
    med=np.median(x); mad=np.median(np.abs(x-med))*1.4826
    if np.isfinite(mad) and mad>1e-12:return float(mad)
    sd=np.std(x,ddof=1)
    if np.isfinite(sd) and sd>1e-12:return float(sd)
    return float("nan")

FEATURES=["A_dec","log_tau_dec","log_abs_tau_inc","recovery_fraction"]

def matrix(df):
    return np.column_stack([
        df["A_dec"].to_numpy(float),
        np.log(df["tau_dec"].to_numpy(float)),
        np.log(np.abs(df["tau_inc"].to_numpy(float))),
        df["recovery_fraction"].to_numpy(float)
    ])

def path_stat(df,alt,permutations=10000):
    observed=[]; details=[]; pooled_by_c={}
    for c in CONCS:
        a=df[(df.path=="sucrose")&(df.condition_mM==c)].copy()
        b=df[(df.path==alt)&(df.condition_mM==c)].copy()
        if len(a)<3 or len(b)<3:return {"disposition":"TRANSPORT_UNRESOLVED_SOURCE_LIMITED_P0Q","reason":f"n<3 at {c}","alt":alt}
        Xa=matrix(a); Xb=matrix(b); X=np.vstack([Xa,Xb])
        scales=np.array([robust_scale(X[:,j]) for j in range(X.shape[1])])
        if not np.all(np.isfinite(scales)):return {"disposition":"TRANSPORT_UNRESOLVED_SOURCE_LIMITED_P0Q","reason":f"zero scale at {c}","alt":alt}
        center=np.median(X,axis=0)
        Za=(Xa-center)/scales; Zb=(Xb-center)/scales
        ma=np.median(Za,axis=0); mb=np.median(Zb,axis=0)
        delta=mb-ma
        dist=float(np.linalg.norm(delta))
        observed.append(dist)
        pooled_by_c[c]=(X,len(a),len(b),center,scales)
        for j,f in enumerate(FEATURES):
            details.append({"path":alt,"condition_mM":c,"feature":f,"standardized_median_difference":float(delta[j]),
                            "abs_exceeds_0_50":bool(abs(delta[j])>0.50)})
    D=float(np.mean(observed))
    null=np.empty(permutations,float)
    for r in range(permutations):
        ds=[]
        for c in CONCS:
            X,na,nb,center,scales=pooled_by_c[c]
            idx=RNG.permutation(len(X))
            za=(X[idx[:na]]-center)/scales; zb=(X[idx[na:]]-center)/scales
            ds.append(np.linalg.norm(np.median(zb,axis=0)-np.median(za,axis=0)))
        null[r]=np.mean(ds)
    p=float((1+np.sum(null>=D))/(permutations+1))
    maxdiff=max(abs(x["standardized_median_difference"]) for x in details)
    return {"alt":alt,"D_path":D,"raw_permutation_p":p,"permutations":permutations,
            "max_abs_standardized_median_difference":float(maxdiff),
            "coordinate_differences":details}

def holm(results):
    valid=[r for r in results if "raw_permutation_p" in r]
    m=len(valid)
    order=sorted(range(m),key=lambda i:valid[i]["raw_permutation_p"])
    running=0.0
    for rank,i in enumerate(order):
        adj=min(1.0,(m-rank)*valid[i]["raw_permutation_p"])
        running=max(running,adj)
        valid[i]["holm_p"]=running
    for r in results:
        if "holm_p" not in r: continue
        if r["holm_p"]>=0.05 and r["max_abs_standardized_median_difference"]<=0.50:
            r["disposition"]="TRANSPORT_COMPATIBLE_P0Q"
        else:
            r["disposition"]="PATH_DEPENDENT_REORGANIZATION_P0Q"
    return results

def main():
    rows=[];fails=[];manifest=[];inventory=[]
    for path_name,items in FILES.items():
        for c,(rel,blob) in items.items():
            p,sha=fetch(rel,blob)
            rr,ff,n=fit_file(p,path_name,c)
            rows+=rr;fails+=ff
            inventory.append({"path":path_name,"condition_mM":c,"source_trace_count":n,"valid_fit_count":len(rr),"failure_count":len(ff)})
            manifest.append({"path":rel,"git_blob_sha1":blob,"sha256":sha,"bytes":p.stat().st_size})
    df=pd.DataFrame(rows); fd=pd.DataFrame(fails); inv=pd.DataFrame(inventory)
    if df.empty: raise RuntimeError("no valid fits")
    df.to_csv(OUT/"path_transport_cell_features.csv",index=False)
    fd.to_csv(OUT/"path_transport_fit_failures.csv",index=False)
    inv.to_csv(OUT/"path_transport_inventory.csv",index=False)
    pd.DataFrame(manifest).to_csv(OUT/"source_manifest.csv",index=False)
    res=holm([path_stat(df,a,10000) for a in ["sorbitol","sodium","clockwise"]])
    all_disp=[r.get("disposition") for r in res]
    if any(x=="TRANSPORT_UNRESOLVED_SOURCE_LIMITED_P0Q" for x in all_disp):
        whole="PATH_TRANSPORT_PARTIALLY_SOURCE_LIMITED_P0Q"
    elif all(x=="TRANSPORT_COMPATIBLE_P0Q" for x in all_disp):
        whole="MULTICOORDINATE_MOTOR_ARCHITECTURE_TRANSPORT_COMPATIBLE_ACROSS_TESTED_PATHS_P0Q"
    elif any(x=="PATH_DEPENDENT_REORGANIZATION_P0Q" for x in all_disp):
        whole="MULTICOORDINATE_MOTOR_ARCHITECTURE_CONTEXT_DEPENDENT_ACROSS_TESTED_PATHS_P0Q"
    else:
        whole="PATH_TRANSPORT_UNRESOLVED_P0Q"
    summary=[]
    for path_name in FILES:
        for c in CONCS:
            z=df[(df.path==path_name)&(df.condition_mM==c)]
            if len(z):
                summary.append({"path":path_name,"condition_mM":c,"n":len(z),
                    "A_dec_median":float(np.median(z.A_dec)),
                    "tau_dec_median":float(np.median(z.tau_dec)),
                    "tau_inc_median":float(np.median(z.tau_inc)),
                    "recovery_fraction_median":float(np.median(z.recovery_fraction)),
                    "nonpositive_tau_inc":int(np.sum(z.tau_inc<=0))})
    result={
      "schema_version":"0.1","experiment_id":"MENESES2026_PATH_TRANSPORT_P0Q_V01",
      "status":"EXECUTED_VALID_P0Q",
      "evidence_class":"P0-Q_LITERATURE_OPEN_DIRECT_EXPERIMENTAL_TRANSPORT_QUALIFICATION",
      "upstream_commit":COMMIT,
      "inventory":inventory,
      "condition_medians":summary,
      "path_comparisons":res,
      "biological_chi":whole,
      "Chi_bio":"FOUR_COORDINATE_MOTOR_RESPONSE_ORGANIZATION",
      "chi_bio":"NOT_OPENED_NOT_LICENSED",
      "claim_ceiling":"one E. coli osmotic-stress system; direct experimental path-transport qualification; no universal invariance or scalar boundary"
    }
    (OUT/"MENESES2026_PATH_TRANSPORT_P0Q_V01_RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    try:main()
    except Exception as e:
        fail={"schema_version":"0.1","experiment_id":"MENESES2026_PATH_TRANSPORT_P0Q_V01",
              "status":"EXECUTION_FAILURE_PRESERVED","error_type":type(e).__name__,"error":str(e),
              "traceback":traceback.format_exc()}
        (OUT/"MENESES2026_PATH_TRANSPORT_P0Q_V01_FAILURE.json").write_text(json.dumps(fail,indent=2)+"\n")
        print(json.dumps(fail,indent=2))
        raise
