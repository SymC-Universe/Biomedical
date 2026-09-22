#!/usr/bin/env python3
from __future__ import annotations

import argparse, base64, csv, hashlib, json, lzma, math, re
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd

RNA_SHA = "674b19b7ed9ae4c5ef35ee2824936429aa5d46c0735a3d180f41552fcbbdb658"
METH_SHA = "5934c497882fbe8178d128a3a7f71e765480af6bbd460e0398de3428cd075b77"
GMT_SHA = "eecaf6dad908334ae885406ec72bdc0646d8917588ed7c219fac92fc5363f596"
SUPPORT_B64_SHA = "1463a4a6ad157dc770278ef97b6fcd2fb80b6e73ce4d774a2ca47aa7870391b1"
SUPPORT_RAW_SHA = "d45947345007b901e684adf92840889acf1ab00377153d54de2766cd1084c9b2"
N = 30
REPS = 100
NS = "GRI_BIOSYS_TN_C1_20260922"
TCGA_RE = re.compile(r"^(TCGA-[A-Z0-9]{2}-[A-Z0-9]{4})-([0-9]{2})[A-Z]?")

DATA = {}

def sha256_file(path, chunk=16*1024*1024):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(chunk),b""): h.update(b)
    return h.hexdigest()

def stable_seed(namespace,cancer,track,stratum,resample,null_type,replicate=0):
    s=f"{namespace}|{cancer}|{track}|{stratum}|{int(resample)}|{null_type}|{int(replicate)}".encode()
    return int.from_bytes(hashlib.sha256(s).digest()[:8],"big")%(2**32)

def bh_fdr(vals):
    p=np.asarray(vals,float); out=np.full_like(p,np.nan)
    good=np.flatnonzero(np.isfinite(p))
    if len(good)==0:return out
    v=p[good]; o=np.argsort(v,kind="mergesort"); r=v[o]; m=len(r)
    q=r*m/np.arange(1,m+1,dtype=float); q=np.minimum.accumulate(q[::-1])[::-1]; q=np.minimum(q,1)
    tmp=np.empty_like(q); tmp[o]=q; out[good]=tmp; return out

def sign_two(values):
    v=np.asarray(values,float);v=v[np.isfinite(v)]
    pos=int((v>0).sum());neg=int((v<0).sum());ties=int((v==0).sum());n=pos+neg
    if n==0:return pos,neg,ties,np.nan
    k=min(pos,neg); tail=sum(math.comb(n,i) for i in range(k+1))/(2**n)
    return pos,neg,ties,min(1.0,2*tail)

def parse_barcode(v):
    s=str(v).strip().strip('"').upper().replace(".","-")
    m=TCGA_RE.match(s)
    if not m:return None
    participant=m.group(1);st=m.group(2);parts=s.split("-")
    return participant,st,"-".join(parts[:4])

def read_annotation(path):
    d=pd.read_csv(path,sep="\t",dtype=str,low_memory=False)
    lo={str(c).lower().strip():c for c in d.columns}
    bc=next((lo[x] for x in lo if x in {"aliquot_barcode","sample","sample_barcode","barcode"}),None)
    ca=next((lo[x] for x in lo if x in {"cancer type","cancer_type","project","project_id"}),None)
    du=next((lo[x] for x in lo if x.replace(" ","_") in {"do_not_use","donotuse"}),None)
    if bc is None or ca is None:raise ValueError("annotation columns unavailable")
    active={}
    for row in d.to_dict("records"):
        p=parse_barcode(row.get(bc,""))
        if not p:continue
        _,_,root=p
        if du and str(row.get(du,"") or "").strip().lower() in {"true","1","yes","y"}:continue
        cancer=str(row.get(ca,"") or "").strip()
        if cancer:active[root]=cancer
    return active

def header_records(path,annotation,allowed):
    with open(path,"r",encoding="utf-8",errors="strict") as f: hdr=f.readline().rstrip("\r\n").split("\t")
    rec=[]
    for pos,raw in enumerate(hdr[1:],1):
        p=parse_barcode(raw)
        if not p:continue
        participant,st,root=p
        if st not in {"01","11"}:continue
        cancer=annotation.get(root)
        if cancer not in allowed:continue
        rec.append({"pos":pos,"participant":participant,"state":"TUMOR" if st=="01" else "NORMAL","cancer":cancer,"label":str(raw).strip().strip('"')})
    by=defaultdict(list)
    for r in rec:by[(r["cancer"],r["state"],r["participant"])].append(r)
    unique={k:v[0] for k,v in by.items() if len(v)==1}
    dups=[{"cancer":k[0],"state":k[1],"participant":k[2],"n_columns":len(v),"labels":"|".join(x["label"] for x in v)} for k,v in by.items() if len(v)>1]
    return unique,dups

