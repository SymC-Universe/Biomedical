from pathlib import Path
import subprocess, sys

root = Path(__file__).resolve().parent

def run(args):
    return subprocess.run(args, cwd=root).returncode

if __name__ == "__main__":
    print("NSD Phase 0D v0.2 development / qualification runner")
    print("PROTOCOL = General v0.7.1 FINAL + authoritative v0.7.1A Addendum")
    print("P0-D = discovery, mechanism mapping, Function/Limit landscapes; P0-Q = controlled qualification. P1 remains fail-closed.")
    print("PURPOSE = protocol compliance, integrity, refusal, semantic guards, four-hold qualification, comparator stress, stochastic comparator qualification, truth-blind order/rank sweep, and rank-signal null stress")
    for args in [
        [sys.executable, "-m", "pytest", "-q"],
        [sys.executable, "scripts/run_p0_four_hold_qualification.py"],
        [sys.executable, "scripts/run_p0_comparator_stress_matrix.py"],
        [sys.executable, "scripts/run_p0_subspace_dmd_stress.py"],
        [sys.executable, "scripts/run_p0_order_rank_sweep.py"],
        [sys.executable, "scripts/run_p0_rank_signal_null_stress.py"],
        [sys.executable, "scripts/capture_environment.py"],
        [sys.executable, "scripts/make_candidate_manifest.py"],
    ]:
        rc = run(args)
        if rc:
            raise SystemExit(rc)
    print("P0-D / P0-Q DEVELOPMENT, QUALIFICATION, STRESS AND SWEEP CHECKS COMPLETE. Dedicated Function/Limit mapping workflows are separate so exploratory maps do not silently become release gates. No P1 scientific holdout is authorized or executed.")
