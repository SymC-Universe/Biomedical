# GRI Chi_bio S1 empirical state-reduction preselection audit

**Date:** 2026-09-13  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4  
**Candidate family:** G1-S1-L3, user-approved and frozen at family level  
**Chi_bio status:** `NOT_ADMITTED`  
**Purpose:** narrow the empirical transcriptomic representation without inspecting cancer-specific Chi_bio values, Atlas placement, or closeness to unity.

## 1. Why this audit is required

The G1 family is now scientifically selected, but the empirical state vector is still underdetermined. A raw gene vector, a predeclared module state, a network-constrained state, and an outcome-blind latent state define different operators and therefore different scientific objects. Choosing among them after seeing cancer-specific G1 placement would create leakage.

This audit compares the admissible routes using only identifiability, interpretability, transport, dimensionality, substrate-coupling logic, and failure behavior.

## 2. Frozen evaluation criteria

A state-reduction route must be judged on the following pre-outcome properties:

1. **operator identifiability:** can the chosen state support a stable estimate of a regulatory operator with the available sample/time structure?
2. **biological semantics:** does each coordinate have an interpretable transcriptomic/regulatory meaning?
3. **dimension control:** is dimension low enough relative to sample/timepoint count to avoid unconstrained operator fitting?
4. **transport:** can the same representation be applied without cancer-specific semantic redefinition?
5. **substrate compatibility:** can methylation/context modify the regulatory map without being silently folded into the state?
6. **local/embedded separation:** can intrinsic regulation and embedded realized behavior remain distinguishable?
7. **modal fidelity:** can the reduction preserve or explicitly quantify losses in dominant eigenspaces and non-normal structure?
8. **outcome independence:** can all choices be frozen without using cancer prognosis, favored Atlas region, or distance from unity?
9. **refusal capability:** can the route explicitly return non-identifiability or representation dependence rather than force a number?
10. **computational economy:** can the route be piloted with small, analytically or numerically checkable cases before broad mapping?

## 3. Candidate routes

### R1. Raw high-dimensional transcriptomic gene state

**Definition:** `x` is the full eligible gene-expression vector.

**Advantages**
- minimal semantic compression;
- no module or latent-basis choice is imposed initially;
- potentially preserves fine modal structure.

**Problems**
- operator dimension is enormous relative to available temporal data and often relative even to cross-sectional sample size;
- any empirical Jacobian/transition estimator would require strong regularization whose structure would dominate the scientific object;
- local gene-gene dynamics are not identifiable from static covariance alone;
- transport across cancers with differing expression support would require additional rules.

**Pre-outcome disposition:** `RETAIN_AS_REFERENCE_ONLY_NOT_PRIMARY_ESTIMATOR`.

### R2. Predeclared biologically interpretable regulatory modules

**Definition:** `x` is a fixed module-level transcriptomic state using an externally or prospectively declared module basis.

Possible basis families include transcription-factor regulons, curated regulatory programs, or another fixed biological module system. Existing Hallmark labels may be used only if separately justified for regulatory-state semantics; current H3b weakness means Hallmark same-label specificity cannot itself justify the basis.

**Advantages**
- strong dimensional reduction;
- biological interpretability;
- clean substrate/context coupling at module level;
- straightforward transport if membership is frozen globally;
- compatible with scalar/modal/conglomerate traceability.

**Risks**
- module definitions import prior biological assumptions;
- coarse modules can merge distinct regulatory modes;
- overlapping modules can generate rank/identifiability problems;
- any cancer-specific pruning can create leakage.

**Pre-outcome disposition:** `LEADING_EMPIRICAL_ROUTE_FOR_REVIEW`.

### R3. Outcome-blind latent transcriptomic state

**Definition:** `x` is a latent state learned without downstream outcome, Atlas, unity, treatment-response, or cancer-rank information.

Admissible examples in principle include frozen PCA/SVD subspaces or other unsupervised linear reductions with prospectively fixed dimension rules.

**Advantages**
- preserves dominant variance/subspace geometry efficiently;
- dimension can be tuned by an outcome-blind reconstruction/stability rule;
- may preserve empirically dominant modes better than semantic modules.

**Risks**
- latent axes can rotate across cohorts/cancers;
- the operator becomes basis-dependent unless transport/alignment is frozen;
- dominant variance is not guaranteed to equal regulatory relevance;
- dimension selection becomes a major scientific degree of freedom.

**Pre-outcome disposition:** `LEADING_NONSEMANTIC_COMPARATOR`.

### R4. Network-constrained transcriptomic state/operator

**Definition:** retain a gene or module state but constrain permitted regulatory edges using a predeclared external network/regulon graph.

**Advantages**
- reduces effective parameter count without requiring severe state compression;
- ties operator sparsity to independent biological structure;
- natural route for testing whether substrate changes regulatory coefficients on a fixed graph.

**Risks**
- network prior may be cell-type or context mismatched;
- missing true edges and false prior edges can bias stability spectra;
- external network choice becomes part of the hypothesis and requires provenance/transport audit.

**Pre-outcome disposition:** `HIGH_PRIORITY_STRUCTURAL_CONSTRAINT`, not yet selected as the state representation itself.

## 4. Pairing routes rather than forcing one winner prematurely

The strongest prospective comparison is not R2 versus R3 as mutually exclusive dogma. A disciplined qualification can use:

- **R2 as the primary interpretable state candidate**;
- **R3 as an outcome-blind representation-sensitivity comparator**;
- **R4 as an optional structural constraint layer** if independently justified;
- **R1 as a reference proving why unconstrained full-state operator recovery is not identifiable.**

This arrangement tests whether the candidate scalar/modal conclusions survive a meaningful change of representation without letting the representation be selected by favorable cancer placement.

## 5. Recommended next freeze candidate, not yet executed

The current pre-outcome recommendation is:

```text
Primary empirical state: R2 fixed regulatory-module transcriptomic state
Representation sensitivity: R3 frozen outcome-blind linear latent state
Structural option: R4 independently sourced network constraint
Reference non-identifiable route: R1 raw full-gene operator
```

However, the exact R2 module basis is still scientifically material and is **not frozen by this audit**. Selecting Hallmarks, TF regulons, or another module system changes the operator semantics.

## 6. Required tests before any real G1 mapping

Whichever R2 basis is selected must pass, prospectively:

- fixed membership/provenance audit;
- rank and effective-dimension audit;
- resampling stability of state coordinates;
- operator-estimation identifiability pilot on synthetic known-truth data at matched dimension/sample structure;
- representation perturbation against R3;
- modal/subspace stability, not scalar-only agreement;
- explicit refusal when the fitted operator is unstable to reasonable resampling or regularization;
- no parameter selection by closeness of G1 to unity.

## 7. Stop boundary

Safe work can specify the comparison and qualification machinery, but selecting the exact R2 biological module basis would define the empirical state and therefore requires a separate scientific freeze unless an already frozen independent basis is adopted under a documented transfer argument.

**Current recommendation:** proceed to source/provenance comparison of candidate fixed regulatory module bases and build the identifiability gate before choosing one.