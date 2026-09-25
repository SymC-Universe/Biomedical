#!/usr/bin/env python3
from __future__ import annotations
import gzip, hashlib, io, json, pathlib, re, tarfile, tempfile, urllib.request
from datetime import datetime, timezone

ROOT=pathlib.Path(__file__).resolve().parents[2]
BIO=ROOT/"BIO_CHI"
CFG=BIO/"config"/"HARMANGE2023_LINEAGE_SOURCE_DISCOVERY_FREEZE_v0_2.json"
OUTDIR=BIO/"artifacts"/"generated"; OUTDIR.mkdir(parents=True,exist_ok=True)
OUT=OUTDIR/"harmange2023_lineage_source_discovery_v0_2.json"
UA="BioChiReviewerReproducibility/0.2"
BASE="https://ftp.ncbi.nlm.nih.gov/geo/series/GSE237nnn/GSE237228"

def fetch(url, timeout=240):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read()
        return b,{"requested_url":url,"resolved_url":r.geturl(),"content_type":r.headers.get("Content-Type"),"content_length":r.headers.get("Content-Length"),"last_modified":r.headers.get("Last-Modified")}

def sha(b): return hashlib.sha256(b).hexdigest()

def parse_soft(raw):
    txt=gzip.decompress(raw).decode("utf-8",errors="replace")
    series={}
    samples={}
    cur=None; acc=None
    for line in txt.splitlines():
        if line.startswith("^SERIES = "):
            cur="series"; acc=line.split("=",1)[1].strip()
        elif line.startswith("^SAMPLE = "):
            cur="sample"; acc=line.split("=",1)[1].strip()
            samples[acc]={"accession":acc,"title":None,"supplementary":[],"relations":[],"characteristics":[],"description":[]}
        elif cur=="series" and line.startswith("!Series_"):
            key,val=(line[1:].split(" = ",1)+[""])[:2] if " = " in line else (line[1:],"")
            series.setdefault(key,[]).append(val)
        elif cur=="sample" and acc:
            rec=samples[acc]
            if line.startswith("!Sample_title = "): rec["title"]=line.split("=",1)[1].strip()
            elif line.startswith("!Sample_supplementary_file") and " = " in line: rec["supplementary"].append(line.split(" = ",1)[1].strip())
            elif line.startswith("!Sample_relation = "): rec["relations"].append(line.split("=",1)[1].strip())
            elif line.startswith("!Sample_characteristics_ch1 = "): rec["characteristics"].append(line.split("=",1)[1].strip())
            elif line.startswith("!Sample_description = "): rec["description"].append(line.split("=",1)[1].strip())
    return {"series":series,"samples":samples}

def directory_listing(url):
    raw,meta=fetch(url)
    txt=raw.decode("utf-8",errors="replace")
    hrefs=re.findall(r'href="([^"]+)"',txt)
    files=sorted(set(h for h in hrefs if h not in ("../","/") and not h.endswith("/") and not h.startswith("?") and "vulnerability-disclosure" not in h))
    return {"url":url,"listing_sha256":sha(raw),"files":files,"meta":meta}

def first_nonempty_lines_gz(raw,n=5):
    out=[]
    with gzip.GzipFile(fileobj=io.BytesIO(raw),mode="rb") as gz:
        for bline in gz:
            s=bline.decode("utf-8",errors="replace").rstrip("\r\n")
            if s:
                out.append(s)
                if len(out)>=n: break
    return out

def matrixmarket_header_only(url):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    with urllib.request.urlopen(req,timeout=240) as r:
        gz=gzip.GzipFile(fileobj=r,mode="rb")
        comments=[]; banner=None; dims=None; lines_consumed=0
        while True:
            line=gz.readline()
            if not line: break
            lines_consumed+=1
            s=line.decode("utf-8",errors="replace").strip()
            if not s: continue
            if banner is None:
                banner=s
                continue
            if s.startswith("%"):
                comments.append(s)
                continue
            dims=s
            break
        # Stop here. Do not read any matrix-entry line.
        return {
          "banner":banner,"comments":comments,"dimensions_line":dims,
          "decompressed_lines_consumed":lines_consumed,
          "matrix_entries_consumed":0,
          "response_content_length":r.headers.get("Content-Length"),
          "last_modified":r.headers.get("Last-Modified")
        }

