# GRI current provenance map and verification-gap ledger

**Date:** 2026-09-16  
**Status:** CURRENT POINTER / VERIFICATION LAYER  
**Historical registry preserved:** `MILESTONE_ARTIFACTS.md`

## Purpose

`MILESTONE_ARTIFACTS.md` remains the historical milestone registry through its own 2026-08-30 state. This file does not rewrite that record. It extends current navigation across the later SCC25, B3, `Chi_bio`, restoration, source-audit, and manuscript lineages while distinguishing exact verified identifiers from gaps that still need reconciliation.

Documentation pointers are not evidence artifacts merely because they live beside evidence.

## A. Historical static Pan-Cancer lineage

Use the existing historical registry plus the frozen Stage C1/post-C1 archives as the source of exact static-stage execution identities.

Known historical registry examples include Stage A, A1.1, B1, B2, C0/C1A handoffs and associated run/artifact identities recorded in `MILESTONE_ARTIFACTS.md`.

**Current rule:** do not copy those identifiers into a new table from memory. When the revised manuscript needs an exact static value/run/hash, reconcile it directly to the historical registry and frozen archive, then record the source in the manuscript ledger.

## B. `Chi_bio` admission-cycle closure

Canonical closure record:

`../docs/GRI_CHI_BIO_ADMISSION_CYCLE_CLOSURE_20260913.md`

Closure input head:

`c95d071999ba0d4c601f190181eeda8137aa4571`

Durable machine state source:

`GRI_CHI_BIO_AI_WORKSTATE_CLOSED_20260913.md`

### B1. Short-term SCC25 G2

```text
workflow_run = 34756865980
artifact_id = 10317941541
artifact_sha256 = 9b6890012183f6d173df4092af1629098d6bd9591490c57c53e92a270f0be55f
scientific_disposition = D1_PREDICTIVE_ADEQUACY_REFUSED_AT_R2_AND_R3
D2_opened = false
```

### B2. Chronic SCC25 G2, primary

```text
workflow_run = 34769901215
artifact_id = 10321342847
artifact_sha256 = 4ad76198657cbb4f5a5839b5ad4068625ccb0801fe050d16b83006d2ef8a5687
scientific_role = PRIMARY_CHRONIC_G2_RESULT
```

### B3. Chronic SCC25 bounded feature-gate robustness

```text
workflow_run = 34770059647
artifact_id = 10321991562
artifact_sha256 = 7a6a289d14ac7129cce979f340cb54fbbde7b3e767d411c243af76af1c7afed2
scientific_role = BOUNDED_FOUNDATIONAL_ROBUSTNESS
```

### B4. B3 matched-network identifiability holdout

```text
workflow_run = 34797932432
artifact_id = 10330711216
artifact_sha256 = 02562ee9f1b47d497529b1e60a3c7df295cbf3b29d8983d1b50271cd189f4298
status = REFUSE_B3_MATCHED_NETWORK_IDENTIFIABILITY
passing_dimensions = []
selected_dimension = null
promotion_effect = NONE
```

### B5. B3 graph-topology spectrum audit

```text
workflow_run = 34798559079
artifact_id = 10330477936
artifact_sha256 = ec28faedd4a1cfee32a288eebd5dd282bcd810ceab0c41e932d383bead27e30f
expression_opened = false
TF_activity_scored = false
scientific_disposition = NO_NATURALLY_PRIVILEGED_COMPACT_2_TO_5D_GRAPH_BASIS
```

### B6. Closure-head deterministic CI

```text
workflow = GRI_v2_tests
workflow_run = 34798656672
conclusion = success
scientific_role = VALIDATION_CI_NOT_BIOLOGICAL_EVIDENCE
```

Obsolete mechanical orphan recorded by the closure file:

```text
workflow_run = 34749223154
commit = 92c36323c4c4cb6c0a5bb12d92c5dd625739d811
role = SUPERSEDED_MECHANICAL_ORPHAN
scientific_evidence = NONE
```

Do not treat that orphan as an incomplete scientific result.

## C. G1 restoration R0 lineage

Current workflow:

`.github/workflows/gri-v2-chi-bio-g1-restoration-r0-embedding-preflight.yml`

Current workflow contract pins the chronic G2 source identity before the R0 embedding/preflight can operate. The workflow references:

```text
source_chronic_g2_run = 34769901215
source_chronic_g2_artifact = 10321342847
```

The workflow also contains an **expected downloaded-source digest**:

```text
expected_source_digest_in_R0_workflow = 57f886283851756b7ee1066725fe194a203333daa8a626f688fe28b2a8d6012
```

This value is intentionally **not equated** here with the closure record's packaged artifact SHA-256 `4ad76198657c...`. They are recorded as distinct digest roles until the exact object hashed by each field is reconciled. Similar-looking hash fields must not be merged by assumption.

