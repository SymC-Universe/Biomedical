#!/usr/bin/env python3
from __future__ import annotations

import gzip, hashlib, io, itertools, json, math, pathlib, urllib.request
from datetime import datetime, timezone

import numpy as np
import pandas as pd

ROOT=pathlib.Path(__file__).resolve().parents[2]
BIO=ROOT/"BIO_CHI"
CFG=BIO/"config"/"REHMAN2021_TOPDOWN_ANALYSIS_FREEZE_v0_2.json"
OUTDIR=BIO/"artifacts"/"generated"
OUTDIR.mkdir(parents=True,exist_ok=True)
OUT_JSON=OUTDIR/"rehman2021_topdown_analysis_v0_1.json"
OUT_MD=OUTDIR/"REHMAN2021_TOPDOWN_ANALYSIS_V01_AUDIT.md"
UA="BioChiReviewerReproducibility/0.1"

def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    with urllib.request.urlopen(req,timeout=180) as r:
        return r.read()

def sha(b): return hashlib.sha256(b).hexdigest()

def parse_soft_titles(raw):
    txt=gzip.decompress(raw).decode("utf-8",errors="replace")
    samples={}
    cur=None
    for line in txt.splitlines():
        if line.startswith("^SAMPLE = "):
            cur=line.split("=",1)[1].strip()
            samples[cur]={"title":None,"characteristics":[]}
        elif cur and line.startswith("!Sample_title = "):
            samples[cur]["title"]=line.split("=",1)[1].strip()
        elif cur and line.startswith("!Sample_characteristics_ch1 = "):
            samples[cur]["characteristics"].append(line.split("=",1)[1].strip())
    return samples

def correlation_distance(x,y):
    x=np.asarray(x,float); y=np.asarray(y,float)
    sx=float(np.std(x)); sy=float(np.std(y))
    if sx==0 or sy==0: return float("nan")
    r=float(np.corrcoef(x,y)[0,1])
    return 1.0-r

def exact_perm_stat(a,b,stat_fn):
    vals=np.array(list(a)+list(b),dtype=float)
    n=len(a)
    obs=float(stat_fn(np.array(a),np.array(b)))
    stats=[]
    for inds in itertools.combinations(range(len(vals)),n):
        mask=np.zeros(len(vals),dtype=bool)
        mask[list(inds)]=True
        aa=vals[mask]; bb=vals[~mask]
        stats.append(float(stat_fn(aa,bb)))
    stats=np.array(stats)
    p=float(np.mean(stats>=obs-1e-15))
    return {"observed":obs,"exact_one_sided_p":p,"enumerations":int(len(stats)),"perm_min":float(np.min(stats)),"perm_max":float(np.max(stats))}

def dist_summary(dist,groups):
    return {g:{
        "n":len(groups[g]),
        "values":[float(dist[s]) for s in groups[g]],
        "median":float(np.median([dist[s] for s in groups[g]])),
        "mean":float(np.mean([dist[s] for s in groups[g]]))
    } for g in groups}

