# GRI Chi_bio chronic G2 empirical post-result audit

**Date:** 2026-09-13  
**Protocol authority:** `General_Cross_Project_Research_Protocol_v0.7.5_FINAL.md`  
**Freeze:** `GRI_CHI_BIO_CHRONIC_G2_R1_A3_20260913_V1`  
**Workflow run:** `34769901215`  
**Outcome artifact:** `10321342847`  
**Artifact SHA-256:** `4ad76198657cbb4f5a5839b5ad4068625ccb0801fe050d16b83006d2ef8a5687`  
**Chi_bio status:** `NOT_ADMITTED`

## 1. Firewall and execution status

This audit records the first result from the frozen GSE98812 SCC25 weekly G2 experiment. It does not amend preprocessing, feature selection, ranks, D1/D2 roles, predictive thresholds, sensitivity rules, or spectral semantics.

The chronology is preserved:

1. PBS-only source/design qualification completed without reading chronic CTX columns.
2. The chronic scientific contract was frozen.
3. The outcome-bearing engine was committed afterward.
4. The complete GRI test suite and frozen-contract validation passed.
5. Only then did the second CI job open the hash-bound CTX trajectory.
6. The outcome-bearing job completed successfully and uploaded the immutable result record.

The result is therefore not attributable to an aborted runner, missing source, source-hash drift, feature-gate drift, rank-deficient declared fit, or failed CI qualification.

## 2. Source identity reproduced exactly

```text
source: GSE98812_GEOExprsData.txt.gz
SHA-256: 1ce13bae71bd38f619261ec0ca5dcef5dd70b967083cee059e94758aaaf6abb5
source gene rows: 20,531
source sample columns: 36
retained genes: 14,767
retained-gene-ID SHA-256:
74dd1945ebb97a148a2a9effc3bbffdc2427d82476c8a461a0ec488f17384318
```

The runner used `log2(source_value + 1)` with no CPM renormalization and exactly 20 source-native weekly transitions, ten PBS plus ten 100 nM cetuximab.

## 3. Rank r=2

Frozen baselines:

```text
persistence NRMSE:                  1.0653881194731833
arm-specific LOTO mean NRMSE:      0.9339406350478573
```

### D1 shared operator

```text
D1 LOTO NRMSE:                      0.9067093706901029
full fit status:                    PASS
all 20 LOTO refits admissible:      true
D1 adequacy:                        PASS
point rho(T):                       0.8552726370980106
point sigma_max(T):                 0.8567067241123604
point non-normal warning:           false
scaled condition number:            3.1477116131059875
sensitivity rho range:              0.7119090891336093 .. 0.9159945617451319
unit-circle side:                   BELOW
non-normal warning disposition:     ABSENT
```

Relative to the frozen baselines, D1 lowers aggregate LOTO NRMSE by approximately:

```text
14.89% versus persistence
 2.92% versus arm-specific mean-next-state
```

This passes the predeclared adequacy rule, but the smaller margin versus the arm-specific mean baseline must be preserved as context rather than inflated into a large-effect claim.

### D2 treatment-interaction operator

```text
D2 LOTO NRMSE:                      0.9791317482524758
full fit status:                    PASS
all 20 LOTO refits admissible:      true
D2 wins versus D1:                  7 / 20
required wins:                      12 / 20
D2 reorganization support:          NOT_SUPPORTED
```

D2 has approximately 7.99% higher aggregate LOTO NRMSE than D1 and also fails to beat the arm-specific mean baseline. Therefore treatment-specific operator reorganization is not supported at `r=2` under the frozen predictive rule.

Its spectral quantities remain diagnostic only because predictive D2 support was not earned. They must not be used to claim treatment stabilization or destabilization.

## 4. Rank r=3

Frozen baselines:

```text
persistence NRMSE:                  1.1580949197915669
arm-specific LOTO mean NRMSE:      0.9598340407414122
```

### D1 shared operator

```text
D1 LOTO NRMSE:                      0.9431169152410929
full fit status:                    PASS
all 20 LOTO refits admissible:      true
D1 adequacy:                        PASS
point rho(T):                       0.8658280630749884
point sigma_max(T):                 0.8790156588516493
point non-normal warning:           false
scaled condition number:            3.149068924811844
sensitivity rho range:              0.6936386085403153 .. 0.9663473216372083
unit-circle side:                   BELOW
non-normal warning disposition:     INDETERMINATE
```

