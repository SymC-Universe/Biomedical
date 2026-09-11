# GRI external Atlas / validation dataset candidate inventory

**Date:** 2026-09-10  
**Status:** P0-D SOURCE DISCOVERY ONLY  
**Not a cohort selection or P1 freeze.**  
**Protocol authority:** General Cross-Project Research Protocol v0.7.1 + v0.7.1A

## Purpose

Identify external data families that may eventually populate the Regulatory Substrate Atlas, support Function/Limit mapping, or serve as untouched/independent validation candidates.

Discovery does not mean selection. No candidate is chosen because it is expected to agree with GRI. Final P1 cohort selection, comparator, inclusion rules, and decision rule require a separate frozen MFR-14 process before decisive outcomes are opened.

Retrieval date for sources below: 2026-09-10.

## Candidate A: external lung adenocarcinoma methylation + expression cohort

### Source of record

- NCBI GEO methylation series: `GSE66836`
  - https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE66836
- NCBI GEO expression series: `GSE66863`
  - https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE66863
- NCBI BioProject: `PRJNA278125`
  - https://www.ncbi.nlm.nih.gov/bioproject/278125

### Verified source facts

The methylation GEO record describes:

- 164 lung adenocarcinoma tumors;
- 19 matched normal lung samples;
- Illumina Infinium HumanMethylation450 methylation.

The expression companion `GSE66863` contains 121 lung adenocarcinoma tumor samples measured on the Agilent 60K mRNA expression array. GEO explicitly states that the expression sample numbers are matched between `GSE66836` and `GSE66863`.

Therefore the currently source-verified paired cross-omic tumor subset is **121**, not all 164 methylation tumors. The additional methylation tumors and 19 matched normal lung samples remain useful methylation/reference context but are not assumed to possess matched expression.

### Potential role

- `NOMINAL_FUNCTION`: high-priority external single-cancer static cross-omic architecture cohort;
- `PERTURBED_FUNCTION`: possible smoking/mutation-defined context comparisons, subject to independent prespecification;
- external expression-platform transfer because expression is microarray-based rather than TCGA RNA-seq;
- normal-tissue methylation context from the 19 matched-normal samples, without assuming paired expression for those normals.

### Independence notes

Potentially independent from TCGA at data/cohort/source level. It is particularly useful because the original study used TCGA as an independent validation cohort for its own prognostic signature, not as the source of these 121 paired tumor measurements. Any use of the same Hallmark definitions/transformations is method overlap, not automatically data dependence.

### Current state

`CANDIDATE_HIGH_PRIORITY_STATIC_EXTERNAL`

`PAIRED_CROSS_OMIC_TUMORS_SOURCE_VERIFIED = 121`

No outcome values have been used here to select favorable GRI performance.

---

## Candidate B: CGGA CCell_4083 multi-omics glioma cohort

### Source of record

CGGA download portal:

- https://www.cgga.org.cn/download.jsp

### Verified source facts

The current CGGA portal lists dataset `CCell_4083` as:

- data type: Multi-omics;
- 35 samples;
- Methylation_EPIC;
- RNA-seq;
- 10X scRNA-seq;
- phosphoproteomics;
- proteomics;
- matched clinical-data download is listed on the same dataset block.

### Potential role

- `NOMINAL_FUNCTION`: independent glioma multi-omic architecture;
- cross-modality Atlas test because methylation, RNA, protein/phosphoprotein, and single-cell layers are listed for one named multi-omics dataset;
- candidate test of whether current System Model output transfers outside TCGA and across platform.

### Independence notes

CGGA is an external Chinese glioma resource distinct from TCGA. Exact per-sample overlap across the listed modalities must still be verified from downloaded manifests/sample identifiers rather than inferred solely from the portal's overall `35 samples` label.

### Current state

`CANDIDATE_HIGH_PRIORITY_MULTIOMIC_EXTERNAL`

