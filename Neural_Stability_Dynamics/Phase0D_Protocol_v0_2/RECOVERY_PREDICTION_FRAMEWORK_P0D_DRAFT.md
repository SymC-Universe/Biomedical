# Closed-Loop Recovery Prediction Framework

Date: 2026-09-11
Status: **P0-D DEVELOPMENTAL FRAMEWORK. NOT P0-Q. NOT P1. NO CLINICAL OR ATLAS THRESHOLDS FROZEN.**

## Purpose

Formalize the predictive idea that once an admitted system model includes subsystem dynamics, directed coupling, feedback-return transformations, and uncertainty, the model can be challenged to predict whether and how the coupled system returns after perturbation.

This is a prediction framework, not a diagnostic claim. It does not assume that chi alone determines recovery.

## Core local linear statement

For a locally adequate closed-loop generator `A_cl`, a small perturbation `delta x(0)` evolves as

`delta x(t) = exp(A_cl t) delta x(0)`.

Therefore prediction of recovery requires the coupled/closed-loop object, not only the uncoupled subsystem generators.

For a grouped subsystem `G` embedded in an environment `E`, the effective frequency-dependent feedback correction remains

`Sigma_G(s) = K_GE (sI - A_E)^(-1) K_EG`.

The quantity `Sigma_G(s)` represents what `G` sends into the environment, how the environment transforms it, and what returns to modify `G`.

## Distinct prediction targets

### R1. Asymptotic return

Define the spectral abscissa

`a(A_cl) = max_j Re(lambda_j(A_cl))`.

Within a valid local linearization:

- `a < 0`: sufficiently small perturbations decay asymptotically toward the local equilibrium;
- `a = 0`: marginal/boundary behavior requiring additional analysis;
- `a > 0`: at least one infinitesimal direction grows locally.

This statement is local and does not by itself establish global basin stability.

### R2. Recovery timescale

When `a < 0`, the slowest asymptotic exponential scale is related to `-1/a`. This is a dominant asymptotic timescale, not automatically a complete finite-time recovery time.

### R3. Transient amplification

A system can have `a < 0` and still amplify some perturbations transiently when the closed-loop generator is non-normal. Therefore stable poles alone are insufficient for a general finite-time recovery claim.

A physically meaningful transient-gain calculation requires a declared state/output metric; Euclidean norms must not be used across dimensionally heterogeneous state coordinates without normalization or a justified metric.

### R4. Basin retention / regime return

For nonlinear systems, asymptotic local stability of one equilibrium does not guarantee return after a finite perturbation. A sufficiently large perturbation may cross a basin boundary, trigger a different attractor, reorganize the active lineages, or invalidate the local model.

Accordingly, `RETURNS_TO_PRIOR_LOCAL_STATE`, `TRANSITIONS_TO_NEW_STABLE_STATE`, `FAILS_TO_RECOVER`, and `MODEL_NO_LONGER_ADEQUATE` are conceptually distinct outcomes.

### R5. Lineage recovery

A perturbation can preserve the global equilibrium while reorganizing modal lineages. NSD should therefore predict not only state return but also which admitted lineages persist, split, merge, disappear, emerge, or become unresolved during recovery.

### R6. Feedback pathway failure

Recovery may fail because a specific feedback-return pathway changes gain, phase, delay, saturation, or transformation. A pathway-level prediction should preserve directionality and identify which return operator changed rather than treating failure as a scalar deficit.

## Role of chi

Chi is not defined as probability of recovery, health, resilience, or diagnostic severity.

For a licensed second-order lineage `B_j`,

`chi_j = -tr(B_j) / (2 sqrt(det(B_j)))`

and

`Delta_chi,j = chi_j^2 - 1`.

Chi describes the stability geometry of that lineage across complex-pair, repeated-root, and real-split branches. A lineage may satisfy `chi > 1` and remain asymptotically stable. Therefore `chi > 1` must never be equated with loss of recovery.

The predictive use of chi is relational: coupling and feedback may move or reorganize global lineages, and those global/effective lineages may carry their own licensed chi coordinates. Their movement can then be related prospectively to recovery behavior without defining recovery from chi by fiat.

## Candidate predictive sequence

A mature prediction should eventually have this form:

1. identify the current admitted subsystem and global lineages;
2. estimate local chi coordinates where licensed;
3. estimate directed coupling / feedback-return architecture;
4. apply or observe a perturbation without using the future outcome for model selection;
5. predict the post-perturbation closed-loop generator or response family;
6. predict lineage persistence/reorganization and asymptotic recovery class;
7. attach uncertainty, adequacy, observability, and unresolved pathways;
8. score the prediction against untouched future observations;
9. allow explicit refusal when the model cannot support the requested resolution.

## First pre-Atlas falsification tests

### P0-D19A: fixed local dynamics, varied feedback, predicted return

Hold uncoupled subsystem generators fixed. Vary only directed feedback closure. For each coupled generator, calculate from the pre-perturbation model:

- global poles and spectral abscissa;
- global lineage chi values where algebraically licensed;
- feedback-return operators at declared frequencies/rates;
- exact response to a set of predeclared small perturbations.

Test whether changes in feedback predict changes in recovery dynamics while local subsystem chi remains fixed.

### P0-D19B: stable spectrum versus transient amplification

Construct or identify coupled generators with negative spectral abscissa but different non-normality. Use a dimensionless or explicitly justified state metric. Test whether some asymptotically stable systems exhibit larger transient excursions before recovery.

This tests the proposition that pole/chi information is necessary but not sufficient for finite-time resilience.

### P0-D19C: hierarchy-preserving prediction

Using the P0-D18 hierarchy construction, predict the outer-system response using both the full nested model and the reduced feedback-return representation. The reduced prediction should match the full model only to the degree that the reduction preserves the relevant input-output/feedback behavior.

### P0-D19D: deliberate model break

Introduce a perturbation that changes an unmodelled pathway or invalidates the local linearization. The correct outcome is not forced recovery prediction but an adequacy failure / refusal signal.

## Nonclaims and guardrails

- No claim that recovery is universally controlled by chi.
- No claim that chi=1 is a loss-of-stability threshold.
- No claim that chi=1.2-1.3 is a recovery target; the separately timestamped prospective note remains non-targeted and cannot steer this work.
- No clinical diagnosis or patient-level prognosis is authorized.
- No Atlas outcome is used to choose the model or prediction target.
- No recovery threshold, safety margin, confidence level, perturbation magnitude, or success region is frozen here.
- Local linear predictions apply only where model adequacy supports the local approximation.

## Working interpretation

The predictive opportunity is not merely to classify the present state. It is to reconstruct enough of the closed-loop interaction architecture to ask a counterfactual or prospective question:

`If this system is perturbed in this way, what does its own coupled feedback architecture predict will happen next, and what evidence would force the model to refuse?`

That is the pre-Atlas route from descriptive NSD to a genuinely predictive stability tool.