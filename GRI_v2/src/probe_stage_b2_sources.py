from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.request
from pathlib import Path

PATIENT_RE = re.compile(r"TCGA[-.][A-Z0-9]{2}[-.][A-Z0-9]{4}")
SAMPLE_RE = re.compile(r"TCGA[-.][A-Z0-9]{2}[-.][A-Z0-9]{4}[-.][0-9]{2}[A-Z]?")
USER_AGENT = "Cancer-Stability-Atlas/Stage-B2"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _header_dict(response) -> dict:
    return {str(k).lower(): str(v) for k, v in response.headers.items()}


def probe_data_endpoint(url: str) -> dict:
    """Inspect the legacy PanCanAtlas data endpoint without downloading the file.

    The publication-supplement UUIDs remain downloadable through /data/{uuid}
    even when the current /files/{uuid} metadata route does not index them.
    Prefer HEAD; fall back to a one-byte Range request if HEAD is unsupported.
    """
    head_error = None
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT}, method="HEAD")
        with urllib.request.urlopen(req, timeout=180) as r:
            headers = _header_dict(r)
            length = headers.get("content-length")
            return {
                "metadata_status": "OK_DATA_ENDPOINT_HEAD",
                "http_status": getattr(r, "status", None),
                "content_length": int(length) if length and length.isdigit() else None,
                "content_type": headers.get("content-type"),
                "content_disposition": headers.get("content-disposition"),
                "accept_ranges": headers.get("accept-ranges"),
            }
    except Exception as exc:
        head_error = f"{type(exc).__name__}: {exc}"

    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": USER_AGENT, "Range": "bytes=0-0"},
        )
        with urllib.request.urlopen(req, timeout=180) as r:
            headers = _header_dict(r)
            # Read a single byte only. Closing the response prevents accidental
            # acquisition of a deferred large assay if Range is ignored.
            r.read(1)
            content_range = headers.get("content-range")
            total = None
            if content_range and "/" in content_range:
                tail = content_range.rsplit("/", 1)[-1]
                if tail.isdigit():
                    total = int(tail)
            if total is None:
                length = headers.get("content-length")
                if length and length.isdigit() and getattr(r, "status", None) == 200:
                    total = int(length)
            return {
                "metadata_status": "OK_DATA_ENDPOINT_RANGE",
                "http_status": getattr(r, "status", None),
                "content_length": total,
                "content_type": headers.get("content-type"),
                "content_disposition": headers.get("content-disposition"),
                "accept_ranges": headers.get("accept-ranges"),
                "content_range": content_range,
                "head_error": head_error,
            }
    except Exception as exc:
        return {
            "metadata_status": "ERROR",
            "metadata_error": f"HEAD={head_error}; RANGE={type(exc).__name__}: {exc}",
        }


def download(url: str, path: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
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
        data_url = f"https://api.gdc.cancer.gov/data/{src['gdc_uuid']}"
        rec.update(probe_data_endpoint(data_url))

        if src["download_now"]:
            path = dl_dir / src["file_name"]
            try:
                download(data_url, path)
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
