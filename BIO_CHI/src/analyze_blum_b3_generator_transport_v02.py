#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import pathlib
from itertools import combinations

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import linear_sum_assignment

from reproduce_blum_b3_native_v02 import rhs_factory, pool_matrix


ROOT=pathlib.Path(__file__).resolve().parents[2]
CFG=ROOT/"BIO_CHI"/"config"
OUT=ROOT/"BIO_CHI"/"artifacts"/"generated"/"blum_b3_generator_transport_v02"
OUT.mkdir(parents=True,exist_ok=True)


def stoichiometry() -> np.ndarray:
    S=np.zeros((15,16),dtype=float)
    changes=[
        {0:-1,1:1},{0:1,1:-1},
        {2:-1,3:1},{2:1,3:-1},
        {4:-1,5:1},{4:1,5:-1},
        {6:-1,7:1},{6:1,7:-1},
        {8:-1,9:1},{8:1,9:-1},
        {10:-1,11:1},{10:1,11:-1},
        {12:-1,13:1},{12:1,13:-1},
        {10:-1,13:-1,14:1},{10:1,13:1,14:-1}
    ]
    for j,ch in enumerate(changes):
        for i,v in ch.items():
            S[i,j]=v
    return S


def initial_state(p):
    return np.array([
        0.1,0.0,0.7,0.0,0.68,0.0,0.26,0.0,p["nfb_init"],0.0,
        p["fgfr_init_mean"],0.0,p["h_init_mean"],0.0,0.0
    ],dtype=float)


def source_rates_complex(p,fgf,x):
    Ras,Ras_s,Raf,Raf_s,Mek,Mek_s,Erk,Erk_s,Nfb,Nfb_s,FgfR,FgfR_s,H,H_F,H_F_R=x
    kn_h=p["K_NFB"]**p["h_nfb"]
    nfb_h=Nfb_s**p["h_nfb"]
    return np.array([
        p["k_1_2"]*(p["r_h"]*H_F_R+(1-p["r_h"])*FgfR_s)*(Ras/(p["K_1_2"]+Ras)),
        p["k_2_1"]*(Ras_s/(p["K_2_1"]+Ras_s)),
        p["k_3_4"]*Ras_s*(Raf/(p["K_3_4"]+Raf))*(kn_h/(kn_h+nfb_h)),
        p["k_4_3"]*(Raf_s/(p["K_4_3"]+Raf_s)),
        p["k_5_6"]*Raf_s*(Mek/(p["K_5_6"]+Mek)),
        p["k_6_5"]*(Mek_s/(p["K_6_5"]+Mek_s)),
        p["k_7_8"]*Mek_s*(Erk/(p["K_7_8"]+Erk)),
        p["k_8_7"]*(Erk_s/(p["K_8_7"]+Erk_s)),
        p["f_1_2"]*Erk_s*(Nfb/(p["F_1_2"]+Nfb)),
        p["f_2_1"]*(Nfb_s/(p["F_2_1"]+Nfb_s)),
        p["r_3_4"]*fgf*FgfR,
        p["r_4_3"]*FgfR_s,
        p["r_5_6"]*H*fgf,
        p["r_6_5"]*H_F,
        p["r_5_7"]*H_F*FgfR,
        p["r_7_5"]*H_F_R
    ])


def rhs_complex(p,fgf,S,x):
    return S @ source_rates_complex(p,fgf,x)


