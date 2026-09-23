#!/usr/bin/env python3
from __future__ import annotations

import argparse, csv, hashlib, json, math, re
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd

METH_SHA="5934c497882fbe8178d128a3a7f71e765480af6bbd460e0398de3428cd075b77"
PURITY_SHA="f430a975433d82e0098d7405619d4f12a0c765fcd97e7d63cc9b1de7f2d763cd"
LEUK_SHA="5a8268caedbf8dc98a75be0528d583238d7355761d9fc746e42002f223a982d9"
RNA_INHERITED_SHA="674b19b7ed9ae4c5ef35ee2824936429aa5d46c0735a3d180f41552fcbbdb658"
N=30
DRAWS=20
NS="GRI_BIOSYS_R1_H1_COMPOSITION_20260923"
CANCERS="ACC BLCA BRCA CESC CHOL COAD DLBC ESCA GBM HNSC KICH KIRC KIRP LGG LIHC LUAD LUSC MESO OV PAAD PCPG PRAD READ SARC SKCM STAD TGCT THCA THYM UCEC UCS UVM".split()
EXPECTED_ELIGIBLE=sorted(set(CANCERS)-{"DLBC","THYM"})
TCGA_RE=re.compile(r"^(TCGA-[A-Z0-9]{2}-[A-Z0-9]{4})-([0-9]{2})[A-Z]?")

DATA={}

def sha256_file(path,chunk=16*1024*1024):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(chunk),b""): h.update(b)
    return h.hexdigest()

def stable_seed(*parts):
    s="|".join(map(str,parts)).encode()
    return int.from_bytes(hashlib.sha256(s).digest()[:8],"big")%(2**32)

def parse_barcode(v):
    s=str(v).strip().strip('"').upper().replace(".","-")
    m=TCGA_RE.match(s)
    if not m:return None
    pid=m.group(1);st=m.group(2);parts=s.split("-")
    root="-".join(parts[:4])
    return pid,st,root

def read_annotation(path):
    d=pd.read_csv(path,sep="\t",dtype=str,low_memory=False)
    lo={str(c).lower().strip():c for c in d.columns}
    bc=next((lo[x] for x in lo if x in {"aliquot_barcode","sample","sample_barcode","barcode"}),None)
    ca=next((lo[x] for x in lo if x in {"cancer type","cancer_type","project","project_id"}),None)
    du=next((lo[x] for x in lo if x.replace(" ","_") in {"do_not_use","donotuse"}),None)
    if bc is None or ca is None:raise ValueError("annotation columns unavailable")
    active={}
    conflicts=[]
    for row in d.to_dict("records"):
        p=parse_barcode(row.get(bc,""))
        if not p:continue
        _,_,root=p
        if du and str(row.get(du,"") or "").strip().lower() in {"true","1","yes","y"}:continue
        cancer=str(row.get(ca,"") or "").strip()
        if not cancer:continue
        if root in active and active[root]!=cancer:conflicts.append((root,active[root],cancer))
        active[root]=cancer
    if conflicts:raise ValueError(f"annotation cancer conflicts: {conflicts[:5]}")
    return active

def header_primary_unique_from_line(header_line,annotation):
    hdr=header_line.rstrip("\r\n").split("\t")
    by=defaultdict(list)
    for pos,raw in enumerate(hdr[1:],1):
        p=parse_barcode(raw)
        if not p:continue
        pid,st,root=p
        if st!="01":continue
        cancer=annotation.get(root)
        if cancer not in CANCERS:continue
        by[(cancer,pid)].append({"pos":pos,"root":root,"label":str(raw).strip().strip('"')})
    unique={k:v[0] for k,v in by.items() if len(v)==1}
    dups={k:v for k,v in by.items() if len(v)>1}
    return unique,dups

def first_line(path):
    with open(path,"r",encoding="utf-8",errors="strict") as f:
        return f.readline()

