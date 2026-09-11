from __future__ import annotations

import numpy as np
from scipy.signal.windows import hann


def csd_svd_surface(data, sfreq, min_hz=1.0, max_hz=45.0):
    """Frequency-resolved observational CSD-SVD surface.

    Parameters
    ----------
    data : array, shape (epochs, channels, samples)
        Source-provided epochs. No physical-mode interpretation is imposed.
    sfreq : float
        Sampling frequency in Hz.

    Returns
    -------
    dict containing frequency grid, leading spectral values/vectors/subspaces,
    participation, and numerical PSD diagnostics.
    """
    x = np.asarray(data, float)
    if x.ndim != 3:
        raise ValueError("data must have shape epochs x channels x samples")
    n_epochs, n_channels, n_times = x.shape
    if n_epochs < 1 or n_channels < 2 or n_times < 8:
        raise ValueError("insufficient data dimensions for CSD-SVD")
    sfreq = float(sfreq)
    if not np.isfinite(sfreq) or sfreq <= 0:
        raise ValueError("sfreq must be positive and finite")

    x = x - np.mean(x, axis=-1, keepdims=True)
    window = hann(n_times, sym=False)
    window_energy = float(np.sum(window * window))
    z = np.fft.rfft(x * window[None, None, :], axis=-1)
    freqs_all = np.fft.rfftfreq(n_times, d=1.0 / sfreq)
    mask = (freqs_all >= float(min_hz) - 1e-12) & (freqs_all <= float(max_hz) + 1e-12)
    indices = np.flatnonzero(mask)
    freqs = freqs_all[indices]
    if len(freqs) == 0:
        raise ValueError("frozen frequency range contains no FFT bins")

    # All retained frequencies are strictly positive and below Nyquist in the
    # current A2 pilot, so the one-sided factor is 2 throughout.
    scale = 2.0 / (sfreq * window_energy)
    k = min(4, n_channels)
    singular_values = np.empty((len(freqs), k), float)
    singular_shares = np.empty((len(freqs), k), float)
    u1 = np.empty((len(freqs), n_channels), complex)
    u2 = np.empty((len(freqs), n_channels, min(2, n_channels)), complex)
    participation = np.empty((len(freqs), n_channels), float)
    trace_power = np.empty(len(freqs), float)
    hermitian_relative_error = np.empty(len(freqs), float)
    minimum_eigenvalue = np.empty(len(freqs), float)
    material_negative = np.zeros(len(freqs), bool)

    for out_i, fft_i in enumerate(indices):
        zf = z[:, :, fft_i]
        G_raw = scale * (zf.T @ zf.conj()) / float(n_epochs)
        denom = max(float(np.linalg.norm(G_raw, ord="fro")), np.finfo(float).tiny)
        hermitian_relative_error[out_i] = float(
            np.linalg.norm(G_raw - G_raw.conj().T, ord="fro") / denom
        )
        G = 0.5 * (G_raw + G_raw.conj().T)
        values, vectors = np.linalg.eigh(G)
        order = np.argsort(values.real)[::-1]
        values = values.real[order]
        vectors = vectors[:, order]
        minimum_eigenvalue[out_i] = float(np.min(values))
        max_eig = max(float(np.max(values)), np.finfo(float).tiny)
        material_negative[out_i] = bool(np.min(values) < -1e-10 * max_eig)
        clipped = np.maximum(values, 0.0)
        trace = float(np.sum(clipped))
        if not np.isfinite(trace) or trace <= 0:
            raise ValueError(f"non-positive/non-finite cross-spectral trace at {freqs[out_i]} Hz")
        singular_values[out_i] = clipped[:k]
        singular_shares[out_i] = clipped[:k] / trace
        u1[out_i] = vectors[:, 0]
        u2[out_i] = vectors[:, : min(2, n_channels)]
        p = np.abs(vectors[:, 0]) ** 2
        participation[out_i] = p / np.sum(p)
        trace_power[out_i] = trace

    if np.any(material_negative):
        bad = freqs[material_negative]
        raise ValueError(f"material negative CSD eigenvalue at frequencies {bad.tolist()}")

    return {
        "frequency_hz": freqs,
        "singular_values_first4": singular_values,
        "singular_shares_first4": singular_shares,
        "u1": u1,
        "u2": u2,
        "participation_u1": participation,
        "trace_power": trace_power,
        "hermitian_relative_error": hermitian_relative_error,
        "minimum_eigenvalue": minimum_eigenvalue,
        "n_epochs": int(n_epochs),
        "n_channels": int(n_channels),
        "n_times": int(n_times),
        "sfreq": sfreq,
        "window": "hann_periodic_sym_false",
        "one_sided_scale": scale,
    }


def carrier_mac(u, v):
    u = np.asarray(u, complex)
    v = np.asarray(v, complex)
    if u.shape != v.shape or u.ndim != 2:
        raise ValueError("carrier arrays must be frequency x channel with matching shapes")
    un = np.linalg.norm(u, axis=1)
    vn = np.linalg.norm(v, axis=1)
    if np.any(un <= 0) or np.any(vn <= 0):
        raise ValueError("zero carrier norm")
    inner = np.sum(np.conj(u / un[:, None]) * (v / vn[:, None]), axis=1)
    return np.abs(inner) ** 2


def subspace_similarity(U, V):
    U = np.asarray(U, complex)
    V = np.asarray(V, complex)
    if U.shape != V.shape or U.ndim != 3:
        raise ValueError("subspaces must be frequency x channel x dimension")
    out = np.empty(U.shape[0], float)
    for i in range(U.shape[0]):
        s = np.linalg.svd(U[i].conj().T @ V[i], compute_uv=False)
        out[i] = float(np.mean(np.minimum(s, 1.0) ** 2))
    return out


def participation_total_variation(p, q):
    p = np.asarray(p, float)
    q = np.asarray(q, float)
    if p.shape != q.shape or p.ndim != 2:
        raise ValueError("participation arrays must be frequency x channel")
    return 0.5 * np.sum(np.abs(p - q), axis=1)


def finite_pearson(x, y, log=False):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    if x.shape != y.shape:
        raise ValueError("correlation arrays must match")
    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask]
    y = y[mask]
    if log:
        positive = (x > 0) & (y > 0)
        x = np.log(x[positive])
        y = np.log(y[positive])
    if len(x) < 3 or np.std(x) == 0 or np.std(y) == 0:
        return None
    return float(np.corrcoef(x, y)[0, 1])


def compare_surfaces(a, b):
    if not np.allclose(a["frequency_hz"], b["frequency_hz"], rtol=0, atol=1e-12):
        raise ValueError("frequency grids differ")
    mac = carrier_mac(a["u1"], b["u1"])
    sub = subspace_similarity(a["u2"], b["u2"])
    tv = participation_total_variation(a["participation_u1"], b["participation_u1"])
    return {
        "leading_carrier_MAC_per_frequency": mac,
        "two_dimensional_subspace_similarity_per_frequency": sub,
        "participation_total_variation_per_frequency": tv,
        "leading_share_curve_correlation": finite_pearson(
            a["singular_shares_first4"][:, 0],
            b["singular_shares_first4"][:, 0],
            log=False,
        ),
        "log_total_cross_spectral_power_curve_correlation": finite_pearson(
            a["trace_power"], b["trace_power"], log=True
        ),
        "median_leading_carrier_MAC": float(np.median(mac)),
        "median_two_dimensional_subspace_similarity": float(np.median(sub)),
        "median_participation_total_variation": float(np.median(tv)),
    }
