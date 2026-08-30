from __future__ import annotations

import hashlib
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ModalSummary:
    normalized_eigenvalues: np.ndarray
    eigenvectors: np.ndarray
    leading_share: float
    normalized_entropy: float
    effective_rank: float
    participation_ratio: float
    spectral_concentration: float
    mode_feature_contributions: np.ndarray


def _matrix(x, name: str) -> np.ndarray:
    a = np.asarray(x, dtype=float)
    if a.ndim != 2:
        raise ValueError(f"{name} must be a two-dimensional matrix")
    if a.shape[0] < 3 or a.shape[1] < 1:
        raise ValueError(f"{name} has insufficient shape {a.shape}")
    if not np.isfinite(a).all():
        raise ValueError(f"{name} contains non-finite values")
    return a


def stable_seed(namespace: str, *parts: object) -> int:
    payload = "|".join([str(namespace), *[str(p) for p in parts]]).encode("utf-8")
    digest = hashlib.sha256(payload).digest()
    return int.from_bytes(digest[:8], "big", signed=False) % (2**32)


def center_columns(x) -> np.ndarray:
    a = _matrix(x, "x")
    return a - a.mean(axis=0, keepdims=True)


def marginal_permute(x, seed: int) -> np.ndarray:
    a = _matrix(x, "x")
    rng = np.random.default_rng(int(seed))
    out = np.empty_like(a)
    for j in range(a.shape[1]):
        out[:, j] = a[rng.permutation(a.shape[0]), j]
    return out


def row_permute(x, seed: int) -> np.ndarray:
    a = _matrix(x, "x")
    rng = np.random.default_rng(int(seed))
    return a[rng.permutation(a.shape[0]), :]


def modal_summary(x, top_modes: int = 5) -> ModalSummary:
    a = center_columns(x)
    n, p = a.shape
    gram = (a @ a.T) / float(p)
    values, vectors = np.linalg.eigh(gram)
    order = np.argsort(values)[::-1]
    values = values[order]
    vectors = vectors[:, order]

    scale = float(np.sum(np.abs(values)))
    tol = 1e-10 * max(scale, 1.0)
    if float(values.min()) < -tol:
        raise ValueError("sample-space Gram matrix has a materially negative eigenvalue")
    values = np.where(values < 0.0, 0.0, values)

    # Column centering creates one guaranteed zero sample-space mode. Keep the
    # remaining n-1 modal slots, including any additional zeros from rank loss.
    values = values[: n - 1]
    vectors = vectors[:, : n - 1]
    total = float(values.sum())
    if not np.isfinite(total) or total <= 0.0:
        raise ValueError("total modal variance is zero")

    q = values / total
    positive = q > 0.0
    entropy = float(-np.sum(q[positive] * np.log(q[positive])))
    max_modes = n - 1
    h_norm = float(entropy / np.log(max_modes)) if max_modes > 1 else 0.0
    effective_rank = float(np.exp(entropy))
    participation = float(1.0 / np.sum(q * q))
    s_spec = float(1.0 - h_norm)

    k = max(0, min(int(top_modes), len(values)))
    contributions = np.zeros((k, p), dtype=float)
    for mode in range(k):
        lam = float(values[mode])
        if lam <= 0.0:
            continue
        u = vectors[:, mode]
        projection = a.T @ u
        contributions[mode, :] = (projection * projection) / (float(p) * lam)

    return ModalSummary(
        normalized_eigenvalues=q,
        eigenvectors=vectors[:, :k].copy(),
        leading_share=float(q[0]),
        normalized_entropy=h_norm,
        effective_rank=effective_rank,
        participation_ratio=participation,
        spectral_concentration=s_spec,
        mode_feature_contributions=contributions,
    )


def linear_cka(x, y) -> float:
    a = center_columns(x)
    b = center_columns(y)
    if a.shape[0] != b.shape[0]:
        raise ValueError("x and y must contain the same number of samples")
    k = a @ a.T
    l = b @ b.T
    denom = float(np.linalg.norm(k, ord="fro") * np.linalg.norm(l, ord="fro"))
    if denom <= 0.0 or not np.isfinite(denom):
        raise ValueError("CKA denominator is zero")
    return float(np.sum(k * l) / denom)


