#!/usr/bin/env python3
"""Frozen E. coli sensory Bio Chi P0-Q execution.

Implements ECOLI2024_REPRESENTATION_TEST_SPEC_v0_1.md.
No outcome-dependent tuning is permitted.
"""
from __future__ import annotations
import hashlib, json, math, os, sys, time
from pathlib import Path
import numpy as np
import pandas as pd
import requests
from scipy.io import loadmat
from scipy.optimize import minimize
from scipy.special import gammaln
from scipy.stats import spearmanr

SEED=20260925
RNG=np.random.default_rng(SEED)
ROOT=Path(__file__).resolve().parent
DATA=ROOT/"ecoli_raw"
OUT=ROOT/"ecoli_results"
DATA.mkdir(parents=True,exist_ok=True)
OUT.mkdir(parents=True,exist_ok=True)

BACKGROUNDS=[
 {"b":0.0,"files":[("220106_FOV1.mat",3293951),("230417_FOV1.mat",3293967)],"L":[0.2,0.5,1.0,2.0,4.0]},
 {"b":0.1,"files":[("230830_FOV1.mat",3294022),("230830_FOV2.mat",3294023),("230831_FOV1.mat",3294021),("230831_FOV2.mat",3294024)],"L":[0.3,0.6,1.1,2.1,4.1]},
 {"b":0.3,"files":[("220615_FOV1.mat",3293957),("230410_FOV1.mat",3293969)],"L":[0.5,0.8,1.3,2.3,4.3]},
 {"b":1.0,"files":[("230428_FOV1.mat",3293970),("230429_FOV1.mat",3293971)],"L":[1.2,1.5,2.0,3.0,5.0]},
 {"b":10.0,"files":[("220302_FOV1.mat",3293952),("220303_FOV1.mat",3293953)],"L":[10.5,11.0,12.0,14.0,18.0]},
 {"b":100.0,"files":[("210816_FOV1.mat",3293903),("230717_FOV1.mat",3294012),("230718_FOV1.mat",3294015)],"L":[102.0,105.0,110.0,120.0,140.0]}
]
BVAL=[x["b"] for x in BACKGROUNDS]
BIDX={b:i for i,b in enumerate(BVAL)}

def sha256(p):
 h=hashlib.sha256()
 with open(p,"rb") as f:
  for chunk in iter(lambda:f.read(1<<20),b""): h.update(chunk)
 return h.hexdigest()

def download(name,fid):
 p=DATA/name
 if p.exists() and p.stat().st_size>1000: return p
 urls=[
  f"https://datadryad.org/downloads/file_stream/{fid}",
  f"https://datadryad.org/stash/downloads/file_stream/{fid}",
 ]
 last=None
 for url in urls:
  for attempt in range(3):
   try:
    r=requests.get(url,headers={"User-Agent":"Mozilla/5.0 BioChi-Repro/0.1","Accept":"application/octet-stream,*/*"},timeout=90,allow_redirects=True)
    if r.status_code==200 and len(r.content)>1000:
     p.write_bytes(r.content); return p
    last=f"{url} HTTP {r.status_code} bytes={len(r.content)}"
   except Exception as e: last=f"{url} {type(e).__name__}: {e}"
   time.sleep(2**attempt)
 raise RuntimeError(f"download failed {name}: {last}")

def cells_from_mat(path):
 m=loadmat(path,simplify_cells=True)
 if "reorgData" not in m: raise KeyError("reorgData absent")
 r=m["reorgData"]
 if not isinstance(r,dict) or "resp_data" not in r: raise TypeError("reorgData.resp_data absent/unrecognized")
 cells=r["resp_data"]
 if isinstance(cells,dict): cells=[cells]
 elif isinstance(cells,np.ndarray): cells=list(cells.ravel())
 elif not isinstance(cells,(list,tuple)): cells=[cells]
 return cells

def process_fov(path,b,Ls):
 cells=cells_from_mat(path)
 rows=[]
 n_total=0;n_keep=0
 for ci,c in enumerate(cells):
  n_total+=1
  if not isinstance(c,dict) or "a" not in c or "s" not in c: continue
  a=np.asarray(c["a"],dtype=float)
  s=np.asarray(c["s"],dtype=float)
  if a.shape[0]!=35 and a.shape[1]==35: a=a.T
  if s.shape[0]!=35 and s.shape[1]==35: s=s.T
  if a.shape[0]<35 or s.shape[0]<2: continue
  stim=np.asarray(s[1,:],dtype=float).ravel()
  pre=stim==stim[0]
  post=~pre
  idx=np.flatnonzero(post)
  if len(idx)<3: continue
  post[idx[0]:idx[0]+2]=False
  premed=np.empty((7,5)); postmed=np.empty((7,5))
  ok=True
  for lev in range(5):
   ridx=np.arange(lev,35,5)[:7]
   if len(ridx)!=7: ok=False;break
   aa=a[ridx,:]
   premed[:,lev]=np.nanmedian(aa[:,pre],axis=1)
   postmed[:,lev]=np.nanmedian(aa[:,post],axis=1)
  if not ok: continue
  a0=float(np.nanmedian(premed))
  if not np.isfinite(a0) or a0<0.15: continue
  rn=np.nanmedian(postmed,axis=0)/a0
  if not np.all(np.isfinite(rn)): continue
  n_keep+=1
  for j,L in enumerate(Ls):
   rows.append({"background":b,"fov":path.name,"cell":ci,"L":float(L),"rnorm":float(rn[j]),"event":int(rn[j]<0.5),"a0":a0})
 if n_keep==0: raise RuntimeError(f"no cells survived source filter in {path.name}")
 return rows,{"background":b,"fov":path.name,"cells_loaded":n_total,"cells_retained":n_keep}

