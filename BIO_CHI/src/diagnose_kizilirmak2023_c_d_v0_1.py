#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, urllib.request
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT=Path("BIO_CHI/artifacts/generated/kizilirmak2023_c_d_diagnostic_v01")
ROOT.mkdir(parents=True,exist_ok=True)
URL="https://ars.els-cdn.com/content/image/1-s2.0-S2589004223026500-mmc3.xls"
SHA="f76c8eaf685d192f2340d178aac62f8263004077276d3e64f96ba41faab408f4"
CLONES=["B","R","G"]
CIRCUIT=["Tnfrsf1a","Rela","Nfkbia","Tnfaip3"]

def get(url):
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 GRI-BioChi-diagnostic/0.1"})
    with urllib.request.urlopen(req,timeout=120) as r:
        return r.read()

def sha(b): return hashlib.sha256(b).hexdigest()

def calc(df, cols):
    x=df[cols].apply(pd.to_numeric,errors="coerce").to_numpy(float)
    finite=np.all(np.isfinite(x),axis=1)
    mu=np.mean(x,axis=1)
    sd=np.std(x,axis=1,ddof=1)
    eligible=finite & np.isfinite(mu) & np.isfinite(sd) & (mu>0)
    chi=np.full(len(df),np.nan)
    chi[eligible]=sd[eligible]/(2*mu[eligible])
    return mu,sd,chi,eligible

b=get(URL)
if sha(b)!=SHA: raise RuntimeError("Table S3 SHA mismatch")
(ROOT/"mmc3.xls").write_bytes(b)
df=pd.read_excel(ROOT/"mmc3.xls",sheet_name="Sheet1",engine="xlrd")
df.columns=[str(c).strip() for c in df.columns]
df["GeneID"]=df["GeneID"].astype(str).str.strip()
cols={cl:[f"s{i}_clone_{cl}_ut" for i in range(1,6)] for cl in CLONES}
mu={};sd={};chi={};el={}
for cl in CLONES:
    mu[cl],sd[cl],chi[cl],el[cl]=calc(df,cols[cl])
common=el["B"]&el["R"]&el["G"]

out={"schema_version":"0.1","status":"PASS","evidence_tier":"post-result diagnostic / promotion debt active"}

# A ratio decomposition.
positive=common&(chi["B"]>0)&(chi["R"]>0)&(sd["B"]>0)&(sd["R"]>0)
log_sd=np.log(sd["B"][positive]/sd["R"][positive])
log_mu=np.log(mu["B"][positive]/mu["R"][positive])
log_chi=np.log(chi["B"][positive]/chi["R"][positive])
out["A_decomposition"]={
 "n_positive_ratio":int(np.sum(positive)),
 "median_log_sd_ratio_B_over_R":float(np.median(log_sd)),
 "median_log_mu_ratio_B_over_R":float(np.median(log_mu)),
 "median_log_chi_ratio_B_over_R":float(np.median(log_chi)),
 "fraction_sd_B_gt_R":float(np.mean(sd["B"][common]>sd["R"][common])),
 "fraction_mu_B_gt_R":float(np.mean(mu["B"][common]>mu["R"][common])),
 "fraction_chi_B_gt_R":float(np.mean(chi["B"][common]>chi["R"][common]))
}

# Mean dependence.
mean_dep={}
for cl in ["B","R","G"]:
    m=common&np.isfinite(chi[cl])
    mean_dep[cl]={
      "spearman_chi_vs_mu":float(spearmanr(chi[cl][m],mu[cl][m]).statistic),
      "spearman_sd_vs_mu":float(spearmanr(sd[cl][m],mu[cl][m]).statistic)
    }
out["mean_dependence"]=mean_dep

# Expression-stratified map based on pooled B/R transformed mean.
pool=(mu["B"]+mu["R"])/2
ids=np.flatnonzero(common)
q=pd.qcut(pool[common],10,labels=False,duplicates="drop")
deciles=[]
for k in sorted(np.unique(q)):
    ix=ids[np.asarray(q)==k]
    deciles.append({
      "decile":int(k)+1,
      "n":int(len(ix)),
      "pooled_mean_min":float(np.min(pool[ix])),
      "pooled_mean_max":float(np.max(pool[ix])),
      "median_chi_B":float(np.median(chi["B"][ix])),
      "median_chi_R":float(np.median(chi["R"][ix])),
      "Delta_A":float(np.median(chi["B"][ix])-np.median(chi["R"][ix]))
    })
out["expression_deciles"]=deciles

# Lower-mean threshold stress using pooled-mean percentiles.
stress=[]
for pct in [0,10,25,50]:
    threshold=float(np.percentile(pool[common],pct))
    m=common&(pool>=threshold)
    stress.append({
      "lower_percentile":pct,
      "threshold":threshold,
      "n":int(np.sum(m)),
      "Delta_A":float(np.median(chi["B"][m])-np.median(chi["R"][m]))
    })
out["lower_mean_stress"]=stress

neg_dec=sum(d["Delta_A"]<0 for d in deciles)
neg_stress=sum(d["Delta_A"]<0 for d in stress)
strong_mean=(abs(mean_dep["B"]["spearman_chi_vs_mu"])>=0.5 and abs(mean_dep["R"]["spearman_chi_vs_mu"])>=0.5)
if neg_dec>=3 or neg_stress>=1:
    aclass="A_MEAN_SCALE_FRAGILE"
elif strong_mean:
    aclass="A_DIRECTION_ROBUST_BUT_MEAN_DEPENDENT"
else:
    aclass="A_DIRECTION_ROBUST_WITHOUT_STRONG_MEAN_DEPENDENCE"
