#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import pathlib
from itertools import combinations

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import linear_sum_assignment

from reproduce_blum_b3_native_v02 import rhs_factory, pool_matrix, STATE_ORDER


ROOT=pathlib.Path(__file__).resolve().parents[2]
CFG=ROOT/"BIO_CHI"/"config"
OUT=ROOT/"BIO_CHI"/"artifacts"/"generated"/"blum_b3_generator_transport_v01"
OUT.mkdir(parents=True,exist_ok=True)


def stoichiometry() -> np.ndarray:
    S=np.zeros((15,16),dtype=float)
    def col(j, changes):
        for i,v in changes.items():
            S[i,j]=v
    col(0,{0:-1,1:1}); col(1,{0:1,1:-1})
    col(2,{2:-1,3:1}); col(3,{2:1,3:-1})
    col(4,{4:-1,5:1}); col(5,{4:1,5:-1})
    col(6,{6:-1,7:1}); col(7,{6:1,7:-1})
    col(8,{8:-1,9:1}); col(9,{8:1,9:-1})
    col(10,{10:-1,11:1}); col(11,{10:1,11:-1})
    col(12,{12:-1,13:1}); col(13,{12:1,13:-1})
    col(14,{10:-1,13:-1,14:1}); col(15,{10:1,13:1,14:-1})
    return S


def initial_state(p: dict[str,float]) -> np.ndarray:
    return np.array([
        0.1,0.0,0.7,0.0,0.68,0.0,0.26,0.0,p["nfb_init"],0.0,
        p["fgfr_init_mean"],0.0,p["h_init_mean"],0.0,0.0
    ],dtype=float)


def jacobian(rhs, x: np.ndarray, mult: float) -> np.ndarray:
    n=x.size
    J=np.zeros((n,n),dtype=float)
    base=np.finfo(float).eps**(1/3)
    for j in range(n):
        h=mult*base*max(1.0,abs(float(x[j])))
        xp=x.copy(); xm=x.copy()
        xp[j]+=h; xm[j]-=h
        J[:,j]=(rhs(0.0,xp)-rhs(0.0,xm))/(2*h)
    return J


def measurement(p: dict[str,float], x: np.ndarray) -> float:
    Erk=float(x[6]); Erk_s=float(x[7])
    F=float(p["FRET_E"]); emax=0.8; einit=0.0
    num=(0.15*Erk_s
         +einit*(-1.15*Erk-1.15*Erk_s+F*Erk_s)
         +emax*((1+0.15*F*einit)*Erk+(1-1.15*F+0.15*F*einit)*Erk_s))
    den=(emax-einit)*(Erk+Erk_s-F*Erk_s)
    return num/den


def measurement_gradient(p: dict[str,float], x: np.ndarray) -> np.ndarray:
    g=np.zeros(x.size,dtype=float)
    base=np.finfo(float).eps**(1/3)
    for j in range(x.size):
        h=base*max(1.0,abs(float(x[j])))
        xp=x.copy(); xm=x.copy()
        xp[j]+=h; xm[j]-=h
        g[j]=(measurement(p,xp)-measurement(p,xm))/(2*h)
    return g


def eig_match(ref: np.ndarray, alt: np.ndarray):
    cost=np.abs(ref[:,None]-alt[None,:])
    rr,cc=linear_sum_assignment(cost)
    matched=np.empty_like(ref)
    matched[rr]=alt[cc]
    spread=np.abs(matched-ref)
    denom=np.maximum(np.abs(ref),1e-12)
    rel=spread/denom
    return matched,spread,rel


def modal_metrics(Jr: np.ndarray, Cr: np.ndarray):
    vals,V=np.linalg.eig(Jr)
    cond=float(np.linalg.cond(V,2))
    scale=max(float(np.max(np.abs(vals))),np.finfo(float).tiny)
    min_sep=min(abs(vals[i]-vals[j]) for i,j in combinations(range(vals.size),2))
    norm_sep=float(min_sep/scale)

    O=np.vstack([Cr @ np.linalg.matrix_power(Jr,k) for k in range(Jr.shape[0])])
    sv=np.linalg.svd(O,compute_uv=False)
    tol=max(O.shape)*np.finfo(float).eps*(float(sv[0]) if sv.size else 0.0)
    rank=int(np.sum(sv>tol))
    crnorm=float(np.linalg.norm(Cr,2))
    vis=[]
    for j in range(vals.size):
        v=V[:,j]
        den=crnorm*float(np.linalg.norm(v,2))
        vis.append(float(abs(Cr@v)/den) if den>0 else 0.0)
    return vals,V,cond,norm_sep,rank,sv,vis


