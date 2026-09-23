#!/usr/bin/env python3
from __future__ import annotations

import argparse, csv, gzip, json, re
from collections import Counter, defaultdict
from pathlib import Path
import pandas as pd

PT_RE=re.compile(r"(PT-\d+)",re.I)

def unquote(x):
    s=str(x).strip()
    if len(s)>=2 and s[0]=='"' and s[-1]=='"':
        s=s[1:-1]
    return s.replace('""','"')

def parse_matrix(path: Path):
    meta=defaultdict(list)
    with gzip.open(path,'rt',encoding='utf-8',errors='replace') as f:
        for line in f:
            if not line.startswith('!Sample_'):
                continue
            parts=line.rstrip('\r\n').split('\t')
            key=parts[0][1:]
            vals=[unquote(x) for x in parts[1:]]
            meta[key].append(vals)
    acc=(meta.get('Sample_geo_accession') or [[]])[0]
    title=(meta.get('Sample_title') or [[]])[0]
    platform=(meta.get('Sample_platform_id') or [[]])[0]
    source=(meta.get('Sample_source_name_ch1') or [[]])[0]
    desc=(meta.get('Sample_description') or [[]])[0]
    n=max(map(len,[acc,title,platform,source,desc]+[x for x in meta.get('Sample_characteristics_ch1',[]) ]),default=0)
    def get(v,i): return v[i] if i<len(v) else ''
    rows=[]
    for i in range(n):
        r={
            'gsm':get(acc,i),
            'title':get(title,i),
            'platform':get(platform,i),
            'source_name':get(source,i),
            'description':get(desc,i),
        }
        chars={}
        for charrow in meta.get('Sample_characteristics_ch1',[]):
            val=get(charrow,i).strip()
            if not val: continue
            if ':' in val:
                k,v=val.split(':',1)
                k=k.strip().lower().replace(' ','_').replace('-','_')
                v=v.strip()
            else:
                k='characteristic_unkeyed'
                v=val
            # retain repeated keys losslessly
            if k in chars:
                prev=chars[k]
                chars[k]=prev+' || '+v
            else:
                chars[k]=v
        r['characteristics']=chars
        hay=' '.join([r['title'],r['source_name'],r['description']]+list(chars.values()))
        m=PT_RE.search(hay)
        r['participant']=m.group(1).upper() if m else ''
        title_upper=r['title'].upper()
        if '_NT_' in title_upper or re.search(r'\bNON[- _]?TUMOU?R\b|\bADJACENT\b',hay,re.I):
            r['state']='ADJACENT'
        elif '_T_' in title_upper or re.search(r'\bTUMOU?R\b',hay,re.I):
            r['state']='TUMOR'
        else:
            r['state']='UNKNOWN'
        rows.append(r)
    return rows

def all_fields(rows):
    keys=sorted({k for r in rows for k in r['characteristics']})
    out=[]
    for r in rows:
        z={k:v for k,v in r.items() if k!='characteristics'}
        z.update({k:r['characteristics'].get(k,'') for k in keys})
        out.append(z)
    return out,keys

def classify_key(k):
    x=k.lower()
    biological=['gleason','stage','grade','subtype','phenotype','tumor','cancer','psa','metast','pathologic']
    if any(t in x for t in biological):
        return 'BIOLOGICAL_STATE_NOT_AUTOMATIC_ADJUSTMENT'
    if 'race' in x or 'ancestry' in x or 'ethnic' in x:
        return 'DEMOGRAPHIC_RACE'
    if re.search(r'(^|_)age($|_)',x):
        return 'DEMOGRAPHIC_AGE'
    if 'sex' in x or 'gender' in x:
        return 'DEMOGRAPHIC_SEX'
    if any(t in x for t in ['batch','plate','sentrix','slide','chip','array_position','position','scan','center','centre','site','institution']):
        return 'TECHNICAL_OR_ACQUISITION'
    return 'OTHER'

def numeric_values(vals):
    out=[]
    for v in vals:
        s=str(v).strip()
        if not s: continue
        m=re.fullmatch(r'[-+]?\d+(?:\.\d+)?',s)
        if m:
            out.append(float(s))
    return out

