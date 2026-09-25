#!/usr/bin/env python3
from __future__ import annotations
import hashlib, itertools, json, math, sys, urllib.request, zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from scipy.stats import spearmanr, kendalltau

ROOT=Path("BIO_CHI/artifacts/generated/kizilirmak2023_c_d_v01")
ROOT.mkdir(parents=True,exist_ok=True)
TABLE_URL="https://ars.els-cdn.com/content/image/1-s2.0-S2589004223026500-mmc3.xls"
DYN_URL="https://ars.els-cdn.com/content/image/1-s2.0-S2589004223026500-mmc2.zip"
TABLE_SHA="f76c8eaf685d192f2340d178aac62f8263004077276d3e64f96ba41faab408f4"
DYN_SHA="9ee2914095e9676b92806c33e46929965c6b4c7535f74a00d4462152678ba7b8"
CLONES=["B","R","G"]
CIRCUIT=["Tnfrsf1a","Rela","Nfkbia","Tnfaip3"]

def get(url: str) -> bytes:
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 GRI-BioChi-analysis/0.1"})
    with urllib.request.urlopen(req,timeout=120) as r:
        return r.read()

def sha(b:bytes)->str:
    return hashlib.sha256(b).hexdigest()

def matlab_smooth5(y: np.ndarray) -> np.ndarray:
    # MATLAB smooth(y) default: moving average, span 5, with progressively
    # shorter odd spans at the endpoints.
    y=np.asarray(y,dtype=float)
    n=len(y)
    if n<5:
        return pd.Series(y).rolling(window=min(5,n),center=True,min_periods=1).mean().to_numpy()
    out=np.empty(n,dtype=float)
    out[0]=y[0]
    out[1]=np.mean(y[:3])
    for i in range(2,n-2):
        out[i]=np.mean(y[i-2:i+3])
    out[-2]=np.mean(y[-3:])
    out[-1]=y[-1]
    return out

def dynamic_metrics(raw: np.ndarray, dt_min: float=6.0) -> dict:
    raw=np.asarray(raw,dtype=float)
    # Source matrices are time x cell.
    finite_cols=np.all(np.isfinite(raw),axis=0)
    x=raw[:,finite_cols]
    counts=[]
    aucs=[]
    first_peaks=[]
    for j in range(x.shape[1]):
        y=x[:,j]
        ys=matlab_smooth5(y)
        peaks, props=find_peaks(ys,prominence=0.15)
        prom=props.get("prominences",np.array([]))
        peaks=peaks[prom>0.15]
        counts.append(int(len(peaks)))
        aucs.append(float(np.trapezoid(y,dx=dt_min)))
        first_peaks.append(float(np.max(y)))
    counts=np.asarray(counts,int)
    aucs=np.asarray(aucs,float)
    return {
        "timepoints":int(x.shape[0]),
        "cells_total":int(raw.shape[1]),
        "cells_finite":int(x.shape[1]),
        "oscillatory_fraction_ge2":float(np.mean(counts>=2)),
        "peak_count_median":float(np.median(counts)),
        "peak_count_mean":float(np.mean(counts)),
        "peak_count_distribution":{str(k):int(np.sum(counts==k)) for k in sorted(set(counts.tolist()))},
        "auc_median":float(np.median(aucs)),
        "auc_mean":float(np.mean(aucs)),
        "first_peak_median":float(np.median(first_peaks)),
    }

def signclass(v: float) -> int:
    if not np.isfinite(v) or v==0: return 0
    return 1 if v>0 else -1

def chi_from_cols(df:pd.DataFrame, cols:list[str], ddof:int=1):
    arr=df[cols].apply(pd.to_numeric,errors="coerce").to_numpy(float)
    finite=np.all(np.isfinite(arr),axis=1)
    mu=np.mean(arr,axis=1)
    sd=np.std(arr,axis=1,ddof=ddof)
    eligible=finite & np.isfinite(mu) & np.isfinite(sd) & (mu>0)
    chi=np.full(len(df),np.nan,float)
    chi[eligible]=sd[eligible]/(2.0*mu[eligible])
    return chi, eligible, mu, sd

def summary(vals: np.ndarray) -> dict:
    v=np.asarray(vals,float)
    v=v[np.isfinite(v)]
    return {
        "n":int(len(v)),
        "median":float(np.median(v)),
        "q25":float(np.quantile(v,0.25)),
        "q75":float(np.quantile(v,0.75)),
        "mean":float(np.mean(v)),
    }

