from __future__ import annotations

import hashlib
import math
from pathlib import Path
from typing import Sequence

import numpy as np
import pandas as pd


def sha256_file(path: Path, chunk: int = 16 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as fh:
        for block in iter(lambda: fh.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def stable_seed(namespace: str, *parts: object) -> int:
    payload = "|".join([namespace] + [str(x) for x in parts]).encode("utf-8")
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "big", signed=False) % (2**32)


def parse_gmt(path: Path) -> dict[str, list[str]]:
    modules: dict[str, list[str]] = {}
    with Path(path).open("r", encoding="utf-8", errors="strict") as fh:
        for line in fh:
            parts = line.rstrip("\r\n").split("\t")
            if len(parts) >= 3:
                name = parts[0].strip()
                genes = [g.strip() for g in parts[2:] if g.strip()]
                if name and genes:
                    modules[name] = list(dict.fromkeys(genes))
    if len(modules) != 50 or any(not x.startswith("HALLMARK_") for x in modules):
        raise ValueError(f"expected exactly 50 HALLMARK modules; found {len(modules)}")
    return modules


def bh_fdr(pvalues: Sequence[float]) -> np.ndarray:
    p = np.asarray(pvalues, dtype=float)
    out = np.full(p.shape, np.nan, dtype=float)
    good = np.flatnonzero(np.isfinite(p))
    if len(good) == 0:
        return out
    vals = p[good]
    order = np.argsort(vals, kind="mergesort")
    ranked = vals[order]
    m = len(ranked)
    q = ranked * m / np.arange(1, m + 1, dtype=float)
    q = np.minimum.accumulate(q[::-1])[::-1]
    q = np.minimum(q, 1.0)
    tmp = np.empty_like(q)
    tmp[order] = q
    out[good] = tmp
    return out


def exact_sign_test_two_sided(values: Sequence[float]) -> tuple[int, int, int, float]:
    vals = np.asarray(values, dtype=float)
    vals = vals[np.isfinite(vals)]
    pos = int(np.sum(vals > 0))
    neg = int(np.sum(vals < 0))
    ties = int(np.sum(vals == 0))
    n = pos + neg
    if n == 0:
        return pos, neg, ties, float("nan")
    k = min(pos, neg)
    tail = sum(math.comb(n, j) for j in range(0, k + 1)) / (2**n)
    return pos, neg, ties, float(min(1.0, 2.0 * tail))


def _rank_columns(x: np.ndarray) -> np.ndarray:
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


def spearman(x: Sequence[float], y: Sequence[float]) -> float:
    a = np.asarray(x, float)
    b = np.asarray(y, float)
    good = np.isfinite(a) & np.isfinite(b)
    if int(good.sum()) < 3:
        return float("nan")
    ra = pd.Series(a[good]).rank(method="average").to_numpy(dtype=float)
    rb = pd.Series(b[good]).rank(method="average").to_numpy(dtype=float)
    if np.std(ra, ddof=1) <= 0 or np.std(rb, ddof=1) <= 0:
        return float("nan")
    return float(np.corrcoef(ra, rb)[0, 1])


def center_rna_missing(x: np.ndarray) -> np.ndarray:
    """Sample-size-generalized C1 v2.2 full-modal RNA binding."""
    a = np.asarray(x, dtype=float)
    if a.ndim != 2 or a.shape[0] < 3:
        raise ValueError(f"RNA matrix must be n x genes with n>=3, got {a.shape}")
    finite = np.isfinite(a)
    if finite.all():
        return a - a.mean(axis=0, keepdims=True)
    counts = finite.sum(axis=0)
    safe = np.where(finite, a, 0.0)
    means = np.divide(safe.sum(axis=0), counts, out=np.zeros(a.shape[1], dtype=float), where=counts > 0)
    centered = np.where(finite, a - means[None, :], 0.0)
    if not np.isfinite(centered).all():
        raise ValueError("RNA missingness binding produced non-finite centered values")
    if not np.allclose(centered.sum(axis=0), 0.0, atol=1e-10, rtol=0.0):
        raise ValueError("RNA centered-column sum drift")
    return centered


def centered_kernel(x: np.ndarray) -> np.ndarray:
    a = np.asarray(x, float)
    if a.ndim != 2 or a.shape[0] < 3:
        raise ValueError("kernel input must be n x features")
    k = a @ a.T
    n = k.shape[0]
    h = np.eye(n) - np.ones((n, n), dtype=float) / float(n)
    return h @ k @ h


def cka_kernels(ka: np.ndarray, kb: np.ndarray) -> float:
    a = np.asarray(ka, float)
    b = np.asarray(kb, float)
    if a.shape != b.shape or a.ndim != 2 or a.shape[0] != a.shape[1]:
        raise ValueError("CKA kernels must be same-shape square matrices")
    den = float(np.linalg.norm(a, "fro") * np.linalg.norm(b, "fro"))
    return float(np.sum(a * b) / den) if den > 0 and np.isfinite(den) else float("nan")


def cka_row_perm_nulls(ka: np.ndarray, kb: np.ndarray, perms: np.ndarray) -> np.ndarray:
    a = np.asarray(ka, float)
    b = np.asarray(kb, float)
    den = float(np.linalg.norm(a, "fro") * np.linalg.norm(b, "fro"))
    if den <= 0 or not np.isfinite(den):
        return np.full(len(perms), np.nan)
    out = np.empty(len(perms), float)
    for i, p in enumerate(np.asarray(perms, dtype=int)):
        kp = a[np.ix_(p, p)]
        out[i] = float(np.sum(kp * b) / den)
    return out


def permutation_matrix(namespace: str, cancer: str, track: str, rep: int, test: str,
                       n: int, b: int) -> np.ndarray:
    seed = stable_seed(namespace, cancer, track, rep, test, "patient_null")
    rng = np.random.default_rng(seed)
    return np.vstack([rng.permutation(n) for _ in range(b)]).astype(np.int16)


def h2_headroom(observed: float, null_median: float) -> float:
    if not (np.isfinite(observed) and np.isfinite(null_median)):
        return float("nan")
    den = 1.0 - float(null_median)
    if den <= 0:
        return float("nan")
    return float((observed - null_median) / den)


def same_hallmark_fast(a: np.ndarray, b: np.ndarray) -> float:
    if np.asarray(a).shape != np.asarray(b).shape:
        raise ValueError("Hallmark score matrices must match")
    ar = _rank_columns(a)
    br = _rank_columns(b)
    vals = np.nansum(ar * br, axis=0)
    return float(np.nanmedian(np.abs(vals)))


def same_hallmark_patient_nulls(a: np.ndarray, b: np.ndarray, perms: np.ndarray) -> np.ndarray:
    ar = _rank_columns(a)
    br = _rank_columns(b)
    out = np.empty(len(perms), float)
    for i, p in enumerate(np.asarray(perms, dtype=int)):
        vals = np.nansum(ar[p, :] * br, axis=0)
        out[i] = float(np.nanmedian(np.abs(vals)))
    return out


def methylation_pc1(m: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """C1 methylation Hallmark PC1 generalized from fixed n=30 to arbitrary n."""
    a = np.asarray(m, dtype=float)
    if a.ndim != 2 or a.shape[0] < 3 or not np.isfinite(a).all():
        raise ValueError("methylation Hallmark matrix invalid")
    xc = a - a.mean(axis=0, keepdims=True)
    if np.allclose(xc, 0):
        raise ValueError("methylation Hallmark has zero variation")
    u, s, vt = np.linalg.svd(xc, full_matrices=False)
    eig = u[:, 0] * s[0]
    load = vt[0].copy()
    mean_state = np.mean(a, axis=1)
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


def rna_hallmark_pc1(raw: np.ndarray, minimum_genes: int = 15,
                      finite_fraction: float = 0.95, minimum_finite: int = 20
                      ) -> tuple[np.ndarray, int, float]:
    """Stage-A Hallmark PC1 generalized in n while preserving the frozen rule."""
    x = np.asarray(raw, dtype=float)
    if x.ndim != 2 or x.shape[0] < 3:
        raise ValueError("RNA Hallmark matrix invalid")
    finite = np.isfinite(x)
    counts = finite.sum(axis=0)
    required = max(int(minimum_finite), int(math.ceil(float(finite_fraction) * x.shape[0])))
    if required > x.shape[0]:
        raise ValueError(f"RNA finite requirement {required} exceeds draw n={x.shape[0]}")
    sd = np.nanstd(x, axis=0, ddof=1)
    valid = (counts >= required) & np.isfinite(sd) & (sd > 0)
    if int(valid.sum()) < int(minimum_genes):
        raise ValueError(f"RNA Hallmark has fewer than {minimum_genes} eligible genes")
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


def median_impute(x: np.ndarray, medians: np.ndarray) -> np.ndarray:
    a = np.asarray(x, dtype=float).copy()
    med = np.asarray(medians, dtype=float)
    if a.ndim != 2 or med.shape != (a.shape[1],):
        raise ValueError("median-imputation shape mismatch")
    bad = ~np.isfinite(a)
    if bad.any():
        a[bad] = np.broadcast_to(med, a.shape)[bad]
    if not np.isfinite(a).all():
        raise ValueError("non-finite value remains after median imputation")
    return a
