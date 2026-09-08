from __future__ import annotations
from pathlib import Path
import csv, json, hashlib, traceback
import numpy as np
from scipy.optimize import linear_sum_assignment

from src.synthetic_systems import (
    make_linear_system, simulate_linear, simulate_shared_basis_switch,
    simulate_observation_switch, generate_1f, make_noise_bases,
    add_measurement_noise, truth_modes
)
from src.ssi_cov import decompose, fit_from_decomposition
from src.selector import (
    evaluate_scalar_layer, evaluate_modal_layer, evaluate_system_layer,
    positive_complex_indices, match_indices, mac, subspace_similarity,
    participation_tv, crowding_components, select_observable_order,
    cluster_relational_compare
)

ROOT=Path(__file__).resolve().parent
CP=ROOT/'configs'/'phase0d_design.json'
RP=ROOT/'configs'/'frozen_rules.json'
OUT=ROOT/'results'/'phase0d_v01'
OUT.mkdir(parents=True,exist_ok=True)


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def write_csv(path,rows):
    if not rows:
        path.write_text(''); return
    fields=[]
    for r in rows:
        for k in r:
            if k not in fields: fields.append(k)
    with open(path,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader(); w.writerows(rows)


def finite_quantile(values,q):
    a=np.asarray([x for x in values if x is not None and np.isfinite(x)],float)
    return None if len(a)==0 else float(np.quantile(a,q))


def rate(num,den): return None if den==0 else float(num/den)

def admitted(decision): return str(decision).startswith('ADMIT_')

def expected_success(decision,expect):
    if expect=='ADMIT': return admitted(decision)
    if expect=='REFUSE': return not admitted(decision)
    return None


def challenge_scored(spec,N):
    if spec['role']=='null': return True
    if spec['role']!='layer_challenge': return False
    return int(N) in [int(x) for x in spec.get('score_only_n_samples',[])]


def match_truth(true_vals,est_vals,true_indices,est_indices):
    ti=list(true_indices); ei=list(est_indices)
    if not ti or not ei: return []
    cost=np.empty((len(ti),len(ei)),float)
    for a,i in enumerate(ti):
        for b,j in enumerate(ei):
            cost[a,b]=abs(true_vals[i]-est_vals[j])/max(abs(true_vals[i]),1e-12)
    rr,cc=linear_sum_assignment(cost)
    return [(int(ti[a]),int(ei[b]),float(cost[a,b])) for a,b in zip(rr,cc)]


def strong_truth_indices(true_vals,true_shapes,ratio_min,min_hz):
    amp=np.linalg.norm(true_shapes,axis=0)
    ratio=amp/max(float(np.max(amp)),1e-12)
    states=[int(i) for i,x in enumerate(ratio) if x>=float(ratio_min)]
    pos=[i for i in states if true_vals[i].imag/(2*np.pi)>=float(min_hz)]
    return states,pos


def system_truth_score(true_vals,true_shapes,strong_pos,est_vals,est_shapes,min_hz,rules):
    est_pos=list(positive_complex_indices(est_vals,min_hz))
    denom=len(strong_pos)
    if denom==0:
        return {'truth_mode_coverage':0.0,'truth_subspace_similarity':0.0,'truth_channel_participation_TV':1.0,
                'truth_relational_geometry_status':'NO_TRUE_COMPLEX_MODES','truth_relational_geometry_error':np.nan}
    m=match_truth(true_vals,est_vals,strong_pos,est_pos)
    cutoff=float(rules['truth_scoring']['spurious_truth_match_distance_gt'])
    good=[x for x in m if x[2]<=cutoff]
    cov=len(good)/denom
    if len(good)!=denom:
        return {'truth_mode_coverage':cov,'truth_subspace_similarity':0.0,'truth_channel_participation_TV':1.0,
                'truth_relational_geometry_status':'INCOMPLETE_TRUTH_COVERAGE','truth_relational_geometry_error':np.inf}
    tis=[x[0] for x in good]; eis=[x[1] for x in good]
    T=true_shapes[:,tis]; E=est_shapes[:,eis]
    rg=cluster_relational_compare(true_vals[tis],T,est_vals[eis],E,rules['modal_layer']['crowding_ratio_subspace_only_le'])
    return {
        'truth_mode_coverage':cov,
        'truth_subspace_similarity':subspace_similarity(T,E),
        'truth_channel_participation_TV':participation_tv(T,E),
        'truth_relational_geometry_status':rg['status'],
        'truth_relational_geometry_error':rg['distance']
    }


def run():
    cfg=json.loads(CP.read_text()); rules=json.loads(RP.read_text())
    cfg_hash=sha(CP); rules_hash=sha(RP)
    (OUT/'CONFIG_SHA256.txt').write_bytes((cfg_hash+'\n').encode('ascii'))
    (OUT/'RULES_SHA256.txt').write_bytes((rules_hash+'\n').encode('ascii'))

    min_hz=float(rules['common']['complex_frequency_min_hz'])
    ratio_min=float(cfg['strong_observability_ratio_min'])
    maxN=max(cfg['durations_samples'])
    master=np.random.SeedSequence(cfg['seed'])
    children=master.spawn(len(cfg['systems'])*cfg['replicates'])
    ci=0

    layer_rows=[]; scalar_truth_rows=[]; modal_truth_rows=[]; system_truth_rows=[]; failures=[]
    stationary_trials=0; exact_order_agree=0; stationary_scalar_admit=0; stationary_modal_admit=0
    stationary_system_trials=0; stationary_system_admit=0
    strong_complex_total=0; scalar_strong_covered=0; scalar_admitted_est_total=0; scalar_spurious=0
    pole_errors=[]; freq_errors=[]; decay_errors=[]
    modal_truth_total=0; modal_truth_covered=0; individual_truth_macs=[]
    crowded_truth_total=0; crowded_truth_covered=0; crowded_truth_subspaces=[]
    system_truth_coverages=[]; system_truth_subs=[]; system_truth_tvs=[]; system_truth_resolved_rel=[]

    challenge_names=['global_timescale_switch','observation_switch','structural_switch','crowding_transition','null_1f']
    challenge_counts={k:{'n':0,'scalar_success':0,'modal_success':0,'system_success':0} for k in challenge_names}

    for spec in cfg['systems']:
        for rep in range(cfg['replicates']):
            base_rng=np.random.default_rng(children[ci]); ci+=1
            try:
                ss=base_rng.integers(0,2**32-1,size=4,dtype=np.uint32)
                sys_rng=np.random.default_rng(int(ss[0])); proc_rng=np.random.default_rng(int(ss[1])); noise_rng=np.random.default_rng(int(ss[2]))
                true_vals=None; true_shapes=None
                if spec['kind']=='linear':
                    A,C=make_linear_system(spec,cfg['n_channels'],sys_rng)
                    clean=simulate_linear(A,C,cfg['dt_seconds'],maxN,cfg['process_scale'],proc_rng)
                    true_vals,true_shapes=truth_modes(A,C)
                elif spec['kind']=='switch_shared_basis':
                    clean=simulate_shared_basis_switch(spec,cfg['n_channels'],cfg['dt_seconds'],maxN,cfg['process_scale'],sys_rng,proc_rng)
                elif spec['kind']=='observation_switch':
                    clean=simulate_observation_switch(spec,cfg['n_channels'],cfg['dt_seconds'],maxN,cfg['process_scale'],sys_rng,proc_rng)
                elif spec['kind']=='null_1f':
                    clean=generate_1f(maxN,cfg['n_channels'],float(spec['beta']),proc_rng)
                else:
                    raise ValueError('unknown system kind')

                strong_states=[]; strong_pos=[]; target_effective_order=None
                if true_vals is not None:
                    strong_states,strong_pos=strong_truth_indices(true_vals,true_shapes,ratio_min,min_hz)
                    target_effective_order=len(strong_states)

                rho=max(float(x['rho']) for x in cfg['noise_profiles'])
                white_base,colored_base=make_noise_bases(maxN,cfg['n_channels'],rho,noise_rng)

                for profile in cfg['noise_profiles']:
                    noisy_full=add_measurement_noise(clean,profile,white_base,colored_base)
                    for N in cfg['durations_samples']:
                        Y=noisy_full[:N].copy()
                        tid=f"{spec['name']}__r{rep:02d}__{profile['name']}__N{N}"
                        segments={'full':Y,'first_half':Y[:N//2],'second_half':Y[N//2:]}
                        try:
                            decomps={}; fits={}
                            for segn,Ys in segments.items():
                                U,S,p=decompose(Ys,cfg['block_rows']); decomps[segn]=(U,S,p); fits[segn]={}
                                for q in cfg['candidate_orders']:
                                    fits[segn][q]=fit_from_decomposition(U,S,p,q,cfg['dt_seconds'])

                            scalar=evaluate_scalar_layer(fits,decomps,cfg['candidate_orders'],rules)
                            modal=evaluate_modal_layer(fits,decomps,cfg['candidate_orders'],rules)
                            system=evaluate_system_layer(fits,decomps,cfg['candidate_orders'],rules)
                            qfull=select_observable_order(decomps['full'],cfg['candidate_orders'],rules['common'])
                            q1=scalar.get('first_selected_order'); q2=scalar.get('second_selected_order')
                            inflation=''
                            if qfull is not None and q1 is not None and q2 is not None: inflation=int(qfull)-max(int(q1),int(q2))

                            row={
                                'trial_id':tid,'system':spec['name'],'role':spec['role'],'challenge':spec.get('challenge',''),
                                'replicate':rep,'noise_profile':profile['name'],'n_samples':N,
                                'full_selected_order':qfull if qfull is not None else '',
                                'first_selected_order':q1 if q1 is not None else '',
                                'second_selected_order':q2 if q2 is not None else '',
                                'full_minus_max_local_order':inflation,
                                'target_effective_order':target_effective_order if target_effective_order is not None else '',
                                'scalar_decision':scalar['decision'],'modal_decision':modal['decision'],'system_decision':system['decision'],
                                'scalar_split_median_pole_distance':scalar.get('split_median_pole_distance',''),
                                'scalar_first_cross_order_median_pole_distance':scalar.get('first_cross_order_median_pole_distance',''),
                                'scalar_second_cross_order_median_pole_distance':scalar.get('second_cross_order_median_pole_distance',''),
                                'system_split_whole_subspace_similarity':system.get('split_whole_subspace_similarity',''),
                                'system_split_channel_participation_TV':system.get('split_channel_participation_TV',''),
                                'system_split_relational_geometry_status':system.get('split_relational_geometry_status',''),
                                'system_split_relational_pole_geometry_distance':system.get('split_relational_pole_geometry_distance',''),
                                'system_first_cross_order_whole_subspace_similarity':system.get('first_cross_order_whole_subspace_similarity',''),
                                'system_second_cross_order_whole_subspace_similarity':system.get('second_cross_order_whole_subspace_similarity',''),
                                'system_first_cross_order_channel_participation_TV':system.get('first_cross_order_channel_participation_TV',''),
                                'system_second_cross_order_channel_participation_TV':system.get('second_cross_order_channel_participation_TV',''),
                                'system_first_cross_order_relational_geometry_status':system.get('first_cross_order_relational_geometry_status',''),
                                'system_second_cross_order_relational_geometry_status':system.get('second_cross_order_relational_geometry_status',''),
                                'system_first_cross_order_relational_pole_geometry_distance':system.get('first_cross_order_relational_pole_geometry_distance',''),
                                'system_second_cross_order_relational_pole_geometry_distance':system.get('second_cross_order_relational_pole_geometry_distance',''),
                                'expected_scalar':spec.get('expected_scalar','UNSCORED'),'expected_modal':spec.get('expected_modal','UNSCORED'),'expected_system':spec.get('expected_system','UNSCORED'),
                                'challenge_scored':challenge_scored(spec,N)
                            }
                            layer_rows.append(row)

                            if spec['role']=='stationary_truth':
                                stationary_trials+=1
                                if qfull is not None and target_effective_order is not None and int(qfull)==int(target_effective_order): exact_order_agree+=1
                                if admitted(scalar['decision']): stationary_scalar_admit+=1
                                if admitted(modal['decision']): stationary_modal_admit+=1
                                if spec.get('expected_system')=='ADMIT':
                                    stationary_system_trials+=1
                                    if admitted(system['decision']): stationary_system_admit+=1
                                strong_complex_total+=len(strong_pos)

                                if qfull is not None and qfull!=max(cfg['candidate_orders']):
                                    est_vals,est_shapes=fits['full'][int(qfull)]
                                    est_pos=list(positive_complex_indices(est_vals,min_hz))
                                    matches=match_truth(true_vals,est_vals,strong_pos,est_pos)
                                    cutoff=float(rules['truth_scoring']['spurious_truth_match_distance_gt'])

                                    if admitted(scalar['decision']):
                                        scalar_admitted_est_total+=len(est_pos)
                                        matched_est=set()
                                        for ti,ei,dist in matches:
                                            matched_est.add(ei)
                                            tf=abs(true_vals[ti].imag)/(2*np.pi); ef=abs(est_vals[ei].imag)/(2*np.pi)
                                            rel_decay=abs((-est_vals[ei].real)-(-true_vals[ti].real))/max(-true_vals[ti].real,1e-12)
                                            covered=dist<=cutoff
                                            if covered: scalar_strong_covered+=1
                                            pole_errors.append(dist); freq_errors.append(abs(ef-tf)); decay_errors.append(rel_decay)
                                            scalar_truth_rows.append({'trial_id':tid,'true_index':ti,'est_index':ei,'normalized_pole_error':dist,'abs_frequency_error_hz':abs(ef-tf),'relative_decay_error':rel_decay,'covered':bool(covered)})
                                        scalar_spurious+=len([ei for ei in est_pos if ei not in matched_est])
                                        scalar_spurious+=len([1 for _,_,d in matches if d>cutoff])

                                    if admitted(modal['decision']):
                                        map_truth={ti:ei for ti,ei,d in matches if d<=cutoff}
                                        true_pos_vals=np.asarray([true_vals[i] for i in strong_pos],complex)
                                        clusters,singletons,_=crowding_components(true_pos_vals,rules['modal_layer']['crowding_ratio_subspace_only_le'])
                                        for local_i in singletons:
                                            modal_truth_total+=1; ti=strong_pos[local_i]
                                            if ti not in map_truth:
                                                modal_truth_rows.append({'trial_id':tid,'truth_kind':'INDIVIDUAL','true_index':ti,'truth_MAC':0.0,'covered':False}); continue
                                            modal_truth_covered+=1; ei=map_truth[ti]; mval=mac(true_shapes[:,ti],est_shapes[:,ei]); individual_truth_macs.append(mval)
                                            modal_truth_rows.append({'trial_id':tid,'truth_kind':'INDIVIDUAL','true_index':ti,'est_index':ei,'truth_MAC':mval,'covered':True})
                                        for cid,cl in enumerate(clusters):
                                            crowded_truth_total+=1; tis=[strong_pos[x] for x in cl]
                                            if not all(ti in map_truth for ti in tis):
                                                modal_truth_rows.append({'trial_id':tid,'truth_kind':'SUBSPACE','cluster_id':cid,'truth_indices':';'.join(map(str,tis)),'truth_subspace_similarity':0.0,'covered':False}); continue
                                            crowded_truth_covered+=1; eis=[map_truth[ti] for ti in tis]
                                            ssval=subspace_similarity(true_shapes[:,tis],est_shapes[:,eis]); crowded_truth_subspaces.append(ssval)
                                            modal_truth_rows.append({'trial_id':tid,'truth_kind':'SUBSPACE','cluster_id':cid,'truth_indices':';'.join(map(str,tis)),'estimated_indices':';'.join(map(str,eis)),'truth_subspace_similarity':ssval,'covered':True})

                                    if spec.get('expected_system')=='ADMIT' and admitted(system['decision']):
                                        score=system_truth_score(true_vals,true_shapes,strong_pos,est_vals,est_shapes,min_hz,rules)
                                        system_truth_coverages.append(score['truth_mode_coverage'])
                                        system_truth_subs.append(score['truth_subspace_similarity']); system_truth_tvs.append(score['truth_channel_participation_TV'])
                                        if score['truth_relational_geometry_status']=='RESOLVED' and np.isfinite(score['truth_relational_geometry_error']):
                                            system_truth_resolved_rel.append(score['truth_relational_geometry_error'])
                                        system_truth_rows.append({'trial_id':tid,**score})

                            elif challenge_scored(spec,N):
                                name=spec['challenge']; c=challenge_counts[name]; c['n']+=1
                                if expected_success(scalar['decision'],spec['expected_scalar']): c['scalar_success']+=1
                                if expected_success(modal['decision'],spec['expected_modal']): c['modal_success']+=1
                                if expected_success(system['decision'],spec['expected_system']): c['system_success']+=1

                        except Exception as e:
                            failures.append({'trial_id':tid,'system':spec['name'],'error_type':type(e).__name__,'error':str(e),'traceback':traceback.format_exc()})
            except Exception as e:
                failures.append({'trial_id':f"{spec['name']}__r{rep:02d}__BASE",'system':spec['name'],'error_type':type(e).__name__,'error':str(e),'traceback':traceback.format_exc()})

    metrics={
        'stationary_trial_count':stationary_trials,
        'stationary_exact_effective_order_agreement_rate_diagnostic':rate(exact_order_agree,stationary_trials),
        'stationary_scalar_admission_rate':rate(stationary_scalar_admit,stationary_trials),
        'stationary_modal_admission_rate':rate(stationary_modal_admit,stationary_trials),
        'stationary_system_trial_count':stationary_system_trials,
        'stationary_system_admission_rate':rate(stationary_system_admit,stationary_system_trials),
        'strong_complex_scalar_coverage':rate(scalar_strong_covered,strong_complex_total),
        'modal_truth_coverage':rate(modal_truth_covered,modal_truth_total),
        'crowded_truth_coverage':rate(crowded_truth_covered,crowded_truth_total) if crowded_truth_total else 1.0,
        'spurious_admitted_complex_mode_rate':rate(scalar_spurious,scalar_admitted_est_total),
        'admitted_complex_pole_error_p90':finite_quantile(pole_errors,.90),
        'admitted_complex_frequency_error_hz_p90':finite_quantile(freq_errors,.90),
        'admitted_complex_relative_decay_error_p90':finite_quantile(decay_errors,.90),
        'individual_truth_MAC_p10':finite_quantile(individual_truth_macs,.10),
        'crowded_truth_subspace_similarity_p10':finite_quantile(crowded_truth_subspaces,.10),
        'system_truth_mode_coverage_p10':finite_quantile(system_truth_coverages,.10),
        'system_truth_subspace_similarity_p10':finite_quantile(system_truth_subs,.10),
        'system_truth_channel_participation_TV_p90':finite_quantile(system_truth_tvs,.90),
        'system_truth_resolved_relational_geometry_error_p90':finite_quantile(system_truth_resolved_rel,.90),
        'failed_fits':len(failures)
    }
    for name,c in challenge_counts.items():
        metrics[f'{name}_scored_trials']=c['n']
        metrics[f'{name}_scalar_expected_behavior_rate']=rate(c['scalar_success'],c['n'])
        metrics[f'{name}_modal_expected_behavior_rate']=rate(c['modal_success'],c['n'])
        metrics[f'{name}_system_expected_behavior_rate']=rate(c['system_success'],c['n'])

    t=rules['truth_scoring']
    def ge(k,thr): return metrics.get(k) is not None and metrics[k]>=float(thr)
    def le(k,thr): return metrics.get(k) is not None and metrics[k]<=float(thr)
    scalar_checks={
        'mechanical_failures':metrics['failed_fits']<=int(t['mechanical_failures_max']),
        'stationary_scalar_admission_rate':ge('stationary_scalar_admission_rate',t['stationary_scalar_admission_rate_min']),
        'strong_complex_scalar_coverage':ge('strong_complex_scalar_coverage',t['strong_complex_scalar_coverage_min']),
        'spurious_admitted_complex_mode_rate':le('spurious_admitted_complex_mode_rate',t['spurious_admitted_complex_mode_rate_max']),
        'pole_error_p90':le('admitted_complex_pole_error_p90',t['admitted_complex_pole_error_p90_max']),
        'frequency_error_p90':le('admitted_complex_frequency_error_hz_p90',t['admitted_complex_frequency_error_hz_p90_max']),
        'relative_decay_error_p90':le('admitted_complex_relative_decay_error_p90',t['admitted_complex_relative_decay_error_p90_max'])
    }
    modal_checks={
        'mechanical_failures':metrics['failed_fits']<=int(t['mechanical_failures_max']),
        'stationary_modal_admission_rate':ge('stationary_modal_admission_rate',t['stationary_modal_admission_rate_min']),
        'modal_truth_coverage':ge('modal_truth_coverage',t['modal_truth_coverage_min']),
        'crowded_truth_coverage':ge('crowded_truth_coverage',t['crowded_truth_coverage_min']),
        'individual_truth_MAC_p10':ge('individual_truth_MAC_p10',t['individual_truth_MAC_p10_min']),
        'crowded_truth_subspace_p10':ge('crowded_truth_subspace_similarity_p10',t['crowded_truth_subspace_similarity_p10_min'])
    }
    system_checks={
        'mechanical_failures':metrics['failed_fits']<=int(t['mechanical_failures_max']),
        'stationary_system_admission_rate':ge('stationary_system_admission_rate',t['stationary_system_admission_rate_min']),
        'truth_mode_coverage_p10':ge('system_truth_mode_coverage_p10',t['strong_complex_scalar_coverage_min']),
        'truth_subspace_similarity_p10':ge('system_truth_subspace_similarity_p10',t['system_truth_subspace_similarity_p10_min']),
        'truth_channel_participation_TV_p90':le('system_truth_channel_participation_TV_p90',t['system_truth_channel_participation_TV_p90_max']),
        'truth_resolved_relational_geometry_p90':le('system_truth_resolved_relational_geometry_error_p90',t['system_truth_resolved_relational_geometry_error_p90_max'])
    }
    challenge_rule_map={
        'global_timescale_switch':('global_timescale_switch_scalar_refusal_rate_min','global_timescale_switch_modal_admission_rate_min','global_timescale_switch_system_admission_rate_min'),
        'observation_switch':('observation_switch_scalar_admission_rate_min','observation_switch_modal_refusal_rate_min','observation_switch_system_refusal_rate_min'),
        'structural_switch':('structural_switch_scalar_refusal_rate_min','structural_switch_modal_admission_rate_min','structural_switch_system_refusal_rate_min'),
        'crowding_transition':('crowding_transition_scalar_refusal_rate_min','crowding_transition_modal_admission_rate_min','crowding_transition_system_refusal_rate_min'),
        'null_1f':('null_scalar_refusal_rate_min','null_modal_refusal_rate_min','null_system_refusal_rate_min')
    }
    for name,(sk,mk,gk) in challenge_rule_map.items():
        scalar_checks[f'{name}_expected']=ge(f'{name}_scalar_expected_behavior_rate',t[sk])
        modal_checks[f'{name}_expected']=ge(f'{name}_modal_expected_behavior_rate',t[mk])
        system_checks[f'{name}_expected']=ge(f'{name}_system_expected_behavior_rate',t[gk])

    layer_status={
        'scalar_layer':'PASS' if all(scalar_checks.values()) else 'FAIL',
        'modal_layer':'PASS' if all(modal_checks.values()) else 'FAIL',
        'system_layer':'PASS' if all(system_checks.values()) else 'FAIL'
    }
    epistemic='PASS_THREE_LAYER_SYNTHETIC_ADMISSION' if all(v=='PASS' for v in layer_status.values()) else 'PARTIAL_OR_FAILED_HOLDOUT_PRESERVE_DO_NOT_RETUNE'
    summary={
        'schema':'nsd-phase0d-local-order-three-layer-holdout-result-v0.1',
        'config_sha256':cfg_hash,'rules_sha256':rules_hash,'epistemic_status':epistemic,
        'layer_status':layer_status,'metrics':metrics,
        'scalar_checks':scalar_checks,'modal_checks':modal_checks,'system_checks':system_checks,
        'order_note':'Exact effective-order agreement is diagnostic only. Admission is controlled by strong-mode coverage, spurious-mode rate, layer stability, and challenge behavior.',
        'next_gate':'Only prospectively passing layers may enter label-blind EEG adequacy. Preserve any failed layer without threshold retuning on Phase 0D v0.1.',
        'claim_ceiling':rules['claim_ceiling']
    }
    write_csv(OUT/'layer_decisions.csv',layer_rows); write_csv(OUT/'scalar_truth_rows.csv',scalar_truth_rows)
    write_csv(OUT/'modal_truth_rows.csv',modal_truth_rows); write_csv(OUT/'system_truth_rows.csv',system_truth_rows)
    (OUT/'failures.json').write_text(json.dumps(failures,indent=2))
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2))
    (OUT/'WORKING_STATE.json').write_text(json.dumps({
        'status':'COMPLETE','scientific_holdout_status':epistemic,'layer_status':layer_status,
        'config_sha256':cfg_hash,'rules_sha256':rules_hash,'next_gate':summary['next_gate']
    },indent=2))
    print(json.dumps(summary,indent=2))
    return 0


if __name__=='__main__':
    raise SystemExit(run())
