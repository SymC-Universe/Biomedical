#!/usr/bin/env python3
from __future__ import annotations
import json, math, pathlib
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
BIO = ROOT / "BIO_CHI"
OUT = BIO / "artifacts" / "generated" / "blum_b3_modal_p0q_v01"
OUT.mkdir(parents=True, exist_ok=True)

p = {
"k_1_2":0.17983,"K_1_2":0.00034363,"k_2_1":0.51401,"K_2_1":0.64348,
"k_3_4":2.1251,"K_3_4":0.00010092,"K_NFB":7.9237e-06,"k_4_3":0.058363,
"K_4_3":0.0051924,"k_5_6":34.3875,"K_5_6":0.15889,"k_6_5":0.20789,
"K_6_5":0.13295,"k_7_8":0.42425,"K_7_8":8.3307e-06,"k_8_7":3.0977,
"K_8_7":1.8444,"f_1_2":2.8077e-05,"F_1_2":0.0092886,"f_2_1":1.0782e-05,
"F_2_1":8.053e-05,"h_nfb":0.74022,"fgf_input":0.0,"r_h":0.81717,
"r_3_4":0.063087,"r_4_3":0.046734,"r_5_6":0.01334,"r_6_5":0.081762,
"r_5_7":89.1764,"r_7_5":1.8483,"fgfr_init_mean":0.40487,
"nfb_init":0.42902,"h_init_mean":1.9705,"FRET_sigma":0.0001,"FRET_E":0.012115,
"erk_max":0.8,"erk_initial":0.0
}

names=["Ras","Ras_star","Raf","Raf_star","Mek","Mek_star","Erk","Erk_star",
       "Nfb","Nfb_star","FgfR","FgfR_star","H","H_F","H_F_R"]
xstar=np.array([0.1,0,0.7,0,0.68,0,0.26,0,0.42902,0,0.40487,0,1.9705,0,0],float)

def rhs(x):
    Ras,RasS,Raf,RafS,Mek,MekS,Erk,ErkS,Nfb,NfbS,FgfR,FgfRS,H,HF,HFR=x
    a12=p["k_1_2"]*(p["r_h"]*HFR+(1-p["r_h"])*FgfRS)*(Ras/(p["K_1_2"]+Ras))
    a21=p["k_2_1"]*(RasS/(p["K_2_1"]+RasS))
    a34=p["k_3_4"]*RasS*(Raf/(p["K_3_4"]+Raf))*(p["K_NFB"]**p["h_nfb"]/(p["K_NFB"]**p["h_nfb"]+NfbS**p["h_nfb"]))
    a43=p["k_4_3"]*(RafS/(p["K_4_3"]+RafS))
    a56=p["k_5_6"]*RafS*(Mek/(p["K_5_6"]+Mek))
    a65=p["k_6_5"]*(MekS/(p["K_6_5"]+MekS))
    a78=p["k_7_8"]*MekS*(Erk/(p["K_7_8"]+Erk))
    a87=p["k_8_7"]*(ErkS/(p["K_8_7"]+ErkS))
    f12=p["f_1_2"]*ErkS*(Nfb/(p["F_1_2"]+Nfb))
    f21=p["f_2_1"]*(NfbS/(p["F_2_1"]+NfbS))
    r34=p["r_3_4"]*p["fgf_input"]*FgfR
    r43=p["r_4_3"]*FgfRS
    r56=p["r_5_6"]*H*p["fgf_input"]
    r65=p["r_6_5"]*HF
    r57=p["r_5_7"]*HF*FgfR
    r75=p["r_7_5"]*HFR
    return np.array([
      -a12+a21, a12-a21, -a34+a43, a34-a43, -a56+a65, a56-a65,
      -a78+a87, a78-a87, -f12+f21, f12-f21,
      -r34+r43-r57+r75, r34-r43, -r56+r65, r56-r65-r57+r75, r57-r75
    ],float)

def fret(x):
    Erk,ErkS=x[6],x[7]
    E=p["FRET_E"]; em=p["erk_max"]; ei=p["erk_initial"]
    num=0.15*ErkS + ei*(-1.15*Erk-1.15*ErkS+E*ErkS) + em*((1+0.15*E*ei)*Erk+(1-1.15*E+0.15*E*ei)*ErkS)
    den=(em-ei)*(Erk+ErkS-E*ErkS)
    return num/den

def jacobian(mult):
    n=len(xstar); J=np.zeros((n,n)); base=np.finfo(float).eps**(1/3)
    for j in range(n):
        h=mult*base*max(1.0,abs(xstar[j]))
        xp=xstar.copy(); xm=xstar.copy(); xp[j]+=h; xm[j]-=h
        J[:,j]=(rhs(xp)-rhs(xm))/(2*h)
    return J

