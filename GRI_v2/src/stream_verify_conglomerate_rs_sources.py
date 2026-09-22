from __future__ import annotations

"""Resource-safe exact-byte verification for the large GRI R/S source files.

This stage is source/provenance only. It opens no biological outcome, derives no
carrier feature, selects no model, and creates no scalar. Files are fetched in
ordered HTTP byte ranges so SHA-256 can be computed without storing multi-GB
sources on the runner.

The source identities are read from already-frozen repository records:
- R: chi_bio_conglomerate_v01_source_bindings.json
- S: STAGE_C0_METHYLATION_SOURCE_SUMMARY.json
"""

import argparse
import hashlib
import json
import re
import time
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCE_BINDINGS = ROOT / "config" / "chi_bio_conglomerate_v01_source_bindings.json"
METHYLATION_SUMMARY = (
    ROOT
    / "development_outputs"
    / "stage_c0_methylation"
    / "STAGE_C0_METHYLATION_SOURCE_SUMMARY.json"
)

DEFAULT_CHUNK_BYTES = 64 * 1024 * 1024
DEFAULT_RETRIES = 3
USER_AGENT = "SymC-GRI-source-verifier/1.0"


class StreamVerificationError(RuntimeError):
    pass


def _parse_content_range(value: str | None) -> tuple[int, int, int] | None:
    if not value:
        return None
    # Accept either standard "bytes 0-9/100" or observed "0-9/100".
    m = re.search(r"(?:bytes\s+)?(\d+)-(\d+)/(\d+)", value.strip(), re.I)
    if not m:
        return None
    return tuple(int(x) for x in m.groups())


def _source_specs() -> list[dict[str, Any]]:
    bindings = json.loads(SOURCE_BINDINGS.read_text(encoding="utf-8"))
    methyl = json.loads(METHYLATION_SUMMARY.read_text(encoding="utf-8"))

    r = bindings["blocks"]["R"]["remote_source"]
    specs = [
        {
            "block_id": "R",
            "role": "RNA_REGULATORY_SOURCE",
            "file_name": r["file_name"],
            "gdc_uuid": r["gdc_uuid"],
            "expected_size_bytes": int(r["expected_size_bytes"]),
            "expected_sha256": r["expected_sha256"],
            "source_record": str(SOURCE_BINDINGS.relative_to(ROOT.parent)),
        },
        {
            "block_id": "S",
            "role": "METHYLATION_SUBSTRATE_SOURCE",
            "file_name": methyl["source_file"],
            "gdc_uuid": methyl["gdc_uuid"],
            "expected_size_bytes": int(methyl["expected_content_length_bytes"]),
            "expected_sha256": methyl["source_sha256"],
            "source_record": str(METHYLATION_SUMMARY.relative_to(ROOT.parent)),
        },
    ]
    return specs


def _fetch_range(
    url: str,
    start: int,
    end: int,
    *,
    timeout_s: int,
    retries: int,
) -> tuple[bytes, dict[str, str], int]:
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept-Encoding": "identity",
                "Range": f"bytes={start}-{end}",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout_s) as resp:
                status = int(getattr(resp, "status", resp.getcode()))
                headers = {k.lower(): v for k, v in resp.headers.items()}
                data = resp.read()

            if status != 206:
                raise StreamVerificationError(
                    f"range request {start}-{end} returned HTTP {status}; "
                    "refusing a possible full-file response"
                )
            parsed = _parse_content_range(headers.get("content-range"))
            if parsed is None:
                raise StreamVerificationError(
                    f"range request {start}-{end} missing/invalid Content-Range"
                )
            got_start, got_end, _ = parsed
            if (got_start, got_end) != (start, end):
                raise StreamVerificationError(
                    f"requested {start}-{end}, got Content-Range {got_start}-{got_end}"
                )
            expected_len = end - start + 1
            if len(data) != expected_len:
                raise StreamVerificationError(
                    f"requested {expected_len} bytes, received {len(data)}"
                )
            return data, headers, attempt
        except Exception as exc:  # network and validation failures are retried
            last_error = exc
            if attempt < retries:
                time.sleep(min(10, 2 ** (attempt - 1)))
    raise StreamVerificationError(
        f"failed range {start}-{end} after {retries} attempts: {last_error}"
    )