result={
  "schema_version":"0.1",
  "task_id":"GRI_BIOCHI_KIZILIRMAK_C_D_EXECUTION_20260925",
  "evidence_tier":"P0 exploratory / source-qualified relational test",
  "status":"STARTED",
  "source":{},
  "dynamic":{},
  "A_genomewide":{},
  "B_circuit":{},
  "D_joint":{},
  "claim_ceiling":"No physical damping-ratio identification; no chi=1 biological boundary."
}

# Materialize and pin sources.
tb=get(TABLE_URL); db=get(DYN_URL)
if sha(tb)!=TABLE_SHA: raise RuntimeError("Table S3 SHA mismatch")
if sha(db)!=DYN_SHA: raise RuntimeError("Data S1 SHA mismatch")
(ROOT/"mmc3.xls").write_bytes(tb)
(ROOT/"mmc2.zip").write_bytes(db)
result["source"]={"table_s3_sha256":sha(tb),"data_s1_sha256":sha(db)}

# Native dynamics first. If this fails, do not open transcriptomic values.
with zipfile.ZipFile(ROOT/"mmc2.zip") as z:
    dyn={}
    for fig in ["Fig2","Fig1"]:
        dyn[fig]={}
        for cl in CLONES:
            name=f"Dynamics data/{fig}/NFkappaBTNF_Clone{cl}_{fig}.csv"
            with z.open(name) as fh:
                mat=pd.read_csv(fh,header=None).to_numpy(float)
            dyn[fig][cl]=dynamic_metrics(mat)
