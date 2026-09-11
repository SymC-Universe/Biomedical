# NSD-Native Hankel Sampling-Covariance Candidate

Date: 2026-09-11
Protocol: General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum
Status: **P0-D DERIVATION / CALIBRATION CANDIDATE. NOT A P1 UNCERTAINTY PROCEDURE.**

## Why this step comes before modal intervals

The pyOMA2 P0-Q reference established an executable covariance-SSI uncertainty route but also showed that its finite-sample Hankel estimator is not identical to NSD's. Direct transfer of pyOMA2's Hankel covariance root is therefore refused.

Before propagating uncertainty into poles, frequency, decay or carrier quantities, NSD should first test whether it can estimate the sampling covariance of the **exact finite-sample Hankel object it actually computes**.

## Exact NSD finite-sample object

For a zero-mean samples-by-channels record `Y` of length `n`, NSD uses

`R_l = (1/(n-l)) sum_{t=l}^{n-1} y_t y_{t-l}^T`

for lag `l >= 1`.

With `b` block rows, the current covariance Hankel is assembled as

`H[i,j] = R_{i+j+1}`

for block indices `i,j = 0,...,b-1`.

This is the object whose finite-sample variability must be respected.

## P0-D batch covariance candidate

Split one globally centered record into `K` equal contiguous batches. For batch `k`, compute `H_k` with the same lag-specific `n_k-l` denominator used by the NSD estimator. Let

`h_k = vec(H_k)` and `h_bar = K^{-1} sum h_k`.

Define the exploratory covariance estimate

`Sigma_H_batch = [1/(K(K-1))] sum_k (h_k-h_bar)(h_k-h_bar)^T`.

Equivalently, a covariance-root representation has columns

`t_k = (h_k-h_bar)/sqrt(K(K-1))`

so `T T^T = Sigma_H_batch`.

The division by `K` relative to the ordinary sample covariance of batch estimates corresponds to the variance reduction for an average of `K` approximately independent equal-length batch estimates.

## Important limitations

This is **not claimed to be the exact covariance of the full-record NSD Hankel**. Contiguous batches are temporally dependent in a general process; pairs that cross batch boundaries are absent from `H_k`; finite-batch edge effects are lag-dependent; and the full record is not literally an average of the batch Hankels.

Those discrepancies are exactly why this is P0-D calibration rather than an adopted uncertainty rule.

## Calibration target

For one fixed synthetic system/observation map, generate many independent process realizations. Across the independent full-record Hankels, compute the empirical sampling covariance `Sigma_H_empirical`.

For each realization and each candidate `K`, compute `Sigma_H_batch`, then average the predicted diagonal variances over realizations.

Compare without a pass threshold:

- distribution of predicted/empirical diagonal-variance ratios for sufficiently nonzero entries;
- log-variance correlation;
- covariance-matrix relative Frobenius difference where interpretable;
- sensitivity to record duration;
- sensitivity to batch count;
- nominal versus perturbed noise conditions.

No `K`, duration, tolerance or coverage level is selected from the same map.

## Promotion firewall

If one batch-count/duration region looks favorable, that is a P0-D Function-Map result and creates promotion debt. It cannot become the final NSD uncertainty method without an independently generated P0-Q qualification.

Only after a sampling-covariance route for the actual NSD Hankel is independently supported should first-order or numerical sensitivity propagation into modal quantities be implemented and calibrated.
