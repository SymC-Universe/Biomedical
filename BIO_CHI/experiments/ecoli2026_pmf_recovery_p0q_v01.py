#!/usr/bin/env python3
# execution trigger after workflow registration
from __future__ import annotations
import hashlib, json, math, traceback, urllib.request
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.ndimage import median_filter
from scipy.optimize import curve_fit
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

UPSTREAM="d14d0caaa07299f13d1b1121d1e4630454fd724b"
BASE=f"https://raw.githubusercontent.com/wadhwalab/2026-Meneses-Osmotic/{UPSTREAM}"
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"ecoli2026_pmf_results"; OUT.mkdir(parents=True,exist_ok=True)
DATA=OUT/"source"; DATA.mkdir(parents=True,exist_ok=True)
CONCS=[200,300,400,500]

def fetch(rel):
    p=DATA/rel.replace("/","__")
    if not p.exists():
        req=urllib.request.Request(f"{BASE}/{rel}",headers={"User-Agent":"SymC-BioChi-P0Q/0.1"})
        with urllib.request.urlopen(req,timeout=120) as r:
            p.write_bytes(r.read())
    if p.stat().st_size<100:
        raise RuntimeError(f"source too small: {rel} {p.stat().st_size}")
    return p

def sha256(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for c in iter(lambda:f.read(1<<20),b""): h.update(c)
    return h.hexdigest()

def exp_decrease(t,A,tau,C,t0):
    return A/(1.0+np.exp((t-175.0-t0)/tau))+C

def exp_increase(t,B,tau,D):
    return B*(1.0-np.exp(-(t-270.0)/tau))+D

def exp_adapt(t,B,tau,D):
    return B*(1.0-np.exp(-(t-200.0)/tau))+D

def bead_features():
    rows=[]; fails=[]; manifest=[]
    for conc in CONCS:
        rel=f"data/time-series/bead/sucrose_{conc}mM.parquet"
        p=fetch(rel); manifest.append((rel,p.stat().st_size,sha256(p)))
        df=pd.read_parquet(p)
        if "time_s" not in df: raise RuntimeError(f"time_s missing {rel}")
        t=pd.to_numeric(df["time_s"],errors="coerce").to_numpy(float)
        cellcols=[c for c in df.columns if c not in ("frame","time_s")]
        for cell in cellcols:
            try:
                y=pd.to_numeric(df[cell],errors="coerce").to_numpy(float)
                good=np.isfinite(t)&np.isfinite(y)
                tt=t[good]; yy=y[good]
                base=yy[tt<=175]
                if len(base)<20 or not np.isfinite(base.mean()) or base.mean()==0:
                    raise ValueError("invalid_baseline")
                yn=yy/base.mean()
                md=(tt>=175)&(tt<=240)
                mi=(tt>270)&(tt<=360)
                if md.sum()<20: raise ValueError("insufficient_decrease_window")
                if mi.sum()<20: raise ValueError("insufficient_increase_window")
                yd=yn[md]; td=tt[md]
                yi=yn[mi]; ti=tt[mi]
                p0d=[1-np.nanmin(yd),10,np.nanmin(yd),10]
                pd_,_=curve_fit(exp_decrease,td,yd,p0=p0d,maxfev=30000)
                A,tau_dec,C,t0=pd_
                p0i=[1,50,0.5]
                pi_,_=curve_fit(exp_increase,ti,yi,p0=p0i,maxfev=30000)
                B,tau_inc,D=pi_
                if not np.isfinite(tau_dec) or tau_dec<=0: raise ValueError(f"invalid_tau_dec:{tau_dec}")
                if not np.isfinite(tau_inc) or tau_inc<=0: raise ValueError(f"invalid_tau_inc:{tau_inc}")
                shock=(tt>=180)&(tt<=270)
                rec=(tt>=330)&(tt<=350)
                if shock.sum()<20 or rec.sum()<20: raise ValueError("insufficient_nonparametric_window")
                minv=float(np.nanmin(yn[shock]))
                amp=float(1-minv)
                recv=float(np.nanmean(yn[rec]))
                rfrac=float((recv-minv)/(1-minv)) if abs(1-minv)>1e-12 else np.nan
                if not np.isfinite(rfrac): raise ValueError("undefined_recovery_fraction")
                rows.append(dict(condition_mM=conc,cell=cell,n_samples=len(tt),
                                 tau_dec=float(tau_dec),tau_inc=float(tau_inc),
                                 collapse_amplitude=amp,recovery_fraction=rfrac,
                                 minimum_norm_speed=minv,recovery_330_350=recv,
                                 fit_A=float(A),fit_C=float(C),fit_t0=float(t0),
                                 fit_B=float(B),fit_D=float(D)))
            except Exception as e:
                fails.append(dict(lineage="reversible",condition_mM=conc,cell=cell,
                                  failure_type=type(e).__name__,failure=str(e)))
    return pd.DataFrame(rows),pd.DataFrame(fails),manifest

def adaptation_features(manifest):
    rows=[]; fails=[]
    for conc in CONCS:
        rel=f"data/time-series/bead/adaption_{conc}mM.parquet"
        p=fetch(rel); manifest.append((rel,p.stat().st_size,sha256(p)))
        df=pd.read_parquet(p)
        t=pd.to_numeric(df["time_s"],errors="coerce").to_numpy(float)
        cellcols=[c for c in df.columns if c not in ("frame","time_s")]
        finite_t=t[np.isfinite(t)]
        dt=float(np.median(np.diff(finite_t))) if len(finite_t)>2 else .1
        k=max(1,int(round(1.0/dt)))
        if k%2==0:k+=1
        for cell in cellcols:
            try:
                y=pd.to_numeric(df[cell],errors="coerce").to_numpy(float)
                good=np.isfinite(t)&np.isfinite(y)
                tt=t[good]; yy=y[good]
                if len(yy)<20: raise ValueError("insufficient_trace")
                yf=median_filter(yy,size=k,mode="nearest")
                base=yf[tt<180]
                if len(base)<20 or not np.isfinite(base.mean()) or base.mean()==0:
                    raise ValueError("invalid_baseline")
                yn=yf/base.mean()
                m=(tt>=250)&(tt<=600)
                if m.sum()<20: raise ValueError("insufficient_adaptation_window")
                x=tt[m]; z=yn[m]
                bounds=([0,0.1,0],[2,500,1.5])
                B0=float(np.clip(1-z[0],0,2)); p0=[B0,10,float(np.clip(z[0],0,1.5))]
                popt,_=curve_fit(exp_adapt,x,z,p0=p0,bounds=bounds,maxfev=30000)
                B,tau,D=[float(v) for v in popt]
                if not np.isfinite(tau) or tau<=0: raise ValueError(f"invalid_tau_adapt:{tau}")
                rows.append(dict(condition_mM=conc,cell=cell,tau_adapt=tau,
                                 fit_B=B,fit_D=D,plateau=B+D,kernel_samples=k))
            except Exception as e:
                fails.append(dict(lineage="adaptation",condition_mM=conc,cell=cell,
                                  failure_type=type(e).__name__,failure=str(e)))
    return pd.DataFrame(rows),pd.DataFrame(fails)

def rep_test(df):
    feats=["collapse_amplitude","tau_dec","tau_inc","recovery_fraction"]
    X=df[feats].copy()
    X["tau_dec"]=np.log(X["tau_dec"])
    X["tau_inc"]=np.log(X["tau_inc"])
    X=X.to_numpy(float)
    groups=df["condition_mM"].to_numpy(int)
    preds={1:np.empty_like(X),2:np.empty_like(X)}
    fold=[]
    for hold in CONCS:
        tr=groups!=hold; te=groups==hold
        if tr.sum()<3 or te.sum()<1: raise RuntimeError(f"LOCO fold unavailable {hold}")
        sc=StandardScaler().fit(X[tr])
        ztr=sc.transform(X[tr]); zte=sc.transform(X[te])
        for rank in (1,2):
            p=PCA(n_components=rank,svd_solver="full").fit(ztr)
            zhat=p.inverse_transform(p.transform(zte))
            preds[rank][te]=zhat
            mse=float(np.mean((zte-zhat)**2))
            fold.append(dict(holdout_mM=hold,rank=rank,n_train=int(tr.sum()),n_test=int(te.sum()),mse=mse))
    metrics={}
    for rank in (1,2):
        # convert each fold's held-out target to its fold standardization again for exact aggregate residual.
        residuals=[]; bycoord=[[] for _ in feats]
        for hold in CONCS:
            tr=groups!=hold; te=groups==hold
            sc=StandardScaler().fit(X[tr])
            zte=sc.transform(X[te])
            rr=zte-preds[rank][te]
            residuals.append(rr)
            for j in range(len(feats)): bycoord[j].append(rr[:,j])
        rr=np.vstack(residuals)
        rmse={f:float(np.sqrt(np.mean(np.concatenate(bycoord[j])**2))) for j,f in enumerate(feats)}
        metrics[str(rank)]={"mse":float(np.mean(rr**2)),"coordinate_rmse":rmse,"max_coordinate_rmse":max(rmse.values())}
    r1=metrics["1"]; r2=metrics["2"]
    adequate1=(r1["mse"]<=0.25 and r1["max_coordinate_rmse"]<=0.75)
    improve=(r1["mse"]-r2["mse"])/r1["mse"] if r1["mse"]>0 else 0
    adequate2=(r2["mse"]<=0.25 and r2["max_coordinate_rmse"]<=0.75)
    if adequate1:
        disp="ONE_COORDINATE_COMPRESSION_ADEQUATE_BUT_NOT_CHI_BIO"
    elif adequate2 and improve>=0.25:
        disp="TWO_COORDINATE_CHI_BIO_REQUIRED_P0Q"
    else:
        disp="MULTICOORDINATE_UNRESOLVED_P0Q"
    return {"features":["collapse_amplitude","log_tau_dec","log_tau_inc","recovery_fraction"],
            "folds":fold,"rank_metrics":metrics,"r2_fractional_mse_improvement_over_r1":float(improve),
            "disposition":disp}

def recompute_track_assay(kind,value_col,shock_end,manifest):
    rows=[]; detail=[]
    for label in ["control",200,300,400,500]:
        fn="control.parquet" if label=="control" else f"{label}mM.parquet"
        rel=f"data/time-series/{kind}/{fn}"
        p=fetch(rel); manifest.append((rel,p.stat().st_size,sha256(p)))
        df=pd.read_parquet(p)
        vals=[]
        for tid,g in df.groupby("track_id"):
            g=g.sort_values("frame")
            frame=pd.to_numeric(g["frame"],errors="coerce").to_numpy(float)
            y=pd.to_numeric(g[value_col],errors="coerce").to_numpy(float)
            good=np.isfinite(frame)&np.isfinite(y);frame=frame[good];y=y[good]
            pre=(frame>=25)&(frame<=34)
            if pre.sum()<5: continue
            b=float(np.mean(y[pre]))
            if not np.isfinite(b) or b==0: continue
            d=(y-b)/b
            time=frame*5.0
            for tt,v in zip(time,d):
                vals.append((tid,tt,float(v)))
        if not vals: raise RuntimeError(f"no normalized tracks {kind} {label}")
        z=pd.DataFrame(vals,columns=["track_id","time_s","dff"])
        pop=z.groupby("time_s",as_index=False)["dff"].mean()
        shock=pop[(pop.time_s>=180)&(pop.time_s<=shock_end)]
        rec=pop[(pop.time_s>=300)&(pop.time_s<=380)]
        row=dict(condition=str(label),n_cells=int(z.track_id.nunique()),
                 minimum_mean_change_during_shock=float(shock.dff.min()),
                 time_of_minimum_s=float(shock.loc[shock.dff.idxmin(),"time_s"]),
                 mean_change_during_shock=float(shock.dff.mean()),
                 mean_change_after_recovery_300_380_s=float(rec.dff.mean()))
        rows.append(row)
        detail.append(z.assign(condition=str(label)))
    return pd.DataFrame(rows),pd.concat(detail,ignore_index=True)

def main():
    motor,fail1,manifest=bead_features()
    adapt,fail2=adaptation_features(manifest)
    if motor.empty: raise RuntimeError("no valid reversible motor fits")
    if adapt.empty: raise RuntimeError("no valid adaptation fits")
    rep=rep_test(motor)
    tmrm,tmrm_detail=recompute_track_assay("tmrm","fluorescence",270,manifest)
    area,area_detail=recompute_track_assay("cell-area","area",265,manifest)
    mf=pd.DataFrame(manifest,columns=["source_path","bytes","sha256"]).drop_duplicates()
    mf.to_csv(OUT/"source_manifest.csv",index=False)
    motor.to_csv(OUT/"motor_reversible_cell_features.csv",index=False)
    fail1.to_csv(OUT/"motor_reversible_fit_failures.csv",index=False)
    adapt.to_csv(OUT/"motor_adaptation_cell_features.csv",index=False)
    fail2.to_csv(OUT/"motor_adaptation_fit_failures.csv",index=False)
    tmrm.to_csv(OUT/"tmrm_recomputed_summary.csv",index=False)
    area.to_csv(OUT/"cell_area_recomputed_summary.csv",index=False)
    (OUT/"representation_cv.json").write_text(json.dumps(rep,indent=2)+"\n")

    med_motor=motor.groupby("condition_mM").agg(
        collapse_amplitude_median=("collapse_amplitude","median"),
        tau_dec_median=("tau_dec","median"),
        tau_inc_median=("tau_inc","median"),
        recovery_fraction_median=("recovery_fraction","median"),
        n=("cell","count")).reset_index()
    med_adapt=adapt.groupby("condition_mM").agg(
        tau_adapt_median=("tau_adapt","median"),
        plateau_median=("plateau","median"),n=("cell","count")).reset_index()

    t_non=tmrm[tmrm.condition!="control"].copy()
    a_non=area[area.condition!="control"].copy()
    independent_perturbation=bool((t_non.minimum_mean_change_during_shock < -0.02).all() and
                                  (a_non.minimum_mean_change_during_shock < -0.02).all())
    recovery_vectors_identical=bool(np.allclose(
        t_non.mean_change_after_recovery_300_380_s.to_numpy(float),
        a_non.mean_change_after_recovery_300_380_s.to_numpy(float),
        rtol=1e-6,atol=1e-8))
    motor_recovery=bool((med_motor.recovery_fraction_median>0).all())
    biochi="DIRECT_PERTURBATION_RECOVERY_RELATION_SUPPORTED_P0Q" if independent_perturbation and motor_recovery else "DIRECT_WHOLE_EVENT_QUALIFICATION_INCOMPLETE_P0Q"

    result={
      "schema_version":"0.1","experiment_id":"ECOLI2026_PMF_RECOVERY_P0Q_V01",
      "status":"EXECUTED_VALID_DIRECT_MEASUREMENT_P0Q",
      "evidence_class":"P0-Q_LITERATURE_OPEN_DIRECT_MEASUREMENT_REPRESENTATION_QUALIFICATION",
      "upstream_commit":UPSTREAM,
      "motor_reversible":{"n_valid":int(len(motor)),"n_failures":int(len(fail1)),
                          "by_condition":med_motor.to_dict(orient="records")},
      "motor_adaptation":{"n_valid":int(len(adapt)),"n_failures":int(len(fail2)),
                          "by_condition":med_adapt.to_dict(orient="records")},
      "representation":rep,
      "independent_observables":{"tmrm":tmrm.to_dict(orient="records"),
                                 "cell_area":area.to_dict(orient="records"),
                                 "noncontrol_perturbation_threshold_pass":independent_perturbation,
                                 "recovery_vectors_numerically_identical":recovery_vectors_identical},
      "chi_bio":"NOT_LICENSED_SOURCE_MODEL_NONOSCILLATORY",
      "Chi_bio":rep["disposition"],
      "biological_chi":biochi,
      "claim_ceiling":"P0-Q direct-measurement representation qualification in released curated data; not universal law or mechanistic identification"
    }
    (OUT/"ECOLI2026_PMF_RECOVERY_P0Q_V01_RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    try:
        main()
    except Exception as e:
        fail={"schema_version":"0.1","experiment_id":"ECOLI2026_PMF_RECOVERY_P0Q_V01",
              "status":"EXECUTION_FAILURE_PRESERVED","error_type":type(e).__name__,
              "error":str(e),"traceback":traceback.format_exc()}
        (OUT/"ECOLI2026_PMF_RECOVERY_P0Q_V01_FAILURE.json").write_text(json.dumps(fail,indent=2)+"\n")
        print(json.dumps(fail,indent=2))
        raise
