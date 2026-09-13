# GRI Chi_bio G1 known-truth result audit

**Date:** 2026-09-12  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4  
**Candidate family:** `G1_S1_L3_v0_1`  
**Research mode:** pre-real-data P0-D/P0-Q candidate qualification  
**Chi_bio promotion state:** `NOT_ADMITTED`  
**Cancer-specific Chi_bio values used:** NO  
**Atlas/unity placement used to select tests:** NO

## 1. Execution identity

GitHub Actions `GRI v2 tests` run **#496** completed successfully on branch `gri-v071-protocol-integration-20260910-chi-bio` at head `db5ff615a1daa7721da7de0dcb77e6646726f704`.

- unit/regression suite: **163 passed**;
- frozen G1 known-truth harness step: **PASS**;
- uploaded artifact: `gri-chi-bio-g1-known-truth`;
- artifact ID: `10311124881`;
- artifact ZIP SHA-256: `f6bddce117c6b20154a2f36c4927209b4a1bc7f9c5940bc5fb038297193af6b1`;
- harness status: `PASS_EXACT_AND_FAILURE_CASES_NO_REAL_DATA`;
- harness promotion consequence: `CB9_SYNTHETIC_MATH_COMPONENT_SUPPORTED_ONLY; CANDIDATE_LOCK_NOT_EARNED`.

The only new-test warning in this run was a Python invalid-escape warning in a regex literal. It was mechanical and subsequently repaired without changing scientific content.

## 2. G1A common-restoration exact cases

All frozen G1A cases passed for `beta = 0.25, 1.0, 4.0`.

For every tested matrix,

```text
J = beta(M-I)
```

satisfied

```text
alpha(J) = beta [alpha(M)-1]
```

with zero observed relation error at reported floating precision.

The frozen stable, boundary, and unstable matrices were classified correctly relative to unity for all three beta values.

This verifies the implementation and the exact unity relation for the restricted common-restoration model class. It does not establish that an empirical transcriptomic GRI state has common restoration.

## 3. G1B symmetric generalized exact cases

All three frozen cases passed for heterogeneous positive restoration `R = diag(2.0, 0.5)`:

```text
stable:   value = 0.9, alpha(J) = -0.1
boundary: value = 1.0, alpha(J) =  0.0
unstable: value = 1.1, alpha(J) = +0.2
```

The exact coordinate is

```text
lambda_max(R^-1/2 K R^-1/2)
```

under the frozen requirements that `K` is symmetric and `R` is symmetric positive definite.

This is a valid unity route for that restricted gradient-like/symmetric class. It is not licensed for a general directed regulatory operator.

## 4. Directed heterogeneous counterexamples

Both frozen counterexamples passed and materially narrow the candidate interpretation.

### False-safe example

```text
R = diag(2.0, 0.5)
K = [[3, -4],
     [1,  0]]
```

Observed:

```text
alpha(R^-1 K) = 0.75   -> naive rule would label below unity
alpha(K-R)    = 0.25   -> true local Jacobian is unstable
```

### False-unsafe example

```text
R = diag(2.0, 0.5)
K = [[-4, -4],
     [ 4,  3]]
```

Observed:

```text
alpha(R^-1 K) ~= 2.00000004  -> naive rule would label above unity
alpha(K-R)    ~= -0.31385934 -> true local Jacobian is stable
```

Therefore the project now has executable proof that the simple normalization

```text
M = R^-1 K
Chi_candidate = alpha(M)
```

cannot be generalized to heterogeneous directed transcriptomic dynamics merely because the Guo-Amir source model has an `alpha(M)=1` boundary.

This is a useful falsification result, not a setback to be hidden. It prevents an attractive but invalid transfer.

## 5. Modal degeneracy

Both exact and near-degenerate leading-mode cases triggered

```text
DOMINANT_SUBSPACE_NEAR_DEGENERATE
```

as required.

The implementation therefore does not pretend that one uniquely identified eigenvector exists when the leading real-part gap is below the frozen tolerance.

## 6. Non-normal transient case

For the frozen non-normal matrix

```text
M = [[0.8, 4.0],
     [0.0, 0.8]]
```

with `beta=1`:

```text
alpha(J) = -0.2
continuous-time numerical abscissa = +1.8
```

Thus the scalar correctly remains asymptotically stable while a companion warning exposes an instantaneous Euclidean growth direction. This validates the design rule that scalar stability must not erase modal/transient structure.

## 7. Frozen uncertainty pilot

Truth matrix:

```text
M = diag(0.4, 0.8, 0.98)
truth G1A = 0.98
B = 200 per sigma
seed = 20260912
```

Results:

| sigma | median | 2.5% | 97.5% | truth covered | fraction >=1 | unity disposition |
|---:|---:|---:|---:|---|---:|---|
| 0.001 | 0.9800276 | 0.9781115 | 0.9817877 | yes | 0.000 | BELOW_UNITY_RESOLVED |
| 0.005 | 0.9801832 | 0.9708368 | 0.9889216 | yes | 0.000 | BELOW_UNITY_RESOLVED |
| 0.020 | 0.9809666 | 0.9444093 | 1.0158951 | yes | 0.155 | UNCERTAINTY_SPANS_BOUNDARY |
| 0.050 | 0.9853719 | 0.8803751 | 1.0703520 | yes | 0.370 | UNCERTAINTY_SPANS_BOUNDARY |

The refusal logic behaves in the intended direction: as operator uncertainty grows enough that the frozen interval crosses unity, the result becomes unresolved rather than being forced into a stable/unstable label.

This is only a synthetic perturbation pilot. It does not constitute calibrated biological measurement uncertainty.

## 8. Gate disposition after the run

```text
CB1 semantic family/state/scope:         PASS
CB2 native generator derivation:         PASS for source family
CB3 natural normalization:               PASS for G1A/G1B; OPEN for general directed S1
CB4 independently meaningful inputs:     PARTIAL / empirical K,R measurement mapping open
CB5 scalar-modal-conglomerate relation:  PASS structurally
CB6 outcome/Atlas independence:          PASS
CB7 competing-generator identifiability: OPEN
CB8 uncertainty/tolerance:               PARTIAL; synthetic refusal behavior works, biological uncertainty open
CB9 known-truth/null recovery:           PARTIAL PASS; synthetic mathematical component supported
```

`CANDIDATE_LOCKED` is therefore **not** earned.

## 9. Scientific consequence

The approved G1/S1/L3 program remains active, but it is now more narrowly and correctly stated:

1. **G1A** is exact if a common restoring timescale is independently justified.
2. **G1B** is exact for a symmetric/generalized gradient-like regulatory class.
3. A generic directed transcriptomic network with heterogeneous turnover does **not** inherit an `alpha(R^-1 K)=1` boundary.
4. If the real S1 state does not satisfy an exact G1 subclass, the project must either derive a different native normalization, narrow G1 to an appropriate subsystem, or elevate G2 for separate review.
5. No rescaling to preserve the desired number 1 is allowed.

## 10. Next exact work

Safe next work without cancer-specific Chi outcomes:

- audit whether biologically plausible transcriptomic representations can satisfy G1A or G1B without contrivance;
- compare G1 identifiability against G2 and G4 under the available temporal/perturbational source architecture;
- finish SCC25 source manifests and representation firewalls;
- extend uncertainty/refusal design to empirically estimated operators;
- ingest completed C1/post-C1 return archives read-only when available;
- keep all cancer-specific Chi_bio computation blocked until an empirical estimator is independently frozen.
