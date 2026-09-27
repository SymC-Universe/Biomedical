# NSD D1Q Discrete Exact-Image Control Preflight v0.1

Status: QUALIFICATION-ONLY CONTROL MODEL  
Date: 27 September 2026  
Authority: SymC General Operations Manual v0.8.6  
Branch: `nsd-rebuild-gom-v0.8.0`

## Purpose

D1Q is a qualification-only one-mode control spanning the underdamped discrete exact-white-Q image D. It exists to test C1Q family scope without forcing the estimated one-mode law to satisfy continuous embeddability.

D1Q is not a biological target and is not added to production A0/A1/A2.

## Parameterization

D1Q uses four model-specific coordinates:

- A: standardized latent fraction;
- rho: discrete pole radius;
- f_d: damped frequency;
- h = H/(A sinh L), with L=-ln rho and |h|<1.

The regular transition is

[
F_D=
\rho
\begin{bmatrix}
\xi & -1\\
1-\xi^2 & \xi
\end{bmatrix},
\qquad
\xi=\cos\theta,
\qquad
\theta=2\pi f_d/f_s.
]

With

[
H=hA\sinh L,
]

the constructive stationary covariance uses

[
P=
\begin{bmatrix}
A & -H\\
-H & D_*
\end{bmatrix},
]

where

[
D_*=
A\frac{(1+\rho^4)-2\rho^2\xi^2}{2\rho^2}.
]

The exact process covariance is

[
Q_D=P-F_DPF_D^T.
]

For |h|<=1 this is PSD by construction.

## Continuous diagnostic

D1Q reports the implied continuous-lineage nuisance coordinate

[
g_D
=
\frac{H}{A}
\frac{\theta}{L\sin\theta}.
]

It does not constrain |g_D|<=1.

Therefore:

- |g_D|<=1 is pointwise compatible with continuous family C on the licensed branch;
- |g_D|>1 is a valid discrete D point but outside C.

This field is a qualification diagnostic, not an admission decision.

## Relation to C1Q

C1Q and D1Q are both k=4 one-mode candidates. C is a strict subset of D at finite sampling interval.

Consequently ordinary BIC complexity penalties cannot choose scientific scope between them: both pay the same k log n term. D1Q can only match or improve the unconstrained in-sample likelihood relative to C1Q, subject to numerical optimization.

The relevant qualification outputs are therefore:

- C1Q-minus-D1Q likelihood gap;
- D1Q implied g;
- D1Q h boundary proximity;
- paired-sampling behavior;
- structural-order and predictive-closure controls.

No one field is promoted to a universal refusal threshold here.

## Executable assets

Candidate:
`NSD_vNext/engine/nsd_engine/discrete_exact_candidate.py`

Contracts:
`NSD_vNext/engine/tests/test_discrete_exact_candidate.py`

Finite-sample scope probe:
`NSD_vNext/engine/tools/probe_d1q_scope_controls.py`

Workflow:
`.github/workflows/nsd-d1q-scope-controls.yml`

## Promotion firewall

D1Q is a control layer only. It must not become a substitute biological family merely because it fits data better than C1Q. N-B1 remains targeted to continuous-time lineage C.

Real-EEG local chi remains unlicensed.
