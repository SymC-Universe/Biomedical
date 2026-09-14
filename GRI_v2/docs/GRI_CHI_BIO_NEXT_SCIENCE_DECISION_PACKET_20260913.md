# GRI Chi_bio next science-decision packet

**Date:** 2026-09-13  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4  
**Approved family:** G1-S1-L3  
**Approved architecture bundle:** A3 + B3 + C3  
**Temporal comparator:** G2  
**Stochastic alternative:** G4  
**Chi_bio:** `NOT_ADMITTED`

## 1. What is now frozen by explicit approval

The following scientific architecture is prospectively frozen:

- primary family: G1 normalized regulatory-interaction architecture;
- state semantics: transcriptomic regulatory state;
- methylation/substrate: external/contextual modifier rather than naive concatenated state;
- system scope: paired local + embedded analysis;
- temporal comparator: G2 transition operator;
- materially different alternative: G4 attraction/diffusion;
- **A3:** `r=2` and `r=3` are co-equal robustness representations; neither may be selected after outcomes; material disagreement returns `REPRESENTATION_DEPENDENT_NO_TRANSFER`;
- **B3:** G1 representation will use an externally sourced signed-regulon universe plus an outcome-blind low-dimensional rule; CollecTRI leads source qualification and DoRothEA is retained as a representation sensitivity;
- **C3:** normalized empirical G1 is withheld until restoration is independently resolved rather than supplied by an assumed common beta.

Architecture freeze:

`config/gri_Chi_bio_ABC_architecture_freeze_20260913_v0_1.json`

This is an architecture freeze, not a complete empirical execution freeze.

## 2. What safe work resolved after A3/B3/C3 approval

### A3 execution guard

The empirical freeze contract now supports an A3 design only when:

```text
primary_rank = null
sensitivity_ranks = []
robustness_ranks = [2,3]
```

and a material-conclusion schema is frozen before real candidate values. The code cannot silently promote either rank.

### B3 provenance guard

CollecTRI and DoRothEA candidate repository identities are pinned for provenance, but repository commits are not treated as byte-identical data exports. A read-only export preflight hashes the exact future interaction table and inventories schema/row count while being prohibited from scoring TF activity, selecting dimension, fitting an operator or computing Chi.

The exact regulon export, exact panel and scoring rule remain unfrozen.

### C3 enforcement

The architecture contract explicitly forbids normalized empirical G1 execution and forbids smuggling in a restoration normalization while C3 is active. Effective-Jacobian/local-stability work may continue without calling it normalized G1.

## 3. New G2 operator-model issue discovered before real data

The earlier controlled model

```text
x_(k+1) = T x_k + B u_k + c
```

has one shared `T`. Treatment may shift forcing/equilibrium through `B u`, but treatment cannot change `rho(T)` in that model because the operator is shared by construction.

That makes it a useful restricted/null model, but it cannot directly answer whether cetuximab reorganizes the transition operator.

A minimal treatment-dependent alternative is:

```text
x_(k+1) = T0 x_k + u_k DeltaT x_k + B u_k + c

PBS: T_PBS = T0
CTX: T_CTX = T0 + DeltaT
```

This treatment-interaction formulation has been implemented and tested only on known-truth synthetic data. No SCC25 molecular matrix has been opened by this work.

Detailed attack:

`docs/GRI_CHI_BIO_G2_OPERATOR_MODEL_ATTACK_P0D_20260913.md`

## 4. Next science choice D: first G2 operator model

### D1: shared operator + additive treatment input

```text
x_(k+1) = T x_k + B u_k + c
```

Role: restricted/null model asking whether treatment acts as forcing while one common local operator remains adequate.

Limitation: cannot establish treatment-associated operator reorganization.

### D2: treatment-interaction operator

```text
x_(k+1) = T0 x_k + u_k DeltaT x_k + B u_k + c
```

Role: explicit treatment-associated operator reorganization in one frozen representation.

Short-term SCC25 formal design count, if PBS day 0 is prospectively licensed as the shared pretreatment state:

```text
10 transitions total
r=2 -> 2r+2 = 6 predictor columns
r=3 -> 2r+2 = 8 predictor columns
```

Both A3 ranks are algebraically possible, but `r=3` has very little residual information and therefore requires especially strong conditioning/adequacy checks.

### D3: separate-arm operators

Fit independent `T_PBS` and `T_CTX` in the same frozen state basis.

Role: flexible stress sensitivity.

Limitation: loses parameter sharing and is vulnerable to tiny-sample instability.

**Current pre-outcome recommendation:** D2 primary, D1 restricted/null comparator, D3 stress sensitivity only if conditioning remains adequate. This recommendation is based on identifiability, not SCC25 outcomes, and is **not yet frozen**.

## 5. Remaining full G2 empirical-freeze decisions

Even after A3, the first real G2 execution still requires prospective freezing of all of the following:

### E. RNA count transformation / normalization

The short-term processed source is a gene-level count matrix. Raw counts must not be fed directly into PCA merely because they are available.

