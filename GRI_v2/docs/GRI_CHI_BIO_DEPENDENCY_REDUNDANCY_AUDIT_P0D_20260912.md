# GRI Chi_bio dependency and redundancy audit

**Date:** 2026-09-12  
**Status:** P0-D STRUCTURAL AUDIT, BEFORE CANDIDATE-GENERATOR SELECTION  
**Chi_bio status:** `NOT_ADMITTED`  
**Primary source contract:** Stage C1 frozen v2 lineage plus completed post-C1 v2.2 P0-Q audit

## 1. Purpose

Before proposing a system-level `Chi_bio` formula, identify which current GRI quantities are independent observables, deterministic compressions, shared-source summaries, null contrasts, or robustness transformations of the same underlying information.

This prevents a future candidate from obtaining apparent support by counting the same information multiple times.

## 2. Core dependency graph

```text
methylation beta matrix B_M
        |
        +--> centered X_M
        |       |
        |       +--> G_M = X_M X_M^T / p
        |       |       |
        |       |       +--> eigenspectrum q_1...q_29
        |       |       |       |
        |       |       |       +--> S_spec = 1 - H_norm
        |       |       |       +--> effective rank / participation ratio
        |       |       |       +--> modal concentration summaries
        |       |       |
        |       |       +--> eigenvectors / eigenspaces / probe contributions
        |       |
        |       +--> K_M = X_M X_M^T
        |               |
RNA X_R -------+--------+--> H2 / CKA(X_M, X_R)
        |                      |
        |                      +--> patient-permutation null -> Delta_CKA
        |                      +--> top-mode ablations -> S4 robustness family
        |                      +--> principal angles share the leading subspaces
        |
probe-gene map + Hallmarks
        |
        +--> methylation gene scores -> Hallmark methylation eigengenes
RNA Hallmark eigengenes -------------------------+
                                                  |
                                                  +--> A_same
                                                         |
                                                         +--> patient null -> H3a / Delta_A_patient
                                                         +--> label null   -> H3b / Delta_A_label

purity + leukocyte covariates
        |
        +--> shared residual projection R_Z
                 |
                 +--> adjusted X_M / X_R -> H2_adj
                 +--> adjusted Hallmark features -> H3a_adj / H3b_adj
```

## 3. Deterministic-compression relationships

### 3.1 S_spec is not independent of the methylation eigenspectrum

`S_spec = 1 - H_norm`, where `H_norm` is computed directly from normalized eigenvalues `q_k`.

Therefore:

```text
full eigenspectrum -> S_spec
```

is deterministic. `S_spec` cannot be counted as independent evidence in addition to the same spectrum. It is a compression of that modal information.

### 3.2 Other spectral rank/concentration summaries share the same carrier

Effective rank, participation ratio, `q1`, and related spectral summaries are different functionals of the same eigenspectrum. They may retain different aspects of concentration, but they are not independent measurements of separate biological processes merely because their formulas differ.

### 3.3 H2 and principal-angle outputs share the same cross-layer carrier

Global CKA uses the complete sample-space Gram matrices produced from the same `X_M` and `X_R`. Principal angles use leading methylation/RNA sample-mode subspaces from those same matrices.

They answer different structural questions:

- CKA: global geometry alignment;
- principal angles: orientation of selected leading subspaces.

But they share upstream information and must not be treated as statistically independent evidence by default.

### 3.4 S4 ablations are perturbations of H2, not new orthogonal coordinates

Top-1/top-3 ablation recomputes cross-layer geometry after removal of leading directions. The resulting quantities diagnose where H2 is carried. They are valuable modal-robustness information but remain descendants of the same cross-layer representation.

## 4. Shared-base contrasts

### 4.1 H3a and H3b share A_same

Both H3a and H3b begin from the same observed same-Hallmark coupling summary `A_same`.

They differ in what is destroyed:

- H3a patient null destroys cross-assay patient alignment while retaining Hallmark identity;
- H3b label null retains patients while destroying same-Hallmark identity.

Therefore H3a and H3b test different hypotheses, but their observed numerator/base statistic is shared. A candidate Chi_bio must not treat them as unrelated input channels.

### 4.2 Adjusted H2/H3 are robustness descendants

