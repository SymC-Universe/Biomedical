# NSD Second-Order Oscillator Convention Note v0.1

Date: 14 September 2026
Status: FROZEN KNOWN-TRUTH CONVENTION FOR INITIAL ENGINE QUALIFICATION

## 1. Purpose

NSD historically used `chi = gamma/(2 omega)` loosely across contexts. The vNext Engine needs one exact canonical second-order convention for synthetic known-truth tests so that frequency and damping quantities cannot drift by notation.

The initial fixture uses the classical second-order form:

```text
x'' + 2 zeta omega_0 x' + omega_0^2 x = u(t)
```

where:
- `zeta` is the dimensionless classical damping ratio;
- `omega_0` is the undamped natural angular frequency in rad/s;
- `f_0 = omega_0/(2 pi)` is the undamped natural frequency in Hz.

For the current SymC/NSD comparison, `zeta` is the canonical second-order dimensionless stability coordinate in this fixture. A different symbol may be used in manuscript notation later, but the conversion must be explicit.

## 2. Underdamped poles

For `0 < zeta < 1`, the characteristic poles are:

```text
s_1,2 = -zeta omega_0 +/- i omega_0 sqrt(1 - zeta^2)
```

Therefore:

```text
decay rate alpha = zeta omega_0
omega_d = omega_0 sqrt(1 - zeta^2)
f_d = f_0 sqrt(1 - zeta^2)
```

The real pole part controls exponential decay and the imaginary pole part controls free oscillation frequency.

## 3. Three frequencies that must not be conflated

For a damped second-order system there can be at least three relevant frequency quantities:

1. **Undamped natural frequency**

```text
f_0 = omega_0/(2 pi)
```

2. **Damped free-oscillation frequency**

```text
f_d = f_0 sqrt(1 - zeta^2)
```

3. **Forced displacement-resonance frequency**, when it exists

```text
f_r = f_0 sqrt(1 - 2 zeta^2)
```

The forced displacement resonance exists only when:

```text
zeta < 1/sqrt(2)
```

This has a direct NSD consequence:

> A measured spectral peak center cannot be called `f_0` merely because it is the center of a peak, and it cannot be assumed to equal the free damped frequency either.

The mapping depends on the generator and observable.

## 4. Important edge case

A system can be **underdamped** in the classical pole sense (`zeta < 1`) yet have **no displacement resonance maximum** under harmonic forcing when:

```text
1/sqrt(2) <= zeta < 1
```

This matters for peak-based neural inference. The absence of a resonance peak does not by itself prove an overdamped pole structure.

Likewise, a broad or absent spectral peak cannot be translated directly into a high damping ratio without the generative assumptions that connect the measured spectrum to this transfer function.

## 5. Transfer power fixture

For unit forcing and displacement output, the initial known-truth spectral fixture uses:

```text
|H(i omega)|^2 = 1 / [ (omega_0^2 - omega^2)^2 + (2 zeta omega_0 omega)^2 ]
```

This is an analytic test object. It is not asserted to be the correct generator for resting scalp EEG.

Its purpose is to test whether candidate estimators can recover known parameters and, equally importantly, whether descriptive peak quantities are being mislabeled.

## 6. Free-response fixture

For initial displacement `x_0` and initial velocity `v_0`, the exact underdamped free response is:

```text
x(t) = exp(-alpha t) [ A cos(omega_d t) + B sin(omega_d t) ]
```

with:

```text
A = x_0
B = (v_0 + alpha x_0)/omega_d
alpha = zeta omega_0
```

This provides an exact time-domain known-truth signal without numerical-integration error.

## 7. Relation to historical NSD notation

The 2025 manuscript used expressions such as:

```text
chi = gamma/(2 omega)
```

but mixed interpretations of `omega` across drive frequency, measured oscillatory frequency, and stability-space axes.

The vNext project does **not** inherit that ambiguity.

For any future mode-specific NSD scalar, the manuscript/code must state:
- governing equation;
- coefficient units;
- whether the frequency is angular or ordinary frequency;
- whether the denominator uses `omega_0`, `omega_d`, measured peak center, or another quantity;
- exact conversion between the fitted parameters and the dimensionless ratio;
- scope over which the conversion has been qualified.

## 8. Current executable implementation

The contract scaffold contains `DHOTruth`, `impulse_response`, and `transfer_power` fixtures implementing the convention above.

Current regression tests verify:
- pole/frequency relationships;
- damped frequency below natural frequency;
- resonance center distinct from natural and damped frequencies;
- the underdamped/no-resonance edge case;
- exact initial-condition behavior;
- transfer-power peak agreement with analytic resonance;
- rejection of non-underdamped inputs from this specific fixture.

These tests are known-truth infrastructure, not evidence about psychiatric neurophysiology.