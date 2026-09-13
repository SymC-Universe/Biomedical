# GRI Chi_bio G1 candidate derivation: normalized regulatory interaction eigenvalue

**Date:** 2026-09-12  
**Status:** P0-D CANDIDATE DERIVATION, NOT FROZEN  
**Chi_bio status:** `NOT_ADMITTED`  
**Cancer-specific candidate values inspected:** NO  
**Unity placement inspected:** NO

## 1. Native source model

Guo & Amir, *Nature Communications* 12, 130 (2021), DOI `10.1038/s41467-020-20472-x`, derive a reduced protein-concentration regulatory model under a fast-mRNA approximation:

```text
dc/dt = beta0 [phi(c) - c]
```

where `c` is the vector of protein concentrations, `phi(c)` is the regulatory production/allocation map, and `beta0 > 0` is a kinetic scale.

At a steady state `c_ss = phi(c_ss)`, define the dimensionless interaction matrix

```text
M_ij = partial phi_i / partial c_j | c_ss
```

The Jacobian of the reduced dynamics is

```text
A = beta0 (M - I).
```

If `lambda_M` is an eigenvalue of `M`, the corresponding Jacobian eigenvalue is

```text
lambda_A = beta0 (lambda_M - 1).
```

Because `beta0 > 0`, local asymptotic stability requires

```text
max Re(lambda_M) < 1.
```

The natural boundary is therefore

```text
max Re(lambda_M) = 1.
```

The number 1 is produced by the identity term in the native regulatory dynamics. It is not a post-result rescaling.

## 2. Candidate system coordinate

A mathematically direct candidate scalar from this model class is

```text
G1 = alpha(M) = max_k Re(lambda_k(M))
```

where `alpha` is the spectral abscissa.

If the GRI System Model can justify an `M` with the same semantic role, then the model-native interpretation would be:

```text
G1 < 1   local steady state stable within the model
G1 = 1   local linear stability boundary
G1 > 1   local steady state unstable within the model
```

This derivation is sufficient to make G1 a serious **candidate** for a system-level Chi-like coordinate. It is not sufficient to name it `Chi_bio` for GRI.

## 3. Why G1 is attractive for the GRI architecture

### Scalar

`alpha(M)` is one dimensionless scalar with a natural unity boundary.

### Modal/vector

The eigenvalue achieving the spectral abscissa has an associated right/left mode or invariant subspace. Therefore the scalar is traceable to a carrier rather than existing as an arbitrary summary.

### Conglomerate/system

The matrix `M` represents coupled regulatory interactions. The scalar emerges from the conglomerate interaction operator rather than averaging separate scalar metrics.

This is structurally compatible with the program-level rule that scalar, modal, and conglomerate views must remain linked but separable.

## 4. Critical semantic obstacle

The current C1 methylation/RNA architecture does **not** directly estimate the Guo-Amir `M`.

Specifically:

- a covariance or Gram matrix is not `M`;
- H2/CKA is not `M`;
- a principal-angle spectrum is not `M`;
- Hallmark coupling is not `M`;
- `S_spec` is not `M`;
- methylation is not automatically a protein-production regulator in the specific source model;
- bulk tumor composition and microenvironment are not represented in the source model merely because they are measured in GRI.

Therefore no current TCGA quantity may be substituted for `M` by analogy.

## 5. GRI-specific derivation obligations

Before G1 could be frozen as `Chi_bio`, the GRI System Model would have to specify:

1. **state vector `x`:** what biological variables form the local state;
2. **regulatory map `Phi(x, e)`:** what maps the state back onto its production/update state, including any environmental/context variable `e`;
3. **normalizing/self-restoring term:** why the local generator contains an identity-equivalent term that makes unity natural;
4. **operator `M_GRI = dPhi/dx`:** how it is measured or inferred independently;
5. **embedding:** whether `M_GRI` is intrinsic/local or already includes composition/microenvironment/treatment feedback;
6. **modal carrier:** how right/left modes or invariant subspaces are retained;
7. **validity regime:** locality, steady-state approximation, timescale separation, sampling interval, and nonlinearity limits;
8. **uncertainty:** uncertainty on `M_GRI`, the leading spectral quantity, and near-degenerate modes;
9. **non-normality:** whether spectral abscissa is sufficient for the biological question or transient amplification requires additional system descriptors;
10. **hierarchical closure:** why a cell/module-level operator can be interpreted as a tumor-level system coordinate if that step is claimed.

## 6. Identifiability requirements

### Static TCGA alone

`M_GRI` is not identifiable from current static C1 covariance/geometry without strong additional assumptions. Many dynamical operators can generate similar covariance structure.

Therefore static TCGA cannot directly provide G1 truth.

### Perturbational route

Systematic perturbation-response methods can estimate local response matrices related to Jacobian structure using multiple controlled perturbations around a stable state. This is a better route for identifying the operator than relabeling covariance.

### Longitudinal route

Dense time-course data can constrain a reduced operator, especially with matched controls/exogenous inputs, but a single trajectory with far fewer timepoints than state dimensions is underdetermined unless dimension reduction/regularization is prospectively justified.

## 7. Relationship to DNB/covariance early-warning theory

Dynamic-network-biomarker theory shows that covariance/fluctuation structure changes as a dominant Jacobian eigenvalue approaches its critical value. This creates a possible **estimator bridge**:

```text
operator-derived G1 truth in dynamic systems
        -> frozen estimator from static observables
        -> held-out dynamic validation
        -> TCGA transport
```

It does not support:

```text
static covariance = M_GRI.
```

## 8. Candidate falsifiers before freeze

G1 should be rejected or narrowed if any of the following holds:

- no biologically coherent GRI regulatory map produces the required normalized interaction operator;
- unity enters only through arbitrary rescaling;
- operator inference is non-identifiable at available resolution;
- the leading spectral scalar is unstable to plausible representation choices;
- distinct modal/conglomerate architectures with materially different response behavior collapse to the same G1 without an adequate refusal rule;
- non-normal/transient behavior dominates the target biological outcome while G1 remains unchanged;
- external perturbational evidence fails after a frozen implementation;
- apparent performance is no better than simpler covariance/DNB statistics under equal information.

## 9. Current decision status

```text
CB2 native generator/derivation: CANDIDATE-SPECIFICALLY STRONG
CB3 natural normalization: CANDIDATE-SPECIFICALLY STRONG
CB5 modal/conglomerate traceability: STRUCTURALLY PLAUSIBLE
CB7 identifiability: OPEN
CB8 uncertainty: OPEN
CB9 known-truth recovery: NOT YET IMPLEMENTED
CB10 internal P0-Q: NOT STARTED
CB14 unity basis: MATHEMATICALLY NATURAL IN SOURCE MODEL, NOT BIOLOGICALLY ADMITTED FOR GRI
```

**G1 is not frozen.** The next science-changing choice would be selecting the GRI state vector/regulatory map and thereby defining what `M_GRI` actually is.