# BioSystems TN-C0 tumor-normal eligibility audit - 22 September 2026

**Status:** CLOSED / PASS  
**Evidence class:** metadata-only source and eligibility gate  
**Biological outcome status:** SEALED; no molecular values read  
**Frozen design:** `BIOSYSTEMS_TUMOR_NORMAL_CONTROL_FREEZE_20260922.md`  
**Frozen eligibility config:** `../config/biosystems_tn_c0_eligibility_v1.json`

## Result

TN-C0 successfully inventoried the exact TCGA sample headers and quality annotation without reading expression or methylation matrix values.

The firewall test passed using quoted TCGA headers and sentinel molecular strings that are required to remain absent from the output.

The final metadata run was GitHub Actions run `35784202933` at commit `52599f2521df4819bd5cbaa21372a8f45713f04a`.

### Exact source counts

- RNA header: 11,069 parsed TCGA samples.
- RNA sample type 01: 9,702 unique primary-tumor participants after raw header parsing; quality-filtered cancer mapping is shown below.
- RNA sample type 11: 737 unique Solid Tissue Normal participants in the raw source header.
- Methylation header: 12,039 parsed TCGA samples.
- Methylation sample type 01: 10,268 unique primary-tumor participants in the raw source header.
- Methylation sample type 11: 1,066 unique Solid Tissue Normal participants in the raw source header.

### Annotation/quality reconciliation

No source-header participant was genuinely missing cancer annotation after the discrepancy audit:

- RNA missing-annotation participants: **0**.
- Methylation missing-annotation participants: **0**.
- Annotation cancer conflicts: **0**.

All previously unmatched rows were explained by the pre-existing sample-quality `Do_not_use` exclusion:

- RNA: 136 type-01, 1 type-06, and 23 type-11 unique participants excluded.
- Methylation: 34 type-01 and 1 type-11 unique participants excluded.

The 23 quality-excluded RNA normals are distributed across BRCA (12), COAD (4), ESCA (1), KICH (1), KIRC (1), LUAD (2), LUSC (1), and PRAD (1). The single quality-excluded methylation normal is BRCA.

No eligibility threshold was changed after these counts were known.

## Frozen eligible sets

### TN-A1 RNA primary control, n = 30 per state

**12 cancers:**

`BRCA, COAD, HNSC, KIRC, KIRP, LIHC, LUAD, LUSC, PRAD, STAD, THCA, UCEC`

Each has at least 30 quality-eligible unique type-01 RNA participants and at least 30 quality-eligible unique type-11 RNA participants.

### TN-C1 multiomic primary control, n = 30 RNA+methylation overlap per state

**5 cancers:**

`BRCA, LIHC, PRAD, THCA, UCEC`

Each has at least 30 quality-eligible unique participants represented in both RNA and methylation in the tumor state and at least 30 in both assays in the normal state.

### Paired RNA sensitivity, n >= 20 participants with both tissue states

**13 cancers:**

`BRCA, COAD, HNSC, KICH, KIRC, KIRP, LIHC, LUAD, LUSC, PRAD, STAD, THCA, UCEC`

KICH is paired-sensitivity eligible with 24 paired participants but is not eligible for the n=30 RNA primary control. This distinction is frozen and must not be blurred in reporting.

## Full cancer-level inventory

