#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, urllib.request, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

ROOT=Path("BIO_CHI/artifacts/generated/kizilirmak2023_il1b_c_d_v01")
ROOT.mkdir(parents=True,exist_ok=True)
TABLE_URL="https://ars.els-cdn.com/content/image/1-s2.0-S2589004223026500-mmc3.xls"
DYN_URL="https://ars.els-cdn.com/content/image/1-s2.0-S2589004223026500-mmc2.zip"
TABLE_SHA="f76c8eaf685d192f2340d178aac62f8263004077276d3e64f96ba41faab408f4"
DYN_SHA="9ee2914095e9676b92806c33e46929965c6b4c7535f74a00d4462152678ba7b8"
CLONES=["B","R","G"]
CIRCUIT=["Il1rap","Rela","Nfkbia","Tnfaip3"]

def get(url):
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 GRI-BioChi-IL1B-analysis/0.1"})
    with urllib.request.urlopen(req,timeout=120) as r: return r.read()
def sha(b): return hashlib.sha256(b).hexdigest()

def matlab_smooth5(y):
    y=np.asarray(y,dtype=float); n=len(y)
    if n<5: return pd.Series(y).rolling(window=min(5,n),center=True,min_periods=1).mean().to_numpy()
    out=np.empty(n,float); out[0]=y[0]; out[1]=np.mean(y[:3])
    for i in range(2,n-2): out[i]=np.mean(y[i-2:i+3])
    out[-2]=np.mean(y[-3:]); out[-1]=y[-1]
    return out

def dynamics(raw,dt=6.0):
    raw=np.asarray(raw,float)
    x=raw[:,np.all(np.isfinite(raw),axis=0)]
    counts=[]; aucs=[]; first=[]
    for j in range(x.shape[1]):
        y=x[:,j]; ys=matlab_smooth5(y)
        peaks,props=find_peaks(ys,prominence=0.15)
        prom=props.get("prominences",np.array([]))
        peaks=peaks[prom>0.15]
        counts.append(len(peaks)); aucs.append(float(np.trapezoid(y,dx=dt))); first.append(float(np.max(y)))
    counts=np.asarray(counts,int); aucs=np.asarray(aucs,float); first=np.asarray(first,float)
    return {
      "timepoints":int(x.shape[0]),"cells":int(x.shape[1]),
      "oscillatory_fraction_ge2":float(np.mean(counts>=2)),
      "peak_count_median":float(np.median(counts)),
      "peak_count_mean":float(np.mean(counts)),
      "peak_count_distribution":{str(k):int(np.sum(counts==k)) for k in sorted(set(counts.tolist()))},
      "auc_median":float(np.median(aucs)),"auc_mean":float(np.mean(aucs)),
      "first_peak_median":float(np.median(first))
    }

def chi_calc(df,cols,ddof=1):
    x=df[cols].apply(pd.to_numeric,errors="coerce").to_numpy(float)
    finite=np.all(np.isfinite(x),axis=1); mu=np.mean(x,axis=1); sd=np.std(x,axis=1,ddof=ddof)
    el=finite & np.isfinite(mu)&np.isfinite(sd)&(mu>0)
    chi=np.full(len(df),np.nan); chi[el]=sd[el]/(2*mu[el])
    return chi,el,mu,sd
def summ(v):
    v=np.asarray(v,float); v=v[np.isfinite(v)]
    return {"n":int(len(v)),"median":float(np.median(v)),"q25":float(np.quantile(v,.25)),"q75":float(np.quantile(v,.75)),"mean":float(np.mean(v))}
def sgn(v): return 0 if (not np.isfinite(v) or v==0) else (1 if v>0 else -1)
def robust(full,arr): return bool(sgn(full)!=0 and all(sgn(x)==sgn(full) for x in arr))

result={"schema_version":"0.1","task_id":"GRI_BIOCHI_KIZILIRMAK_IL1B_C_D_TRANSPORT_20260925","status":"STARTED","evidence_tier":"P0 exploratory transport / source-qualified relational test"}

tb=get(TABLE_URL); db=get(DYN_URL)
if sha(tb)!=TABLE_SHA or sha(db)!=DYN_SHA: raise RuntimeError("source hash mismatch")
(ROOT/"mmc3.xls").write_bytes(tb); (ROOT/"mmc2.zip").write_bytes(db)
result["source_hashes"]={"table_s3":sha(tb),"data_s1":sha(db)}

# Native IL-1beta dynamics first.
with zipfile.ZipFile(ROOT/"mmc2.zip") as z:
    dyn={}
    for cl in CLONES:
        name=f"Dynamics data/Fig5/NFkappaBIL1beta_Clone{cl}_Fig5.csv"
        with z.open(name) as fh:
            mat=pd.read_csv(fh,header=None).to_numpy(float)
        dyn[cl]=dynamics(mat)
