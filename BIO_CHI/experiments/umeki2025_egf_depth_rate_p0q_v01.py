#!/usr/bin/env python3
# workflow trigger after registration
from __future__ import annotations
import hashlib, json, math, traceback, urllib.request, urllib.parse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

UPSTREAM="3467850de2e45dfc2b7766ba4dce0d7af8839a00"
BASE=f"https://raw.githubusercontent.com/YasushiSako/transfer_entropy_2/{UPSTREAM}"
SEED=20260925
RNG=np.random.default_rng(SEED)
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"umeki2025_egf_depth_rate_results"
SRC=OUT/"source"
OUT.mkdir(parents=True,exist_ok=True); SRC.mkdir(parents=True,exist_ok=True)

DOSES=[0.1,1.0,10.0,100.0]
FILES={
  0.1:{
    "SOS":("EGF dose dynamics data/SOS_wt_EGF01ng.csv","157404e86adf690e67fa0d52fcaed553023a2ed6"),
    "RAF":("EGF dose dynamics data/RAF_wt_EGF01ng.csv","1994dd3dd45f59110bb37257e7411e9fa5232c71")},
  1.0:{
    "SOS":("EGF dose dynamics data/SOS_wt_EGF1ng.csv","69e15154cd06db9489872811a05f889ecf669665"),
    "RAF":("EGF dose dynamics data/RAF_wt_EGF1ng.csv","17e81faafa8b6a32c8f8ad77c2e9fa4d35b16e2a")},
  10.0:{
    "SOS":("EGF dose dynamics data/SOS_wt_EGF10ng.csv","5b1eda54b292fb60b2d66058cef08f40cb988d77"),
    "RAF":("EGF dose dynamics data/RAF_wt_EGF10ng.csv","61b5f598347b29a1d084c9e8c1239b05070fb375")},
  100.0:{
    "SOS":("EGF dose dynamics data/SOS_wt_EGF100ng.csv","b21c017747e6856e30391d45e71f3f36da06a1a9"),
    "RAF":("EGF dose dynamics data/RAF_wt_EGF100ng.csv","a866a47924026b06c89a834359a236126abb9dcc")}
}
PUBLISHED_COUNTS={0.1:300,1.0:310,10.0:370,100.0:337}

