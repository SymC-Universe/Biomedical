#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, pathlib, urllib.request
from datetime import datetime, timezone

ROOT=pathlib.Path(__file__).resolve().parents[2]
BIO=ROOT/"BIO_CHI"
CFG=BIO/"config"/"SU2026_M397_RPKM_SOURCE_FREEZE_v0_1.json"
OUT=BIO/"artifacts"/"generated"
OUT.mkdir(parents=True,exist_ok=True)
OUT_FILE=OUT/"su2026_m397_rpkm_source_freeze_v0_1.json"
UA="BioChiReviewerReproducibility/0.1"

def main():
    cfg=json.loads(CFG.read_text(encoding="utf-8"))
    req=urllib.request.Request(cfg["url"],headers={"User-Agent":UA,"Accept":"application/gzip,application/octet-stream,*/*;q=0.5"})
    with urllib.request.urlopen(req,timeout=180) as r:
        data=r.read()
        meta={
          "resolved_url":r.geturl(),"http_status":getattr(r,"status",None),
          "content_type":r.headers.get("Content-Type"),"content_length_header":r.headers.get("Content-Length"),
          "etag":r.headers.get("ETag"),"last_modified":r.headers.get("Last-Modified")
        }
    result={
      "schema_version":"0.1",
      "generated_at_utc":datetime.now(timezone.utc).isoformat(),
      "gate":cfg["gate"],
      "geo_series":cfg["geo_series"],
      "source_file":cfg["source_file"],
      "url":cfg["url"],
      "download_meta":meta,
      "size_bytes":len(data),
      "sha256":hashlib.sha256(data).hexdigest(),
      "gzip_magic_verified":data[:2]==b"\x1f\x8b",
      "decompressed":False,
      "header_read":False,
      "expression_values_read":False,
      "scientific_values_interpreted":False
    }
    result["status"]="PASS_EXACT_COMPRESSED_SOURCE_FROZEN" if result["gzip_magic_verified"] else "FAIL_NOT_GZIP"
    OUT_FILE.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
    if result["status"]!="PASS_EXACT_COMPRESSED_SOURCE_FROZEN":
        raise SystemExit("BIO_CHI_SU_RPKM_SOURCE_FREEZE_FAIL")
    print("BIO_CHI_SU_RPKM_SOURCE_FREEZE_PASS")
if __name__=="__main__": main()
