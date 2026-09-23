#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import urllib.parse
import urllib.request
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[2]
BIO = ROOT / "BIO_CHI"
CFG = BIO / "config" / "BLUM2019_PUBLISHER_SOURCE_ENDPOINTS_v0_1.json"
OUT = BIO / "artifacts" / "generated"
OUT.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT / "blum2019_publisher_source_freeze_v0_1.json"

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/140.0 Safari/537.36"
)
REFERER = "https://link.springer.com/article/10.15252/msb.20198947"
MAX_BYTES = 250 * 1024 * 1024


def request_url(url: str):
    return urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/zip,application/octet-stream,*/*;q=0.8",
            "Referer": REFERER,
            "Accept-Language": "en-US,en;q=0.9",
        },
    )


def download_candidate(url: str) -> tuple[bytes, dict]:
    with urllib.request.urlopen(request_url(url), timeout=180) as r:
        meta = {
            "requested_url": url,
            "resolved_url": r.geturl(),
            "http_status": getattr(r, "status", None),
            "content_type": r.headers.get("Content-Type"),
            "content_length_header": r.headers.get("Content-Length"),
            "content_disposition": r.headers.get("Content-Disposition"),
            "last_modified": r.headers.get("Last-Modified"),
            "etag": r.headers.get("ETag"),
        }
        chunks = []
        total = 0
        while True:
            chunk = r.read(1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_BYTES:
                return b"", {
                    **meta,
                    "size_bytes_observed": total,
                    "download_status": "DEFERRED_OVER_LIMIT",
                }
            chunks.append(chunk)
    data = b"".join(chunks)
    return data, {**meta, "size_bytes_observed": len(data), "download_status": "DOWNLOADED"}


def looks_like_zip(data: bytes) -> bool:
    return data.startswith((b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08"))


def freeze_archive(rec: dict) -> dict:
    attempts = [rec["url"]]
    parsed = urllib.parse.urlsplit(rec["url"])
    query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    if not any(k == "download" for k, _ in query):
        query.append(("download", "1"))
        attempts.append(urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urllib.parse.urlencode(query), parsed.fragment)))

    attempt_records = []
    for candidate in attempts:
        try:
            data, meta = download_candidate(candidate)
        except Exception as exc:
            attempt_records.append({
                "requested_url": candidate,
                "status": "REQUEST_ERROR",
                "error": f"{type(exc).__name__}: {exc}",
            })
            continue

        if meta.get("download_status") == "DEFERRED_OVER_LIMIT":
            return {
                **rec,
                **meta,
                "sha256": None,
                "hash_status": "DEFERRED_OVER_LIMIT",
                "hash_limit_bytes": MAX_BYTES,
                "archive_contents_opened": False,
                "attempts": attempt_records,
            }

        if not looks_like_zip(data):
            attempt_records.append({
                **meta,
                "status": "NON_ZIP_RESPONSE",
                "response_prefix_hex": data[:32].hex(),
                "response_prefix_ascii": data[:160].decode("utf-8", errors="replace"),
            })
            continue

        return {
            **rec,
            **meta,
            "sha256": hashlib.sha256(data).hexdigest(),
            "hash_status": "FROZEN_ZIP_BYTES",
            "zip_magic_verified": True,
            "archive_contents_opened": False,
            "attempts": attempt_records,
        }

    return {
        **rec,
        "sha256": None,
        "hash_status": "NON_ARCHIVE_RESPONSE",
        "archive_contents_opened": False,
        "attempts": attempt_records,
    }


def main() -> None:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    results = []
    failures = []
    for rec in cfg["archives"]:
        frozen = freeze_archive(rec)
        results.append(frozen)
        if frozen.get("hash_status") not in {"FROZEN_ZIP_BYTES", "DEFERRED_OVER_LIMIT"}:
            failures.append(f"{rec['id']}: {frozen.get('hash_status')}")

    result = {
        "schema_version": "0.2",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_config": str(CFG.relative_to(ROOT)),
        "audit_type": "outcome_blind_whole_archive_identity_freeze",
        "archive_contents_opened": False,
        "scientific_values_interpreted": False,
        "zip_magic_required": True,
        "max_bytes_per_archive": MAX_BYTES,
        "archives": results,
        "failures": failures,
    }
    OUT_FILE.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUT_FILE.relative_to(ROOT)),
        "archive_count": len(results),
        "frozen_zip_count": sum(x.get("hash_status") == "FROZEN_ZIP_BYTES" for x in results),
        "deferred_count": sum(str(x.get("hash_status", "")).startswith("DEFERRED") for x in results),
        "failure_count": len(failures),
        "failures": failures,
    }, indent=2))
    if failures:
        raise SystemExit("BIO_CHI_BLUM_PUBLISHER_SOURCE_FREEZE_PARTIAL")
    print("BIO_CHI_BLUM_PUBLISHER_SOURCE_FREEZE_PASS")


if __name__ == "__main__":
    main()
