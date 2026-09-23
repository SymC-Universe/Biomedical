#!/usr/bin/env python3
from __future__ import annotations

import gzip
import hashlib
import json
import pathlib
import re
import urllib.request
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[2]
BIO = ROOT / "BIO_CHI"
OUT = BIO / "artifacts" / "generated"
OUT.mkdir(parents=True, exist_ok=True)

CONFIGS = [
    BIO / "config" / "SU2026_SOURCE_SUBSET_v0_1.json",
    BIO / "config" / "REHMAN2021_SOURCE_SUBSET_v0_1.json",
]

def geo_soft_url(gse: str) -> str:
    m = re.fullmatch(r"GSE(\d+)", gse)
    if not m:
        raise ValueError(f"bad GEO accession: {gse}")
    digits = m.group(1)
    bucket = f"GSE{digits[:-3]}nnn"
    return f"https://ftp.ncbi.nlm.nih.gov/geo/series/{bucket}/{gse}/soft/{gse}_family.soft.gz"

def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent":"BioChiGeoMetadataAudit/0.1"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()

def parse_soft(raw_gz: bytes) -> dict:
    text = gzip.decompress(raw_gz).decode("utf-8", errors="replace")
    samples = {}
    current = None
    for line in text.splitlines():
        if line.startswith("^SAMPLE = "):
            current = line.split("=",1)[1].strip()
            samples[current] = {"title":None,"characteristics":[],"source_name":None}
        elif current and line.startswith("!Sample_title = "):
            samples[current]["title"] = line.split("=",1)[1].strip()
        elif current and line.startswith("!Sample_source_name_ch1 = "):
            samples[current]["source_name"] = line.split("=",1)[1].strip()
        elif current and line.startswith("!Sample_characteristics_ch1 = "):
            samples[current]["characteristics"].append(line.split("=",1)[1].strip())
        elif line.startswith("^SERIES"):
            current = None
    return samples

def expected_samples(cfg: dict) -> list[str]:
    if "samples" in cfg:
        return list(cfg["samples"])
    gsms = []
    for key in ("rna_timecourse","atac_anchor_samples","histone_anchor_samples"):
        for item in cfg.get(key, []):
            gsms.append(item["gsm"])
    gsms.extend(cfg.get("replicate_histone_samples", []))
    return gsms

audits=[]
failures=[]
for cfg_path in CONFIGS:
    cfg=json.loads(cfg_path.read_text(encoding="utf-8"))
    gse=cfg["geo"]
    url=geo_soft_url(gse)
    raw=fetch(url)
    sha=hashlib.sha256(raw).hexdigest()
    parsed=parse_soft(raw)
    expected=expected_samples(cfg)
    missing=[x for x in expected if x not in parsed]
    selected={x:parsed[x] for x in expected if x in parsed}
    audit={
        "config":cfg_path.relative_to(ROOT).as_posix(),
        "geo":gse,
        "soft_url":url,
        "soft_sha256":sha,
        "soft_size_bytes":len(raw),
        "expected_sample_count":len(expected),
        "found_sample_count":len(selected),
        "missing_samples":missing,
        "selected_sample_metadata":selected,
        "molecular_values_opened":False,
    }
    audits.append(audit)
    if missing:
        failures.append(f"{gse}: missing expected samples {missing}")

result={
    "schema_version":"0.1",
    "generated_at_utc":datetime.now(timezone.utc).isoformat(),
    "audit_type":"metadata_only",
    "molecular_values_opened":False,
    "audits":audits,
    "failures":failures,
}
out=OUT/"geo_metadata_audit_v0_1.json"
out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
print(json.dumps(result,indent=2))
if failures:
    raise SystemExit("BIO_CHI_GEO_METADATA_AUDIT_FAIL")
print("BIO_CHI_GEO_METADATA_AUDIT_PASS")
