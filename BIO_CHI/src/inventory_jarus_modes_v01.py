#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import itertools
import json
import pathlib
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
BIO = ROOT / "BIO_CHI"
FREEZE = json.loads((BIO / "config" / "JARUS_MODAL_INVENTORY_FREEZE_v0_1.json").read_text(encoding="utf-8"))
OUTDIR = BIO / "artifacts" / "generated" / "jarus_modal_inventory_v01"
OUT = OUTDIR / "modal_inventory_v0_1.json"
EXPECTED_CASES = FREEZE["input"]["cases"]
EXPECTED_MULTIPLIERS = [float(x) for x in FREEZE["input"]["jacobian_step_multipliers"]]


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def as_list(v):
    if isinstance(v, list):
        return v
    if isinstance(v, dict):
        return [v]
    if v is None:
        return []
    raise TypeError(type(v).__name__)


def complex_modes(step: dict) -> list[complex]:
    reals = as_list(step.get("eigenvalues_real"))
    imags = as_list(step.get("eigenvalues_imag"))
    if len(reals) != 6 or len(imags) != 6:
        raise ValueError(f"expected six eigenvalues, got real={len(reals)} imag={len(imags)}")
    return [complex(float(r), float(i)) for r, i in zip(reals, imags)]


def best_assignment(reference: list[complex], target: list[complex]) -> tuple[list[int], float]:
    best_perm = None
    best_cost = None
    for perm in itertools.permutations(range(6)):
        cost = sum(abs(reference[i] - target[perm[i]]) for i in range(6))
        if best_cost is None or cost < best_cost or (cost == best_cost and perm < best_perm):
            best_cost = cost
            best_perm = perm
    return list(best_perm), float(best_cost)


def enc(z: complex) -> dict:
    return {"real": float(z.real), "imag": float(z.imag)}


def sign(x: float) -> int:
    return 1 if x > 0 else (-1 if x < 0 else 0)


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: inventory_jarus_modes_v01.py <v03-artifact.zip>")
    artifact = pathlib.Path(sys.argv[1]).resolve()
    digest = sha256_file(artifact)
    expected_digest = FREEZE["source_v03_artifact_zip_sha256"]
    if digest != expected_digest:
        raise SystemExit(f"SOURCE_ARTIFACT_DIGEST_MISMATCH expected={expected_digest} actual={digest}")

    with zipfile.ZipFile(artifact) as zf:
        matches = [n for n in zf.namelist() if pathlib.PurePosixPath(n).name == "local_stability_v0_3.json"]
        if len(matches) != 1:
            raise SystemExit(f"SOURCE_MEMBER_ERROR matches={matches}")
        raw = json.loads(zf.read(matches[0]).decode("utf-8"))

    cases = {c["case_id"]: c for c in raw.get("cases", [])}
    if list(EXPECTED_CASES) != [c for c in EXPECTED_CASES if c in cases] or set(cases) != set(EXPECTED_CASES):
        raise SystemExit(f"CASE_SET_MISMATCH got={sorted(cases)} expected={sorted(EXPECTED_CASES)}")

    output_cases = []
    for case_id in EXPECTED_CASES:
        roots = as_list(cases[case_id].get("roots"))
        if len(roots) != 1:
            raise SystemExit(f"ROOT_COUNT_MISMATCH {case_id} count={len(roots)}")
        steps = as_list(roots[0].get("jacobian_steps"))
        by_mult = {float(s["multiplier"]): s for s in steps}
        if sorted(by_mult) != sorted(EXPECTED_MULTIPLIERS):
            raise SystemExit(f"STEP_SET_MISMATCH {case_id} got={sorted(by_mult)}")

        spectra = {m: complex_modes(by_mult[m]) for m in EXPECTED_MULTIPLIERS}
        ref_m = 1.0
        ref = spectra[ref_m]
        assignments = {ref_m: list(range(6))}
        assignment_costs = {ref_m: 0.0}
        for m in EXPECTED_MULTIPLIERS:
            if m == ref_m:
                continue
            perm, cost = best_assignment(ref, spectra[m])
            assignments[m] = perm
            assignment_costs[m] = cost

        matched = {m: [spectra[m][assignments[m][i]] for i in range(6)] for m in EXPECTED_MULTIPLIERS}
        modes = []
        for i in range(6):
            refz = ref[i]
            diffs = [abs(matched[m][i] - refz) for m in EXPECTED_MULTIPLIERS]
            abs_spread = max(diffs)
            rel_spread = None if abs(refz) == 0 else abs_spread / abs(refz)
            modes.append({
                "reference_index": i,
                "reference_eigenvalue": enc(refz),
                "matched_eigenvalues": {str(m): enc(matched[m][i]) for m in EXPECTED_MULTIPLIERS},
                "absolute_complex_spread": float(abs_spread),
                "relative_complex_spread": None if rel_spread is None else float(rel_spread),
            })

        step_records = []
        abscissae = []
        for m in EXPECTED_MULTIPLIERS:
            vals = spectra[m]
            abscissa = max(z.real for z in vals)
            abscissae.append(abscissa)
            step_records.append({
                "multiplier": m,
                "eigenvalues": [enc(z) for z in vals],
                "stored_exact_real_count": sum(1 for z in vals if z.imag == 0.0),
                "stored_nonzero_imag_count": sum(1 for z in vals if z.imag != 0.0),
                "spectral_abscissa": float(abscissa),
            })

        output_cases.append({
            "case_id": case_id,
            "steps": step_records,
            "assignments_from_multiplier_1": {str(m): assignments[m] for m in EXPECTED_MULTIPLIERS},
            "assignment_total_complex_distance": {str(m): assignment_costs[m] for m in EXPECTED_MULTIPLIERS},
            "all_modes": modes,
            "spectral_abscissa_sign_invariant": len({sign(x) for x in abscissae}) == 1,
            "spectral_abscissa_signs": [sign(x) for x in abscissae],
        })

    result = {
        "schema_version": "0.1",
        "audit_type": "descriptive_post_view_all_mode_generator_inventory",
        "authority": "SymC GOM v0.8.4",
        "freeze": "BIO_CHI/config/JARUS_MODAL_INVENTORY_FREEZE_v0_1.json",
        "source_v03_artifact_id": FREEZE["source_v03_artifact_id"],
        "source_v03_artifact_zip_sha256": digest,
        "prospective_validation_claim_allowed": False,
        "root_solver_rerun": False,
        "jacobian_recomputed": False,
        "all_six_modes_preserved": True,
        "mode_selected": False,
        "preferred_complex_pair_selected": False,
        "chi_bio_constructed": False,
        "Chi_bio_admitted": False,
        "Bio_Chi_constructed": False,
        "representation_independence_claimed": False,
        "cases": output_cases,
        "interpretation": "Descriptive inventory only. Every stored eigenvalue is retained across all three already-computed finite-difference steps. Numerical mode matching is used only to report step-size correspondence. No biological mode, scalar coordinate, modal representation, or representation-independence claim is selected or admitted here."
    }
    OUTDIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    print("BIO_CHI_JARUS_MODAL_INVENTORY_V01_COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
