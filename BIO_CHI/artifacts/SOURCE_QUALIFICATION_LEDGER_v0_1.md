# Bio Chi source qualification ledger v0.1

**Date:** 22 September 2026  
**Status:** ACTIVE / OUTCOME-BLIND SOURCE QUALIFICATION  
**Rule:** source qualification establishes identity and reproducibility only. It does not promote a biological result.

## Verified public source records

### Rehman et al. 2021 — colorectal diapause-like DTP

- GEO: **GSE145356**
- GEO status: public.
- Organism: Homo sapiens.
- Design includes vehicle, DTP-state, regrowth, and resistant samples.
- Samples: 25.
- BioProject: PRJNA606811.
- SRA study: **SRP249585**.
- Processed merged HTSeq read-count file is available from the GEO Series record.
- Raw sequencing is available through SRA.
- WES accession reported by the paper: EGAS00001004773. Controlled-access handling must be audited separately.

**Source disposition:** PUBLIC RNA EXECUTION FEASIBLE. Barcode/WES components require separate source-path audit.

### Marsolier et al. 2022 — H3K27me3 chemotolerance

- GEO SuperSeries: **GSE164716**
- GEO status: public.
- Organism: Homo sapiens.
- Samples: 100.
- Public subseries include:
  - GSE164385 scChIP-seq
  - GSE164409 ChIP-seq
  - GSE164715 scRNA-seq
  - GSE186965 ChIP-reChIP
  - GSE186966 CUT&Tag
  - GSE196764 WES
- GEO raw archive: GSE164716_RAW.tar, approximately 13.2 GB at current record.
- Public analysis code:
  - vallotlab/ChemoPersistance
  - TeamPerie/lentiviral_barcode_detection_in10X_data
- Published code release v1.0.0 is archived on Zenodo, DOI 10.5281/zenodo.6010802.

**Source disposition:** STRONG PUBLIC MULTIOMIC/CARRIER CANDIDATE. Exact primary files and minimal reproducible subset still need freezing before analysis.

### Harmange et al. 2023 — scMemorySeq

- GEO: **GSE237228**
- GEO status: public.
- Organism: Homo sapiens.
- Experiment types include high-throughput expression profiling and genome binding/occupancy profiling.
- Samples: 22.
- Series contains untreated and treatment-effect scRNA-seq records and associated chromatin-accessibility data.

**Source disposition:** PUBLIC LINEAGE/MEMORY CANDIDATE. Exact barcode/scRNA/ATAC file map must be frozen before execution.

### Shaffer et al. 2017 — rare-cell priming and resistance

- GEO SuperSeries: **GSE97682**
- GEO status: public.
- Organism: Homo sapiens.
- Samples: 155.
- Experiment types include RNA-seq and chromatin/occupancy profiling.
- Public raw and processed series material is available from GEO.
- Historical paper-level SRA lineage must be reconciled to the current GEO/BioProject record before scripts are frozen.

**Source disposition:** PUBLIC RECOVERY/REORGANIZATION BOUNDARY CANDIDATE.

### Srivatsan et al. 2020 — sci-Plex

- GEO: **GSE139944**
- BioProject: PRJNA587707.
- SRA study: SRP228591.
- Public raw and processed data available.
- Primary design has perturbation response without washout/recovery.

**Source disposition:** PUBLIC RESPONSE-SURFACE NEGATIVE CONTROL. Must refuse recovery claims by design.

### Lee et al. 2014 — paclitaxel tolerance

- Paper reports SRA accession **SRP040309**.
- Public-source verification of the exact run/file map remains pending.

**Source disposition:** ACCESSION REPORTED / SOURCE MAP PENDING.

## Scalar/model-track source qualification

### Jaruszewicz-Błońska et al. 2023 — identifiable NF-κB model

- DOI: 10.1371/journal.pone.0286416.
- Open-access PLOS ONE / PMC article.
- Reduced six-variable ODE model.
- Article states computer codes for original/reduced models are supplied as S1 Code.
- The model includes an on-off TNF protocol used for identifiability analysis.
- It is a model-identifiability candidate, not by itself a biological χ admission.

**Source disposition:** EXECUTABLE MODEL QUALIFICATION CANDIDATE.

### Son et al. 2021 — dynamic NF-κB

- DOI: 10.1126/scisignal.aaz4382.
- Dense single-cell trajectories described in the article.
- Paper states single-cell trace data are available upon request rather than an immediately verified public repository.

**Source disposition:** SCIENTIFICALLY STRONG / ACCESS RISK.

### Blum et al. 2019 — temporal ERK/MAPK perturbation

- Public model/inference code reported at `Mijan/LFNS_MSB`.
- Raw single-cell data acquisition path remains to be verified.

**Source disposition:** MODEL/CODE ACCESSIBLE / RAW DATA AUDIT PENDING.

### Geva-Zatorsky et al. 2006 — p53/Mdm2

- DOI: 10.1038/msb4100068.
- Supplementary movies/data support long single-cell time series.
- Modern machine-readable raw-data availability remains to be audited.
- Sustained single-cell oscillations make this an important anti-damping / representation-limit case.

**Source disposition:** LIMIT-CASE CANDIDATE, NOT PRIMARY RECOVERY.

## Unresolved high-priority sources

1. **Su sequential transcriptional-wave / hysteresis melanoma study**
   - exact public accession and canonical publication identity must be resolved before promotion.
2. **Jiang et al. 2020 yeast stress-memory**
   - paper is open access; exact downloadable single-cell trace/source package remains unverified.
3. **Sharma et al. 2010 PC9 DTP/DTEP**
   - recovery figures are strong, but machine-readable public source availability must be established.
4. **Harmange barcode mapping**
   - exact lineage-barcode files and relationship to GEO sample records must be mapped.

## Next mechanical source tasks

- enumerate files and checksums for GSE145356, GSE164716, GSE237228, and GSE97682;
- freeze a minimal downloadable subset for each candidate without opening new target outcomes;
- identify licenses/redistribution constraints;
- resolve exact Su study identity/accession;
- verify Jiang and Sharma reusable-data availability;
- map Jaruszewicz S1 Code to a pinned repository-local test fixture or source hash;
- record all source identities in machine-readable manifests before any newly designed analysis opens target outcomes.
