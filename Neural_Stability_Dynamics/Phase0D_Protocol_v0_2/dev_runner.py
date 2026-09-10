from pathlib import Path
import subprocess, sys

root = Path(__file__).resolve().parent

def run(args):
    return subprocess.run(args, cwd=root).returncode

if __name__ == "__main__":
    print("NSD Phase 0D v0.2 P0 protocol-reconciliation development runner")
    print("PURPOSE = DEBUGGING | protocol compliance, integrity, refusal, and semantic-guard development")
    rc = run([sys.executable, "-m", "pytest", "-q"])
    if rc:
        raise SystemExit(rc)
    rc = run([sys.executable, "scripts/capture_environment.py"])
    if rc:
        raise SystemExit(rc)
    rc = run([sys.executable, "scripts/make_candidate_manifest.py"])
    if rc:
        raise SystemExit(rc)
    print("P0 DEVELOPMENT CHECKS COMPLETE. This does not authorize or execute a scientific holdout.")