def parse_gmt(path):
    mods={}
    with open(path,encoding="utf-8") as f:
        for line in f:
            p=line.rstrip("\r\n").split("\t")
            if len(p)>=3:mods[p[0]]=list(dict.fromkeys(x for x in p[2:] if x))
    if len(mods)!=50:raise ValueError(f"expected 50 Hallmarks, got {len(mods)}")
    return mods

def load_support(path):
    b=Path(path).read_bytes()
    if hashlib.sha256(b).hexdigest()!=SUPPORT_B64_SHA:raise ValueError("C1 support payload b64 hash mismatch")
    raw=lzma.decompress(base64.b64decode(b))
    if hashlib.sha256(raw).hexdigest()!=SUPPORT_RAW_SHA:raise ValueError("C1 support payload raw hash mismatch")
    txt=raw.decode("utf-8").splitlines()
    if not txt or txt[0]!="CORE" or "MASK" not in txt:raise ValueError("C1 support payload schema drift")
    k=txt.index("MASK")
    core={}
    for line in txt[1:k]:
        if not line:continue
        pid,genes=line.split("\t",1)
        core[pid]=[g for g in genes.split(";") if g]
    mask={x for x in txt[k+1:] if x}
    if len(core)!=3999 or len(mask)!=579:raise ValueError(f"C1 support semantic drift core={len(core)} mask={len(mask)}")
    return core,mask

def load_rna(path, records, modules):
    union=set(g for m in modules.values() for g in m)
    positions=[r["rna_pos"] for r in records]
    if len(set(positions))!=len(positions): raise ValueError("duplicate RNA source positions in frozen record set")
    source_order=sorted(positions)
    source_to_record={p:i for i,p in enumerate(positions)}
    reorder=np.asarray([source_to_record[p] for p in source_order],dtype=int)
    inverse=np.empty_like(reorder); inverse[reorder]=np.arange(len(reorder))
    use=[0]+positions
    vals=[];genes=[];seen=set()
    for ch in pd.read_csv(path,sep="\t",header=0,usecols=use,chunksize=192,low_memory=False,
                          na_values=["","NA","N/A","NaN","nan","NULL","null"],keep_default_na=True):
        gid=ch.iloc[:,0].astype(str).str.strip().str.strip('"').str.split("|",regex=False).str[0]
        keep=[]
        for i,g in enumerate(gid.tolist()):
            if g in union and g not in seen:seen.add(g);keep.append(i);genes.append(g)
        if not keep:continue
        x=ch.iloc[keep,1:].apply(pd.to_numeric,errors="coerce").to_numpy(dtype=float,copy=True).T.copy()
        if x.shape[0]!=len(source_order): raise ValueError("RNA selected-column count drift")
        x=x[inverse,:].copy()
        fin=np.isfinite(x);x[fin&(x<0)]=0;x[fin]=np.log2(x[fin]+1)
        vals.append(x)
    x=np.concatenate(vals,axis=1)
    if x.shape!=(len(records),len(genes)):raise ValueError("RNA extraction shape drift")
    return x,np.asarray(genes,dtype=object)

def load_meth(path,records):
    positions=[r["meth_pos"] for r in records]
    if len(set(positions))!=len(positions): raise ValueError("duplicate methylation source positions in frozen record set")
    source_order=sorted(positions)
    source_to_record={p:i for i,p in enumerate(positions)}
    reorder=np.asarray([source_to_record[p] for p in source_order],dtype=int)
    inverse=np.empty_like(reorder); inverse[reorder]=np.arange(len(reorder))
    use=[0]+positions
    probe_ids=[];blocks=[]
    for ch in pd.read_csv(path,sep="\t",header=None,skiprows=1,usecols=use,chunksize=96,engine="c",low_memory=False,
                          na_values=["","NA","N/A","NaN","nan","NULL","null"],keep_default_na=True):
        ids=ch.iloc[:,0].astype(str).str.strip().str.strip('"').tolist();probe_ids.extend(ids)
        x=ch.iloc[:,1:].apply(pd.to_numeric,errors="coerce").to_numpy(dtype=np.float32,copy=True).T.copy()
        if x.shape[0]!=len(source_order): raise ValueError("methylation selected-column count drift")
        x=x[inverse,:].copy()
        fin=np.isfinite(x)
        if fin.any() and (float(np.nanmin(x))<0 or float(np.nanmax(x))>1):raise ValueError("beta outside [0,1]")
        blocks.append(x)
    b=np.concatenate(blocks,axis=1)
    if len(probe_ids)!=22601 or len(set(probe_ids))!=22601:raise ValueError("methylation probe universe drift")
    if b.shape!=(len(records),22601):raise ValueError("methylation extraction shape drift")
    return b,np.asarray(probe_ids,dtype=object)

