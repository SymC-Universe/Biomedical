#!/usr/bin/env python3
"""P0-D exploratory TNF operating-state spectral topology map.

Purpose: map the native Jaruszewicz-Blońska six-state NF-kB equilibrium
and complete local spectrum as the source TNF input varies. Exploratory only.
No confirmatory admission, adaptive transition fitting, or mode selection.
"""
from __future__ import annotations
import csv
import json
import pathlib
import numpy as np
import sympy as sp
from scipy.linalg import eigvals
from scipy.optimize import least_squares

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "BIO_CHI" / "artifacts" / "generated" / "jarus_tnf_spectral_topology_p0d_v01"
OUT.mkdir(parents=True, exist_ok=True)

# Exact literals from the pinned published reduced.m source.
P = {
    "kdeg": "0.000107", "k1": "0.00195", "k3": "0.00145", "k2": "0.0357",
    "a3": "0.0946", "delta": "0.108", "epsilon": "0.0428", "cdeg": "0.000106",
    "c4a": "0.00313", "a2": "0.0763", "c5a": "0.00005778",
    "i1a": "0.000595", "c3a": "0.000372",
}

ys = sp.symbols("y1:7")
u = sp.symbols("u", real=True)
y1,y2,y3,y4,y5,y6 = ys
k = {name: sp.Float(value) for name,value in P.items()}

f = sp.Matrix([
    k["kdeg"]*(1-y1)-u*k["k1"]*y1,
    u*k["k1"]*y1-(k["k3"]+k["kdeg"]+u*k["k2"]*y4)*y2,
    k["a3"]*y2*(1-y3)*k["delta"]/(y5+k["delta"])-k["i1a"]*y5*y3/(k["epsilon"]+y3),
    k["cdeg"]*(y3-y4),
    k["c4a"]*y6-k["a3"]*y5*y2*(1-y3)/(y5+k["delta"])-k["a2"]*y2*y5-k["c5a"]*y5-k["i1a"]*y5*y3/(k["epsilon"]+y3),
    k["c3a"]*(y3-y6),
])
J = f.jacobian(sp.Matrix(ys))
rf = sp.lambdify((ys,u), f, "numpy")
rJ = sp.lambdify((ys,u), J, "numpy")

def rhs(x, uu):
    return np.asarray(rf(tuple(x), uu), dtype=float).reshape(-1)

def jac_analytic(x, uu):
    return np.asarray(rJ(tuple(x), uu), dtype=float)

def jac_fd(x, uu, multiplier=1.0):
    x=np.asarray(x,float); out=np.zeros((6,6)); base=np.finfo(float).eps**(1/3)
    for j in range(6):
        h=multiplier*base*max(1.0,abs(x[j]))
        xp=x.copy(); xm=x.copy(); xp[j]+=h; xm[j]-=h
        out[:,j]=(rhs(xp,uu)-rhs(xm,uu))/(2*h)
    return out

def solve_equilibrium(uu, previous):
    if uu == 0.0:
        return np.array([1.,0.,0.,0.,0.,0.]), 0.0, 1
    seeds=[previous,np.array([1.,0.,0.,0.,0.,0.]),np.full(6,1e-3),np.full(6,0.1),np.full(6,1.0)]
    sols=[]
    for seed in seeds:
        z=least_squares(lambda q: rhs(q,uu), np.maximum(seed,0),
                        bounds=(np.zeros(6),np.full(6,np.inf)),
                        xtol=1e-14,ftol=1e-14,gtol=1e-14,max_nfev=100000)
        resid=float(np.linalg.norm(rhs(z.x,uu),np.inf))
        if z.success and resid <= 1e-9 and np.all(np.isfinite(z.x)):
            if not any(np.max(np.abs(z.x-q)/np.maximum(1,np.abs(q))) <= 1e-7 for q in sols):
                sols.append(z.x)
    if not sols:
        raise RuntimeError(f"NO_ACCEPTED_ROOT u={uu}")
    chosen=min(sols,key=lambda q:np.linalg.norm(q-previous))
    return chosen,float(np.linalg.norm(rhs(chosen,uu),np.inf)),len(sols)

