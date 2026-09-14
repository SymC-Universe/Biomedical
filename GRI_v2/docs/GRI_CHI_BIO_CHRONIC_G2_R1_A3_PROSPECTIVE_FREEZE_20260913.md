# GRI Chi_bio chronic G2 R1/A3 prospective freeze

**Date:** 2026-09-13  
**Protocol authority:** `General_Cross_Project_Research_Protocol_v0.7.5_FINAL.md`  
**Machine freeze:** `config/gri_Chi_bio_chronic_g2_r1_A3_empirical_freeze_20260913_v1.json`  
**Freeze ID:** `GRI_CHI_BIO_CHRONIC_G2_R1_A3_20260913_V1`  
**Chi_bio status:** `NOT_ADMITTED`

## 1. Prospective firewall

This freeze was committed **before any chronic cetuximab temporal operator was fit**. The only numerical chronic RNA information inspected before freezing was source identity/anatomy/scale and the explicitly PBS-only state-design qualification. That qualification did not read any `C*.100nM` columns and did not fit a temporal operator.

The short-term GSE114446 empirical refusal is preserved as a separate completed pilot. Its outcome is not used to tune this weekly source. The reason D2 is opened here is the pre-outcome known-truth long-geometry calibration, which showed that 10+10 transitions can support a treatment-interaction operator while still preferring D1 when D1 is the truth.

## 2. Frozen source and state

RNA source:

```text
GSE98812_GEOExprsData.txt.gz
SHA-256: 1ce13bae71bd38f619261ec0ca5dcef5dd70b967083cee059e94758aaaf6abb5
20,531 gene rows
36 sample columns
```

The source study used RSEM gene-count output with upper-quartile normalization before downstream log transformation. The public processed table is therefore treated as an already normalized abundance matrix. The frozen transform is:

```text
x = log2(source_value + 1)
```

No CPM or library-size renormalization is permitted.

### PBS-only feature gate

Before freeze, an outcome-blind probe read only:

```text
C1.PBS ... C11.PBS
```

Primary gate, fixed before that probe:

```text
source_value >= 1 in at least 6/11 PBS states
```

Result:

```text
retained genes:                 14,767
retained-gene-ID SHA-256:       74dd1945ebb97a148a2a9effc3bbffdc2427d82476c8a461a0ec488f17384318
PBS-centered numerical rank:    10
cumulative variance r=2:        0.45561631362956706
cumulative variance r=3:        0.5540354985740922
qualification workflow run:     34769623766
qualification artifact:         10320569821
artifact SHA-256:               d58c611ede827c0c775a75cd6b7762317552fce16969eb78d3560625cd4e47f9
```

Diagnostic thresholds `0.1` and `10` were also recorded prospectively but are **not eligible to replace** the primary threshold after inspection.

## 3. A3 state reduction

For each retained gene, subtract its mean across the eleven PBS states. Fit SVD/PCA on PBS only, without gene-wise variance standardization. Project both PBS and cetuximab states through that frozen PBS basis.

Run `r=2` and `r=3` as coequal A3 representations. Neither may be selected as the preferred rank after outcomes. Component signs are canonicalized by making the largest-absolute loading positive.

## 4. Weekly transition geometry

Use only:

```text
PBS:  C1.PBS ... C11.PBS
CTX:  C1.100nM ... C11.100nM
```

Construct:

```text
10 PBS transitions: C1->C2 ... C10->C11
10 CTX transitions: C1->C2 ... C10->C11
20 total transitions
```

There is no shared measured day-0 state in this trajectory. The separate baseline and stable-resistant-clone samples are excluded from this first chronic operator test.

## 5. Frozen models

### D1 shared-operator null

```text
x_next = T x_now + B u + c
u = 0 PBS, 1 CTX
```

D1 is adequate at a rank only if all 20 LOTO refits are numerically admissible and aggregate LOTO NRMSE beats both frozen baselines:

1. persistence `pred = x_now`;
2. arm-specific leave-one-out mean next state.

### D2 operator-reorganization candidate

```text
x_next = T_control x_now + u DeltaT x_now + B u + c
T_treated = T_control + DeltaT
```

D2 is fit prospectively at both ranks regardless of whether D1 passes. It earns predictive reorganization support at a rank only when all D2 refits are admissible and:

1. D2 aggregate LOTO NRMSE beats persistence;
2. D2 aggregate LOTO NRMSE beats the arm-specific mean baseline;
3. D2 aggregate LOTO NRMSE beats D1;
4. D2 beats D1 on per-transition relative prediction error for at least **12/20** omitted transitions.

The `12/20` rule preserves the predeclared 60% win fraction used as `6/10` in the short-term architecture and was fixed before chronic CTX opening.

A cross-rank `REORGANIZATION_SUPPORTED` result requires D2 support at both `r=2` and `r=3`.

## 6. Numerical refusal

Every full fit and LOTO fit must have full declared design rank. Required predictor columns are Euclidean-normalized before condition-number SVD.

Refuse if:

```text
zero-norm required predictor
nonfinite singular value
rank deficiency
scaled condition number > 67,108,864
```

The ceiling is `1/sqrt(float64 epsilon)`, inherited prospectively from the already frozen G2 numerical contract. Error/spectral comparisons use the same `32 * float64 epsilon` tolerance convention.

## 7. Frozen uncertainty envelope

No iid bootstrap over serial weeks is permitted.

For each model/rank, the model-conditional sensitivity envelope contains:

1. point fit;
2. all 20 LOTO refits;
3. one paired earliest-transition block refit removing both PBS `C1->C2` and CTX `C1->C2`;
4. eleven leave-one-PBS-state basis refits, retaining the frozen feature universe, refitting the basis on ten PBS states, reprojecting all 22 states, then refitting the declared model.

A required-refit failure makes the corresponding spectral conclusion `INDETERMINATE`.

## 8. Spectral semantics

`rho(T)` and `sigma_max(T)` are mathematical diagnostics of the source-native one-week operator.

`BELOW` requires every required admissible refit to have `rho < 1`; `ABOVE` requires every one to have `rho > 1`; otherwise the result is `INDETERMINATE`. Boundary-touching within numerical tolerance is also `INDETERMINATE`.

For supported D2 only, the sign of

```text
rho(T_treated) - rho(T_control)
```

is interpretable only if its sign survives the complete required sensitivity envelope and agrees across both A3 ranks.

The non-normal warning remains the existing `rho < 1` with `sigma_max > 1` diagnostic.

None of these rules admits a biological `chi=1` boundary.

## 9. Timescale firewall

The GSE98812 operators are native **one-week** transition operators. Do not power, root, exponentiate, or otherwise convert them numerically into the one-day GSE114446 operators unless a separate semigroup/time-homogeneity test is later earned.

## 10. Reserved channels

The following remain closed during this first chronic transcriptomic execution:

```text
proliferation
ATAC-seq
single-cell RNA
methylation concatenation
biological unity boundary
Chi_bio computation
```

They remain later functional, relational, substrate, or carrier tests rather than ingredients used to force a first-pass transcriptomic result.

## 11. Immediate next action

The next permitted step is to implement and qualify the outcome-bearing chronic runner **without changing this freeze**, then open the exact hash-bound CTX trajectory once. Mechanical defects may be repaired transparently; scientific refusals are preserved.
