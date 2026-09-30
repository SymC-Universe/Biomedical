"""Frozen N-B2/N-B3 observation-only mechanics."""
import numpy as np
from scipy.linalg import expm

def schedule(fs,T=32.0):
    return np.arange(int(round(float(fs)*float(T)))+1,dtype=float)/float(fs)

def observed_recovery(A,C,x0,times):
    return np.stack([np.asarray(C)@expm(np.asarray(A)*float(t))@np.asarray(x0) for t in np.asarray(times,float)])

def io_impulse(A,B,C,times):
    return np.stack([np.asarray(C)@expm(np.asarray(A)*float(t))@np.asarray(B) for t in np.asarray(times,float)])

def relerr(a,b):
    a=np.asarray(a); b=np.asarray(b)
    return float(np.linalg.norm(a-b)/max(1.0,float(np.linalg.norm(a)),float(np.linalg.norm(b))))

def compatible(a,b,tol=1e-10):
    e=relerr(a,b)
    return bool(e<=tol),e

def recovery_classes(case_ids,observed,tol=1e-10):
    unused=list(case_ids); classes=[]
    while unused:
        a=unused.pop(0); group=[a]; rest=[]
        for b in unused:
            ok,_=compatible(observed[a],observed[b],tol)
            if ok: group.append(b)
            else: rest.append(b)
        classes.append(group); unused=rest
    return {"compatible_classes":classes,"hidden_descriptor_accessed":False,
            "scientific_adjudication":"NOT_PERFORMED_BY_ENGINE"}
