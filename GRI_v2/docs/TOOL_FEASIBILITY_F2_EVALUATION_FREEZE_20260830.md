# Tool Feasibility F2 replicated synthetic evaluation freeze

**STATUS: FROZEN BEFORE THE REPLICATED F2 SWEEP**

Date: 2026-08-30

This document operationalizes `config/tool_feasibility_plan_v0_1.json` for the replicated synthetic challenge. It does not alter the frozen Stage C1 v2 biological contract and does not use or inspect Stage C1 beta-value biology.

The initial F1 regression tests have already established that the code behaves sensibly on a small number of strong deterministic examples. Those tests are treated as engineering smoke tests only. The replicated F2 criteria below are fixed before generating the F2 sweep artifact and are not tuned to maximize pass rate.

## 1. Replication design

- deterministic seed namespace: `GRI_V2_TOOL_FEASIBILITY_20260830_F2`
- 24 independent synthetic replicates per scenario unless a scenario is explicitly evaluated as a paired comparison;
- global sample-geometry null: 39 deterministic patient-row permutations per replicate;
- semantic/module null: 39 deterministic module-label permutations per replicate;
- autonomy calibration: 12 deterministic patient-row permutations inside the cross-validated modal-predictability calibration for autonomy scenarios;
- default synthetic sample size: 80, increased to 120 for the nonlinear-only challenge;
- feature dimensions may differ by layer and scenario;
- no outcome labels, TCGA methylation beta values, or C1 biological results are used.

Permutation resolution with 39 global/semantic null replicates is sufficient for a one-sided empirical p-value of 0.025. The synthetic gate is an engineering feasibility challenge, not a biomedical hypothesis-testing family.

## 2. Generic decision primitives

### 2.1 Global shared-geometry detection

For each replicate:

- `CKA_obs = linear_cka(A,B)`;
- construct 39 patient-row-permuted A null values against fixed B;
- `Delta_CKA = CKA_obs - median(CKA_null)`;
- empirical one-sided `p = (1 + count(null >= observed)) / 40`.

A replicate is classified as `GLOBAL_SHARED_DETECTED` only when:

- empirical `p <= 0.05`; and
- `Delta_CKA >= 0.05`.

This dual condition prevents a tiny but stable numerical difference from being treated as meaningful shared geometry.

### 2.2 Semantic/module-specific detection

For matched module-score matrices:

- observed statistic is median absolute same-module Spearman correlation;
- construct 39 module-label permutation null values;
- `Delta_semantic = observed - median(label_null)`;
- empirical one-sided p-value as above.

A replicate is classified as `SEMANTIC_SHARED_DETECTED` only when:

- empirical `p <= 0.05`; and
- `Delta_semantic >= 0.10`.

### 2.3 Autonomy candidate

Regulatory autonomy remains a candidate measurement, not an admitted biological coordinate.

For source/substrate matrix S and regulatory/target matrix R:

- estimate cross-validated modal predictability of target modes from source modes;
- calibrate predictability against deterministic patient-row permutation;
- candidate autonomy is `1 - clip(observed_R2 - median(null_R2), 0, 1)`.

The autonomy question is evaluated primarily by **paired ordering and confounder correction**, not by a universal biological cutoff.

## 3. Scenario-level required behavior

A scenario passes when at least 80% of its 24 replicates satisfy the stated replicate-level behavior, except paired autonomy comparisons where the stated paired win rate and median difference apply.

### S0 independent

- global sharing must **not** be detected in at least 90% of replicates;
- median candidate autonomy must be >= 0.85.

This is a mandatory safety scenario.

### S1 one shared mode

- global sharing detected in at least 80% of replicates;
- median `Delta_CKA > 0`;
- cross-validated modal predictability exceeds the independent S0 median.

### S2 shared plus private modes

- global sharing detected in at least 80% of replicates;
- target effective rank remains > 2 at the scenario median;
- median candidate autonomy is greater than the low-autonomy S10 median, showing that detectable coupling does not force full predictability.

### S3 measured confounder only

- raw global sharing detected in at least 80% of replicates;
- after projection of the true measured confounder, global sharing must **not** be detected in at least 90% of replicates;
- median adjusted `Delta_CKA` must fall by at least 0.10 from raw.

This is a mandatory safety scenario.

### S4 global sharing with labels scrambled

- global sharing detected in at least 80% of replicates;
- semantic same-module sharing must **not** be detected in at least 90% of replicates.

### S5 module-specific sharing with weak global alignment

- semantic sharing detected in at least 80% of replicates;
- global sharing detected in no more than 30% of replicates.

This tests whether the semantic layer can carry information not reducible to the global CKA decision.

### S6 technical false concordance

The synthetic generator labels the contaminating feature subset prospectively.

- unmasked data show global sharing in at least 80% of replicates;
- after removing the known contaminating features, global sharing must **not** be detected in at least 90% of replicates;
- median `Delta_CKA` reduction is at least 0.10.

This is a mandatory safety scenario.

### S7 feature imbalance and controlled missingness

A matched shared truth is generated with unequal feature counts. Random missing cells are introduced below the stated completeness ceiling and median-imputed without using cross-layer outcomes.

- both complete and imputed representations detect global sharing in at least 80% of replicates;
- median absolute change in `Delta_CKA` is <= 0.10.

### S8 nonlinear-only sharing outside the initial linear scope

A symmetric nonlinear relationship is generated such that first-order linear cross-layer dependence is absent in expectation.

- global linear sharing is detected in no more than 30% of replicates.

Passing this scenario means the linear tool under-detects/refuses rather than manufacturing a linear claim. It does **not** mean nonlinear dependence is absent.

### S9 versus S10 autonomy ordering

S9 and S10 are generated as paired replicates with comparable shared-signal strength:

- S9 contains strong target-private modes;
- S10 is dominated by source-predictable target modes.

Required behavior:

- `autonomy_S9 > autonomy_S10` in at least 80% of paired replicates;
- median paired autonomy difference >= 0.20;
- both scenarios retain detectable global sharing in at least 80% of replicates.

### S11 confounded false autonomy loss

- raw source->target predictability must exceed its patient-permutation null in at least 80% of replicates;
- after projecting the true measured confounder from both layers, median candidate autonomy must increase by at least 0.20;
- adjusted predictability must fail empirical permutation significance in at least 80% of replicates.

This is a mandatory safety scenario.

## 4. F2 gate interpretation

The F2 result is classified before baseline competition as follows.

### `F2_GO_CANDIDATE`

- all mandatory safety scenarios S0, S3, S6, and S11 pass; and
- at least 10 of the 12 scenario behaviors pass, counting the paired S9/S10 autonomy test as one behavior and S9/S10 global-sharing support within that behavior.

### `F2_NARROW_CANDIDATE`

- all mandatory safety scenarios pass; and
- 7 to 9 scenario behaviors pass.

The failing capabilities are removed from the candidate tool before F3 rather than repaired by changing the synthetic truth definitions.

### `F2_STOP_SIGNAL`

- any mandatory safety scenario fails; or
- fewer than 7 scenario behaviors pass.

A STOP signal prevents promotion of the architecture as a standalone tool. It does not invalidate the already-frozen C1 scientific question.

## 5. No post-result rescue

After the replicated sweep is generated, do not change:

- scenario truth definitions;
- signal/noise parameters of completed scenarios;
- null counts;
- detection thresholds;
- pass-rate thresholds;
- mandatory safety scenarios;
- autonomy formula used in this F2 sweep.

If a capability fails, retain the failure. A materially different estimator may be explored later only as a new version and may not retroactively convert this F2 result into a pass.
