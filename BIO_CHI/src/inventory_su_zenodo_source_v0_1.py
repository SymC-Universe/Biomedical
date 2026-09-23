#!/usr/bin/env python3
from __future__ import annotations
import hashlib, io, json, pathlib, urllib.request, zipfile
from datetime import datetime, timezone

ROOT=pathlib.Path(__file__).resolve().parents[2]
BIO=ROOT/"BIO_CHI"
CFG=BIO/"config"/"SU2026_ZENODO_SOURCE_INVENTORY_FREEZE_v0_1.json"
OUT=BIO/"artifacts"/"generated"
OUT.mkdir(parents=True,exist_ok=True)
OUT_FILE=OUT/"su2026_zenodo_source_inventory_v0_1.json"
UA="BioChiReviewerReproducibility/0.1"
MAX=100*1024*1024

def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,application/zip,application/octet-stream,*/*;q=0.5"})
    with urllib.request.urlopen(req,timeout=180) as r:
        data=r.read()
        return data,{"resolved_url":r.geturl(),"content_type":r.headers.get("Content-Type"),"content_length":r.headers.get("Content-Length"),"etag":r.headers.get("ETag"),"last_modified":r.headers.get("Last-Modified")}

def md5(b): return hashlib.md5(b).hexdigest()
def sha256(b): return hashlib.sha256(b).hexdigest()

def main():
    cfg=json.loads(CFG.read_text(encoding="utf-8"))
    raw,meta=fetch(cfg["api_url"])
    rec=json.loads(raw.decode("utf-8"))
    files=[]
    failures=[]
    for f in rec.get("files",[]):
        name=f.get("key") or f.get("filename")
        size=f.get("size")
        checksum=f.get("checksum")
        links=f.get("links",{}) if isinstance(f.get("links"),dict) else {}
        url=links.get("self") or links.get("content") or links.get("download")
        item={"name":name,"size_bytes":size,"checksum":checksum,"download_url":url,"archive_members":None,"payload_interpreted":False}
        if url and isinstance(size,int) and size<=MAX and name and name.lower().endswith((".zip",".tar.gz",".tgz")):
            try:
                data,dmeta=fetch(url)
                item["download_meta"]=dmeta
                item["download_sha256"]=sha256(data)
                if isinstance(checksum,str) and checksum.startswith("md5:"):
                    item["advertised_md5_verified"]=(md5(data)==checksum.split(":",1)[1])
                    if not item["advertised_md5_verified"]:
                        failures.append(name+": advertised MD5 mismatch")
                if zipfile.is_zipfile(io.BytesIO(data)):
                    with zipfile.ZipFile(io.BytesIO(data),"r") as zf:
                        item["archive_type"]="zip"
                        item["archive_members"]=[{
                            "path":x.filename,"is_dir":x.is_dir(),"file_size":x.file_size,
                            "compress_size":x.compress_size,"crc32_hex":f"{x.CRC:08x}"
                        } for x in zf.infolist()]
                else:
                    item["archive_type"]="non_zip_archive_not_opened"
            except Exception as exc:
                item["download_error"]=f"{type(exc).__name__}: {exc}"
                failures.append(name+": "+item["download_error"])
        files.append(item)
    result={
      "schema_version":"0.1",
      "generated_at_utc":datetime.now(timezone.utc).isoformat(),
      "gate":cfg["gate"],
      "record_api_sha256":sha256(raw),
      "record_id":rec.get("id"),
      "doi":rec.get("doi"),
      "title":(rec.get("metadata") or {}).get("title"),
      "record_meta":meta,
      "file_count":len(files),
      "files":files,
      "member_payloads_read":False,
      "scientific_values_interpreted":False,
      "failures":failures,
      "status":"PASS_ZENODO_SOURCE_INVENTORY" if not failures else "PARTIAL_ZENODO_SOURCE_INVENTORY"
    }
    OUT_FILE.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
      "output":str(OUT_FILE.relative_to(ROOT)),
      "status":result["status"],
      "doi":result["doi"],"file_count":len(files),
      "files":[{"name":x["name"],"size_bytes":x["size_bytes"],"checksum":x["checksum"],"member_count":len(x["archive_members"]) if isinstance(x["archive_members"],list) else None} for x in files],
      "failures":failures
    },indent=2))
    if failures: raise SystemExit("BIO_CHI_SU_ZENODO_SOURCE_INVENTORY_PARTIAL")
    print("BIO_CHI_SU_ZENODO_SOURCE_INVENTORY_PASS")

if __name__=="__main__": main()
