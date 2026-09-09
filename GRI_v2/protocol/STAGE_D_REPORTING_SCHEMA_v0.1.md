# Stage D Reporting Schema v0.1

Every Stage-D dataset report must contain the same top-level sections so favorable and unfavorable outcomes cannot be selectively emphasized.

## 1. Provenance
- accession/file hashes;
- repository commit/config hashes;
- environment/backend;
- sample manifest hash.

## 2. Evaluability
- total samples;
- retained samples;
- condition/timepoint counts;
- paired/unpaired structure;
- missingness/batch/platform status;
- exclusions with reasons.

## 3. Scalar view
Report every frozen scalar coordinate, uncertainty, and refusal state.

## 4. Modal view
Report frozen spectra/subspace quantities, uncertainty, and mode/subspace nonidentifiability.

## 5. Conglomeration view
Report frozen Hallmark/network/contact quantities, uncertainty, and mapping limitations.

## 6. Relationship R
Report view agreement/disagreement using the frozen relationship states.

## 7. Uncertainty U
Report uncertainty/refusal separately for scalar, modal, conglomeration, relationship, and lineage if used.

## 8. Primary perturbation/recovery result
Report observed endpoint(s), comparator(s), null(s), effect direction, and support.

## 9. Specificity/capacity controls
Report every frozen generic/scrambled/equal-dimensional comparator regardless of outcome.

## 10. Nonlinear secondary detector
Report whether it agrees, disagrees, or is non-evaluable. Do not use it to rewrite the linear primary.

## 11. Failure ledger
List every failed/null/nonidentifiable endpoint and why.

## 12. Claim status
State the highest satisfied promotion gate and every higher gate not satisfied.
