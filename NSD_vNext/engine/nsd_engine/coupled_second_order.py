"""Known-truth coupled second-order fixtures for NSD local chi vs system Chi.

This module uses native continuous-time linear systems to test the GOM v0.8.3
joint question without inventing a whole-system scalar.

Each isolated subsystem is a standard second-order oscillator

    q'' + 2*zeta*omega_n*q' + omega_n^2*q = 0

so its native local scalar is the modal damping ratio zeta. Coupling is then
introduced explicitly in the full state matrix. The resulting system is
described by established quantities such as the full eigenspectrum, spectral
abscissa, numerical abscissa and finite-time propagator gain.

Qualification fixtures only. No EEG inference or clinical interpretation.
"""

from __future__ import annotations

from dataclasses import dataclass
import cmath
import math

import numpy as np
from scipy.linalg import expm


@dataclass(frozen=True)
class CoupledSecondOrder2Mode:
    omega1_rad_s: float
    zeta1: float
    omega2_rad_s: float
    zeta2: float
    position_coupling_12: float = 0.0
    position_coupling_21: float = 0.0
    velocity_coupling_12: float = 0.0
    velocity_coupling_21: float = 0.0
    name: str = "unnamed"

    def __post_init__(self) -> None:
        for field in (
            "omega1_rad_s",
            "zeta1",
            "omega2_rad_s",
            "zeta2",
            "position_coupling_12",
            "position_coupling_21",
            "velocity_coupling_12",
            "velocity_coupling_21",
        ):
            value = float(getattr(self, field))
            if not math.isfinite(value):
                raise ValueError(f"{field} must be finite")
        if self.omega1_rad_s <= 0 or self.omega2_rad_s <= 0:
            raise ValueError("natural frequencies must be positive")
        if not self.name.strip():
            raise ValueError("name must be non-empty")

    @property
    def local_damping_ratios(self) -> tuple[float, float]:
        return (float(self.zeta1), float(self.zeta2))

    @property
    def local_natural_frequencies_rad_s(self) -> tuple[float, float]:
        return (float(self.omega1_rad_s), float(self.omega2_rad_s))

    @staticmethod
    def _local_poles(omega: float, zeta: float) -> tuple[complex, complex]:
        # Valid for any real zeta. For zeta > 1 the square root becomes real
        # through the complex-valued expression.
        root = cmath.sqrt(complex(zeta * zeta - 1.0, 0.0))
        return (
            -zeta * omega + omega * root,
            -zeta * omega - omega * root,
        )

    @property
    def isolated_local_poles(self) -> tuple[complex, complex, complex, complex]:
        return (
            *self._local_poles(self.omega1_rad_s, self.zeta1),
            *self._local_poles(self.omega2_rad_s, self.zeta2),
        )

    @property
    def isolated_local_stability(self) -> tuple[bool, bool]:
        first = all(p.real < 0 for p in self._local_poles(self.omega1_rad_s, self.zeta1))
        second = all(p.real < 0 for p in self._local_poles(self.omega2_rad_s, self.zeta2))
        return (first, second)

    @property
    def matrix(self) -> np.ndarray:
        w1 = float(self.omega1_rad_s)
        w2 = float(self.omega2_rad_s)
        return np.asarray(
            [
                [0.0, 1.0, 0.0, 0.0],
                [
                    -(w1 * w1),
                    -2.0 * self.zeta1 * w1,
                    self.position_coupling_12,
                    self.velocity_coupling_12,
                ],
                [0.0, 0.0, 0.0, 1.0],
                [
                    self.position_coupling_21,
                    self.velocity_coupling_21,
                    -(w2 * w2),
                    -2.0 * self.zeta2 * w2,
                ],
            ],
            dtype=np.float64,
        )

    @property
    def eigenvalues(self) -> tuple[complex, ...]:
        values = np.linalg.eigvals(self.matrix)
        return tuple(complex(x) for x in values)

    @property
    def spectral_abscissa(self) -> float:
        return float(max(x.real for x in self.eigenvalues))

    @property
    def asymptotically_stable(self) -> bool:
        return self.spectral_abscissa < 0.0

    @property
    def numerical_abscissa(self) -> float:
        symmetric = 0.5 * (self.matrix + self.matrix.T)
        return float(np.max(np.linalg.eigvalsh(symmetric)))

    @property
    def reactive(self) -> bool:
        return self.numerical_abscissa > 0.0

    @property
    def nonnormality_commutator_norm_sq(self) -> float:
        A = self.matrix
        commutator = A @ A.T - A.T @ A
        return float(np.sum(commutator * commutator))

    @property
    def eigenvector_condition_number(self) -> float:
        _, vectors = np.linalg.eig(self.matrix)
        return float(np.linalg.cond(vectors))

    def same_local_modes(
        self,
        other: "CoupledSecondOrder2Mode",
        *,
        atol: float = 1e-12,
    ) -> bool:
        return all(
            math.isclose(a, b, abs_tol=atol, rel_tol=0.0)
            for a, b in zip(
                (
                    self.omega1_rad_s,
                    self.zeta1,
                    self.omega2_rad_s,
                    self.zeta2,
                ),
                (
                    other.omega1_rad_s,
                    other.zeta1,
                    other.omega2_rad_s,
                    other.zeta2,
                ),
            )
        )

    def same_eigenspectrum(
        self,
        other: "CoupledSecondOrder2Mode",
        *,
        atol: float = 1e-10,
    ) -> bool:
        left = sorted(self.eigenvalues, key=lambda z: (round(z.real, 12), z.imag))
        right = sorted(other.eigenvalues, key=lambda z: (round(z.real, 12), z.imag))
        return all(abs(a - b) <= atol for a, b in zip(left, right))

    def transient_gain(self, t: float) -> float:
        if not math.isfinite(t) or t < 0:
            raise ValueError("t must be finite and non-negative")
        return float(np.linalg.svd(expm(self.matrix * t), compute_uv=False)[0])

    def max_transient_gain(
        self,
        *,
        t_max: float = 20.0,
        samples: int = 2001,
    ) -> tuple[float, float]:
        if not math.isfinite(t_max) or t_max <= 0:
            raise ValueError("t_max must be finite and positive")
        if samples < 2:
            raise ValueError("samples must be >= 2")
        best_t = 0.0
        best_gain = self.transient_gain(0.0)
        for t in np.linspace(0.0, t_max, samples):
            gain = self.transient_gain(float(t))
            if gain > best_gain:
                best_t = float(t)
                best_gain = gain
        return best_t, best_gain

    def sustained_return_time(
        self,
        *,
        gain_threshold: float = 1.05,
        t_max: float = 30.0,
        samples: int = 3001,
    ) -> float | None:
        """Return first time after which worst-case gain stays <= threshold.

        The quantity is a deterministic grid diagnostic for known-truth
        recovery/reorganization tests. None means the threshold was not
        sustained before t_max.
        """
        if not math.isfinite(gain_threshold) or gain_threshold <= 0:
            raise ValueError("gain_threshold must be finite and positive")
        if not math.isfinite(t_max) or t_max <= 0:
            raise ValueError("t_max must be finite and positive")
        if samples < 2:
            raise ValueError("samples must be >= 2")

        times = np.linspace(0.0, t_max, samples)
        gains = np.asarray([self.transient_gain(float(t)) for t in times])
        suffix_max = np.maximum.accumulate(gains[::-1])[::-1]
        indices = np.flatnonzero(suffix_max <= gain_threshold)
        return float(times[indices[0]]) if indices.size else None