`EXACT_MODALITY_OVERLAP = TO_BE_VERIFIED`

---

## Candidate C: CGGA legacy glioma methylation / expression resources

### Source of record

CGGA portal:

- https://www.cgga.org.cn/
- https://www.cgga.org.cn/download.jsp

### Verified source facts

The portal separately lists:

- `methyl_159`: 159 samples, Illumina HumanMethylation27;
- `mRNA-array_301`: 301 samples, Agilent whole-human-genome array;
- RNA-seq cohorts of 325 and 693 samples;
- primary/recurrent LGG and GBM categories in the CGGA resource.

### Potential role

- external static Atlas context;
- possible `PERTURBED_FUNCTION` / `BOUNDARY_OR_TRANSITION` research role through primary-versus-recurrent status if exact matched/appropriate independence can be established;
- platform robustness because methylation 27K differs from current merged TCGA 27K/450K handling.

### Critical gap

The public portal summary does **not** establish how many patients have both methylation and the specific expression modality needed for cross-layer GRI analysis. That overlap must be computed from source identifiers before this can be treated as a paired validation cohort.

### Current state

`CANDIDATE_MEDIUM_PRIORITY_PENDING_OVERLAP_AUDIT`

---

## Candidate D: colorectal primary-to-liver-metastasis paired multi-omic series

### Source of record

NCBI GEO:

- `GSE213402`
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE213402

### Verified source facts

The GEO record states:

- 20 samples;
- paired primary cancer and liver metastases from 10 colorectal cancer patients;
- RRBS methylation;
- RNA-seq expression.

### Potential role

This is too small for simply importing the current n=30 per-cancer C1 design, but is scientifically valuable as a P0-D **paired-state / perturbation-like natural progression context**.

Potential roles:

- `PERTURBED_FUNCTION`;
- candidate architecture reorganization mapping from primary to metastatic state;
- hypothesis generation for future system-level preservation/reorganization tests.

### Current state

`P0_D_PERTURBED_FUNCTION_CANDIDATE_SMALL_N`

It cannot independently confirm a rule developed from itself.

---

## Candidate E: acquired ALK-inhibitor resistance multi-omic cell-line series

### Sources of record

NCBI GEO SuperSeries / subseries:

- `GSE139388`
- `GSE139387`
- `GSE179326`

Representative SuperSeries:

- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE139388

### Verified source facts

The GEO records describe an H3122 ALK-positive lung cancer cell model with parental versus acquired ceritinib-resistant states, including 450K DNA methylation and RNA expression/single-cell RNA-related subseries.

### Potential role

- `PERTURBED_FUNCTION` P0-D mechanism/response mapping;
- controlled acquired-resistance reorganization;
- possible future qualification of whether the Engine distinguishes ordinary shared structure from treatment-driven restructuring.

### Limit

Very small biological-system count and cell-line context. It is not a representative patient cohort and does not satisfy a broad external cancer-validation task.

### Current state

`P0_D_MECHANISM_TESTBED_NOT_EXTERNAL_POPULATION_VALIDATION`

---

## Candidate F: prostate tumor / adjacent-tissue paired study family

### Sources of record

NCBI GEO methylation series:

- `GSE262522`
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE262522

NCBI GEO RNA-seq companion:

- `GSE237995`
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE237995

NCBI RNA BioProject:

- `PRJNA997353`
- https://www.ncbi.nlm.nih.gov/bioproject/PRJNA997353

### Verified source facts

Both GEO series carry the same study title: `Race-specific coregulatory and transcriptomic profiles associated with DNA methylation and androgen receptor in prostate cancer`, with `GSE262522` identified as the m450K methylation series and `GSE237995` as the RNA-seq series.

The RNA BioProject states an overall design of:

- 58 African American samples: 31 tumors + 27 adjacent tissue;
- 63 European American samples: 31 tumors + 32 adjacent tissue;
- total 121 RNA BioSamples / 121 SRA experiments.

