#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,gzip,hashlib,json,math
from pathlib import Path
import numpy as np
import pandas as pd

C1_SHA="589365b92797f6e0ea479b75437c44ed86327cfc86b3e7caf7df01b4be2bcdd9"
SOURCE_SHA="90a7a8c12343831524a9711be7e0b3f33f297fe408662fa68c5efa49a7c862d0"

def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()

def resolve(header,p,state):
    marker="_T_" if state=="TUMOR" else "_NT_"
    hits=[h for h in header if p in str(h) and marker in str(h)]
    if len(hits)!=1: raise SystemExit(f"HEADER_RESOLUTION_FAIL {p} {state} {hits}")
    return hits[0]

def read_matrix(path,probe_order,participants):
    with gzip.open(path,"rt",encoding="utf-8",newline="") as f:
        header=next(csv.reader(f,delimiter="\t"))
    th=[resolve(header,p,"TUMOR") for p in participants]
    nh=[resolve(header,p,"NORMAL") for p in participants]
    wanted=th+nh; pos={h:header.index(h) for h in wanted}; target=set(probe_order)
    rows={}; offset=None
    with gzip.open(path,"rt",encoding="utf-8",newline="") as f:
        next(f)
        for line in f:
            parts=line.rstrip("\r\n").split("\t")
            if not parts:continue
            pid=parts[0].strip().strip('"')
            if pid not in target:continue
            if offset is None:
                if len(parts)==len(header)+1:offset=1
                elif len(parts)==len(header):offset=0
                else:raise SystemExit("ROW_WIDTH_DRIFT")
            vals=[]
            for h in wanted:
                raw=parts[pos[h]+offset].strip().strip('"')
                try:vals.append(float(raw))
                except:vals.append(np.nan)
            rows[pid]=vals
    keep=[p for p in probe_order if p in rows]
    if len(keep)<20000:raise SystemExit(f"LOW_C1_OVERLAP {len(keep)}")
    x=np.asarray([rows[p] for p in keep],float).T
    n=len(participants)
    return np.asarray(keep,object),x[:n],x[n:]

def binom_tail(k,n):
    return float(sum(math.comb(n,j) for j in range(k,n+1))/(2**n))

def auc(scores,labels):
    s=np.asarray(scores,float); y=np.asarray(labels,int)
    ranks=pd.Series(s).rank(method="average").to_numpy(float)
    n1=int(y.sum()); n0=len(y)-n1
    return float((ranks[y==1].sum()-n1*(n1+1)/2)/(n1*n0))

