"""Frozen truth-blind Profile-I mechanics for NSD v0.2 N-B1."""
import math
import numpy as np
from scipy.optimize import minimize, minimize_scalar
from .continuous_lineage_candidate_rs import _recurrence_covariance_seed,fit_continuous_lineage_candidate_rs
from .v02_profile_coords import standardize,nuisance_from_physical,objective

GRID=np.linspace(0.05,0.98,61)
RAW_BOUND=8.0


def starts(std,fs,fit,chi,previous=None):
    out=[]
    if previous is not None:
        out.append(("continuation",np.asarray(previous,float)))
    p=fit.parameters
    g=nuisance_from_physical(p["latent_fraction"],p["natural_frequency_hz"],chi,p["g"])
    if g is not None:
        out.append(("global_projected",g))
    rec=_recurrence_covariance_seed(std,fs,1.0,45.0)
    if rec.get("status")=="SEED_READY":
        r=np.asarray(rec["raw_parameters"],float)
        out.append(("recurrence",r[[0,2,3]]))
    fn=float(p["natural_frequency_hz"])
    fixed=[(.25,max(1.2,.75*fn),-.6),(.25,fn,.6),(.55,max(1.2,.75*fn),0.0),
           (.55,min(44.0,1.25*fn),-.6),(.85,fn,.6),(.85,min(44.0,1.25*fn),0.0)]
    for i,(A,f,gval) in enumerate(fixed):
        s=nuisance_from_physical(A,f,chi,gval)
        if s is not None and np.all(np.abs(s)<=RAW_BOUND):
            out.append((f"fixed_{i}",s))
    unique=[]
    for origin,s in out:
        if not any(np.max(np.abs(s-u[1]))<1e-10 for u in unique):
            unique.append((origin,s))
    return unique


def _bound_hit(x):
    x=np.asarray(x,float)
    return bool(np.any(np.isclose(np.abs(x),RAW_BOUND,atol=1e-8)))


def _optimizer_record(origin,start,r=None,error=None):
    rec={"origin":str(origin),"initial_raw":np.asarray(start,float).tolist()}
    if error is not None:
        rec.update({"finite":False,"success":False,"status":None,"message":str(error),
                    "nll":None,"nit":None,"nfev":None,"terminal_raw":None,
                    "nuisance_bound_hit":None})
        return rec
    x=np.asarray(r.x,float)
    fun=float(r.fun)
    finite=bool(math.isfinite(fun) and fun<1e90)
    rec.update({
        "finite":finite,
        "success":bool(getattr(r,"success",False)),
        "status":int(getattr(r,"status",-1)),
        "message":str(getattr(r,"message","")),
        "nll":fun if finite else None,
        "nit":int(getattr(r,"nit",0)),
        "nfev":int(getattr(r,"nfev",0)),
        "terminal_raw":x.tolist(),
        "nuisance_bound_hit":_bound_hit(x),
    })
    return rec


def optimize_chi(std,fs,fit,chi,previous=None):
    sol=[]; runs=[]
    for origin,s in starts(std,fs,fit,chi,previous):
        try:
            r=minimize(lambda x:objective(std,fs,chi,x),s,method="L-BFGS-B",
                       bounds=[(-RAW_BOUND,RAW_BOUND)]*3,
                       options={"maxiter":80,"ftol":1e-8,"maxls":30})
            rec=_optimizer_record(origin,s,r=r)
        except Exception as exc:
            rec=_optimizer_record(origin,s,error=exc)
            runs.append(rec)
            continue
        runs.append(rec)
        if rec["finite"]:
            sol.append((origin,r))
    if not sol:
        return {"chi":float(chi),"status":"NO_FINITE_SOLUTION","nll":None,
                "optimizer_runs":runs}
    origin,best=min(sol,key=lambda z:float(z[1].fun))
    x=np.asarray(best.x,float)
    return {"chi":float(chi),"status":"FINITE","nll":float(best.fun),
            "nuisance_raw":x.tolist(),"winning_start":origin,
            "nuisance_bound_hit":_bound_hit(x),
            "optimizer_runs":runs}


def _finite_nll(row):
    value=row.get("nll")
    return value is not None and math.isfinite(float(value))


def _endpoint_candidate(row,kind):
    if not _finite_nll(row):
        return None
    return {
        "kind":kind,
        "chi":float(row["chi"]),
        "nll":float(row["nll"]),
        "success":True,
        "scalar_status":"BASE_GRID_ENDPOINT",
        "scalar_message":"endpoint candidate retained from frozen base grid",
        "scalar_nit":0,
        "scalar_nfev":0,
        "nuisance_raw":row.get("nuisance_raw"),
        "winning_start":row.get("winning_start"),
        "nuisance_bound_hit":row.get("nuisance_bound_hit"),
        "optimizer_runs":row.get("optimizer_runs",[]),
        "scalar_evaluations":[],
    }


