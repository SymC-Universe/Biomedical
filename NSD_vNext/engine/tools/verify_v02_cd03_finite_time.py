"""Independent CD-03 finite-time reference checks for frozen NSD v0.2."""
import json, math
from pathlib import Path
import numpy as np
from scipy.linalg import expm


def root():
    return Path(__file__).resolve().parents[3]


def load(name):
    return json.loads((root()/"NSD_vNext/control"/name).read_text())


def A(spec):
    w1,w2=float(spec["omega1"]),float(spec["omega2"])
    return np.array([[0,1,0,0],[-w1*w1,-2*spec["zeta1"]*w1,spec["k12"],spec["c12"]],
                     [0,0,0,1],[spec["k21"],spec["c21"],-w2*w2,-2*spec["zeta2"]*w2]],float)


def gain(M,t):
    return float(np.linalg.svd(expm(M*t),compute_uv=False)[0])


def response(M,x,t):
    y=expm(M*t)@x
    return float(np.linalg.norm(y)/np.linalg.norm(x))


def switched(reg,t):
    cfg=reg["time_varying"]; mats=[]
    for k12,k21 in zip(cfg["k12_sequence"],cfg["k21_sequence"]):
        mats.append(A({**cfg["base"],"k12":k12,"k21":k21,"c12":0.0,"c21":0.0}))
    seg=float(cfg["segment_seconds"]); phase=float(cfg["phase_offset_seconds"])
    cur=0.0; Phi=np.eye(4)
    while cur < t-1e-14:
        idx=int(math.floor((cur+phase)/seg))%2
        boundary=(math.floor((cur+phase)/seg)+1)*seg-phase
        nxt=min(t,boundary if boundary>cur+1e-14 else cur+seg)
        Phi=expm(mats[idx]*(nxt-cur))@Phi
        cur=nxt
    return Phi,mats


def verify():
    reg=load("NB23_OPERATOR_REGISTRY_CANDIDATE_v0.1.json")
    xb=np.asarray(reg["x0"]["BALANCED_UNIT"],float)
    base=A(reg["systems"]["SSBASE"]); nn=A(reg["systems"]["SSNONNORMAL"])
    ts=np.linspace(0,32,4097)
    gb=np.array([gain(base,float(t)) for t in ts])
    gn=np.array([gain(nn,float(t)) for t in ts])
    rb=np.array([response(base,xb,float(t)) for t in ts])
    rn=np.array([response(nn,xb,float(t)) for t in ts])
    pb,pn=float(gb.max()),float(gn.max())
    ib,inon=float(np.trapezoid(rb,ts)),float(np.trapezoid(rn,ts))
    if abs(pb-pn) <= 1e-9*max(1,abs(pb),abs(pn)):
        raise RuntimeError("C04 dense-reference peak separation absent")
    if abs(ib-inon) <= 1e-9*max(1,abs(ib),abs(inon)):
        raise RuntimeError("C04 dense-reference burden separation absent")

    cfg=reg["time_varying"]
    b=float(cfg["segment_seconds"])-float(cfg["phase_offset_seconds"])
    Phi,mats=switched(reg,b+0.25)
    ref=expm(mats[1]*0.25)@expm(mats[0]*b)
    err=float(np.linalg.norm(Phi-ref))
    if err > 1e-10:
        raise RuntimeError("ordered switching reference mismatch")
    return {"status":"PASS","c04_base_peak":pb,"c04_nonnormal_peak":pn,
            "c04_base_burden":ib,"c04_nonnormal_burden":inon,
            "switch_reference_error":err,
            "scientific_adjudication":"NOT_PERFORMED_BY_GITHUB"}


if __name__=="__main__":
    print(json.dumps(verify(),indent=2,sort_keys=True))
