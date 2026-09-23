#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import numpy as np
import pandas as pd

from src import run_biosystems_adversarial_r1_h1_composition as base

NS="GRI_BIOSYS_R1_H1_COMP_TSS_20260923"
N=30
DRAWS=20
MIN_TSS_N=3
MIN_RESID_DF=10
DATA={}

def tss(pid):
    p=str(pid).split("-")
    if len(p)<3 or not p[1]:
        raise ValueError(f"invalid TCGA participant for TSS {pid}")
    return p[1]

def spectrum_metrics(b):
    x=np.asarray(b,float)
    x=x-x.mean(0,keepdims=True)
    g=(x@x.T)/float(x.shape[1])
    vals=np.linalg.eigvalsh(g)[::-1]
    scale=float(np.sum(np.abs(vals)));tol=1e-10*scale if scale>0 else 0
    if np.any(vals < -tol): raise ValueError("negative modal eigenvalue")
    vals=np.where(vals<0,0,vals)[:x.shape[0]-1]
    tot=float(vals.sum())
    if not np.isfinite(tot) or tot<=0:return np.nan,np.nan
    q=vals/tot;nz=q>0
    h=float(-np.sum(q[nz]*np.log(q[nz])))
    s=float(1-h/math.log(x.shape[0]-1))
    pc1=float(vals[0]/tot)
    return s,pc1

def design_matrix(purity,leuk,tss_values):
    purity=np.asarray(purity,float);leuk=np.asarray(leuk,float)
    zp=(purity-purity.mean())/purity.std(ddof=1)
    zl=(leuk-leuk.mean())/leuk.std(ddof=1)
    counts=pd.Series(tss_values).value_counts().to_dict()
    cats=[v if counts[v]>=MIN_TSS_N else "RARE_TSS" for v in tss_values]
    levels=sorted(set(cats))
    cols=[np.ones(len(cats)),zp,zl]
    # deterministic reference = lexicographically first
    for lev in levels[1:]:
        cols.append(np.asarray([1.0 if z==lev else 0.0 for z in cats]))
    X=np.column_stack(cols)
    return X,cats,levels

def draw_one(cancer,draw):
    pool=np.asarray(DATA["rows"][cancer],int)
    sel=np.sort(np.random.default_rng(base.stable_seed(NS,cancer,draw,"participants")).choice(pool,size=N,replace=False))
    b=np.asarray(DATA["beta"][sel,:],float).copy()
    fin=np.isfinite(b);retain=fin.sum(0)>=29
    if int(retain.sum())<20000:
        return {"cancer":cancer,"draw":draw,"status":"NOT_EVALUABLE_PROBE_SUPPORT"},sel
    b=b[:,retain]
    bad=~np.isfinite(b)
    if bad.any():
        med=np.nanmedian(b,0)
        if not np.isfinite(med).all():raise ValueError("nonfinite retained median")
        b[bad]=np.broadcast_to(med,b.shape)[bad]

    purity=np.asarray(DATA["purity"][sel],float)
    leuk=np.asarray(DATA["leuk"][sel],float)
    tv=[DATA["tss"][i] for i in sel]
    X,cats,levels=design_matrix(purity,leuk,tv)
    rank=int(np.linalg.matrix_rank(X));rdf=N-rank
    if rank!=X.shape[1] or rdf<MIN_RESID_DF:
        return {
            "cancer":cancer,"draw":draw,"status":"NOT_EVALUABLE_TSS_DESIGN",
            "design_columns":int(X.shape[1]),"rank":rank,"residual_df":rdf,
            "tss_levels":len(levels)
        },sel
    coef=np.linalg.lstsq(X,b,rcond=None)[0]
    fitted=X@coef
    resid=b-fitted
    null=fitted+base.perm_cols(resid,base.stable_seed(NS,cancer,draw,"comp_tss_null"))

    sraw,praw=spectrum_metrics(b)
    snull,pnull=spectrum_metrics(null)
    return {
      "cancer":cancer,"draw":draw,"status":"EVALUABLE",
      "retained_probes":int(retain.sum()),
      "design_columns":int(X.shape[1]),"rank":rank,"residual_df":rdf,
      "tss_raw_levels":len(set(tv)),"tss_modeled_levels":len(levels),
      "tss_modeled_counts_json":json.dumps(pd.Series(cats).value_counts().sort_index().to_dict(),sort_keys=True),
      "s_raw":sraw,"s_comp_tss_null":snull,"delta_comp_tss_preserved":sraw-snull,
      "pc1_raw":praw,"pc1_comp_tss_null":pnull,"delta_pc1_comp_tss":praw-pnull,
    },sel

