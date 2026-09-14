from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np

from src.ssi_cov import decompose, fit_from_decomposition
from src.selector import evaluate_modal_layer, evaluate_scalar_layer, evaluate_system_layer
from src.synthetic_systems import build_canonical, simulate_shared_basis_switch

DT = 0.01
N_SAMPLES = 4000
N_CHANNELS = 8
BLOCK_ROWS = 18
CANDIDATE_ORDERS = [2, 4, 6]
REPLICATES = 8
PROCESS_SCALE = 1.0
RULES_PATH = ROOT / "configs" / "development_rules.json"


def _mode(decay: float, frequency_hz: float) -> dict:
    return {"type": "complex", "decay": float(decay), "frequency_hz": float(frequency_hz)}


def _condition_specs() -> list[dict]:
    stationary = [_mode(4.0, 3.0), _mode(7.0, 6.0)]
    switched = [_mode(12.0, 1.7), _mode(2.5, 9.0)]
    return [
        {
            "name": "STATIONARY_CONTROL",
            "modes_first": copy.deepcopy(stationary),
            "modes_second": copy.deepcopy(stationary),
            "similarity": "orthogonal",
            "switch_sample": N_SAMPLES // 2,
        },
        {
            "name": "STRUCTURAL_SWITCH",
            "modes_first": copy.deepcopy(stationary),
            "modes_second": copy.deepcopy(switched),
            "similarity": "orthogonal",
            "switch_sample": N_SAMPLES // 2,
        },
    ]


def _native_eigenvalues(modes: list[dict]) -> np.ndarray:
    A, _ = build_canonical(modes)
    return np.linalg.eigvals(A)


def _prepare(Y: np.ndarray) -> tuple[dict, dict]:
    midpoint = len(Y) // 2
    segments = {
        "full": Y,
        "first_half": Y[:midpoint],
        "second_half": Y[midpoint:],
    }
    decomps = {}
    fits = {}
    for name, data in segments.items():
        dec = decompose(data, BLOCK_ROWS)
        decomps[name] = dec
        fits[name] = {
            q: fit_from_decomposition(*dec, q, DT)
            for q in CANDIDATE_ORDERS
        }
    return fits, decomps


def _disposition(decisions: dict[str, str]) -> str:
    values = [str(v) for v in decisions.values()]
    if any(v.startswith("REFUSE") for v in values):
        return "REFUSE_CURRENT_MODEL"
    if any(v.startswith("ENGINE_EXCEPTION") for v in values):
        return "ENGINE_EXCEPTION_NO_PREDICTION"
    return "STRUCTURAL_OUTPUT_ONLY_NO_RECOVERY_PREDICTION"


