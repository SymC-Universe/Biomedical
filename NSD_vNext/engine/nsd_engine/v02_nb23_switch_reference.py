"""Independent non-confirmatory reference for frozen NSD v0.2 switched discrepancy.

This module intentionally does not call the production certificate or its
branch-and-bound state. It provides dense/high-resolution fixture evidence
only and emits no scientific verdict.
"""
from __future__ import annotations
import math
import numpy as np
from scipy.linalg import expm


def reference_ordered_switch_propagator(A0,A1,segment_seconds,phase_offset_seconds,t):
    A0=np.asarray(A0,float); A1=np.asarray(A1,float)
    seg=float(segment_seconds); phase=float(phase_offset_seconds); end=float(t)
    if seg<=0 or end<0:
        raise ValueError("invalid switch duration/time")
    if A0.shape!=A1.shape or A0.ndim!=2 or A0.shape[0]!=A0.shape[1]:
        raise ValueError("generator shape mismatch")
    Phi=np.eye(A0.shape[0])
    cur=0.0
    while cur<end-1e-14:
        idx=int(math.floor((cur+phase)/seg))%2
        next_boundary=(math.floor((cur+phase)/seg)+1)*seg-phase
        if next_boundary<=cur+1e-14:
            next_boundary=cur+seg
        nxt=min(end,next_boundary)
        A=A0 if idx==0 else A1
        Phi=expm(A*(nxt-cur))@Phi
        cur=nxt
    return Phi


def dense_switching_discrepancy_reference(
    A0,A1,segment_seconds,phase_offset_seconds,horizon=2.0,samples=20001
):
    A0=np.asarray(A0,float); A1=np.asarray(A1,float)
    Abar=0.5*(A0+A1)
    times=np.linspace(0.0,float(horizon),int(samples))
    vals=np.empty(times.size,float)
    for i,t in enumerate(times):
        Phi=reference_ordered_switch_propagator(
            A0,A1,segment_seconds,phase_offset_seconds,float(t)
        )
        vals[i]=float(np.linalg.norm(Phi-expm(Abar*float(t)),2))
    j=int(np.argmax(vals))
    return {
        "times":times,
        "values":vals,
        "maximum":float(vals[j]),
        "argmax_time":float(times[j]),
        "verdict_namespace":"NUMERICAL_REFERENCE_ONLY",
        "scientific_adjudication":"NOT_PERFORMED_BY_REFERENCE",
    }
