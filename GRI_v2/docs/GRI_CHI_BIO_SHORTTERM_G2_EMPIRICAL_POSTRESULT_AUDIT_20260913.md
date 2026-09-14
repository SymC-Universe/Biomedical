# GRI Chi_bio short-term G2 empirical post-result audit

**Date:** 2026-09-13  
**Protocol authority:** `General_Cross_Project_Research_Protocol_v0.7.5_FINAL.md`  
**Research mode:** P0-D empirical temporal transport test  
**Source:** GSE114446 SCC25 short-term time course  
**Freeze:** `GRI_CHI_BIO_SHORTTERM_G2_R1_A3_20260913_V1`  
**Chi_bio status:** `NOT_ADMITTED`  
**Promotion effect:** `NONE_PILOT_EVIDENCE_REQUIRES_POSTRESULT_AUDIT`

## 1. Purpose and firewall

This file is a **post-result audit** of the already frozen short-term SCC25 G2 pilot. It does not amend the prospective freeze, reopen model selection, rescue a failed rank, or authorize outcome-driven preprocessing changes.

The scientific freeze was committed before the empirical engine. The outcome-bearing engine then executed on the frozen rules. This audit records the result that actually occurred.

## 2. Execution identity

GitHub Actions workflow `GRI Chi_bio short-term G2 empirical pilot` completed successfully on branch `gri-v071-protocol-integration-20260910-chi-bio` at head:

```text
7c6a4f1483ac53513fd10b707d8885607e2f56c8
```

Workflow run:

```text
34756865980
```

Both jobs were green:

1. frozen execution qualification / full GRI tests / empirical preflight;
2. frozen SCC25 short-term empirical execution.

Outcome artifact:

```text
gri-chi-bio-shortterm-g2-empirical-v1
artifact id: 10317941541
ZIP SHA-256: 9b6890012183f6d173df4092af1629098d6bd9591490c57c53e92a270f0be55f
```

Therefore the result below is not attributable to a failed runner, missing source, rank-deficient solve, or aborted workflow.

## 3. Source identity and preprocessing actually executed

Frozen source:

```text
GSE114446_STCCountsCG.txt.gz
SHA-256: c1318f5ad3b62d26c043de370cdca7300548337918f4543b13769bbe7a08a6c2
compressed bytes: 3,802,045
uncompressed bytes: 9,620,387
gene rows: 56,470
```

Frozen transformation:

```text
log2(CPM + 1)
```

with library totals computed before feature filtering.

Frozen outcome-blind feature gate:

```text
CPM >= 1 in at least 3/6 SCC25 PBS states
CTX excluded from feature selection
```

Retained genes:

```text
14,413
retained-gene-ID SHA-256:
572bbd7c8ee504456ca070a5f4e7ca0e9cb6a7a64a399dcbc2472227c454b232
```

The shared pretreatment day-0 convention remained in force. The declared empirical geometry contained 10 ordered transitions.

## 4. Primary D1 result

The prospective short-term architecture required D1 to establish predictive adequacy before D2 could be opened.

### Rank r=2

```text
D1 LOTO NRMSE:                    1.273329446532937
persistence baseline NRMSE:      1.178833035174781
arm-mean baseline NRMSE:         1.0825046455717018
point-fit rho(T):                0.5171638809730674
point-fit sigma_max(T):          0.6653314195820624
relative residual Frobenius:     0.6759222114674747
scaled condition number:         2.788140429574982
design rank:                     4 / 4
all LOTO refits admissible:       true
```

Prospective adequacy disposition:

```text
REFUSE
```

D1 failed to beat either frozen predictive baseline.

### Rank r=3

```text
D1 LOTO NRMSE:                    1.5481265365434007
persistence baseline NRMSE:      1.0769901679912097
arm-mean baseline NRMSE:         0.9894257253755194
point-fit rho(T):                0.6471029832150128
point-fit sigma_max(T):          0.76218670754602
relative residual Frobenius:     0.5913135817464447
scaled condition number:         5.2613027229354445
design rank:                     5 / 5
all LOTO refits admissible:       true
```

Prospective adequacy disposition:

```text
REFUSE
```

Again D1 failed to beat either frozen predictive baseline.

## 5. Sensitivity envelope and unit-circle disposition

The point estimates alone are not licensed to define a stability side.

### r=2

Across the predeclared sensitivity/refit envelope:

```text
rho_min = 0.37536442315407287
rho_max = 1.2484278574287935
```

Disposition:

```text
INDETERMINATE
```

### r=3

Across the predeclared sensitivity/refit envelope:

```text
rho_min = 0.4272245686780659
rho_max = 1.3310948236071525
```

The shared-origin-block sensitivity itself gave:

```text
rho(T) = 1.328696865930114
sigma_max(T) = 4.475423908763483
scaled condition number = 15.198534931527185
```

Disposition:

```text
INDETERMINATE
```

The envelope crossing the mathematical discrete-time unit circle is therefore material. The point-fit radii below one cannot be promoted into a biological stability claim.

## 6. D2 decision

The frozen D2 escalation rule was not earned at either rank:

```text
r=2: NOT_EARNED
r=3: NOT_EARNED
D2 evaluated: false
```

This is an important negative result. It means the short-term pilot **does not test or reject treatment-specific operator reorganization**. It says only that the prerequisite shared-operator D1 transfer model failed the prospectively frozen predictive-adequacy gate, so the protocol forbade opening the more flexible D2 model in this source/geometry.

D2 must not be opened post hoc on this same short-term outcome merely to seek a better-looking result.

## 7. Scientific interpretation

The earned disposition is:

```text
REPRESENTATION_DEPENDENT_NO_TRANSFER
```

The current R1/A3 short-term state representation does not earn a transferable D1 dynamical model under the frozen 10-transition geometry. This is a scientific refusal, not a mechanical failure.

The result does **not** establish any of the following:

- that SCC25 has no treatment-dependent dynamical reorganization;
- that no useful low-dimensional representation exists;
- that the system is mathematically stable or unstable;
- that a biological unity boundary has been observed;
- that `Chi_bio` has been measured;
- that the chronic weekly source should inherit the same model preference.

## 8. Required consequence

The short-term pilot is now closed under its frozen rules.

The next permissible empirical move is an **independent, prospectively frozen chronic SCC25 weekly test** using the previously identified 22-state / 20-transition source geometry. That source must receive its own source-specific transformation, feature-selection, state-reduction, day-0/trajectory, D1/D2, conditioning, refusal, and sensitivity freeze before any chronic outcome-bearing fit is opened.

The chronic design may use the already completed **pre-outcome synthetic long-geometry calibration** to choose its architecture. It may not use the numerical short-term outcome above to tune chronic thresholds or preprocessing.

R2/B3 and later functional/relational channels remain separate downstream tests and must not be used to rescue this R1/A3 result.

## 9. Status after audit

```text
short-term R1/A3 G2: CLOSED WITH PROSPECTIVE REFUSAL
D2 short-term:       NOT OPENED
unit-circle side:    INDETERMINATE
Chi_bio:             NOT_ADMITTED
biological unity:    NOT_ADMITTED
next gate:           CHRONIC SOURCE-SPECIFIC PRE-OUTCOME FREEZE
```
