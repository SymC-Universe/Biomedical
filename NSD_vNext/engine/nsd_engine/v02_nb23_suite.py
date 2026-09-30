"""Frozen NSD v0.2 N-B2/N-B3 suite construction.

Constructs operator identities from the frozen packet without evaluating
scientific targets or assigning representation/recoverability verdicts.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np

from .v02_nb23_core import second_order_matrix
from .v02_nb23_targets import transform_physical_system, period_mean_operator


def _root():
    return Path(__file__).resolve().parents[3]


def _load(name):
    return json.loads((_root()/"NSD_vNext/control"/name).read_text(encoding="utf-8"))


def frozen_registry():
    return _load("NB23_OPERATOR_REGISTRY_CANDIDATE_v0.1.json")


def frozen_suite():
    return _load("NB23_EXHAUSTIVE_SUITE_CANDIDATE_v0.1.json")


def _base_member(member, reg):
    A=second_order_matrix(reg["systems"][member["system"]])
    B=np.asarray(reg["B"][member["B"]],float)
    C=np.asarray(reg["C"][member["C"]],float)
    G=np.eye(A.shape[0]) if member["G"]=="I4" else None
    if G is None:
        raise RuntimeError("unsupported frozen metric identity")
    x0=np.asarray(reg["x0"][member["x0"]],float)
    return {"A":A,"B":B,"C":C,"G":G,"x0":x0}


def build_member(case_id):
    reg=frozen_registry(); suite=frozen_suite()
    if case_id not in suite["members"]:
        raise KeyError(case_id)
    member=suite["members"][case_id]

    if "system" in member:
        out=_base_member(member,reg)
        out.update({"case_id":case_id,"kind":"LINEAR_STATIONARY"})
        return out

    if member.get("transform"):
        source=build_member(member["source"])
        S=np.asarray(reg["similarity_S"],float)
        out=transform_physical_system(source["A"],source["B"],source["C"],source["G"],source["x0"],S)
        out.update({"case_id":case_id,"kind":"SIMILARITY_TRANSFORM","source":member["source"]})
        return out

    special=member.get("special")
    if special in ("partial_observation.stable_A","partial_observation.unstable_A"):
        key="stable_A" if special.endswith("stable_A") and "unstable" not in special else "unstable_A"
        p=reg["partial_observation"]
        A=np.asarray(p[key],float)
        return {"case_id":case_id,"kind":"PARTIAL_OBSERVATION","A":A,
                "B":None,"C":np.asarray(p["C"],float),"G":np.eye(4),
                "x0":np.asarray(p["x0"],float)}

    if special=="alias_control":
        cfg=reg["alias_control"]; f=float(member["f_hz"]); d=float(cfg["decay"])
        w=2.0*math.pi*f
        A=np.asarray([[-d,-w],[w,-d]],float)
        return {"case_id":case_id,"kind":"ALIAS_CONTROL","A":A,"B":None,
                "C":np.asarray(cfg["C"],float),"G":np.eye(2),
                "x0":np.asarray(cfg["x0"],float),"sample_rate_hz":float(cfg["sample_rate_hz"]),
                "continuous_frequency_hz":f}

    if special in ("time_varying","time_varying.surrogate"):
        cfg=reg["time_varying"]; mats=[]
        for k12,k21 in zip(cfg["k12_sequence"],cfg["k21_sequence"]):
            spec={**cfg["base"],"k12":k12,"k21":k21,"c12":0.0,"c21":0.0}
            mats.append(second_order_matrix(spec))
        Abar=period_mean_operator(mats[0],mats[1])
        if special=="time_varying.surrogate":
            return {"case_id":case_id,"kind":"STATIONARY_SURROGATE","A":Abar,
                    "B":None,"C":None,"G":np.eye(4),"x0":None}
        return {"case_id":case_id,"kind":"TIME_VARYING","A_sequence":mats,"Abar":Abar,
                "segment_seconds":float(cfg["segment_seconds"]),
                "phase_offset_seconds":float(cfg["phase_offset_seconds"]),
                "B":None,"C":None,"G":np.eye(4),"x0":None}

    if special=="misspecification":
        cfg=reg["misspecification"]
        A=second_order_matrix(reg["systems"][cfg["source_system"]])
        return {"case_id":case_id,"kind":"MISSPECIFICATION","A":A,"B":None,
                "C_linear_probe":np.asarray(reg["C"][cfg["linear_probe"]],float),
                "observation_rule":cfg["observation"],"outside_linear_observation_family":True,
                "G":np.eye(4),"x0":np.asarray(reg["x0"]["BALANCED_UNIT"],float)}

    raise RuntimeError(f"unsupported frozen suite member {case_id}")


def suite_identity_summary():
    suite=frozen_suite()
    ids=list(suite["members"])
    return {"member_count":len(ids),"case_ids":ids,
            "scientific_adjudication":"NOT_PERFORMED_BY_GITHUB"}