def one_cancer(c):
    rr=[];mm=[]
    for d in range(DRAWS):
        r,sel=draw_one(c,d);rr.append(r)
        mm.append({"cancer":c,"draw":d,"participants":"|".join(DATA["participants"][i] for i in sel)})
    return rr,mm

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--meth",required=True)
    ap.add_argument("--annotation",required=True)
    ap.add_argument("--purity",required=True)
    ap.add_argument("--leuk",required=True)
    ap.add_argument("--rna-header",required=True)
    ap.add_argument("--c1-probes",required=True)
    ap.add_argument("--out",required=True,type=Path)
    ap.add_argument("--workers",type=int,default=4)
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)

    for path,expected,label in [(a.meth,base.METH_SHA,"methylation"),(a.purity,base.PURITY_SHA,"purity"),(a.leuk,base.LEUK_SHA,"leukocyte")]:
        got=base.sha256_file(path)
        if got!=expected:raise ValueError(f"{label} SHA mismatch {got}")

    ann=base.read_annotation(a.annotation)
    meth_unique,_=base.header_primary_unique_from_line(base.first_line(a.meth),ann)
    rna_unique,_=base.header_primary_unique_from_line(base.first_line(a.rna_header),ann)
    purity=base.read_purity(a.purity);leuk=base.read_leuk(a.leuk)

    pool_by=defaultdict(list);records=[]
    for cancer in base.CANCERS:
        pids=sorted(pid for (c,pid) in set(meth_unique)&set(rna_unique)
                    if c==cancer and pid in purity and pid in leuk and leuk[pid][0]==cancer)
        for pid in pids:
            records.append({
              "cancer":cancer,"participant":pid,"meth_pos":meth_unique[(cancer,pid)]["pos"],
              "purity":purity[pid],"leuk":leuk[pid][1],"tss":tss(pid)
            })
        pool_by[cancer]=pids
    eligible=sorted(c for c in base.CANCERS if len(pool_by[c])>=N)
    if eligible!=base.EXPECTED_ELIGIBLE:
        raise ValueError(f"eligibility drift {eligible}")

    idx={(r["cancer"],r["participant"]):i for i,r in enumerate(records)}
    rows={c:[idx[(c,p)] for p in pool_by[c]] for c in eligible}
    beta,_=base.load_methylation(a.meth,records,a.c1_probes)
    DATA.update(
      beta=beta,rows=rows,
      participants=[r["participant"] for r in records],
      purity=np.asarray([r["purity"] for r in records],float),
      leuk=np.asarray([r["leuk"] for r in records],float),
      tss=[r["tss"] for r in records],
    )

    allrows=[];members=[]
    with ThreadPoolExecutor(max_workers=max(1,min(a.workers,len(eligible)))) as ex:
        fut={ex.submit(one_cancer,c):c for c in eligible}
        for f in as_completed(fut):
            c=fut[f];rr,mm=f.result();allrows.extend(rr);members.extend(mm);print("completed",c,flush=True)
    df=pd.DataFrame(allrows).sort_values(["cancer","draw"])
    df.to_csv(a.out/"R1_H1_TSS_DRAW_METRICS.csv.gz",index=False,compression={"method":"gzip","mtime":0})
    pd.DataFrame(members).sort_values(["cancer","draw"]).to_csv(a.out/"R1_H1_TSS_MEMBERSHIP.csv.gz",index=False,compression={"method":"gzip","mtime":0})
    ev=df[df.status.eq("EVALUABLE")].copy()
    sums=[]
    for c,g in ev.groupby("cancer",sort=True):
        row={"cancer":c,"evaluable_draws":len(g),"pool_n":len(rows[c])}
        for col in ["delta_comp_tss_preserved","delta_pc1_comp_tss","residual_df","tss_modeled_levels"]:
            v=pd.to_numeric(g[col],errors="coerce").to_numpy(float);v=v[np.isfinite(v)]
            row[col+"_median"]=float(np.median(v)) if len(v) else np.nan
            row[col+"_q25"]=float(np.quantile(v,.25)) if len(v) else np.nan
            row[col+"_q75"]=float(np.quantile(v,.75)) if len(v) else np.nan
        sums.append(row)
    cs=pd.DataFrame(sums);cs.to_csv(a.out/"R1_H1_TSS_CANCER_SUMMARY.csv",index=False)
    vals=cs.delta_comp_tss_preserved_median.to_numpy(float)
    pos,neg,ties,p=base.sign_two(vals)
    pvals=cs.delta_pc1_comp_tss_median.to_numpy(float)
    ppos,pneg,pties,pp=base.sign_two(pvals)
    if len(vals)<20:
        disp="R1_H1_COMP_TSS_HOLD"
    elif float(np.median(vals))>0 and p<.05:
        disp="R1_H1_COMP_TSS_ROBUST"
    else:
        disp="R1_H1_COMP_TSS_SENSITIVE"
    summary={
      "schema":"biosystems-adversarial-r1-h1-tss-v1",
      "status":"COMPLETE","role":"POST_RESULT_P0_Q_ADVERSARIAL_SENSITIVITY",
      "disposition":disp,
      "cancers_evaluable":len(vals),"positive":pos,"negative":neg,"ties":ties,
      "h1_median":float(np.median(vals)) if len(vals) else None,
      "h1_q25":float(np.quantile(vals,.25)) if len(vals) else None,
      "h1_q75":float(np.quantile(vals,.75)) if len(vals) else None,
      "h1_sign_p_two_sided":p,
      "pca_pc1_positive":ppos,"pca_pc1_negative":pneg,"pca_pc1_ties":pties,
      "pca_pc1_median_delta":float(np.median(pvals)) if len(pvals) else None,
      "pca_pc1_sign_p_two_sided":pp,
      "n_per_draw":N,"draws_per_cancer":DRAWS,"min_tss_n":MIN_TSS_N,"min_residual_df":MIN_RESID_DF,
      "claim_ceiling":"preserves linear purity/leukocyte effects and TSS-associated CpG mean shifts only; not full batch/composition independence"
    }
    (a.out/"R1_H1_TSS_GLOBAL_SUMMARY.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
    print(json.dumps(summary,indent=2,sort_keys=True))

if __name__=="__main__":main()
