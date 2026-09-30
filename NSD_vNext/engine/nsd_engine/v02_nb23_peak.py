"""Certified frozen NSD v0.2 finite-time peak mechanics.

Implements the prospectively frozen interval branch-and-bound certificate for
physical-metric propagator gain. The code returns numerical evidence only and
never assigns a scientific verdict.
"""
from __future__ import annotations

from dataclasses import dataclass
import heapq
import math
import numpy as np
from scipy.linalg import expm

from .v02_nb23_core import metric_roots
from .v02_nb23_targets import ordered_switch_propagator


class PeakCertificationError(RuntimeError):
    pass


@dataclass
class _Interval:
    a: float
    b: float
    ga: float
    gb: float
    upper: float


def _mu2(M):
    H=0.5*(M+M.T)
    return float(np.max(np.linalg.eigvalsh(H)))


def _gain(E):
    return float(np.linalg.svd(E,compute_uv=False)[0])


def _interval_upper(Ea,Eb,M,h):
    mu_f=max(0.0,_mu2(M)); mu_b=max(0.0,_mu2(-M))
    left=float(np.linalg.norm(M@Ea,2))*math.exp(mu_f*h)
    right=float(np.linalg.norm(M@Eb,2))*math.exp(mu_b*h)
    return float(min(_gain(Ea)+left*h,_gain(Eb)+right*h))


def _branch_and_bound(make_E, interval_M, partitions, rel_tol=1e-9, tie_rel=1e-9, max_intervals=200000):
    heap=[]; cache={}; serial=0; lower=-math.inf
    def E(t):
        key=float(t)
        if key not in cache:
            cache[key]=np.asarray(make_E(key),float)
        return cache[key]
    for a,b in partitions:
        Ea,Eb=E(a),E(b); ga,gb=_gain(Ea),_gain(Eb); lower=max(lower,ga,gb)
        M=np.asarray(interval_M(a,b),float); ub=_interval_upper(Ea,Eb,M,b-a)
        heapq.heappush(heap,(-ub,serial,_Interval(float(a),float(b),ga,gb,ub))); serial+=1
    splits=0
    while heap:
        max_upper=-heap[0][0]
        tol=float(rel_tol)*max(1.0,abs(lower))
        if max_upper-lower<=tol:
            break
        if len(heap)+splits>=int(max_intervals):
            raise PeakCertificationError("interval budget exhausted before frozen peak tolerance")
        _,_,iv=heapq.heappop(heap)
        mid=0.5*(iv.a+iv.b); Em=E(mid); gm=_gain(Em); lower=max(lower,gm)
        for a,b,ga,gb in ((iv.a,mid,iv.ga,gm),(mid,iv.b,gm,iv.gb)):
            Ea,Eb=E(a),E(b); M=np.asarray(interval_M(a,b),float)
            ub=_interval_upper(Ea,Eb,M,b-a)
            heapq.heappush(heap,(-ub,serial,_Interval(a,b,ga,gb,ub))); serial+=1
        splits+=1
    max_upper=max((-x[0] for x in heap),default=lower)
    tie=float(tie_rel)*max(1.0,abs(lower))
    intervals=sorted([[x[2].a,x[2].b] for x in heap if x[2].upper>=lower-tie])
    return {"lower":float(lower),"upper":float(max_upper),
            "relative_gap":float((max_upper-lower)/max(1.0,abs(lower))),
            "argmax_intervals":intervals,"evaluated_times":len(cache),"split_count":splits,
            "scientific_adjudication":"NOT_PERFORMED_BY_GITHUB"}


def certified_stationary_peak(A,G,horizon=32.0,rel_tol=1e-9,tie_rel=1e-9,max_intervals=200000):
    A=np.asarray(A,float); G=np.asarray(G,float); R,Ri=metric_roots(G); M=R@A@Ri
    out=_branch_and_bound(lambda t:expm(M*float(t)),lambda a,b:M,[(0.0,float(horizon))],
                          rel_tol=rel_tol,tie_rel=tie_rel,max_intervals=max_intervals)
    out["kind"]="STATIONARY_PHYSICAL_GAIN"
    return out


def switch_boundaries(segment_seconds,phase_offset_seconds,horizon):
    seg=float(segment_seconds); phase=float(phase_offset_seconds); T=float(horizon)
    if seg<=0 or T<0: raise ValueError("invalid switch contract")
    pts=[0.0,T]; k=math.floor(phase/seg)
    while True:
        b=(k+1)*seg-phase
        if b>T: break
        if b>0: pts.append(float(b))
        k+=1
    return sorted(set(pts))


def certified_switched_peak(A0,A1,G,segment_seconds,phase_offset_seconds,horizon=32.0,
                            rel_tol=1e-9,tie_rel=1e-9,max_intervals=200000):
    A0=np.asarray(A0,float); A1=np.asarray(A1,float); G=np.asarray(G,float)
    R,Ri=metric_roots(G); M=[R@A0@Ri,R@A1@Ri]
    def make_E(t):
        return R@ordered_switch_propagator(A0,A1,float(segment_seconds),float(phase_offset_seconds),float(t))@Ri
    def active_M(a,b):
        mid=0.5*(float(a)+float(b))
        idx=int(math.floor((mid+float(phase_offset_seconds))/float(segment_seconds)))%2
        return M[idx]
    pts=switch_boundaries(segment_seconds,phase_offset_seconds,horizon)
    out=_branch_and_bound(make_E,active_M,list(zip(pts[:-1],pts[1:])),
                          rel_tol=rel_tol,tie_rel=tie_rel,max_intervals=max_intervals)
    out["kind"]="SWITCHED_PHYSICAL_GAIN"; out["switch_partitions"]=list(zip(pts[:-1],pts[1:]))
    return out
