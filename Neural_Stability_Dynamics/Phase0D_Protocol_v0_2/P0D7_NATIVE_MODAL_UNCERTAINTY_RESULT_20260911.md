# P0-D7 NSD-Native Modal Uncertainty Result

Date: 2026-09-11
Status: P0-D RESULT. NOT P0-Q. NOT P1.
Workflow run: `34610971064`
Job: `103301080134`
Artifact ID: `10267873244`
Artifact ZIP SHA256: `2d9f4fdad43dfffd2a88d2e742644ae48c86ccd8d4e69563df7b63054c529c53`

## Result

The NSD-native Hankel covariance-root candidate from P0-D5 was successfully propagated through the current fixed-order SSI-COV realization into native modal decay and frequency coordinates by symmetric perturb-and-refit first-order sensitivity.

All 192 requested record/cell evaluations completed without propagation failure: 2 conditions x 2 durations x 2 batch counts x 24 independent realizations.

### Local linearization

The numerical first-order propagation itself is highly stable over the tested perturbation steps. Comparing epsilon 0.25 versus 0.50, the median absolute log variance ratio within cells/modes/coordinates was approximately `0.00041` to `0.00211`.

This indicates that the tested perturbations lie in a strongly local/linear regime for these two separated oscillatory modes. The dominant remaining mismatch is therefore not finite-difference step instability.

### Predicted versus empirical variance

For epsilon 0.50, mean predicted variance divided by empirical across-realization variance was:

| condition | n | batches | mode 1 decay | mode 1 freq | mode 2 decay | mode 2 freq |
|---|---:|---:|---:|---:|---:|---:|
| nominal | 3600 | 6 | 1.003 | 0.960 | 0.734 | 0.923 |
| nominal | 3600 | 12 | 0.963 | 0.885 | 0.753 | 0.942 |
| nominal | 7200 | 6 | 1.600 | 1.169 | 1.161 | 1.104 |
| nominal | 7200 | 12 | 1.787 | 1.042 | 1.354 | 1.171 |
| white sensor 10% | 3600 | 6 | 1.033 | 0.959 | 0.737 | 0.936 |
| white sensor 10% | 3600 | 12 | 0.987 | 0.885 | 0.754 | 0.952 |
| white sensor 10% | 7200 | 6 | 1.600 | 1.164 | 1.134 | 1.123 |
| white sensor 10% | 7200 | 12 | 1.777 | 1.036 | 1.323 | 1.181 |

The white-sensor perturbation barely changes the pattern. Frequency variance is generally closer to empirical variability than decay variance. The sign and duration dependence of the mismatch closely follow the scale-calibration issue already observed in P0-D5 at the Hankel level.

## Interpretation

P0-D7 supports the following bounded statements:

1. **The exact NSD Hankel -> SSI realization -> pole-coordinate map can carry an estimator-native covariance root into finite, reproducible modal variance estimates.**
2. **The numerical first-order propagation is locally stable for the tested separated two-mode system.**
3. **The principal unresolved problem is sampling-covariance scale calibration, not the pole-propagation Jacobian itself.**
4. **Frequency and decay should remain separately calibrated.** Their variance behavior is not interchangeable.
5. **P0-D5 and P0-D7 form a coherent uncertainty chain:** Hankel variance shape is recovered strongly; that uncertainty propagates coherently to modal coordinates; duration/batch-dependent scale bias remains.

## What this does not establish

- no confidence interval;
- no nominal coverage rate;
- no batch-count choice;
- no epsilon freeze;
- no multiplicity convention;
- no carrier/subspace uncertainty;
- no P1 INDETERMINATE rule;
- no neural-data uncertainty validity.

## Next mathematical target

The next non-science-breaking uncertainty task is to diagnose and reduce the duration/batch-dependent scale bias in the NSD-native Hankel sampling covariance estimate while preserving the exact finite-sample NSD estimator. Candidate routes include time-series-aware covariance/influence estimation and calibrated resampling architectures. Any final estimator choice and confidence convention requires new qualification evidence before freeze.