from __future__ import annotations

import argparse, hashlib, json
from pathlib import Path
import numpy as np
import pandas as pd


def sha256_file(path: str | Path) -> str:
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()


def stable_seed(global_seed:int,*parts:str)->int:
    payload=(str(global_seed)+'|'+'|'.join(parts)).encode()
    return int.from_bytes(hashlib.sha256(payload).digest()[:8],'little',signed=False)


def tcga_ids(s: pd.Series):
    s=s.astype(str)
    return pd.DataFrame({
      'patient_id':s.str.extract(r'(TCGA-[A-Z0-9]{2}-[A-Z0-9]{4})',expand=False),
      'sample_root':s.str.extract(r'(TCGA-[A-Z0-9]{2}-[A-Z0-9]{4}-[0-9]{2}[A-Z])',expand=False),
      'sample_type':s.str.extract(r'TCGA-[A-Z0-9]{2}-[A-Z0-9]{4}-([0-9]{2})',expand=False),
    })


def build_rppa_alignment(cache_path, rppa_path):
    npz=np.load(cache_path,allow_pickle=True)
    stage=pd.DataFrame({'sample_id':npz['sample_ids'].astype(str),'patient_id':npz['patient_ids'].astype(str),'cancer_type':npz['cancer_types'].astype(str)})
    stage['sample_root']=stage.sample_id.str.extract(r'(TCGA-[A-Z0-9]{2}-[A-Z0-9]{4}-[0-9]{2}[A-Z])',expand=False)
    r=pd.read_csv(rppa_path,sep='\t')
    ids=tcga_ids(r.SampleID);r=pd.concat([r,ids],axis=1);r=r[r.sample_type.eq('01')].copy()
    roots=r.groupby('sample_root').size();unique_roots=set(roots[roots==1].index)
    pats=r.groupby('patient_id').size();unique_pats=set(pats[pats==1].index)
    root_map={x:i for i,x in zip(r.index,r.sample_root) if x in unique_roots}
    pat_map={x:i for i,x in zip(r.index,r.patient_id) if x in unique_pats}
    ridx=np.full(len(stage),-1,dtype=int);method=np.full(len(stage),'none',dtype=object)
    for i,row in enumerate(stage.itertuples(index=False)):
        if row.sample_root in root_map: ridx[i]=root_map[row.sample_root];method[i]='exact_sample_root'
        elif row.patient_id in pat_map: ridx[i]=pat_map[row.patient_id];method[i]='unique_patient_fallback'
    feature_cols=[c for c in r.columns if c not in {'SampleID','TumorType','patient_id','sample_root','sample_type'}]
    matched=np.flatnonzero(ridx>=0)
    X=r.loc[ridx[matched],feature_cols].apply(pd.to_numeric,errors='coerce').to_numpy(float)
    finite=np.isfinite(X).mean(axis=0);sd=np.nanstd(X,axis=0,ddof=1)
    keep=(finite>=.95)&np.isfinite(sd)&(sd>0)
    kept=[c for c,k in zip(feature_cols,keep) if k]
    if len(kept)!=189: raise ValueError(f'Frozen RPPA common panel expected 189 features, found {len(kept)}')
    P=np.full((len(stage),len(kept)),np.nan,dtype=float)
    P[matched]=r.loc[ridx[matched],kept].apply(pd.to_numeric,errors='coerce').to_numpy(float)
    if not np.isfinite(P[matched]).all(): raise ValueError('Frozen 189-feature RPPA common panel is not complete in matched samples')
    stage['rppa_match_method']=method
    return stage,P,kept


def load_eigengenes(path, stage):
    e=pd.read_csv(path,compression='infer')
    required={'cancer_type','module','sample_id','eigengene'}
    if not required.issubset(e.columns):raise ValueError('eigengene file missing required columns')
    if e.duplicated(['sample_id','module']).any():raise ValueError('eigengene file has duplicate sample-module rows')
    wide=e.pivot(index='sample_id',columns='module',values='eigengene')
    modules=sorted(wide.columns.astype(str))
    if len(modules)!=50:raise ValueError(f'expected 50 Hallmark eigengenes, found {len(modules)}')
    wide=wide.reindex(stage.sample_id)
    if wide.isna().any().any():raise ValueError('Stage A eigengene matrix not complete for Stage A sample universe')
    return wide.to_numpy(float),modules


