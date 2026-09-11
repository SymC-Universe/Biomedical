from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
from scipy.linalg import expm
from scipy.optimize import linear_sum_assignment

from src.dmd import fit_dmd
from src.model_adequacy import (
    residual_autocorrelation_energy,
    surrogate_whiteness_record,
    fit_covariance_markov_parameter,
    covariance_reconstruction_error,
)
from src.uncertainty import central_empirical_interval, known_truth_calibration
from src.mode_tracking import track_modes


def _match_error(a, b):
    a = np.asarray(a, complex)
    b = np.asarray(b, complex)
    cost = np.abs(a[:, None] - b[None, :])
    ri, cj = linear_sum_assignment(cost)
    matched = cost[ri, cj]
    return {
        "n_matched": int(len(matched)),
        "median_absolute_error": float(np.median(matched)),
        "max_absolute_error": float(np.max(matched)),
    }


def _dmd_known_truth():
    dt = 0.05
    blocks = []
    truth_continuous = []
    for decay, hz in [(0.4, 2.0), (0.8, 5.0)]:
        b = 2 * np.pi * hz
        Ac = np.array([[-decay, -b], [b, -decay]])
        blocks.append(expm(Ac * dt))
        truth_continuous.extend([-decay + 1j * b, -decay - 1j * b])

    F = np.zeros((4, 4))
    F[:2, :2] = blocks[0]
    F[2:, 2:] = blocks[1]
    rng = np.random.default_rng(20260910)
    Q, _ = np.linalg.qr(rng.normal(size=(4, 4)))
    Fy = Q @ F @ Q.T

    x = rng.normal(size=4)
    Y = []
    for _ in range(500):
        Y.append(x.copy())
        x = Fy @ x

    estimated, _ = fit_dmd(np.asarray(Y), dt=dt, rank=4)
    return {
        "status": "P0_KNOWN_TRUTH_COMPARATOR_QUALIFICATION",
        "continuous_pole_error": _match_error(
            estimated, np.asarray(truth_continuous, complex)
        ),
    }


def _covariance_adequacy_known_truth():
    F = np.array([[0.9, 0.1], [0.0, 0.7]])
    C = np.array([[1.0, 0.2], [0.3, 1.0]])
    G = np.array([[0.5, 0.1], [0.2, 0.3]])
    covs = [C @ np.linalg.matrix_power(F, lag - 1) @ G for lag in range(1, 21)]

    fit_lags = list(range(1, 6))
    evaluation_lags = list(range(6, 21))
    fitted_G = fit_covariance_markov_parameter(F, C, covs, fit_lags)
    true_error, _ = covariance_reconstruction_error(
        F, C, fitted_G, covs, evaluation_lags
    )

    wrong_F = np.array([[0.5, 0.0], [0.0, 0.4]])
    wrong_G = fit_covariance_markov_parameter(wrong_F, C, covs, fit_lags)
    wrong_error, _ = covariance_reconstruction_error(
        wrong_F, C, wrong_G, covs, evaluation_lags
    )
    return {
        "status": "P0_KNOWN_TRUTH_MODEL_ADEQUACY_QUALIFICATION",
        "true_model_evaluation_error": float(true_error),
        "wrong_but_stable_model_evaluation_error": float(wrong_error),
        "wrong_model_spectral_radius": float(
            np.max(np.abs(np.linalg.eigvals(wrong_F)))
        ),
        "interpretation": (
            "A stable transition matrix can still reconstruct the covariance "
            "sequence poorly; stability is therefore not an adequacy proof."
        ),
    }


def _residual_whiteness_known_bad():
    rng = np.random.default_rng(9001)
    white = rng.normal(size=(1500, 3))
    innovations = rng.normal(size=(1500, 3))
    serial = np.zeros_like(innovations)
    for t in range(1, len(serial)):
        serial[t] = 0.9 * serial[t - 1] + innovations[t]

    white_record = surrogate_whiteness_record(
        white, 10, 199, np.random.default_rng(9002)
    )
    serial_record = surrogate_whiteness_record(
        serial, 10, 199, np.random.default_rng(9003)
    )
    return {
        "status": "P0_KNOWN_BAD_DIAGNOSTIC_QUALIFICATION",
        "white_residual_record": white_record,
        "serially_correlated_residual_record": serial_record,
        "energy_ratio_serial_to_white": float(
            serial_record["observed_energy"] /
            max(white_record["observed_energy"], 1e-15)
        ),
    }


def _uncertainty_calibration_math():
    rng = np.random.default_rng(77)
    truth = 2.0
    repeated = truth + rng.normal(0.0, 0.08, size=400)
    rec = central_empirical_interval(repeated, confidence=0.95)
    cal = known_truth_calibration(repeated, truth=truth)
    return {
        "status": "P0_UNCERTAINTY_CONTAINER_AND_CALIBRATION_ONLY",
        "empirical_interval": {
            "estimate": rec.estimate,
            "standard_error": rec.standard_error,
            "lower": rec.lower,
            "upper": rec.upper,
            "method": rec.method,
            "status": rec.status,
        },
        "known_truth_calibration": cal,
        "ssi_analytical_uncertainty_status": "NOT_IMPLEMENTED_P0_HOLD",
        "note": (
            "This section validates uncertainty bookkeeping and known-truth "
            "calibration only. It does not substitute for SSI analytical "
            "single-record uncertainty."
        ),
    }


def _unequal_order_bookkeeping():
    va = np.array([-1.0 + 2.0j, -0.8 + 4.0j])
    vb = np.array([-1.01 + 2.01j, -0.81 + 4.01j, -0.5 + 7.0j])
    sa = np.eye(3, 2, dtype=complex)
    sb = np.eye(3, 3, dtype=complex)
    out = track_modes(va, sa, vb, sb, min_hz=0.0)

    ambiguous = track_modes(
        np.array([-1.0 + 2.0j]),
        np.array([[1.0], [0.0]], dtype=complex),
        np.array([-1.0 + 2.0j, -1.0 + 2.0j]),
        np.array([[1.0, 1.0], [0.0, 0.0]], dtype=complex),
        min_hz=0.0,
    )
    return {
        "status": "P0_ASSIGNMENT_BOOKKEEPING_ONLY",
        "unequal_order_case": out,
        "exact_ambiguity_case": ambiguous,
        "adjudication_status": "NOT_FROZEN",
    }


def build_record():
    return {
        "schema": "nsd-phase0d-v0.2-p0-four-hold-qualification-v1",
        "status": "P0_DESCRIPTIVE_NOT_CONFIRMATORY",
        "protocol": "General Cross-Project Research Protocol v0.7.1 FINAL",
        "p1_authorized": False,
        "dmd_comparator": _dmd_known_truth(),
        "model_adequacy_covariance": _covariance_adequacy_known_truth(),
        "model_adequacy_residual_whiteness": _residual_whiteness_known_bad(),
        "uncertainty": _uncertainty_calibration_math(),
        "unequal_order": _unequal_order_bookkeeping(),
        "nonclaims": [
            "No P1 comparator is frozen.",
            "No adequacy threshold or residual-whiteness rejection level is frozen.",
            "No SSI analytical uncertainty method is claimed implemented.",
            "No shared/lost/added mode is scientifically adjudicated.",
            "No chi value, neural regime boundary, phenotype, or mechanism is tested."
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/p0_qualification/four_hold_summary.json")
    args = parser.parse_args()

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    record = build_record()
    out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out.resolve())
    print("P0 FOUR-HOLD QUALIFICATION COMPLETE. No P1 science was executed.")


if __name__ == "__main__":
    main()
