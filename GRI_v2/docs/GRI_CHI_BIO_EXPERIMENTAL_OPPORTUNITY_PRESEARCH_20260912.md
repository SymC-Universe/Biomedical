# GRI Chi_bio experimental-opportunity plan, pre-search record

**Date:** 2026-09-12  
**Status:** PRE-LITERATURE-COLLISION DESIGN RECORD  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4  
**Literature-collision status at freeze:** NOT YET PERFORMED FOR THESE SPECIFIC DESIGNS

## Purpose

Before targeted searching for experiments that may already answer the Chi_bio question, preserve the experiments we would want if no such literature existed. This record does not claim novelty and does not authorize human/animal/clinical experimentation.

## Experiment A: dense perturb-and-release regulatory time course

### Question
Can a system-level coordinate derived from scalar + modal/vector + conglomerate organization predict whether a regulatory state returns, reorganizes, or crosses into a different response regime after a controlled perturbation?

### Ideal design

- one or more well-characterized cancer cell systems;
- baseline measurements before perturbation;
- a controlled reversible perturbation with domain-native rationale;
- dense early and late timepoints sufficient to distinguish transient response from recovery/reorganization;
- matched RNA plus at least one regulatory substrate measurement, preferably DNA methylation and/or chromatin accessibility; protein/phosphoprotein context where feasible;
- biological replicates;
- a washout/release phase where the perturbation permits it;
- independently defined phenotypic response/recovery readout not used to build Chi_bio.

### Required outputs

- state-space trajectory;
- modal/eigenstructure over time or a justified local approximation;
- recovery/relaxation and/or transition operator;
- uncertainty on candidate Chi_bio;
- explicit refusal if timing cannot identify the candidate generator;
- test of unity only after candidate construction is frozen.

## Experiment B: paired acquisition of treatment resistance

### Question
Does the same frozen Chi_bio construction transport from baseline to acquired resistance, and does its movement correspond to a separately defined change in regulatory response class?

### Ideal design

- matched baseline and resistant states from the same biological lineage;
- methylation + RNA on the same state, plus treatment metadata;
- multiple resistant states or intermediate states where available;
- no candidate selection based on whether the resistant state crosses unity;
- patient-derived and cell-model branches analyzed separately.

### Required outputs

- within-lineage coordinate movement;
- modal reorganization versus scalar movement;
- conglomerate/context changes;
- boundary-blind comparison of candidate Chi_bio before and after resistance;
- explicit test of whether scalar movement is preserved when modal architecture differs.

## Experiment C: longitudinal tumor evolution with repeated multi-omic sampling

### Question
Can Chi_bio distinguish preserved system organization from reorganization across clinically ordered tumor states without assuming that chronological order is itself a stability mechanism?

### Ideal design

- repeated samples from the same patient;
- exact patient/timepoint identity;
- regulatory substrate + RNA measured at each relevant state;
- treatment/exposure history between samples;
- enough repeated states to separate patient identity from transition structure;
- where possible, single-cell/single-nucleus data to compare lower-scale organization with tumor-level aggregation.

### Required outputs

- within-patient trajectories;
- local versus embedded organization distinction;
- hierarchical-closure test where both lower- and higher-scale measurements exist;
- candidate Chi_bio transport and refusal status;
- no recovery claim unless sampling actually resolves recovery.

## Experiment D: known-truth synthetic generator

### Question
Can the implementation recover a system-level Chi-like balance coordinate when one is known to exist, and refuse when scalar compression is intentionally invalid?

### Design

Generate synthetic systems spanning:

- identifiable versus non-identifiable parameterizations;
- normal versus non-normal mode structure;
- aligned versus discordant scalar/modal organization;
- coupled systems where multiple internal organizations produce similar aggregate output;
- cases with and without a true unity boundary;
- noise and missingness levels comparable to the intended biological measurements.

### Required outputs

- recovery bias and uncertainty;
- false admission rate;
- boundary classification accuracy where a true boundary exists;
- refusal accuracy where no coherent scalar exists;
- evidence that a convenient aggregate score is not mistaken for the known truth.

## Experiment E: Atlas-blind external transport

### Question
Does a frozen Chi_bio construction remain measurable and ordered under a genuinely external representation without using the external Atlas to redefine the coordinate?

### Design

- freeze candidate formula/code before opening decisive external Chi_bio results;
- qualify sample identity and representation adapter independently;
- preserve all external cases, including disagreement and refusal;
- compare a priori unity with a freely estimated alternative threshold only after coordinate computation.

## Priority order before targeted literature collision

1. Experiment D can be built computationally once a candidate generator exists.
2. Experiments B/C are likely answerable from already identified public longitudinal/perturbational source families if their time resolution and modalities are adequate.
3. Experiment A is the strongest direct dynamical design if existing data do not provide enough temporal density.
4. Experiment E is required before confirmatory Atlas use.

## Claim firewall

Finding that prior literature already performed one or more of these designs is a success, not a loss of novelty. Such evidence should be treated as known-truth opportunity, method inheritance, or prior art according to what it actually establishes.

**Next protocol step:** perform a targeted literature-collision pass against these frozen design questions, then classify each as already answered, partly answered, method-available, conflicting, or residual/unanswered.