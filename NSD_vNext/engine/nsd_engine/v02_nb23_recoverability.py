"""Frozen observation-compatible set mechanics for NSD v0.2 N-B2/N-B3.

Compatibility is pairwise under the frozen observed-array numerical rule.
The tolerance relation is not assumed transitive, so this module does not
silently promote it to an equivalence partition.
"""
from __future__ import annotations
import numpy as np


def relative_error(a,b):
    a=np.asarray(a); b=np.asarray(b)
    return float(np.linalg.norm(a-b)/max(1.0,float(np.linalg.norm(a)),float(np.linalg.norm(b))))


def compatible(a,b,tol=1e-10):
    err=relative_error(a,b)
    return bool(err<=float(tol)),err


def compatibility_sets(case_ids,observed,tol=1e-10):
    ids=list(case_ids)
    sets={a:[] for a in ids}
    pairwise={}
    for i,a in enumerate(ids):
        for b in ids[i:]:
            ok,err=compatible(observed[a],observed[b],tol)
            pairwise[f"{a}|{b}"]={"compatible":bool(ok),"relative_error":float(err)}
            pairwise[f"{b}|{a}"]={"compatible":bool(ok),"relative_error":float(err)}
            if ok:
                sets[a].append(b)
                if b!=a:
                    sets[b].append(a)
    for a in ids:
        sets[a]=sorted(set(sets[a]))
    return {
        "compatible_sets_by_case":sets,
        "pairwise":pairwise,
        "hidden_descriptor_accessed":False,
        "scientific_adjudication":"NOT_PERFORMED_BY_ENGINE",
    }