def attach_b1_context(stage,b1_path):
    b=pd.read_csv(b1_path)
    if b.sample_id.duplicated().any():raise ValueError('B1 context not unique by sample_id')
    out=stage.merge(b[['sample_id','purity','leukocyte_fraction']],on='sample_id',how='left',validate='one_to_one')
    if not np.array_equal(out.sample_id.to_numpy(str),stage.sample_id.to_numpy(str)):
        raise ValueError('B1 context merge changed Stage A sample order')
    return out


def residualize_matrix(x,c):
    x=np.asarray(x,float);c=np.asarray(c,float)
    if c.ndim==1:c=c[:,None]
    if not np.isfinite(x).all() or not np.isfinite(c).all():return None
    c=(c-c.mean(0))/c.std(0,ddof=1)
    if not np.isfinite(c).all():return None
    d=np.column_stack([np.ones(len(c)),c])
    if np.linalg.matrix_rank(d)<d.shape[1]:return None
    beta=np.linalg.lstsq(d,x,rcond=None)[0]
    return x-d@beta


def zscore_complete(x):
    x=np.asarray(x,float);sd=x.std(0,ddof=1);valid=np.isfinite(sd)&(sd>0)
    if not valid.all():return None
    return (x-x.mean(0))/sd


def protein_metrics(p):
    z=zscore_complete(p)
    if z is None:return None
    n=z.shape[0]
    corr=z.T@z/float(n-1);iu=np.triu_indices(z.shape[1],1)
    pair=float(np.median(np.abs(corr[iu])))
    gram=z@z.T;vals=np.linalg.eigvalsh(gram);lam=max(float(vals[-1]),0.0);den=float(np.trace(gram))
    return pair,float(lam/den) if den>0 else float('nan')


def bridge(e,p):
    ze=zscore_complete(e);zp=zscore_complete(p)
    if ze is None or zp is None:return None
    corr=ze.T@zp/float(len(e)-1)
    return np.median(np.abs(corr),axis=1)


