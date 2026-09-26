# BioSystems Reproducibility Guide V30

**Manuscript ID:** BIOSYS-D-26-00267  
**Date:** 25 September 2026  
**Repository:** `SymC-Universe/Biomedical`  
**Reviewer branch:** `biosystems-v30-context-transport-20260925`  
**Immediate parent:** `biosystems-v29-direct-pmf-recovery-20260925` @ `4f3c2ea5f38ff94a37818c09a61fb0f9a99b9dfd`  
**Original oncology scientific parent:** `biosystems-v26-final-substantive-20260923` @ `509c4f3335d9020ea8e910579d6d98cb2fa9e58d`

## Status

The original C1/P1 oncology evidence spine remains unchanged. V30 adds a separately frozen same-source transport attack on the direct Meneses 2026 E. coli PMF experiment. The transport question is narrower than the V29 whole-event qualification: does the immediate multicoordinate motor-response organization preserve its geometry when osmolyte, buffer context, or clockwise-lock/strain context changes?

The answer is mixed by design rather than collapsed to a yes/no universal statement. Perturbation-depth ordering transports across every tested context, but the full recovery organization does not.

The private manuscript and Supplementary Information remain authoring artifacts. The public GitHub record contains the freezes, source identities, executable code, result pins, failure/refusal lineage, and reviewer commands.

## V1. Ancestry

**[CLAIM]** V30 is an overlay on V29 and does not rewrite the prior oncology or direct-recovery evidence.

```bash
git fetch origin   biosystems-v30-context-transport-20260925   biosystems-v29-direct-pmf-recovery-20260925

git merge-base --is-ancestor   4f3c2ea5f38ff94a37818c09a61fb0f9a99b9dfd   origin/biosystems-v30-context-transport-20260925

echo $?
```

**Expected output:** `0`.

For the direct experimental PMF qualification, source-method reconciliation, and preserved implementation-failure chronology, begin with the V29 guide:

`GRI_v2/reviewer/BIOSYSTEMS_REPRODUCIBILITY_GUIDE_20260925_V29.md`.

## V2. Frozen immediate-response transport test

**[CLAIM]** The Meneses immediate motor-response geometry is context dependent even though collapse magnitude remains monotonically dose ordered in every tested context.

**Scientific branch:** `bio-chi-meneses-context-transport-p0q-20260925`

**Frozen source and analysis identity**

- upstream repository: `wadhwalab/2026-Meneses-Osmotic`
- upstream commit: `d14d0caaa07299f13d1b1121d1e4630454fd724b`
- publication DOI: `10.1016/j.bpj.2026.04.014`
- freeze: `BIO_CHI/config/MENESES2026_IMMEDIATE_CONTEXT_TRANSPORT_P0Q_V01_FREEZE.json`
- preflight: `BIO_CHI/control/MENESES2026_IMMEDIATE_CONTEXT_TRANSPORT_PREFLIGHT_20260925.md`
- engine: `BIO_CHI/experiments/meneses2026_immediate_context_transport_p0q_v01.py`
- result pin: `BIO_CHI/config/MENESES2026_IMMEDIATE_CONTEXT_TRANSPORT_P0Q_V01_RESULT_PIN.json`
- closure: `BIO_CHI/control/MENESES2026_IMMEDIATE_CONTEXT_TRANSPORT_CLOSURE_20260925.md`
- workflow run: `36216876191`
- artifact: `10897867200`
- artifact SHA-256: `2bc6a34636d84954cb84f4c8bf9f841500f12a70a78b56d38e58250fb09ff0e6`
- result JSON SHA-256: `53debdf0a18cc73168b94c748437576437326b60ff8adb5dce133c7c0c845271`

**Reference context**

`sucrose_MB_CCW`: KAF95 CCW motors, sucrose shock, potassium-containing motility buffer.

**Target contexts**

