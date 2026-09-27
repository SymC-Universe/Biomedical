#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import io
import json
import pathlib
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[2]
BIO = ROOT / "BIO_CHI"
CFG = BIO / "config" / "LEE2014_SRP040309_SOURCE_MAP_FREEZE_v0_1.json"
OUT = BIO / "artifacts" / "generated"
OUT.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT / "lee2014_srp040309_source_map_v0_1.json"
UA = "BioChiReviewerReproducibility/0.1"


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def esearch(term: str) -> dict:
    q = urllib.parse.urlencode({
        "db": "sra",
        "term": term,
        "retmax": 100000,
        "retmode": "json",
        "tool": "BioChiSourceQualification",
    })
    raw = fetch("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + q)
    return json.loads(raw.decode("utf-8"))


def efetch_runinfo(ids: list[str]) -> tuple[bytes, str]:
    q = urllib.parse.urlencode({
        "db": "sra",
        "id": ",".join(ids),
        "rettype": "runinfo",
        "retmode": "text",
        "tool": "BioChiSourceQualification",
    })
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" + q
    return fetch(url), url


def main() -> None:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    accession = cfg["reported_study_accession"]

    search = esearch(f"{accession}[Study Accession]")
    ids = search.get("esearchresult", {}).get("idlist", [])
    search_count = int(search.get("esearchresult", {}).get("count", "0") or 0)
    if not ids:
        # Fail closed but try the literal accession once; this is still the frozen question.
        search = esearch(accession)
        ids = search.get("esearchresult", {}).get("idlist", [])
        search_count = int(search.get("esearchresult", {}).get("count", "0") or 0)
    if not ids:
        raise SystemExit("LEE2014_SRA_MAP_NO_RECORDS")

    raw, runinfo_url = efetch_runinfo(ids)
    text = raw.decode("utf-8-sig", errors="replace")
    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows:
        raise SystemExit("LEE2014_SRA_MAP_EMPTY_RUNINFO")

    def vals(key: str) -> list[str]:
        return sorted({(r.get(key) or "").strip() for r in rows if (r.get(key) or "").strip()})

    studies = vals("SRAStudy")
    if studies and accession not in studies:
        raise SystemExit(f"LEE2014_SRA_MAP_STUDY_MISMATCH expected={accession} got={studies}")

    compact_rows = []
    keep = [
        "Run","ReleaseDate","LoadDate","spots","bases","spots_with_mates","avgLength","size_MB",
        "AssemblyName","download_path","Experiment","LibraryName","LibraryStrategy","LibrarySelection",
        "LibrarySource","LibraryLayout","InsertSize","InsertDev","Platform","Model","SRAStudy",
        "BioProject","Study_Pubmed_id","ProjectID","Sample","BioSample","SampleType","TaxID",
        "ScientificName","CenterName","Submission","Consent"
    ]
    for row in rows:
        compact_rows.append({k:(row.get(k) or "").strip() for k in keep if k in row})

    result = {
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "gate": cfg["gate"],
        "reported_study_accession": accession,
        "esearch_record_count": search_count,
        "esearch_ids": ids,
        "runinfo_url": runinfo_url,
        "runinfo_sha256": sha256(raw),
        "runinfo_size_bytes": len(raw),
        "run_count": len(rows),
        "runs": vals("Run"),
        "experiments": vals("Experiment"),
        "samples": vals("Sample"),
        "biosamples": vals("BioSample"),
        "bioprojects": vals("BioProject"),
        "studies": vals("SRAStudy"),
        "library_strategy_counts": dict(Counter((r.get("LibraryStrategy") or "").strip() for r in rows)),
        "library_layout_counts": dict(Counter((r.get("LibraryLayout") or "").strip() for r in rows)),
        "platform_counts": dict(Counter((r.get("Platform") or "").strip() for r in rows)),
        "records": compact_rows,
        "sequence_reads_downloaded": False,
        "molecular_values_interpreted": False,
        "status": "PASS_SRA_METADATA_SOURCE_MAP",
    }
    OUT_FILE.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUT_FILE.relative_to(ROOT)),
        "status": result["status"],
        "run_count": result["run_count"],
        "studies": result["studies"],
        "bioprojects": result["bioprojects"],
        "library_strategy_counts": result["library_strategy_counts"],
        "library_layout_counts": result["library_layout_counts"],
        "first_runs": result["runs"][:5],
        "last_runs": result["runs"][-5:],
    }, indent=2))
    print("BIO_CHI_LEE2014_SRA_SOURCE_MAP_PASS")


if __name__ == "__main__":
    main()