def profile_evidence(signal,fs):
    """Return mechanical evidence; no truth parameter is accepted."""
    std=standardize(signal)
    fit=fit_continuous_lineage_candidate_rs(signal,fs,fmin_hz=1.0,fmax_hz=45.0,
        burn_in_samples=128,optimizer_maxiter=80,max_optimized_starts=18)
    fitted=float(fit.parameters["damping_ratio"])
    grid=sorted(set([float(x) for x in GRID]+[fitted]))
    rows=[]; previous=None
    for chi in grid:
        row=optimize_chi(std,fs,fit,chi,previous)
        rows.append(row)
        if row.get("nuisance_raw") is not None:
            previous=np.asarray(row["nuisance_raw"],float)

    n=np.asarray([np.nan if r["nll"] is None else float(r["nll"]) for r in rows])
    brackets=[]
    for i in range(1,len(rows)-1):
        if np.isfinite(n[i-1:i+2]).all() and n[i]<=n[i-1] and n[i]<=n[i+1]:
            brackets.append((grid[i-1],grid[i+1],"interior"))
    if np.isfinite(n[:2]).all() and n[0]<=n[1]:
        brackets.append((grid[0],grid[1],"left_endpoint_adjacent"))
    if np.isfinite(n[-2:]).all() and n[-1]<=n[-2]:
        brackets.append((grid[-2],grid[-1],"right_endpoint_adjacent"))

    refined=[]
    for lo,hi,kind in brackets:
        scalar_evaluations=[]
        def scalar_objective(z):
            detail=optimize_chi(std,fs,fit,float(z))
            scalar_evaluations.append({
                "chi":float(z),
                "status":detail.get("status"),
                "nll":detail.get("nll"),
                "winning_start":detail.get("winning_start"),
                "nuisance_bound_hit":detail.get("nuisance_bound_hit"),
                "optimizer_runs":detail.get("optimizer_runs",[]),
            })
            return 1e100 if detail.get("nll") is None else float(detail["nll"])

        r=minimize_scalar(scalar_objective,bounds=(lo,hi),method="bounded",
                          options={"xatol":1e-6,"maxiter":200})
        detail=optimize_chi(std,fs,fit,float(r.x))
        refined.append({
            "kind":kind,
            "bracket":[float(lo),float(hi)],
            "chi":float(r.x),
            "nll":float(r.fun),
            "success":bool(r.success),
            "scalar_status":int(getattr(r,"status",-1)),
            "scalar_message":str(getattr(r,"message","")),
            "scalar_nit":int(getattr(r,"nit",0)),
            "scalar_nfev":int(getattr(r,"nfev",0)),
            "nuisance_raw":detail.get("nuisance_raw"),
            "winning_start":detail.get("winning_start"),
            "nuisance_bound_hit":detail.get("nuisance_bound_hit"),
            "optimizer_runs":detail.get("optimizer_runs",[]),
            "scalar_evaluations":scalar_evaluations,
        })

    candidates=list(refined)
    left=_endpoint_candidate(rows[0],"left_endpoint")
    right=_endpoint_candidate(rows[-1],"right_endpoint")
    if left is not None:
        candidates.append(left)
    if right is not None:
        candidates.append(right)

    global_nll=float(fit.negative_log_likelihood)
    tie=1e-8*max(1.0,abs(global_nll))
    finite=[x for x in candidates if math.isfinite(float(x["nll"]))]
    best=min((float(x["nll"]) for x in finite),default=math.inf)
    tied=[x for x in finite if abs(float(x["nll"])-best)<=tie]

    fitted_rows=[r for r in rows if abs(float(r["chi"])-fitted)<=1e-12]
    fitted_row_nll=(float(fitted_rows[0]["nll"])
                    if fitted_rows and fitted_rows[0].get("nll") is not None else None)
    reproduction_tol=1e-5*max(1.0,abs(global_nll))
    reproduced=bool(fitted_row_nll is not None and
                    abs(fitted_row_nll-global_nll)<=reproduction_tol)

    return {
        "schema":"NSD_NB1_V02_PROFILE_EVIDENCE_V02",
        "truth_parameter_used_in_profile":False,
        "scientific_adjudication":"NOT_PERFORMED_BY_ENGINE",
        "fitted_chi":fitted,
        "global_nll":global_nll,
        "fit_evidence":{
            "success":bool(fit.success),
            "bic":float(fit.bic),
            "parameters":{k:float(v) for k,v in fit.parameters.items()},
            "raw_parameters":[float(v) for v in fit.raw_parameters],
            "attempted_start_count":int(fit.attempted_start_count),
            "converged_start_count":int(fit.converged_start_count),
            "optimizer_message":str(fit.optimizer_message),
            "legacy_attempted_start_count":int(fit.legacy_attempted_start_count),
            "legacy_converged_start_count":int(fit.legacy_converged_start_count),
            "legacy_best_negative_log_likelihood":float(fit.legacy_best_negative_log_likelihood),
            "legacy_best_success":bool(fit.legacy_best_success),
            "legacy_best_raw_parameters":[float(v) for v in fit.legacy_best_raw_parameters],
            "winning_start_origin":str(fit.winning_start_origin),
            "recurrence_seed_status":str(fit.recurrence_seed_status),
            "recurrence_seed_ready":bool(fit.recurrence_seed_ready),
            "recurrence_seed_start_nll":(
                None if fit.recurrence_seed_start_nll is None
                else float(fit.recurrence_seed_start_nll)
            ),
            "recurrence_seed_condition_number":(
                None if fit.recurrence_seed_condition_number is None
                else float(fit.recurrence_seed_condition_number)
            ),
        },
        "global_nll":global_nll,
        "fitted_profile_row_nll":fitted_row_nll,
        "fitted_profile_reproduction_tolerance":reproduction_tol,
        "fitted_profile_reproduced":reproduced,
        "profile_points":rows,
        "refinement_brackets":[[float(a),float(b),str(k)] for a,b,k in brackets],
        "refined_candidates":refined,
        "endpoint_candidates":[x for x in (left,right) if x is not None],
        "selection_candidates":candidates,
        "competing_global_tie_tolerance":tie,
        "unique_lowest_candidate":len(tied)==1,
        "lowest_candidate_interior":bool(
            len(tied)==1 and tied[0]["kind"] not in ("left_endpoint","right_endpoint")
            and .05<float(tied[0]["chi"])<.98
        ),
        "lowest_candidate_nuisance_bound_hit":(
            tied[0].get("nuisance_bound_hit") if len(tied)==1 else None
        ),
    }
