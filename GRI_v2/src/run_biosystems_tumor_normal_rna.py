#!/usr/bin/env python3
from __future__ import annotations

import argparse, csv, hashlib, json, math, os, re
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd

from src.module_network_accel import compute_module_metrics_accelerated

EXPECTED_RNA_SHA256 = "674b19b7ed9ae4c5ef35ee2824936429aa5d46c0735a3d180f41552fcbbdb658"
EXPECTED_GMT_SHA256 = "eecaf6dad908334ae885406ec72bdc0646d8917588ed7c219fac92fc5363f596"
FIXED_N = 30
PRIMARY_REPS = 100
PAIRED_N = 20
PAIRED_REPS = 100
PRIMARY_NAMESPACE = "GRI_BIOSYS_TN_A1_20260922"
PAIRED_NAMESPACE = "GRI_BIOSYS_TN_P20_20260922"

TCGA_SAMPLE_RE = re.compile(r"^(TCGA-[A-Z0-9]{2}-[A-Z0-9]{4})-([0-9]{2})[A-Z]?")

_X = None
_GENES = None
_MODULES = None
_GROUPS = None


def sha256_file(path: Path, chunk=16*1024*1024):
    h=hashlib.sha256()
    with path.open("rb") as fh:
        for b in iter(lambda: fh.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def stable_seed(namespace, cancer, state, draw):
    p=f"{namespace}|{cancer}|{state}|{int(draw)}".encode()
    return int.from_bytes(hashlib.sha256(p).digest()[:8],"big") % (2**32)


def exact_sign_two_sided(values):
    a=np.asarray(values,float); a=a[np.isfinite(a)]
    pos=int(np.sum(a>0)); neg=int(np.sum(a<0)); ties=int(np.sum(a==0)); n=pos+neg
    if n==0: return pos,neg,ties,float("nan")
    k=min(pos,neg)
    tail=sum(math.comb(n,i) for i in range(0,k+1))/(2**n)
    return pos,neg,ties,min(1.0,2*tail)


def bh_fdr(vals):
    p=np.asarray(vals,float); out=np.full_like(p,np.nan)
    good=np.flatnonzero(np.isfinite(p))
    if not len(good): return out
    v=p[good]; order=np.argsort(v,kind="mergesort"); r=v[order]; m=len(r)
    q=r*m/np.arange(1,m+1,dtype=float); q=np.minimum.accumulate(q[::-1])[::-1]; q=np.minimum(q,1.0)
    tmp=np.empty_like(q); tmp[order]=q; out[good]=tmp
    return out


def parse_barcode(v):
    s=str(v).strip().strip('"').upper().replace(".","-")
    m=TCGA_SAMPLE_RE.match(s)
    if not m: return None
    participant=m.group(1); st=m.group(2)
    parts=s.split("-"); sample="-".join(parts[:4])
    return participant,st,sample


def read_annotation(path):
    d=pd.read_csv(path,sep="\t",dtype=str,low_memory=False)
    lower={str(c).lower().strip():c for c in d.columns}
    bc=next((lower[x] for x in lower if x in {"aliquot_barcode","sample","sample_barcode","barcode"}),None)
    ca=next((lower[x] for x in lower if x in {"cancer type","cancer_type","project","project_id"}),None)
    du=next((lower[x] for x in lower if x.replace(" ","_") in {"do_not_use","donotuse"}),None)
    if bc is None or ca is None: raise ValueError("sample annotation columns unavailable")
    active={}; excluded=set()
    for r in d.itertuples(index=False,name=None):
        row=dict(zip(d.columns,r)); p=parse_barcode(row.get(bc,""))
        if not p: continue
        _,_,root=p; cancer=str(row.get(ca,"") or "").strip()
        if not cancer: continue
        if du and str(row.get(du,"") or "").strip().lower() in {"true","1","yes","y"}:
            excluded.add(root); continue
        if root in active and active[root] != cancer: raise ValueError(f"annotation cancer conflict {root}")
        active[root]=cancer
    return active,excluded


def parse_gmt(path):
    mods={}
    with open(path,"r",encoding="utf-8",errors="strict") as fh:
        for line in fh:
            p=line.rstrip("\r\n").split("\t")
            if len(p)>=3:
                name=p[0].strip(); genes=[x.strip() for x in p[2:] if x.strip()]
                if name and genes: mods[name]=list(dict.fromkeys(genes))
    if len(mods)!=50 or any(not x.startswith("HALLMARK_") for x in mods):
        raise ValueError(f"expected 50 Hallmarks, found {len(mods)}")
    return mods


def build_records(source, annotation, allowed_cancers):
    with open(source,"r",encoding="utf-8",errors="strict") as fh:
        header=fh.readline().rstrip("\r\n").split("\t")
    records=[]
    for pos,raw in enumerate(header[1:],start=1):
        p=parse_barcode(raw)
        if not p: continue
        participant,st,root=p
        if st not in {"01","11"}: continue
        cancer=annotation.get(root)
        if cancer not in allowed_cancers: continue
        records.append({"pos":pos,"label":str(raw).strip().strip('"'),"participant":participant,
                        "sample_type":st,"state":"TUMOR" if st=="01" else "NORMAL","sample_root":root,"cancer":cancer})
    by=defaultdict(list)
    for r in records: by[(r["cancer"],r["state"],r["participant"])].append(r)
    kept=[]; dup=[]
    for key,vals in sorted(by.items()):
        if len(vals)==1: kept.append(vals[0])
        else: dup.append({"cancer":key[0],"state":key[1],"participant":key[2],"source_columns":"|".join(x["label"] for x in vals)})
    kept=sorted(kept,key=lambda r:r["pos"])
    return kept,dup


def load_hallmark_union(source, records, modules):
    union=set(g for genes in modules.values() for g in genes)
    usecols=[0]+[r["pos"] for r in records]
    pieces=[]; genes=[]; seen=set()
    for chunk in pd.read_csv(source,sep="\t",header=0,usecols=usecols,chunksize=192,low_memory=False,
                             na_values=["","NA","N/A","NaN","nan","NULL","null"],keep_default_na=True):
        gids=chunk.iloc[:,0].astype(str).str.strip().str.strip('"').str.split("|",regex=False).str[0]
        keep=[]
        for i,g in enumerate(gids.tolist()):
            if g in union and g not in seen:
                seen.add(g); keep.append(i); genes.append(g)
        if not keep: continue
        vals=chunk.iloc[keep,1:].apply(pd.to_numeric,errors="coerce").to_numpy(dtype=float, copy=True).T.copy()
        finite=np.isfinite(vals)
        vals[finite & (vals<0)] = 0.0
        vals[finite] = np.log2(vals[finite] + 1.0)
        pieces.append(vals)
    if not pieces: raise ValueError("no Hallmark-union genes recovered from RNA source")
    x=np.concatenate(pieces,axis=1)
    if x.shape[0]!=len(records) or x.shape[1]!=len(genes): raise ValueError("RNA extraction shape drift")
    return x,np.asarray(genes,dtype=object)


def metric_rows(x,genes,modules):
    ms=compute_module_metrics_accelerated(
        x,genes,modules,minimum_mapped_genes=15,
        minimum_gene_finite_fraction=0.95,minimum_gene_finite_samples=20,
        minimum_pairwise_overlap_fraction=0.80,minimum_pairwise_overlap_samples=20)
    return ms


def init_worker(x,genes,modules,groups):
    global _X,_GENES,_MODULES,_GROUPS
    _X=x; _GENES=genes; _MODULES=modules; _GROUPS=groups


def one_cancer(cancer):
    global _X,_GENES,_MODULES,_GROUPS
    out_mod=[]; out_draw=[]; out_mem=[]; paired_mod=[]; paired_draw=[]; paired_mem=[]
    g=_GROUPS[cancer]
    if g.get("PRIMARY_ELIGIBLE", False):
        for rep in range(PRIMARY_REPS):
            sels={}
            for state in ["TUMOR","NORMAL"]:
                pool=g[state]
                rng=np.random.default_rng(stable_seed(PRIMARY_NAMESPACE,cancer,state,rep))
                sel=np.sort(rng.choice(pool,size=FIXED_N,replace=False)); sels[state]=sel
                m=metric_rows(_X[sel,:],_GENES,_MODULES)
                out_mem.append({"lane":"TN_A1","cancer":cancer,"state":state,"resample":rep,
                                "participants":"|".join(g["row_to_participant"][int(i)] for i in sel)})
                for z in m:
                    out_mod.append({"lane":"TN_A1","cancer":cancer,"state":state,"resample":rep,"module":z.module,
                                    "n_genes":z.n_genes,"cin_pairwise_median_abs":z.cin_pairwise_median_abs,
                                    "cin_pc1_variance_fraction":z.cin_pc1_variance_fraction,
                                    "cout_eigengene_median_abs":z.cout_eigengene_median_abs,
                                    "pc1_imputed_fraction":z.pc1_imputed_fraction})
                if not m: raise ValueError(f"{cancer} {state}: no evaluable Hallmarks")
                out_draw.append({"lane":"TN_A1","cancer":cancer,"state":state,"resample":rep,
                                 "evaluable_hallmarks":len(m),
                                 "cin_pairwise":float(np.nanmedian([z.cin_pairwise_median_abs for z in m])),
                                 "cin_pc1":float(np.nanmedian([z.cin_pc1_variance_fraction for z in m])),
                                 "cout":float(np.nanmedian([z.cout_eigengene_median_abs for z in m]))})
    paired_parts=g.get("PAIRED_PARTS",[])
    if len(paired_parts)>=PAIRED_N:
        for rep in range(PAIRED_REPS):
            rng=np.random.default_rng(stable_seed(PAIRED_NAMESPACE,cancer,"PAIRED",rep))
            parts=np.asarray(paired_parts,dtype=object)
            chosen=parts[np.sort(rng.choice(len(parts),size=PAIRED_N,replace=False))]
            for state in ["TUMOR","NORMAL"]:
                sel=np.asarray([g["participant_to_row"][state][str(p)] for p in chosen],dtype=int)
                m=metric_rows(_X[sel,:],_GENES,_MODULES)
                paired_mem.append({"lane":"TN_P20","cancer":cancer,"state":state,"resample":rep,
                                   "participants":"|".join(map(str,chosen.tolist()))})
                for z in m:
                    paired_mod.append({"lane":"TN_P20","cancer":cancer,"state":state,"resample":rep,"module":z.module,
                                       "n_genes":z.n_genes,"cin_pairwise_median_abs":z.cin_pairwise_median_abs,
                                       "cin_pc1_variance_fraction":z.cin_pc1_variance_fraction,
                                       "cout_eigengene_median_abs":z.cout_eigengene_median_abs,
                                       "pc1_imputed_fraction":z.pc1_imputed_fraction})
                paired_draw.append({"lane":"TN_P20","cancer":cancer,"state":state,"resample":rep,
                                    "evaluable_hallmarks":len(m),
                                    "cin_pairwise":float(np.nanmedian([z.cin_pairwise_median_abs for z in m])),
                                    "cin_pc1":float(np.nanmedian([z.cin_pc1_variance_fraction for z in m])),
                                    "cout":float(np.nanmedian([z.cout_eigengene_median_abs for z in m]))})
    return out_mod,out_draw,out_mem,paired_mod,paired_draw,paired_mem


def summarize(draw_df,lane):
    d=draw_df[draw_df["lane"].eq(lane)].copy()
    metrics=["cin_pairwise","cin_pc1","cout"]
    state_rows=[]; effect_rows=[]
    for (c,state),g in d.groupby(["cancer","state"],sort=True):
        row={"lane":lane,"cancer":c,"state":state}
        for m in metrics:
            v=pd.to_numeric(g[m],errors="coerce").to_numpy(float); v=v[np.isfinite(v)]
            row[m+"_median"]=float(np.median(v)); row[m+"_q05"]=float(np.quantile(v,.05)); row[m+"_q95"]=float(np.quantile(v,.95))
        state_rows.append(row)
    for c,g in d.groupby("cancer",sort=True):
        t=g[g.state.eq("TUMOR")].set_index("resample"); n=g[g.state.eq("NORMAL")].set_index("resample")
        common=sorted(set(t.index)&set(n.index))
        row={"lane":lane,"cancer":c,"paired_draws":len(common)}
        for m in metrics:
            diff=t.loc[common,m].to_numpy(float)-n.loc[common,m].to_numpy(float); diff=diff[np.isfinite(diff)]
            row[m+"_tumor_minus_normal_median"]=float(np.median(diff))
            row[m+"_diff_q05"]=float(np.quantile(diff,.05)); row[m+"_diff_q95"]=float(np.quantile(diff,.95))
        effect_rows.append(row)
    eff=pd.DataFrame(effect_rows)
    tests=[]
    for m in metrics:
        col=m+"_tumor_minus_normal_median"; v=pd.to_numeric(eff[col],errors="coerce").to_numpy(float); v=v[np.isfinite(v)]
        pos,neg,ties,p=exact_sign_two_sided(v)
        tests.append({"lane":lane,"metric":m,"eligible_cancers":len(v),"positive_cancers":pos,"negative_cancers":neg,
                      "ties":ties,"median_effect":float(np.median(v)) if len(v) else np.nan,"sign_test_p_two_sided":p})
    q=bh_fdr([r["sign_test_p_two_sided"] for r in tests])
    for r,qq in zip(tests,q):
        r["bh_q"]=float(qq) if np.isfinite(qq) else np.nan
        r["passes_q05"]=bool(np.isfinite(qq) and qq<.05)
        if r["passes_q05"]: r["outcome_class"]="TN-SPECIFIC"
        elif r["positive_cancers"]>0 and r["negative_cancers"]>0: r["outcome_class"]="TN-HETEROGENEOUS"
        else: r["outcome_class"]="TN-SHARED_NO_RESOLVED_SHIFT"
    return pd.DataFrame(state_rows),eff,pd.DataFrame(tests)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--rna",required=True,type=Path); ap.add_argument("--annotation",required=True,type=Path)
    ap.add_argument("--gmt",required=True,type=Path); ap.add_argument("--eligibility",required=True,type=Path)
    ap.add_argument("--out",required=True,type=Path); ap.add_argument("--workers",type=int,default=2)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=True)
    if sha256_file(a.rna)!=EXPECTED_RNA_SHA256: raise ValueError("RNA source SHA-256 mismatch")
    if sha256_file(a.gmt)!=EXPECTED_GMT_SHA256: raise ValueError("Hallmark GMT SHA-256 mismatch")
    cfg=json.loads(a.eligibility.read_text())
    primary=set(cfg["eligible_sets"]["rna_primary_n30"]); paired=set(cfg["eligible_sets"]["rna_paired_sensitivity_n20"])
    allowed=primary|paired
    annotation,_=read_annotation(a.annotation); modules=parse_gmt(a.gmt)
    records,dups=build_records(a.rna,annotation,allowed)
    pd.DataFrame(dups).to_csv(a.out/"TN_RNA_DUPLICATE_PARTICIPANT_EXCLUSIONS.csv",index=False)
    x,genes=load_hallmark_union(a.rna,records,modules)
    recdf=pd.DataFrame(records); recdf["matrix_row"]=np.arange(len(recdf))
    recdf.to_csv(a.out/"TN_RNA_SAMPLE_MANIFEST.csv",index=False)
    groups={}
    for cancer in sorted(primary):
        groups[cancer]={"row_to_participant":dict(zip(recdf.matrix_row.astype(int),recdf.participant.astype(str))),"PRIMARY_ELIGIBLE":True}
        groups[cancer]["participant_to_row"]={}
        for state in ["TUMOR","NORMAL"]:
            z=recdf[(recdf.cancer.eq(cancer))&(recdf.state.eq(state))]
            if len(z)<FIXED_N: raise ValueError(f"{cancer} {state} below n30 after duplicate exclusion: {len(z)}")
            groups[cancer][state]=z.matrix_row.to_numpy(int)
            groups[cancer]["participant_to_row"][state]=dict(zip(z.participant.astype(str),z.matrix_row.astype(int)))
        groups[cancer]["PAIRED_PARTS"]=sorted(set(groups[cancer]["participant_to_row"]["TUMOR"])&set(groups[cancer]["participant_to_row"]["NORMAL"]))
    for cancer in sorted(paired-primary):
        groups[cancer]={"row_to_participant":dict(zip(recdf.matrix_row.astype(int),recdf.participant.astype(str))),"participant_to_row":{},"PRIMARY_ELIGIBLE":False}
        for state in ["TUMOR","NORMAL"]:
            z=recdf[(recdf.cancer.eq(cancer))&(recdf.state.eq(state))]
            groups[cancer][state]=z.matrix_row.to_numpy(int)
            groups[cancer]["participant_to_row"][state]=dict(zip(z.participant.astype(str),z.matrix_row.astype(int)))
        groups[cancer]["PAIRED_PARTS"]=sorted(set(groups[cancer]["participant_to_row"]["TUMOR"])&set(groups[cancer]["participant_to_row"]["NORMAL"]))
    for cancer in paired:
        if len(groups[cancer]["PAIRED_PARTS"])<PAIRED_N: raise ValueError(f"{cancer}: paired set fell below n20")

    mod=[];draw=[];mem=[];pmod=[];pdraw=[];pmem=[]
    cancers=sorted(primary|paired)
    with ProcessPoolExecutor(max_workers=max(1,min(a.workers,len(cancers))),initializer=init_worker,initargs=(x,genes,modules,groups)) as ex:
        futs={ex.submit(one_cancer,c):c for c in cancers}
        for fut in as_completed(futs):
            c=futs[fut]; A,B,C,D,E,F=fut.result()
            mod+=A;draw+=B;mem+=C;pmod+=D;pdraw+=E;pmem+=F
            print(f"completed RNA tumor-normal {c}",flush=True)
    moddf=pd.DataFrame(mod+pmod); drawdf=pd.DataFrame(draw+pdraw); memdf=pd.DataFrame(mem+pmem)
    moddf.to_csv(a.out/"TN_RNA_MODULE_METRICS.csv.gz",index=False,compression="gzip")
    drawdf.to_csv(a.out/"TN_RNA_DRAW_COORDINATES.csv.gz",index=False,compression="gzip")
    memdf.to_csv(a.out/"TN_RNA_RESAMPLE_MEMBERSHIP.csv.gz",index=False,compression="gzip")
    outputs={}
    for lane in ["TN_A1","TN_P20"]:
        state,eff,tests=summarize(drawdf,lane)
        state.to_csv(a.out/f"{lane}_STATE_SUMMARY.csv",index=False)
        eff.to_csv(a.out/f"{lane}_CANCER_EFFECTS.csv",index=False)
        tests.to_csv(a.out/f"{lane}_GLOBAL_INFERENCE.csv",index=False)
        outputs[lane]={"state_rows":len(state),"cancer_rows":len(eff),"tests":tests.to_dict(orient="records")}
    summary={"schema":"gri-biosystems-tn-rna-v1","status":"COMPLETE","rna_sha256":EXPECTED_RNA_SHA256,
             "gmt_sha256":EXPECTED_GMT_SHA256,"primary_namespace":PRIMARY_NAMESPACE,"paired_namespace":PAIRED_NAMESPACE,
             "fixed_n":FIXED_N,"primary_resamples":PRIMARY_REPS,"paired_n":PAIRED_N,"paired_resamples":PAIRED_REPS,
             "hallmark_union_genes":int(len(genes)),"sample_manifest_rows":int(len(recdf)),"duplicate_exclusions":int(len(dups)),
             "molecular_values_opened":True,"outputs":outputs}
    (a.out/"TN_RNA_RUN_SUMMARY.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
    print(json.dumps(summary,indent=2,sort_keys=True),flush=True)

if __name__=="__main__":
    main()
