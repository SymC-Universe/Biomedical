#!/usr/bin/env python3
"""Meneses 2026 immediate motor context-transport P0-Q test.

Frozen by MENESES2026_IMMEDIATE_CONTEXT_TRANSPORT_P0Q_V01_FREEZE.json.
"""
from __future__ import annotations
import itertools, json, math, sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist
from scipy.stats import spearmanr

import meneses2026_ecoli_pmf_recovery_p0q_v01 as base
from meneses2026_source_method_reconciliation_v01 import fit_immediate_manuscript

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"meneses2026_context_transport_results"
OUT.mkdir(parents=True,exist_ok=True)
CONCS=[200,300,400,500]
CONTEXTS={
 "sucrose_MB_CCW":{
  200:("data/time-series/bead/sucrose_200mM.parquet","41c7e7837d7f6e0418180d85ded212a102af0621",8),
  300:("data/time-series/bead/sucrose_300mM.parquet","78d915b2264dd6fa273ba061e605ee8597a28a06",10),
  400:("data/time-series/bead/sucrose_400mM.parquet","36ebcaa9c817ba8c11527e69d6f8b49669b1f2d6",8),
  500:("data/time-series/bead/sucrose_500mM.parquet","dd3b2ef0b1b77c43c02080c88080abb5b0cd3f61",12)},
 "sorbitol_MB_CCW":{
  200:("data/time-series/bead/sorbitol_200mM.parquet","f105b4efa5815bff50bbe51ef493550b49c91d36",8),
  300:("data/time-series/bead/sorbitol_300mM.parquet","cec88379c5da5a07dc444fd25c2f0be8937ec81e",8),
  400:("data/time-series/bead/sorbitol_400mM.parquet","f3fd7373b2944f01b945b7259661f3fc6a75fc85",8),
  500:("data/time-series/bead/sorbitol_500mM.parquet","1833accfa1e4405bebfd0e9430008854e3492567",8)},
 "sucrose_SPB_CCW":{
  200:("data/time-series/bead/sodium_200mM.parquet","57ec489e1a19cc3a20ea6dea270152b86b359fa0",10),
  300:("data/time-series/bead/sodium_300mM.parquet","5496ff4a54d4631fd0349d63966926d7ae065b7f",10),
  400:("data/time-series/bead/sodium_400mM.parquet","fe51858b5cc7b6e6e7d1eb94a4bcb165ce1d312c",10),
  500:("data/time-series/bead/sodium_500mM.parquet","52ab687a447fb5681492e4a25e7cf7814b2270c2",10)},
 "sucrose_CW_lock":{
  200:("data/time-series/bead/clockwise_200mM.parquet","c09ed5d53afd435097e26d5b10330dfd09e3538e",8),
  300:("data/time-series/bead/clockwise_300mM.parquet","c38f3e0ccffd884aee46732917233a73cd573212",8),
  400:("data/time-series/bead/clockwise_400mM.parquet","342d9c3c9164a20b3ec9d9ee7749989221854f41",9),
  500:("data/time-series/bead/clockwise_500mM.parquet","7a42570406646d9f329f1c9a32c870ffaf6fc56a",8)}
}
FEATURES=["A_dec","tau_dec","tau_inc","speed_increase_max"]

def medians(df):
    rows=[]
    for c in CONCS:
        z=df[(df.condition_mM==c)&(df.fit_valid)]
        if len(z)==0:
            raise RuntimeError(f"no valid fit at {c} mM")
        vals=[float(np.nanmedian(z[f].to_numpy(float))) for f in FEATURES]
        if not np.all(np.isfinite(vals)):
            raise RuntimeError(f"nonfinite condition median at {c} mM")
        rows.append(vals)
    return np.asarray(rows,float)

def zwithin(X):
    sd=X.std(axis=0,ddof=1)
    if np.any(~np.isfinite(sd)) or np.any(sd==0):
        raise RuntimeError("zero/nonfinite within-context coordinate variance")
    return (X-X.mean(axis=0))/sd

def geom_vec(X):
    return pdist(zwithin(X),metric="euclidean")

def exact_transport(refX,targetX):
    ref=geom_vec(refX)
    obs=float(spearmanr(ref,geom_vec(targetX)).statistic)
    vals=[]
    for perm in itertools.permutations(range(4)):
        vals.append(float(spearmanr(ref,geom_vec(targetX[list(perm),:])).statistic))
    p=float(np.mean(np.asarray(vals)>=obs-1e-15))
    return obs,p,vals

def rho_dose(v):
    return float(spearmanr(CONCS,v).statistic)

def classify(rho_geom,p_exact,rho_A):
    if rho_geom>=0.8 and p_exact<=0.10 and rho_A>=0.8:
        return "STRONG_GEOMETRY_TRANSPORT_P0Q"
    if rho_geom>=0.5 and rho_A>=0.5:
        return "PARTIAL_GEOMETRY_TRANSPORT_P0Q"
    return "GEOMETRY_TRANSPORT_REFUSED_P0Q"

