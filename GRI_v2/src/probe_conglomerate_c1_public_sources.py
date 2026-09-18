from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

CONFIG_REL = Path("GRI_v2/config/gri_conglomerate_c1_source_registry_20260918.json")
OUTPUT_REL = Path("GRI_v2/artifacts/GRI_CONGLOMERATE_C1_PUBLIC_SOURCE_PROBE_20260918.json")


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def parse_content_range(value: Optional[str]) -> Optional[int]:
    if not value:
        return None
    # Expected form: bytes 0-0/12345
    try:
        total = value.rsplit("/", 1)[1]
        if total == "*":
            return None
        return int(total)
    except (IndexError, ValueError):
        return None


def probe_size(url: str, timeout: int = 60) -> Tuple[Optional[int], Dict[str, Any]]:
    req = urllib.request.Request(
        url,
        headers={
            "Range": "bytes=0-0",
            "User-Agent": "GRI-Conglomerate-C1-Source-Probe/1.0",
        },
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        content_range = resp.headers.get("Content-Range")
        content_length = resp.headers.get("Content-Length")
        size = parse_content_range(content_range)
        if size is None and content_length is not None:
            try:
                size = int(content_length)
            except ValueError:
                size = None

        # Read at most one byte. If a server ignores Range, do not consume a large payload.
        _ = resp.read(1)
        return size, {
            "http_status": getattr(resp, "status", None),
            "content_range": content_range,
            "content_length": content_length,
            "content_type": resp.headers.get("Content-Type"),
            "content_disposition": resp.headers.get("Content-Disposition"),
        }


def stream_sha256(url: str, timeout: int = 120) -> Tuple[str, int]:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "GRI-Conglomerate-C1-Source-Probe/1.0"},
        method="GET",
    )
    h = hashlib.sha256()
    n = 0
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        while True:
            chunk = resp.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
            n += len(chunk)
    return h.hexdigest(), n


def evaluate_source(source: Dict[str, Any], full_hash_limit: int) -> Dict[str, Any]:
    row: Dict[str, Any] = {
        "id": source["id"],
        "blocks": source["blocks"],
        "role": source["role"],
        "file_name": source["file_name"],
        "gdc_uuid": source["gdc_uuid"],
        "url": source["url"],
        "probe_policy": source["probe_policy"],
        "provenance": source["provenance"],
    }

    try:
        observed_size, metadata = probe_size(source["url"])
        row.update(metadata)
        row["observed_size_bytes"] = observed_size
        row["expected_size_bytes"] = source.get("expected_size_bytes")
        if source.get("expected_size_bytes") is not None and observed_size is not None:
            row["size_match"] = observed_size == source["expected_size_bytes"]
        else:
            row["size_match"] = None

        if observed_size is not None and observed_size <= full_hash_limit:
            observed_sha, observed_bytes = stream_sha256(source["url"])
            row["observed_sha256"] = observed_sha
            row["full_download_bytes"] = observed_bytes
            row["expected_sha256"] = source.get("expected_sha256")
            if source.get("expected_sha256"):
                row["sha256_match"] = observed_sha == source["expected_sha256"]
            else:
                row["sha256_match"] = None
            row["cloud_rematerialization"] = "VERIFIED_FULL_HASH"
        else:
            row["observed_sha256"] = None
            row["expected_sha256"] = source.get("expected_sha256")
            row["sha256_match"] = None
            row["cloud_rematerialization"] = "PUBLIC_ENDPOINT_SIZE_PROBED_LARGE_SOURCE"

        failures = []
        if row["size_match"] is False:
            failures.append("SIZE_MISMATCH")
        if row["sha256_match"] is False:
            failures.append("SHA256_MISMATCH")
        row["failures"] = failures
        row["status"] = "PASS" if not failures else "FAIL"
    except Exception as exc:
        row["status"] = "ERROR"
        row["error"] = f"{type(exc).__name__}: {exc}"
        row["failures"] = ["NETWORK_OR_SOURCE_PROBE_ERROR"]

    return row


def build_probe(repo_root: Path) -> Dict[str, Any]:
    cfg = load_json(repo_root / CONFIG_REL)
    limit = int(cfg["rules"]["small_source_full_hash_limit_bytes"])
    rows = [evaluate_source(s, limit) for s in cfg["sources"]]

    fail_rows = [r["id"] for r in rows if r["status"] != "PASS"]
    verified_full_hash = [
        r["id"] for r in rows
        if r.get("cloud_rematerialization") == "VERIFIED_FULL_HASH"
        and r["status"] == "PASS"
    ]
    large_public = [
        r["id"] for r in rows
        if r.get("cloud_rematerialization") == "PUBLIC_ENDPOINT_SIZE_PROBED_LARGE_SOURCE"
        and r["status"] == "PASS"
    ]

    if fail_rows:
        status = "C1_SOURCE_PROBE_BLOCKED"
    else:
        status = "C1_PUBLIC_SOURCE_PATHS_VERIFIED"

    return {
        "schema": "gri-conglomerate-c1-public-source-probe-v1",
        "date": "2026-09-18",
        "status": status,
        "config": str(CONFIG_REL),
        "sources_total": len(rows),
        "verified_full_hash_sources": verified_full_hash,
        "large_public_sources_size_probed": large_public,
        "failed_or_error_sources": fail_rows,
        "sources": rows,
        "derived_artifact_dependencies": cfg["derived_artifact_dependencies"],
        "science_changed": False,
        "biological_outcome_opened": False,
        "next": (
            "build C1 patient/system block materialization package from verified public sources "
            "and exact frozen derived-artifact adapters; do not aggregate blocks"
        ),
    }


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    result = build_probe(repo_root)
    out = repo_root / OUTPUT_REL
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, indent=2, sort_keys=True)
        f.write("\n")
    print(json.dumps({
        "status": result["status"],
        "sources_total": result["sources_total"],
        "verified_full_hash_sources": result["verified_full_hash_sources"],
        "large_public_sources_size_probed": result["large_public_sources_size_probed"],
        "failed_or_error_sources": result["failed_or_error_sources"],
        "output": str(OUTPUT_REL),
    }, indent=2))


if __name__ == "__main__":
    main()