def complex_pair_records(vals: np.ndarray, vis: list[float]):
    floor=math.sqrt(np.finfo(float).eps)
    pos=[i for i,z in enumerate(vals) if z.imag>0]
    neg=[i for i,z in enumerate(vals) if z.imag<0]
    used=set()
    records=[]
    for i in pos:
        if not neg:
            continue
        j=min((j for j in neg if j not in used), key=lambda j: abs(vals[j]-np.conj(vals[i])), default=None)
        if j is None:
            continue
        used.add(j)
        lam=vals[i]
        pair_res=float(abs(vals[j]-np.conj(lam)))
        omega0=float(abs(lam))
        records.append({
            "positive_imag_mode_index":int(i),
            "negative_imag_mode_index":int(j),
            "lambda_real":float(lam.real),
            "lambda_imag":float(lam.imag),
            "conjugate_pair_residual":pair_res,
            "gamma":float(-2*lam.real),
            "omega0":omega0,
            "omega_d":float(abs(lam.imag)),
            "chi_bio_i":float(-lam.real/omega0) if omega0>0 else None,
            "FRET_visibility_positive_mode":float(vis[i]),
            "FRET_visibility_negative_mode":float(vis[j]),
            "FRET_visible":bool(max(vis[i],vis[j])>floor),
            "visibility_floor_sqrt_eps":floor
        })
    return records


def find_equilibrium(rhs, y0, Cpool, freeze_eq):
    candidates=[]
    for horizon in freeze_eq["candidate_horizons_minutes"]:
        sol=solve_ivp(rhs,(0.0,float(horizon)),y0,method="BDF",rtol=1e-10,atol=1e-12)
        if not sol.success or sol.y.size==0:
            candidates.append({"horizon":horizon,"solver_success":False})
            continue
        x=sol.y[:,-1]
        residual=float(np.linalg.norm(rhs(float(horizon),x),ord=np.inf))
        drift=float(np.max(np.abs(Cpool@x-Cpool@y0)))
        min_state=float(np.min(x))
        ok=(np.all(np.isfinite(x)) and residual<=1e-9 and drift<=1e-8 and min_state>=-1e-10)
        rec={
            "horizon_minutes":int(horizon),
            "solver_success":True,
            "residual_inf":residual,
            "pool_drift_max_abs":drift,
            "minimum_state":min_state,
            "accepted":bool(ok)
        }
        candidates.append(rec)
        if ok:
            return x,int(horizon),candidates
    return None,None,candidates


def lane_params(source_freeze, lane):
    names=source_freeze["primary_parameter_names"]
    vals=source_freeze["primary_parameter_values"] if lane=="primary" else source_freeze["sensitivity_parameter_values"]
    return dict(zip(names,map(float,vals)))


