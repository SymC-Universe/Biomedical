# Tool Feasibility F2 Audit

**STATUS: CLOSED - `F2_GO_CANDIDATE`**

Date: 2026-08-30

## Scope

This is a synthetic known-truth engineering feasibility result only. It contains no Stage C1 methylation beta-value biology, no biomedical association, no mechanism claim, no clinical claim, no biological chi, and no historical CV/2 analysis.

Canonical inputs:

- `config/tool_feasibility_plan_v0_1.json`
- `docs/TOOL_FEASIBILITY_F2_EVALUATION_FREEZE_20260830.md`
- `docs/TOOL_FEASIBILITY_F2_PRERESULT_PROTOCOL_REPAIR_20260830.md`
- `docs/TOOL_FEASIBILITY_F2_PRERESULT_BEHAVIOR_COUNT_REPAIR_20260830.md`

The two protocol repairs occurred before any replicated F2 scenario output existed:

1. autonomy permutation count was changed from 12 to 19 because 12 permutations cannot resolve an empirical p-value of 0.05;
2. the scored-behavior count was corrected from 12 to 11 because S9 and S10 were prospectively defined as one paired autonomy behavior.

The first workflow attempt then failed mechanically before producing scenario results because Bernoulli missingness could violate the already-frozen S7 per-feature completeness floor. The repaired wrapper places exactly 3 missing cells per 80-sample feature (3.75%), preserving the frozen S7 truth condition. No scientific threshold or completed scenario result was changed.

## Execution

Successful GitHub Actions run: `33325429587`

Job: `99294598941`

Repository tests before sweep: **60 passed, 7 pre-existing B1 NumPy warnings**.

Replicated sweep:

- 24 replicates per scenario;
- 39 patient-row nulls for global CKA decisions;
- 39 module-label nulls for semantic decisions;
- 19 patient-row nulls for autonomy calibration;
- deterministic namespace `GRI_V2_TOOL_FEASIBILITY_20260830_F2`.

Artifact:

- ID `9736091098`
- name `GRI_V2_TOOL_FEASIBILITY_F2_20260830`
- SHA-256 `a9a1a9bf762e96454422b26141f056b8efc91f3381c0a170664892ac03dffc1f`

Canonical compact outputs are retained under:

`development_outputs/tool_feasibility_f2/`

## Frozen gate result

**10 of 11 scored behaviors passed.**

All mandatory safety behaviors passed:

- S0 independent: PASS
- S3 measured confounder only: PASS
- S6 technical false concordance: PASS
- S11 confounded false autonomy loss: PASS

Under the pre-result gate, this is `F2_GO_CANDIDATE`.

This means the architecture is sufficiently plausible to justify F3 baseline competition. It is not validation of a biomedical tool.

## Scenario results

### S0 - independent layers: PASS

- global-sharing nondetection rate: **1.00**
- median candidate autonomy: **1.00**

The initial auditor did not manufacture shared structure or loss of autonomy in the independent synthetic case.

### S1 - one shared mode: PASS

- global-sharing detection rate: **1.00**
- median `Delta_CKA`: **0.95175**
- median cross-validated modal predictive R2: **0.81749**
- S0 median predictive R2: **-0.06762**

Strong known shared structure was separated from the independent case.

### S2 - shared plus private modes: PASS

- global-sharing detection rate: **1.00**
- median target effective rank: **6.4733**
- median candidate autonomy: **0.63082**
- S10 low-autonomy median: **0.00**

The modal/conglomeration architecture detected shared geometry without forcing all target organization into the shared component.

### S3 - measured confounder only: PASS, mandatory safety

- raw global-sharing detection rate: **1.00**
- adjusted global-sharing nondetection rate: **1.00**
- median `Delta_CKA` drop after true confounder projection: **0.91757**

The confounder-generated apparent sharing collapsed under the correct measured-covariate projection.

### S4 - global sharing, semantic labels scrambled: PASS

