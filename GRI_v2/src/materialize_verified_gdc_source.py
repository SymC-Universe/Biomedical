from __future__ import annotations

import argparse
import hashlib
import re
import time
import urllib.request
from pathlib import Path


USER_AGENT = "SymC-GRI-BioSystems-materializer/1.0"


class MaterializeError(RuntimeError):
    pass


def parse_content_range(value: str | None):
    if not value:
        return None
    m = re.search(r"(?:bytes\s+)?(\d+)-(\d+)/(\d+)", value.strip(), re.I)
    return tuple(int(x) for x in m.groups()) if m else None


def fetch_range(url: str, start: int, end: int, timeout: int, retries: int) -> bytes:
    last = None
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
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                status = int(getattr(resp, "status", resp.getcode()))
                headers = {k.lower(): v for k, v in resp.headers.items()}
                data = resp.read()
            if status != 206:
                raise MaterializeError(f"range {start}-{end} returned HTTP {status}")
            parsed = parse_content_range(headers.get("content-range"))
            if parsed is None:
                raise MaterializeError(f"range {start}-{end} has invalid Content-Range")
            got_start, got_end, total = parsed
            if (got_start, got_end) != (start, end):
                raise MaterializeError(
                    f"range mismatch requested={start}-{end} got={got_start}-{got_end}"
                )
            if len(data) != end - start + 1:
                raise MaterializeError(
                    f"range {start}-{end} length {len(data)} != {end-start+1}"
                )
            return data
        except Exception as exc:
            last = exc
            if attempt < retries:
                time.sleep(min(10, 2 ** (attempt - 1)))
    raise MaterializeError(f"range {start}-{end} failed after {retries}: {last}")


def materialize(uuid: str, output: Path, size: int, sha256: str,
                chunk_bytes: int, timeout: int, retries: int) -> None:
    url = f"https://api.gdc.cancer.gov/data/{uuid}"
    output.parent.mkdir(parents=True, exist_ok=True)
    tmp = output.with_suffix(output.suffix + ".partial")
    if tmp.exists():
        tmp.unlink()
    h = hashlib.sha256()
    written = 0
    with tmp.open("wb") as fh:
        for start in range(0, size, chunk_bytes):
            end = min(size - 1, start + chunk_bytes - 1)
            data = fetch_range(url, start, end, timeout, retries)
            fh.write(data)
            h.update(data)
            written += len(data)
            if written % (256 * 1024 * 1024) < chunk_bytes:
                print(f"{output.name}: {written}/{size} bytes", flush=True)
    if written != size:
        raise MaterializeError(f"wrote {written} bytes, expected {size}")
    digest = h.hexdigest()
    if digest != sha256:
        raise MaterializeError(f"SHA256 {digest} != expected {sha256}")
    tmp.replace(output)
    print(f"{output.name}: VERIFIED {written} bytes sha256={digest}", flush=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--uuid", required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--size", type=int, required=True)
    p.add_argument("--sha256", required=True)
    p.add_argument("--chunk-bytes", type=int, default=16 * 1024 * 1024)
    p.add_argument("--timeout", type=int, default=180)
    p.add_argument("--retries", type=int, default=8)
    a = p.parse_args()
    materialize(
        a.uuid, a.output, a.size, a.sha256,
        a.chunk_bytes, a.timeout, a.retries
    )


if __name__ == "__main__":
    main()