def main():
    freeze=json.loads((CFG/"BLUM_B3_GENERATOR_TRANSPORT_FREEZE_v0_1.json").read_text())
    src=json.loads((CFG/"BLUM_B3_TRANSPORT_SOURCE_FREEZE_v0_2.json").read_text())
    repro=json.loads((CFG/"BLUM_B3_NATIVE_REPRODUCTION_V02_RESULT_PIN.json").read_text())
    if repro.get("status") != freeze["required_source_reproduction_status"]:
        raise SystemExit("BLUM_B3_GENERATOR_REQUIRES_PASSED_NATIVE_REPRODUCTION")

    S=stoichiometry()
    rank=int(np.linalg.matrix_rank(S))
    if rank != int(freeze["stoichiometric_structure"]["expected_rank"]):
        raise SystemExit(f"BLUM_B3_STOICHIOMETRY_RANK_MISMATCH {rank}")
    Cpool=pool_matrix()
    cs=float(np.max(np.abs(Cpool@S)))
    if cs != 0.0:
        raise SystemExit(f"BLUM_B3_CONSERVATION_MATRIX_FAIL {cs}")

    U,svals,_=np.linalg.svd(S,full_matrices=False)
    Q=U[:,:rank]
    independent_cols=[0,2,4,6,8,10,12,14]
    Q2,_=np.linalg.qr(S[:,independent_cols],mode="reduced")

    sep_floor=math.sqrt(np.finfo(float).eps)
    cond_ceiling=1/sep_floor
    spread_ceiling=float(freeze["jacobian_gate"]["maximum_relative_complex_spread_for_numerical_pass"])

    records=[]
    lane_summary={}
    for lane in ["primary","sensitivity"]:
        p=lane_params(src,lane)
        lane_summary[lane]={"contexts":{}}
        for ctx in freeze["input_contexts"]:
            ctx_id=ctx["id"]; fgf=float(ctx["fgf_input"])
            rhs=rhs_factory(p,fgf)
            y0=initial_state(p)
            xstar,horizon,eq_attempts=find_equilibrium(rhs,y0,Cpool,freeze["equilibrium_gate"])
            if xstar is None:
                rec={"lane":lane,"context":ctx_id,"fgf_input":fgf,"status":"INDETERMINATE_EQUILIBRIUM","equilibrium_attempts":eq_attempts}
                records.append(rec); lane_summary[lane]["contexts"][ctx_id]=rec["status"]; continue

            grad=measurement_gradient(p,xstar)
            Cr=grad@Q
            Cr2=grad@Q2

            steps=[]
            ref_vals=None
            all_step_pass=True
            reference_metrics=None
            max_rel_spread=0.0
            basis_max_rel=0.0
            for mult in freeze["jacobian_gate"]["multipliers"]:
                J=jacobian(rhs,xstar,float(mult))
                Jr=Q.T@J@Q
                Jr2=Q2.T@J@Q2
                vals,V,cond,norm_sep,obs_rank,sv,vis=modal_metrics(Jr,Cr)
                vals2,*_=modal_metrics(Jr2,Cr2)
                _,_,basis_rel=eig_match(vals,vals2)
                basis_rel_max=float(np.max(basis_rel))
                basis_max_rel=max(basis_max_rel,basis_rel_max)

                if ref_vals is None:
                    ref_vals=vals.copy()
                    rel_spread=np.zeros_like(np.abs(vals),dtype=float)
                    reference_metrics=(vals,V,cond,norm_sep,obs_rank,sv,vis)
                else:
                    _,_,rel_spread=eig_match(ref_vals,vals)
                    max_rel_spread=max(max_rel_spread,float(np.max(rel_spread)))

                cond_pass=math.isfinite(cond) and cond<cond_ceiling
                sep_pass=math.isfinite(norm_sep) and norm_sep>sep_floor
                step_pass=(cond_pass and sep_pass and basis_rel_max<=1e-8 and np.all(np.isfinite(vals)))
                all_step_pass=all_step_pass and step_pass
                steps.append({
                    "multiplier":float(mult),
                    "eigenvalues":[{"real":float(z.real),"imag":float(z.imag)} for z in vals],
                    "condition_number_V_2":float(cond),
                    "minimum_normalized_eigenvalue_separation":float(norm_sep),
                    "FRET_observability_rank":int(obs_rank),
                    "FRET_observability_singular_values":[float(x) for x in sv],
                    "FRET_mode_visibility":[float(x) for x in vis],
                    "basis_invariance_max_relative_eigenvalue_difference":basis_rel_max,
                    "relative_spread_from_reference":[float(x) for x in rel_spread],
                    "step_pass":bool(step_pass)
                })

            vals,V,cond,norm_sep,obs_rank,sv,vis=reference_metrics
            spread_pass=max_rel_spread<=spread_ceiling
            all_step_pass=all_step_pass and spread_pass
            pairs=complex_pair_records(vals,vis)
            visible_pairs=[x for x in pairs if x["FRET_visible"]]
            if not pairs:
                scalar_status="SCALAR_REFUSED_NO_COMPLEX_FACTOR"
            elif not visible_pairs:
                scalar_status="SCALAR_REFUSED_NOT_OBSERVABLE"
            else:
                scalar_status="MODEL_SPECIFIC_CHI_BIO_PAIR_FAMILY_PRESENT"

            if not all_step_pass:
                modal_status="REFUSE_B3_MODAL_NUMERICAL_CONDITIONING"
            elif obs_rank==rank:
                modal_status="PASS_B3_GENERATOR_MODAL_QUALIFICATION"
            else:
                modal_status="PASS_B3_MODAL_WITH_PARTIAL_FRET_OBSERVABILITY"

            rec={
                "lane":lane,
                "context":ctx_id,
                "fgf_input":fgf,
                "status":modal_status,
                "equilibrium":{
                    "accepted_horizon_minutes":horizon,
                    "state":[float(x) for x in xstar],
                    "residual_inf":float(np.linalg.norm(rhs(float(horizon),xstar),ord=np.inf)),
                    "pool_drift_max_abs":float(np.max(np.abs(Cpool@xstar-Cpool@y0))),
                    "attempts":eq_attempts
                },
                "stoichiometric_rank":rank,
                "reduced_dimension":rank,
                "FRET_observability_rank_reference":int(obs_rank),
                "FRET_full_observability":bool(obs_rank==rank),
                "maximum_relative_eigenvalue_spread_across_steps":float(max_rel_spread),
                "maximum_basis_invariance_relative_eigenvalue_difference":float(basis_max_rel),
                "scalar_status":scalar_status,
                "complex_pair_count":len(pairs),
                "FRET_visible_complex_pair_count":len(visible_pairs),
                "complex_pairs":pairs,
                "steps":steps
            }
            records.append(rec)
            lane_summary[lane]["contexts"][ctx_id]={
                "modal_status":modal_status,
                "scalar_status":scalar_status,
                "complex_pair_count":len(pairs),
                "visible_pair_count":len(visible_pairs),
                "FRET_observability_rank":int(obs_rank)
            }

    primary_eval=[r for r in records if r["lane"]=="primary" and not r["status"].startswith("INDETERMINATE")]
    sens_eval=[r for r in records if r["lane"]=="sensitivity" and not r["status"].startswith("INDETERMINATE")]
    all_eval=primary_eval+sens_eval
    if len(all_eval)<4:
        modal_overall="INDETERMINATE_EQUILIBRIUM"
    elif any(r["status"]=="REFUSE_B3_MODAL_NUMERICAL_CONDITIONING" for r in all_eval):
        modal_overall="REFUSE_B3_MODAL_NUMERICAL_CONDITIONING"
    elif all(r["status"]=="PASS_B3_GENERATOR_MODAL_QUALIFICATION" for r in all_eval):
        modal_overall="PASS_B3_GENERATOR_MODAL_QUALIFICATION"
    else:
        modal_overall="PASS_B3_MODAL_WITH_PARTIAL_FRET_OBSERVABILITY"

    common_visible=[]
    for ctx in [x["id"] for x in freeze["input_contexts"]]:
        p=lane_summary["primary"]["contexts"].get(ctx,{})
        s=lane_summary["sensitivity"]["contexts"].get(ctx,{})
        if isinstance(p,dict) and isinstance(s,dict):
            if p.get("scalar_status")=="MODEL_SPECIFIC_CHI_BIO_PAIR_FAMILY_PRESENT" and s.get("scalar_status")=="MODEL_SPECIFIC_CHI_BIO_PAIR_FAMILY_PRESENT":
                common_visible.append(ctx)
    primary_any=any(isinstance(v,dict) and v.get("scalar_status")=="MODEL_SPECIFIC_CHI_BIO_PAIR_FAMILY_PRESENT" for v in lane_summary["primary"]["contexts"].values())
    sens_any=any(isinstance(v,dict) and v.get("scalar_status")=="MODEL_SPECIFIC_CHI_BIO_PAIR_FAMILY_PRESENT" for v in lane_summary["sensitivity"]["contexts"].values())
    if common_visible:
        scalar_overall="SCALAR_TRANSPORT_PRESENT"
    elif primary_any or sens_any:
        scalar_overall="SCALAR_TRANSPORT_PARAMETER_DEPENDENT"
    else:
        scalar_overall="SCALAR_TRANSPORT_REFUSED"

    result={
        "schema_version":"0.1",
        "project":"Bio Chi Investigation",
        "gate":"Blum B3 stoichiometric-subspace generator transport",
        "freeze":"BIO_CHI/config/BLUM_B3_GENERATOR_TRANSPORT_FREEZE_v0_1.json",
        "epistemic_mode":"P0-Q",
        "stoichiometric_rank":rank,
        "full_state_dimension":15,
        "dynamic_subspace_dimension":rank,
        "conservation_matrix_times_stoichiometry_max_abs":cs,
        "modal_transport_status":modal_overall,
        "scalar_transport_status":scalar_overall,
        "common_contexts_with_FRET_visible_complex_pair_family":common_visible,
        "lane_summary":lane_summary,
        "records":records,
        "broad_Bio_Chi_admitted":False,
        "P1_confirmation_claimed":False,
        "chi_equal_1_boundary_claimed":False,
        "master_scalar_created":False,
        "interpretation_limit":"Independent P0-Q transport of the generator-first scalar/modal construction only. Native B3 remains the comparator. Whole-system Bio Chi and predictive confirmation require a separately frozen realized-response/joint-meaning test."
    }
    out=OUT/"blum_b3_generator_transport_v0_1.json"
    out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
