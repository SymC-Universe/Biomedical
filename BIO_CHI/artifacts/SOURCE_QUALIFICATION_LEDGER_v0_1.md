# Bio Chi source qualification ledger v0.1

**Date:** 23 September 2026  
**Status:** ACTIVE / OUTCOME-BLIND SOURCE QUALIFICATION  
**Rule:** source qualification establishes identity and reproducibility only. It does not promote a biological result.

## Frozen public-source map

The generic external-source freeze is pinned in `BIO_CHI/config/EXTERNAL_SOURCE_FREEZE_PIN_v0_1.json`. That record preserves exact file-map identities and available hashes for GSE145356, GSE164716, GSE237228, GSE97682, and GSE255671 without interpreting molecular values. Large files that exceeded the frozen hash ceiling remain explicitly deferred rather than implicitly treated as hashed.

## Verified public source records

### Rehman et al. 2021 — colorectal diapause-like DTP

- GEO: **GSE145356**.
- Organism: Homo sapiens.
- Design includes vehicle, DTP-state, regrowth, and resistant samples.
- Samples: 25.
- BioProject: PRJNA606811.
- SRA study: **SRP249585**.
- Processed merged HTSeq read-count material and raw sequencing paths are public.
- WES accession reported by the paper: EGAS00001004773. Controlled-access handling remains separate.

**Source disposition:** PUBLIC RNA EXECUTION FEASIBLE. Barcode/WES components require separate source-path audit.

### Marsolier et al. 2022 — H3K27me3 chemotolerance

- GEO SuperSeries: **GSE164716**.
- Public subseries include GSE164385, GSE164409, GSE164715, GSE186965, GSE186966, and GSE196764.
- Public analysis code includes `vallotlab/ChemoPersistance` and `TeamPerie/lentiviral_barcode_detection_in10X_data`.
- Published code release v1.0.0 is archived on Zenodo, DOI 10.5281/zenodo.6010802.

**Source disposition:** STRONG PUBLIC MULTIOMIC/CARRIER CANDIDATE. Minimal executable subset remains to be selected under the frozen eligibility contract, not by target result.

### Harmange et al. 2023 — scMemorySeq

- GEO: **GSE237228**.
- Public series contains expression and chromatin-accessibility material; exact GEO file identities are now captured by the external-source freeze.

**Source disposition:** PUBLIC LINEAGE/MEMORY CANDIDATE. Exact lineage-barcode-to-sample mapping remains a Q2 task.

### Shaffer et al. 2017 — rare-cell priming and resistance

- GEO SuperSeries: **GSE97682**.
- Public raw/processed series material is captured by the external-source freeze.
- Historical paper-level SRA lineage still requires exact reconciliation before an execution script is frozen.

**Source disposition:** PUBLIC RECOVERY/REORGANIZATION BOUNDARY CANDIDATE.

### Srivatsan et al. 2020 — sci-Plex

- GEO: **GSE139944**; BioProject PRJNA587707; SRA SRP228591.
- Primary design is perturbation response without washout/recovery.

**Source disposition:** PUBLIC RESPONSE-SURFACE NEGATIVE CONTROL. Recovery claims must be refused by design.

### Lee et al. 2014 — paclitaxel tolerance

- Paper reports SRA accession **SRP040309**.
- Exact run/file map remains pending.

**Source disposition:** ACCESSION REPORTED / SOURCE MAP PENDING.

## Scalar/model-track and known-truth source qualification

### Jaruszewicz-Błońska et al. 2023 — identifiable NF-κB model

- DOI: 10.1371/journal.pone.0286416.
- Reduced six-variable ODE source is supplied as S1 Code and is hash-pinned in the Bio Chi source freeze.
- Native source reproduction, Figure-8 execution, local-stability work, all-mode inventory, and full-state coordinate control are tracked separately in machine-readable pins.
- This executable model remains a model-identifiability candidate; it is not by itself a biological `chi_bio` admission.

**Source disposition:** EXECUTABLE MODEL QUALIFICATION PATH ACTIVE. Primary biological observability/identifiability remains a separate Q2/Q3 gate.

### Son et al. 2021 — dynamic NF-κB

- DOI: 10.1126/scisignal.aaz4382.
- Full-text source audit confirms dense single-cell stimulation/recovery timing, but the primary single-cell trace data are stated to be available **upon request**.
- Custom MATLAB control/analysis software is described; no stable public repository was established by the targeted audit.

**Source disposition:** SCIENTIFICALLY STRONG / REPRODUCIBILITY ACCESS RISK. Do not treat the trajectories as public-downloadable.

### Jiang et al. 2020 — yeast stress memory

- DOI: 10.1126/scisignal.aay3585; PMCID: PMC7302112.
- Article and supplementary material are public; the paper states data needed for its conclusions are in the article/supplement.
- The targeted full-text audit did not establish a standalone public raw single-cell trajectory repository or accession.
- Custom MATLAB code is stated to be available upon request.