def read_leuk(path):
    d=pd.read_csv(path,sep="\t",header=None,names=["cancer","sample","value"],dtype=str)
    d["p"]=d["sample"].map(parse_barcode)
    d=d[d["p"].notna()].copy()
    d["pid"]=d["p"].map(lambda x:x[0]);d["stype"]=d["p"].map(lambda x:x[1]);d["root"]=d["p"].map(lambda x:x[2])
    d["value_num"]=pd.to_numeric(d["value"],errors="coerce")
    d=d[d["stype"].eq("01") & d["value_num"].notna()].copy()
    g=d.groupby(["pid","cancer"],sort=True)["value_num"].median().reset_index()
    # participant must map to one cancer
    cc=g.groupby("pid")["cancer"].nunique()
    bad=set(cc[cc!=1].index)
    g=g[~g["pid"].isin(bad)].copy()
    return {r.pid:(str(r.cancer),float(r.value_num)) for r in g.itertuples(index=False)}

def read_purity(path):
    d=pd.read_csv(path,sep="\t",dtype=str,low_memory=False)
    lo={str(c).lower().strip():c for c in d.columns}
    sample=lo.get("sample")
    purity=lo.get("purity")
    status=next((lo[x] for x in lo if x.replace("_"," ")=="call status"),None)
    if sample is None or purity is None or status is None:raise ValueError(f"purity schema drift {list(d.columns)[:20]}")
    d["p"]=d[sample].map(parse_barcode)
    d=d[d["p"].notna()].copy()
    d["pid"]=d["p"].map(lambda x:x[0]);d["stype"]=d["p"].map(lambda x:x[1])
    d["numeric"]=pd.to_numeric(d[purity],errors="coerce")
    d=d[d["stype"].eq("01") & d[status].astype(str).str.lower().eq("called") & d["numeric"].notna()].copy()
    counts=d.groupby("pid").size()
    unique=set(counts[counts==1].index)
    d=d[d["pid"].isin(unique)].copy()
    return {r.pid:float(r.numeric) for r in d[["pid","numeric"]].itertuples(index=False)}

def modal_s(b):
    b=np.asarray(b,float)
    x=b-b.mean(axis=0,keepdims=True)
    g=(x@x.T)/float(b.shape[1])
    vals=np.linalg.eigvalsh(g)[::-1]
    scale=float(np.sum(np.abs(vals)));tol=1e-10*scale if scale>0 else 0
    if np.any(vals < -tol):raise ValueError("negative modal eigenvalue")
    vals=np.where(vals<0,0,vals)[:b.shape[0]-1]
    tot=float(vals.sum())
    if not np.isfinite(tot) or tot<=0:return np.nan
    q=vals/tot;nz=q>0
    h=float(-np.sum(q[nz]*np.log(q[nz])))
    return float(1-h/math.log(b.shape[0]-1))

def perm_cols(x,seed):
    x=np.asarray(x,float)
    rng=np.random.default_rng(seed)
    order=np.argsort(rng.random(x.shape),axis=0,kind="mergesort")
    cols=np.arange(x.shape[1])[None,:]
    return x[order,cols]

def sign_two(vals):
    v=np.asarray(vals,float);v=v[np.isfinite(v)]
    pos=int((v>0).sum());neg=int((v<0).sum());ties=int((v==0).sum());n=pos+neg
    if n==0:return pos,neg,ties,np.nan
    k=min(pos,neg)
    tail=sum(math.comb(n,i) for i in range(k+1))/(2**n)
    return pos,neg,ties,min(1.0,2*tail)

