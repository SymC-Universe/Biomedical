#!/usr/bin/env python3
"""Download the exact payloads named by a ds003775 pair manifest.

Identity is not trusted here. The downstream D4 verifier checks byte count,
MD5, EDF structure, channel labels, duration, and sampling metadata.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import time
import urllib.request


def download(url: str, destination: Path, retries: int = 3) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    last_error: Exception | None = None
    for attempt in range(retries):
        tmp = destination.with_suffix(destination.suffix + ".part")
        try:
            request = urllib.request.Request(
                url,
                headers={"User-Agent": "NSD-vNext-T0-payload-audit/0.1"},
            )
            with urllib.request.urlopen(request, timeout=120) as response, tmp.open("wb") as out:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    out.write(chunk)
            tmp.replace(destination)
            return
        except Exception as exc:
            last_error = exc
            if tmp.exists():
                tmp.unlink()
            if attempt + 1 < retries:
                time.sleep(2 * (attempt + 1))
    assert last_error is not None
    raise last_error


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    recordings = list(manifest["recordings"])
    if len(recordings) != 2:
        raise ValueError("repeat payload download requires exactly two recordings")

    summary = []
    for item in recordings:
        relative = Path(str(item["relative_path"]))
        destination = args.output_dir / relative.name
        download(str(item["download_url"]), destination)
        summary.append({
            "session_id": item["session_id"],
            "filename": destination.name,
            "downloaded_size_bytes": destination.stat().st_size,
        })

    print(json.dumps({
        "subject_id": manifest["subject_id"],
        "downloads": summary,
        "identity_status": "UNVERIFIED_UNTIL_D4_TOOL",
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