def measurement_gradient():
    C=np.zeros(len(xstar)); base=np.finfo(float).eps**(1/3)
    for j in range(len(xstar)):
        h=base*max(1.0,abs(xstar[j]))
        xp=xstar.copy(); xm=xstar.copy(); xp[j]+=h; xm[j]-=h
        C[j]=(fret(xp)-fret(xm))/(2*h)
    return C

resid=float(np.linalg.norm(rhs(xstar),np.inf))
C=measurement_gradient()
steps=[]
positive_complex_by_step=[]
for mult in (1.0,0.5,0.25):
    J=jacobian(mult)
    ev,V=np.linalg.eig(J)
    vis=[]
    for j in range(len(ev)):
        v=V[:,j]; vis.append(float(abs(C@v)/np.linalg.norm(v)))
    order=np.lexsort((np.imag(ev),np.real(ev)))
    ev=ev[order]; V=V[:,order]; vis=np.array(vis)[order]
    records=[]
    pc=[]
    for z,vv in zip(ev,vis):
        records.append({"real":float(z.real),"imag":float(z.imag),"visibility":float(vv)})
        if z.imag>1e-10:
            pc.append(complex(z))
    steps.append({"multiplier":mult,"modes":records})
    positive_complex_by_step.append(pc)

base=positive_complex_by_step[0]
max_spread=0.0
pair_match_ok=True
if any(len(z)!=len(base) for z in positive_complex_by_step[1:]):
    pair_match_ok=False; max_spread=float("inf")
else:
    for arr in positive_complex_by_step[1:]:
        used=[False]*len(arr)
        for b in base:
            candidates=[(abs(z-b),i,z) for i,z in enumerate(arr) if not used[i]]
            d,i,z=min(candidates,key=lambda t:t[0]); used[i]=True
            max_spread=max(max_spread,float(d/max(abs(b),1e-12)))

base_modes=steps[0]["modes"]
eligible=[]
for m in base_modes:
    z=complex(m["real"],m["imag"])
    if z.imag>1e-10 and z.real<0 and m["visibility"]>=1e-8:
        eligible.append({
          "real_per_min":m["real"],"imag_per_min":m["imag"],"visibility":m["visibility"],
          "chi":float(-z.real/abs(z)),"period_min":float(2*math.pi/z.imag)
        })

known_bad=np.diag([-1.,-2.,-3.])
kb_eigs=np.linalg.eigvals(known_bad)
known_bad_pass=bool(np.sum(np.imag(kb_eigs)>1e-10)==0)

if not np.isfinite(max_spread) or not pair_match_ok or max_spread>1e-5:
    status="INDETERMINATE_NUMERICAL_PAIR_IDENTITY"
elif len(eligible)==0:
    status="REFUSE_NO_VISIBLE_STABLE_COMPLEX_PAIR"
elif len(eligible)>1:
    status="REFUSE_MULTIPLE_VISIBLE_STABLE_COMPLEX_PAIRS"
else:
    status="UNIQUE_VISIBLE_STABLE_COMPLEX_PAIR_CANDIDATE"

result={
 "schema_version":"0.1",
 "project":"Bio Chi Investigation",
 "gate":"Blum 2019 publication-selected B3 full-spectrum modal qualification",
 "freeze":"BIO_CHI/config/BLUM2019_B3_MODAL_P0Q_FREEZE_v0_1.json",
 "source_commit":"5c917abda0618d75c00c9cab45f24ed893dd71f1",
 "source_model":"B3",
 "equilibrium_rhs_inf_norm":resid,
 "equilibrium_pass":bool(resid<=1e-12),
 "measurement_gradient":C.tolist(),
 "jacobian_steps":steps,
 "positive_imag_complex_pair_count_base":len(base),
 "matched_nonreal_pair_relative_spread_max":max_spread,
 "pair_match_ok":pair_match_ok,
 "eligible_visible_stable_complex_pairs":eligible,
 "eligible_visible_stable_complex_pair_count":len(eligible),
 "known_bad_real_diagonal_pass":known_bad_pass,
 "status":status,
 "chi_bio_admitted":False,
 "Chi_bio_admitted":False,
 "Bio_Chi_constructed":False,
 "interpretation":"Complete B3 local spectrum and source-FRET modal visibility only. Scalar admission and chi=1 claims remain prohibited."
}
(OUT/"blum_b3_modal_p0q_v0_1.json").write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
print(json.dumps({k:result[k] for k in ["equilibrium_rhs_inf_norm","positive_imag_complex_pair_count_base","matched_nonreal_pair_relative_spread_max","eligible_visible_stable_complex_pair_count","status"]},indent=2))
if not result["equilibrium_pass"]:
    raise SystemExit("BIO_CHI_BLUM_B3_EQUILIBRIUM_FAIL")
if status=="INDETERMINATE_NUMERICAL_PAIR_IDENTITY":
    raise SystemExit("BIO_CHI_BLUM_B3_MODAL_NUMERICAL_INDETERMINATE")