def same_local_same_spectrum_different_transient_fixture(
) -> tuple[CoupledSecondOrder2Mode, CoupledSecondOrder2Mode]:
    """CVX-01/CVX-06 fixture.

    Feed-forward coupling preserves the block-triangular eigenspectrum while
    changing reactivity and finite-time gain. Local zeta values are identical.
    """
    baseline = CoupledSecondOrder2Mode(
        1.0, 0.20, 1.0, 0.20,
        name="uncoupled_identical_local_modes",
    )
    feedforward = CoupledSecondOrder2Mode(
        1.0, 0.20, 1.0, 0.20,
        position_coupling_12=2.0,
        name="feedforward_same_local_same_spectrum",
    )
    return baseline, feedforward


def same_local_different_embedding_fixture(
) -> tuple[CoupledSecondOrder2Mode, CoupledSecondOrder2Mode]:
    """CVX-01/CVX-05 fixture with same local modes but altered full spectrum."""
    baseline = CoupledSecondOrder2Mode(
        1.0, 0.20, 1.0, 0.20,
        name="uncoupled_reference",
    )
    coupled = CoupledSecondOrder2Mode(
        1.0, 0.20, 1.0, 0.20,
        position_coupling_12=0.80,
        position_coupling_21=0.80,
        name="reciprocal_coupling_changed_embedding",
    )
    return baseline, coupled


def locally_stable_globally_unstable_second_order_fixture(
) -> CoupledSecondOrder2Mode:
    """CVX-03 fixture: stable isolated modes, destabilized by coupling."""
    return CoupledSecondOrder2Mode(
        1.0, 0.20, 1.0, 0.20,
        position_coupling_12=1.20,
        position_coupling_21=1.20,
        name="stable_local_modes_coupling_destabilized",
    )
