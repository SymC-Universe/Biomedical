from __future__ import annotations
import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.linalg import subspace_angles

def mac(a,b):
    a=np.asarray(a,complex).ravel(); b=np.asarray(b,complex).ravel()
    den=np.vdot(a,a).real*np.vdot(b,b).real
    return np.nan if den<=0 else float(abs(np.vdot(a,b))**2/den)

def match_modes(tv,ev):
    tv=np.asarray(tv,complex); ev=np.asarray(ev,complex)
    if len(tv)==0 or len(ev)==0: return []
    cost=np.empty((len(tv),len(ev)))
    for i,t in enumerate(tv):
        for j,e in enumerate(ev):
            cost[i,j]=abs(t-e)/max(abs(t),1e-12)
    ri,cj=linear_sum_assignment(cost)
    return list(zip(ri.tolist(),cj.tolist(),cost[ri,cj].tolist()))

def subspace_similarity(A,B):
    A=np.asarray(A,complex); B=np.asarray(B,complex)
    if A.ndim!=2 or B.ndim!=2 or A.shape[0]!=B.shape[0] or min(A.shape[1],B.shape[1])==0:
        return np.nan
    ang=subspace_angles(A,B)
    return float(np.mean(np.cos(ang)**2))

def pole_fields(z):
    z=complex(z)
    return {
      "real":float(z.real),
      "imag":float(z.imag),
      "frequency_hz":float(abs(z.imag)/(2*np.pi)),
      "decay_per_s":float(-z.real),
      "stable":bool(z.real<0)
    }
