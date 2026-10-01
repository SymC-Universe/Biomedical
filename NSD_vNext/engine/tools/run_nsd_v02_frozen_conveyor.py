#!/usr/bin/env python3
"""Frozen NSD v0.2 evidence conveyor.

GitHub execution only: generate frozen evidence, checkpoint, hash, resume, and
stop at SCIENTIFIC_REVIEW_READY. Scientific adjudication is intentionally
outside this runner.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
from typing import Any

import numpy as np
import scipy

HERE=Path(__file__).resolve()
ENGINE_ROOT=HERE.parents[1]
NSD_ROOT=HERE.parents[2]
REPO_ROOT=HERE.parents[3]
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0,str(ENGINE_ROOT))

from nsd_engine.v02_frozen_contract import validate_frozen_science,git_blob_sha,FrozenContractError
from nsd_engine.v02_nb1_generators import generate_truth,coarse_from_fine
from nsd_engine.v02_nb1_profile import profile_evidence
from nsd_engine.v02_nb23_suite import build_member,frozen_suite
from nsd_engine.v02_nb23_targets import (
    spectral_abscissa,embedded_eigenvalues,physical_response_curve,
    integrated_burden,state_impulse_curve,io_impulse_curve,
    ordered_switch_propagator,switching_discrepancy_curve,
)
from nsd_engine.v02_nb23_peak import (
    certified_stationary_peak,certified_switching_discrepancy_max
)
from nsd_engine.v02_nb23_observation import schedule,observed_recovery
from nsd_engine.v02_nb23_recoverability import compatibility_sets

CONTROL=NSD_ROOT/"control"
RESULTS=NSD_ROOT/"results"/"v0_2_frozen"
NB1_DIR=RESULTS/"nb1"
NB23_DIR=RESULTS/"nb23"
MANIFEST=RESULTS/"evidence_manifest.json"
AUTHORITY=CONTROL/"V0_2_EXECUTION_AUTHORITY_v0.1.json"
ORDER=CONTROL/"V0_2_EXECUTION_CASE_ORDER_v0.1.json"
FINAL_ID=CONTROL/"V0_2_FINAL_CODE_IDENTITY_v0.1.json"
NB1_CP=CONTROL/"V0_2_RUNTIME_CHECKPOINT_NB1_v0.1.json"
NB23_CP=CONTROL/"V0_2_RUNTIME_CHECKPOINT_NB23_v0.1.json"

START=time.time()
RUNTIME_MIN=330
RESERVE_MIN=15
COMMIT_EVERY=4


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path,obj: Any) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8")


def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()


def env_record() -> dict[str,Any]:
    return {
        "python":platform.python_version(),
        "numpy":np.__version__,
        "scipy":scipy.__version__,
        "platform":platform.platform(),
        "architecture":platform.machine(),
        "github_run_id":os.environ.get("GITHUB_RUN_ID"),
        "github_run_attempt":os.environ.get("GITHUB_RUN_ATTEMPT"),
        "github_sha":os.environ.get("GITHUB_SHA"),
    }


def cpx(z: complex) -> dict[str,float]:
    return {"real":float(np.real(z)),"imag":float(np.imag(z))}


def json_array(x):
    return np.asarray(x).tolist()


def authority() -> dict[str,Any]:
    return load(AUTHORITY)


def final_identity() -> dict[str,Any]:
    return load(FINAL_ID)


def validate_final_identity() -> dict[str,Any]:
    ident=final_identity()
    if ident.get("status")!="FINAL_IMPLEMENTATION_IDENTITY_BOUND_PREEXECUTION":
        raise FrozenContractError("final implementation identity not bound")
    for row in ident["scientific_code_files"]:
        p=REPO_ROOT/row["path"]
        if not p.exists():
            raise FrozenContractError(f"missing bound code file {row['path']}")
        observed=git_blob_sha(p)
        if observed!=row["blob"]:
            raise FrozenContractError(
                f"FROZEN_CONTRACT_VIOLATION: {row['path']} blob {observed} != {row['blob']}"
            )
    versions=ident["runtime_dependencies"]
    observed={
        "python":platform.python_version(),
        "numpy":np.__version__,
        "scipy":scipy.__version__,
    }
    for k,v in observed.items():
        if str(versions[k])!=str(v):
            raise FrozenContractError(f"runtime identity mismatch {k}: {v} != {versions[k]}")
    return ident


def preflight() -> dict[str,Any]:
    sci=validate_frozen_science(REPO_ROOT)
    ident=validate_final_identity()
    order=load(ORDER)
    if order["scientific_baseline"]!="NSD-V02-B01-FROZEN":
        raise FrozenContractError("case order baseline mismatch")
    if len(order["nb1_case_ids"])!=order["nb1_case_count"]:
        raise FrozenContractError("N-B1 case order count mismatch")
    if len(order["nb23_case_ids"])!=order["nb23_case_count"]:
        raise FrozenContractError("N-B2/N-B3 case order count mismatch")
    if len(set(order["nb1_case_ids"]))!=len(order["nb1_case_ids"]):
        raise FrozenContractError("duplicate N-B1 case identity")
    if len(set(order["nb23_case_ids"]))!=len(order["nb23_case_ids"]):
        raise FrozenContractError("duplicate N-B2/N-B3 case identity")
    return {
        "status":"PREFLIGHT_PASS",
        "scientific_contract":sci,
        "final_identity_status":ident["status"],
        "nb1_case_count":order["nb1_case_count"],
        "nb23_case_count":order["nb23_case_count"],
        "scientific_outcomes_opened":False,
        "scientific_adjudication":"NOT_PERFORMED_BY_GITHUB",
        "environment":env_record(),
    }


def git_checkpoint(message: str) -> None:
    if os.environ.get("GITHUB_ACTIONS")!="true":
        return
    paths=[]
    for p in (NB1_CP,NB23_CP,RESULTS):
        if p.exists():
            paths.append(str(p.relative_to(REPO_ROOT)))
    if not paths:
        return
    subprocess.run(["git","add","--"]+paths,cwd=REPO_ROOT,check=True)
    staged=subprocess.run(["git","diff","--cached","--quiet"],cwd=REPO_ROOT)
    if staged.returncode==0:
        return
    subprocess.run(["git","commit","-m",message],cwd=REPO_ROOT,check=True)
    subprocess.run(
        ["git","push","origin","HEAD:nsd-rebuild-gom-v0.8.0"],
        cwd=REPO_ROOT,check=True
    )


def runtime_reserve() -> bool:
    return (time.time()-START)/60.0 >= RUNTIME_MIN-RESERVE_MIN


def checkpoint_identity(lane: str,completed:list[str],all_ids:list[str],next_action:str,state="ACTIVE_COMPUTE"):
    ident=final_identity(); auth=authority()
    output=ident["evidence_schema_blobs"]["nb1" if lane=="N-B1" else "nb23"]
    rng=ident["rng"]["nb1"] if lane=="N-B1" else {
        "primary":"NOT_APPLICABLE_DETERMINISTIC_NOISELESS"
    }
    return {
        "schema":"NSD_LANE_CHECKPOINT_V0_2_FROZEN_V0_2",
        "parent_identity_manifest":{
            "path":"NSD_vNext/control/V0_2_FINAL_CODE_IDENTITY_v0.1.json",
            "blob":auth["final_code_identity"]["blob"],
        },
        "lane":lane,
        "state":state,
        "queue_order_identity":ident["queue_identity"],
        "completed_work_cursor":{"count":len(completed)},
        "case_set_digest":ident["case_sets"]["nb1" if lane=="N-B1" else "nb23"],
        "authority_plan_blob":ident["final_architecture_blobs"]["nb1" if lane=="N-B1" else "nb23"],
        "packet_blob":ident["packet_blobs"]["nb1" if lane=="N-B1" else "nb23"],
        "config_blob":ident["config_blobs"]["nb1" if lane=="N-B1" else "nb23"],
        "code_manifest_blob":auth["final_code_identity"]["blob"],
        "dependency_identity":ident["runtime_dependencies"],
        "environment_identity":ident["environment"],
        "rng_identity":rng,
        "output_schema_identity":output,
        "completed_case_ids":completed,
        "completed_artifact_hashes":{},
        "incomplete_case_ids":[x for x in all_ids if x not in set(completed)],
        "active_run_id":int(os.environ["GITHUB_RUN_ID"]) if os.environ.get("GITHUB_RUN_ID") else None,
        "next_exact_action":next_action,
        "stop_reason":None,
        "scientific_values_exposed":bool(completed),
        "mismatch_policy":"FROZEN_CONTRACT_VIOLATION",
    }


def read_completed(path:Path)->list[str]:
    if not path.exists():
        return []
    return list(load(path).get("completed_case_ids",[]))


def nb1_tasks():
    f=load(CONTROL/"NB1_PACKET_FUNCTION_TRUTHS_v0.1.json")["truths"]
    l=load(CONTROL/"NB1_PACKET_LIMIT_TRUTHS_v0.1.json")["truths"]
    seeds=load(CONTROL/"NB1_PACKET_SEEDS_v0.2.json")["seeds"]
    truth_by_id={x["id"]:x for x in f+l}
    tasks={}
    for truth in f+l:
        obs=["gain_0.7","gain_1.4"] if truth["id"]=="NB1B01-F09" else ["native"]
        for i,seed in enumerate(seeds):
            for o in obs:
                for rate in ("fine_240","coarse_120"):
                    cid=f"{truth['id']}__r{i:02d}__{o}__{rate}"
                    tasks[cid]=(truth,i,int(seed),o,rate)
    return tasks


def nb1_row(cid,task):
    truth,replicate,parent_seed,obs_label,rate=task
    generated=generate_truth(truth,parent_seed)
    if obs_label=="native":
        fine=generated.fine
        obs_contract={"label":"native","transform":"identity"}
    else:
        fine=generated.observations[obs_label]
        obs_contract={
            "label":obs_label,
            "transform":"positive_scalar_gain",
            "gain":float(obs_label.split("_")[1]),
        }
    if rate=="fine_240":
        signal=np.asarray(fine,float); fs=240.0
    else:
        signal=coarse_from_fine(fine); fs=120.0
    prof=profile_evidence(signal,fs)
    fit=prof["fit_evidence"]
    time_homogeneous=truth["generator"]!="PIECEWISE_C_REORGANIZATION"
    path=f"NSD_vNext/results/v0_2_frozen/nb1/{cid}.json"
    return {
        "schema":"NSD_NB1_V0_2_EVIDENCE_ROW_V0_2",
        "packet_id":"NB1-B01-EXACT-PREQ-V03",
        "authority_identity":{"scientific_baseline":"NSD-V02-B01-FROZEN"},
        "truth_identity":truth,
        "generator_contract":{"generator":truth["generator"],"known_truth_only":True},
        "seed_identity":{
            "replicate_index":replicate,
            "parent_seed_decimal":str(parent_seed),
            "rng":"PCG64DXSM",
        },
        "sampling_contract":{
            "rate_label":rate,"sampling_rate_hz":fs,
            "sample_count":int(signal.size),
            "same_generated_fine_path":True,
            "coarse_transform":"y120[j]=y240[2j]" if fs==120 else "native 240-Hz fine path",
        },
        "observation_contract":obs_contract,
        "channel_inputs":{
            "generator_identity":truth["generator"],
            "time_homogeneous_full_record_law":time_homogeneous,
            "sampling_same_path":True,
            "candidate_frequency_domain_hz":[1,45],
            "coarsest_nyquist_hz":60,
            "reference_channel_applicable":truth["id"] in ("NB1B01-F09","NB1B01-L09"),
        },
        "raw_evidence":{
            "mean":float(np.mean(signal)),
            "std":float(np.std(signal)),
            "fit":fit,
        },
        "search_integrity_evidence":{
            "winning_start_origin":fit["winning_start_origin"],
            "attempted_start_count":fit["attempted_start_count"],
            "converged_start_count":fit["converged_start_count"],
            "recurrence_seed_status":fit["recurrence_seed_status"],
        },
        "profile_evidence":prof,
        "paired_rate_evidence":None,
        "failure_record":None,
        "artifact_identity":{"path":path},
        "environment":env_record(),
        "scientific_adjudication":"NOT_PERFORMED_BY_GITHUB",
        "licenses_real_eeg_local_chi":False,
    }


def representation_contract(case_id:str):
    suite=frozen_suite()
    eq=[e["id"] for e in suite.get("equivalence_classes",[]) if case_id in e.get("members",[])]
    targets=load(CONTROL/"NB23_TARGET_AND_CONTRAST_CANDIDATE_v0.1.json")
    contrasts=[c["id"] for c in targets["contrasts"] if case_id in c.get("members",[])]
    return {"equivalence_classes":eq,"contrasts":contrasts}


def operator_identity(member:dict,hidden=False):
    if hidden:
        return {"hidden_descriptor_accessed":False}
    out={"kind":member["kind"]}
    for key in ("A","A_sequence","Abar","B","C","G","x0","C_linear_probe"):
        if key in member and member[key] is not None:
            out[key]=json_array(member[key])
    for key in ("segment_seconds","phase_offset_seconds","sample_rate_hz","continuous_frequency_hz"):
        if key in member:
            out[key]=member[key]
    if "observation_rule" in member:
        out["observation_rule"]=member["observation_rule"]
    return out


def exact_target_evidence(case_id,member):
    T=32.0; times=np.linspace(0.0,T,4097)
    out={}
    numerical={}
    kind=member["kind"]
    if kind=="TIME_VARYING":
        A0,A1=member["A_sequence"]
        props=[
            ordered_switch_propagator(
                A0,A1,member["segment_seconds"],member["phase_offset_seconds"],float(t)
            ) for t in times
        ]
        disc=switching_discrepancy_curve(
            A0,A1,member["segment_seconds"],member["phase_offset_seconds"],times
        )
        cert=certified_switching_discrepancy_max(
            A0,A1,member["G"],member["segment_seconds"],member["phase_offset_seconds"],
            horizon=T,rel_tol=1e-9,tie_rel=1e-9,max_intervals=200000
        )
        out.update({
            "times_seconds":times.tolist(),
            "switched_propagator":[json_array(x) for x in props],
            "switching_discrepancy_curve":disc.tolist(),
            "period_mean_operator":json_array(member["Abar"]),
        })
        numerical["switching_discrepancy_certificate"]=cert
        return out,numerical

    A=np.asarray(member["A"],float)
    out["spectral_abscissa"]=spectral_abscissa(A)
    out["embedded_eigenvalues"]=[cpx(z) for z in embedded_eigenvalues(A)]
    G=np.asarray(member.get("G",np.eye(A.shape[0])),float)
    numerical["stationary_peak_certificate"]=certified_stationary_peak(
        A,G,horizon=T,rel_tol=1e-9,tie_rel=1e-9,max_intervals=200000
    )
    if member.get("x0") is not None:
        curve=physical_response_curve(A,G,member["x0"],times)
        out["times_seconds"]=times.tolist()
        out["response_curve"]=curve.tolist()
        out["integrated_burden"]=integrated_burden(times,curve)
    if member.get("B") is not None:
        out["state_impulse"]=json_array(state_impulse_curve(A,member["B"],times))
    if member.get("B") is not None and member.get("C") is not None:
        out["io_impulse"]=json_array(io_impulse_curve(A,member["B"],member["C"],times))
    if member.get("C") is not None and member.get("x0") is not None:
        out["observed_recovery"]=json_array(observed_recovery(A,member["C"],member["x0"],times))
    return out,numerical


def observed_arrays(member):
    arrays={}
    if member["kind"]=="TIME_VARYING":
        return arrays
    A=np.asarray(member["A"],float)
    C=member.get("C")
    x0=member.get("x0")
    if member["kind"]=="MISSPECIFICATION":
        C=member.get("C_linear_probe"); x0=member.get("x0")
    if C is None or x0 is None:
        return arrays
    for fs in (96.0,48.0,24.0):
        t=schedule(fs,32.0)
        y=observed_recovery(A,C,x0,t)
        if member["kind"]=="MISSPECIFICATION":
            y=np.square(y)
        arrays[str(int(fs))]={"times_seconds":t.tolist(),"observed":json_array(y)}
    return arrays


def nb23_exact_row(case_id,member):
    target,numerical=exact_target_evidence(case_id,member)
    path=f"NSD_vNext/results/v0_2_frozen/nb23/{case_id}__exact.json"
    return {
        "schema":"NSD_NB23_V0_2_EVIDENCE_RECORD_V0_2",
        "packet_id":"NB23-B01-FROZEN",
        "authority_identity":{"scientific_baseline":"NSD-V02-B01-FROZEN"},
        "case_id":case_id,
        "suite_identity":{"suite":"NB23_EXHAUSTIVE_SUITE_CANDIDATE_v0.1.json"},
        "representation_contract":representation_contract(case_id),
        "operator_identity":operator_identity(member,hidden=False),
        "observation_contract":{"layer":"exact_truth"},
        "target_namespace":"EXACT_SUFFICIENCY",
        "target_evidence":target,
        "numerical_verification":numerical,
        "generator_provenance_validation":{"built_from_frozen_registry":True},
        "failure_record":None,
        "artifact_identity":{"path":path},
        "environment":env_record(),
        "scientific_adjudication":"NOT_PERFORMED_BY_GITHUB",
        "representation_ranking":None,
        "combined_cross_lane_pass":None,
        "whole_system_scalar":None,
    }


def nb23_obs_row(case_id,member,arrays):
    path=f"NSD_vNext/results/v0_2_frozen/nb23/{case_id}__recoverability.json"
    return {
        "schema":"NSD_NB23_V0_2_EVIDENCE_RECORD_V0_2",
        "packet_id":"NB23-B01-FROZEN",
        "authority_identity":{"scientific_baseline":"NSD-V02-B01-FROZEN"},
        "case_id":case_id,
        "suite_identity":{"suite":"NB23_EXHAUSTIVE_SUITE_CANDIDATE_v0.1.json"},
        "representation_contract":representation_contract(case_id),
        "operator_identity":operator_identity(member,hidden=True),
        "observation_contract":{
            "sampling_projection_hz":[96,48,24],
            "hidden_descriptor_accessed":False,
        },
        "target_namespace":"OBSERVATION_CONDITIONED_RECOVERABILITY",
        "target_evidence":{"sampled_observations":arrays},
        "numerical_verification":{"observed_array_relative_tolerance":1e-10},
        "generator_provenance_validation":{"built_from_frozen_registry":True},
        "failure_record":None,
        "artifact_identity":{"path":path},
        "environment":env_record(),
        "scientific_adjudication":"NOT_PERFORMED_BY_GITHUB",
        "representation_ranking":None,
        "combined_cross_lane_pass":None,
        "whole_system_scalar":None,
    }


def run_nb1(order):
    tasks=nb1_tasks()
    completed=read_completed(NB1_CP)
    completed_set=set(completed)
    since=0
    NB1_DIR.mkdir(parents=True,exist_ok=True)
    for cid in order:
        if cid in completed_set and (NB1_DIR/f"{cid}.json").exists():
            continue
        if runtime_reserve():
            dump(NB1_CP,checkpoint_identity(
                "N-B1",completed,order,f"resume N-B1 case {cid}",state="ADVANCED_CHECKPOINT"
            ))
            git_checkpoint("NSD v0.2: runtime-reserve N-B1 checkpoint")
            return False
        try:
            row=nb1_row(cid,tasks[cid])
        except Exception as exc:
            truth,rep,parent_seed,obs_label,rate=tasks[cid]
            row={
                "schema":"NSD_NB1_V0_2_EVIDENCE_ROW_V0_2",
                "packet_id":"NB1-B01-EXACT-PREQ-V03",
                "authority_identity":{"scientific_baseline":"NSD-V02-B01-FROZEN"},
                "truth_identity":truth,
                "generator_contract":{"generator":truth["generator"]},
                "seed_identity":{"replicate_index":rep,"parent_seed_decimal":str(parent_seed),"rng":"PCG64DXSM"},
                "sampling_contract":{"rate_label":rate},
                "observation_contract":{"label":obs_label},
                "channel_inputs":{},
                "raw_evidence":{},
                "search_integrity_evidence":{},
                "profile_evidence":{},
                "paired_rate_evidence":None,
                "failure_record":{"type":type(exc).__name__,"message":str(exc)},
                "artifact_identity":{"path":f"NSD_vNext/results/v0_2_frozen/nb1/{cid}.json"},
                "environment":env_record(),
                "scientific_adjudication":"NOT_PERFORMED_BY_GITHUB",
                "licenses_real_eeg_local_chi":False,
            }
        dump(NB1_DIR/f"{cid}.json",row)
        completed.append(cid); completed_set.add(cid); since+=1
        dump(NB1_CP,checkpoint_identity("N-B1",completed,order,"continue next frozen N-B1 case"))
        if since>=COMMIT_EVERY:
            git_checkpoint(f"NSD v0.2: checkpoint {len(completed)} N-B1 cases")
            since=0
    if since:
        git_checkpoint("NSD v0.2: checkpoint completed N-B1 evidence")
    dump(NB1_CP,checkpoint_identity(
        "N-B1",completed,order,"await scientific review after cross-lane evidence closure",
        state="SCIENTIFIC_REVIEW_READY"
    ))
    return True


def run_nb23(order):
    completed=read_completed(NB23_CP)
    completed_set=set(completed); since=0
    NB23_DIR.mkdir(parents=True,exist_ok=True)
    observed_for_groups={}
    for cid in order:
        exact_path=NB23_DIR/f"{cid}__exact.json"
        if cid in completed_set and exact_path.exists():
            rec=NB23_DIR/f"{cid}__recoverability.json"
            if rec.exists():
                observed_for_groups[cid]=load(rec)["target_evidence"]["sampled_observations"]
            continue
        if runtime_reserve():
            dump(NB23_CP,checkpoint_identity(
                "N-B2/N-B3",completed,order,f"resume N-B2/N-B3 case {cid}",state="ADVANCED_CHECKPOINT"
            ))
            git_checkpoint("NSD v0.2: runtime-reserve N-B2 N-B3 checkpoint")
            return False
        member=build_member(cid)
        try:
            exact=nb23_exact_row(cid,member)
        except Exception as exc:
            exact={
                "schema":"NSD_NB23_V0_2_EVIDENCE_RECORD_V0_2",
                "packet_id":"NB23-B01-FROZEN",
                "authority_identity":{"scientific_baseline":"NSD-V02-B01-FROZEN"},
                "case_id":cid,
                "suite_identity":{"suite":"NB23_EXHAUSTIVE_SUITE_CANDIDATE_v0.1.json"},
                "representation_contract":representation_contract(cid),
                "operator_identity":operator_identity(member,hidden=False),
                "observation_contract":{"layer":"exact_truth"},
                "target_namespace":"EXACT_SUFFICIENCY",
                "target_evidence":{},
                "numerical_verification":{},
                "generator_provenance_validation":{"built_from_frozen_registry":True},
                "failure_record":{"type":type(exc).__name__,"message":str(exc)},
                "artifact_identity":{"path":str(exact_path.relative_to(REPO_ROOT))},
                "environment":env_record(),
                "scientific_adjudication":"NOT_PERFORMED_BY_GITHUB",
                "representation_ranking":None,
                "combined_cross_lane_pass":None,
                "whole_system_scalar":None,
            }
        dump(exact_path,exact)
        arrays=observed_arrays(member)
        if arrays:
            obs=nb23_obs_row(cid,member,arrays)
            dump(NB23_DIR/f"{cid}__recoverability.json",obs)
            observed_for_groups[cid]=arrays
        completed.append(cid); completed_set.add(cid); since+=1
        dump(NB23_CP,checkpoint_identity(
            "N-B2/N-B3",completed,order,"continue next frozen N-B2/N-B3 case"
        ))
        if since>=COMMIT_EVERY:
            git_checkpoint(f"NSD v0.2: checkpoint {len(completed)} N-B2 N-B3 cases")
            since=0

    suite=frozen_suite()
    compat={}
    for eq in suite.get("equivalence_classes",[]):
        ids=[x for x in eq["members"] if x in observed_for_groups and "96" in observed_for_groups[x]]
        if len(ids)>=2:
            data={x:np.asarray(observed_for_groups[x]["96"]["observed"],float) for x in ids}
            compat[eq["id"]]=compatibility_sets(ids,data,tol=1e-10)
    dump(NB23_DIR/"recoverability_compatibility.json",{
        "schema":"NSD_NB23_V0_2_PAIRWISE_RECOVERABILITY_EVIDENCE_V0_1",
        "compatibility":compat,
        "hidden_descriptor_accessed":False,
        "scientific_adjudication":"NOT_PERFORMED_BY_GITHUB",
    })
    if since:
        git_checkpoint("NSD v0.2: checkpoint completed N-B2 N-B3 evidence")
    dump(NB23_CP,checkpoint_identity(
        "N-B2/N-B3",completed,order,"await scientific review after cross-lane evidence closure",
        state="SCIENTIFIC_REVIEW_READY"
    ))
    return True


def final_manifest():
    files=sorted(p for p in RESULTS.rglob("*") if p.is_file() and p!=MANIFEST)
    return {
        "schema":"NSD_V0_2_FROZEN_EVIDENCE_MANIFEST_V0_1",
        "scientific_baseline":"NSD-V02-B01-FROZEN",
        "files":[
            {"path":str(p.relative_to(REPO_ROOT)),"sha256":sha256_file(p),"bytes":p.stat().st_size}
            for p in files
        ],
        "nb1_checkpoint":load(NB1_CP),
        "nb23_checkpoint":load(NB23_CP),
        "scientific_adjudication":"NOT_PERFORMED_BY_GITHUB",
        "terminal_state":"SCIENTIFIC_REVIEW_READY",
        "environment":env_record(),
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--preflight",action="store_true")
    args=parser.parse_args()
    summary=preflight()
    if args.preflight:
        print(json.dumps(summary,indent=2,sort_keys=True))
        return 0

    auth=authority()
    if auth.get("execution_authorized") is not True or auth.get("status")!="AUTHORIZED_FROZEN_EXECUTION":
        raise FrozenContractError("result-producing execution is not authorized")

    RESULTS.mkdir(parents=True,exist_ok=True)
    order=load(ORDER)
    nb23_done=run_nb23(order["nb23_case_ids"])
    if not nb23_done:
        return 0
    nb1_done=run_nb1(order["nb1_case_ids"])
    if not nb1_done:
        return 0
    dump(MANIFEST,final_manifest())
    git_checkpoint("NSD v0.2: SCIENTIFIC_REVIEW_READY evidence complete")
    print(json.dumps({
        "status":"SCIENTIFIC_REVIEW_READY",
        "nb1_completed":len(load(NB1_CP)["completed_case_ids"]),
        "nb23_completed":len(load(NB23_CP)["completed_case_ids"]),
        "manifest":str(MANIFEST.relative_to(REPO_ROOT)),
    },indent=2))
    return 0


if __name__=="__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"NSD v0.2 conveyor failure: {type(exc).__name__}: {exc}",file=sys.stderr)
        raise
