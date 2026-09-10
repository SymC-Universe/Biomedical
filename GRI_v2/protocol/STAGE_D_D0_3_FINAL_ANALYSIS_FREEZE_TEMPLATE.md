# Stage D D0.3 Final Analysis Freeze Template

Status: TEMPLATE ONLY. DO NOT MARK FROZEN UNTIL D0.1/D0.2 METADATA/DESIGN AUDIT IS COMPLETE.

This document exists so all decisions required before biological outcome inspection are visible in advance. Empty fields are not permission to choose after results.

## Dataset-specific design

For each D1-D4 dataset record:
- exact assay files;
- sample IDs and condition labels;
- replicate structure;
- paired/unpaired status;
- time points;
- treatment/dose/withdrawal definitions;
- platform/batch variables;
- control matching rule;
- evaluability exclusions and why.

## Feature universes

Freeze separately for:
- methylation scalar view;
- methylation modal view;
- RNA scalar/modal/conglomeration views;
- Hallmark mapping;
- PCHi-C/contact layer if used;
- unsupervised capacity-matched comparator;
- size-matched shuffled-Hallmark comparator;
- regulatory-context depth sets.

For each universe record:
- source annotation;
- mapping version;
- minimum completeness;
- variance/nonzero rules;
- missingness handling;
- feature count before/after filtering;
- rule for features absent from a platform.

## Transformations

Freeze:
- beta/M-value treatment for methylation;
- RNA scale;
- centering/scaling;
- imputation training scope;
- batch covariate treatment;
- dimensionality reduction fitting scope;
- sign/orientation rules;
- no-target-leakage rule.

## Recovery endpoints

Freeze per layer:
- norm for Q_residual;
- acute time point;
- recovery endpoint(s);
- matched early/late control definitions;
- direction-preserving versus magnitude-only secondary endpoints;
- replicate aggregation;
- uncertainty method.

## D2 time-course model competition

Specify candidate families and selection metric before fit:
- persistent-offset/no-recovery;
- single exponential;
- biexponential only if support permits;
- nonparametric descriptive fallback.

Freeze:
- minimum time points;
- minimum replicates;
- parameter bounds;
- identifiability rule;
- model-comparison criterion;
- when tau must be refused.

## Cross-layer detectors

### Linear primary
Freeze exact linear-kernel CKA / Spearman / ridge definitions and their roles.

### Nonlinear secondary
Freeze exact kernel/test, including:
- RBF kernel construction;
- bandwidth rule independent of outcome;
- centering;
- null generation;
- minimum n;
- small-n/refusal rule;
- synthetic calibration.

A nonlinear result cannot retroactively rescue a failed linear primary; it is reported as its own detector branch.

## CKA calibration

Freeze:
- empirical permutation replicate count B;
- deterministic RNG namespace/seeds;
- analytic expected floor;
- full spectra storage;
- fixed-spectrum CKA_max;
- realized-alignment denominator stability/refusal rule;
- empirical upper-tail reporting.

## Nulls and comparators

Freeze exact counts/seeds for:
- sample-label shuffle;
- Hallmark-label shuffle;
- size-matched shuffled Hallmark membership;
- top-k unsupervised methylation PCs;
- technical/platform attacks;
- treatment/dose controls;
- regulatory-context depth comparison.

## Multiple testing

List every formal family and its size before results. Descriptive sensitivities receive no automatic p-values.

## D1/D2 signature freeze

Define in advance:
- eligibility for a recovery-associated signature;
- sign/direction rule;
- whether a signature may be modal, scalar, conglomeration, or cross-view relationship;
- uncertainty requirement;
- rejection/refusal states;
- exact moment D3/D4 outcome access becomes allowed.

## D3/D4 challenge

Freeze:
- transformation-state ordering supplied by experiment design;
- primary contrast(s);
- direction expected from D1/D2 signature only;
- no retrospective feature selection;
- nonlinear secondary interpretation;
- transformation-resistant state definition from source metadata, not from Stage-D score.

## Promotion/refusal

Reference `stage_d_promotion_contract_v0.1.json` without modification unless an explicit pre-outcome amendment is committed.

## Provenance lock

Record:
- GitHub commit SHA;
- hashes of all acquisition manifests;
- hashes of normalized sample manifests;
- hashes of all configs;
- environment lock;
- confirmation that biological outcome matrices had not been interpreted before this freeze.