result["dynamic"]=dyn
fig2_pass=dyn["Fig2"]["R"]["oscillatory_fraction_ge2"]>dyn["Fig2"]["B"]["oscillatory_fraction_ge2"]
fig2_auc_pass=dyn["Fig2"]["B"]["auc_median"]>dyn["Fig2"]["R"]["auc_median"]
fig1_robust=dyn["Fig1"]["R"]["oscillatory_fraction_ge2"]>dyn["Fig1"]["B"]["oscillatory_fraction_ge2"]
result["dynamic_gate"]={
    "fig2_primary_R_gt_B_oscillatory_fraction":bool(fig2_pass),
    "fig2_secondary_B_gt_R_median_AUC":bool(fig2_auc_pass),
    "fig1_R_gt_B_oscillatory_fraction_robustness":bool(fig1_robust)
}
if not fig2_pass:
    result["status"]="REFUSE_NATIVE_DYNAMIC_REPRODUCTION_GATE"
    (ROOT/"KIZILIRMAK2023_C_D_RESULT_PIN_V01.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    raise SystemExit(2)

# Only after the native gate passes, open static RNA values.
df=pd.read_excel(ROOT/"mmc3.xls",sheet_name="Sheet1",engine="xlrd")
df.columns=[str(c).strip() for c in df.columns]
df["GeneID"]=df["GeneID"].astype(str).str.strip()
if df["GeneID"].duplicated().any():
    result["status"]="REFUSE_DUPLICATE_GENE_IDS"
    result["duplicate_gene_ids"]=int(df["GeneID"].duplicated().sum())
    (ROOT/"KIZILIRMAK2023_C_D_RESULT_PIN_V01.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    raise SystemExit(3)

cols={cl:[f"s{i}_clone_{cl}_ut" for i in range(1,6)] for cl in CLONES}
chis={}; elig={}; mus={}; sds={}
for cl in CLONES:
    chis[cl],elig[cl],mus[cl],sds[cl]=chi_from_cols(df,cols[cl],ddof=1)
common=elig["B"] & elig["R"] & elig["G"]
result["static_representation"]={
    "source":"Table S3 published log2 RPKM",
    "historical_reference":"log2(TPM+1)",
    "common_eligible_genes":int(np.sum(common)),
    "excluded_from_common":int(len(df)-np.sum(common)),
    "all_rows":int(len(df)),
    "scale_qualification":"transport of historical operational form on source-native transformed abundance; not exact preprocessing replication"
}

geneout=pd.DataFrame({"GeneID":df["GeneID"]})
for cl in CLONES:
    geneout[f"chi_{cl}"]=chis[cl]
geneout=geneout.loc[common].reset_index(drop=True)
geneout.to_csv(ROOT/"KIZILIRMAK2023_GENEWISE_CHI_GRI_V01.csv",index=False)

A_summ={cl:summary(chis[cl][common]) for cl in CLONES}
delta_A=A_summ["B"]["median"]-A_summ["R"]["median"]
paired=chis["B"][common]-chis["R"][common]
result["A_genomewide"]={
    "clone_summaries":A_summ,
    "Delta_A_B_minus_R":float(delta_A),
    "fraction_gene_chi_B_gt_R":float(np.mean(paired>0)),
    "paired_gene_difference_median":float(np.median(paired))
}

# Matched leave-one-biological-replicate-out robustness.
loo_A=[]; loo_B=[]
idx_by_gene={g:int(np.flatnonzero(df["GeneID"].to_numpy()==g)[0]) for g in CIRCUIT}
for drop in range(5):
    chi4={}; el4={}
    for cl in CLONES:
        keep=[c for i,c in enumerate(cols[cl]) if i!=drop]
        chi4[cl],el4[cl],_,_=chi_from_cols(df,keep,ddof=1)
    cm=el4["B"] & el4["R"] & el4["G"]
    a=float(np.nanmedian(chi4["B"][cm])-np.nanmedian(chi4["R"][cm]))
    loo_A.append(a)
    bv=[];rv=[]
    for g in CIRCUIT:
        ix=idx_by_gene[g]
        if el4["B"][ix] and el4["R"][ix]:
            bv.append(chi4["B"][ix]);rv.append(chi4["R"][ix])
    loo_B.append(float(np.median(bv)-np.median(rv)) if len(bv)==len(CIRCUIT) else float("nan"))

result["A_genomewide"]["leave_one_replicate_out_Delta_A"]=loo_A
result["A_genomewide"]["direction_robust_all5"]=bool(signclass(delta_A)!=0 and all(signclass(v)==signclass(delta_A) for v in loo_A))

# B: four frozen source-defined circuit genes.
crows=[]
for g in CIRCUIT:
    ix=idx_by_gene[g]
    rec={"GeneID":g}
    for cl in CLONES:
        rec[f"chi_{cl}"]=float(chis[cl][ix]) if np.isfinite(chis[cl][ix]) else None
        rec[f"eligible_{cl}"]=bool(elig[cl][ix])
    crows.append(rec)
circ=pd.DataFrame(crows)
circ.to_csv(ROOT/"KIZILIRMAK2023_CIRCUIT_CHI_GRI_V01.csv",index=False)
if not all(bool(r[f"eligible_{cl}"]) for r in crows for cl in CLONES):
    result["status"]="REFUSE_CIRCUIT_GENE_INELIGIBILITY"
    result["B_circuit"]["genes"]=crows
    (ROOT/"KIZILIRMAK2023_C_D_RESULT_PIN_V01.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    raise SystemExit(4)
B_summ={cl:summary(circ[f"chi_{cl}"].to_numpy(float)) for cl in CLONES}
delta_B=B_summ["B"]["median"]-B_summ["R"]["median"]
result["B_circuit"]={
    "genes":crows,
    "clone_summaries":B_summ,
    "Delta_B_B_minus_R":float(delta_B),
    "leave_one_replicate_out_Delta_B":loo_B,
    "direction_robust_all5":bool(signclass(delta_B)!=0 and all(signclass(v)==signclass(delta_B) for v in loo_B))
}

# Three-clone descriptive ordering only; never promoted as n=3 confirmation.
osc=np.array([dyn["Fig2"][cl]["oscillatory_fraction_ge2"] for cl in CLONES],float)
avec=np.array([A_summ[cl]["median"] for cl in CLONES],float)
bvec=np.array([B_summ[cl]["median"] for cl in CLONES],float)
def order_desc(v):
    sp=float(spearmanr(v,osc).statistic)
    kt=float(kendalltau(v,osc).statistic)
    perms=[]
    for p in itertools.permutations(range(3)):
        perms.append(float(spearmanr(v[list(p)],osc).statistic))
    return {"spearman_rho":sp,"kendall_tau":kt,"all6_label_permutation_spearman":perms,
            "one_sided_negative_exact_fraction":float(sum(x<=sp for x in perms)/len(perms))}
result["three_clone_descriptive"]={"A_vs_oscillatory_fraction":order_desc(avec),"B_vs_oscillatory_fraction":order_desc(bvec)}

a_pos=delta_A>0 and result["A_genomewide"]["direction_robust_all5"]
b_pos=delta_B>0 and result["B_circuit"]["direction_robust_all5"]
a_stable=result["A_genomewide"]["direction_robust_all5"]
b_stable=result["B_circuit"]["direction_robust_all5"]
if not a_stable or not b_stable:
    D="scale_or_representation_instability_no_promotion"
elif a_pos and b_pos:
    D="concordant_global_and_circuit_damping_like_direction"
elif a_pos and not b_pos:
    D="global_or_distributed_signal_without_local_circuit_concordance"
elif (not a_pos) and b_pos:
    D="circuit_localized_signal_diluted_or_absent_genomewide"
else:
    D="joint_non_support_for_historical_damping_like_direction"
result["D_joint"]={
    "classification":D,
    "A_expected_direction_met":bool(delta_A>0),
    "B_expected_direction_met":bool(delta_B>0),
    "A_direction_robust":bool(a_stable),
    "B_direction_robust":bool(b_stable),
    "dynamic_primary_gate_pass":bool(fig2_pass),
    "dynamic_fig1_robustness_pass":bool(fig1_robust),
    "interpretation_ceiling":"exploratory relational evidence only"
}
result["status"]="PASS_ANALYSIS_EXECUTED"
(ROOT/"KIZILIRMAK2023_C_D_RESULT_PIN_V01.json").write_text(json.dumps(result,indent=2),encoding="utf-8")

# Compact reviewer/research audit.
lines=[
"# Kizilirmak 2023 C + D result audit",
"",
f"**Status:** {result['status']}",
"",
"## Native dynamics reproduction gate",
f"- Fig2 oscillatory fraction (>=2 peaks): B={dyn['Fig2']['B']['oscillatory_fraction_ge2']:.6f}, R={dyn['Fig2']['R']['oscillatory_fraction_ge2']:.6f}, G={dyn['Fig2']['G']['oscillatory_fraction_ge2']:.6f}.",
f"- Primary R > B gate: **{fig2_pass}**.",
f"- Fig2 median AUC: B={dyn['Fig2']['B']['auc_median']:.6f}, R={dyn['Fig2']['R']['auc_median']:.6f}; B > R: **{fig2_auc_pass}**.",
f"- Fig1 independent source-data robustness R > B oscillatory fraction: **{fig1_robust}**.",
"",
"## A — genome-wide historical-proxy lane",
f"- Common eligible genes: {result['static_representation']['common_eligible_genes']}.",
f"- Median chi_GRI: B={A_summ['B']['median']:.8g}, R={A_summ['R']['median']:.8g}, G={A_summ['G']['median']:.8g}.",
f"- Delta_A (B-R)={delta_A:.8g}; expected damping-like direction Delta_A>0: **{delta_A>0}**.",
f"- Leave-one-biological-replicate-out deltas: {loo_A}.",
f"- Direction robust across all five omissions: **{result['A_genomewide']['direction_robust_all5']}**.",
"",
"## B — source-defined TNF/NF-kB circuit lane",
f"- Frozen genes: {', '.join(CIRCUIT)}.",
f"- Median circuit chi_GRI: B={B_summ['B']['median']:.8g}, R={B_summ['R']['median']:.8g}, G={B_summ['G']['median']:.8g}.",
f"- Delta_B (B-R)={delta_B:.8g}; expected damping-like direction Delta_B>0: **{delta_B>0}**.",
f"- Leave-one-biological-replicate-out deltas: {loo_B}.",
f"- Direction robust across all five omissions: **{result['B_circuit']['direction_robust_all5']}**.",
"",
"## D — what A and B say together",
f"**{D}**",
"",
"Genes and single cells are not treated as independent system-level replicates. No gene-level or cell-level p-value is promoted as validation of the cross-layer hypothesis. The three-clone rank statistics are descriptive only.",
"",
"## Claim ceiling",
"The result cannot identify mean expression with oscillator frequency, RNA SD with dissipation, chi_GRI with a physical damping ratio, or chi=1 with a biological critical boundary."
]
(ROOT/"KIZILIRMAK2023_C_D_RESULT_AUDIT_V01.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