**Source disposition:** STRONG KNOWN-TRUTH DESIGN / RAW-TRACE EXECUTION ACCESS NOT YET CLOSED. Public article/supplement is not equivalent to a frozen raw trajectory package.

### Blum et al. 2019 — temporal ERK/MAPK perturbation

- DOI: 10.15252/msb.20198947.
- Publication date: 19 November 2019; article is open access under CC BY 4.0.
- The article's data-availability section states that CellProfiler pipelines are supplied as Code EV1 and that the inference source, model files, and inference results are public at `Mijan/LFNS_MSB`.
- Article supplementary resources include source-data ZIPs for Figures 1–5, Code EV1, and CP pipelines.
- Public model/inference repository `Mijan/LFNS_MSB` is pinned outcome-blind at branch `MSB_version`, commit `5c917abda0618d75c00c9cab45f24ed893dd71f1`, tree `cbb79d66f79a84bc8af28ca85f1678295348da83` in `BIO_CHI/config/BLUM2019_PUBLIC_SOURCE_PIN_v0_1.json`.
- A separate public processed dataset is now identified at **Mendeley Data DOI 10.17632/ccnxn84w8z.2**, Version 2, published 13 May 2020. The repository lists `data.zip` at **7.97 MB**, contributors Maciej Dobrzynski and Yannick Blum, and **CC BY 4.0** licensing. Identity is pinned in `BIO_CHI/config/BLUM2019_MENDELEY_DATA_PIN_v0_1.json` before archive inspection.
- Native population comparison uses the Jeffries-Matusita distance.
- Short temporal perturbations with washout/recovery are described in the publication.
- Direct `data.zip` endpoint and archive SHA-256 are **not yet frozen**; no hash is claimed.
- Raw microscopy public-download status is not inferred from the processed-data deposit.

**Source disposition:** PUBLIC VERSIONED PROCESSED DATA + PUBLIC MODEL/INFERENCE SOURCE QUALIFIED. DIRECT ARCHIVE ENDPOINT/HASH PENDING. Candidate status is unchanged; no result-based promotion has occurred.

### Geva-Zatorsky et al. 2006 — p53/Mdm2

- DOI: 10.1038/msb4100068.
- Supplementary movies/data support long single-cell time series.
- Modern machine-readable raw-data availability remains to be audited.
- Sustained single-cell oscillations make this an important anti-damping / representation-limit case.

**Source disposition:** LIMIT-CASE CANDIDATE, NOT PRIMARY RECOVERY.

## Verified hysteresis/reorganization source

### Su et al. 2026 — sequential transcriptional waves and NF-κB-driven chromatin remodeling

- Nature Communications 17, 3228 (2026), DOI **10.1038/s41467-026-71349-4**.
- GEO **GSE255671**; BioProject **PRJNA1076128**; additional longitudinal sources GSE65186, EGAS00001000992, and E-MTAB-5493.
- Public analysis/modeling code: `jihoonlee0/melanoma_reversible_transition`; archived release DOI **10.5281/zenodo.17751601**.
- Study includes oncogene inhibition followed by release and a reported hysteretic forward/reverse trajectory.
- GSE255671 exact public file-map identity is captured by the external-source freeze.

**Source disposition:** STRONG PUBLIC HYSTERESIS/REORGANIZATION CANDIDATE. Minimal execution subset must still be frozen before outcome opening.

## Preserved unresolved/source-limited cases

1. **Sharma et al. 2010 PC9 DTP/DTEP**
   - DOI 10.1016/j.cell.2010.02.027; PMCID PMC2851638.
   - Public original article documents drug-free reversal/resensitization.
   - Reproducibility Project: Cancer Biology registered a detailed replication protocol, DOI 10.7554/eLife.09462.
   - No modern standalone machine-readable raw dataset for the original 2010 study was established by targeted search.
   - **Disposition: STRONG BIOLOGICAL RECOVERY REFERENCE / ORIGINAL RAW DATA UNVERIFIED.**
2. **Harmange lineage-barcode mapping**
   - Exact lineage-barcode files and their mapping to GEO sample records remain to be closed.
3. **Jiang raw single-cell trajectories**
   - Public paper/supplement confirmed; standalone raw trace package remains unverified.
4. **Son NF-κB primary trajectories**
   - Explicitly upon request; not a public-download execution path at present.

## Next mechanical source tasks

- freeze the exact downloadable endpoint and SHA-256 of Blum Mendeley `data.zip` without interpreting archive contents; then inventory only schema/file identities before any native-metric execution;
- continue exact lineage/carrier mapping for Harmange and other carrier-qualified candidates;
- reconcile Shaffer SRA/BioProject lineage before freezing an execution subset;
- verify Lee SRP040309 exact run/file map;
- qualify candidate testbeds against the frozen P0-D eligibility contract without using expected SymC agreement as a selection criterion;
- keep `chi_bio`, `Chi_bio`, and Bio Chi admission closed until their respective prospective gates are satisfied.
