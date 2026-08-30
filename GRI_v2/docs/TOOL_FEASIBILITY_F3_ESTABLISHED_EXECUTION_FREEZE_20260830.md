# Tool Feasibility F3 established-comparator execution freeze

**STATUS: FROZEN BEFORE AJIVE / MOFA2 / DIVAS COMPARISON OUTPUTS**

Date: 2026-08-30

This document fixes the execution details for the established-method portion of the already-frozen F3 baseline plan. It does not modify Stage C1 v2, does not inspect Stage C1 beta-value biology, and does not alter the F2 result.

## 1. Purpose

F3 is an engineering/redundancy audit before the F4 GO / NARROW / STOP investment decision. It is not a novelty contest and not a biomedical validation result.

The primary question is whether the integrated auditor provides useful decision/calibration/refusal behavior beyond established shared/private decomposition methods. Novelty is tracked only as a diagnostic lens under `TOOL_PREDICTION_PROSPECTIVE_OBJECTIVE_AMENDMENT_20260830.md`.

## 2. Frozen synthetic input family

Use exactly the same deterministic generators and seed namespace used by the completed F2/F3-simple work. No generator parameters may be changed for these comparators.

Heavy third-party comparison uses the **first 8 deterministic replicates** (`replicate = 0..7`) for each required representation. This number is fixed before any established-method output is calculated and is chosen to limit third-party compute while preserving repeated known-truth comparisons.

Required representations:

- S0 raw
- S1 raw
- S2 raw
- S3 raw and correctly covariate-adjusted
- S4 raw
- S5 raw
- S6 raw and technical-mask representation
- S9 raw
- S10 raw
- S11 raw and correctly covariate-adjusted

These cover every contrast in the frozen F3 plan. No scenario is added or removed after method outputs are seen.

## 3. AJIVE B4

Implementation lineage:

- maintained repository: `idc9/mvdr`
- pinned commit: `ab04895a04a8f4e1b40e332591c736ba18bf8fd7`
- dependency `idc9/ya_pca` pinned commit: `77f633643e9b9e092fe6f62266e21129393d08f7`
- the Python 3.11 `inspect.getargspec` compatibility shim is permitted exactly as documented in the F3 smoke gate; it changes no AJIVE mathematics.

Frozen settings:

- `init_signal_ranks=[5,5]`
- no forced joint rank
- no forced individual ranks
- `check_joint_identif=True`
- `n_wedin_samples=100`
- `n_rand_samples=100`
- `n_jobs=1`
- centering enabled

Record:

- estimated joint rank;
- individual rank for each view;
- Frobenius-squared joint, individual, and residual/noise energy fractions for each view from AJIVE's reconstructed decomposition.

No post-result threshold is introduced to force a binary AJIVE verdict.

## 4. MOFA2 B5

Implementation:

- `mofapy2==0.7.5`
- two Gaussian views, one sample group;
- 5 factors fixed from the synthetic rank budget;
- no outcome supervision.

Frozen settings:

- `scale_groups=False`
- `scale_views=False`
- `factors=5`
- `spikeslab_factors=False`
- `spikeslab_weights=False`
- `ard_factors=False`
- `ard_weights=True`
- 300 maximum training iterations;
- fast convergence mode;
- deterministic per-scenario/per-replicate seed;
- quiet training output where supported.

Record factor-wise variance explained in both views using MOFA2's own `calculate_variance_explained` output.

To avoid inventing a factor-activity threshold after results, compare continuous quantities only:

- `shared_r2_mass = sum_k min(max(R2_Xk,0), max(R2_Yk,0))`
- `source_private_r2_mass = sum_k max(R2_Xk - R2_Yk, 0)`
- `target_private_r2_mass = sum_k max(R2_Yk - R2_Xk, 0)`
- `jointness_fraction = shared / (shared + source_private + target_private)` when denominator > 0.

These are descriptive summaries of MOFA2's variance-explained output, not new biological coordinates.

## 5. DIVAS B6

Implementation lineage:

- repository: `ByronSyun/DIVAS`
- pinned commit: `294986fac88bdeea1071902aa360b19e820c85de`
- package version: `0.1.1`
- package subdirectory: `pkg/`

Frozen settings:

- two named blocks (`SOURCE`, `TARGET`);
- input orientation features x samples as required by DIVAS;
- `nsim=50`;
- `iprint=FALSE`;
- `colCent=FALSE`;
- `rowCent=TRUE` so each feature is centered across matched samples;
- deterministic scenario/replicate seed;
- `ReturnDetail=TRUE` for auditable rank/decomposition extraction.

Record:

- dimensions of structures shared by both blocks;
- dimensions assigned to SOURCE-only and TARGET-only structures;
- available score/decomposition dimensions required to compare S9 versus S10 and raw versus adjusted confounding scenarios.

If the published implementation cannot evaluate a representation for a documented mathematical/software reason, record `NOT_EVALUABLE`. Do not substitute a weaker baseline.

## 6. Contrast evaluation

Use the seven contrasts already frozen in `TOOL_FEASIBILITY_F3_BASELINE_FREEZE_20260830.md`:

1. S0 independent versus S1 shared;
2. S1 genuine shared versus S3 confounder-only before/after correct adjustment;
3. shared geometry versus S4 semantic-label scramble;
4. S1 genuine shared versus S6 technical false concordance before/after mask;
5. S5 module-specific weak-global versus S0;
6. S9 high-coupling/high-autonomy versus S10 high-coupling/low-autonomy;
7. S11 raw confounded predictability versus correctly adjusted S11.

Established shared/private methods are not expected to solve semantic-label or technical-mask questions unless their native output genuinely does so. `NOT_SUPPLIED` is an informative outcome rather than a failure to force-fit another method.

## 7. F4 interpretation

The comparator result is combined with F2 and F3-simple evidence to choose:

- `GO`: take a narrowed integrated architecture into prospectively frozen prediction testing;
- `NARROW`: remove redundant named components but retain useful audit/prediction/refusal layers;
- `STOP`: do not invest further in the standalone architecture.

No F4 outcome validates a biomedical tool. Prediction and external validation remain mandatory downstream.

## 8. Claim ceiling

Synthetic methodological comparison only. No cancer mechanism, clinical utility, treatment response, biological chi, substrate inheritance, temporal dynamics, or Stage C1 biological claim is licensed.