result["native_dynamics"]=dyn
primary_R_gt_B=dyn["R"]["oscillatory_fraction_ge2"]>dyn["B"]["oscillatory_fraction_ge2"]
secondary_G_gt_B=dyn["G"]["oscillatory_fraction_ge2"]>dyn["B"]["oscillatory_fraction_ge2"]
auc_B_gt_R=dyn["B"]["auc_median"]>dyn["R"]["auc_median"]
auc_B_gt_G=dyn["B"]["auc_median"]>dyn["G"]["auc_median"]
first_BG_gt_R=((dyn["B"]["first_peak_median"]+dyn["G"]["first_peak_median"])/2)>dyn["R"]["first_peak_median"]
result["dynamic_gate"]={
 "primary_R_gt_B_oscillatory_fraction":bool(primary_R_gt_B),
 "secondary_G_gt_B_oscillatory_fraction":bool(secondary_G_gt_B),
 "B_gt_R_median_AUC":bool(auc_B_gt_R),
 "B_gt_G_median_AUC":bool(auc_B_gt_G),
 "descriptive_mean_BG_first_peak_gt_R":bool(first_BG_gt_R)
}
if not primary_R_gt_B:
    result["status"]="REFUSE_IL1B_NATIVE_PRIMARY_DYNAMIC_GATE"
    (ROOT/"KIZILIRMAK2023_IL1B_C_D_RESULT_PIN_V01.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    raise SystemExit(2)

# Static A/B only after primary native gate.
df=pd.read_excel(ROOT/"mmc3.xls",sheet_name="Sheet1",engine="xlrd")
df.columns=[str(c).strip() for c in df.columns]; df["GeneID"]=df["GeneID"].astype(str).str.strip()
if df["GeneID"].duplicated().any(): raise RuntimeError("duplicate GeneID")
cols={cl:[f"s{i}_clone_{cl}_ut" for i in range(1,6)] for cl in CLONES}
chi={};el={};mu={};sd={}
for cl in CLONES: chi[cl],el[cl],mu[cl],sd[cl]=chi_calc(df,cols[cl],1)
common=el["B"]&el["R"]&el["G"]
A={cl:summ(chi[cl][common]) for cl in CLONES}
dA_BR=A["B"]["median"]-A["R"]["median"]; dA_BG=A["B"]["median"]-A["G"]["median"]

idx={g:int(np.flatnonzero(df["GeneID"].to_numpy()==g)[0]) for g in CIRCUIT}
if set(idx)!=set(CIRCUIT): raise RuntimeError("missing frozen circuit gene")
B={cl:summ(np.array([chi[cl][idx[g]] for g in CIRCUIT],float)) for cl in CLONES}
dB_BR=B["B"]["median"]-B["R"]["median"]; dB_BG=B["B"]["median"]-B["G"]["median"]

loo_A_BR=[]; loo_A_BG=[]; loo_B_BR=[]; loo_B_BG=[]
for drop in range(5):
    c4={}; e4={}
    for cl in CLONES:
        keep=[c for i,c in enumerate(cols[cl]) if i!=drop]
        c4[cl],e4[cl],_,_=chi_calc(df,keep,1)
    cm=e4["B"]&e4["R"]&e4["G"]
    loo_A_BR.append(float(np.nanmedian(c4["B"][cm])-np.nanmedian(c4["R"][cm])))
    loo_A_BG.append(float(np.nanmedian(c4["B"][cm])-np.nanmedian(c4["G"][cm])))
    for pair,out in [(("B","R"),loo_B_BR),(("B","G"),loo_B_BG)]:
        x=np.array([c4[pair[0]][idx[g]] for g in CIRCUIT],float)
        y=np.array([c4[pair[1]][idx[g]] for g in CIRCUIT],float)
        out.append(float(np.median(x)-np.median(y)))

result["A_genomewide"]={
 "common_eligible_genes":int(np.sum(common)),"clone_summaries":A,
 "Delta_A_B_minus_R":float(dA_BR),"Delta_A_B_minus_G":float(dA_BG),
 "LOO_Delta_A_BR":loo_A_BR,"LOO_Delta_A_BG":loo_A_BG,
 "BR_direction_robust":robust(dA_BR,loo_A_BR),"BG_direction_robust":robust(dA_BG,loo_A_BG)
}

genes=[]
for g in CIRCUIT:
    ix=idx[g]
    genes.append({"GeneID":g,
      "chi_B":float(chi["B"][ix]),"chi_R":float(chi["R"][ix]),"chi_G":float(chi["G"][ix]),
      "Delta_BR":float(chi["B"][ix]-chi["R"][ix]),"Delta_BG":float(chi["B"][ix]-chi["G"][ix])})
result["B_circuit"]={
 "genes":genes,"clone_summaries":B,
 "Delta_B_B_minus_R":float(dB_BR),"Delta_B_B_minus_G":float(dB_BG),
 "LOO_Delta_B_BR":loo_B_BR,"LOO_Delta_B_BG":loo_B_BG,
 "BR_direction_robust":robust(dB_BR,loo_B_BR),"BG_direction_robust":robust(dB_BG,loo_B_BG)
}

# Leave-one-gene-out circuit fragility is prespecified diagnostic only.
loge=[]
for leave in CIRCUIT:
    keep=[g for g in CIRCUIT if g!=leave]
    rec={"left_out":leave}
    for other,label in [("R","BR"),("G","BG")]:
        xb=np.array([chi["B"][idx[g]] for g in keep],float)
        xo=np.array([chi[other][idx[g]] for g in keep],float)
        rec[f"Delta_{label}"]=float(np.median(xb)-np.median(xo))
    loge.append(rec)
result["B_circuit"]["leave_one_gene_out"]=loge

# D: transport of global relation vs local scalar.
A_global=(dA_BR>0 and dA_BG>0 and robust(dA_BR,loo_A_BR) and robust(dA_BG,loo_A_BG))
B_local=(dB_BR>0 and dB_BG>0 and robust(dB_BR,loo_B_BR) and robust(dB_BG,loo_B_BG))
partial_dyn=primary_R_gt_B and not secondary_G_gt_B
if partial_dyn:
    D="partial_dynamic_transport"
elif not A_global:
    D="global_nontransport"
elif A_global and B_local:
    D="global_and_local_concordant_transport"
else:
    D="global_transport_with_local_scalar_refusal"
result["D_joint"]={
 "classification":D,
 "A_global_transport":bool(A_global),"B_local_scalar_transport":bool(B_local),
 "native_primary_pass":bool(primary_R_gt_B),"native_secondary_pass":bool(secondary_G_gt_B),
 "claim_ceiling":"exploratory relational transport only; no physical damping-ratio identification"
}
result["status"]="PASS_IL1B_TRANSPORT_EXECUTED"
(ROOT/"KIZILIRMAK2023_IL1B_C_D_RESULT_PIN_V01.json").write_text(json.dumps(result,indent=2),encoding="utf-8")

lines=[
"# Kizilirmak IL-1beta C+D transport v0.1","",f"**Status:** {result['status']}","",
"## Native IL-1beta dynamics",
f"- Oscillatory fraction >=2 peaks: B={dyn['B']['oscillatory_fraction_ge2']:.6f}, R={dyn['R']['oscillatory_fraction_ge2']:.6f}, G={dyn['G']['oscillatory_fraction_ge2']:.6f}.",
f"- Primary R>B: **{primary_R_gt_B}**; secondary G>B: **{secondary_G_gt_B}**.",
f"- Median AUC: B={dyn['B']['auc_median']:.6f}, R={dyn['R']['auc_median']:.6f}, G={dyn['G']['auc_median']:.6f}.","",
"## A — unchanged genome-wide lane",
f"- Median chi_GRI: B={A['B']['median']:.8g}, R={A['R']['median']:.8g}, G={A['G']['median']:.8g}.",
f"- Delta_A B-R={dA_BR:.8g}; robust={result['A_genomewide']['BR_direction_robust']}.",
f"- Delta_A B-G={dA_BG:.8g}; robust={result['A_genomewide']['BG_direction_robust']}.","",
"## B — IL-1beta source-native circuit",
f"- Frozen genes: {', '.join(CIRCUIT)}.",
f"- Median circuit chi_GRI: B={B['B']['median']:.8g}, R={B['R']['median']:.8g}, G={B['G']['median']:.8g}.",
f"- Delta_B B-R={dB_BR:.8g}; robust={result['B_circuit']['BR_direction_robust']}.",
f"- Delta_B B-G={dB_BG:.8g}; robust={result['B_circuit']['BG_direction_robust']}.",
]
for g in genes: lines.append(f"- {g['GeneID']}: Delta_BR={g['Delta_BR']:.8g}; Delta_BG={g['Delta_BG']:.8g}.")
lines += ["","## D — joint transport",f"**{D}**","",
"## Claim boundary","This transport does not test or restore mu=omega, sigma=gamma, chi_GRI as a physical damping ratio, or chi=1 as a biological critical boundary."]
(ROOT/"KIZILIRMAK2023_IL1B_C_D_RESULT_AUDIT_V01.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
