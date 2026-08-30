from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

EXPECTED_CACHE_SHA256 = "e65f6788aa6037fef407169794f29d63322de2769343bb6e594fe469dfeb8e63"
CHUNK = 8 * 1024 * 1024


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(CHUNK), b""):
            h.update(chunk)
    return h.hexdigest()


def validate_cache(path: Path) -> str:
    path = path.expanduser()
    if not path.exists():
        raise FileNotFoundError(f"Selected Stage A cache does not exist: {path}")
    if not path.is_file():
        raise ValueError(f"Selected Stage A cache is not a regular file: {path}")
    actual = sha256_file(path)
    if actual != EXPECTED_CACHE_SHA256:
        raise ValueError(
            "Selected file is not the frozen completed Stage A hallmark_profile_cache.npz. "
            f"SHA-256 {actual} != expected {EXPECTED_CACHE_SHA256}"
        )
    return actual


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cache", type=Path)
    args = ap.parse_args()
    try:
        actual = validate_cache(args.cache)
    except (FileNotFoundError, OSError, ValueError) as exc:
        print(f"STAGE_A_CACHE_INVALID: {exc}", file=sys.stderr, flush=True)
        raise SystemExit(2)
    print(f"STAGE_A_CACHE_VALID {actual}", flush=True)


if __name__ == "__main__":
    main()