def load_methylation(path,records,expected_probe_path):
    positions=[r["meth_pos"] for r in records]
    if len(set(positions))!=len(positions):raise ValueError("duplicate methylation positions")
    source_order=sorted(positions)
    source_to_record={p:i for i,p in enumerate(positions)}
    reorder=np.asarray([source_to_record[p] for p in source_order],dtype=int)
    inverse=np.empty_like(reorder);inverse[reorder]=np.arange(len(reorder))
    use=[0]+positions
    ids=[];blocks=[]
    for ch in pd.read_csv(path,sep="\t",header=None,skiprows=1,usecols=use,chunksize=96,engine="c",low_memory=False,
                          na_values=["","NA","N/A","NaN","nan","NULL","null"],keep_default_na=True):
        ids.extend(ch.iloc[:,0].astype(str).str.strip().str.strip('"').tolist())
        x=ch.iloc[:,1:].apply(pd.to_numeric,errors="coerce").to_numpy(dtype=np.float32,copy=True).T.copy()
        if x.shape[0]!=len(source_order):raise ValueError("selected-column count drift")
        blocks.append(x[inverse,:].copy())
    beta=np.concatenate(blocks,axis=1)
    expected=[x.strip() for x in Path(expected_probe_path).read_text().splitlines() if x.strip()]
    if ids!=expected:raise ValueError(f"exact C1 probe carrier/order drift source={len(ids)} expected={len(expected)}")
    if beta.shape!=(len(records),22601):raise ValueError(f"methylation shape drift {beta.shape}")
    finite=np.isfinite(beta)
    if finite.any() and (float(np.nanmin(beta))<0 or float(np.nanmax(beta))>1):raise ValueError("beta outside [0,1]")
    return beta,np.asarray(ids,dtype=object)

def draw_one(cancer,draw):
    pool=np.asarray(DATA["rows"][cancer],int)
    seed=stable_seed(NS,cancer,draw,"participants")
    sel=np.sort(np.random.default_rng(seed).choice(pool,size=N,replace=False))
    b=np.asarray(DATA["beta"][sel,:],float).copy()
    fin=np.isfinite(b)
    retain=fin.sum(axis=0)>=29
    if int(retain.sum())<20000:
        return {"cancer":cancer,"draw":draw,"status":"NOT_EVALUABLE_PROBE_SUPPORT","retained_probes":int(retain.sum())},sel
    b=b[:,retain]
    bad=~np.isfinite(b)
    if bad.any():
        med=np.nanmedian(b,axis=0)
        if not np.isfinite(med).all():raise ValueError("nonfinite retained median")
        b[bad]=np.broadcast_to(med,b.shape)[bad]

    purity=np.asarray(DATA["purity"][sel],float)
    leuk=np.asarray(DATA["leuk"][sel],float)
    zp=(purity-purity.mean())/purity.std(ddof=1)
    zl=(leuk-leuk.mean())/leuk.std(ddof=1)
    X=np.column_stack([np.ones(N),zp,zl])
    if np.linalg.matrix_rank(X)!=3:
        return {"cancer":cancer,"draw":draw,"status":"NOT_EVALUABLE_COVARIATE_RANK","retained_probes":int(retain.sum())},sel
    coef=np.linalg.lstsq(X,b,rcond=None)[0]
    fitted=X@coef
    resid=b-fitted

    sraw=modal_s(b)
    sind=modal_s(perm_cols(b,stable_seed(NS,cancer,draw,"raw_independent_null")))
    scomp=modal_s(fitted+perm_cols(resid,stable_seed(NS,cancer,draw,"composition_preserving_null")))
    sres=modal_s(resid)
    sresnull=modal_s(perm_cols(resid,stable_seed(NS,cancer,draw,"residual_independent_null")))
    draw_raw=sraw-sind
    draw_comp=sraw-scomp
    draw_res=sres-sresnull
    return {
        "cancer":cancer,"draw":draw,"status":"EVALUABLE","retained_probes":int(retain.sum()),
        "purity_mean":float(purity.mean()),"purity_sd":float(purity.std(ddof=1)),
        "leuk_mean":float(leuk.mean()),"leuk_sd":float(leuk.std(ddof=1)),
        "purity_leuk_r":float(np.corrcoef(purity,leuk)[0,1]),
        "s_raw":sraw,"s_independent_null":sind,"delta_raw":draw_raw,
        "s_composition_preserving_null":scomp,"delta_comp_preserved":draw_comp,
        "s_residual":sres,"s_residual_null":sresnull,"delta_residual":draw_res,
        "residual_retention":float(draw_res/draw_raw) if np.isfinite(draw_raw) and draw_raw>0 else np.nan,
    },sel