def spearman(a,b):
    a=np.asarray(a,float);b=np.asarray(b,float);good=np.isfinite(a)&np.isfinite(b)
    if good.sum()<3:return np.nan
    ra=pd.Series(a[good]).rank(method="average").to_numpy(float);rb=pd.Series(b[good]).rank(method="average").to_numpy(float)
    if np.std(ra,ddof=1)<=0 or np.std(rb,ddof=1)<=0:return np.nan
    return float(np.corrcoef(ra,rb)[0,1])

def same_stat(a,b):
    v=[]
    for j in range(a.shape[1]):
        r=spearman(a[:,j],b[:,j]);v.append(abs(r) if np.isfinite(r) else np.nan)
    v=np.asarray(v,float)
    return float(np.nanmedian(v)) if np.isfinite(v).any() else np.nan

def modal(beta):
    b=np.asarray(beta,float)
    x=b-b.mean(0,keepdims=True);p=b.shape[1];g=(x@x.T)/float(p)
    vals,vecs=np.linalg.eigh(g);vals=vals[np.argsort(vals)[::-1]]
    scale=float(np.sum(np.abs(vals)));tol=1e-10*scale
    if np.any(vals<-tol):raise ValueError("negative modal eigenvalue")
    vals=np.where(vals<0,0,vals)[:29];q=vals/vals.sum();nz=q>0
    h=float(-np.sum(q[nz]*np.log(q[nz])));s=float(1-h/math.log(29.0))
    return s,x

def perm_cols(beta,seed):
    b=np.asarray(beta,float);rng=np.random.default_rng(seed);keys=rng.random(b.shape)
    order=np.argsort(keys,axis=0,kind="mergesort");cols=np.arange(b.shape[1])[None,:]
    return b[order,cols]

def cka(x,y):
    a=np.asarray(x,float);b=np.asarray(y,float);ka=a@a.T;kb=b@b.T;n=a.shape[0]
    h=np.eye(n)-np.ones((n,n))/n;kac=h@ka@h;kbc=h@kb@h
    den=float(np.linalg.norm(kac,"fro")*np.linalg.norm(kbc,"fro"))
    return float(np.sum(kac*kbc)/den) if den>0 else np.nan

def rna_centered(x):
    x=np.asarray(x,float);fin=np.isfinite(x)
    if fin.all():return x-x.mean(0,keepdims=True)
    counts=fin.sum(0);safe=np.where(fin,x,0.0)
    means=np.divide(safe.sum(0),counts,out=np.zeros(x.shape[1]),where=counts>0)
    return np.where(fin,x-means[None,:],0.0)

def meth_pc1(m):
    m=np.asarray(m,float);xc=m-m.mean(0,keepdims=True)
    if np.allclose(xc,0):raise ValueError("zero meth Hallmark")
    u,s,vt=np.linalg.svd(xc,full_matrices=False);eig=u[:,0]*s[0];load=vt[0].copy();mean=m.mean(1)
    if np.std(eig,ddof=1)>0 and np.std(mean,ddof=1)>0:
        if float(np.corrcoef(eig,mean)[0,1])<0:eig=-eig
    else:
        j=int(np.argmax(np.abs(load)))
        if load[j]<0:eig=-eig
    return eig

def rna_pc1(raw):
    x=np.asarray(raw,float);fin=np.isfinite(x);cnt=fin.sum(0);sd=np.nanstd(x,axis=0,ddof=1)
    valid=(cnt>=max(20,int(math.ceil(.95*x.shape[0]))))&np.isfinite(sd)&(sd>0)
    if int(valid.sum())<15:raise ValueError("RNA Hallmark <15 genes")
    y=x[:,valid];mu=np.nanmean(y,0);ss=np.nanstd(y,0,ddof=1);z=(y-mu)/ss;z=np.where(np.isfinite(z),z,0)
    u,s,_=np.linalg.svd(z,full_matrices=False);eig=u[:,0]*s[0];mean=z.mean(1)
    if np.std(eig,ddof=1)>0 and np.std(mean,ddof=1)>0 and float(np.corrcoef(eig,mean)[0,1])<0:eig=-eig
    return eig,int(valid.sum())

