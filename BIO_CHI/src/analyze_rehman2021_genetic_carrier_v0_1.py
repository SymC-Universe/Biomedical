#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, math, pathlib, urllib.request
import numpy as np

ROOT=pathlib.Path(__file__).resolve().parents[2]
BIO=ROOT/"BIO_CHI"
CFG=BIO/"config"/"REHMAN2021_GENETIC_CARRIER_FREEZE_v0_1.json"
OUTDIR=BIO/"artifacts"/"generated"
OUTDIR.mkdir(parents=True,exist_ok=True)
OUT=OUTDIR/"rehman2021_genetic_carrier_v0_1.json"
AUDIT=OUTDIR/"REHMAN2021_GENETIC_CARRIER_V01_AUDIT.md"
UA="BioChiReviewerReproducibility/0.1"

def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    with urllib.request.urlopen(req,timeout=60) as r:
        return r.read()
def sha(b): return hashlib.sha256(b).hexdigest()

def parse_csvints(s):
    return [int(x) for x in s.strip().split(",")]

def metrics(v,centroid):
    d=np.asarray(v,float)-np.asarray(centroid,float)
    rms=float(np.sqrt(np.mean(d*d)))
    mad=float(np.median(np.abs(d)))
    sv=float(np.std(v)); sc=float(np.std(centroid))
    corr=None if sv==0 or sc==0 else float(np.corrcoef(v,centroid)[0,1])
    return {"rms_vaf_deviation":rms,"median_abs_vaf_deviation":mad,"pearson":corr,"one_minus_pearson":None if corr is None else 1.0-corr}

