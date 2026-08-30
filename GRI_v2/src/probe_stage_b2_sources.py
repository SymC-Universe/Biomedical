from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.request
from pathlib import Path

PATIENT_RE = re.compile(r"TCGA[-.][A-Z0-9]{2}[-.][A-Z0-9]{4}")
SAMPLE_RE = re.compile(r"TCGA[-.][A-Z0-9]{2}[-.][A-Z0-9]{4}[-.][0-9]{2}[A-Z]?")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def request_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "Cancer-Stability-Atlas/Stage-B2"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.load(r)


def download(url: str, path: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "Cancer-Stability-Atlas/Stage-B2"})
    with urllib.request.urlopen(req, timeout=180) as r, path.open("wb") as out:
        while True:
            chunk = r.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)


def scan(path: Path) -> dict:
    patients: set[str] = set()
    samples: set[str] = set()
    preview = None
    with path.open("rb") as f:
        for line_b in f:
            line = line_b.decode("utf-8", errors="ignore")
            if preview is None and line.strip():
                preview = line.rstrip()[:500]
            patients.update(x.replace(".", "-") for x in PATIENT_RE.findall(line))
            samples.update(x.replace(".", "-") for x in SAMPLE_RE.findall(line))
    return {
        "unique_tcga_patients_detected": len(patients),
        "unique_tcga_sample_roots_detected": len(samples),
        "first_nonempty_line_preview": preview,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True)
    ap.add_argument("--download-dir", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
    dl_dir = Path(args.download_dir)
    dl_dir.mkdir(parents=True, exist_ok=True)
    records = []

    for src in plan["sources"]:
        rec = {k: src[k] for k in ["id", "role", "file_name", "gdc_uuid", "download_now", "independence"]}
        meta_url = (
            f"https://api.gdc.cancer.gov/files/{src['gdc_uuid']}?"
            "fields=file_id,file_name,file_size,md5sum,access,data_category,data_type,experimental_strategy"
        )
        try:
            rec["gdc_metadata"] = request_json(meta_url).get("data", {})
            rec["metadata_status"] = "OK"
        except Exception as exc:
            rec["metadata_status"] = "ERROR"
            rec["metadata_error"] = f"{type(exc).__name__}: {exc}"

        if src["download_now"]:
            path = dl_dir / src["file_name"]
            try:
                download(f"https://api.gdc.cancer.gov/data/{src['gdc_uuid']}", path)
                rec.update({
                    "download_status": "OK",
                    "downloaded_bytes": path.stat().st_size,
                    "sha256": sha256_file(path),
                    **scan(path),
                })
            except Exception as exc:
                rec["download_status"] = "ERROR"
                rec["download_error"] = f"{type(exc).__name__}: {exc}"
        else:
            rec["download_status"] = "DEFERRED_METADATA_ONLY"
        records.append(rec)

    out = {
        "status": "STAGE_B2_SOURCE_PROBE_ONLY",
        "plan_version": plan["version"],
        "no_biological_association_performed": True,
        "sources": records,
    }
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
