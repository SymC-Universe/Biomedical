# GRI Chi_bio science decision packet

**Date:** 2026-09-12  
**Status:** FIRST SCIENCE-CHANGING DECISION BOUNDARY  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4  
**Chi_bio status:** `NOT_ADMITTED`  
**No candidate formula frozen by this packet.**  
**No cancer-specific Chi_bio values inspected.**  
**No unity placement inspected.**

## 1. Why a user/scientific decision is now required

Safe work has exhausted the generator-neutral path far enough that the next operations would define the scientific object rather than merely audit, document, validate, package, or source-qualify it.

The unresolved choice is not simply "which formula looks best." It is:

> What biological state and operator is `Chi_bio` supposed to summarize?

That choice determines the state variables, local-versus-embedded scope, identifiability problem, uncertainty model, synthetic truth generator, external calibration source, and ultimately what unity could mean.

Under v0.7.4 this is science-changing and must be frozen before outcome-bearing Chi_bio values are computed.

## 2. What has already been fixed without selecting the science

The following are now locked as program guardrails, not as a Chi_bio definition:

- `Chi_bio` is system-level and distinct from lower-level `chi_dyn`;
- current state is `NOT_ADMITTED`;
- CV/2, `S_spec`, H2, H3a, H3b, CKA, or any arbitrary weighted combination cannot be directly renamed Chi_bio;
- scalar/modal/conglomerate relationships must remain traceable;
- Atlas placement cannot define or tune the coordinate;
- post-hoc rescaling cannot manufacture unity;
- explicit refusal is required when one coherent scalar does not exist;
- a candidate definition may be locked before it is biologically validated;
- internal TCGA qualification cannot license temporal recovery or a biological unity boundary;
- external untouched evidence is required before P1 admission;
- `Chi_bio = 1` receives biological boundary meaning only after CB14.

## 3. Candidate generator families that survived the first derivation screen

### Option G1: normalized regulatory interaction operator

Candidate mathematical object:

```text
M_GRI = derivative of a normalized regulatory update/production map
G1 = max Re eig(M_GRI)
```

Source-model property:

```text
local stable region: G1 < 1
boundary:           G1 = 1
local unstable:     G1 > 1
```

**Strengths**

- unity arises naturally in a published native gene-regulatory stability model;
- the scalar is traceable to an eigenmode/eigenspace;
- the object is a coupled regulatory operator, not a weighted summary of existing GRI scores;
- strongest current path to the requested natural unity boundary.

**Risks/open questions**

- the published operator is not automatically the GRI operator;
- current C1 covariance/CKA does not identify `M_GRI`;
- state vector and regulatory map must be chosen explicitly;
- local cell/module stability does not automatically equal bulk-tumor embedded stability;
- non-normal transient behavior may matter beyond the spectral abscissa.

### Option G2: discrete transition operator

Candidate mathematical object:

```text
x_(k+1) = T x_k + B u_k + noise
G2 = spectral radius rho(T)
```

Model property:

```text
autonomous stable region: G2 < 1
boundary:                  G2 = 1
unstable:                  G2 > 1
```

**Strengths**

- unity is mathematically natural;
- directly suited to ordered/perturbational data;
- modal carrier is explicit;
- treatment/environment can in principle enter as exogenous input rather than being hidden.

**Risks/open questions**

- depends on sampling interval;
- full high-dimensional `T` is not identifiable from the 11-week SCC25 series;
- dimensional reduction would define the scientific state and therefore must be frozen prospectively;
- continual treatment must be represented explicitly;
- spectral radius can miss non-normal transient amplification.

### Option G4: attractor attraction/diffusion balance

Candidate class:

```text
stabilizing attraction/restoration versus stochastic spreading/escape
```

**Strengths**

- conceptually closest to resilience/return/escape at system level;
- strong cancer-native attractor precedent;
- naturally connects Function and Limit maps.

**Current blocker**

No unique, source-independent unity normalization has yet been derived. This is therefore a scientifically important alternative family, but not currently as close to a `Chi_bio = 1` construction as G1/G2.

## 4. State-vector choices that would materially change the science

Whichever generator is selected, the state vector cannot be chosen mechanically after seeing Chi outcomes.

### S1 - transcriptomic regulatory state, substrate/context external

```text
x = RNA/module regulatory state
methylation, composition, genomic/protein context = substrate/parameters/exogenous context
```

**Advantage:** closer to native transcriptional regulatory dynamics and easier to interpret as a regulatory response state.

**Cost:** methylation does not enter the state directly, so the system-level relationship to the epigenetic substrate must be modeled through coupling/parameters rather than by concatenation.

### S2 - joint methylation + RNA state

```text
x = jointly represented methylation and RNA state
```

**Advantage:** directly captures the cross-layer architecture central to current GRI.

