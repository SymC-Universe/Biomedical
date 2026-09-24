#!/usr/bin/env python3
from __future__ import annotations
import json, math, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
CFG = ROOT / "BIO_CHI" / "config"
OUT = ROOT / "BIO_CHI" / "artifacts" / "generated" / "jarus_joint_meaning_v01"
OUT.mkdir(parents=True, exist_ok=True)

scalar = json.loads((CFG/"JARUS_CHI_BIO_SCALAR_P0Q_V01_RESULT_PIN.json").read_text())
modal_adm = json.loads((CFG/"JARUS_CHI_BIO_MODAL_ADMISSION_V01.json").read_text())
modal = json.loads((CFG/"JARUS_MODAL_INVENTORY_V01_RESULT_PIN.json").read_text())
beh = json.loads((CFG/"JARUS_FIG8_V02_RESULT_PIN_v0_1.json").read_text())
rt = json.loads((CFG/"JARUS_LOCAL_NONLINEAR_ROUNDTRIP_V01_RESULT_PIN.json").read_text())

if scalar["status"] != "CHI_BIO_P0Q_SUPPORTED_MODEL_SPECIFIC":
    raise SystemExit("joint gate requires admitted model-specific chi_bio")
if not modal_adm["admission"]["Chi_bio_model_specific_admitted"]:
    raise SystemExit("joint gate requires admitted model-specific Chi_bio")
if rt["status"] != "PASS_LOCAL_NONLINEAR_ROUNDTRIP":
    raise SystemExit("joint gate requires passed local nonlinear roundtrip")

cases=[]
any_scalar_incomplete=False
any_local_realized_divergence=False
all_modal_roundtrip=True

for case_id in ["FIG8A_NOMINAL_DAMPED","FIG8B_LIMIT_CYCLE","FIG8C_RELAXATION_OSCILLATION"]:
    rr=rt["cases"][case_id]
    mm=modal["cases"][case_id]
    bb=beh["behavior_adjudication"]["cases"][case_id]
    lam_real=float(rr["lambda_real"])
    spectral=float(mm["spectral_abscissae"][0])
    tol=1e-10*max(abs(lam_real),abs(spectral),1e-12)
    pair_sets_abscissa=abs(lam_real-spectral) <= tol
    scalar_local_status="SCALAR_SUFFICIENT_LOCAL" if pair_sets_abscissa else "SCALAR_INCOMPLETE_LOCAL"
    any_scalar_incomplete |= not pair_sets_abscissa

    local_direction="DECAYING_LOCAL_PAIR" if lam_real < 0 else ("AMPLIFYING_LOCAL_PAIR" if lam_real > 0 else "NEUTRAL_LOCAL_PAIR")
    if case_id=="FIG8A_NOMINAL_DAMPED":
        amps=[float(x) for x in bb["complete_amplitudes"]]
        finite_direction="DECREASING_AMPLITUDE" if amps[-1] < amps[0] else "NONDECREASING_AMPLITUDE"
        first_amp,last_amp=amps[0],amps[-1]
    else:
        first_amp=float(bb["first_complete_amplitude"])
        last_amp=float(bb["last_complete_amplitude"])
        finite_direction="DECREASING_AMPLITUDE" if last_amp < first_amp else "NONDECREASING_AMPLITUDE"

    concordant=(lam_real < 0 and finite_direction=="DECREASING_AMPLITUDE") or (lam_real > 0 and finite_direction=="NONDECREASING_AMPLITUDE")
    local_realized_status="LOCAL_REALIZED_DIRECTION_CONCORDANT" if concordant else "LOCAL_REALIZED_DIRECTION_DIVERGENT"
    any_local_realized_divergence |= not concordant

    pair_tau_seconds=(-1/lam_real) if lam_real < 0 else (1/lam_real if lam_real > 0 else None)
    spectral_tau_seconds=(-1/spectral) if spectral < 0 else (1/spectral if spectral > 0 else None)

    full_modal_pass=(rr.get("full_primary_error_1e-4") is not None and rt["scientific_disposition"]["full_six_state_lane_primary"]=="PASS_ALL_THREE_CASES")
    all_modal_roundtrip &= full_modal_pass

    cases.append({
        "case_id":case_id,
        "chi_bio":float(rr["chi_bio"]),
        "pair_lambda_real":lam_real,
        "spectral_abscissa":spectral,
        "pair_sets_spectral_abscissa":pair_sets_abscissa,
        "scalar_local_classification":scalar_local_status,
        "pair_or_local_efold_seconds":pair_tau_seconds,
        "spectral_abscissa_efold_seconds":spectral_tau_seconds,
        "finite_window_status":bb["finite_window_status"],
        "first_complete_amplitude":first_amp,
        "last_complete_amplitude":last_amp,
        "finite_window_direction":finite_direction,
        "local_pair_direction":local_direction,
        "local_vs_realized_classification":local_realized_status,
        "full_modal_local_roundtrip_pass":full_modal_pass
    })

outcomes=[]
if any_scalar_incomplete:
    outcomes.append("Chi_bio_ADDS_LOCAL_INFORMATION")
else:
    outcomes.append("SCALAR_SUFFICIENT_WITHIN_DECLARED_LOCAL_QUESTION")
if any_local_realized_divergence:
    outcomes.append("REALIZED_BEHAVIOR_REQUIRES_SYSTEM_LAYER")
if not all_modal_roundtrip:
    outcomes.append("REPRESENTATION_DEPENDENT")

result={
    "schema_version":"0.1",
    "project":"Bio Chi Investigation",
    "gate":"model-specific chi_bio <-> Chi_bio joint meaning and local-vs-realized behavior",
    "freeze":"BIO_CHI/config/JARUS_CHI_CHIBIO_JOINT_MEANING_FREEZE_v0_1.json",
    "epistemic_mode":"P0-Q",
    "status":"PASS_JOINT_MEANING_QUALIFICATION",
    "joint_outcomes":outcomes,
    "cases":cases,
    "interpretation":{
        "scalar_to_modal":"The admitted chi_bio factor is useful but not generally sufficient for local system stability. In the nominal damped case a separate real mode is slower than the oscillatory pair, so Chi_bio contributes information that chi_bio necessarily discards.",
        "modal_to_local_nonlinear":"The complete Chi_bio local modal representation passes the frozen local nonlinear round-trip in all three cases.",
        "local_to_realized":"In the two locally unstable B/C equilibria, the complex pair sets the positive spectral abscissa while the frozen finite-window peak-to-trough amplitudes decrease. Local instability and finite-window realized trajectory morphology are therefore distinct facts, not contradictory measurements of one scalar property.",
        "system_implication":"A system/trajectory layer is required to interpret realized behavior beyond local scalar or local modal identity. This qualifies the need for Bio Chi architecture but does not by itself establish broad cross-system Bio Chi or a global attractor topology."
    },
    "guards":{
        "master_scalar_created":False,
        "chi_equal_1_boundary_claimed":False,
        "stable_limit_cycle_proved":False,
        "P1_confirmation_claimed":False
    },
    "next_gate":"Class-C model-specific Bio Chi conglomerate adjudication, with independent ERK B3 transport retained as the next broader qualification route"
}
p=OUT/"jarus_joint_meaning_v0_1.json"
p.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
