#!/usr/bin/env python3
from __future__ import annotations
import argparse, gzip, hashlib, itertools, json, math
from pathlib import Path
import numpy as np
import pandas as pd

TRAJ = ["Control","D3","D8","D13","D21","D29","D33","D38","D59",
        "dr29.D4","dr29.D10","dr29.D15","dr29.D17","dr29.D30","dr29.D35"]
POST = [("dr29.D4",4),("dr29.D10",10),("dr29.D15",15),("dr29.D17",17),("dr29.D30",30),("dr29.D35",35)]

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024), b""): h.update(b)
    return h.hexdigest()

def spearman(x,y):
    xr=pd.Series(x).rank(method="average").to_numpy(float)
    yr=pd.Series(y).rank(method="average").to_numpy(float)
    if np.std(xr)==0 or np.std(yr)==0: return float("nan")
    return float(np.corrcoef(xr,yr)[0,1])

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",type=Path,required=True)
    ap.add_argument("--freeze",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    a=ap.parse_args()
    a.out.mkdir(parents=True,exist_ok=True)
    cfg=json.loads(a.freeze.read_text())
    got=sha256(a.source)
    exp=cfg["source"]["sha256"]
    if got!=exp: raise SystemExit(f"SOURCE_SHA_MISMATCH {got} != {exp}")

    df=pd.read_csv(a.source,sep="\t",compression="gzip",low_memory=False)
    miss=[c for c in TRAJ if c not in df.columns]
    if miss: raise SystemExit(f"MISSING_TRAJECTORY_COLUMNS {miss}")
    x=df[TRAJ].apply(pd.to_numeric,errors="coerce").to_numpy(float)
    keep=np.all(np.isfinite(x) & (x>=0),axis=1)
    xr=x[keep]
    if xr.shape[0] < 1000: raise SystemExit(f"TOO_FEW_RETAINED_GENES {xr.shape[0]}")
    z=np.log2(xr+1.0)
    base=z[:,0]
    d={}
    for j,c in enumerate(TRAJ):
        d[c]=float(np.median(np.abs(z[:,j]-base)))

    days=np.array([day for _,day in POST],float)
    vals=np.array([d[c] for c,_ in POST],float)
    rho=spearman(days,vals)
    perm=[]
    for p in itertools.permutations(vals.tolist()):
        perm.append(spearman(days,np.asarray(p,float)))
    perm=np.asarray(perm,float)
    p_exact=float(np.mean(perm <= rho))
    d4=d["dr29.D4"]; d35=d["dr29.D35"]; d59=d["D59"]
    cond={
        "rho_negative": bool(rho < 0),
        "exact_p_le_0_05": bool(p_exact <= 0.05),
        "D35_lt_D4": bool(d35 < d4),
        "D35_lt_D59": bool(d35 < d59),
    }
    if all(cond.values()):
        status="RECOVERY_DYNAMIC_SUPPORTED"
    elif d35 < d4 and d35 < d59:
        status="PARTIAL_RECOVERY_SIGNAL"
    else:
        status="PERSISTENT_OR_REORGANIZED"

    rows=[]
    for c in TRAJ:
        phase="baseline" if c=="Control" else ("drug_removed" if c.startswith("dr29.") else "drug_on")
        row={"column":c,"phase":phase,"displacement_from_D0":d[c]}
        if c.startswith("dr29."):
            row["days_after_removal"]=dict(POST)[c]
        rows.append(row)
    pd.DataFrame(rows).to_csv(a.out/"SU2026_SIMPLE_RECOVERY_TRAJECTORY_V01.csv",index=False)

    out={
        "schema_version":"0.1",
        "status":status,
        "source_sha256":got,
        "retained_gene_count":int(xr.shape[0]),
        "total_source_rows":int(x.shape[0]),
        "metric":cfg["metric"],
        "trajectory_displacement":d,
        "post_removal_days":days.tolist(),
        "post_removal_displacement":vals.tolist(),
        "spearman_rho":rho,
        "exact_one_sided_permutation_p":p_exact,
        "permutation_count":int(len(perm)),
        "conditions":cond,
        "D4":d4,
        "D35":d35,
        "D59":d59,
        "recovery_fraction_1_minus_D35_over_D59": None if d59==0 else float(1-d35/d59),
        "claim_ceiling":cfg["claim_ceiling"],
    }
    (a.out/"SU2026_SIMPLE_RECOVERY_RESULT_V01.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
