"""Frozen truth-blind Profile-I mechanics for NSD v0.2 N-B1."""
import math
import numpy as np
from scipy.optimize import minimize, minimize_scalar
from .continuous_lineage_candidate_rs import _recurrence_covariance_seed,fit_continuous_lineage_candidate_rs
from .v02_profile_coords import standardize,nuisance_from_physical,objective

GRID=np.linspace(0.05,0.98,61)

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
        if s is not None and np.all(np.abs(s)<=8.0):
            out.append((f"fixed_{i}",s))
    unique=[]
    for origin,s in out:
        if not any(np.max(np.abs(s-u[1]))<1e-10 for u in unique):
            unique.append((origin,s))
    return unique

def optimize_chi(std,fs,fit,chi,previous=None):
    sol=[]
    for origin,s in starts(std,fs,fit,chi,previous):
        r=minimize(lambda x:objective(std,fs,chi,x),s,method="L-BFGS-B",
                   bounds=[(-8.0,8.0)]*3,
                   options={"maxiter":80,"ftol":1e-8,"maxls":30})
        if math.isfinite(float(r.fun)) and float(r.fun)<1e90:
            sol.append((origin,r))
    if not sol:
        return {"chi":float(chi),"status":"NO_FINITE_SOLUTION","nll":None}
    origin,best=min(sol,key=lambda z:float(z[1].fun))
    x=np.asarray(best.x,float)
    return {"chi":float(chi),"status":"FINITE","nll":float(best.fun),
            "nuisance_raw":x.tolist(),"winning_start":origin,
            "nuisance_bound_hit":bool(np.any(np.isclose(np.abs(x),8.0,atol=1e-8)))}

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
        r=minimize_scalar(lambda z:optimize_chi(std,fs,fit,float(z))["nll"] or 1e100,
                          bounds=(lo,hi),method="bounded",
                          options={"xatol":1e-6,"maxiter":200})
        detail=optimize_chi(std,fs,fit,float(r.x))
        refined.append({"kind":kind,"chi":float(r.x),"nll":float(r.fun),"success":bool(r.success),
                        "nuisance_raw":detail.get("nuisance_raw"),
                        "winning_start":detail.get("winning_start"),
                        "nuisance_bound_hit":detail.get("nuisance_bound_hit")})
    global_nll=float(fit.negative_log_likelihood)
    tie=1e-8*max(1.0,abs(global_nll))
    finite=[x for x in refined if math.isfinite(x["nll"])]
    best=min((x["nll"] for x in finite),default=math.inf)
    tied=[x for x in finite if abs(x["nll"]-best)<=tie]
    return {"schema":"NSD_NB1_V02_PROFILE_EVIDENCE_V01",
            "truth_parameter_used_in_profile":False,
            "scientific_adjudication":"NOT_PERFORMED_BY_ENGINE",
            "fitted_chi":fitted,"global_nll":global_nll,
            "profile_points":rows,"refined_candidates":refined,
            "unique_lowest_candidate":len(tied)==1,
            "lowest_candidate_interior":bool(len(tied)==1 and .05<tied[0]["chi"]<.98)}
