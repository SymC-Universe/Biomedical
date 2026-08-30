from __future__ import annotations

import argparse
import inspect
import json
from collections import Counter
from pathlib import Path

MVDR_COMMIT = "ab04895a04a8f4e1b40e332591c736ba18bf8fd7"
DIVAS_COMMIT = "294986fac88bdeea1071902aa360b19e820c85de"
DIVAS_VERSION = "0.1.1"

AJIVE_RUNTIME_REPAIR = {
    "location": "mvdr.ajive.random_direction.sample_randdir -> module-global draw_samples",
    "pinned_upstream_mismatch": (
        "sample_randdir passes n_samples=... while the pinned draw_samples signature accepts n_draws=..."
    ),
    "action": "alias n_samples to n_draws in the module-global call boundary",
    "scientific_effect": (
        "none: preserves the frozen random-direction draw count, seed flow, AJIVE ranks, centering, "
        "identifiability check, and mathematics"
    ),
}

DIVAS_KNOWN_NOT_EVALUABLE = {
    (
        "$ operator is invalid for atomic vectors",
        "result$status",
    ): "PUBLISHED_CVXR_RETURN_TYPE_INCOMPATIBILITY",
    (
        "non-conformable arguments",
        "randU %*% diag(singValsTilde, nrow = length(singValsTilde))",
    ): "PUBLISHED_SIGNAL_EXTRACTION_DIMENSION_FAILURE",
    (
        "non-numeric matrix extent",
        "matrix(0, n, 1)",
    ): "PUBLISHED_JOINT_STRUCTURE_DIMENSION_FAILURE",
}


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _patch_mvdr_draw_samples_compat() -> dict[str, object]:
    """Repair the second pinned mvdr keyword mismatch without changing AJIVE semantics."""
    import mvdr.ajive.random_direction as random_direction

    native_draw_samples = random_direction.draw_samples
    draw_sig = inspect.signature(native_draw_samples)
    sample_sig = inspect.signature(random_direction.sample_randdir)

    if getattr(native_draw_samples, "_gri_f3_n_samples_compat", False):
        return {
            "applied": False,
            "already_present": True,
            "draw_samples_signature": str(draw_sig),
            "sample_randdir_signature": str(sample_sig),
            **AJIVE_RUNTIME_REPAIR,
        }

    if "n_samples" in draw_sig.parameters:
        return {
            "applied": False,
            "already_present": False,
            "draw_samples_signature": str(draw_sig),
            "sample_randdir_signature": str(sample_sig),
            **AJIVE_RUNTIME_REPAIR,
        }
    if "n_draws" not in draw_sig.parameters:
        raise RuntimeError(f"unexpected pinned mvdr draw_samples signature: {draw_sig}")
    if "n_samples" not in sample_sig.parameters:
        raise RuntimeError(f"unexpected pinned mvdr sample_randdir signature: {sample_sig}")

    def draw_samples_compat(
        fun,
        n_samples=None,
        n_draws=None,
        n_jobs=None,
        backend=None,
        random_state=None,
        args=None,
        kws=None,
    ):
        if n_draws is None:
            n_draws = 1 if n_samples is None else n_samples
        elif n_samples is not None and int(n_draws) != int(n_samples):
            raise ValueError("conflicting n_draws and n_samples values")
        return native_draw_samples(
            fun=fun,
            n_draws=n_draws,
            n_jobs=n_jobs,
            backend=backend,
            random_state=random_state,
            args=[] if args is None else args,
            kws={} if kws is None else kws,
        )

    draw_samples_compat._gri_f3_n_samples_compat = True  # type: ignore[attr-defined]
    random_direction.draw_samples = draw_samples_compat
    return {
        "applied": True,
        "already_present": False,
        "draw_samples_signature_before": str(draw_sig),
        "sample_randdir_signature": str(sample_sig),
        **AJIVE_RUNTIME_REPAIR,
    }


