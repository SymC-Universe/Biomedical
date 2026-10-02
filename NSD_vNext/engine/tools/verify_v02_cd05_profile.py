"""Independent CD-05 mechanical reproduction for frozen NSD v0.2 Profile-I.

This verifier checks the physical-coordinate mapping and fixed-chi likelihood
route without calling the production coordinate-conversion helper. It uses a
non-confirmatory deterministic probe signal and emits no scientific verdict.
"""
from __future__ import annotations

import inspect
import json
import math
import numpy as np

from nsd_engine.continuous_lineage_candidate import _nll
from nsd_engine.v02_nb1_profile import profile_evidence
from nsd_engine.v02_profile_coords import nuisance_from_physical, objective


def _logit(p: float) -> float:
    if not 0.0 < p < 1.0:
        raise RuntimeError("mechanical probe outside transform domain")
    return math.log(p / (1.0 - p))


def _independent_raw(A: float, fn: float, chi: float, g: float, fs: float) -> np.ndarray:
    # Independent reconstruction of the frozen raw C1Q coordinate map.
    fd = fn * math.sqrt(1.0 - chi * chi)
    nu = 2.0 * math.pi * fd
    alpha = nu * chi / math.sqrt(1.0 - chi * chi)
    rho = math.exp(-alpha / fs)

    frac_p = (A - 1e-5) / (1.0 - 2e-5)
    rho_p = (rho - 1e-3) / (0.999 - 1e-3)
    freq_p = (fd - 1.0) / (45.0 - 1.0)
    return np.asarray([
        _logit(frac_p),
        _logit(rho_p),
        _logit(freq_p),
        math.atanh(g),
    ], dtype=float)


def verify() -> dict:
    # Mechanical probe is intentionally not a frozen confirmatory truth.
    A, fn, chi, g, fs = 0.47, 7.25, 0.31, 0.22, 120.0
    nuisance = nuisance_from_physical(A, fn, chi, g)
    if nuisance is None:
        raise RuntimeError("production nuisance map refused mechanical probe")

    raw_ref = _independent_raw(A, fn, chi, g, fs)

    t = np.arange(2048, dtype=float) / fs
    signal = np.sin(2.0 * math.pi * 5.3 * t) + 0.17 * np.cos(2.0 * math.pi * 11.1 * t)
    signal = signal + 0.03 * np.sin(2.0 * math.pi * 1.7 * t)
    standardized = (signal - float(np.mean(signal))) / float(np.std(signal))

    direct = float(_nll(standardized, raw_ref, fs, 1.0, 45.0, 128))
    routed = float(objective(standardized, fs, chi, nuisance))
    scale = max(1.0, abs(direct), abs(routed))
    rel = abs(direct - routed) / scale
    if rel > 1e-12:
        raise RuntimeError(f"CD-05 likelihood reproduction mismatch: {rel}")

    params = tuple(inspect.signature(profile_evidence).parameters)
    if params != ("signal", "fs"):
        raise RuntimeError("Profile-I public interface can accept non-frozen truth information")

    return {
        "status": "PASS",
        "mechanical_probe_only": True,
        "truth_parameter_used_in_profile_interface": False,
        "coordinate_likelihood_relative_error": rel,
        "scientific_adjudication": "NOT_PERFORMED_BY_GITHUB",
    }


if __name__ == "__main__":
    print(json.dumps(verify(), sort_keys=True))
