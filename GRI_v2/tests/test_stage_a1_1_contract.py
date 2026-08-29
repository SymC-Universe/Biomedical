import json
from pathlib import Path
import numpy as np
from src.module_network import compute_module_metrics


def test_plan_forbids_chi_cv2_composite():
    p = json.loads((Path(__file__).parents[1] / 'config' / 'stage_a1_1_calibration_plan.json').read_text())
    assert p['fixed_n'] == 30 and p['resamples_per_cancer'] == 100 and p['global_seed'] == 20260829
    assert p['constraints']['chi_allowed'] is False
    assert p['constraints']['cv2_used'] is False
    assert p['constraints']['composite_stability_score_allowed'] is False


def test_module_metric_handles_sparse_missing_under_frozen_policy():
    rng = np.random.default_rng(1)
    latent = rng.normal(size=30)
    mod = np.column_stack([latent + rng.normal(scale=.1, size=30) for _ in range(5)])
    bg = rng.normal(size=(30, 8))
    x = np.column_stack([mod, bg])
    x[0, 0] = np.nan
    genes = [f'M{i}' for i in range(5)] + [f'B{i}' for i in range(8)]
    out = compute_module_metrics(
        x, genes, {'TEST': [f'M{i}' for i in range(5)]}, minimum_mapped_genes=3,
        minimum_gene_finite_fraction=.95, minimum_gene_finite_samples=20,
        minimum_pairwise_overlap_fraction=.80, minimum_pairwise_overlap_samples=20,
    )
    assert len(out) == 1
    assert out[0].cin_pairwise_median_abs > .9


def test_windows_launcher_avoids_nested_for_f_command_quoting():
    root = Path(__file__).resolve().parents[1]
    text = (root / 'RUN_STAGE_A1_1_WINDOWS.bat').read_text()
    assert 'for /f "usebackq' not in text.lower()
    assert 'scripts_select_file.py' in text
    assert 'set /p CACHE=<' in text
    assert 'set /p GMT=<' in text
