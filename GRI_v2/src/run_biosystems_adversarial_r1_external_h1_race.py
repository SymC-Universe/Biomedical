#!/usr/bin/env python3
from __future__ import annotations

import argparse, json, hashlib
from pathlib import Path
import numpy as np
import pandas as pd

from src.run_biosystems_external_prostate_p1 import (
    EXPECTED,
    sha256_file,
    load_c1_support,
    read_external_methylation,
    symmetric_probe_rules,
    h1_nulls,
    endpoint_row,
)

R1_NAMESPACE = "GRI_BIOSYS_EXT_PROSTATE_R1_H1_RACE_20260923"


def parse_race(headers):
    out=[]
    for h in headers:
        s=str(h).upper()
        if s.endswith("_AA"):
            out.append("AA")
        elif s.endswith("_EA"):
            out.append("EA")
        else:
            raise ValueError(f"unresolved race suffix in source header: {h}")
    return np.asarray(out,dtype=object)


def residualize_race(beta, race):
    race=np.asarray(race,dtype=object)
    levels=sorted(set(race.tolist()))
    if levels != ["AA","EA"]:
        raise ValueError(f"race residualization requires AA+EA, got {levels}")
    x=np.column_stack([np.ones(len(race),float),(race=="EA").astype(float)])
    rank=np.linalg.matrix_rank(x)
    if rank != 2:
        raise ValueError(f"race design rank {rank} != 2")
    coef=np.linalg.lstsq(x,np.asarray(beta,float),rcond=None)[0]
    resid=np.asarray(beta,float)-x@coef
    return resid


