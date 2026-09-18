from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

REGISTRY_REL = Path("GRI_v2/config/gri_conglomerate_c1_source_registry_20260918.json")
C1_FREEZE_REL = Path("GRI_v2/config/stage_c1_frozen_v2.json")
COVERAGE_REL = Path("GRI_v2/development_outputs/stage_c0_1_sample_identity/stage_c0_1_unique_match_coverage.csv")
OUTPUT_REL = Path("GRI_v2/artifacts/GRI_STAGE_A_FINITE_FILTER_RECONSTRUCTION_AUDIT_20260918.json")

PATIENT_RE = re.compile(r"(TCGA-[A-Z0-9]{2}-[A-Z0-9]{4})")
TYPE_RE = re.compile(r"TCGA-[A-Z0-9]{2}-[A-Z0-9]{4}-([0-9]{2})")

TCGA_CODES = [
    "ACC","BLCA","BRCA","CESC","CHOL","COAD","DLBC","ESCA","GBM","HNSC",
    "KICH","KIRC","KIRP","LAML","LGG","LIHC","LUAD","LUSC","MESO","OV",
    "PAAD","PCPG","PRAD","READ","SARC","SKCM","STAD","TGCT","THCA","THYM",
    "UCEC","UCS","UVM",
]
THRESHOLDS = [0.80, 0.90, 0.95, 0.975, 0.99, 1.0]


def root() -> Path:
    return Path(__file__).resolve().parents[2]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, path: Path) -> None:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "GRI-Stage-A-Finite-Audit/1.0"},
    )
    with urllib.request.urlopen(req, timeout=300) as resp, path.open("wb") as out:
        while True:
            chunk = resp.read(4 * 1024 * 1024)
            if not chunk:
                break
            out.write(chunk)


def get_hallmark_gmt(cfg: Dict[str, Any], path: Path) -> str:
    expected = cfg["inputs"]["hallmark_membership_sha256"]
    errors = []
    for url in cfg["inputs"]["hallmark_download_urls"]:
        try:
            download(url, path)
            observed = sha256_file(path)
            if observed == expected:
                return observed
            errors.append(f"{url}: hash {observed} != {expected}")
        except Exception as exc:
            errors.append(f"{url}: {type(exc).__name__}: {exc}")
    raise RuntimeError("Could not obtain frozen Hallmark file: " + " | ".join(errors))


def hallmark_union(gmt_path: Path) -> set[str]:
    genes: set[str] = set()
    with gmt_path.open("r", encoding="utf-8") as f:
        for line in f:
            p = line.rstrip("\r\n").split("\t")
            genes.update(x for x in p[2:] if x)
    return genes


