# NSD White-Process Pole Identifiability Preflight v0.1

Date: 25 September 2026
Status: PREDECISION ANALYTIC PREFLIGHT ONLY
Authority: GOM v0.8.6
Scope: P0-Q candidate-packet refinement. No model-family change, no real-EEG admission, no threshold freeze.

## Purpose

Clarify what is and is not structurally identifiable for the scalar one-oscillator state-space family after the frozen process-noise challenge showed that the current isotropic-Q A1 can be displaced by A2 under anisotropic or colored single-oscillator truth.

This note does not authorize implementation of a new candidate. It records an analytic distinction needed for the pending user-level model-family decision.

## Current scalar oscillator

For

x[t+1] = F x[t] + w[t]
y[t]   = e1^T x[t] + v[t]

with

F = rho R(theta), 0 < rho < 1,

white process noise with arbitrary positive-semidefinite 2x2 covariance Q, white observation noise v, and stationary state covariance P, the positive-lag scalar covariance is

gamma_k = e1^T F^k P e1,  k >= 1.

Writing P11 = e1^T P e1 and P12 for the off-diagonal element,

gamma_k = rho^k [cos(k theta) P11 - sin(k theta) P12].

White observation noise changes gamma_0 only and does not change gamma_k for k >= 1.

## Exact recurrence

By Cayley-Hamilton,

F^2 - 2 rho cos(theta) F + rho^2 I = 0.

Therefore every positive-lag covariance sequence from this one-oscillator family obeys

gamma_{k+2}
= 2 rho cos(theta) gamma_{k+1}
- rho^2 gamma_k,

for k >= 1, independent of the orientation or anisotropy of Q.

Using gamma_1 through gamma_4,

a = 2 rho cos(theta)
  = (gamma_1 gamma_4 - gamma_2 gamma_3)
    / (gamma_1 gamma_3 - gamma_2^2),

b = rho^2
  = (gamma_2 gamma_4 - gamma_3^2)
    / (gamma_1 gamma_3 - gamma_2^2).

For

gamma_k = rho^k [A cos(k theta) + B sin(k theta)],

the denominator satisfies

gamma_1 gamma_3 - gamma_2^2
= -rho^4 (A^2 + B^2) sin^2(theta).

Thus the pole pair is generically structurally recoverable from positive-lag covariance whenever the latent signal is nonzero and sin(theta) != 0.

## Correction to the earlier full-Q interpretation

A fully free symmetric Q is not uniquely identifiable from the scalar output. There is an exact nuisance direction: different Q matrices can generate the same scalar Gaussian output law.

However:

NONIDENTIFIABLE Q != NONIDENTIFIABLE OSCILLATOR POLES.

The full-Q ambiguity concerns the latent process-noise covariance itself. It does not generically destroy identification of rho and theta because the scalar positive-lag covariance recurrence is fixed by F.

Therefore the earlier conclusion "do not use a general-Q route because Q is non-identifiable" is too broad if the scientific target is only the licensed modal pole/frequency/damping coordinate.

A future expansion, if approved, should avoid claiming or interpreting an unidentifiable Q. It can instead parameterize only the observable nuisance equivalence class.

## Observable white-process nuisance class

For standardized scalar output, arbitrary white Q changes the two observable covariance amplitudes P11 and P12 while leaving the same second-order pole recurrence.

Relative to current isotropic A1, this adds one observable covariance-shape degree of freedom after scale is accounted for.

Equivalent implementation families could include:
- a constrained state-space realization with a fixed nuisance gauge;
- a scalar innovations/ARMA realization with the same complex-conjugate AR poles and unconstrained admissible moving-average nuisance terms;
- a covariance-phase form that fits the cosine and sine amplitudes while enforcing a valid Gaussian covariance realization.

These are candidate architectures only. Choosing among them is an estimator/model-family decision and remains blocked pending user adjudication.

## Relationship to A1-Qdiag

