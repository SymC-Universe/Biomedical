# GRI Conglomerate Chi C1 patient/system carrier materialization contract

**Date:** 2026-09-18  
**Status:** FROZEN BEFORE REAL CONGLOMERATE CARRIER MATERIALIZATION  
**Branch:** `gri-conglomerate-chi-tool-v1-20260918`

## Purpose

C1 converts already-defined block-level measurements into one reproducible patient/system-level capital-Chi carrier without creating a master score, fitting an outcome, or changing any upstream scientific definition.

The C1 operation is **structural materialization**, not biological model selection.

## Carrier rule

Each row is one feature measurement or qualified derived measurement for one entity in one block. Blocks are concatenated in long form. They are never summed, averaged, z-scored across blocks, weighted, or otherwise compressed by C1.

Allowed block IDs:

- `R`: RNA regulatory organization
- `S`: methylation / regulatory-substrate organization
- `E`: embedding/composition/context
- `G`: genomic constraint/context
- `P`: protein/phosphoprotein
- `M`: modal/vector carrier
- `T`: temporal/operator
- `Q`: quality/uncertainty/confidence/refusal

## Required row fields

| Field | Rule |
| --- | --- |
| `entity_id` | stable patient/system identity for joining within a cohort |
| `cohort_id` | source cohort identity |
| `system_id` | cancer/system label |
| `sample_id` | source sample/state identity when applicable |
| `block_id` | one of R,S,E,G,P,M,T,Q |
| `feature_id` | frozen feature/coordinate identifier |
| `value` | numeric only when value_status permits; blank otherwise |
| `value_status` | OBSERVED, DERIVED_FROZEN, MISSING, NOT_APPLICABLE, REFUSED, or NOT_IDENTIFIABLE |
| `uncertainty_value` | optional numeric uncertainty, blank when unavailable |
| `uncertainty_kind` | NONE, SD, SE, CI95_HALF_WIDTH, BOOTSTRAP_SD, or OTHER |
| `local_embedded_role` | LOCAL, EMBEDDED, CONTEXT, TEMPORAL, QUALITY, or NOT_APPLICABLE |
| `time_index` | numeric/string ordered index only when genuinely observed; otherwise blank |
| `time_order_known` | TRUE only for directly ordered measurements |
| `evidence_class` | P0-D, P0-Q, P1, P2, or HISTORICAL |
| `independence_role` | DEVELOPMENT, INTERNAL_HOLDOUT, EXTERNAL_UNTOUCHED, REUSED_DEPENDENT, or NOT_APPLICABLE |
| `source_id` | exact upstream source/artifact identifier |
| `source_digest_or_run` | immutable hash or workflow/run/artifact identity |
| `transform_id` | frozen upstream transform/representation; `RAW` where none |

## Missingness and refusal firewall

- A missing feature is never represented by numeric zero.
- `NOT_APPLICABLE` is distinct from `MISSING`.
- `REFUSED` and `NOT_IDENTIFIABLE` remain explicit states and cannot be converted to imputed values by C1.
- Static TCGA rows cannot use `time_order_known=TRUE`.
- The T block is absent or NOT_APPLICABLE for systems without directly ordered temporal data.

## Duplicate rule

The tuple

`(entity_id, cohort_id, sample_id, block_id, feature_id, transform_id)`

must be unique. Exact duplicate rows are a hard error rather than silently averaged.

## Forbidden output columns

C1 output must not contain:

- `Chi_bio_value`
- `chi_bio_value`
- `master_score`
- `global_stability_score`
- any generated diagnostic class
- any generated predictive outcome

Such objects require later, separately frozen stages if they are ever scientifically justified.

## C1 outputs

1. `conglomerate_carrier_long.csv`
2. `conglomerate_carrier_manifest.json`

The manifest records input file hashes, row counts by block/status/evidence class, duplicate checks, forbidden-column checks, and output SHA-256.

## C1 claim ceiling

C1 can establish only that the previously defined attributes can be materialized together without losing their identities and epistemic roles. It does not establish that the blocks form a useful diagnostic, predictive tool, biological mechanism, disease stage, scalar coordinate, or unity boundary.

## Next gate

C2 may add tested cross-block relationships as a **separate relation table**. C3 may benchmark/ablate the carrier only after C1/C2 schemas pass known-truth tests and the real-data materialization manifest is frozen.