def build_gene_map(probe_ids,retain,core):
    idx=np.flatnonzero(retain);glob_to_local={str(probe_ids[g]):i for i,g in enumerate(idx.tolist())};gm=defaultdict(list)
    for pid,genes in core.items():
        loc=glob_to_local.get(pid)
        if loc is not None:
            for g in genes:gm[g].append(loc)
    return {g:np.asarray(sorted(set(v)),int) for g,v in gm.items()},idx

def hallmark_mats(beta30,expr30,gene_map,modules,gene_index):
    ms={};rs={};meta={}
    for h in sorted(modules):
        mm=[];usedm=[];probes=set()
        for gene in modules[h]:
            loc=gene_map.get(gene)
            if loc is None or len(loc)==0:continue
            mm.append(np.median(beta30[:,loc],axis=1));usedm.append(gene);probes.update(map(int,loc))
        if len(usedm)<10 or len(probes)<10:continue
        rg=[g for g in modules[h] if g in gene_index]
        if not rg:continue
        rr=expr30[:,[gene_index[g] for g in rg]]
        try:
            me=meth_pc1(np.column_stack(mm));re,nrg=rna_pc1(rr)
        except Exception:continue
        ms[h]=me;rs[h]=re;meta[h]=(len(usedm),len(probes),nrg)
    common=sorted(set(ms)&set(rs))
    if not common:return common,np.empty((30,0)),np.empty((30,0)),meta
    return common,np.column_stack([ms[h] for h in common]),np.column_stack([rs[h] for h in common]),meta

def state_rules(beta, rows_t, rows_n, mask_bool):
    xt=np.asarray(beta[rows_t,:],float);xn=np.asarray(beta[rows_n,:],float)
    ft=np.isfinite(xt).sum(0)/len(rows_t)>=.95;fn=np.isfinite(xn).sum(0)/len(rows_n)>=.95
    common=ft&fn
    with np.errstate(all="ignore"):
        mt=np.nanmedian(xt,axis=0);mn=np.nanmedian(xn,axis=0)
    if not np.isfinite(mt[common]).all() or not np.isfinite(mn[common]).all():raise ValueError("retained probe median nonfinite")
    return common,common&(~mask_bool),mt,mn

def one_cancer(cancer):
    beta=DATA["beta"];expr=DATA["expr"];probe_ids=DATA["probe_ids"];modules=DATA["modules"];genes=DATA["genes"];core=DATA["core"];mask=DATA["mask"];rows=DATA["rows"]
    gi={str(g):i for i,g in enumerate(genes)}
    rt=np.asarray(rows[(cancer,"TUMOR")],int);rn=np.asarray(rows[(cancer,"NORMAL")],int)
    primary,masked,medt,medn=state_rules(beta,rt,rn,mask)
    tracks={"PRIMARY_PUBLICATION":primary,"MASKED_TECHNICAL":masked}
    maps={};indices={}
    for tr,retain in tracks.items():maps[tr],indices[tr]=build_gene_map(probe_ids,retain,core)
    outputs=[];members=[]
    for state,pool,med in [("TUMOR",rt,medt),("NORMAL",rn,medn)]:
        ctoken=f"{cancer}:{state}"
        for rep in range(REPS):
            sel=np.sort(np.random.default_rng(stable_seed(NS,ctoken,"SHARED","ALL",rep,"resample",0)).choice(pool,size=N,replace=False))
            e30=expr[sel,:];xr=rna_centered(e30);members.append({"cancer":cancer,"state":state,"resample":rep,"participants":"|".join(DATA["participants"][i] for i in sel)})
            for tr,retain in tracks.items():
                idx=indices[tr];b=np.asarray(beta[np.ix_(sel,idx)],float).copy();bad=~np.isfinite(b)
                if bad.any():b[bad]=np.broadcast_to(med[idx],b.shape)[bad]
                s,xc=modal(b);sn,_=modal(perm_cols(b,stable_seed(NS,ctoken,tr,"ALL_PROBES",rep,"modal_null",0)))
                dc1=s-sn
                cv=cka(xc,xr);perm=np.random.default_rng(stable_seed(NS,ctoken,tr,"ALL_PROBES",rep,"patient_null",0)).permutation(N);cn=cka(xc[perm,:],xr)
                common,ms,rs,_=hallmark_mats(b,e30,maps[tr],modules,gi);valid=len(common)>=25
                ap=al=np.nan
                if valid:
                    same=same_stat(ms,rs)
                    pp=np.random.default_rng(stable_seed(NS,ctoken,tr,"PROMOTER_CORE",rep,"patient_null",0)).permutation(N)
                    lp=np.random.default_rng(stable_seed(NS,ctoken,tr,"PROMOTER_CORE",rep,"label_null",0)).permutation(len(common))
                    ap=same-same_stat(ms[pp,:],rs);al=same-same_stat(ms[:,lp],rs)
                outputs.append({"cancer":cancer,"state":state,"track":tr,"resample":rep,"eligible_probe_count":len(idx),
                                "common_hallmarks":len(common),"primary_valid":valid,"delta_s":dc1,"delta_cka":cv-cn,
                                "delta_a_patient":ap,"delta_a_label":al})
    diag={"cancer":cancer,"tumor_pool_n":len(rt),"normal_pool_n":len(rn),"common_primary_probes":int(primary.sum()),"common_masked_probes":int(masked.sum())}
    return outputs,members,diag

