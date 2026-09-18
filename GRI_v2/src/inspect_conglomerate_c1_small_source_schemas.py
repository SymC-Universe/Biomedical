from __future__ import annotations

import csv
import json
import re
import urllib.request
from pathlib import Path
from typing import Any, Dict, List

CONFIG_REL = Path("GRI_v2/config/gri_conglomerate_c1_source_registry_20260918.json")
OUTPUT_REL = Path("GRI_v2/artifacts/GRI_CONGLOMERATE_C1_SMALL_SOURCE_SCHEMAS_20260918.json")

TCGA_PAT = re.compile(r"TCGA[-.][A-Z0-9]{2}[-.][A-Z0-9]{4}")
CANCER_CODE = re.compile(r"^[A-Z0-9]{2,5}$")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_registry() -> Dict[str, Any]:
    return json.loads((repo_root() / CONFIG_REL).read_text(encoding="utf-8"))


def download(url: str, path: Path) -> None:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "GRI-Conglomerate-C1-Schema-Inspect/1.0"},
    )
    with urllib.request.urlopen(req, timeout=180) as resp, path.open("wb") as out:
        while True:
            chunk = resp.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)


def read_lines(path: Path, limit: int = 8) -> List[str]:
    rows: List[str] = []
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.strip():
                rows.append(line.rstrip("\r\n"))
                if len(rows) >= limit:
                    break
    return rows


def split_line(line: str) -> List[str]:
    if "\t" in line:
        return line.split("\t")
    return next(csv.reader([line]))


def inspect_source(source: Dict[str, Any], workdir: Path) -> Dict[str, Any]:
    path = workdir / source["file_name"]
    download(source["url"], path)
    lines = read_lines(path)
    split = [split_line(x) for x in lines]
    first = split[0] if split else []
    second = split[1] if len(split) > 1 else []

    header_like = any(
        token.lower() in {
            "sample", "sampleid", "tumortype", "purity", "patient", "patient_id",
            "cancer_type", "cancer", "aneuploidy_score", "loh_frac_altered",
        }
        for token in first
    )

    obvious_cancer_columns = [
        token for token in first
        if any(key in token.lower() for key in ("tumor", "cancer", "cohort", "study"))
    ]

    tcga_fields_first_rows = []
    candidate_cancer_tokens = set()
    for row in split:
        for token in row:
            if TCGA_PAT.search(token.replace(".", "-")):
                tcga_fields_first_rows.append(token[:80])
            t = token.strip()
            if CANCER_CODE.fullmatch(t) and t not in {"NA", "TRUE", "FALSE"}:
                candidate_cancer_tokens.add(t)

    return {
        "id": source["id"],
        "file_name": source["file_name"],
        "bytes": path.stat().st_size,
        "field_count_first_row": len(first),
        "header_like": header_like,
        "first_row_fields": first[:250],
        "second_row_preview": second[:30],
        "obvious_cancer_columns": obvious_cancer_columns,
        "candidate_cancer_tokens_first_rows": sorted(candidate_cancer_tokens),
        "tcga_fields_first_rows": tcga_fields_first_rows[:20],
    }


def main() -> None:
    cfg = load_registry()
    sources = [
        s for s in cfg["sources"]
        if s["probe_policy"] == "full_hash_if_under_limit"
    ]
    workdir = Path("_c1_small_source_schema_probe")
    workdir.mkdir(exist_ok=True)
    rows = [inspect_source(s, workdir) for s in sources]

    result = {
        "schema": "gri-conglomerate-c1-small-source-schema-inspection-v1",
        "date": "2026-09-18",
        "status": "SCHEMA_INSPECTION_COMPLETE",
        "biological_outcome_opened": False,
        "model_fit": False,
        "sources": rows,
    }
    out = repo_root() / OUTPUT_REL
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
