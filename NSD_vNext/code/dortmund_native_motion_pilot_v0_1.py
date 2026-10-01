[Reading 154 lines from start (total: 154 lines, 0 remaining)]

from __future__ import annotations
import json, os, re, shutil, subprocess, sys, platform
from pathlib import Path

subprocess.check_call([sys.executable,"-m","pip","install","-q","openneuro-py","fooof==1.1.1"])

import numpy as np
import pandas as pd
import mne
import openneuro as on
from fooof import FOOOF
from mne.time_frequency import psd_array_welch

TASK="NSD_DORTMUND_HEALTHY_NATIVE_MOTION_PILOT_V01"
DATASET="ds005385"
OUT=Path("/kaggle/working")
DATA=OUT/"dortmund"
PART_URL="https://raw.githubusercontent.com/OpenNeuroDatasets/ds005385/main/participants.tsv"

parts=pd.read_csv(PART_URL,sep="\t",dtype=str)
parts["age_num"]=pd.to_numeric(parts["age"],errors="coerce")
parts["late0"]=parts["late_ses1"].fillna("").astype(str).eq("0")
parts=parts[(parts["session1"]=="yes") & parts["late0"]].copy()
parts["age_bin"]=pd.cut(parts["age_num"],bins=[19,29,39,49,59,70],labels=["20-29","30-39","40-49","50-59","60-70"],include_lowest=True)
selected=[]
for age_bin in ["20-29","30-39","40-49","50-59","60-70"]:
    for sex in ["F","M"]:
        sub=parts[(parts["age_bin"].astype(str)==age_bin)&(parts["sex"]==sex)].sort_values("participant_id")
        selected.extend(sub.head(4)["participant_id"].tolist())
selected=list(dict.fromkeys(selected))
if len(selected)!=40:
    raise RuntimeError(f"Expected 40 pilot subjects, got {len(selected)}")

conditions={
 "EC_pre":("EyesClosed","pre"),
 "EC_post":("EyesClosed","post"),
 "EO_pre":("EyesOpen","pre"),
 "EO_post":("EyesOpen","post"),
}

def band_int(freqs, psd, lo, hi):
    m=(freqs>=lo)&(freqs<=hi)
    return float(np.trapezoid(psd[m],freqs[m]))

def features(path):
    raw=mne.io.read_raw_edf(path,preload=True,verbose="ERROR")
    raw.pick(picks="eeg")
    raw.filter(1.0,40.0,verbose="ERROR")
    raw.set_eeg_reference("average",projection=False,verbose="ERROR")
    x=raw.get_data()
    sf=float(raw.info["sfreq"])
    psd,freqs=psd_array_welch(x,sfreq=sf,fmin=1.0,fmax=40.0,n_fft=4096,n_per_seg=4096,n_overlap=2048,average="mean",verbose=False)
    names=list(raw.ch_names)
    posterior=[i for i,n in enumerate(names) if re.match(r"^(P(?:[0-9]+|z)|PO(?:[0-9]+|z)|O(?:[0-9]+|z))$",n,re.I)]
    if not posterior:
        raise RuntimeError("No posterior ROI channels found")
    ppost=np.nanmean(psd[posterior,:],axis=0)
    pall=np.nanmean(psd,axis=0)
    alpha_rel=band_int(freqs,ppost,8,13)/band_int(freqs,ppost,1,40)
    am=(freqs>=8)&(freqs<=13)
    apf=float(freqs[am][np.argmax(ppost[am])])
    tbr=band_int(freqs,pall,4,8)/band_int(freqs,pall,13,30)
    fm=FOOOF(peak_width_limits=[1.0,8.0],max_n_peaks=6,min_peak_height=0.1,aperiodic_mode="fixed",verbose=False)
    fm.fit(freqs,pall,[2.0,40.0])
    aper=float(fm.aperiodic_params_[1])
    return {
      "posterior_alpha_relative_power":float(alpha_rel),
      "alpha_peak_frequency_hz":apf,
      "theta_beta_ratio":float(tbr),
      "aperiodic_exponent":aper,
      "sfreq":sf,
      "n_eeg_channels":len(names),
      "n_posterior_channels":len(posterior),
      "duration_sec":float(raw.n_times/sf),
    }