def principal_angles(x, y, top_k: int = 5) -> np.ndarray:
    a = center_columns(x)
    b = center_columns(y)
    if a.shape[0] != b.shape[0]:
        raise ValueError("x and y must contain the same number of samples")

    ua, sa, _ = np.linalg.svd(a, full_matrices=False)
    ub, sb, _ = np.linalg.svd(b, full_matrices=False)
    eps_a = np.finfo(float).eps * max(a.shape) * (float(sa[0]) if len(sa) else 0.0)
    eps_b = np.finfo(float).eps * max(b.shape) * (float(sb[0]) if len(sb) else 0.0)
    rank_a = int(np.sum(sa > eps_a))
    rank_b = int(np.sum(sb > eps_b))
    k = min(int(top_k), rank_a, rank_b)
    if k < 1:
        raise ValueError("one layer has zero modal rank")

    cosines = np.linalg.svd(ua[:, :k].T @ ub[:, :k], compute_uv=False)
    cosines = np.clip(cosines, 0.0, 1.0)
    return np.arccos(cosines)


def residualize_covariates(x, covariates) -> np.ndarray:
    a = _matrix(x, "x")
    z = np.asarray(covariates, dtype=float)
    if z.ndim == 1:
        z = z[:, None]
    if z.ndim != 2 or z.shape[0] != a.shape[0]:
        raise ValueError("covariates must have one row per sample")
    if not np.isfinite(z).all():
        raise ValueError("covariates contain non-finite values")
    design = np.column_stack([np.ones(a.shape[0], dtype=float), z])
    projection = design @ np.linalg.pinv(design)
    return (np.eye(a.shape[0], dtype=float) - projection) @ a


def _average_ranks(x: np.ndarray) -> np.ndarray:
    values = np.asarray(x, dtype=float)
    if values.ndim != 1 or not np.isfinite(values).all():
        raise ValueError("rank input must be a finite vector")
    order = np.argsort(values, kind="mergesort")
    sorted_values = values[order]
    ranks = np.empty(len(values), dtype=float)
    i = 0
    while i < len(values):
        j = i + 1
        while j < len(values) and sorted_values[j] == sorted_values[i]:
            j += 1
        avg = 0.5 * ((i + 1) + j)
        ranks[order[i:j]] = avg
        i = j
    return ranks


def spearman(x, y) -> float:
    a = np.asarray(x, dtype=float)
    b = np.asarray(y, dtype=float)
    if a.ndim != 1 or b.ndim != 1 or len(a) != len(b) or len(a) < 3:
        raise ValueError("Spearman inputs must be equal-length vectors of length >=3")
    ra = _average_ranks(a)
    rb = _average_ranks(b)
    ra = ra - ra.mean()
    rb = rb - rb.mean()
    denom = float(np.linalg.norm(ra) * np.linalg.norm(rb))
    if denom <= 0.0:
        return float("nan")
    return float(np.dot(ra, rb) / denom)


def same_module_abs_spearman(layer_a, layer_b) -> tuple[float, np.ndarray]:
    a = _matrix(layer_a, "layer_a")
    b = _matrix(layer_b, "layer_b")
    if a.shape != b.shape:
        raise ValueError("module score matrices must have identical shape")
    values = np.array([abs(spearman(a[:, j], b[:, j])) for j in range(a.shape[1])], dtype=float)
    finite = values[np.isfinite(values)]
    if len(finite) == 0:
        raise ValueError("no finite module correlations")
    return float(np.median(finite)), values


def semantic_label_effect(layer_a, layer_b, seed: int) -> dict[str, float]:
    a = _matrix(layer_a, "layer_a")
    b = _matrix(layer_b, "layer_b")
    if a.shape != b.shape:
        raise ValueError("module score matrices must have identical shape")
    observed, _ = same_module_abs_spearman(a, b)
    rng = np.random.default_rng(int(seed))
    perm = rng.permutation(a.shape[1])
    null_value, _ = same_module_abs_spearman(a[:, perm], b)
    return {
        "observed": observed,
        "label_null": null_value,
        "effect": float(observed - null_value),
    }