A1-Qdiag remains a valid narrow candidate for the exact axis-aligned white-noise challenges already used. It nests the current isotropic A1 and covers the 16:1 diagonal and first-axis rank-1 challenge families.

It is not mathematically necessary for pole identifiability, and it does not span every rotated white-Q observable covariance. Therefore it should be treated as a targeted constrained implementation candidate, not as the unique solution to white-process misspecification.

## Colored process noise remains separate

For the frozen AR(1)-colored process drive, let eta[t] be the colored drive and augment the state as z[t] = [x[t], eta[t]].

The minimal augmented transition has oscillator poles rho exp(+/- i theta) plus the real coloring pole phi. Generically the positive-lag scalar covariance therefore obeys a third-order recurrence with characteristic polynomial

(lambda - phi)
(lambda^2 - 2 rho cos(theta) lambda + rho^2).

Equivalently,

gamma_{k+3}
= (2 rho cos(theta) + phi) gamma_{k+2}
- (rho^2 + 2 phi rho cos(theta)) gamma_{k+1}
+ phi rho^2 gamma_k.

This is structurally distinct from the white-process one-oscillator recurrence and from a generic two-oscillator A2 recurrence, although finite noisy records can still make the families difficult to distinguish.

A colored-process candidate therefore still requires a separately frozen augmented-state or equivalent scalar innovations representation.

## Candidate-packet consequence

The pending user-level choice remains expansion versus refusal-only.

If expansion is approved, the white-process step should not silently estimate or interpret a fully free Q. The first prospective design should compare:
1. current A0/A1/A2;
2. one identifiable white-process single-oscillator extension that represents the observable nuisance class without interpreting Q;
3. fresh true-multimode controls;
4. explicit held-out, innovation, stationarity, and identifiability refusals.

A1-Qdiag may be retained as the simplest constrained implementation candidate, but the broader observable-equivalence formulation should be considered before the implementation freeze.

The colored-process extension remains a separate second stage.

## Exact scalar admissibility for the observable-white candidate

The broader standardized one-oscillator white-process observable class can be written as

gamma_0 = 1,

gamma_k = rho^k [A cos(k theta) + B sin(k theta)],  k >= 1.

For the original state-space interpretation with white observation noise, A = P11 and therefore 0 <= A <= 1 because gamma_0 = P11 + R = 1 with R >= 0. The new phase coordinate B is observable but need not be assigned to any unique latent-Q element.

Let

a = 2 rho cos(theta),
b = rho^2,
g0 = 1,
g1 = gamma_1,
g2 = gamma_2.

Applying the oscillator AR polynomial 1 - a L + b L^2 gives an MA(2)-equivalent residual covariance sequence with

q0 = (a^2 + b^2 + 1) g0 - 2 a (b + 1) g1 + 2 b g2,

q1 = (a^2 + b + 1) g1 - a (b + 1) g0 - a g2,

q2 = g2 - a g1 + b g0.

For the covariance-phase form above,

q2 = rho^2 (1 - A),

so q2 >= 0 throughout the original white-observation-noise state-space image.

The residual spectral numerator is

N(omega) = q0 + 2 q1 cos(omega) + 2 q2 cos(2 omega).

With x = cos(omega),

N(x) = 4 q2 x^2 + 2 q1 x + q0 - 2 q2,   -1 <= x <= 1.

Therefore exact observable admissibility can be enforced without an empirical threshold and without identifying latent Q:

- require N(1) >= 0 and N(-1) >= 0;
- if q2 > 0 and the quadratic vertex x* = -q1/(4 q2) lies in [-1,1], also require N(x*) >= 0;
- if q2 = 0, the numerator is linear in x and the endpoint conditions are sufficient.

Equivalently, when q2 > 0 and |q1| <= 4 q2, the interior condition is

q0 - 2 q2 - q1^2/(4 q2) >= 0.

This is an exact spectral-positivity condition for the scalar observable law, not a fitted production threshold.

This refinement further favors an observable-equivalence candidate over interpretation of a free Q: preserve the single oscillator denominator, free only the missing covariance-phase/numerator nuisance degree, and reject parameter combinations that do not define a nonnegative spectrum.

