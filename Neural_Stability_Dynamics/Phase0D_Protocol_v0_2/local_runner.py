from pathlib import Path
import subprocess, sys

root = Path(__file__).resolve().parent

def run(args):
    return subprocess.run(args, cwd=root).returncode

if __name__ == "__main__":
    print("NSD Phase 0D v0.2 confirmatory runner guard")
    print("Protocol baseline: General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum")
    rc = run([sys.executable, "scripts/verify_p1_readiness.py"])
    if rc:
        print("CONFIRMATORY EXECUTION BLOCKED BEFORE SCIENTIFIC DATA GENERATION.")
        raise SystemExit(rc)
    rc = run([sys.executable, "scripts/verify_frozen_manifest.py"])
    if rc:
        print("CONFIRMATORY EXECUTION BLOCKED BY BYTE-INTEGRITY FAILURE.")
        raise SystemExit(rc)
    raise SystemExit("P1_READY exists but no scientific Phase 0D v0.2 runner has been frozen yet. This is an invalid repository state; stop and audit.")
