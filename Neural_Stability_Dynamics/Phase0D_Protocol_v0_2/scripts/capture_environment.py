from __future__ import annotations
from pathlib import Path
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
    return {"python":sys.version,"python_executable":sys.executable,"platform":platform.platform(),"machine":platform.machine(),"numpy":version_of("numpy"),"scipy":version_of("scipy"),"pytest":version_of("pytest")}


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    out = root / "results" / "dev_validation" / "environment.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(capture(), indent=2) + "\n", encoding="utf-8")
    print(out)
