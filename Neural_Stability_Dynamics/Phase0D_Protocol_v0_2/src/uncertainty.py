from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import numpy as np


@dataclass(frozen=True)
class UncertaintyRecord:
    estimate: float
    standard_error: Optional[float] = None
    lower: Optional[float] = None
    upper: Optional[float] = None
    method: str = "UNSPECIFIED"
    status: str = "P0_NOT_ADJUDICATED"


def interval_spans_threshold(record: UncertaintyRecord, threshold: float):
    """Return True/False when a valid interval exists, otherwise None."""
    if record.lower is None or record.upper is None:
        return None
    lo, hi = float(record.lower), float(record.upper)
    if not (np.isfinite(lo) and np.isfinite(hi)) or lo > hi:
        return None
    return bool(lo <= float(threshold) <= hi)


def interval_contains(record: UncertaintyRecord, value: float):
    if record.lower is None or record.upper is None:
        return None
    lo, hi = float(record.lower), float(record.upper)
    if not (np.isfinite(lo) and np.isfinite(hi)) or lo > hi:
        return None
    return bool(lo <= float(value) <= hi)


def adjudication_from_interval(record: UncertaintyRecord, threshold: float, higher_is_better=True):
    spans = interval_spans_threshold(record, threshold)
    if spans is None:
        return "INDETERMINATE_NO_INTERVAL"
    if spans:
        return "INDETERMINATE_SPANS_BOUNDARY"
    if higher_is_better:
        return "ABOVE" if float(record.lower) > float(threshold) else "BELOW"
    return "BELOW" if float(record.upper) < float(threshold) else "ABOVE"


def central_empirical_interval(values, confidence, estimate=None, method="P0_EMPIRICAL_CENTRAL"):
    """Construct a descriptive central interval from repeated P0 estimates.

    This is a calibration utility, not an SSI analytical uncertainty estimator.
    The confidence level must be supplied explicitly so no hidden P1 convention
    is introduced.
    """
    x = np.asarray(values, float).ravel()
    confidence = float(confidence)
    if x.size < 2 or not np.all(np.isfinite(x)):
        raise ValueError("at least two finite repeated estimates are required")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must lie strictly between 0 and 1")
    alpha = 1.0 - confidence
    lo, hi = np.quantile(x, [alpha / 2.0, 1.0 - alpha / 2.0])
    point = float(np.mean(x) if estimate is None else estimate)
    return UncertaintyRecord(
        estimate=point,
        standard_error=float(np.std(x, ddof=1) / np.sqrt(x.size)),
        lower=float(lo),
        upper=float(hi),
        method=str(method),
        status="P0_CALIBRATION_NOT_P1_UNCERTAINTY",
    )


def known_truth_calibration(values, truth):
    """Descriptive error summary for repeated known-truth simulations."""
    x = np.asarray(values, float).ravel()
    truth = float(truth)
    if x.size == 0 or not np.all(np.isfinite(x)) or not np.isfinite(truth):
        raise ValueError("finite estimates and truth are required")
    err = x - truth
    return {
        "status": "P0_KNOWN_TRUTH_CALIBRATION",
        "n": int(x.size),
        "truth": truth,
        "mean_estimate": float(np.mean(x)),
        "bias": float(np.mean(err)),
        "mae": float(np.mean(np.abs(err))),
        "rmse": float(np.sqrt(np.mean(err ** 2))),
        "sd_estimates": float(np.std(x, ddof=1)) if x.size > 1 else 0.0,
    }
