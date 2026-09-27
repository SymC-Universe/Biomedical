#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import urllib.request
import zipfile
from collections import Counter
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[2]
BIO = ROOT / "BIO_CHI"
CFG = BIO / "config" / "BLUM2019_SCHEMA_INVENTORY_FREEZE_v0_1.json"
OUT = BIO / "artifacts" / "generated"
OUT.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT / "blum2019_schema_inventory_v0_1.json"
ARCHIVE_PATH = OUT / "blum2019_data_frozen.zip"
USER_AGENT = "BioChiReviewerReproducibility/0.1"


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, path: pathlib.Path) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/zip,*/*;q=0.5"})
    with urllib.request.urlopen(req, timeout=180) as r, path.open("wb") as fh:
        while True:
            chunk = r.read(1024 * 1024)
            if not chunk:
                break
            fh.write(chunk)
        return {
            "resolved_url": r.geturl(),
            "http_status": getattr(r, "status", None),
            "content_type": r.headers.get("Content-Type"),
            "content_length_header": r.headers.get("Content-Length"),
            "etag": r.headers.get("ETag"),
            "last_modified": r.headers.get("Last-Modified"),
        }


def extension(name: str) -> str:
    p = pathlib.PurePosixPath(name)
    if name.endswith("/"):
        return ""
    return p.suffix.lower()


def top_level(name: str) -> str:
    stripped = name.strip("/")
    return stripped.split("/", 1)[0] if stripped else ""


def main() -> None:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    expected = cfg["frozen_archive_sha256"]
    meta = download(cfg["frozen_download_url"], ARCHIVE_PATH)
    observed = sha256_file(ARCHIVE_PATH)
    if observed != expected:
        raise SystemExit(f"BLUM_SCHEMA_INVENTORY_HASH_MISMATCH expected={expected} observed={observed}")

    members = []
    extension_counts = Counter()
    top_counts = Counter()
    total_uncompressed = 0
    total_compressed = 0

    # infolist() reads ZIP directory metadata only. Member payloads are never opened/read.
    with zipfile.ZipFile(ARCHIVE_PATH, "r") as zf:
        for info in zf.infolist():
            ext = extension(info.filename)
            top = top_level(info.filename)
            extension_counts[ext or "<none>"] += 1
            top_counts[top or "<root>"] += 1
            total_uncompressed += info.file_size
            total_compressed += info.compress_size
            members.append({
                "path": info.filename,
                "is_dir": info.is_dir(),
                "file_size": info.file_size,
                "compress_size": info.compress_size,
                "crc32_hex": f"{info.CRC:08x}",
                "extension": ext,
                "top_level": top,
            })

    result = {
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "gate": cfg["gate"],
        "source_config": str(CFG.relative_to(ROOT)),
        "archive_sha256": observed,
        "archive_size_bytes": ARCHIVE_PATH.stat().st_size,
        "download_meta": meta,
        "member_payloads_read": False,
        "scientific_values_interpreted": False,
        "member_count": len(members),
        "total_uncompressed_bytes": total_uncompressed,
        "total_compressed_bytes": total_compressed,
        "extension_counts": dict(sorted(extension_counts.items())),
        "top_level_counts": dict(sorted(top_counts.items())),
        "members": members,
        "status": "PASS_METADATA_ONLY_INVENTORY",
    }
    OUT_FILE.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    ARCHIVE_PATH.unlink(missing_ok=True)
    print(json.dumps({
        "output": str(OUT_FILE.relative_to(ROOT)),
        "status": result["status"],
        "archive_sha256": observed,
        "member_count": len(members),
        "member_payloads_read": False,
        "extension_counts": result["extension_counts"],
        "top_level_counts": result["top_level_counts"],
    }, indent=2))
    print("BIO_CHI_BLUM_SCHEMA_INVENTORY_PASS")


if __name__ == "__main__":
    main()