def analytic_rate_jacobian(p,fgf,x):
    Ras,Ras_s,Raf,Raf_s,Mek,Mek_s,Erk,Erk_s,Nfb,Nfb_s,FgfR,FgfR_s,H,H_F,H_F_R=x
    G=np.zeros((16,15),dtype=float)

    A=p["r_h"]*H_F_R+(1-p["r_h"])*FgfR_s
    G[0,0]=p["k_1_2"]*A*p["K_1_2"]/(p["K_1_2"]+Ras)**2
    G[0,11]=p["k_1_2"]*(1-p["r_h"])*Ras/(p["K_1_2"]+Ras)
    G[0,14]=p["k_1_2"]*p["r_h"]*Ras/(p["K_1_2"]+Ras)

    G[1,1]=p["k_2_1"]*p["K_2_1"]/(p["K_2_1"]+Ras_s)**2

    h=p["h_nfb"]; Kpow=p["K_NFB"]**h; Npow=Nfb_s**h
    inhib=Kpow/(Kpow+Npow)
    G[2,1]=p["k_3_4"]*(Raf/(p["K_3_4"]+Raf))*inhib
    G[2,2]=p["k_3_4"]*Ras_s*p["K_3_4"]/(p["K_3_4"]+Raf)**2*inhib
    if Nfb_s <= 0:
        raise FloatingPointError("analytic Hill derivative requires positive Nfb_star")
    dinhib=-Kpow*h*(Nfb_s**(h-1))/(Kpow+Npow)**2
    G[2,9]=p["k_3_4"]*Ras_s*(Raf/(p["K_3_4"]+Raf))*dinhib

    G[3,3]=p["k_4_3"]*p["K_4_3"]/(p["K_4_3"]+Raf_s)**2

    G[4,3]=p["k_5_6"]*Mek/(p["K_5_6"]+Mek)
    G[4,4]=p["k_5_6"]*Raf_s*p["K_5_6"]/(p["K_5_6"]+Mek)**2
    G[5,5]=p["k_6_5"]*p["K_6_5"]/(p["K_6_5"]+Mek_s)**2

    G[6,5]=p["k_7_8"]*Erk/(p["K_7_8"]+Erk)
    G[6,6]=p["k_7_8"]*Mek_s*p["K_7_8"]/(p["K_7_8"]+Erk)**2
    G[7,7]=p["k_8_7"]*p["K_8_7"]/(p["K_8_7"]+Erk_s)**2

    G[8,7]=p["f_1_2"]*Nfb/(p["F_1_2"]+Nfb)
    G[8,8]=p["f_1_2"]*Erk_s*p["F_1_2"]/(p["F_1_2"]+Nfb)**2
    G[9,9]=p["f_2_1"]*p["F_2_1"]/(p["F_2_1"]+Nfb_s)**2

    G[10,10]=p["r_3_4"]*fgf
    G[11,11]=p["r_4_3"]
    G[12,12]=p["r_5_6"]*fgf
    G[13,13]=p["r_6_5"]
    G[14,10]=p["r_5_7"]*H_F
    G[14,13]=p["r_5_7"]*FgfR
    G[15,14]=p["r_7_5"]
    return G


def analytic_jacobian(p,fgf,S,x):
    return S @ analytic_rate_jacobian(p,fgf,x)


def complex_step_jacobian(p,fgf,S,x,h=1e-20):
    J=np.zeros((x.size,x.size),dtype=float)
    for j in range(x.size):
        xc=x.astype(complex)
        xc[j]+=1j*h
        J[:,j]=np.imag(rhs_complex(p,fgf,S,xc))/h
    return J


def measurement_complex(p,x):
    Erk=x[6]; Erk_s=x[7]
    F=p["FRET_E"]; emax=0.8; einit=0.0
    num=(0.15*Erk_s
         +einit*(-1.15*Erk-1.15*Erk_s+F*Erk_s)
         +emax*((1+0.15*F*einit)*Erk+(1-1.15*F+0.15*F*einit)*Erk_s))
    den=(emax-einit)*(Erk+Erk_s-F*Erk_s)
    return num/den


def measurement_gradient_complex_step(p,x,h=1e-20):
    g=np.zeros(x.size,dtype=float)
    for j in range(x.size):
        xc=x.astype(complex)
        xc[j]+=1j*h
        g[j]=np.imag(measurement_complex(p,xc))/h
    return g


def eig_match(ref,alt):
    cost=np.abs(ref[:,None]-alt[None,:])
    rr,cc=linear_sum_assignment(cost)
    matched=np.empty_like(ref)
    matched[rr]=alt[cc]
    rel=np.abs(matched-ref)/np.maximum(np.abs(ref),1e-12)
    return matched,rel


def modal_metrics(Jr,Cr):
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


