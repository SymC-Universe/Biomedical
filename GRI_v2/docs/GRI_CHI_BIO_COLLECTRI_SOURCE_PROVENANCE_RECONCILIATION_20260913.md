# GRI CollecTRI source-provenance reconciliation

**Date:** 2026-09-13  
**Mode:** P0-D provenance qualification only  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.5  
**Architecture:** approved A3 + B3 + C3  
**Chi_bio:** `NOT_ADMITTED`

## Purpose

This record closes the exact-byte source-provenance step for the CollecTRI branch of approved B3 without selecting an empirical state, TF panel, scoring method, dimensionality rule, transition operator, or Chi_bio value.

## 1. Initial workflow failure

The first CollecTRI provenance job made four bounded requests to the frozen source and received HTTP 504 gateway time-outs. No source bytes were acquired and no downstream transformation, TF activity scoring, operator fitting, or candidate computation occurred.

Disposition: `EXTERNAL_PROVIDER_FAILURE_NO_SCIENTIFIC_CONTRADICTION`.

Only the failed provenance job was retried. Successful jobs were not rerun.

## 2. Bounded retry result

The retry succeeded on its first source request with HTTP 200 and 4,345,649 bytes received.

Frozen source record:

`Zenodo 8192729 / CollecTRI_regulons.csv`

Raw source SHA-256:

`4473c9189dd53dacc80297709ad1452dda1086a1cc2185f9a56146c261668701`

Canonical human export SHA-256:

`f0bb980ad26a033fd39b370108d6d45e038127c635c7fd9b5df557e2703ef540`

Workflow artifact digest:

`sha256:d8d807c4e90c545e30f840498215e7ac705f73dbb7dc59a61e25a5d3fc9676f5`

Transformation semantics:

`decoupler 2.2.0 human collectri, remove_complexes=False`

## 3. Canonical inventory

The provenance-only canonical export contains:

- 42,990 signed edges;
- 1,185 unique TF sources;
- 6,675 unique targets;
- 37,168 positive edges;
- 5,822 negative edges;
- 0 zero-weight edges;
- 0 exact duplicate rows after provider semantics;
- 0 rows in duplicated source-target pairs after provider semantics;
- 0 source-target pairs carrying multiple signs after provider semantics.

Canonical columns:

`source, target, weight, resources, references, sign_decision`

## 4. Firewall verification

The successful provenance run records all of the following as false:

- real expression files opened;
- TF activity scored;
- regulon panel selected;
- state dimension selected;
- operator fit;
- G1 computed;
- G2 computed;
- Chi_bio computed.

Promotion effect: `NONE`.

Therefore this result qualifies **source identity and export semantics only**. It does not convert CollecTRI from B3's leading qualification source into a selected empirical state.

## 5. What is now closed

The earlier repository-commit-versus-data-export ambiguity is closed for this exact CollecTRI export. Downstream B3 work can cite immutable source bytes and a deterministic canonical export rather than treating a repository commit as a substitute for data identity.

## 6. What remains open

The following are still prospective science/design decisions and are not chosen by this record:

1. exact TF panel or outcome-blind subset rule;
2. state scoring rule;
3. dimensionality rule;
4. organism/identifier transport checks against each empirical source;
5. exact DoRothEA export provenance for the independent representation sensitivity;
6. any empirical operator model or Chi_bio calculation.

The existing B3 firewall remains active: no selection may use SCC25 or TCGA Chi behavior, distance to unity, proliferation agreement, Atlas placement, or clinical outcomes.

## 7. Current disposition

`PASS_COLLECTRI_SOURCE_PROVENANCE_ONLY_NOT_STATE_SELECTION`

This is a no-regret prerequisite closure. It carries no promotion and does not change the hard stop on real SCC25 G2 execution before the D-L empirical freeze is explicitly completed.
