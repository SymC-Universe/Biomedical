#!/usr/bin/env python3
from __future__ import annotations
import argparse, base64, csv, gzip, hashlib, itertools, json, lzma, math
from pathlib import Path
import numpy as np
import pandas as pd

C1_PROBE_IDS_SHA="589365b92797f6e0ea479b75437c44ed86327cfc86b3e7caf7df01b4be2bcdd9"

def sha256_file(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def bh(vals):
    p=np.asarray(vals,float); o=np.argsort(p); r=p[o]
    q=np.minimum.accumulate((r*len(r)/np.arange(1,len(r)+1))[::-1])[::-1]
    q=np.minimum(q,1.0); out=np.empty_like(q); out[o]=q
    return out

def rank_average(x):
    return pd.Series(np.asarray(x,float)).rank(method="average").to_numpy(float)

def spearman(x,y):
    x=np.asarray(x,float); y=np.asarray(y,float)
    good=np.isfinite(x)&np.isfinite(y)
    if good.sum()<10:return np.nan
    xr=rank_average(x[good]); yr=rank_average(y[good])
    if np.std(xr)==0 or np.std(yr)==0:return np.nan
    return float(np.corrcoef(xr,yr)[0,1])

def kw_stat(values, labels):
    x=np.asarray(values,float); lab=np.asarray(labels,int)
    ranks=rank_average(x); n=len(x)
    H=0.0
    for g in sorted(set(lab)):
        rr=ranks[lab==g]; ng=len(rr)
        H += (rr.sum()**2)/ng
    H=12.0/(n*(n+1))*H-3*(n+1)
    # tie correction
    _,counts=np.unique(x,return_counts=True)
    denom=n**3-n
    if denom>0:
        C=1.0-float(np.sum(counts**3-counts))/denom
        if C>0:H/=C
    return float(H)

def exact_kw_p(values):
    vals=np.asarray(values,float)
    obs_lab=np.array([0,0,0,1,1,1,1,1,2,2,2])
    obs=kw_stat(vals,obs_lab)
    idx=set(range(11)); stats=[]
    for g0 in itertools.combinations(range(11),3):
        rem=sorted(idx-set(g0))
        for g1 in itertools.combinations(rem,5):
            lab=np.full(11,2,int); lab[list(g0)]=0; lab[list(g1)]=1
            stats.append(kw_stat(vals,lab))
    stats=np.asarray(stats,float)
    return obs,float(np.mean(stats>=obs-1e-15)),int(len(stats))

def load_support(probe_path:Path,support_path:Path):
    if sha256_file(probe_path)!=C1_PROBE_IDS_SHA: raise SystemExit("C1_PROBE_SHA_MISMATCH")
    probes=[x.strip() for x in probe_path.read_text().splitlines() if x.strip()]
    if len(probes)!=22601 or len(set(probes))!=22601: raise SystemExit("C1_PROBE_CARRIER_DRIFT")
    b=support_path.read_bytes(); raw=lzma.decompress(base64.b64decode(b))
    lines=raw.decode("utf-8").splitlines()
    if not lines or lines[0]!="CORE" or "MASK" not in lines: raise SystemExit("SUPPORT_SCHEMA_DRIFT")
    k=lines.index("MASK"); core={}
    for line in lines[1:k]:
        if not line:continue
        pid,genes=line.split("\t",1); core[pid]=[g for g in genes.split(";") if g]
    mask={x for x in lines[k+1:] if x}
    if len(core)!=3999 or len(mask)!=579: raise SystemExit(f"SUPPORT_SEMANTIC_DRIFT core={len(core)} mask={len(mask)}")
    return probes,core,mask,hashlib.sha256(b).hexdigest(),hashlib.sha256(raw).hexdigest()

def read_meth_matrix(path:Path, gsms, required_probes):
    target=set(required_probes); rows={}; header=None; idx=None
    with gzip.open(path,"rt",encoding="utf-8",errors="replace",newline="") as f:
        for line in f:
            if line.startswith("!series_matrix_table_begin"):
                header=next(csv.reader([next(f).rstrip("\r\n")],delimiter="\t",quotechar='"'))
                pos={h:i for i,h in enumerate(header)}
                miss=[g for g in gsms if g not in pos]
                if miss: raise SystemExit(f"METH_GSM_MISSING {miss}")
                idx=[pos[g] for g in gsms]
                break
        if header is None: raise SystemExit("METH_TABLE_HEADER_NOT_FOUND")
        for line in f:
            if line.startswith("!series_matrix_table_end"):break
            parts=next(csv.reader([line.rstrip("\r\n")],delimiter="\t",quotechar='"'))
            if not parts:continue
            pid=parts[0]
            if pid not in target:continue
            vals=[]
            for j in idx:
                try:vals.append(float(parts[j]))
                except Exception:vals.append(np.nan)
            rows[pid]=vals
    keep=[p for p in required_probes if p in rows]
    x=np.asarray([rows[p] for p in keep],float).T
    finite=np.all(np.isfinite(x),axis=0)
    keep=np.asarray(keep,dtype=object)[finite]; x=x[:,finite]
    if len(keep)<15000: raise SystemExit(f"LOW_FINITE_C1_SUPPORT {len(keep)}")
    return keep,x

def read_rna(path:Path, source_columns):
    df=pd.read_csv(path,sep="\t",compression="gzip",low_memory=False)
    if "GENE" not in df.columns: raise SystemExit("RNA_GENE_COLUMN_MISSING")
    miss=[g for g in source_columns if g not in df.columns]
    if miss: raise SystemExit(f"RNA_SOURCE_COLUMN_MISSING {miss}")
    raw=df["GENE"].astype(str).str.strip()
    symbol=raw.str.split("|",n=1,regex=False).str[0].str.strip()
    vals=df[source_columns].apply(pd.to_numeric,errors="coerce")
    tmp=vals.copy(); tmp.insert(0,"symbol",symbol)
    tmp=tmp.loc[(tmp["symbol"]!="")&(tmp["symbol"]!="?")&(tmp["symbol"].str.lower()!="nan")]
    # fixed duplicate rule: median per symbol per sample
    agg=tmp.groupby("symbol",sort=True)[source_columns].median()
    x=agg.to_numpy(float)
    med=np.nanmedian(x,axis=1,keepdims=True)
    mad=np.nanmedian(np.abs(x-med),axis=1)
    good=np.all(np.isfinite(x),axis=1)&np.isfinite(mad)&(mad>0)
    agg=agg.iloc[np.flatnonzero(good)]
    x=agg.to_numpy(float); med=np.median(x,axis=1,keepdims=True); mad=np.median(np.abs(x-med),axis=1,keepdims=True)
    rz=(x-med)/(1.4826*mad)
    return agg.index.to_numpy(dtype=object),rz.T

def phase_name(w):
    if w<=3:return "sensitive"
    if w<=8:return "resistance_acquisition"
    return "late_resistant"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--freeze",type=Path,required=True)
    ap.add_argument("--manifest",type=Path,required=True)
    ap.add_argument("--rna",type=Path,required=True)
    ap.add_argument("--methylation",type=Path,required=True)
    ap.add_argument("--c1-probes",type=Path,required=True)
    ap.add_argument("--support",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=True)
    cfg=json.loads(a.freeze.read_text()); man=json.loads(a.manifest.read_text())
    if sha256_file(a.rna)!=cfg["source"]["rna_sha256"]: raise SystemExit("RNA_SHA_MISMATCH")
    if sha256_file(a.methylation)!=cfg["source"]["methylation_sha256"]: raise SystemExit("METH_SHA_MISMATCH")
    probes,core,mask,support_sha,support_raw_sha=load_support(a.c1_probes,a.support)

    states=sorted(man["main_timecourse"],key=lambda z:(z["week"],0 if z["arm"]=="PBS" else 1))
    if len(states)!=22: raise SystemExit("MAIN_TIMECOURSE_COUNT_DRIFT")
    rna_gsms=[z["rna_gsm"] for z in states]; meth_gsms=[z["methylation_gsm"] for z in states]
    # The hash-bound processed RNA source uses source-native generation/arm columns rather than GSM names.
    # This mapping was established in the outcome-free chronic source audit before this extension.
    rna_source_columns=[f"C{z['week']}.PBS" if z["arm"]=="PBS" else f"C{z['week']}.100nM" for z in states]
    pids,mx=read_meth_matrix(a.methylation,meth_gsms,probes)
    genes,rx=read_rna(a.rna,rna_source_columns)

    # indexes are PBS,CTX within each week
    meth_dist=[]; rna_dist=[]; meth_delta=[]; rna_delta=[]
    for wi in range(11):
        p=2*wi; t=p+1
        md=mx[t]-mx[p]; rd=rx[t]-rx[p]
        meth_delta.append(md); rna_delta.append(rd)
        meth_dist.append(float(np.median(np.abs(md))))
        rna_dist.append(float(np.median(np.abs(rd))))
    meth_dist=np.asarray(meth_dist); rna_dist=np.asarray(rna_dist)
    mh,mp,mperm=exact_kw_p(meth_dist); rh,rp,rperm=exact_kw_p(rna_dist)
    q=bh([mp,rp])

    # promoter-core gene mapping over retained methylation probes
    pi={str(p):i for i,p in enumerate(pids)}
    gene_to_idx={}
    for pid,gs in core.items():
        i=pi.get(pid)
        if i is None:continue
        for g in gs:gene_to_idx.setdefault(g,[]).append(i)
    rg={str(g):i for i,g in enumerate(genes)}
    common=sorted(set(gene_to_idx)&set(rg))
    # require usable gene object
    m_gene=[]; r_gene=[]
    for w in range(11):
        md=meth_delta[w]; rd=rna_delta[w]
        mg=[]; rr=[]
        for g in common:
            idx=gene_to_idx[g]
            mg.append(float(np.median(md[idx])))
            rr.append(float(rd[rg[g]]))
        m_gene.append(np.asarray(mg,float)); r_gene.append(np.asarray(rr,float))
    if len(common)<500: raise SystemExit(f"LOW_PROMOTER_RNA_GENE_SUPPORT {len(common)}")

    forward=[]; reverse=[]
    for t in range(10):
        forward.append(abs(spearman(m_gene[t],r_gene[t+1])))
        reverse.append(abs(spearman(r_gene[t],m_gene[t+1])))
    f=np.asarray(forward,float); r=np.asarray(reverse,float)
    diff=f-r; obs=float(np.mean(diff))
    # exact within-transition direction swaps
    null=[]
    for bits in itertools.product([0,1],repeat=10):
        d=np.where(np.asarray(bits,bool),-diff,diff)
        null.append(float(np.mean(d)))
    null=np.asarray(null,float)
    pdir=float(np.mean(null>=obs-1e-15))
    dir_support=bool(obs>0 and pdir<=0.05)

    rows=[]
    for w in range(1,12):
        rows.append({"week":w,"phase":phase_name(w),"methylation_distance":meth_dist[w-1],"rna_distance":rna_dist[w-1]})
    pd.DataFrame(rows).to_csv(a.out/"SCC25_TREATMENT_RESPONSE_DISTANCES_V01.csv",index=False)
    pd.DataFrame({
        "transition":[f"{i}->{i+1}" for i in range(1,11)],
        "forward_abs_rho_meth_t_to_rna_t1":f,
        "reverse_abs_rho_rna_t_to_meth_t1":r,
        "forward_minus_reverse":diff
    }).to_csv(a.out/"SCC25_TEMPORAL_DIRECTION_V01.csv",index=False)

    result={
      "schema_version":"0.1","status":"COMPLETE_P0D",
      "source_sha256":{"rna":sha256_file(a.rna),"methylation":sha256_file(a.methylation),
                       "support_payload":support_sha,"support_decoded":support_raw_sha},
      "rna_gsm_to_source_column":[
        {"week":z["week"],"arm":z["arm"],"gsm":z["rna_gsm"],"source_column":col}
        for z,col in zip(states,rna_source_columns)
      ],
      "c1_probe_count_retained_all_22_states":int(len(pids)),
      "rna_gene_count_after_fixed_symbol_and_MAD_gate":int(len(genes)),
      "promoter_rna_common_gene_count":int(len(common)),
      "E2":{
        "methylation_distance":meth_dist.tolist(),"rna_distance":rna_dist.tolist(),
        "methylation_kw_H":mh,"methylation_exact_p":mp,"methylation_bh_q":float(q[0]),
        "rna_kw_H":rh,"rna_exact_p":rp,"rna_bh_q":float(q[1]),
        "permutation_count":mperm,
        "support_rule_pass":bool((q[0]<=0.05) or (q[1]<=0.05))
      },
      "E3":{
        "forward_abs_rho":f.tolist(),"reverse_abs_rho":r.tolist(),
        "mean_forward_minus_reverse":obs,
        "exact_one_sided_swap_p":pdir,
        "swap_count":int(len(null)),
        "support_rule_pass":dir_support,
        "claim_ceiling":cfg["E3"]["claim_ceiling"]
      }
    }
    (a.out/"SCC25_RESPONSE_DIRECTION_RESULT_V01.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=="__main__":main()
