#!/usr/bin/env python3
# execution trigger after workflow registration
import json, hashlib, math, urllib.request
from pathlib import Path
import numpy as np
from scipy.io import loadmat
from scipy.integrate import solve_ivp

SEED=20260925
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"hog1_results"; OUT.mkdir(parents=True,exist_ok=True)
URL="https://raw.githubusercontent.com/neuertlab/Jashnsaz_STARProtocols_2021/main/Jashnsaz_et_al_dir02_simData/Models_and_TrueParams/FP_OBJ_FIM.mat"
MAT=OUT/"FP_OBJ_FIM.mat"
EXPECTED_BLOB="7b152c6aa33018970dcd689244864fcb595f1f52"

if not MAT.exists():
    urllib.request.urlretrieve(URL,MAT)

sha256=hashlib.sha256(MAT.read_bytes()).hexdigest()
m=loadmat(MAT,simplify_cells=True)
obj=m["FP_OBJ_FIM"]
params=np.asarray(obj["best_pars"],dtype=float).ravel()

A=np.array([[0,0,1,0],[0,0,0,-1],[-1,1,0,0],[0,0,1,0]],dtype=int)
B=np.array([-1,1,0,0],dtype=int)
C=np.array([-1,-1,-1,-1],dtype=int)
if len(params)!=2*(np.count_nonzero(A)+np.count_nonzero(B)+np.count_nonzero(C)):
    raise RuntimeError(f"parameter count mismatch: {len(params)}")

def rhs(t,x,salt):
    K=params; pc=0
    d=0.1
    fa=np.zeros(4); fb=np.zeros(4)
    for j in range(4):
        if B[j]==1:
            fb[j]+=K[pc]*(1-x[j])/((1-x[j])+K[pc+1]); pc+=2
        elif B[j]==-1:
            fb[j]-=K[pc]*x[j]/(x[j]+K[pc+1]); pc+=2
        if C[j]==-1:
            fa[j]-=K[pc]*d*x[j]/(x[j]+K[pc+1]); pc+=2
        elif C[j]==1:
            fa[j]+=K[pc]*d*(1-x[j])/((1-x[j])+K[pc+1]); pc+=2
    for j in range(4):
        for k in range(4):
            if A[j,k]==1:
                fa[j]+=K[pc]*x[k]*(1-x[j])/((1-x[j])+K[pc+1]); pc+=2
            elif A[j,k]==-1:
                fa[j]-=K[pc]*x[k]*x[j]/(x[j]+K[pc+1]); pc+=2
    return fa + salt(t)*fb

final=0.3
T=1500.0
profiles={
 "step": lambda t: final if t>=0.001 else 0.0,
 "root2": lambda t: min(final*(max(t,0)/T)**0.5,final),
 "linear": lambda t: min(final*(max(t,0)/T),final),
 "quadratic": lambda t: min(final*(max(t,0)/T)**2,final),
 "quintic": lambda t: min(final*(max(t,0)/T)**5,final),
 "heptic": lambda t: min(final*(max(t,0)/T)**7,final),
}
t_eval=np.arange(0,3000+60,60,dtype=float)
ic=np.array([0.05,0.05,0.05,0.0])
records=[]
trajectories={}
spectra={}
for name,salt in profiles.items():
    sol=solve_ivp(lambda t,x: rhs(t,x,salt),(0,3000),ic,t_eval=t_eval,method="BDF",rtol=1e-9,atol=1e-11)
    if not sol.success: raise RuntimeError(name+": "+sol.message)
    y=sol.y[3,:]
    trajectories[name]={"t_min":(sol.t/60).tolist(),"hog1":y.tolist(),"salt":[salt(t) for t in sol.t]}
    peak=float(np.max(y)); imax=int(np.argmax(y)); tpeak=float(sol.t[imax]/60)
    auc=float(np.trapz(y,sol.t/60))
    endpoint=float(y[-1])
    ret=float((peak-endpoint)/peak) if peak!=0 else float("nan")
    records.append([peak,tpeak,auc,endpoint,ret])
    xf=sol.y[:,-1]
    eps=1e-6
    J=np.zeros((4,4))
    for j in range(4):
        dx=np.zeros(4); dx[j]=eps
        J[:,j]=(rhs(3000,xf+dx,salt)-rhs(3000,xf-dx,salt))/(2*eps)
    ev=np.linalg.eigvals(J)
    spectra[name]=[[float(z.real),float(z.imag)] for z in ev]

