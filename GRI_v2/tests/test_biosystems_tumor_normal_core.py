from __future__ import annotations

import math

import numpy as np
import pandas as pd

from src import biosystems_tumor_normal_core as tn


def frozen_center_rna_missing_n30(expr30: np.ndarray) -> np.ndarray:
    x = np.asarray(expr30, dtype=float)
    if x.ndim != 2 or x.shape[0] != 30:
        raise ValueError
    finite = np.isfinite(x)
    if finite.all():
        return x - x.mean(axis=0, keepdims=True)
    counts = finite.sum(axis=0)
    safe = np.where(finite, x, 0.0)
    means = np.divide(safe.sum(axis=0), counts, out=np.zeros(x.shape[1], dtype=float), where=counts > 0)
    return np.where(finite, x - means[None, :], 0.0)


def frozen_methylation_pc1_n30(gene_matrix: np.ndarray):
    m = np.asarray(gene_matrix, dtype=float)
    if m.ndim != 2 or m.shape[0] != 30 or not np.isfinite(m).all():
        raise ValueError
    xc = m - m.mean(axis=0, keepdims=True)
    u, s, vt = np.linalg.svd(xc, full_matrices=False)
    eig = u[:, 0] * s[0]
    load = vt[0].copy()
    mean_state = np.mean(m, axis=1)
    if np.std(eig, ddof=1) > 0 and np.std(mean_state, ddof=1) > 0:
        pr = float(np.corrcoef(eig, mean_state)[0, 1])
        if pr < 0:
            eig = -eig
            load = -load
        elif pr == 0:
            j = int(np.argmax(np.abs(load)))
            if load[j] < 0:
                eig = -eig
                load = -load
    else:
        j = int(np.argmax(np.abs(load)))
        if load[j] < 0:
            eig = -eig
            load = -load
    return eig, load


def frozen_rna_hallmark_pc1_n30(raw: np.ndarray, minimum_genes: int = 15):
    x = np.asarray(raw, dtype=float)
    if x.ndim != 2 or x.shape[0] != 30:
        raise ValueError
    finite = np.isfinite(x)
    counts = finite.sum(axis=0)
    required = max(20, int(math.ceil(0.95 * x.shape[0])))
    sd = np.nanstd(x, axis=0, ddof=1)
    valid = (counts >= required) & np.isfinite(sd) & (sd > 0)
    if int(valid.sum()) < int(minimum_genes):
        raise ValueError
    xv = x[:, valid]
    mean = np.nanmean(xv, axis=0)
    sdv = np.nanstd(xv, axis=0, ddof=1)
    z = (xv - mean) / sdv
    imputed = ~np.isfinite(z)
    z = np.where(np.isfinite(z), z, 0.0)
    u, s, _ = np.linalg.svd(z, full_matrices=False)
    eig = u[:, 0] * s[0]
    mean_state = np.mean(z, axis=1)
    if np.std(eig, ddof=1) > 0 and np.std(mean_state, ddof=1) > 0:
        if float(np.corrcoef(eig, mean_state)[0, 1]) < 0:
            eig = -eig
    return eig, int(valid.sum()), float(imputed.sum() / imputed.size if imputed.size else 0.0)


def frozen_centered_kernel(x: np.ndarray) -> np.ndarray:
    a = np.asarray(x, float)
    k = a @ a.T
    n = k.shape[0]
    h = np.eye(n) - np.ones((n, n)) / float(n)
    return h @ k @ h


def frozen_cka(ka: np.ndarray, kb: np.ndarray) -> float:
    den = float(np.linalg.norm(ka, "fro") * np.linalg.norm(kb, "fro"))
    return float(np.sum(ka * kb) / den)


def frozen_rank_columns(x: np.ndarray) -> np.ndarray:
    a = np.asarray(x, dtype=float)
    if a.ndim == 1:
        a = a[:, None]
    out = np.full_like(a, np.nan, dtype=float)
    for j in range(a.shape[1]):
        s = pd.Series(a[:, j], dtype=float)
        good = s.notna()
        if int(good.sum()) >= 3:
            r = s[good].rank(method="average").to_numpy(dtype=float, copy=True)
            r -= r.mean()
            den = np.sqrt(np.sum(r * r))
            if den > 0:
                out[np.flatnonzero(good.to_numpy()), j] = r / den
    return out


