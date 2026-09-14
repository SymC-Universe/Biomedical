# GRI Chi_bio SCC25 state-reduction candidate survey

**Date:** 2026-09-12  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4  
**Research mode:** P0-D pre-outcome representation survey  
**Approved state semantics:** S1 transcriptomic regulatory state  
**Empirical reduction selected:** NO  
**Chi_bio outcomes inspected:** NO

## 1. Purpose

The approved S1 state is conceptually transcriptomic, but the SCC25 source has only 11 ordered states per arm. An unconstrained transcriptome-scale operator is impossible. A reduced state is therefore required for any G2 temporal operator and is likely required for any empirically identifiable G1 operator.

This survey compares reduction classes using only representation independence, algebraic identifiability, biological semantics, and transport burden. It does not inspect Chi_bio values, unity crossings, proliferation response, or resistant-clone separation.

## 2. Hard constraints before comparing methods

Any admitted reduction must:

- remain transcriptomic in semantic target;
- be frozen before real Chi_bio values;
- not use proliferation response, resistance labels, unity placement, Atlas placement, or clinical outcome to choose basis or dimension;
- fit within the formal rank ceiling of the chosen transition architecture;
- preserve an explicit transport rule;
- carry a refusal rule when projection is unstable or source-specific;
- keep methylation external as substrate/context under the approved S1 plan;
- preserve local-versus-embedded distinction.

The executable enforcement layer is `src/chi_bio_state_reduction_contract.py`.

## 3. Candidate R1: control-only unsupervised basis

Construction class:

```text
fit RNA basis using PBS control states only
freeze basis + dimension rule
project cetuximab states without refitting
```

A centered 11-state PBS trajectory has at most 10 nonzero sample-space directions before additional transition-model constraints.

### Strengths

- treatment trajectory does not define the basis;
- proliferation phenotype remains untouched;
- treated states can test whether the control-defined coordinate system transports under perturbation;
- mechanically simple and reproducible;
- natural first G2 feasibility representation.

### Weaknesses

- only 11 control states, so estimated directions can be unstable;
- a control-only basis can miss treatment-emergent regulatory dimensions;
- unsupervised variance is not equivalent to regulatory mechanism;
- exact dimension rule still needs a scientific freeze.

### Best role

Leading **operational G2 feasibility** candidate, not automatically a mechanistic G1 state.

## 4. Candidate R2: predeclared biological module basis

Construction class:

```text
externally defined gene modules/regulons
-> fixed per-state module scores
```

### Strengths

- biological semantics are explicit;
- no SCC25 outcome is needed to define the basis;
- may make reduced restoration timescales measurable at module level;
- compatible with G1 if the modules correspond to a defensible regulatory map.

### Weaknesses

- current Hallmark-style semantic specificity is not uniformly strong in GRI; H3b is the weak/support-sensitive branch;
- a 50-module Hallmark state still exceeds the practical SCC25 transition dimension;
- choosing a small subset from the cetuximab literature could introduce question-specific selection bias;
- generic pathway scores are not automatically state variables of a dynamical generator.

### Best role

Strong **mechanistic candidate class** if an independently frozen small module/regulon set can be justified without treatment-outcome tuning.

## 5. Candidate R3: external fixed transcriptomic basis

Construction class:

```text
fit/freeze basis in an external reference such as existing TCGA or another independent transcriptomic source
-> transport basis unchanged into SCC25
```

### Strengths

- maximal protection against SCC25 trajectory leakage;
- clean transport test;
- basis can be frozen before SCC25 values are opened.

### Weaknesses

- bulk-tumor versus cell-line representation mismatch can dominate;
- external basis may encode composition/microenvironment absent from SCC25;
- a transported statistical basis is not automatically a regulatory state;
- failure may reflect transport mismatch rather than failure of the underlying generator.

### Best role

Useful **transport/representation stress test**, not preferred as the sole primary SCC25 state.

## 6. Candidate R4: externally grounded mechanistic TF/regulon state

Construction class:

```text
fixed transcription-factor/regulon definitions
-> infer low-dimensional regulatory activities from RNA
```

### Strengths

- closest semantic match to a regulatory interaction operator;
- directionality/mechanistic prior can be explicit rather than inferred from covariance alone;
- potentially compatible with G1's requirement for a regulatory map.

### Weaknesses

- many available regulons would still be too high-dimensional;
- selecting a small panel creates a new scientific choice;
- inferred activity is model-dependent and not directly measured;
- a TF-activity state does not solve the independent restoration/turnover problem by itself.

### Best role

Leading **G1-oriented representation family** for later review if a small, externally frozen panel and restoration measurement route can be justified.

## 7. Candidate R5: both-arm unsupervised basis

Construction class:

```text
fit PCA/SVD/latent basis to all 22 weekly RNA states
```

### Strengths

- uses the full measured transcriptomic geometry;
- can represent treatment-emergent directions;
- maximizes descriptive variance capture at fixed dimension.

### Weaknesses

- treatment trajectory helps define the coordinate system later used to evaluate that same trajectory;
- weakens independence for a first temporal falsification test;
- basis can rotate toward treatment separation even without using explicit labels;
- still lacks mechanistic interpretation.

### Best role

Exploratory/sensitivity representation after a cleaner primary freeze, not the preferred first temporal validation basis.

## 8. Candidate R6: published CoGAPS/time-course basis

The original study's CoGAPS factors and feature filters were optimized for the same longitudinal dataset.

### Strengths

- established descriptive biology for this source;
- likely captures major resistance-associated patterns.

### Disqualifying issue for primary Chi_bio validation

The basis/filtering is informed by the time-course data structure used for the new test. Reusing it as if prospectively independent would blur construction and validation.

### Best role

Native comparator/descriptive reference only unless a separate leakage-controlled role is frozen.

## 9. Current ranking by role, not scientific selection

### For G2 empirical feasibility

```text
1. R1 control-only unsupervised basis
2. R3 external fixed basis as transport stress test
3. R5 both-arm unsupervised basis as sensitivity/exploratory representation
```

### For G1 mechanistic development

```text
1. R4 externally grounded mechanistic TF/regulon state
2. R2 predeclared small biological-module state
3. R1 control-only basis as a statistical comparator, not mechanistic truth
```

These rankings are based on independence and identifiability structure. They do not select a final empirical state.

## 10. Important divergence between G1 and G2

The reduction survey exposes a useful architectural split:

- the representation easiest to identify temporally for **G2** is not necessarily the representation with the strongest regulatory semantics for **G1**;
- forcing one basis to serve both candidates could create artificial agreement;
- the protocol therefore favors candidate-specific representation qualification followed by an explicit cross-representation transport test.

This is a feature, not a bookkeeping inconvenience. If G1 and G2 require different valid representations, their agreement cannot be assumed and their disagreement becomes informative.

## 11. Exact next science-changing choice

Safe work can specify and test contracts, rank ceilings, source identities, and known-truth systems. The next empirical move requires freezing at least:

```text
primary reduction class
exact dimension rule
data role used to fit the basis
transport/refusal rule
```

For the first SCC25 G2 feasibility test, **R1 control-only unsupervised basis is the leading review candidate** because it preserves the treated trajectory and proliferation phenotype from representation fitting.

For the G1 route, **R4/R2 remain stronger semantically but currently lack a qualified restoration strategy**.

No reduction is selected by this document.
