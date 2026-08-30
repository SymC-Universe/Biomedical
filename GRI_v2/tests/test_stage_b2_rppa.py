import numpy as np
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parents[1]))
from src.run_stage_b2_rppa import protein_metrics,bridge,residualize_matrix


def test_permutation_preserves_protein_only_metrics():
    rng=np.random.default_rng(1);p=rng.normal(size=(30,20));perm=rng.permutation(30)
    a=protein_metrics(p);b=protein_metrics(p[perm])
    assert np.allclose(a,b,atol=1e-12)


def test_bridge_matches_manual_median_absolute_correlation():
    rng=np.random.default_rng(2)
    e=rng.normal(size=(30,3))
    p=rng.normal(size=(30,5))
    observed=bridge(e,p)
    manual=np.empty(3,float)
    for i in range(3):
        manual[i]=np.median([abs(np.corrcoef(e[:,i],p[:,j])[0,1]) for j in range(5)])
    assert np.allclose(observed,manual,atol=1e-12)


def test_bridge_detects_panel_wide_cross_assay_alignment():
    rng=np.random.default_rng(3)
    latent=rng.normal(size=30)
    e=np.column_stack([latent,rng.normal(size=(30,2))])
    p=np.column_stack([latent+0.05*rng.normal(size=30) for _ in range(9)])
    aligned=bridge(e,p)[0]
    perm=rng.permutation(30)
    broken=bridge(e,p[perm])[0]
    assert aligned > 0.9
    assert aligned > broken + 0.5


def test_residualization_removes_covariate():
    c=np.arange(30,dtype=float);x=np.column_stack([2*c+1,-c+3]);r=residualize_matrix(x,c)
    assert r is not None
    assert np.max(np.abs(r)) < 1e-10