rows=[]; failures=[]
for si,subj in enumerate(selected,1):
    include=[]
    for key,(task,acq) in conditions.items():
        include.append(f"{subj}/ses-1/eeg/{subj}_ses-1_task-{task}_acq-{acq}_eeg.edf")
    try:
        on.download(dataset=DATASET,target_dir=DATA,include=include)
        meta=parts.loc[parts["participant_id"]==subj].iloc[0]
        for key,(task,acq) in conditions.items():
            p=DATA/subj/"ses-1"/"eeg"/f"{subj}_ses-1_task-{task}_acq-{acq}_eeg.edf"
            if not p.exists():
                raise FileNotFoundError(str(p))
            f=features(p)
            f.update({"participant_id":subj,"sex":meta["sex"],"age":float(meta["age_num"]),"age_bin":str(meta["age_bin"]),"condition":key})
            rows.append(f)
    except Exception as e:
        failures.append({"participant_id":subj,"error":repr(e)})
    finally:
        sp=DATA/subj
        if sp.exists():
            shutil.rmtree(sp,ignore_errors=True)
    print(f"{si}/{len(selected)} {subj} rows={len(rows)} failures={len(failures)}",flush=True)

df=pd.DataFrame(rows)
df.to_csv(OUT/"dortmund_native_motion_pilot_features.csv",index=False)
pd.DataFrame({"participant_id":selected}).to_csv(OUT/"dortmund_native_motion_pilot_subjects.csv",index=False)

metrics=["posterior_alpha_relative_power","alpha_peak_frequency_hz","theta_beta_ratio","aperiodic_exponent"]
summary={
 "task_id":TASK,
 "classification":"INDEPENDENT_HEALTHY_NATIVE_BASELINE_PILOT",
 "dataset":DATASET,
 "selected_subjects":selected,
 "n_selected":len(selected),
 "n_rows":int(len(df)),
 "n_failures":len(failures),
 "failures":failures,
 "environment":{"python":platform.python_version(),"numpy":np.__version__,"pandas":pd.__version__,"mne":mne.__version__},
 "methods":{
   "bandpass_hz":[1,40],"reference":"average","psd":"Welch",
   "welch_n_fft":4096,"welch_n_per_seg":4096,"welch_n_overlap":2048,
   "alpha_hz":[8,13],"theta_hz":[4,8],"beta_hz":[13,30],
   "aperiodic":{"fit_hz":[2,40],"peak_width_limits":[1,8],"max_n_peaks":6,"min_peak_height":0.1,"mode":"fixed"}
 },
 "condition_means":{},
 "ec_minus_eo_pre":{},
 "post_minus_pre":{},
}
for m in metrics:
    summary["condition_means"][m]={k:float(df.loc[df.condition==k,m].mean()) for k in conditions}
    piv=df.pivot(index="participant_id",columns="condition",values=m)
    paired=piv[["EC_pre","EO_pre"]].dropna()
    diff=paired["EC_pre"]-paired["EO_pre"]
    summary["ec_minus_eo_pre"][m]={
      "n":int(len(diff)),"mean_difference":float(diff.mean()),
      "cohens_d_paired":float(diff.mean()/diff.std(ddof=1)) if len(diff)>1 and diff.std(ddof=1)>0 else None
    }
    for state in ["EC","EO"]:
        z=piv[[f"{state}_pre",f"{state}_post"]].dropna()
        d=z[f"{state}_post"]-z[f"{state}_pre"]
        summary["post_minus_pre"].setdefault(m,{})[state]={
          "n":int(len(d)),"mean_difference":float(d.mean()),
          "sd_difference":float(d.std(ddof=1)) if len(d)>1 else None
        }

expected={
 "posterior_alpha_relative_power":"positive",
 "alpha_peak_frequency_hz":"positive",
 "theta_beta_ratio":"negative",
 "aperiodic_exponent":"negative",
}
summary["literature_direction_checks"]={}
for m,direction in expected.items():
    v=summary["ec_minus_eo_pre"][m]["mean_difference"]
    summary["literature_direction_checks"][m]={"expected_ec_minus_eo":direction,"observed":v,"pass":bool(v>0 if direction=="positive" else v<0)}

(OUT/"dortmund_native_motion_pilot_summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"task_id":TASK,"n_rows":len(df),"n_failures":len(failures),"direction_checks":summary["literature_direction_checks"]},indent=2))

[executed on device: Popstop (6c701129-153c-433b-9874-1ae1524c8c10)]