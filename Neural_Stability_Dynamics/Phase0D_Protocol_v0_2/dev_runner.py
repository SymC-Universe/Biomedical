from pathlib import Path
import subprocess, sys

root = Path(__file__).resolve().parent

def run(args):
    return subprocess.run(args, cwd=root).returncode

if __name__ == "__main__":
    print("NSD Phase 0D v0.2 P0 protocol-reconciliation development runner")
    print("PURPOSE = DEBUGGING | protocol compliance, integrity, refusal, semantic guards, four-hold qualification, comparator stress, stochastic comparator qualification, and truth-blind order/rank sweep")
    for args in [
        [sys.executable, "-m", "pytest", "-q"],
        [sys.executable, "scripts/run_p0_four_hold_qualification.py"],
        [sys.executable, "scripts/run_p0_comparator_stress_matrix.py"],
        [sys.executable, "scripts/run_p0_subspace_dmd_stress.py"],
        [sys.executable, "scripts/run_p0_order_rank_sweep.py"],
        [sys.executable, "scripts/capture_environment.py"],
        [sys.executable, "scripts/make_candidate_manifest.py"],
    ]:
        rc = run(args)
        if rc:
            raise SystemExit(rc)
    print("P0 DEVELOPMENT / QUALIFICATION / STRESS / SWEEP CHECKS COMPLETE. This does not authorize or execute a scientific holdout.")