def binom_ll(k,n,p):
 p=np.clip(np.asarray(p),1e-12,1-1e-12); k=np.asarray(k); n=np.asarray(n)
 return float(np.sum(gammaln(n+1)-gammaln(k+1)-gammaln(n-k+1)+k*np.log(p)+(n-k)*np.log(1-p)))

def fit_model(df,kind):
 g=df.groupby(["background","fov","L"],as_index=False)["event"].agg(["sum","count"]).reset_index()
 Lmin=float(g.L.min());Lmax=float(g.L.max())
 mulo,muh=math.log(Lmin)-5,math.log(Lmax)+5
 initmu=[]
 for b in BVAL:
  z=g[g.background==b]
  initmu.append(float(np.log(np.median(z.L))) if len(z) else math.log(math.sqrt(Lmin*Lmax)))
 if kind=="R1":
  x0=np.array(initmu+[0.0]);bounds=[(mulo,muh)]*6+[(math.log(.05),math.log(5.0))]
 elif kind=="R2":
  x0=np.array(initmu+[0.0]*6);bounds=[(mulo,muh)]*6+[(math.log(.05),math.log(5.0))]*6
 else: raise ValueError(kind)
 def neg(x):
  mus=x[:6]
  sig=np.exp(x[6]) if kind=="R1" else np.exp(x[6:12])
  ps=[]
  for _,r in g.iterrows():
   bi=BIDX[float(r.background)]
   s=sig if kind=="R1" else sig[bi]
   z=(math.log(float(r.L))-mus[bi])/s
   p=0.5*(1+math.erf(z/math.sqrt(2)));ps.append(p)
  return -binom_ll(g["sum"].to_numpy(),g["count"].to_numpy(),np.array(ps))
 res=minimize(neg,x0,method="L-BFGS-B",bounds=bounds,options={"maxiter":2000,"ftol":1e-12})
 if not res.success: raise RuntimeError(f"{kind} optimizer failed: {res.message}")
 x=res.x
 return {"kind":kind,"x":x,"mus":x[:6],"sigmas":np.repeat(np.exp(x[6]),6) if kind=="R1" else np.exp(x[6:12]),"ll":-float(res.fun)}

def score_fov(train,test,kind):
 fit=fit_model(train,kind)
 g=test.groupby(["background","fov","L"],as_index=False)["event"].agg(["sum","count"]).reset_index()
 ps=[]
 for _,r in g.iterrows():
  bi=BIDX[float(r.background)]
  z=(math.log(float(r.L))-fit["mus"][bi])/fit["sigmas"][bi]
  ps.append(0.5*(1+math.erf(z/math.sqrt(2))))
 return binom_ll(g["sum"],g["count"],ps),fit