def one_cancer(cancer):
    rows=[];members=[]
    for d in range(DRAWS):
        r,sel=draw_one(cancer,d);rows.append(r)
        members.append({"cancer":cancer,"draw":d,"participants":"|".join(DATA["participants"][i] for i in sel)})
    return rows,members

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

    for path,expected,label in [(a.meth,METH_SHA,"methylation"),(a.purity,PURITY_SHA,"purity"),(a.leuk,LEUK_SHA,"leukocyte")]:
        got=sha256_file(path);print(label,got,flush=True)
        if got!=expected:raise ValueError(f"{label} SHA mismatch {got} != {expected}")
    ann_sha=sha256_file(a.annotation);print("annotation",ann_sha,flush=True)

    ann=read_annotation(a.annotation)
    meth_unique,meth_dups=header_primary_unique_from_line(first_line(a.meth),ann)
    rna_unique,rna_dups=header_primary_unique_from_line(first_line(a.rna_header),ann)
    purity=read_purity(a.purity)
    leuk=read_leuk(a.leuk)

    pool_by=defaultdict(list);records=[]
    for cancer in CANCERS:
        pids=sorted(
            pid for (c,pid) in set(meth_unique)&set(rna_unique)
            if c==cancer and pid in purity and pid in leuk and leuk[pid][0]==cancer
        )
        for pid in pids:
            records.append({
                "cancer":cancer,"participant":pid,"meth_pos":meth_unique[(cancer,pid)]["pos"],
                "purity":purity[pid],"leuk":leuk[pid][1]
            })
        pool_by[cancer]=pids

    eligibility=pd.DataFrame([{"cancer":c,"composition_complete_pool_n":len(pool_by[c]),"eligible_n30":len(pool_by[c])>=30} for c in CANCERS])
    eligibility.to_csv(a.out/"R1_H1_COMPOSITION_ELIGIBILITY.csv",index=False)
    got_eligible=sorted(eligibility.loc[eligibility.eligible_n30,"cancer"].tolist())
    if got_eligible!=EXPECTED_ELIGIBLE:
        raise ValueError(f"SOURCE_ELIGIBILITY_HOLD expected={EXPECTED_ELIGIBLE} got={got_eligible}")

    record_index={(r["cancer"],r["participant"]):i for i,r in enumerate(records)}
    rows_by={c:[record_index[(c,p)] for p in pool_by[c]] for c in got_eligible}
    beta,probe_ids=load_methylation(a.meth,records,a.c1_probes)
    DATA.update(
        beta=beta,
        rows=rows_by,
        participants=[r["participant"] for r in records],
        purity=np.asarray([r["purity"] for r in records],float),
        leuk=np.asarray([r["leuk"] for r in records],float),
    )

    allrows=[];members=[]
    with ThreadPoolExecutor(max_workers=max(1,min(a.workers,len(got_eligible)))) as ex:
        fut={ex.submit(one_cancer,c):c for c in got_eligible}
        for f in as_completed(fut):
            c=fut[f];rr,mm=f.result();allrows.extend(rr);members.extend(mm)
            print("completed",c,flush=True)

    df=pd.DataFrame(allrows).sort_values(["cancer","draw"])
    df.to_csv(a.out/"R1_H1_COMPOSITION_DRAW_METRICS.csv.gz",index=False,compression={"method":"gzip","mtime":0})
    pd.DataFrame(members).sort_values(["cancer","draw"]).to_csv(a.out/"R1_H1_COMPOSITION_MEMBERSHIP.csv.gz",index=False,compression={"method":"gzip","mtime":0})

    evaluable=df[df.status.eq("EVALUABLE")].copy()
    summary=[]
    for c,g in evaluable.groupby("cancer",sort=True):
        row={"cancer":c,"evaluable_draws":len(g),"pool_n":len(rows_by[c])}
        for col in ["retained_probes","delta_raw","delta_comp_preserved","delta_residual","residual_retention","purity_leuk_r"]:
            v=pd.to_numeric(g[col],errors="coerce").to_numpy(float);v=v[np.isfinite(v)]
            row[col+"_median"]=float(np.median(v)) if len(v) else np.nan
            row[col+"_q25"]=float(np.quantile(v,.25)) if len(v) else np.nan
            row[col+"_q75"]=float(np.quantile(v,.75)) if len(v) else np.nan
        summary.append(row)
    cs=pd.DataFrame(summary)
    cs.to_csv(a.out/"R1_H1_COMPOSITION_CANCER_SUMMARY.csv",index=False)
    if len(cs)!=30 or not (cs.evaluable_draws==DRAWS).all():
        raise ValueError("evaluable draw/cancer count drift")

    vals=cs["delta_comp_preserved_median"].to_numpy(float)
    pos,neg,ties,p=sign_two(vals)
    med=float(np.median(vals));q25=float(np.quantile(vals,.25));q75=float(np.quantile(vals,.75))
    disposition="R1_H1_MEASURED_COMPOSITION_ROBUST" if (med>0 and np.isfinite(p) and p<.05) else "R1_H1_MEASURED_COMPOSITION_SENSITIVE"

    global_summary={
        "schema":"biosystems-adversarial-r1-h1-composition-v1",
        "status":"COMPLETE",
        "role":"POST_RESULT_P0_Q_ADVERSARIAL_SENSITIVITY_CANNOT_RETROACTIVELY_PROMOTE",
        "disposition":disposition,
        "primary_metric":"cancer median S_raw - S_composition_preserving_null",
        "cancers":len(vals),"positive":pos,"negative":neg,"ties":ties,
        "pan_cancer_median":med,"pan_cancer_q25":q25,"pan_cancer_q75":q75,
        "exact_sign_test_p_two_sided":p,
        "secondary_median_residual_retention":float(np.nanmedian(cs["residual_retention_median"].to_numpy(float))),
        "expected_eligible_cancers":EXPECTED_ELIGIBLE,
        "draws_per_cancer":DRAWS,"n_per_draw":N,
        "seed_namespace":NS,
        "source_sha256":{
            "methylation":METH_SHA,"purity":PURITY_SHA,"leukocyte":LEUK_SHA,
            "rna_inherited_full_source_identity":RNA_INHERITED_SHA,"annotation_observed":ann_sha,
        },
        "claim_ceiling":"only tests linear structure captured by ABSOLUTE purity and methylation-derived leukocyte fraction; does not establish composition independence or remove batch, subtype, age, sex, ancestry, stromal, center, plate, or array effects",
    }
    (a.out/"R1_H1_COMPOSITION_GLOBAL_SUMMARY.json").write_text(json.dumps(global_summary,indent=2,sort_keys=True)+"\n")

    prov={
        "methylation_duplicate_participants_excluded":len(meth_dups),
        "rna_duplicate_participants_excluded":len(rna_dups),
        "record_count_loaded":len(records),
        "annotation_sha256":ann_sha,
        "eligibility":eligibility.to_dict("records"),
    }
    (a.out/"R1_H1_COMPOSITION_PROVENANCE.json").write_text(json.dumps(prov,indent=2,sort_keys=True)+"\n")

    hashes=[]
    for pth in sorted(a.out.glob("*")):
        if pth.is_file():
            hashes.append({"file":pth.name,"bytes":pth.stat().st_size,"sha256":sha256_file(pth)})
    (a.out/"R1_H1_COMPOSITION_SHA256.json").write_text(json.dumps(hashes,indent=2)+"\n")
    print(json.dumps(global_summary,indent=2,sort_keys=True),flush=True)

if __name__=="__main__":
    main()