def audit_lane(df, participants, lane):
    sub=df[df.participant.isin(participants) & df.state.eq('TUMOR')].copy()
    counts=sub.groupby('participant').size().to_dict()
    missing=[p for p in participants if counts.get(p,0)==0]
    dup={p:n for p,n in counts.items() if n!=1}
    rows=[]
    base_cols={'series','gsm','title','platform','source_name','description','participant','state'}
    fields=[c for c in sub.columns if c not in base_cols]
    for field in sorted(fields):
        vals=[str(x).strip() for x in sub[field].tolist()]
        non=[x for x in vals if x and x.lower() not in {'nan','na','n/a','none','unknown'}]
        cov=len(non)/len(participants) if participants else 0
        cnt=Counter(non)
        klass=classify_key(field)
        nums=numeric_values(non)
        continuous=(len(nums)==len(non) and len(set(nums))>=8)
        candidate=False
        reason=''
        if klass in {'DEMOGRAPHIC_RACE','DEMOGRAPHIC_AGE','DEMOGRAPHIC_SEX','TECHNICAL_OR_ACQUISITION'} and cov>=.90:
            if continuous and len(nums)>=20:
                candidate=True; reason='continuous_rule_pass'
            elif not continuous:
                big=[n for n in cnt.values() if n>=5]
                if len(big)>=2:
                    candidate=True; reason='categorical_rule_pass'
                else:
                    reason='insufficient_level_support'
        elif klass.startswith('BIOLOGICAL_STATE'):
            reason='biological_state_or_mediator_not_automatic'
        elif cov<.90:
            reason='coverage_below_90pct'
        else:
            reason='not_prespecified_confound_class'
        rows.append({
            'lane':lane,'field':field,'class':klass,'coverage_fraction':cov,
            'nonempty_n':len(non),'unique_n':len(cnt),'continuous':continuous,
            'adjustment_candidate':candidate,'candidate_reason':reason,
            'value_counts_json':json.dumps(dict(cnt.most_common()),sort_keys=True),
        })
    return sub,rows,missing,dup

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--rna',type=Path,required=True)
    ap.add_argument('--m450',type=Path,required=True)
    ap.add_argument('--epic',type=Path,required=True)
    ap.add_argument('--config',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    cfg=json.loads(a.config.read_text())
    series=[]
    for name,path in [('GSE237995',a.rna),('GSE262522',a.m450),('GSE262524',a.epic)]:
        rr=parse_matrix(path)
        flat,keys=all_fields(rr)
        for x in flat:x['series']=name
        series.extend(flat)
    df=pd.DataFrame(series)
    df.to_csv(a.out/'R1_EXTERNAL_METADATA_SAMPLE_MANIFEST.csv',index=False)
    p30=[x.upper() for x in cfg['primary_450k']['selected_participants']]
    p32=[x.upper() for x in cfg['primary_450k']['complete_pair_pool']]
    pe=[x.upper() for x in cfg['epic_sensitivity']['participants']]
    all_aud=[]; identities={}
    for series_name,participants,lane in [
        ('GSE262522',p30,'PRIMARY_450K_N30'),
        ('GSE262522',p32,'SENSITIVITY_450K_N32'),
        ('GSE262524',pe,'SENSITIVITY_EPIC_N26'),
    ]:
        sdf=df[df.series.eq(series_name)].copy()
        sub,rows,missing,dup=audit_lane(sdf,participants,lane)
        all_aud.extend(rows)
        identities[lane]={'expected_n':len(participants),'matched_tumor_n':int(sub.participant.nunique()),'missing':missing,'nonunique':dup}
    audit=pd.DataFrame(all_aud)
    audit.to_csv(a.out/'R1_EXTERNAL_METADATA_FIELD_AUDIT.csv',index=False)
    candidates=audit[audit.adjustment_candidate.eq(True)].copy()
    candidates.to_csv(a.out/'R1_EXTERNAL_METADATA_ADJUSTMENT_CANDIDATES.csv',index=False)
    if any(v['missing'] or v['nonunique'] for v in identities.values()):
        disposition='METADATA_IDENTITY_HOLD'
    else:
        primary=candidates[candidates.lane.eq('PRIMARY_450K_N30')]
        # race already has its own completed sensitivity; still list but do not count as additional
        additional=primary[~primary['class'].eq('DEMOGRAPHIC_RACE')]
        disposition='METADATA_ADJUSTMENT_CANDIDATES_IDENTIFIED' if len(additional) else 'NO_ADDITIONAL_IDENTIFIABLE_TECHNICAL_COVARIATES'
    summary={
        'schema':'biosystems-adversarial-r1-external-metadata-audit-v1',
        'status':'COMPLETE',
        'molecular_outcomes_opened':False,
        'disposition':disposition,
        'identity':identities,
        'primary_adjustment_candidates':candidates[candidates.lane.eq('PRIMARY_450K_N30')][['field','class','coverage_fraction','unique_n','candidate_reason']].to_dict('records'),
        'rule':'metadata-only inventory; no H1/H2/H3 values read',
    }
    (a.out/'R1_EXTERNAL_METADATA_SUMMARY.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
