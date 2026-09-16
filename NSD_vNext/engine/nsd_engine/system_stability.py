"""Native continuous-time stability fixtures for local-vs-embedded tests.

This module provides exact or numerically controlled descriptors for real 2x2
linear systems so the project can test GOM local-versus-embedded questions
without inventing a project-branded whole-system scalar.

For x' = A x with A = [[a, b], [c, d]]:
- isolated local growth/decay rates are a and d;
- the full eigenspectrum determines asymptotic stability;
- the numerical abscissa of (A + A^T)/2 detects possible instantaneous
  Euclidean-norm growth;
- the propagator norm ||exp(A t)||_2 measures finite-time amplification.

These are established dynamical-systems quantities and are known-truth support,
not clinical estimators.
"""

from __future__ import annotations

from dataclasses import dataclass
import cmath
import math

import numpy as np
from scipy.linalg import expm


@dataclass(frozen=True)
class LinearSystem2D:
    a: float
    b: float
    c: float
    d: float
    name: str = "unnamed"

    def __post_init__(self) -> None:
        for field_name in ("a", "b", "c", "d"):
            value = getattr(self, field_name)
            if not math.isfinite(value):
                raise ValueError(f"{field_name} must be finite")
        if not self.name.strip():
            raise ValueError("name must be non-empty")

    @property
    def matrix(self) -> np.ndarray:
        return np.asarray([[self.a, self.b], [self.c, self.d]], dtype=float)

    @property
    def trace(self) -> float:
        return self.a + self.d

    @property
    def determinant(self) -> float:
        return self.a * self.d - self.b * self.c

    @property
    def isolated_local_rates(self) -> tuple[float, float]:
        """Growth/decay rates of the uncoupled scalar components."""
        return (self.a, self.d)

    @property
    def local_components_stable(self) -> bool:
        return self.a < 0.0 and self.d < 0.0

    @property
    def eigenvalues(self) -> tuple[complex, complex]:
        discriminant = complex(self.trace * self.trace - 4.0 * self.determinant, 0.0)
        root = cmath.sqrt(discriminant)
        return ((self.trace + root) / 2.0, (self.trace - root) / 2.0)

    @property
    def spectral_abscissa(self) -> float:
        """max Re(lambda_i(A)); negative implies asymptotic stability."""
        return max(value.real for value in self.eigenvalues)

    @property
    def asymptotically_stable(self) -> bool:
        return self.spectral_abscissa < 0.0

    @property
    def numerical_abscissa(self) -> float:
        """Largest eigenvalue of the symmetric part (A + A^T)/2."""
        offdiag = 0.5 * (self.b + self.c)
        trace_s = self.a + self.d
        determinant_s = self.a * self.d - offdiag * offdiag
        discriminant = max(0.0, trace_s * trace_s - 4.0 * determinant_s)
        return 0.5 * (trace_s + math.sqrt(discriminant))

    @property
    def reactive(self) -> bool:
        return self.numerical_abscissa > 0.0

    @property
    def nonnormality_commutator_norm_sq(self) -> float:
        """Squared Frobenius norm of A A^T - A^T A."""
        aat = self.matrix @ self.matrix.T
        ata = self.matrix.T @ self.matrix
        commutator = aat - ata
        return float(np.sum(commutator * commutator))

    @property
    def normal(self) -> bool:
        return math.isclose(self.nonnormality_commutator_norm_sq, 0.0, abs_tol=1e-12)

    def same_isolated_local_dynamics(self, other: "LinearSystem2D") -> bool:
        return math.isclose(self.a, other.a) and math.isclose(self.d, other.d)

    def same_eigenspectrum(self, other: "LinearSystem2D", *, atol: float = 1e-12) -> bool:
        left = sorted(self.eigenvalues, key=lambda z: (z.real, z.imag))
        right = sorted(other.eigenvalues, key=lambda z: (z.real, z.imag))
        return all(abs(a - b) <= atol for a, b in zip(left, right))

    def transient_gain(self, t: float) -> float:
        """Return ||exp(A t)||_2 for t >= 0."""
        if not math.isfinite(t) or t < 0.0:
            raise ValueError("t must be finite and non-negative")
        propagator = expm(self.matrix * t)
        return float(np.linalg.svd(propagator, compute_uv=False)[0])

    def max_transient_gain(
        self,
        *,
        t_max: float = 5.0,
        samples: int = 501,
    ) -> tuple[float, float]:
        """Sample max ||exp(A t)||_2 over [0, t_max].

        Returns (t_at_max, gain). This deterministic grid search is a
        qualification utility, not a claim of exact continuous-time
        maximization.
        """
        if not math.isfinite(t_max) or t_max <= 0.0:
            raise ValueError("t_max must be finite and positive")
        if samples < 2:
            raise ValueError("samples must be >= 2")

        best_t = 0.0
        best_gain = 1.0
        for t in np.linspace(0.0, t_max, samples):
            gain = self.transient_gain(float(t))
            if gain > best_gain:
                best_t = float(t)
                best_gain = gain
        return best_t, best_gain


def same_local_different_coupling_fixture() -> tuple[LinearSystem2D, LinearSystem2D]:
    """Same isolated rates/eigenvalues, but only one system is reactive."""
    baseline = LinearSystem2D(-1.0, 0.0, 0.0, -1.0, name="uncoupled_stable")
    reactive = LinearSystem2D(-1.0, 4.0, 0.0, -1.0, name="same_spectrum_reactive")
    return baseline, reactive


def different_local_same_global_spectrum_fixture() -> tuple[LinearSystem2D, LinearSystem2D]:
    """Different local rates with the same embedded eigenvalues {-1, -2}.

    This is a CVX-02 fixture: local inspection differs materially while the
    asymptotic eigenspectrum of the embedded system is identical.
    """
    baseline = LinearSystem2D(-1.0, 0.0, 0.0, -2.0, name="diagonal_reference")
    compensated = LinearSystem2D(1.0, 2.0, -3.0, -4.0, name="coupling_compensated")
    return baseline, compensated


def locally_stable_globally_unstable_fixture() -> LinearSystem2D:
    """Both isolated rates are -1, but reciprocal coupling creates +1 mode."""
    return LinearSystem2D(-1.0, 2.0, 2.0, -1.0, name="coupling_destabilized")


def locally_unstable_globally_stabilized_fixture() -> LinearSystem2D:
    """One isolated component grows, while coupled eigenvalues are both -1."""
    return LinearSystem2D(1.0, -2.0, 2.0, -3.0, name="coupling_stabilized")