The exact transformation must be frozen before the treated trajectory is used. Candidate classes include a prospectively fixed variance-stabilizing/count-normalizing transformation or an explicitly defined library-size normalization plus log transform. The choice must preserve a clean transport story into the chronic source.

### F. Feature universe

The source exposes tens of thousands of genes while only 6 PBS control states define the R1 basis. A feature rule is therefore part of the hypothesis, not invisible preprocessing.

A defensible rule must be outcome-blind and cannot select genes because they respond to cetuximab, improve a unity crossing or match proliferation.

### G. Day-0 initialization

Short-term SCC25 has PBS day 0 and treated days 1-5. The clean candidate convention is to license the PBS day-0 molecular state as the common pre-treatment initial state for both branches. This is biologically natural but still must be prospectively recorded because it changes the transition count from 9 to 10.

### H. Conditioning refusal

Full column rank is necessary but not sufficient. A frozen condition-number / perturbation-stability rule is needed so an algebraically solvable but numerically explosive operator is refused rather than interpreted.

### I. Model adequacy refusal

The first analysis needs a rule for when a low-order linear transition model is simply not adequate. Candidate diagnostics include residual scale, leave-one-transition-out sensitivity, coefficient/spectral perturbation stability and restricted-versus-interaction predictive comparison.

### J. Uncertainty

Weeks/days are serial descendants, not iid biological replicates. Ordinary iid bootstrap over time points is not licensed. Any uncertainty procedure must preserve that limitation and distinguish model-conditional perturbation uncertainty from biological replication uncertainty.

### K. Cross-timescale transport

Daily GSE114446 and weekly GSE98812 cannot be compared numerically as though their raw transition radii have the same interval. A transport rule is required. Any conversion such as `rho_ref = rho_Delta^(Delta_ref/Delta)` requires a separately justified time-invariant semigroup interpretation.

### L. A3 material-conclusion schema

A3 needs the exact statements that must agree under `r=2` and `r=3` before outcomes. Otherwise "material agreement" could be redefined after the fact.

Examples of candidate material conclusions for later freeze include:

- whether the chosen operator model is identifiable and passes adequacy checks;
- whether treatment-associated operator reorganization is supported under the chosen model;
- whether the side of the mathematical unit-circle boundary is the same under both ranks, while explicitly withholding biological boundary interpretation;
- whether non-normal transient warnings materially alter the asymptotic spectral statement.

## 6. Synthetic calibration now authorized and running as P0-D

A deterministic synthetic calibration harness now exercises the proposed treatment-interaction design at both A3 ranks under known-truth stable, near-unit-circle, above-unit-circle and non-normal systems across a fixed synthetic noise grid.

It reports:

- full-rank fit fraction;
- design condition-number distribution;
- control and treated spectral-radius recovery error;
- treatment-operator recovery error;
- mathematical unit-circle side recovery;
- non-normal warning recovery.

It explicitly does **not**:

- estimate SCC25 measurement noise;
- select an empirical condition-number cutoff;
- choose a rank winner;
- compute real G2;
- admit Chi_bio.

Runner:

`src/run_chi_bio_g2_interaction_calibration.py`

The CI workflow executes 500 replicates per synthetic cell and uploads the JSON as a development artifact.

## 7. B3 work that can continue independently

Safe B3 work can continue through:

- exact CollecTRI / DoRothEA export acquisition and byte hashing;
- schema/evidence/sign provenance;
- organism and identifier mapping checks;
- duplicate/contradictory edge accounting;
- gene-universe overlap with SCC25 and frozen TCGA RNA identifiers;
- synthetic low-dimensional identifiability tests using fixed candidate rules.

It must still stop before choosing the exact panel by inspecting SCC25/TCGA candidate behavior.

## 8. Computational posture

Nothing in the immediate SCC25 G2/B3 qualification requires HPC or GPU compute. The limiting problem is **identifiability**, not floating-point throughput.

The short-term matrix has about 56k genes but only 11 SCC25 states; after transformation, PCA to `r=2/3` and fitting 2x2/3x3 operators is laptop-scale. The chronic 22-state series is likewise small.

The heavier stage is later TCGA transport. The frozen C1 RNA state is approximately `9457 x 22601` float64, about 213.7 million values or 1.71 GB in decimal bytes before copies/intermediates. That later stage should be designed around memory mapping/chunking and compact regulon/module scores rather than repeated dense transcriptome copies.

## 9. Current hard stop

Safe preparation can continue through synthetic calibration, provenance qualification, contracts, source hashing and non-outcome normalization/feature-method comparison.

Real SCC25 G2 remains blocked until D through L are frozen. Normalized empirical G1 remains blocked by C3 until independent restoration information exists.

## 10. Claim ceiling

The A3+B3+C3 architecture is approved and frozen. It supports a disciplined path to a temporal comparator and a mechanistically grounded future G1 state. It does not support an admitted biological Chi, a numerical G1, a cancer ranking or a biological unity boundary.
