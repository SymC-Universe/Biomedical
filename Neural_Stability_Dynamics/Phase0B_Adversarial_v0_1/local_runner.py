from pathlib import Path
import subprocess, sys, time

R = Path(__file__).resolve().parent
O = R / "results" / "phase0b"
O.mkdir(parents=True, exist_ok=True)
L = O / "RUN_LOG.txt"


def log(s):
    print(s, flush=True)
    with open(L, "a", encoding="utf-8") as f:
        f.write(s + "\n")


def cmd(a):
    return subprocess.run(a, cwd=R).returncode


if __name__ == "__main__":
    L.write_text("")
    log("NSD Phase 0B adversarial structure-identification runner v0.1")
    log("Development/calibration only. No EEG, labels, or admission threshold.")
    log("[A] Running tests before synthetic execution...")
    rc = cmd([sys.executable, "-m", "pytest", "-q"])
    if rc:
        log("TEST GATE FAILED. Execution not authorized.")
        raise SystemExit(rc)
    log("    tests PASS")
    log("[B] Writing code/config SHA-256 manifest...")
    rc = cmd([sys.executable, "scripts/make_manifest.py"])
    if rc:
        log("MANIFEST FAILURE. Execution stopped.")
        raise SystemExit(rc)
    for attempt in range(1, 4):
        log(f"WORKER ATTEMPT {attempt}/3")
        rc = cmd([sys.executable, "run_phase0b.py"])
        if rc == 0:
            log("RUN COMPLETE. Preserve all adversarial outcomes before designing Phase 0C.")
            raise SystemExit(0)
        log(f"Worker exited with code {rc}. Mechanical retry in 5 seconds; frozen design unchanged.")
        time.sleep(5)
    log("RUN DID NOT COMPLETE. Preserve results/phase0b and send RUN_LOG.txt.")
    raise SystemExit(1)
