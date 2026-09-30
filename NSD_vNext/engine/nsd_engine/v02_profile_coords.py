"""Frozen coordinate helpers for NSD v0.2 N-B1 Profile-I."""
import math
import numpy as np
from .continuous_lineage_candidate import _nll
from .state_space_adequacy import _raw_fraction,_raw_frequency,_raw_rho,_frequency_from_raw

def standardize(x):
    x=np.asarray(x,float)
    if x.ndim!=1 or not np.isfinite(x).all():
        raise ValueError("signal must be finite 1-D")
    sd=float(np.std(x))
    if sd<=0 or not math.isfinite(sd):
        raise ValueError("invalid variance")
    return (x-float(np.mean(x)))/sd

def nuisance_from_physical(A,fn,chi,g):
    if not 0.0<chi<1.0:
        return None
    fd=float(fn)*math.sqrt(max(1e-15,1.0-chi*chi))
    try:
        z=np.array([_raw_fraction(float(A)),_raw_frequency(fd,1.0,45.0),
                    float(np.arctanh(np.clip(float(g),-.999999,.999999)))])
    except Exception:
        return None
    return z if np.isfinite(z).all() else None

def raw_from_nuisance(n,chi,fs):
    a,f,g=map(float,n)
    if not 0.0<chi<1.0:
        return None
    try:
        fd=_frequency_from_raw(f,1.0,45.0)
        nu=2.0*math.pi*fd
        alpha=nu*chi/math.sqrt(1.0-chi*chi)
        raw_rho=_raw_rho(math.exp(-alpha/float(fs)))
    except Exception:
        return None
    z=np.array([a,raw_rho,f,g])
    if not np.isfinite(z).all() or np.any(np.abs(z)>8.0):
        return None
    return z

def objective(std,fs,chi,nuisance):
    raw=raw_from_nuisance(nuisance,chi,fs)
    if raw is None:
        return 1e100
    value=float(_nll(std,raw,float(fs),1.0,45.0,128))
    return value if math.isfinite(value) else 1e100
