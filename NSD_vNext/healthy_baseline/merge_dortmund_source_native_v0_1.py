from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import pandas as pd

PIPELINE_ID="DORTMUND_SOURCE_NATIVE_V01"
DATASET="ds005385"
SNAPSHOT="1.0.3"
EXPECTED_AGE_GROUPS=[(20,29),(30,39),(40,49),(50,59),(60,70)]
SOURCE_FINAL_RECORDINGS=3229

def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--chunks", nargs=5, required=True)
    ap.add_argument("--output-dir", required=True)
    args=ap.parse_args()
    out=Path(args.output_dir); out.mkdir(parents=True,exist_ok=True)

    frames=[]
    chunk_meta=[]
    for pstr in args.chunks:
        p=Path(pstr)
        df=pd.read_csv(p)
        if "pipeline_id" not in df or not set(df["pipeline_id"].dropna().astype(str)).issubset({PIPELINE_ID}):
            raise RuntimeError(f"pipeline mismatch: {p}")
        if "dataset" not in df or not set(df["dataset"].dropna().astype(str)).issubset({DATASET}):
            raise RuntimeError(f"dataset mismatch: {p}")
        if "snapshot" not in df or not set(df["snapshot"].dropna().astype(str)).issubset({SNAPSHOT}):
            raise RuntimeError(f"snapshot mismatch: {p}")
        frames.append(df)
        chunk_meta.append({"path":str(p),"sha256":sha256_file(p),"rows":int(len(df)),
                           "age_min":int(df["age"].min()),"age_max":int(df["age"].max()),
                           "participants":int(df["participant_id"].nunique())})

    merged=pd.concat(frames,ignore_index=True)
    if merged["source_relative_path"].duplicated().any():
        dup=merged.loc[merged["source_relative_path"].duplicated(False),"source_relative_path"].tolist()
        raise RuntimeError(f"duplicate source recordings: {dup[:20]}")

    participants=merged[["participant_id","age"]].drop_duplicates()
    if participants["participant_id"].duplicated().any():
        raise RuntimeError("participant maps to multiple ages")

    observed_groups=sorted({(int(df["age"].min()),int(df["age"].max())) for df in frames})
    if observed_groups != EXPECTED_AGE_GROUPS:
        raise RuntimeError(f"age group mismatch: {observed_groups}")

    merged=merged.sort_values(["participant_id","session","eye_state","timepoint","source_relative_path"]).reset_index(drop=True)
    merged_path=out/"dortmund_source_native_merged_v0_1.csv"
    merged.to_csv(merged_path,index=False)

    summary={
      "schema":"DORTMUND_SOURCE_NATIVE_MERGE_V0_1",
      "pipeline_id":PIPELINE_ID,"dataset":DATASET,"snapshot":SNAPSHOT,
      "chunks":chunk_meta,
      "participant_count":int(merged["participant_id"].nunique()),
      "recordings_attempted":int(len(merged)),
      "recordings_pass":int((merged["qc_status"]=="PASS").sum()),
      "recordings_rejected_lt5":int((merged["qc_status"]=="REJECT_LT5_CLEAN_EPOCHS").sum()),
      "recordings_other_failure":int((~merged["qc_status"].isin(["PASS","REJECT_LT5_CLEAN_EPOCHS"])).sum()),
      "source_paper_final_recordings":SOURCE_FINAL_RECORDINGS,
      "pass_minus_source_final":int((merged["qc_status"]=="PASS").sum()-SOURCE_FINAL_RECORDINGS),
      "merged_sha256":sha256_file(merged_path),
      "scientific_ceiling":"coverage/QC merge only; mixed-model interpretation remains gated"
    }
    (out/"dortmund_source_native_merge_summary_v0_1.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__=="__main__": main()