def pca_fit(primary_matrix, sample_names, groups, heldout_matrix, heldout_names):
    # primary_matrix shape samples x genes, already z-scaled by primary mean/std
    U,S,Vt=np.linalg.svd(primary_matrix,full_matrices=False)
    denom=max(1,primary_matrix.shape[0]-1)
    ev=(S**2)/denom
    ratio=ev/ev.sum()
    cum=np.cumsum(ratio)
    k=int(np.searchsorted(cum,0.80)+1)
    scores=(U*S)[:,:k]
    components=Vt[:k,:]
    held_scores=heldout_matrix@components.T if heldout_matrix.size else np.empty((0,k))

    idx={s:i for i,s in enumerate(sample_names)}
    gs={}
    for g,names in groups.items():
        arr=np.vstack([scores[idx[s],:] for s in names])
        gs[g]={"centroid":arr.mean(axis=0),"scores":arr}

    c=gs["control"]["centroid"]; d=gs["dtp"]["centroid"]; r=gs["regrowth"]["centroid"]
    v_return=c-d
    v_obs=r-d
    nr=np.linalg.norm(v_return); no=np.linalg.norm(v_obs)
    cosine=float(np.dot(v_return,v_obs)/(nr*no)) if nr>0 and no>0 else None
    per_pc=[]
    for j in range(k):
        den=abs(float(d[j]-c[j]))
        frac=None if den<=1e-12 else float(1.0-abs(float(r[j]-c[j]))/den)
        per_pc.append({
            "pc":j+1,
            "explained_variance_ratio":float(ratio[j]),
            "control_mean":float(c[j]),
            "dtp_mean":float(d[j]),
            "regrowth_mean":float(r[j]),
            "return_fraction":frac
        })

    held={}
    hidx={s:i for i,s in enumerate(heldout_names)}
    if heldout_names:
        harr=np.vstack([held_scores[hidx[s],:] for s in heldout_names])
        hc=harr.mean(axis=0)
        held={
            "centroid":[float(x) for x in hc],
            "distance_to_control":float(np.linalg.norm(hc-c)),
            "distance_to_regrowth":float(np.linalg.norm(hc-r)),
            "distance_to_dtp":float(np.linalg.norm(hc-d)),
            "scores":{s:[float(x) for x in held_scores[hidx[s],:]] for s in heldout_names}
        }

    return {
        "retained_pc_count":k,
        "cumulative_variance_at_k":float(cum[k-1]),
        "explained_variance_ratio":[float(x) for x in ratio[:k]],
        "return_vector_cosine":cosine,
        "per_pc":per_pc,
        "group_centroids":{g:[float(x) for x in v["centroid"]] for g,v in gs.items()},
        "heldout_resistant_projection":held
    }

def run_event(logcpm, cpm, samples, primary_groups, heldout, filter_samples, control_override=None):
    filt_idx=[samples.index(s) for s in filter_samples]
    keep=(cpm[:,filt_idx]>=1.0).sum(axis=1)>=3
    X=logcpm[keep,:]
    genes_kept=int(np.sum(keep))
    groups=dict(primary_groups)
    if control_override is not None:
        groups["control"]=control_override

    cidx=[samples.index(s) for s in groups["control"]]
    centroid=np.mean(X[:,cidx],axis=1)

    corr_dist={}
    for s in sum(groups.values(),[])+heldout:
        corr_dist[s]=correlation_distance(X[:,samples.index(s)],centroid)

    primary_names=sum(primary_groups.values(),[])
    pidx=[samples.index(s) for s in primary_names]
    Xp=X[:,pidx].T
    mu=Xp.mean(axis=0)
    sd=Xp.std(axis=0,ddof=0)
    nz=sd>0
    Zp=(Xp[:,nz]-mu[nz])/sd[nz]

    z_dist={}
    cpos=[primary_names.index(s) for s in primary_groups["control"]]
    zcent=Zp[cpos,:].mean(axis=0)
    for s in primary_names:
        pos=primary_names.index(s)
        z_dist[s]=float(np.linalg.norm(Zp[pos,:]-zcent))
    # heldout z using primary scaling
    held_mat=[]
    for s in heldout:
        xi=X[:,samples.index(s)][nz]
        zi=(xi-mu[nz])/sd[nz]
        z_dist[s]=float(np.linalg.norm(zi-zcent))
        held_mat.append(zi)

    corr_summ=dist_summary(corr_dist,{**groups,"resistant":heldout})
    z_summ=dist_summary(z_dist,{**primary_groups,"resistant":heldout})

    rec_idx_corr=1.0-corr_summ["regrowth"]["median"]/corr_summ["dtp"]["median"]
    rec_idx_z=1.0-z_summ["regrowth"]["median"]/z_summ["dtp"]["median"]

    rec_perm_corr=exact_perm_stat(
        [corr_dist[s] for s in primary_groups["dtp"]],
        [corr_dist[s] for s in primary_groups["regrowth"]],
        lambda a,b: np.median(a)-np.median(b)
    )
    rec_perm_z=exact_perm_stat(
        [z_dist[s] for s in primary_groups["dtp"]],
        [z_dist[s] for s in primary_groups["regrowth"]],
        lambda a,b: np.median(a)-np.median(b)
    )
    bnd_perm_corr=exact_perm_stat(
        [corr_dist[s] for s in heldout],
        [corr_dist[s] for s in primary_groups["regrowth"]],
        lambda a,b: np.median(a)-np.median(b)
    )
    bnd_perm_z=exact_perm_stat(
        [z_dist[s] for s in heldout],
        [z_dist[s] for s in primary_groups["regrowth"]],
        lambda a,b: np.median(a)-np.median(b)
    )

    held_z=np.vstack(held_mat) if held_mat else np.empty((0,Zp.shape[1]))
    modal=pca_fit(Zp,primary_names,primary_groups,held_z,heldout)

    return {
        "genes_kept":genes_kept,
        "primary_correlation_distance":{
            "summary":corr_summ,
            "recovery_index":float(rec_idx_corr),
            "recovery_exact_test":rec_perm_corr,
            "heldout_boundary_exact_test":bnd_perm_corr
        },
        "z_euclidean_sensitivity":{
            "summary":z_summ,
            "recovery_index":float(rec_idx_z),
            "recovery_exact_test":rec_perm_z,
            "heldout_boundary_exact_test":bnd_perm_z,
            "genes_after_zero_variance_removal":int(np.sum(nz))
        },
        "modal":modal
    }