def complex_pairs(vals,vis):
    floor=math.sqrt(np.finfo(float).eps)
    pos=[i for i,z in enumerate(vals) if z.imag>0]
    neg=[i for i,z in enumerate(vals) if z.imag<0]
    used=set(); out=[]
    for i in pos:
        choices=[j for j in neg if j not in used]
        if not choices: continue
        j=min(choices,key=lambda j:abs(vals[j]-np.conj(vals[i])))
        used.add(j)
        lam=vals[i]; w=float(abs(lam))
        out.append({
            "positive_imag_mode_index":int(i),
            "negative_imag_mode_index":int(j),
            "lambda_real":float(lam.real),
            "lambda_imag":float(lam.imag),
            "conjugate_pair_residual":float(abs(vals[j]-np.conj(lam))),
            "gamma":float(-2*lam.real),
            "omega0":w,
            "omega_d":float(abs(lam.imag)),
            "chi_bio_i":float(-lam.real/w) if w>0 else None,
            "FRET_visibility_positive_mode":float(vis[i]),
            "FRET_visibility_negative_mode":float(vis[j]),
            "FRET_visible":bool(max(vis[i],vis[j])>floor),
            "visibility_floor_sqrt_eps":floor
        })
    return out


def find_equilibrium(rhs,y0,Cpool,freeze_eq):
    attempts=[]
    for horizon in freeze_eq["candidate_horizons_minutes"]:
        sol=solve_ivp(rhs,(0,float(horizon)),y0,method="BDF",rtol=1e-10,atol=1e-12)
        if not sol.success:
            attempts.append({"horizon_minutes":horizon,"solver_success":False}); continue
        x=sol.y[:,-1]
        residual=float(np.linalg.norm(rhs(float(horizon),x),ord=np.inf))
        drift=float(np.max(np.abs(Cpool@x-Cpool@y0)))
        minstate=float(np.min(x))
        ok=np.all(np.isfinite(x)) and residual<=1e-9 and drift<=1e-8 and minstate>=-1e-10
        attempts.append({"horizon_minutes":horizon,"solver_success":True,"residual_inf":residual,"pool_drift_max_abs":drift,"minimum_state":minstate,"accepted":bool(ok)})
        if ok: return x,int(horizon),attempts
    return None,None,attempts


def lane_params(src,lane):
    names=src["primary_parameter_names"]
    vals=src["primary_parameter_values"] if lane=="primary" else src["sensitivity_parameter_values"]
    return dict(zip(names,map(float,vals)))


