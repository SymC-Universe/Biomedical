from __future__ import annotations
from pathlib import Path
import argparse
import json
import platform
import sys


def version_of(name):
    try:
        module = __import__(name)
        return getattr(module, "__version__", "UNKNOWN")
    except Exception as exc:
        return f"UNAVAILABLE:{type(exc).__name__}"


def capture():
    return {
        "python": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "numpy": version_of("numpy"),
        "scipy": version_of("scipy"),
        "pytest": version_of("pytest"),
    }


def write_environment(output=None):
    root = Path(__file__).resolve().parents[1]
    out = Path(output) if output is not None else root / "results" / "dev_validation" / "environment.json"
    if not out.is_absolute():
        out = root / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(capture(), indent=2) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "output",
        nargs="?",
        default=None,
        help="Optional output path. Relative paths are resolved from the Phase0D_Protocol_v0_2 root.",
    )
    args = parser.parse_args()
    print(write_environment(args.output))
