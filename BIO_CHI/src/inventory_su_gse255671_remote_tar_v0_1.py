#!/usr/bin/env python3
from __future__ import annotations
import json, math, pathlib, urllib.request
from datetime import datetime, timezone

ROOT=pathlib.Path(__file__).resolve().parents[2]
BIO=ROOT/"BIO_CHI"
CFG=BIO/"config"/"SU2026_GSE255671_REMOTE_TAR_INVENTORY_FREEZE_v0_1.json"
OUT=BIO/"artifacts"/"generated"
OUT.mkdir(parents=True,exist_ok=True)
OUT_FILE=OUT/"su2026_gse255671_remote_tar_inventory_v0_1.json"
UA="BioChiReviewerReproducibility/0.1"
BLOCK=512

def head(url):
    req=urllib.request.Request(url,method="HEAD",headers={"User-Agent":UA})
    with urllib.request.urlopen(req,timeout=120) as r:
        return {
          "status":getattr(r,"status",None),
          "content_length":int(r.headers["Content-Length"]) if r.headers.get("Content-Length") else None,
          "accept_ranges":r.headers.get("Accept-Ranges"),
          "etag":r.headers.get("ETag"),
          "last_modified":r.headers.get("Last-Modified")
        }

def get_range(url,start,end):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Range":f"bytes={start}-{end}"})
    with urllib.request.urlopen(req,timeout=120) as r:
        data=r.read()
        status=getattr(r,"status",None)
        cr=r.headers.get("Content-Range")
    expected=end-start+1
    if status!=206 or len(data)!=expected:
        raise RuntimeError(f"range unsupported/mismatch status={status} content_range={cr!r} len={len(data)} expected={expected}")
    return data

def cstr(b):
    return b.split(b"\0",1)[0].decode("utf-8",errors="replace").strip()

def octal(b):
    s=b.split(b"\0",1)[0].strip(b" \0")
    if not s: return 0
    try: return int(s,8)
    except ValueError: raise RuntimeError(f"invalid tar size field {b!r}")

def padded(n):
    return int(math.ceil(n/BLOCK))*BLOCK if n else 0

def parse_pax(payload):
    out={}
    pos=0
    while pos<len(payload):
        sp=payload.find(b" ",pos)
        if sp<0: break
        try: n=int(payload[pos:sp])
        except ValueError: break
        rec=payload[sp+1:pos+n]
        if b"=" in rec:
            k,v=rec.rstrip(b"\n").split(b"=",1)
            out[k.decode("utf-8",errors="replace")]=v.decode("utf-8",errors="replace")
        pos += n
    return out

def main():
    cfg=json.loads(CFG.read_text(encoding="utf-8"))
    url=cfg["url"]
    hm=head(url)
    if hm["content_length"]!=cfg["expected_size_bytes"]:
        raise SystemExit(f"SU_REMOTE_TAR_SIZE_DRIFT expected={cfg['expected_size_bytes']} observed={hm['content_length']}")
    # Explicitly prove range semantics before traversal.
    probe=get_range(url,0,511)
    if len(probe)!=512: raise SystemExit("SU_REMOTE_TAR_RANGE_PROBE_FAIL")

    offset=0
    members=[]
    pending_longname=None
    pending_pax={}
    tar_header_bytes_read=512
    metadata_payload_bytes_read=0
    ordinary_payload_bytes_read=0
    zero_blocks=0

    while offset+BLOCK <= hm["content_length"]:
        header = probe if offset==0 else get_range(url,offset,offset+BLOCK-1)
        if offset!=0: tar_header_bytes_read += BLOCK
        if header == b"\0"*BLOCK:
            zero_blocks += 1
            if zero_blocks>=2: break
            offset += BLOCK
            continue
        zero_blocks=0

        name=cstr(header[0:100])
        prefix=cstr(header[345:500])
        if prefix: name=prefix+"/"+name
        size=octal(header[124:136])
        typeflag=header[156:157].decode("ascii",errors="replace") or "0"

        if typeflag in ("L","K","x","g"):
            payload=b""
            if size:
                payload=get_range(url,offset+BLOCK,offset+BLOCK+size-1)
                metadata_payload_bytes_read += len(payload)
            if typeflag=="L":
                pending_longname=payload.rstrip(b"\0\n").decode("utf-8",errors="replace")
            elif typeflag in ("x","g"):
                pending_pax.update(parse_pax(payload))
            members.append({
              "path":name,"typeflag":typeflag,"declared_size_bytes":size,
              "metadata_entry":True,"ordinary_payload_read":False
            })
        else:
            resolved=pending_pax.get("path") or pending_longname or name
            members.append({
              "path":resolved,"header_name":name if resolved!=name else None,
              "typeflag":typeflag,"declared_size_bytes":size,
              "metadata_entry":False,"ordinary_payload_read":False
            })
            pending_longname=None
            pending_pax={}

        offset += BLOCK + padded(size)
        if len(members)>100000:
            raise SystemExit("SU_REMOTE_TAR_MEMBER_CAP_EXCEEDED")

    result={
      "schema_version":"0.1",
      "generated_at_utc":datetime.now(timezone.utc).isoformat(),
      "gate":cfg["gate"],
      "url":url,
      "head":hm,
      "member_count":len(members),
      "members":members,
      "tar_header_bytes_read":tar_header_bytes_read,
      "metadata_payload_bytes_read":metadata_payload_bytes_read,
      "ordinary_member_payload_bytes_read":ordinary_payload_bytes_read,
      "traversal_end_offset":offset,
      "end_zero_blocks":zero_blocks,
      "scientific_values_interpreted":False,
      "status":"PASS_REMOTE_TAR_HEADER_INVENTORY" if ordinary_payload_bytes_read==0 and zero_blocks>=2 else "FAIL_REMOTE_TAR_HEADER_INVENTORY"
    }
    OUT_FILE.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
      "output":str(OUT_FILE.relative_to(ROOT)),
      "status":result["status"],
      "member_count":len(members),
      "ordinary_payload_bytes_read":ordinary_payload_bytes_read,
      "metadata_payload_bytes_read":metadata_payload_bytes_read,
      "first_members":members[:10],
      "last_members":members[-10:]
    },indent=2))
    if result["status"]!="PASS_REMOTE_TAR_HEADER_INVENTORY":
        raise SystemExit("BIO_CHI_SU_REMOTE_TAR_INVENTORY_FAIL")
    print("BIO_CHI_SU_REMOTE_TAR_INVENTORY_PASS")

if __name__=="__main__": main()