Relative to the frozen baselines, D1 lowers aggregate LOTO NRMSE by approximately:

```text
18.56% versus persistence
 1.74% versus arm-specific mean-next-state
```

Again, this passes the frozen predictive rule, with a modest margin versus the stronger arm-specific mean comparator.

The `INDETERMINATE` non-normal warning is not caused by the point fit. Warning-positive required sensitivity refits are:

```text
LOTO omitted transition indices:    0, 4, 6
paired earliest-transition block:   warning present
PBS-basis LOO omitted indices:      0, 1, 4
```

Representative sensitivity values remain `rho < 1` but cross `sigma_max = 1`, which is why transient amplification is representation/sensitivity dependent while the asymptotic unit-circle side remains consistently below one.

### D2 treatment-interaction operator

```text
D2 LOTO NRMSE:                      1.312273232727232
full fit status:                    PASS
all 20 LOTO refits admissible:      true
D2 wins versus D1:                  4 / 20
required wins:                      12 / 20
D2 reorganization support:          NOT_SUPPORTED
```

D2 has approximately 39.14% higher aggregate LOTO NRMSE than D1 and is worse than both frozen baselines. Treatment-specific operator reorganization is therefore not supported at `r=3`.

As at `r=2`, D2 spectral quantities are non-promotable diagnostics because predictive support was not earned.

## 5. Cross-rank result

The frozen material conclusions are:

```text
                         r=2             r=3
D1 adequacy              PASS            PASS
D1 unit-circle side      BELOW           BELOW
D1 non-normal warning    ABSENT          INDETERMINATE
D2 reorganization        NOT_SUPPORTED   NOT_SUPPORTED
```

The machine-level overall disposition is therefore correctly:

```text
REPRESENTATION_DEPENDENT_NO_TRANSFER
```

under the frozen rule that **any material A3 categorical disagreement** prevents a single transferable aggregate label.

However, the post-result audit must preserve the structure inside that label:

- predictive D1 adequacy is cross-rank concordant;
- D2 non-support is cross-rank concordant;
- the D1 mathematical unit-circle side is cross-rank concordant and remains BELOW throughout both required envelopes;
- only the non-normal/transient-amplification warning is representation dependent.

The formal overall label must not be rewritten, but neither should it be paraphrased as though both ranks disagree on predictive dynamics.

## 6. What this result supports

Under this source, feature universe, weekly interval, low-dimensional A3 representation, and frozen predictive rules, the data support a **shared weekly low-dimensional transition operator with treatment entering as forcing/input more strongly than a treatment-specific operator reorganization model**.

That statement is limited to the earned predictive comparison. It does not establish that cetuximab leaves the full biological network unchanged, and it does not rule out reorganization in omitted dimensions, regulatory-module coordinates, other intervals, single-cell states, chromatin states, or substrate/epigenetic organization.

## 7. What this result does not support

Do not claim from this result that:

- a biological `chi = 1` boundary has been observed;
- `Chi_bio` has been measured or admitted;
- cetuximab globally stabilizes the system because D2 treated `rho` is lower in point fits;
- D2 has been biologically falsified outside this R1/A3 weekly predictive test;
- the weekly operator can be numerically converted to the prior daily operator;
- serial weeks are biological replicates;
- the rank-3 transient warning is a stable biological feature.

## 8. Required next robustness move

The primary frozen result is closed and immutable. The pre-outcome source qualification also declared two bounded feature-threshold diagnostics:

```text
source_value >= 0.1 in at least 6/11 PBS states
source_value >= 10  in at least 6/11 PBS states
```

They were explicitly forbidden from replacing the primary threshold after inspection. They may now be used only as a **post-result bounded robustness audit** under v0.7.5 to ask whether the primary categorical conclusions are fragile to this already-declared control-only feature-universe perturbation.

That audit must:

1. retain the exact same transform, A3 ranks, transition geometry, D1/D2 models, numerical gates, 12/20 D2 win rule, and sensitivity envelope;
2. report both declared thresholds, not select the more favorable one;
3. leave the primary `source_value >= 1` result unchanged regardless of the diagnostic outcome;
4. keep `Chi_bio` and biological unity unadmitted.

After that bounded audit, the next independent scientific branch is the predeclared R2/B3 regulatory-module/functional-relational lane rather than repeated optimization of R1/A3.
