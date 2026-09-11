from __future__ import annotations
import numpy as np

from .ssi_cov import output_covariances


def fit_linear_predictor(Y_train, ridge=0.0):
    """Fit Y[t+1] = Y[t] A^T by least squares. P0 adequacy diagnostic only."""
    Y = np.asarray(Y_train, float)
    if Y.ndim != 2 or Y.shape[0] < 3:
        raise ValueError("Y_train must be samples x channels")
    X, T = Y[:-1], Y[1:]
    p = X.shape[1]
    G = X.T @ X + float(ridge) * np.eye(p)
    A_t = np.linalg.pinv(G) @ X.T @ T
    return A_t.T


def one_step_residuals(Y, A):
    Y = np.asarray(Y, float)
    A = np.asarray(A, float)
    if Y.ndim != 2 or A.shape != (Y.shape[1], Y.shape[1]):
        raise ValueError("shape mismatch")
    pred = Y[:-1] @ A.T
    return Y[1:] - pred


def normalized_prediction_error(Y, A):
    residual = one_step_residuals(Y, A)
    denom = float(np.sum((Y[1:] - Y[1:].mean(0, keepdims=True)) ** 2))
    if denom <= 0:
        return np.nan
    return float(np.sum(residual ** 2) / denom)


def residual_autocorrelation_energy(residuals, max_lag):
    """Scale-free residual temporal-structure diagnostic.

    Returns summed Frobenius energy of lagged residual correlation matrices.
    It is intentionally descriptive at P0, not a frozen pass threshold.
    """
    E = np.asarray(residuals, float)
    max_lag = int(max_lag)
    if E.ndim != 2 or max_lag <= 0 or E.shape[0] <= max_lag:
        raise ValueError("insufficient residual samples")
    E = E - E.mean(0, keepdims=True)
    cov0 = (E.T @ E) / E.shape[0]
    d = np.sqrt(np.maximum(np.diag(cov0), 1e-15))
    scale = d[:, None] * d[None, :]
    total = 0.0
    for lag in range(1, max_lag + 1):
        c = (E[lag:].T @ E[:-lag]) / (E.shape[0] - lag)
        r = c / scale
        total += float(np.linalg.norm(r, "fro") ** 2)
    return total


def surrogate_whiteness_record(residuals, max_lag, n_surrogates, rng):
    """Permutation-surrogate calibration of residual autocorrelation energy.

    The returned Monte-Carlo p value is descriptive in P0. No rejection level
    is selected here. Row permutation preserves contemporaneous covariance
    while destroying serial ordering.
    """
    E = np.asarray(residuals, float)
    n_surrogates = int(n_surrogates)
    if E.ndim != 2 or E.shape[0] <= int(max_lag):
        raise ValueError("insufficient residual samples")
    if n_surrogates <= 0:
        raise ValueError("n_surrogates must be positive")
    if rng is None or not hasattr(rng, "permutation"):
        raise ValueError("an explicit NumPy-style RNG is required")

    observed = residual_autocorrelation_energy(E, max_lag)
    null = np.empty(n_surrogates, float)
    for b in range(n_surrogates):
        null[b] = residual_autocorrelation_energy(E[rng.permutation(E.shape[0])], max_lag)
    p_upper = float((1 + np.sum(null >= observed)) / (n_surrogates + 1))
    return {
        "status": "P0_DESCRIPTIVE_NOT_ADJUDICATED",
        "observed_energy": float(observed),
        "surrogate_median_energy": float(np.median(null)),
        "surrogate_q95_energy": float(np.quantile(null, 0.95)),
        "monte_carlo_upper_tail_p": p_upper,
        "n_surrogates": n_surrogates,
    }