It does not authorize implementation or real-EEG admission.


## Structural identifiability versus numerical conditioning

The closed-form covariance inversions above establish structural identifiability, not uniform numerical conditioning.

Once rho and theta are known, the first two positive lags satisfy

[gamma_1 / rho, gamma_2 / rho^2]^T
=
M(theta) [A, B]^T,

with

M(theta) =
[[cos(theta), sin(theta)],
 [cos(2 theta), sin(2 theta)]].

The determinant is

det M(theta) = sin(theta),

and the exact 2-norm condition number is

kappa_2(M)
=
sqrt((1 + |cos(theta)|) / (1 - |cos(theta)|)).

For 0 < theta < pi/2 this reduces to

kappa_2(M) = cot(theta / 2).

Therefore the covariance-phase coordinate is structurally unique whenever sin(theta) != 0, but direct finite-lag inversion becomes increasingly ill-conditioned as theta approaches 0, and symmetrically near the Nyquist degeneracy.

The pole-recovery recurrence has the same structural warning because

gamma_1 gamma_3 - gamma_2^2
=
-rho^4 (A^2 + B^2) sin^2(theta).

Accordingly, the closed-form lag formulas are proofs of uniqueness and candidate diagnostics, not a proposed production estimator.

For the current 256 Hz fitter band, the normalized two-lag condition number is about 81.5 at 1 Hz and about 1.62 at 45 Hz. The existing operating-region probe only exercises isotropic B=0 truths at 5, 10, and 20 Hz; across its current damping grid the same condition number is already approximately 16.6-27.2 at 5 Hz, 8.3-13.6 at 10 Hz, and 4.1-6.7 at 20 Hz.

This does not establish that conditioning caused any prior likelihood-fit failure. It identifies a prospective qualification requirement. Any approved nonzero-B exact-image candidate should be tested across the intended frequency/conditioning region with fresh known-truth controls, including B=0 isotropic controls, nonzero-B white-process truths, near-image-boundary cases, and colored-process out-of-family refusals. The production route should remain likelihood/innovations based rather than use plug-in two-lag inversion.

No numerical conditioning cutoff, frequency floor, eta grid, duration, optimizer setting, or acceptance threshold is frozen by this note.



## Signal-strength and phase-coverage qualification gap

The current operating-region truth grid does not span the full fitted latent-signal range.

For the isotropic simulator, measurement-noise SD ratio r gives population standardized latent variance fraction

A = 1 / (1 + r^2).

The existing operating-region values r = 0, 0.5, 1 therefore cover approximately A = 1, 0.8, 0.5, while the current likelihood parameterization permits latent_fraction down to about 1e-5.

Using B = A kappa eta in the exact-image recurrence denominator gives

gamma_1 gamma_3 - gamma_2^2
= -rho^4 A^2 (1 + kappa^2 eta^2) sin^2(theta).

Thus, even away from the frequency degeneracy, pole/covariance recovery becomes weak as A approaches zero because the identifying denominator collapses quadratically in latent signal fraction.

The existing nonzero-B process challenges also occupy only one pole/noise-strength setting (10 Hz natural frequency, zeta = 0.30, observation-noise SD ratio 0.50) and their nonzero-B projections all have the same sign. They therefore establish mechanistic alignment at one known-truth point, not operating-region qualification for the exact-image family.

Any approved exact-image expansion should prospectively extend known-truth qualification across signal strength and both covariance-phase signs/orientations, while preserving B=0 controls and colored-process refusals. Exact signal-strength levels, eta values, grids, and refusal thresholds remain unfrozen.


## Interpretation ceiling

This preflight does not:
- change the frozen A0/A1/A2 family;
- authorize A1-Qdiag, a general-white-Q output model, or A1-colored;
- define any numerical threshold;
- license real-EEG damping or local chi;
- identify process-noise covariance as biological structure;
- alter N-B2 or N-B3 claims.

Real-EEG local chi remains unlicensed.
