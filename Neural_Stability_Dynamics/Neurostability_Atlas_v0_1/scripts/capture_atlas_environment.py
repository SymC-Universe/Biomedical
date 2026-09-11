from __future__ import annotations

import argparse
import json
import platform
import sys
from importlib import metadata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _version(package: str):
    try:
        return metadata.version(package)
    except metadata.PackageNotFoundError:
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/a2_srm/environment.json")
    args = parser.parse_args()
    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "schema": "neurostability-atlas-environment-v0.1",
        "python": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "packages": {
            "numpy": _version("numpy"),
            "scipy": _version("scipy"),
            "mne": _version("mne"),
            "pytest": _version("pytest"),
        },
    }
    out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