**Cost:** methylation and RNA operate on different biological timescales and measurement geometries; naive concatenation would be scientifically indefensible. A block/coupled model and scale convention would be required.

### S3 - frozen Hallmark/module reduced state

```text
x = predeclared module-level methylation/RNA state
```

**Advantage:** dimensionality becomes tractable, aligns with existing Hallmark architecture, and can retain interpretable coupling blocks.

**Cost:** module reduction discards within-module structure; H3b is already weak/support-sensitive; using Hallmark identity as the state basis may overcommit to semantic labels that current evidence does not support strongly.

### S4 - outcome-blind latent reduced state

```text
x = latent factors/subspaces selected without downstream outcome or unity information
```

**Advantage:** may preserve dominant modal geometry more faithfully than Hallmark labels and reduce dimensionality enough for operator identification.

**Cost:** latent-state construction itself becomes a major engine component requiring independent freeze, nulls, dimensionality selection, transport testing, and biological interpretation discipline.

## 5. Local-versus-embedded scope choices

The same numerical operator can mean different things depending on system boundary.

### L1 - local/intrinsic regulatory state

Target the intrinsic regulatory organization of the modeled cells/modules. Composition, microenvironment, treatment, and other external factors are modeled separately.

### L2 - effective embedded bulk-tumor state

Treat observed bulk molecular evolution as the realized embedded system, including composition and environment insofar as they are present in the measurements.

### L3 - paired local + embedded analysis

Estimate/qualify a local operator where data allow, separately characterize embedded realized behavior, and test whether a higher-level relationship is preserved. This is the most faithful v0.7.4 relational/hierarchical architecture but also the most demanding.

None is selected here.

## 6. Pre-outcome recommendation, not a freeze

The strongest current **review order** is:

```text
1. G1 normalized regulatory interaction family as the leading theoretical unity candidate
2. G2 transition-operator family as the leading operational/temporal comparator
3. G4 attraction/diffusion family retained as a qualitatively different stochastic system alternative
```

This order is based on derivation quality and identifiability structure, not on cancer placement or closeness to unity.

For the state-vector question, the safest review sequence is:

```text
S1 transcriptomic state + explicit substrate/context coupling
versus
S3 predeclared module/block state
versus
S4 outcome-blind latent state
```

S2 naive joint methylation+RNA concatenation should **not** be selected without a proper coupled-block derivation because it risks mixing timescales and measurement geometry merely to preserve all available data.

This recommendation is advisory only. No candidate ID, formula, state vector, or operator has been frozen.

## 7. What happens immediately after scientific selection

Once the generator/state/scope are selected explicitly, safe execution resumes automatically:

1. write the full MFR-14 candidate record;
2. freeze the generator equations and state semantics;
3. freeze normalization and unity basis;
4. extend the known-truth harness with generator-specific equations, grids, noise models, and failure cases;
5. run analytically checkable synthetic cases;
6. run known-bad/refusal cases;
7. audit identifiability and uncertainty;
8. package the completed C1/post-C1 numeric outputs read-only;
9. evaluate static-estimator feasibility without inspecting unity as an outcome selector;
10. freeze any estimator before mapping the 32 cancers;
11. use the qualified temporal sources for P0-Q/holdout calibration;
12. only then prepare the P1 external freeze.

## 8. What is needed from the current C1/post-C1 files

The repository has the scientific audit, manuscript tables, and source logs, but not the complete machine-readable Stage C1 and post-C1 returned result archives needed for per-cancer/resample identifiability calculations.

No C1 rerun is needed.

Required user-local artifacts for the next numeric packaging step are the already completed return bundles, especially:

```text
GRI_Stage_C1_Frozen_v2...\RETURN_TO_CHAT\Stage_C1_Result.zip
...
RETURN_TO_CHAT\Post_C1_Adversarial_Sensitivity_v2_2_Result.zip
```

These should be supplied/uploaded when the generator decision is made or earlier if convenient. The exporter is already specified to read them without recomputing frozen science.

## 9. Exact current stop

Mechanical/governance/source-discovery work can continue, but computing an outcome-bearing `Chi_bio` now would require one of the following unapproved scientific choices:

- choosing G1/G2/G4 or another generator as the candidate;
- choosing S1/S2/S3/S4 or another state representation;
- choosing L1/L2/L3 system scope;
- choosing a dimension-reduction rule that changes the operator;
- choosing how methylation couples into the generator;
- choosing what system-level quantity unity is supposed to separate.

Those choices define the hypothesis. They cannot be silently inferred from the existing cancer results.

**Decision required before CANDIDATE_LOCKED:** generator + state vector + local/embedded scope.  
**Current recommendation for review:** G1 first, G2 as operational comparator, G4 as stochastic alternative; avoid naive S2 concatenation.  
**Current scientific status:** `Chi_bio = NOT_ADMITTED`.