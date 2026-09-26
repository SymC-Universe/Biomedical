#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
import urllib.request

def md5_file(path: Path)->str:
    h=hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def download(url: str, path: Path)->None:
    req=urllib.request.Request(url,headers={"User-Agent":"SymC-NSD-ds004148-D4/1.0"})
    with urllib.request.urlopen(req,timeout=180) as r, path.open("wb") as out:
        while True:
            chunk=r.read(1024*1024)
            if not chunk:
                break
            out.write(chunk)

def parse_vhdr(path: Path)->dict:
    text=path.read_text(encoding="utf-8-sig",errors="replace")
    def grab(name):
        m=re.search(rf"(?mi)^\s*{re.escape(name)}\s*=\s*(.+?)\s*$",text)
        return m.group(1).strip() if m else None
    nchan=int(grab("NumberOfChannels")) if grab("NumberOfChannels") else None
    interval_us=float(grab("SamplingInterval")) if grab("SamplingInterval") else None
    sampling_hz=(1_000_000.0/interval_us) if interval_us else None
    binary_format=grab("BinaryFormat")
    data_orientation=grab("DataOrientation")
    data_file=grab("DataFile")
    marker_file=grab("MarkerFile")
    channels=[]
    for m in re.finditer(r"(?mi)^Ch(\d+)=(.*)$",text):
        parts=[p.strip() for p in m.group(2).split(",")]
        channels.append({
            "index":int(m.group(1)),
            "name":parts[0] if parts else None,
            "reference":parts[1] if len(parts)>1 else None,
            "resolution":parts[2] if len(parts)>2 else None,
            "unit":parts[3] if len(parts)>3 else None,
        })
    return {
        "number_of_channels":nchan,
        "sampling_interval_us":interval_us,
        "sampling_rate_hz":sampling_hz,
        "binary_format":binary_format,
        "data_orientation":data_orientation,
        "data_file":data_file,
        "marker_file":marker_file,
        "channels":channels,
        "raw_text":text,
    }

def bytes_per_sample(binary_format: str|None)->int|None:
    if binary_format is None:return None
    mapping={"INT_16":2,"UINT_16":2,"IEEE_FLOAT_32":4}
    return mapping.get(binary_format.strip().upper())

def run(manifest_path: Path, outdir: Path, output: Path)->dict:
    manifest=json.loads(manifest_path.read_text(encoding="utf-8"))
    outdir.mkdir(parents=True,exist_ok=True)
    base=manifest["pilot"]["relative_base"]
    mirror=manifest["source_release"]["nemar_mirror"]
    paths={}
    identities={}
    for ext,spec in manifest["pilot"]["files"].items():
        name=base.split("/")[-1]+"."+ext
        target=outdir/name
        url=f"https://data.nemar.org/{mirror}/{base}.{ext}"
        download(url,target)
        actual_md5=md5_file(target)
        identities[ext]={
            "url":url,
            "size_bytes":target.stat().st_size,
            "md5":actual_md5,
            "size_match":target.stat().st_size==int(spec["size_bytes"]),
            "md5_match":actual_md5==spec["md5"],
        }
        paths[ext]=target

    vh=parse_vhdr(paths["vhdr"])
    bps=bytes_per_sample(vh["binary_format"])
    nchan=vh["number_of_channels"]
    fs=vh["sampling_rate_hz"]
    duration=float(manifest["bids_contract"]["recording_duration_seconds"])
    expected_binary_bytes=(
        int(nchan*fs*duration*bps)
        if None not in (nchan,fs,bps) else None
    )
    checks={
        "all_file_identities":all(v["size_match"] and v["md5_match"] for v in identities.values()),
        "brainvision_channel_count_matches_channels_tsv":nchan==int(manifest["bids_contract"]["channels_tsv_rows"]),
        "brainvision_channel_count_differs_from_json_as_expected":nchan!=int(manifest["bids_contract"]["eeg_json_declared_channel_count"]),
        "channel_definition_count_matches_header":len(vh["channels"])==nchan,
        "sampling_rate_hz":fs==float(manifest["bids_contract"]["sampling_rate_hz"]),
        "binary_size_consistent_with_61ch_500hz_300s":expected_binary_bytes==paths["eeg"].stat().st_size,
        "data_file_name_matches":vh["data_file"]==paths["eeg"].name,
        "marker_file_name_matches":vh["marker_file"]==paths["vmrk"].name,
    }
    result={
        "schema":"NSD_DS004148_D4_PILOT_REPORT_V0_1",
        "dataset":"ds004148",
        "pilot":manifest["pilot"],
        "identities":identities,
        "brainvision":{
            k:v for k,v in vh.items() if k!="raw_text"
        },
        "derived_binary_layout":{
            "bytes_per_sample":bps,
            "expected_binary_bytes":expected_binary_bytes,
            "actual_binary_bytes":paths["eeg"].stat().st_size,
        },
        "checks":checks,
        "passed":all(checks.values()),
        "source_discrepancy":{
            "channels_tsv_rows":manifest["bids_contract"]["channels_tsv_rows"],
            "eeg_json_declared_channel_count":manifest["bids_contract"]["eeg_json_declared_channel_count"],
            "raw_brainvision_number_of_channels":nchan,
        },
        "scientific_features_computed":False,
        "modal_inference_run":False,
        "chi_computed":False,
        "capital_chi_computed":False,
        "claim_ceiling":manifest["claim_ceiling"],
    }
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,sort_keys=True))
    return result

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--manifest",type=Path,required=True)
    ap.add_argument("--download-dir",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    return 0 if run(args.manifest,args.download_dir,args.output)["passed"] else 1

if __name__=="__main__":
    raise SystemExit(main())