def main():
    cfg=json.loads(CFG.read_text())
    base="https://raw.githubusercontent.com/{repo}/{commit}/{path}"
    purl=base.format(repo=cfg["source"]["repository"],commit=cfg["source"]["commit"],path=cfg["source"]["combined_params_path"])
    surl=base.format(repo=cfg["source"]["repository"],commit=cfg["source"]["commit"],path=cfg["source"]["combined_ssm_path"])
    pb=fetch(purl); sb=fetch(surl)
    params=json.loads(pb.decode("utf-8"))
    samples=params["samples"]
    if samples!=cfg["source_sample_order"]:
        raise SystemExit(f"sample order mismatch: {samples!r}")
    garbage=set(params.get("garbage",[]))
    if garbage!=set(cfg["mutation_rows"]["source_declared_garbage"]):
        raise SystemExit(f"garbage mismatch: {garbage}")

    lines=sb.decode("utf-8").strip().splitlines()
    head=lines[0].split("\t")
    if head!=["id","name","var_reads","total_reads","var_read_prob"]:
        raise SystemExit(f"unexpected SSM header: {head}")
    ids=[]; names=[]; rows=[]
    skipped=[]
    for line in lines[1:]:
        f=line.split("\t")
        mid=f[0]
        if mid in garbage:
            skipped.append(mid); continue
        vr=parse_csvints(f[2]); tr=parse_csvints(f[3])
        if len(vr)!=8 or len(tr)!=8:
            raise SystemExit(f"{mid}: expected 8 samples")
        if any(x<=0 for x in tr):
            raise SystemExit(f"{mid}: zero/nonpositive total reads")
        vaf=np.array(vr,dtype=float)/np.array(tr,dtype=float)
        if not np.all(np.isfinite(vaf)):
            raise SystemExit(f"{mid}: nonfinite VAF")
        ids.append(mid); names.append(f[1]); rows.append(vaf)
    M=np.vstack(rows) # mutations x samples
    idx={s:i for i,s in enumerate(samples)}
    primary_idx=[idx[s] for s in cfg["primary_baseline"]["samples"]]
    sens_idx=[idx[s] for s in cfg["baseline_sensitivity"]["samples"]]
    cent_primary=M[:,primary_idx].mean(axis=1)
    cent_sens=M[:,sens_idx].mean(axis=1)

    post=cfg["posttreatment_samples"]["recovery"]+cfg["posttreatment_samples"]["resistant"]
    rec={}
    for s in post:
        rec[s]={
          "primary_baseline":metrics(M[:,idx[s]],cent_primary),
          "vehicle_only_baseline":metrics(M[:,idx[s]],cent_sens)
        }

    reg=cfg["posttreatment_samples"]["recovery"][0]
    res=cfg["posttreatment_samples"]["resistant"]
    primary_pass=all(rec[reg]["primary_baseline"]["rms_vaf_deviation"] < rec[s]["primary_baseline"]["rms_vaf_deviation"] for s in res)
    sens_pass=all(rec[reg]["vehicle_only_baseline"]["rms_vaf_deviation"] < rec[s]["vehicle_only_baseline"]["rms_vaf_deviation"] for s in res)
    gate=primary_pass and sens_pass

    # Rank summaries are descriptive only.
    ordering_primary=sorted(post,key=lambda s:rec[s]["primary_baseline"]["rms_vaf_deviation"])
    ordering_sens=sorted(post,key=lambda s:rec[s]["vehicle_only_baseline"]["rms_vaf_deviation"])

    result={
      "schema_version":"0.1",
      "gate":cfg["gate"],
      "status":"PASS_DESCRIPTIVE_CARRIER_PERSISTENCE_GATE" if gate else "FAIL_DESCRIPTIVE_CARRIER_PERSISTENCE_GATE",
      "source":{
        "repository":cfg["source"]["repository"],"commit":cfg["source"]["commit"],
        "params_sha256":sha(pb),"ssm_sha256":sha(sb),
        "source_params_blob":cfg["source"]["combined_params_blob"],"source_ssm_blob":cfg["source"]["combined_ssm_blob"]
      },
      "mutation_count_retained":len(ids),
      "source_declared_garbage_skipped":sorted(skipped),
      "sample_order":samples,
      "sample_metrics":rec,
      "gate":{
        "primary_baseline_all_three_resistant_farther_than_regrowth":primary_pass,
        "vehicle_only_baseline_all_three_resistant_farther_than_regrowth":sens_pass,
        "combined_pass":gate
      },
      "rms_distance_order":{
        "primary_baseline":ordering_primary,
        "vehicle_only_baseline":ordering_sens
      },
      "epistemic":{
        "tier":"P0-Q post-result carrier qualification",
        "inferential_p_value":None,
        "clone_frequency_inference_performed":False,
        "scalar_constructed":False,
        "exact_MATH_reproduction":False
      }
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    lines_md=[
      "# Rehman 2021 genetic carrier persistence v0.1","",
      f"**Status:** {result['status']}",
      f"**Mutations retained:** {len(ids)}",
      f"**Source garbage skipped:** {', '.join(sorted(skipped))}","",
      "| Sample | RMS vs P0/G0/vehicle centroid | RMS vs vehicle-only centroid | 1-Pearson primary | Median abs VAF dev primary |",
      "|---|---:|---:|---:|---:|"
    ]
    for s in post:
        a=rec[s]["primary_baseline"]; b=rec[s]["vehicle_only_baseline"]
        op="n/a" if a["one_minus_pearson"] is None else f"{a['one_minus_pearson']:.8g}"
        lines_md.append(f"| {s} | {a['rms_vaf_deviation']:.8g} | {b['rms_vaf_deviation']:.8g} | {op} | {a['median_abs_vaf_deviation']:.8g} |")
    lines_md += ["",f"Primary-baseline gate: {primary_pass}",f"Vehicle-only sensitivity gate: {sens_pass}","",
                 "This is a descriptive post-result P0-Q carrier test. One regrowth genetic sample is available in the combined source, so no inferential p-value is manufactured."]
    AUDIT.write_text("\n".join(lines_md)+"\n")
    print(json.dumps({
      "status":result["status"],"mutation_count_retained":len(ids),
      "sample_metrics":rec,"gate":result["gate"],"ordering":result["rms_distance_order"]
    },indent=2))
    print("BIO_CHI_REHMAN_GENETIC_CARRIER_DONE")
if __name__=="__main__":
    main()
