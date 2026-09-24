#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import pathlib

import numpy as np
from scipy.integrate import solve_ivp


STATE_ORDER = [
    "Ras","Ras_star","Raf","Raf_star","Mek","Mek_star","Erk","Erk_star",
    "Nfb","Nfb_star","FgfR","FgfR_star","H","H_F","H_F_R"
]


def git_blob_sha(path: pathlib.Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def read_csv_vector(path: pathlib.Path) -> np.ndarray:
    txt = path.read_text(encoding="utf-8").strip()
    return np.array([float(x.strip()) for x in txt.replace("\n", " ").split(",") if x.strip()], dtype=float)


def read_state_matrix(path: pathlib.Path) -> np.ndarray:
    rows=[]
    for line in path.read_text(encoding="utf-8").strip().splitlines():
        vals=[float(x.strip()) for x in line.split(",") if x.strip()]
        rows.append(vals)
    a=np.asarray(rows,dtype=float)
    if a.ndim != 2:
        raise SystemExit("BLUM_B3_SOURCE_MATRIX_NOT_2D")
    return a


def rhs_factory(p: dict[str,float], fgf: float):
    def rhs(_t: float, y: np.ndarray) -> np.ndarray:
        (Ras,Ras_s,Raf,Raf_s,Mek,Mek_s,Erk,Erk_s,Nfb,Nfb_s,FgfR,FgfR_s,H,H_F,H_F_R)=y
        v1=p["k_1_2"]*(p["r_h"]*H_F_R+(1-p["r_h"])*FgfR_s)*(Ras/(p["K_1_2"]+Ras))
        v2=p["k_2_1"]*(Ras_s/(p["K_2_1"]+Ras_s))
        nfb_h=Nfb_s**p["h_nfb"]
        kn_h=p["K_NFB"]**p["h_nfb"]
        v3=p["k_3_4"]*Ras_s*(Raf/(p["K_3_4"]+Raf))*(kn_h/(kn_h+nfb_h))
        v4=p["k_4_3"]*(Raf_s/(p["K_4_3"]+Raf_s))
        v5=p["k_5_6"]*Raf_s*(Mek/(p["K_5_6"]+Mek))
        v6=p["k_6_5"]*(Mek_s/(p["K_6_5"]+Mek_s))
        v7=p["k_7_8"]*Mek_s*(Erk/(p["K_7_8"]+Erk))
        v8=p["k_8_7"]*(Erk_s/(p["K_8_7"]+Erk_s))
        v9=p["f_1_2"]*Erk_s*(Nfb/(p["F_1_2"]+Nfb))
        v10=p["f_2_1"]*(Nfb_s/(p["F_2_1"]+Nfb_s))
        v11=p["r_3_4"]*fgf*FgfR
        v12=p["r_4_3"]*FgfR_s
        v13=p["r_5_6"]*H*fgf
        v14=p["r_6_5"]*H_F
        v15=p["r_5_7"]*H_F*FgfR
        v16=p["r_7_5"]*H_F_R
        return np.array([
            -v1+v2,
             v1-v2,
            -v3+v4,
             v3-v4,
            -v5+v6,
             v5-v6,
            -v7+v8,
             v7-v8,
            -v9+v10,
             v9-v10,
            -v11+v12-v15+v16,
             v11-v12,
            -v13+v14,
             v13-v14-v15+v16,
             v15-v16
        ],dtype=float)
    return rhs


def pool_matrix() -> np.ndarray:
    # Exact conserved totals from the source reaction stoichiometry.
    C=np.zeros((7,15),dtype=float)
    C[0,[0,1]]=1       # Ras total
    C[1,[2,3]]=1       # Raf total
    C[2,[4,5]]=1       # Mek total
    C[3,[6,7]]=1       # Erk total
    C[4,[8,9]]=1       # Nfb total
    C[5,[10,11,14]]=1  # FgfR-containing total
    C[6,[12,13,14]]=1  # H/HSPG-containing total
    return C


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--freeze",required=True)
    ap.add_argument("--trajectory",required=True)
    ap.add_argument("--times",required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()

    freeze=json.loads(pathlib.Path(args.freeze).read_text())
    traj_path=pathlib.Path(args.trajectory)
    times_path=pathlib.Path(args.times)
    outdir=pathlib.Path(args.out); outdir.mkdir(parents=True,exist_ok=True)

    exp_traj_sha=freeze["source_files"]["primary_reference_trajectory"]["git_blob_sha"]
    exp_time_sha=freeze["source_files"]["primary_reference_times"]["git_blob_sha"]
    got_traj_sha=git_blob_sha(traj_path)
    got_time_sha=git_blob_sha(times_path)
    if got_traj_sha != exp_traj_sha:
        raise SystemExit(f"BLUM_B3_TRAJECTORY_BLOB_MISMATCH {got_traj_sha}")
    if got_time_sha != exp_time_sha:
        raise SystemExit(f"BLUM_B3_TIMES_BLOB_MISMATCH {got_time_sha}")

    names=freeze["primary_parameter_names"]
    values=freeze["primary_parameter_values"]
    if len(names) != len(values):
        raise SystemExit("BLUM_B3_PARAMETER_LENGTH_MISMATCH")
    p=dict(zip(names,map(float,values)))

    t=read_csv_vector(times_path)
    source=read_state_matrix(traj_path)
    if source.shape != (15,t.size):
        raise SystemExit(f"BLUM_B3_SOURCE_SHAPE {source.shape} times={t.size}")
    expected_t=np.arange(0,180,2,dtype=float)
    if t.size != 90 or not np.array_equal(t,expected_t):
        raise SystemExit(f"BLUM_B3_UNEXPECTED_TIME_GRID n={t.size} first={t[0] if t.size else None} last={t[-1] if t.size else None}")

    y0=np.array([
        0.1,0.0,0.7,0.0,0.68,0.0,0.26,0.0,p["nfb_init"],0.0,
        p["fgfr_init_mean"],0.0,p["h_init_mean"],0.0,0.0
    ],dtype=float)
    fgf=float(freeze["primary_reproduction_protocol"]["fgf_input"])
    rhs=rhs_factory(p,fgf)
    sol=solve_ivp(
        rhs,(float(t[0]),float(t[-1])),y0,t_eval=t,method="BDF",
        rtol=1e-10,atol=1e-10
    )
    if not sol.success or sol.y.shape != source.shape or not np.all(np.isfinite(sol.y)):
        raise SystemExit(f"BLUM_B3_SOLVE_FAIL {sol.message}")

    err=sol.y-source
    max_abs=float(np.max(np.abs(err)))
    rmse=float(np.sqrt(np.mean(err**2)))
    state_max=[float(x) for x in np.max(np.abs(err),axis=1)]
    state_rmse=[float(x) for x in np.sqrt(np.mean(err**2,axis=1))]

    C=pool_matrix()
    pools=C@sol.y
    pool_drift=float(np.max(np.abs(pools-pools[:,[0]])))

    thresholds=freeze["primary_reproduction_protocol"]["pass_thresholds_frozen_before_result"]
    passed=(
        np.all(np.isfinite(sol.y)) and
        max_abs <= float(thresholds["maximum_absolute_state_error"]) and
        rmse <= float(thresholds["root_mean_square_state_error"])
    )

    result={
        "schema_version":"0.1",
        "project":"Bio Chi Investigation",
        "gate":"Blum B3 publication-native deterministic trajectory reproduction",
        "freeze":"BIO_CHI/config/BLUM_B3_TRANSPORT_SOURCE_FREEZE_v0_2.json",
        "epistemic_mode":"P0-Q",
        "status":"PASS_NATIVE_B3_TRAJECTORY_REPRODUCTION" if passed else "FAIL_NATIVE_B3_TRAJECTORY_REPRODUCTION",
        "source_git_blob_sha":{
            "trajectory":got_traj_sha,
            "times":got_time_sha
        },
        "source_shape":list(source.shape),
        "timepoints":int(t.size),
        "solver":{
            "method":"BDF",
            "rtol":1e-10,
            "atol":1e-10
        },
        "experiment":{
            "name":"sus_2-5ng",
            "fgf_input":fgf,
            "time_start_min":float(t[0]),
            "time_end_min":float(t[-1])
        },
        "metrics":{
            "maximum_absolute_state_error":max_abs,
            "root_mean_square_state_error":rmse,
            "per_state_max_abs_error":dict(zip(STATE_ORDER,state_max)),
            "per_state_rmse":dict(zip(STATE_ORDER,state_rmse)),
            "maximum_conserved_pool_drift_reproduction":pool_drift
        },
        "frozen_thresholds":thresholds,
        "spectrum_opened":False,
        "chi_bio_constructed":False,
        "Chi_bio_constructed":False,
        "Bio_Chi_transport_adjudicated":False,
        "interpretation":"Native-model reproduction preflight only. No ERK generator spectrum or SymC coordinate is computed in this gate."
    }
    (outdir/"blum_b3_native_reproduction_v0_2.json").write_text(json.dumps(result,indent=2)+"\n")
    np.savetxt(outdir/"blum_b3_reproduced_states.csv",sol.y,delimiter=",",fmt="%.12g")
    print(json.dumps(result,indent=2))
    if not passed:
        raise SystemExit("BLUM_B3_NATIVE_REPRODUCTION_SCIENTIFIC_GATE_FAIL")


if __name__=="__main__":
    main()
