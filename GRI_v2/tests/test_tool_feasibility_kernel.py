from __future__ import annotations

import numpy as np

from src.tool_feasibility_kernel import (
    cross_validated_modal_predictability,
    linear_cka,
    marginal_permute,
    modal_summary,
    predictability_permutation_calibration,
    principal_angles,
    residualize_covariates,
    same_module_abs_spearman,
    semantic_label_effect,
    stable_seed,
)


def _patient_effect(x, y, seed=123):
    observed = linear_cka(x, y)
    rng = np.random.default_rng(seed)
    null = linear_cka(x[rng.permutation(len(x))], y)
    return observed - null


def test_stable_seed_is_reproducible_and_order_sensitive():
    a = stable_seed("TEST", "A", 1, "B")
    b = stable_seed("TEST", "A", 1, "B")
    c = stable_seed("TEST", "B", 1, "A")
    assert a == b
    assert a != c
    assert 0 <= a < 2**32


def test_modal_summary_and_feature_contributions_close_exactly():
    rng = np.random.default_rng(11)
    z = rng.normal(size=(30, 3))
    x = z @ rng.normal(size=(3, 120)) + 0.15 * rng.normal(size=(30, 120))
    s = modal_summary(x, top_modes=5)
    assert s.normalized_eigenvalues.shape == (29,)
    assert np.isclose(s.normalized_eigenvalues.sum(), 1.0, atol=1e-10)
    assert s.mode_feature_contributions.shape == (5, 120)
    assert np.allclose(s.mode_feature_contributions.sum(axis=1), 1.0, atol=1e-8)
    assert 0.0 <= s.normalized_entropy <= 1.0
    assert 0.0 <= s.spectral_concentration <= 1.0
    assert 1.0 <= s.effective_rank <= 29.0
    assert 1.0 <= s.participation_ratio <= 29.0


def test_marginal_permutation_preserves_every_feature_empirical_distribution():
    rng = np.random.default_rng(12)
    x = rng.normal(size=(30, 40))
    xp = marginal_permute(x, 991)
    assert np.allclose(np.sort(x, axis=0), np.sort(xp, axis=0))
    assert np.allclose(x.mean(axis=0), xp.mean(axis=0))
    assert np.allclose(x.var(axis=0), xp.var(axis=0))


def test_structured_layer_has_more_spectral_concentration_than_marginal_null():
    rng = np.random.default_rng(13)
    z = rng.normal(size=(30, 2))
    x = z @ rng.normal(size=(2, 200)) + 0.35 * rng.normal(size=(30, 200))
    observed = modal_summary(x).spectral_concentration
    null = modal_summary(marginal_permute(x, 1401)).spectral_concentration
    assert observed > null + 0.15


def test_shared_patient_geometry_exceeds_independent_patient_effect():
    rng = np.random.default_rng(14)
    n = 60
    z = rng.normal(size=(n, 3))
    x = z @ rng.normal(size=(3, 100)) + 0.5 * rng.normal(size=(n, 100))
    y_shared = z @ rng.normal(size=(3, 120)) + 0.5 * rng.normal(size=(n, 120))
    y_independent = rng.normal(size=(n, 120))
    shared_effect = _patient_effect(x, y_shared, 1402)
    independent_effect = _patient_effect(x, y_independent, 1402)
    assert shared_effect > 0.20
    assert shared_effect > independent_effect + 0.15


def test_principal_angles_are_small_for_shared_modes_and_larger_for_independent():
    rng = np.random.default_rng(15)
    n = 60
    z = rng.normal(size=(n, 3))
    x = z @ rng.normal(size=(3, 80)) + 0.15 * rng.normal(size=(n, 80))
    y = z @ rng.normal(size=(3, 90)) + 0.15 * rng.normal(size=(n, 90))
    independent = rng.normal(size=(n, 90))
    shared_angles = principal_angles(x, y, top_k=3)
    independent_angles = principal_angles(x, independent, top_k=3)
    assert float(np.median(shared_angles)) < 0.35
    assert float(np.median(independent_angles)) > float(np.median(shared_angles)) + 0.45


def test_common_confounder_alignment_collapses_after_projection():
    rng = np.random.default_rng(16)
    n = 70
    z = rng.normal(size=(n, 1))
    x = 2.0 * z @ rng.normal(size=(1, 100)) + 0.7 * rng.normal(size=(n, 100))
    y = 2.0 * z @ rng.normal(size=(1, 120)) + 0.7 * rng.normal(size=(n, 120))
    raw_effect = _patient_effect(x, y, 1601)
    xr = residualize_covariates(x, z)
    yr = residualize_covariates(y, z)
    adjusted_effect = _patient_effect(xr, yr, 1601)
    assert raw_effect > 0.20
    assert adjusted_effect < raw_effect - 0.15
    assert abs(adjusted_effect) < 0.12


