from __future__ import annotations
from pathlib import Path
import argparse
import contextlib
import io
import json
import os
import platform
import sys


THREAD_ENV_KEYS = (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "BLIS_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "NUMEXPR_NUM_THREADS",
)


def version_of(name):
    try:
        module = __import__(name)
        return getattr(module, "__version__", "UNKNOWN")
    except Exception as exc:
        return f"UNAVAILABLE:{type(exc).__name__}"


def config_text(name):
    """Capture package numerical-build configuration without failing the run."""
    try:
        module = __import__(name)
        show = getattr(module, "show_config", None)
        if show is None:
            return "UNAVAILABLE:NO_SHOW_CONFIG"
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            show()
        text = buf.getvalue().strip()
        return text if text else "EMPTY"
    except Exception as exc:
        return f"UNAVAILABLE:{type(exc).__name__}:{exc}"


def cpu_model():
    """Best-effort CPU model capture for numerical replay provenance."""
    candidates = [platform.processor()]
    try:
        cpuinfo = Path("/proc/cpuinfo")
        if cpuinfo.exists():
            for line in cpuinfo.read_text(encoding="utf-8", errors="replace").splitlines():
                if line.lower().startswith("model name") and ":" in line:
                    candidates.append(line.split(":", 1)[1].strip())
                    break
    except Exception:
        pass
    for value in candidates:
        if value:
            return value
    return "UNKNOWN"


def capture():
    uname = platform.uname()
    return {
        "schema": "nsd-environment-v2-numerical-backend-provenance",
        "python": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "system": uname.system,
        "release": uname.release,
        "version": uname.version,
        "machine": uname.machine,
        "processor": uname.processor,
        "cpu_model": cpu_model(),
        "logical_cpu_count": os.cpu_count(),
        "numpy": version_of("numpy"),
        "scipy": version_of("scipy"),
        "pytest": version_of("pytest"),
        "numpy_build_config": config_text("numpy"),
        "scipy_build_config": config_text("scipy"),
        "linear_algebra_thread_environment": {
            key: os.environ.get(key) for key in THREAD_ENV_KEYS
        },
        "reproducibility_note": (
            "Numerical backend and threading provenance are recorded because "
            "near-singular SVD/eigendecomposition outcomes can be sensitive to "
            "floating-point reduction order and backend details. This sidecar "
            "does not alter scientific computation."
        ),
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
