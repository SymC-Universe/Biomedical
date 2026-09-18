from __future__ import annotations

import csv
import json
import re
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List

REGISTRY_REL = Path("GRI_v2/config/gri_conglomerate_c1_source_registry_20260918.json")
COVERAGE_REL = Path("GRI_v2/development_outputs/stage_c0_1_sample_identity/stage_c0_1_unique_match_coverage.csv")
OUTPUT_REL = Path("GRI_v2/artifacts/GRI_STAGE_A_IDENTITY_RECONSTRUCTION_AUDIT_20260918.json")

PATIENT_RE = re.compile(r"(TCGA-[A-Z0-9]{2}-[A-Z0-9]{4})")
ROOT_RE = re.compile(r"(TCGA-[A-Z0-9]{2}-[A-Z0-9]{4}-[0-9]{2}[A-Z])")
TYPE_RE = re.compile(r"TCGA-[A-Z0-9]{2}-[A-Z0-9]{4}-([0-9]{2})")

TCGA_CODES = [
    "ACC","BLCA","BRCA","CESC","CHOL","COAD","DLBC","ESCA","GBM","HNSC",
    "KICH","KIRC","KIRP","LAML","LGG","LIHC","LUAD","LUSC","MESO","OV",
    "PAAD","PCPG","PRAD","READ","SARC","SKCM","STAD","TGCT","THCA","THYM",
    "UCEC","UCS","UVM",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def fetch_rna_header(url: str, max_bytes: int = 2 * 1024 * 1024) -> List[str]:
    req = urllib.request.Request(
        url,
        headers={
            "Range": f"bytes=0-{max_bytes - 1}",
            "User-Agent": "GRI-Stage-A-Identity-Reconstruction/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read(max_bytes)
    first = data.decode("utf-8", errors="replace").splitlines()[0]
    return [x.strip().strip('"') for x in first.split("\t")]


def gdc_project_patients(code: str) -> List[str]:
    filt = {
        "op": "=",
        "content": {
            "field": "project.project_id",
            "value": f"TCGA-{code}",
        },
    }
    params = urllib.parse.urlencode({
        "filters": json.dumps(filt, separators=(",", ":")),
        "fields": "submitter_id,project.project_id",
        "format": "JSON",
        "size": "5000",
    })
    url = "https://api.gdc.cancer.gov/cases?" + params
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "GRI-Stage-A-Identity-Reconstruction/1.0"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    hits = payload["data"]["hits"]
    return [str(h["submitter_id"]) for h in hits]


def frozen_counts() -> Dict[str, int]:
    out: Dict[str, int] = {}
    with (repo_root() / COVERAGE_REL).open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            out[row["cancer_type"]] = int(row["stage_a_n"])
    return out


def main() -> None:
    registry = json.loads((repo_root() / REGISTRY_REL).read_text(encoding="utf-8"))
    rna = next(s for s in registry["sources"] if s["id"] == "RNA_PANCAN_FINAL")
    fields = fetch_rna_header(rna["url"])
    sample_ids = fields[1:]

    project_map: Dict[str, str] = {}
    project_case_counts: Dict[str, int] = {}
    project_conflicts: Dict[str, List[str]] = {}
    patient_projects: Dict[str, set[str]] = defaultdict(set)

    for code in TCGA_CODES:
        patients = gdc_project_patients(code)
        project_case_counts[code] = len(patients)
        for pid in patients:
            patient_projects[pid].add(code)

    for pid, codes in patient_projects.items():
        if len(codes) == 1:
            project_map[pid] = next(iter(codes))
        else:
            project_conflicts[pid] = sorted(codes)

    parsed = []
    by_patient_primary: Dict[str, List[str]] = defaultdict(list)
    unmapped_primary = []
    for sid in sample_ids:
        p = PATIENT_RE.search(sid)
        t = TYPE_RE.search(sid)
        root = ROOT_RE.search(sid)
        pid = p.group(1) if p else None
        stype = t.group(1) if t else None
        sroot = root.group(1) if root else None
        parsed.append((sid, pid, stype, sroot))
        if pid and stype == "01":
            by_patient_primary[pid].append(sid)
            if pid not in project_map:
                unmapped_primary.append(pid)

    primary_columns = [x for x in parsed if x[2] == "01" and x[1]]
    unique_primary_patients = sorted(by_patient_primary)
    duplicate_primary_patients = {
        p: sorted(v) for p, v in by_patient_primary.items() if len(v) > 1
    }

    counts = Counter()
    for pid in unique_primary_patients:
        code = project_map.get(pid)
        if code:
            counts[code] += 1

    expected = frozen_counts()
    comparison = {}
    mismatches = {}
    for code, exp in sorted(expected.items()):
        obs = int(counts.get(code, 0))
        comparison[code] = {"expected_stage_a_n": exp, "observed_unique_primary_patients": obs}
        if obs != exp:
            mismatches[code] = comparison[code]

    extra_primary_codes = {
        code: int(n) for code, n in sorted(counts.items()) if code not in expected and n
    }

    status = (
        "STAGE_A_IDENTITY_COUNTS_REPRODUCED"
        if not mismatches and not project_conflicts and not set(unmapped_primary)
        else "STAGE_A_IDENTITY_RECONSTRUCTION_REQUIRES_RECONCILIATION"
    )

    result = {
        "schema": "gri-stage-a-identity-reconstruction-audit-v1",
        "date": "2026-09-18",
        "status": status,
        "rna_header_fields": len(fields),
        "rna_sample_columns": len(sample_ids),
        "primary_01_columns": len(primary_columns),
        "unique_primary_01_patients": len(unique_primary_patients),
        "duplicate_primary_01_patients": len(duplicate_primary_patients),
        "duplicate_primary_preview": dict(list(sorted(duplicate_primary_patients.items()))[:25]),
        "gdc_project_case_counts": project_case_counts,
        "gdc_patient_project_conflicts": project_conflicts,
        "unmapped_primary_patients": sorted(set(unmapped_primary)),
        "observed_primary_by_project": dict(sorted((k, int(v)) for k, v in counts.items() if v)),
        "frozen_count_comparison": comparison,
        "frozen_count_mismatches": mismatches,
        "extra_primary_projects_not_in_frozen_32": extra_primary_codes,
        "biological_outcome_opened": False,
        "model_fit": False,
        "identity_only": True,
        "next_if_reproduced": (
            "freeze exact primary-sample selection if duplicate primary patients exist, "
            "then build the cloud Stage-A cache reconstruction package"
        ),
    }
    out = repo_root() / OUTPUT_REL
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