def fit_covariance_markov_parameter(F, C, covariances, fit_lags):
    """Fit G in R_y(k) ~= C F^(k-1) G for positive lags.

    This is directly aligned with the covariance sequence used by SSI-COV and
    avoids pretending that unidentifiable Q/R noise covariances are known.
    """
    F = np.asarray(F, float)
    C = np.asarray(C, float)
    covs = [np.asarray(R, float) for R in covariances]
    fit_lags = [int(k) for k in fit_lags]

    if F.ndim != 2 or F.shape[0] != F.shape[1]:
        raise ValueError("F must be square")
    if C.ndim != 2 or C.shape[1] != F.shape[0]:
        raise ValueError("C/F shape mismatch")
    if not fit_lags or min(fit_lags) < 1 or max(fit_lags) > len(covs):
        raise ValueError("fit_lags outside available covariance sequence")

    p = C.shape[0]
    if any(R.shape != (p, p) for R in covs):
        raise ValueError("covariance shape mismatch")

    design = []
    target = []
    for lag in fit_lags:
        design.append(C @ np.linalg.matrix_power(F, lag - 1))
        target.append(covs[lag - 1])
    A = np.vstack(design)
    B = np.vstack(target)
    G, _, _, _ = np.linalg.lstsq(A, B, rcond=None)
    return G


def covariance_reconstruction_error(F, C, G, covariances, lags):
    """Normalized covariance-sequence reconstruction error.

    Returns aggregate normalized squared Frobenius error and per-lag errors.
    No adequacy threshold is encoded.
    """
    F = np.asarray(F, float)
    C = np.asarray(C, float)
    G = np.asarray(G, float)
    covs = [np.asarray(R, float) for R in covariances]
    lags = [int(k) for k in lags]
    if not lags or min(lags) < 1 or max(lags) > len(covs):
        raise ValueError("lags outside available covariance sequence")

    numerator = 0.0
    denominator = 0.0
    per_lag = {}
    for lag in lags:
        observed = covs[lag - 1]
        predicted = C @ np.linalg.matrix_power(F, lag - 1) @ G
        num = float(np.linalg.norm(observed - predicted, "fro") ** 2)
        den = float(np.linalg.norm(observed, "fro") ** 2)
        numerator += num
        denominator += den
        per_lag[str(lag)] = float(num / max(den, 1e-15))
    return float(numerator / max(denominator, 1e-15)), per_lag


def covariance_adequacy_record(Y, F, C, fit_lags, evaluation_lags):
    """Fit the SSI-compatible lag-covariance map, then test held-out lags."""
    fit_lags = [int(k) for k in fit_lags]
    evaluation_lags = [int(k) for k in evaluation_lags]
    if not fit_lags or not evaluation_lags:
        raise ValueError("fit and evaluation lags are required")
    max_lag = max(max(fit_lags), max(evaluation_lags))
    covs = output_covariances(np.asarray(Y, float), max_lag)
    G = fit_covariance_markov_parameter(F, C, covs, fit_lags)
    fit_error, fit_by_lag = covariance_reconstruction_error(F, C, G, covs, fit_lags)
    evaluation_error, evaluation_by_lag = covariance_reconstruction_error(
        F, C, G, covs, evaluation_lags
    )
    return {
        "status": "P0_DESCRIPTIVE_NOT_ADJUDICATED",
        "fit_lags": fit_lags,
        "evaluation_lags": evaluation_lags,
        "fit_normalized_covariance_error": fit_error,
        "evaluation_normalized_covariance_error": evaluation_error,
        "fit_error_by_lag": fit_by_lag,
        "evaluation_error_by_lag": evaluation_by_lag,
        "spectral_radius_discrete": float(np.max(np.abs(np.linalg.eigvals(F)))),
    }


def adequacy_record(train, test, ridge=0.0, max_lag=10):
    """Independent output-prediction diagnostic retained alongside SSI checks."""
    A = fit_linear_predictor(train, ridge=ridge)
    train_resid = one_step_residuals(train, A)
    return {
        "status": "P0_DESCRIPTIVE_NOT_ADJUDICATED",
        "spectral_radius_discrete": float(np.max(np.abs(np.linalg.eigvals(A)))),
        "train_residual_autocorrelation_energy": residual_autocorrelation_energy(
            train_resid, max_lag
        ),
        "test_normalized_prediction_error": normalized_prediction_error(test, A),
    }
