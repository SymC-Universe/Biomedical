#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import urllib.request

ENGINE_ROOT = Path(__file__).resolve().parents[1]
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

from nsd_engine.edf import read_edf_header

EXPECTED_LABELS = (
    "Fp1", "Fp2", "F7", "F3", "Fz", "F4", "F8", "FC5", "FC1", "FC2", "FC6",
    "T7", "C3", "Cz", "C4", "T8", "TP9", "CP5", "CP1", "CP2", "CP6", "TP10",
    "P7", "P3", "Pz", "P4", "P8", "PO9", "O1", "Oz", "O2", "PO10", "AF7",
    "AF3", "AF4", "AF8", "F5", "F1", "F2", "F6", "FT9", "FT7", "FC3", "FC4",
    "FT8", "FT10", "C5", "C1", "C2", "C6", "TP7", "CP3", "CPz", "CP4", "TP8",
    "P5", "P1", "P2", "P6", "PO7", "PO3", "POz", "PO4", "PO8",
)

def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def recording_name(subject: str, row: dict) -> str:
    return f"{subject}_{row['session']}_task-{row['task']}_acq-{row['acquisition']}_eeg.edf"

def download(url: str, path: Path) -> None:
    req=urllib.request.Request(url,headers={"User-Agent":"SymC-NSD-ds005385-D4/1.0"})
    with urllib.request.urlopen(req,timeout=180) as r, path.open("wb") as out:
        while True:
            chunk=r.read(1024*1024)
            if not chunk:
                break
            out.write(chunk)

def verify_one(path: Path, row: dict, manifest: dict) -> dict:
    header=read_edf_header(path,validate_physical_range=False)
    labels=tuple(s.label for s in header.signals)
    rates=sorted({round(s.sampling_rate_hz,9) for s in header.signals})
    checks={
        "size_bytes": path.stat().st_size == int(row["size_bytes"]),
        "sha256": sha256_file(path) == row["sha256"],
        "signal_count_total": header.signal_count == int(manifest["expected_signal_count_total"]),
        "eeg_channel_count": len(labels[:int(manifest["expected_eeg_channel_count"])]) == int(manifest["expected_eeg_channel_count"]),
        "eeg_labels": labels[:64] == EXPECTED_LABELS,
        "auxiliary_labels": list(labels[64:]) == manifest["expected_auxiliary_labels"],
        "sampling_rate_hz": rates == [float(manifest["expected_sampling_rate_hz"])],
        "duration_seconds": header.recording_duration_seconds == float(row["duration_seconds"]),
        "edf_internal_size_consistency": header.expected_file_size_bytes == path.stat().st_size,
    }
    return {
        "session":row["session"],
        "task":row["task"],
        "acquisition":row["acquisition"],
        "path":str(path),
        "checks":checks,
        "passed":all(checks.values()),
        "actual_size_bytes":path.stat().st_size,
        "actual_sha256":sha256_file(path),
        "duration_seconds":header.recording_duration_seconds,
        "signal_count_total":header.signal_count,
        "physical_range_policy":manifest["physical_range_policy"],
        "physical_values_used_for_scaling":False,
    }

def run(manifest_path: Path, outdir: Path, output: Path) -> dict:
    manifest=json.loads(manifest_path.read_text(encoding="utf-8"))
    outdir.mkdir(parents=True,exist_ok=True)
    records=[]
    subject=manifest["subject"]
    mirror=manifest["source_release"]["nemar_mirror"]
    for row in manifest["recordings"]:
        name=recording_name(subject,row)
        rel=f"{subject}/{row['session']}/eeg/{name}"
        url=f"https://data.nemar.org/{mirror}/{rel}"
        target=outdir/name
        download(url,target)
        rec=verify_one(target,row,manifest)
        rec["source_url"]=url
        records.append(rec)
    result={
        "schema":"NSD_DS005385_D4_SUB001_REPEAT_CONDITION_REPORT_V0_1",
        "dataset":"ds005385",
        "subject":subject,
        "recordings_expected":len(manifest["recordings"]),
        "recordings_passed":sum(r["passed"] for r in records),
        "all_passed":all(r["passed"] for r in records),
        "records":records,
        "physical_range_policy":manifest["physical_range_policy"],
        "claim_ceiling":manifest["claim_ceiling"],
        "scientific_features_computed":False,
        "modal_inference_run":False,
        "chi_computed":False,
        "capital_chi_computed":False,
    }
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return result

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--manifest",type=Path,required=True)
    ap.add_argument("--download-dir",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    result=run(args.manifest,args.download_dir,args.output)
    print(json.dumps(result,indent=2,sort_keys=True))
    return 0 if result["all_passed"] else 1

if __name__=="__main__":
    raise SystemExit(main())
