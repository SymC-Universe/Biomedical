from __future__ import annotations
from pathlib import Path
import csv, json, hashlib, traceback
import numpy as np
from scipy.optimize import linear_sum_assignment

from src.synthetic_systems import (
    make_linear_system, simulate_linear, simulate_switch_fixed, generate_1f,
    make_noise_bases, add_measurement_noise, truth_modes
)
from src.ssi_cov import decompose, fit_from_decomposition
from src.metrics import mac, subspace_similarity
from src.selector import (
    evaluate_model, positive_complex_indices, split_shape_metrics,
    order_mode_persistence, crowding_clusters, cluster_split_subspace
)

ROOT=Path(__file__).resolve().parent
CP=ROOT/"configs"/"phase0c_design.json"
RP=ROOT/"configs"/"frozen_rules.json"
OUT=ROOT/"results"/"phase0c"
OUT.mkdir(parents=True,exist_ok=True)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def write_csv(path,rows,fieldnames=None):
    if not rows:
        path.write_text("")
        return
    if fieldnames is None:
        keys=[]
        for r in rows:
            for k in r:
                if k not in keys: keys.append(k)
        fieldnames=keys
    with open(path,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fieldnames,extrasaction="ignore")
        w.writeheader()
        for r in rows: w.writerow(r)

def quantile_or_none(x,q):
    a=np.asarray([v for v in x if v is not None and np.isfinite(v)],float)
    return None if len(a)==0 else float(np.quantile(a,q))