def q05(s):return s.quantile(.05)
def q95(s):return s.quantile(.95)
q05.__name__='p05';q95.__name__='p95'


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--cache',required=True);ap.add_argument('--eigengenes',required=True);ap.add_argument('--rppa',required=True)
    ap.add_argument('--b1-context',required=True);ap.add_argument('--plan',required=True);ap.add_argument('--out',required=True)
    args=ap.parse_args();plan=json.loads(Path(args.plan).read_text())
    checks={'stage_a_profile_cache_sha256':sha256_file(args.cache),'stage_a_module_eigengenes_sha256':sha256_file(args.eigengenes),'stage_b1_context_matched_sha256':sha256_file(args.b1_context),'rppa_sha256':sha256_file(args.rppa)}
    for k,v in checks.items():
        if v!=plan['inputs'][k]:raise ValueError(f'SHA mismatch for {k}: {v}')
    stage,P,features=build_rppa_alignment(args.cache,args.rppa);stage=attach_b1_context(stage,args.b1_context)
    E,modules=load_eigengenes(args.eigengenes,stage)
    n=int(plan['rppa']['fixed_n']);reps=int(plan['rppa']['resamples_per_cancer']);seed=int(plan['rppa']['global_seed'])
    rows=[];task_rows=[]
    for mode in ['PRIMARY','CONTEXT_SENSITIVITY']:
      for cancer in sorted(stage.cancer_type.unique()):
        mask=(stage.cancer_type.to_numpy()==cancer)&np.isfinite(P).all(axis=1)
        if mode=='CONTEXT_SENSITIVITY':mask &= np.isfinite(stage.purity.to_numpy(float))&np.isfinite(stage.leukocyte_fraction.to_numpy(float))
        eligible=np.flatnonzero(mask)
        if len(eligible)<n:continue
        rng=np.random.default_rng(stable_seed(seed,'sample',mode,cancer));valid=0
        for r in range(reps):
            sel=np.sort(rng.choice(eligible,n,replace=False));p=P[sel];e=E[sel]
            pm=protein_metrics(p)
            if pm is None:continue
            perm=np.random.default_rng(stable_seed(seed,'perm',mode,cancer,str(r))).permutation(n)
            raw=bridge(e,p);raw_null=bridge(e,p[perm])
            if raw is None or raw_null is None:continue
            if mode=='CONTEXT_SENSITIVITY':
                c=stage.loc[sel,['purity','leukocyte_fraction']].to_numpy(float)
                ea=residualize_matrix(e,c);pa=residualize_matrix(p,c)
                if ea is None or pa is None:continue
                actual=bridge(ea,pa);null=bridge(ea,pa[perm])
                if actual is None or null is None:continue
            else:
                actual=raw;null=raw_null
            valid+=1
            for j,module in enumerate(modules):
                rows.append({'analysis_mode':mode,'cancer_type':cancer,'eligible_n':len(eligible),'resample':r,'module':module,
                  'rppa_pairwise_median_abs':pm[0],'rppa_pc1_variance_fraction':pm[1],
                  'raw_rna_rppa_coupling':float(raw[j]),'raw_null_coupling':float(raw_null[j]),'raw_specific_coupling':float(raw[j]-raw_null[j]),
                  'analysis_coupling':float(actual[j]),'analysis_null_coupling':float(null[j]),'analysis_specific_coupling':float(actual[j]-null[j])})
        task_rows.append({'analysis_mode':mode,'cancer_type':cancer,'eligible_n':len(eligible),'valid_resamples':valid})
        print(f'{mode} {cancer} n={len(eligible)} valid={valid}',flush=True)
    rawdf=pd.DataFrame(rows);tasks=pd.DataFrame(task_rows)
    if (tasks.valid_resamples!=reps).any():raise RuntimeError('not all RPPA tasks produced all frozen resamples')
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    rawdf.to_csv(out/'stage_b2_rppa_resample_metrics.csv.gz',index=False,compression={'method':'gzip','compresslevel':1})
    tasks.to_csv(out/'stage_b2_rppa_task_status.csv',index=False)
    value=['rppa_pairwise_median_abs','rppa_pc1_variance_fraction','raw_rna_rppa_coupling','raw_null_coupling','raw_specific_coupling','analysis_coupling','analysis_null_coupling','analysis_specific_coupling']
    agg=rawdf.groupby(['analysis_mode','cancer_type','module'])[value].agg(['median',q05,q95]);agg.columns=[f'{a}__{b}' for a,b in agg.columns];mod=agg.reset_index();mod.to_csv(out/'stage_b2_rppa_module_effects.csv',index=False)
    cancer=mod.groupby(['analysis_mode','cancer_type']).agg(
      module_count=('module','size'),
      median_rppa_pairwise=('rppa_pairwise_median_abs__median','median'),
      median_rppa_pc1=('rppa_pc1_variance_fraction__median','median'),
      median_raw_coupling=('raw_rna_rppa_coupling__median','median'),
      median_raw_specific=('raw_specific_coupling__median','median'),
      median_analysis_coupling=('analysis_coupling__median','median'),
      median_analysis_specific=('analysis_specific_coupling__median','median'),
    ).reset_index();cancer.to_csv(out/'stage_b2_rppa_cancer_diagnostic.csv',index=False)
    summary={'status':'DEVELOPMENT_ORTHOGONAL_STATIC_RPPA_INTEGRATION_ONLY','claim_ceiling':plan['claim_ceiling'],'chi_present':False,'cv2_used':False,'composite_score_present':False,
      'matched_stage_a_samples':int(np.isfinite(P).all(axis=1).sum()),'common_panel_features':len(features),'modules':len(modules),'fixed_n':n,'resamples_per_task':reps,
      'tasks':len(tasks),'tasks_by_mode':tasks.groupby('analysis_mode').size().astype(int).to_dict(),'minimum_valid_resamples':int(tasks.valid_resamples.min()),
      'raw_rows':len(rawdf),'module_summary_rows':len(mod),'cancer_summary_rows':len(cancer),'source_sha256':checks}
    (out/'STAGE_B2_RPPA_SUMMARY.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    (out/'stage_b2_rppa_common_panel.txt').write_text('\n'.join(features)+'\n')
    print(json.dumps(summary,indent=2,sort_keys=True))

if __name__=='__main__':main()