def classify(uu, x, resid, n_roots):
    ja=jac_analytic(x,uu)
    ev=eigvals(ja)
    fd_checks=[]
    for m in (1.0,0.5,0.25):
        ef=eigvals(jac_fd(x,uu,m))
        fd_checks.append({
            "multiplier":m,
            "max_real":float(np.max(ef.real)),
            "nonreal_count":int(np.sum(np.abs(ef.imag)>1e-10)),
        })
    pos=sorted([e for e in ev if e.imag>1e-12],key=lambda e:abs(e.imag))
    return {
        "u":float(uu),"equilibrium":[float(v) for v in x],"residual_inf":resid,
        "accepted_root_count_from_fixed_seeds":int(n_roots),
        "max_real":float(np.max(ev.real)),
        "stable_strict":bool(np.max(ev.real)<0),
        "nonreal_count":int(np.sum(np.abs(ev.imag)>1e-12)),
        "positive_imag_count":len(pos),
        "positive_imag_modes":[
            {"real":float(e.real),"imag":float(e.imag),
             "chi_if_stable":float(-e.real/abs(e)) if e.real<0 else None}
            for e in pos
        ],
        "eigenvalues":[[float(e.real),float(e.imag)] for e in ev],
        "finite_difference_crosscheck":fd_checks,
    }

def scan(grid):
    previous=np.array([1.,0.,0.,0.,0.,0.])
    rows=[]
    for uu in grid:
        x,resid,nroots=solve_equilibrium(float(uu),previous)
        previous=x
        rows.append(classify(float(uu),x,resid,nroots))
    return rows

# Fixed grids declared before this reproducibility execution.
grids={
    "broad_0_to_1_step_0p01":np.round(np.arange(0,1.0000001,0.01),10),
    "low_0_to_0p015_step_0p0001":np.round(np.arange(0,0.0150001,0.0001),10),
    "upper_0p055_to_0p070_step_0p0001":np.round(np.arange(0.055,0.0700001,0.0001),10),
}

all_results={}
for name,grid in grids.items():
    rows=scan(grid)
    changes=[]
    for a,b in zip(rows,rows[1:]):
        if a["nonreal_count"] != b["nonreal_count"]:
            changes.append({
                "u_left":a["u"],"u_right":b["u"],
                "nonreal_left":a["nonreal_count"],"nonreal_right":b["nonreal_count"],
            })
    all_results[name]={"rows":rows,"nonreal_count_change_brackets":changes}

# Integrity checks at source endpoints.
u0=all_results["broad_0_to_1_step_0p01"]["rows"][0]
u1=all_results["broad_0_to_1_step_0p01"]["rows"][-1]
assert u0["equilibrium"] == [1.0,0.0,0.0,0.0,0.0]
assert u0["nonreal_count"] == 0
assert abs(u0["max_real"]) < 1e-14
assert u1["nonreal_count"] == 2
chi1=u1["positive_imag_modes"][0]["chi_if_stable"]
assert abs(chi1-0.21311451897468006)/0.21311451897468006 < 1e-6

result={
    "schema_version":"0.1",
    "project":"Bio Chi Investigation",
    "epistemic_class":"P0_D_EXPLORATORY_FUNCTION_LIMIT_MAPPING",
    "purpose":"Map state-dependent equilibrium and complete local spectral topology versus native TNF input without selecting a preferred mode.",
    "source_model":"Jaruszewicz-Blonska et al. reduced six-state NF-kB model",
    "source_parameter_literals":P,
    "rules":{
        "tnf_zero_equilibrium":"exact source species0 [1,0,0,0,0,0]",
        "positive_tnf_equilibrium":"nonnegative least_squares with continuation plus four fixed independent seeds",
        "residual_inf_max":1e-9,
        "jacobian_primary":"analytic symbolic differentiation of exact source equations",
        "jacobian_crosscheck":"centered finite differences at multipliers 1, 0.5, 0.25",
        "nonreal_tolerance_primary":1e-12,
        "no_adaptive_transition_search":True,
        "no_mode_selection":True,
        "no_confirmatory_claim":True,
    },
    "grids":all_results,
    "endpoint_integrity":{
        "u0_nonreal_count":u0["nonreal_count"],
        "u0_max_real":u0["max_real"],
        "u1_nonreal_count":u1["nonreal_count"],
        "u1_chi":chi1,
        "u1_expected_chi":0.21311451897468006,
    },
    "interpretation_limit":"Descriptive grid brackets and modal topology only. No bifurcation classification, biological validation, universal threshold, or broad chi admission.",
}
(OUT/"jarus_tnf_spectral_topology_p0d_v0_1.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")

with (OUT/"transition_brackets.csv").open("w",newline="",encoding="utf-8") as fh:
    w=csv.writer(fh)
    w.writerow(["grid","u_left","u_right","nonreal_left","nonreal_right"])
    for name,g in all_results.items():
        for z in g["nonreal_count_change_brackets"]:
            w.writerow([name,z["u_left"],z["u_right"],z["nonreal_left"],z["nonreal_right"]])

print(json.dumps({
    "endpoint_integrity":result["endpoint_integrity"],
    "transition_brackets":{k:v["nonreal_count_change_brackets"] for k,v in all_results.items()}
},indent=2))
print("BIO_CHI_JARUS_TNF_SPECTRAL_TOPOLOGY_P0D_PASS")
