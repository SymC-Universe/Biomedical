# Bio Chi C1Q-RS Repeated-Realization Uncertainty Map Plan v0.2

**Status:** APQ-2 QUALIFIED CANDIDATE  
**Date:** 27 September 2026  
**Governed by:** SymC General Operations Manual v1.0  
**Lifecycle stage:** Stage 3, P0-D/P0-Q uncertainty qualification  
**Purpose:** empirical estimator sampling-distribution mapping under correct C-family specification  
**APQ ledger:** `NSD_vNext/docs/BIO_CHI_C1Q_RS_UNCERTAINTY_APQ_LEDGER_v0.1.md`

## Scientific target

Across new valid C truths, quantify the finite-sample sampling behavior of the preferred C1Q-RS qualification search implementation at 256 Hz and exact same-path 128 Hz decimation.

This is an estimator uncertainty map conditional on the C model being correct. It is not a model-uncertainty analysis and not a biological uncertainty claim.

## Claim ceiling

P0-D/P0-Q known-truth qualification only. No biological prevalence, empirical admission threshold, production promotion, C-family membership claim, or real-EEG local chi can follow from this map.

## Frozen truth envelope

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

Frozen seeds:

`989969, 353795, 292995, 180979, 415219, 783915, 881434, 585460, 100788, 562898, 806242, 577187`

Sampling:

- 60 s duration;
- 256 Hz fine rate;
- exact factor-2 same-path decimation to 128 Hz;
- 192 rate-level fits total;
- 96 fine/coarse paired units.

The synthetic design is a qualification envelope, not a biological prevalence model.

## Estimator

Use unchanged C1Q-RS as the preferred qualification search implementation. Do not alter likelihood, parameterization, bounds, start family, recurrence-seed logic, optimization budgets, or rescue behavior.

Legacy C1Q is not rerun.

## Mechanical preflight

Cells 0 and 6, seeds `989969` and `100788`.

Preflight may stop only for invalid truth covariance, alias-safety violation, C1Q-RS runtime/schema failure, design mismatch, or artifact/reproducibility failure. Scientific recovery cannot retune the plan.

## Row-level outputs

For every rate-level fit preserve:

- cell and seed;
- truth A, (1-A), frequency, chi, g;
- duration and cycles observed (f_n	imes60);
- fitted A, natural frequency, chi, g;
- signed and absolute errors;
- NLL/BIC;
- recurrence-seed admissibility and winning-origin metadata;
- attempted/converged optimizer starts;
- raw optimized coordinates;
- minimum raw-box edge distance;
- numerical raw-boundary flag defined prospectively as raw-box edge distance <= (10^{-6});
- transformed g-boundary distance (1-|g|).

No boundary row is dropped from the distribution.

## Cell/rate summaries

For each cell and rate across 12 realizations report:

- row count;
- mean and median signed error;
- median absolute error;
- mean and standard deviation of fitted coordinate;
- median absolute deviation;
- 25th, 50th, 75th percentiles;
- minimum and maximum;
- numerical raw-boundary count;
- recurrence-seed-ready count;
- recurrence-winning count;
- optimizer unresolved count.

The full 12 fitted values remain available, so summaries cannot hide multimodal or outlying behavior.

No 5th/95th interval, confidence interval, coverage claim, or admission threshold is defined.

## Same-path rate summaries

For each cell and seed report absolute fine/coarse drift in chi, g, and natural frequency. Summarize their full distribution, median, quartiles, range, MAD, and SD.

Rate drift is practical estimator sensitivity under fixed duration, not a test of the exact continuous-lineage invariance theorem.

## Cross-cell interpretation

Because there are only eight truth locations, cross-cell relationships are descriptive only. Plot and tabulate dispersion against A, observation-noise fraction, frequency, chi, g, and cycles observed. Do not infer a causal parameter dependence or a general envelope law.

## Outcome architecture

**Broadly stable estimator sampling behavior:** repeated estimates remain centered and comparatively compact across most truth/rate cells without recurrent numerical-boundary attraction.

**Region-dependent sampling behavior:** bias or dispersion differs visibly among truth cells/rates. This narrows practical qualification interpretation but does not define a threshold.

**Weak/unstable region:** repeated realizations produce broad, boundary-attracted, or strongly rate-sensitive estimates even under correct specification.

**Implementation failure:** repeated runtime/schema/optimizer failure prevents a meaningful uncertainty map.

**Need more information:** twelve realizations do not support a stable qualitative interpretation for a cell.

## Reproducibility

Numerical/decision-equivalent repeatability in the declared Python/NumPy/SciPy environment. Artifact records exact cells, seeds, RNG rule, environment, commit, and row-level output.

## Dependency structure

Truth construction, alias safety, C1Q-RS identity, and same-path decimation are foundational. Mechanical failure stops execution. Poor recovery or wide dispersion is preserved as the scientific result.

## APQ closure

Two role-isolated first passes completed. No unresolved BLOCKER or MATERIAL objection remains. The plan is eligible for freeze.
