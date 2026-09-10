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
    """Return True/False when an interval exists, otherwise None.

    This helper carries uncertainty semantics without choosing confidence levels
    or freezing any P1 threshold.
    """
    if record.lower is None or record.upper is None:
        return None
    lo, hi = float(record.lower), float(record.upper)
    if not (np.isfinite(lo) and np.isfinite(hi)):
        return None
    return bool(lo <= float(threshold) <= hi)


def adjudication_from_interval(record: UncertaintyRecord, threshold: float, higher_is_better=True):
    spans = interval_spans_threshold(record, threshold)
    if spans is None:
        return "INDETERMINATE_NO_INTERVAL"
    if spans:
        return "INDETERMINATE_SPANS_BOUNDARY"
    if higher_is_better:
        return "ABOVE" if float(record.lower) > float(threshold) else "BELOW"
    return "BELOW" if float(record.upper) < float(threshold) else "ABOVE"
