#!/usr/bin/env python3
from __future__ import annotations

import gzip
import hashlib
import io
import json
import pathlib
import urllib.request
import zipfile
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[2]
BIO = ROOT / "BIO_CHI"
CFG = BIO / "config" / "BLUM2019_NATIVE_METRIC_INPUT_MAPPING_FREEZE_v0_1.json"
OUT = BIO / "artifacts" / "generated"
OUT.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT / "blum2019_native_metric_input_mapping_v0_1.json"
ARCHIVE = OUT / "blum2019_data_frozen.zip"
USER_AGENT = "BioChiReviewerReproducibility/0.1"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, path: pathlib.Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/zip,*/*;q=0.5"})
    with urllib.request.urlopen(req, timeout=180) as r, path.open("wb") as fh:
        while True:
            chunk = r.read(1024 * 1024)
            if not chunk:
                break
            fh.write(chunk)


def first_text_line(payload: bytes) -> str:
    return payload.decode("utf-8-sig", errors="replace").splitlines()[0] if payload else ""


def main() -> None:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    pin = json.loads((BIO / "config" / "BLUM2019_MENDELEY_SOURCE_FREEZE_V02_RESULT_PIN.json").read_text(encoding="utf-8"))
    download(pin["selected_file"]["download_url"], ARCHIVE)
    observed = sha256_file(ARCHIVE)
    if observed != cfg["frozen_archive_sha256"]:
        raise SystemExit(f"BLUM_INPUT_MAPPING_HASH_MISMATCH expected={cfg['frozen_archive_sha256']} observed={observed}")

    allowed = cfg["allowed_members"]
    records = []
    readme_text = None
    with zipfile.ZipFile(ARCHIVE, "r") as zf:
        names = set(zf.namelist())
        missing = [p for p in allowed if p not in names]
        if missing:
            raise SystemExit(f"BLUM_INPUT_MAPPING_MISSING_MEMBERS {missing}")
        for path in allowed:
            raw = zf.read(path)
            rec = {
                "path": path,
                "member_sha256": sha256(raw),
                "member_size_bytes": len(raw),
            }
            if path.endswith("README.txt"):
                readme_text = raw.decode("utf-8", errors="replace")
                rec["inspection"] = "FULL_README_TEXT"
                rec["text"] = readme_text
            elif path.endswith(".csv.gz"):
                with gzip.GzipFile(fileobj=io.BytesIO(raw), mode="rb") as gz:
                    header = gz.readline()
                rec["inspection"] = "CSV_HEADER_ONLY_FROM_GZIP"
                rec["header"] = first_text_line(header)
            elif path.endswith(".csv"):
                header = raw.splitlines()[0] if raw else b""
                rec["inspection"] = "CSV_HEADER_ONLY"
                rec["header"] = first_text_line(header)
            else:
                rec["inspection"] = "UNEXPECTED_ALLOWED_TYPE"
            records.append(rec)

    # Do not infer biological semantics beyond explicit header/README text.
    result = {
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "gate": cfg["gate"],
        "source_config": str(CFG.relative_to(ROOT)),
        "archive_sha256": observed,
        "data_rows_read": False,
        "metric_computed": False,
        "scientific_values_interpreted": False,
        "records": records,
        "status": "PASS_DOCUMENTATION_AND_HEADERS_CAPTURED",
    }
    OUT_FILE.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    ARCHIVE.unlink(missing_ok=True)
    print(json.dumps({
        "output": str(OUT_FILE.relative_to(ROOT)),
        "status": result["status"],
        "record_count": len(records),
        "data_rows_read": False,
        "metric_computed": False,
        "headers": {r["path"]: r.get("header") for r in records if "header" in r},
    }, indent=2))
    print("BIO_CHI_BLUM_NATIVE_INPUT_MAPPING_PASS")


if __name__ == "__main__":
    main()