The methylation series provides 450K IDAT/raw and processed functional-normalization matrices. Individual methylation and RNA GEO samples use the same participant-style naming convention, for example `PT-..._T_AA` / adjacent-tissue forms, but exact one-to-one overlap across all 121 samples has **not yet been computed** in this audit and is therefore not assumed.

### Potential role

- high-priority external `NOMINAL_FUNCTION` cross-omic prostate architecture candidate;
- tumor-versus-adjacent context;
- population/context robustness research across the prespecified study groups;
- cross-platform transfer relative to TCGA processing.

### Current state

`CANDIDATE_HIGH_PRIORITY_STATIC_EXTERNAL_PENDING_EXACT_ID_OVERLAP`

`EXPRESSION_COMPANION = GSE237995_VERIFIED`

`RNA_SAMPLE_COUNT = 121_SOURCE_VERIFIED`

---

## Candidate G: ICGC ARGO program family

### Sources of record

- ARGO platform: https://platform.icgc-argo.org/
- retired ICGC 25K portal notice: https://dcc.icgc.org/

### Verified source facts

The ICGC ARGO platform currently provides controlled clinical/molecular data across multiple international cancer programs. Access to controlled molecular data requires approval.

### Potential role

- source family for materially external cohort/system validation;
- multi-cancer transfer/generalization if required modalities are available;
- possible prospective/longitudinal clinical context depending on program.

### Current gap

This audit has **not** established that a selected ARGO program contains the exact paired methylation+RNA modalities required for the current GRI Engine task. It is a source-family lead, not an admitted dataset.

### Current state

`SOURCE_FAMILY_LEAD_ACCESS_AND_MODALITY_AUDIT_REQUIRED`

---

# Initial priority by research purpose

This ranking is by **data architecture and research role**, not by agreement with GRI results.

### Static external cross-layer validation candidates

1. `GSE66836 + GSE66863` lung adenocarcinoma: 121 source-declared matched tumor expression/methylation sample numbers; 450K methylation plus Agilent expression; larger methylation-only context also available.
2. `GSE262522 + GSE237995` prostate study family: 450K methylation plus RNA-seq, 121 RNA samples under a common study design; exact one-to-one cross-modality ID overlap still requires verification.
3. `CGGA CCell_4083`: 35-sample multi-omics dataset with EPIC methylation + RNA-seq + proteomics/phosphoproteomics + scRNA-seq listed; exact modality overlap still requires verification.
4. CGGA legacy methylation/expression families: large enough individually, but exact paired overlap unresolved.

### Function/perturbation mapping candidates

1. `GSE213402`: paired primary/metastatic colorectal samples, useful architecture for P0-D state-change mapping but n=20 total.
2. `GSE139388` family: acquired drug-resistance cell-line perturbation, mechanistically useful but not population validation.
3. CGGA primary/recurrent categories: potentially useful if pairing/temporal relationship is source-verified.

### Rare-natural-limit candidates

**NONE ADMITTED.**

No candidate above is promoted to `RARE_NATURAL_TESTBED` without a domain-native rarity criterion, authenticity/confounding gate, base-rate context, and outcome-independent selection route.

# Next source-discovery actions

Safe P0-D actions:

1. retain the source-verified 121 matched lung tumor subset as a high-priority candidate without evaluating GRI outcomes;
2. compute/verify exact ID overlap for `GSE262522/GSE237995` before calling it a paired 121-sample cohort;
3. inspect `CCell_4083` downloadable manifests for exact modality overlap and raw/processed availability;
4. determine paired overlap between CGGA `methyl_159` and each expression cohort;
5. inventory whether selected ARGO programs actually provide paired methylation + expression;
6. search for larger paired longitudinal/perturbational patient cohorts;
7. preserve candidates that fail overlap/access criteria rather than replacing them silently.

**No external P1 dataset has been chosen or opened for decisive GRI evaluation by this discovery record.**