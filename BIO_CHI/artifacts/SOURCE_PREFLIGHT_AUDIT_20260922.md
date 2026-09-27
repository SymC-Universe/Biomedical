# Bio Chi source preflight audit — 22 September 2026

**Status:** PASS  
**Outcome opening:** FALSE  
**Branch:** `chi-bio-recovery-p0d-20260922`

## Source endpoint preflight

Workflow:
- name: `Bio Chi source preflight`
- run: **35810054670**
- conclusion: **success**
- head commit: `e2290062d1ba2677b2bdb493544ec512d333e6e3`

Artifact:
- name: `BIO_CHI_SOURCE_PREFLIGHT_V01`
- artifact ID: **10729701313**
- digest: `sha256:cb3224e9b457896de257a3bbd93d7a4c8c2a7def2f0ab9d6d7971f1a65db063d`

Generated manifest:
- source-manifest SHA-256: `286fab67787fe92f62c2747e90545d91232145d48d3d331b97af1adc0971ed82`
- failures: **0**
- biological outcomes opened: **false**

Verified direct files:
- Rehman GSE145356 merged HTSeq counts:
  - 1,191,595 bytes
  - last-modified 14 Feb 2020
- Rehman GSE145356 raw supplementary TAR:
  - 5,847,040 bytes
  - last-modified 8 Jan 2021
- Marsolier GSE164716 raw supplementary TAR:
  - 14,151,997,440 bytes
  - last-modified 1 Feb 2024

Landing pages for GSE145356, GSE164716, GSE237228, GSE97682, GSE255671, and the identifiable NF-kB paper all returned successfully.

## GEO metadata-only audit

Workflow:
- name: `Bio Chi GEO metadata audit`
- run: **35810202024**
- conclusion: **success**
- head commit: `20c65d8e869c002ac97fdd84bc15c2f83bc83497`

Artifact:
- name: `BIO_CHI_GEO_METADATA_AUDIT_V01`
- artifact ID: **10729531884**
- digest: `sha256:b625e3b92c01692d566e4134175f803646f1e46fd8aefa78171105617bcc28d4`

### Su 2026 / GSE255671

Metadata source:
- `GSE255671_family.soft.gz`
- SHA-256: `558cc094375f27af9c786f4bb12da1e86b228129203691d3b5cdd38c6214cd4c`
- compressed size: 14,990 bytes

Expected candidate-subset samples: **37**  
Found: **37**  
Missing: **0**

The audit confirms the declared M397 ordered RNA series:
- baseline Day 0;
- drug-on Days 3, 8, 13, 21, 29, 33, 38, 59;
- drug removal after 29 days followed by Days 4, 10, 15, 17, 30, 35.

It also confirms the declared ATAC and H3K4me3/H3K27ac baseline, early-treatment, late-treatment, and drug-removal anchors, plus RelA ChIP anchors.

No molecular values were opened.

### Rehman 2021 / GSE145356

Metadata source:
- `GSE145356_family.soft.gz`
- SHA-256: `1a39c3472db263c4c32964bb9467e5842bf6f70992ed3c98ef17884893522fb0`
- compressed size: 4,224 bytes

Expected samples: **25**  
Found: **25**  
Missing: **0**

Metadata confirms:
- saline controls, 8 weeks;
- DMSO controls, 8 weeks;
- 5-FU/LV, 8 weeks;
- CPT-11 regrowth, 8-week treatment lineage;
- FOLFIRI regrowth, 8-week treatment lineage;
- CPT-11 resistant, 7 months;
- CPT-11, 8 weeks.

No molecular values were opened.

## Scientific consequence

This audit establishes source identity and time/state ordering only. It does **not**:
- select a winning Bio Chi hypothesis;
- define a recovery metric;
- define χ_bio;
- define Χ_bio modal rank;
- define a Bio Chi conglomerate score;
- inspect expression/chromatin outcome values.

The next scientific analysis must be separately frozen before those target values are opened for the new Bio Chi questions.
