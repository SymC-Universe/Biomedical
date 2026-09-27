# NSD One-Mode Continuous-Lineage Candidate Preflight v0.1

Status: QUALIFICATION-ONLY CANDIDATE  
Date: 27 September 2026  
Authority: SymC General Operations Manual v0.8.6  
Branch: `nsd-rebuild-gom-v0.8.0`

## Purpose

This preflight defines C1Q, a qualification-only one-mode continuous-lineage candidate used to test whether the single nuisance coordinate g/H removes false A2 model-order pressure for valid one-mode C truths.

C1Q is not added to the production A0/A1/A2 ModelFamily and does not license real EEG.

## Parameterization

The current underdamped qualification candidate has four model-specific coordinates:

- A: standardized latent fraction;
- rho: discrete pole radius;
- f_d: damped frequency;
- g: continuous-lineage covariance-phase nuisance coordinate, constrained to (-1,1).

With

[
\alpha=-f_s\ln\rho,\qquad
\nu=2\pi f_d,\qquad
G=gA\alpha,
]

the continuous generator and constructive stationary covariance are

[
K=
\begin{bmatrix}
-\alpha & -1\\
\nu^2 & -\alpha
\end{bmatrix},
\qquad
P=
\begin{bmatrix}
A & -G\\
-G & A(2\alpha^2+\nu^2)
\end{bmatrix}.
]

The exact discrete model is

[
F=e^{K/f_s},
\qquad
Q_d=P-FPF^T,
\qquad
R=1-A.
]

The scalar observation is [1,0]. Local chi is

[
\chi=\frac{\alpha}{\sqrt{\alpha^2+\nu^2}}.
]

The corresponding regular covariance coordinate is

[
H=G\frac{\sin(\nu/f_s)}{\nu}.
]

## Nesting

At g=0, C1Q reduces observationally to current A1. Therefore:

- A1 remains the simpler k=3 submodel;
- C1Q is k=4;
- if g is unnecessary, ordinary BIC penalizes C1Q by one additional parameter;
- if nonzero g is required, C1Q can represent a one-mode C truth that current A1 cannot.

This nesting is intentional. The candidate is not a blanket replacement for A1.

## Motivation

The successful spectral-KL result at run `36354717604` and the successful finite-realization probe at run `36354816856` show that valid one-mode C truths with nonzero g can create false A2 pressure under current A1.

C1Q exists to determine whether that pressure can be absorbed by the correct one-mode nuisance degree before any A2 selection is interpreted as multimodality.

## Executable implementation

Qualification-only module:

`NSD_vNext/engine/nsd_engine/continuous_lineage_candidate.py`

Contracts:

`NSD_vNext/engine/tests/test_continuous_lineage_candidate.py`

Exploratory comparison:

`NSD_vNext/engine/tools/probe_continuous_lineage_nonzero_g.py`

The implementation uses the same steady-state innovations likelihood structure and the same A/rho/frequency reachable box as the current state-space qualification machinery, with g added as one bounded nuisance coordinate.

## Promotion firewall

C1Q must remain qualification-only until prospective known-truth tests establish at minimum:

- g=0 nesting behaves correctly;
- nonzero-g one-mode C truths no longer require false A2 selection;
- chi recovery is stable across paired alias-safe sampling;
- C1Q does not absorb genuine separated two-mode truth as one mode;
- D\C, S\D, colored-process, A2-collision, and closure/refusal controls behave correctly;
- near-critical conditioning and all-regime extension are separately resolved.

Promotion into the production estimator family is a scientific decision and is not authorized by this preflight.