out["A_diagnostic_classification"]={
  "classification":aclass,
  "negative_deciles":int(neg_dec),
  "negative_threshold_stresses":int(neg_stress),
  "strong_mean_dependence":bool(strong_mean)
}

# Circuit component and replicate diagnostics.
index={g:int(np.flatnonzero(df["GeneID"].to_numpy()==g)[0]) for g in CIRCUIT}
gene_diag=[]
for g in CIRCUIT:
    ix=index[g]
    rec={
      "GeneID":g,
      "mu_B":float(mu["B"][ix]),"mu_R":float(mu["R"][ix]),
      "sd_B":float(sd["B"][ix]),"sd_R":float(sd["R"][ix]),
      "chi_B":float(chi["B"][ix]),"chi_R":float(chi["R"][ix]),
      "Delta_chi_B_minus_R":float(chi["B"][ix]-chi["R"][ix]),
      "leave_one_replicate_out_Delta":[]
    }
    for drop in range(5):
        cb=[c for i,c in enumerate(cols["B"]) if i!=drop]
        cr=[c for i,c in enumerate(cols["R"]) if i!=drop]
        mb,sdb,chb,elb=calc(df.loc[[ix]].copy(),cb)
        mr,sdr,chr_,elr=calc(df.loc[[ix]].copy(),cr)
        rec["leave_one_replicate_out_Delta"].append(float(chb[0]-chr_[0]))
    gene_diag.append(rec)
out["B_gene_diagnostics"]=gene_diag

full_B=np.array([chi["B"][index[g]] for g in CIRCUIT],float)
full_R=np.array([chi["R"][index[g]] for g in CIRCUIT],float)
full_delta=float(np.median(full_B)-np.median(full_R))
loge=[]
for leave in CIRCUIT:
    keep=[g for g in CIRCUIT if g!=leave]
    bv=np.array([chi["B"][index[g]] for g in keep],float)
    rv=np.array([chi["R"][index[g]] for g in keep],float)
    loge.append({"left_out_gene":leave,"Delta_B":float(np.median(bv)-np.median(rv))})
pos=sum(g["Delta_chi_B_minus_R"]>0 for g in gene_diag)
neg=sum(g["Delta_chi_B_minus_R"]<0 for g in gene_diag)
subset_flip=any(np.sign(x["Delta_B"])!=np.sign(full_delta) for x in loge if x["Delta_B"]!=0)
out["B_component_summary"]={
  "full_Delta_B":full_delta,
  "genes_positive_direction":int(pos),
  "genes_negative_direction":int(neg),
  "leave_one_gene_out":loge,
  "leave_one_gene_out_sign_flip":bool(subset_flip),
  "classification":"B_COMPONENT_HETEROGENEITY" if ((pos>0 and neg>0) or subset_flip) else "B_COMPONENT_DIRECTION_COHERENT"
}

out["parent_D_disposition"]="scale_or_representation_instability_no_promotion"
out["interpretive_note"]="Diagnostics do not alter the frozen parent result. Source-reported NF-kB mechanism uses abundance/ratio control, including induced IkBa feedback, not transcript CV as the mechanistic damping variable."
(ROOT/"KIZILIRMAK2023_C_D_DIAGNOSTIC_V01.json").write_text(json.dumps(out,indent=2),encoding="utf-8")

lines=[
"# Kizilirmak C+D post-result diagnostic v0.1","",
f"**A diagnostic:** {out['A_diagnostic_classification']['classification']}",
f"**B diagnostic:** {out['B_component_summary']['classification']}","",
"## A decomposition",
f"- Median log SD ratio B/R: {out['A_decomposition']['median_log_sd_ratio_B_over_R']:.6g}",
f"- Median log mean ratio B/R: {out['A_decomposition']['median_log_mu_ratio_B_over_R']:.6g}",
f"- Median log chi ratio B/R: {out['A_decomposition']['median_log_chi_ratio_B_over_R']:.6g}",
f"- Fraction genes SD_B>SD_R: {out['A_decomposition']['fraction_sd_B_gt_R']:.4f}",
f"- Fraction genes mean_B>mean_R: {out['A_decomposition']['fraction_mu_B_gt_R']:.4f}",
f"- Fraction genes chi_B>chi_R: {out['A_decomposition']['fraction_chi_B_gt_R']:.4f}","",
"## Mean dependence"
]
for cl,v in mean_dep.items():
    lines.append(f"- {cl}: rho(chi,mean)={v['spearman_chi_vs_mu']:.4f}; rho(SD,mean)={v['spearman_sd_vs_mu']:.4f}")
lines += ["","## Expression deciles"]
for d in deciles:
    lines.append(f"- D{d['decile']}: n={d['n']}, Delta_A={d['Delta_A']:.8g}")
lines += ["","## Lower-mean stress"]
for d in stress:
    lines.append(f"- >= pooled-mean P{d['lower_percentile']}: n={d['n']}, Delta_A={d['Delta_A']:.8g}")
lines += ["","## B component diagnostics"]
for g in gene_diag:
    lines.append(f"- {g['GeneID']}: Delta_chi(B-R)={g['Delta_chi_B_minus_R']:.8g}; LOO={g['leave_one_replicate_out_Delta']}")
for x in loge:
    lines.append(f"- Leave out {x['left_out_gene']}: circuit Delta_B={x['Delta_B']:.8g}")
lines += ["","## Disposition","Parent D remains **scale_or_representation_instability_no_promotion**. These are failure/root-cause diagnostics only."]
(ROOT/"KIZILIRMAK2023_C_D_DIAGNOSTIC_AUDIT_V01.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
