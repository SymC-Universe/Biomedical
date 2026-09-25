#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, urllib.request, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

ROOT=Path("BIO_CHI/artifacts/generated/kizilirmak2023_context_gate_v01")
ROOT.mkdir(parents=True,exist_ok=True)
TABLE_URL="https://ars.els-cdn.com/content/image/1-s2.0-S2589004223026500-mmc3.xls"
DYN_URL="https://ars.els-cdn.com/content/image/1-s2.0-S2589004223026500-mmc2.zip"
TABLE_SHA="f76c8eaf685d192f2340d178aac62f8263004077276d3e64f96ba41faab408f4"
DYN_SHA="9ee2914095e9676b92806c33e46929965c6b4c7535f74a00d4462152678ba7b8"
CLONES=["B","R","G"]
GENES=["Tnfrsf1a","Il1rap","Rela","Nfkbia","Tnfaip3"]

def get(url):
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 GRI-BioChi-context-gate/0.1"})
    with urllib.request.urlopen(req,timeout=120) as r: return r.read()
def sha(b): return hashlib.sha256(b).hexdigest()

def smooth5(y):
    y=np.asarray(y,float); n=len(y)
    if n<5: return pd.Series(y).rolling(window=min(5,n),center=True,min_periods=1).mean().to_numpy()
    o=np.empty(n,float); o[0]=y[0]; o[1]=np.mean(y[:3])
    for i in range(2,n-2): o[i]=np.mean(y[i-2:i+3])
    o[-2]=np.mean(y[-3:]); o[-1]=y[-1]
    return o

def dyn_metrics(mat,dt=6.0):
    mat=np.asarray(mat,float); mat=mat[:,np.all(np.isfinite(mat),axis=0)]
    counts=[]; aucs=[]; fp=[]; maxv=[]
    for j in range(mat.shape[1]):
        y=mat[:,j]; ys=smooth5(y)
        peaks,props=find_peaks(ys,prominence=0.15)
        prom=props.get("prominences",np.array([]))
        peaks=peaks[prom>0.15]
        counts.append(len(peaks))
        aucs.append(float(np.trapezoid(y,dx=dt)))
        if len(peaks):
            fp.append(float(ys[peaks[0]]))
        maxv.append(float(np.max(ys)))
    counts=np.asarray(counts,int); aucs=np.asarray(aucs,float); fp=np.asarray(fp,float); maxv=np.asarray(maxv,float)
    return {
      "cells":int(mat.shape[1]),"timepoints":int(mat.shape[0]),
      "oscillatory_fraction_ge2":float(np.mean(counts>=2)),
      "auc_median":float(np.median(aucs)),
      "first_detected_peak_n":int(len(fp)),
      "first_detected_peak_median":float(np.median(fp)) if len(fp) else None,
      "smoothed_max_median":float(np.median(maxv)),
      "peak_count_mean":float(np.mean(counts))
    }

def rna_metrics(df,gene):
    row=df.loc[df["GeneID"].astype(str).str.strip()==gene]
    if len(row)!=1: raise RuntimeError(f"{gene} rows={len(row)}")
    out={}
    for cl in CLONES:
        cols=[f"s{i}_clone_{cl}_ut" for i in range(1,6)]
        x=row[cols].apply(pd.to_numeric,errors="coerce").to_numpy(float).ravel()
        if len(x)!=5 or not np.all(np.isfinite(x)): raise RuntimeError(f"{gene} {cl} invalid")
        mu=float(np.mean(x)); sd=float(np.std(x,ddof=1)); chi=float(sd/(2*mu)) if mu>0 else None
        out[cl]={"mean":mu,"sd":sd,"chi_GRI":chi}
    return out

tb=get(TABLE_URL); db=get(DYN_URL)
if sha(tb)!=TABLE_SHA or sha(db)!=DYN_SHA: raise RuntimeError("source hash mismatch")
(ROOT/"mmc3.xls").write_bytes(tb); (ROOT/"mmc2.zip").write_bytes(db)

# Reproduce both source-native stimuli identically.
with zipfile.ZipFile(ROOT/"mmc2.zip") as z:
    dyn={"TNF":{},"IL1B":{}}
    for cl in CLONES:
        for stim,fig,pat in [
            ("TNF","Fig2",f"Dynamics data/Fig2/NFkappaBTNF_Clone{cl}_Fig2.csv"),
            ("IL1B","Fig5",f"Dynamics data/Fig5/NFkappaBIL1beta_Clone{cl}_Fig5.csv")
        ]:
            with z.open(pat) as fh:
                mat=pd.read_csv(fh,header=None).to_numpy(float)
            dyn[stim][cl]=dyn_metrics(mat)

df=pd.read_excel(ROOT/"mmc3.xls",sheet_name="Sheet1",engine="xlrd")
df.columns=[str(c).strip() for c in df.columns]
df["GeneID"]=df["GeneID"].astype(str).str.strip()
rna={g:rna_metrics(df,g) for g in GENES}