def run_python_comparators(inputs: Path, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    repair = _patch_mvdr_draw_samples_compat()
    _write_json(
        out / "F3_AJIVE_RUNTIME_COMPAT.json",
        {
            "status": "F3_AJIVE_RUNTIME_COMPAT_READY",
            "mvdr_commit": MVDR_COMMIT,
            "repair": repair,
            "claim_ceiling": "synthetic established-method comparison only",
            "c1_beta_value_biology_read": False,
            "biological_chi_used": False,
        },
    )

    from src import run_tool_feasibility_f3_established_python as runner

    runner.run(inputs, out)


def classify_divas(out: Path) -> None:
    raw_path = out / "F3_DIVAS_SUMMARY.json"
    if not raw_path.is_file():
        raise SystemExit(f"missing DIVAS raw summary: {raw_path}")

    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    divas = raw.get("divas", {})
    if divas.get("commit") != DIVAS_COMMIT:
        raise SystemExit(f"unexpected DIVAS commit: {divas.get('commit')!r}")
    if str(divas.get("version")) != DIVAS_VERSION:
        raise SystemExit(f"unexpected DIVAS version: {divas.get('version')!r}")
    if raw.get("c1_beta_value_biology_read") is not False or raw.get("biological_chi_used") is not False:
        raise SystemExit("DIVAS raw summary violated frozen no-biology-read guard")

    failures = list(raw.get("failures", []))
    raw_status = str(raw.get("status", ""))
    sidecar_path = out / "F3_DIVAS_EVALUABILITY.json"

    if raw_status == "F3_DIVAS_COMPLETE" and not failures:
        _write_json(
            sidecar_path,
            {
                "status": "F3_DIVAS_EVALUABLE_COMPLETE",
                "raw_status": raw_status,
                "records": int(raw.get("records", 0)),
                "not_evaluable_records": 0,
                "unexpected_failures": 0,
                "divas_commit": DIVAS_COMMIT,
                "divas_version": DIVAS_VERSION,
                "raw_failure_evidence_preserved": raw_path.name,
                "claim_ceiling": "synthetic established-method comparison only",
                "c1_beta_value_biology_read": False,
                "biological_chi_used": False,
            },
        )
        return

    if raw_status != "F3_DIVAS_MECHANICAL_FAILURE" or not failures:
        _write_json(
            sidecar_path,
            {
                "status": "F3_DIVAS_UNEXPECTED_STATE",
                "raw_status": raw_status,
                "failure_count": len(failures),
                "raw_failure_evidence_preserved": raw_path.name,
            },
        )
        raise SystemExit(2)

    classified: list[dict[str, object]] = []
    unexpected: list[dict[str, object]] = []
    counts: Counter[str] = Counter()
    for failure in failures:
        key = (str(failure.get("error", "")), str(failure.get("error_call", "")))
        reason = DIVAS_KNOWN_NOT_EVALUABLE.get(key)
        if reason is None:
            unexpected.append(failure)
            continue
        counts[reason] += 1
        classified.append(
            {
                "scenario": failure.get("scenario"),
                "representation": failure.get("representation"),
                "replicate": failure.get("replicate"),
                "reason": reason,
                "error": failure.get("error"),
                "error_call": failure.get("error_call"),
            }
        )

    payload: dict[str, object] = {
        "status": "F3_DIVAS_NOT_EVALUABLE_PUBLISHED_IMPLEMENTATION" if not unexpected else "F3_DIVAS_UNEXPECTED_FAILURE",
        "raw_status": raw_status,
        "records": int(raw.get("records", 0)),
        "not_evaluable_records": len(classified),
        "unexpected_failures": len(unexpected),
        "reason_counts": dict(sorted(counts.items())),
        "not_evaluable": classified,
        "unexpected": unexpected,
        "divas_commit": DIVAS_COMMIT,
        "divas_version": DIVAS_VERSION,
        "decision_rule": (
            "Frozen F3 rule: if the published DIVAS implementation cannot evaluate a representation for a "
            "documented mathematical/software reason, record NOT_EVALUABLE and do not substitute a weaker baseline."
        ),
        "raw_failure_evidence_preserved": raw_path.name,
        "raw_replicate_evidence_preserved": "f3_divas_replicates.csv",
        "claim_ceiling": "synthetic established-method comparison only",
        "c1_beta_value_biology_read": False,
        "biological_chi_used": False,
    }
    _write_json(sidecar_path, payload)
    if unexpected:
        raise SystemExit(2)


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="command", required=True)

    py = sub.add_parser("run-python")
    py.add_argument("--inputs", type=Path, required=True)
    py.add_argument("--out", type=Path, required=True)

    divas = sub.add_parser("classify-divas")
    divas.add_argument("--out", type=Path, required=True)

    args = ap.parse_args()
    if args.command == "run-python":
        run_python_comparators(args.inputs, args.out)
    elif args.command == "classify-divas":
        classify_divas(args.out)
    else:  # pragma: no cover
        raise SystemExit(f"unknown command: {args.command}")


if __name__ == "__main__":
    main()
