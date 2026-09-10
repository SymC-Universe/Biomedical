from __future__ import annotations
import numpy as np
from scipy.optimize import linear_sum_assignment
from .selector import mac, pole_distance


def track_modes(vals_a, shapes_a, vals_b, shapes_b, min_hz=0.0):
    """P0 unequal-order bookkeeping with no frozen scientific thresholds.

    Returns best one-to-one assignments plus unmatched modes. Ambiguity must be
    adjudicated by a later uncertainty-aware rule and is therefore preserved.
    """
    va = np.asarray(vals_a, complex)
    vb = np.asarray(vals_b, complex)
    sa = np.asarray(shapes_a, complex)
    sb = np.asarray(shapes_b, complex)
    ia = np.where(va.imag / (2 * np.pi) >= float(min_hz))[0]
    ib = np.where(vb.imag / (2 * np.pi) >= float(min_hz))[0]
    if len(ia) == 0 or len(ib) == 0:
        return {"status":"ORDER_CHANGE_UNRESOLVED","shared":[],"lost":ia.tolist(),"added":ib.tolist()}
    cost = np.empty((len(ia), len(ib)), float)
    meta = {}
    for r, i in enumerate(ia):
        for c, j in enumerate(ib):
            d = pole_distance(va[i], vb[j])
            m = mac(sa[:, i], sb[:, j])
            m = 0.0 if not np.isfinite(m) else m
            cost[r, c] = d + (1.0 - m)
            meta[(r,c)] = (d,m)
    rr, cc = linear_sum_assignment(cost)
    shared=[]
    used_a=set(); used_b=set()
    for r,c in zip(rr,cc):
        i,j=int(ia[r]),int(ib[c]); d,m=meta[(r,c)]
        shared.append({"a_index":i,"b_index":j,"pole_distance":float(d),"MAC":float(m),"status":"CANDIDATE_SHARED_NOT_ADJUDICATED"})
        used_a.add(i); used_b.add(j)
    lost=[int(i) for i in ia if int(i) not in used_a]
    added=[int(j) for j in ib if int(j) not in used_b]
    return {"status":"P0_ASSIGNMENT_NOT_ADJUDICATED","shared":shared,"lost":lost,"added":added}
