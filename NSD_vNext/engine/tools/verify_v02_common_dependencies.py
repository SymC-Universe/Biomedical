"""Independent mechanical checks for frozen NSD v0.2 common dependencies.

This verifier is intentionally separate from the future production evaluator.
It checks only prospectively declared identities/invariances and emits no
scientific verdict.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
import numpy as np
from scipy.linalg import expm


def _root() -> Path:
    return Path(__file__).resolve().parents[3]


def _load(name: str):
    return json.loads((_root()/"NSD_vNext/control"/name).read_text(encoding="utf-8"))


def _A(s):
    w1,w2=float(s["omega1"]),float(s["omega2"])
    return np.array([
        [0.,1.,0.,0.],
        [-w1*w1,-2*float(s["zeta1"])*w1,float(s["k12"]),float(s["c12"])],
        [0.,0.,0.,1.],
        [float(s["k21"]),float(s["c21"]),-w2*w2,-2*float(s["zeta2"])*w2],
    ])


def _roots(G):
    d,V=np.linalg.eigh((G+G.T)/2)
    if d.min() <= 0:
        raise RuntimeError("metric not SPD")
    R=V@np.diag(np.sqrt(d))@V.T
    return R, V@np.diag(1/np.sqrt(d))@V.T


def _gain(A,G,t):
    R,Ri=_roots(G)
    return float(np.linalg.svd(R@expm(A*t)@Ri,compute_uv=False)[0])


def _response(A,G,x0,t):
    x=expm(A*t)@x0
    return float(np.sqrt(x@G@x)/np.sqrt(x0@G@x0))


def verify():
    reg=_load("NB23_OPERATOR_REGISTRY_CANDIDATE_v0.1.json")
    tol=_load("NB23_PACKET_APQ_REVISION_v0.1.json")["numerical_definitions"]

    # CD-02 complementary alias identity.
    t=np.arange(3073,dtype=float)/96.0
    y8=np.exp(-0.2*t)*np.cos(2*math.pi*8*t)
    y88=np.exp(-0.2*t)*np.cos(2*math.pi*88*t)
    alias_rel=float(np.linalg.norm(y8-y88)/max(1.,np.linalg.norm(y8),np.linalg.norm(y88)))
    if alias_rel > 1e-10:
        raise RuntimeError("CD-02 alias identity failed")

    # CD-04 physical-metric similarity identity, evaluated independently.
    A=_A(reg["systems"]["IO"])
    B=np.asarray(reg["B"]["BAL"],float)
    C=np.asarray(reg["C"]["CDIFF"],float)
    x0=np.asarray(reg["x0"]["BALANCED_UNIT"],float)
    G=np.eye(4)
    S=np.asarray(reg["similarity_S"],float)
    Si=np.linalg.inv(S)
    Ap=S@A@Si; Bp=S@B; Cp=C@Si; x0p=S@x0; Gp=Si.T@G@Si
    maxerr=0.0
    for tt in (0.,0.125,0.5,1.,4.,12.):
        maxerr=max(maxerr,
            abs(_gain(A,G,tt)-_gain(Ap,Gp,tt)),
            abs(_response(A,G,x0,tt)-_response(Ap,Gp,x0p,tt)),
            float(np.linalg.norm(C@expm(A*tt)@B-Cp@expm(Ap*tt)@Bp)))
    if maxerr > 1e-9:
        raise RuntimeError("CD-04 similarity identity failed")

    # C04 design-separation witness on a frozen outcome-blind probe grid.
    Abase=_A(reg["systems"]["SSBASE"])
    Ann=_A(reg["systems"]["SSNONNORMAL"])
    xb=np.asarray(reg["x0"]["BALANCED_UNIT"],float)
    probe=(0.125,0.25,0.5,1.,2.,4.,8.)
    diffs=[abs(_response(Abase,np.eye(4),xb,z)-_response(Ann,np.eye(4),xb,z)) for z in probe]
    idx=int(np.argmax(diffs))
    if diffs[idx] <= 1e-9:
        raise RuntimeError("C04 response separation witness absent on frozen probe grid")

    return {
        "status":"PASS",
        "alias96_relative_error":alias_rel,
        "similarity_probe_max_error":maxerr,
        "c04_probe_time_seconds":probe[idx],
        "c04_response_abs_difference":diffs[idx],
        "scientific_adjudication":"NOT_PERFORMED_BY_GITHUB",
        "tolerance_identity":tol,
    }


if __name__=="__main__":
    print(json.dumps(verify(),indent=2,sort_keys=True))
