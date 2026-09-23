# BioSystems adversarial Round 1 - external prostate metadata/technical covariate audit freeze

**Date:** 23 September 2026
**Status:** FROZEN BEFORE METADATA INVENTORY EXECUTION
**Branch:** `biosystems-adversarial-r1-20260923`
**Immutable parent:** `biosystems-resubmission-20260923-final` @ `18b1e3b6c828626143ac37da3fe279dd605751d5`
**Program authority:** SymC General Operations Manual v0.8.4
**Role:** source/metadata qualification only. No H1/H2/H3 molecular endpoint may be computed in this gate.

## Question

Which non-outcome demographic or technical covariates are actually source-bound and sufficiently observed in the frozen independent prostate lanes to support a scientifically interpretable post-result H1 sensitivity?

The audit exists because Round-1 review correctly identified batch/center/plate/array/age and other structured sample axes as possible explanations for the unusually large external H1 effect.

## Frozen source families

- RNA: GSE237995
- 450K methylation: GSE262522
- EPIC methylation: GSE262524

The participant sets remain exactly those in `biosystems_external_prostate_p1_v1_0.json`.

No participant may be added, removed, or selected using any molecular result.

## Metadata-only inputs

The workflow may read:
- GEO series-matrix metadata;
- GEO sample titles/accessions;
- source `characteristics_ch1`, descriptions, platform identifiers and acquisition labels;
- the already-frozen P1 participant IDs and source header labels.

It may not read beta values, RNA counts, H1/H2/H3 values, or P1 null outputs.

## Inventory rules

For each frozen lane, inventory every source-bound field and report:
- field/key name;
- raw source values;
- normalized non-destructive representation;
- finite/nonempty coverage;
- number of unique values;
- category counts for categorical variables;
- whether the field is constant;
- whether it is outcome-like/biological-state information versus non-outcome demographic/technical metadata.

## Candidate confound classes

The audit specifically searches for:
- age;
- sex;
- race/ancestry label;
- tissue collection center/site;
- processing batch;
- plate;
- Sentrix/slide/chip identifier;
- array row/position;
- scan/acquisition batch;
- other source-declared technical grouping.

Disease grade/stage, Gleason score, tumor subtype and molecular phenotype may be inventoried but are **not** automatically eligible confound regressors because they can be biological state/mediator variables.

## Mechanical eligibility rule for a later H1 sensitivity

A non-outcome covariate is marked `ADJUSTMENT_CANDIDATE` only when:

- its source meaning is unambiguous;
- it is not derived from GRI/H1 outcome;
- primary 450K n=30 coverage is >=90%;
- for categorical variables, at least two levels contain >=5 primary participants;
- for continuous variables, at least 20 primary participants are finite and at least 8 distinct values are present;
- its use does not condition on tumor response/outcome or remove the biological state being tested.

A field failing these rules remains documented but is not forced into a regression.

Race is already separately tested and remains listed for provenance; this audit does not rerun race H1.

## Disposition

This gate returns only:

- `METADATA_ADJUSTMENT_CANDIDATES_IDENTIFIED`;
- `NO_ADDITIONAL_IDENTIFIABLE_TECHNICAL_COVARIATES`;
- or `METADATA_IDENTITY_HOLD`.

If candidate covariates are identified, a **separate prospective Round-1 sensitivity freeze** must define the exact regression/null before any molecular value is opened.

If none are identified, the manuscript must state that broader external technical/batch structure remains unresolved because the public source does not expose an identifiable adjustment variable under the frozen rules.

## Claim ceiling

This audit cannot validate H1, upgrade P1, explain the external effect magnitude, or establish absence of batch/confounding. It only determines what source-supported adjustment is possible.
