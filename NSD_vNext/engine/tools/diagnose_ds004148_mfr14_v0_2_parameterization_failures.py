#!/usr/bin/env python3
"""Locate fixed-primary versus knee-sensitivity specparam refusals for the
three MFR-14 v0.2 failed subjects. No cohort endpoint is computed.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

TOOLS_ROOT = Path(__file__).resolve().parent
if str(TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOLS_ROOT))

from run_ds004148_eyesopen_mfr14_replication_v0_2 import (
    _download,
    _hash,
    _parse_vhdr,
    _read_brainvision,
    _resolve_annex_identity,
)
from run_ds004148_descriptive_transfer import (
    FROZEN_FIXED,
    SENSITIVITY_KNEE,
    WELCH,
)
from nsd_engine.psd import estimate_welch_psd
from nsd_engine.specparam_adapter import fit_specparam_descriptive

FAILED_SUBJECTS=("sub-21","sub-26","sub-27")


def _load_recording(subject, session, source, root):
    repository=source["public_git_repository"]
    commit=source["public_git_commit"]
    mirror=source["nemar_mirror"]
    task="eyesopen"
    base=f"{subject}/{session}/eeg/{subject}_{session}_task-{task}_eeg"
    nemar=f"https://data.nemar.org/{mirror}/{base}"
    local={}
    identity={}
    for ext in ("vhdr","vmrk","eeg"):
        source_path=base+"."+ext
        annex=_resolve_annex_identity(repository,commit,source_path,ext)
        path=root/f"{subject}__{session}__{task}.{ext}"
        _download(nemar+"."+ext,path)
        size=path.stat().st_size
        md5=_hash(path,"md5")
        if size != int(annex["expected_size_bytes"]) or md5 != annex["expected_md5"]:
            raise ValueError(f"{subject} {session} {ext}: source identity failure")
        identity[ext]={**annex,"observed_size_bytes":size,"observed_md5":md5}
        local[ext]=path

    header=_parse_vhdr(local["vhdr"])
    labels,data=_read_brainvision(local["eeg"],header)
    if data.shape != (61,150000):
        raise ValueError(f"{subject} {session}: decoded shape {data.shape}")
    return labels,data,identity


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--cohort-manifest",required=True,type=Path)
    ap.add_argument("--labels-manifest",required=True,type=Path)
    ap.add_argument("--output-dir",required=True,type=Path)
    args=ap.parse_args()

    cohort=json.loads(args.cohort_manifest.read_text(encoding="utf-8"))
    label_doc=json.loads(args.labels_manifest.read_text(encoding="utf-8"))
    frozen_labels=list(label_doc["labels"])
    args.output_dir.mkdir(parents=True,exist_ok=True)
    payload_dir=args.output_dir/"payloads"
    payload_dir.mkdir(exist_ok=True)

    records=[]
    fixed_failures=[]
    knee_failures=[]

    for subject in FAILED_SUBJECTS:
        if subject not in cohort["subjects"]:
            raise ValueError(f"{subject} not in frozen v0.2 cohort")
        for session in cohort["sessions"]:
            labels,data,identity=_load_recording(
                subject,session,cohort["source_release"],payload_dir
            )
            index={label:i for i,label in enumerate(labels)}
            missing=[label for label in frozen_labels if label not in index]
            if missing:
                raise ValueError(f"{subject} {session}: missing stable57 labels {missing}")

            for label in frozen_labels:
                signal=data[index[label]]
                psd=estimate_welch_psd(
                    signal,500.0,fmin_hz=1.0,fmax_hz=45.0,config=WELCH
                )
                row={
                    "subject":subject,
                    "session":session,
                    "channel":label,
                    "fixed_status":"NOT_RUN",
                    "knee_status":"NOT_RUN",
                }
                try:
                    fixed=fit_specparam_descriptive(
                        psd.frequencies_hz,psd.power,settings=FROZEN_FIXED
                    )
                    row["fixed_status"]="PASS"
                    row["fixed_peak_count"]=len(fixed.peaks)
                except Exception as exc:
                    row["fixed_status"]="REFUSED"
                    row["fixed_error_type"]=type(exc).__name__
                    row["fixed_error"]=str(exc)
                    fixed_failures.append(dict(row))
                    records.append(row)
                    continue

                try:
                    knee=fit_specparam_descriptive(
                        psd.frequencies_hz,psd.power,settings=SENSITIVITY_KNEE
                    )
                    row["knee_status"]="PASS"
                    row["knee_peak_count"]=len(knee.peaks)
                except Exception as exc:
                    row["knee_status"]="REFUSED"
                    row["knee_error_type"]=type(exc).__name__
                    row["knee_error"]=str(exc)
                    knee_failures.append(dict(row))

                records.append(row)

    result={
        "schema":"NSD_DS004148_MFR14_V0_2_PARAMETERIZATION_FAILURE_DIAGNOSTIC_V0_1",
        "status":"FAILURE_STAGE_DIAGNOSTIC_COMPLETE",
        "subjects":list(FAILED_SUBJECTS),
        "channel_count":len(frozen_labels),
        "record_count":len(records),
        "fixed_failure_count":len(fixed_failures),
        "knee_failure_count":len(knee_failures),
        "fixed_failures":fixed_failures,
        "knee_failures":knee_failures,
        "records":records,
        "licenses_replication_claim":False,
        "licenses_modal_damping":False,
        "licenses_local_chi":False,
        "licenses_capital_chi":False,
    }
    out=args.output_dir/"mfr14_v0_2_parameterization_failure_diagnostic_v0.1.json"
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
        "fixed_failure_count":len(fixed_failures),
        "knee_failure_count":len(knee_failures),
        "fixed_failures":[
            (x["subject"],x["session"],x["channel"],x.get("fixed_error_type"))
            for x in fixed_failures
        ],
        "knee_failures":[
            (x["subject"],x["session"],x["channel"],x.get("knee_error_type"))
            for x in knee_failures
        ],
    },indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
