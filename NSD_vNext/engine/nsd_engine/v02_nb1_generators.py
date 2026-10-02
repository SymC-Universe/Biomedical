"""Frozen NSD v0.2 N-B1 known-truth generators.

Mechanical generation only. Family labels come from the prospectively frozen
contracts; this module never infers semantic membership from fitted data.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
from pathlib import Path
import json

import numpy as np
from scipy.linalg import expm, solve_discrete_lyapunov


FS_FINE = 240.0
SECONDS = 96.0
MOD63 = (1 << 63) - 1


def _root() -> Path:
    return Path(__file__).resolve().parents[3]


def _load(name: str):
    return json.loads((_root()/"NSD_vNext/control"/name).read_text(encoding="utf-8"))


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64DXSM(int(seed)))


def _hash_seed(text: str) -> int:
    digest=hashlib.sha256(text.encode("utf-8")).digest()
    return int.from_bytes(digest[:8],"big",signed=False) % MOD63


def child_seed(parent_seed: int, truth_id: str, label: str) -> int:
    base=f"{int(parent_seed)}|{truth_id}|{label}"
    used=set()
    retry=0
    while True:
        text=base if retry==0 else f"{base}|retry|{retry}"
        seed=_hash_seed(text)
        if seed != 0 and seed not in used:
            return seed
        used.add(seed)
        retry += 1


def _sqrt_psd(M: np.ndarray) -> np.ndarray:
    vals,vecs=np.linalg.eigh(0.5*(M+M.T))
    if float(vals.min()) < -1e-9:
        raise RuntimeError(f"PSD contract violation: min eigenvalue {float(vals.min())}")
    return vecs@np.diag(np.sqrt(np.clip(vals,0,None)))@vecs.T


@dataclass(frozen=True)
class CTruth:
    A: float
    fn_hz: float
    chi: float
    g: float


def c_matrices(truth: CTruth, fs: float=FS_FINE):
    A=float(truth.A); fn=float(truth.fn_hz); chi=float(truth.chi); g=float(truth.g)
    if not (0 < A < 1 and 1 <= fn <= 45 and 0 < chi < 1 and abs(g) <= 1):
        raise RuntimeError("frozen C domain predicate failed")
    wn=2*math.pi*fn
    alpha=chi*wn
    nu=wn*math.sqrt(1-chi*chi)
    G=g*A*alpha
    D=A*(2*alpha*alpha+nu*nu)
    K=np.array([[-alpha,-1.0],[nu*nu,-alpha]],float)
    P=np.array([[A,-G],[-G,D]],float)
    Qc=-(K@P+P@K.T)
    F=expm(K/fs)
    Qd=P-F@P@F.T
    for name,M in (("P",P),("Qc",Qc),("Qd",Qd)):
        vals=np.linalg.eigvalsh(0.5*(M+M.T))
        if float(vals.min()) < -1e-9:
            raise RuntimeError(f"{name} frozen PSD contract failed")
    return K,P,Qc,F,Qd


def simulate_c(truth: CTruth, seed: int, *, fs: float=FS_FINE, seconds: float=SECONDS,
               measurement_noise: bool=True) -> np.ndarray:
    _,P,_,F,Qd=c_matrices(truth,fs)
    n=int(round(fs*seconds))
    R=rng(seed)
    x=_sqrt_psd(P)@R.normal(size=2)
    Qs=_sqrt_psd(Qd)
    obs_sd=math.sqrt(max(0.0,1.0-truth.A)) if measurement_noise else 0.0
    out=np.empty(n,float)
    for j in range(n):
        # Frozen draw order: observation draw, emit, then two process draws.
        obs=float(R.normal())
        out[j]=x[0]+obs_sd*obs
        x=F@x+Qs@R.normal(size=2)
    return out


def _rotation_transition(fn_hz: float, chi: float, fs: float) -> np.ndarray:
    wn=2*math.pi*fn_hz
    alpha=chi*wn
    nu=wn*math.sqrt(1-chi*chi)
    rho=math.exp(-alpha/fs)
    theta=nu/fs
    return rho*np.array([[math.cos(theta),-math.sin(theta)],
                         [math.sin(theta), math.cos(theta)]],float)


def _residual_q(A,rho,xi,H):
    q2=rho*rho*(1-A)
    q1=rho*((1+rho*rho)*H + xi*(A*(1+3*rho*rho)-2*(1+rho*rho)))
    q0=1+rho**4+4*rho*rho*xi*xi-2*A*rho**4-4*A*rho*rho*xi*xi-4*H*rho*rho*xi
    return q0,q1,q2


def _spectral_minimum(A,rho,xi,H):
    q0,q1,q2=_residual_q(A,rho,xi,H)
    def p(x): return 4*q2*x*x+2*q1*x+q0-2*q2
    xs=[-1.,1.]
    if q2>0:
        v=-q1/(4*q2)
        if -1 <= v <= 1: xs.append(v)
    return min(p(x) for x in xs)


def _boundary(A,rho,xi,sign,start):
    from scipy.optimize import brentq
    inside=sign*abs(start)
    outside=inside
    for _ in range(80):
        outside*=1.5
        if _spectral_minimum(A,rho,xi,outside) <= 0:
            break
    else:
        raise RuntimeError("failed to bracket S boundary")
    lo,hi=sorted((inside,outside))
    return float(brentq(lambda H:_spectral_minimum(A,rho,xi,H),lo,hi))


def _spectral_factor(A,rho,xi,H):
    q0,q1,q2=_residual_q(A,rho,xi,H)
    roots=np.roots(np.array([q2,q1,q0,q1,q2],float))
    inside=[complex(z) for z in roots if abs(z)<1-1e-8]
    if len(inside)!=2:
        inside=sorted((complex(z) for z in roots),key=abs)[:2]
    r1,r2=inside
    m1=float(np.real(-(r1+r2)))
    m2=float(np.real(r1*r2))
    sigma2=float(q2/m2)
    if sigma2 <= 0: raise RuntimeError("invalid spectral factor")
    return sigma2,m1,m2


def simulate_arma_region(*, A: float, fn_hz: float, chi: float, region: str,
                         seed: int, fs: float=FS_FINE, seconds: float=SECONDS) -> np.ndarray:
    wn=2*math.pi*fn_hz
    alpha=chi*wn
    nu=wn*math.sqrt(1-chi*chi)
    L=alpha/fs; rho=math.exp(-L); theta=nu/fs; xi=math.cos(theta)
    HC=A*L*math.sin(theta)/theta
    HD=A*math.sinh(L)
    if region=="D_NOT_C_POS": H=HC+0.5*(HD-HC)
    elif region=="D_NOT_C_NEG": H=-(HC+0.5*(HD-HC))
    elif region in ("S_NOT_D_POS","S_NOT_D_NEG"):
        Sp=_boundary(A,rho,xi,+1,HD)
        Sm=_boundary(A,rho,xi,-1,HD)
        H=0.5*(HD+Sp) if region.endswith("POS") else 0.5*(-HD+Sm)
    else: raise ValueError(region)
    sigma2,m1,m2=_spectral_factor(A,rho,xi,H)
    n=int(round(fs*seconds)); burn=int(round(5*fs)); total=n+burn
    R=rng(seed)
    eps=R.normal(0,math.sqrt(sigma2),size=total+2)
    y=np.zeros(total+2,float)
    ar1=2*rho*xi; ar2=-(rho*rho)
    for t in range(2,total+2):
        y[t]=ar1*y[t-1]+ar2*y[t-2]+eps[t]+m1*eps[t-1]+m2*eps[t-2]
    return y[burn+2:burn+2+n]


def simulate_colored_memory(parent_seed: int, truth_id: str, *, fs=FS_FINE, seconds=SECONDS):
    T=_rotation_transition(10.0,0.30,fs)
    rho=math.sqrt(abs(float(np.linalg.det(T))))
    beta=math.sqrt(max(0.0,1-rho*rho))
    phi=0.70
    Aaug=np.block([[T,beta*np.eye(2)],[np.zeros((2,2)),phi*np.eye(2)]])
    Q=np.zeros((4,4)); Q[2:,2:]=(1-phi*phi)*np.eye(2)
    P=solve_discrete_lyapunov(Aaug,Q)
    R=rng(child_seed(parent_seed,truth_id,"augmented"))
    z=_sqrt_psd(P)@R.normal(size=4)
    n=int(round(fs*seconds)); out=np.empty(n)
    sd=math.sqrt(float(P[0,0]))
    for j in range(n):
        out[j]=z[0]/sd
        noise=np.zeros(4); noise[2:]=math.sqrt(1-phi*phi)*R.normal(size=2)
        z=Aaug@z+noise
    return out


def _latent_mode(fn_hz,chi,seed,*,fs=FS_FINE,seconds=SECONDS):
    # Unit-variance latent oscillator, g=0, no measurement noise.
    wn=2*math.pi*fn_hz; alpha=chi*wn; nu=wn*math.sqrt(1-chi*chi)
    K=np.array([[-alpha,-1.0],[nu*nu,-alpha]],float)
    P=np.array([[1.0,0.0],[0.0,2*alpha*alpha+nu*nu]],float)
    F=expm(K/fs); Qd=P-F@P@F.T
    R=rng(seed); x=_sqrt_psd(P)@R.normal(size=2); Qs=_sqrt_psd(Qd)
    n=int(round(fs*seconds)); out=np.empty(n)
    for j in range(n):
        out[j]=x[0]
        x=F@x+Qs@R.normal(size=2)
    return out


def simulate_two_mode(parent_seed,truth_id,*,reference_mix=False,fs=FS_FINE,seconds=SECONDS):
    a=_latent_mode(10.0,0.25,child_seed(parent_seed,truth_id,"mode1"),fs=fs,seconds=seconds)
    b=_latent_mode(20.0,0.35,child_seed(parent_seed,truth_id,"mode2"),fs=fs,seconds=seconds)
    R=rng(child_seed(parent_seed,truth_id,"obs"))
    eps=R.normal(size=a.size)
    if reference_mix:
        m=(a+0.35*b)/math.sqrt(1+0.35**2)
        return math.sqrt(0.8)*m+math.sqrt(0.2)*eps
    return math.sqrt(0.4)*a+math.sqrt(0.4)*b+math.sqrt(0.2)*eps


def simulate_piecewise(parent_seed,truth_id,*,fs=FS_FINE,seconds=SECONDS):
    if seconds != 96.0 or fs != 240.0:
        raise RuntimeError("L07 is frozen to 240 Hz and 96 s")
    t1=CTruth(.72,9.0,.28,.20); t2=CTruth(.72,17.0,.52,-.35)
    _,P1,_,F1,Q1=c_matrices(t1,fs); _,_,_,F2,Q2=c_matrices(t2,fs)
    Rp=rng(child_seed(parent_seed,truth_id,"process"))
    Ro=rng(child_seed(parent_seed,truth_id,"obs"))
    x=_sqrt_psd(P1)@Rp.normal(size=2)
    q1=_sqrt_psd(Q1); q2=_sqrt_psd(Q2)
    n=int(fs*seconds); cut=int(fs*48); out=np.empty(n)
    obs_sd=math.sqrt(.28)
    for j in range(n):
        out[j]=x[0]+obs_sd*Ro.normal()
        if j < cut-1: x=F1@x+q1@Rp.normal(size=2)
        else: x=F2@x+q2@Rp.normal(size=2)
    return out


def simulate_ar1(seed,phi=.86,*,fs=FS_FINE,seconds=SECONDS):
    R=rng(seed); n=int(round(fs*seconds)); y=np.empty(n)
    y[0]=R.normal(); sd=math.sqrt(1-phi*phi)
    for j in range(1,n): y[j]=phi*y[j-1]+sd*R.normal()
    return y


@dataclass
class GeneratedTruth:
    truth_id: str
    generator: str
    fine: np.ndarray
    observations: dict[str,np.ndarray]


def generate_truth(truth: dict, parent_seed: int) -> GeneratedTruth:
    tid=truth["id"]; gen=truth["generator"]
    obs={}
    if gen in ("CONTINUOUS_C","CONTINUOUS_C_GAIN_CONTROL"):
        tr=CTruth(float(truth["A"]),float(truth["fn_hz"]),float(truth["chi"]),float(truth["g"]))
        fine=simulate_c(tr,parent_seed)
        if gen=="CONTINUOUS_C_GAIN_CONTROL":
            obs={"gain_0.7":0.7*fine,"gain_1.4":1.4*fine}
    elif gen in ("D_NOT_C_POS","D_NOT_C_NEG","S_NOT_D_POS","S_NOT_D_NEG"):
        fine=simulate_arma_region(A=float(truth["base_A"]),fn_hz=float(truth["base_fn_hz"]),
                                  chi=float(truth["base_chi"]),region=gen,seed=parent_seed)
    elif gen=="COLORED_MEMORY":
        fine=simulate_colored_memory(parent_seed,tid)
    elif gen=="GENUINE_TWO_MODE":
        fine=simulate_two_mode(parent_seed,tid)
    elif gen=="PIECEWISE_C_REORGANIZATION":
        fine=simulate_piecewise(parent_seed,tid)
    elif gen=="AR1_NONOSCILLATORY":
        fine=simulate_ar1(parent_seed,float(truth["phi"]))
    elif gen=="REFERENCE_MIXTURE_TWO_MODE":
        fine=simulate_two_mode(parent_seed,tid,reference_mix=True)
    else:
        raise ValueError(f"unsupported frozen generator {gen}")
    if fine.size != 23040:
        raise RuntimeError("frozen fine sample count mismatch")
    return GeneratedTruth(tid,gen,fine,obs)


def coarse_from_fine(fine: np.ndarray) -> np.ndarray:
    fine=np.asarray(fine,float)
    if fine.size != 23040:
        raise RuntimeError("fine record must contain exactly 23040 samples")
    out=fine[::2]
    if out.size != 11520:
        raise RuntimeError("coarse record sample count mismatch")
    return out
