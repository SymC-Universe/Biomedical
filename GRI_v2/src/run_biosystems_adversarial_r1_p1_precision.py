#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd

from src import run_biosystems_external_prostate_p1 as p1

B_NEW=9999

def run_lane(beta_t,beta_n,probe_ids_all,mask_all,rna_t,genes,core_raw,modules,ns,lane,workers):
    p1.B=B_NEW
    result, nulls, diag = p1.run_architecture_lane(
        beta_t,beta_n,probe_ids_all,mask_all,rna_t,genes,core_raw,modules,ns,lane,workers
    )
    return result,nulls,diag

def status_map(result):
    return {
        tr:{r["endpoint"]:bool(r.get("passes_q05",False)) for r in rows if r["endpoint"] in {"H1","H2","H3a"}}
        for tr,rows in result.items()
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",required=True,type=Path)
    ap.add_argument("--rna",required=True,type=Path)
    ap.add_argument("--m450",required=True,type=Path)
    ap.add_argument("--epic",required=True,type=Path)
    ap.add_argument("--gmt",required=True,type=Path)
    ap.add_argument("--c1-probes",required=True,type=Path)
    ap.add_argument("--support",required=True,type=Path)
    ap.add_argument("--out",required=True,type=Path)
    ap.add_argument("--workers",type=int,default=4)
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    cfg=json.loads(a.config.read_text());ns=cfg["seed_namespace"]

    for label,path in [("rna",a.rna),("m450",a.m450),("epic",a.epic),("gmt",a.gmt)]:
        got=p1.sha256_file(path)
        if got!=p1.EXPECTED[label]:
            raise ValueError(f"{label} SHA mismatch {got} != {p1.EXPECTED[label]}")

    modules=p1.parse_gmt(a.gmt)
    c1_probe_ids,c1_mask,core_raw=p1.load_c1_support(a.c1_probes,a.support)
    mask_lookup={str(p):bool(m) for p,m in zip(c1_probe_ids,c1_mask)}
    aligned=lambda pids: np.asarray([mask_lookup[str(p)] for p in pids],dtype=bool)

    primary_parts=cfg["primary_450k"]["selected_participants"]
    epic_parts=cfg["epic_sensitivity"]["participants"]

    m30=p1.read_external_methylation(a.m450,c1_probe_ids,primary_parts)
    r30=p1.read_external_rna(a.rna,primary_parts,modules)
    primary,pnull,pdiag=run_lane(
        m30["tumor"],m30["normal"],m30["probe_ids"],aligned(m30["probe_ids"]),
        r30["tumor"],r30["genes"],core_raw,modules,ns,"PRIMARY_450K_N30",a.workers
    )

    me=p1.read_external_methylation(a.epic,c1_probe_ids,epic_parts)
    re=p1.read_external_rna(a.rna,epic_parts,modules)
    epic,enull,ediag=run_lane(
        me["tumor"],me["normal"],me["probe_ids"],aligned(me["probe_ids"]),
        re["tumor"],re["genes"],core_raw,modules,ns,"SENSITIVITY_EPIC_N26",a.workers
    )

    original_status={
      "PRIMARY_450K_N30":{
        "PRIMARY_PUBLICATION":{"H1":True,"H2":False,"H3a":False},
        "MASKED_TECHNICAL":{"H1":True,"H2":False,"H3a":False},
      },
      "SENSITIVITY_EPIC_N26":{
        "PRIMARY_PUBLICATION":{"H1":True,"H2":False,"H3a":False},
        "MASKED_TECHNICAL":{"H1":True,"H2":False,"H3a":False},
      },
    }
    got={"PRIMARY_450K_N30":status_map(primary),"SENSITIVITY_EPIC_N26":status_map(epic)}
    disposition="R1_P1_PRECISION_CONCORDANT" if got==original_status else "R1_P1_PRECISION_STATUS_CONFLICT"

    pd.DataFrame(p1.flatten_endpoint_rows(primary)).to_csv(a.out/"R1_P1_PRECISION_PRIMARY_450K_N30.csv",index=False)
    pd.DataFrame(p1.flatten_endpoint_rows(epic)).to_csv(a.out/"R1_P1_PRECISION_EPIC_N26.csv",index=False)
    np.savez_compressed(a.out/"R1_P1_PRECISION_PRIMARY_NULLS.npz",**{f"{tr}_{e}":v for tr,z in pnull.items() for e,v in z.items()})
    np.savez_compressed(a.out/"R1_P1_PRECISION_EPIC_NULLS.npz",**{f"{tr}_{e}":v for tr,z in enull.items() for e,v in z.items()})
    summary={
      "schema":"biosystems-adversarial-r1-p1-precision-v1",
      "status":"COMPLETE",
      "role":"POST_RESULT_MONTE_CARLO_PRECISION_ONLY",
      "B_original":999,
      "B_precision":B_NEW,
      "seed_namespace":ns,
      "deterministic_stream_nested":True,
      "disposition":disposition,
      "status_map":got,
      "primary_endpoints":primary["PRIMARY_PUBLICATION"],
      "primary_masked":primary["MASKED_TECHNICAL"],
      "epic_endpoints":epic["PRIMARY_PUBLICATION"],
      "epic_masked":epic["MASKED_TECHNICAL"],
      "source_sha256":p1.EXPECTED,
      "claim_ceiling":"higher Monte Carlo precision for the same P1 nulls only; no change to original P1 classification, confound control, or biological interpretation",
    }
    (a.out/"R1_P1_PRECISION_SUMMARY.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
    print(json.dumps(summary,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