def git_blob_sha(data:bytes)->str:
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def sha256(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()

def fetch(path,blob):
    local=SRC/path.replace("/","__")
    if not local.exists():
        url=f"{BASE}/{urllib.parse.quote(path)}"\n        req=urllib.request.Request(url,headers={"User-Agent":"SymC-BioChi-Umeki/0.1"})
        with urllib.request.urlopen(req,timeout=120) as r:
            local.write_bytes(r.read())
    data=local.read_bytes()
    got=git_blob_sha(data)
    if got!=blob:
        raise RuntimeError(f"git blob mismatch {path}: {got} != {blob}")
    return local,sha256(data)

def load_csv(path):
    df=pd.read_csv(path)
    if df.shape[1]<2:
        raise RuntimeError(f"not enough columns in {path}")
    t=pd.to_numeric(df.iloc[:,0],errors="coerce")
    keep=t.notna()
    if keep.sum()<20:
        raise RuntimeError(f"time column has too few numeric rows in {path}")
    out=df.loc[keep].copy()
    out.iloc[:,0]=t.loc[keep].astype(float)
    out=out.sort_values(out.columns[0])
    return out

def positive_auc(t,y,lo,hi):
    m=(t>=lo)&(t<=hi)&np.isfinite(y)
    if m.sum()<2:return np.nan
    return float(np.trapezoid(np.maximum(y[m],0.0),t[m]))

def feature_row(dose,cell,t,sos,raf):
    paired=np.isfinite(t)&np.isfinite(sos)&np.isfinite(raf)&(t>=0)&(t<=60)
    total=((t>=0)&(t<=60)&np.isfinite(t)).sum()
    if total<20 or paired.sum()/total<0.90:
        raise ValueError(f"paired_finite_fraction={paired.sum()/max(total,1):.4f}")
    tt=t[paired]; ss=sos[paired]; rr=raf[paired]
    early=(tt>=0)&(tt<=15)
    if early.sum()<5:raise ValueError("insufficient_early_window")
    sos_peak=float(np.max(ss[early])); raf_peak=float(np.max(rr[early]))
    sos_den=positive_auc(tt,ss,0,60); raf_den=positive_auc(tt,rr,0,60)
    sos_late=positive_auc(tt,ss,30,60); raf_late=positive_auc(tt,rr,30,60)
    if not all(np.isfinite([sos_den,raf_den,sos_late,raf_late])) or sos_den<=0 or raf_den<=0:
        raise ValueError("zero_or_nonfinite_total_positive_auc")
    sos_p=float(sos_late/sos_den); raf_p=float(raf_late/raf_den)
    def centroid(y):
        m=(tt>=15)&(tt<=60)&np.isfinite(y)
        if m.sum()<2:return np.nan
        yy=np.maximum(y[m],0.0); den=float(np.trapezoid(yy,tt[m]))
        if den<=0:return np.nan
        return float(np.trapezoid(tt[m]*yy,tt[m])/den)
    sos_c=centroid(ss); raf_c=centroid(rr)
    if not np.isfinite(sos_c) or not np.isfinite(raf_c):
        raise ValueError("undefined_late_centroid")
    return {
      "dose_ng_ml":dose,"cell":str(cell),
      "SOS_peak_early":sos_peak,"RAF_peak_early":raf_peak,
      "SOS_centroid_15_60":sos_c,"SOS_persistence_30_60":sos_p,
      "RAF_centroid_15_60":raf_c,"RAF_persistence_30_60":raf_p
    }

def source_and_features():
    manifest=[]; inventory=[]; rows=[]; failures=[]
    for dose in DOSES:
        loaded={}
        for ch in ("SOS","RAF"):
            rel,blob=FILES[dose][ch]
            p,h=fetch(rel,blob)
            df=load_csv(p); loaded[ch]=df
            manifest.append({"dose_ng_ml":dose,"channel":ch,"source_path":rel,
                             "git_blob_sha1":blob,"sha256":h,"bytes":p.stat().st_size,
                             "n_time_rows":len(df),"n_signal_columns":df.shape[1]-1})
        s=loaded["SOS"]; r=loaded["RAF"]
        st=pd.to_numeric(s.iloc[:,0],errors="coerce").to_numpy(float)
        rt=pd.to_numeric(r.iloc[:,0],errors="coerce").to_numpy(float)
        if len(st)!=len(rt) or not np.allclose(st,rt,rtol=0,atol=1e-12,equal_nan=True):
            raise RuntimeError(f"SOS/RAF time-axis mismatch at dose {dose}")
        scol={str(c):c for c in s.columns[1:]}; rcol={str(c):c for c in r.columns[1:]}
        pairs=sorted(set(scol)&set(rcol))
        if not pairs:raise RuntimeError(f"no paired cells at dose {dose}")
        inventory.append({"dose_ng_ml":dose,"published_cell_count":PUBLISHED_COUNTS[dose],
                          "SOS_columns":len(scol),"RAF_columns":len(rcol),"paired_columns":len(pairs),
                          "paired_minus_published":len(pairs)-PUBLISHED_COUNTS[dose]})
        for cell in pairs:
            try:
                sos=pd.to_numeric(s[scol[cell]],errors="coerce").to_numpy(float)
                raf=pd.to_numeric(r[rcol[cell]],errors="coerce").to_numpy(float)
                rows.append(feature_row(dose,cell,st,sos,raf))
            except Exception as e:
                failures.append({"dose_ng_ml":dose,"cell":cell,
                                 "failure_type":type(e).__name__,"failure":str(e)})
    return pd.DataFrame(rows),pd.DataFrame(failures),pd.DataFrame(manifest),pd.DataFrame(inventory)

TEMP=["SOS_centroid_15_60","SOS_persistence_30_60","RAF_centroid_15_60","RAF_persistence_30_60"]
DEPTH=["SOS_peak_early","RAF_peak_early"]
REP=DEPTH+TEMP

def design_m0(ds):
    a=ds[:,0];b=ds[:,1]
    return np.column_stack([np.ones(len(ds)),a,b,a*a,b*b,a*b])

def design_m1(ds,zd):
    a=ds[:,0];b=ds[:,1];q=np.asarray(zd,float)
    return np.column_stack([np.ones(len(ds)),a,b,a*a,b*b,a*b,q,q*a,q*b])

def depth_vs_input_cv(df):
    residual0=[];residual1=[]; folds=[]
    doses=df.dose_ng_ml.to_numpy(float)
    D=df[DEPTH].to_numpy(float)
    T=df[TEMP].to_numpy(float)
    L=np.log10(doses)
    for hold in DOSES:
        tr=doses!=hold;te=~tr
        if tr.sum()<20 or te.sum()<10:raise RuntimeError(f"insufficient LOCO fold {hold}")
        sd=StandardScaler().fit(D[tr]); st=StandardScaler().fit(T[tr])
        zdtr=sd.transform(D[tr]); zdte=sd.transform(D[te])
        zttr=st.transform(T[tr]); ztte=st.transform(T[te])
        lm=float(L[tr].mean()); ls=float(L[tr].std(ddof=1))
        if ls<=0:raise RuntimeError("zero log-dose scale")
        zltr=(L[tr]-lm)/ls; zlte=(L[te]-lm)/ls
        X0tr=design_m0(zdtr); X0te=design_m0(zdte)
        X1tr=design_m1(zdtr,zltr); X1te=design_m1(zdte,zlte)
        R0=np.empty_like(ztte);R1=np.empty_like(ztte)
        for j in range(len(TEMP)):
            b0=np.linalg.lstsq(X0tr,zttr[:,j],rcond=None)[0]
            b1=np.linalg.lstsq(X1tr,zttr[:,j],rcond=None)[0]
            R0[:,j]=ztte[:,j]-X0te@b0
            R1[:,j]=ztte[:,j]-X1te@b1
        residual0.append(R0);residual1.append(R1)
        folds.append({"holdout_dose_ng_ml":hold,"n_train":int(tr.sum()),"n_test":int(te.sum()),
                      "m0_mse":float(np.mean(R0**2)),"m1_mse":float(np.mean(R1**2))})
    R0=np.vstack(residual0);R1=np.vstack(residual1)
    m0=float(np.mean(R0**2));m1=float(np.mean(R1**2));imp=float((m0-m1)/m0) if m0>0 else np.nan
    per={}
    for j,n in enumerate(TEMP):
        a=float(np.mean(R0[:,j]**2));b=float(np.mean(R1[:,j]**2))
        per[n]={"m0_mse":a,"m1_mse":b,"fractional_improvement":float((a-b)/a) if a>0 else np.nan}
    return {"m0_mse":m0,"m1_mse":m1,"fractional_improvement":imp,"per_coordinate":per,"folds":folds}

def bootstrap_depth(df,n=2000):
    groups={d:df[df.dose_ng_ml==d].copy() for d in DOSES}
    vals=[]
    for _ in range(n):
        parts=[]
        for d,g in groups.items():
            idx=RNG.integers(0,len(g),size=len(g))
            parts.append(g.iloc[idx].copy())
        bdf=pd.concat(parts,ignore_index=True)
        try: vals.append(depth_vs_input_cv(bdf)["fractional_improvement"])
        except Exception: pass
    if len(vals)<int(.9*n):raise RuntimeError(f"bootstrap success too low {len(vals)}/{n}")
    x=np.asarray(vals,float)
    return {"requested":n,"successful":len(vals),"seed":SEED,
            "median":float(np.median(x)),
            "ci95":[float(np.quantile(x,.025)),float(np.quantile(x,.975))]}

def rank1_cv(df):
    X=df[REP].to_numpy(float); doses=df.dose_ng_ml.to_numpy(float)
    res=[];folds=[]
    for hold in DOSES:
        tr=doses!=hold;te=~tr
        sc=StandardScaler().fit(X[tr]);ztr=sc.transform(X[tr]);zte=sc.transform(X[te])
        p=PCA(n_components=1,svd_solver="full").fit(ztr)
        zh=p.inverse_transform(p.transform(zte));r=zte-zh
        res.append(r)
        folds.append({"holdout_dose_ng_ml":hold,"n_train":int(tr.sum()),"n_test":int(te.sum()),
                      "mse":float(np.mean(r**2)),
                      "training_pc1_variance_fraction":float(p.explained_variance_ratio_[0])})
    R=np.vstack(res)
    mse=float(np.mean(R**2))
    rmse={n:float(np.sqrt(np.mean(R[:,j]**2))) for j,n in enumerate(REP)}
    maxrm=max(rmse.values())
    adequate=bool(mse<=0.25 and maxrm<=0.75)
    return {"features":REP,"mse":mse,"coordinate_rmse":rmse,"max_coordinate_rmse":maxrm,
            "one_coordinate_adequacy":adequate,
            "disposition":"ONE_COORDINATE_COMPRESSION_ADEQUATE_P0Q" if adequate else "MULTICOORDINATE_SIGNALING_ORGANIZATION_REQUIRED_P0Q",
            "folds":folds}

def main():
    df,fail,manifest,inventory=source_and_features()
    if len(df)<100:raise RuntimeError(f"too few valid paired cells: {len(df)}")
    if set(np.round(df.dose_ng_ml,10))!=set(DOSES):raise RuntimeError("not all doses represented")
    df.to_csv(OUT/"cell_features.csv",index=False)
    fail.to_csv(OUT/"representation_failures.csv",index=False)
    manifest.to_csv(OUT/"source_manifest.csv",index=False)
    inventory.to_csv(OUT/"pair_inventory.csv",index=False)
    primary=depth_vs_input_cv(df)
    boot=bootstrap_depth(df,2000)
    I=primary["fractional_improvement"];lo,hi=boot["ci95"]
    if I>=0.25 and lo>0:
        pdisp="INPUT_MAGNITUDE_ADDS_TEMPORAL_INFORMATION_P0Q"
    elif I<=0.10 and hi<=0.10:
        pdisp="EARLY_DEPTH_SUFFICIENT_FOR_TEMPORAL_ORGANIZATION_P0Q"
    else:
        pdisp="DEPTH_VS_INPUT_TEMPORAL_ORGANIZATION_UNRESOLVED_P0Q"
    rep=rank1_cv(df)
    (OUT/"depth_vs_input_cv.json").write_text(json.dumps({"primary":primary,"bootstrap":boot,"disposition":pdisp},indent=2)+"\n")
    (OUT/"rank1_representation_cv.json").write_text(json.dumps(rep,indent=2)+"\n")
    by=df.groupby("dose_ng_ml").agg(
      n=("cell","count"),
      SOS_peak_median=("SOS_peak_early","median"),RAF_peak_median=("RAF_peak_early","median"),
      SOS_centroid_median=("SOS_centroid_15_60","median"),RAF_centroid_median=("RAF_centroid_15_60","median"),
      SOS_persistence_median=("SOS_persistence_30_60","median"),RAF_persistence_median=("RAF_persistence_30_60","median")
    ).reset_index()
    result={
      "schema_version":"0.1","experiment_id":"UMEKI2025_EGF_SOS_RAF_DEPTH_RATE_P0Q_V01",
      "status":"EXECUTED_VALID_P0Q",
      "evidence_class":"P0-Q_LITERATURE_OPEN_DIRECT_SINGLE_CELL_REPRESENTATION_QUALIFICATION",
      "upstream_commit":UPSTREAM,
      "n_valid_paired_cells":int(len(df)),"n_representation_failures":int(len(fail)),
      "pair_inventory":inventory.to_dict(orient="records"),
      "dose_medians":by.to_dict(orient="records"),
      "depth_vs_input":{"cross_validation":primary,"bootstrap":boot,"disposition":pdisp},
      "representation":rep,
      "biological_chi":"EGF_INPUT_TO_PAIRED_SOS_RAF_TEMPORAL_ORGANIZATION_QUALIFIED_P0Q",
      "Chi_bio":rep["disposition"],
      "chi_bio":"NOT_OPENED_NOT_LICENSED",
      "claim_ceiling":"one direct single-cell RAS-MAPK source in SOS-knockout HeLa cells; no universal scalar or cancer-wide mechanism"
    }
    (OUT/"UMEKI2025_EGF_SOS_RAF_DEPTH_RATE_P0Q_V01_RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    try:main()
    except Exception as e:
        fail={"schema_version":"0.1","experiment_id":"UMEKI2025_EGF_SOS_RAF_DEPTH_RATE_P0Q_V01",
              "status":"EXECUTION_FAILURE_PRESERVED","error_type":type(e).__name__,"error":str(e),
              "traceback":traceback.format_exc()}
        (OUT/"UMEKI2025_EGF_SOS_RAF_DEPTH_RATE_P0Q_V01_FAILURE.json").write_text(json.dumps(fail,indent=2)+"\n")
        print(json.dumps(fail,indent=2))
        raise
