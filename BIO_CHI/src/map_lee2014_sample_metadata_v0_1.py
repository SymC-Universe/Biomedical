#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[2]
BIO = ROOT / "BIO_CHI"
CFG = BIO / "config" / "LEE2014_SRA_SAMPLE_METADATA_FREEZE_v0_1.json"
PIN = BIO / "config" / "LEE2014_SRP040309_SOURCE_MAP_V01_RESULT_PIN.json"
OUT = BIO / "artifacts" / "generated"
OUT.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT / "lee2014_sra_sample_metadata_v0_1.json"
UA = "BioChiReviewerReproducibility/0.1"


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def text_at(elem, path: str):
    x = elem.find(path)
    if x is None or x.text is None:
        return None
    return x.text.strip()


def main() -> None:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    pin = json.loads(PIN.read_text(encoding="utf-8"))
    # Resolve current SRA record IDs from the already frozen accession, not by biology labels.
    q = urllib.parse.urlencode({
        "db":"sra","term":f'{cfg["study_accession"]}[Study Accession]',
        "retmax":100000,"retmode":"json","tool":"BioChiSourceQualification"
    })
    search_raw = fetch("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"+q)
    ids = json.loads(search_raw.decode("utf-8"))["esearchresult"]["idlist"]
    if len(ids) != pin["run_count"]:
        # NCBI internal record count need not equal run count in all studies, so preserve it rather than assume equality.
        pass
    q2 = urllib.parse.urlencode({
        "db":"sra","id":",".join(ids),"rettype":"full","retmode":"xml",
        "tool":"BioChiSourceQualification"
    })
    url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"+q2
    raw=fetch(url)
    root=ET.fromstring(raw)

    records=[]
    attr_counts=Counter()
    for pkg in root.findall(".//EXPERIMENT_PACKAGE"):
        exp=pkg.find("./EXPERIMENT")
        sample=pkg.find("./SAMPLE")
        submission=pkg.find("./SUBMISSION")
        study=pkg.find("./STUDY")
        if exp is None:
            continue
        exp_acc=exp.attrib.get("accession")
        sample_acc=sample.attrib.get("accession") if sample is not None else None
        exp_title=text_at(exp,"./TITLE")
        design_desc=text_at(exp,"./DESIGN/DESIGN_DESCRIPTION")
        library=exp.find("./DESIGN/LIBRARY_DESCRIPTOR")
        attrs={}
        if sample is not None:
            for a in sample.findall("./SAMPLE_ATTRIBUTES/SAMPLE_ATTRIBUTE"):
                tag=text_at(a,"./TAG")
                val=text_at(a,"./VALUE")
                if tag:
                    attrs[tag]=val
                    attr_counts[tag]+=1
        runs=[x.attrib.get("accession") for x in pkg.findall("./RUN_SET/RUN") if x.attrib.get("accession")]
        rec={
            "experiment":exp_acc,
            "experiment_title":exp_title,
            "design_description":design_desc,
            "sample":sample_acc,
            "sample_title":text_at(sample,"./TITLE") if sample is not None else None,
            "sample_description":text_at(sample,"./DESCRIPTION") if sample is not None else None,
            "sample_attributes":attrs,
            "runs":runs,
            "study":study.attrib.get("accession") if study is not None else None,
            "submission":submission.attrib.get("accession") if submission is not None else None,
        }
        if library is not None:
            rec["library_name"]=text_at(library,"./LIBRARY_NAME")
            rec["library_strategy"]=text_at(library,"./LIBRARY_STRATEGY")
            rec["library_source"]=text_at(library,"./LIBRARY_SOURCE")
            rec["library_selection"]=text_at(library,"./LIBRARY_SELECTION")
        records.append(rec)

    all_runs=sorted({run for r in records for run in r["runs"]})
    expected_runs=sorted(pin["runs"])
    missing=sorted(set(expected_runs)-set(all_runs))
    extra=sorted(set(all_runs)-set(expected_runs))
    result={
        "schema_version":"0.1",
        "generated_at_utc":datetime.now(timezone.utc).isoformat(),
        "gate":cfg["gate"],
        "metadata_xml_url":url,
        "metadata_xml_sha256":sha256(raw),
        "metadata_xml_size_bytes":len(raw),
        "package_count":len(records),
        "expected_runs":expected_runs,
        "mapped_runs":all_runs,
        "missing_expected_runs":missing,
        "extra_runs":extra,
        "sample_attribute_tag_counts":dict(sorted(attr_counts.items())),
        "records":records,
        "sequence_reads_downloaded":False,
        "molecular_values_interpreted":False,
        "status":"PASS_SRA_SAMPLE_METADATA_MAP" if not missing and not extra else "SOURCE_IDENTITY_MISMATCH"
    }
    OUT_FILE.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "output":str(OUT_FILE.relative_to(ROOT)),
        "status":result["status"],
        "package_count":len(records),
        "attribute_tags":list(result["sample_attribute_tag_counts"]),
        "titles":[r["experiment_title"] for r in records],
        "sample_titles":[r["sample_title"] for r in records],
        "missing_expected_runs":missing,
        "extra_runs":extra
    },indent=2))
    if result["status"]!="PASS_SRA_SAMPLE_METADATA_MAP":
        raise SystemExit("BIO_CHI_LEE2014_SAMPLE_METADATA_IDENTITY_MISMATCH")
    print("BIO_CHI_LEE2014_SAMPLE_METADATA_PASS")


if __name__=="__main__":
    main()
