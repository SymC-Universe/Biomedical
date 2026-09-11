# P0-D7 NSD-Native Modal Uncertainty Propagation Plan

Date: 2026-09-11
Protocol: General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum
Status: P0-D DERIVATION / CALIBRATION. NOT P0-Q. NOT P1.

## Question

Can the NSD-native sampling-covariance root already constructed for the exact finite-sample covariance Hankel be propagated through the actual fixed-order SSI-COV realization to recover useful sampling-variance information for native pole coordinates?

This is the next mathematical step after P0-D5. It does not select a confidence level, uncertainty threshold, batch count, model order or P1 INDETERMINATE rule.

## Lineage

Published SSI uncertainty work propagates uncertainty from output-correlation estimates through the state-space/modal identification map using first-order sensitivity. Subsequent work validates predicted modal variance against observed repeated-measurement variability. Recent work also studies simulation/perturbation routes that sample correlation objects and rerun SSI. NSD must preserve this lineage while remaining estimator-native because its finite-sample covariance estimator differs from the external pyOMA2 route already audited.

## NSD-native route

For a fixed supported order r, the current NSD map is

H -> SVD(H) -> extended observability O_r -> state transition F_r -> eig(F_r) -> continuous poles lambda_j = log(mu_j)/dt.

P0-D5 supplies a low-rank root T such that T T^T approximates the sampling covariance of vec(H) for the exact current NSD Hankel estimator.

For each root direction t_k, perturb the structured Hankel locally:

vec(H_k^+) = vec(H) + epsilon t_k
vec(H_k^-) = vec(H) - epsilon t_k

Rerun the same fixed-order SSI map and match each perturbed positive-frequency pole back to the base pole. The central directional derivative of a native coordinate q is approximated by

D_k q = [q(H_k^+) - q(H_k^-)] / (2 epsilon).

Because T is a covariance root, the first-order propagated variance estimate is

Var(q) ~= sum_k (D_k q)^2.

This is a numerical first-order sensitivity calculation. It introduces no new estimator and no scientific selector.

## Coordinates tested first

- continuous-time decay coordinate alpha_j = -Re(lambda_j), where stable;
- frequency f_j = Im(lambda_j)/(2 pi) for positive-frequency modes.

Carrier/subspace uncertainty is deliberately deferred until the pole route is mechanically and empirically characterized.

## P0-D calibration

Reuse the P0-D5 fixed-system synthetic construction with independent process realizations:

- two stable oscillatory modes;
- 4 observed channels;
- durations 3600 and 7200 samples;
- nominal and 10% white-sensor perturbation;
- batch counts 6 and 12;
- 24 independent realizations per condition;
- fixed order 4;
- no data-derived threshold selection.

For each truth mode and native coordinate compare:

1. empirical across-realization variance of the SSI estimate;
2. mean and median propagated variance predicted from each record;
3. predicted/empirical variance ratio;
4. estimator bias separately from sampling variance;
5. descriptive standardized error |estimate-truth|/predicted SE;
6. local finite-difference sensitivity to epsilon as a linearization diagnostic.

## Failure modes preserved

- perturbed fit changes modal count;
- pole assignment becomes ambiguous;
- finite-difference result changes materially with epsilon;
- predicted variance is nonfinite or zero for a varying coordinate;
- crowding/order ambiguity dominates scalar pole SE;
- systematic estimator bias is large relative to sampling SE.

Such events are open-channel outputs, not silently discarded records.

## Nonclaims

- No confidence interval is licensed by P0-D7.
- No nominal coverage claim is made.
- No batch count is selected.
- No epsilon is frozen as a scientific setting.
- No uncertainty threshold or P1 INDETERMINATE rule is selected.
- No carrier/subspace uncertainty is claimed.
- No neural-data validity follows from synthetic calibration.

## Promotion condition

If the estimator-native pole variance has coherent scale and ranking behavior, a later untouched P0-Q design may qualify a frozen propagation implementation and confidence/adjudication convention. If it does not, MFR-09 remains blocked and the failure is retained.