def _pca_train_scores(train: np.ndarray, test: np.ndarray, requested_k: int) -> tuple[np.ndarray, np.ndarray]:
    mean = train.mean(axis=0, keepdims=True)
    train_c = train - mean
    test_c = test - mean
    _, s, vt = np.linalg.svd(train_c, full_matrices=False)
    if len(s) == 0:
        raise ValueError("PCA training matrix has zero rank")
    eps = np.finfo(float).eps * max(train_c.shape) * float(s[0])
    rank = int(np.sum(s > eps))
    k = min(int(requested_k), rank)
    if k < 1:
        raise ValueError("PCA training matrix has zero rank")
    loadings = vt[:k, :].T
    return train_c @ loadings, test_c @ loadings


def cross_validated_modal_predictability(
    source,
    target,
    *,
    source_modes: int = 5,
    target_modes: int = 5,
    alpha: float = 1.0,
    folds: int = 5,
    seed: int = 0,
) -> dict[str, float]:
    x = _matrix(source, "source")
    y = _matrix(target, "target")
    if x.shape[0] != y.shape[0]:
        raise ValueError("source and target must contain the same samples")
    n = x.shape[0]
    if folds < 2 or folds > n // 2:
        raise ValueError("folds must be between 2 and n//2")
    if alpha < 0.0:
        raise ValueError("alpha must be nonnegative")

    rng = np.random.default_rng(int(seed))
    indices = rng.permutation(n)
    test_folds = [f for f in np.array_split(indices, int(folds)) if len(f) > 0]
    total_sse = 0.0
    total_sst = 0.0

    for test_idx in test_folds:
        train_mask = np.ones(n, dtype=bool)
        train_mask[test_idx] = False
        train_idx = np.flatnonzero(train_mask)

        x_train = x[train_idx]
        x_test = x[test_idx]
        y_train = y[train_idx]
        y_test = y[test_idx]

        xs_train, xs_test = _pca_train_scores(x_train, x_test, source_modes)
        ys_train, ys_test = _pca_train_scores(y_train, y_test, target_modes)

        gram = xs_train.T @ xs_train
        ridge = gram + float(alpha) * np.eye(gram.shape[0], dtype=float)
        coef = np.linalg.pinv(ridge) @ xs_train.T @ ys_train
        prediction = xs_test @ coef

        total_sse += float(np.sum((ys_test - prediction) ** 2))
        total_sst += float(np.sum(ys_test**2))

    if total_sst <= 0.0:
        raise ValueError("target test variance is zero")
    r2 = float(1.0 - total_sse / total_sst)
    return {
        "cv_modal_r2": r2,
        "bounded_dependence": float(np.clip(r2, 0.0, 1.0)),
        "candidate_autonomy_from_raw_r2": float(1.0 - np.clip(r2, 0.0, 1.0)),
    }


def predictability_permutation_calibration(
    source,
    target,
    *,
    source_modes: int = 5,
    target_modes: int = 5,
    alpha: float = 1.0,
    folds: int = 5,
    permutations: int = 50,
    seed: int = 0,
) -> dict[str, object]:
    if permutations < 1:
        raise ValueError("permutations must be >=1")
    observed = cross_validated_modal_predictability(
        source,
        target,
        source_modes=source_modes,
        target_modes=target_modes,
        alpha=alpha,
        folds=folds,
        seed=seed,
    )["cv_modal_r2"]

    x = _matrix(source, "source")
    null = []
    for i in range(int(permutations)):
        perm_seed = stable_seed("PREDICTABILITY_NULL", seed, i)
        xp = row_permute(x, perm_seed)
        value = cross_validated_modal_predictability(
            xp,
            target,
            source_modes=source_modes,
            target_modes=target_modes,
            alpha=alpha,
            folds=folds,
            seed=stable_seed("PREDICTABILITY_CV", seed, i),
        )["cv_modal_r2"]
        null.append(float(value))

    null_array = np.asarray(null, dtype=float)
    null_median = float(np.median(null_array))
    excess = float(observed - null_median)
    p_upper = float((1 + np.sum(null_array >= observed)) / (len(null_array) + 1))
    bounded_excess = float(np.clip(excess, 0.0, 1.0))
    return {
        "observed_cv_modal_r2": float(observed),
        "null_median_cv_modal_r2": null_median,
        "dependence_excess_over_null": excess,
        "candidate_autonomy_score": float(1.0 - bounded_excess),
        "permutation_p_upper": p_upper,
        "null_values": null_array,
    }
