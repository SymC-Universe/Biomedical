# NSD Structural-Order Refusal Preflight v0.1

Status: PREDECISION ANALYTIC / KNOWN-TRUTH QUALIFICATION ONLY  
Date: 27 September 2026  
Authority: SymC General Operations Manual v0.8.6  
Branch: `nsd-rebuild-gom-v0.8.0`

## Purpose

C1Q can absorb valid nonzero-g one-mode continuous-lineage structure, but the colored-process adversarial control shows that model fit alone cannot establish second-order lineage. A colored process with an additional real pole can be approximated strongly enough that C1Q wins BIC even though the generating law is not a white-driven second-order C-family process.

This preflight therefore adds a structural-order refusal layer before any C1Q promotion or real-EEG local-chi admission.

## Exact second-order contract

For a genuine second-order positive-lag covariance sequence,

[
\gamma_{k+2}=a\gamma_{k+1}-b\gamma_k,
]

with

[
a=2\rho\xi,\qquad b=\rho^2,
]

the recurrence residual

[
r_k=\gamma_{k+2}-a\gamma_{k+1}+b\gamma_k
]

is exactly zero.

Equivalently, any consecutive 3x3 positive-lag Hankel matrix

[
H_3=
\begin{bmatrix}
\gamma_1&\gamma_2&\gamma_3\\
\gamma_2&\gamma_3&\gamma_4\\
\gamma_3&\gamma_4&\gamma_5
\end{bmatrix}
]

has rank at most two and determinant zero.

These identities hold across the regular underdamped, critical, and stable positive-real overdamped second-order family. They are structural-order statements, not empirical cutoffs.

## Added third-pole contract

For

[
\gamma_k=\gamma_k^{(2)}+C\phi^k,
]

where `gamma^(2)` obeys the second-order recurrence and `phi` is a distinct extra pole,

[
r_k=C\phi^k(\phi^2-a\phi+b).
]

The residual is generically nonzero whenever:

- C is nonzero;
- phi is nonzero;
- phi is not one of the second-order recurrence roots.

For a generic sum of three distinct exponentials,

[
\gamma_k=\sum_{j=1}^3 c_j\lambda_j^k,
]

the 3x3 Hankel determinant factorizes as

[
\det H_3
=
\left(\prod_j c_j\lambda_j\right)
\left(\prod_{i<j}(\lambda_j-\lambda_i)^2\right),
]

and is therefore nonzero when all residues and poles are nonzero and distinct.

## Frozen colored-process example

The existing colored-process known truth has the positive-lag decomposition

[
\gamma_k
=
\rho^k[
0.86394453\cos(k\theta)
+
0.16609964\sin(k\theta)]
-
0.06394453(0.7)^k.
]

The extra `phi=0.7` pole is distinct from the complex-conjugate oscillator pair. Its exact positive-lag covariance is therefore generically rank three, even though C1Q can win finite-sample BIC.

This provides an exact root cause for the colored-process adversarial failure: it is not merely nonzero g/H. It contains an additional dynamical pole.

## Sampling caution

Raw Hankel determinant magnitude is not sampling-rate invariant and must not become a universal production threshold. Exact decimation can also create alias-induced order collapse in the underdamped family.

Therefore the present contracts establish only the exact structural distinction. Finite-sample structural-order admission/refusal requires prospective uncertainty calibration and alias-aware handling.

## Executable contracts

`NSD_vNext/engine/tests/test_structural_order_refusal_contracts.py`

The tests verify:

- rank <= 2 / determinant zero for exact second-order underdamped, critical, and overdamped laws;
- exact zero recurrence residual for second-order laws;
- exact nonzero residual formula for an added third pole;
- rank-three behavior for the frozen colored-process decomposition;
- the generic three-exponential Vandermonde determinant factorization.

## Interpretation ceiling

This preflight does not:

- define a finite-data Hankel or singular-value cutoff;
- define a production structural-order refusal code;
- promote C1Q;
- license real-EEG local chi;
- replace predictive closure or sampling-lineage qualification;
- alter N-B2 or N-B3.
