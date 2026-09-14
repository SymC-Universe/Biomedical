# GRI Chi_bio G2 known-truth comparator result audit

**Date:** 2026-09-12  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4  
**Research mode:** P0-D/P0-Q synthetic comparator qualification  
**Role:** approved G2 temporal comparator, not primary Chi_bio admission  
**Chi_bio status:** `NOT_ADMITTED`  
**Real cancer data used:** NO

## 1. Execution identity

GitHub Actions `GRI v2 tests` run **#526** completed successfully on branch `gri-v071-protocol-integration-20260910-chi-bio` at head `af4a58b147a93859bcec4583a77e103ea15eea33`.

- regression/unit suite: **200 passed**;
- pre-existing Stage B1 summary warnings: 7 NumPy divide warnings, no test failure;
- frozen G1 harness: PASS;
- frozen G2 comparator harness: PASS;
- G2 artifact: `gri-chi-bio-g2-known-truth`;
- G2 artifact ID: `10311367585`;
- G2 artifact ZIP SHA-256: `9f99a739c58994d34e7e4ee64be90178f5a2fa23017594c868e41faa744d3d3c`;
- G2 status: `PASS_G2_COMPARATOR_KNOWN_TRUTH_NO_REAL_DATA`;
- promotion consequence: `G2_COMPARATOR_SYNTHETIC_COMPONENT_SUPPORTED_ONLY; NO_CHI_BIO_PROMOTION`.

## 2. Unit-circle truth cases

The frozen discrete transition cases recovered the expected spectral-radius regimes exactly:

```text
rho(T) = 0.9 -> BELOW_UNITY
rho(T) = 1.0 -> AT_UNITY_WITHIN_TOLERANCE
rho(T) = 1.1 -> ABOVE_UNITY
```

This verifies the basic G2 unit-circle implementation. It does not establish that a real biological system is represented by one fixed transition operator.

## 3. Sampling-interval consistency

For the synthetic time-invariant semigroup cases,

```text
T_Delta = exp(J Delta)
rho(T_Delta) = exp(alpha(J) Delta)
```

reference-interval conversion recovered a common unit-interval value across `Delta = 0.5, 1.0, 2.0`.

### Stable truth

```text
alpha(J) = -0.2
raw radii = [0.9048374180, 0.8187307531, 0.6703200460]
reference values ~= [0.8187307531, 0.8187307531, 0.8187307531]
```

### Unstable truth

```text
alpha(J) = +0.1
raw radii = [1.0512710964, 1.1051709181, 1.2214027582]
reference values ~= [1.1051709181, 1.1051709181, 1.1051709181]
```

The deliberately inconsistent case with identical radii at unequal intervals was correctly **refused** as incompatible with a single semigroup rate.

Scientific consequence: sampling-interval normalization is available as a testable model consequence, not a free rescaling operation. Cross-timescale SCC25 analysis must first test the semigroup assumption; it cannot assume it merely to align daily and weekly values.

## 4. Shared-operator refusal case

The harness included one exactly consistent and one incompatible transition set.

Observed:

```text
consistent exact operator exists:   true
inconsistent exact operator exists: false
```

This supports the intended refusal branch: a future temporal series need not be forced into one constant `T` if the ordered transitions reject that model.

## 5. Non-normal transient case

For

```text
T = [[0.8, 4.0],
     [0.0, 0.8]]
```

observed:

```text
rho(T) = 0.8
largest singular value = 4.1540659229
```

The asymptotic scalar is below unity while one-step amplification is large in Euclidean norm. Therefore G2, like G1, requires modal/transient companion diagnostics. A scalar `rho(T)<1` cannot erase substantial non-normal amplification.

## 6. Frozen noise pilot

Truth transition:

```text
T = diag(0.5, 0.8, 0.98)
truth rho(T)=0.98
B=200 per sigma
seed=20260912
```

Results:

| sigma | median | 2.5% | 97.5% | truth covered | fraction >=1 | disposition |
|---:|---:|---:|---:|---|---:|---|
| 0.001 | 0.9800276 | 0.9781115 | 0.9817876 | yes | 0.000 | BELOW_UNITY_RESOLVED |
| 0.005 | 0.9801847 | 0.9708372 | 0.9889186 | yes | 0.000 | BELOW_UNITY_RESOLVED |
| 0.020 | 0.9809086 | 0.9444103 | 1.0158882 | yes | 0.155 | UNCERTAINTY_SPANS_BOUNDARY |
| 0.050 | 0.9853693 | 0.8778425 | 1.0696923 | yes | 0.370 | UNCERTAINTY_SPANS_BOUNDARY |

The refusal behavior is therefore operating as designed: uncertainty that crosses unity returns an unresolved disposition rather than a forced regime label.

This is synthetic operator noise only and is not a biological uncertainty model.

## 7. Comparison with the G1 synthetic qualification

Both candidate families now have executable known-truth/failure coverage, but the qualification questions are different:

### G1

- strongest direct theoretical unity construction in licensed subclasses;
- numerical coordinate requires restoration/decomposition information;
- naive heterogeneous directed normalization is falsified.

### G2

- exact unit-circle boundary for a defined discrete operator;
- no K/R decomposition required;
- interval dependence is explicit and testable;
- a single fixed operator can be refused;
- non-normal transients remain a material companion output.

This strengthens G2 as the empirical temporal comparator without silently promoting it to the global primary Chi_bio candidate.

## 8. Gate consequence

This run supports the **synthetic known-truth component** of the G2 comparator architecture. It does not satisfy empirical identifiability, state-reduction, external validation, or biological unity admission.

No candidate promotion follows from this run.

## 9. Current next gate

The remaining blocker for real temporal execution is not basic G2 mathematics. It is the empirical state representation and source-file gate:

1. acquire and hash exact source files;
2. freeze one outcome-blind transcriptomic state reduction and dimension rule;
3. freeze normalization/transport/refusal rules;
4. only then estimate real temporal operators;
5. preserve proliferation, ATAC, and single-cell endpoints from construction leakage.

Until then, `Chi_bio` remains `NOT_ADMITTED` and no SCC25 candidate value is computed.