def main():
 manifest=[]
 allrows=[];fovstats=[]
 for spec in BACKGROUNDS:
  for name,fid in spec["files"]:
   p=download(name,fid)
   manifest.append({"name":name,"dryad_file_id":fid,"bytes":p.stat().st_size,"sha256":sha256(p)})
   rows,st=process_fov(p,spec["b"],spec["L"])
   allrows.extend(rows);fovstats.append(st)
 df=pd.DataFrame(allrows)
 df.to_csv(OUT/"cell_level_source_object.csv",index=False)
 pd.DataFrame(fovstats).to_csv(OUT/"fov_counts.csv",index=False)
 pd.DataFrame(manifest).to_csv(OUT/"source_manifest.csv",index=False)

 full1=fit_model(df,"R1"); full2=fit_model(df,"R2")
 fovs=list(df.fov.unique());cv=[]
 for f in fovs:
  test=df[df.fov==f];train=df[df.fov!=f]
  ll1,_=score_fov(train,test,"R1");ll2,_=score_fov(train,test,"R2")
  cv.append({"fov":f,"background":float(test.background.iloc[0]),"ll_R1":ll1,"ll_R2":ll2,"delta":ll2-ll1})
 cvdf=pd.DataFrame(cv);cvdf.to_csv(OUT/"leave_one_fov_out_scores.csv",index=False)
 delta=float(cvdf.delta.sum())
 vals=cvdf.delta.to_numpy()
 boot=np.array([RNG.choice(vals,size=len(vals),replace=True).sum() for _ in range(10000)])
 ci=[float(np.quantile(boot,.025)),float(np.quantile(boot,.975))]
 if ci[0]>0: disp="R2_REQUIRED_P0Q"
 elif ci[1]<0: disp="R1_SUFFICIENT_P0Q"
 else: disp="REPRESENTATION_DIFFERENCE_UNRESOLVED_P0Q"

 sig=np.asarray(full2["sigmas"],float)
 rho,pv=spearmanr(np.arange(6),sig)
 endpoint=float(sig[-1]-sig[0])

 # FOV-level bootstrap for descriptive sigma summaries.
 desc=[]
 byb={b:list(df[df.background==b].fov.unique()) for b in BVAL}
 for _ in range(2000):
  parts=[]
  for b in BVAL:
   fs=byb[b]
   draw=RNG.choice(fs,size=len(fs),replace=True)
   for j,f in enumerate(draw):
    z=df[df.fov==f].copy();z["fov"]=f"{f}__bs{j}";parts.append(z)
  bd=pd.concat(parts,ignore_index=True)
  try:
   ft=fit_model(bd,"R2"); ss=np.asarray(ft["sigmas"],float)
   rr,_=spearmanr(np.arange(6),ss)
   desc.append((rr,float(ss[-1]-ss[0])))
  except Exception:
   pass
 desc=np.asarray(desc,float)
 dci={"rho":[float(np.quantile(desc[:,0],.025)),float(np.quantile(desc[:,0],.975))] if len(desc) else [None,None],
      "endpoint":[float(np.quantile(desc[:,1],.025)),float(np.quantile(desc[:,1],.975))] if len(desc) else [None,None],
      "successful_bootstrap_fits":int(len(desc))}

 empirical=df.groupby(["background","fov","L"],as_index=False)["event"].agg(["sum","count"]).reset_index()
 empirical.to_csv(OUT/"empirical_cdf_counts.csv",index=False)
 summary={
  "schema_version":"0.1","experiment_id":"ECOLI2024_SENSORY_TOPDOWN_P0Q_V01",
  "status":"EXECUTED_VALID_RESULT","evidence_class":"P0-Q_LITERATURE_OPEN_REPRESENTATION_QUALIFICATION",
  "n_fovs":len(fovs),"n_cells_by_background":{str(b):int(df[df.background==b].cell.astype(str).groupby(df[df.background==b].fov).nunique().sum()) for b in BVAL},
  "R1":{"ll_full":full1["ll"],"mu_logK":[float(x) for x in full1["mus"]],"shared_sigma":float(full1["sigmas"][0])},
  "R2":{"ll_full":full2["ll"],"mu_logK":[float(x) for x in full2["mus"]],"sigma_logK":[float(x) for x in full2["sigmas"]]},
  "predictive_comparison":{"delta_LL_CV":delta,"bootstrap_95_CI":ci,"bootstrap_resamples":10000,"seed":SEED,"disposition":disp},
  "whole_event_descriptive":{"backgrounds_uM":BVAL,"spearman_rho_background_rank_vs_sigma":float(rho),"spearman_p_descriptive":float(pv),"sigma_100_minus_sigma_0":endpoint,"fov_bootstrap_95_CI":dci},
  "chi_bio":"NOT_OPENED_NOT_LICENSED",
  "Chi_bio":disp,
  "Bio_Chi":"BACKGROUND_CONDITIONED_SENSORY_DISTRIBUTION_REORGANIZATION_REPRODUCED_DESCRIPTIVELY" if rho<0 and endpoint<0 else "SOURCE_OPEN_EVENT_NOT_REPRODUCED_UNDER_FROZEN_SUMMARY",
  "source_manifest":manifest
 }
 (OUT/"ECOLI2024_SENSORY_TOPDOWN_P0Q_V01_RESULT.json").write_text(json.dumps(summary,indent=2)+"\n")
 print(json.dumps(summary,indent=2))

if __name__=="__main__":
 try: main()
 except Exception as e:
  fail={"schema_version":"0.1","experiment_id":"ECOLI2024_SENSORY_TOPDOWN_P0Q_V01","status":"EXECUTION_FAILURE_PRESERVED","error_type":type(e).__name__,"error":str(e)}
  (OUT/"ECOLI2024_SENSORY_TOPDOWN_P0Q_V01_FAILURE.json").write_text(json.dumps(fail,indent=2)+"\n")
  print(json.dumps(fail,indent=2),file=sys.stderr)
  raise