`H2_adj`, `H3a_adj`, and `H3b_adj` arise after the same purity/leukocyte residual projection is applied to the underlying data.

They are essential context-sensitivity checks, not separate independent observations that can be added to raw H2/H3 to inflate information count.

## 5. Current evidence classes for candidate construction

| Quantity/family | Structural class | Direct Chi_bio component status |
|---|---|---|
| raw methylation / RNA observables | source observables | eligible for generator consideration if model licenses |
| eigenspectrum/eigenspaces | modal carrier | eligible for generator consideration; not preselected |
| S_spec | deterministic modal compression | `NOT_PREDECLARED`; cannot be direct alias |
| H2 / Delta_CKA | global cross-layer contrast | `NOT_PREDECLARED`; cannot be direct alias |
| principal angles | leading-subspace relation | `NOT_PREDECLARED`; shared carrier with H2 |
| S4 ablations | perturbation/attribution diagnostic | diagnostic input candidate only if derivation licenses |
| A_same / H3a / H3b | Hallmark conglomerate contrasts | `NOT_PREDECLARED`; H3a/H3b share base statistic |
| H2_adj / H3_adj | context-projected robustness | robustness/context descriptors, not extra independent evidence |
| S3 complete-case / S7 TSS200 | representation robustness | robustness descriptors, not independent system coordinates |
| purity/leukocyte | embedded/context observables | may condition validity; must not be silently conflated with intrinsic state |
| RPPA/genomic context | additional context layers | candidate system inputs only after pathway/dependency audit |
| predictive outputs | downstream performance | prohibited for defining a candidate later validated on same performance outcome |

## 6. Consequence: the current results cannot simply be summed into Chi_bio

A construction such as

```text
Chi_bio = w1*S_spec + w2*H2 + w3*H3a + w4*principal_angle_score + ...
```

has no present scientific license. It would combine deterministic descendants and shared-source contrasts, and arbitrary fitted weights would risk manufacturing both apparent robustness and a unity crossing.

The current architecture is instead useful for identifying **what a native generator would need to explain simultaneously**.

## 7. Minimal candidate-generator obligations suggested by current evidence

Any serious generator should be able to represent or explain, within its claimed scope:

1. a scalar compression can remain similar while modal orientation changes;
2. leading modes carry substantial H2 geometry but do not exhaust it;
3. strong global geometry can coexist with weak same-label semantic specificity;
4. broad H2/H3a structure persists after limited composition projection;
5. local regulatory organization and embedded/context behavior can differ;
6. multiple internal organizations may produce similar aggregate/cancer-level behavior;
7. the model can refuse a coherent scalar when modal/conglomerate disagreement exceeds its validity regime.

These are structural constraints, not a selected Chi_bio formula.

## 8. What can be audited before full numeric packaging arrives

Already safe and complete at structural level:

- deterministic dependency map for S_spec;
- shared-carrier classification for CKA/principal angles/S4;
- shared-base classification for H3a/H3b;
- raw/adjusted lineage for composition projections;
- distinction between robustness transforms and independent observables;
- prohibition on downstream prediction outputs defining their own validation coordinate.

## 9. What still requires the machine-readable per-cancer bundle

To move from structural dependency to empirical identifiability we need per-cancer/resample or sufficiently rich per-cancer summaries for:

- covariance/correlation and mutual redundancy among candidate summaries;
- rank/condition diagnostics for any proposed low-dimensional representation;
- cancer-by-cancer scalar/modal disagreement;
- uncertainty propagation;
- leave-one-cancer-out stability;
- whether candidate ingredients provide measurable information beyond one another rather than algebraic repackaging.

No Stage C1 rerun is required. This is an export/integration need.

## 10. Current disposition

```text
CB1 semantic separation = materially advanced
CB4 input lineage/dependency = materially advanced
CB5 scalar-modal-conglomerate dependency = structurally advanced
CB2 generator derivation = OPEN
CB7 identifiability = OPEN pending candidate + numeric bundle
CB9 known-truth harness = designable but generator-specific implementation waits on CB2
```

**Scientific stop remains unchanged:** do not select a Chi_bio generator or inspect candidate unity placement until competing generator classes have been compared on derivation and identifiability grounds.