def main():
    allfits=[]
    manifest=[]
    trace_counts={}
    matrices={}
    for ctx,items in CONTEXTS.items():
        trace_counts[ctx]={}
        rows=[]
        for c,(path,blob,nexp) in items.items():
            p=base.fetch(path,blob)
            data=p.read_bytes()
            fits=fit_immediate_manuscript(p,c)
            df=pd.DataFrame(fits)
            df["context"]=ctx
            rows.append(df)
            nobs=int(len(df))
            trace_counts[ctx][str(c)]={"observed":nobs,"expected":nexp,"valid_fits":int(df.fit_valid.sum())}
            manifest.append({"context":ctx,"condition_mM":c,"path":path,"blob_sha1":blob,
                             "sha256":base.sha256(data),"bytes":len(data)})
        cdf=pd.concat(rows,ignore_index=True)
        allfits.append(cdf)
        matrices[ctx]=medians(cdf)
    fitdf=pd.concat(allfits,ignore_index=True)
    fitdf.to_csv(OUT/"context_motor_fits.csv",index=False)
    pd.DataFrame(manifest).to_csv(OUT/"source_manifest.csv",index=False)

    counts_pass=all(v["observed"]==v["expected"] for ctx in trace_counts.values() for v in ctx.values())

    ref=matrices["sucrose_MB_CCW"]
    transport={}
    for ctx in ["sorbitol_MB_CCW","sucrose_SPB_CCW","sucrose_CW_lock"]:
        X=matrices[ctx]
        rg,p,perms=exact_transport(ref,X)
        rhoA=rho_dose(X[:,0])
        transport[ctx]={
          "distance_geometry_spearman_rho":rg,
          "exact_one_sided_p_24_permutations":p,
          "A_dec_dose_spearman_rho":rhoA,
          "disposition":classify(rg,p,rhoA),
          "permutation_rhos":perms
        }

    # Coordinate dose trends for every context.
    trends={}
    for ctx,X in matrices.items():
        trends[ctx]={f:rho_dose(X[:,i]) for i,f in enumerate(FEATURES)}

    # Pooled 16 x 4 representation.
    Xpool=np.vstack([matrices[c] for c in CONTEXTS])
    sd=Xpool.std(axis=0,ddof=1)
    if np.any(sd==0) or np.any(~np.isfinite(sd)):
        raise RuntimeError("zero/nonfinite pooled coordinate variance")
    Z=(Xpool-Xpool.mean(axis=0))/sd
    U,S,Vt=np.linalg.svd(Z,full_matrices=False)
    var=S*S
    pc1=float(var[0]/var.sum())
    recon=np.outer(U[:,0]*S[0],Vt[0,:])
    maxres=float(np.max(np.abs(Z-recon)))
    oned=bool(pc1>=0.95 and maxres<=0.10)

    # Overall whole-event transport label.
    ds=[transport[c]["disposition"] for c in transport]
    if all(x=="STRONG_GEOMETRY_TRANSPORT_P0Q" for x in ds):
        whole="IMMEDIATE_RESPONSE_ORGANIZATION_STRONGLY_TRANSPORTS_ACROSS_ALL_CONTEXTS_P0Q"
    elif any(x=="GEOMETRY_TRANSPORT_REFUSED_P0Q" for x in ds):
        whole="IMMEDIATE_RESPONSE_ORGANIZATION_CONTEXT_DEPENDENT_P0Q"
    else:
        whole="IMMEDIATE_RESPONSE_ORGANIZATION_PARTIALLY_TRANSPORTS_P0Q"

    result={
      "schema_version":"0.1",
      "experiment_id":"MENESES2026_IMMEDIATE_CONTEXT_TRANSPORT_P0Q_V01",
      "status":"EXECUTED_VALID_P0Q" if counts_pass else "SOURCE_TRACE_COUNT_FAILURE_PRESERVED",
      "evidence_class":"P0-Q_LITERATURE_OPEN_SAME_SOURCE_TRANSPORT",
      "source":{"repository":base.UPSTREAM,"commit":base.COMMIT,"manifest":manifest},
      "trace_counts":trace_counts,
      "trace_count_pass":bool(counts_pass),
      "features":FEATURES,
      "condition_matrices":{ctx:{str(c):{f:float(matrices[ctx][i,j]) for j,f in enumerate(FEATURES)}
                                  for i,c in enumerate(CONCS)} for ctx in CONTEXTS},
      "dose_trends_spearman":trends,
      "transport":transport,
      "pooled_representation":{
        "singular_values":[float(x) for x in S],
        "pc1_variance_fraction":pc1,
        "max_abs_standardized_1d_reconstruction_residual":maxres,
        "one_dimensional_adequacy":oned,
        "Chi_bio_disposition":"ONE_DIMENSIONAL_IMMEDIATE_RESPONSE_COMPRESSION_ADEQUATE_P0Q" if oned else "MULTICOORDINATE_IMMEDIATE_RESPONSE_ARCHITECTURE_REQUIRED_P0Q"
      },
      "chi_bio":{"disposition":"NOT_OPENED_NOT_LICENSED"},
      "Bio_Chi":{"disposition":whole},
      "claim_ceiling":"same-source P0-Q transport qualification; literature-open; clockwise-lock context includes strain/plasmid background change"
    }
    (OUT/"MENESES2026_IMMEDIATE_CONTEXT_TRANSPORT_P0Q_V01_RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    try:
        main()
    except Exception as e:
        fail={"schema_version":"0.1","experiment_id":"MENESES2026_IMMEDIATE_CONTEXT_TRANSPORT_P0Q_V01",
              "status":"EXECUTION_FAILURE_PRESERVED","error_type":type(e).__name__,"error":str(e)}
        (OUT/"MENESES2026_IMMEDIATE_CONTEXT_TRANSPORT_P0Q_V01_FAILURE.json").write_text(json.dumps(fail,indent=2)+"\n")
        print(json.dumps(fail,indent=2),file=sys.stderr)
        raise