### R0 current provenance gap

The current provenance layer does not yet record a verified completed R0 scientific result run/artifact. If a later R0 run exists, add it only after verifying its workflow run, artifact ID/name, commit, result status, and hashes from live GitHub/runtime output or its frozen result artifact.

## D. External source-audit provenance

The following current source-audit files are **P0-D qualification artifacts**, not confirmatory biological results:

- `GRI_BREAST_PAIRED_EXTERNAL_IDENTITY_AUDIT_P0D_20260911.md`
- `GRI_CARE_IDH_LONGITUDINAL_MULTIOMIC_SOURCE_AUDIT_P0D_20260911.md`
- `GRI_CGGA_CCELL4083_MODALITY_AUDIT_P0D_20260911.md`
- `GRI_IDH_GLIOMA_DUAL_CAPTURE_LONGITUDINAL_SOURCE_AUDIT_P0D_20260911.md`
- `GRI_MELANOMA_MAPKI_EXTERNAL_IDENTITY_AUDIT_P0D_20260911.md`
- `GRI_PROSTATE_EXTERNAL_IDENTITY_AUDIT_P0D_20260911.md`
- `GRI_HNSCC_CETUXIMAB_TIMECOURSE_SOURCE_AUDIT_P0D_20260912.md`
- `GRI_HNSCC_SHORTTERM_CETUXIMAB_TIMECOURSE_SOURCE_AUDIT_P0D_20260912.md`
- `GRI_HNSCC_DAY5_ATAC_SUBSTRATE_SOURCE_AUDIT_P0D_20260912.md`

Their evidentiary role is source identity, order, modality, access, and leakage qualification. A source-audit markdown file cannot be cited as though the GRI Engine has already produced a biological result on that external cohort.

## E. Current architecture/control provenance

Important current machine/human-readable controls include:

- `../config/gri_Chi_bio_ABC_architecture_freeze_20260913_v0_1.json`
- `../config/gri_Chi_bio_admission_cycle_closure_20260913_v1.json`
- `../src/chi_bio_abc_architecture_contract.py`
- the relevant G2/B3/R0 freeze/config files and regression tests;
- `GRI_CHI_BIO_AI_WORKSTATE_CLOSED_20260913.md`;
- `../docs/GRI_CHI_BIO_ADMISSION_CYCLE_CLOSURE_20260913.md`.

A current prose summary may point to these controls. It does not supersede the machine record or frozen output it summarizes.

## F. Manuscript provenance layer

Current manuscript-control files:

- `../manuscript/LIVING_MANUSCRIPT_DRAFT.md`
- `../manuscript/MANUSCRIPT_RECONCILIATION_LEDGER.md`
- `../manuscript/README.md`
- `../manuscript/sections/06_G1_RESTORATION_IDENTIFIABILITY.md`
- `../notes/CURRENT_STATUS_20260916_GOM_V080.md`
- `../docs/GRI_FUNCTION_LIMIT_EVIDENCE_MAP_20260916.md`

These are **narrative/reconciliation artifacts**. They are not primary evidence for a numerical result. Final manuscript numbers and figures must trace through them to a frozen evidence object.

## G. Verification-gap ledger

| Gap | Current status | Mechanical next step | Scientific effect if unresolved |
| --- | --- | --- | --- |
| exact current R0 completed-run identity, if any | UNVERIFIED IN THIS MAP | inspect live run/result state and add only verified identifiers | none until an R0 result is claimed |
| R0 expected-source-digest role vs closure artifact SHA role | DISTINCT_HASH_ROLES, EXACT OBJECT MAPPING PENDING | inspect workflow/downloaded object and closure hashing procedure | prevents accidental false hash mismatch/equivalence claim |
| exact Stage C1/post-C1 manuscript numeric provenance | HISTORICAL ARCHIVES AVAILABLE, LINE-BY-LINE RECONCILIATION PENDING | extract only from frozen archives/registries | blocks final numerical manuscript freeze, not current qualitative drafting |
| exact crosswalks for several external candidate datasets | SOURCE-SPECIFIC GAPS RECORDED | complete deterministic identity/access work without opening GRI outcomes | blocks P1 readiness/transport claims |
| final figure input hashes | NOT YET BUILT | attach figure-generation inputs/commit/hash during rebuild | blocks final figure release only |
| final reference/citation metadata | NOT FINAL | primary-source verification at manuscript freeze | blocks publication polish, not current science |

## H. Cold-audit rule

For each final manuscript claim, a cold auditor should be able to trace:

`claim -> manuscript ledger -> frozen result/protocol -> run/artifact/source identity -> code/config/freeze -> uncertainty/refusal rule`.

If that chain cannot be reconstructed, the claim stays below final-release status even if the prose is already drafted.
