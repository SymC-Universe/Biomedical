from __future__ import annotations

import csv
import json
import re
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

TCGA_CODES = [
    "ACC","BLCA","BRCA","CESC","CHOL","COAD","DLBC","ESCA","GBM","HNSC",
    "KICH","KIRC","KIRP","LAML","LGG","LIHC","LUAD","LUSC","MESO","OV",
    "PAAD","PCPG","PRAD","READ","SARC","SKCM","STAD","TGCT","THCA","THYM",
    "UCEC","UCS","UVM",
]
PATIENT_RE = re.compile(r"(TCGA-[A-Z0-9]{2}-[A-Z0-9]{4})", re.I)
ROOT_RE = re.compile(r"(TCGA-[A-Z0-9]{2}-[A-Z0-9]{4}-[0-9]{2}[A-Z])", re.I)
TYPE_RE = re.compile(r"TCGA-[A-Z0-9]{2}-[A-Z0-9]{4}-([0-9]{2})", re.I)
UA = "GRI-BioSystems-TumorNormal-SourceGate/1.0"

def root_dir() -> Path:
    return Path(__file__).resolve().parents[2]

def normalize(x: str) -> str:
    return x.strip().strip('"').upper().replace(".", "-")

def fetch_first_line(url: str, chunk: int = 1024 * 1024, max_bytes: int = 8 * 1024 * 1024) -> str:
    buf = b""
    start = 0
    while start < max_bytes:
        end = min(start + chunk - 1, max_bytes - 1)
        req = urllib.request.Request(url, headers={"Range": f"bytes={start}-{end}", "User-Agent": UA})
        with urllib.request.urlopen(req, timeout=180) as resp:
            part = resp.read()
        buf += part
        if b"\n" in buf:
            return buf.splitlines()[0].decode("utf-8", errors="strict")
        if not part:
            break
        start = end + 1
    raise RuntimeError("Header newline not found within max_bytes")

def parse_labels(line: str) -> list[str]:
    fields = line.rstrip("\r\n").split("\t")
    if len(fields) < 2:
        raise RuntimeError("Header has fewer than two fields")
    return [normalize(x) for x in fields[1:]]

def sample_root(label: str):
    m = ROOT_RE.search(label)
    return normalize(m.group(1)) if m else None

def patient(label: str):
    m = PATIENT_RE.search(label)
    return normalize(m.group(1)) if m else None

def sample_type(label: str):
    m = TYPE_RE.search(label)
    return m.group(1) if m else None

def gdc_project_map():
    pmap = {}
    conflicts = {}
    all_codes = defaultdict(set)
    for code in TCGA_CODES:
        filt = {"op": "=", "content": {"field": "project.project_id", "value": f"TCGA-{code}"}}
        params = urllib.parse.urlencode({
            "filters": json.dumps(filt, separators=(",", ":")),
            "fields": "submitter_id,project.project_id",
            "format": "JSON",
            "size": "5000",
        })
        req = urllib.request.Request("https://api.gdc.cancer.gov/cases?" + params, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=180) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        for hit in payload["data"]["hits"]:
            all_codes[normalize(str(hit["submitter_id"]))].add(code)
    for pid, codes in all_codes.items():
        if len(codes) == 1:
            pmap[pid] = next(iter(codes))
        else:
            conflicts[pid] = sorted(codes)
    return pmap, conflicts

def modality_inventory(labels: list[str]):
    by_type_patient = defaultdict(lambda: defaultdict(set))
    by_type_roots = defaultdict(Counter)
    unparsed = []
    for label in labels:
        pid = patient(label)
        st = sample_type(label)
        rt = sample_root(label)
        if not pid or not st or not rt:
            unparsed.append(label)
            continue
        by_type_patient[st][pid].add(rt)
        by_type_roots[st][rt] += 1
    return by_type_patient, by_type_roots, unparsed

def unique_patients(d):
    return {pid for pid, roots in d.items() if len(roots) == 1}