def tar_members_only(url):
    tmp=tempfile.NamedTemporaryFile(prefix="gse237228_",suffix=".tar",delete=False)
    tmp_path=pathlib.Path(tmp.name)
    h=hashlib.sha256(); total=0
    try:
        req=urllib.request.Request(url,headers={"User-Agent":UA})
        with urllib.request.urlopen(req,timeout=600) as r:
            while True:
                chunk=r.read(8*1024*1024)
                if not chunk: break
                tmp.write(chunk); h.update(chunk); total+=len(chunk)
        tmp.close()
        members=[]
        with tarfile.open(tmp_path,"r:*") as tf:
            for m in tf.getmembers():
                members.append({
                  "name":m.name,"size":m.size,"type":("file" if m.isfile() else "dir" if m.isdir() else "other"),
                  "mode":oct(m.mode),"mtime":m.mtime
                })
        return {"downloaded_bytes":total,"sha256":h.hexdigest(),"member_count":len(members),"members":members,"member_payloads_read":False}
    finally:
        try: tmp.close()
        except: pass
        try: tmp_path.unlink()
        except: pass

def main():
    cfg=json.loads(CFG.read_text())
    suppl=directory_listing(BASE+"/suppl/")
    soft,softmeta=fetch(BASE+"/soft/GSE237228_family.soft.gz")
    if sha(soft)!=cfg["known_files"]["soft"]["sha256"]: raise SystemExit("SOFT SHA mismatch")
    parsed=parse_soft(soft)

    small={}
    for key in ["barcodes","genes"]:
        info=cfg["known_files"][key]
        raw,meta=fetch(BASE+"/suppl/"+info["name"])
        if sha(raw)!=info["sha256"]: raise SystemExit(f"{key} SHA mismatch")
        lines=first_nonempty_lines_gz(raw,5)
        # Count identifiers, still no molecular values.
        with gzip.GzipFile(fileobj=io.BytesIO(raw),mode="rb") as gz:
            count=sum(1 for line in gz if line.strip())
        small[key]={"name":info["name"],"bytes":len(raw),"sha256":sha(raw),"first_nonempty_lines":lines,"nonempty_line_count":count,"meta":meta}

    mtx=matrixmarket_header_only(BASE+"/suppl/"+cfg["known_files"]["matrix"]["name"])
    rawtar=tar_members_only(BASE+"/suppl/"+cfg["known_files"]["raw_tar"]["name"])

    # Keyword scan is filenames/metadata only.
    keywords=["lineage","barcode","lenti","bc","clone","10x","matrix","feature","gene","meta"]
    member_hits=[]
    for m in rawtar["members"]:
        low=m["name"].lower()
        hits=[k for k in keywords if k in low]
        if hits: member_hits.append({"name":m["name"],"size":m["size"],"keywords":hits})

    sample_supp={acc:rec["supplementary"] for acc,rec in parsed["samples"].items() if rec["supplementary"]}
    result={
      "schema_version":"0.2","generated_at_utc":datetime.now(timezone.utc).isoformat(),
      "gate":cfg["gate"],"status":"PASS_OUTCOME_BLIND_SOURCE_SCHEMA_DISCOVERY",
      "supplementary_directory":suppl,
      "soft":{"bytes":len(soft),"sha256":sha(soft),"meta":softmeta,"series_metadata":parsed["series"],"sample_count":len(parsed["samples"]),"sample_supplementary_map":sample_supp},
      "small_files":small,
      "matrixmarket_header":mtx,
      "raw_tar":rawtar,
      "raw_tar_keyword_hits":member_hits,
      "molecular_values_opened":False,
      "raw_tar_member_payloads_read":False
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({
      "status":result["status"],
      "supplementary_files":suppl["files"],
      "sample_supplementary_count":len(sample_supp),
      "barcodes":small["barcodes"],
      "genes":small["genes"],
      "matrixmarket_header":mtx,
      "raw_tar":{"downloaded_bytes":rawtar["downloaded_bytes"],"sha256":rawtar["sha256"],"member_count":rawtar["member_count"],"members":rawtar["members"],"keyword_hits":member_hits},
      "molecular_values_opened":False
    },indent=2))
    print("BIO_CHI_HARMANGE_LINEAGE_SOURCE_DISCOVERY_PASS")
if __name__=="__main__":main()
