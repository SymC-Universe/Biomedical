from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.request
from pathlib import Path

PATIENT_RE = re.compile(r"TCGA-[A-Z0-9]{2}-[A-Z0-9]{4}")
SAMPLE_RE = re.compile(r"TCGA-[A-Z0-9]{2}-[A-Z0-9]{4}-[0-9]{2}[A-Z]?")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Cancer-Stability-Atlas/Stage-B0"})
    with urllib.request.urlopen(req, timeout=180) as r, path.open("wb") as out:
        while True:
            chunk = r.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)


def scan_barcodes(path: Path) -> dict:
    patients: set[str] = set()
    samples: set[str] = set()
    first_nonempty = None
    with path.open("rb") as f:
        for line_b in f:
            line = line_b.decode("utf-8", errors="ignore")
            if first_nonempty is None and line.strip():
                first_nonempty = line.rstrip("\r\n")[:500]
            normalized = line.replace(".", "-")
            patients.update(PATIENT_RE.findall(normalized))
            samples.update(SAMPLE_RE.findall(normalized))
    primary_samples = {s for s in samples if len(s) >= 15 and s[13:15] == "01"}
    return {
        "unique_tcga_patients_detected": len(patients),
        "unique_tcga_sample_barcodes_detected": len(samples),
        "unique_primary_tumor_sample_barcodes_detected": len(primary_samples),
        "first_nonempty_line_preview": first_nonempty,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True)
    ap.add_argument("--download-dir", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
    dl_dir = Path(args.download_dir)
    records = []
    probe_roles = set(plan["stage_b0_probe_roles"])
    for src in plan["sources"]:
        if src["role"] not in probe_roles:
            continue
        path = dl_dir / src["file_name"]
        rec = {k: src[k] for k in ["id", "role", "independence", "circularity", "file_name", "gdc_uuid", "url"]}
        try:
            download(src["url"], path)
            rec.update({
                "download_status": "OK",
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
                **scan_barcodes(path),
            })
        except Exception as exc:
            rec.update({"download_status": "ERROR", "error": f"{type(exc).__name__}: {exc}"})
        records.append(rec)

    out = {
        "status": "STAGE_B0_SOURCE_PROBE_ONLY",
        "plan_version": plan["version"],
        "primary_data_family": plan["primary_data_family"],
        "no_biological_association_performed": True,
        "sources": records,
    }
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