def frozen_same_hallmark(a: np.ndarray, b: np.ndarray) -> float:
    ar = frozen_rank_columns(a)
    br = frozen_rank_columns(b)
    v = np.nansum(ar * br, axis=0)
    return float(np.nanmedian(np.abs(v)))


def test_n30_rna_centering_equivalence():
    rng = np.random.default_rng(123)
    x = rng.normal(size=(30, 41))
    x[2, 3] = np.nan
    x[8, 3] = np.nan
    x[:, 7] = np.nan
    got = tn.center_rna_missing(x)
    ref = frozen_center_rna_missing_n30(x)
    assert np.array_equal(np.isnan(got), np.isnan(ref))
    assert np.allclose(got, ref, atol=1e-12, rtol=0)


def test_n30_methylation_pc1_equivalence():
    rng = np.random.default_rng(456)
    x = rng.random((30, 23))
    ge, gl = tn.methylation_pc1(x)
    re, rl = frozen_methylation_pc1_n30(x)
    assert np.allclose(ge, re, atol=1e-12, rtol=1e-12)
    assert np.allclose(gl, rl, atol=1e-12, rtol=1e-12)


def test_n30_rna_hallmark_pc1_equivalence():
    rng = np.random.default_rng(789)
    x = rng.normal(size=(30, 22))
    x[0, 0] = np.nan
    ge, gn, gi = tn.rna_hallmark_pc1(x, minimum_genes=15)
    re, rn, ri = frozen_rna_hallmark_pc1_n30(x, minimum_genes=15)
    assert gn == rn
    assert gi == ri
    assert np.allclose(ge, re, atol=1e-12, rtol=1e-12)


def test_n30_cka_equivalence():
    rng = np.random.default_rng(321)
    a = rng.normal(size=(30, 50))
    b = rng.normal(size=(30, 37))
    ga = tn.centered_kernel(a)
    gb = tn.centered_kernel(b)
    ra = frozen_centered_kernel(a)
    rb = frozen_centered_kernel(b)
    assert np.allclose(ga, ra, atol=1e-12, rtol=0)
    assert np.allclose(gb, rb, atol=1e-12, rtol=0)
    assert abs(tn.cka_kernels(ga, gb) - frozen_cka(ra, rb)) < 1e-14


def test_n30_same_hallmark_equivalence():
    rng = np.random.default_rng(654)
    a = rng.normal(size=(30, 31))
    b = rng.normal(size=(30, 31))
    assert abs(tn.same_hallmark_fast(a, b) - frozen_same_hallmark(a, b)) < 1e-14


def test_n20_generalized_rules_are_well_defined():
    rng = np.random.default_rng(987)
    m = rng.random((20, 18))
    r = rng.normal(size=(20, 20))
    eig_m, _ = tn.methylation_pc1(m)
    eig_r, n_genes, _ = tn.rna_hallmark_pc1(r, minimum_genes=15)
    assert eig_m.shape == (20,)
    assert eig_r.shape == (20,)
    assert n_genes == 20
    assert np.isfinite(eig_m).all()
    assert np.isfinite(eig_r).all()


def test_n20_rna_rule_requires_all_20_finite():
    rng = np.random.default_rng(741)
    x = rng.normal(size=(20, 15))
    x[0, 0] = np.nan
    try:
        tn.rna_hallmark_pc1(x, minimum_genes=15)
    except ValueError:
        pass
    else:
        raise AssertionError("n=20 should lose a gene with one missing value under max(20,ceil(.95*n))")


def test_two_sided_sign_test():
    pos, neg, ties, p = tn.exact_sign_test_two_sided([1, 1, 1, 1, -1])
    assert (pos, neg, ties) == (4, 1, 0)
    assert abs(p - 0.375) < 1e-15
