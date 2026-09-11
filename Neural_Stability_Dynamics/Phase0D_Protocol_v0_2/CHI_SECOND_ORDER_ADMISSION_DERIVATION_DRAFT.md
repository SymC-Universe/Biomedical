# NSD Second-Order Pole Factorization and Chi Admission Derivation Draft

Date: 2026-09-11
Status: MATHEMATICAL DERIVATION / ADMISSION-FIREWALL DRAFT. NOT A CHI VALIDATION. NOT P0-Q. NOT P1.
Protocol: General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum

## Purpose

System Model v1.0 withholds `chi` by default. This note separates a mathematical fact that follows from any stable complex-conjugate pole pair from the stronger physical interpretation required before an NSD/SymC chi coordinate may be admitted.

The distinction is essential because algebraic equivalence to a real second-order polynomial does not by itself establish a literal neural mass-spring-damper mechanism, a unique physical damping coefficient, or a system-level chi.

## 1. Stable conjugate pole pair

Let an identified continuous-time conjugate pair be

`lambda_+ = -alpha + i beta`

`lambda_- = -alpha - i beta`

with `alpha > 0` and `beta > 0` for a stable oscillatory pair.

The real quadratic factor having these roots is

`(s - lambda_+)(s - lambda_-)`

`= (s + alpha - i beta)(s + alpha + i beta)`

`= (s + alpha)^2 + beta^2`

`= s^2 + 2 alpha s + (alpha^2 + beta^2)`.

Thus every stable complex pair admits the exact algebraic representation

`s^2 + 2 alpha s + omega_n^2 = 0`

with

`omega_n = sqrt(alpha^2 + beta^2)`.

## 2. Standard pole damping ratio

The normalized second-order denominator is conventionally written

`s^2 + 2 zeta omega_n s + omega_n^2 = 0`.

Matching coefficients gives

`2 zeta omega_n = 2 alpha`,

so

`zeta_pole = alpha / omega_n`

and therefore

`zeta_pole = alpha / sqrt(alpha^2 + beta^2)`.

Equivalently, if the pole is written `lambda = sigma + i omega` with stable `sigma < 0`,

`zeta_pole = -sigma / sqrt(sigma^2 + omega^2)`.

For a stable oscillatory pair, `0 < zeta_pole < 1`.

This coordinate is determined entirely by pole geometry. It is **not** `alpha / beta`; `beta` is the damped oscillation frequency, whereas `sqrt(alpha^2 + beta^2)` is the second-order natural-frequency magnitude associated with the pole pair.

## 3. What the algebra licenses

If the continuous-time pole pair itself is supported and its uncertainty is characterized, NSD may in principle derive a coordinate with an explicit name such as:

- `modal_pole_damping_ratio`, or
- `zeta_pole`.

Such a coordinate is a **derived spectral coordinate**. Its derivation is exact conditional on the identified pole pair and continuous-time mapping.

It may be useful for:

- comparing pole geometry across modes/conditions;
- describing the relative radial-versus-rotational position of a complex pole;
- Atlas coordinate mapping if provenance, units, uncertainty and derivation status are retained;
- testing whether particular second-order-like relationships recur empirically.

## 4. What the algebra does not license

A conjugate pair alone does not establish that:

- `alpha` is a literal physical neural damping coefficient;
- `omega_n` is a literal restoring-force frequency arising from one physical second-order coordinate;
- the identified state basis is a unique mechanistic basis;
- the mode is dynamically isolated from higher-order/non-normal/coupled structure;
- the same physical parameters persist across windows or systems;
- `zeta_pole` is a system-level stability coordinate;
- a whole neural system has one coherent chi;
- proximity to any target value is desirable or functional;
- the derived coordinate is the same scientific object as SymC chi in domains where gamma and omega are independently physical parameters.

Therefore `zeta_pole` must not be silently relabeled `chi` merely because the polynomial has second-order form.

## 5. Proposed admission hierarchy

This hierarchy is a draft for later qualification, not a frozen gate.

### Level S0: native pole only

