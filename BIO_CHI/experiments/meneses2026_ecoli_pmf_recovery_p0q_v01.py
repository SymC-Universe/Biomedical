#!/usr/bin/env python3
# execution trigger after workflow registration
"""Frozen Meneses 2026 E. coli PMF recovery Bio Chi P0-Q analysis.

Implements MENESES2026_ECOLI_PMF_RECOVERY_P0Q_V01_FREEZE.json.
The publication outcome is literature-open. This script tests source reproduction,
rate-depth structure, joint representation adequacy, and scalar eligibility.
"""
from __future__ import annotations
import hashlib, json, math, sys
from pathlib import Path
import numpy as np
import pandas as pd
import requests
from scipy.ndimage import median_filter
from scipy.optimize import curve_fit
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "meneses2026_raw"
OUT = ROOT / "meneses2026_results"
RAW.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

UPSTREAM = "wadhwalab/2026-Meneses-Osmotic"
COMMIT = "d14d0caaa07299f13d1b1121d1e4630454fd724b"
CONCS = [200,300,400,500]

FILES = {
 "immediate": {
  200:("data/time-series/bead/sucrose_200mM.parquet","41c7e7837d7f6e0418180d85ded212a102af0621"),
  300:("data/time-series/bead/sucrose_300mM.parquet","78d915b2264dd6fa273ba061e605ee8597a28a06"),
  400:("data/time-series/bead/sucrose_400mM.parquet","36ebcaa9c817ba8c11527e69d6f8b49669b1f2d6"),
  500:("data/time-series/bead/sucrose_500mM.parquet","dd3b2ef0b1b77c43c02080c88080abb5b0cd3f61")},
 "sustained": {
  200:("data/time-series/bead/adaption_200mM.parquet","bad33e747b10472a3c38d95eaa50c4a215f9df31"),
  300:("data/time-series/bead/adaption_300mM.parquet","5c4837e9d3fe1226f873e987adfcdc64d35590d9"),
  400:("data/time-series/bead/adaption_400mM.parquet","cad15ff5fc8f353ddb8eadf7a6b98d9456ff776b"),
  500:("data/time-series/bead/adaption_500mM.parquet","f812fc92ad22be5847687d74f06c3ed1a178dd44")},
 "tmrm": {
  0:("data/time-series/tmrm/control.parquet","cb8db0e660690e14e6ab243e4565160f93af4801"),
  200:("data/time-series/tmrm/200mM.parquet","8ec6fafc765c8ebd28690a9ddaf604cf813ef868"),
  300:("data/time-series/tmrm/300mM.parquet","5a8b15c41f90dfec9abe4e8792c11729a5e93be5"),
  400:("data/time-series/tmrm/400mM.parquet","5a2bb35651ae54243f5a749de177553a8e94056b"),
  500:("data/time-series/tmrm/500mM.parquet","40df15665ca620ef1f6d55e9349b406c48d0cfbe")},
 "area": {
  0:("data/time-series/cell-area/control.parquet","315fb80c65b2ce5a17131affe91f6bf2ba065f7c"),
  200:("data/time-series/cell-area/200mM.parquet","bcd45ac8b271ba6122f5f6d06a588b66bc6ba424"),
  300:("data/time-series/cell-area/300mM.parquet","b009ffbf6f235c4ccca9e8bb5bd17784d6f25bce"),
  400:("data/time-series/cell-area/400mM.parquet","03b9c5d3d65b6c5efc0b1e94df3709dfb0be4554"),
  500:("data/time-series/cell-area/500mM.parquet","ae0949f3abe6d3ee712c2e7356059d5210efe8db")}
}
EXPECTED_COUNTS={"immediate":{200:8,300:10,400:8,500:12},"sustained":{200:8,300:8,400:8,500:4}}
EXPECTED_TMRM={
 0:{"min":-0.008366,"tmin":260.0,"shockmean":0.000587,"post":0.00506},
 200:{"min":-0.064102,"tmin":215.0,"shockmean":-0.052921,"post":0.001083},
 300:{"min":-0.102654,"tmin":215.0,"shockmean":-0.083792,"post":0.007433},
 400:{"min":-0.124333,"tmin":260.0,"shockmean":-0.090796,"post":-0.010395},
 500:{"min":-0.170652,"tmin":255.0,"shockmean":-0.141426,"post":-0.01689}}
