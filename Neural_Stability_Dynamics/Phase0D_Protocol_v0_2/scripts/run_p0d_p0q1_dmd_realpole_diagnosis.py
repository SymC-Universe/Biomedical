from __future__ import annotations
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
import numpy as np
from scripts.run_p0q1_rank_signal_holdout import _load_freeze,_refusal_record
from src.rank_gate import _candidate_from_sweep
from src.rank_sweep import sweep_subspace_dmd,adjacent_rank_stability

cfg=_load_freeze(ROOT/'configs/P0Q1_RANK_SIGNAL_FREEZE.json'); rule=cfg['rank_signal_rule']; grid=cfg['candidate_grid']
rows=[]
for rep in range(cfg['replicates_per_family']):
    Y=_refusal_record(cfg,'real_pole_only_linear_system',rep)
    sw=sweep_subspace_dmd(Y,cfg['dt'],grid)
    gate=_candidate_from_sweep(sw,grid,rule['gap_ratio_min'],rule['complex_frequency_min_hz'])
    ranks=[]
    for r in grid:
        fit=sw['fits'][r]; item={'rank':r,'gap':fit.get('singular_gap_ratio'),'status':fit.get('status')}
        if fit.get('status')=='OK':
            vals=np.asarray(fit['vals'],complex)
            item['poles']=[{'real':float(z.real),'imag':float(z.imag),'hz':float(z.imag/(2*np.pi))} for z in vals]
            item['unstable']=int(np.sum(vals.real>=0)); item['positive_complex']=int(np.sum(vals.imag/(2*np.pi)>=rule['complex_frequency_min_hz']))
        ranks.append(item)
    rows.append({'replicate':rep,'gate':gate,'ranks':ranks,'adjacent_rank_stability':adjacent_rank_stability(sw,rule['complex_frequency_min_hz'])})
out={'schema':'nsd-p0d-p0q1-dmd-realpole-diagnosis-v1','status':'P0_D_RETROSPECTIVE_NONINDEPENDENT','p0q1_status':'SUBSPACE_DMD_FAILS_P0Q1_UNCHANGED','truth':'two stable real continuous-time poles -0.7 and -2.4; no oscillatory mode','records':rows,'nonclaims':['No P0Q1 result is rescored or repaired.','No revised rank gate is selected from these records.','Any rule motivated here requires a new version and untouched P0-Q evidence.']}
p=ROOT/'results/p0d_mapping/p0q1_dmd_realpole_diagnosis.json'; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(p)
for x in rows: print(json.dumps({'replicate':x['replicate'],'gate':x['gate'],'selected_rank_record':next(r for r in x['ranks'] if r['rank']==x['gate'].get('candidate_rank'))},sort_keys=True))
