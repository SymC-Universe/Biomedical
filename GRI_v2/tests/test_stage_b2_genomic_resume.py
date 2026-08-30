from pathlib import Path
import sys
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).parents[1]))
from src.run_stage_b2_genomic import METRICS
from src.run_stage_b2_genomic_resume import summarize_task, task_slug


def synthetic_task_df():
    rows=[]
    modules=['M1','M2','M3']
    for r in range(4):
        for j,m in enumerate(modules):
            row={'analysis_mode':'PRIMARY','coordinate_id':'ANEUPLOIDY_AS','cancer_type':'ACC','eligible_n':50,'resample':r,'module':m}
            for k,metric in enumerate(METRICS):
                ref=.1*j+.01*r+.001*k
                actual=ref+.02
                null=ref+.005
                row[f'reference__{metric}']=ref
                row[f'actual__{metric}']=actual
                row[f'null__{metric}']=null
                row[f'actual_delta__{metric}']=actual-ref
                row[f'null_delta__{metric}']=null-ref
                row[f'specific_delta__{metric}']=actual-null
            rows.append(row)
    return pd.DataFrame(rows)


def test_task_slug_is_deterministic():
    assert task_slug(7,'PRIMARY','ANEUPLOIDY_AS','ACC') == '0007__PRIMARY__ANEUPLOIDY_AS__ACC'


def test_per_task_summary_preserves_specific_delta():
    module,diag=summarize_task(synthetic_task_df())
    assert len(module)==3
    assert diag['valid_resamples']==4
    for metric in METRICS:
        assert np.isclose(diag[f'median_specific_delta__{metric}'],.015)
