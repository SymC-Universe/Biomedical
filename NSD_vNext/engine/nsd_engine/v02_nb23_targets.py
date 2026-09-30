"""Frozen NSD v0.2 N-B2/N-B3 deterministic target mechanics.

Mechanical target construction only. This module emits raw target evidence and
never assigns representation sufficiency, recoverability, or scientific PASS.
"""
from __future__ import annotations

import math
import numpy as np
from scipy.linalg import expm

from .v02_nb23_core import metric_roots


def spectral_abscissa(A) -> float:
    vals = np.linalg.eigvals(np.asarray(A, float))
    return float(np.max(np.real(vals)))


def embedded_eigenvalues(A) -> np.ndarray:
    vals = np.linalg.eigvals(np.asarray(A, float))
    order = np.lexsort((np.imag(vals), np.real(vals)))
    return vals[order]


def physical_response_curve(A, G, x0, times) -> np.ndarray:
    A = np.asarray(A, float)
    G = np.asarray(G, float)
    x0 = np.asarray(x0, float).reshape(-1)
    denom = float(np.sqrt(x0 @ G @ x0))
    if not math.isfinite(denom) or denom <= 0.0:
        raise RuntimeError("invalid frozen physical initial-state norm")
    out = []
    for t in np.asarray(times, float):
        x = expm(A * float(t)) @ x0
        out.append(float(np.sqrt(x @ G @ x) / denom))
    return np.asarray(out, float)


def integrated_burden(times, response_curve) -> float:
    t = np.asarray(times, float)
    r = np.asarray(response_curve, float)
    if t.ndim != 1 or r.ndim != 1 or t.size != r.size or t.size < 2:
        raise ValueError("times and response curve must be same-length 1-D arrays")
    if not np.all(np.diff(t) > 0):
        raise ValueError("times must be strictly increasing")
    return float(np.trapezoid(r, t))


def state_impulse_curve(A, B, times) -> np.ndarray:
    A = np.asarray(A, float)
    B = np.asarray(B, float)
    return np.stack([expm(A * float(t)) @ B for t in np.asarray(times, float)])


def io_impulse_curve(A, B, C, times) -> np.ndarray:
    A = np.asarray(A, float)
    B = np.asarray(B, float)
    C = np.asarray(C, float)
    return np.stack([C @ expm(A * float(t)) @ B for t in np.asarray(times, float)])


def transform_physical_system(A, B, C, G, x0, S):
    A = np.asarray(A, float)
    B = np.asarray(B, float)
    C = np.asarray(C, float)
    G = np.asarray(G, float)
    x0 = np.asarray(x0, float)
    S = np.asarray(S, float)
    Si = np.linalg.inv(S)
    return {
        "A": S @ A @ Si,
        "B": S @ B,
        "C": C @ Si,
        "G": Si.T @ G @ Si,
        "x0": S @ x0,
    }


def _switch_index(t: float, segment_seconds: float, phase_offset_seconds: float) -> int:
    return int(math.floor((float(t) + float(phase_offset_seconds)) / float(segment_seconds))) % 2


def ordered_switch_propagator(A0, A1, segment_seconds: float, phase_offset_seconds: float, t: float) -> np.ndarray:
    """Chronological right-continuous propagator Phi(t,0) for the frozen two-state switch."""
    A = [np.asarray(A0, float), np.asarray(A1, float)]
    seg = float(segment_seconds)
    phase = float(phase_offset_seconds)
    end = float(t)
    if seg <= 0 or end < 0:
        raise ValueError("invalid switch duration/time")
    n = A[0].shape[0]
    Phi = np.eye(n)
    cur = 0.0
    while cur < end - 1e-14:
        idx = _switch_index(cur, seg, phase)
        boundary = (math.floor((cur + phase) / seg) + 1) * seg - phase
        if boundary <= cur + 1e-14:
            boundary = cur + seg
        nxt = min(end, boundary)
        Phi = expm(A[idx] * (nxt - cur)) @ Phi
        cur = nxt
    return Phi


def period_mean_operator(A0, A1) -> np.ndarray:
    """Frozen two-segment period-time-weighted mean; segment durations are equal."""
    return 0.5 * (np.asarray(A0, float) + np.asarray(A1, float))


def switching_discrepancy_curve(A0, A1, segment_seconds, phase_offset_seconds, times) -> np.ndarray:
    Abar = period_mean_operator(A0, A1)
    vals = []
    for t in np.asarray(times, float):
        Phi = ordered_switch_propagator(A0, A1, segment_seconds, phase_offset_seconds, float(t))
        vals.append(float(np.linalg.norm(Phi - expm(Abar * float(t)), 2)))
    return np.asarray(vals, float)


def physical_gain_at(A, G, t: float) -> float:
    R, Ri = metric_roots(np.asarray(G, float))
    return float(np.linalg.svd(R @ expm(np.asarray(A, float) * float(t)) @ Ri, compute_uv=False)[0])


def evidence_namespace() -> str:
    return "RAW_TARGET_EVIDENCE_ONLY"
