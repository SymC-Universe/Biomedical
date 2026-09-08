from __future__ import annotations
import numpy as np
from scipy.linalg import expm, qr


def complex_block(decay, frequency_hz):
    b = 2 * np.pi * float(frequency_hz)
    a = float(decay)
    return np.array([[-a, -b], [b, -a]], float)


def build_canonical(modes):
    blocks = []
    block_slices = []
    k = 0
    for m in modes:
        if m["type"] == "complex":
            B = complex_block(m["decay"], m["frequency_hz"])
        elif m["type"] == "real":
            B = np.array([[float(m["pole"])]], float)
        else:
            raise ValueError("unknown mode type")
        blocks.append(B)
        block_slices.append(slice(k, k + B.shape[0]))
        k += B.shape[0]
    A0 = np.zeros((k, k), float)
    k = 0
    for B in blocks:
        A0[k:k + B.shape[0], k:k + B.shape[0]] = B
        k += B.shape[0]
    return A0, block_slices


def similarity_matrix(n, spec, rng):
    if spec.get("similarity", "orthogonal") == "orthogonal":
        Q, _ = qr(rng.normal(size=(n, n)))
        return Q
    if spec["similarity"] == "cond":
        c = float(spec["condition_number"])
        U, _ = qr(rng.normal(size=(n, n)))
        V, _ = qr(rng.normal(size=(n, n)))
        s = np.geomspace(1.0, c, n)
        return U @ np.diag(s) @ V.T
    raise ValueError("unknown similarity")


def make_linear_system(spec, n_channels, rng):
    A0, slices = build_canonical(spec["modes"])
    n = A0.shape[0]
    S = similarity_matrix(n, spec, rng)
    A = S @ A0 @ np.linalg.inv(S)

    # Define the observation map in canonical modal coordinates first so the
    # weak-observability challenge is controlled prospectively.
    Cz = rng.normal(size=(n_channels, n))
    if "weak_block" in spec:
        sl = slices[int(spec["weak_block"])]
        Cz[:, sl] *= float(spec["weak_scale"])
    # y = Cz z and x = S z, so y = Cz S^-1 x.
    C = Cz @ np.linalg.inv(S)
    # Normalize electrode-scale rows while preserving relative modal visibility.
    rs = np.linalg.norm(C, axis=1, keepdims=True)
    C = C / np.maximum(rs, 1e-12)
    return A, C


def simulate_linear(A, C, dt, n_samples, process_scale, rng, burn=None):
    F = expm(A * dt)
    n = A.shape[0]
    p = C.shape[0]
    if burn is None:
        burn = max(2000, int(20 / dt))
    x = np.zeros(n)
    Y = np.empty((n_samples, p))
    for _ in range(burn):
        x = F @ x + process_scale * np.sqrt(dt) * rng.normal(size=n)
    for k in range(n_samples):
        x = F @ x + process_scale * np.sqrt(dt) * rng.normal(size=n)
        Y[k] = C @ x
    Y -= Y.mean(0, keepdims=True)
    return Y


def simulate_switch(spec, n_channels, dt, n_samples, process_scale, rng):
    first = {"modes": spec["modes_first"], "similarity": spec.get("similarity", "orthogonal")}
    second = {"modes": spec["modes_second"], "similarity": spec.get("similarity", "orthogonal")}
    A1, C1 = make_linear_system(first, n_channels, rng)
    A20, _ = build_canonical(second["modes"])
    from scipy.linalg import schur
    _, Q = schur(A1, output="real")
    A2 = Q @ A20 @ Q.T
    F1 = expm(A1 * dt)
    F2 = expm(A2 * dt)
    n = A1.shape[0]
    x = np.zeros(n)
    Y = np.empty((n_samples, n_channels))
    burn = max(2000, int(20 / dt))
    for _ in range(burn):
        x = F1 @ x + process_scale * np.sqrt(dt) * rng.normal(size=n)
    h = n_samples // 2
    for k in range(n_samples):
        F = F1 if k < h else F2
        x = F @ x + process_scale * np.sqrt(dt) * rng.normal(size=n)
        Y[k] = C1 @ x
    Y -= Y.mean(0, keepdims=True)
    return Y


def generate_1f(n_samples, n_channels, beta, rng):
    nfreq = n_samples // 2 + 1
    f = np.fft.rfftfreq(n_samples)
    amp = np.ones_like(f)
    amp[1:] = np.maximum(f[1:], 1 / n_samples) ** (-beta / 2)
    amp[0] = 0.0
    Z = np.empty((n_samples, n_channels))
    for j in range(n_channels):
        phase = rng.normal(size=nfreq) + 1j * rng.normal(size=nfreq)
        x = np.fft.irfft(phase * amp, n=n_samples)
        x = (x - x.mean()) / max(x.std(), 1e-12)
        Z[:, j] = x
    M = rng.normal(size=(n_channels, n_channels))
    Y = Z @ M.T
    Y -= Y.mean(0, keepdims=True)
    Y /= np.maximum(Y.std(0, keepdims=True), 1e-12)
    return Y


def add_measurement_noise(clean, profile, white_base, colored_base):
    sd = np.maximum(clean.std(0, keepdims=True), 1e-12)
    frac = float(profile["fraction_channel_sd"])
    base = white_base if profile["type"] == "white" else colored_base
    return clean + frac * sd * base


def make_noise_bases(n_samples, n_channels, rho, rng):
    white = rng.normal(size=(n_samples, n_channels))
    innov = rng.normal(size=(n_samples, n_channels))
    colored = np.zeros_like(innov)
    scale = np.sqrt(max(1 - rho * rho, 1e-12))
    for k in range(1, n_samples):
        colored[k] = rho * colored[k - 1] + scale * innov[k]
    white = (white - white.mean(0)) / np.maximum(white.std(0), 1e-12)
    colored = (colored - colored.mean(0)) / np.maximum(colored.std(0), 1e-12)
    return white, colored


def truth_modes(A, C):
    vals, vecs = np.linalg.eig(A)
    return vals, C @ vecs
