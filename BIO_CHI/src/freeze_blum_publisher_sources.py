#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import urllib.request
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[2]
BIO = ROOT / "BIO_CHI"
CFG = BIO / "config" / "BLUM2019_PUBLISHER_SOURCE_ENDPOINTS_v0_1.json"
OUT = BIO / "artifacts" / "generated"
OUT.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT / "blum2019_publisher_source_freeze_v0_1.json"

USER_AGENT = "BioChiBlumSourceFreeze/0.1 (+reviewer-reproducibility)"
MAX_BYTES = 250 * 1024 * 1024


def freeze_archive(rec: dict) -> dict:
    req = urllib.request.Request(rec["url"], headers={"User-Agent": USER_AGENT})
    h = hashlib.sha256()
    total = 0
    with urllib.request.urlopen(req, timeout=180) as r:
        meta = {
            "resolved_url": r.geturl(),
            "http_status": getattr(r, "status", None),
            "content_type": r.headers.get("Content-Type"),
            "content_length_header": r.headers.get("Content-Length"),
            "last_modified": r.headers.get("Last-Modified"),
            "etag": r.headers.get("ETag"),
        }
        while True:
            chunk = r.read(1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_BYTES:
                return {
                    **rec,
                    **meta,
                    "size_bytes_observed": total,
                    "sha256": None,
                    "hash_status": "DEFERRED_OVER_LIMIT",
                    "hash_limit_bytes": MAX_BYTES,
                    "archive_contents_opened": False,
                }
            h.update(chunk)
    return {
        **rec,
        **meta,
        "size_bytes_observed": total,
        "sha256": h.hexdigest(),
        "hash_status": "FROZEN",
        "archive_contents_opened": False,
    }


def main() -> None:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    results = []
    failures = []
    for rec in cfg["archives"]:
        try:
            results.append(freeze_archive(rec))
        except Exception as exc:
            failures.append(f"{rec['id']}: {type(exc).__name__}: {exc}")
            results.append({
                **rec,
                "hash_status": "ERROR",
                "sha256": None,
                "error": f"{type(exc).__name__}: {exc}",
                "archive_contents_opened": False,
            })

    result = {
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_config": str(CFG.relative_to(ROOT)),
        "audit_type": "outcome_blind_whole_archive_identity_freeze",
        "archive_contents_opened": False,
        "scientific_values_interpreted": False,
        "max_bytes_per_archive": MAX_BYTES,
        "archives": results,
        "failures": failures,
    }
    OUT_FILE.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUT_FILE.relative_to(ROOT)),
        "archive_count": len(results),
        "frozen_count": sum(x.get("hash_status") == "FROZEN" for x in results),
        "deferred_count": sum(str(x.get("hash_status", "")).startswith("DEFERRED") for x in results),
        "failure_count": len(failures),
        "failures": failures,
    }, indent=2))
    if failures:
        raise SystemExit("BIO_CHI_BLUM_PUBLISHER_SOURCE_FREEZE_PARTIAL")
    print("BIO_CHI_BLUM_PUBLISHER_SOURCE_FREEZE_PASS")


if __name__ == "__main__":
    main()