- `sorbitol_MB_CCW`: non-ionic osmolyte changed from sucrose to sorbitol.
- `sucrose_SPB_CCW`: sucrose shock in sodium-phosphate buffer rather than potassium-phosphate motility buffer.
- `sucrose_CW_lock`: clockwise-locked HCB1797 preparation under sucrose shock. This also changes strain/plasmid background and is not interpreted as a pure rotor-direction intervention.

**Frozen lower representation**

At each of 200, 300, 400, and 500 mM, the condition vector is:

```text
(A_dec, tau_dec, tau_inc, recovery_endpoint)
```

Coordinates are standardized within context. The six pairwise Euclidean distances among the four dose conditions define context geometry. The target geometry is compared with the reference by Spearman correlation, and an exact one-sided p value is obtained from all 24 permutations of target dose labels.

Strong transport required geometry rho >= 0.8, exact p <= 0.10, and collapse-amplitude dose rho >= 0.8. Partial transport and refusal were frozen before output inspection.

**Command**

```bash
git fetch origin bio-chi-meneses-context-transport-p0q-20260925

git show   origin/bio-chi-meneses-context-transport-p0q-20260925:BIO_CHI/config/MENESES2026_IMMEDIATE_CONTEXT_TRANSPORT_P0Q_V01_RESULT_PIN.json
```

**Expected output**

```text
status = EXECUTED_VALID_P0Q
trace_count_pass = true
total source traces = 143

A_dec dose rho:
  sucrose_MB_CCW = 1.0
  sorbitol_MB_CCW = 1.0
  sucrose_SPB_CCW = 1.0
  sucrose_CW_lock = 1.0

sorbitol:
  geometry rho = 0.7714285714
  exact p = 0.0416666667
  PARTIAL_GEOMETRY_TRANSPORT_P0Q

sodium-phosphate buffer:
  geometry rho = -0.1428571429
  exact p = 0.5833333333
  GEOMETRY_TRANSPORT_REFUSED_P0Q

clockwise-lock/strain:
  geometry rho = 0.7714285714
  exact p = 0.0416666667
  PARTIAL_GEOMETRY_TRANSPORT_P0Q

Bio_Chi =
  IMMEDIATE_RESPONSE_ORGANIZATION_CONTEXT_DEPENDENT_P0Q
```

The frozen strong threshold is not relaxed for the two rho=0.7714 lanes.

## V3. Pooled representation

**[CLAIM]** Pooling the four contexts does not reveal a common one-dimensional response coordinate.

**Expected pinned values**

```text
singular values =
  [5.5851527819, 3.6112885222, 3.2173962143, 2.3265908994]

PC1 variance fraction =
  0.5198988599458688

maximum standardized 1D reconstruction residual =
  2.152137227372826

one-dimensional adequacy =
  false

Chi_bio =
  MULTICOORDINATE_IMMEDIATE_RESPONSE_ARCHITECTURE_REQUIRED_P0Q

chi_bio =
  NOT_OPENED_NOT_LICENSED
```

The fitted response times are empirical source-native summaries and are not relabeled as scalar biological damping coordinates.

## V4. SPB refusal root-cause audit

**[CLAIM]** The sodium-phosphate-buffer transport refusal is not explained by one bad coordinate, by switching median to mean, or by source-fit attrition. Under the frozen diagnostic it is classified as distributed context reorganization.

**Fixed identity**

- diagnostic freeze: `BIO_CHI/control/MENESES2026_CONTEXT_TRANSPORT_ROOT_CAUSE_FREEZE_20260925.md`
- diagnostic engine: `BIO_CHI/experiments/meneses2026_context_transport_root_cause_v01.py`
- diagnostic result pin: `BIO_CHI/config/MENESES2026_CONTEXT_TRANSPORT_ROOT_CAUSE_V01_RESULT_PIN.json`
- run: `36216972266`
- artifact: `10897118026`
- artifact SHA-256: `745555a472c0b8dbc1ce49ddcc19063c26968db3c070661327639f983488ce50`
- result JSON SHA-256: `7781f434be4c198c0b706a607afbe1f08394c052fba2d67a7d7362dc8070db2e`

**Command**

