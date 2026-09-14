# GRI Chi_bio B3 regulon topology-spectrum post-result audit

**Date:** 2026-09-13 / workflow completion 2026-09-14 UTC  
**Protocol authority:** `General_Cross_Project_Research_Protocol_v0.7.5_FINAL.md`  
**Workflow run:** `34798559079`  
**Execution head:** `6c02d21246ca497cb7ba8f2bb7057af5823126a8`  
**Artifact ID:** `10330477936`  
**Artifact SHA-256:** `ec28faedd4a1cfee32a288eebd5dd282bcd810ceab0c41e932d383bead27e30f`  
**Expression opened:** `false`  
**TF activity scored:** `false`  
**Chi_bio:** `NOT_ADMITTED`

## 1. Purpose

After the prospectively frozen ULM -> control-PCA B3 construction failed its unseen-seed matched-network holdout, a materially different outcome-free possibility remained: perhaps the **external regulon graph itself** contains a compact natural regulator-mode structure that could define coordinates before expression is seen.

This audit tests that possibility descriptively using the exact frozen eligible CollecTRI and DoRothEA A/B/C geometries. It does not define a post-hoc admission threshold and cannot itself promote a graph-derived B3 state.

## 2. CollecTRI primary topology

Eligible regulator count:

```text
766
```

### Signed regulator-target geometry

```text
numerical rank:                         766
entropy effective rank:                538.18
participation ratio:                   354.61
spectral mass, first 1 mode:             2.24%
spectral mass, first 2 modes:            3.43%
spectral mass, first 5 modes:            5.72%
spectral mass, first 10 modes:           8.86%
spectral mass, first 20 modes:          13.83%
spectral mass, first 50 modes:          25.10%
spectral mass, first 100 modes:         38.64%
```

The largest eigengap among k=1..20 occurs after mode 1:

```text
lambda_1 = 17.1237
lambda_2 =  9.1858
ratio = 1.864
```

However that first mode accounts for only `2.24%` of total spectral mass. The apparent first-mode gap therefore does **not** imply a compact one-dimensional regulon representation.

### Unsigned target-support geometry

```text
numerical rank:                         766
entropy effective rank:                504.22
participation ratio:                   249.78
spectral mass, first 1 mode:             4.17%
spectral mass, first 2 modes:            5.22%
spectral mass, first 5 modes:            7.60%
spectral mass, first 10 modes:          10.77%
spectral mass, first 20 modes:          15.86%
spectral mass, first 50 modes:          27.10%
spectral mass, first 100 modes:         40.42%
```

Again the largest early eigengap is after the first mode, but even the first five unsigned modes retain only `7.60%` of total network spectral mass.

## 3. DoRothEA A/B/C sensitivity topology

Eligible regulator count:

```text
271
```

### Signed regulator-target geometry

```text
numerical rank:                         271
entropy effective rank:                242.18
participation ratio:                   209.87
spectral mass, first 1 mode:             2.09%
spectral mass, first 2 modes:            3.69%
spectral mass, first 5 modes:            6.49%
spectral mass, first 10 modes:          10.30%
spectral mass, first 20 modes:          16.99%
spectral mass, first 50 modes:          33.03%
spectral mass, first 100 modes:         54.23%
```

The largest early eigengap is after mode 2:

```text
lambda_2 = 4.3474
lambda_3 = 2.6489
ratio = 1.641
```

Yet the first two modes together contain only `3.69%` of total spectral mass.

### Unsigned target-support geometry

```text
numerical rank:                         271
entropy effective rank:                238.92
participation ratio:                   199.59
spectral mass, first 1 mode:             2.55%
spectral mass, first 2 modes:            4.35%
spectral mass, first 5 modes:            7.20%
spectral mass, first 10 modes:          11.00%
spectral mass, first 20 modes:          17.66%
spectral mass, first 50 modes:          33.64%
spectral mass, first 100 modes:         54.75%
```

The largest early eigengap again occurs after mode 2, but those first two modes contain only `4.35%` of total mass.

## 4. Cross-resource interpretation

Both independent regulon resources give the same broad qualitative answer:

1. the eligible regulator geometry is full numerical rank;
2. entropy effective rank remains a large fraction of the available regulator count;
3. the first 2-5 modes capture only a few percent of total network spectral mass;
4. substantial spectral mass remains distributed over tens to hundreds of modes;
5. an early eigengap exists, but it does not coincide with strong low-rank concentration.

Therefore the external networks do **not** supply a compelling compact 2-5 dimensional coordinate system merely by taking their leading graph/similarity modes.

This result is consistent with, but logically independent from, the earlier ULM -> control-PCA holdout refusal. The previous failure cannot be explained away by saying that an obvious low-dimensional regulon topology was ignored.

## 5. What is closed

The following shortcut is now **not admitted**:

```text
external regulon graph
-> take the first 1-5 graph/spectral modes because an eigengap is visible
-> treat those modes as the B3 biological state
```

The eigengaps are real descriptive features, but the associated low-order modes account for too little of the total network geometry to justify that compression by topology alone.

No post-hoc threshold is introduced here, so this is not a preregistered pass/fail hypothesis test. It is a negative pre-outcome design result: the topology audit does not provide the independent scientific justification required to open such a candidate on real SCC25/TCGA expression.

## 6. What remains possible

The broader B3 concept is not falsified. Remaining materially distinct candidates would require new lineage and their own known-truth program, for example:

- an externally fixed small regulator/module panel justified by independent biology rather than current outcomes;
- a higher-dimensional regularized operator with a prospectively frozen regularization/tuning rule;
- another externally defined functional/module basis with direct biological semantics.

None is authorized by this audit.

## 7. Relation to normalized G1

Even a future B3 state success would not identify normalized G1 by itself. The independent restoration decomposition remains unresolved:

```text
J = K - R
```

B3 can address state representation and effective dynamics, but `K` versus `R` requires separate restoration information.

## 8. Current disposition

```text
B3 external-network provenance:             PASS
B3 namespace / identifier mapping:          PASS
B3 network-dependence audit:                PASS
B3 ULM runtime:                              PASS
ULM -> control-PCA matched-network holdout:  REFUSE
compact graph-mode shortcut:                 NOT ADMITTED
real SCC25/TCGA B3 activity opening:         FORBIDDEN
normalized G1:                               CLOSED
Chi_bio:                                     NOT_ADMITTED
```
