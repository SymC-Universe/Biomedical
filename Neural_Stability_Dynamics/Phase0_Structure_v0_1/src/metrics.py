from __future__ import annotations
import numpy as np
from scipy.optimize import linear_sum_assignment

def mac(a,b):
    a=np.asarray(a,complex).ravel(); b=np.asarray(b,complex).ravel(); den=np.vdot(a,a).real*np.vdot(b,b).real
    return np.nan if den<=0 else float(abs(np.vdot(a,b))**2/den)

def match_modes(tv,ev):
    tv=np.asarray(tv,complex); ev=np.asarray(ev,complex); cost=np.empty((len(tv),len(ev)))
    for i,t in enumerate(tv):
        for j,e in enumerate(ev): cost[i,j]=abs(t-e)/max(abs(t),1e-12)
    ri,cj=linear_sum_assignment(cost); return list(zip(ri.tolist(),cj.tolist(),cost[ri,cj].tolist()))

def pole_summary(lam):
    lam=complex(lam); decay=-lam.real; freq=abs(lam.imag)/(2*np.pi); mag=abs(lam)
    chi=decay/mag if decay>0 and mag>0 and abs(lam.imag)>1e-10 else np.nan
    return decay,freq,chi
