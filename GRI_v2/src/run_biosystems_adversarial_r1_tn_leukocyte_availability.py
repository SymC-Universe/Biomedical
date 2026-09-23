#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path
from collections import Counter
import numpy as np
import pandas as pd

EXP_SHA="5a8268caedbf8dc98a75be0528d583238d7355761d9fc746e42002f223a982d9"
A1="BRCA COAD HNSC KIRC KIRP LIHC LUAD LUSC PRAD STAD THCA UCEC".split()
P20="BRCA COAD HNSC KICH KIRC KIRP LIHC LUAD LUSC PRAD STAD THCA UCEC".split()
TCGA_RE=re.compile(r"^(TCGA-[A-Z0-9]{2}-[A-Z0-9]{4})-([0-9]{2})[A-Z]?",re.I)

def sha256(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(8*1024*1024),b""):h.update(b)
    return h.hexdigest()

def parse(v):
    s=str(v).strip().upper().replace(".","-")
    m=TCGA_RE.match(s)
    if not m:return None
    return m.group(1),m.group(2)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--leuk",required=True,type=Path)
    ap.add_argument("--out",required=True,type=Path)
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    got=sha256(a.leuk)
    if got!=EXP_SHA:raise SystemExit(f"SHA mismatch {got}")
    d=pd.read_csv(a.leuk,sep="\t",header=None,names=["cancer","sample","value"],dtype=str)
    d["parsed"]=d["sample"].map(parse)
    d=d[d.parsed.notna()].copy()
    d["participant"]=d.parsed.map(lambda z:z[0])
    d["stype"]=d.parsed.map(lambda z:z[1])
    d["value_num"]=pd.to_numeric(d["value"],errors="coerce")
    rows=[]
    pair_rows=[]
    for cancer in sorted(set(A1)|set(P20)):
        sub=d[d.cancer.eq(cancer)].copy()
        for st in ["01","11"]:
            x=sub[sub.stype.eq(st)]
            finite=x[x.value_num.notna()]
            part_counts=finite.groupby("participant").size()
            vals=finite.value_num.to_numpy(float)
            rows.append({
                "cancer":cancer,"sample_type":st,
                "source_rows":int(len(x)),
                "finite_rows":int(len(finite)),
                "unique_finite_participants":int(finite.participant.nunique()),
                "duplicate_finite_participants":int((part_counts>1).sum()),
                "value_min":float(np.min(vals)) if len(vals) else None,
                "value_median":float(np.median(vals)) if len(vals) else None,
                "value_max":float(np.max(vals)) if len(vals) else None,
            })
        t=set(sub[(sub.stype=="01") & sub.value_num.notna()].participant)
        n=set(sub[(sub.stype=="11") & sub.value_num.notna()].participant)
        pair_rows.append({
            "cancer":cancer,
            "finite_tumor_participants":len(t),
            "finite_normal_participants":len(n),
            "finite_paired_participants":len(t&n),
            "in_tn_a1":cancer in A1,
            "in_tn_p20":cancer in P20,
            "leuk_tn_symmetric_eligible":bool(cancer in A1 and len(t)>=30 and len(n)>=30),
            "leuk_paired20_eligible":bool(cancer in P20 and len(t&n)>=20),
        })
    s=pd.DataFrame(rows);p=pd.DataFrame(pair_rows)
    s.to_csv(a.out/"R1_TN_LEUKOCYTE_SAMPLETYPE_COUNTS.csv",index=False)
    p.to_csv(a.out/"R1_TN_LEUKOCYTE_ELIGIBILITY.csv",index=False)
    sym=p[p.leuk_tn_symmetric_eligible].cancer.tolist()
    pair=p[p.leuk_paired20_eligible].cancer.tolist()
    if len(sym)==len(A1) and len(pair)==len(P20):
        disp="SYMMETRIC_LEUKOCYTE_SENSITIVITY_FEASIBLE"
    elif len(sym) or len(pair):
        disp="PARTIAL_SYMMETRIC_LEUKOCYTE_COVERAGE"
    else:
        disp="NO_SYMMETRIC_LEUKOCYTE_ROUTE"
    summary={
      "schema":"biosystems-adversarial-r1-tn-leukocyte-availability-v1",
      "status":"COMPLETE",
      "source_sha256":got,
      "molecular_architecture_values_opened":False,
      "tn_a1_cancers":A1,
      "tn_p20_cancers":P20,
      "symmetric_n30_cancers":sym,
      "paired_n20_cancers":pair,
      "disposition":disp,
      "claim_ceiling":"source availability only; does not remove tissue-composition confounding"
    }
    (a.out/"R1_TN_LEUKOCYTE_AVAILABILITY_SUMMARY.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
    print(json.dumps(summary,indent=2,sort_keys=True))
if __name__=="__main__":main()