def verify_source(
    spec: dict[str, Any],
    *,
    chunk_bytes: int = DEFAULT_CHUNK_BYTES,
    timeout_s: int = 180,
    retries: int = DEFAULT_RETRIES,
) -> dict[str, Any]:
    if chunk_bytes <= 0:
        raise ValueError("chunk_bytes must be positive")

    total = int(spec["expected_size_bytes"])
    url = f"https://api.gdc.cancer.gov/data/{spec['gdc_uuid']}"
    h = hashlib.sha256()
    newline_count = 0
    prefix = b""
    attempts_total = 0
    range_count = 0
    etags: set[str] = set()

    for start in range(0, total, chunk_bytes):
        end = min(total - 1, start + chunk_bytes - 1)
        data, headers, attempts = _fetch_range(
            url,
            start,
            end,
            timeout_s=timeout_s,
            retries=retries,
        )
        range_count += 1
        attempts_total += attempts
        h.update(data)
        newline_count += data.count(b"\n")
        if len(prefix) < 1024 * 1024:
            need = 1024 * 1024 - len(prefix)
            prefix += data[:need]
        etag = headers.get("etag")
        if etag:
            etags.add(etag)

    digest = h.hexdigest()
    header_line = prefix.split(b"\n", 1)[0].decode("utf-8", errors="replace")
    result = {
        "block_id": spec["block_id"],
        "role": spec["role"],
        "file_name": spec["file_name"],
        "gdc_uuid": spec["gdc_uuid"],
        "expected_size_bytes": total,
        "bytes_hashed": total,
        "expected_sha256": spec["expected_sha256"],
        "sha256": digest,
        "hash_match": digest == spec["expected_sha256"],
        "range_count": range_count,
        "request_attempts_total": attempts_total,
        "newline_count": newline_count,
        "first_line_utf8_preview": header_line[:500],
        "etag_values": sorted(etags),
        "source_record": spec["source_record"],
        "biological_outcomes_opened": False,
        "features_derived": False,
        "scalar_created": False,
    }
    if not result["hash_match"]:
        raise StreamVerificationError(
            f"{spec['block_id']} SHA-256 mismatch: {digest} != {spec['expected_sha256']}"
        )
    return result


def run(
    *,
    out_path: Path,
    chunk_bytes: int = DEFAULT_CHUNK_BYTES,
    timeout_s: int = 180,
    retries: int = DEFAULT_RETRIES,
) -> dict[str, Any]:
    specs = _source_specs()
    verified: list[dict[str, Any]] = []
    for spec in specs:
        verified.append(
            verify_source(
                spec,
                chunk_bytes=chunk_bytes,
                timeout_s=timeout_s,
                retries=retries,
            )
        )

    result = {
        "schema": "GRI_CONGLOMERATE_RS_STREAM_VERIFICATION_V01",
        "status": "PASS",
        "purpose": "exact-byte source identity only",
        "sources": verified,
        "all_hashes_match": all(x["hash_match"] for x in verified),
        "no_biological_outcomes_opened": True,
        "no_features_derived": True,
        "no_conglomerate_weights_selected": True,
        "no_scalar_chi_created": True,
        "next_gate": (
            "bind resource-safe frozen R/S feature extraction/materialization rules "
            "to these exact source identities without opening clinical outcomes"
        ),
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "conglomerate_v01_outputs" / "large_rs_stream_verification.json",
    )
    parser.add_argument("--chunk-bytes", type=int, default=DEFAULT_CHUNK_BYTES)
    parser.add_argument("--timeout-seconds", type=int, default=180)
    parser.add_argument("--retries", type=int, default=DEFAULT_RETRIES)
    args = parser.parse_args()

    result = run(
        out_path=args.output,
        chunk_bytes=args.chunk_bytes,
        timeout_s=args.timeout_seconds,
        retries=args.retries,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