def main():
    cfg=json.loads(CFG.read_text())
    cb=fetch(cfg["source"]["counts_url"])
    sb=fetch(cfg["source"]["soft_url"])
    if sha(cb)!=cfg["source"]["counts_sha256"]: raise SystemExit("count source SHA mismatch")
    if sha(sb)!=cfg["source"]["soft_sha256"]: raise SystemExit("SOFT source SHA mismatch")

    soft=parse_soft_titles(sb)
    title_to_acc={rec["title"]:acc for acc,rec in soft.items() if rec["title"]}

    df=pd.read_csv(io.BytesIO(gzip.decompress(cb)),sep="\t",dtype={0:str,1:str,2:str})
    meta_cols=list(df.columns[:3])
    count_cols=list(df.columns[3:])
    acc_cols={}
    for col in count_cols:
        if col in title_to_acc: acc_cols[title_to_acc[col]]=col
        elif col in soft: acc_cols[col]=col
        else:
            hits=[acc for acc,rec in soft.items() if rec["title"] and (col==rec["title"] or col.startswith(rec["title"]+"_") or rec["title"].startswith(col+"_"))]
            if len(set(hits))==1: acc_cols[hits[0]]=col
    required=set(sum(cfg["primary_groups"].values(),[])+cfg["heldout_boundary_group"]+cfg["control_sensitivity_additional"])
    missing=sorted(required-set(acc_cols))
    if missing: raise SystemExit("missing required columns: "+repr(missing))

    # Exclude HTSeq technical summary rows if present; use Ensembl ID as stable gene row identity.
    ens=df[meta_cols[0]].astype(str)
    gene_mask=~ens.str.startswith("__")
    dfg=df.loc[gene_mask,:].copy()

    ordered_samples=sorted(required)
    counts=dfg[[acc_cols[s] for s in ordered_samples]].apply(pd.to_numeric,errors="raise").to_numpy(dtype=float)
    if np.any(counts<0) or not np.all(np.isfinite(counts)): raise SystemExit("invalid counts")
    lib=counts.sum(axis=0)
    if np.any(lib<=0): raise SystemExit("zero library size")
    cpm=counts/lib[None,:]*1e6
    logcpm=np.log2(cpm+1.0)

    primary_groups={k:list(v) for k,v in cfg["primary_groups"].items()}
    held=list(cfg["heldout_boundary_group"])
    primary_filter_samples=sum(primary_groups.values(),[])

    # matrices currently ordered by ordered_samples; run_event expects samples list matching columns
    primary=run_event(logcpm,cpm,ordered_samples,primary_groups,held,primary_filter_samples)

    sensitivity_controls=primary_groups["control"]+list(cfg["control_sensitivity_additional"])
    control_sensitivity=run_event(logcpm,cpm,ordered_samples,primary_groups,held,primary_filter_samples,control_override=sensitivity_controls)

    result={
      "schema_version":"0.1",
      "generated_at_utc":datetime.now(timezone.utc).isoformat(),
      "gate":"Rehman 2021 top-down whole-event + derived modal analysis",
      "status":"PASS_ANALYSIS_EXECUTED",
      "source":{
        "counts_sha256":sha(cb),"soft_sha256":sha(sb),
        "gene_rows_before_filter":int(dfg.shape[0]),
        "sample_columns_used":ordered_samples
      },
      "primary":primary,
      "control_sensitivity":control_sensitivity,
      "dispositions":{
        "biochi_event_identifiable":True,
        "biochi_relation_testable":True,
        "heldout_boundary_testable":True,
        "scalar_opened":False,
        "scalar_disposition":"SCALAR_NOT_REQUIRED_AND_NOT_LICENSED_FROM_STATIC_PCA"
      },
      "claim_ceiling":"P0-Q top-down event and representation analysis; not exact reproduction of Rehman Figure 4 PCA and not P1 confirmation"
    }
    OUT_JSON.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")

    pc=primary["primary_correlation_distance"]
    ze=primary["z_euclidean_sensitivity"]
    modal=primary["modal"]
    lines=[
      "# Rehman 2021 top-down Bio Chi analysis v0.1","",
      f"**Status:** {result['status']}",
      f"**Filtered genes:** {primary['genes_kept']}",
      "",
      "## Whole-event geometry","",
      "| Metric | DTP median | Regrowth median | Resistant median | Recovery index | Recovery exact p | Resistant>regrowth exact p |",
      "|---|---:|---:|---:|---:|---:|---:|",
      f"| 1-Pearson to control centroid | {pc['summary']['dtp']['median']:.8g} | {pc['summary']['regrowth']['median']:.8g} | {pc['summary']['resistant']['median']:.8g} | {pc['recovery_index']:.8g} | {pc['recovery_exact_test']['exact_one_sided_p']:.8g} | {pc['heldout_boundary_exact_test']['exact_one_sided_p']:.8g} |",
      f"| z-Euclidean sensitivity | {ze['summary']['dtp']['median']:.8g} | {ze['summary']['regrowth']['median']:.8g} | {ze['summary']['resistant']['median']:.8g} | {ze['recovery_index']:.8g} | {ze['recovery_exact_test']['exact_one_sided_p']:.8g} | {ze['heldout_boundary_exact_test']['exact_one_sided_p']:.8g} |",
      "",
      "## Derived modal representation","",
      f"- retained PCs to >=80% variance: {modal['retained_pc_count']}",
      f"- cumulative variance: {modal['cumulative_variance_at_k']:.8g}",
      f"- DTP-to-regrowth versus DTP-to-control return-vector cosine: {modal['return_vector_cosine']}",
      "",
      "## Scalar gate","",
      "No scalar was opened. This branch has no source-native dynamical generator, and static PCA alone does not license the program scalar constructor.",
      "",
      "## Ceiling","",
      "P0-Q only. This is a prospectively frozen replacement analysis of the public counts, not an exact reproduction of the source paper's under-specified PCA pipeline."
    ]
    OUT_MD.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":result["status"],
      "primary":{
        "genes_kept":primary["genes_kept"],
        "correlation_distance":pc,
        "z_euclidean":ze,
        "modal":{
          "retained_pc_count":modal["retained_pc_count"],
          "cumulative_variance_at_k":modal["cumulative_variance_at_k"],
          "return_vector_cosine":modal["return_vector_cosine"],
          "per_pc":modal["per_pc"],
          "heldout_resistant_projection":modal["heldout_resistant_projection"]
        }
      },
      "control_sensitivity":{
        "correlation_distance":control_sensitivity["primary_correlation_distance"],
        "z_euclidean":control_sensitivity["z_euclidean_sensitivity"]
      }
    },indent=2))
    print("BIO_CHI_REHMAN_TOPDOWN_ANALYSIS_DONE")

if __name__=="__main__":
    main()
