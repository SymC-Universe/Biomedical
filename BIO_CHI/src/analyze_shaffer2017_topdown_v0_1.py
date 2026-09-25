#!/usr/bin/env python3
from __future__ import annotations
import gzip, hashlib, json, math, pathlib, urllib.request
from collections import defaultdict
from datetime import datetime, timezone
import numpy as np

ROOT=pathlib.Path(__file__).resolve().parents[2]
BIO=ROOT/"BIO_CHI"
CFG=BIO/"config"/"SHAFFER2017_TOPDOWN_EVENT_FREEZE_v0_1.json"
OUTDIR=BIO/"artifacts"/"generated"; OUTDIR.mkdir(parents=True,exist_ok=True)
OUT=OUTDIR/"shaffer2017_topdown_analysis_v0_1.json"
AUDIT=OUTDIR/"SHAFFER2017_TOPDOWN_ANALYSIS_V01_AUDIT.md"
URL="https://ftp.ncbi.nlm.nih.gov/geo/series/GSE97nnn/GSE97681/suppl/GSE97681_wm9LdB_star_HTSeqCounts_full.tsv.gz"
UA="BioChiReviewerReproducibility/0.1"

def fetch(url):
 req=urllib.request.Request(url,headers={"User-Agent":UA})
 with urllib.request.urlopen(req,timeout=180) as r:return r.read()
def sha(b):return hashlib.sha256(b).hexdigest()

def corr_distance(a,b):
 if np.std(a)==0 or np.std(b)==0:return float("nan")
 return float(1-np.corrcoef(a,b)[0,1])
def cosine(a,b):
 na=float(np.linalg.norm(a)); nb=float(np.linalg.norm(b))
 if na==0 or nb==0:return None
 return float(np.dot(a,b)/(na*nb))

