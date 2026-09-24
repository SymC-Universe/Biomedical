#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import pathlib

import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm

from reproduce_blum_b3_native_v02 import rhs_factory, pool_matrix
from analyze_blum_b3_generator_transport_v02 import (
    stoichiometry, initial_state, analytic_jacobian, measurement_complex,
    measurement_gradient_complex_step, find_equilibrium, lane_params
)


ROOT=pathlib.Path(__file__).resolve().parents[2]
CFG=ROOT/"BIO_CHI"/"config"
OUT=ROOT/"BIO_CHI"/"artifacts"/"generated"/"blum_b3_local_nonlinear_roundtrip_v01"
OUT.mkdir(parents=True,exist_ok=True)


def safe_scale(x: np.ndarray, d: np.ndarray):
    d=d/np.linalg.norm(d)
    neg=d<0
    if np.any(neg):
        lim=float(np.min(x[neg]/(-d[neg])))
    else:
        lim=float("inf")
    eqnorm=float(np.linalg.norm(x,2))
    base=min(eqnorm,0.5*lim) if math.isfinite(lim) else eqnorm
    if not math.isfinite(base) or base<=0:
        return None,d,lim
    return base,d,lim


def deterministic_fret_series(p, Y):
    return np.array([float(np.real(measurement_complex(p,Y[:,k]))) for k in range(Y.shape[1])],dtype=float)


def relative_error(actual,pred):
    den=float(np.linalg.norm(pred))
    if den <= 1e-14:
        return None
    return float(np.linalg.norm(actual-pred)/den)


def integrate(rhs,x0,t):
    sol=solve_ivp(rhs,(float(t[0]),float(t[-1])),x0,t_eval=t,method="BDF",rtol=1e-10,atol=1e-12)
    if not sol.success or sol.y.shape != (15,t.size) or not np.all(np.isfinite(sol.y)):
        return None
    return sol.y


def source_key(lane,ctx_id):
    prefix="primary" if lane=="primary" else "sensitivity"
    suffix="FGF_2p5" if ctx_id=="SUSTAINED_FGF_2P5" else "FGF_250"
    return f"{prefix}_{suffix}"


def compare_generator_pin(vals, pairs, pin_record):
    expected=pin_record["complex_pairs"]
    got=sorted([float(x["chi"]) for x in pairs])
    exp=sorted([float(x["chi_bio_i"]) for x in expected])
    if len(got)!=len(exp):
        return False,{"reason":"pair_count","got":len(got),"expected":len(exp)}
    diffs=[abs(a-b) for a,b in zip(got,exp)]
    return max(diffs,default=0.0)<=1e-9,{"chi_abs_differences":diffs}


def pair_inventory(vals,V,Cr):
    floor=math.sqrt(np.finfo(float).eps)
    out=[]
    for i,z in enumerate(vals):
        if z.imag<=0:
            continue
        neg=[j for j,w in enumerate(vals) if w.imag<0]
        if not neg:
            continue
        j=min(neg,key=lambda j:abs(vals[j]-np.conj(z)))
        vis=float(abs(Cr@V[:,i])/(np.linalg.norm(Cr)*np.linalg.norm(V[:,i])))
        if vis<=floor:
            continue
        out.append({"i":i,"j":j,"lambda":z,"chi":float(-z.real/abs(z)),"visibility":vis})
    return out


