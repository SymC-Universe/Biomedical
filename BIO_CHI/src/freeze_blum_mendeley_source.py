#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import html
import json
import pathlib
import re
import urllib.parse
import urllib.request
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[2]
BIO = ROOT / "BIO_CHI"
OUT = BIO / "artifacts" / "generated"
OUT.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT / "blum2019_mendeley_source_freeze_v0_1.json"

DATASET_ID = "ccnxn84w8z"
VERSION = 2
FILENAME = "data.zip"
LANDING = f"https://data.mendeley.com/datasets/{DATASET_ID}/{VERSION}"
MAX_BYTES = 250 * 1024 * 1024
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/140.0 Safari/537.36"
)


def req(url: str):
    return urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/zip,application/octet-stream,text/html;q=0.8,*/*;q=0.5",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": LANDING,
        },
    )


def get(url: str) -> tuple[bytes, dict]:
    with urllib.request.urlopen(req(url), timeout=180) as r:
        meta = {
            "requested_url": url,
            "resolved_url": r.geturl(),
            "http_status": getattr(r, "status", None),
            "content_type": r.headers.get("Content-Type"),
            "content_length_header": r.headers.get("Content-Length"),
            "content_disposition": r.headers.get("Content-Disposition"),
            "etag": r.headers.get("ETag"),
            "last_modified": r.headers.get("Last-Modified"),
        }
        chunks = []
        total = 0
        while True:
            chunk = r.read(1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_BYTES:
                return b"", {**meta, "size_bytes_observed": total, "download_status": "DEFERRED_OVER_LIMIT"}
            chunks.append(chunk)
    data = b"".join(chunks)
    return data, {**meta, "size_bytes_observed": len(data), "download_status": "DOWNLOADED"}


def is_zip(data: bytes) -> bool:
    return data.startswith((b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08"))


def candidate_urls_from_landing() -> tuple[list[str], dict]:
    raw, meta = get(LANDING)
    text = raw.decode("utf-8", errors="replace")
    decoded = html.unescape(text).replace("\\/", "/")
    urls = set()

    for match in re.findall(r"https?://[^\"'<>\\s]+", decoded):
        u = match.rstrip("),]}")
        if DATASET_ID in u and ("public-files" in u or "file_downloaded" in u or "/download" in u):
            urls.add(u)

    for match in re.findall(r"/public-files/datasets/[^\"'<>\\s]+", decoded):
        urls.add(urllib.parse.urljoin("https://data.mendeley.com", match.rstrip("),]}")))

    # Metadata-only context around the expected filename helps diagnose API/page shape
    contexts = []
    lower = decoded.lower()
    target = FILENAME.lower()
    start = 0
    while len(contexts) < 8:
        i = lower.find(target, start)
        if i < 0:
            break
        contexts.append(decoded[max(0, i-220): min(len(decoded), i+420)])
        start = i + len(target)

    return sorted(urls), {
        "landing_meta": meta,
        "landing_sha256": hashlib.sha256(raw).hexdigest(),
        "landing_size_bytes": len(raw),
        "filename_contexts": contexts,
        "scientific_values_interpreted": False,
    }


def main() -> None:
    candidates = [
        f"https://data.mendeley.com/public-files/datasets/{DATASET_ID}/files/{urllib.parse.quote(FILENAME)}/download",
        f"https://data.mendeley.com/public-files/datasets/{DATASET_ID}/files/{urllib.parse.quote(FILENAME)}/file_downloaded",
    ]
    discovery_error = None
    landing_info = None
    try:
        discovered, landing_info = candidate_urls_from_landing()
        candidates.extend(discovered)
    except Exception as exc:
        discovery_error = f"{type(exc).__name__}: {exc}"

    seen = set()
    attempts = []
    success = None
    for url in candidates:
        if url in seen:
            continue
        seen.add(url)
        try:
            data, meta = get(url)
        except Exception as exc:
            attempts.append({"requested_url": url, "status": "REQUEST_ERROR", "error": f"{type(exc).__name__}: {exc}"})
            continue
        if meta.get("download_status") == "DEFERRED_OVER_LIMIT":
            attempts.append({**meta, "status": "DEFERRED_OVER_LIMIT"})
            continue
        if is_zip(data):
            success = {
                **meta,
                "status": "FROZEN_ZIP_BYTES",
                "zip_magic_verified": True,
                "sha256": hashlib.sha256(data).hexdigest(),
                "archive_contents_opened": False,
            }
            break
        attempts.append({
            **meta,
            "status": "NON_ZIP_RESPONSE",
            "sha256": hashlib.sha256(data).hexdigest(),
            "response_prefix_hex": data[:32].hex(),
            "response_prefix_ascii": data[:160].decode("utf-8", errors="replace"),
        })

    result = {
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "audit_type": "outcome_blind_mendeley_archive_identity_freeze",
        "dataset_id": DATASET_ID,
        "dataset_version": VERSION,
        "dataset_doi": "10.17632/ccnxn84w8z.2",
        "expected_filename": FILENAME,
        "landing_page": LANDING,
        "archive_contents_opened": False,
        "scientific_values_interpreted": False,
        "landing_discovery": landing_info,
        "landing_discovery_error": discovery_error,
        "attempts": attempts,
        "frozen_archive": success,
        "status": "PASS" if success else "MECHANICAL_SOURCE_ACCESS_FAILURE",
    }
    OUT_FILE.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUT_FILE.relative_to(ROOT)),
        "status": result["status"],
        "attempt_count": len(attempts) + (1 if success else 0),
        "sha256": success.get("sha256") if success else None,
        "size_bytes": success.get("size_bytes_observed") if success else None,
        "resolved_url": success.get("resolved_url") if success else None,
    }, indent=2))
    if not success:
        raise SystemExit("BIO_CHI_BLUM_MENDELEY_SOURCE_FREEZE_NO_ARCHIVE")
    print("BIO_CHI_BLUM_MENDELEY_SOURCE_FREEZE_PASS")


if __name__ == "__main__":
    main()