def fit_pc1(train):
    # train is samples x features, already standardized
    gram=train@train.T
    vals,vecs=np.linalg.eigh(gram)
    u=vecs[:,-1]; sv=math.sqrt(max(float(vals[-1]),0))
    if sv<=0:raise SystemExit("PC1_ZERO_SINGULAR")
    load=(train.T@u)/sv
    load=load/np.linalg.norm(load)
    return load

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--matrix",type=Path,required=True)
    ap.add_argument("--config",type=Path,required=True)
    ap.add_argument("--c1-probes",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    if sha(a.matrix)!=SOURCE_SHA:raise SystemExit("SOURCE_SHA_MISMATCH")
    if sha(a.c1_probes)!=C1_SHA:raise SystemExit("C1_SHA_MISMATCH")
    cfg=json.loads(a.config.read_text())
    participants=cfg["primary_450k"]["complete_pair_pool"]
    probes=[x.strip() for x in a.c1_probes.read_text().splitlines() if x.strip()]
    pids,tum,norm=read_matrix(a.matrix,probes,participants)
    n=len(participants)
    rows=[]
    pc_correct=0; mean_correct=0; oof_scores=[];oof_labels=[]
    for hold in range(n):
        tr=[i for i in range(n) if i!=hold]
        T=tum[tr];N=norm[tr]
        ft=np.isfinite(T).mean(0)>=0.95;fn=np.isfinite(N).mean(0)>=0.95; keep=ft&fn
        if int(keep.sum())<15000:raise SystemExit(f"LOW_TRAIN_FEATURES fold={hold} n={int(keep.sum())}")
        train=np.vstack([T[:,keep],N[:,keep]])
        med=np.nanmedian(train,axis=0)
        bad=~np.isfinite(train)
        if bad.any():train[bad]=np.broadcast_to(med,train.shape)[bad]
        mu=train.mean(0);sd=train.std(0,ddof=1)
        good=np.isfinite(sd)&(sd>0)
        train=(train[:,good]-mu[good])/sd[good]
        load=fit_pc1(train)
        train_scores=train@load
        # first 31 are tumors
        sign=1.0 if train_scores[:n-1].mean()>train_scores[n-1:].mean() else -1.0
        load*=sign;train_scores*=sign
        # project heldout, using training medians/scaling
        raw_t=tum[hold,keep].copy(); raw_n=norm[hold,keep].copy()
        raw_t=np.where(np.isfinite(raw_t),raw_t,med)
        raw_n=np.where(np.isfinite(raw_n),raw_n,med)
        zt=(raw_t[good]-mu[good])/sd[good];zn=(raw_n[good]-mu[good])/sd[good]
        st=float(zt@load);sn=float(zn@load)
        pcok=st>sn;pc_correct+=int(pcok)
        # global mean beta comparator over same pre-SD-gate training eligible probes
        ttrain=np.nanmean(T[:,keep]);ntrain=np.nanmean(N[:,keep])
        msign=1.0 if ttrain>ntrain else -1.0
        mt=float(np.nanmean(raw_t))*msign;mn=float(np.nanmean(raw_n))*msign
        mok=mt>mn;mean_correct+=int(mok)
        # standardize oof scores by training score distribution for descriptive AUC
        smu=float(train_scores.mean());ssd=float(train_scores.std(ddof=1))
        oof_scores.extend([(st-smu)/ssd,(sn-smu)/ssd]);oof_labels.extend([1,0])
        rows.append({"participant":participants[hold],"fold":hold+1,"features":int(good.sum()),
                     "pc1_tumor":st,"pc1_normal":sn,"pc1_correct":pcok,
                     "mean_tumor":mt,"mean_normal":mn,"mean_correct":mok})
    pd.DataFrame(rows).to_csv(a.out/"PROSTATE_DIAGNOSTIC_LOPO_V01.csv",index=False)
    k=pc_correct; km=mean_correct
    # paired discordance exact one-sided: PC correct when mean wrong vs reverse
    a_only=sum(r["pc1_correct"] and not r["mean_correct"] for r in rows)
    b_only=sum(r["mean_correct"] and not r["pc1_correct"] for r in rows)
    d=a_only+b_only
    adds_p=binom_tail(a_only,d) if d else 1.0
    result={
      "schema_version":"0.1","status":"COMPLETE_P0D",
      "source_sha256":sha(a.matrix),"n_pairs":n,"common_c1_probes":int(len(pids)),
      "pc1_concordant_pairs":k,"pc1_one_sided_binomial_p":binom_tail(k,n),
      "pc1_descriptive_oof_auc":auc(oof_scores,oof_labels),
      "global_mean_concordant_pairs":km,"global_mean_one_sided_binomial_p":binom_tail(km,n),
      "pc1_only_correct_pairs":a_only,"mean_only_correct_pairs":b_only,
      "pc1_vs_mean_discordance_one_sided_p":adds_p,
      "primary_support":bool(k>16 and binom_tail(k,n)<=0.05),
      "adds_over_global_mean":bool(a_only>b_only and adds_p<=0.05),
      "claim_ceiling":"exploratory external tissue-state discrimination; not clinical diagnostic utility, not deployable biomarker, not H1 patient-level score"
    }
    (a.out/"PROSTATE_DIAGNOSTIC_LOPO_RESULT_V01.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=="__main__":main()