def main():
    freeze=json.loads((CFG/"BLUM_B3_LOCAL_NONLINEAR_ROUNDTRIP_FREEZE_v0_1.json").read_text())
    src=json.loads((CFG/"BLUM_B3_TRANSPORT_SOURCE_FREEZE_v0_2.json").read_text())
    genpin=json.loads((CFG/"BLUM_B3_GENERATOR_TRANSPORT_V02_RESULT_PIN.json").read_text())
    if genpin["status"]!=freeze["source_generator_required_status"]:
        raise SystemExit("B3_ROUNDTRIP_REQUIRES_GENERATOR_PASS")

    S=stoichiometry()
    U,_,_=np.linalg.svd(S,full_matrices=False)
    Q=U[:,:8]
    Cpool=pool_matrix()
    independent_cols=[0,2,4,6,8,10,12,14]
    fractions=[1e-3,1e-4,1e-5]
    samples=int(freeze["solver"]["samples_per_lane"])

    context_records=[]
    overall_pair=True
    overall_full=True
    overall_self=True
    any_indeterminate=False
    all_real_refusal=True

    for lane in freeze["parameter_lanes"]:
        p=lane_params(src,lane)
        for ctx in freeze["input_contexts"]:
            ctx_id=ctx["id"]; fgf=float(ctx["fgf_input"])
            rhs=rhs_factory(p,fgf)
            y0=initial_state(p)
            xstar,horizon,attempts=find_equilibrium(rhs,y0,Cpool,{
                "candidate_horizons_minutes":[1000,10000,100000]
            })
            if xstar is None:
                context_records.append({"lane":lane,"context":ctx_id,"status":"INDETERMINATE_EQUILIBRIUM","attempts":attempts})
                any_indeterminate=True
                continue

            J=analytic_jacobian(p,fgf,S,xstar)
            Jr=Q.T@J@Q
            vals,V=np.linalg.eig(Jr)
            grad=measurement_gradient_complex_step(p,xstar)
            Cr=grad@Q
            pairs=pair_inventory(vals,V,Cr)
            ok_pin,pincheck=compare_generator_pin(vals,pairs,genpin["records"][source_key(lane,ctx_id)])
            if not ok_pin:
                context_records.append({"lane":lane,"context":ctx_id,"status":"FAIL_B3_IMPLEMENTATION_SELF_CHECK","generator_pin_check":pincheck})
                overall_self=False
                continue

            real_indices=[i for i,z in enumerate(vals) if z.imag==0]
            real_refusal=bool(real_indices)
            all_real_refusal=all_real_refusal and real_refusal

            pair_results=[]
            context_pair_pass=True
            for pi,pair in enumerate(pairs):
                i=pair["i"]; lam=pair["lambda"]; v=V[:,i]
                proj=Cr@v
                if abs(proj)<=0:
                    pair_results.append({"pair_index":pi,"status":"INDETERMINATE_ZERO_FRET_PHASE_PROJECTION"})
                    context_pair_pass=False; any_indeterminate=True; continue
                phase=np.exp(-1j*np.angle(proj))
                wphys=Q@(v*phase)
                d=np.real(wphys)
                dnorm=float(np.linalg.norm(d))
                if dnorm<=0 or not math.isfinite(dnorm):
                    pair_results.append({"pair_index":pi,"status":"INDETERMINATE_ZERO_REAL_PAIR_DIRECTION"})
                    context_pair_pass=False; any_indeterminate=True; continue
                d=d/dnorm
                base,d,limit=safe_scale(xstar,d)
                if base is None:
                    pair_results.append({"pair_index":pi,"status":"INDETERMINATE_POSITIVITY_SCALE"})
                    context_pair_pass=False; any_indeterminate=True; continue

                period=2*math.pi/abs(lam.imag)
                t=np.linspace(0,2*period,samples)
                denom=float(np.linalg.norm(np.real(wphys)))
                ampcheck=1e-4*base
                delta0=ampcheck*d
                pair_lin=np.column_stack([
                    ampcheck*np.real(wphys*np.exp(lam*tt))/denom for tt in t
                ])
                full_lin=np.column_stack([
                    Q@(expm(Jr*tt)@(Q.T@delta0)) for tt in t
                ])
                selferr=float(np.linalg.norm(pair_lin-full_lin,"fro")/max(np.linalg.norm(pair_lin,"fro"),np.finfo(float).tiny))
                selfpass=selferr<=1e-9
                overall_self=overall_self and selfpass

                amp_records=[]
                h0=float(np.real(measurement_complex(p,xstar)))
                for frac in fractions:
                    amp=frac*base
                    x0=xstar+amp*d
                    if np.min(x0)<-1e-12:
                        amp_records.append({"fraction":frac,"status":"INDETERMINATE_POSITIVITY_SCALE"})
                        continue
                    Y=integrate(rhs,x0,t)
                    if Y is None:
                        amp_records.append({"fraction":frac,"status":"INDETERMINATE_NUMERICAL"})
                        continue
                    pred=np.column_stack([
                        amp*np.real(wphys*np.exp(lam*tt))/denom for tt in t
                    ])
                    actual=Y-xstar[:,None]
                    state_err=float(np.linalg.norm(actual-pred,"fro")/max(np.linalg.norm(pred,"fro"),np.finfo(float).tiny))
                    fret_actual=deterministic_fret_series(p,Y)-h0
                    fret_pred=grad@pred
                    fret_err=relative_error(fret_actual,fret_pred)
                    amp_records.append({
                        "fraction":frac,"absolute_amplitude":amp,
                        "all_state_relative_error":state_err,
                        "FRET_relative_error":fret_err,
                        "minimum_nonlinear_state":float(np.min(Y)),
                        "status":"COMPLETE"
                    })

                prim={r["fraction"]:r for r in amp_records if r.get("status")=="COMPLETE"}
                pair_pass=(1e-3 in prim and 1e-4 in prim and
                           prim[1e-4]["all_state_relative_error"]<prim[1e-3]["all_state_relative_error"] and
                           (prim[1e-4]["FRET_relative_error"] is None or prim[1e-3]["FRET_relative_error"] is None or
                            prim[1e-4]["FRET_relative_error"]<prim[1e-3]["FRET_relative_error"]) and selfpass)
                context_pair_pass=context_pair_pass and pair_pass
                pair_results.append({
                    "pair_index":pi,
                    "lambda_real":float(lam.real),"lambda_imag":float(lam.imag),
                    "chi_bio_i":float(pair["chi"]),"FRET_visibility":float(pair["visibility"]),
                    "safe_scale":float(base),"positive_step_limit":float(limit),
                    "horizon_minutes":float(t[-1]),
                    "pair_vs_full_linear_relative_state_error":selferr,
                    "implementation_self_check_pass":bool(selfpass),
                    "amplitudes":amp_records,
                    "primary_pass":bool(pair_pass)
                })

            full_results=[]
            context_full_pass=True
            spectral=float(np.max(vals.real))
            if spectral>=0:
                full_horizon=None
                context_full_pass=False
                any_indeterminate=True
            else:
                full_horizon=5/abs(spectral)
                tfull=np.linspace(0,full_horizon,samples)
                h0=float(np.real(measurement_complex(p,xstar)))
                for colidx in independent_cols:
                    d=S[:,colidx].copy()
                    d=d/np.linalg.norm(d)
                    base,d,limit=safe_scale(xstar,d)
                    if base is None:
                        full_results.append({"stoichiometric_column":colidx,"status":"INDETERMINATE_POSITIVITY_SCALE"})
                        context_full_pass=False; any_indeterminate=True; continue
                    amp_records=[]
                    for frac in fractions:
                        amp=frac*base
                        x0=xstar+amp*d
                        if np.min(x0)<-1e-12:
                            amp_records.append({"fraction":frac,"status":"INDETERMINATE_POSITIVITY_SCALE"}); continue
                        Y=integrate(rhs,x0,tfull)
                        if Y is None:
                            amp_records.append({"fraction":frac,"status":"INDETERMINATE_NUMERICAL"}); continue
                        z0=Q.T@(amp*d)
                        pred=np.column_stack([Q@(expm(Jr*tt)@z0) for tt in tfull])
                        actual=Y-xstar[:,None]
                        state_err=float(np.linalg.norm(actual-pred,"fro")/max(np.linalg.norm(pred,"fro"),np.finfo(float).tiny))
                        fret_actual=deterministic_fret_series(p,Y)-h0
                        fret_pred=grad@pred
                        fret_err=relative_error(fret_actual,fret_pred)
                        amp_records.append({
                            "fraction":frac,"absolute_amplitude":amp,
                            "all_state_relative_error":state_err,
                            "FRET_relative_error":fret_err,
                            "minimum_nonlinear_state":float(np.min(Y)),
                            "status":"COMPLETE"
                        })
                    prim={r["fraction"]:r for r in amp_records if r.get("status")=="COMPLETE"}
                    dir_pass=(1e-3 in prim and 1e-4 in prim and
                              prim[1e-4]["all_state_relative_error"]<prim[1e-3]["all_state_relative_error"] and
                              (prim[1e-4]["FRET_relative_error"] is None or prim[1e-3]["FRET_relative_error"] is None or
                               prim[1e-4]["FRET_relative_error"]<prim[1e-3]["FRET_relative_error"]))
                    context_full_pass=context_full_pass and dir_pass
                    full_results.append({
                        "stoichiometric_column":colidx,
                        "safe_scale":float(base),"positive_step_limit":float(limit),
                        "amplitudes":amp_records,"primary_pass":bool(dir_pass)
                    })

            overall_pair=overall_pair and context_pair_pass
            overall_full=overall_full and context_full_pass
            context_records.append({
                "lane":lane,"context":ctx_id,"fgf_input":fgf,
                "status":"COMPLETE",
                "generator_pin_check":pincheck,
                "complex_pair_count":len(pairs),
                "pair_lane_pass":bool(context_pair_pass),
                "full_modal_lane_pass":bool(context_full_pass),
                "spectral_abscissa":spectral,
                "full_modal_horizon_minutes":float(full_horizon) if full_horizon is not None else None,
                "real_pole_refusal_control_pass":real_refusal,
                "pair_results":pair_results,
                "full_modal_results":full_results
            })

    if not overall_self or not all_real_refusal:
        status="FAIL_B3_IMPLEMENTATION_SELF_CHECK"
    elif any_indeterminate and not (overall_pair and overall_full):
        status="INDETERMINATE_NUMERICAL"
    elif not overall_pair:
        status="FAIL_B3_PAIR_LOCAL_ROUNDTRIP"
    elif not overall_full:
        status="FAIL_B3_FULL_MODAL_LOCAL_ROUNDTRIP"
    else:
        status="PASS_B3_LOCAL_NONLINEAR_ROUNDTRIP"

    result={
        "schema_version":"0.1","project":"Bio Chi Investigation",
        "gate":"Blum B3 local nonlinear round-trip",
        "freeze":"BIO_CHI/config/BLUM_B3_LOCAL_NONLINEAR_ROUNDTRIP_FREEZE_v0_1.json",
        "epistemic_mode":"P0-Q","status":status,
        "contexts":context_records,
        "pair_lane_all_contexts_pass":bool(overall_pair),
        "full_modal_lane_all_contexts_pass":bool(overall_full),
        "implementation_self_checks_pass":bool(overall_self and all_real_refusal),
        "ERK_Chi_bio_admitted":False,
        "Bio_Chi_transport_adjudicated":False,
        "P1_confirmation_claimed":False,
        "interpretation_limit":"Local nonlinear qualification only. Source-wide transient/realized response and Bio Chi joint meaning remain separate."
    }
    (OUT/"blum_b3_local_nonlinear_roundtrip_v0_1.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
