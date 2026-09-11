# Neurostability Atlas v0.1

Date opened: 2026-09-11
Governing System Model: **NSD System Model v1.0, architecture locked**
Governing protocol: **General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum**
Status: **ATLAS P0-D/P0-Q COORDINATE-MAP CONSTRUCTION. NOT AN ENGINE TRAINING TARGET. NOT P1.**

## Purpose

The Neurostability Atlas is an independent, provenance-rich map of native and explicitly licensed derived dynamical coordinates relevant to the locked NSD System Model.

It is not a table of desired NSD answers. It does not tell the Structural Engine what it must find. It does not assume that every neural system has one scalar chi, one modal order, one stability regime, or one universal normal range.

The Atlas exists to answer a different question:

> What dynamical coordinates are actually supported in the literature, open datasets and independently reconstructable evidence, under what conditions, with what uncertainty, and across what functional/perturbation/transition/limit contexts?

## Relationship to the locked System Model

Atlas coordinate families mirror the System Model's scientific objects:

1. scalar / spectral coordinates;
2. modal / carrier and invariant-subspace coordinates;
3. conglomerate / system-organization coordinates;
4. open-channel coordinates including identifiability, adequacy and uncertainty;
5. optional model-conditional derived coordinates only when their derivation is licensed.

The Atlas may contain coordinates corresponding to Engine outputs, but Atlas values are read-only with respect to confirmatory Engine rule construction.

## First rule: native before derived

Every source is represented first in its own native model/parameterization.

A derived coordinate is admitted only if:

- the source reports the required native quantities or they are independently reconstructed from accessible raw data;
- the transformation is explicit and dimensionally valid;
- the assumptions of the transformation are recorded;
- the source/model supports those assumptions;
- uncertainty/provenance are propagated or explicitly marked unresolved.

A computable-looking ratio is not enough.

## Chi policy

`chi` is **WITHHELD by default**.

The Atlas may record chi only when a source/native model provides or licenses the required second-order factorization and the exact meaning of the frequency term is specified. Generic complex poles do not automatically license chi.

Allowed statuses include:

- `CHI_NATIVE_REPORTED`;
- `CHI_DERIVED_LICENSED_SECOND_ORDER`;
- `CHI_WITHHELD_NO_SECOND_ORDER_LICENSE`;
- `CHI_WITHHELD_INSUFFICIENT_NATIVE_PARAMETERS`;
- `CHI_NOT_APPLICABLE`.

No missing chi value is imputed merely to fill the map.

## Research-role coverage

Atlas source intake seeks, where scientifically available:

- `NOMINAL_FUNCTION`;
- `PERTURBED_FUNCTION`;
- `BOUNDARY_OR_TRANSITION`;
- `RARE_NATURAL_LIMIT`.

Equal counts are not required. A rare natural case is used only if its rarity is domain-native and its eligibility can be established independently of the NSD result.

## Evidence independence

Each Atlas source/entry carries pathway-specific grades for:

- data;
- cohort/system;
- outcome/label;
- parameter/tuning;
- method/estimator;
- Atlas/Engine interaction;
- source/literature;
- temporal/decisive-evidence timing.

The Atlas is not called independent simply because it is stored in a different folder.

## Coordinate eligibility states

Every requested coordinate is classified as one of:

- `NATIVE_REPORTED`;
- `NATIVE_RECONSTRUCTED_FROM_RAW_DATA`;
- `DERIVED_EXACT`;
- `DERIVED_MODEL_CONDITIONAL`;
- `WITHHELD_INSUFFICIENT_INFORMATION`;
- `WITHHELD_ASSUMPTION_NOT_LICENSED`;
- `NOT_APPLICABLE`;
- `UNRESOLVED`.

Missing and refused coordinates are part of the Atlas.

## v0.1 sequence

`A0 coordinate schema -> A1 source discovery -> A2 native extraction/reconstruction -> A3 licensed derivation -> A4 provenance/independence QA -> A5 Function/Limit occupancy map -> A6 Atlas qualification -> read-only Engine/Atlas comparison`

No Atlas coordinate is used to tune an Engine threshold during this sequence.

## Current queue

1. freeze the v0.1 coordinate ontology/schema;
2. build a source-intake ledger spanning nominal, perturbed, transition and qualified rare-limit contexts;
3. prioritize open/full-text or open-data evidence where exact numeric provenance can be reconstructed;
4. populate native coordinates before SymC-derived coordinates;
5. preserve non-coordinates and failed derivations rather than replacing them with assumptions.
