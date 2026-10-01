from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import numpy as np
import pandas as pd

FEATURES=["posterior_alpha_relative_power","alpha_peak_frequency_hz","theta_beta_ratio","aperiodic_exponent"]
CONDITIONS=["EC_pre","EC_post","EO_pre","EO_post"]
EXPECTED_SUBJECTS=517
EXPECTED_ROWS=2068

def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--pilot",required=True)
    ap.add_argument("--batches",nargs=4,required=True)
    ap.add_argument("--manifest",required=True)
    ap.add_argument("--output-dir",required=True)
    args=ap.parse_args()
    out=Path(args.output_dir); out.mkdir(parents=True,exist_ok=True)

    manifest=json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    expected=set(manifest["clean_session1_subjects"])
    if len(expected)!=EXPECTED_SUBJECTS: raise RuntimeError("manifest subject count mismatch")

    frames=[]
    inputs=[]
    for role,pstr in [("pilot",args.pilot)]+[(f"batch_{i}",p) for i,p in enumerate(args.batches)]:
        p=Path(pstr); df=pd.read_csv(p)
        frames.append(df); inputs.append({"role":role,"path":str(p),"sha256":sha256_file(p),"rows":int(len(df))})
    merged=pd.concat(frames,ignore_index=True)

    key=["participant_id","condition"]
    if merged.duplicated(key).any():
        raise RuntimeError("duplicate participant-condition rows")
    observed=set(merged["participant_id"])
    missing=sorted(expected-observed); extra=sorted(observed-expected)
    counts=merged.groupby("participant_id")["condition"].nunique()
    bad_counts=counts[counts!=4]
    bad_conditions=[]
    for sid,g in merged.groupby("participant_id"):
        if set(g["condition"])!=set(CONDITIONS): bad_conditions.append(sid)
    if missing or extra or len(bad_counts) or bad_conditions:
        raise RuntimeError(f"coverage failure missing={missing[:10]} extra={extra[:10]} bad_counts={bad_counts.index.tolist()[:10]} bad_conditions={bad_conditions[:10]}")
    if len(merged)!=EXPECTED_ROWS: raise RuntimeError(f"row count {len(merged)} != {EXPECTED_ROWS}")

    merged=merged.sort_values(["participant_id","condition"]).reset_index(drop=True)
    merged_path=out/"dortmund_clean_native_motion_517_v0_1.csv"; merged.to_csv(merged_path,index=False)

    summary={"schema":"DORTMUND_CLEAN_NATIVE_MOTION_517_V0_1","participant_count":EXPECTED_SUBJECTS,"row_count":EXPECTED_ROWS,
             "inputs":inputs,"merged_sha256":sha256_file(merged_path),"condition_means":{},"ec_minus_eo_pre":{},"post_minus_pre":{}}
    for m in FEATURES:
        summary["condition_means"][m]={c:float(merged.loc[merged.condition==c,m].mean()) for c in CONDITIONS}
        piv=merged.pivot(index="participant_id",columns="condition",values=m)
        d=piv["EC_pre"]-piv["EO_pre"]
        summary["ec_minus_eo_pre"][m]={"n":int(d.notna().sum()),"mean_difference":float(d.mean()),
          "cohens_d_paired":float(d.mean()/d.std(ddof=1))}
        summary["post_minus_pre"][m]={}
        for state in ["EC","EO"]:
            q=piv[f"{state}_post"]-piv[f"{state}_pre"]
            summary["post_minus_pre"][m][state]={"n":int(q.notna().sum()),"mean_difference":float(q.mean()),
              "sd_difference":float(q.std(ddof=1))}

    age=merged[["participant_id","age","sex"]].drop_duplicates()
    age["age_decade"]=pd.cut(age["age"],bins=[19,29,39,49,59,70],labels=["20-29","30-39","40-49","50-59","60-70"],include_lowest=True).astype(str)
    summary["age_sex_counts"]=age.groupby(["age_decade","sex"],observed=True).size().rename("n").reset_index().to_dict(orient="records")
    summary["scientific_ceiling"]="independent healthy native state/load distribution only; no NSD quantity, diagnosis, recovery-trajectory, or pathological threshold"
    (out/"dortmund_clean_native_motion_517_summary_v0_1.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__=="__main__": main()
