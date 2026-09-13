# GRI Chi_bio SCC25 representation and leakage firewall

**Date:** 2026-09-12  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4  
**Source:** Stein-O'Brien et al. SCC25 cetuximab time course, GSE98812/GSE98813/GSE98815  
**Research mode:** P0-D source/representation control  
**Chi_bio status:** `NOT_ADMITTED`  
**Chi_bio outcomes on SCC25:** `UNOPENED`

## 1. Purpose

The SCC25 time course is a high-priority temporal falsification/calibration source because it contains ordered treated and time-matched control states with RNA-seq and DNA methylation measured on corresponding weekly states. This document freezes what may and may not be used to construct a future G1/G2 state representation before any Chi_bio trajectory is inspected.

The source identity is frozen separately in `config/gri_scc25_paired_timecourse_manifest_p0d_v0_1.json`.

## 2. Main trajectory role

Only the 22 paired weekly states are admitted to the **main ordered trajectory**:

```text
11 weeks x 2 arms = 22 paired states
arm 1 = PBS
arm 2 = 100 nM cetuximab
```

Each state has one RNA GSM and one methylation GSM in the frozen manifest.

Baseline samples and stable resistant clones remain separate source roles. They cannot be silently appended to the ordered sequence because they do not share the same temporal role.

## 3. Published feature-selection firewall

The published study used feature filtering tailored to its own longitudinal integration question, including RNA filtering by time-course expression behavior and methylation filtering by switching/dynamic behavior before CoGAPS integration.

Those published filters are legitimate for the original paper. They are **not prospectively independent for the new Chi_bio question**.

Therefore the future Chi_bio adapter may not simply inherit the paper's outcome/time-structure-informed reduced RNA or methylation feature sets and call them a neutral state representation.

Rule:

```text
published outcome/time-informed feature filter
!=
prospectively frozen Chi_bio state definition
```

A future G1/G2 state reduction must be frozen using criteria that do not inspect:

- candidate Chi_bio trajectory;
- distance from unity;
- proliferation transition timing;
- treated-versus-control separation produced by candidate Chi;
- stable-resistant-clone labels as a tuning target;
- downstream cancer outcome.

## 4. Phenotype firewall

The independent proliferation trajectory is scientifically valuable precisely because it can contradict a future candidate.

It therefore cannot be used simultaneously to choose the state reduction and then be counted as evidence that the resulting coordinate tracks resistance.

Frozen role:

```text
proliferation phenotype = independent response/transition axis
not = state-construction input
not = dimension-selection input
not = unity-tuning target
```

The proliferation series may be opened for a formally frozen validation question only after the candidate state/operator/decision rule is fixed.

## 5. Methylation role under the approved G1/S1/L3 plan

The approved S1 state is transcriptomic regulatory state.

Therefore methylation remains:

```text
substrate/context input or modifier
```

and is **not** naively concatenated with RNA into one state vector merely to retain both modalities.

Candidate methylation roles that may be investigated before outcome inspection include:

- parameter/context stratification of the regulatory map;
- modifier of regulatory edges or modules when a native biological derivation supports it;
- separate substrate coordinate used to test operator reorganization;
- embedding/context variable in local-versus-embedded analysis.

No specific methylation-to-operator mapping is frozen here.

## 6. Serial dependence and replication

The weekly molecular profiles are ordered serial descendants. Replicated culture flasks were pooled to produce each molecular state.

Therefore:

- the 11 weeks per arm are not 11 independent biological replicates;
- ordinary iid uncertainty across weeks is not licensed;
- a transition model has 10 one-step transitions per arm;
- effective sample information is smaller than a 22-independent-sample treatment would imply;
- stable resistant clones cannot be used to inflate temporal sample count.

Any uncertainty engine must preserve the serial structure rather than resampling weeks as exchangeable independent observations unless a separately justified procedure is frozen.

## 7. G2 dimensionality firewall

For

```text
x_(k+1) = T x_k + B u_k + c + noise,
```

the SCC25 series is dramatically underpowered for an unconstrained transcriptome-scale `T`.

Best-case algebraic rank ceilings already established:

- shared `T`, one treatment input, intercept, both arms: `d <= 18`;
- separate arm-specific `T` with intercept: `d <= 9` per arm.

These are only formal ceilings. They do not account for serial dependence, pooled states, collinearity, noise, regularization debt, or validation. A practical state must be lower-dimensional or structurally constrained.

The dimension may not be chosen by maximizing agreement with resistance or by producing a desired unity crossing.

## 8. G1 restoration firewall

The G1 hardening result is binding:

- a generic transcriptomic trajectory that identifies an effective `J` does not identify `K` and `R` separately;
- heterogeneous directed systems do not inherit `alpha(R^-1 K)=1` as an exact boundary;
- a common restoring scale `R=beta I` must be independently justified if G1A is used;
- G1B requires a symmetric production Jacobian and SPD restoration operator and therefore cannot be applied to a directed GRN by convenience.

No SCC25 fit may choose a restoration model because it makes the candidate cross one at a biologically appealing week.

## 9. Baseline and stable-clone roles

### Baselines

Baseline samples may later serve a separately frozen normalization, initialization, or source-QC role. They are not part of the 22-state ordered trajectory by default.

### Stable resistant clones

Stable clones may later serve as an externalized endpoint/limit test within the same laboratory lineage, but only under a separately frozen role. They may not be used to train a trajectory coordinate and then reused as if independent confirmation.

## 10. Platform metadata discrepancy

GEO identifies the methylation platform as `GPL13534`, Illumina HumanMethylation450 BeadChip. Individual sample records describe the labeling protocol as `Infinium Human MethylationEPIC Beadchip Kit` while exposing 485,512 processed probe rows, consistent with the 450K platform record.

This discrepancy is preserved as source metadata. The adapter must rely on actual probe identities/platform provenance rather than silently rewriting one label to match the other.

## 11. Data acquisition and provenance requirements

Before any SCC25 candidate computation:

1. obtain and hash the exact source files used;
2. preserve raw accession identity and download timestamp;
3. verify RNA/methylation state correspondence against the frozen GSM manifest;
4. record raw versus processed representation and transformation;
5. preserve missingness and feature-universe rules;
6. keep original paper filters as provenance only unless separately re-licensed;
7. freeze state-reduction code and parameters;
8. freeze treatment/control input coding;
9. freeze interval/time convention;
10. freeze uncertainty/refusal rules;
11. only then compute candidate trajectories.

## 12. Current disposition

```text
source identity:              FROZEN P0-D
main 22-state pairing:        FROZEN
Chi_bio state reduction:      NOT FROZEN
G1 restoration model:         NOT FROZEN
G2 state dimension:           NOT FROZEN
methylation coupling formula: NOT FROZEN
proliferation validation axis: PRESERVED / UNOPENED FOR CHI VALIDATION
Chi_bio outcome:              NOT COMPUTED
```

The next safe operation is to compare outcome-blind reduction/measurement routes by identifiability and native biological meaning. Selecting one empirical state reduction is a scientific freeze and must occur before any Chi_bio values are computed.