Requirements:

- supported continuous-time pole pair;
- model adequacy sufficient for the pole claim;
- estimator/method uncertainty retained.

Allowed outputs:

- `sigma`, `omega`, frequency, decay and related native pole coordinates.

`chi`: WITHHELD.

### Level S1: algebraic spectral damping coordinate

Additional requirement:

- stable complex-conjugate pair for which the real quadratic factorization is valid and the transformation is explicitly recorded.

Allowed derived output:

`zeta_pole = -sigma / sqrt(sigma^2 + omega^2)`.

Interpretation:

**pole-geometry / algebraic second-order descriptor only**.

`chi`: still WITHHELD.

### Level S2: physically interpretable modal second-order coordinate

Would require independent scientific evidence that the claim object supports a meaningful second-order modal interpretation, including the relationship between the identified pole factor and physically interpretable damping/restoring quantities.

Possible evidence classes may include:

- a derived mechanistic/state reduction with independently meaningful coefficients;
- agreement with externally measured or independently modeled second-order parameters;
- perturbations that prospectively move the inferred parameters as the proposed mechanism predicts;
- adequate isolation or an explicit coupled-mode derivation showing how the effective modal parameters arise.

Only after such requirements are prospectively defined and qualified could a mode-level SymC-style `chi_mode` be considered.

### Level S3: system-level chi

Not implied by S2 and not part of System Model v1.0.

A system-level chi would require a separate derivation defining how multiple modes, subspaces, observable-order changes and conglomerate organization map to one scalar without erasing scientifically relevant structure. Such a derivation must survive independent testing and is not assumed to exist.

## 6. Uncertainty propagation

For an admitted S1 spectral coordinate

`zeta = alpha / sqrt(alpha^2 + beta^2)`,

its gradient is

`d zeta / d alpha = beta^2 / (alpha^2 + beta^2)^(3/2)`

`d zeta / d beta = -alpha beta / (alpha^2 + beta^2)^(3/2)`.

Therefore, if the joint covariance of `(alpha, beta)` is available,

`Var(zeta) ~= grad(zeta)^T Cov(alpha,beta) grad(zeta)`

under a first-order delta-method approximation.

Using only separate marginal standard errors while discarding covariance can misstate the derived uncertainty. Thus a future S1 Atlas coordinate should inherit the **joint pole-coordinate covariance**, not only separate frequency and decay errors.

P0-D7 currently establishes marginal pole-coordinate propagation but does not yet freeze a full calibrated joint covariance or a zeta uncertainty rule.

## 7. Special cases

### Real stable pole

For `beta = 0`, the pole is non-oscillatory. Algebraically one may obtain a repeated/real second-order factor only with additional structure, but an oscillatory damping-ratio interpretation is not automatically meaningful. NSD should not manufacture an oscillatory chi coordinate from a real-pole object.

### Unstable complex pole

For `alpha < 0` under the sign convention above, the mode is unstable. A formal pole-angle ratio can still be calculated, but it should not be passed through the same stable-damping interpretation without an explicitly separate definition.

### Crowded modes

When individual pole/carrier identity is unresolved but a joint subspace remains identifiable, an individual `zeta_pole` may be epistemically weaker than the supported subspace claim. Resolution gating therefore precedes derived scalar reporting.

## 8. Atlas consequence

The Neurostability Atlas should treat the objects distinctly:

- native `sigma`, `omega`, frequency, decay: eligible when the pole claim is supported;
- derived `zeta_pole`: potentially eligible as an explicitly labeled algebraic spectral coordinate after its own derivation/provenance schema is admitted;
- `chi_mode`: WITHHELD pending S2 physical admission;
- `chi_system`: WITHHELD pending a separate system-level derivation and validation.

This preserves useful mathematical information without allowing an attractive scalar to outrun its physical meaning.

## 9. Freeze boundary

This note does not freeze S1/S2/S3 admission criteria, confidence rules, numerical thresholds, or any chi coordinate. It records the algebraic derivation and the distinction that must be preserved in future qualification.