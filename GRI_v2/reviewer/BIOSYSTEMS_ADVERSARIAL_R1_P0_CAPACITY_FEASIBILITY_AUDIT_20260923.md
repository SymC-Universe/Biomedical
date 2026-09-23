# BioSystems adversarial Round 1 - P0 equal-capacity comparator feasibility audit

**Date:** 23 September 2026
**Status:** CLOSED / NEW POST-FINAL RECOMPUTATION NOT WARRANTED FOR THIS REVISION
**Branch:** `biosystems-adversarial-r1-20260923`
**Immutable parent:** `biosystems-resubmission-20260923-final` @ `18b1e3b6c828626143ac37da3fe279dd605751d5`
**Program authority:** SymC General Operations Manual v0.8.4

## Reviewer issue

The reported P0 prediction comparison uses approximately 45 methylation Hallmark scores plus two measured composition covariates against a two-covariate-only baseline. This is not an equal-capacity comparison and therefore cannot by itself establish Hallmark-specific representational advantage.

The criticism is valid.

## Historical provenance

The repository and prior audit trail establish:

- the P0 architecture was prospectively frozen with a 24-cancer pan-cancer promotion floor;
- only 19 cancers were P0-evaluable, so pan-cancer promotion was unavailable by construction;
- FINAL_HOLDOUT ultimately contained 18 primary-evaluable cancers after the frozen composition-complete n>=30 rule;
- the all-methylation model beat the two-covariate model in 17/18 FINAL_HOLDOUT cancers;
- a later manuscript lineage referred to a dimensionality-matched control as frozen, but the exact executable freeze was not recovered;
- `GRI_POSTFINAL_CAPACITY_CONTROL_PROVENANCE_DISCREPANCY_20260911.md` therefore correctly marks that historical capacity-control preregistration as unverified.

No new Round-1 document may retroactively call such a control preregistered.

## What would constitute a fair new P0-Q control

A scientifically meaningful post-FINAL comparator would need, at minimum:

1. the identical DISCOVERY / REPLICATION / FINAL_HOLDOUT participant partitions;
2. the same RNA target construction and held-out targets;
3. the same two measured composition covariates;
4. exactly 45 non-Hallmark methylation degrees of freedom plus the same two covariates;
5. discovery-only fitting/tuning of the alternate representation;
6. unchanged held-out evaluation metric;
7. no use of FINAL_HOLDOUT outcomes to choose the alternate representation.

A plausible benchmark would be 45 discovery-fitted generic methylation principal components plus the two covariates, evaluated against the same RNA Hallmark targets. Random 45-probe subsets would not provide a stable or representation-matched benchmark without an additional prospectively fixed ensemble rule.

## Reconstruction cost / evidence boundary

The exact participant-level FINAL feature matrices used by the historical P0 execution are not stored in the public repository.

Reconstructing a fair P0-Q comparator from source would require reopening the entire source-projection path, including:
- the 5.02 GB frozen methylation source;
- the 1.88 GB EB++ RNA source or exact Stage-A profile cache;
- split and sample-eligibility reconstruction;
- discovery-only methylation preprocessing;
- discovery-only RNA target transforms;
- generic 45-dimensional methylation representation fitting;
- untouched projection to FINAL_HOLDOUT;
- independent reconstruction checks against historical identities.

That would be a legitimate **new post-FINAL experiment**, not a cheap missing baseline and not part of the untouched original holdout.

## Round-1 decision

For this BioSystems revision:

1. P0 is removed from the Abstract's central evidence claims.
2. The 17/18 FINAL_HOLDOUT comparison is retained only as a bounded internal observation that methylation-derived predictors contained held-out information beyond the two measured covariates.
3. The manuscript explicitly states that the comparison does **not** isolate Hallmark-specific organization from generic methylation dimensionality, subtype, residual composition, or model capacity.
4. The 24-cancer promotion floor and 18-cancer FINAL denominator are stated explicitly.
5. No Hallmark-specific incremental-value claim is based on P0.
6. The nonexistent historical capacity-control preregistration is not referenced as though it were real.

Under GOM run-economy and claim-compression rules, rebuilding the full source pipeline solely to defend a claim that has now been withdrawn is not warranted for this revision.

## Future route

If P0 becomes central in a later predictive-method paper, the 45-generic-PC plus two-covariate comparator should be frozen prospectively as a new P0-Q branch before computing its result.

## Final disposition

`P0_CAPACITY_CRITICISM = VALID`

`P0_CENTRAL_PROMOTION = WITHDRAWN`

`NEW_P0_Q_RECOMPUTATION_FOR_CURRENT_BIOSYSTEMS_REVISION = NOT_WARRANTED_AFTER_CLAIM_COMPRESSION`
