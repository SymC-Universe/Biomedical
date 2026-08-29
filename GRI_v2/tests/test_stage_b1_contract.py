import json
from pathlib import Path
import numpy as np

from src.module_network import compute_module_metrics
from src.module_network_accel import compute_module_metrics_accelerated
from src.run_stage_b1 import residualize_expression


def test_stage_b1_plan_is_static_and_fixed_before_results():
    p = json.loads((Path(__file__).parents[1] / "config" / "stage_b1_context_adjustment_plan.json").read_text())
    assert p["status"] == "frozen_after_stage_b0_coverage_before_any_context_network_association"
    assert p["fixed_n_design"]["n"] == 30
    assert p["fixed_n_design"]["resamples_per_cancer_model"] == 100
    assert p["construction_null"]["enabled"] is True
    assert p["constraints"]["chi_allowed"] is False
    assert p["constraints"]["cv2_used"] is False
    assert p["constraints"]["stage_a_metric_redefinition_allowed"] is False


def test_accelerated_metrics_match_frozen_reference_with_missing_data():
    rng = np.random.default_rng(4)
    n = 30
    latent = rng.normal(size=n)
    x = np.column_stack(
        [latent + rng.normal(scale=.2, size=n) for _ in range(6)]
        + [rng.normal(size=n) for _ in range(8)]
    )
    x[0, 0] = np.nan
    genes = [f"M{i}" for i in range(6)] + [f"B{i}" for i in range(8)]
    modules = {"TEST": [f"M{i}" for i in range(6)]}
    kw = dict(
        minimum_mapped_genes=3,
        minimum_gene_finite_fraction=.95,
        minimum_gene_finite_samples=20,
        minimum_pairwise_overlap_fraction=.8,
        minimum_pairwise_overlap_samples=20,
    )
    a = compute_module_metrics(x, genes, modules, **kw)[0]
    b = compute_module_metrics_accelerated(x, genes, modules, **kw)[0]
    assert abs(a.cin_pairwise_median_abs - b.cin_pairwise_median_abs) < 1e-12
    assert abs(a.cin_pc1_variance_fraction - b.cin_pc1_variance_fraction) < 1e-12
    assert abs(a.cout_eigengene_median_abs - b.cout_eigengene_median_abs) < 1e-12


def test_residualization_removes_linear_context_signal():
    rng = np.random.default_rng(5)
    c = rng.normal(size=30)
    x = np.column_stack([
        3 * c + rng.normal(scale=.1, size=30),
        -2 * c + rng.normal(scale=.1, size=30),
    ])
    r = residualize_expression(x, c)
    assert abs(np.corrcoef(r[:, 0], c)[0, 1]) < 1e-10
    assert abs(np.corrcoef(r[:, 1], c)[0, 1]) < 1e-10