EXPECTED_AREA={
 0:{"min":-0.005768,"tmin":260.0,"shockmean":0.000036,"post":0.000262},
 200:{"min":-0.119935,"tmin":220.0,"shockmean":-0.077107,"post":-0.020967},
 300:{"min":-0.120608,"tmin":255.0,"shockmean":-0.100716,"post":-0.009355},
 400:{"min":-0.149982,"tmin":250.0,"shockmean":-0.105433,"post":0.000736},
 500:{"min":-0.149904,"tmin":265.0,"shockmean":-0.111384,"post":-0.014936}}

def git_blob_sha1(data:bytes)->str:
    h=hashlib.sha1()
    h.update(f"blob {len(data)}\0".encode())
    h.update(data)
    return h.hexdigest()

def sha256(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()

def fetch(path:str, expected_blob:str)->Path:
    p=RAW/path.replace("/","__")
    if p.exists():
        data=p.read_bytes()
    else:
        url=f"https://raw.githubusercontent.com/{UPSTREAM}/{COMMIT}/{path}"
        r=requests.get(url,timeout=120,headers={"User-Agent":"BioChi-Repro/0.1"})
        r.raise_for_status()
        data=r.content
        p.write_bytes(data)
    got=git_blob_sha1(data)
    if got!=expected_blob:
        raise RuntimeError(f"blob mismatch for {path}: {got} != {expected_blob}")
    return p

def exp_decrease(t,A,tau,C,t0):
    z=np.clip((t-175.0-t0)/tau,-700,700)
    return A/(1+np.exp(z))+C

def exp_increase(t,B,tau,D):
    z=np.clip(-(t-270.0)/tau,-700,700)
    return B*(1-np.exp(z))+D

def exp_adapt(t,B,tau,D):
    z=np.clip(-(t-200.0)/tau,-700,700)
    return B*(1-np.exp(z))+D

def wide_traces(df):
    t=df["time_s"].to_numpy(float) if "time_s" in df.columns else df["frame"].to_numpy(float)/300.0
    cols=[c for c in df.columns if c not in ("time_s","frame")]
    return t,cols

def fit_immediate(path,conc):
    df=pd.read_parquet(path)
    t,cols=wide_traces(df)
    rows=[]
    for c in cols:
        y=pd.to_numeric(df[c],errors="coerce").to_numpy(float)
        valid=np.isfinite(t)&np.isfinite(y)
        tt=t[valid]; yy=y[valid]
        baseline=np.mean(yy[tt<=180])
        rec={"condition_mM":conc,"trace":c,"baseline":float(baseline),"fit_valid":False}
        if not np.isfinite(baseline) or baseline==0:
            rec["failure"]="invalid_baseline"; rows.append(rec); continue
        yn=yy/baseline
        md=(tt>=175)&(tt<=240)
        mi=(tt>270)&(tt<=360)
        try:
            yd=yn[md]; td=tt[md]
            pdec,_=curve_fit(exp_decrease,td,yd,p0=[1-np.min(yd),10,np.min(yd),10],maxfev=50000)
            A,tau_d,C,t0=pdec
            yinc=yn[mi]; tinc=tt[mi]
            pinc,_=curve_fit(exp_increase,tinc,yinc,p0=[1,50,0.5],maxfev=50000)
            B,tau_i,D=pinc
            if not all(np.isfinite([A,tau_d,C,t0,B,tau_i,D])) or tau_d<=0 or tau_i<=0:
                raise RuntimeError("nonfinite_or_nonpositive_tau")
            rec.update({"fit_valid":True,"A_dec":float(A),"tau_dec":float(tau_d),"C_dec":float(C),
                        "t0_dec":float(t0),"B_inc":float(B),"tau_inc":float(tau_i),"D_inc":float(D)})
        except Exception as e:
            rec["failure"]=f"{type(e).__name__}:{e}"
        rows.append(rec)
    return rows

def odd_kernel_for_1s(t):
    dt=float(np.nanmedian(np.diff(t)))
    k=max(1,int(round(1.0/dt)))
    if k%2==0:k+=1
    return k

def fit_sustained(path,conc):
    df=pd.read_parquet(path)
    t,cols=wide_traces(df)
    rows=[]
    k=odd_kernel_for_1s(t)
    for c in cols:
        y=pd.to_numeric(df[c],errors="coerce").to_numpy(float)
        valid=np.isfinite(t)&np.isfinite(y)
        tt=t[valid]; yy=y[valid]
        yy=median_filter(yy,size=k,mode="nearest")
        baseline=np.nanmean(yy[tt<180])
        rec={"condition_mM":conc,"trace":c,"baseline":float(baseline),"fit_valid":False,"median_kernel":k}
        if not np.isfinite(baseline) or baseline==0:
            rec["failure"]="invalid_baseline"; rows.append(rec); continue
        yn=yy/baseline
        m=(tt>=250)&(tt<=600)
        x=tt[m]; z=yn[m]
        ok=np.isfinite(z);x=x[ok];z=z[ok]
        try:
            bounds=([0,0.1,0],[2,500,1.5])
            p0=[np.clip(1-z[0],0,2),10,np.clip(z[0],0,1.5)]
            p,_=curve_fit(exp_adapt,x,z,p0=p0,bounds=bounds,maxfev=50000)
            B,tau,D=p
            rec.update({"fit_valid":True,"B":float(B),"tau_adapt":float(tau),"D":float(D),"plateau":float(B+D)})
        except Exception as e:
            rec["failure"]=f"{type(e).__name__}:{e}"
        rows.append(rec)
    return rows

def normalize_long(df,value_col,kind):
    df=df[df["track_id"]>=0].copy()
    df["dff"]=np.nan
    for tid,g in df.groupby("track_id"):
        g=g.sort_values("frame")
        base=g[(g["frame"]<35)&(g["frame"]>=25)]
        if len(base)<3: continue
        f0=float(base[value_col].mean())
        if kind=="tmrm":
            vals=(g[value_col]-f0)/(f0-1)
        else:
            vals=(g[value_col]-f0)/f0
        df.loc[g.index,"dff"]=vals
    df["time_s"]=df["frame"]*5.0
    return df

def long_summary(path,kind):
    df=pd.read_parquet(path)
    val="fluorescence" if kind=="tmrm" else "area"
    nd=normalize_long(df,val,kind)
    pop=nd.groupby("time_s")["dff"].mean().reset_index()
    lo,hi=(180,270) if kind=="tmrm" else (180,265)
    sw=pop[(pop.time_s>=lo)&(pop.time_s<=hi)]
    rw=pop[(pop.time_s>=300)&(pop.time_s<=380)]
    imin=sw["dff"].idxmin()
    return {
      "n_cells":int(nd.loc[np.isfinite(nd.dff),"track_id"].nunique()),
      "min":float(sw.loc[imin,"dff"]),
      "tmin":float(sw.loc[imin,"time_s"]),
      "shockmean":float(sw["dff"].mean()),
      "post":float(rw["dff"].mean())
    }

def check_summary(obs,exp):
    diffs={k:abs(obs[k]-exp[k]) for k in ("min","shockmean","post")}
    tdiff=abs(obs["tmin"]-exp["tmin"])
    return {"diffs":diffs,"tmin_diff_s":tdiff,"pass":max(diffs.values())<=0.005 and tdiff<=5.0}

def med_by_cond(df,col):
    out={}
    for c in CONCS:
        z=df[(df.condition_mM==c)&(df.fit_valid)][col].to_numpy(float)
        z=z[np.isfinite(z)]
        out[c]=float(np.median(z)) if len(z) else float("nan")
    return out

def rho(vals):
    arr=np.array([vals[c] for c in CONCS],float)
    if not np.all(np.isfinite(arr)): return float("nan")
    return float(spearmanr(CONCS,arr).statistic)

def ratio(vals):
    arr=np.array([vals[c] for c in CONCS],float)
    arr=arr[np.isfinite(arr)&(arr>0)]
    return float(np.max(arr)/np.min(arr)) if len(arr)==4 else float("nan")

def main():
    manifest=[]
    paths={}
    for family,items in FILES.items():
        paths[family]={}
        for c,(path,blob) in items.items():
            p=fetch(path,blob)
            data=p.read_bytes()
            manifest.append({"family":family,"condition_mM":c,"path":path,"blob_sha1":blob,"sha256":sha256(data),"bytes":len(data)})
            paths[family][c]=p

    immediate=[]
    sustained=[]
    for c in CONCS:
        immediate += fit_immediate(paths["immediate"][c],c)
        sustained += fit_sustained(paths["sustained"][c],c)
    idf=pd.DataFrame(immediate); sdf=pd.DataFrame(sustained)
    idf.to_csv(OUT/"immediate_motor_fits.csv",index=False)
    sdf.to_csv(OUT/"sustained_motor_fits.csv",index=False)

    counts={"immediate":{},"sustained":{}}
    count_pass=True
    for c in CONCS:
        counts["immediate"][c]={"observed":int((idf.condition_mM==c).sum()),"expected":EXPECTED_COUNTS["immediate"][c],
                                "valid_fits":int(((idf.condition_mM==c)&idf.fit_valid).sum())}
        counts["sustained"][c]={"observed":int((sdf.condition_mM==c).sum()),"expected":EXPECTED_COUNTS["sustained"][c],
                                "valid_fits":int(((sdf.condition_mM==c)&sdf.fit_valid).sum())}
        count_pass &= counts["immediate"][c]["observed"]==EXPECTED_COUNTS["immediate"][c]
        count_pass &= counts["sustained"][c]["observed"]==EXPECTED_COUNTS["sustained"][c]

    tmrm={}; area={}; repchecks={"tmrm":{},"area":{}}
    for c in [0]+CONCS:
        tmrm[c]=long_summary(paths["tmrm"][c],"tmrm")
        area[c]=long_summary(paths["area"][c],"area")
        repchecks["tmrm"][c]=check_summary(tmrm[c],EXPECTED_TMRM[c])
        repchecks["area"][c]=check_summary(area[c],EXPECTED_AREA[c])
    orth_pass=all(x["pass"] for fam in repchecks.values() for x in fam.values())
    cells_pass=all(tmrm[c]["n_cells"]==40 and area[c]["n_cells"]==40 for c in [0]+CONCS)

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
    for c in CONCS:
        rows.append([
          A[c],td[c],ti[c],ta[c],pl[c],
          tmrm[c]["min"],tmrm[c]["post"],area[c]["min"],area[c]["post"]
        ])
    X=np.asarray(rows,float)
    features=["A_dec","tau_dec","tau_inc","tau_adapt","adaptation_plateau","TMRM_min","TMRM_postrecovery","Area_min","Area_postrecovery"]
    if not np.all(np.isfinite(X)):
        raise RuntimeError("joint representation contains nonfinite condition summary")
    sd=X.std(axis=0,ddof=1)
    if np.any(sd==0): raise RuntimeError("joint representation contains zero-variance coordinate")
    Z=(X-X.mean(axis=0))/sd
    U,S,Vt=np.linalg.svd(Z,full_matrices=False)
    var=S*S
    pc1=float(var[0]/var.sum())
    recon=np.outer(U[:,0]*S[0],Vt[0,:])
    maxres=float(np.max(np.abs(Z-recon)))
    oned=bool(pc1>=0.95 and maxres<=0.10)

    result={
      "schema_version":"0.1",
      "experiment_id":"MENESES2026_ECOLI_PMF_RECOVERY_P0Q_V01",
      "status":"EXECUTED_VALID_P0Q" if count_pass and orth_pass and cells_pass else "SOURCE_REPRODUCTION_FAILURE_PRESERVED",
      "evidence_class":"P0-Q_LITERATURE_OPEN_DIRECT_EXPERIMENTAL_QUALIFICATION",
      "source":{"repository":UPSTREAM,"commit":COMMIT,"manifest":manifest},
      "source_reproduction":{"bead_trace_counts":counts,"trace_count_pass":bool(count_pass),
        "tmrm_cell_area_summary_checks":repchecks,"orthogonal_summary_pass":bool(orth_pass),"orthogonal_cell_count_pass":bool(cells_pass)},
      "fit_failures":{"immediate":int((~idf.fit_valid).sum()),"sustained":int((~sdf.fit_valid).sum())},
      "condition_medians":trends,
      "rate_depth_dissociation":{"frozen_rule_pass":bool(rate_depth),
        "disposition":"RATE_STABLE_DEPTH_VARIABLE_CANDIDATE_P0Q" if rate_depth else "FROZEN_RATE_DEPTH_RULE_NOT_MET_P0Q"},
      "joint_representation":{"features":features,"matrix":X.tolist(),"singular_values":[float(x) for x in S],
        "pc1_variance_fraction":pc1,"max_abs_standardized_1d_reconstruction_residual":maxres,
        "one_dimensional_adequacy":oned,
        "Chi_bio_disposition":"ONE_DIMENSIONAL_CONDITION_COMPRESSION_ADEQUATE_P0Q" if oned else "MULTICOORDINATE_RECOVERY_ARCHITECTURE_REQUIRED_P0Q"},
      "chi_bio":{"disposition":"NOT_OPENED_NOT_LICENSED","reason":"source fit taus are descriptive empirical summaries, not independently licensed mechanistic modal carriers"},
      "Bio_Chi":{"disposition":"DIRECT_EXPERIMENTAL_COLLAPSE_RECOVERY_RELATION_REPRODUCED_P0Q" if count_pass and orth_pass and cells_pass else "NOT_ADMITTED_SOURCE_REPRODUCTION_FAILED"},
      "claim_ceiling":"direct experimental P0-Q representation qualification in one E. coli osmotic-stress system; no universal biological chi value or boundary"
    }
    (OUT/"MENESES2026_ECOLI_PMF_RECOVERY_P0Q_V01_RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
    pd.DataFrame([{"condition_mM":c,**tmrm[c]} for c in [0]+CONCS]).to_csv(OUT/"tmrm_reproduction.csv",index=False)
    pd.DataFrame([{"condition_mM":c,**area[c]} for c in [0]+CONCS]).to_csv(OUT/"area_reproduction.csv",index=False)
    pd.DataFrame(manifest).to_csv(OUT/"source_manifest.csv",index=False)
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    try:
        main()
    except Exception as e:
        fail={"schema_version":"0.1","experiment_id":"MENESES2026_ECOLI_PMF_RECOVERY_P0Q_V01",
              "status":"EXECUTION_FAILURE_PRESERVED","error_type":type(e).__name__,"error":str(e)}
        (OUT/"MENESES2026_ECOLI_PMF_RECOVERY_P0Q_V01_FAILURE.json").write_text(json.dumps(fail,indent=2)+"\n")
        print(json.dumps(fail,indent=2),file=sys.stderr)
        raise
