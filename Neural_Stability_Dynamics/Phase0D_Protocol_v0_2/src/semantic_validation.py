from __future__ import annotations
from pathlib import Path
import csv, json


def _rows(path: Path):
    with Path(path).open(newline="", encoding="utf-8") as f: return list(csv.DictReader(f))


def _is_admit(value: str) -> bool:
    return str(value).startswith("ADMIT_")


def recompute_core_semantics(results_dir: Path) -> dict:
    """Independent core semantic reconstruction from detailed rows. Expansion is required before P2."""
    results_dir = Path(results_dir)
    rows = _rows(results_dir / "layer_decisions.csv")
    failures = json.loads((results_dir / "failures.json").read_text(encoding="utf-8"))
    stationary = [r for r in rows if r.get("role") == "stationary_truth"]
    system_scored = [r for r in stationary if r.get("expected_system") == "ADMIT"]
    return {
        "trial_count":len(rows),
        "stationary_trial_count":len(stationary),
        "stationary_scalar_admission_rate":None if not stationary else sum(_is_admit(r.get("scalar_decision","")) for r in stationary)/len(stationary),
        "stationary_modal_admission_rate":None if not stationary else sum(_is_admit(r.get("modal_decision","")) for r in stationary)/len(stationary),
        "stationary_system_trial_count":len(system_scored),
        "stationary_system_admission_rate":None if not system_scored else sum(_is_admit(r.get("system_decision","")) for r in system_scored)/len(system_scored),
        "failed_fits":len(failures),
    }


def compare_summary(results_dir: Path) -> tuple[bool, list[str]]:
    results_dir = Path(results_dir)
    summary = json.loads((results_dir / "summary.json").read_text(encoding="utf-8"))
    core = recompute_core_semantics(results_dir); metrics = summary.get("metrics", {}); problems=[]
    for k in ["stationary_trial_count","stationary_scalar_admission_rate","stationary_modal_admission_rate","stationary_system_trial_count","stationary_system_admission_rate","failed_fits"]:
        a=core[k]; b=metrics.get(k)
        if isinstance(a,float) or isinstance(b,float):
            if a is None or b is None or abs(float(a)-float(b))>1e-12: problems.append(f"SEMANTIC_MISMATCH:{k}:{a}!={b}")
        elif a != b: problems.append(f"SEMANTIC_MISMATCH:{k}:{a}!={b}")
    return not problems, problems