def summarize(df):
    hyps=["delta_s","delta_cka","delta_a_patient","delta_a_label"]; states=[];effects=[]
    for (c,tr,st),g in df.groupby(["cancer","track","state"],sort=True):
        row={"cancer":c,"track":tr,"state":st}
        for h in hyps:
            v=pd.to_numeric(g[h],errors="coerce").to_numpy(float);v=v[np.isfinite(v)]
            row[h+"_median"]=float(np.median(v)) if len(v) else np.nan;row[h+"_q05"]=float(np.quantile(v,.05)) if len(v) else np.nan;row[h+"_q95"]=float(np.quantile(v,.95)) if len(v) else np.nan
        states.append(row)
    for (c,tr),g in df.groupby(["cancer","track"],sort=True):
        t=g[g.state.eq("TUMOR")].set_index("resample");n=g[g.state.eq("NORMAL")].set_index("resample");ix=sorted(set(t.index)&set(n.index))
        row={"cancer":c,"track":tr,"paired_draws":len(ix)}
        for h in hyps:
            d=t.loc[ix,h].to_numpy(float)-n.loc[ix,h].to_numpy(float);d=d[np.isfinite(d)]
            row[h+"_tumor_minus_normal_median"]=float(np.median(d)) if len(d) else np.nan
            row[h+"_diff_q05"]=float(np.quantile(d,.05)) if len(d) else np.nan;row[h+"_diff_q95"]=float(np.quantile(d,.95)) if len(d) else np.nan
        effects.append(row)
    eff=pd.DataFrame(effects);tests=[]
    for tr in ["PRIMARY_PUBLICATION","MASKED_TECHNICAL"]:
        sub=eff[eff.track.eq(tr)]
        fam=[]
        for label,h in [("H1","delta_s"),("H2","delta_cka"),("H3a","delta_a_patient"),("H3b","delta_a_label")]:
            v=pd.to_numeric(sub[h+"_tumor_minus_normal_median"],errors="coerce").to_numpy(float);v=v[np.isfinite(v)]
            pos,neg,ties,p=sign_two(v);fam.append({"track":tr,"hypothesis":label,"metric":h,"cancers":len(v),"positive":pos,"negative":neg,"ties":ties,"median_effect":float(np.median(v)) if len(v) else np.nan,"sign_test_p_two_sided":p})
        q=bh_fdr([x["sign_test_p_two_sided"] for x in fam])
        for x,qq in zip(fam,q):x["bh_q"]=float(qq) if np.isfinite(qq) else np.nan;x["passes_q05"]=bool(np.isfinite(qq) and qq<.05)
        tests+=fam
    return pd.DataFrame(states),eff,pd.DataFrame(tests)

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--rna",required=True);ap.add_argument("--meth",required=True);ap.add_argument("--annotation",required=True);ap.add_argument("--gmt",required=True);ap.add_argument("--support",required=True);ap.add_argument("--eligibility",required=True);ap.add_argument("--out",required=True,type=Path);ap.add_argument("--workers",type=int,default=2);a=ap.parse_args()
    a.out.mkdir(parents=True,exist_ok=True)
    for p,e,l in [(a.rna,RNA_SHA,"RNA"),(a.meth,METH_SHA,"methylation"),(a.gmt,GMT_SHA,"Hallmark")]:
        got=sha256_file(p);print(l,got,flush=True)
        if got!=e:raise ValueError(f"{l} SHA mismatch")
    cfg=json.loads(Path(a.eligibility).read_text());cancers=set(cfg["eligible_sets"]["multiomic_primary_n30"])
    ann=read_annotation(a.annotation);rna_map,rdup=header_records(a.rna,ann,cancers);meth_map,mdup=header_records(a.meth,ann,cancers)
    keys=sorted(set(rna_map)&set(meth_map));by=defaultdict(list)
    for k in keys:by[(k[0],k[1])].append(k[2])
    records=[]
    for cancer in sorted(cancers):
        for state in ["TUMOR","NORMAL"]:
            parts=sorted(by[(cancer,state)])
            if len(parts)<30:raise ValueError(f"{cancer} {state} overlap fell below n30: {len(parts)}")
            for p in parts:
                k=(cancer,state,p);records.append({"cancer":cancer,"state":state,"participant":p,"rna_pos":rna_map[k]["pos"],"meth_pos":meth_map[k]["pos"]})
    for i,r in enumerate(records):r["row"]=i
    if len({r["rna_pos"] for r in records})!=len(records) or len({r["meth_pos"] for r in records})!=len(records):
        raise ValueError("frozen C1 record set contains duplicated assay source positions")
    pd.DataFrame(rdup).to_csv(a.out/"TN_C1_RNA_DUPLICATES_EXCLUDED.csv",index=False);pd.DataFrame(mdup).to_csv(a.out/"TN_C1_METH_DUPLICATES_EXCLUDED.csv",index=False);pd.DataFrame(records).to_csv(a.out/"TN_C1_SAMPLE_MANIFEST.csv",index=False)
    modules=parse_gmt(a.gmt);core,maskids=load_support(a.support)
    expr,genes=load_rna(a.rna,records,modules);beta,probe_ids=load_meth(a.meth,records);mask=np.asarray([str(p) in maskids for p in probe_ids],bool)
    if int(mask.sum())!=579:raise ValueError(f"technical mask source overlap drift {int(mask.sum())}")
    rows={(c,s):[r["row"] for r in records if r["cancer"]==c and r["state"]==s] for c in cancers for s in ["TUMOR","NORMAL"]}
    DATA.update(beta=beta,expr=expr,probe_ids=probe_ids,genes=genes,modules=modules,core=core,mask=mask,rows=rows,participants=[r["participant"] for r in records])
    allrows=[];members=[];diags=[]
    with ThreadPoolExecutor(max_workers=max(1,min(a.workers,len(cancers)))) as ex:
        fut={ex.submit(one_cancer,c):c for c in sorted(cancers)}
        for f in as_completed(fut):
            c=fut[f];r,m,d=f.result();allrows+=r;members+=m;diags.append(d);print("completed TN-C1",c,d,flush=True)
    df=pd.DataFrame(allrows);df.to_csv(a.out/"TN_C1_RESAMPLE_METRICS.csv.gz",index=False,compression={"method":"gzip","mtime":0});pd.DataFrame(members).to_csv(a.out/"TN_C1_RESAMPLE_MEMBERSHIP.csv.gz",index=False,compression={"method":"gzip","mtime":0});pd.DataFrame(diags).sort_values("cancer").to_csv(a.out/"TN_C1_REPRESENTATION_DIAGNOSTICS.csv",index=False)
    state,eff,tests=summarize(df);state.to_csv(a.out/"TN_C1_STATE_SUMMARY.csv",index=False);eff.to_csv(a.out/"TN_C1_CANCER_EFFECTS.csv",index=False);tests.to_csv(a.out/"TN_C1_GLOBAL_INFERENCE.csv",index=False)
    summary={"schema":"gri-biosystems-tn-c1-v1","status":"COMPLETE","molecular_values_opened":True,"cancers":sorted(cancers),"n":N,"resamples":REPS,"seed_namespace":NS,"rna_sha256":RNA_SHA,"methylation_sha256":METH_SHA,"support_raw_sha256":SUPPORT_RAW_SHA,"diagnostics":sorted(diags,key=lambda x:x["cancer"]),"tests":tests.to_dict("records")}
    (a.out/"TN_C1_RUN_SUMMARY.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n");print(json.dumps(summary,indent=2),flush=True)

if __name__=="__main__":main()
