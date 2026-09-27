#!/usr/bin/env python3
from __future__ import annotations

import itertools
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
BIO = ROOT / "BIO_CHI"
FREEZE = json.loads((BIO / "config" / "JARUS_FULL_STATE_REPRESENTATION_CONTROL_FREEZE_v0_1.json").read_text(encoding="utf-8"))
OUTDIR = BIO / "artifacts" / "generated" / "jarus_full_state_representation_control_v01"
RAW = OUTDIR / "representation_control_raw_v0_1.json"
OUT = OUTDIR / "representation_control_summary_v0_1.json"
REPS = [r["id"] for r in FREEZE["representations"]]
MULTS = [float(x) for x in FREEZE["finite_difference_rule"]["multipliers"]]
CASES = FREEZE["cases"]


def as_list(v):
    if isinstance(v, list): return v
    if isinstance(v, dict): return [v]
    if v is None: return []
    raise TypeError(type(v).__name__)


def modes(rec: dict) -> list[complex]:
    rr = as_list(rec.get("eigenvalues_real")); ii = as_list(rec.get("eigenvalues_imag"))
    if len(rr) != 6 or len(ii) != 6:
        raise ValueError(f"expected six eigenvalues in {rec.get('representation')} x{rec.get('multiplier')}")
    return [complex(float(r),float(i)) for r,i in zip(rr,ii)]


def best_assignment(ref, target):
    best_perm=None; best_cost=None
    for perm in itertools.permutations(range(6)):
        cost=sum(abs(ref[i]-target[perm[i]]) for i in range(6))
        if best_cost is None or cost < best_cost or (cost == best_cost and perm < best_perm):
            best_cost=cost; best_perm=perm
    return list(best_perm), float(best_cost)


def enc(z): return {"real":float(z.real),"imag":float(z.imag)}

def sign(x): return 1 if x>0 else (-1 if x<0 else 0)


def main() -> int:
    if not RAW.exists(): raise SystemExit(f"missing raw control {RAW}")
    raw=json.loads(RAW.read_text(encoding="utf-8"))
    raw_cases={c["case_id"]:c for c in as_list(raw.get("cases"))}
    if set(raw_cases) != set(CASES): raise SystemExit(f"CASE_SET_MISMATCH {sorted(raw_cases)}")
    cases_out=[]
    any_nonfinite=False
    any_sign_change=False
    global_max_rel=0.0
    for case_id in CASES:
        records=as_list(raw_cases[case_id].get("records"))
        index={(r["representation"],float(r["multiplier"])):r for r in records}
        if set(index) != {(rep,m) for rep in REPS for m in MULTS}:
            raise SystemExit(f"RECORD_SET_MISMATCH {case_id}")
        case_comparisons=[]
        for m in MULTS:
            phys_rec=index[("physical_x",m)]
            phys=modes(phys_rec)
            phys_ab=float(phys_rec["spectral_abscissa"])
            step={
                "multiplier":m,
                "physical_x_spectral_abscissa":phys_ab,
                "representations":[]
            }
            for rep in REPS:
                rec=index[(rep,m)]; vals=modes(rec); finite=bool(rec.get("all_finite",False))
                any_nonfinite = any_nonfinite or (not finite)
                if rep == "physical_x": perm=list(range(6)); cost=0.0
                else: perm,cost=best_assignment(phys,vals)
                matched=[vals[perm[i]] for i in range(6)]
                diffs=[abs(matched[i]-phys[i]) for i in range(6)]
                rels=[None if abs(phys[i])==0 else diffs[i]/abs(phys[i]) for i in range(6)]
                finite_rels=[x for x in rels if x is not None]
                max_rel=max(finite_rels) if finite_rels else None
                if max_rel is not None: global_max_rel=max(global_max_rel,max_rel)
                ab=float(rec["spectral_abscissa"]); sign_same=sign(ab)==sign(phys_ab)
                any_sign_change = any_sign_change or (not sign_same)
                step["representations"].append({
                    "representation":rep,
                    "all_finite":finite,
                    "spectral_abscissa":ab,
                    "spectral_abscissa_sign_matches_physical_x":sign_same,
                    "assignment_from_physical_x":perm,
                    "assignment_total_complex_distance":cost,
                    "max_absolute_complex_difference":float(max(diffs)),
                    "max_relative_complex_difference":None if max_rel is None else float(max_rel),
                    "matched_eigenvalues":[enc(z) for z in matched]
                })
            case_comparisons.append(step)
        cases_out.append({"case_id":case_id,"comparisons":case_comparisons})

    result={
        "schema_version":"0.1",
        "audit_type":"necessary_not_sufficient_full_state_coordinate_invariance_control_summary",
        "authority":"SymC GOM v0.8.4",
        "freeze":"BIO_CHI/config/JARUS_FULL_STATE_REPRESENTATION_CONTROL_FREEZE_v0_1.json",
        "execution_complete":True,
        "all_records_finite":not any_nonfinite,
        "any_spectral_abscissa_sign_change_vs_physical_x":any_sign_change,
        "maximum_observed_relative_complex_difference":float(global_max_rel),
        "scientific_promotion_threshold":None,
        "root_solver_rerun":False,
        "mode_selected":False,
        "preferred_complex_pair_selected":False,
        "chi_bio_constructed":False,
        "Chi_bio_admitted":False,
        "Bio_Chi_constructed":False,
        "biological_representation_independence_claimed":False,
        "cases":cases_out,
        "interpretation":"This is only a necessary numerical full-state coordinate-invariance control. No pass threshold is used for scientific promotion. Invertible full-state coordinate agreement cannot establish biological observability, reduced-representation adequacy, identifiability, modal admission, or scalar adequacy."
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:result[k] for k in ["execution_complete","all_records_finite","any_spectral_abscissa_sign_change_vs_physical_x","maximum_observed_relative_complex_difference"]},indent=2))
    print("BIO_CHI_JARUS_FULL_STATE_REPRESENTATION_CONTROL_SUMMARY_COMPLETE")
    return 0

if __name__ == "__main__": raise SystemExit(main())
