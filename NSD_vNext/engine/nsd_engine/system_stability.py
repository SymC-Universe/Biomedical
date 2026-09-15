"""Small native continuous-time stability fixtures for local-vs-embedded tests.

This module is intentionally narrow. It provides exact descriptors for real
2x2 linear systems so the project can test a core GOM question without
inventing a project-branded whole-system scalar.

For x' = A x with A = [[a, b], [c, d]]:
- isolated local growth/decay rates are a and d;
- the full eigenspectrum determines asymptotic stability;
- the numerical abscissa of (A + A^T)/2 detects possible instantaneous
  Euclidean-norm growth and therefore exposes non-normal/reactive behavior that
  the eigenspectrum alone can miss.

These are established dynamical-systems quantities and are known-truth support,
not clinical estimators.
"""

from __future__ import annotations

from dataclasses import dataclass
import cmath
import math


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
        """Largest eigenvalue of the symmetric part (A + A^T)/2.

        For the Euclidean norm, a positive value means some state has positive
        instantaneous energy/norm growth even if all eigenvalues of A have
        negative real part.
        """
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
        """Squared Frobenius norm of A A^T - A^T A.

        Zero is necessary and sufficient for normality for a real matrix under
        the standard inner product. This is a descriptor, not a normalized
        clinical score.
        """
        # A A^T
        aat00 = self.a * self.a + self.b * self.b
        aat01 = self.a * self.c + self.b * self.d
        aat11 = self.c * self.c + self.d * self.d
        # A^T A
        ata00 = self.a * self.a + self.c * self.c
        ata01 = self.a * self.b + self.c * self.d
        ata11 = self.b * self.b + self.d * self.d

        m00 = aat00 - ata00
        m01 = aat01 - ata01
        m10 = m01
        m11 = aat11 - ata11
        return m00 * m00 + m01 * m01 + m10 * m10 + m11 * m11

    @property
    def normal(self) -> bool:
        return math.isclose(self.nonnormality_commutator_norm_sq, 0.0, abs_tol=1e-12)

    def same_isolated_local_dynamics(self, other: "LinearSystem2D") -> bool:
        return math.isclose(self.a, other.a) and math.isclose(self.d, other.d)


def same_local_different_coupling_fixture() -> tuple[LinearSystem2D, LinearSystem2D]:
    """Same isolated rates/eigenvalues, but only one system is reactive.

    The second matrix is upper triangular and strongly non-normal. Both have
    eigenvalues {-1, -1}, yet its numerical abscissa is positive.
    """
    baseline = LinearSystem2D(-1.0, 0.0, 0.0, -1.0, name="uncoupled_stable")
    reactive = LinearSystem2D(-1.0, 4.0, 0.0, -1.0, name="same_spectrum_reactive")
    return baseline, reactive


def locally_stable_globally_unstable_fixture() -> LinearSystem2D:
    """Both isolated rates are -1, but reciprocal coupling creates +1 mode."""
    return LinearSystem2D(-1.0, 2.0, 2.0, -1.0, name="coupling_destabilized")


def locally_unstable_globally_stabilized_fixture() -> LinearSystem2D:
    """One isolated component grows, while coupled eigenvalues are both -1.

    The matrix is intentionally non-normal/reactive, illustrating that
    asymptotic stabilization and transient behavior remain distinct questions.
    """
    return LinearSystem2D(1.0, -2.0, 2.0, -3.0, name="coupling_stabilized")