- global-sharing detection rate: **1.00**
- semantic-sharing nondetection rate: **1.00**
- median semantic effect: **-0.00340**

Global sample geometry did not automatically create matched-module specificity.

### S5 - module-specific sharing with weak global alignment: PASS

- semantic-sharing detection rate: **1.00**
- global-sharing detection rate: **0.00**
- median semantic effect: **0.82378**

The conglomeration/module layer detected known matched structure that the global geometry decision did not promote.

### S6 - technical false concordance: PASS, mandatory safety

- raw global-sharing detection rate: **1.00**
- masked global-sharing nondetection rate: **1.00**
- median `Delta_CKA` drop: **0.98530**

A prospectively labeled technical subset could manufacture apparent sharing, and the known technical mask exposed it rather than allowing robust promotion.

### S7 - feature imbalance and controlled missingness: PASS

- complete-data global detection rate: **1.00**
- imputed-data global detection rate: **1.00**
- median absolute change in `Delta_CKA`: **0.00656**

The qualitative decision was stable under the frozen controlled-missingness condition.

### S8 - nonlinear-only relationship: FAIL

- linear-CKA global detection rate: **0.375**
- frozen maximum allowed rate: **0.30**
- median `Delta_CKA`: **0.03354**

The failure is retained.

The synthetic relationship used a symmetric quadratic latent transform intended to remove first-order linear cross-layer dependence in expectation. Nonetheless, the Gram-based linear CKA decision crossed the frozen significance/effect rule in 9 of 24 replicates.

This does **not** license changing the F2 threshold or generator. It establishes a limitation: the current global CKA layer cannot be described simply as a detector that safely ignores all nonlinear dependence. Linear CKA is built from linear kernels, but its squared cross-covariance / Gram-geometry statistic can retain finite-sample sensitivity under nonlinear dependent constructions, especially when repeated high-dimensional features amplify small empirical cross-moments.

Operational consequence for F3/tool design:

- do not advertise the current CKA gate as a general test of "linear dependence only";
- do not interpret a positive CKA result as proof of a linear biological mapping;
- retain an explicit scope/diagnostic warning for nonlinear or otherwise misspecified dependence;
- compare the global gate against simpler covariance/subspace baselines and, later, nonlinear dependence diagnostics if the tool proceeds.

S8 remains a failed F2 behavior.

### Paired S9/S10 - high coupling with high versus low autonomy: PASS

- paired autonomy ordering win rate: **1.00**
- median paired autonomy difference: **0.87239**
- S9 global-sharing detection rate: **1.00**
- S10 global-sharing detection rate: **1.00**
- S9 median autonomy: **0.87239**
- S10 median autonomy: **0.00**

The candidate distinguished retained target-private organization from dominant source-predictable target structure in this strong known-truth setting.

### S11 - confounded false autonomy loss: PASS, mandatory safety

- raw predictability exceeded its permutation null in **1.00** of replicates;
- adjusted predictability was nonsignificant in **1.00** of replicates;
- median autonomy gain after correct confounder projection: **0.79562**.

The candidate did not permanently interpret measured-confounder-generated predictability as loss of autonomy when the correct covariate was supplied.

## Scientific interpretation

F2 supports only the following engineering statement:

> Under strong replicated synthetic known-truth systems, the initial architecture can distinguish independence, genuine shared structure, shared-plus-private structure, measured-confounder-only sharing, global-versus-semantic sharing, technical false concordance, controlled missingness, and strong high-versus-low autonomy cases. It failed the prespecified nonlinear-only refusal criterion.

The synthetic signals are intentionally clear and are not evidence that real tumors will separate this cleanly.

## Next gate

Proceed to F3 baseline competition under:

`docs/TOOL_FEASIBILITY_F3_BASELINE_FREEZE_20260830.md`

The autonomy quantity remains a **candidate** until direct comparison with ordinary predictive R2 and established joint/individual subspace approaches. No novelty claim is licensed by F2.