def main():
    cfg_path = root_dir() / "GRI_v2/config/biosystems_tumor_normal_source_gate_20260922.json"
    cfg = json.loads(cfg_path.read_text())
    rna_url = "https://api.gdc.cancer.gov/data/" + cfg["source_bindings"]["rna"]["gdc_uuid"]
    met_url = "https://api.gdc.cancer.gov/data/" + cfg["source_bindings"]["methylation"]["gdc_uuid"]

    rna_labels = parse_labels(fetch_first_line(rna_url))
    met_labels = parse_labels(fetch_first_line(met_url))
    pmap, conflicts = gdc_project_map()

    rna, rna_roots, rna_unparsed = modality_inventory(rna_labels)
    met, met_roots, met_unparsed = modality_inventory(met_labels)

    types = ["01", "11"]
    rows = []
    details = {"rna": {}, "methylation": {}}
    for st in types:
        details["rna"][st] = {
            "sample_columns": sum(len(v) for v in rna[st].values()),
            "unique_patients_single_root": len(unique_patients(rna[st])),
            "patients_with_multiple_roots": sum(1 for v in rna[st].values() if len(v) > 1),
            "duplicate_sample_roots": sum(1 for n in rna_roots[st].values() if n > 1),
        }
        details["methylation"][st] = {
            "sample_columns": sum(len(v) for v in met[st].values()),
            "unique_patients_single_root": len(unique_patients(met[st])),
            "patients_with_multiple_roots": sum(1 for v in met[st].values() if len(v) > 1),
            "duplicate_sample_roots": sum(1 for n in met_roots[st].values() if n > 1),
        }

    rna_unique = {st: unique_patients(rna[st]) for st in types}
    met_unique = {st: unique_patients(met[st]) for st in types}
    cross = {st: rna_unique[st] & met_unique[st] for st in types}
    complete_pair = cross["01"] & cross["11"]

    for code in TCGA_CODES:
        def nset(s):
            return sum(1 for pid in s if pmap.get(pid) == code)
        row = {
            "cancer_type": code,
            "rna_tumor_01_unique": nset(rna_unique["01"]),
            "rna_normal_11_unique": nset(rna_unique["11"]),
            "methylation_tumor_01_unique": nset(met_unique["01"]),
            "methylation_normal_11_unique": nset(met_unique["11"]),
            "crossmodal_tumor_01_unique": nset(cross["01"]),
            "crossmodal_normal_11_unique": nset(cross["11"]),
            "complete_paired_01_11_crossmodal": nset(complete_pair),
        }
        row["primary_n30_eligible"] = row["crossmodal_tumor_01_unique"] >= 30 and row["crossmodal_normal_11_unique"] >= 30
        row["paired_n15_eligible"] = row["complete_paired_01_11_crossmodal"] >= 15
        row["small_normal_n20_sensitivity"] = 20 <= row["crossmodal_normal_11_unique"] <= 29
        rows.append(row)

    out_dir = root_dir() / "GRI_v2/development_outputs/biosystems_tumor_normal_source_gate"
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "TUMOR_NORMAL_SOURCE_COUNTS.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    summary = {
        "schema": "gri-biosystems-tumor-normal-source-gate-result-v1",
        "status": "SOURCE_GATE_COMPLETE_NO_BIOLOGICAL_VALUES",
        "rna_header_sample_columns": len(rna_labels),
        "methylation_header_sample_columns": len(met_labels),
        "sample_type_definitions": cfg["sample_types"],
        "modality_inventory": details,
        "primary_n30_eligible_cancers": [r["cancer_type"] for r in rows if r["primary_n30_eligible"]],
        "paired_n15_eligible_cancers": [r["cancer_type"] for r in rows if r["paired_n15_eligible"]],
        "small_normal_n20_sensitivity_cancers": [r["cancer_type"] for r in rows if r["small_normal_n20_sensitivity"]],
        "gdc_patient_project_conflicts": conflicts,
        "rna_unparsed_header_labels": rna_unparsed[:25],
        "methylation_unparsed_header_labels": met_unparsed[:25],
        "biological_values_opened": False,
        "feature_calculation_performed": False,
        "model_fit_performed": False,
        "outcome_selected_filtering_performed": False,
        "next_gate": "freeze exact tumor-normal analysis implementation against these source-feasibility counts before reading molecular values",
    }
    (out_dir / "TUMOR_NORMAL_SOURCE_GATE_SUMMARY.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
