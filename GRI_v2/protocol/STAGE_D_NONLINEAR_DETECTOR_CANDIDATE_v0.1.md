# Stage D nonlinear detector candidate v0.1

Status: CANDIDATE TO BE FINALIZED AT D0.3 BEFORE BIOLOGICAL OUTCOME INSPECTION

Reason: upstream synthetic known-truth testing retained a nonlinear-only failure. Therefore a negative linear-kernel CKA/Spearman/ridge result cannot be interpreted as absence of cross-layer dependence.

## Candidate secondary detector

RBF-kernel CKA / HSIC on sample-space representations.

Candidate pre-outcome rules:
1. Standardize the frozen feature representation using training/control rules that do not use the target outcome.
2. Use squared Euclidean pairwise distances among samples.
3. Set the RBF bandwidth by a median-distance heuristic computed within the source representation only, before target response values are used.
4. Center Gram matrices with H = I - 11^T/n.
5. Compute RBF-CKA and an HSIC-based dependence statistic as separate reported values.
6. Calibrate against a deterministic patient/sample-label permutation distribution.
7. Refuse the nonlinear statistic if the median pairwise distance is zero/nonfinite, sample size is below the D0.3 minimum, or more than the frozen fraction of distances collapse numerically.
8. Synthetic calibration must include: independence, linear shared signal, nonlinear-only shared signal, confounder-only shared signal, and small-n instability.

## Interpretation

- Positive nonlinear-only result: `NONLINEAR_ONLY_SUPPORT` under the frozen secondary detector.
- Negative linear and negative nonlinear result: `NO_DETECTABLE_INFLUENCE_UNDER_SUPPORTED_DETECTORS`, not a universal statement of no relationship.
- The nonlinear branch cannot retroactively change a frozen linear primary endpoint.

Final bandwidth details, sample minimum, permutation count, and multiplicity family remain to be frozen at D0.3 after metadata/design support is known but before any Stage-D numeric biological matrix is interpreted.
