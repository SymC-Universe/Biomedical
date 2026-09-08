from pathlib import Path
import csv,json,hashlib,traceback
import numpy as np
from src.synthetic_systems import make_system,simulate,continuous_truth
from src.ssi_cov import ssi_cov,continuous_modes
from src.metrics import match_modes,mac,pole_summary
ROOT=Path(__file__).resolve().parent; CP=ROOT/'configs'/'phase0_structure.json'; OUT=ROOT/'results'/'phase0_structure'; OUT.mkdir(parents=True,exist_ok=True)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
    cfg=json.loads(CP.read_text()); ch=sha(CP); (OUT/'CONFIG_SHA256.txt').write_text(ch+'\n')
    total=len(cfg['systems'])*len(cfg['noise_conditions'])*len(cfg['n_samples'])*cfg['replicates']; ss=np.random.SeedSequence(cfg['seed']).spawn(total); si=0; rows=[]; fails=[]
    for sc in cfg['systems']:
      for nc in cfg['noise_conditions']:
       for N in cfg['n_samples']:
        for rep in range(cfg['replicates']):
         rng=np.random.default_rng(ss[si]); si+=1; tid=f"{sc['name']}__{nc['name']}__N{N}__r{rep:02d}"
         try:
          A,C=make_system(sc['modes'],cfg['n_channels'],rng); Y,_=simulate(A,C,cfg['dt_seconds'],N,nc['process_scale'],nc['observation_scale'],rng)
          tv,ts=continuous_truth(A,C); Fh,Ch,S=ssi_cov(Y,cfg['latent_order'],cfg['block_rows']); ev,es=continuous_modes(Fh,Ch,cfg['dt_seconds'])
          for ti,ei,pd in match_modes(tv,ev):
           td,tf,tc=pole_summary(tv[ti]); ed,ef,ec=pole_summary(ev[ei])
           rows.append({'trial_id':tid,'system':sc['name'],'noise':nc['name'],'n_samples':N,'replicate':rep,'true_index':ti,'est_index':ei,'true_real':tv[ti].real,'true_imag':tv[ti].imag,'est_real':ev[ei].real,'est_imag':ev[ei].imag,'normalized_pole_error':pd,'mode_shape_MAC':mac(ts[:,ti],es[:,ei]),'true_decay_per_s':td,'est_decay_per_s':ed,'true_frequency_hz':tf,'est_frequency_hz':ef,'secondary_true_chi':tc,'secondary_est_chi':ec,'largest_singular_value':float(S[0]),'status':'CANDIDATE_ENGINEERING_ONLY'})
         except Exception as e: fails.append({'trial_id':tid,'error_type':type(e).__name__,'error':str(e),'traceback':traceback.format_exc()})
    if rows:
      with open(OUT/'trial_results.csv','w',newline='',encoding='utf-8') as f: w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    (OUT/'failures.json').write_text(json.dumps(fails,indent=2))
    pe=np.array([r['normalized_pole_error'] for r in rows]); ma=np.array([r['mode_shape_MAC'] for r in rows]); fe=np.array([abs(r['est_frequency_hz']-r['true_frequency_hz']) for r in rows]); de=np.array([abs(r['est_decay_per_s']-r['true_decay_per_s']) for r in rows])
    summary={'schema':'nsd-phase0-structure-result-v0.1','config_sha256':ch,'engineering_status':'DIAGNOSTIC_ONLY_NO_ADMISSION_GATE','trials_expected':total,'modal_rows':len(rows),'failed_trials':len(fails),'median_normalized_pole_error':float(np.nanmedian(pe)) if len(pe) else None,'p90_normalized_pole_error':float(np.nanpercentile(pe,90)) if len(pe) else None,'median_mode_shape_MAC':float(np.nanmedian(ma)) if len(ma) else None,'p10_mode_shape_MAC':float(np.nanpercentile(ma,10)) if len(ma) else None,'median_abs_frequency_error_hz':float(np.nanmedian(fe)) if len(fe) else None,'median_abs_decay_error_per_s':float(np.nanmedian(de)) if len(de) else None,'claim_ceiling':'Engineering comparison of known synthetic latent structure to an output-only SSI-COV candidate. No EEG, diagnosis, treatment, clinical admission threshold, model-order selection, or whole-system scalar.'}
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)); (OUT/'WORKING_STATE.json').write_text(json.dumps({'status':'COMPLETE' if not fails else 'COMPLETE_WITH_FAILURES','config_sha256':ch,'trials_expected':total,'failed_trials':len(fails),'next_gate':'review engineering recovery; then freeze prospective synthetic acceptance criteria or reject candidate'},indent=2)); print(json.dumps(summary,indent=2))
if __name__=='__main__': run()
