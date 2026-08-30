import numpy as np
import pandas as pd
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1]))
from src.run_stage_b2_genomic import residualize_expression, attach_source


def test_residualization_removes_linear_covariate():
    c = np.arange(30, dtype=float)
    x = np.column_stack([2.0*c + 3.0, -0.5*c + 7.0])
    r = residualize_expression(x, c)
    assert r is not None
    assert abs(np.corrcoef(r[:,0], c)[0,1]) < 1e-10 or np.std(r[:,0]) < 1e-10


def test_unique_patient_fallback_only():
    stage = pd.DataFrame({
        'sample_id':['TCGA-AA-0001-01A-X','TCGA-AA-0002-01A-X'],
        'patient_id':['TCGA-AA-0001','TCGA-AA-0002'],
        'cancer_type':['X','X'],
        'sample_root':['TCGA-AA-0001-01A','TCGA-AA-0002-01A'],
    })
    src = pd.DataFrame({'id':['TCGA-AA-0001-01','TCGA-AA-0002-01','TCGA-AA-0002-01'], 'v':['1','2','3']})
    out = attach_source(stage, src, 'id', ['v'])
    assert out.loc[0,'v'] == 1.0
    assert np.isnan(out.loc[1,'v'])


def test_residualization_rejects_constant_covariate():
    x = np.arange(60,dtype=float).reshape(30,2)
    c = np.ones(30)
    assert residualize_expression(x,c) is None


def test_fast_complete_path_matches_frozen_accelerated(tmp_path):
    from src import run_stage_b2_genomic as m
    from src.module_network_accel import compute_module_metrics_accelerated
    rng = np.random.default_rng(7)
    x = rng.normal(size=(30, 20))
    genes = np.array([f'G{i}' for i in range(20)])
    modules = {'M': [f'G{i}' for i in range(15)]}
    m.G['genes'] = genes
    m.G['modules'] = modules
    m.G['module_indices'] = {'M': np.arange(15)}
    fast = m.compute_metrics(x)['M']
    slow_obj = compute_module_metrics_accelerated(x, genes, modules, minimum_mapped_genes=15, minimum_gene_finite_fraction=.95, minimum_gene_finite_samples=20, minimum_pairwise_overlap_fraction=.8, minimum_pairwise_overlap_samples=20)[0]
    slow = {k: float(getattr(slow_obj,k)) for k in m.METRICS}
    for k in m.METRICS:
        assert abs(fast[k] - slow[k]) < 1e-10
