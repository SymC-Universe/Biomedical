# BioSystems submission provenance manifest - 22 September 2026

**Status:** ACTIVE / P1 RESULT FIELD PENDING  
**Purpose:** submission-specific source, code, config and evidence identity index.  
**Revision branch:** `gri-biosystems-revision-20260922`

## Core source identities

| Source | Identity |
|---|---|
| PanCan RNA EB++ | SHA-256 `674b19b7ed9ae4c5ef35ee2824936429aa5d46c0735a3d180f41552fcbbdb658`; 1,882,540,959 bytes |
| PanCan methylation HM27/HM450 merged | SHA-256 `5934c497882fbe8178d128a3a7f71e765480af6bbd460e0398de3428cd075b77`; 5,022,150,019 bytes |
| MSigDB Hallmark 2026.1.Hs raw GMT | SHA-256 `eecaf6dad908334ae885406ec72bdc0646d8917588ed7c219fac92fc5363f596` |
| Frozen Hallmark membership | SHA-256 `bc6a9a33d7421dc407d33a66859760ba25e47b2f398e1a43c9156f80c71b3900` |
| C1A annotation export | SHA-256 `a7f83233f97c3933752d74b8042e967de88df20eba2cf477a536136631a8da17` |
| C1A Chen cross-reactive ID export | SHA-256 `078e95716af2b20c3515f59d09310d20c3515f59d09310d20c3515f59d0931` **DO NOT USE: placeholder-length check intentionally fails; canonical identity is recovered from source artifact at execution** |
| C1 exact probe carrier | 22,601 unique probe IDs; reconstruction bound to run `33318029738` artifact `CSA_STAGE_C1A_PROBE_INVENTORY_WINDOWS_20260830` |
| Sample-quality annotation | GDC UUID `1a7d7be8-675d-4e60-a105-19d4121bdebf` |

> **Integrity note:** the Chen export hash is not copied manually into submission metadata from memory. The exact frozen source artifact is recovered and hash-checked by the execution workflow. Any manifest generated for final release must populate it from the machine record rather than this human-readable index.

## Completed tumor-normal evidence

### TN-C0 metadata-only gate
- run: `35784202933`
- commit: `52599f2521df4819bd5cbaa21372a8f45713f04a`
- artifact: `GRI_TUMOR_NORMAL_METADATA_INVENTORY_V01`
- artifact ID: `10719607059`
- digest: `sha256:3ff9aa61654bd468041040a31c8dbda427fc7ca6b5ea6afd1af07f06a95ad3f8`

### TN-A1 / TN-P20 RNA
- run: `35796888899`
- commit: `72232b72415fb7579da09a4711448166772f4712`
- artifact: `GRI_BIOSYSTEMS_TN_RNA_RESULTS_V01`
- artifact ID: `10724424893`
- digest: `sha256:b2a72fd5483ab47b61369df5f082188bcc9a2d4caca494d032e51e3f5e48029e`

### TN-C1 multiomic
- run: `35797400570`
- commit: `d02b94c43ec1c943d1137a4b1d1da1e690ca06fe`
- artifact: `GRI_BIOSYSTEMS_TN_C1_RESULTS_V01`
- artifact ID: `10725150891`
- digest: `sha256:17c23bc3e5d49d2c7936f6ac5357526fa8a3ed95933dd1d0257f028bf764cf3d`

## Independent external prostate P1 source identities

Source-only preflight:
- run `35801003396`
- head `6b40ddce2dd66b4401f74ba327ff34369b1361fc`
- artifact `GRI_BIOSYSTEMS_EXTERNAL_PROSTATE_P1_SOURCE_PREFLIGHT_V01`
- artifact ID `10725064779`
- digest `sha256:f77168c359135047d01dbd23b1f848e7929a0a2c0ce2a0254dee374c703aa7d1`
- GRI outcome opened: **false**

External molecular files:
- GSE237995 RNA raw counts: SHA-256 `9f94093f3254e1478d37f0b888d8f652e1d7bbf7f6265dd81f15d4d490f8cc92`; 5,443,862 bytes; 58,037 source rows.
- GSE262522 450K Funnorm beta: SHA-256 `90a7a8c12343831524a9711be7e0b3f33f297fe408662fa68c5efa49a7c862d0`; 290,009,723 bytes; 485,512 unique CpGs.
- GSE262524 EPIC Funnorm beta: SHA-256 `b55bf7b2e427c27e84a331c7f8c07f296dd64c07fa54c74445bb40288777e69f`; 414,961,637 bytes; 865,859 unique CpGs.

P1 scientific freeze:
- `BIOSYSTEMS_EXTERNAL_PROSTATE_P1_FREEZE_20260922.md`
- freeze commit `7c9e2c4367c5c0bc2eca9b6c2f265162b8fb044f`
- config commit `b06175746ec99da948385a21da9876581a9bb053`
- execution clarification final commit `807cf13b357b4156695839cc0d95fa128f1317c1`
- executor mechanical head before launch: `f8dccf37b142163b8ecdd060810232ab63e7c526`
- launch commit: `867e611c87545f09671a306cdce741f605496154`
- active workflow run: `35801487875`
- decisive result identity: **PENDING**

## Reviewer/governance identities

- tumor-normal protocol lineage audit: commit `3994ec6fb83673df3e387b2e4ee38f9c995fed45`
- TN-C1 biological audit: commit `baed983a21e4c0579983d3fc38bfa6048ffeb314`
- combined tumor-normal closeout: commit `4adcf399b417a3fe7a53ef5b4339908f7284a4b8`
- reviewer matrix normal-control closure: commit `cc22cd8e808c641e4e939c621a08c547c03486c1`
- resubmission closeout update: commit `f8bd0324d9153bbdb64ba3c81fc46c8325f2b2b1`
- revised non-claim ledger: `BIOSYSTEMS_REVISED_NONCLAIM_LEDGER_20260922.md`

## Private manuscript source

Current editable manuscript is intentionally outside the public repository:
`Atlas - GRI update v1/Private Working Manuscripts/Oncology/GRI_BioSystems_working_v5_2026-09-22.tex`

Final release must record the exact Library/exported byte hash of the manuscript source and final PDF after the external P1 result is incorporated and visual QA is complete.

## Release rule

This file is an index, not a substitute for machine-generated `SHA256SUMS`.

Before final resubmission:
1. replace the P1 pending field with the completed run/artifact/digest;
2. export the final private manuscript source;
3. generate machine hashes for manuscript, supplement, figures, tables, configs and response package;
4. cross-check every human-readable hash here against those machine records;
5. refuse release on any discrepancy.
