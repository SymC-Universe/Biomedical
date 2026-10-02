# Bio Chi C1Q-RS Repeated-Realization Uncertainty Map Plan v0.1

**Status:** APQ-2 SUBSTANTIAL DRAFT  
**Date:** 27 September 2026  
**Governed by:** SymC General Operations Manual v1.0  
**Lifecycle stage:** Stage 3, P0-D/P0-Q uncertainty qualification  
**Purpose:** empirical finite-sample uncertainty mapping for the preferred C1Q-RS qualification search implementation

## Scientific target

The search-route defect has been repaired and prospectively qualified. The next unresolved estimation question is not whether C1Q-RS can find a better basin, but how much finite-sample uncertainty remains in the recovered local coordinates across the intended C-family interior.

The native question is:

> Across new valid C truths, how dispersed, biased, and rate-sensitive are C1Q-RS estimates of local chi, g, and natural frequency under repeated stochastic realizations?

This plan does not define an admission threshold. It produces the empirical uncertainty map needed before any uncertainty-aware admission or predictive-closure tolerance can be designed.

## Claim ceiling

P0-D/P0-Q known-truth uncertainty qualification only.

A successful result may support statements about the sampling behavior of C1Q-RS under correct specification. It cannot:

- establish that biology belongs to C;
- promote C1Q-RS to production;
- define a biological threshold;
- license real EEG;
- estimate biological prevalence;
- erase semantic Limit Map failures.

## Frozen untouched uncertainty envelope

Eight new Sobol cells generated with SciPy Sobol dimension 4, `scramble=True`, seed `20260929`, within the same intended C interior:

| Cell | A | f_n Hz | chi | g |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0.808004818 | 14.655366315 | 0.508266046 | 0.584395017 |
| 1 | 0.287373873 | 12.656497417 | 0.230462532 | -0.441439599 |
| 2 | 0.503600127 | 22.101059450 | 0.757180555 | 0.086737482 |
| 3 | 0.677586268 | 6.585799037 | 0.326081456 | -0.142218795 |
| 4 | 0.595341533 | 22.291574446 | 0.247282106 | -0.220373040 |
| 5 | 0.422104721 | 5.021647139 | 0.669478590 | 0.352440502 |
| 6 | 0.292389809 | 18.952085106 | 0.496195269 | -0.719590691 |
| 7 | 0.813598516 | 9.736141725 | 0.765096168 | 0.650094895 |

Frozen realization seeds:

`989969, 353795, 292995, 180979, 415219, 783915, 881434, 585460, 100788, 562898, 806242, 577187`

These coordinates and seeds have not been used in the earlier C1Q-RS development or untouched qualification maps.

Sampling is fixed at:

- 60 s duration;
- 256 Hz fine rate;
- exact factor-2 same-path decimation to 128 Hz;
- fine/coarse pair treated as one metamorphic unit.

Total planned fits: (8	imes12	imes2=192).

## Estimator and implementation

Use the frozen preferred qualification search implementation C1Q-RS without modifying:

- likelihood;
- parameterization;
- parameter count;
- transformed bounds;
- legacy start family;
- recurrence-seed construction;
- optimization budgets;
- rescue behavior.

Legacy C1Q is not rerun in this uncertainty plan. Its search defect has already been established and repaired. Historical legacy comparisons remain preserved.

## Outputs

For each rate-level fit preserve:

- truth coordinates;
- fitted A, natural frequency, chi, g;
- signed and absolute errors;
- raw parameter coordinates;
- transformed boundary distances;
- recurrence-seed readiness and winner origin;
- NLL/BIC;
- optimizer success/start metadata.

For each truth cell and rate summarize the 12-realization empirical distribution:

- mean signed error;
- median signed error;
- median absolute error;
- 5th, 25th, 50th, 75th, 95th percentiles of fitted chi, g, and natural frequency;
- empirical standard deviation and median absolute deviation;
- minimum/maximum;
- boundary-attraction count;
- recurrence-start winning count;
- optimizer unresolved count.

For each same-path pair summarize:

- chi rate drift;
- g rate drift;
- natural-frequency rate drift.

Across cells, report descriptive associations between truth coordinates and dispersion using rank correlations only. These are exploratory and not causal.

## Mechanical preflight

Run cells 0 and 6 at seeds `989969` and `100788`.

Preflight may stop only for:

- invalid truth covariance;
- alias-safety failure;
- C1Q-RS execution/schema failure;
- design-identity mismatch;
- artifact/reproducibility failure.

Observed uncertainty magnitude cannot retune the design.

## Outcome architecture

**Broadly stable uncertainty:** most cells show centered, bounded sampling distributions with no repeated numerical-boundary pathology.

**Region-dependent uncertainty:** dispersion/bias differs materially by A, frequency, chi, g, or sampling rate. The result narrows the practical operating region but does not define a threshold.

**Weak-identification region:** repeated realizations produce wide or multimodal estimates, frequent boundary attraction, or large same-path rate drift despite correct family specification.

**Implementation failure:** repeated optimizer or schema failure prevents scientific interpretation.

**Need more information:** 12 realizations are insufficient to distinguish apparent regional structure from stochastic variation.

## Statistical meaning

Twelve realizations per cell provide an empirical sampling-distribution map, not biological replication and not a powered prevalence estimate.

The 5th/95th empirical quantiles are descriptive distribution summaries. They are not confidence intervals and are not admission thresholds.

No hypothesis test or multiplicity-adjusted significance claim is planned.

## Reproducibility class

Numerical/decision-equivalent repeatability is required in the declared software environment. Exact coordinate table, seed list, software versions, branch commit, and C1Q-RS implementation identity are recorded in artifacts.

## Dependency structure

Foundational:

1. exact C truth constructor remains valid;
2. C1Q-RS implementation remains frozen;
3. exact same-path decimation remains correct;
4. all eight cells remain alias-safe.

A shared mechanical failure stops execution. Poor recovery remains the result and does not trigger retuning.

## APQ request

`APQ-2 SUBSTANTIAL` because the map will determine whether uncertainty calibration can proceed toward a future admission architecture.