| Cancer | RNA T01 | RNA N11 | RNA TN paired | RNA n30 | RNA paired n20 | Meth T01 | Meth N11 | RNA+Meth T | RNA+Meth N | Multiomic n30 |
|---|---:|---:|---:|:---:|:---:|---:|---:|---:|---:|:---:|
| ACC | 78 | 0 | 0 | N | N | 79 | 0 | 78 | 0 | N |
| BLCA | 404 | 19 | 19 | N | N | 408 | 21 | 404 | 17 | N |
| BRCA | 1084 | 102 | 102 | Y | Y | 1069 | 111 | 1068 | 93 | Y |
| CESC | 301 | 3 | 3 | N | N | 303 | 3 | 301 | 3 | N |
| CHOL | 36 | 9 | 9 | N | N | 36 | 9 | 36 | 9 | N |
| COAD | 444 | 37 | 37 | Y | Y | 443 | 70 | 442 | 28 | N |
| DLBC | 48 | 0 | 0 | N | N | 48 | 0 | 48 | 0 | N |
| ESCA | 182 | 10 | 10 | N | N | 183 | 15 | 182 | 8 | N |
| GBM | 154 | 5 | 0 | N | N | 419 | 2 | 126 | 1 | N |
| HNSC | 514 | 44 | 43 | Y | Y | 522 | 50 | 514 | 20 | N |
| KICH | 65 | 24 | 24 | N | Y | 65 | 0 | 65 | 0 | N |
| KIRC | 515 | 71 | 71 | Y | Y | 516 | 344 | 514 | 23 | N |
| KIRP | 285 | 32 | 32 | Y | Y | 286 | 48 | 285 | 23 | N |
| LGG | 514 | 0 | 0 | N | N | 514 | 0 | 514 | 0 | N |
| LIHC | 369 | 50 | 50 | Y | Y | 374 | 50 | 368 | 41 | Y |
| LUAD | 510 | 57 | 56 | Y | Y | 573 | 52 | 508 | 20 | N |
| LUSC | 486 | 50 | 50 | Y | Y | 488 | 67 | 485 | 8 | N |
| MESO | 87 | 0 | 0 | N | N | 87 | 0 | 87 | 0 | N |
| OV | 302 | 0 | 0 | N | N | 589 | 12 | 302 | 0 | N |
| PAAD | 156 | 4 | 4 | N | N | 162 | 10 | 156 | 4 | N |
| PCPG | 178 | 3 | 3 | N | N | 178 | 3 | 178 | 3 | N |
| PRAD | 493 | 51 | 51 | Y | Y | 494 | 50 | 493 | 35 | Y |
| READ | 157 | 10 | 9 | N | N | 155 | 11 | 154 | 6 | N |
| SARC | 254 | 2 | 2 | N | N | 256 | 4 | 254 | 0 | N |
| SKCM | 103 | 1 | 0 | N | N | 104 | 2 | 103 | 1 | N |
| STAD | 412 | 35 | 32 | Y | Y | 440 | 27 | 412 | 0 | N |
| TGCT | 149 | 0 | 0 | N | N | 149 | 0 | 149 | 0 | N |
| THCA | 500 | 59 | 59 | Y | Y | 502 | 56 | 500 | 50 | Y |
| THYM | 120 | 2 | 2 | N | N | 124 | 2 | 120 | 2 | N |
| UCEC | 529 | 34 | 22 | Y | Y | 531 | 46 | 529 | 34 | Y |
| UCS | 57 | 0 | 0 | N | N | 57 | 0 | 57 | 0 | N |
| UVM | 80 | 0 | 0 | N | N | 80 | 0 | 80 | 0 | N |

## Duplicate/aliquot diagnostics

Raw headers contain no duplicate type-11 participants in either RNA or methylation.

For type 01:
- RNA has 4 participants represented more than once.
- Methylation has 43 participants represented more than once.

Eligibility is participant-level, so these do not inflate the counts above. Exact aliquot selection for biological execution must use deterministic source/quality rules and may not be chosen after viewing molecular outcomes.

## Provenance

- RNA source UUID: `3586c0da-64d0-4b74-a449-5ff4d9136611`.
- Methylation source UUID: `d82e2c44-89eb-43d9-b6d3-712732bf6a53`.
- Sample-quality annotation UUID: `1a7d7be8-675d-4e60-a105-19d4121bdebf`.
- Workflow run: `35784202933`.
- Artifact: `GRI_TUMOR_NORMAL_METADATA_INVENTORY_V01`, artifact ID `10719607059`.
- Artifact digest: `sha256:3ff9aa61654bd468041040a31c8dbda427fc7ca6b5ea6afd1af07f06a95ad3f8`.
- Inventory JSON SHA-256: `81d1e7c2089a8a4957593542df8628cf21cf976025161ee194974397c60eca6e`.
- RNA header SHA-256: `598c13309763ead5e347a772cabf51b7df4ba9a1eac87bcf4df56d803b065434`.
- Methylation header SHA-256: `932b1bc6155d522ade004ac0b7a4ed304b175615b7b7a397566884ba4a1c4e7c`.

## Claim ceiling

TN-C0 establishes only source identity, sample-type availability, quality-filtered cancer assignment, participant overlap and eligibility.

It does **not** establish:
- any tumor-normal molecular difference;
- tumor specificity;
- healthy-state architecture;
- methylation/RNA coupling differences;
- a biological chi or Chi state;
- causal or clinical meaning.

## Next authorized boundary

TN-C0 is closed.

The biological matrices remain outcome-sealed. The next stage is to bind TN-A1/TN-C1 execution to the frozen cancer sets, participant/aliquot rules, inherited Stage A/C1 constructions, deterministic resampling and prespecified outputs before reading type-11 molecular values.