def main():
 cfg=json.loads(CFG.read_text())
 raw=fetch(URL)
 if sha(raw)!=cfg["source"]["processed_sha256"]:raise SystemExit("processed file SHA mismatch")
 # lookup accepted accession/title tokens and required sample roles
 tokens={}
 sample_roles={}
 for sub,sc in cfg["carriers"].items():
  b=sc["baseline"]
  for tok in [b["accession"],b["title"]]:tokens[tok]=b["accession"]
  sample_roles[b["accession"]]={"subclone":sub,"role":"baseline","lane":None,"title":b["title"]}
  for lane in sc["lanes"]:
   for role,key in [("drug","drug"),("holiday48","holiday48"),("holiday7","holiday7")]:
    rec=lane[key]
    for tok in [rec["accession"],rec["title"]]:tokens[tok]=rec["accession"]
    sample_roles[rec["accession"]]={"subclone":sub,"role":role,"lane":lane["lane"],"title":rec["title"]}
 required=set(sample_roles)
 counts=defaultdict(dict)
 seen=set()
 matched_raw_ids={}
 with gzip.open(pathlib.Path(OUTDIR/"tmp.tsv.gz"),"wb") as _: pass
 # parse source bytes directly
 import io
 with gzip.GzipFile(fileobj=io.BytesIO(raw),mode="rb") as gz:
  header=gz.readline().decode("utf-8",errors="replace").rstrip("\r\n").split("\t")
  if header!=["experiment","sampleID","gene_id","counts"]:raise SystemExit(f"unexpected header {header}")
  for line in gz:
   parts=line.decode("utf-8",errors="replace").rstrip("\r\n").split("\t")
   if len(parts)!=4:continue
   experiment,sample_id,gene,cval=parts
   acc=None
   for candidate in [sample_id,experiment]:
    if candidate in tokens:acc=tokens[candidate];matched_raw_ids[candidate]=acc;break
   if acc is None:continue
   if gene.startswith("__"):continue
   key=(acc,gene)
   if key in seen:raise SystemExit(f"duplicate sample-gene row {key}")
   seen.add(key)
   try:c=float(cval)
   except:raise SystemExit(f"non-numeric count for {key}")
   if not math.isfinite(c) or c<0:raise SystemExit(f"invalid count for {key}")
   counts[acc][gene]=c
 missing=sorted(required-set(counts))
 if missing:raise SystemExit("required selected samples not found in processed file: "+repr(missing))
 genes=sorted(set.intersection(*(set(counts[a]) for a in sorted(required))))
 if not genes:raise SystemExit("no common genes")
 sample_order=sorted(required)
 mat=np.array([[counts[a][g] for a in sample_order] for g in genes],dtype=float)
 lib=mat.sum(axis=0)
 if np.any(lib<=0):raise SystemExit("zero library")
 cpm=mat/lib[None,:]*1e6
 keep=(cpm>=1).sum(axis=1)>=3
 cpm=cpm[keep]; genes_f=[g for g,k in zip(genes,keep) if k]
 log=np.log2(cpm+1.0)
 idx={a:i for i,a in enumerate(sample_order)}
 vec={a:log[:,idx[a]] for a in sample_order}

 lane_results={}
 carrier_lanes=defaultdict(list)
 for sub,sc in cfg["carriers"].items():
  base=vec[sc["baseline"]["accession"]]
  for lane in sc["lanes"]:
   rec={"subclone":sub}
   ds={}
   for role in ["drug","holiday48","holiday7"]:
    a=lane[role]["accession"]; ds[role]=corr_distance(vec[a],base)
   if not all(math.isfinite(x) for x in ds.values()) or ds["drug"]<=0:raise SystemExit("non-evaluable primary distance")
   rec["correlation_distance"]=ds
   rec["return48"]=1-ds["holiday48"]/ds["drug"]
   rec["return7"]=1-ds["holiday7"]/ds["drug"]
   rec["holiday48_improves_vs_drug"]=ds["holiday48"]<ds["drug"]
   rec["holiday7_improves_vs_drug"]=ds["holiday7"]<ds["drug"]
   rec["holiday7_improves_vs_holiday48"]=ds["holiday7"]<ds["holiday48"]
   lane_results[lane["lane"]]=rec
   carrier_lanes[sub].append(rec)

 carrier_primary={}
 for sub,rs in carrier_lanes.items():
  means={role:float(np.mean([r["correlation_distance"][role] for r in rs])) for role in ["drug","holiday48","holiday7"]}
  carrier_primary[sub]={
   "mean_correlation_distance":means,
   "return48":1-means["holiday48"]/means["drug"],
   "return7":1-means["holiday7"]/means["drug"],
   "day7_improves_vs_drug":means["holiday7"]<means["drug"],
   "day7_improves_vs_day48":means["holiday7"]<means["holiday48"]
  }
 primary_pass=all(x["day7_improves_vs_drug"] for x in carrier_primary.values())
 sign_success=sum(x["day7_improves_vs_drug"] for x in carrier_primary.values())
 # exact one-sided sign test under p=.5
 from math import comb
 sign_p=sum(comb(3,k) for k in range(sign_success,4))/8

 # z-euclidean sensitivity
 gene_mean=log.mean(axis=1); gene_sd=log.std(axis=1,ddof=0); nz=gene_sd>0
 z=(log[nz]-gene_mean[nz,None])/gene_sd[nz,None]
 zvec={a:z[:,idx[a]] for a in sample_order}
 sens={}
 for sub,sc in cfg["carriers"].items():
  base=zvec[sc["baseline"]["accession"]]
  rows=[]
  for lane in sc["lanes"]:
   ds={role:float(np.linalg.norm(zvec[lane[role]["accession"]]-base)) for role in ["drug","holiday48","holiday7"]}
   rows.append(ds)
  m={role:float(np.mean([r[role] for r in rows])) for role in ["drug","holiday48","holiday7"]}
  sens[sub]={"mean_z_euclidean":m,"day7_improves_vs_drug":m["holiday7"]<m["drug"],"return7":1-m["holiday7"]/m["drug"] if m["drug"]>0 else None}

 # PCA modal representation
 X=log.T
 Xc=X-X.mean(axis=0,keepdims=True)
 U,S,Vt=np.linalg.svd(Xc,full_matrices=False)
 var=S*S
 ratio=var/var.sum()
 cum=np.cumsum(ratio)
 k=int(np.searchsorted(cum,0.80)+1)
 scores=U[:,:k]*S[:k]
 score={a:scores[idx[a],:] for a in sample_order}
 modal_lanes={}
 modal_carriers=defaultdict(list)
 for sub,sc in cfg["carriers"].items():
  base=score[sc["baseline"]["accession"]]
  for lane in sc["lanes"]:
   drug=score[lane["drug"]["accession"]]; h48=score[lane["holiday48"]["accession"]]; h7=score[lane["holiday7"]["accession"]]
   ds={"drug":float(np.linalg.norm(drug-base)),"holiday48":float(np.linalg.norm(h48-base)),"holiday7":float(np.linalg.norm(h7-base))}
   rec={"subclone":sub,"modal_distance":ds,"day7_improves_vs_drug":ds["holiday7"]<ds["drug"],
        "drug_to_day7_vs_drug_to_baseline_cosine":cosine(h7-drug,base-drug)}
   modal_lanes[lane["lane"]]=rec;modal_carriers[sub].append(rec)
 modal_primary={}
 for sub,rs in modal_carriers.items():
  m={role:float(np.mean([r["modal_distance"][role] for r in rs])) for role in ["drug","holiday48","holiday7"]}
  modal_primary[sub]={"mean_modal_distance":m,"day7_improves_vs_drug":m["holiday7"]<m["drug"],"return7":1-m["holiday7"]/m["drug"] if m["drug"]>0 else None,
                      "mean_direction_cosine":float(np.mean([r["drug_to_day7_vs_drug_to_baseline_cosine"] for r in rs if r["drug_to_day7_vs_drug_to_baseline_cosine"] is not None]))}
 modal_pass=all(x["day7_improves_vs_drug"] for x in modal_primary.values())
 if primary_pass and modal_pass: relation="P0Q_RECOVERY_WITH_MODAL_RETURN"
 elif primary_pass and not modal_pass: relation="P0Q_GLOBAL_RECOVERY_WITH_MODAL_REORGANIZATION"
 else: relation="P0Q_RECOVERY_NOT_REPRODUCED_UNDER_FROZEN_PRIMARY_GATE"

 result={
  "schema_version":"0.1","generated_at_utc":datetime.now(timezone.utc).isoformat(),
  "status":"PASS_ANALYSIS_EXECUTED","source_sha256":sha(raw),"sample_count":len(sample_order),"filtered_gene_count":len(genes_f),
  "matched_raw_ids":matched_raw_ids,
  "whole_event":{"lane_results":lane_results,"carrier_primary":carrier_primary,"primary_pass":primary_pass,"sign_successes":sign_success,"exact_one_sided_sign_p":sign_p,
                 "sensitivity_z_euclidean":sens},
  "modal":{"retained_pc_count":k,"cumulative_variance":float(cum[k-1]),"lane_results":modal_lanes,"carrier_primary":modal_primary,"modal_return_pass":modal_pass},
  "disposition":{"Bio_Chi_relation":relation,"scalar":"SCALAR_NOT_REQUIRED_AND_NOT_LICENSED"},
  "epistemic":{"tier":"P0-Q","five_wells_nested_within_three_subclones":True,"independent_heldout_behavior_lane":False}
 }
 OUT.write_text(json.dumps(result,indent=2)+"\n")
 lines=["# Shaffer 2017 top-down WM989 drug-holiday analysis v0.1","",f"**Disposition:** {relation}","",
 "| Subclone | Drug distance | 48h distance | 7d distance | day7 closer than drug |",
 "|---|---:|---:|---:|---|"]
 for sub,x in carrier_primary.items():
  m=x["mean_correlation_distance"];lines.append(f"| {sub} | {m['drug']:.6g} | {m['holiday48']:.6g} | {m['holiday7']:.6g} | {x['day7_improves_vs_drug']} |")
 lines+=["",f"Primary subclone directional successes: {sign_success}/3; exact one-sided sign p={sign_p:.6g} (resolution diagnostic).",
         f"Modal basis retained {k} PCs, cumulative variance {cum[k-1]:.4f}; modal return gate={modal_pass}.",
         "","Five wells are descriptive lanes nested within three subclones. Scalar construction remained closed."]
 AUDIT.write_text("\n".join(lines)+"\n")
 print(json.dumps({"status":result["status"],"whole_event":result["whole_event"],"modal":result["modal"],"disposition":result["disposition"]},indent=2))
 print("BIO_CHI_SHAFFER_TOPDOWN_ANALYSIS_DONE")
if __name__=="__main__":main()
