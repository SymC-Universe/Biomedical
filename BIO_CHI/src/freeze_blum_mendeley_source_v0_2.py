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
OUT = BIO / "artifacts" / "generated"
OUT.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT / "blum2019_mendeley_source_freeze_v0_2.json"

DATASET_ID = "ccnxn84w8z"
VERSION = 2
FILENAME = "data.zip"
DATASET_DOI = "10.17632/ccnxn84w8z.2"
LANDING = f"https://data.mendeley.com/datasets/{DATASET_ID}/{VERSION}"
PUBLIC_FILES_API = (
    f"https://data.mendeley.com/public-api/datasets/{DATASET_ID}/files"
    f"?folder_id=root&version={VERSION}"
)
MAX_BYTES = 250 * 1024 * 1024
USER_AGENT = "BioChiReviewerReproducibility/0.2"


def request(url: str, accept: str = "*/*") -> urllib.request.Request:
    return urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": accept,
            "Referer": LANDING,
        },
    )


def read_all(url: str, accept: str = "*/*") -> tuple[bytes, dict]:
    with urllib.request.urlopen(request(url, accept), timeout=180) as r:
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
        chunks: list[bytes] = []
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


def is_zip(data: bytes) -> bool:
    return data.startswith((b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08"))


def normalize_file_records(payload) -> list[dict]:
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]
    if isinstance(payload, dict):
        for key in ("files", "results", "items"):
            value = payload.get(key)
            if isinstance(value, list):
                return [x for x in value if isinstance(x, dict)]
    return []


def file_name(rec: dict) -> str | None:
    for key in ("filename", "name", "file_name"):
        value = rec.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def download_url(rec: dict) -> str | None:
    cd = rec.get("content_details")
    if isinstance(cd, dict):
        for key in ("download_url", "downloadUrl", "url"):
            value = cd.get(key)
            if isinstance(value, str) and value:
                return value
    for key in ("download_url", "downloadUrl", "url"):
        value = rec.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def compact_metadata(rec: dict) -> dict:
    cd = rec.get("content_details") if isinstance(rec.get("content_details"), dict) else {}
    keep = {
        "id": rec.get("id"),
        "filename": file_name(rec),
        "size": rec.get("size") if rec.get("size") is not None else rec.get("file_size"),
        "mime_type": rec.get("mime_type"),
        "content_details_id": cd.get("id"),
        "content_details_download_url": download_url(rec),
    }
    return keep


def main() -> None:
    failures: list[str] = []
    api_raw = b""
    api_meta: dict = {}
    api_sha = None
    records: list[dict] = []
    target: dict | None = None
    target_url: str | None = None
    frozen_archive: dict | None = None

    try:
        api_raw, api_meta = read_all(PUBLIC_FILES_API, "application/json,*/*;q=0.8")
        api_sha = hashlib.sha256(api_raw).hexdigest()
        payload = json.loads(api_raw.decode("utf-8"))
        records = normalize_file_records(payload)
        matches = [r for r in records if (file_name(r) or "").lower() == FILENAME.lower()]
        if len(matches) != 1:
            failures.append(
                f"expected exactly one {FILENAME!r} record from public files API, found {len(matches)}"
            )
        else:
            target = matches[0]
            target_url = download_url(target)
            if not target_url:
                failures.append("target file record has no public download URL")
    except Exception as exc:
        failures.append(f"public files API: {type(exc).__name__}: {exc}")

    if target_url:
        try:
            data, meta = read_all(target_url, "application/zip,application/octet-stream,*/*;q=0.5")
            if meta.get("download_status") == "DEFERRED_OVER_LIMIT":
                failures.append("target archive exceeded MAX_BYTES")
            elif not is_zip(data):
                failures.append(
                    "target download did not resolve to ZIP bytes "
                    f"(content_type={meta.get('content_type')!r})"
                )
            else:
                frozen_archive = {
                    **meta,
                    "status": "FROZEN_ZIP_BYTES",
                    "zip_magic_verified": True,
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "archive_contents_opened": False,
                }
        except Exception as exc:
            failures.append(f"archive download: {type(exc).__name__}: {exc}")

    result = {
        "schema_version": "0.2",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "audit_type": "outcome_blind_mendeley_public_api_archive_identity_freeze",
        "dataset_id": DATASET_ID,
        "dataset_version": VERSION,
        "dataset_doi": DATASET_DOI,
        "expected_filename": FILENAME,
        "landing_page": LANDING,
        "public_files_api": {
            "url": PUBLIC_FILES_API,
            "meta": api_meta,
            "response_sha256": api_sha,
            "response_size_bytes": len(api_raw),
            "record_count": len(records),
            "file_records": [compact_metadata(r) for r in records],
        },
        "selected_file_record": compact_metadata(target) if target else None,
        "frozen_archive": frozen_archive,
        "archive_contents_opened": False,
        "scientific_values_interpreted": False,
        "failures": failures,
        "status": "PASS" if frozen_archive is not None and not failures else "MECHANICAL_SOURCE_ACCESS_FAILURE",
    }
    OUT_FILE.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUT_FILE.relative_to(ROOT)),
        "status": result["status"],
        "api_record_count": len(records),
        "selected_filename": file_name(target) if target else None,
        "archive_sha256": frozen_archive.get("sha256") if frozen_archive else None,
        "archive_size_bytes": frozen_archive.get("size_bytes_observed") if frozen_archive else None,
        "failure_count": len(failures),
        "failures": failures,
    }, indent=2))
    if result["status"] != "PASS":
        raise SystemExit("BIO_CHI_BLUM_MENDELEY_SOURCE_FREEZE_V02_FAILED")
    print("BIO_CHI_BLUM_MENDELEY_SOURCE_FREEZE_V02_PASS")


if __name__ == "__main__":
    main()
