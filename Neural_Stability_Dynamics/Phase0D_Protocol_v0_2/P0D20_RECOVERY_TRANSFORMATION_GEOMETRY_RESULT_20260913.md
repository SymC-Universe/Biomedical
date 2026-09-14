# P0-D20 Recovery Transformation Geometry Result

Date recorded: 2026-09-13
Execution date: 2026-09-13
Status: **P0-D exploratory synthetic evidence; not P0-Q or P1. No recovery threshold, chi_system rule, neural rule, or Atlas interpretation frozen.**
Purpose: `FUNCTION_MAPPING + LIMIT_MAPPING`

## Source of record
- Run `34749881567`, job `103704378679`
- Source commit `6c49a7931e574d6e6d92fd10bc385a1df736e18d`
- Dedicated workflow conclusion: `success`
- Recovery-transformation tests: `5 passed`
- Branch-wide P0 validation run `34749881536`: `success`
- Artifact `10315208274`
- Artifact ZIP SHA-256 `978d5490c4e7ccfa4f2c6892f6a6db2cadc5ce66b13b44d927481d2c6fd9d9a7`

## Question
With local subsystem generators fixed and outgoing/return edge spectral norms matched, does changing only feedback-transformation geometry alter asymptotic recovery and finite-time perturbation amplification?

This directly separates coupling magnitude from what the sending/receiving pathways do to the state that is transmitted and returned.

## Fixed construction
- Local subsystem 0: `chi=0.55`, `f=3 Hz`
- Local subsystem 1: `chi=0.85`, `f=5 Hz`
- Same coupling-rate grid and same edge-norm magnitude across transformation variants
- Synthetic dimensionless-state metric only
- Atlas not used
- Prospective `chi~1.2-1.3` note not used

## Results at g=12

| Transformation geometry | Spectral abscissa | Dominant tau (s) | Worst-case gain | Peak time (s) |
|---|---:|---:|---:|---:|
| position out / position return | -17.70361427 | 0.05648564 | 1.01266812 | 0.0125 |
| position out / velocity return | -8.28877631 | 0.12064507 | 1.00897073 | 0.0200 |
| velocity out / position return | -7.21408008 | 0.13861781 | 1.01347855 | 0.0125 |
| velocity out / velocity return | -9.71866263 | 0.10289482 | 1.00000000 | 0.0000 |
| mixed out / mixed return | -9.29300088 | 0.10760787 | 1.00677100 | 0.0150 |

All variants were asymptotically stable.

## Results at g=22

| Transformation geometry | Spectral abscissa | Dominant tau (s) | Worst-case gain | Peak time (s) |
|---|---:|---:|---:|---:|
| position out / position return | -1.81861785 | 0.54986813 | 1.13128298 | 0.0800 |
| position out / velocity return | -5.10607513 | 0.19584514 | 1.06664861 | 0.0475 |
| velocity out / position return | -3.06377068 | 0.32639519 | 1.09569762 | 0.0325 |
| velocity out / velocity return | -6.17576787 | 0.16192318 | 1.00000000 | 0.0000 |
| mixed out / mixed return | -7.08714163 | 0.14110061 | 1.08709414 | 0.0500 |

All variants remained asymptotically stable despite large differences in recovery rate and transient amplification.

## Supported P0-D interpretation
1. Coupling magnitude alone is insufficient to characterize recovery behavior.
2. Feedback transformation geometry is a dynamical variable in its own right.
3. Systems with identical local dynamics and matched edge norms can differ strongly in embedded recovery timescale and transient response.
4. The receiving/intermediary transformation is therefore part of conglomerate organization, not metadata external to it.
5. Asymptotic stability, recovery speed, and finite-time amplification remain distinct objects.
6. The result strengthens the relational-stability construction from P0-D16/P0-D17/P0-D19 without defining a scalar `chi_system`.

## Cross-project relevance
The result is consistent with the broader General Protocol v0.7.4 relational-stability architecture: local identity can remain fixed while embedded realized behavior changes through coupling, transformation, and feedback. Cross-domain recurrence may be recorded as a hypothesis-generating pattern but is not itself evidence of unbounded universality.

## Nonclaims
- No biological or anatomical meaning is assigned to the synthetic transformation templates.
- No neural coupling law is inferred.
- No recovery threshold or safety margin is selected.
- No `chi_system` is defined.
- No empirical Atlas zone is used or promoted.
- No support is claimed for the firewalled `chi~1.2-1.3` note.
- No clinical prediction is made.

## Next safe P0-D work
1. Test hierarchy-preserving recovery prediction using the P0-D18 grouped/nested feedback construction.
2. Add an effective-dimension / observability / crowding null-floor challenge before empirical promotion, motivated by the recent GRI confounding lesson.
3. Run a deliberate model-break/refusal case.
4. Perform the v0.7.4 milestone balance audit after the recovery sequence.
5. Only then decide whether any recovery-related construct is mature enough to propose for P0-Q qualification.
