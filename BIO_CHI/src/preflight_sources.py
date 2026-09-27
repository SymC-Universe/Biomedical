#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "BIO_CHI" / "config" / "SOURCE_MANIFEST_v0_1.json"
OUT = ROOT / "BIO_CHI" / "artifacts" / "generated"
OUT.mkdir(parents=True, exist_ok=True)

def head(url: str) -> dict:
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent":"BioChiSourcePreflight/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return {
                "url": url,
                "ok": 200 <= r.status < 400,
                "status": r.status,
                "content_length": r.headers.get("Content-Length"),
                "etag": r.headers.get("ETag"),
                "last_modified": r.headers.get("Last-Modified"),
            }
    except urllib.error.HTTPError as e:
        return {"url":url,"ok":False,"status":e.code,"error":str(e)}
    except Exception as e:
        return {"url":url,"ok":False,"status":None,"error":repr(e)}

manifest_bytes = MANIFEST.read_bytes()
manifest = json.loads(manifest_bytes)
records = []
failed = []

for source in manifest["sources"]:
    landing = head(source["landing_page"])
    file_records = [head(u) for u in source.get("files", [])]
    rec = {
        "id": source["id"],
        "accession": source["accession"],
        "landing_page": landing,
        "files": file_records,
        "outcome_opened": False,
    }
    records.append(rec)
    if source.get("expected_public") and not landing.get("ok"):
        failed.append(f"{source['id']}: landing page not reachable")
    for fr in file_records:
        if not fr.get("ok"):
            failed.append(f"{source['id']}: file not reachable: {fr['url']}")

result = {
    "schema_version":"0.1",
    "generated_at_utc":datetime.now(timezone.utc).isoformat(),
    "source_manifest_sha256":hashlib.sha256(manifest_bytes).hexdigest(),
    "outcome_opened":False,
    "records":records,
    "failures":failed,
}
outpath = OUT / "source_preflight_v0_1.json"
outpath.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))

if failed:
    print("BIO_CHI_SOURCE_PREFLIGHT_FAIL", file=sys.stderr)
    raise SystemExit(1)
print("BIO_CHI_SOURCE_PREFLIGHT_PASS")