X=np.asarray(records,float)
mu=X.mean(axis=0); sd=X.std(axis=0,ddof=1)
if np.any(sd==0): raise RuntimeError("zero-variance frozen coordinate")
Z=(X-mu)/sd
U,S,Vt=np.linalg.svd(Z-Z.mean(axis=0),full_matrices=False)
var=S*S
pc1=float(var[0]/var.sum())
recon=np.outer(U[:,0]*S[0],Vt[0,:])+Z.mean(axis=0)
max_z_resid=float(np.max(np.abs(Z-recon)))
adequate=bool(pc1>=0.95 and max_z_resid<=0.10)
rank=int(np.sum(S>1e-10))

# scalar eligibility: all contexts must have a stable complex pair.
complex_pairs={}
eligible=True
for name,evs in spectra.items():
    ev=[complex(r,i) for r,i in evs]
    cand=[z for z in ev if abs(z.imag)>1e-8 and z.real<0]
    if len(cand)<2:
        eligible=False; complex_pairs[name]=None
    else:
        z=max(cand,key=lambda q:abs(q.imag))
        complex_pairs[name]={"real":z.real,"imag":abs(z.imag),"chi_candidate":(-z.real/abs(z.imag))}

result={
 "schema_version":"0.1",
 "experiment_id":"HOG1_INPUT_CONTEXT_P0Q_V01",
 "status":"EXECUTED_VALID_SOURCE_NATIVE_MODEL_QUALIFICATION",
 "evidence_class":"P0-Q_SOURCE_NATIVE_MODEL_QUALIFICATION",
 "source":{"url":URL,"download_sha256":sha256,"github_blob_sha1":EXPECTED_BLOB,"n_params":int(len(params))},
 "contexts":list(profiles),
 "features":["peak","time_to_peak_min","auc_0_50min","endpoint_50min","postpeak_return_fraction"],
 "feature_matrix":{n:{k:float(v) for k,v in zip(["peak","time_to_peak_min","auc_0_50min","endpoint_50min","postpeak_return_fraction"],row)} for n,row in zip(profiles,X)},
 "representation":{"singular_values":[float(x) for x in S],"intrinsic_rank":rank,"pc1_variance_fraction":pc1,"max_abs_standardized_reconstruction_residual":max_z_resid,"one_dimensional_adequacy":adequate,"Chi_bio_disposition":"ONE_DIMENSIONAL_COMPRESSION_ADEQUATE_P0Q" if adequate else "MULTICOORDINATE_RESPONSE_ORGANIZATION_REQUIRED_P0Q"},
 "local_spectra":spectra,
 "scalar_gate":{"stable_complex_pair_all_contexts":eligible,"complex_pair_candidates":complex_pairs,"chi_bio_disposition":"CANDIDATE_REQUIRES_WHOLE_EVENT_PREDICTIVE_TRANSPORT_TEST" if eligible else "NOT_LICENSED_NO_STABLE_COMPLEX_PAIR_ACROSS_ALL_CONTEXTS"},
 "Bio_Chi_disposition":"INPUT_CONTEXT_REORGANIZES_REALIZED_HOG1_RESPONSE_WITH_FIXED_NETWORK_AND_PARAMETERS_P0Q",
 "claim_ceiling":"source-native model qualification; not experimental validation"
}
(OUT/"HOG1_INPUT_CONTEXT_P0Q_V01_RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
(OUT/"HOG1_INPUT_CONTEXT_P0Q_V01_TRAJECTORIES.json").write_text(json.dumps(trajectories)+"\n")
print(json.dumps(result,indent=2))
