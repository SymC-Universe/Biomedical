from __future__ import annotations

import argparse, json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))

import numpy as np
from src.hankel_uncertainty import nsd_covariance_hankel, batch_hankel_covariance_root, diagonal_variance_from_root
from src.synthetic_systems import make_linear_system, simulate_linear, make_noise_bases, add_measurement_noise

DT=0.02; BLOCK_ROWS=12; N_CHANNELS=4; PROCESS_SCALE=0.35
DURATIONS=[3600,7200]; BATCH_COUNTS=[6,12]; REPLICATES=24; SEED=202609112300
MODES=[{"type":"complex","decay":0.6,"frequency_hz":3.0},{"type":"complex","decay":1.0,"frequency_hz":8.0}]
CONDITIONS=[("nominal",None),("white_sensor_10pct",{"type":"white","fraction_channel_sd":0.10})]


def _simulate_fixed(A,C,n,rep,noise):
    r=np.random.default_rng(SEED+10000*rep+n)
    Y=simulate_linear(A,C,DT,n,PROCESS_SCALE,r)
    if noise is not None:
        rn=np.random.default_rng(SEED+900000+10000*rep+n)
        w,c=make_noise_bases(n,N_CHANNELS,0.0,rn)
        Y=add_measurement_noise(Y,noise,w,c)
    return Y


def _summary(emp,pred):
    mask=np.isfinite(emp)&np.isfinite(pred)&(emp>0)&(pred>0)
    e=emp[mask]; p=pred[mask]; ratio=p/e
    corr=float(np.corrcoef(np.log(e),np.log(p))[0,1]) if len(e)>1 else None
    return {"entries":int(len(e)),"predicted_over_empirical_variance_median":float(np.median(ratio)),"ratio_p10":float(np.quantile(ratio,0.10)),"ratio_p90":float(np.quantile(ratio,0.90)),"log_variance_correlation":corr,"median_absolute_log_ratio":float(np.median(np.abs(np.log(ratio))))}


def build():
    sysrng=np.random.default_rng(SEED)
    A,C=make_linear_system({"modes":MODES,"similarity":"orthogonal"},N_CHANNELS,sysrng)
    rows=[]
    for cname,noise in CONDITIONS:
        for n in DURATIONS:
            full=[]; pred={k:[] for k in BATCH_COUNTS}
            for rep in range(REPLICATES):
                Y=_simulate_fixed(A,C,n,rep,noise)
                full.append(nsd_covariance_hankel(Y,BLOCK_ROWS).reshape(-1,order="F"))
                for k in BATCH_COUNTS:
                    T,meta=batch_hankel_covariance_root(Y,BLOCK_ROWS,k)
                    pred[k].append(diagonal_variance_from_root(T))
            empirical=np.var(np.vstack(full),axis=0,ddof=1)
            for k in BATCH_COUNTS:
                predicted=np.mean(np.vstack(pred[k]),axis=0)
                rows.append({"condition":cname,"coverage_role":"NOMINAL_FUNCTION" if cname=="nominal" else "PERTURBED_FUNCTION","n_samples":n,"n_batches":k,**_summary(empirical,predicted)})
    return {"schema":"nsd-p0d5-native-hankel-uncertainty-v1","status":"P0_D_SAMPLING_COVARIANCE_CALIBRATION_NOT_CONFIRMATORY","protocol":"General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum","p1_authorized":False,"estimator":"exact current NSD lag-specific covariance Hankel","design":{"durations":DURATIONS,"batch_counts":BATCH_COUNTS,"replicates":REPLICATES,"block_rows":BLOCK_ROWS,"channels":N_CHANNELS,"conditions":[x[0] for x in CONDITIONS]},"summary":rows,"nonclaims":["No batch count is selected from this map.","The batch covariance root is an approximation whose block-dependence and cross-boundary omissions require calibration.","No modal standard error or confidence interval is produced.","No P1 uncertainty or INDETERMINATE rule is frozen."]}

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--output",default="results/p0d_mapping/native_hankel_uncertainty_v1.json"); a=ap.parse_args()
    rec=build(); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(rec,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(out.resolve())
    for row in rec["summary"]: print(json.dumps(row,sort_keys=True))
    print("P0-D NATIVE HANKEL UNCERTAINTY CALIBRATION COMPLETE. No modal interval or P1 rule frozen.")