def run():
    cfg=json.loads(CP.read_text())
    rules=json.loads(RP.read_text())
    cfg_hash=sha(CP); rules_hash=sha(RP)
    (OUT/"CONFIG_SHA256.txt").write_text(cfg_hash+"\n")
    (OUT/"RULES_SHA256.txt").write_text(rules_hash+"\n")

    maxN=max(cfg["durations_samples"])
    master=np.random.SeedSequence(cfg["seed"])
    children=master.spawn(len(cfg["systems"])*cfg["replicates"])
    ci=0
    model_rows=[]; mode_rows=[]; cluster_rows=[]; truth_rows=[]; failures=[]
    stationary_trial_count=0; stationary_admit_count=0; stationary_correct_order=0
    off_trial_count=0; off_refuse_count=0
    strong_complex_total=0; strong_complex_covered=0
    admitted_complex_total=0; spurious_complex=0
    admitted_pole_errors=[]; admitted_freq_errors=[]; admitted_rel_decay_errors=[]
    individual_truth_macs=[]; crowded_truth_subspaces=[]

    for spec in cfg["systems"]:
        for rep in range(cfg["replicates"]):
            base_rng=np.random.default_rng(children[ci]); ci+=1
            try:
                ss=base_rng.integers(0,2**32-1,size=4,dtype=np.uint32)
                sys_rng=np.random.default_rng(int(ss[0]))
                proc_rng=np.random.default_rng(int(ss[1]))
                noise_rng=np.random.default_rng(int(ss[2]))
                true_vals=None; true_shapes=None
                if spec["kind"]=="linear":
                    A,C=make_linear_system(spec,cfg["n_channels"],sys_rng)
                    clean=simulate_linear(A,C,cfg["dt_seconds"],maxN,cfg["process_scale"],proc_rng)
                    true_vals,true_shapes=truth_modes(A,C)
                elif spec["kind"]=="switch_fixed":
                    clean=simulate_switch_fixed(spec,cfg["n_channels"],cfg["dt_seconds"],maxN,cfg["process_scale"],proc_rng)
                elif spec["kind"]=="null_1f":
                    clean=generate_1f(maxN,cfg["n_channels"],float(spec["beta"]),proc_rng)
                else:
                    raise ValueError("unknown system kind")

                rho=max(float(x["rho"]) for x in cfg["noise_profiles"])
                white_base,colored_base=make_noise_bases(maxN,cfg["n_channels"],rho,noise_rng)

                strong_true_state_idx=[]
                strong_true_pos_idx=[]
                target_effective_order=None
                if true_vals is not None:
                    amp=np.linalg.norm(true_shapes,axis=0)
                    ratio=amp/max(float(np.max(amp)),1e-12)
                    strong_true_state_idx=[int(i) for i,v in enumerate(ratio) if v>=float(cfg["strong_observability_ratio_min"])]
                    strong_true_pos_idx=[i for i in strong_true_state_idx if true_vals[i].imag/(2*np.pi)>=float(rules["complex_frequency_min_hz"])]
                    target_effective_order=len(strong_true_state_idx)

                for profile in cfg["noise_profiles"]:
                    noisy_full=add_measurement_noise(clean,profile,white_base,colored_base)
                    for N in cfg["durations_samples"]:
                        Y=noisy_full[:N].copy()
                        tid=f"{spec['name']}__r{rep:02d}__{profile['name']}__N{N}"
                        segments={"full":Y,"first_half":Y[:N//2],"second_half":Y[N//2:]}
                        decomps={}; fits={}
                        try:
                            for segn,Ys in segments.items():
                                U,S,p=decompose(Ys,cfg["block_rows"])
                                decomps[segn]=(U,S,p); fits[segn]={}
                                for q in cfg["candidate_orders"]:
                                    fits[segn][q]=fit_from_decomposition(U,S,p,q,cfg["dt_seconds"])

                            decision=evaluate_model(fits,decomps,cfg["candidate_orders"],rules)
                            q=decision["selected_order"]
                            row={
                                "trial_id":tid,"system":spec["name"],"role":spec["role"],"replicate":rep,
                                "noise_profile":profile["name"],"n_samples":N,
                                "selected_order":q if q is not None else "",
                                "target_effective_order":target_effective_order if target_effective_order is not None else "",
                                "decision":decision["decision"],
                                "complex_split_median_distance":decision.get("complex_split_median_distance",""),
                                "complex_cross_order_median_distance":decision.get("complex_cross_order_median_distance","")
                            }
                            model_rows.append(row)

                            if spec["role"]=="stationary_truth":
                                stationary_trial_count+=1
                                if decision["decision"]=="ADMIT_MODEL":
                                    stationary_admit_count+=1
                                if decision["decision"]=="ADMIT_MODEL" and q is not None and target_effective_order is not None and int(q)==int(target_effective_order):
                                    stationary_correct_order+=1
                                strong_complex_total+=len(strong_true_pos_idx)
                            else:
                                off_trial_count+=1
                                if decision["decision"]!="ADMIT_MODEL":
                                    off_refuse_count+=1

                            if decision["decision"]!="ADMIT_MODEL":
                                continue

                            q=int(q)
                            vals,shapes=fits["full"][q]
                            nextq=sorted(x for x in cfg["candidate_orders"] if x>q)[0]
                            vals_next,shapes_next=fits["full"][nextq]
                            min_hz=float(rules["complex_frequency_min_hz"])
                            split_rows=split_shape_metrics(
                                vals,shapes,
                                fits["first_half"][q][0],fits["first_half"][q][1],
                                fits["second_half"][q][0],fits["second_half"][q][1],
                                min_hz
                            )
                            split_map={r["full_index"]:r for r in split_rows}
                            order_map=order_mode_persistence(vals,shapes,vals_next,shapes_next,min_hz)
                            clusters,_=crowding_clusters(vals,min_hz,float(rules["crowding_ratio_subspace_only_le"]))
                            current_clusters=[]
                            cluster_of={}
                            for cid,cl in enumerate(clusters):
                                for i in cl: cluster_of[i]=cid
                                s1=cluster_split_subspace(cl,vals,shapes,fits["first_half"][q][0],fits["first_half"][q][1],min_hz)
                                s2=cluster_split_subspace(cl,vals,shapes,fits["second_half"][q][0],fits["second_half"][q][1],min_hz)
                                split_ss=float(min(s1,s2)) if np.isfinite(s1) and np.isfinite(s2) else np.nan
                                crow={
                                    "trial_id":tid,"cluster_id":cid,"selected_order":q,
                                    "estimated_indices":";".join(str(i) for i in cl),
                                    "split_subspace_similarity":split_ss,
                                    "claim_status":"ADMIT_SUBSPACE" if np.isfinite(split_ss) and split_ss>=float(rules["split_subspace_similarity_min"]) else "REFUSE_SUBSPACE_UNSTABLE"
                                }
                                cluster_rows.append(crow); current_clusters.append(crow)

                            admitted_est_idx=[]
                            for i,z in enumerate(vals):
                                freq=abs(z.imag)/(2*np.pi)
                                if freq<min_hz:
                                    mode_rows.append({
                                        "trial_id":tid,"selected_order":q,"est_index":i,
                                        "est_real":float(z.real),"est_imag":float(z.imag),"est_frequency_hz":float(freq),
                                        "claim_status":"REFUSE_REAL_POLE_SCALAR","shape_claim":"NONE"
                                    })
                                    continue
                                if z.imag<0:
                                    continue
                                sr=split_map.get(i,{})
                                op=order_map.get(i,{})
                                if i in cluster_of:
                                    cid=cluster_of[i]
                                    crow=current_clusters[cid]
                                    ok=(crow["claim_status"]=="ADMIT_SUBSPACE"
                                        and sr.get("split_pole_distance",np.inf)<=float(rules["complex_split_median_distance_max"])
                                        and op.get("order_pole_distance",np.inf)<=float(rules["complex_cross_order_median_distance_max"]))
                                    status="ADMIT_COMPLEX_POLE_SUBSPACE_SHAPE" if ok else "REFUSE_MODE_UNSTABLE"
                                    shape_claim="SUBSPACE_ONLY" if ok else "NONE"
                                else:
                                    ok=(sr.get("split_pole_distance",np.inf)<=float(rules["complex_split_median_distance_max"])
                                        and op.get("order_pole_distance",np.inf)<=float(rules["complex_cross_order_median_distance_max"])
                                        and sr.get("split_shape_MAC",-np.inf)>=float(rules["individual_split_MAC_min"]))
                                    status="ADMIT_COMPLEX_MODE" if ok else "REFUSE_MODE_UNSTABLE"
                                    shape_claim="INDIVIDUAL" if ok else "NONE"
                                mode_rows.append({
                                    "trial_id":tid,"selected_order":q,"est_index":i,
                                    "est_real":float(z.real),"est_imag":float(z.imag),"est_frequency_hz":float(freq),
                                    "split_pole_distance":sr.get("split_pole_distance",""),
                                    "split_shape_MAC":sr.get("split_shape_MAC",""),
                                    "order_pole_distance":op.get("order_pole_distance",""),
                                    "order_shape_MAC":op.get("order_shape_MAC",""),
                                    "claim_status":status,"shape_claim":shape_claim,
                                    "cluster_id":cluster_of.get(i,"")
                                })
                                if status.startswith("ADMIT_"):
                                    admitted_est_idx.append(i)

                            admitted_complex_total+=len(admitted_est_idx)

                            if true_vals is not None:
                                tpos=np.array(strong_true_pos_idx,dtype=int)
                                epos=np.array(admitted_est_idx,dtype=int)
                                matches=[]
                                if len(tpos) and len(epos):
                                    cost=np.empty((len(tpos),len(epos)))
                                    for a,ti in enumerate(tpos):
                                        for b,ei in enumerate(epos):
                                            cost[a,b]=abs(true_vals[ti]-vals[ei])/max(abs(true_vals[ti]),1e-12)
                                    rr,cc=linear_sum_assignment(cost)
                                    matches=[(int(tpos[a]),int(epos[b]),float(cost[a,b])) for a,b in zip(rr,cc)]
                                matched_e=set()
                                for ti,ei,dist in matches:
                                    matched_e.add(ei)
                                    tf=abs(true_vals[ti].imag)/(2*np.pi)
                                    ef=abs(vals[ei].imag)/(2*np.pi)
                                    rel_decay=abs((-vals[ei].real)-(-true_vals[ti].real))/max(-true_vals[ti].real,1e-12)
                                    is_covered=dist<=float(rules["spurious_truth_match_distance_gt"])
                                    if is_covered: strong_complex_covered+=1
                                    admitted_pole_errors.append(dist)
                                    admitted_freq_errors.append(abs(ef-tf))
                                    admitted_rel_decay_errors.append(rel_decay)
                                    mr=next((x for x in reversed(mode_rows) if x["trial_id"]==tid and x.get("est_index")==ei),None)
                                    shape_claim=mr["shape_claim"] if mr else "NONE"
                                    truth_mac_val=np.nan
                                    if shape_claim=="INDIVIDUAL":
                                        truth_mac_val=mac(true_shapes[:,ti],shapes[:,ei])
                                        individual_truth_macs.append(truth_mac_val)
                                    truth_rows.append({
                                        "trial_id":tid,"true_index":ti,"est_index":ei,
                                        "normalized_pole_error":dist,"abs_frequency_error_hz":abs(ef-tf),
                                        "relative_decay_error":rel_decay,"shape_claim":shape_claim,
                                        "truth_MAC":truth_mac_val if np.isfinite(truth_mac_val) else "",
                                        "covered":bool(is_covered)
                                    })
                                spurious_complex += len([ei for ei in epos if ei not in matched_e])
                                spurious_complex += len([1 for _,_,dist in matches if dist>float(rules["spurious_truth_match_distance_gt"])])

                                for crow in [r for r in current_clusters if r["claim_status"]=="ADMIT_SUBSPACE"]:
                                    cl=[int(x) for x in crow["estimated_indices"].split(";")]
                                    if not cl or len(strong_true_pos_idx)<len(cl): continue
                                    cost=np.empty((len(strong_true_pos_idx),len(cl)))
                                    for a,ti in enumerate(strong_true_pos_idx):
                                        for b,ei in enumerate(cl):
                                            cost[a,b]=abs(true_vals[ti]-vals[ei])/max(abs(true_vals[ti]),1e-12)
                                    rr,cc=linear_sum_assignment(cost)
                                    pairs=[(int(strong_true_pos_idx[a]),int(cl[b]),float(cost[a,b])) for a,b in zip(rr,cc)]
                                    if len(pairs)==len(cl):
                                        tis=[x[0] for x in pairs]; eis=[x[1] for x in pairs]
                                        ss=subspace_similarity(true_shapes[:,tis],shapes[:,eis])
                                        crow["truth_subspace_similarity"]=ss
                                        crowded_truth_subspaces.append(ss)

                        except Exception as e:
                            failures.append({
                                "trial_id":tid,"system":spec["name"],
                                "error_type":type(e).__name__,"error":str(e),
                                "traceback":traceback.format_exc()
                            })
            except Exception as e:
                failures.append({
                    "trial_id":f"{spec['name']}__r{rep:02d}__BASE","system":spec["name"],
                    "error_type":type(e).__name__,"error":str(e),
                    "traceback":traceback.format_exc()
                })

    model_admit_rate=stationary_admit_count/max(stationary_trial_count,1)
    correct_order_rate=stationary_correct_order/max(stationary_trial_count,1)
    off_refusal_rate=off_refuse_count/max(off_trial_count,1)
    coverage=strong_complex_covered/max(strong_complex_total,1)
    spurious_rate=spurious_complex/max(admitted_complex_total,1)
    pole_p90=quantile_or_none(admitted_pole_errors,.90)
    freq_p90=quantile_or_none(admitted_freq_errors,.90)
    decay_p90=quantile_or_none(admitted_rel_decay_errors,.90)
    mac_p10=quantile_or_none(individual_truth_macs,.10)
    sub_p10=quantile_or_none(crowded_truth_subspaces,.10)

    t=rules["admission_targets"]
    checks={
        "mechanical_failures":len(failures)<=int(t["mechanical_failures_max"]),
        "strong_stationary_model_admission_rate":model_admit_rate>=float(t["strong_stationary_model_admission_rate_min"]),
        "correct_effective_order_rate":correct_order_rate>=float(t["strong_stationary_correct_effective_order_rate_min"]),
        "off_model_refusal_rate":off_refusal_rate>=float(t["off_model_refusal_rate_min"]),
        "strong_complex_mode_coverage":coverage>=float(t["strong_complex_mode_coverage_min"]),
        "spurious_admitted_complex_mode_rate":spurious_rate<=float(t["spurious_admitted_complex_mode_rate_max"]),
        "admitted_complex_pole_error_p90":pole_p90 is not None and pole_p90<=float(t["admitted_complex_pole_error_p90_max"]),
        "admitted_complex_frequency_error_p90":freq_p90 is not None and freq_p90<=float(t["admitted_complex_frequency_error_hz_p90_max"]),
        "admitted_complex_relative_decay_error_p90":decay_p90 is not None and decay_p90<=float(t["admitted_complex_relative_decay_error_p90_max"]),
        "individual_truth_MAC_p10":mac_p10 is not None and mac_p10>=float(t["individual_truth_MAC_p10_min"]),
        "crowded_truth_subspace_p10":sub_p10 is not None and sub_p10>=float(t["subspace_truth_similarity_p10_min"])
    }
    holdout_pass=all(checks.values())
    summary={
        "schema":"nsd-phase0c-holdout-result-v0.1",
        "config_sha256":cfg_hash,"rules_sha256":rules_hash,
        "epistemic_status":"HOLDOUT_PASS_SYNTHETIC_STRUCTURE_ONLY" if holdout_pass else "HOLDOUT_FAIL_PRESERVE_DO_NOT_RETUNE",
        "stationary_trial_count":stationary_trial_count,
        "stationary_model_admission_rate":model_admit_rate,
        "correct_effective_order_rate":correct_order_rate,
        "off_model_trial_count":off_trial_count,
        "off_model_refusal_rate":off_refusal_rate,
        "strong_complex_mode_coverage":coverage,
        "spurious_admitted_complex_mode_rate":spurious_rate,
        "admitted_complex_pole_error_p90":pole_p90,
        "admitted_complex_frequency_error_hz_p90":freq_p90,
        "admitted_complex_relative_decay_error_p90":decay_p90,
        "individual_truth_MAC_p10":mac_p10,
        "crowded_truth_subspace_similarity_p10":sub_p10,
        "failed_fits":len(failures),
        "checks":checks,
        "next_gate":"label-blind EEG adequacy only if all checks pass; otherwise preserve holdout failure and revise/narrow method without retuning on Phase 0C",
        "claim_ceiling":rules["claim_ceiling"]
    }
    write_csv(OUT/"model_decisions.csv",model_rows)
    write_csv(OUT/"mode_decisions.csv",mode_rows)
    write_csv(OUT/"cluster_decisions.csv",cluster_rows)
    write_csv(OUT/"truth_score_rows.csv",truth_rows)
    (OUT/"failures.json").write_text(json.dumps(failures,indent=2))
    (OUT/"summary.json").write_text(json.dumps(summary,indent=2))
    (OUT/"WORKING_STATE.json").write_text(json.dumps({
        "status":"COMPLETE","scientific_holdout_status":summary["epistemic_status"],
        "config_sha256":cfg_hash,"rules_sha256":rules_hash,
        "next_gate":summary["next_gate"]
    },indent=2))
    print(json.dumps(summary,indent=2))

if __name__=="__main__":
    run()
