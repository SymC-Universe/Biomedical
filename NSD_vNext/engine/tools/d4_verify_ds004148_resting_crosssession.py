#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, urllib.request
from pathlib import Path

def md5_file(path):
    h=hashlib.md5()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def download(url,path):
    req=urllib.request.Request(url,headers={"User-Agent":"SymC-NSD-ds004148-D4-expansion/1.0"})
    with urllib.request.urlopen(req,timeout=180) as r, Path(path).open("wb") as out:
        while True:
            chunk=r.read(1024*1024)
            if not chunk: break
            out.write(chunk)

def parse_vhdr(path):
    text=Path(path).read_text(encoding="utf-8-sig",errors="replace")
    def grab(name):
        m=re.search(rf"(?mi)^\s*{re.escape(name)}\s*=\s*(.+?)\s*$",text)
        return m.group(1).strip() if m else None
    channels=[]
    for m in re.finditer(r"(?mi)^Ch(\d+)=(.*)$",text):
        parts=[p.strip() for p in m.group(2).split(",")]
        channels.append({"index":int(m.group(1)),"name":parts[0] if parts else None})
    interval=float(grab("SamplingInterval"))
    return {
      "number_of_channels":int(grab("NumberOfChannels")),
      "sampling_rate_hz":1_000_000.0/interval,
      "binary_format":grab("BinaryFormat"),
      "data_orientation":grab("DataOrientation"),
      "data_file":grab("DataFile"),
      "marker_file":grab("MarkerFile"),
      "channels":channels
    }

def bps(fmt):
    return {"INT_16":2,"UINT_16":2,"IEEE_FLOAT_32":4}.get(str(fmt).upper())

def run(manifest_path, download_dir, output):
    m=json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    outdir=Path(download_dir); outdir.mkdir(parents=True,exist_ok=True)
    results=[]
    for rec in m["recordings"]:
        local={}
        ids={}
        for ext,spec in rec["files"].items():
            name=rec["base"].split("/")[-1]+"."+ext
            p=outdir/f"{rec['session']}__{name}"
            url=f"https://data.nemar.org/{m['source_release']['nemar_mirror']}/{rec['base']}.{ext}"
            download(url,p)
            ids[ext]={"size_bytes":p.stat().st_size,"md5":md5_file(p),
                      "size_match":p.stat().st_size==spec["size_bytes"],
                      "md5_match":md5_file(p)==spec["md5"],"url":url}
            local[ext]=p
        h=parse_vhdr(local["vhdr"])
        bytes_per=bps(h["binary_format"])
        expected_bytes=int(m["expected"]["raw_channels"]*m["expected"]["sampling_rate_hz"]*
                           m["expected"]["duration_seconds"]*bytes_per)
        checks={
          "identities":all(v["size_match"] and v["md5_match"] for v in ids.values()),
          "raw_channel_count":h["number_of_channels"]==m["expected"]["raw_channels"],
          "channel_definition_count":len(h["channels"])==m["expected"]["raw_channels"],
          "sampling_rate":h["sampling_rate_hz"]==m["expected"]["sampling_rate_hz"],
          "binary_format":h["binary_format"].upper()==m["expected"]["binary_format"],
          "binary_layout":local["eeg"].stat().st_size==expected_bytes,
          "data_file":h["data_file"]==local["eeg"].name.split("__",1)[-1],
          "marker_file":h["marker_file"]==local["vmrk"].name.split("__",1)[-1],
        }
        results.append({"session":rec["session"],"task":rec["task"],"identities":ids,
                        "header":h,"expected_binary_bytes":expected_bytes,
                        "actual_binary_bytes":local["eeg"].stat().st_size,
                        "checks":checks,"passed":all(checks.values())})
    result={
      "schema":"NSD_DS004148_D4_RESTING_CROSSSESSION_REPORT_V0_1",
      "dataset":"ds004148","subject":m["subject"],
      "recordings_expected":len(results),
      "recordings_passed":sum(x["passed"] for x in results),
      "all_passed":all(x["passed"] for x in results),
      "records":results,
      "source_channel_discrepancy_retained":True,
      "signal_features_computed":False,"modal_inference_run":False,
      "chi_computed":False,"capital_chi_computed":False,
      "claim_ceiling":m["claim_ceiling"]
    }
    Path(output).parent.mkdir(parents=True,exist_ok=True)
    Path(output).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,sort_keys=True))
    return result

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--manifest",required=True,type=Path)
    ap.add_argument("--download-dir",required=True,type=Path)
    ap.add_argument("--output",required=True,type=Path)
    a=ap.parse_args()
    return 0 if run(a.manifest,a.download_dir,a.output)["all_passed"] else 1
if __name__=="__main__": raise SystemExit(main())
