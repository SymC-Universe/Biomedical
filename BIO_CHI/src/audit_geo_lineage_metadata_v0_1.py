#!/usr/bin/env python3
from __future__ import annotations

import gzip
import hashlib
import json
import pathlib
import urllib.request
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[2]
BIO = ROOT / "BIO_CHI"
CFG = BIO / "config" / "P0D_GEO_LINEAGE_METADATA_FREEZE_v0_1.json"
OUT = BIO / "artifacts" / "generated"
OUT.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT / "geo_lineage_metadata_audit_v0_1.json"
USER_AGENT = "BioChiReviewerReproducibility/0.1"


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify(url: str, expected: str) -> bytes:
    raw = fetch(url)
    observed = sha256(raw)
    if observed != expected:
        raise SystemExit(f"HASH_MISMATCH {url} expected={expected} observed={observed}")
    return raw


def parse_soft(raw_gz: bytes) -> dict:
    text = gzip.decompress(raw_gz).decode("utf-8", errors="replace")
    series = {
        "accession": None,
        "title": [],
        "summary": [],
        "overall_design": [],
        "relations": [],
        "supplementary_files": [],
        "sample_ids": [],
    }
    samples: dict[str, dict] = {}
    current_sample = None

    for line in text.splitlines():
        if line.startswith("^SERIES = "):
            series["accession"] = line.split("=", 1)[1].strip()
            current_sample = None
        elif line.startswith("^SAMPLE = "):
            current_sample = line.split("=", 1)[1].strip()
            series["sample_ids"].append(current_sample)
            samples[current_sample] = {
                "title": [],
                "source_name": [],
                "characteristics": [],
                "relations": [],
            }
        elif line.startswith("^") and not line.startswith("^SAMPLE"):
            current_sample = None
        elif current_sample is None:
            if line.startswith("!Series_title = "):
                series["title"].append(line.split("=",1)[1].strip())
            elif line.startswith("!Series_summary = "):
                series["summary"].append(line.split("=",1)[1].strip())
            elif line.startswith("!Series_overall_design = "):
                series["overall_design"].append(line.split("=",1)[1].strip())
            elif line.startswith("!Series_relation = "):
                series["relations"].append(line.split("=",1)[1].strip())
            elif line.startswith("!Series_supplementary_file = "):
                series["supplementary_files"].append(line.split("=",1)[1].strip())
        else:
            rec = samples[current_sample]
            if line.startswith("!Sample_title = "):
                rec["title"].append(line.split("=",1)[1].strip())
            elif line.startswith("!Sample_source_name_ch1 = "):
                rec["source_name"].append(line.split("=",1)[1].strip())
            elif line.startswith("!Sample_characteristics_ch1 = "):
                rec["characteristics"].append(line.split("=",1)[1].strip())
            elif line.startswith("!Sample_relation = "):
                rec["relations"].append(line.split("=",1)[1].strip())
    return {"series": series, "samples": samples}


def first_header_from_gzip(raw_gz: bytes) -> str:
    with gzip.GzipFile(fileobj=__import__("io").BytesIO(raw_gz), mode="rb") as gz:
        line = gz.readline()
    return line.decode("utf-8-sig", errors="replace").rstrip("\r\n")


def main() -> None:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    audits = []
    for ds in cfg["datasets"]:
        soft = verify(ds["family_soft"]["url"], ds["family_soft"]["sha256"])
        parsed = parse_soft(soft)
        audit = {
            "id": ds["id"],
            "geo": ds["geo"],
            "family_soft_sha256": sha256(soft),
            "series": parsed["series"],
            "samples": parsed["samples"],
            "sample_count": len(parsed["samples"]),
            "molecular_values_read": False,
            "cell_metadata_rows_read": False,
        }
        mh = ds.get("metadata_header")
        if mh:
            raw = verify(mh["url"], mh["sha256"])
            audit["metadata_header_sha256"] = sha256(raw)
            audit["metadata_header"] = first_header_from_gzip(raw)
        audits.append(audit)

    result = {
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "gate": cfg["gate"],
        "source_config": str(CFG.relative_to(ROOT)),
        "molecular_values_read": False,
        "cell_metadata_rows_read": False,
        "audits": audits,
        "status": "PASS_METADATA_ONLY_SOURCE_LINEAGE_AUDIT",
    }
    OUT_FILE.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUT_FILE.relative_to(ROOT)),
        "status": result["status"],
        "datasets": [
            {
                "id": a["id"],
                "sample_count": a["sample_count"],
                "series_relations": a["series"]["relations"],
                "metadata_header": a.get("metadata_header"),
            }
            for a in audits
        ],
    }, indent=2))
    print("BIO_CHI_GEO_LINEAGE_METADATA_AUDIT_PASS")


if __name__ == "__main__":
    main()
