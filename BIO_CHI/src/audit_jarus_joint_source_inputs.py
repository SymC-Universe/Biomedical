#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, pathlib, re

ROOT=pathlib.Path(__file__).resolve().parents[2]
BIO=ROOT/"BIO_CHI"
BASE=BIO/"artifacts"/"generated"/"jarus_matlab_compat"/"source"/"S1_Codes"/"MATLAB files"/"Reduced2023"
OUT=BIO/"artifacts"/"generated"/"jarus_joint_source_audit"
OUT.mkdir(parents=True,exist_ok=True)

files={}
for name in ("reduced.m","simulate_reduced.m","run_simulate_reduced.m"):
    p=BASE/name
    txt=p.read_text(encoding="utf-8",errors="replace")
    lines=txt.splitlines()
    if name=="reduced.m":
        keep=[(i+1,l.strip()) for i,l in enumerate(lines) if re.search(r"^(kdeg|k1|k2|k3|delta|epsilon|cdeg|c4a|a3|a2|c5a|i1a)\s*=|dy\([1-6]\)",l.strip())]
    elif name=="simulate_reduced.m":
        keep=[(i+1,l.strip()) for i,l in enumerate(lines) if re.search(r"species0|t_equil_begin|t_tnf_begin|t_tnf_end|t_sim_end|pulse_begin|pulse_end|rest_end|steps\{|dur_tnf|n_tnf|plot_tspan",l)]
    else:
        keep=[(i+1,l.strip()) for i,l in enumerate(lines) if re.search(r"simulate_reduced|plot_title|n_pulses",l)]
    files[name]={
      "sha256":hashlib.sha256(p.read_bytes()).hexdigest(),
      "selected_lines":[{"line":i,"text":s} for i,s in keep]
    }

result={
 "schema_version":"0.1",
 "audit_type":"jarus_joint_scalar_modal_system_source_inputs",
 "scientific_endpoint_opened":False,
 "chi_bio_recomputed":False,
 "source_files":files,
 "interpretation_limit":"Source literals and protocol control-flow only. No trajectory, mode, scalar, or comparison result is computed."
}
(OUT/"jarus_joint_source_audit_v0_1.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