# Frozen source-rank adjudication.
tnf_mean={cl:rna["Tnfrsf1a"][cl]["mean"] for cl in CLONES}
tnf_fp={cl:dyn["TNF"][cl]["first_detected_peak_median"] for cl in CLONES}
tnf_receptor_pass=(tnf_mean["B"]>tnf_mean["R"]>tnf_mean["G"])
tnf_peak_pass=(tnf_fp["B"]>tnf_fp["R"]>tnf_fp["G"])
tnf_pass=tnf_receptor_pass and tnf_peak_pass

il_mean={cl:rna["Il1rap"][cl]["mean"] for cl in CLONES}
il_fp={cl:dyn["IL1B"][cl]["first_detected_peak_median"] for cl in CLONES}
il_receptor_pass=(il_mean["R"]<il_mean["B"] and il_mean["R"]<il_mean["G"])
il_peak_pass=(il_fp["R"]<il_fp["B"] and il_fp["R"]<il_fp["G"])
il_pass=il_receptor_pass and il_peak_pass

stim_shift={}
for cl in CLONES:
    stim_shift[cl]={
      "Delta_oscillatory_fraction_IL1B_minus_TNF":float(dyn["IL1B"][cl]["oscillatory_fraction_ge2"]-dyn["TNF"][cl]["oscillatory_fraction_ge2"]),
      "Delta_AUC_median_IL1B_minus_TNF":float(dyn["IL1B"][cl]["auc_median"]-dyn["TNF"][cl]["auc_median"]),
      "Delta_first_peak_median_IL1B_minus_TNF":float(dyn["IL1B"][cl]["first_detected_peak_median"]-dyn["TNF"][cl]["first_detected_peak_median"])
    }

classification="CONTEXT_GATING_LIMIT_OF_GLOBAL_STATIC_SCALAR" if (tnf_pass and il_pass) else "CONTEXT_GATE_EXPLANATION_INCOMPLETE"

out={
  "schema_version":"0.1",
  "task_id":"GRI_BIOCHI_KIZILIRMAK_CONTEXT_GATE_20260925",
  "status":"PASS_DIAGNOSTIC_EXECUTED",
  "source_hashes":{"table_s3":sha(tb),"data_s1":sha(db)},
  "dynamics":dyn,
  "rna_components":rna,
  "stimulus_shift":stim_shift,
  "rank_tests":{
    "TNF":{"receptor_mean_B_gt_R_gt_G":bool(tnf_receptor_pass),"first_peak_B_gt_R_gt_G":bool(tnf_peak_pass),"pass":bool(tnf_pass)},
    "IL1B":{"receptor_mean_R_lowest_BG_top_pair":bool(il_receptor_pass),"first_peak_R_lowest_BG_top_pair":bool(il_peak_pass),"pass":bool(il_pass)}
  },
  "classification":classification,
  "interpretation":"Stimulus-specific limiting-receptor abundance can reorganize early NF-kB activation and downstream oscillatory phenotype in ways not encoded by the unchanged genome-wide historical chi_GRI scalar. This supports a context-gating limitation of the scalar if both source-rank tests pass.",
  "forbidden_inference":"No new scalar, no mu=omega, no sigma=gamma, no physical damping-ratio identification."
}
(ROOT/"KIZILIRMAK2023_CONTEXT_GATE_V01.json").write_text(json.dumps(out,indent=2),encoding="utf-8")

lines=["# Kizilirmak TNF vs IL-1beta context-gating diagnostic v0.1","",f"**Classification:** {classification}","",
       "## Source-native dynamics"]
for stim in ["TNF","IL1B"]:
    for cl in CLONES:
        d=dyn[stim][cl]
        lines.append(f"- {stim} {cl}: oscillatory={d['oscillatory_fraction_ge2']:.6f}; AUC={d['auc_median']:.6f}; first peak={d['first_detected_peak_median']:.6f}")
lines+=["","## Receptor means and rank tests"]
for g in ["Tnfrsf1a","Il1rap"]:
    lines.append(f"- {g}: B={rna[g]['B']['mean']:.6f}, R={rna[g]['R']['mean']:.6f}, G={rna[g]['G']['mean']:.6f}")
lines.append(f"- TNF receptor/first-peak rank match: **{tnf_pass}**")
lines.append(f"- IL-1beta receptor/first-peak rank match: **{il_pass}**")
lines+=["","## Stimulus shifts"]
for cl,v in stim_shift.items():
    lines.append(f"- {cl}: Delta oscillatory={v['Delta_oscillatory_fraction_IL1B_minus_TNF']:.6f}; Delta AUC={v['Delta_AUC_median_IL1B_minus_TNF']:.6f}; Delta first peak={v['Delta_first_peak_median_IL1B_minus_TNF']:.6f}")
lines+=["","## Component table"]
for g in GENES:
    lines.append(f"- {g}:")
    for cl in CLONES:
        m=rna[g][cl]
        lines.append(f"  - {cl}: mean={m['mean']:.6f}; SD={m['sd']:.6f}; chi_GRI={m['chi_GRI']:.8g}")
lines+=["","## Boundary","This diagnostic explains or fails to explain context gating. It cannot restore the retired literal damping mapping."]
(ROOT/"KIZILIRMAK2023_CONTEXT_GATE_AUDIT_V01.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