def one_lane(label, source, participant_ids, c1_probe_ids, c1_mask, workers):
    m=read_external_methylation(source,c1_probe_ids,participant_ids)
    common_keep,bt,bn=symmetric_probe_rules(m["tumor"],m["normal"])
    pids=m["probe_ids"][common_keep]
    mask_lookup={str(p):bool(v) for p,v in zip(c1_probe_ids,c1_mask)}
    mask=np.asarray([mask_lookup[str(p)] for p in pids],dtype=bool)
    race=parse_race(m["tumor_headers"])

    rows=[]
    for track,keep in {
        "PRIMARY_PUBLICATION":np.ones(len(pids),dtype=bool),
        "MASKED_TECHNICAL":~mask,
    }.items():
        b=bt[:,keep]

        # Exact raw reconstruction: same original namespace/lane/track => same null stream.
        obs_raw,null_raw=h1_nulls(
            b,
            "GRI_BIOSYS_EXT_PROSTATE_P1_20260922",
            label,
            track,
            workers=workers,
        )
        rr=endpoint_row("H1_RAW_RECONSTRUCTION",obs_raw,null_raw)
        rr.update(lane=label,track=track,n=int(b.shape[0]),probe_count=int(b.shape[1]),
                  race_AA=int(np.sum(race=="AA")),race_EA=int(np.sum(race=="EA")))
        rows.append(rr)

        resid=residualize_race(b,race)
        obs_r,null_r=h1_nulls(
            resid,
            R1_NAMESPACE,
            label+"_RACE_RESIDUAL",
            track,
            workers=workers,
        )
        r=endpoint_row("H1_RACE_RESIDUAL",obs_r,null_r)
        r.update(lane=label,track=track,n=int(b.shape[0]),probe_count=int(b.shape[1]),
                 race_AA=int(np.sum(race=="AA")),race_EA=int(np.sum(race=="EA")),
                 raw_effect=float(rr["effect"]),
                 effect_retention_fraction=float(r["effect"]/rr["effect"]) if rr["effect"]!=0 else np.nan,
                 passes_p05=bool(r["effect"]>0 and r["p_upper"]<=0.05))
        rows.append(r)

        aa=(race=="AA")
        if int(aa.sum())>=20:
            baa=b[aa,:]
            obs_a,null_a=h1_nulls(
                baa,
                R1_NAMESPACE,
                label+"_AA_ONLY",
                track,
                workers=workers,
            )
            a=endpoint_row("H1_AA_ONLY",obs_a,null_a)
            a.update(lane=label,track=track,n=int(baa.shape[0]),probe_count=int(baa.shape[1]),
                     race_AA=int(aa.sum()),race_EA=0,
                     passes_p05=bool(a["effect"]>0 and a["p_upper"]<=0.05))
            rows.append(a)

    return rows, {
        "lane":label,
        "n":int(bt.shape[0]),
        "common_probe_count":int(common_keep.sum()),
        "masked_removed":int(mask.sum()),
        "race_AA":int(np.sum(race=="AA")),
        "race_EA":int(np.sum(race=="EA")),
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",required=True,type=Path)
    ap.add_argument("--m450",required=True,type=Path)
    ap.add_argument("--epic",required=True,type=Path)
    ap.add_argument("--c1-probes",required=True,type=Path)
    ap.add_argument("--support",required=True,type=Path)
    ap.add_argument("--out",required=True,type=Path)
    ap.add_argument("--workers",type=int,default=4)
    a=ap.parse_args()
    a.out.mkdir(parents=True,exist_ok=True)

    for label,path in [("m450",a.m450),("epic",a.epic)]:
        got=sha256_file(path)
        if got!=EXPECTED[label]:
            raise ValueError(f"{label} SHA mismatch {got} != {EXPECTED[label]}")

    cfg=json.loads(a.config.read_text())
    c1_probe_ids,c1_mask,_=load_c1_support(a.c1_probes,a.support)

    lanes=[
        ("PRIMARY_450K_N30",a.m450,cfg["primary_450k"]["selected_participants"]),
        ("SENSITIVITY_450K_N32",a.m450,cfg["primary_450k"]["complete_pair_pool"]),
        ("SENSITIVITY_EPIC_N26",a.epic,cfg["epic_sensitivity"]["participants"]),
    ]

    rows=[]; diags=[]
    for label,src,parts in lanes:
        z,d=one_lane(label,src,parts,c1_probe_ids,c1_mask,a.workers)
        rows.extend(z); diags.append(d)
        print("completed",label,d,flush=True)

    df=pd.DataFrame(rows)
    df.to_csv(a.out/"R1_EXTERNAL_H1_RACE_SENSITIVITY.csv",index=False)

    primary=df[(df.lane=="PRIMARY_450K_N30")&(df.track=="PRIMARY_PUBLICATION")&(df.endpoint=="H1_RACE_RESIDUAL")]
    if len(primary)!=1:
        raise ValueError("primary race-residual H1 row missing")
    pr=primary.iloc[0]
    primary_status="R1_H1_RACE_ROBUST" if bool(pr.passes_p05) else "R1_H1_RACE_SENSITIVE"

    epic=df[(df.lane=="SENSITIVITY_EPIC_N26")&(df.track=="PRIMARY_PUBLICATION")&(df.endpoint=="H1_RACE_RESIDUAL")]
    if len(epic)!=1:
        raise ValueError("EPIC race-residual H1 row missing")
    er=epic.iloc[0]
    cross_platform=bool(pr.passes_p05 and er.passes_p05)

    summary={
        "schema":"biosystems-adversarial-r1-external-h1-race-v1",
        "status":"COMPLETE",
        "role":"POST_RESULT_ADVERSARIAL_SENSITIVITY_CANNOT_RESCUE_ORIGINAL_P1",
        "primary_status":primary_status,
        "cross_platform_race_residual_support":cross_platform,
        "diagnostics":diags,
        "primary_row":pr.to_dict(),
        "epic_row":er.to_dict(),
        "source_sha256":{"m450":EXPECTED["m450"],"epic":EXPECTED["epic"]},
        "B":999,
        "namespace":R1_NAMESPACE,
        "claim_ceiling":"tests known AA/EA axis only; does not adjust purity, age, sex, center, plate, batch, or other composition",
    }
    (a.out/"R1_EXTERNAL_H1_RACE_SUMMARY.json").write_text(json.dumps(summary,indent=2,sort_keys=True,default=lambda x: x.item() if hasattr(x,"item") else str(x))+"\n")

    hashes=[]
    for p in sorted(a.out.glob("*")):
        if p.is_file():
            h=hashlib.sha256(p.read_bytes()).hexdigest()
            hashes.append({"file":p.name,"bytes":p.stat().st_size,"sha256":h})
    (a.out/"R1_EXTERNAL_H1_RACE_SHA256.json").write_text(json.dumps(hashes,indent=2)+"\n")
    print(json.dumps(summary,indent=2,sort_keys=True,default=str),flush=True)


if __name__=="__main__":
    main()
