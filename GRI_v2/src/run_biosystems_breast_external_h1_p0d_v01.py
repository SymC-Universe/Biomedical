#!/usr/bin/env python3
from __future__ import annotations
import argparse, base64, csv, gzip, hashlib, itertools, json, lzma, math
from pathlib import Path
import numpy as np
import pandas as pd

C1_PROBE_IDS_SHA="589365b92797f6e0ea479b75437c44ed86327cfc86b3e7caf7df01b4be2bcdd9"
SUPPORT_B64_SHA="1463a4a6ad157dc770278ef97b6fcd2fb80b6e73ce4d774a2ca47aa7870391b"
SUPPORT_RAW_SHA="d45947345007b901e684adf92840889acf1ab00377153d54de2766cd1084c9b2"
NS="BIOSYSTEMS_BREAST_H1_EXTERNAL_V01"

def sha256_file(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def stable_seed(*tokens)->int:
    s="|".join(map(str,tokens)).encode()
    return int.from_bytes(hashlib.sha256(s).digest()[:8],"big")%(2**32)

def load_support(probe_path:Path,support_path:Path):
    if sha256_file(probe_path)!=C1_PROBE_IDS_SHA: raise SystemExit("C1_PROBE_SHA_MISMATCH")
    pids=[x.strip() for x in probe_path.read_text().splitlines() if x.strip()]
    if len(pids)!=22601 or len(set(pids))!=22601: raise SystemExit(f"C1_PROBE_COUNT_DRIFT {len(pids)}")
    b=support_path.read_bytes()
    support_sha=hashlib.sha256(b).hexdigest()
    try:
        raw=lzma.decompress(base64.b64decode(b))
    except Exception as e:
        raise SystemExit(f"SUPPORT_DECODE_FAIL {e}")
    lines=raw.decode("utf-8").splitlines()
    if not lines or lines[0]!="CORE" or "MASK" not in lines:
        raise SystemExit("SUPPORT_SCHEMA_DRIFT")
    k=lines.index("MASK")
    core_rows=[x for x in lines[1:k] if x]
    mask=set(x for x in lines[k+1:] if x)
    if len(core_rows)!=3999: raise SystemExit(f"SUPPORT_CORE_COUNT_DRIFT {len(core_rows)}")
    if len(mask)!=579: raise SystemExit(f"SUPPORT_MASK_COUNT_DRIFT {len(mask)}")
    if len(mask.intersection(set(pids)))!=579: raise SystemExit("SUPPORT_MASK_NOT_ALIGNED_TO_C1_CARRIER")
    return np.asarray(pids,dtype=object),mask,support_sha,hashlib.sha256(raw).hexdigest()

def unquote_fields(line:str):
    return next(csv.reader([line],delimiter="\t",quotechar='"'))

def parse_matrix_metadata(path:Path):
    sample_accessions=[]; sample_titles=[]; char_lines=[]
    table_header=None
    with gzip.open(path,"rt",encoding="utf-8",errors="replace",newline="") as f:
        for line in f:
            if line.startswith("!Sample_geo_accession"):
                sample_accessions=unquote_fields(line.rstrip("\r\n"))[1:]
            elif line.startswith("!Sample_title"):
                sample_titles=unquote_fields(line.rstrip("\r\n"))[1:]
            elif line.startswith("!Sample_characteristics_ch1"):
                char_lines.append(unquote_fields(line.rstrip("\r\n"))[1:])
            elif line.startswith("!series_matrix_table_begin"):
                table_header=unquote_fields(next(f).rstrip("\r\n"))
                break
    if not sample_accessions or not table_header: raise SystemExit("SERIES_METADATA_INCOMPLETE")
    n=len(sample_accessions)
    if sample_titles and len(sample_titles)!=n: raise SystemExit("TITLE_COUNT_MISMATCH")
    rec={g:{"gsm":g,"title":sample_titles[i] if sample_titles else ""} for i,g in enumerate(sample_accessions)}
    for row in char_lines:
        if len(row)!=n: continue
        for i,val in enumerate(row):
            if ":" not in val: continue
            key,v=val.split(":",1)
            rec[sample_accessions[i]][key.strip().lower()]=v.strip()
    return rec,table_header

def pair_map(meta):
    by={}
    for gsm,r in meta.items():
        pid=r.get("unique patient id","").strip()
        st=r.get("sample type","").strip().lower()
        if not pid or st not in {"primary tumor","lymph node metastasis"}: continue
        by.setdefault(pid,{})[st]=gsm
    complete={p:z for p,z in by.items() if set(z)=={"primary tumor","lymph node metastasis"}}
    if len(complete)!=44: raise SystemExit(f"EXPECTED_44_COMPLETE_PAIRS_GOT_{len(complete)}")
    return complete

def select30(pairs):
    ranked=sorted(pairs,key=lambda p:hashlib.sha256(f"{NS}|{p}".encode()).hexdigest())
    return ranked[:30]

def read_selected(path,required_probe_order,gsms):
    target=set(map(str,required_probe_order))
    values={}
    with gzip.open(path,"rt",encoding="utf-8",errors="replace",newline="") as f:
        in_table=False; header=None; idx=None
        for line in f:
            if line.startswith("!series_matrix_table_begin"):
                header=unquote_fields(next(f).rstrip("\r\n"))
                pos={h:i for i,h in enumerate(header)}
                miss=[g for g in gsms if g not in pos]
                if miss: raise SystemExit(f"GSM_MISSING_FROM_TABLE {miss[:5]}")
                idx=[pos[g] for g in gsms]
                in_table=True
                continue
            if not in_table: continue
            if line.startswith("!series_matrix_table_end"): break
            parts=unquote_fields(line.rstrip("\r\n"))
            if not parts: continue
            pid=parts[0]
            if pid not in target: continue
            row=[]
            for j in idx:
                try: row.append(float(parts[j]))
                except Exception: row.append(np.nan)
            values[pid]=row
    keep=[str(p) for p in required_probe_order if str(p) in values]
    if len(keep)<20000: raise SystemExit(f"LOW_C1_OVERLAP {len(keep)}")
    return np.asarray(keep,dtype=object),np.asarray([values[p] for p in keep],float).T

def symmetric_rules(a,b):
    ka=np.isfinite(a).sum(0)/a.shape[0]>=0.95
    kb=np.isfinite(b).sum(0)/b.shape[0]>=0.95
    keep=ka&kb
    am=np.nanmedian(a[:,keep],axis=0); bm=np.nanmedian(b[:,keep],axis=0)
    aa=a[:,keep].copy(); bb=b[:,keep].copy()
    bad=~np.isfinite(aa)
    if bad.any(): aa[bad]=np.broadcast_to(am,aa.shape)[bad]
    bad=~np.isfinite(bb)
    if bad.any(): bb[bad]=np.broadcast_to(bm,bb.shape)[bad]
    return keep,aa,bb

def centered(x): return x-x.mean(0,keepdims=True)

def spectral_concentration(x):
    xc=centered(x); n,p=xc.shape
    g=(xc@xc.T)/float(p)
    vals=np.linalg.eigvalsh(g)[::-1]
    vals=np.where(vals<0,0,vals)[:n-1]
    if vals.sum()<=0:return float("nan")
    q=vals/vals.sum(); nz=q>0
    h=-float(np.sum(q[nz]*np.log(q[nz])))
    return float(1-h/math.log(n-1))

def permute_columns(xc,seed):
    rng=np.random.default_rng(seed); n,p=xc.shape
    idx=np.broadcast_to(np.arange(n,dtype=np.int16)[:,None],(n,p)).copy()
    cols=np.arange(p)
    for i in range(n-1,0,-1):
        j=rng.integers(0,i+1,size=p)
        tmp=idx[i].copy(); idx[i]=idx[j,cols]; idx[j,cols]=tmp
    return xc[idx,cols[None,:]]

def h1(beta,label,B):
    xc=centered(beta); obs=spectral_concentration(beta)
    null=np.empty(B,float)
    for r in range(B):
        null[r]=spectral_concentration(permute_columns(xc,stable_seed(NS,label,r)))
    med=float(np.median(null)); effect=float(obs-med)
    p=float((1+np.sum(null>=obs))/(B+1))
    return {"label":label,"n":int(beta.shape[0]),"probes":int(beta.shape[1]),"B":B,
            "observed":float(obs),"null_median":med,"effect":effect,"p_upper":p,
            "direction_positive":bool(effect>0)}

def run_lane(path,pids,probe_ids,mask_set,B,label_prefix):
    gsms=[]
    # placeholder, caller supplies global pair map via closure
    raise RuntimeError

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--matrix",type=Path,required=True)
    ap.add_argument("--c1-probes",type=Path,required=True)
    ap.add_argument("--support",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=True)
    probe_ids,mask_set,support_sha,support_raw_sha=load_support(a.c1_probes,a.support)
    meta,_=parse_matrix_metadata(a.matrix)
    pairs=pair_map(meta)
    p30=select30(pairs)
    p44=sorted(pairs)

    def extract(participants):
        prim=[pairs[p]["primary tumor"] for p in participants]
        meta_g=[pairs[p]["lymph node metastasis"] for p in participants]
        pids,x=read_selected(a.matrix,probe_ids,prim+meta_g)
        n=len(participants); A=x[:n]; B=x[n:]
        keep,A,B=symmetric_rules(A,B)
        p=pids[keep]
        mask=np.asarray([str(z) in mask_set for z in p],bool)
        return p,A,B,mask,prim,meta_g

    p30ids,A30,B30,m30,gp30,gm30=extract(p30)
    results=[]
    results.append(h1(A30,"PRIMARY_N30_PUBLICATION",999))
    results.append(h1(A30[:,~m30],"PRIMARY_N30_MASKED",999))
    results.append(h1(B30,"METASTASIS_PAIRED_N30_PUBLICATION",999))
    results.append(h1(B30[:,~m30],"METASTASIS_PAIRED_N30_MASKED",999))

    p44ids,A44,B44,m44,gp44,gm44=extract(p44)
    results.append(h1(A44,"PRIMARY_FULL_N44_PUBLICATION",199))
    results.append(h1(B44,"METASTASIS_FULL_N44_PUBLICATION",199))

    pd.DataFrame(results).to_csv(a.out/"BREAST_EXTERNAL_H1_ENDPOINTS_V01.csv",index=False)
    out={
      "schema_version":"0.1","status":"COMPLETE_P0D",
      "source":"GSE58999",
      "source_matrix_sha256":sha256_file(a.matrix),
      "support_payload_sha256":support_sha,
      "support_payload_decoded_sha256":support_raw_sha,
      "complete_pair_count":len(pairs),
      "selected_n30_participants":p30,
      "selection_rule":"first 30 patient IDs after ascending SHA256(BIOSYSTEMS_BREAST_H1_EXTERNAL_V01|patient_id)",
      "selected_primary_gsms":gp30,
      "selected_metastasis_gsms":gm30,
      "n30_common_probe_count":int(len(p30ids)),
      "n30_masked_removed":int(m30.sum()),
      "full_common_probe_count":int(len(p44ids)),
      "results":results,
      "primary_success":bool(results[0]["effect"]>0 and results[0]["p_upper"]<=0.01 and results[1]["effect"]>0 and results[4]["effect"]>0),
      "claim_ceiling":"P0-D second external within-methylation H1 transport only; not external H2/H3 transport, causality, recovery, or clinical utility"
    }
    (a.out/"BREAST_EXTERNAL_H1_RESULT_V01.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=="__main__": main()