def gdc_project_map() -> Dict[str, str]:
    out: Dict[str, str] = {}
    for code in TCGA_CODES:
        filt = {
            "op": "=",
            "content": {"field": "project.project_id", "value": f"TCGA-{code}"},
        }
        params = urllib.parse.urlencode({
            "filters": json.dumps(filt, separators=(",", ":")),
            "fields": "submitter_id",
            "format": "JSON",
            "size": "5000",
        })
        req = urllib.request.Request(
            "https://api.gdc.cancer.gov/cases?" + params,
            headers={"User-Agent": "GRI-Stage-A-Finite-Audit/1.0"},
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        for hit in payload["data"]["hits"]:
            pid = str(hit["submitter_id"])
            if pid in out and out[pid] != code:
                raise ValueError(f"GDC patient appears in multiple TCGA projects: {pid}")
            out[pid] = code
    return out


def frozen_counts() -> Dict[str, int]:
    out: Dict[str, int] = {}
    with (root() / COVERAGE_REL).open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            out[row["cancer_type"]] = int(row["stage_a_n"])
    return out


def parse_gene_symbol(raw: str) -> str:
    token = raw.strip().strip('"')
    return token.split("|", 1)[0]


def finite_token(token: str) -> bool:
    x = token.strip().strip('"')
    if not x or x.upper() in {"NA", "NAN", "NULL"}:
        return False
    try:
        return math.isfinite(float(x))
    except ValueError:
        return False


def main() -> None:
    registry = json.loads((root() / REGISTRY_REL).read_text(encoding="utf-8"))
    c1 = json.loads((root() / C1_FREEZE_REL).read_text(encoding="utf-8"))
    rna = next(s for s in registry["sources"] if s["id"] == "RNA_PANCAN_FINAL")

    work = Path("_stage_a_finite_filter_audit")
    work.mkdir(exist_ok=True)
    rna_path = work / rna["file_name"]
    gmt_path = work / "h.all.v2026.1.Hs.symbols.gmt"

    download(rna["url"], rna_path)
    observed_rna_sha = sha256_file(rna_path)
    if observed_rna_sha != rna["expected_sha256"]:
        raise ValueError(f"RNA SHA mismatch {observed_rna_sha} != {rna['expected_sha256']}")
    observed_gmt_sha = get_hallmark_gmt(c1, gmt_path)
    hallmarks = hallmark_union(gmt_path)

    with rna_path.open("r", encoding="utf-8", errors="strict") as f:
        header = f.readline().rstrip("\r\n").split("\t")
        sample_ids = [x.strip().strip('"') for x in header[1:]]

        primary_positions = []
        primary_ids = []
        primary_patients = []
        for j, sid in enumerate(sample_ids, start=1):
            pm = PATIENT_RE.search(sid)
            tm = TYPE_RE.search(sid)
            if pm and tm and tm.group(1) == "01":
                primary_positions.append(j)
                primary_ids.append(sid)
                primary_patients.append(pm.group(1))

        finite_counts = [0] * len(primary_positions)
        seen_hallmark_symbols: List[str] = []
        duplicate_symbol_counts = Counter()

        for line_no, line in enumerate(f, start=2):
            first_tab = line.find("\t")
            if first_tab < 0:
                continue
            symbol = parse_gene_symbol(line[:first_tab])
            if symbol not in hallmarks:
                continue
            duplicate_symbol_counts[symbol] += 1
            fields = line.rstrip("\r\n").split("\t")
            if len(fields) != len(header):
                raise ValueError(
                    f"RNA row {line_no} field count {len(fields)} != header {len(header)}"
                )
            seen_hallmark_symbols.append(symbol)
            for k, pos in enumerate(primary_positions):
                if finite_token(fields[pos]):
                    finite_counts[k] += 1

    observed_unique_symbols = sorted(set(seen_hallmark_symbols))
    duplicate_hallmark_symbols = {
        k: int(v) for k, v in duplicate_symbol_counts.items() if v > 1
    }
    denom_rows = len(seen_hallmark_symbols)

    project_map = gdc_project_map()
    expected = frozen_counts()

    sample_rows = []
    for sid, pid, count in zip(primary_ids, primary_patients, finite_counts):
        sample_rows.append({
            "sample_id": sid,
            "patient_id": pid,
            "project": project_map.get(pid),
            "finite_count": int(count),
            "finite_fraction": (float(count) / denom_rows) if denom_rows else float("nan"),
        })

    threshold_results: Dict[str, Any] = {}
    for threshold in THRESHOLDS:
        eligible = [r for r in sample_rows if r["finite_fraction"] >= threshold]
        by_patient: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        for r in eligible:
            by_patient[r["patient_id"]].append(r)

        counts_by_project = Counter()
        for pid, rows in by_patient.items():
            code = project_map.get(pid)
            if code:
                counts_by_project[code] += 1

        mismatches = {}
        for code, exp in sorted(expected.items()):
            obs = int(counts_by_project.get(code, 0))
            if obs != exp:
                mismatches[code] = {"expected": exp, "observed": obs}

        threshold_results[f"{threshold:.3f}"] = {
            "eligible_primary_columns": len(eligible),
            "eligible_unique_patients": len(by_patient),
            "counts_by_project": dict(sorted((k, int(v)) for k, v in counts_by_project.items() if v)),
            "frozen_count_mismatches": mismatches,
            "mismatch_cancer_count": len(mismatches),
        }

    exact_thresholds = [
        t for t, row in threshold_results.items()
        if row["mismatch_cancer_count"] == 0
    ]

    result = {
        "schema": "gri-stage-a-finite-filter-reconstruction-audit-v1",
        "date": "2026-09-18",
        "status": (
            "FINITE_FILTER_EXACTLY_REPRODUCES_FROZEN_COUNTS"
            if exact_thresholds
            else "FINITE_FILTER_DOES_NOT_FULLY_REPRODUCE_FROZEN_COUNTS"
        ),
        "rna_sha256": observed_rna_sha,
        "hallmark_membership_sha256": observed_gmt_sha,
        "hallmark_union_membership_count": len(hallmarks),
        "hallmark_rows_found_in_rna": denom_rows,
        "unique_hallmark_symbols_found_in_rna": len(observed_unique_symbols),
        "duplicate_hallmark_symbols_in_rna": duplicate_hallmark_symbols,
        "raw_rna_sample_columns": len(sample_ids),
        "primary_01_columns": len(primary_ids),
        "primary_01_unique_patients": len(set(primary_patients)),
        "finite_fraction_min": min(r["finite_fraction"] for r in sample_rows),
        "finite_fraction_median": sorted(r["finite_fraction"] for r in sample_rows)[len(sample_rows)//2],
        "threshold_results": threshold_results,
        "exact_frozen_count_thresholds": exact_thresholds,
        "expected_frozen_stage_a_total": int(sum(expected.values())),
        "historical_nonfinite_hallmark_cells": 141836,
        "biological_outcome_opened": False,
        "model_fit": False,
        "interpretation": (
            "reproducibility diagnostic only; no threshold becomes a new scientific rule "
            "merely because it matches the historical count"
        ),
    }
    out = root() / OUTPUT_REL
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "hallmark_union_membership_count": result["hallmark_union_membership_count"],
        "hallmark_rows_found_in_rna": result["hallmark_rows_found_in_rna"],
        "primary_01_columns": result["primary_01_columns"],
        "primary_01_unique_patients": result["primary_01_unique_patients"],
        "exact_frozen_count_thresholds": result["exact_frozen_count_thresholds"],
        "threshold_mismatch_counts": {
            k: v["mismatch_cancer_count"] for k, v in result["threshold_results"].items()
        },
        "output": str(OUTPUT_REL),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