def main():
    freeze=json.loads((CFG/"BLUM_B3_GENERATOR_TRANSPORT_FREEZE_v0_2.json").read_text())
    src=json.loads((CFG/"BLUM_B3_TRANSPORT_SOURCE_FREEZE_v0_2.json").read_text())
    repro=json.loads((CFG/"BLUM_B3_NATIVE_REPRODUCTION_V02_RESULT_PIN.json").read_text())
    v01=json.loads((CFG/"BLUM_B3_GENERATOR_TRANSPORT_V01_RESULT_PIN.json").read_text())
    if repro["status"]!="PASS_NATIVE_B3_TRAJECTORY_REPRODUCTION":
        raise SystemExit("B3_V02_REQUIRES_NATIVE_REPRO_PASS")
    if v01["status"]!="REFUSE_B3_MODAL_NUMERICAL_CONDITIONING":
        raise SystemExit("B3_V02_REQUIRES_PRESERVED_V01_REFUSAL")

    S=stoichiometry()
    rank=int(np.linalg.matrix_rank(S))
    if rank != 8: raise SystemExit(f"B3_BAD_STOICH_RANK {rank}")
    Cpool=pool_matrix()
    if float(np.max(np.abs(Cpool@S))) != 0.0:
        raise SystemExit("B3_CONSERVATION_STRUCTURAL_FAIL")
    U,_,_=np.linalg.svd(S,full_matrices=False); Q=U[:,:rank]
    Q2,_=np.linalg.qr(S[:,[0,2,4,6,8,10,12,14]],mode="reduced")

    sep_floor=math.sqrt(np.finfo(float).eps)
    cond_ceiling=1/sep_floor
    basis_ceiling=float(freeze["conditioning_gate"]["basis_invariance_relative_eigenvalue_difference_ceiling"])
    jac_ceiling=float(freeze["jacobian_gate"]["independent_derivative_check"]["relative_Frobenius_error_ceiling"])

    records=[]; lane_summary={"primary":{"contexts":{}},"sensitivity":{"contexts":{}}}
    any_jac_fail=False
    for lane in ["primary","sensitivity"]:
        p=lane_params(src,lane)
        for ctx in freeze["input_contexts"]:
            ctx_id=ctx["id"]; fgf=float(ctx["fgf_input"])
            native_rhs=rhs_factory(p,fgf)
            y0=initial_state(p)
            xstar,horizon,attempts=find_equilibrium(native_rhs,y0,Cpool,freeze["equilibrium_gate"])
            if xstar is None:
                rec={"lane":lane,"context":ctx_id,"fgf_input":fgf,"status":"INDETERMINATE_EQUILIBRIUM","equilibrium_attempts":attempts}
                records.append(rec); lane_summary[lane]["contexts"][ctx_id]=rec["status"]; continue

            rhs_anchor=float(np.max(np.abs(np.real(rhs_complex(p,fgf,S,xstar))-native_rhs(0,xstar))))
            Ja=analytic_jacobian(p,fgf,S,xstar)
            Jcs=complex_step_jacobian(p,fgf,S,xstar,h=float(freeze["jacobian_gate"]["independent_derivative_check"]["step"]))
            jac_rel=float(np.linalg.norm(Ja-Jcs,"fro")/max(np.linalg.norm(Jcs,"fro"),np.finfo(float).tiny))
            jac_check=(rhs_anchor<=1e-12 and np.all(np.isfinite(Ja)) and np.all(np.isfinite(Jcs)) and jac_rel<=jac_ceiling)
            any_jac_fail=any_jac_fail or not jac_check

            grad=measurement_gradient_complex_step(p,xstar)
            Cr=grad@Q; Cr2=grad@Q2
            Jr=Q.T@Ja@Q; Jr2=Q2.T@Ja@Q2
            vals,V,cond,norm_sep,obs_rank,sv,vis=modal_metrics(Jr,Cr)
            vals2,*_=modal_metrics(Jr2,Cr2)
            _,basis_rel=eig_match(vals,vals2)
            basis_max=float(np.max(basis_rel))

            cond_pass=math.isfinite(cond) and cond<cond_ceiling
            sep_pass=math.isfinite(norm_sep) and norm_sep>sep_floor
            basis_pass=basis_max<=basis_ceiling
            modal_numeric_pass=jac_check and cond_pass and sep_pass and basis_pass and np.all(np.isfinite(vals))

            pairs=complex_pairs(vals,vis)
            visible=[x for x in pairs if x["FRET_visible"]]
            if not jac_check:
                modal_status="REFUSE_ANALYTIC_JACOBIAN_SELF_CHECK"
                scalar_status="SCALAR_WITHHELD_UPSTREAM_JACOBIAN_REFUSAL"
            elif not modal_numeric_pass:
                modal_status="REFUSE_B3_MODAL_NUMERICAL_CONDITIONING"
                scalar_status="SCALAR_WITHHELD_UPSTREAM_MODAL_REFUSAL"
            else:
                modal_status="PASS_B3_GENERATOR_MODAL_QUALIFICATION" if obs_rank==rank else "PASS_B3_MODAL_WITH_PARTIAL_FRET_OBSERVABILITY"
                if not pairs:
                    scalar_status="SCALAR_REFUSED_NO_COMPLEX_FACTOR"
                elif not visible:
                    scalar_status="SCALAR_REFUSED_NOT_OBSERVABLE"
                else:
                    scalar_status="MODEL_SPECIFIC_CHI_BIO_PAIR_FAMILY_PRESENT"

            rec={
                "lane":lane,"context":ctx_id,"fgf_input":fgf,"status":modal_status,
                "equilibrium":{"accepted_horizon_minutes":horizon,"state":[float(x) for x in xstar],"residual_inf":float(np.linalg.norm(native_rhs(float(horizon),xstar),ord=np.inf)),"pool_drift_max_abs":float(np.max(np.abs(Cpool@xstar-Cpool@y0))),"attempts":attempts},
                "analytic_jacobian_self_check":{"source_native_rhs_anchor_max_abs":rhs_anchor,"analytic_vs_complex_step_relative_Frobenius_error":jac_rel,"ceiling":jac_ceiling,"pass":bool(jac_check)},
                "condition_number_V_2":float(cond),
                "minimum_normalized_eigenvalue_separation":float(norm_sep),
                "basis_invariance_max_relative_eigenvalue_difference":basis_max,
                "FRET_observability_rank":int(obs_rank),
                "FRET_observability_singular_values":[float(x) for x in sv],
                "FRET_mode_visibility":[float(x) for x in vis],
                "eigenvalues":[{"real":float(z.real),"imag":float(z.imag)} for z in vals],
                "spectral_abscissa":float(np.max(vals.real)),
                "complex_pair_count":len(pairs),
                "FRET_visible_complex_pair_count":len(visible),
                "complex_pairs":pairs,
                "scalar_status":scalar_status
            }
            records.append(rec)
            lane_summary[lane]["contexts"][ctx_id]={
                "modal_status":modal_status,"scalar_status":scalar_status,
                "complex_pair_count":len(pairs),"visible_pair_count":len(visible),
                "FRET_observability_rank":int(obs_rank)
            }

    if any(r["status"]=="INDETERMINATE_EQUILIBRIUM" for r in records):
        modal_overall="INDETERMINATE_EQUILIBRIUM"
    elif any(r["status"]=="REFUSE_ANALYTIC_JACOBIAN_SELF_CHECK" for r in records):
        modal_overall="REFUSE_ANALYTIC_JACOBIAN_SELF_CHECK"
    elif any(r["status"]=="REFUSE_B3_MODAL_NUMERICAL_CONDITIONING" for r in records):
        modal_overall="REFUSE_B3_MODAL_NUMERICAL_CONDITIONING"
    elif all(r["status"]=="PASS_B3_GENERATOR_MODAL_QUALIFICATION" for r in records):
        modal_overall="PASS_B3_GENERATOR_MODAL_QUALIFICATION"
    else:
        modal_overall="PASS_B3_MODAL_WITH_PARTIAL_FRET_OBSERVABILITY"

    common=[]
    for ctx in [x["id"] for x in freeze["input_contexts"]]:
        p=lane_summary["primary"]["contexts"].get(ctx,{})
        s=lane_summary["sensitivity"]["contexts"].get(ctx,{})
        if isinstance(p,dict) and isinstance(s,dict) and p.get("scalar_status")=="MODEL_SPECIFIC_CHI_BIO_PAIR_FAMILY_PRESENT" and s.get("scalar_status")=="MODEL_SPECIFIC_CHI_BIO_PAIR_FAMILY_PRESENT":
            common.append(ctx)
    primary_any=any(isinstance(x,dict) and x.get("scalar_status")=="MODEL_SPECIFIC_CHI_BIO_PAIR_FAMILY_PRESENT" for x in lane_summary["primary"]["contexts"].values())
    sens_any=any(isinstance(x,dict) and x.get("scalar_status")=="MODEL_SPECIFIC_CHI_BIO_PAIR_FAMILY_PRESENT" for x in lane_summary["sensitivity"]["contexts"].values())
    if modal_overall.startswith("REFUSE") or modal_overall.startswith("INDETERMINATE"):
        scalar_overall="SCALAR_TRANSPORT_WITHHELD_UPSTREAM_MODAL_REFUSAL"
    elif common:
        scalar_overall="SCALAR_TRANSPORT_PRESENT"
    elif primary_any or sens_any:
        scalar_overall="SCALAR_TRANSPORT_PARAMETER_DEPENDENT"
    else:
        scalar_overall="SCALAR_TRANSPORT_REFUSED"

    result={
        "schema_version":"0.2","project":"Bio Chi Investigation",
        "gate":"Blum B3 analytic-Jacobian stoichiometric-subspace generator transport",
        "freeze":"BIO_CHI/config/BLUM_B3_GENERATOR_TRANSPORT_FREEZE_v0_2.json",
        "epistemic_mode":"P0-Q",
        "preserved_v01_refusal":"BIO_CHI/config/BLUM_B3_GENERATOR_TRANSPORT_V01_RESULT_PIN.json",
        "dynamic_subspace_dimension":rank,
        "modal_transport_status":modal_overall,
        "scalar_transport_status":scalar_overall,
        "common_contexts_with_FRET_visible_complex_pair_family":common,
        "lane_summary":lane_summary,"records":records,
        "broad_Bio_Chi_admitted":False,"P1_confirmation_claimed":False,
        "chi_equal_1_boundary_claimed":False,"master_scalar_created":False,
        "interpretation_limit":"P0-Q transport of generator-first scalar/modal structure after analytic-Jacobian qualification. Whole-system Bio Chi transport requires a separate realized-response/joint-meaning gate."
    }
    (OUT/"blum_b3_generator_transport_v0_2.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