def _jsonable(obj):
    if isinstance(obj, dict):
        return {str(k): _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_jsonable(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return [_jsonable(v) for v in obj.tolist()]
    if isinstance(obj, complex):
        return [float(obj.real), float(obj.imag)]
    if isinstance(obj, np.generic):
        return _jsonable(obj.item())
    if isinstance(obj, float) and not np.isfinite(obj):
        return None
    return obj


def _one_record(spec: dict, replicate: int, rules: dict) -> dict:
    Y = simulate_shared_basis_switch(
        spec,
        n_channels=N_CHANNELS,
        dt=DT,
        n_samples=N_SAMPLES,
        process_scale=PROCESS_SCALE,
        sys_rng=np.random.default_rng(12000 + replicate),
        proc_rng=np.random.default_rng(13000 + replicate),
    )
    row = {
        "condition": spec["name"],
        "replicate": replicate,
        "finite_measurements": bool(np.all(np.isfinite(Y))),
    }
    try:
        fits, decomps = _prepare(Y)
        scalar = evaluate_scalar_layer(fits, decomps, CANDIDATE_ORDERS, rules)
        modal = evaluate_modal_layer(fits, decomps, CANDIDATE_ORDERS, rules)
        system = evaluate_system_layer(fits, decomps, CANDIDATE_ORDERS, rules)
        decisions = {
            "scalar": scalar.get("decision", ""),
            "modal": modal.get("decision", ""),
            "system": system.get("decision", ""),
        }
        row.update({
            "engine_status": "COMPLETED",
            "decisions": decisions,
            "disposition": _disposition(decisions),
            "scalar": scalar,
            "modal": modal,
            "system": system,
            "recovery_prediction": None,
        })
    except Exception as exc:
        decisions = {
            "scalar": "ENGINE_EXCEPTION",
            "modal": "ENGINE_EXCEPTION",
            "system": "ENGINE_EXCEPTION",
        }
        row.update({
            "engine_status": "ENGINE_EXCEPTION",
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
            "decisions": decisions,
            "disposition": _disposition(decisions),
            "recovery_prediction": None,
        })
    return _jsonable(row)


def build_record() -> dict:
    rules_text = RULES_PATH.read_text(encoding="utf-8")
    rules = json.loads(rules_text)
    specs = _condition_specs()
    records = []
    truth = []
    for spec in specs:
        first = _native_eigenvalues(spec["modes_first"])
        second = _native_eigenvalues(spec["modes_second"])
        truth.append({
            "condition": spec["name"],
            "first_half_stable": bool(np.all(first.real < 0)),
            "second_half_stable": bool(np.all(second.real < 0)),
            "native_generators_equal": bool(np.allclose(np.sort_complex(first), np.sort_complex(second))),
            "first_half_poles": [[float(v.real), float(v.imag)] for v in first],
            "second_half_poles": [[float(v.real), float(v.imag)] for v in second],
        })
        for replicate in range(REPLICATES):
            records.append(_one_record(spec, replicate, rules))

    aggregates = []
    for spec in specs:
        rows = [r for r in records if r["condition"] == spec["name"]]
        aggregates.append({
            "condition": spec["name"],
            "records": len(rows),
            "engine_completed": int(sum(r["engine_status"] == "COMPLETED" for r in rows)),
            "current_model_refusals": int(sum(r["disposition"] == "REFUSE_CURRENT_MODEL" for r in rows)),
            "engine_exceptions": int(sum(r["engine_status"] == "ENGINE_EXCEPTION" for r in rows)),
            "scalar_refusals": int(sum(str(r["decisions"]["scalar"]).startswith("REFUSE") for r in rows)),
            "modal_refusals": int(sum(str(r["decisions"]["modal"]).startswith("REFUSE") for r in rows)),
            "system_refusals": int(sum(str(r["decisions"]["system"]).startswith("REFUSE") for r in rows)),
            "partial_system_outputs": int(sum(str(r["decisions"]["system"]).startswith("PARTIAL") for r in rows)),
        })

    return {
        "schema": "nsd-phase0d-p0d23-out-of-model-refusal-v1",
        "status": "P0_D_EXPLORATORY_KNOWN_TRUTH_REFUSAL_CHALLENGE_NOT_CONFIRMATORY",
        "protocol": "General Cross-Project Research Protocol v0.7.7",
        "p1_authorized": False,
        "development_rules_path": str(RULES_PATH.relative_to(ROOT)),
        "development_rules_text_preserved_for_run": rules_text,
        "construction": {
            "dt": DT,
            "n_samples": N_SAMPLES,
            "n_channels": N_CHANNELS,
            "block_rows": BLOCK_ROWS,
            "candidate_orders": CANDIDATE_ORDERS,
            "replicates": REPLICATES,
            "process_scale": PROCESS_SCALE,
            "switch_sample": N_SAMPLES // 2,
        },
        "truth_P0_audit_only": truth,
        "aggregates": aggregates,
        "records": records,
        "firewall": (
            "Condition identity and native truth are used only to construct and audit the P0-D challenge. "
            "The existing selector receives fitted measurement-derived objects and the unchanged development rules only."
        ),
        "nonclaims": [
            "No refusal-rate threshold is frozen by this run.",
            "Unexpected admission is preserved as Limit-Map evidence and does not authorize threshold retuning.",
            "No structural admission is upgraded into a recovery prediction.",
            "No EEG, diagnosis, treatment, Atlas zone, preferred chi value, chi_system or clinical rule is tested.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="results/p0d_mapping/out_of_model_refusal_v1.json",
    )
    args = parser.parse_args()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    record = build_record()
    out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out.resolve())
    for row in record["aggregates"]:
        print(json.dumps(row, sort_keys=True))
    print("P0-D23 OUT-OF-MODEL REFUSAL CHALLENGE COMPLETE. Existing rules unchanged; no recovery prediction licensed.")


if __name__ == "__main__":
    main()