def test_semantic_label_null_distinguishes_corresponding_modules_from_scramble():
    rng = np.random.default_rng(17)
    n, modules = 70, 16
    latent = rng.normal(size=(n, modules))
    a = latent + 0.35 * rng.normal(size=(n, modules))
    b = latent + 0.35 * rng.normal(size=(n, modules))

    semantic = semantic_label_effect(a, b, seed=1701)
    scrambled = np.roll(a, 5, axis=1)
    scrambled_semantic = semantic_label_effect(scrambled, b, seed=1701)

    assert semantic["observed"] > 0.75
    assert semantic["effect"] > 0.45
    assert scrambled_semantic["observed"] < 0.35
    # Feature-label permutation leaves global linear sample geometry unchanged.
    assert np.isclose(linear_cka(a, b), linear_cka(scrambled, b), atol=1e-12)


def test_cross_validated_modal_predictability_separates_shared_from_independent():
    rng = np.random.default_rng(18)
    n = 90
    z = rng.normal(size=(n, 4))
    source = z @ rng.normal(size=(4, 80)) + 0.45 * rng.normal(size=(n, 80))
    shared_target = z @ rng.normal(size=(4, 90)) + 0.45 * rng.normal(size=(n, 90))
    independent_target = rng.normal(size=(n, 90))

    shared = cross_validated_modal_predictability(source, shared_target, source_modes=4, target_modes=4, alpha=0.5, folds=5, seed=1801)
    independent = cross_validated_modal_predictability(source, independent_target, source_modes=4, target_modes=4, alpha=0.5, folds=5, seed=1801)

    assert shared["cv_modal_r2"] > 0.55
    assert shared["cv_modal_r2"] > independent["cv_modal_r2"] + 0.50


def test_candidate_autonomy_distinguishes_shared_plus_private_from_dominantly_predictable_target():
    rng = np.random.default_rng(19)
    n = 100
    shared = rng.normal(size=(n, 3))
    private = rng.normal(size=(n, 5))
    source = shared @ rng.normal(size=(3, 100)) + 0.35 * rng.normal(size=(n, 100))

    low_autonomy_target = shared @ rng.normal(size=(3, 100)) + 0.30 * rng.normal(size=(n, 100))
    high_autonomy_target = (
        shared @ rng.normal(size=(3, 100))
        + 1.7 * private @ rng.normal(size=(5, 100))
        + 0.30 * rng.normal(size=(n, 100))
    )

    low = predictability_permutation_calibration(
        source,
        low_autonomy_target,
        source_modes=5,
        target_modes=5,
        alpha=0.5,
        folds=5,
        permutations=12,
        seed=1901,
    )
    high = predictability_permutation_calibration(
        source,
        high_autonomy_target,
        source_modes=5,
        target_modes=5,
        alpha=0.5,
        folds=5,
        permutations=12,
        seed=1901,
    )

    assert low["candidate_autonomy_score"] < 0.45
    assert high["candidate_autonomy_score"] > low["candidate_autonomy_score"] + 0.25


def test_confounder_generated_false_autonomy_loss_is_removed_by_residualization():
    rng = np.random.default_rng(20)
    n = 100
    confounder = rng.normal(size=(n, 2))
    target_private = rng.normal(size=(n, 4))
    source = 2.5 * confounder @ rng.normal(size=(2, 90)) + 0.5 * rng.normal(size=(n, 90))
    target = (
        2.5 * confounder @ rng.normal(size=(2, 90))
        + 1.2 * target_private @ rng.normal(size=(4, 90))
        + 0.5 * rng.normal(size=(n, 90))
    )

    raw = predictability_permutation_calibration(
        source,
        target,
        source_modes=5,
        target_modes=5,
        alpha=0.5,
        folds=5,
        permutations=12,
        seed=2001,
    )
    source_adj = residualize_covariates(source, confounder)
    target_adj = residualize_covariates(target, confounder)
    adjusted = predictability_permutation_calibration(
        source_adj,
        target_adj,
        source_modes=5,
        target_modes=5,
        alpha=0.5,
        folds=5,
        permutations=12,
        seed=2001,
    )

    assert raw["candidate_autonomy_score"] < 0.65
    assert adjusted["candidate_autonomy_score"] > raw["candidate_autonomy_score"] + 0.20


def test_same_module_spearman_handles_ties_and_reports_vector():
    a = np.column_stack([
        np.arange(12, dtype=float),
        np.repeat([0.0, 1.0, 2.0], 4),
    ])
    b = a.copy()
    median_value, values = same_module_abs_spearman(a, b)
    assert np.allclose(values, 1.0)
    assert np.isclose(median_value, 1.0)