```bash
git show   origin/bio-chi-meneses-context-transport-p0q-20260925:BIO_CHI/config/MENESES2026_CONTEXT_TRANSPORT_ROOT_CAUSE_V01_RESULT_PIN.json
```

**Expected output**

```text
SPB primary geometry rho = -0.1428571429

leave-one-coordinate-out rho:
  omit A_dec = -0.1428571429
  omit tau_dec = 0.6000000000
  omit tau_inc = 0.4285714286
  omit recovery endpoint = -0.2571428571

mean-based geometry rho = 0.2571428571
mean-based exact p = 0.4166666667

trace bootstrap B = 2000
median rho = 0.0857142857
95% interval = [-0.7714285714, 0.8857142857]
fraction rho >= 0.5 = 0.1895
fraction rho >= 0.8 = 0.0480
fraction rho <= 0 = 0.4185

root cause =
  DISTRIBUTED_CONTEXT_REORGANIZATION
```

This is a post-result diagnostic. It explains the refusal but cannot promote or replace it.

## V5. Current biological chi interpretation

The Meneses sequence now supports a sharper hierarchy:

- **biological chi:** a directly measured perturbation-to-organization-to-recovery relation is admitted within this E. coli system;
- **modal/vector `Chi_bio`:** multicoordinate organization is required, both within the original recovery experiment and across the transport panel;
- **scalar `chi_bio`:** remains unopened/unlicensed.

The transport result further shows that a conserved perturbation-depth response can coexist with context-dependent internal organization. A one-number amplitude description would preserve the common dose trend while hiding changes in collapse timing, recovery timing, and endpoint organization.

This is not independent cross-source replication. It is same-source P0-Q transport evidence. The clockwise-lock lane carries a strain/plasmid-background caveat, and the SPB refusal does not isolate a potassium-specific causal mechanism.

## V6. V30 smoke test

```bash
set -e

git fetch origin   biosystems-v30-context-transport-20260925   biosystems-v29-direct-pmf-recovery-20260925   bio-chi-meneses-context-transport-p0q-20260925

git merge-base --is-ancestor   4f3c2ea5f38ff94a37818c09a61fb0f9a99b9dfd   origin/biosystems-v30-context-transport-20260925

git show   origin/bio-chi-meneses-context-transport-p0q-20260925:BIO_CHI/config/MENESES2026_IMMEDIATE_CONTEXT_TRANSPORT_P0Q_V01_RESULT_PIN.json   | grep -q IMMEDIATE_RESPONSE_ORGANIZATION_CONTEXT_DEPENDENT_P0Q

git show   origin/bio-chi-meneses-context-transport-p0q-20260925:BIO_CHI/config/MENESES2026_IMMEDIATE_CONTEXT_TRANSPORT_P0Q_V01_RESULT_PIN.json   | grep -q MULTICOORDINATE_IMMEDIATE_RESPONSE_ARCHITECTURE_REQUIRED_P0Q

git show   origin/bio-chi-meneses-context-transport-p0q-20260925:BIO_CHI/config/MENESES2026_IMMEDIATE_CONTEXT_TRANSPORT_P0Q_V01_RESULT_PIN.json   | grep -q GEOMETRY_TRANSPORT_REFUSED_P0Q

git show   origin/bio-chi-meneses-context-transport-p0q-20260925:BIO_CHI/config/MENESES2026_CONTEXT_TRANSPORT_ROOT_CAUSE_V01_RESULT_PIN.json   | grep -q DISTRIBUTED_CONTEXT_REORGANIZATION

echo V30_SMOKE_TEST_PASS
```

**Expected output**

```text
V30_SMOKE_TEST_PASS
```

## What happens next

The Meneses source family has now answered the questions it can answer efficiently: direct collapse/recovery, representation depth, source-method robustness, same-source context transport, a frozen transport refusal, and root-cause analysis of that refusal.

The next experiment should use an independent acquisition lineage with longitudinal perturbation/recovery data. This reduces source-specific overfitting and tests whether context-dependent multicoordinate organization itself transports across biological systems.

## What the user needs to do

Nothing is required at this checkpoint.
